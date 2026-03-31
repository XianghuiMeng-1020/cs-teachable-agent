import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { 
  Wand2, 
  BarChart3, 
  GitCompare, 
  Sparkles, 
  AlertCircle,
  CheckCircle,
  Lightbulb,
  Zap,
  Coins,
  Type,
  ArrowRight,
  Loader2
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";

interface PromptOptimizerProps {
  domain?: string;
}

function PromptOptimizer({ domain = "general" }: PromptOptimizerProps) {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any>(null);

  const optimizeMutation = useMutation({
    mutationFn: async (prompt: string) => {
      const res = await apiFetch("/ai-experiments/optimize-prompt", {
        method: "POST",
        body: JSON.stringify({ prompt, domain }),
      });
      return res.json();
    },
    onSuccess: setResult,
  });

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-stone-700">Your Prompt</label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter a prompt to optimize... (e.g., 'Explain Python variables')"
          className="w-full mt-1 p-3 border border-stone-200 rounded-lg min-h-[100px] text-sm focus:ring-2 focus:ring-brand-500"
        />
      </div>

      <Button
        onClick={() => optimizeMutation.mutate(input)}
        disabled={!input.trim() || optimizeMutation.isPending}
        loading={optimizeMutation.isPending}
        icon={Wand2}
      >
        Optimize Prompt
      </Button>

      {result && (
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-2">
          {/* Improvement Score */}
          <div className="flex items-center gap-4 p-4 bg-stone-50 rounded-lg">
            <div className={cn(
              "w-16 h-16 rounded-full flex items-center justify-center text-lg font-bold",
              (result.improvement_score || 0) > 70 ? "bg-emerald-100 text-emerald-700" :
              (result.improvement_score || 0) > 40 ? "bg-amber-100 text-amber-700" :
              "bg-stone-200 text-stone-600"
            )}>
              {result.improvement_score || "?"}
            </div>
            <div>
              <p className="font-medium text-stone-900">Improvement Score</p>
              <p className="text-sm text-stone-500">
                {result.improvement_score && result.improvement_score > 70 
                  ? "Excellent optimization!" 
                  : result.improvement_score && result.improvement_score > 40
                  ? "Good improvements made"
                  : "Some optimizations possible"}
              </p>
            </div>
          </div>

          {/* Analysis */}
          {result.analysis && (
            <div className="p-4 bg-amber-50 rounded-lg border border-amber-100">
              <div className="flex items-start gap-2">
                <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
                <div>
                  <p className="font-medium text-amber-900">Analysis</p>
                  <p className="text-sm text-amber-800 mt-1">{result.analysis}</p>
                </div>
              </div>
            </div>
          )}

          {/* Optimized Prompt */}
          {result.optimized && result.optimized !== result.original && (
            <div className="p-4 bg-brand-50 rounded-lg border border-brand-100">
              <div className="flex items-start gap-2">
                <Sparkles className="w-5 h-5 text-brand-600 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium text-brand-900">Optimized Prompt</p>
                  <div className="mt-2 p-3 bg-white rounded border border-brand-200 text-sm text-stone-700">
                    {result.optimized}
                  </div>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="mt-2"
                    onClick={() => setInput(result.optimized)}
                  >
                    Use This
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* Tips */}
          {result.tips && result.tips.length > 0 && (
            <div className="p-4 bg-stone-50 rounded-lg">
              <p className="font-medium text-stone-900 flex items-center gap-2">
                <Lightbulb className="w-4 h-4" />
                Prompt Engineering Tips
              </p>
              <ul className="mt-2 space-y-1">
                {result.tips.map((tip: string, i: number) => (
                  <li key={i} className="text-sm text-stone-600 flex items-start gap-2">
                    <span className="text-brand-500 mt-0.5">•</span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function TokenVisualizer() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<any>(null);

  const analyzeMutation = useMutation({
    mutationFn: async (text: string) => {
      const res = await apiFetch("/ai-experiments/token-analysis", {
        method: "POST",
        body: JSON.stringify({ text }),
      });
      return res.json();
    },
    onSuccess: setResult,
  });

  const analysis = result?.token_analysis;

  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium text-stone-700">Text to Analyze</label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter text to analyze token usage..."
          className="w-full mt-1 p-3 border border-stone-200 rounded-lg min-h-[100px] text-sm focus:ring-2 focus:ring-brand-500"
        />
      </div>

      <Button
        onClick={() => analyzeMutation.mutate(input)}
        disabled={!input.trim() || analyzeMutation.isPending}
        loading={analyzeMutation.isPending}
        icon={Type}
      >
        Analyze Tokens
      </Button>

      {analysis && (
        <div className="space-y-4 animate-in fade-in">
          {/* Token Count */}
          <div className="grid grid-cols-3 gap-3">
            <Card padding="md" className="text-center">
              <p className="text-2xl font-bold text-stone-900">{analysis.total_tokens}</p>
              <p className="text-xs text-stone-500">Total Tokens</p>
            </Card>
            <Card padding="md" className="text-center">
              <p className="text-2xl font-bold text-stone-900">{analysis.word_count}</p>
              <p className="text-xs text-stone-500">Words</p>
            </Card>
            <Card padding="md" className="text-center">
              <p className="text-2xl font-bold text-stone-900">{analysis.char_count}</p>
              <p className="text-xs text-stone-500">Characters</p>
            </Card>
          </div>

          {/* Token Distribution */}
          <div className="p-4 bg-stone-50 rounded-lg">
            <p className="font-medium text-stone-900 mb-3">Token Distribution</p>
            <div className="space-y-2">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-stone-600">Text Content</span>
                  <span className="font-medium">{analysis.text_tokens} tokens</span>
                </div>
                <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-brand-500 rounded-full"
                    style={{ width: `${(analysis.text_tokens / analysis.total_tokens) * 100}%` }}
                  />
                </div>
              </div>
              {analysis.code_tokens > 0 && (
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-stone-600">Code Blocks</span>
                    <span className="font-medium">{analysis.code_tokens} tokens</span>
                  </div>
                  <div className="h-2 bg-stone-200 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-purple-500 rounded-full"
                      style={{ width: `${(analysis.code_tokens / analysis.total_tokens) * 100}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Cost Estimation */}
          <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-100">
            <div className="flex items-center gap-2 mb-3">
              <Coins className="w-5 h-5 text-emerald-600" />
              <p className="font-medium text-emerald-900">Estimated Cost</p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="p-2 bg-white rounded">
                <p className="text-xs text-stone-500">GPT-4</p>
                <p className="font-medium text-stone-900">${analysis.estimated_cost_gpt4.toFixed(6)}</p>
              </div>
              <div className="p-2 bg-white rounded">
                <p className="text-xs text-stone-500">GPT-3.5</p>
                <p className="font-medium text-stone-900">${analysis.estimated_cost_gpt3.toFixed(6)}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function ResponseComparator() {
  const [responseA, setResponseA] = useState("");
  const [responseB, setResponseB] = useState("");
  const [result, setResult] = useState<any>(null);

  const compareMutation = useMutation({
    mutationFn: async () => {
      const res = await apiFetch("/ai-experiments/compare-responses", {
        method: "POST",
        body: JSON.stringify({ response_a: responseA, response_b: responseB }),
      });
      return res.json();
    },
    onSuccess: setResult,
  });

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm font-medium text-stone-700">Response A</label>
          <textarea
            value={responseA}
            onChange={(e) => setResponseA(e.target.value)}
            placeholder="Paste first response..."
            className="w-full mt-1 p-3 border border-stone-200 rounded-lg min-h-[150px] text-sm"
          />
        </div>
        <div>
          <label className="text-sm font-medium text-stone-700">Response B</label>
          <textarea
            value={responseB}
            onChange={(e) => setResponseB(e.target.value)}
            placeholder="Paste second response..."
            className="w-full mt-1 p-3 border border-stone-200 rounded-lg min-h-[150px] text-sm"
          />
        </div>
      </div>

      <Button
        onClick={() => compareMutation.mutate()}
        disabled={!responseA.trim() || !responseB.trim() || compareMutation.isPending}
        loading={compareMutation.isPending}
        icon={GitCompare}
      >
        Compare Responses
      </Button>

      {result && (
        <div className="space-y-4 animate-in fade-in">
          {/* Similarity Score */}
          <div className="flex items-center gap-4 p-4 bg-stone-50 rounded-lg">
            <div className={cn(
              "w-20 h-20 rounded-full flex items-center justify-center text-xl font-bold",
              result.similarity_score > 70 ? "bg-rose-100 text-rose-700" :
              result.similarity_score > 30 ? "bg-amber-100 text-amber-700" :
              "bg-emerald-100 text-emerald-700"
            )}>
              {result.similarity_score}%
            </div>
            <div>
              <p className="font-medium text-stone-900">Similarity Score</p>
              <p className="text-sm text-stone-500">
                {result.similarity_score > 70 
                  ? "Very similar - responses are nearly identical" 
                  : result.similarity_score > 30
                  ? "Moderately similar - some overlap in content"
                  : "Low similarity - responses are quite different"}
              </p>
            </div>
          </div>

          {/* Length Comparison */}
          <div className="p-4 bg-stone-50 rounded-lg">
            <p className="font-medium text-stone-900 mb-3">Length Comparison</p>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-3 bg-white rounded border border-stone-200">
                <p className="text-xs text-stone-500">Response A</p>
                <p className="text-lg font-medium">{result.length_comparison?.response_a_words} words</p>
                <p className="text-xs text-stone-400">{result.length_comparison?.response_a_chars} chars</p>
              </div>
              <div className="p-3 bg-white rounded border border-stone-200">
                <p className="text-xs text-stone-500">Response B</p>
                <p className="text-lg font-medium">{result.length_comparison?.response_b_words} words</p>
                <p className="text-xs text-stone-400">{result.length_comparison?.response_b_chars} chars</p>
              </div>
            </div>
            <p className="text-sm text-stone-600 mt-2">
              Length difference: {Math.abs(result.length_comparison?.length_difference_pct || 0)}%
            </p>
          </div>

          {/* Structure Analysis */}
          <div className="p-4 bg-brand-50 rounded-lg">
            <p className="font-medium text-brand-900 mb-2">Structure Analysis</p>
            <div className="flex gap-4 text-sm">
              <div className="flex items-center gap-2">
                {result.structure_analysis?.response_a_has_code ? 
                  <CheckCircle className="w-4 h-4 text-emerald-600" /> :
                  <AlertCircle className="w-4 h-4 text-stone-400" />
                }
                <span className={result.structure_analysis?.response_a_has_code ? "text-stone-700" : "text-stone-400"}>
                  A has code
                </span>
              </div>
              <div className="flex items-center gap-2">
                {result.structure_analysis?.response_b_has_code ? 
                  <CheckCircle className="w-4 h-4 text-emerald-600" /> :
                  <AlertCircle className="w-4 h-4 text-stone-400" />
                }
                <span className={result.structure_analysis?.response_b_has_code ? "text-stone-700" : "text-stone-400"}>
                  B has code
                </span>
              </div>
            </div>
          </div>

          {/* Key Differences */}
          {result.key_differences && result.key_differences.length > 0 && (
            <div className="p-4 bg-amber-50 rounded-lg">
              <p className="font-medium text-amber-900 mb-2">Key Differences</p>
              <ul className="space-y-1">
                {result.key_differences.map((diff: string, i: number) => (
                  <li key={i} className="text-sm text-amber-800 flex items-start gap-2">
                    <ArrowRight className="w-4 h-4 mt-0.5 shrink-0" />
                    {diff}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

interface AdvancedAILabProps {
  domain?: string;
}

export function AdvancedAILab({ domain = "general" }: AdvancedAILabProps) {
  return (
    <Card padding="lg">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-brand-100 rounded-lg">
          <Zap className="w-5 h-5 text-brand-600" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-stone-900">Advanced AI Lab</h3>
          <p className="text-sm text-stone-500">Experiment with AI capabilities</p>
        </div>
      </div>

      <Tabs defaultValue="optimizer">
        <TabsList className="grid w-full grid-cols-3 mb-4">
          <TabsTrigger value="optimizer">
            <Wand2 className="w-4 h-4 mr-2" />
            Prompt Optimizer
          </TabsTrigger>
          <TabsTrigger value="tokens">
            <BarChart3 className="w-4 h-4 mr-2" />
            Token Visualizer
          </TabsTrigger>
          <TabsTrigger value="compare">
            <GitCompare className="w-4 h-4 mr-2" />
            Response Compare
          </TabsTrigger>
        </TabsList>

        <TabsContent value="optimizer" className="m-0">
          <PromptOptimizer domain={domain} />
        </TabsContent>

        <TabsContent value="tokens" className="m-0">
          <TokenVisualizer />
        </TabsContent>

        <TabsContent value="compare" className="m-0">
          <ResponseComparator />
        </TabsContent>
      </Tabs>
    </Card>
  );
}
