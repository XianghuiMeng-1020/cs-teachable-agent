import { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
  Scatter,
  ScatterChart,
  ZAxis,
} from "recharts";
import {
  Activity,
  TrendingUp,
  Clock,
  Target,
  Calendar,
  BookOpen,
  Zap,
  BarChart3,
  PieChart as PieChartIcon,
  Filter,
  Download,
  Share2,
  AlertCircle,
  CheckCircle,
  Brain,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";

interface LearningBehaviorDashboardProps {
  taId: number;
  userId?: number;
}

const COLORS = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];

// Mock data generator for demonstration
const generateMockData = () => {
  const days = 30;
  const dailyData = Array.from({ length: days }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (days - i - 1));
    
    return {
      date: date.toISOString().split("T")[0],
      day: date.getDate(),
      conceptsLearned: Math.floor(Math.random() * 4),
      testsTaken: Math.floor(Math.random() * 3),
      learningTime: Math.floor(Math.random() * 60) + 10,
      masteryScore: Math.min(100, Math.floor(Math.random() * 30) + 50 + i * 1.5),
      engagement: Math.floor(Math.random() * 40) + 60,
    };
  });
  
  const conceptDistribution = [
    { name: "Variables", value: 25, mastery: 0.8 },
    { name: "Loops", value: 20, mastery: 0.65 },
    { name: "Functions", value: 18, mastery: 0.5 },
    { name: "Conditionals", value: 15, mastery: 0.75 },
    { name: "Lists", value: 12, mastery: 0.4 },
    { name: "Dictionaries", value: 10, mastery: 0.3 },
  ];
  
  const timeOfDayData = [
    { hour: "6-9 AM", sessions: 5, avgDuration: 25 },
    { hour: "9-12 PM", sessions: 12, avgDuration: 35 },
    { hour: "12-3 PM", sessions: 8, avgDuration: 30 },
    { hour: "3-6 PM", sessions: 15, avgDuration: 40 },
    { hour: "6-9 PM", sessions: 20, avgDuration: 45 },
    { hour: "9-12 AM", sessions: 10, avgDuration: 30 },
  ];
  
  const learningPatterns = [
    { subject: "Speed", A: 80, fullMark: 100 },
    { subject: "Consistency", A: 70, fullMark: 100 },
    { subject: "Mastery", A: 65, fullMark: 100 },
    { subject: "Engagement", A: 85, fullMark: 100 },
    { subject: "Help Seeking", A: 60, fullMark: 100 },
    { subject: "Review", A: 75, fullMark: 100 },
  ];
  
  return {
    dailyData,
    conceptDistribution,
    timeOfDayData,
    learningPatterns,
    summary: {
      totalLearningTime: dailyData.reduce((a, b) => a + b.learningTime, 0),
      totalConcepts: dailyData.reduce((a, b) => a + b.conceptsLearned, 0),
      avgMastery: dailyData[dailyData.length - 1].masteryScore,
      streakDays: 12,
      consistency: 0.78,
    },
  };
};

