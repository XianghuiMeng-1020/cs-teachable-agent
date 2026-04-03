import { Shield, Camera, Clipboard, Brain, Eye } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useState } from "react";

export function ProctorBadge() {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);

  const protections = [
    { icon: Camera, label: t("teach.proctor.screenshot", { defaultValue: "Screenshot Protection" }) },
    { icon: Clipboard, label: t("teach.proctor.clipboard", { defaultValue: "Copy Protection" }) },
    { icon: Brain, label: t("teach.proctor.behavior", { defaultValue: "Behavior Analysis" }) },
    { icon: Eye, label: t("teach.proctor.focus", { defaultValue: "Focus Tracking" }) },
  ];

  return (
    <div className="relative">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-rose-50 border border-rose-200 text-rose-700 hover:bg-rose-100 transition-colors"
      >
        <Shield className="w-3.5 h-3.5" />
        <span className="text-[10px] font-semibold uppercase tracking-wide">
          {t("teach.proctor.badge", { defaultValue: "Proctored" })}
        </span>
      </button>

      {expanded && (
        <div className="absolute top-full right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-stone-200 p-2 z-50">
          <p className="text-[10px] text-stone-500 font-medium mb-1.5 px-1">
            {t("teach.proctor.active", { defaultValue: "Active Protections" })}
          </p>
          {protections.map(({ icon: Icon, label }) => (
            <div key={label} className="flex items-center gap-2 px-1 py-1">
              <Icon className="w-3 h-3 text-emerald-500" />
              <span className="text-[11px] text-stone-700">{label}</span>
              <span className="ml-auto text-[9px] text-emerald-600 font-medium">ON</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
