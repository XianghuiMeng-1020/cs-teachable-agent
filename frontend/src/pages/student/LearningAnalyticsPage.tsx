import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { ContextualHelp } from "@/components/ui/ContextualHelp";
import { Card } from "@/components/ui/Card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { Button } from "@/components/ui/Button";
import { LearningPacePanel } from "@/components/analytics/LearningPacePanel";
import { CognitiveLoadPanel } from "@/components/analytics/CognitiveLoadPanel";
import { ConceptRelationGraph } from "@/components/analytics/ConceptRelationGraph";
import { LearningBehaviorDashboard } from "@/components/analytics/LearningBehaviorDashboard";
import { CrossDomainTransfer } from "@/components/analytics/CrossDomainTransfer";
import { WebVitalsPanel } from "@/components/analytics/WebVitalsPanel";
import { ExperimentPanel } from "@/components/analytics/ExperimentPanel";
import { StreakTracker } from "@/components/gamification/StreakTracker";
import { AchievementShowcase } from "@/components/gamification/AchievementShowcase";
import { KnowledgeGraph3D } from "@/components/learning/KnowledgeGraph3D";
import { 
  Brain, 
  Activity, 
  Network, 
  BarChart3, 
  Flame,
  Download,
  Share2,
  Sparkles,
  Trophy,
  ArrowRightLeft,
  Box,
  FlaskConical,
  Gauge
} from "lucide-react";

