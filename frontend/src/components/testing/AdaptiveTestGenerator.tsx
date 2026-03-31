import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  Wand2,
  Brain,
  Target,
  Clock,
  ChevronRight,
  Lightbulb,
  AlertCircle,
  CheckCircle,
  Sparkles,
  RefreshCw,
  Play,
  HelpCircle,
  TrendingUp,
  Zap,
  BarChart3,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";

interface AdaptiveQuestion {
  id: string;
  text: string;
  target_unit: string;
  difficulty: string;
  type: string;
  estimated_time: number;
  hints: string[];
}

interface TestMetadata {
  total_questions: number;
  total_estimated_time: number;
  average_difficulty: number;
  knowledge_gaps_targeted: string[];
  adaptive_strategy: string;
}

interface AdaptiveTest {
  test_id: string;
  questions: AdaptiveQuestion[];
  test_metadata: TestMetadata;
}

interface AdaptiveTestGeneratorProps {
  taId: number;
}

const DIFFICULTY_COLORS = {
  EASY: { bg: "bg-emerald-100", text: "text-emerald-700", border: "border-emerald-200" },
  MEDIUM: { bg: "bg-brand-100", text: "text-brand-700", border: "border-brand-200" },
  HARD: { bg: "bg-amber-100", text: "text-amber-700", border: "border-amber-200" },
  EXPERT: { bg: "bg-rose-100", text: "text-rose-700", border: "border-rose-200" },
};

const TYPE_ICONS = {
  conceptual: Lightbulb,
  application: Play,
  analysis: BarChart3,
};

