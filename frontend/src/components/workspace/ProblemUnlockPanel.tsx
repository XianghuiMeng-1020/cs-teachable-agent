import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Lock, Unlock, Lightbulb, BookOpen, ArrowRight, CheckCircle, Target, Sparkles, TrendingUp } from "lucide-react";
import { Link } from "react-router-dom";
import { ROUTES } from "@/lib/constants";
import { motion } from "framer-motion";

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
            <h3 className="font-semibold text-amber-900 text-lg">📚 No Problems Available Yet</h3>
            <p className="mt-2 text-sm text-amber-800">
              Your TA needs to learn some basic concepts before it can attempt any problems.
              Start by teaching fundamental concepts like variables or basic operations.
            </p>
            <div className="mt-4 flex items-center gap-3">
              <Link to={ROUTES.teach}>
                <Button variant="primary" size="sm" icon={ArrowRight}>
                  Start Teaching
                </Button>
              </Link>
              <span className="text-xs text-amber-600">
                💡 Tip: Teaching 3-5 concepts will unlock your first problem!
              </span>
            </div>
          </div>
        </div>
      </Card>
    );
  }

  // Calculate how many more concepts needed to unlock next problem
  const conceptsNeeded = nearestUnlockable && nearestUnlockable.missing.length > 0
    ? nearestUnlockable.missing.length
    : 0;

  return (
    <Card padding="lg">
      <div className="space-y-6">
        {/* Overall Progress */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-semibold text-stone-900 flex items-center gap-2">
              <Target className="w-5 h-5 text-brand-500" />
              Problem Unlock Progress
            </h3>
            <span className="text-sm font-medium text-stone-600">
              {unlockedCount} / {totalCount} unlocked
            </span>
          </div>
          <ProgressBar 
            value={overallProgress * 100} 
            className="h-3"
            color={unlockedCount === totalCount ? "success" : "brand"}
          />
          <div className="mt-2 flex items-center justify-between">
            <p className="text-xs text-stone-500">
              {learnedUnitIds.length} of {requiredKus.length} required concepts learned
            </p>
            {conceptsNeeded > 0 && (
              <p className="text-xs font-medium text-brand-600">
                🔓 Teach {conceptsNeeded} more concept{conceptsNeeded > 1 ? 's' : ''} to unlock next problem!
              </p>
            )}
          </div>
        </div>

        {/* Nearest Unlockable Problem */}
        {nearestUnlockable && unlockedCount < totalCount && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-r from-brand-50 to-indigo-50 rounded-xl p-4 border-2 border-brand-200 shadow-sm"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 bg-brand-100 rounded-lg">
                <Sparkles className="w-5 h-5 text-brand-600" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold text-stone-900">🎯 Closest to Unlock</h4>
                  <span className="text-xs px-2 py-0.5 bg-brand-100 text-brand-700 rounded-full font-medium">
                    {Math.round(nearestUnlockable.progress * 100)}% Ready
                  </span>
                </div>
                <p className="text-sm text-stone-600 mt-1 line-clamp-2">
                  {nearestUnlockable.problem_statement}
                </p>
                
                {/* Progress Section */}
                <div className="mt-3 bg-white/60 rounded-lg p-3">
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-stone-600 font-medium">
                      {nearestUnlockable.learnedCount} / {nearestUnlockable.requiredCount} prerequisites learned
                    </span>
                    <TrendingUp className="w-4 h-4 text-brand-500" />
                  </div>
                  <ProgressBar 
                    value={nearestUnlockable.progress * 100} 
                    className="h-2"
                    color="brand"
                  />
                </div>

                {/* Missing Concepts - Enhanced */}
                {nearestUnlockable.missing.length > 0 && (
                  <div className="mt-3">
                    <p className="text-xs font-medium text-stone-700 mb-2">
                      📖 Teach these concepts to unlock:
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {nearestUnlockable.missing.map(ku => (
                        <span 
                          key={ku} 
                          className="text-xs px-2.5 py-1 bg-white rounded-md border border-brand-200 text-brand-700 font-medium shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                          title={`Click to teach ${ku.replace(/_/g, ' ')}`}
                        >
                          {ku.replace(/_/g, ' ')}
                        </span>
                      ))}
                    </div>
                    <Link to={ROUTES.teach} className="block mt-3">
                      <Button variant="primary" size="sm" className="w-full" icon={ArrowRight}>
                        Teach These Concepts Now
                      </Button>
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
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
            <h4 className="text-sm font-medium text-stone-700 mb-3 flex items-center gap-2">
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
                    className="flex items-center gap-3 p-3 bg-stone-50 rounded-lg opacity-75"
                  >
                    <Lock className="w-4 h-4 text-stone-400 shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-stone-600 truncate">
                        {problem.problem_statement.slice(0, 60)}...
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <div className="flex-1 h-1 bg-stone-200 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-stone-400 rounded-full"
                            style={{ width: `${progress * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-stone-400">
                          {learned.length}/{required.length}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
              {lockedProblems.length > 5 && (
                <p className="text-xs text-stone-400 text-center py-2">
                  +{lockedProblems.length - 5} more locked problems
                </p>
              )}
            </div>
          </div>
        )}

        {/* Enhanced Tip */}
        <div className="flex items-start gap-3 text-sm bg-gradient-to-r from-amber-50 to-yellow-50 p-4 rounded-xl border border-amber-200">
          <div className="p-1.5 bg-amber-100 rounded-lg shrink-0">
            <Lightbulb className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <p className="font-medium text-amber-900 mb-1">
              💡 How to unlock more problems?
            </p>
            <p className="text-amber-800 text-xs leading-relaxed">
              Each problem requires specific knowledge units. Teach your TA the missing concepts shown above to unlock them. 
              The more concepts you teach, the more problems become available!
            </p>
          </div>
        </div>
      </div>
    </Card>
  );
}