export function LearningAnalyticsPage() {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState("overview");

  const mockUserId = 1;
  const mockTaId = 1;

  const paceRows = useMemo(
    () =>
      [
        {
          date: t("analytics.paceMockToday", { defaultValue: "Today" }),
          paceLabel: t("analytics.medium"),
          changeLabel: t("analytics.stable"),
          changeKind: "stable" as const,
        },
        {
          date: t("analytics.paceMockYesterday", { defaultValue: "Yesterday" }),
          paceLabel: t("analytics.fast"),
          changeLabel: "+15%",
          changeKind: "up" as const,
        },
        {
          date: t("analytics.paceMockTwoDaysAgo", { defaultValue: "Two days ago" }),
          paceLabel: t("analytics.slow"),
          changeLabel: "-20%",
          changeKind: "down" as const,
        },
        {
          date: t("analytics.paceMockThreeDaysAgo", { defaultValue: "3 days ago" }),
          paceLabel: t("analytics.medium"),
          changeLabel: t("analytics.stable"),
          changeKind: "stable" as const,
        },
      ] as const,
    [t],
  );

  return (
    <div className="min-h-screen bg-stone-50 pb-12">
      {/* Header */}
      <div className="bg-white border-b border-stone-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-brand-700 to-brand-600 rounded-xl">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-stone-900">{t("analytics.title")}</h1>
                <p className="text-sm text-stone-500">{t("analytics.desc")}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <Share2 className="w-4 h-4 mr-2" />
                {t("analytics.share", { defaultValue: "Share" })}
              </Button>
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <Download className="w-4 h-4 mr-2" />
                {t("analytics.exportReport", { defaultValue: "Export report" })}
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-white p-1 border border-stone-200 rounded-xl flex-wrap">
            <TabsTrigger value="overview" className="rounded-lg">
              <Activity className="w-4 h-4 mr-2" />
              {t("analytics.overview")}
            </TabsTrigger>
            <TabsTrigger value="pace" className="rounded-lg">
              <Sparkles className="w-4 h-4 mr-2" />
              {t("analytics.learningPace")}
            </TabsTrigger>
            <TabsTrigger value="cognitive" className="rounded-lg">
              <Brain className="w-4 h-4 mr-2" />
              {t("analytics.cognitiveLoad")}
            </TabsTrigger>
            <TabsTrigger value="concepts" className="rounded-lg">
              <Network className="w-4 h-4 mr-2" />
              {t("analytics.conceptRelations")}
            </TabsTrigger>
            <TabsTrigger value="behavior" className="rounded-lg">
              <BarChart3 className="w-4 h-4 mr-2" />
              {t("analytics.behaviorAnalysis", { defaultValue: "Behavior analysis" })}
            </TabsTrigger>
            <TabsTrigger value="3d-graph" className="rounded-lg">
              <Box className="w-4 h-4 mr-2" />
              {t("analytics.graph3d")}
            </TabsTrigger>
            <TabsTrigger value="achievements" className="rounded-lg">
              <Trophy className="w-4 h-4 mr-2" />
              {t("analytics.achievements")}
            </TabsTrigger>
            <TabsTrigger value="transfer" className="rounded-lg">
              <ArrowRightLeft className="w-4 h-4 mr-2" />
              {t("analytics.crossDomain")}
            </TabsTrigger>
            <TabsTrigger value="performance" className="rounded-lg">
              <Gauge className="w-4 h-4 mr-2" />
              {t("analytics.performance")}
            </TabsTrigger>
            <TabsTrigger value="experiments" className="rounded-lg hidden md:flex">
              <FlaskConical className="w-4 h-4 mr-2" />
              {t("analytics.experiments")}
            </TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-emerald-100 rounded-lg">
                    <Activity className="w-5 h-5 text-emerald-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-stone-900">87%</p>
                    <p className="text-sm text-stone-500">{t("analytics.learningEfficiency")}</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Brain className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-stone-900">{t("analytics.medium")}</p>
                    <p className="text-sm text-stone-500">{t("analytics.cognitiveLoad")}</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Network className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-stone-900">23</p>
                    <p className="text-sm text-stone-500">{t("mastery.conceptMastery")}</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <Flame className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-stone-900">12</p>
                    <p className="text-sm text-stone-500">
                      {t("analytics.studyDaysLabel", { defaultValue: "Study days" })}
                    </p>
                  </div>
                </div>
              </Card>
            </div>

            {/* Main Dashboard */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column */}
              <div className="lg:col-span-2 space-y-6">
                <LearningBehaviorDashboard 
                  taId={mockTaId} 
                  userId={mockUserId} 
                />
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                <StreakTracker userId={mockUserId} />
                <LearningPacePanel studentId={mockUserId} />
              </div>
            </div>
          </TabsContent>

          {/* Learning Pace Tab */}
          <TabsContent value="pace" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <LearningPacePanel studentId={mockUserId} />
              <Card padding="lg">
                <h3 className="font-semibold text-stone-900 mb-4">{t("analytics.paceHistory")}</h3>
                <div className="space-y-4">
                  {paceRows.map((item, i) => (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-stone-100 last:border-0">
                      <div>
                        <p className="font-medium text-stone-900">{item.date}</p>
                        <p className="text-sm text-stone-500">{item.paceLabel}</p>
                      </div>
                      <span className={`text-sm font-medium ${
                        item.changeKind === "stable" ? "text-stone-500" :
                        item.changeKind === "up" ? "text-emerald-600" : "text-amber-600"
                      }`}>
                        {item.changeLabel}
                      </span>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* Cognitive Load Tab */}
          <TabsContent value="cognitive" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <CognitiveLoadPanel studentId={mockUserId} />
              <Card padding="lg">
                <h3 className="font-semibold text-stone-900 mb-4">
                  {t("analytics.loadDistribution", { defaultValue: "Load distribution" })}
                </h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-stone-600">{t("analytics.loadStatus.optimal")}</span>
                      <span className="font-medium text-emerald-600">45%</span>
                    </div>
                    <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 rounded-full" style={{ width: "45%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-stone-600">
                        {t("analytics.loadZoneHigh", { defaultValue: "High load zone" })}
                      </span>
                      <span className="font-medium text-orange-500">30%</span>
                    </div>
                    <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: "30%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-stone-600">{t("analytics.loadStatus.overload")}</span>
                      <span className="font-medium text-red-500">10%</span>
                    </div>
                    <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: "10%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-stone-600">{t("analytics.loadStatus.low")}</span>
                      <span className="font-medium text-blue-500">15%</span>
                    </div>
                    <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                      <div className="h-full bg-blue-500 rounded-full" style={{ width: "15%" }} />
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          </TabsContent>

          {/* Concept Relations Tab */}
          <TabsContent value="concepts" className="space-y-6">
            <ConceptRelationGraph className="h-[600px]" />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card padding="md">
                <h4 className="font-medium text-stone-900 mb-2">
                  {t("analytics.keyPrerequisites", { defaultValue: "Key prerequisites" })}
                </h4>
                <ul className="text-sm text-stone-600 space-y-1">
                  <li>• {t("analytics.prereq1", { defaultValue: "Variables and data types" })}</li>
                  <li>• {t("analytics.prereq2", { defaultValue: "Control flow basics" })}</li>
                  <li>• {t("analytics.prereq3", { defaultValue: "Function definitions" })}</li>
                </ul>
              </Card>
              <Card padding="md">
                <h4 className="font-medium text-stone-900 mb-2">
                  {t("analytics.similarClusters", { defaultValue: "Similar concept clusters" })}
                </h4>
                <ul className="text-sm text-stone-600 space-y-1">
                  <li>• {t("analytics.cluster1", { defaultValue: "Lists and dictionaries" })}</li>
                  <li>• {t("analytics.cluster2", { defaultValue: "Loops and iteration" })}</li>
                  <li>• {t("analytics.cluster3", { defaultValue: "Classes and objects" })}</li>
                </ul>
              </Card>
              <Card padding="md">
                <h4 className="font-medium text-stone-900 mb-2">
                  {t("analytics.suggestedOrder", { defaultValue: "Suggested learning order" })}
                </h4>
                <ol className="text-sm text-stone-600 space-y-1">
                  <li>1. {t("analytics.orderStep1", { defaultValue: "Variables → Data types" })}</li>
                  <li>2. {t("analytics.orderStep2", { defaultValue: "Operators → Expressions" })}</li>
                  <li>3. {t("analytics.orderStep3", { defaultValue: "Conditionals → Loops" })}</li>
                </ol>
              </Card>
            </div>
          </TabsContent>

          {/* Behavior Tab */}
          <TabsContent value="behavior">
            <LearningBehaviorDashboard taId={mockTaId} userId={mockUserId} />
          </TabsContent>

          {/* 3D Graph Tab */}
          <TabsContent value="3d-graph" className="space-y-6">
            <KnowledgeGraph3D className="h-[600px]" />
          </TabsContent>

          {/* Achievements Tab */}
          <TabsContent value="achievements" className="space-y-6">
            <AchievementShowcase />
          </TabsContent>

          {/* Transfer Tab */}
          <TabsContent value="transfer" className="space-y-6">
            <CrossDomainTransfer />
          </TabsContent>

          {/* Performance Tab */}
          <TabsContent value="performance" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <WebVitalsPanel />
              <Card padding="lg">
                <h3 className="font-semibold text-stone-900 mb-4">{t("analytics.performanceTips")}</h3>
                <ul className="space-y-3 text-sm text-stone-600">
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-500">✓</span>
                    {t("analytics.perfTip3d", { defaultValue: "Use 3D knowledge graph sparingly on mobile devices" })}
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-500">✓</span>
                    {t("analytics.perfTipSw", { defaultValue: "Enable service worker for offline access" })}
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-500">✓</span>
                    {t("analytics.perfTipTabs", { defaultValue: "Close unused tabs to free up memory" })}
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-500">✓</span>
                    {t("analytics.perfTipBrowser", { defaultValue: "Use latest Chrome or Firefox for best experience" })}
                  </li>
                </ul>
              </Card>
            </div>
          </TabsContent>

          {/* Experiments Tab */}
          <TabsContent value="experiments" className="space-y-6">
            <ExperimentPanel />
          </TabsContent>
        </Tabs>
      </div>
      <ContextualHelp pageKey="analytics" />
    </div>
  );
}
