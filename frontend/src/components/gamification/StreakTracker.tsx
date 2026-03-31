import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Flame,
  Snowflake,
  Trophy,
  Calendar,
  Clock,
  Zap,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  ChevronRight,
  Award,
  Target,
  RotateCcw,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";

interface StreakDay {
  date: string;
  day_name: string;
  is_today: boolean;
  was_active: boolean;
  activity_count: number;
  learning_time: number;
}

interface StreakWeek {
  week: number;
  days: StreakDay[];
}

interface StreakSummary {
  current_streak: number;
  longest_streak: number;
  freezes_remaining: number;
  next_milestone: {
    name: string | null;
    days_required: number | null;
    days_to_go: number | null;
  };
  risk_assessment: {
    risk_level: string;
    days_until_break: number | null;
    message: string;
    recommendation: string;
  };
  is_active_today: boolean;
}

interface StreakTrackerProps {
  userId?: number;
  compact?: boolean;
}

const MILESTONE_ICONS: Record<string, string> = {
  "Getting Started": "🔥",
  "Week Warrior": "⚡",
  "Two Week Wonder": "🌟",
  "21-Day Habit": "🎯",
  "Monthly Master": "🏆",
  "Double Month": "💎",
  "Century Club": "👑",
  "Year of Growth": "🌈",
};

