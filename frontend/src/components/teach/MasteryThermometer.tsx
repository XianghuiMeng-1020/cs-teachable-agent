import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

interface MasteryThermometerProps {
  percent: number;
  label?: string;
  className?: string;
}

const TICKS = [0, 20, 40, 60, 80, 100];
const MASTERY_THRESHOLD = 80;

function getFillColor(pct: number): string {
  if (pct >= 80) return "from-emerald-400 to-emerald-600";
  if (pct >= 60) return "from-yellow-400 to-amber-500";
  if (pct >= 40) return "from-orange-400 to-orange-500";
  return "from-red-400 to-red-500";
}

export function MasteryThermometer({ percent, label, className = "" }: MasteryThermometerProps) {
  const { t } = useTranslation();
  const clamped = Math.max(0, Math.min(100, Math.round(percent)));

  return (
    <div className={`flex items-stretch gap-3 ${className}`}>
      {/* Thermometer column */}
      <div className="relative flex flex-col items-center w-12 shrink-0">
        {/* Tube */}
        <div className="relative w-6 flex-1 rounded-t-full bg-stone-200 overflow-hidden min-h-[140px]">
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: `${clamped}%` }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t ${getFillColor(clamped)} rounded-t-full`}
          />
          {/* Threshold line */}
          <div
            className="absolute left-0 right-0 border-t-2 border-dashed border-stone-600/50"
            style={{ bottom: `${MASTERY_THRESHOLD}%` }}
          />
        </div>
        {/* Bulb */}
        <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${getFillColor(clamped)} shadow-md flex items-center justify-center -mt-1 z-10`}>
          <span className="text-[10px] font-bold text-white">{clamped}%</span>
        </div>
      </div>

      {/* Tick labels */}
      <div className="relative flex-1 min-h-[140px] flex flex-col justify-between py-1">
        {[...TICKS].reverse().map((tick) => (
          <div key={tick} className="flex items-center gap-1.5">
            <div className={`w-3 h-px ${tick === MASTERY_THRESHOLD ? "bg-stone-700" : "bg-stone-300"}`} />
            <span className={`text-[10px] leading-none ${tick === MASTERY_THRESHOLD ? "font-semibold text-stone-800" : "text-stone-400"}`}>
              {tick}%{tick === MASTERY_THRESHOLD ? " ✓" : ""}
            </span>
          </div>
        ))}
      </div>

      {/* Info */}
      <div className="flex flex-col justify-end gap-1 pb-2">
        <span className="text-xs font-medium text-stone-500">
          {label ?? t("teach.mastery", { defaultValue: "Mastery" })}
        </span>
        {clamped >= MASTERY_THRESHOLD && (
          <motion.span
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-xs font-bold text-emerald-600"
          >
            {t("teach.mastered", { defaultValue: "Mastered!" })}
          </motion.span>
        )}
      </div>
    </div>
  );
}
