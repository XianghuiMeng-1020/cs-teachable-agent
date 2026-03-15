import { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { X, ChevronRight, ChevronLeft, Sparkles, MessageSquare, Target, BarChart3, Award } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface GuideStep {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
  target?: string;
  position?: "top" | "bottom" | "left" | "right";
}

const guideSteps: GuideStep[] = [
  {
    id: "welcome",
    title: "Welcome to CS Teachable Agent! 👋",
    description: "This is your personal AI learning companion. I'll guide you through the key features to help you get started.",
    icon: Sparkles,
  },
  {
    id: "teach",
    title: "Teach Your TA 📚",
    description: "Go to 'Teach TA' to start teaching your AI companion. Explain concepts in your own words - the better you teach, the better it learns!",
    icon: MessageSquare,
    target: "[href='/teach']",
  },
  {
    id: "test",
    title: "Test Understanding 📝",
    description: "Visit 'Test TA' to run comprehensive tests. You'll unlock more problems as your TA learns new concepts.",
    icon: Target,
    target: "[href='/test']",
  },
  {
    id: "analytics",
    title: "Track Your Progress 📊",
    description: "Check 'Analytics' to see detailed insights about your learning journey, including 3D knowledge graphs and achievement badges!",
    icon: BarChart3,
    target: "[href='/learning-analytics']",
  },
  {
    id: "achievements",
    title: "Earn Achievements 🏆",
    description: "Complete lessons, help peers, and maintain streaks to unlock badges and earn points. Can you collect them all?",
    icon: Award,
  },
];

const GUIDE_COMPLETED_KEY = "user_guide_completed_v1";

export function UserGuide() {
  const [isOpen, setIsOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [hasSeenGuide, setHasSeenGuide] = useState(true);

  useEffect(() => {
    const completed = localStorage.getItem(GUIDE_COMPLETED_KEY);
    if (!completed) {
      setHasSeenGuide(false);
      // Show guide after a short delay
      const timer = setTimeout(() => setIsOpen(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleNext = useCallback(() => {
    if (currentStep < guideSteps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      handleComplete();
    }
  }, [currentStep]);

  const handlePrev = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  }, [currentStep]);

  const handleComplete = useCallback(() => {
    localStorage.setItem(GUIDE_COMPLETED_KEY, "true");
    setHasSeenGuide(true);
    setIsOpen(false);
  }, []);

  const handleSkip = useCallback(() => {
    localStorage.setItem(GUIDE_COMPLETED_KEY, "true");
    setHasSeenGuide(true);
    setIsOpen(false);
  }, []);

  const restartGuide = useCallback(() => {
    setCurrentStep(0);
    setIsOpen(true);
  }, []);

  const step = guideSteps[currentStep];
  const Icon = step.icon;
  const progress = ((currentStep + 1) / guideSteps.length) * 100;

  if (!isOpen) {
    // Show restart button in corner if guide was completed
    if (hasSeenGuide) {
      return (
        <button
          onClick={restartGuide}
          className="fixed bottom-4 right-4 z-40 p-3 bg-brand-500 text-white rounded-full shadow-lg hover:bg-brand-600 hover:shadow-xl transition-all duration-200 hover:scale-110"
          title="Restart Guide"
        >
          <Sparkles className="w-5 h-5" />
        </button>
      );
    }
    return null;
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        onClick={handleSkip}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
          className="w-full max-w-md"
          onClick={e => e.stopPropagation()}
        >
          <Card padding="none" className="overflow-hidden">
            {/* Header with Progress */}
            <div className="bg-gradient-to-r from-brand-500 to-brand-600 p-6 text-white">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium opacity-90">
                  Step {currentStep + 1} of {guideSteps.length}
                </span>
                <button
                  onClick={handleSkip}
                  className="p-1 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              {/* Progress Bar */}
              <div className="h-1.5 bg-white/30 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-white rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>

            {/* Content */}
            <div className="p-6">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-brand-100 rounded-xl shrink-0">
                  <Icon className="w-8 h-8 text-brand-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-slate-600 leading-relaxed">
                    {step.description}
                  </p>
                </div>
              </div>

              {/* Navigation */}
              <div className="flex items-center justify-between mt-8">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handlePrev}
                  disabled={currentStep === 0}
                  icon={ChevronLeft}
                >
                  Back
                </Button>

                <div className="flex gap-2">
                  {guideSteps.map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setCurrentStep(idx)}
                      className={`w-2 h-2 rounded-full transition-colors ${
                        idx === currentStep
                          ? "bg-brand-500"
                          : idx < currentStep
                          ? "bg-brand-300"
                          : "bg-slate-200"
                      }`}
                    />
                  ))}
                </div>

                <Button
                  variant="primary"
                  size="sm"
                  onClick={handleNext}
                  iconRight={currentStep === guideSteps.length - 1 ? undefined : ChevronRight}
                >
                  {currentStep === guideSteps.length - 1 ? "Get Started!" : "Next"}
                </Button>
              </div>
            </div>

            {/* Skip Option */}
            <div className="px-6 pb-4 text-center">
              <button
                onClick={handleSkip}
                className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
              >
                Skip guide (you can restart it later)
              </button>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