export function LearningBehaviorDashboard({ taId, userId }: LearningBehaviorDashboardProps) {
  const [timeRange, setTimeRange] = useState<"7d" | "30d" | "90d">("30d");
  const [activeTab, setActiveTab] = useState("overview");
  
  // In production, this would be an API call
  const data = useMemo(() => generateMockData(), []);
  
  const { summary, dailyData, conceptDistribution, timeOfDayData, learningPatterns } = data;
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 flex items-center gap-2">
            <Activity className="w-6 h-6 text-brand-600" />
            Learning Behavior Analytics
          </h2>
          <p className="text-slate-500 mt-1">
            Deep insights into your learning patterns and progress
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as any)}
            className="px-3 py-2 border border-slate-200 rounded-lg text-sm"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
          </select>
          
          <Button variant="outline" size="sm" icon={Download}>
            Export
          </Button>
        </div>
      </div>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card padding="md" className="bg-gradient-to-br from-brand-50 to-brand-100">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-600">Total Learning Time</p>
              <p className="text-2xl font-bold text-slate-900">
                {Math.floor(summary.totalLearningTime / 60)}h {summary.totalLearningTime % 60}m
              </p>
            </div>
            <div className="p-2 bg-white rounded-lg">
              <Clock className="w-5 h-5 text-brand-600" />
            </div>
          </div>
          <div className="flex items-center gap-1 mt-2 text-sm">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-emerald-600">+15%</span>
            <span className="text-slate-500">vs last period</span>
          </div>
        </Card>
        
        <Card padding="md" className="bg-gradient-to-br from-emerald-50 to-emerald-100">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-600">Concepts Mastered</p>
              <p className="text-2xl font-bold text-slate-900">{summary.totalConcepts}</p>
            </div>
            <div className="p-2 bg-white rounded-lg">
              <BookOpen className="w-5 h-5 text-emerald-600" />
            </div>
          </div>
          <div className="flex items-center gap-1 mt-2 text-sm">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-emerald-600">+8</span>
            <span className="text-slate-500">new this week</span>
          </div>
        </Card>
        
        <Card padding="md" className="bg-gradient-to-br from-amber-50 to-amber-100">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-600">Average Mastery</p>
              <p className="text-2xl font-bold text-slate-900">{summary.avgMastery.toFixed(1)}%</p>
            </div>
            <div className="p-2 bg-white rounded-lg">
              <Target className="w-5 h-5 text-amber-600" />
            </div>
          </div>
          <div className="flex items-center gap-1 mt-2 text-sm">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-emerald-600">+5.2%</span>
            <span className="text-slate-500">improvement</span>
          </div>
        </Card>
        
        <Card padding="md" className="bg-gradient-to-br from-purple-50 to-purple-100">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-sm text-slate-600">Current Streak</p>
              <p className="text-2xl font-bold text-slate-900">{summary.streakDays} days</p>
            </div>
            <div className="p-2 bg-white rounded-lg">
              <Zap className="w-5 h-5 text-purple-600" />
            </div>
          </div>
          <div className="flex items-center gap-1 mt-2 text-sm">
            <CheckCircle className="w-4 h-4 text-purple-500" />
            <span className="text-purple-600">{Math.round(summary.consistency * 100)}%</span>
            <span className="text-slate-500">consistency</span>
          </div>
        </Card>
      </div>
      
      {/* Main Dashboard Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4 lg:w-auto">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="concepts">Concepts</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>
        
        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Learning Progress Over Time */}
          <Card padding="lg">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">Learning Progress Over Time</h3>
                <p className="text-sm text-slate-500">Concepts learned and mastery progression</p>
              </div>
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-brand-500 rounded-full" />
                  <span className="text-slate-600">Mastery Score</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-emerald-500 rounded-full" />
                  <span className="text-slate-600">Concepts</span>
                </div>
              </div>
            </div>
            
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={dailyData}>
                  <XAxis 
                    dataKey="day" 
                    tick={{ fontSize: 12 }}
                    tickFormatter={(value) => `${value}`}
                  />
                  <YAxis yAxisId="left" tick={{ fontSize: 12 }} />
                  <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Area
                    yAxisId="left"
                    type="monotone"
                    dataKey="masteryScore"
                    stroke="#6366f1"
                    fill="#6366f1"
                    fillOpacity={0.2}
                    strokeWidth={2}
                    name="Mastery Score"
                  />
                  <Bar
                    yAxisId="right"
                    dataKey="conceptsLearned"
                    fill="#10b981"
                    name="Concepts Learned"
                    radius={[4, 4, 0, 0]}
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </Card>
          
          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Engagement Trend */}
            <Card padding="lg">
              <h3 className="text-lg font-semibold text-slate-900 mb-2 flex items-center gap-2">
                <Activity className="w-5 h-5 text-brand-500" />
                Engagement Trend
              </h3>
              <p className="text-sm text-slate-500 mb-4">Daily engagement levels</p>
              
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={dailyData}>
                    <defs>
                      <linearGradient id="engagementGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="day" tick={{ fontSize: 12 }} />
                    <YAxis tick={{ fontSize: 12 }} domain={[0, 100]} />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="engagement"
                      stroke="#f59e0b"
                      strokeWidth={2}
                      fill="url(#engagementGradient)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>
            
            {/* Learning Time Distribution */}
            <Card padding="lg">
              <h3 className="text-lg font-semibold text-slate-900 mb-2 flex items-center gap-2">
                <Clock className="w-5 h-5 text-brand-500" />
                Peak Learning Hours
              </h3>
              <p className="text-sm text-slate-500 mb-4">When you're most active</p>
              
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={timeOfDayData} layout="vertical">
                    <XAxis type="number" tick={{ fontSize: 12 }} />
                    <YAxis dataKey="hour" type="category" tick={{ fontSize: 12 }} width={70} />
                    <Tooltip />
                    <Bar dataKey="sessions" fill="#6366f1" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </div>
        </TabsContent>
        
        {/* Concepts Tab */}
        <TabsContent value="concepts" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Concept Distribution */}
            <Card padding="lg">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Concept Distribution</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={conceptDistribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {conceptDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 space-y-2">
                {conceptDistribution.map((concept, index) => (
                  <div key={concept.name} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <span className="text-slate-700">{concept.name}</span>
                    </div>
                    <span className="text-slate-500">{concept.value}%</span>
                  </div>
                ))}
              </div>
            </Card>
            
            {/* Concept Mastery Levels */}
            <Card padding="lg">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Mastery by Concept</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={learningPatterns}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" tick={{ fontSize: 11 }} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} />
                    <Radar
                      name="Your Performance"
                      dataKey="A"
                      stroke="#6366f1"
                      strokeWidth={2}
                      fill="#6366f1"
                      fillOpacity={0.3}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </div>
        </TabsContent>
        
        {/* Patterns Tab */}
        <TabsContent value="patterns" className="space-y-6">
          <Card padding="lg">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Learning Pattern Analysis</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Pattern 1: Speed vs Accuracy */}
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <Brain className="w-5 h-5 text-brand-500" />
                  <span className="font-medium text-slate-900">Speed vs Accuracy</span>
                </div>
                <p className="text-sm text-slate-600 mb-3">
                  You tend to trade speed for accuracy. Consider slowing down on complex problems.
                </p>
                <div className="text-2xl font-bold text-brand-600">72%</div>
                <div className="text-xs text-slate-500">accuracy at current speed</div>
              </div>
              
              {/* Pattern 2: Learning Style */}
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <BookOpen className="w-5 h-5 text-emerald-500" />
                  <span className="font-medium text-slate-900">Learning Style</span>
                </div>
                <p className="text-sm text-slate-600 mb-3">
                  You learn best through examples and practice rather than reading theory.
                </p>
                <div className="text-2xl font-bold text-emerald-600">Practical</div>
                <div className="text-xs text-slate-500">preferred style</div>
              </div>
              
              {/* Pattern 3: Peak Performance */}
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="flex items-center gap-2 mb-3">
                  <Zap className="w-5 h-5 text-amber-500" />
                  <span className="font-medium text-slate-900">Peak Performance</span>
                </div>
                <p className="text-sm text-slate-600 mb-3">
                  Your best work happens between 3-6 PM. Schedule challenging tasks then.
                </p>
                <div className="text-2xl font-bold text-amber-600">3-6 PM</div>
                <div className="text-xs text-slate-500">optimal time</div>
              </div>
            </div>
          </Card>
        </TabsContent>
        
        {/* Insights Tab */}
        <TabsContent value="insights" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Strengths */}
            <Card padding="lg" className="border-l-4 border-l-emerald-500">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle className="w-5 h-5 text-emerald-500" />
                <h3 className="text-lg font-semibold text-slate-900">Your Strengths</h3>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-1">✓</span>
                  <span className="text-slate-700">Consistent daily engagement - you've maintained a strong study habit</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-1">✓</span>
                  <span className="text-slate-700">Quick learner on variable concepts - 85% mastery achieved</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-500 mt-1">✓</span>
                  <span className="text-slate-700">Regular use of Teaching Helper for quality improvement</span>
                </li>
              </ul>
            </Card>
            
            {/* Areas for Improvement */}
            <Card padding="lg" className="border-l-4 border-l-amber-500">
              <div className="flex items-center gap-2 mb-4">
                <AlertCircle className="w-5 h-5 text-amber-500" />
                <h3 className="text-lg font-semibold text-slate-900">Focus Areas</h3>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-2">
                  <span className="text-amber-500 mt-1">!</span>
                  <span className="text-slate-700">Functions and scope concepts need more practice (45% mastery)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-500 mt-1">!</span>
                  <span className="text-slate-700">Consider reviewing loop concepts before moving to advanced topics</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-500 mt-1">!</span>
                  <span className="text-slate-700">Weekend study sessions could improve consistency</span>
                </li>
              </ul>
            </Card>
          </div>
          
          {/* Personalized Recommendations */}
          <Card padding="lg" className="bg-gradient-to-r from-brand-50 to-purple-50">
            <h3 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-brand-600" />
              Personalized Recommendations
            </h3>
            <div className="space-y-4">
              <div className="flex items-start gap-4 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-8 h-8 bg-brand-100 rounded-full flex items-center justify-center shrink-0">
                  <span className="text-brand-600 font-bold">1</span>
                </div>
                <div>
                  <p className="font-medium text-slate-900">Focus on Functions</p>
                  <p className="text-sm text-slate-600 mt-1">
                    Based on your data, function concepts are your current bottleneck. 
                    We recommend completing the "Function Basics" learning path this week.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-4 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-8 h-8 bg-brand-100 rounded-full flex items-center justify-center shrink-0">
                  <span className="text-brand-600 font-bold">2</span>
                </div>
                <div>
                  <p className="font-medium text-slate-900">Optimal Study Schedule</p>
                  <p className="text-sm text-slate-600 mt-1">
                    Your peak performance is at 3-6 PM. Try to schedule challenging 
                    concepts during this window for better retention.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start gap-4 p-3 bg-white rounded-lg shadow-sm">
                <div className="w-8 h-8 bg-brand-100 rounded-full flex items-center justify-center shrink-0">
                  <span className="text-brand-600 font-bold">3</span>
                </div>
                <div>
                  <p className="font-medium text-slate-900">Spaced Repetition</p>
                  <p className="text-sm text-slate-600 mt-1">
                    You have 5 concepts due for review. Reviewing them now will 
                    strengthen your long-term retention.
                  </p>
                </div>
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
