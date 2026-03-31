import { useState } from "react";
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
  explanation: string;
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
  { id: "python", name: "Python", icon: Code, color: "bg-blue-500", description: "编程基础" },
  { id: "database", name: "Database", icon: Database, color: "bg-green-500", description: "数据处理" },
  { id: "ai_literacy", name: "AI Literacy", icon: Cpu, color: "bg-purple-500", description: "人工智能" },
];

const mockTransferData: TransferData = {
  acceleration_factor: 1.8,
  estimated_time_saved_hours: 18,
  transferable_concepts: [
    { source: "Variables", target: "Columns", type: "direct", strength: 4, explanation: "Both store data values" },
    { source: "Conditionals", target: "WHERE Clause", type: "direct", strength: 4, explanation: "Filter logic applies to both" },
    { source: "Lists", target: "Tables", type: "analogical", strength: 3, explanation: "Collections of items/rows" },
    { source: "Functions", target: "Stored Procedures", type: "analogical", strength: 3, explanation: "Reusable logic blocks" },
  ],
  recommended_sequence: [
    "Review Python variables and data types",
    "Learn SQL column types",
    "Understand WHERE clause filtering",
    "Practice JOIN operations (like nested loops)",
    "Master aggregate functions",
  ],
  potential_pitfalls: [
    "SQL is declarative, not imperative",
    "Data persists beyond session (unlike variables)",
    "Don't over-rely on procedural thinking",
  ],
};

const mockReadiness: TransferReadiness = {
  source_mastery: 0.75,
  transfer_readiness: 0.82,
  transferable_skills: ["Variables", "Conditionals", "Loops", "Functions"],
  gaps_to_address: ["Advanced data structures", "Error handling"],
  recommendations: [
    "Excellent readiness! Start learning SQL basics",
    "Your Python foundation is strong for database concepts",
    "Focus on understanding declarative vs imperative paradigms",
  ],
};

export function CrossDomainTransfer({ className }: { className?: string }) {
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
          <h3 className="font-semibold text-stone-900">跨领域知识迁移</h3>
          <p className="text-sm text-stone-500">发现并利用你的知识储备加速学习</p>
        </div>
      </div>

      {/* Domain Selection */}
      <div className="bg-stone-50 rounded-xl p-4 mb-6">
        <div className="flex flex-col md:flex-row items-center gap-4">
          {/* Source Domain */}
          <div className="flex-1 w-full">
            <label className="text-sm font-medium text-stone-700 mb-2 block">已掌握领域</label>
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
                  <p className="text-xs font-medium text-stone-700">{domain.name}</p>
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
            <label className="text-sm font-medium text-stone-700 mb-2 block">目标领域</label>
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
                  <p className="text-xs font-medium text-stone-700">{domain.name}</p>
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
              分析迁移潜力中...
            </>
          ) : (
            <>
              <Zap className="w-4 h-4 mr-2" />
              分析知识迁移
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
                  <span className="font-semibold text-indigo-900">迁移准备度</span>
                </div>
                <span className="text-2xl font-bold text-indigo-600">
                  {Math.round(mockReadiness.transfer_readiness * 100)}%
                </span>
              </div>
              <ProgressBar value={mockReadiness.transfer_readiness * 100} color="brand" />
              <p className="text-sm text-indigo-700 mt-2">
                基于你在{domains.find(d => d.id === sourceDomain)?.name}领域的掌握程度
              </p>
            </div>

            {/* Acceleration Factor */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-5 h-5 text-emerald-600" />
                  <span className="font-medium text-emerald-900">学习加速</span>
                </div>
                <p className="text-3xl font-bold text-emerald-600">
                  {mockTransferData.acceleration_factor}x
                </p>
                <p className="text-xs text-emerald-700">比从零开始快</p>
              </div>
              <div className="bg-amber-50 rounded-lg p-4 border border-amber-200">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-5 h-5 text-amber-600" />
                  <span className="font-medium text-amber-900">预计节省</span>
                </div>
                <p className="text-3xl font-bold text-amber-600">
                  {mockTransferData.estimated_time_saved_hours}h
                </p>
                <p className="text-xs text-amber-700">学习时间</p>
              </div>
            </div>

            {/* Transferable Concepts */}
            <div>
              <h4 className="font-semibold text-stone-900 mb-3 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-yellow-500" />
                可迁移概念 ({mockTransferData.transferable_concepts.length})
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
                      <p className="text-xs text-stone-500">{concept.explanation}</p>
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
              <h4 className="font-semibold text-stone-900 mb-3">推荐学习路径</h4>
              <ol className="space-y-2">
                {mockTransferData.recommended_sequence.map((step, i) => (
                  <li key={i} className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                    <span className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-medium shrink-0">
                      {i + 1}
                    </span>
                    <span className="text-sm text-stone-700">{step}</span>
                  </li>
                ))}
              </ol>
            </div>

            {/* Pitfalls */}
            <div className="bg-amber-50 rounded-lg p-4 border border-amber-200">
              <h4 className="font-semibold text-amber-900 mb-2 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5" />
                注意事项
              </h4>
              <ul className="space-y-1">
                {mockTransferData.potential_pitfalls.map((pitfall, i) => (
                  <li key={i} className="text-sm text-amber-800 flex items-start gap-2">
                    <span>•</span>
                    {pitfall}
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommendations */}
            <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
              <h4 className="font-semibold text-emerald-900 mb-2 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5" />
                建议
              </h4>
              <ul className="space-y-1">
                {mockReadiness.recommendations.map((rec, i) => (
                  <li key={i} className="text-sm text-emerald-800 flex items-start gap-2">
                    <span>•</span>
                    {rec}
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
