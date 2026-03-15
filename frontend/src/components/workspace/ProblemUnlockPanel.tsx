import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Lock, Unlock, Lightbulb, BookOpen, ArrowRight, CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { ROUTES } from "@/lib/constants";

interface ProblemUnlockPanelProps {
  problems: Array<{
    problem_id: string;
    problem_statement: string;
    difficulty?: string;
    knowledge_units_required?: string[];
  }>;
  eligibleIds: string[];
  learnedUnitIds: string[];
  requiredKus: string[];
  currentTaId: number | null;
}

export function ProblemUnlockPanel({
  problems,
  eligibleIds,
  learnedUnitIds,
  requiredKus,
  currentTaId,
}: ProblemUnlockPanelProps) {
  const unlockedCount = eligibleIds.length;
  const totalCount = problems.length;
  const lockedProblems = problems.filter(p => !eligibleIds.includes(p.problem_id));
  
  // Find the problem that's closest to being unlocked
  const nearestUnlockable = lockedProblems
    .map(p => {
      const required = p.knowledge_units_required ?? [];
      const learned = required.filter(ku => learnedUnitIds.includes(ku));
      return {
        ...p,
        progress: required.length > 0 ? learned.length / required.length : 0,
        learnedCount: learned.length,
        requiredCount: required.length,
        missing: required.filter(ku => !learnedUnitIds.includes(ku)),
      };
    })
    .sort((a, b) => b.progress - a.progress)[0];

  const overallProgress = requiredKus.length > 0
    ? learnedUnitIds.length / requiredKus.length
    : 0;

  if (problems.length === 0) {
    return (
      <Card padding="lg" className="bg-gradient-to-r from-amber-50 to-orange-50 border-amber-200">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-amber-100 rounded-xl">
            <BookOpen className="w-6 h-6 text-amber-600" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-amber-900 text-lg">No Problems Available Yet</h3>
            <p className="mt-2 text-sm text-amber-800">
              Your TA needs to learn some basic concepts before it can attempt any problems.
              Start by teaching fundamental concepts like variables or basic operations.
            </p>
            <div className="mt-4">
              <Link to={ROUTES.teach}>
                <Button variant="primary" size="sm" icon={ArrowRight}>
                  Start Teaching
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card padding="lg">
      <div className="space-y-6">
        {/* Overall Progress */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-slate-900">Problem Unlock Progress</h3>
            <span className="text-sm text-slate-500">
              {unlockedCount} / {totalCount} unlocked
            </span>
          </div>
          <ProgressBar 
            value={overallProgress * 100} 
            className="h-2"
            color={unlockedCount === totalCount ? "success" : "brand"}
          />
          <p className="mt-2 text-xs text-slate-500">
            {learnedUnitIds.length} of {requiredKus.length} required concepts learned
          </p>
        </div>

        {/* Nearest Unlockable Problem */}
        {nearestUnlockable && unlockedCount < totalCount && (
          <div className="bg-brand-50 rounded-xl p-4 border border-brand-100">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-brand-100 rounded-lg">
                <Unlock className="w-5 h-5 text-brand-600" />
              </div>
              <div className="flex-1">
                <h4 className="font-medium text-slate-900">Closest to Unlock</h4>
                <p className="text-sm text-slate-600 mt-1">
                  {nearestUnlockable.problem_statement.slice(0, 80)}...
                </p>
                <div className="mt-3">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="text-slate-500">
                      {nearestUnlockable.learnedCount} / {nearestUnlockable.requiredCount} prerequisites learned
                    </span>
                    <span className="text-brand-600 font-medium">
                      {Math.round(nearestUnlockable.progress * 100)}%
                    </span>
                  </div>
                  <ProgressBar 
                    value={nearestUnlockable.progress * 100} 
                    className="h-1.5"
                    color="brand"
                  />
                </div>
                {nearestUnlockable.missing.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1">
                    <span className="text-xs text-slate-500">Still need:</span>
                    {nearestUnlockable.missing.slice(0, 3).map(ku => (
                      <span 
                        key={ku} 
                        className="text-xs px-2 py-0.5 bg-white rounded border border-slate-200 text-slate-600"
                      >
                        {ku.replace(/_/g, ' ')}
                      </span>
                    ))}
                    {nearestUnlockable.missing.length > 3 && (
                      <span className="text-xs text-slate-400">
                        +{nearestUnlockable.missing.length - 3} more
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* All Unlocked */}
        {unlockedCount === totalCount && totalCount > 0 && (
          <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-emerald-100 rounded-lg">
                <CheckCircle className="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <h4 className="font-medium text-emerald-900">All Problems Unlocked!</h4>
                <p className="text-sm text-emerald-700 mt-1">
                  Your TA has learned all the required concepts. You can now run comprehensive tests.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Locked Problems Preview */}
        {lockedProblems.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-slate-700 mb-3 flex items-center gap-2">
              <Lock className="w-4 h-4" />
              Locked Problems ({lockedProblems.length})
            </h4>
            <div className="space-y-2 max-h-[200px] overflow-y-auto pr-2">
              {lockedProblems.slice(0, 5).map(problem => {
                const required = problem.knowledge_units_required ?? [];
                const learned = required.filter(ku => learnedUnitIds.includes(ku));
                const progress = required.length > 0 ? learned.length / required.length : 0;
                
                return (
                  <div 
                    key={problem.problem_id} 
                    className="flex items-center gap-3 p-3 bg-slate-50 rounded-lg opacity-75"
                  >
                    <Lock className="w-4 h-4 text-slate-400 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-slate-600 truncate">
                        {problem.problem_statement.slice(0, 60)}...
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 h-1 bg-slate-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-slate-400 rounded-full"
                            style={{ width: `${progress * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-slate-400">
                          {learned.length}/{required.length}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
              {lockedProblems.length > 5 && (
                <p className="text-xs text-slate-400 text-center py-2">
                  +{lockedProblems.length - 5} more locked problems
                </p>
              )}
            </div>
          </div>
        )}

        {/* Tip */}
        <div className="flex items-start gap-2 text-xs text-slate-500 bg-slate-50 p-3 rounded-lg">
          <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <p>
            Tip: Teach your TA the missing concepts to unlock more problems. 
            Each problem requires specific knowledge units to be learned first.
          </p>
        </div>
      </div>
    </Card>
  );
}
