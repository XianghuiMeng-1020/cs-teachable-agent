import { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  Smile,
  Frown,
  AlertCircle,
  Meh,
  Zap,
  HelpCircle,
  TrendingUp,
  TrendingDown,
  Minus,
  Brain,
  MessageCircle,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { apiFetch } from "@/api/client";
import { cn } from "@/lib/utils";

interface SentimentData {
  emotional_state: string;
  confidence: number;
  engagement_score: number;
  confusion_indicators: string[];
  frustration_indicators: string[];
  positive_indicators: string[];
  help_seeking: boolean;
  needs_intervention: boolean;
  suggested_response: string;
}

interface SentimentIndicatorProps {
  message: string;
  className?: string;
}

const EMOTION_CONFIGS: Record<string, {
  icon: any;
  label: string;
  color: string;
  bg: string;
  description: string;
}> = {
  confused: {
    icon: HelpCircle,
    label: "Confused",
    color: "text-amber-600",
    bg: "bg-amber-50",
    description: "Student may need clarification",
  },
  frustrated: {
    icon: Frown,
    label: "Frustrated",
    color: "text-rose-600",
    bg: "bg-rose-50",
    description: "Intervention recommended",
  },
  engaged: {
    icon: Zap,
    label: "Engaged",
    color: "text-brand-600",
    bg: "bg-brand-50",
    description: "Student is actively learning",
  },
  satisfied: {
    icon: Smile,
    label: "Satisfied",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
    description: "Concept understood",
  },
  neutral: {
    icon: Meh,
    label: "Neutral",
    color: "text-slate-600",
    bg: "bg-slate-50",
    description: "Monitoring engagement",
  },
  excited: {
    icon: Zap,
    label: "Excited",
    color: "text-purple-600",
    bg: "bg-purple-50",
    description: "High enthusiasm detected",
  },
  bored: {
    icon: Minus,
    label: "Bored",
    color: "text-slate-500",
    bg: "bg-slate-100",
    description: "May need more challenge",
  },
};

export function SentimentIndicator({ message, className }: SentimentIndicatorProps) {
  const [sentiment, setSentiment] = useState<SentimentData | null>(null);
  const [expanded, setExpanded] = useState(false);

  const analyzeMutation = useMutation({
    mutationFn: async (text: string) => {
      // Note: This would call a backend API in production
      // For now, we'll do simple client-side analysis
      return analyzeClientSide(text);
    },
    onSuccess: setSentiment,
  });

  // Analyze when message changes
  useEffect(() => {
    if (message.length > 5) {
      const timeout = setTimeout(() => {
        analyzeMutation.mutate(message);
      }, 500);
      return () => clearTimeout(timeout);
    }
  }, [message]);

  if (!sentiment || analyzeMutation.isPending) {
    return (
      <div className={cn("flex items-center gap-2 text-xs text-slate-400", className)}>
        <Brain className="w-3 h-3" />
        <span>Analyzing...</span>
      </div>
    );
  }

  const config = EMOTION_CONFIGS[sentiment.emotional_state] || EMOTION_CONFIGS.neutral;
  const Icon = config.icon;

  const engagementPercent = ((sentiment.engagement_score + 1) / 2) * 100;

  return (
    <div className={cn("space-y-2", className)}>
      {/* Main Indicator */}
      <button
        onClick={() => setExpanded(!expanded)}
        className={cn(
          "flex items-center gap-2 px-3 py-1.5 rounded-full text-xs transition-all",
          config.bg,
          sentiment.needs_intervention && "ring-2 ring-rose-300"
        )}
      >
        <Icon className={cn("w-3.5 h-3.5", config.color)} />
        <span className={cn("font-medium", config.color)}>
          {config.label}
        </span>
        <span className="text-slate-400">|</span>
        <div className="flex items-center gap-1">
          <div className="w-12 h-1.5 bg-slate-200 rounded-full overflow-hidden">
            <div
              className={cn(
                "h-full rounded-full",
                engagementPercent > 60 ? "bg-emerald-500" :
                engagementPercent > 30 ? "bg-amber-500" :
                "bg-rose-500"
              )}
              style={{ width: `${engagementPercent}%` }}
            />
          </div>
        </div>
        {sentiment.help_seeking && (
          <AlertCircle className="w-3.5 h-3.5 text-amber-500" />
        )}
      </button>

      {/* Expanded Details */}
      {expanded && (
        <Card padding="sm" className="animate-in fade-in slide-in-from-top-2">
          <div className="space-y-3">
            {/* Engagement Meter */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-600">Engagement</span>
                <span className={cn(
                  "font-medium",
                  sentiment.engagement_score > 0.3 ? "text-emerald-600" :
                  sentiment.engagement_score > -0.3 ? "text-amber-600" :
                  "text-rose-600"
                )}>
                  {sentiment.engagement_score > 0.3 ? "High" :
                   sentiment.engagement_score > -0.3 ? "Medium" :
                   "Low"}
                </span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={cn(
                    "h-full rounded-full transition-all",
                    sentiment.engagement_score > 0.3 ? "bg-emerald-500" :
                    sentiment.engagement_score > -0.3 ? "bg-amber-500" :
                    "bg-rose-500"
                  )}
                  style={{ width: `${engagementPercent}%` }}
                />
              </div>
            </div>

            {/* Indicators */}
            {sentiment.confusion_indicators.length > 0 && (
              <div>
                <p className="text-xs text-amber-600 font-medium mb-1 flex items-center gap-1">
                  <HelpCircle className="w-3 h-3" />
                  Confusion signals detected
                </p>
                <div className="flex flex-wrap gap-1">
                  {sentiment.confusion_indicators.map((indicator, i) => (
                    <span
                      key={i}
                      className="text-[10px] px-1.5 py-0.5 bg-amber-100 text-amber-700 rounded"
                    >
                      "{indicator}"
                    </span>
                  ))}
                </div>
              </div>
            )}

            {sentiment.frustration_indicators.length > 0 && (
              <div>
                <p className="text-xs text-rose-600 font-medium mb-1 flex items-center gap-1">
                  <AlertCircle className="w-3 h-3" />
                  Frustration signals
                </p>
                <div className="flex flex-wrap gap-1">
                  {sentiment.frustration_indicators.map((indicator, i) => (
                    <span
                      key={i}
                      className="text-[10px] px-1.5 py-0.5 bg-rose-100 text-rose-700 rounded"
                    >
                      "{indicator}"
                    </span>
                  ))}
                </div>
              </div>
            )}

            {sentiment.positive_indicators.length > 0 && (
              <div>
                <p className="text-xs text-emerald-600 font-medium mb-1 flex items-center gap-1">
                  <Smile className="w-3 h-3" />
                  Positive signals
                </p>
                <div className="flex flex-wrap gap-1">
                  {sentiment.positive_indicators.map((indicator, i) => (
                    <span
                      key={i}
                      className="text-[10px] px-1.5 py-0.5 bg-emerald-100 text-emerald-700 rounded"
                    >
                      "{indicator}"
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Suggested Response */}
            {sentiment.needs_intervention && (
              <div className="p-2 bg-brand-50 rounded border border-brand-100">
                <p className="text-xs text-brand-700 font-medium mb-1">
                  Suggested Response:
                </p>
                <p className="text-xs text-brand-600">
                  {sentiment.suggested_response}
                </p>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
}

// Client-side sentiment analysis for demo
function analyzeClientSide(message: string): SentimentData {
  const lower = message.toLowerCase();
  
  const confusionKeywords = ["confused", "don't understand", "lost", "unclear", "huh", "what", "how"];
  const frustrationKeywords = ["frustrated", "stuck", "can't", "difficult", "hard", "error", "bug"];
  const positiveKeywords = ["got it", "understood", "thanks", "clear", "awesome", "great"];
  const excitementKeywords = ["cool", "amazing", "love", "excited", "interesting", "fun"];
  
  const confusionCount = confusionKeywords.filter(kw => lower.includes(kw)).length;
  const frustrationCount = frustrationKeywords.filter(kw => lower.includes(kw)).length;
  const positiveCount = positiveKeywords.filter(kw => lower.includes(kw)).length;
  const excitementCount = excitementKeywords.filter(kw => lower.includes(kw)).length;
  
  const scores: Record<string, number> = {
    confused: confusionCount * 1.5,
    frustrated: frustrationCount * 2,
    satisfied: positiveCount * 1.5,
    excited: excitementCount * 1.5,
    neutral: 0.5,
  };
  
  const state = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
  
  return {
    emotional_state: state,
    confidence: Math.min(1, Math.max(scores[state] / 3, 0.3)),
    engagement_score: (positiveCount + excitementCount - confusionCount - frustrationCount) / 5,
    confusion_indicators: confusionKeywords.filter(kw => lower.includes(kw)).slice(0, 3),
    frustration_indicators: frustrationKeywords.filter(kw => lower.includes(kw)).slice(0, 3),
    positive_indicators: [...positiveKeywords, ...excitementKeywords].filter(kw => lower.includes(kw)).slice(0, 3),
    help_seeking: confusionCount > 0 || frustrationCount > 0,
    needs_intervention: state === "frustrated" || (state === "confused" && confusionCount >= 2),
    suggested_response: state === "frustrated" 
      ? "I notice you might be frustrated. Let's break this down step by step."
      : state === "confused"
      ? "This concept can be tricky. Let me explain it differently."
      : state === "excited"
      ? "Love your enthusiasm! Let's explore this further."
      : "Thanks for your message! Let me respond.",
  };
}
