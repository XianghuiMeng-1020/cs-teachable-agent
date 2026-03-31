import { useState } from "react";
import { Link } from "react-router-dom";
import { 
  BookOpen, 
  Clock, 
  ChevronRight, 
  MapPin, 
  Target, 
  Sparkles,
  TrendingUp,
  Lightbulb,
  CheckCircle2,
  Lock,
  Zap,
  ArrowRight
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";

interface SmartPathNode {
  id: string;
  name: string;
  topic_group: string;
  prerequisites: string[];
  difficulty: number;
  estimated_minutes: number;
}

interface PathSummary {
  total_estimated_minutes: number;
  average_difficulty: number;
  confidence: number;
  rationale: string;
  path_length: number;
}

interface SmartLearningPathProps {
  recommended: SmartPathNode[];
  pathSummary?: PathSummary;
  learnedCount: number;
  totalCount: number;
  className?: string;
  onStartLearning?: (nodeId: string) => void;
}

const DIFFICULTY_COLORS = {
  1: { bg: "bg-emerald-100", text: "text-emerald-700", label: "Beginner" },
  2: { bg: "bg-brand-100", text: "text-brand-700", label: "Easy" },
  3: { bg: "bg-amber-100", text: "text-amber-700", label: "Medium" },
  4: { bg: "bg-orange-100", text: "text-orange-700", label: "Hard" },
  5: { bg: "bg-rose-100", text: "text-rose-700", label: "Expert" },
};

function getDifficultyStyle(difficulty: number) {
  const rounded = Math.round(difficulty);
  return DIFFICULTY_COLORS[rounded as keyof typeof DIFFICULTY_COLORS] || DIFFICULTY_COLORS[3];
}

function formatTopicGroup(group: string): string {
  return group
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export function SmartLearningPath({
  recommended,
  pathSummary,
  learnedCount,
  totalCount,
  className,
  onStartLearning,
}: SmartLearningPathProps) {
  const [expandedNode, setExpandedNode] = useState<string | null>(null);
  const [showRationale, setShowRationale] = useState(false);

  const pct = totalCount ? Math.round((learnedCount / totalCount) * 100) : 0;
  const remainingCount = totalCount - learnedCount;

  // Group nodes by topic for visualization
  const topicGroups: Record<string, SmartPathNode[]> = {};
  recommended.forEach((node) => {
    if (!topicGroups[node.topic_group]) {
      topicGroups[node.topic_group] = [];
    }
    topicGroups[node.topic_group].push(node);
  });

  const hasPath = recommended.length > 0;
  const isComplete = remainingCount === 0;

  if (isComplete) {
    return (
      <Card padding="lg" className={cn("bg-gradient-to-br from-emerald-50 to-brand-50 border-emerald-200", className)}>
        <div className="text-center">
          <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle2 className="w-8 h-8 text-emerald-600" />
          </div>
          <h3 className="text-lg font-semibold text-emerald-900">Learning Complete!</h3>
          <p className="text-emerald-700 mt-2">
            You've mastered all {totalCount} concepts. Excellent work!
          </p>
          <div className="mt-4">
            <Link to={ROUTES.test}>
              <Button variant="primary" icon={Zap}>
                Run Comprehensive Test
              </Button>
            </Link>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card padding="lg" className={cn("overflow-hidden", className)}>
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="p-2 bg-brand-100 rounded-lg">
              <MapPin className="w-5 h-5 text-brand-600" />
            </div>
            <h3 className="text-lg font-semibold text-stone-900">Your Smart Learning Path</h3>
          </div>
          <p className="text-sm text-stone-500 mt-1">
            {hasPath 
              ? `Optimized path covering ${recommended.length} concepts across ${Object.keys(topicGroups).length} topics`
              : "Start teaching to unlock personalized recommendations"
            }
          </p>
        </div>
        
        {pathSummary && (
          <div className="flex items-center gap-2 text-xs">
            <span className={cn(
              "px-2 py-1 rounded-full font-medium",
              pathSummary.confidence > 0.7 ? "bg-emerald-100 text-emerald-700" :
              pathSummary.confidence > 0.4 ? "bg-amber-100 text-amber-700" :
              "bg-stone-100 text-stone-600"
            )}>
              {Math.round(pathSummary.confidence * 100)}% confidence
            </span>
          </div>
        )}
      </div>

      {/* Overall Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-stone-600">Overall Progress</span>
          <span className="font-medium text-stone-900">{learnedCount} / {totalCount} concepts</span>
        </div>
        <ProgressBar value={pct} className="h-2.5" color={pct > 70 ? "success" : pct > 40 ? "brand" : "warning"} />
        <div className="flex items-center justify-between text-xs text-stone-500 mt-2">
          <span>{remainingCount} remaining</span>
          {pathSummary && (
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" />
              ~{pathSummary.total_estimated_minutes} min to complete
            </span>
          )}
        </div>
      </div>

      {/* AI Rationale */}
      {pathSummary?.rationale && (
        <div className="mb-6">
          <button
            onClick={() => setShowRationale(!showRationale)}
            className="flex items-center gap-2 text-sm text-brand-600 hover:text-brand-700"
          >
            <Sparkles className="w-4 h-4" />
            <span>Why this path?</span>
            <ChevronRight className={cn("w-4 h-4 transition-transform", showRationale && "rotate-90")} />
          </button>
          
          {showRationale && (
            <div className="mt-3 p-3 bg-brand-50 rounded-lg text-sm text-stone-700">
              <div className="flex items-start gap-2">
                <Lightbulb className="w-4 h-4 text-brand-500 mt-0.5 shrink-0" />
                <p>{pathSummary.rationale}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Path Visualization */}
      {hasPath ? (
        <div className="space-y-4">
          {recommended.map((node, index) => {
            const difficulty = getDifficultyStyle(node.difficulty);
            const isExpanded = expandedNode === node.id;
            const isLast = index === recommended.length - 1;
            
            return (
              <div key={node.id} className="relative">
                {/* Connection line */}
                {!isLast && (
                  <div className="absolute left-6 top-12 w-0.5 h-6 bg-stone-200" />
                )}
                
                <div
                  className={cn(
                    "flex items-start gap-3 p-3 rounded-xl border transition-all cursor-pointer",
                    isExpanded 
                      ? "border-brand-300 bg-brand-50 shadow-sm" 
                      : "border-stone-200 hover:border-stone-300 hover:bg-stone-50"
                  )}
                  onClick={() => setExpandedNode(isExpanded ? null : node.id)}
                >
                  {/* Node indicator */}
                  <div className={cn(
                    "w-12 h-12 rounded-xl flex items-center justify-center shrink-0",
                    difficulty.bg
                  )}>
                    <span className={cn("text-lg font-bold", difficulty.text)}>
                      {index + 1}
                    </span>
                  </div>
                  
                  {/* Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <h4 className="font-medium text-stone-900">{node.name}</h4>
                        <div className="flex items-center gap-2 mt-1">
                          <span className={cn("text-xs px-2 py-0.5 rounded-full font-medium", difficulty.bg, difficulty.text)}>
                            {difficulty.label}
                          </span>
                          <span className="text-xs text-stone-500 flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {node.estimated_minutes} min
                          </span>
                        </div>
                      </div>
                      <ChevronRight className={cn(
                        "w-5 h-5 text-stone-400 transition-transform shrink-0",
                        isExpanded && "rotate-90"
                      )} />
                    </div>
                    
                    {/* Expanded details */}
                    {isExpanded && (
                      <div className="mt-3 pt-3 border-t border-stone-200 space-y-2">
                        <div className="flex items-center gap-2 text-sm">
                          <Target className="w-4 h-4 text-stone-400" />
                          <span className="text-stone-600">Topic: {formatTopicGroup(node.topic_group)}</span>
                        </div>
                        
                        {node.prerequisites.length > 0 && (
                          <div className="flex items-start gap-2 text-sm">
                            <Lock className="w-4 h-4 text-stone-400 mt-0.5" />
                            <div>
                              <span className="text-stone-600">Prerequisites: </span>
                              <span className="text-stone-500">
                                {node.prerequisites.map(formatTopicGroup).join(", ")}
                              </span>
                            </div>
                          </div>
                        )}
                        
                        <div className="pt-2">
                          <Button
                            size="sm"
                            variant="primary"
                            onClick={(e) => {
                              e.stopPropagation();
                              onStartLearning?.(node.id);
                            }}
                            className="w-full"
                            icon={ArrowRight}
                          >
                            Start Learning This
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="text-center py-8 bg-stone-50 rounded-xl">
          <BookOpen className="w-12 h-12 text-stone-300 mx-auto mb-3" />
          <p className="text-stone-500">Teach your first concept to see personalized recommendations</p>
          <div className="mt-4">
            <Link to={ROUTES.teach}>
              <Button variant="primary" size="sm" icon={ArrowRight}>
                Start Teaching
              </Button>
            </Link>
          </div>
        </div>
      )}

      {/* Stats */}
      {pathSummary && (
        <div className="mt-6 pt-6 border-t border-stone-200 grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="flex items-center justify-center gap-1 text-stone-500 mb-1">
              <TrendingUp className="w-4 h-4" />
              <span className="text-xs">Difficulty</span>
            </div>
            <p className="text-lg font-semibold text-stone-900">
              {pathSummary.average_difficulty.toFixed(1)}/5
            </p>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center gap-1 text-stone-500 mb-1">
              <Clock className="w-4 h-4" />
              <span className="text-xs">Est. Time</span>
            </div>
            <p className="text-lg font-semibold text-stone-900">
              {pathSummary.total_estimated_minutes}m
            </p>
          </div>
          <div className="text-center">
            <div className="flex items-center justify-center gap-1 text-stone-500 mb-1">
              <Target className="w-4 h-4" />
              <span className="text-xs">Concepts</span>
            </div>
            <p className="text-lg font-semibold text-stone-900">
              {pathSummary.path_length}
            </p>
          </div>
        </div>
      )}
    </Card>
  );
}