export function AdaptiveTestGenerator({ taId }: AdaptiveTestGeneratorProps) {
  const [numQuestions, setNumQuestions] = useState(5);
  const [generatedTest, setGeneratedTest] = useState<AdaptiveTest | null>(null);
  const [activeQuestion, setActiveQuestion] = useState(0);
  const [showHint, setShowHint] = useState<number | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const generateMutation = useMutation({
    mutationFn: async () => {
      const res = await apiFetch(`/adaptive-test/generate/${taId}?num_questions=${numQuestions}`, {
        method: "POST",
      });
      return res.json();
    },
    onSuccess: setGeneratedTest,
  });

  const difficulty = generatedTest?.test_metadata?.average_difficulty || 0;

  return (
    <Card padding="lg">
      {/* Header */}
      <div className="flex items-start gap-4 mb-6">
        <div className="p-3 bg-brand-100 rounded-xl">
          <Brain className="w-6 h-6 text-brand-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-stone-900">Adaptive Test Generator</h3>
          <p className="text-stone-500 mt-1">
            AI-generated personalized tests based on your knowledge state, learning history, and identified gaps.
          </p>
        </div>
      </div>

      {!generatedTest ? (
        /* Configuration Panel */
        <div className="space-y-6">
          <div className="p-4 bg-stone-50 rounded-xl">
            <label className="text-sm font-medium text-stone-700 mb-3 block">
              Number of Questions
            </label>
            <div className="flex gap-2">
              {[3, 5, 7, 10].map((n) => (
                <button
                  key={n}
                  onClick={() => setNumQuestions(n)}
                  className={cn(
                    "px-4 py-2 rounded-lg font-medium transition-all",
                    numQuestions === n
                      ? "bg-brand-500 text-white"
                      : "bg-white border border-stone-200 text-stone-600 hover:border-brand-300"
                  )}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-stone-200 rounded-xl">
              <Target className="w-5 h-5 text-brand-500 mb-2" />
              <p className="font-medium text-stone-900">Gap-Focused</p>
              <p className="text-sm text-stone-500">
                Targets your specific knowledge gaps identified by BKT analysis
              </p>
            </div>
            <div className="p-4 border border-stone-200 rounded-xl">
              <TrendingUp className="w-5 h-5 text-emerald-500 mb-2" />
              <p className="font-medium text-stone-900">Difficulty Adaptation</p>
              <p className="text-sm text-stone-500">
                Questions adapt to your mastery level using IRT-based selection
              </p>
            </div>
            <div className="p-4 border border-stone-200 rounded-xl">
              <Zap className="w-5 h-5 text-amber-500 mb-2" />
              <p className="font-medium text-stone-900">Misconception Detection</p>
              <p className="text-sm text-stone-500">
                Special focus on concepts with active misconceptions
              </p>
            </div>
          </div>

          <Button
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            loading={generateMutation.isPending}
            icon={Wand2}
            size="lg"
            className="w-full"
          >
            Generate Adaptive Test
          </Button>
        </div>
      ) : (
        /* Generated Test Display */
        <div className="space-y-4">
          {/* Test Metadata */}
          <div className="p-4 bg-gradient-to-r from-brand-50 to-purple-50 rounded-xl border border-brand-100">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-brand-600" />
                <span className="font-semibold text-brand-900">
                  Personalized Test Generated
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                icon={RefreshCw}
                onClick={() => generateMutation.mutate()}
                loading={generateMutation.isPending}
              >
                Regenerate
              </Button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-stone-900">
                  {generatedTest.test_metadata.total_questions}
                </p>
                <p className="text-xs text-stone-500">Questions</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-stone-900">
                  {generatedTest.test_metadata.total_estimated_time}m
                </p>
                <p className="text-xs text-stone-500">Est. Time</p>
              </div>
              <div className="text-center">
                <p className={cn(
                  "text-2xl font-bold",
                  difficulty <= 1.5 ? "text-emerald-600" :
                  difficulty <= 2.5 ? "text-brand-600" :
                  difficulty <= 3.5 ? "text-amber-600" :
                  "text-rose-600"
                )}>
                  {generatedTest.test_metadata.average_difficulty.toFixed(1)}
                </p>
                <p className="text-xs text-stone-500">Avg Difficulty</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-stone-900">
                  {generatedTest.test_metadata.knowledge_gaps_targeted.length}
                </p>
                <p className="text-xs text-stone-500">Gaps Targeted</p>
              </div>
            </div>
          </div>

          {/* Questions */}
          <Tabs value={String(activeQuestion)} className="w-full">
            <TabsList className="flex flex-wrap gap-1 mb-4 h-auto">
              {generatedTest.questions.map((q, idx) => {
                const colors = DIFFICULTY_COLORS[q.difficulty as keyof typeof DIFFICULTY_COLORS] || DIFFICULTY_COLORS.MEDIUM;
                const isAnswered = answers[q.id];
                
                return (
                  <TabsTrigger
                    key={idx}
                    value={String(idx)}
                    onClick={() => setActiveQuestion(idx)}
                    className={cn(
                      "px-3 py-1.5 text-sm rounded-lg data-[state=active]:ring-2 data-[state=active]:ring-brand-500",
                      isAnswered && "ring-1 ring-emerald-400"
                    )}
                  >
                    <div className="flex items-center gap-2">
                      <span className={cn("w-2 h-2 rounded-full", colors.bg.replace("bg-", "bg-"))} />
                      <span>Q{idx + 1}</span>
                      {isAnswered && <CheckCircle className="w-3 h-3 text-emerald-500" />}
                    </div>
                  </TabsTrigger>
                );
              })}
            </TabsList>

            {generatedTest.questions.map((question, idx) => {
              const colors = DIFFICULTY_COLORS[question.difficulty as keyof typeof DIFFICULTY_COLORS] || DIFFICULTY_COLORS.MEDIUM;
              const TypeIcon = TYPE_ICONS[question.type as keyof typeof TYPE_ICONS] || Lightbulb;
              
              return (
                <TabsContent key={idx} value={String(idx)} className="m-0">
                  <div className="space-y-4">
                    {/* Question Card */}
                    <div className={cn(
                      "p-5 rounded-xl border-2",
                      colors.border,
                      "bg-white"
                    )}>
                      {/* Question Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center gap-2">
                          <span className={cn("px-2 py-1 rounded text-xs font-medium", colors.bg, colors.text)}>
                            {question.difficulty}
                          </span>
                          <span className="flex items-center gap-1 px-2 py-1 bg-stone-100 rounded text-xs text-stone-600">
                            <TypeIcon className="w-3 h-3" />
                            {question.type}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-stone-500">
                          <Clock className="w-3 h-3" />
                          {question.estimated_time} min
                        </div>
                      </div>

                      {/* Question Text */}
                      <div className="prose prose-sm max-w-none mb-4">
                        <p className="text-stone-800 text-base leading-relaxed whitespace-pre-wrap">
                          {question.text}
                        </p>
                      </div>

                      {/* Target Unit */}
                      <div className="flex items-center gap-2 text-sm text-stone-500 mb-4">
                        <Target className="w-4 h-4" />
                        <span>Testing: </span>
                        <span className="font-medium text-stone-700">
                          {question.target_unit.replace(/_/g, " ")}
                        </span>
                      </div>

                      {/* Hints */}
                      {question.hints.length > 0 && (
                        <div className="border-t border-stone-100 pt-4">
                          <button
                            onClick={() => setShowHint(showHint === idx ? null : idx)}
                            className="flex items-center gap-2 text-sm text-brand-600 hover:text-brand-700"
                          >
                            <HelpCircle className="w-4 h-4" />
                            {showHint === idx ? "Hide hint" : "Need a hint?"}
                          </button>
                          
                          {showHint === idx && (
                            <div className="mt-2 p-3 bg-brand-50 rounded-lg">
                              <ul className="space-y-1">
                                {question.hints.map((hint, hidx) => (
                                  <li key={hidx} className="text-sm text-brand-800 flex items-start gap-2">
                                    <span className="text-brand-400">•</span>
                                    {hint}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Answer Input */}
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-stone-700">
                        Your Answer
                      </label>
                      <textarea
                        value={answers[question.id] || ""}
                        onChange={(e) => setAnswers(prev => ({ ...prev, [question.id]: e.target.value }))}
                        placeholder="Type your answer here..."
                        className="w-full p-3 border border-stone-200 rounded-lg min-h-[120px] text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none"
                      />
                    </div>

                    {/* Navigation */}
                    <div className="flex justify-between">
                      <Button
                        variant="outline"
                        onClick={() => setActiveQuestion(Math.max(0, idx - 1))}
                        disabled={idx === 0}
                      >
                        Previous
                      </Button>
                      <Button
                        variant="primary"
                        onClick={() => {
                          if (idx < generatedTest.questions.length - 1) {
                            setActiveQuestion(idx + 1);
                          }
                        }}
                        disabled={idx === generatedTest.questions.length - 1}
                      >
                        Next
                      </Button>
                    </div>
                  </div>
                </TabsContent>
              );
            })}
          </Tabs>

          {/* Progress */}
          <div className="p-4 bg-stone-50 rounded-lg">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-stone-600">Progress</span>
              <span className="font-medium text-stone-900">
                {Object.keys(answers).length} / {generatedTest.questions.length} answered
              </span>
            </div>
            <ProgressBar
              value={(Object.keys(answers).length / generatedTest.questions.length) * 100}
              className="h-2"
            />
          </div>

          {/* Submit */}
          <Button
            variant="primary"
            size="lg"
            icon={CheckCircle}
            className="w-full"
            onClick={() => {
              // Would submit answers for evaluation
              alert("Test submitted! (Evaluation not yet implemented)");
            }}
          >
            Submit Test for Evaluation
          </Button>
        </div>
      )}
    </Card>
  );
}
