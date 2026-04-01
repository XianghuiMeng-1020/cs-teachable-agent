import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { 
  Trophy, 
  Medal, 
  Crown, 
  Star, 
  Zap,
  Target,
  Lock,
  CheckCircle2,
  Share2,
  Sparkles,
  TrendingUp,
  Award
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  tier: "bronze" | "silver" | "gold" | "platinum" | "diamond" | "legendary";
  category: string;
  points: number;
  unlocked: boolean;
  unlocked_at?: string;
  progress: number;
}

interface Title {
  id: string;
  name: string;
  prefix: boolean;
  color: string;
  unlocked: boolean;
}

const mockBadges: Badge[] = [
  { id: "1", name: "First Steps", description: "Complete your first lesson", icon: "🌱", tier: "bronze", category: "learning", points: 10, unlocked: true, progress: 100 },
  { id: "2", name: "Quick Learner", description: "Complete 10 lessons in one day", icon: "⚡", tier: "silver", category: "learning", points: 50, unlocked: true, progress: 100 },
  { id: "3", name: "Knowledge Seeker", description: "Complete 50 lessons", icon: "📚", tier: "gold", category: "learning", points: 100, unlocked: false, progress: 60 },
  { id: "4", name: "Coder Novice", description: "Write your first 100 lines of code", icon: "⌨️", tier: "bronze", category: "practice", points: 20, unlocked: true, progress: 100 },
  { id: "5", name: "Debug Master", description: "Fix 10 bugs in your code", icon: "🐛", tier: "silver", category: "practice", points: 40, unlocked: false, progress: 70 },
  { id: "6", name: "Helpful Peer", description: "Help another student once", icon: "🤝", tier: "bronze", category: "social", points: 15, unlocked: true, progress: 100 },
  { id: "7", name: "Daily Warrior", description: "Complete 7-day streak", icon: "🔥", tier: "silver", category: "challenge", points: 70, unlocked: true, progress: 100 },
  { id: "8", name: "Legend", description: "Reach 5000 total points", icon: "👑", tier: "legendary", category: "special", points: 1000, unlocked: false, progress: 15 },
];

const mockTitles: Title[] = [
  { id: "1", name: "Novice", prefix: true, color: "#8B4513", unlocked: true },
  { id: "2", name: "Student", prefix: true, color: "#4169E1", unlocked: true },
  { id: "3", name: "Scholar", prefix: true, color: "#9932CC", unlocked: false },
  { id: "4", name: "Expert", prefix: true, color: "#FF6347", unlocked: false },
  { id: "5", name: "the Coder", prefix: false, color: "#32CD32", unlocked: false },
];

const tierColors = {
  bronze: "from-amber-700 to-amber-600",
  silver: "from-slate-400 to-slate-300",
  gold: "from-yellow-500 to-yellow-400",
  platinum: "from-cyan-500 to-cyan-400",
  diamond: "from-purple-500 to-pink-500",
  legendary: "from-orange-500 via-red-500 to-purple-500",
};

const tierBorders = {
  bronze: "border-amber-700",
  silver: "border-stone-400",
  gold: "border-yellow-500",
  platinum: "border-cyan-500",
  diamond: "border-purple-500",
  legendary: "border-orange-500",
};

