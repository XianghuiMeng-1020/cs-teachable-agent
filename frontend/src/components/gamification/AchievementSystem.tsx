import { Award, Lock } from "lucide-react";
import { cn } from "@/lib/utils";
import type { GamificationAchievement } from "@/api/client";

interface AchievementSystemProps {
  achievements: GamificationAchievement[];
  className?: string;
}

export function AchievementSystem({ achievements, className }: AchievementSystemProps) {
  if (achievements.length === 0) {
    return (
      <div className={cn("rounded-xl border border-stone-200 bg-stone-50/50 p-4", className)}>
        <h3 className="flex items-center gap-2 text-sm font-semibold text-stone-700">
          <Award className="h-4 w-4 text-stone-500" />
          Achievements
        </h3>
        <p className="mt-2 text-xs text-stone-500">Teach and pass tests to unlock badges.</p>
      </div>
    );
  }
  return (
    <div className={cn("rounded-xl border border-stone-200 bg-white p-4", className)}>
      <h3 className="flex items-center gap-2 text-sm font-semibold text-stone-800">
        <Award className="h-4 w-4 text-amber-500" />
        Achievements
      </h3>
      <ul className="mt-3 space-y-2">
        {achievements.map((a) => (
          <li
            key={a.id}
            className={cn(
              "flex items-center gap-3 rounded-lg border px-3 py-2",
              a.unlocked ? "border-amber-200 bg-amber-50/50" : "border-stone-100 bg-stone-50/50"
            )}
          >
            {a.unlocked ? (
              <Award className="h-5 w-5 shrink-0 text-amber-500" />
            ) : (
              <Lock className="h-5 w-5 shrink-0 text-stone-300" />
            )}
            <div className="min-w-0 flex-1">
              <p className={cn("text-sm font-medium", a.unlocked ? "text-stone-900" : "text-stone-500")}>
                {a.name}
              </p>
              <p className="text-xs text-stone-500">{a.description}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
