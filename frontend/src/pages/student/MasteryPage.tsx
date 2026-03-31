import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useAppStore } from "@/stores/appStore";
import { getState, getMastery } from "@/api/client";
import { Card } from "@/components/ui/Card";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import type { UnitNode } from "@/components/state/KnowledgeGraph";
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Cell,
  PieChart, Pie
} from "recharts";
import { KU_DISPLAY_NAMES } from "@/lib/constants";
import { 
  Award, BookOpen, Target, TrendingUp, Zap, Brain, 
  CheckCircle2, AlertCircle, Clock, GraduationCap,
} from "lucide-react";

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

export function MasteryPage() {
  const currentTaId = useAppStore((s) => s.currentTaId);

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

  const defs = (state as { knowledge_unit_definitions?: { id: string; name?: string }[] })?.knowledge_unit_definitions;
  const nameById = defs ? Object.fromEntries(defs.map((d) => [d.id, d.name ?? d.id])) : {};

  const units: UnitNode[] = state?.units
    ? Object.entries(state.units).map(([unit_id, rec]) => ({
        unit_id,
        status: (rec as { status?: string }).status as UnitNode["status"] ?? "unknown",
        topic_group: (rec as { topic_group?: string }).topic_group ?? defs?.find((d: { id: string; topic_group?: string }) => d.id === unit_id)?.topic_group,
      }))
    : [];

  const learnedCount = units.filter((u) => u.status === "learned").length;
  const partialCount = units.filter((u) => u.status === "partially_learned").length;
  const misconceptionCount = units.filter((u) => u.status === "misconception").length;
  const unknownCount = units.filter((u) => u.status === "unknown").length;

  const progressPercent = units.length > 0 ? Math.round((learnedCount / units.length) * 100) : 0;
  const passRate = mastery?.pass_rate ? Math.round(mastery.pass_rate * 100) : 0;

  // Bar chart data
  const barData = units.map((u) => ({
    name: nameById[u.unit_id] ?? KU_DISPLAY_NAMES[u.unit_id] ?? u.unit_id,
    mastery: u.status === "learned" ? 100 : u.status === "partially_learned" ? 50 : u.status === "misconception" ? 25 : 0,
    fill: u.status === "learned" ? "#10B981" : u.status === "partially_learned" ? "#F59E0B" : u.status === "misconception" ? "#EF4444" : "#E5E7EB",
    status: u.status,
  }));

  // Radar chart data by topic
  const byTopicGroup = units.reduce<Record<string, { learned: number; partial: number; misconception: number; total: number }>>((acc, u) => {
    const g = u.topic_group ?? "Other";
    if (!acc[g]) acc[g] = { learned: 0, partial: 0, misconception: 0, total: 0 };
    acc[g].total += 1;
    if (u.status === "learned") acc[g].learned += 1;
    else if (u.status === "partially_learned") acc[g].partial += 1;
    else if (u.status === "misconception") acc[g].misconception += 1;
    return acc;
  }, {});
  
  const radarData = Object.entries(byTopicGroup).map(([subject, v]) => ({
    subject: subject.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase()),
    value: v.total ? Math.round(((v.learned + v.partial * 0.5) / v.total) * 100) : 0,
    fullMark: 100,
  }));

  if (radarData.length === 0) {
    radarData.push({ subject: "Knowledge", value: 0, fullMark: 100 });
  }

  // Pie chart data
  const pieData = [
    { name: "Mastered", value: learnedCount, color: "#10B981" },
    { name: "In Progress", value: partialCount, color: "#F59E0B" },
    { name: "Misconceptions", value: misconceptionCount, color: "#EF4444" },
    { name: "Not Started", value: unknownCount, color: "#E5E7EB" },
  ].filter(d => d.value > 0);

  return (
    <motion.div 
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      className="space-y-6"
    >
      {/* Header */}
      <motion.div variants={fadeIn} className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shadow-lg">
            <Award className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-stone-900">Mastery Overview</h1>
            <p className="text-sm text-stone-500">
              Track your learning progress and knowledge state visualization
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-brand-50 to-emerald-50 rounded-full border border-brand-200">
          <GraduationCap className="w-5 h-5 text-brand-600" />
          <span className="text-sm font-semibold text-brand-800">
            {learnedCount} of {units.length} concepts mastered ({progressPercent}%)
          </span>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <motion.div variants={fadeIn} className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{learnedCount}</div>
          </div>
          <div className="text-sm text-stone-500">Mastered</div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Clock className="w-5 h-5 text-amber-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{partialCount}</div>
          </div>
          <div className="text-sm text-stone-500">In Progress</div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-rose-100 flex items-center justify-center">
              <AlertCircle className="w-5 h-5 text-rose-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{misconceptionCount}</div>
          </div>
          <div className="text-sm text-stone-500">Misconceptions</div>
        </div>

        <div className="bg-white rounded-xl p-4 border border-stone-200 shadow-sm">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <Target className="w-5 h-5 text-blue-600" />
            </div>
            <div className="text-2xl font-bold text-stone-900">{passRate}%</div>
          </div>
          <div className="text-sm text-stone-500">Test Pass Rate</div>
        </div>
      </motion.div>

      {/* Knowledge Graph */}
      <motion.div variants={fadeIn}>
        <Card padding="lg" className="overflow-hidden">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center">
                <Brain className="w-5 h-5 text-violet-600" />
              </div>
              <div>
                <h2 className="text-lg font-bold text-stone-900">Knowledge Graph</h2>
                <p className="text-sm text-stone-500">Visual representation of your agent's knowledge state</p>
              </div>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-emerald-500" />
                <span className="text-stone-600">Learned</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-amber-500" />
                <span className="text-stone-600">Partial</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-rose-500" />
                <span className="text-stone-600">Misconception</span>
              </div>
              <div className="flex items-center gap-1.5">
                <div className="w-3 h-3 rounded-full bg-stone-300" />
                <span className="text-stone-600">Unknown</span>
              </div>
            </div>
          </div>
          <KnowledgeGraph
            units={units}
            knowledgeUnitDefinitions={defs ?? undefined}
            className="min-h-[400px]"
          />
        </Card>
      </motion.div>

      {/* Charts Grid */}
      <motion.div variants={fadeIn} className="grid gap-6 lg:grid-cols-3">
        {/* Per Concept Bar Chart */}
        <Card padding="lg" className="lg:col-span-2">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-stone-900">Concept Mastery</h2>
              <p className="text-sm text-stone-500">Mastery level for each knowledge unit</p>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} layout="vertical" margin={{ left: 120, right: 20 }}>
                <XAxis 
                  type="number" 
                  domain={[0, 100]} 
                  tick={{ fontSize: 11, fill: "#78716C" }} 
                  axisLine={false} 
                  tickLine={false} 
                />
                <YAxis 
                  type="category" 
                  dataKey="name" 
                  width={110} 
                  tick={{ fontSize: 11, fill: "#57534E" }} 
                  axisLine={false} 
                  tickLine={false} 
                />
                <Tooltip 
                  contentStyle={{ 
                    borderRadius: "8px", 
                    border: "1px solid #E7E5E4", 
                    fontSize: "12px",
                    boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)"
                  }}
                  formatter={(value: any, name: any, props: any) => {
                    const status = props.payload.status;
                    const label = status === "learned" ? "Mastered" : status === "partially_learned" ? "In Progress" : status === "misconception" ? "Misconception" : "Unknown";
                    return [`${value}%`, label];
                  }}
                />
                <Bar dataKey="mastery" radius={[0, 4, 4, 0]} barSize={20}>
                  {barData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Distribution Pie Chart */}
        <Card padding="lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <Zap className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-stone-900">Distribution</h2>
              <p className="text-sm text-stone-500">Knowledge state breakdown</p>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    borderRadius: "8px", 
                    border: "1px solid #E7E5E4", 
                    fontSize: "12px" 
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-stone-600">{item.name}</span>
                </div>
                <span className="font-semibold text-stone-900">{item.value}</span>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* Topic Coverage Radar */}
      <motion.div variants={fadeIn}>
        <Card padding="lg">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
              <Target className="w-5 h-5 text-teal-600" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-stone-900">Topic Coverage</h2>
              <p className="text-sm text-stone-500">Mastery distribution across topic groups</p>
            </div>
          </div>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#E7E5E4" />
                <PolarAngleAxis 
                  dataKey="subject" 
                  tick={{ fontSize: 12, fill: "#57534E", fontWeight: 500 }} 
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]} 
                  tick={{ fontSize: 10, fill: "#A8A29E" }} 
                />
                <Radar 
                  name="Mastery" 
                  dataKey="value" 
                  stroke="#8B5CF6" 
                  fill="#8B5CF6" 
                  fillOpacity={0.25}
                  strokeWidth={2}
                />
                <Tooltip 
                  contentStyle={{ 
                    borderRadius: "8px", 
                    border: "1px solid #E7E5E4", 
                    fontSize: "12px" 
                  }}
                  formatter={(value: number) => [`${value}%`, "Mastery"]}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </motion.div>

      {/* Learning Insights */}
      <motion.div variants={fadeIn}>
        <Card padding="lg" className="bg-gradient-to-br from-brand-50 to-emerald-50 border-brand-200">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-white flex items-center justify-center shadow-sm">
              <BookOpen className="w-6 h-6 text-brand-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold text-stone-900 mb-2">Learning Insights</h3>
              <p className="text-stone-600 mb-4">
                Based on your current progress, here are some recommendations:
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                {misconceptionCount > 0 && (
                  <div className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm">
                    <AlertCircle className="w-5 h-5 text-rose-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-medium text-stone-900">Address Misconceptions</div>
                      <div className="text-sm text-stone-500">
                        You have {misconceptionCount} active misconceptions. Focus on correcting these first.
                      </div>
                    </div>
                  </div>
                )}
                {partialCount > 0 && (
                  <div className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm">
                    <Clock className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-medium text-stone-900">Continue In-Progress</div>
                      <div className="text-sm text-stone-500">
                        {partialCount} concepts are partially learned. Keep teaching to master them.
                      </div>
                    </div>
                  </div>
                )}
                {unknownCount > 0 && (
                  <div className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm">
                    <Zap className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-medium text-stone-900">Explore New Concepts</div>
                      <div className="text-sm text-stone-500">
                        {unknownCount} concepts are waiting. Start teaching to expand your knowledge.
                      </div>
                    </div>
                  </div>
                )}
                {learnedCount > 0 && passRate >= 80 && (
                  <div className="flex items-start gap-3 p-3 bg-white rounded-lg shadow-sm">
                    <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <div className="font-medium text-stone-900">Excellent Progress!</div>
                      <div className="text-sm text-stone-500">
                        Your {passRate}% pass rate shows strong understanding. Keep it up!
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
    </motion.div>
  );
}
