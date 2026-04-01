import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { Lock, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { emitTelemetry } from "@/lib/telemetry";
import { getAdminConfig } from "@/api/admin";

export interface FocusLossEvent {
  timestamp: string;
  reason: "window-blur" | "tab-hidden" | "devtools";
}

interface AntiCheatShellProps {
  children: ReactNode;
  enabled?: boolean;
  onFocusLost?: (event: FocusLossEvent) => void;
  onResume?: () => void;
}

function shouldBypassClipboardLock(target: EventTarget | null): boolean {
  let el = target as HTMLElement | null;
  while (el) {
    if (el.dataset?.allowClipboard === "true") return true;
    el = el.parentElement;
  }
  return false;
}

function formatTime(iso: string): string {
  try {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  } catch {
    return iso;
  }
}

const DEVTOOLS_THRESHOLD = 160;

export function AntiCheatShell({
  children,
  enabled = true,
  onFocusLost,
  onResume,
}: AntiCheatShellProps) {
  const [practiceLocked, setPracticeLocked] = useState(false);
  const [focusEvents, setFocusEvents] = useState<FocusLossEvent[]>([]);
  const lastFocusEventRef = useRef(0);
  const devtoolsDetected = useRef(false);
  const [devtoolsEnabled, setDevtoolsEnabled] = useState(true);

  useEffect(() => {
    getAdminConfig()
      .then((cfg) => {
        if (typeof cfg.devtools_detection_enabled === "boolean")
          setDevtoolsEnabled(cfg.devtools_detection_enabled);
      })
      .catch(() => {});
  }, []);

  const recordFocusLoss = useCallback(
    (reason: FocusLossEvent["reason"]) => {
      if (!enabled) return;
      const now = Date.now();
      if (now - lastFocusEventRef.current < 500) return;
      lastFocusEventRef.current = now;

      setPracticeLocked(true);
      const event: FocusLossEvent = {
        timestamp: new Date().toISOString(),
        reason,
      };
      setFocusEvents((prev) => [event, ...prev].slice(0, 12));
      onFocusLost?.(event);
    },
    [enabled, onFocusLost]
  );

  useEffect(() => {
    if (!enabled) return;

    function handleVisibilityChange() {
      if (document.visibilityState === "hidden") {
        recordFocusLoss("tab-hidden");
      }
    }
    function handleWindowBlur() {
      recordFocusLoss("window-blur");
    }

    window.addEventListener("blur", handleWindowBlur);
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => {
      window.removeEventListener("blur", handleWindowBlur);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [enabled, recordFocusLoss]);

  // DevTools detection via window size differential
  useEffect(() => {
    if (!enabled || !devtoolsEnabled) return;

    const check = () => {
      const widthDiff = window.outerWidth - window.innerWidth;
      const heightDiff = window.outerHeight - window.innerHeight;
      const isOpen = widthDiff > DEVTOOLS_THRESHOLD || heightDiff > DEVTOOLS_THRESHOLD;

      if (isOpen && !devtoolsDetected.current) {
        devtoolsDetected.current = true;
        emitTelemetry("devtools_opened", { widthDiff, heightDiff });
        recordFocusLoss("devtools");
      } else if (!isOpen) {
        devtoolsDetected.current = false;
      }
    };

    const interval = setInterval(check, 1000);
    return () => clearInterval(interval);
  }, [enabled, devtoolsEnabled, recordFocusLoss]);

  const handleResume = () => {
    setPracticeLocked(false);
    onResume?.();
  };

  const handleCopy = (e: React.ClipboardEvent) => {
    if (!enabled) return;
    if (shouldBypassClipboardLock(e.target)) return;
    e.preventDefault();
    emitTelemetry("content_copied");
  };
  const handleCut = (e: React.ClipboardEvent) => {
    if (!enabled) return;
    if (shouldBypassClipboardLock(e.target)) return;
    e.preventDefault();
  };
  const handlePaste = (e: React.ClipboardEvent) => {
    if (!enabled) return;
    if (shouldBypassClipboardLock(e.target)) return;
    e.preventDefault();
    emitTelemetry("paste_blocked", { source: "clipboard" });
  };
  const handleContextMenu = (e: React.MouseEvent) => {
    if (!enabled) return;
    if (shouldBypassClipboardLock(e.target)) return;
    e.preventDefault();
  };

  return (
    <div
      className={enabled ? "anti-cheat-shell" : ""}
      onCopy={handleCopy}
      onCut={handleCut}
      onPaste={handlePaste}
      onContextMenu={handleContextMenu}
    >
      <div className="relative">
        <div
          className="transition-all duration-150"
          style={
            practiceLocked
              ? { filter: "blur(10px)", pointerEvents: "none" }
              : undefined
          }
        >
          {children}
        </div>

        {practiceLocked && (
          <PracticeLockOverlay
            eventCount={focusEvents.length}
            latestEvent={focusEvents[0] ?? null}
            onResume={handleResume}
          />
        )}
      </div>
    </div>
  );
}

// ── Typing cadence hook ─────────────────────────────────────────────

/**
 * Hook to detect paste-like typing speed.
 * Returns a ref callback to attach to input `onInput`.
 * If > `charThreshold` characters appear within `timeWindowMs`,
 * a `typing_anomaly` telemetry event is emitted.
 */
export function useTypingCadence(
  charThreshold = 20,
  timeWindowMs = 500
) {
  const bufferRef = useRef<{ ts: number; len: number }[]>([]);

  const onInput = useCallback(
    (e: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const val = (e.target as HTMLInputElement).value;
      const now = Date.now();
      bufferRef.current.push({ ts: now, len: val.length });

      // Keep only events within time window
      bufferRef.current = bufferRef.current.filter(
        (b) => now - b.ts <= timeWindowMs
      );

      if (bufferRef.current.length >= 2) {
        const first = bufferRef.current[0];
        const last = bufferRef.current[bufferRef.current.length - 1];
        const charDelta = last.len - first.len;
        if (charDelta >= charThreshold) {
          emitTelemetry("typing_anomaly", {
            charDelta,
            timeSpanMs: last.ts - first.ts,
          });
          bufferRef.current = [];
        }
      }
    },
    [charThreshold, timeWindowMs]
  );

  return onInput;
}

// ── Lock Overlay ────────────────────────────────────────────────────

function PracticeLockOverlay({
  eventCount,
  latestEvent,
  onResume,
}: {
  eventCount: number;
  latestEvent: FocusLossEvent | null;
  onResume: () => void;
}) {
  const { t } = useTranslation();

  const reasonLabel = (r: FocusLossEvent["reason"]) => {
    if (r === "tab-hidden") return t("assessment.tabHidden");
    if (r === "devtools") return t("assessment.devToolsDetected");
    return t("assessment.windowBlur");
  };

  return (
    <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-white/70 backdrop-blur-md">
      <div className="w-full max-w-md rounded-2xl border border-stone-200 bg-white p-6 shadow-elevated">
        <div className="flex items-center gap-2 text-stone-900">
          <Lock className="h-5 w-5 text-brand-700" />
          <h3 className="font-serif text-lg font-semibold">{t("assessment.locked")}</h3>
        </div>
        <p className="mt-2 text-sm leading-relaxed text-stone-500">
          {t("assessment.lockedDesc")}
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="inline-flex items-center gap-1 rounded-full border border-amber-200 bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-800">
            <AlertTriangle className="h-3 w-3" />
            {t("assessment.focusEvents", { count: eventCount })}
          </span>
          {latestEvent && (
            <span className="rounded-full border border-stone-200 bg-stone-50 px-2.5 py-1 text-xs text-stone-600">
              {reasonLabel(latestEvent.reason)} · {formatTime(latestEvent.timestamp)}
            </span>
          )}
        </div>
        <div className="mt-5">
          <Button onClick={onResume}>{t("assessment.resumePractice")}</Button>
        </div>
      </div>
    </div>
  );
}
