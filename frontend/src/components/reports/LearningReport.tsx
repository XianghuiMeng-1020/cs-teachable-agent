import { useState, useRef } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  FileText,
  Download,
  Share2,
  Award,
  TrendingUp,
  BookOpen,
  Target,
  Calendar,
  Clock,
  Zap,
  CheckCircle,
  Printer,
  ChevronDown,
  ChevronUp,
  BarChart3,
  PieChart,
  Activity,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart as RePieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";

interface LearningReportProps {
  taId: number;
}

const COLORS = ["#0D9488", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

export function LearningReport({ taId }: LearningReportProps) {
  const reportRef = useRef<HTMLDivElement>(null);
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(["summary"]));

  const { data: report, isLoading } = useQuery({
    queryKey: ["reports", "learning", taId],
    queryFn: async () => {
      const res = await apiFetch(`/reports/my-learning?ta_id=${taId}`);
      return res.json();
    },
  });

  const handlePrint = () => {
    window.print();
  };

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => {
      const next = new Set(prev);
      if (next.has(section)) {
        next.delete(section);
      } else {
        next.add(section);
      }
      return next;
    });
  };

  if (isLoading) {
    return (
      <Card padding="lg" className="text-center py-12">
        <div className="w-12 h-12 border-4 border-brand-200 border-t-brand-500 rounded-full animate-spin mx-auto" />
        <p className="text-stone-500 mt-4">Generating your learning report...</p>
      </Card>
    );
  }

  if (!report) {
    return (
      <Card padding="lg" className="text-center py-12">
        <FileText className="w-12 h-12 text-stone-300 mx-auto mb-4" />
        <p className="text-stone-500">No report data available</p>
      </Card>
    );
  }

  const summary = report.summary;
  const progress = report.learning_progress;
  const engagement = report.engagement;
  const gamification = report.gamification;

  // Prepare chart data
  const masteryData = Object.entries(progress?.knowledge_state || {}).map(([unit, prob]) => ({
    unit: unit.replace(/_/g, " "),
    probability: Math.round((prob as number) * 100),
  }));

  const activityData = [
    { name: "Teaching", value: summary?.total_teaching_sessions || 0, color: COLORS[0] },
    { name: "Tests", value: summary?.total_tests_taken || 0, color: COLORS[1] },
  ];

  const Section = ({
    title,
    icon: Icon,
    id,
    children,
  }: {
    title: string;
    icon: any;
    id: string;
    children: React.ReactNode;
  }) => (
    <div className="border border-stone-200 rounded-xl overflow-hidden mb-4">
      <button
        onClick={() => toggleSection(id)}
        className="w-full flex items-center justify-between p-4 bg-stone-50 hover:bg-stone-100 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5 text-brand-600" />
          <span className="font-semibold text-stone-900">{title}</span>
        </div>
        {expandedSections.has(id) ? (
          <ChevronUp className="w-5 h-5 text-stone-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-stone-400" />
        )}
      </button>
      {expandedSections.has(id) && <div className="p-4">{children}</div>}
    </div>
  );

  return (
    <div className="space-y-4">
      {/* Actions */}
      <div className="flex justify-end gap-2">
        <Button variant="outline" icon={Printer} onClick={handlePrint}>
          Print / PDF
        </Button>
        <Button variant="outline" icon={Download} onClick={() => window.open(`/api/reports/export-json?ta_id=${taId}`, "_blank")}>
          Export JSON
        </Button>
      </div>

      {/* Report Content */}
      <div ref={reportRef} className="bg-white">
        {/* Header */}
        <div className="text-center border-b border-stone-200 pb-6 mb-6">
          <div className="w-16 h-16 bg-brand-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Award className="w-8 h-8 text-brand-600" />
          </div>
          <h1 className="text-2xl font-bold text-stone-900">Learning Analytics Report</h1>
          <p className="text-stone-500 mt-1">
            Domain: <span className="font-medium capitalize">{report.student_info?.domain}</span>
          </p>
          <p className="text-xs text-stone-400 mt-1">
            Generated: {new Date(report.student_info?.generated_at).toLocaleString()}
          </p>
        </div>

        {/* Summary Stats */}
        <Section title="Learning Summary" icon={BarChart3} id="summary">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 bg-brand-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-brand-600">{summary?.total_concepts_learned || 0}</p>
              <p className="text-sm text-stone-600 mt-1">Concepts Learned</p>
            </div>
            <div className="p-4 bg-emerald-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-emerald-600">{Math.round(summary?.test_pass_rate || 0)}%</p>
              <p className="text-sm text-stone-600 mt-1">Test Pass Rate</p>
            </div>
            <div className="p-4 bg-amber-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-amber-600">{summary?.total_teaching_sessions || 0}</p>
              <p className="text-sm text-stone-600 mt-1">Teaching Sessions</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-purple-600">{summary?.study_duration_days || 0}</p>
              <p className="text-sm text-stone-600 mt-1">Days Active</p>
            </div>
          </div>

          {gamification && (
            <div className="mt-6 p-4 bg-gradient-to-r from-amber-50 to-orange-50 rounded-lg border border-amber-100">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
                  <Zap className="w-6 h-6 text-amber-600" />
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-amber-900">
                    Level {gamification.level} Learner
                  </p>
                  <p className="text-sm text-amber-700">
                    {gamification.points} points • {gamification.achievements_unlocked} achievements unlocked
                  </p>
                </div>
              </div>
            </div>
          )}
        </Section>

        {/* Knowledge Mastery */}
        <Section title="Knowledge Mastery" icon={Target} id="mastery">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-stone-600">Average Mastery</span>
              <span className="font-semibold text-stone-900">
                {Math.round((progress?.average_mastery_probability || 0) * 100)}%
              </span>
            </div>
            <ProgressBar 
              value={(progress?.average_mastery_probability || 0) * 100} 
              className="h-3"
              color={(progress?.average_mastery_probability || 0) > 0.7 ? "success" : "brand"}
            />

            {masteryData.length > 0 && (
              <div className="h-48 mt-4">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={masteryData.slice(0, 10)}>
                    <XAxis dataKey="unit" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" height={60} />
                    <YAxis tick={{ fontSize: 10 }} domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="probability" fill="#0D9488" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {progress?.concepts_mastered?.length > 0 && (
              <div className="mt-4">
                <p className="text-sm font-medium text-stone-700 mb-2">Mastered Concepts</p>
                <div className="flex flex-wrap gap-2">
                  {progress.concepts_mastered.map((concept: string) => (
                    <span
                      key={concept}
                      className="px-2 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs flex items-center gap-1"
                    >
                      <CheckCircle className="w-3 h-3" />
                      {concept.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>

        {/* Activity Distribution */}
        <Section title="Activity Analysis" icon={Activity} id="activity">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-stone-700 mb-3">Teaching vs Testing</h4>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <RePieChart>
                    <Pie
                      data={activityData}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={70}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {activityData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RePieChart>
                </ResponsiveContainer>
              </div>
              <div className="flex justify-center gap-4 mt-2">
                {activityData.map((item) => (
                  <div key={item.name} className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="text-xs text-stone-600">{item.name}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-3">
              <div className="p-3 bg-stone-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <TrendingUp className="w-4 h-4 text-stone-400" />
                  <span className="text-sm font-medium text-stone-700">Quality Trend</span>
                </div>
                <p className={cn(
                  "text-sm",
                  engagement?.quality_trend === "improving" ? "text-emerald-600" :
                  engagement?.quality_trend === "declining" ? "text-rose-600" :
                  "text-stone-600"
                )}>
                  {engagement?.quality_trend === "improving" ? "📈 Improving" :
                   engagement?.quality_trend === "declining" ? "📉 Declining" :
                   "➡️ Stable"}
                </p>
              </div>

              <div className="p-3 bg-stone-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <Clock className="w-4 h-4 text-stone-400" />
                  <span className="text-sm font-medium text-stone-700">Teaching/Test Ratio</span>
                </div>
                <p className="text-2xl font-bold text-stone-900">
                  {engagement?.teaching_to_test_ratio || 0}:1
                </p>
              </div>

              <div className="p-3 bg-stone-50 rounded-lg">
                <div className="flex items-center gap-2 mb-1">
                  <Zap className="w-4 h-4 text-stone-400" />
                  <span className="text-sm font-medium text-stone-700">Avg Teaching Quality</span>
                </div>
                <p className="text-2xl font-bold text-stone-900">
                  {Math.round((summary?.average_teaching_quality || 0) * 100)}%
                </p>
              </div>
            </div>
          </div>
        </Section>

        {/* Topics Covered */}
        {progress?.topics_covered?.length > 0 && (
          <Section title="Topics Covered" icon={BookOpen} id="topics">
            <div className="grid grid-cols-2 gap-2">
              {progress.topics_covered.map((topic: string) => (
                <div
                  key={topic}
                  className="flex items-center gap-2 p-2 bg-stone-50 rounded-lg"
                >
                  <CheckCircle className="w-4 h-4 text-emerald-500" />
                  <span className="text-sm text-stone-700">{topic}</span>
                </div>
              ))}
            </div>
          </Section>
        )}
      </div>
    </div>
  );
}
