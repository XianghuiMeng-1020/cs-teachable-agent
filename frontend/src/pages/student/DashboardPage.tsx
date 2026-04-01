import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip as RTooltip, Cell } from "recharts";
import { useAppStore } from "@/stores/appStore";
import { getState, getMastery, getMisconceptions, getHistory, getConfig, getGamification, getLearningPath, listTA } from "@/api/client";
import { getRecommendedItems, getAssessmentStats } from "@/api/assessment";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import {
  BookOpen, BookOpenCheck, CheckCircle, AlertTriangle, MessageCircle,
  Sparkles, BrainCircuit, Bot, MessageSquare, Play, X, ChevronRight, ArrowRight,
  TrendingUp, Target, Zap, Award, Clock, GraduationCap, Flame,
} from "lucide-react";
import { StatCard } from "@/components/ui/StatCard";
import { Card } from "@/components/ui/Card";
import { MasteryRadial } from "@/components/state/MasteryRadial";
import { MisconceptionCard, MisconceptionCardEmpty } from "@/components/state/MisconceptionCard";
import { TimelineView } from "@/components/state/TimelineView";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { PointsSystem } from "@/components/gamification/PointsSystem";
import { AchievementSystem } from "@/components/gamification/AchievementSystem";
import { SmartLearningPath } from "@/components/learning/SmartLearningPath";
import { MisconceptionAI } from "@/components/diagnosis/MisconceptionAI";
import { DomainSelector } from "@/components/onboarding/DomainSelector";
import { useAuthStore } from "@/stores/authStore";
import { ROUTES } from "@/lib/constants";
import type { TimelineEvent } from "@/components/state/TimelineView";

const DASHBOARD_HINT_KEY = "cs-ta-dashboard-hint-dismissed";

// Animation variants
const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

function useActivityTrend(taId: number | null) {
  const { data: historyData } = useQuery({
    queryKey: ["ta", taId, "history-trend", 1, 50],
    queryFn: () => getHistory(taId!, { page: 1, per_page: 50 }),
    enabled: taId != null && taId > 0,
  });
  const items = historyData?.items ?? [];
  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - (6 - i));
    return d.toISOString().slice(0, 10);
  });
  const byDay: Record<string, number> = {};
  last7Days.forEach((day) => (byDay[day] = 0));
  items.forEach((evt) => {
    const day = (evt.timestamp || "").slice(0, 10);
    if (day in byDay) byDay[day]++;
  });
  return last7Days.map((date) => ({ date: date.slice(5), count: byDay[date] ?? 0 }));
}

const ONBOARDING_KEY = "cs-ta-onboarding-completed";

