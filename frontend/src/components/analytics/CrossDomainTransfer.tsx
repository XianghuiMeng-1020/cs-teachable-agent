import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { 
  ArrowRight, 
  Zap, 
  Clock, 
  AlertTriangle,
  CheckCircle2,
  Brain,
  Target,
  TrendingUp,
  Lightbulb,
  ArrowRightLeft,
  Code,
  Database,
  Cpu
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ConceptMapping {
  source: string;
  target: string;
  type: string;
  strength: number;
  explanationKey: string;
}

interface TransferData {
  acceleration_factor: number;
  estimated_time_saved_hours: number;
  transferable_concepts: ConceptMapping[];
  recommended_sequence: string[];
  potential_pitfalls: string[];
}

interface TransferReadiness {
  source_mastery: number;
  transfer_readiness: number;
  transferable_skills: string[];
  gaps_to_address: string[];
  recommendations: string[];
}

const domains = [
  { id: "python", nameKey: "landing.python", icon: Code, color: "bg-blue-500" },
  { id: "database", nameKey: "landing.database", icon: Database, color: "bg-green-500" },
  { id: "ai_literacy", nameKey: "landing.aiLiteracy", icon: Cpu, color: "bg-purple-500" },
] as const;

const mockTransferData: TransferData = {
  acceleration_factor: 1.8,
  estimated_time_saved_hours: 18,
  transferable_concepts: [
    { source: "Variables", target: "Columns", type: "direct", strength: 4, explanationKey: "teach.tips.1" },
    { source: "Conditionals", target: "WHERE Clause", type: "direct", strength: 4, explanationKey: "teach.tips.2" },
    { source: "Lists", target: "Tables", type: "analogical", strength: 3, explanationKey: "teach.tips.3" },
    { source: "Functions", target: "Stored Procedures", type: "analogical", strength: 3, explanationKey: "teach.tips.4" },
  ],
  recommended_sequence: [
    "teach.tips.1",
    "teach.tips.2",
    "dashboard.gettingStartedDesc",
    "mastery.insightsDesc",
    "analytics.desc",
  ],
  potential_pitfalls: [
    "test.readyDesc",
    "test.readyHint",
    "mastery.addressMisconceptionsDesc",
  ],
};

const mockReadiness: TransferReadiness = {
  source_mastery: 0.75,
  transfer_readiness: 0.82,
  transferable_skills: ["Variables", "Conditionals", "Loops", "Functions"],
  gaps_to_address: ["Advanced data structures", "Error handling"],
  recommendations: [
    "mastery.excellentProgressDesc",
    "dashboard.continueTeaching",
    "teach.desc",
  ],
};

export function CrossDomainTransfer({ className }: { className?: string }) {
  const { t } = useTranslation();
  const [sourceDomain, setSourceDomain] = useState("python");
  const [targetDomain, setTargetDomain] = useState("database");
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const handleAnalyze = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setAnalyzing(false);
      setShowAnalysis(true);
    }, 1500);
  };

  const canTransfer = sourceDomain !== targetDomain;

  return (
    <Card padding="lg" className={className}>
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg">
          <ArrowRightLeft className="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 className="font-semibold text-stone-900">{t("analytics.crossDomainTitle")}</h3>
          <p className="text-sm text-stone-500">{t("analytics.desc")}</p>
        </div>
      </div>

      {/* Domain Selection */}
      <div className="bg-stone-50 rounded-xl p-4 mb-6">
        <div className="flex flex-col md:flex-row items-center gap-4">
          {/* Source Domain */}
          <div className="flex-1 w-full">
            <label className="text-sm font-medium text-stone-700 mb-2 block">{t("mastery.mastered")}</label>
            <div className="grid grid-cols-3 gap-2">
              {domains.map(domain => (
                <button
                  key={domain.id}
                  onClick={() => { setSourceDomain(domain.id); setShowAnalysis(false); }}
                  className={`p-3 rounded-lg border-2 text-center transition-all ${
                    sourceDomain === domain.id
                      ? `border-${domain.color.replace('bg-', '')} bg-white shadow-md`
                      : "border-transparent bg-white hover:bg-stone-100"
                  }`}
                >
                  <domain.icon className={`w-6 h-6 mx-auto mb-1 ${domain.color.replace('bg-', 'text-')}`} />
                  <p className="text-xs font-medium text-stone-700">{t(domain.nameKey)}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Arrow */}
          <div className="flex items-center justify-center">
            <ArrowRight className="w-6 h-6 text-stone-400 md:block hidden" />
            <ArrowRight className="w-6 h-6 text-stone-400 md:hidden rotate-90" />
          </div>

          {/* Target Domain */}
          <div className="flex-1 w-full">
            <label className="text-sm font-medium text-stone-700 mb-2 block">{t("mastery.nextObjectives")}</label>
            <div className="grid grid-cols-3 gap-2">
              {domains.map(domain => (
                <button
                  key={domain.id}
                  onClick={() => { setTargetDomain(domain.id); setShowAnalysis(false); }}
                  disabled={domain.id === sourceDomain}
                  className={`p-3 rounded-lg border-2 text-center transition-all ${
                    targetDomain === domain.id
                      ? `border-${domain.color.replace('bg-', '')} bg-white shadow-md`
                      : domain.id === sourceDomain
                      ? "border-transparent bg-stone-100 opacity-50 cursor-not-allowed"
                      : "border-transparent bg-white hover:bg-stone-100"
                  }`}
                >
                  <domain.icon className={`w-6 h-6 mx-auto mb-1 ${domain.id === sourceDomain ? 'text-stone-400' : domain.color.replace('bg-', 'text-')}`} />
                  <p className="text-xs font-medium text-stone-700">{t(domain.nameKey)}</p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Analyze Button */}
        <Button
          className="w-full mt-4"
          disabled={!canTransfer || analyzing}
          onClick={handleAnalyze}
        >
          {analyzing ? (
            <>
              <Brain className="w-4 h-4 mr-2 animate-pulse" />
              {t("common.loading")}
            </>
          ) : (
            <>
              <Zap className="w-4 h-4 mr-2" />
              {t("analytics.crossDomainTitle")}
            </>
          )}
        </Button>
      </div>

      {/* Analysis Results */}
      <AnimatePresence>
        {showAnalysis && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="space-y-6"
          >
            {/* Readiness Score */}
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-4 border border-indigo-100">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Target className="w-5 h-5 text-indigo-600" />
                  <span className="font-semibold text-indigo-900">{t("analytics.crossDomainTitle")}</span>
                </div>
                <span className="text-2xl font-bold text-indigo-600">
                  {Math.round(mockReadiness.transfer_readiness * 100)}%
                </span>
              </div>
              <ProgressBar value={mockReadiness.transfer_readiness * 100} color="brand" />
              <p className="text-sm text-indigo-700 mt-2">
                {t("analytics.crossDomainDesc", {
                  domain: t(domains.find((d) => d.id === sourceDomain)?.nameKey ?? "landing.python"),
                })}
              </p>
            </div>

            {/* Acceleration Factor */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-5 h-5 text-emerald-600" />
                  <span className="font-medium text-emerald-900">{t("analytics.improving")}</span>
                </div>
                <p className="text-3xl font-bold text-emerald-600">
                  {mockTransferData.acceleration_factor}x
                </p>
                <p className="text-xs text-emerald-700">{t("analytics.learningEfficiency")}</p>
              </div>
              <div className="bg-amber-50 rounded-lg p-4 border border-amber-200">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-5 h-5 text-amber-600" />
                  <span className="font-medium text-amber-900">{t("analytics.avgSessionTime")}</span>
                </div>
                <p className="text-3xl font-bold text-amber-600">
                  {mockTransferData.estimated_time_saved_hours}h
                </p>
                <p className="text-xs text-amber-700">{t("dashboard.learningActivity")}</p>
              </div>
            </div>

            {/* Transferable Concepts */}
            <div>
              <h4 className="font-semibold text-stone-900 mb-3 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-500" />
                {t("analytics.conceptRelations")} ({mockTransferData.transferable_concepts.length})
              </h4>
              <div className="space-y-2">
                {mockTransferData.transferable_concepts.map((concept, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-center gap-3 p-3 bg-stone-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium text-stone-900">{concept.source}</span>
                        <ArrowRight className="w-4 h-4 text-stone-400" />
                        <span className="font-medium text-brand-600">{concept.target}</span>
                      </div>
                      <p className="text-xs text-stone-500">{t(concept.explanationKey)}</p>
                    </div>
                    <div className="flex items-center gap-1">
                      {[...Array(concept.strength)].map((_, j) => (
                        <Zap key={j} className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                      ))}
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Recommended Sequence */}
            <div>
              <h4 className="font-semibold text-stone-900 mb-3">{t("mastery.nextObjectives")}</h4>
              <ol className="space-y-2">
                {mockTransferData.recommended_sequence.map((stepKey, i) => (
                  <li key={i} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                    <span className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium shrink-0">
                      {i + 1}
                    </span>
                    <span className="text-sm text-stone-700">{t(stepKey)}</span>
                  </li>
                ))}
              </ol>
            </div>

            {/* Pitfalls */}
            <div className="bg-amber-50 rounded-lg p-4 border border-amber-200">
              <h4 className="font-semibold text-amber-900 mb-2 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                {t("dashboard.needsAttention")}
              </h4>
              <ul className="space-y-1">
                {mockTransferData.potential_pitfalls.map((pitfallKey, i) => (
                  <li key={i} className="text-sm text-amber-800 flex items-start gap-2">
                    <span>•</span>
                    {t(pitfallKey, { count: 1 })}
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommendations */}
            <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
              <h4 className="font-semibold text-emerald-900 mb-2 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                {t("analytics.recommendation")}
              </h4>
              <ul className="space-y-1">
                {mockReadiness.recommendations.map((recKey, i) => (
                  <li key={i} className="text-sm text-emerald-800 flex items-start gap-2">
                    <span>•</span>
                    {t(recKey, { rate: 82 })}
                  </li>
                ))}
              </ul>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </Card>
  );
}