export function StreakTracker({ userId, compact = false }: StreakTrackerProps) {
  const [showDetails, setShowDetails] = useState(false);

  const { data: summary, isLoading: loadingSummary } = useQuery<StreakSummary>({
    queryKey: ["streak", "summary", userId],
    queryFn: async () => {
      // Mock data for now - would be API call
      return {
        current_streak: 7,
        longest_streak: 14,
        freezes_remaining: 2,
        next_milestone: {
          name: "Week Warrior",
          days_required: 7,
          days_to_go: 0,
        },
        risk_assessment: {
          risk_level: "none",
          days_until_break: 1,
          message: "Streak safe - active today",
          recommendation: "Great job! Come back tomorrow to continue.",
        },
        is_active_today: true,
      };
    },
  });

  const { data: calendar, isLoading: loadingCalendar } = useQuery<StreakWeek[]>({
    queryKey: ["streak", "calendar", userId],
    queryFn: async () => {
      // Generate mock calendar
      const weeks: StreakWeek[] = [];
      const today = new Date();
      
      for (let w = 0; w < 4; w++) {
        const days: StreakDay[] = [];
        for (let d = 6; d >= 0; d--) {
          const date = new Date(today);
          date.setDate(date.getDate() - (w * 7 + d));
          
          days.push({
            date: date.toISOString().split("T")[0],
            day_name: date.toLocaleDateString("en", { weekday: "narrow" }),
            is_today: d === 0 && w === 0,
            was_active: Math.random() > 0.3, // Random for demo
            activity_count: Math.floor(Math.random() * 5),
            learning_time: Math.floor(Math.random() * 60),
          });
        }
        weeks.push({ week: w, days });
      }
      
      return weeks;
    },
  });

  if (loadingSummary || !summary) {
    return (
      <Card padding="md" className="animate-pulse">
        <div className="h-20 bg-stone-100 rounded" />
      </Card>
    );
  }

  const { current_streak, longest_streak, freezes_remaining, next_milestone, risk_assessment, is_active_today } = summary;
  const daysToNext = next_milestone.days_to_go || 0;

  // Compact view
  if (compact) {
    return (
      <Card padding="md" className="overflow-hidden">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={cn(
              "w-12 h-12 rounded-full flex items-center justify-center",
              is_active_today ? "bg-orange-100" : "bg-stone-100"
            )}>
              <Flame className={cn(
                "w-6 h-6",
                is_active_today ? "text-orange-500" : "text-stone-400"
              )} />
            </div>
            <div>
              <div className="flex items-baseline gap-1">
                <span className="text-2xl font-bold text-stone-900">{current_streak}</span>
                <span className="text-sm text-stone-500">day streak</span>
              </div>
              <p className="text-xs text-stone-500">
                Best: {longest_streak} days
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            {freezes_remaining > 0 && (
              <div className="flex items-center gap-1 text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                <Snowflake className="w-3 h-3" />
                <span>{freezes_remaining}</span>
              </div>
            )}
            {daysToNext > 0 ? (
              <div className="text-xs text-stone-500">
                {daysToNext} days to {next_milestone.name}
              </div>
            ) : next_milestone.name && (
              <div className="flex items-center gap-1 text-xs text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
                <Trophy className="w-3 h-3" />
                <span>{next_milestone.name}!</span>
              </div>
            )}
          </div>
        </div>

        {/* Mini calendar */}
        {calendar && (
          <div className="mt-3 pt-3 border-t border-stone-100">
            <div className="flex justify-between">
              {calendar[0]?.days.slice(-7).map((day, i) => (
                <div
                  key={i}
                  className={cn(
                    "w-8 h-8 rounded-full flex items-center justify-center text-xs",
                    day.is_today
                      ? "bg-brand-500 text-white ring-2 ring-brand-300"
                      : day.was_active
                      ? "bg-orange-100 text-orange-600"
                      : "bg-stone-100 text-stone-400"
                  )}
                  title={day.date}
                >
                  {day.day_name}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Risk indicator */}
        {risk_assessment.risk_level !== "none" && risk_assessment.risk_level !== "broken" && (
          <div className={cn(
            "mt-3 p-2 rounded-lg flex items-center gap-2 text-xs",
            risk_assessment.risk_level === "high"
              ? "bg-rose-50 text-rose-700"
              : "bg-amber-50 text-amber-700"
          )}>
            <AlertCircle className="w-4 h-4" />
            <span>{risk_assessment.message}</span>
          </div>
        )}
      </Card>
    );
  }

  // Full view
  return (
    <Card padding="lg">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className={cn(
            "w-16 h-16 rounded-2xl flex items-center justify-center",
            is_active_today ? "bg-gradient-to-br from-orange-400 to-red-500" : "bg-stone-100"
          )}>
            <Flame className={cn(
              "w-8 h-8",
              is_active_today ? "text-white" : "text-stone-400"
            )} />
          </div>
          <div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-stone-900">{current_streak}</span>
              <span className="text-lg text-stone-500">day streak</span>
            </div>
            <p className="text-sm text-stone-500">
              Longest: {longest_streak} days
              {freezes_remaining > 0 && (
                <span className="ml-2 text-blue-600">
                  • {freezes_remaining} freeze{freezes_remaining > 1 ? "s" : ""} remaining
                </span>
              )}
            </p>
          </div>
        </div>

        {next_milestone.name && (
          <div className="text-right">
            <p className="text-sm text-stone-500">Next milestone</p>
            <p className="text-lg font-semibold text-stone-900 flex items-center gap-2">
              {MILESTONE_ICONS[next_milestone.name] || "🏆"} {next_milestone.name}
            </p>
            {daysToNext > 0 && (
              <p className="text-xs text-stone-500">
                {daysToNext} day{daysToNext > 1 ? "s" : ""} to go
              </p>
            )}
          </div>
        )}
      </div>

      {/* Progress to next milestone */}
      {next_milestone.days_required && next_milestone.days_required > current_streak && (
        <div className="mb-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-stone-600">Progress to {next_milestone.name}</span>
            <span className="font-medium text-stone-900">
              {current_streak} / {next_milestone.days_required} days
            </span>
          </div>
          <ProgressBar
            value={(current_streak / next_milestone.days_required) * 100}
            className="h-3"
            color="orange"
          />
        </div>
      )}

      {/* Calendar Grid */}
      {calendar && (
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-3">
            <Calendar className="w-4 h-4 text-stone-400" />
            <span className="text-sm font-medium text-stone-700">Last 4 weeks</span>
          </div>
          <div className="space-y-2">
            {calendar.map((week, widx) => (
              <div key={widx} className="flex gap-1">
                {week.days.map((day, didx) => (
                  <div
                    key={didx}
                    className={cn(
                      "w-10 h-10 rounded-lg flex items-center justify-center text-sm font-medium transition-all",
                      day.is_today
                        ? "bg-brand-500 text-white ring-2 ring-brand-300"
                        : day.was_active
                        ? "bg-gradient-to-br from-orange-400 to-orange-500 text-white"
                        : "bg-stone-100 text-stone-400"
                    )}
                    title={`${day.date}: ${day.was_active ? `${day.activity_count} activities, ${day.learning_time} min` : "No activity"}`}
                  >
                    {new Date(day.date).getDate()}
                  </div>
                ))}
              </div>
            ))}
          </div>
          <div className="flex items-center gap-4 mt-3 text-xs text-stone-500">
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-gradient-to-br from-orange-400 to-orange-500 rounded" />
              <span>Active</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-brand-500 rounded" />
              <span>Today</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-3 h-3 bg-stone-100 rounded" />
              <span>Inactive</span>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="p-3 bg-stone-50 rounded-xl text-center">
          <Clock className="w-5 h-5 text-stone-400 mx-auto mb-1" />
          <p className="text-lg font-semibold text-stone-900">12.5h</p>
          <p className="text-xs text-stone-500">Total learning time</p>
        </div>
        <div className="p-3 bg-stone-50 rounded-xl text-center">
          <Zap className="w-5 h-5 text-stone-400 mx-auto mb-1" />
          <p className="text-lg font-semibold text-stone-900">42</p>
          <p className="text-xs text-stone-500">Activities completed</p>
        </div>
        <div className="p-3 bg-stone-50 rounded-xl text-center">
          <Target className="w-5 h-5 text-stone-400 mx-auto mb-1" />
          <p className="text-lg font-semibold text-stone-900">85%</p>
          <p className="text-xs text-stone-500">Consistency score</p>
        </div>
      </div>

      {/* Achieved Milestones */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Award className="w-4 h-4 text-stone-400" />
          <span className="text-sm font-medium text-stone-700">Milestones achieved</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {["Getting Started", "Week Warrior"].map((milestone) => (
            <div
              key={milestone}
              className="flex items-center gap-2 px-3 py-1.5 bg-gradient-to-r from-amber-50 to-orange-50 border border-orange-200 rounded-full"
            >
              <span>{MILESTONE_ICONS[milestone]}</span>
              <span className="text-sm text-orange-800">{milestone}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Risk warning */}
      {risk_assessment.risk_level !== "none" && risk_assessment.risk_level !== "broken" && (
        <div className={cn(
          "mt-6 p-4 rounded-xl flex items-start gap-3",
          risk_assessment.risk_level === "high"
            ? "bg-rose-50 border border-rose-200"
            : "bg-amber-50 border border-amber-200"
        )}>
          <AlertCircle className={cn(
            "w-5 h-5 shrink-0",
            risk_assessment.risk_level === "high" ? "text-rose-600" : "text-amber-600"
          )} />
          <div>
            <p className={cn(
              "font-medium",
              risk_assessment.risk_level === "high" ? "text-rose-900" : "text-amber-900"
            )}>
              {risk_assessment.message}
            </p>
            <p className={cn(
              "text-sm mt-1",
              risk_assessment.risk_level === "high" ? "text-rose-700" : "text-amber-700"
            )}>
              {risk_assessment.recommendation}
            </p>
            <Button
              size="sm"
              variant="primary"
              className="mt-2"
              onClick={() => {
                // Navigate to teach page
                window.location.href = "/teach";
              }}
            >
              Start Learning Now
            </Button>
          </div>
        </div>
      )}

      {/* Success state */}
      {is_active_today && risk_assessment.risk_level === "none" && (
        <div className="mt-6 p-4 bg-emerald-50 rounded-xl border border-emerald-200 flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
          <div>
            <p className="font-medium text-emerald-900">Great job today!</p>
            <p className="text-sm text-emerald-700 mt-1">
              You've maintained your streak. Come back tomorrow to keep it going!
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}