export function AchievementShowcase({ className }: { className?: string }) {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState("badges");
  const [selectedBadge, setSelectedBadge] = useState<Badge | null>(null);
  const [filter, setFilter] = useState<string>("all");

  const stats = {
    totalPoints: 450,
    badgesUnlocked: 5,
    totalBadges: 24,
    titlesUnlocked: 2,
    completion: 21,
    rank: "Student",
    currentStreak: 7,
    longestStreak: 12,
  };

  const filteredBadges = filter === "all" 
    ? mockBadges 
    : mockBadges.filter(b => b.category === filter);

  const categories = ["all", "learning", "practice", "social", "challenge", "special"];

  return (
    <Card padding="lg" className={className}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg">
            <Trophy className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-stone-900">{t("analytics.achievementsTitle")}</h3>
            <p className="text-sm text-stone-500">{t("analytics.desc")}</p>
          </div>
        </div>
        <Button variant="outline" size="sm">
          <Share2 className="w-4 h-4 mr-2" />
          {t("dashboard.viewAll")}
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-yellow-50 to-amber-50 rounded-lg p-3 border border-yellow-200">
          <p className="text-2xl font-bold text-amber-700">{stats.totalPoints}</p>
          <p className="text-xs text-amber-600">{t("dashboard.totalPoints")}</p>
        </div>
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-3 border border-blue-200">
          <p className="text-2xl font-bold text-blue-700">{stats.badgesUnlocked}/{stats.totalBadges}</p>
          <p className="text-xs text-blue-600">{t("analytics.achievements")}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-3 border border-purple-200">
          <p className="text-2xl font-bold text-purple-700">{stats.completion}%</p>
          <p className="text-xs text-purple-600">{t("dashboard.overallProgress")}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-lg p-3 border border-orange-200">
          <p className="text-2xl font-bold text-orange-700">{stats.currentStreak}</p>
          <p className="text-xs text-orange-600">{t("dashboard.streak")}</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="bg-stone-100 p-1 rounded-lg">
          <TabsTrigger value="badges" className="rounded-md">
            <Medal className="w-4 h-4 mr-2" />
            {t("analytics.achievements")}
          </TabsTrigger>
          <TabsTrigger value="titles" className="rounded-md">
            <Crown className="w-4 h-4 mr-2" />
            {t("analytics.tier")}
          </TabsTrigger>
          <TabsTrigger value="progress" className="rounded-md">
            <TrendingUp className="w-4 h-4 mr-2" />
            {t("dashboard.overallProgress")}
          </TabsTrigger>
        </TabsList>

        <TabsContent value="badges" className="space-y-4">
          {/* Category Filter */}
          <div className="flex flex-wrap gap-2">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setFilter(cat)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                  filter === cat
                    ? "bg-brand-500 text-white"
                    : "bg-stone-100 text-stone-600 hover:bg-stone-200"
                }`}
              >
                {cat === "all" ? t("test.total") : 
                 cat === "learning" ? t("analytics.learning") :
                 cat === "practice" ? t("analytics.practicing") :
                 cat === "social" ? t("analytics.social") :
                 cat === "challenge" ? t("analytics.experiments") : t("analytics.special")}
              </button>
            ))}
          </div>

          {/* Badges Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {filteredBadges.map((badge) => (
              <motion.div
                key={badge.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedBadge(badge)}
                className={`relative p-4 rounded-xl border-2 cursor-pointer transition-all ${
                  badge.unlocked 
                    ? `${tierBorders[badge.tier]} bg-gradient-to-br from-white to-slate-50` 
                    : "border-stone-200 bg-stone-50"
                }`}
              >
                {/* Badge Icon */}
                <div className={`w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center text-3xl ${
                  badge.unlocked
                    ? `bg-gradient-to-br ${tierColors[badge.tier]} shadow-lg`
                    : "bg-stone-200"
                }`}>
                  {badge.unlocked ? (
                    badge.icon
                  ) : (
                    <Lock className="w-6 h-6 text-stone-400" />
                  )}
                </div>

                {/* Badge Info */}
                <h4 className={`font-medium text-center text-sm ${badge.unlocked ? "text-stone-900" : "text-stone-400"}`}>
                  {badge.name}
                </h4>
                <p className="text-xs text-center text-stone-500 mt-1 line-clamp-2">
                  {badge.description}
                </p>

                {/* Progress Bar */}
                {!badge.unlocked && (
                  <div className="mt-3">
                    <div className="h-1.5 bg-stone-200 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-brand-500 rounded-full"
                        style={{ width: `${badge.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-stone-400 text-center mt-1">{badge.progress}%</p>
                  </div>
                )}

                {/* Points */}
                {badge.unlocked && (
                  <div className="mt-2 flex items-center justify-center gap-1">
                    <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />
                    <span className="text-xs font-medium text-stone-600">+{badge.points}</span>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="titles" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockTitles.map((title) => (
              <div
                key={title.id}
                className={`p-4 rounded-xl border-2 ${
                  title.unlocked 
                    ? "border-stone-200 bg-white" 
                    : "border-stone-200 bg-stone-50 opacity-60"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div 
                    className="w-12 h-12 rounded-full flex items-center justify-center"
                    style={{ backgroundColor: title.unlocked ? title.color : "#cbd5e1" }}
                  >
                    <Award className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm text-stone-500">
                      {title.prefix ? t("teach.chat") : t("test.desc")}
                    </p>
                    <p className="text-lg font-bold" style={{ color: title.unlocked ? title.color : "#94a3b8" }}>
                      {title.unlocked ? (
                        <>
                          {title.prefix && "[ "}{title.name}{title.prefix && " ]"}
                          {!title.prefix && "XXX [ "}{title.name}{!title.prefix && " ]"}
                        </>
                      ) : (
                        "???"
                      )}
                    </p>
                  </div>
                  {title.unlocked ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                  ) : (
                    <Lock className="w-5 h-5 text-stone-400" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="progress" className="space-y-4">
          <div className="space-y-4">
            {/* Category Progress */}
            {[
              { nameKey: "analytics.learning", total: 8, unlocked: 4, color: "bg-blue-500" },
              { nameKey: "analytics.practicing", total: 6, unlocked: 2, color: "bg-emerald-500" },
              { nameKey: "analytics.social", total: 5, unlocked: 2, color: "bg-purple-500" },
              { nameKey: "analytics.experiments", total: 4, unlocked: 1, color: "bg-orange-500" },
              { nameKey: "analytics.special", total: 3, unlocked: 0, color: "bg-pink-500" },
            ].map((cat) => (
              <div key={cat.nameKey} className="bg-stone-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-stone-700">{t(cat.nameKey)}</span>
                  <span className="text-sm text-stone-500">{cat.unlocked}/{cat.total}</span>
                </div>
                <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                  <div 
                    className={`h-full ${cat.color} rounded-full transition-all`}
                    style={{ width: `${(cat.unlocked / cat.total) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Badge Detail Modal */}
      <AnimatePresence>
        {selectedBadge && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
            onClick={() => setSelectedBadge(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-2xl"
              onClick={e => e.stopPropagation()}
            >
              <div className={`w-24 h-24 mx-auto mb-4 rounded-full flex items-center justify-center text-5xl bg-gradient-to-br ${tierColors[selectedBadge.tier]} shadow-xl`}>
                {selectedBadge.icon}
              </div>
              <h3 className="text-xl font-bold text-center text-stone-900 mb-2">
                {selectedBadge.name}
              </h3>
              <p className="text-stone-600 text-center mb-4">
                {selectedBadge.description}
              </p>
              <div className="flex items-center justify-center gap-4 text-sm text-stone-500">
                <span className="flex items-center gap-1">
                  <Sparkles className="w-4 h-4 text-yellow-500" />
                  {t("dashboard.totalPoints")}: {selectedBadge.points}
                </span>
                <span className="flex items-center gap-1 capitalize">
                  <Zap className="w-4 h-4" />
                  {selectedBadge.tier} {t("analytics.tier")}
                </span>
              </div>
              <Button 
                className="w-full mt-6"
                onClick={() => setSelectedBadge(null)}
              >
                {t("common.close")}
              </Button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
}
