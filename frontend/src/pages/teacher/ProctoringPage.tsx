import { useTranslation } from "react-i18next";
import { useCallback, useEffect, useState } from "react";
import {
  Shield,
  Eye,
  Fingerprint,
  Monitor,
  Printer,
  Keyboard,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  Settings2,
  Users,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import {
  getAdminConfig,
  updateAdminConfig,
  getFlags,
  resolveFlag,
  getFlagSummary,
  type AdminSettings,
  type StudentFlagItem,
  type FlagSummaryStudent,
} from "@/api/admin";
import { cn } from "@/lib/utils";

// ── Severity helpers ────────────────────────────────────────────────

const SEVERITY_STYLE: Record<string, { bg: string; text: string; border: string; icon: React.ElementType }> = {
  critical: { bg: "bg-red-50", text: "text-red-700", border: "border-red-200", icon: XCircle },
  warning: { bg: "bg-amber-50", text: "text-amber-700", border: "border-amber-200", icon: AlertTriangle },
  info: { bg: "bg-sky-50", text: "text-sky-700", border: "border-sky-200", icon: Eye },
};

const FLAG_TYPE_DEFAULTS: Record<string, string> = {
  focus_loss_excess: "Excessive Focus Loss",
  rapid_solve: "Suspiciously Fast Solve",
  paste_attempt: "Paste Blocked",
  typing_anomaly: "Typing Anomaly",
  devtools_opened: "DevTools Detected",
  manual: "Manual Flag",
};

function formatTs(ts: string | null): string {
  if (!ts) return "—";
  try {
    return new Date(ts).toLocaleString([], {
      month: "short", day: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

function flagTypeLabel(flagType: string, t: (key: string, opts?: { defaultValue?: string }) => string): string {
  return t(`teacher.flagType.${flagType}`, { defaultValue: FLAG_TYPE_DEFAULTS[flagType] ?? flagType });
}

// ── Settings Panel ──────────────────────────────────────────────────

function SettingsPanel({
  settings,
  saving,
  onUpdate,
}: {
  settings: AdminSettings;
  saving: boolean;
  onUpdate: (patch: Partial<AdminSettings>) => void;
}) {
  const { t } = useTranslation();
  const toggleRow = (key: keyof AdminSettings, labelKey: string, labelDefault: string, icon: React.ElementType, descKey: string, descDefault: string) => {
    const Icon = icon;
    const val = !!settings[key];
    return (
      <div className="flex items-center justify-between py-3 border-b border-stone-100 last:border-b-0">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-stone-100">
            <Icon className="h-4 w-4 text-stone-600" />
          </div>
          <div>
            <p className="text-sm font-medium text-stone-800">{t(labelKey, { defaultValue: labelDefault })}</p>
            <p className="text-xs text-stone-500">{t(descKey, { defaultValue: descDefault })}</p>
          </div>
        </div>
        <button
          type="button"
          role="switch"
          aria-checked={val}
          onClick={() => onUpdate({ [key]: !val })}
          className={cn(
            "relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200",
            val ? "bg-brand-600" : "bg-stone-200"
          )}
        >
          <span className={cn(
            "pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition-transform duration-200",
            val ? "translate-x-5" : "translate-x-0"
          )} />
        </button>
      </div>
    );
  };

  return (
    <Card padding="lg">
      <div className="flex items-center gap-2 mb-4">
        <Settings2 className="h-5 w-5 text-brand-700" />
        <h2 className="font-serif text-lg font-semibold text-stone-900">{t("teacher.configTitle")}</h2>
        {saving && <span className="ml-auto text-xs text-brand-600 animate-pulse">{t("teacher.savingConfig", { defaultValue: "Saving…" })}</span>}
      </div>

      {/* Hz slider */}
      <div className="mb-5 rounded-lg border border-stone-200 bg-stone-50/50 p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-stone-700">{t("teacher.antiCaptureFlickerRate", { defaultValue: "Anti-Capture Flicker Rate" })}</span>
          <span className="text-sm font-bold text-brand-700">{settings.anti_capture_hz} Hz</span>
        </div>
        <input
          type="range"
          min={20}
          max={60}
          step={1}
          value={settings.anti_capture_hz}
          onChange={(e) => onUpdate({ anti_capture_hz: Number(e.target.value) })}
          className="w-full h-1.5 rounded-full appearance-none bg-stone-200 accent-brand-700 cursor-pointer"
        />
        <div className="mt-1 flex justify-between text-[10px] text-stone-400">
          <span>{t("teacher.hzSubtle", { defaultValue: "20 Hz (subtle)" })}</span>
          <span>{t("teacher.hzStrong", { defaultValue: "60 Hz (strong)" })}</span>
        </div>
      </div>

      {/* Thresholds */}
      <div className="mb-5 grid grid-cols-2 gap-3">
        <div className="rounded-lg border border-stone-200 bg-stone-50/50 p-3">
          <label className="text-xs font-medium text-stone-600 block mb-1">{t("teacher.focusLossThreshold", { defaultValue: "Focus Loss Threshold" })}</label>
          <input
            type="number"
            min={1}
            max={50}
            value={settings.focus_loss_threshold}
            onChange={(e) => onUpdate({ focus_loss_threshold: Number(e.target.value) })}
            className="w-full rounded-md border border-stone-300 bg-white px-2.5 py-1.5 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20 focus:outline-none"
          />
          <p className="text-[10px] text-stone-400 mt-1">{t("teacher.focusLossThresholdHint", { defaultValue: "Auto-flag after N focus losses per session" })}</p>
        </div>
        <div className="rounded-lg border border-stone-200 bg-stone-50/50 p-3">
          <label className="text-xs font-medium text-stone-600 block mb-1">{t("teacher.minSolveTimeMs", { defaultValue: "Min Solve Time (ms)" })}</label>
          <input
            type="number"
            min={1000}
            max={120000}
            step={1000}
            value={settings.min_solve_time_ms}
            onChange={(e) => onUpdate({ min_solve_time_ms: Number(e.target.value) })}
            className="w-full rounded-md border border-stone-300 bg-white px-2.5 py-1.5 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500/20 focus:outline-none"
          />
          <p className="text-[10px] text-stone-400 mt-1">{t("teacher.minSolveTimeHint", { defaultValue: "Flag correct answers faster than this" })}</p>
        </div>
      </div>

      {/* Feature toggles */}
      <div>
        {toggleRow("anti_capture_enabled", "teacher.toggleAntiCapture", "Anti-Capture Overlay", Monitor, "teacher.toggleAntiCaptureDesc", "Camera-interference flickering pattern")}
        {toggleRow("devtools_detection_enabled", "teacher.toggleDevtools", "DevTools Detection", Eye, "teacher.toggleDevtoolsDesc", "Lock screen when browser dev tools open")}
        {toggleRow("typing_anomaly_enabled", "teacher.toggleTypingAnomaly", "Typing Anomaly Detection", Keyboard, "teacher.toggleTypingAnomalyDesc", "Flag paste-like typing speed")}
        {toggleRow("watermark_enabled", "teacher.toggleWatermark", "Invisible Watermarks", Fingerprint, "teacher.toggleWatermarkDesc", "Zero-width chars in code to corrupt AI prompts")}
        {toggleRow("print_block_enabled", "teacher.togglePrintBlock", "Print Blocking", Printer, "teacher.togglePrintBlockDesc", "Prevent print-to-PDF during assessment")}
        {toggleRow("ocr_noise_enabled", "teacher.toggleOcrNoise", "OCR Noise", Shield, "teacher.toggleOcrNoiseDesc", "Subtle visual transforms to hinder OCR")}
      </div>
    </Card>
  );
}

// ── Flag Table ──────────────────────────────────────────────────────

function FlagTable({
  flags,
  loading,
  onResolve,
  onRefresh,
  filter,
  onFilterChange,
}: {
  flags: StudentFlagItem[];
  loading: boolean;
  onResolve: (id: number) => void;
  onRefresh: () => void;
  filter: { resolved: boolean | null; severity: string | null };
  onFilterChange: (f: { resolved: boolean | null; severity: string | null }) => void;
}) {
  const { t } = useTranslation();
  const [expandedId, setExpandedId] = useState<number | null>(null);

  return (
    <Card padding="lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-amber-600" />
          <h2 className="font-serif text-lg font-semibold text-stone-900">{t("teacher.flaggedStudents")}</h2>
          <span className="ml-1 rounded-full bg-stone-100 px-2 py-0.5 text-xs font-medium text-stone-600">
            {flags.length}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={filter.resolved === null ? "all" : filter.resolved ? "resolved" : "unresolved"}
            onChange={(e) => {
              const v = e.target.value;
              onFilterChange({
                ...filter,
                resolved: v === "all" ? null : v === "resolved",
              });
            }}
            className="rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs focus:border-brand-500 focus:outline-none"
          >
            <option value="all">{t("history.all")}</option>
            <option value="unresolved">{t("teacher.pending")}</option>
            <option value="resolved">{t("teacher.resolved")}</option>
          </select>
          <select
            value={filter.severity ?? "all"}
            onChange={(e) =>
              onFilterChange({
                ...filter,
                severity: e.target.value === "all" ? null : e.target.value,
              })
            }
            className="rounded-lg border border-stone-300 bg-white px-2.5 py-1.5 text-xs focus:border-brand-500 focus:outline-none"
          >
            <option value="all">{t("teacher.allSeverity", { defaultValue: "All Severity" })}</option>
            <option value="critical">{t("teacher.severityCritical", { defaultValue: "Critical" })}</option>
            <option value="warning">{t("teacher.severityWarning", { defaultValue: "Warning" })}</option>
            <option value="info">{t("teacher.severityInfo", { defaultValue: "Info" })}</option>
          </select>
          <button
            type="button"
            onClick={onRefresh}
            title={t("teacher.refreshFlags")}
            aria-label={t("teacher.refreshFlags")}
            className="flex h-8 w-8 items-center justify-center rounded-lg border border-stone-200 bg-white text-stone-500 hover:bg-stone-50 transition-colors"
          >
            <RefreshCw className={cn("h-3.5 w-3.5", loading && "animate-spin")} />
          </button>
        </div>
      </div>

      {flags.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-stone-400">
          <CheckCircle2 className="h-10 w-10 mb-2" />
          <p className="text-sm">{t("teacher.noFlags")}</p>
        </div>
      ) : (
        <div className="space-y-2 max-h-[520px] overflow-y-auto pr-1">
          {flags.map((f) => {
            const sev = SEVERITY_STYLE[f.severity] ?? SEVERITY_STYLE.info;
            const SevIcon = sev.icon;
            const expanded = expandedId === f.id;
            return (
              <div
                key={f.id}
                className={cn(
                  "rounded-xl border transition-all duration-150",
                  f.resolved ? "border-stone-200 bg-stone-50/50" : `${sev.border} ${sev.bg}`
                )}
              >
                <button
                  type="button"
                  className="flex w-full items-center gap-3 px-4 py-3 text-left"
                  onClick={() => setExpandedId(expanded ? null : f.id)}
                >
                  <SevIcon className={cn("h-4 w-4 shrink-0", f.resolved ? "text-stone-400" : sev.text)} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className={cn("text-sm font-medium", f.resolved ? "text-stone-500 line-through" : "text-stone-800")}>
                        {f.username ?? t("teacher.userNumber", { id: f.user_id, defaultValue: "User #{{id}}" })}
                      </span>
                      <span className={cn(
                        "rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide",
                        f.resolved ? "bg-stone-200 text-stone-500" : `${sev.bg} ${sev.text}`
                      )}>
                        {flagTypeLabel(f.flag_type, t)}
                      </span>
                    </div>
                    <p className="text-[11px] text-stone-500 mt-0.5">{formatTs(f.created_at)}</p>
                  </div>
                  {expanded ? <ChevronUp className="h-4 w-4 text-stone-400" /> : <ChevronDown className="h-4 w-4 text-stone-400" />}
                </button>

                {expanded && (
                  <div className="px-4 pb-3 border-t border-stone-200/60 mt-1 pt-3">
                    {f.detail && (
                      <pre className="text-xs text-stone-600 bg-white/80 rounded-lg p-2 mb-2 overflow-x-auto font-mono whitespace-pre-wrap">
                        {JSON.stringify(f.detail, null, 2)}
                      </pre>
                    )}
                    {f.session_id && (
                      <p className="text-[11px] text-stone-500 mb-1">
                        {t("teacher.sessionLabel", { defaultValue: "Session" })}: <code className="font-mono">{f.session_id}</code>
                      </p>
                    )}
                    {f.item_id && (
                      <p className="text-[11px] text-stone-500 mb-2">
                        {t("teacher.itemIdLabel", { defaultValue: "Item ID" })}: {f.item_id}
                      </p>
                    )}
                    {!f.resolved && (
                      <Button
                        size="sm"
                        variant="secondary"
                        onClick={(e) => {
                          e.stopPropagation();
                          onResolve(f.id);
                        }}
                      >
                        <CheckCircle2 className="h-3.5 w-3.5" />
                        {t("teacher.resolve")}
                      </Button>
                    )}
                    {f.resolved && (
                      <p className="text-[11px] text-stone-400">
                        {t("teacher.resolved")}
                        {f.resolved_at ? ` ${t("teacher.resolvedOnDate", { date: formatTs(f.resolved_at), defaultValue: "on {{date}}" })}` : ""}
                        {f.resolved_by != null ? ` ${t("teacher.resolvedByUser", { userId: f.resolved_by, defaultValue: "by user #{{userId}}" })}` : ""}
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}

// ── Integrity Overview ──────────────────────────────────────────────

function IntegrityOverview({ students }: { students: FlagSummaryStudent[] }) {
  const { t } = useTranslation();
  if (students.length === 0) {
    return (
      <Card padding="lg">
        <div className="flex items-center gap-2 mb-4">
          <Users className="h-5 w-5 text-brand-700" />
          <h2 className="font-serif text-lg font-semibold text-stone-900">{t("teacher.flagSummary")}</h2>
        </div>
        <p className="text-sm text-stone-400 py-6 text-center">{t("teacher.noFlags")}</p>
      </Card>
    );
  }

  return (
    <Card padding="lg">
      <div className="flex items-center gap-2 mb-4">
        <Users className="h-5 w-5 text-brand-700" />
        <h2 className="font-serif text-lg font-semibold text-stone-900">{t("teacher.flagSummary")}</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-stone-200 text-[11px] font-semibold uppercase tracking-wider text-stone-400">
              <th className="py-2 pr-4">{t("teacher.studentName")}</th>
              <th className="py-2 px-3 text-center">{t("teacher.total")}</th>
              <th className="py-2 px-3 text-center">{t("teacher.unresolvedCount", { defaultValue: "Unresolved" })}</th>
              <th className="py-2 px-3 text-center">{t("teacher.severityCritical", { defaultValue: "Critical" })}</th>
              <th className="py-2 px-3 text-center">{t("teacher.severityWarning", { defaultValue: "Warning" })}</th>
              <th className="py-2 px-3 text-center">{t("teacher.severityInfo", { defaultValue: "Info" })}</th>
              <th className="py-2 pl-3">{t("teacher.latestFlag", { defaultValue: "Latest" })}</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.user_id} className="border-b border-stone-100 last:border-b-0 hover:bg-stone-50/60 transition-colors">
                <td className="py-2.5 pr-4 font-medium text-stone-800">{s.username}</td>
                <td className="py-2.5 px-3 text-center text-stone-600">{s.total_flags}</td>
                <td className="py-2.5 px-3 text-center">
                  <span className={cn(
                    "inline-block min-w-[1.5rem] rounded-full px-1.5 py-0.5 text-xs font-semibold text-center",
                    s.unresolved > 0 ? "bg-amber-100 text-amber-700" : "bg-stone-100 text-stone-400"
                  )}>{s.unresolved}</span>
                </td>
                <td className="py-2.5 px-3 text-center">
                  {s.critical > 0 ? (
                    <span className="inline-block min-w-[1.5rem] rounded-full bg-red-100 px-1.5 py-0.5 text-xs font-semibold text-red-700 text-center">{s.critical}</span>
                  ) : (
                    <span className="text-stone-300">—</span>
                  )}
                </td>
                <td className="py-2.5 px-3 text-center text-stone-600">{s.warning || "—"}</td>
                <td className="py-2.5 px-3 text-center text-stone-500">{s.info || "—"}</td>
                <td className="py-2.5 pl-3 text-xs text-stone-500">{formatTs(s.latest_flag_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

// ── Main Page ───────────────────────────────────────────────────────

export function ProctoringPage() {
  const { t } = useTranslation();
  const [settings, setSettings] = useState<AdminSettings | null>(null);
  const [flags, setFlags] = useState<StudentFlagItem[]>([]);
  const [summary, setSummary] = useState<FlagSummaryStudent[]>([]);
  const [saving, setSaving] = useState(false);
  const [loadingFlags, setLoadingFlags] = useState(true);
  const [filter, setFilter] = useState<{ resolved: boolean | null; severity: string | null }>({
    resolved: false,
    severity: null,
  });

  const loadSettings = useCallback(async () => {
    try {
      const cfg = await getAdminConfig();
      setSettings(cfg);
    } catch {}
  }, []);

  const loadFlags = useCallback(async () => {
    setLoadingFlags(true);
    try {
      const params: Record<string, unknown> = { limit: 200 };
      if (filter.resolved !== null) params.resolved = filter.resolved;
      if (filter.severity) params.severity = filter.severity;
      const res = await getFlags(params as Parameters<typeof getFlags>[0]);
      setFlags(res.flags);
    } catch {}
    setLoadingFlags(false);
  }, [filter]);

  const loadSummary = useCallback(async () => {
    try {
      const res = await getFlagSummary();
      setSummary(res.students);
    } catch {}
  }, []);

  useEffect(() => {
    loadSettings();
    loadFlags();
    loadSummary();
  }, [loadSettings, loadFlags, loadSummary]);

  const handleUpdateSettings = async (patch: Partial<AdminSettings>) => {
    if (!settings) return;
    const next = { ...settings, ...patch };
    setSettings(next);
    setSaving(true);
    try {
      const updated = await updateAdminConfig(patch);
      setSettings(updated);
    } catch {
      setSettings(settings);
    }
    setSaving(false);
  };

  const handleResolve = async (flagId: number) => {
    try {
      await resolveFlag(flagId);
      loadFlags();
      loadSummary();
    } catch {}
  };

  if (!settings) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-brand-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-serif text-display-sm text-stone-900">{t("teacher.proctoringTitle")}</h1>
        <p className="mt-1 text-stone-500">{t("teacher.proctoringDesc")}</p>
      </div>
      <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
        <SettingsPanel settings={settings} saving={saving} onUpdate={handleUpdateSettings} />
        <FlagTable
          flags={flags}
          loading={loadingFlags}
          onResolve={handleResolve}
          onRefresh={() => { loadFlags(); loadSummary(); }}
          filter={filter}
          onFilterChange={setFilter}
        />
      </div>
      <IntegrityOverview students={summary} />
    </div>
  );
}
