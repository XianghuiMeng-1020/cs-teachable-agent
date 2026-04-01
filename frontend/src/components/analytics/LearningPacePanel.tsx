import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { 
  Gauge, 
  Clock, 
  Coffee, 
  Zap, 
  TrendingUp, 
  TrendingDown, 
  Activity,
  AlertCircle,
  CheckCircle2,
  Brain
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface PaceMetrics {
  time_per_concept: number;
  response_time_avg: number;
  help_requests_per_session: number;
  revision_frequency: number;
}

interface PaceData {
  pace_category: string;
  engagement_level: string;
  metrics: PaceMetrics;
  recommendations: {
    speed_multiplier: number;
    optimal_session_length: number;
    recommended_break_interval: number;
    best_learning_times: string[];
  };
  personalized_tips: string[];
}

interface LearningPacePanelProps {
  studentId: number;
  className?: string;
}

export function LearningPacePanel({ studentId, className }: LearningPacePanelProps) {
  const { t } = useTranslation();
  const [paceData, setPaceData] = useState<PaceData | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  // Mock data for demonstration
  const analyzePace = () => {
    setIsAnalyzing(true);
    setTimeout(() => {
      setPaceData({
        pace_category: "average",
        engagement_level: "active",
        metrics: {
          time_per_concept: 7.5,
          response_time_avg: 28,
          help_requests_per_session: 1.2,
          revision_frequency: 0.6,
        },
        recommendations: {
          speed_multiplier: 1.0,
          optimal_session_length: 25,
          recommended_break_interval: 25,
          best_learning_times: ["afternoon", "evening"],
        },
        personalized_tips: [
          "mastery.insightsDesc",
          "dashboard.continueTeaching",
          "teach.tips.3",
        ],
      });
      setIsAnalyzing(false);
    }, 1500);
  };

  useEffect(() => {
    analyzePace();
  }, [studentId]);

  const getPaceColor = (pace: string) => {
    const colors: Record<string, string> = {
      very_slow: "text-red-500",
      slow: "text-orange-500",
      average: "text-green-500",
      fast: "text-blue-500",
      very_fast: "text-purple-500",
    };
    return colors[pace] || "text-stone-500";
  };

  const getPaceIcon = (pace: string) => {
    if (pace.includes("slow")) return <TrendingDown className="w-5 h-5" />;
    if (pace.includes("fast")) return <TrendingUp className="w-5 h-5" />;
    return <Activity className="w-5 h-5" />;
  };

  return (
    <Card padding="lg" className={className}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-brand-100 rounded-lg">
            <Gauge className="w-5 h-5 text-brand-600" />
          </div>
          <div>
            <h3 className="font-semibold text-stone-900">{t("analytics.learningPace")}</h3>
            <p className="text-sm text-stone-500">{t("analytics.desc")}</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? t("common.back") : t("nav.overview")}
        </Button>
      </div>

      {isAnalyzing ? (
        <div className="flex items-center justify-center py-8">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          >
            <Brain className="w-8 h-8 text-brand-500" />
          </motion.div>
          <span className="ml-3 text-stone-600">{t("common.loading")}</span>
        </div>
      ) : paceData ? (
        <div className="space-y-6">
          {/* Main Status */}
          <div className="flex items-center justify-center py-4">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-center"
            >
              <div className={`flex items-center justify-center gap-2 ${getPaceColor(paceData.pace_category)}`}>
                {getPaceIcon(paceData.pace_category)}
                <span className="text-2xl font-bold capitalize">
                  {paceData.pace_category === "very_slow" && t("analytics.slow")}
                  {paceData.pace_category === "slow" && t("analytics.slow")}
                  {paceData.pace_category === "average" && t("analytics.medium")}
                  {paceData.pace_category === "fast" && t("analytics.fast")}
                  {paceData.pace_category === "very_fast" && t("analytics.fast")}
                </span>
              </div>
              <p className="text-sm text-stone-500 mt-1">
                {t("analytics.engagement")}: <span className="capitalize">{paceData.engagement_level}</span>
              </p>
            </motion.div>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-stone-50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-stone-600 mb-1">
                <Clock className="w-4 h-4" />
                <span className="text-sm">{t("analytics.timePerConcept")}</span>
              </div>
              <p className="text-lg font-semibold text-stone-900">
                {paceData.metrics.time_per_concept} {t("analytics.minutes")}
              </p>
            </div>
            <div className="bg-stone-50 rounded-lg p-3">
              <div className="flex items-center gap-2 text-stone-600 mb-1">
                <Zap className="w-4 h-4" />
                <span className="text-sm">{t("analytics.avgSessionTime")}</span>
              </div>
              <p className="text-lg font-semibold text-stone-900">
                {paceData.metrics.response_time_avg}
              </p>
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-brand-50 rounded-lg p-4">
            <h4 className="font-medium text-brand-900 mb-3 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              {t("analytics.recommendation")}
            </h4>
            <ul className="space-y-2">
              {paceData.personalized_tips.map((tipKey, i) => (
                <motion.li
                  key={i}
                  initial={{ x: -10, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-start gap-2 text-sm text-brand-800"
                >
                  <span className="text-brand-500 mt-0.5">•</span>
                  {t(tipKey)}
                </motion.li>
              ))}
            </ul>
          </div>

          {/* Detailed View */}
          <AnimatePresence>
            {showDetails && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden"
              >
                <div className="border-t border-stone-200 pt-4 space-y-4">
                  <h4 className="font-medium text-stone-900">{t("analytics.paceHistory")}</h4>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm text-stone-500">{t("analytics.avgSessionTime")}</label>
                      <div className="flex items-center gap-2">
                        <Clock className="w-4 h-4 text-brand-500" />
                        <span className="font-medium">{paceData.recommendations.optimal_session_length} {t("analytics.minutes")}</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm text-stone-500">{t("analytics.recommendation")}</label>
                      <div className="flex items-center gap-2">
                        <Coffee className="w-4 h-4 text-brand-500" />
                        <span className="font-medium">{paceData.recommendations.recommended_break_interval} {t("analytics.minutes")}</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm text-stone-500">{t("analytics.bestLearningTime")}</label>
                    <div className="flex gap-2">
                      {paceData.recommendations.best_learning_times.map((time) => (
                        <span
                          key={time}
                          className="px-3 py-1 bg-brand-100 text-brand-700 rounded-full text-sm capitalize"
                        >
                          {time === "morning" && t("analytics.morning")}
                          {time === "afternoon" && t("analytics.afternoon")}
                          {time === "evening" && t("analytics.evening")}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="bg-amber-50 rounded-lg p-3 flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-500 mt-0.5" />
                    <p className="text-sm text-amber-800">
                      {t("mastery.insightsDesc")}
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ) : null}
    </Card>
  );
}
