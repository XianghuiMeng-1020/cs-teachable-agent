import { useState } from "react";
import { Card } from "@/components/ui/Card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { Button } from "@/components/ui/Button";
import { LearningPacePanel } from "@/components/analytics/LearningPacePanel";
import { CognitiveLoadPanel } from "@/components/analytics/CognitiveLoadPanel";
import { ConceptRelationGraph } from "@/components/analytics/ConceptRelationGraph";
import { LearningBehaviorDashboard } from "@/components/analytics/LearningBehaviorDashboard";
import { StreakTracker } from "@/components/gamification/StreakTracker";
import { 
  Brain, 
  Activity, 
  Network, 
  BarChart3, 
  Flame,
  Download,
  Share2,
  Sparkles
} from "lucide-react";
import { motion } from "framer-motion";

export function LearningAnalyticsPage() {
  const [activeTab, setActiveTab] = useState("overview");

  const mockUserId = 1;
  const mockTaId = 1;

  return (
    <div className="min-h-screen bg-slate-50 pb-12">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-brand-500 to-brand-600 rounded-xl">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">学习分析中心</h1>
                <p className="text-sm text-slate-500">AI驱动的学习洞察与个性化建议</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <Share2 className="w-4 h-4 mr-2" />
                分享
              </Button>
              <Button variant="outline" size="sm" className="hidden sm:flex">
                <Download className="w-4 h-4 mr-2" />
                导出报告
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="bg-white p-1 border border-slate-200 rounded-xl">
            <TabsTrigger value="overview" className="rounded-lg">
              <Activity className="w-4 h-4 mr-2" />
              总览
            </TabsTrigger>
            <TabsTrigger value="pace" className="rounded-lg">
              <Sparkles className="w-4 h-4 mr-2" />
              学习节奏
            </TabsTrigger>
            <TabsTrigger value="cognitive" className="rounded-lg">
              <Brain className="w-4 h-4 mr-2" />
              认知负荷
            </TabsTrigger>
            <TabsTrigger value="concepts" className="rounded-lg">
              <Network className="w-4 h-4 mr-2" />
              概念图谱
            </TabsTrigger>
            <TabsTrigger value="behavior" className="rounded-lg">
              <BarChart3 className="w-4 h-4 mr-2" />
              行为分析
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
                    <p className="text-2xl font-bold text-slate-900">87%</p>
                    <p className="text-sm text-slate-500">学习效率</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Brain className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-slate-900">适中</p>
                    <p className="text-sm text-slate-500">认知负荷</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-purple-100 rounded-lg">
                    <Network className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-slate-900">23</p>
                    <p className="text-sm text-slate-500">概念掌握</p>
                  </div>
                </div>
              </Card>
              <Card padding="md">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-orange-100 rounded-lg">
                    <Flame className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="text-2xl font-bold text-slate-900">12</p>
                    <p className="text-sm text-slate-500">学习天数</p>
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
                <h3 className="font-semibold text-slate-900 mb-4">节奏历史</h3>
                <div className="space-y-4">
                  {[
                    { date: "今天", pace: "适中", change: "稳定" },
                    { date: "昨天", pace: "较快", change: "+15%" },
                    { date: "前天", pace: "较慢", change: "-20%" },
                    { date: "3天前", pace: "适中", change: "稳定" },
                  ].map((item, i) => (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-slate-100 last:border-0">
                      <div>
                        <p className="font-medium text-slate-900">{item.date}</p>
                        <p className="text-sm text-slate-500">{item.pace}</p>
                      </div>
                      <span className={`text-sm font-medium ${
                        item.change === "稳定" ? "text-slate-500" :
                        item.change.startsWith("+") ? "text-emerald-600" : "text-amber-600"
                      }`}>
                        {item.change}
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
                <h3 className="font-semibold text-slate-900 mb-4">负荷分布</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">最佳学习区</span>
                      <span className="font-medium text-emerald-600">45%</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 rounded-full" style={{ width: "45%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">高负荷区</span>
                      <span className="font-medium text-orange-500">30%</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-orange-500 rounded-full" style={{ width: "30%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">认知过载</span>
                      <span className="font-medium text-red-500">10%</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                      <div className="h-full bg-red-500 rounded-full" style={{ width: "10%" }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-600">低负荷区</span>
                      <span className="font-medium text-blue-500">15%</span>
                    </div>
                    <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
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
                <h4 className="font-medium text-slate-900 mb-2">关键前置概念</h4>
                <ul className="text-sm text-slate-600 space-y-1">
                  <li>• 变量与数据类型</li>
                  <li>• 控制流基础</li>
                  <li>• 函数定义</li>
                </ul>
              </Card>
              <Card padding="md">
                <h4 className="font-medium text-slate-900 mb-2">相似概念簇</h4>
                <ul className="text-sm text-slate-600 space-y-1">
                  <li>• 列表与字典</li>
                  <li>• 循环与迭代</li>
                  <li>• 类与对象</li>
                </ul>
              </Card>
              <Card padding="md">
                <h4 className="font-medium text-slate-900 mb-2">建议学习顺序</h4>
                <ol className="text-sm text-slate-600 space-y-1">
                  <li>1. 变量 → 数据类型</li>
                  <li>2. 运算符 → 表达式</li>
                  <li>3. 条件 → 循环</li>
                </ol>
              </Card>
            </div>
          </TabsContent>

          {/* Behavior Tab */}
          <TabsContent value="behavior">
            <LearningBehaviorDashboard taId={mockTaId} userId={mockUserId} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
