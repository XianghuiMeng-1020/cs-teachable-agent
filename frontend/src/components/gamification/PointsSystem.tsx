import { Trophy, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

interface PointsSystemProps {
  points: number;
  level: number;
  className?: string;
}

export function PointsSystem({ points, level, className }: PointsSystemProps) {
  const nextLevelAt = level * 50;
  const prevLevelAt = (level - 1) * 50;
  const progress = level <= 1 ? points / 50 : (points - prevLevelAt) / (nextLevelAt - prevLevelAt);
  const progressPct = Math.min(100, Math.round(progress * 100));

  return (
    <div className={cn("rounded-xl border border-slate-200 bg-gradient-to-br from-amber-50/80 to-orange-50/50 p-4", className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="rounded-lg bg-amber-100 p-2">
            <Zap className="h-5 w-5 text-amber-600" />
          </div>
          <div>
            <p className="text-2xl font-bold text-slate-900">{points}</p>
            <p className="text-xs text-slate-500">Points</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Trophy className="h-5 w-5 text-amber-500" />
          <span className="text-lg font-semibold text-slate-800">Level {level}</span>
        </div>
      </div>
      <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-amber-500 transition-all"
          style={{ width: `${progressPct}%` }}
        />
      </div>
      <p className="mt-1 text-xs text-slate-500">
        {level <= 1 ? `${50 - points} pts to level 2` : `${nextLevelAt - points} pts to level ${level + 1}`}
      </p>
    </div>
  );
}
