import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Brain,
  Clock,
  TrendingUp,
  Calendar,
  CheckCircle,
  XCircle,
  AlertCircle,
  ChevronRight,
  RotateCw,
  Zap,
  BarChart3,
  Target,
  BookOpen,
  Award,
  ArrowRight,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
} from "recharts";

interface ReviewItem {
  unit_id: string;
  unit_name: string;
  ease_factor: number;
  interval_days: number;
  repetitions: number;
  last_reviewed: string | null;
  next_review: string | null;
  total_reviews: number;
  successful_reviews: number;
  average_rating: number;
  forgetting_rate: number;
}

interface RetentionStats {
  total_scheduled: number;
  due_now: number;
  up_to_date: number;
  average_ease_factor: number;
  average_interval_days: number;
  predicted_retention: Record<string, number>;
  repetition_distribution: Record<string, number>;
  retention_health: string;
}

interface SpacedRepetitionPanelProps {
  taId: number;
}

const RATING_OPTIONS = [
  { value: 1, label: "Again", color: "bg-rose-500", text: "text-rose-700", desc: "Complete blackout" },
  { value: 2, label: "Hard", color: "bg-orange-500", text: "text-orange-700", desc: "Incorrect, remembered answer" },
  { value: 3, label: "Good", color: "bg-brand-500", text: "text-brand-700", desc: "Correct with hesitation" },
  { value: 4, label: "Easy", color: "bg-emerald-500", text: "text-emerald-700", desc: "Perfect response" },
];

