import { useState } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { 
  experimentManager, 
  DEFAULT_EXPERIMENTS,
  useExperiment 
} from "@/hooks/useExperiment";
import { FlaskConical, Target, BarChart3, RotateCcw, CheckCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function ExperimentPanel({ className }: { className?: string }) {
  const [activeExperiments] = useState(() => DEFAULT_EXPERIMENTS);
  const [resetKey, setResetKey] = useState(0);

  const handleReset = () => {
    experimentManager.reset();
    setResetKey(prev => prev + 1);
    window.location.reload();
  };

  const handleForceVariant = (experimentId: string, variantId: string) => {
    experimentManager.forceVariant(experimentId, variantId);
    setResetKey(prev => prev + 1);
  };

  return (
    <Card padding="lg" className={className}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-100 rounded-lg">
            <FlaskConical className="w-5 h-5 text-purple-600" />
          </div>
          <div>
            <h3 className="font-semibold text-stone-900">A/B Testing</h3>
            <p className="text-sm text-stone-500">Experiment Configuration</p>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          icon={RotateCcw}
          onClick={handleReset}
        >
          Reset All
        </Button>
      </div>

      <div className="space-y-4">
        {activeExperiments.map((experiment) => (
          <ExperimentItem
            key={`${experiment.id}-${resetKey}`}
            experiment={experiment}
            onForceVariant={handleForceVariant}
          />
        ))}
      </div>

      <div className="mt-6 p-4 bg-stone-50 rounded-lg">
        <p className="text-xs text-stone-600">
          <strong>How it works:</strong> Experiments randomly assign users to different variants.
          Changes take effect after page reload. Use &quot;Reset All&quot; to clear all assignments.
        </p>
      </div>
    </Card>
  );
}

function ExperimentItem({ 
  experiment, 
  onForceVariant 
}: { 
  experiment: typeof DEFAULT_EXPERIMENTS[0];
  onForceVariant: (expId: string, varId: string) => void;
}) {
  const { variant, isInVariant, trackEvent } = useExperiment(experiment.id);
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div className="border border-stone-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setShowDetails(!showDetails)}
        className="w-full p-4 flex items-center justify-between bg-white hover:bg-stone-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Target className="w-5 h-5 text-stone-400" />
          <div className="text-left">
            <p className="font-medium text-stone-900">{experiment.name}</p>
            <p className="text-xs text-stone-500">{experiment.description}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {variant && (
            <span className="text-xs px-2 py-1 bg-brand-100 text-brand-700 rounded-full font-medium">
              {variant.name}
            </span>
          )}
          <BarChart3 className="w-4 h-4 text-stone-400" />
        </div>
      </button>

      <AnimatePresence>
        {showDetails && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-stone-200 bg-stone-50/50"
          >
            <div className="p-4 space-y-3">
              <p className="text-xs font-medium text-stone-500 uppercase tracking-wide">
                Variants
              </p>
              <div className="grid gap-2">
                {experiment.variants.map((v) => {
                  const isActive = isInVariant(v.id);
                  return (
                    <div
                      key={v.id}
                      className={`flex items-center justify-between p-3 rounded-lg border transition-colors ${
                        isActive
                          ? "bg-brand-50 border-brand-200"
                          : "bg-white border-stone-200 hover:border-stone-300"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        {isActive ? (
                          <CheckCircle className="w-4 h-4 text-brand-500" />
                        ) : (
                          <div className="w-4 h-4 rounded-full border-2 border-stone-300" />
                        )}
                        <span className={`text-sm ${isActive ? "font-medium text-stone-900" : "text-stone-600"}`}>
                          {v.name}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs text-stone-400">{v.weight}%</span>
                        {!isActive && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              onForceVariant(experiment.id, v.id);
                              trackEvent("manual_variant_assignment", { variantId: v.id });
                            }}
                          >
                            Force
                          </Button>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              {variant?.payload && (
                <div className="mt-3 p-3 bg-amber-50 rounded-lg">
                  <p className="text-xs font-medium text-amber-800 mb-1">Active Payload:</p>
                  <pre className="text-xs text-amber-700 overflow-auto">
                    {JSON.stringify(variant.payload, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
