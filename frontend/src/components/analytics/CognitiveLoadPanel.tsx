import { useState, useEffect } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { 
  Brain, 
  AlertTriangle, 
  CheckCircle2, 
  TrendingDown,
  TrendingUp,
  Coffee,
  Lightbulb,
  Zap,
  Minimize2,
  Maximize2,
  Activity
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface LoadIndicators {
  error_rate: number;
  response_time_increase: number;
  help_requests: number;
  pause_frequency: number;
}

interface CognitiveLoadData {
  cognitive_load_level: string;
  load_score: number;
  indicators: LoadIndicators;
  load_breakdown: {
    intrinsic: number;
    extraneous: number;
    germane: number;
  };
  recommendations: {
    action: string;
    difficulty_adjustment: number;
    break_recommended: boolean;
  };
  reduction_suggestions: string[];
}

interface CognitiveLoadPanelProps {
  studentId: number;
  className?: string;
}

export function CognitiveLoadPanel({ studentId, className }: CognitiveLoadPanelProps) {
  const [loadData, setLoadData] = useState<CognitiveLoadData | null>(null);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [showBreak, setShowBreak] = useState(false);

  // Mock monitoring
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate varying cognitive load
      const loadScore = Math.floor(Math.random() * 100);
      const level = loadScore < 20 ? "very_low" :
                    loadScore < 40 ? "low" :
                    loadScore < 60 ? "optimal" :
                    loadScore < 80 ? "high" : "overload";
      
      setLoadData({
        cognitive_load_level: level,
        load_score: loadScore,
        indicators: {
          error_rate: Math.random() * 0.3,
          response_time_increase: Math.random() * 50,
          help_requests: Math.floor(Math.random() * 5),
          pause_frequency: Math.random() * 2,
        },
        load_breakdown: {
          intrinsic: 50 + Math.random() * 20,
          extraneous: 10 + Math.random() * 20,
          germane: 20 + Math.random() * 30,
        },
        recommendations: {
          action: level === "overload" ? "立即降低认知负荷 - 休息或简化" :
                 level === "high" ? "密切监控 - 如需要请提供脚手架" :
                 level === "optimal" ? "最佳学习区域 - 继续按计划进行" :
                 level === "low" ? "保持当前节奏 - 学生感到舒适" :
                 "增加挑战 - 学生可能感到无聊",
          difficulty_adjustment: level === "overload" ? -0.3 :
                                level === "high" ? -0.1 :
                                level === "very_low" ? 0.2 : 0,
          break_recommended: level === "overload",
        },
        reduction_suggestions: level === "overload" ? [
          "🛑 立即休息5分钟",
          "📝 简化当前问题",
          "🎯 回顾前置概念",
        ] : [],
      });
      
      setShowBreak(level === "overload");
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [studentId]);

  const getLoadColor = (level: string) => {
    const colors: Record<string, string> = {
      very_low: "bg-blue-500",
      low: "bg-green-500",
      optimal: "bg-emerald-500",
      high: "bg-orange-500",
      overload: "bg-red-500",
    };
    return colors[level] || "bg-slate-500";
  };

  const getLoadStatus = (level: string) => {
    const statuses: Record<string, { icon: React.ReactNode; text: string }> = {
      very_low: { icon: <TrendingDown className="w-5 h-5" />, text: "负荷过低" },
      low: { icon: <CheckCircle2 className="w-5 h-5" />, text: "负荷较低" },
      optimal: { icon: <Zap className="w-5 h-5" />, text: "最佳学习区" },
      high: { icon: <Activity className="w-5 h-5" />, text: "负荷较高" },
      overload: { icon: <AlertTriangle className="w-5 h-5" />, text: "认知过载" },
    };
    return statuses[level] || { icon: <Brain className="w-5 h-5" />, text: "监测中" };
  };

  return (
    <>
      {/* Break Modal */}
      <AnimatePresence>
        {showBreak && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl"
            >
              <div className="flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mx-auto mb-4">
                <Coffee className="w-8 h-8 text-red-500" />
              </div>
              <h3 className="text-xl font-semibold text-center text-slate-900 mb-2">
                建议休息一下
              </h3>
              <p className="text-center text-slate-600 mb-6">
                检测到认知负荷过高，建议休息 5 分钟后再继续学习。
              </p>
              <div className="flex gap-3">
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => setShowBreak(false)}
                >
                  稍后提醒
                </Button>
                <Button 
                  className="flex-1"
                  onClick={() => setShowBreak(false)}
                >
                  知道了
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <Card padding="lg" className={className}>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Brain className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">认知负荷监测</h3>
              <p className="text-sm text-slate-500">实时追踪脑力消耗，防止过载</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isMonitoring ? "bg-green-500 animate-pulse" : "bg-slate-300"}`} />
            <span className="text-sm text-slate-500">
              {isMonitoring ? "监测中" : "已暂停"}
            </span>
          </div>
        </div>

        {loadData ? (
          <div className="space-y-6">
            {/* Main Load Meter */}
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 mb-2">
                {getLoadStatus(loadData.cognitive_load_level).icon}
                <span className="text-lg font-medium capitalize">
                  {getLoadStatus(loadData.cognitive_load_level).text}
                </span>
              </div>
              <div className="w-full max-w-xs mx-auto">
                <ProgressBar 
                  value={loadData.load_score} 
                  color={
                    loadData.cognitive_load_level === "optimal" ? "success" :
                    loadData.cognitive_load_level === "high" ? "warning" :
                    loadData.cognitive_load_level === "overload" ? "error" : "brand"
                  }
                />
              </div>
              <p className="text-2xl font-bold text-slate-900 mt-2">
                {loadData.load_score}%
              </p>
            </div>

            {/* Load Breakdown */}
            <div className="space-y-3">
              <h4 className="text-sm font-medium text-slate-700">负荷分解</h4>
              <div className="space-y-2">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-600">内在负荷 (内容复杂度)</span>
                    <span className="font-medium">{loadData.load_breakdown.intrinsic.toFixed(1)}%</span>
                  </div>
                  <ProgressBar value={loadData.load_breakdown.intrinsic} color="brand" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-600">外在负荷 (干扰因素)</span>
                    <span className="font-medium">{loadData.load_breakdown.extraneous.toFixed(1)}%</span>
                  </div>
                  <ProgressBar value={loadData.load_breakdown.extraneous} color="warning" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-600">关联负荷 (深度学习)</span>
                    <span className="font-medium">{loadData.load_breakdown.germane.toFixed(1)}%</span>
                  </div>
                  <ProgressBar value={loadData.load_breakdown.germane} color="success" />
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className={`rounded-lg p-4 ${
              loadData.cognitive_load_level === "overload" ? "bg-red-50" :
              loadData.cognitive_load_level === "high" ? "bg-amber-50" :
              loadData.cognitive_load_level === "optimal" ? "bg-emerald-50" :
              "bg-blue-50"
            }`}>
              <div className="flex items-start gap-2">
                <Lightbulb className={`w-5 h-5 mt-0.5 ${
                  loadData.cognitive_load_level === "overload" ? "text-red-500" :
                  loadData.cognitive_load_level === "high" ? "text-amber-500" :
                  loadData.cognitive_load_level === "optimal" ? "text-emerald-500" :
                  "text-blue-500"
                }`} />
                <div>
                  <p className={`font-medium ${
                    loadData.cognitive_load_level === "overload" ? "text-red-900" :
                    loadData.cognitive_load_level === "high" ? "text-amber-900" :
                    loadData.cognitive_load_level === "optimal" ? "text-emerald-900" :
                    "text-blue-900"
                  }`}>
                    {loadData.recommendations.action}
                  </p>
                </div>
              </div>
            </div>

            {/* Reduction Suggestions */}
            {loadData.reduction_suggestions.length > 0 && (
              <div className="bg-slate-50 rounded-lg p-4">
                <h4 className="font-medium text-slate-900 mb-2">降低负荷建议</h4>
                <ul className="space-y-1">
                  {loadData.reduction_suggestions.map((suggestion, i) => (
                    <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                      <span className="text-slate-400">•</span>
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-8">
            <Brain className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <p className="text-slate-500">开始监测以查看认知负荷数据</p>
            <Button 
              className="mt-4" 
              onClick={() => setIsMonitoring(true)}
            >
              开始监测
            </Button>
          </div>
        )}

        {loadData && (
          <div className="mt-4 pt-4 border-t border-slate-200">
            <Button
              variant={isMonitoring ? "outline" : "default"}
              size="sm"
              className="w-full"
              onClick={() => setIsMonitoring(!isMonitoring)}
            >
              {isMonitoring ? (
                <>
                  <Minimize2 className="w-4 h-4 mr-2" />
                  暂停监测
                </>
              ) : (
                <>
                  <Maximize2 className="w-4 h-4 mr-2" />
                  恢复监测
                </>
              )}
            </Button>
          </div>
        )}
      </Card>
    </>
  );
}