export function DashboardPage() {
  const { t } = useTranslation();
  const currentTaId = useAppStore((s) => s.currentTaId);
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();
  const [hintDismissed, setHintDismissed] = useState(() =>
    typeof localStorage !== "undefined" && localStorage.getItem(DASHBOARD_HINT_KEY) === "1"
  );
  const [showDomainSelector, setShowDomainSelector] = useState(false);
  const activityTrend = useActivityTrend(currentTaId);

  const { data: taList, isLoading: isLoadingTAs } = useQuery({
    queryKey: ["ta", "list"],
    queryFn: listTA,
  });

  useEffect(() => {
    if (!isLoadingTAs && taList && taList.length === 0) {
      const hasCompletedOnboarding = typeof localStorage !== "undefined" &&
        localStorage.getItem(ONBOARDING_KEY) === "1";
      if (!hasCompletedOnboarding) setShowDomainSelector(true);
    }
  }, [taList, isLoadingTAs]);

  const handleOnboardingComplete = () => {
    try { localStorage.setItem(ONBOARDING_KEY, "1"); } catch {}
    setShowDomainSelector(false);
  };

  const { data: state } = useQuery({
    queryKey: ["ta", currentTaId, "state"],
    queryFn: () => getState(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: mastery } = useQuery({
    queryKey: ["ta", currentTaId, "mastery"],
    queryFn: () => getMastery(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: misconceptionsData } = useQuery({
    queryKey: ["ta", currentTaId, "misconceptions"],
    queryFn: () => getMisconceptions(currentTaId!),
    enabled: currentTaId != null,
  });
  const { data: historyData } = useQuery({
    queryKey: ["ta", currentTaId, "history", 1, 5],
    queryFn: () => getHistory(currentTaId!, { page: 1, per_page: 5 }),
    enabled: currentTaId != null,
  });
  const { data: config } = useQuery({ queryKey: ["config"], queryFn: getConfig });
  const { data: gamification } = useQuery({ queryKey: ["gamification"], queryFn: getGamification });
  const { data: learningPath } = useQuery({
    queryKey: ["ta", currentTaId, "learning-path"],
    queryFn: () => getLearningPath(currentTaId!),
    enabled: currentTaId != null && currentTaId > 0,
  });
  const { data: practiceRecs } = useQuery({
    queryKey: ["assessment", "recommend", currentTaId],
    queryFn: () => getRecommendedItems({ ta_id: currentTaId ?? undefined, count: 3 }),
  });
  const { data: assessStats } = useQuery({
    queryKey: ["assessment", "stats"],
    queryFn: getAssessmentStats,
  });

  const learnedCount = state?.learned_unit_ids?.length ?? 0;
  const totalKus = state?.units ? Object.keys(state.units).length : 20;
  const misconceptions = misconceptionsData?.misconceptions ?? [];
  const recentEvents: TimelineEvent[] = (historyData?.items ?? []).map((i) => ({
    id: i.id,
    type: (i.type as TimelineEvent["type"]) ?? "teach",
    title: i.title,
    description: i.description,
    timestamp: i.timestamp,
    metadata: i.metadata,
  }));
  const isStubMode = !config?.llm_configured;

  // Calculate streak and progress
  const streakDays = activityTrend.filter(d => d.count > 0).length;
  const progressPercent = totalKus > 0 ? Math.round((learnedCount / totalKus) * 100) : 0;

  if (currentTaId == null) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="space-y-6"
      >
        <div className="text-center py-12">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-100 to-brand-50 mb-6">
            <Bot className="w-10 h-10 text-brand-600" />
          </div>
          <h1 className="text-3xl font-bold text-stone-900 mb-2">{t("dashboard.noTATitle")}</h1>
          <p className="text-stone-500 mb-8">{t("dashboard.welcomeBack", { username: user?.username ?? "" })}</p>
        </div>
        <Card padding="lg" className="border-dashed border-2 border-stone-200">
          <EmptyState
            icon={Bot}
            title={t("dashboard.noTASelected")}
            description={t("dashboard.noTADesc")}
            action={
              <Button onClick={() => setShowDomainSelector(true)} icon={Sparkles}>
                {t("dashboard.createFirstTA")}
              </Button>
            }
          />
        </Card>
        <DomainSelector
          open={showDomainSelector}
          onOpenChange={setShowDomainSelector}
          onComplete={handleOnboardingComplete}
        />
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      <DomainSelector
        open={showDomainSelector}
        onOpenChange={setShowDomainSelector}
        onComplete={handleOnboardingComplete}
      />

      {/* Welcome Header */}
      <motion.div variants={fadeIn} className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-brand-600 via-brand-700 to-violet-700 p-6 sm:p-8 text-white shadow-xl">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-white/10 via-transparent to-transparent" />
        <div className="relative">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-5 h-5 text-brand-200" />
                <span className="text-sm font-medium text-brand-100">{t("dashboard.title")}</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold">{t("dashboard.welcomeBack", { username: user?.username ?? "" })}</h1>
              <p className="mt-1 text-brand-100">{t("dashboard.continueTeaching")}</p>
            </div>
            <div className="flex gap-2">
              <Link to={ROUTES.teach}>
                <Button 
                  icon={MessageSquare} 
                  className="bg-white text-brand-700 hover:bg-brand-50 shadow-lg"
                >
                  {t("dashboard.teachNow")}
                </Button>
              </Link>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-6 flex items-center gap-4">
            <div className="flex-1">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-brand-100">{t("dashboard.overallProgress")}</span>
                <span className="font-semibold">{progressPercent}%</span>
              </div>
              <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${progressPercent}%` }}
                  transition={{ duration: 1, delay: 0.5 }}
                  className="h-full bg-gradient-to-r from-white to-brand-200 rounded-full"
                />
              </div>
            </div>
            {streakDays > 0 && (
              <div className="flex items-center gap-2 bg-white/10 rounded-lg px-3 py-2">
                <Flame className="w-5 h-5 text-amber-300" />
                <div>
                  <div className="text-xs text-brand-100">{t("dashboard.streak")}</div>
                  <div className="font-bold">{streakDays} {t("dashboard.days")}</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </motion.div>

      {/* Notifications */}
      {isStubMode && (
        <motion.div variants={fadeIn} className="rounded-xl border border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center flex-shrink-0">
              <BrainCircuit className="h-5 w-5 text-amber-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-amber-900">{t("dashboard.demoMode")}</p>
              <p className="mt-0.5 text-sm text-amber-700">
                {t("dashboard.demoModeDesc")}
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {!hintDismissed && (
        <motion.div variants={fadeIn} className="rounded-xl border border-brand-200 bg-gradient-to-r from-brand-50 to-emerald-50 p-4">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-lg bg-brand-100 flex items-center justify-center flex-shrink-0">
              <Sparkles className="h-5 w-5 text-brand-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-brand-900">{t("dashboard.gettingStarted")}</p>
              <p className="mt-0.5 text-sm text-brand-700">
                {t("dashboard.gettingStartedDesc")}
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                setHintDismissed(true);
                try { localStorage.setItem(DASHBOARD_HINT_KEY, "1"); } catch {}
              }}
              className="rounded-lg p-1 text-brand-400 hover:text-brand-600 hover:bg-brand-100 transition-colors"
              aria-label={t("common.close")}
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </motion.div>
      )}

      {/* Quick Actions */}
      <motion.div variants={fadeIn} className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { to: ROUTES.teach, icon: MessageSquare, labelKey: "dashboard.teach", color: "from-emerald-500 to-teal-600", descKey: "dashboard.teachDesc" },
          { to: ROUTES.test, icon: Play, labelKey: "dashboard.test", color: "from-blue-500 to-indigo-600", descKey: "dashboard.testDesc" },
          { to: ROUTES.practice, icon: BookOpenCheck, labelKey: "dashboard.practice", color: "from-violet-500 to-purple-600", descKey: "dashboard.practiceDesc" },
          { to: ROUTES.mastery, icon: Target, labelKey: "dashboard.masteryAction", color: "from-amber-500 to-orange-600", descKey: "dashboard.masteryActionDesc" },
        ].map((action) => (
          <Link key={action.to} to={action.to}>
            <motion.div
              whileHover={{ scale: 1.02, y: -2 }}
              whileTap={{ scale: 0.98 }}
              className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${action.color} p-4 text-white shadow-lg hover:shadow-xl transition-all cursor-pointer`}
            >
              <div className="absolute top-0 right-0 w-20 h-20 bg-white/10 rounded-full -mr-10 -mt-10" />
              <action.icon className="w-6 h-6 mb-3" />
              <div className="font-semibold">{t(action.labelKey)}</div>
              <div className="text-xs text-white/80">{t(action.descKey)}</div>
            </motion.div>
          </Link>
        ))}
      </motion.div>

      {/* Stats Grid */}
      <motion.div variants={fadeIn} className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <BookOpen className="w-5 h-5 text-emerald-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{learnedCount}<span className="text-stone-400 text-lg">/{totalKus}</span></div>
          </div>
          <div className="text-sm text-stone-500">{t("dashboard.conceptsLearned")}</div>
          <div className="mt-2 h-1.5 bg-stone-100 rounded-full overflow-hidden">
            <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${progressPercent}%` }} />
          </div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <CheckCircle className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">
              {mastery?.pass_rate != null ? `${Math.round(mastery.pass_rate * 100)}%` : "—"}
            </div>
          </div>
          <div className="text-sm text-stone-500">{t("dashboard.testPassRate")}</div>
          <div className="mt-2 text-xs text-stone-400">{mastery?.test_count ?? 0} {t("dashboard.testsCompleted")}</div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-amber-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{misconceptions.length}</div>
          </div>
          <div className="text-sm text-stone-500">{t("dashboard.activeMisconceptions")}</div>
          <div className="mt-2 text-xs text-stone-400">
            {misconceptions.length > 0 ? t("dashboard.needsAttention") : t("dashboard.allClear")}
          </div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center">
              <Zap className="w-5 h-5 text-violet-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">
              {gamification?.points ?? 0}
            </div>
          </div>
          <div className="text-sm text-stone-500">{t("dashboard.totalPoints")}</div>
          <div className="mt-2 text-xs text-violet-600 font-medium">
            {t("analytics.level")} {gamification?.level ?? 1}
          </div>
        </div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Left column - Activity & Timeline */}
        <motion.div variants={fadeIn} className="space-y-6 lg:col-span-2">
          {/* Activity Chart */}
          {activityTrend.some((d) => d.count > 0) && (
            <Card padding="lg" className="overflow-hidden">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-lg font-bold text-stone-900 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-brand-600" />
                    {t("dashboard.learningActivity")}
                  </h2>
                  <p className="text-sm text-stone-500">{t("dashboard.activityDesc")}</p>
                </div>
                <div className="flex items-center gap-2 text-sm text-stone-500">
                  <Clock className="w-4 h-4" />
                  {t("dashboard.last7Days")}
                </div>
              </div>
              <div className="h-[180px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={activityTrend} margin={{ top: 4, right: 4, left: 0, bottom: 0 }}>
                    <XAxis 
                      dataKey="date" 
                      tick={{ fontSize: 11, fill: "#78716C" }} 
                      axisLine={false} 
                      tickLine={false} 
                    />
                    <YAxis 
                      allowDecimals={false} 
                      tick={{ fontSize: 11, fill: "#78716C" }} 
                      width={28} 
                      axisLine={false} 
                      tickLine={false} 
                    />
                    <RTooltip
                      contentStyle={{ 
                        borderRadius: "8px", 
                        border: "1px solid #E7E5E4", 
                        fontSize: "12px",
                        boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)"
                      }}
                    />
                    <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                      {activityTrend.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.count > 0 ? "#0D9488" : "#E7E5E4"} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          )}

          {/* Recent Activity */}
          <Card padding="lg">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-stone-900 flex items-center gap-2">
                  <Clock className="w-5 h-5 text-brand-600" />
                  {t("dashboard.recentActivity")}
                </h2>
                <p className="text-sm text-stone-500">{t("dashboard.recentActivityDesc")}</p>
              </div>
              <Link
                to={ROUTES.history}
                className="text-sm font-semibold text-brand-600 hover:text-brand-700 flex items-center gap-1 transition-colors"
              >
                {t("dashboard.viewAll")} <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
            {recentEvents.length === 0 ? (
              <div className="text-center py-8">
                <div className="w-16 h-16 rounded-full bg-stone-100 flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="w-8 h-8 text-stone-400" />
                </div>
                <p className="text-stone-500 mb-2">{t("dashboard.noActivity")}</p>
                <p className="text-sm text-stone-400 mb-4">{t("dashboard.noActivityDesc")}</p>
                <Link to={ROUTES.teach}>
                  <Button size="sm" icon={MessageSquare}>{t("dashboard.startTeaching")}</Button>
                </Link>
              </div>
            ) : (
              <TimelineView events={recentEvents} />
            )}
          </Card>

          {/* Misconceptions */}
          {misconceptions.length > 0 && (
            <Card padding="lg">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-lg font-bold text-stone-900 flex items-center gap-2">
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                    {t("dashboard.misconceptionsDetected")}
                  </h2>
                  <p className="text-sm text-stone-500">{t("dashboard.misconceptionsDetectedDesc")}</p>
                </div>
              </div>
              <div className="space-y-3">
                {misconceptions.slice(0, 3).map((m) => (
                  <MisconceptionCard key={m.id} misconception={m} />
                ))}
              </div>
            </Card>
          )}
        </motion.div>

        {/* Right column - Gamification & Learning */}
        <motion.div variants={fadeIn} className="space-y-6">
          {gamification && (
            <>
              <PointsSystem points={gamification.points} level={gamification.level} />
              <AchievementSystem achievements={gamification.achievements} />
            </>
          )}
          
          {learningPath && (
            <SmartLearningPath
              recommended={learningPath.recommended}
              pathSummary={learningPath.path_summary}
              learnedCount={learningPath.learned_count}
              totalCount={learningPath.total_count}
            />
          )}

          {/* Practice Recommendations */}
          {practiceRecs && practiceRecs.length > 0 && (
            <Card padding="md">
              <h3 className="font-semibold text-stone-900 mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-violet-600" />
                {t("dashboard.recommendedPractice")}
              </h3>
              <div className="space-y-3">
                {practiceRecs.slice(0, 3).map((rec: any) => (
                  <Link
                    key={rec.id}
                    to={`${ROUTES.practice}?item=${rec.id}`}
                    className="block p-3 rounded-lg bg-stone-50 hover:bg-stone-100 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-stone-900 text-sm">{rec.title}</div>
                        <div className="text-xs text-stone-500">{rec.domain_id} • {rec.item_type}</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-stone-400" />
                    </div>
                  </Link>
                ))}
              </div>
              <Link to={ROUTES.practice}>
                <Button variant="outline" size="sm" fullWidth className="mt-4">
                  {t("dashboard.viewAllExercises")}
                </Button>
              </Link>
            </Card>
          )}

          {/* Mastery Overview */}
          {mastery && (
            <Card padding="md" className="bg-gradient-to-br from-brand-50 to-emerald-50 border-brand-100">
              <h3 className="font-semibold text-stone-900 mb-4 flex items-center gap-2">
                <Award className="w-5 h-5 text-brand-600" />
                {t("dashboard.masteryOverview")}
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-stone-600">{t("dashboard.overallLevel")}</span>
                  <span className="font-semibold text-brand-700 capitalize">{mastery.level || "Beginner"}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-stone-600">{t("dashboard.passRate")}</span>
                  <span className="font-semibold text-emerald-600">
                    {mastery.pass_rate != null ? `${Math.round(mastery.pass_rate * 100)}%` : "—"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-stone-600">{t("test.total")}</span>
                  <span className="font-semibold text-stone-900">{mastery.test_count ?? 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-stone-600">{t("dashboard.readyForNext")}</span>
                  <span className={`font-semibold ${(mastery.pass_rate ?? 0) >= 0.8 ? "text-emerald-600" : "text-amber-600"}`}>
                    {(mastery.pass_rate ?? 0) >= 0.8 ? t("dashboard.yes") : t("dashboard.keepPracticing")}
                  </span>
                </div>
              </div>
              <Link to={ROUTES.mastery}>
                <Button size="sm" variant="outline" fullWidth className="mt-4 bg-white">
                  {t("dashboard.viewDetailedMastery")}
                </Button>
              </Link>
            </Card>
          )}
        </motion.div>
      </div>
      <ContextualHelp pageKey="dashboard" />
    </motion.div>
  );
}
