import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

interface MasteryBarProps {
  percent: number;
  className?: string;
  showLabel?: boolean;
}

const MASTERY_THRESHOLD = 80;

function getFillColor(pct: number): string {
  if (pct >= MASTERY_THRESHOLD) return "bg-emerald-500";
  if (pct >= 60) return "bg-amber-500";
  if (pct >= 40) return "bg-orange-500";
  return "bg-red-500";
}

export function MasteryBar({ percent, className = "", showLabel = true }: MasteryBarProps) {
  const { t } = useTranslation();
  const clamped = Math.max(0, Math.min(100, Math.round(percent)));
  const isMastered = clamped >= MASTERY_THRESHOLD;
  const fillColor = getFillColor(clamped);

  return (
    <div className={`flex flex-col gap-1 ${className}`}>
      <div className="flex items-center justify-between gap-2">
        {showLabel && (
          <span className="text-xs font-medium text-stone-500">
            {t("teach.mastery", { defaultValue: "Mastery" })}
          </span>
        )}
        <motion.span
          key={clamped}
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className={`text-xs font-bold ${isMastered ? "text-emerald-600" : "text-stone-600"}`}
        >
          {clamped}%
          {isMastered && (
            <span className="ml-1 text-[10px] font-normal text-emerald-500">
              ✓ {t("teach.mastered", { defaultValue: "Mastered" })}
            </span>
          )}
        </motion.span>
      </div>

      {/* Progress bar track */}
      <div className="relative h-2 bg-stone-200 rounded-full overflow-hidden">
        {/* Fill */}
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${clamped}%` }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className={`absolute top-0 left-0 h-full rounded-full ${fillColor}`}
        />
        {/* Threshold marker */}
        <div
          className="absolute top-0 bottom-0 w-0.5 bg-stone-400/50"
          style={{ left: `${MASTERY_THRESHOLD}%` }}
        >
          {/* Marker tooltip */}
          <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-[8px] text-stone-400 whitespace-nowrap">
            80%
          </div>
        </div>
      </div>
    </div>
  );
}

// Re-export old component name for backward compatibility
export { MasteryBar as MasteryThermometer };