export function SpacedRepetitionPanel({ taId }: SpacedRepetitionPanelProps) {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = useState("due");
  const [selectedItem, setSelectedItem] = useState<ReviewItem | null>(null);
  const [showRating, setShowRating] = useState(false);

  // Get due reviews
  const { data: dueData, isLoading: isLoadingDue } = useQuery({
    queryKey: ["spaced-repetition", "due", taId],
    queryFn: async () => {
      const res = await apiFetch(`/spaced-repetition/due-reviews/${taId}`);
      return res.json();
    },
  });

  // Get retention stats
  const { data: statsData, isLoading: isLoadingStats } = useQuery({
    queryKey: ["spaced-repetition", "stats", taId],
    queryFn: async () => {
      const res = await apiFetch(`/spaced-repetition/retention-stats/${taId}`);
      return res.json();
    },
  });

  // Get daily plan
  const { data: planData } = useQuery({
    queryKey: ["spaced-repetition", "plan", taId],
    queryFn: async () => {
      const res = await apiFetch(`/spaced-repetition/daily-plan/${taId}`);
      return res.json();
    },
  });

  // Rate review mutation
  const rateMutation = useMutation({
    mutationFn: async ({ unit_id, rating }: { unit_id: string; rating: number }) => {
      const res = await apiFetch(`/spaced-repetition/rate/${taId}`, {
        method: "POST",
        body: JSON.stringify({ unit_id, rating }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["spaced-repetition", "due", taId] });
      queryClient.invalidateQueries({ queryKey: ["spaced-repetition", "stats", taId] });
      queryClient.invalidateQueries({ queryKey: ["spaced-repetition", "plan", taId] });
      setSelectedItem(null);
      setShowRating(false);
    },
  });

  const dueItems: ReviewItem[] = dueData?.due_items || [];
  const stats: RetentionStats = statsData?.statistics || {} as RetentionStats;
  const forgettingCurve = statsData?.forgetting_curve || [];

  const handleRate = (rating: number) => {
    if (!selectedItem) return;
    rateMutation.mutate({ unit_id: selectedItem.unit_id, rating });
  };

  return (
    <Card padding="lg">
      {/* Header */}
      <div className="flex items-start gap-4 mb-6">
        <div className="p-3 bg-brand-100 rounded-xl">
          <Brain className="w-6 h-6 text-brand-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-slate-900">Smart Review System</h3>
          <p className="text-slate-500 mt-1">
            AI-powered spaced repetition based on the forgetting curve. Reviews are scheduled at optimal intervals for maximum retention.
          </p>
        </div>
        {dueItems.length > 0 && (
          <div className="px-4 py-2 bg-amber-50 rounded-lg border border-amber-200">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-600" />
              <span className="text-sm font-medium text-amber-900">
                {dueItems.length} due for review
              </span>
            </div>
          </div>
        )}
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3 mb-6">
          <TabsTrigger value="due">
            <Clock className="w-4 h-4 mr-2" />
            Due Now ({dueItems.length})
          </TabsTrigger>
          <TabsTrigger value="stats">
            <BarChart3 className="w-4 h-4 mr-2" />
            Retention Stats
          </TabsTrigger>
          <TabsTrigger value="curve">
            <TrendingUp className="w-4 h-4 mr-2" />
            Forgetting Curve
          </TabsTrigger>
        </TabsList>

        {/* Due Reviews Tab */}
        <TabsContent value="due" className="m-0 space-y-4">
          {isLoadingDue ? (
            <div className="text-center py-8">
              <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-500 rounded-full animate-spin mx-auto" />
            </div>
          ) : dueItems.length === 0 ? (
            <div className="text-center py-12 bg-slate-50 rounded-xl">
              <CheckCircle className="w-12 h-12 text-emerald-500 mx-auto mb-4" />
              <h4 className="font-semibold text-slate-900">All Caught Up!</h4>
              <p className="text-slate-500 mt-2 max-w-sm mx-auto">
                No items are due for review. Your memory is well-maintained. Check back tomorrow!
              </p>
            </div>
          ) : (
            <>
              {/* Daily Plan Summary */}
              {planData && (
                <div className="p-4 bg-brand-50 rounded-xl border border-brand-100">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Calendar className="w-5 h-5 text-brand-600" />
                      <div>
                        <p className="font-medium text-brand-900">Today's Review Plan</p>
                        <p className="text-sm text-brand-700">
                          {planData.selected_for_review} items selected • ~{planData.estimated_minutes} minutes
                        </p>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        if (dueItems.length > 0) {
                          setSelectedItem(dueItems[0]);
                          setShowRating(true);
                        }
                      }}
                    >
                      Start Review
                    </Button>
                  </div>
                </div>
              )}

              {/* Review Items List */}
              <div className="space-y-3">
                {dueItems.map((item) => (
                  <div
                    key={item.unit_id}
                    className={cn(
                      "p-4 rounded-xl border transition-all cursor-pointer",
                      selectedItem?.unit_id === item.unit_id
                        ? "border-brand-500 bg-brand-50"
                        : "border-slate-200 hover:border-slate-300 bg-white"
                    )}
                    onClick={() => {
                      setSelectedItem(item);
                      setShowRating(true);
                    }}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-medium text-slate-900">{item.unit_name}</h4>
                        <div className="flex items-center gap-3 mt-2 text-sm text-slate-500">
                          <span className="flex items-center gap-1">
                            <RotateCw className="w-3.5 h-3.5" />
                            {item.repetitions} reviews
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-3.5 h-3.5" />
                            {Math.round(item.interval_days)} day interval
                          </span>
                          <span className={cn(
                            "px-2 py-0.5 rounded text-xs",
                            item.ease_factor > 2.5 ? "bg-emerald-100 text-emerald-700" :
                            item.ease_factor > 2.0 ? "bg-brand-100 text-brand-700" :
                            "bg-amber-100 text-amber-700"
                          )}>
                            Ease: {item.ease_factor.toFixed(2)}
                          </span>
                        </div>
                      </div>
                      <ChevronRight className="w-5 h-5 text-slate-400" />
                    </div>

                    {/* Progress */}
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-xs mb-1">
                        <span className="text-slate-500">Retention strength</span>
                        <span className={cn(
                          "font-medium",
                          item.average_rating >= 3 ? "text-emerald-600" :
                          item.average_rating >= 2 ? "text-amber-600" :
                          "text-rose-600"
                        )}>
                          {item.successful_reviews}/{item.total_reviews} correct
                        </span>
                      </div>
                      <ProgressBar
                        value={(item.average_rating / 4) * 100}
                        className="h-1.5"
                        color={item.average_rating >= 3 ? "success" : item.average_rating >= 2 ? "brand" : "warning"}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Rating Modal */}
          {showRating && selectedItem && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
              <Card padding="lg" className="w-full max-w-lg animate-in fade-in zoom-in">
                <div className="text-center mb-6">
                  <h4 className="text-lg font-semibold text-slate-900">How well did you remember?</h4>
                  <p className="text-slate-500 mt-1">{selectedItem.unit_name}</p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  {RATING_OPTIONS.map((option) => (
                    <button
                      key={option.value}
                      onClick={() => handleRate(option.value)}
                      disabled={rateMutation.isPending}
                      className={cn(
                        "p-4 rounded-xl border-2 transition-all text-left",
                        "hover:scale-[1.02] active:scale-[0.98]",
                        "border-slate-200 hover:border-brand-300"
                      )}
                    >
                      <div className={cn("w-3 h-3 rounded-full mb-2", option.color)} />
                      <p className={cn("font-semibold", option.text)}>{option.label}</p>
                      <p className="text-xs text-slate-500 mt-1">{option.desc}</p>
                    </button>
                  ))}
                </div>

                <Button
                  variant="secondary"
                  className="w-full mt-4"
                  onClick={() => setShowRating(false)}
                >
                  Cancel
                </Button>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Stats Tab */}
        <TabsContent value="stats" className="m-0 space-y-4">
          {isLoadingStats ? (
            <div className="text-center py-8">
              <div className="w-8 h-8 border-4 border-brand-200 border-t-brand-500 rounded-full animate-spin mx-auto" />
            </div>
          ) : (
            <>
              {/* Overview Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 bg-slate-50 rounded-xl text-center">
                  <BookOpen className="w-5 h-5 text-slate-400 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-slate-900">{stats?.total_scheduled || 0}</p>
                  <p className="text-xs text-slate-500">In Schedule</p>
                </div>
                <div className="p-4 bg-emerald-50 rounded-xl text-center">
                  <CheckCircle className="w-5 h-5 text-emerald-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-emerald-700">{stats?.up_to_date || 0}</p>
                  <p className="text-xs text-emerald-600">Up to Date</p>
                </div>
                <div className="p-4 bg-amber-50 rounded-xl text-center">
                  <Clock className="w-5 h-5 text-amber-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-amber-700">{stats?.due_now || 0}</p>
                  <p className="text-xs text-amber-600">Due for Review</p>
                </div>
                <div className="p-4 bg-brand-50 rounded-xl text-center">
                  <Award className="w-5 h-5 text-brand-500 mx-auto mb-2" />
                  <p className="text-2xl font-bold text-brand-700">
                    {stats?.average_ease_factor?.toFixed(2) || "2.50"}
                  </p>
                  <p className="text-xs text-brand-600">Avg Ease Factor</p>
                </div>
              </div>

              {/* Retention Prediction */}
              {stats?.predicted_retention && (
                <div className="p-4 bg-slate-50 rounded-xl">
                  <div className="flex items-center gap-2 mb-4">
                    <Target className="w-5 h-5 text-brand-500" />
                    <h4 className="font-medium text-slate-900">Predicted Retention</h4>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    {Object.entries(stats.predicted_retention).map(([period, value]) => (
                      <div key={period} className="text-center">
                        <p className={cn(
                          "text-xl font-bold",
                          (value as number) > 80 ? "text-emerald-600" :
                          (value as number) > 60 ? "text-amber-600" :
                          "text-rose-600"
                        )}>
                          {Math.round((value as number) * 100)}%
                        </p>
                        <p className="text-xs text-slate-500">
                          {period.replace("_", " ")}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Repetition Distribution */}
              {stats?.repetition_distribution && Object.keys(stats.repetition_distribution).length > 0 && (
                <div className="p-4 bg-slate-50 rounded-xl">
                  <div className="flex items-center gap-2 mb-4">
                    <RotateCw className="w-5 h-5 text-brand-500" />
                    <h4 className="font-medium text-slate-900">Review Distribution</h4>
                  </div>
                  <div className="space-y-2">
                    {Object.entries(stats.repetition_distribution).map(([count, num]) => (
                      <div key={count} className="flex items-center gap-3">
                        <span className="w-16 text-sm text-slate-600">
                          {count === "5" ? "5+ reps" : `${count} reps`}
                        </span>
                        <div className="flex-1 h-4 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-brand-500 rounded-full"
                            style={{
                              width: `${(num as number / stats.total_scheduled) * 100}%`,
                            }}
                          />
                        </div>
                        <span className="w-8 text-sm text-slate-600 text-right">{num as number}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </TabsContent>

        {/* Forgetting Curve Tab */}
        <TabsContent value="curve" className="m-0">
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-xl">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-5 h-5 text-brand-500" />
                <h4 className="font-medium text-slate-900">Ebbinghaus Forgetting Curve</h4>
              </div>
              <p className="text-sm text-slate-600 mb-4">
                Without review, memory retention follows an exponential decay pattern. 
                Spaced repetition counteracts this by scheduling reviews at optimal intervals.
              </p>

              {forgettingCurve.length > 0 && (
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={forgettingCurve}>
                      <defs>
                        <linearGradient id="retentionGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <XAxis
                        dataKey="day"
                        tick={{ fontSize: 12 }}
                        label={{ value: "Days", position: "insideBottom", offset: -5 }}
                      />
                      <YAxis
                        tick={{ fontSize: 12 }}
                        domain={[0, 100]}
                        label={{ value: "Retention %", angle: -90, position: "insideLeft" }}
                      />
                      <Tooltip
                        formatter={(value: number) => [`${value.toFixed(1)}%`, "Retention"]}
                        labelFormatter={(label) => `Day ${label}`}
                      />
                      <Area
                        type="monotone"
                        dataKey="retention"
                        stroke="#6366f1"
                        strokeWidth={2}
                        fill="url(#retentionGradient)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              )}

              {/* Intervals */}
              <div className="grid grid-cols-4 gap-2 mt-4">
                {[
                  { day: 1, label: "1st Review", color: "bg-rose-100 text-rose-700" },
                  { day: 3, label: "2nd Review", color: "bg-amber-100 text-amber-700" },
                  { day: 7, label: "3rd Review", color: "bg-brand-100 text-brand-700" },
                  { day: 14, label: "4th Review", color: "bg-emerald-100 text-emerald-700" },
                ].map((interval) => (
                  <div key={interval.day} className={cn("p-2 rounded-lg text-center", interval.color)}>
                    <p className="text-lg font-bold">Day {interval.day}</p>
                    <p className="text-xs">{interval.label}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
}
