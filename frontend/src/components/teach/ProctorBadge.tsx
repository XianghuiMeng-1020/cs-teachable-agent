import { Shield, Lock, Camera, Clipboard, Brain, Eye, X } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

export function ProctorBadge() {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const protections = [
    { icon: Camera, label: t("teach.proctor.screenshot", { defaultValue: "Screenshot Protection" }), status: "ON" },
    { icon: Clipboard, label: t("teach.proctor.clipboard", { defaultValue: "Copy Protection" }), status: "ON" },
    { icon: Brain, label: t("teach.proctor.behavior", { defaultValue: "Behavior Analysis" }), status: "ON" },
    { icon: Eye, label: t("teach.proctor.focus", { defaultValue: "Focus Tracking" }), status: "ON" },
  ];

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setExpanded(false);
      }
    };
    if (expanded) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [expanded]);

  return (
    <div ref={containerRef} className="relative">
      <button
        onClick={() => setExpanded(!expanded)}
        className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border transition-all duration-200 ${
          expanded
            ? "bg-slate-800 text-white border-slate-700 shadow-md"
            : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100 hover:border-slate-300"
        }`}
      >
        <Lock className="w-3.5 h-3.5" />
        <span className="text-xs font-medium">
          {t("teach.proctor.badge", { defaultValue: "Secure" })}
        </span>
        <Shield className={`w-3 h-3 ml-0.5 ${expanded ? "text-emerald-400" : "text-emerald-500"}`} />
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.95 }}
            transition={{ duration: 0.15 }}
            className="absolute top-full right-0 mt-2 w-56 bg-white rounded-xl shadow-2xl border border-slate-200 overflow-hidden z-50"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-lg bg-slate-800 flex items-center justify-center">
                  <Shield className="w-3.5 h-3.5 text-white" />
                </div>
                <span className="text-xs font-semibold text-slate-700">
                  {t("teach.proctor.active", { defaultValue: "Active Protections" })}
                </span>
              </div>
              <button
                onClick={() => setExpanded(false)}
                className="p-1 rounded-lg hover:bg-slate-200 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Protection list */}
            <div className="p-2">
              {protections.map(({ icon: Icon, label, status }) => (
                <div 
                  key={label} 
                  className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-slate-50 transition-colors"
                >
                  <div className="w-7 h-7 rounded-lg bg-emerald-50 flex items-center justify-center shrink-0">
                    <Icon className="w-3.5 h-3.5 text-emerald-600" />
                  </div>
                  <span className="text-xs text-slate-600 font-medium flex-1">{label}</span>
                  <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700">
                    {status}
                  </span>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="px-4 py-2 bg-slate-50 border-t border-slate-100">
              <p className="text-[10px] text-slate-500 text-center">
                These protections help maintain assessment integrity
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
