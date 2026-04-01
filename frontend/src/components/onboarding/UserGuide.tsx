import { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import {
  X,
  ChevronRight,
  ChevronLeft,
  Sparkles,
  MessageSquare,
  Target,
  BarChart3,
  BookOpenCheck,
  BookOpen,
  Brain,
  Rocket,
  Globe,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface GuideStep {
  id: string;
  titleKey: string;
  descKey: string;
  icon: React.ElementType;
  color: string;
}

const STEPS: GuideStep[] = [
  { id: "welcome", titleKey: "tutorial.step1Title", descKey: "tutorial.step1Desc", icon: Sparkles, color: "from-brand-500 to-brand-600" },
  { id: "domain", titleKey: "tutorial.step2Title", descKey: "tutorial.step2Desc", icon: Globe, color: "from-violet-500 to-indigo-600" },
  { id: "teach", titleKey: "tutorial.step3Title", descKey: "tutorial.step3Desc", icon: MessageSquare, color: "from-emerald-500 to-teal-600" },
  { id: "test", titleKey: "tutorial.step4Title", descKey: "tutorial.step4Desc", icon: Target, color: "from-rose-500 to-pink-600" },
  { id: "practice", titleKey: "tutorial.step5Title", descKey: "tutorial.step5Desc", icon: BookOpenCheck, color: "from-amber-500 to-orange-600" },
  { id: "mastery", titleKey: "tutorial.step6Title", descKey: "tutorial.step6Desc", icon: BookOpen, color: "from-cyan-500 to-blue-600" },
  { id: "analytics", titleKey: "tutorial.step7Title", descKey: "tutorial.step7Desc", icon: Brain, color: "from-fuchsia-500 to-purple-600" },
  { id: "done", titleKey: "tutorial.step8Title", descKey: "tutorial.step8Desc", icon: Rocket, color: "from-brand-500 to-emerald-600" },
];

const GUIDE_COMPLETED_KEY = "arts_cs_onboarding_v2";

interface UserGuideProps {
  forceOpen?: boolean;
}

export function UserGuide({ forceOpen }: UserGuideProps) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [hasSeenGuide, setHasSeenGuide] = useState(true);

  useEffect(() => {
    if (forceOpen) {
      setCurrentStep(0);
      setIsOpen(true);
      return;
    }
    const completed = localStorage.getItem(GUIDE_COMPLETED_KEY);
    if (!completed) {
      setHasSeenGuide(false);
      const timer = setTimeout(() => setIsOpen(true), 800);
      return () => clearTimeout(timer);
    }
  }, [forceOpen]);

  const handleNext = useCallback(() => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      handleComplete();
    }
  }, [currentStep]);

  const handlePrev = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
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

  const step = STEPS[currentStep];
  const Icon = step.icon;
  const progress = ((currentStep + 1) / STEPS.length) * 100;

  if (!isOpen) {
    if (hasSeenGuide) {
      return (
        <button
          onClick={restartGuide}
          className="fixed bottom-20 right-4 z-40 flex items-center gap-2 rounded-full bg-gradient-to-r from-brand-500 to-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105"
          title={t("tutorial.restartGuide")}
        >
          <Sparkles className="w-4 h-4" />
          <span className="hidden sm:inline">{t("tutorial.restartGuide")}</span>
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
        className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
        onClick={handleSkip}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 30 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 30 }}
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
          className="w-full max-w-lg"
          onClick={(e) => e.stopPropagation()}
        >
          <Card padding="none" className="overflow-hidden shadow-2xl">
            {/* Header with gradient and progress */}
            <div className={`bg-gradient-to-r ${step.color} p-6 text-white relative overflow-hidden`}>
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_30%,rgba(255,255,255,0.15),transparent)]" />
              <div className="relative">
                <div className="flex items-center justify-between mb-4">
                  <span className="text-sm font-medium opacity-90">
                    {t("tutorial.stepOf", { current: currentStep + 1, total: STEPS.length })}
                  </span>
                  <button
                    onClick={handleSkip}
                    className="p-1.5 hover:bg-white/20 rounded-full transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                {/* Step indicators */}
                <div className="flex gap-1.5 mb-4">
                  {STEPS.map((_, idx) => (
                    <button
                      key={idx}
                      onClick={() => setCurrentStep(idx)}
                      className={`h-1.5 rounded-full transition-all duration-300 ${
                        idx === currentStep
                          ? "bg-white w-8"
                          : idx < currentStep
                            ? "bg-white/60 w-4"
                            : "bg-white/30 w-4"
                      }`}
                    />
                  ))}
                </div>

                {/* Progress bar */}
                <div className="h-1 bg-white/20 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-white rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.4, ease: "easeOut" }}
                  />
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="p-6">
              <AnimatePresence mode="wait">
                <motion.div
                  key={step.id}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.25 }}
                  className="flex items-start gap-4"
                >
                  <div className={`p-3 bg-gradient-to-br ${step.color} rounded-xl shrink-0 shadow-lg`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="min-w-0">
                    <h3 className="text-xl font-bold text-stone-900 mb-2">
                      {t(step.titleKey)}
                    </h3>
                    <p className="text-stone-600 leading-relaxed whitespace-pre-line">
                      {t(step.descKey)}
                    </p>
                  </div>
                </motion.div>
              </AnimatePresence>

              {/* Navigation */}
              <div className="flex items-center justify-between mt-8 pt-4 border-t border-stone-100">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handlePrev}
                  disabled={currentStep === 0}
                  icon={ChevronLeft}
                >
                  {t("common.back")}
                </Button>

                <Button
                  variant="primary"
                  size="sm"
                  onClick={handleNext}
                  iconRight={currentStep === STEPS.length - 1 ? undefined : ChevronRight}
                >
                  {currentStep === STEPS.length - 1
                    ? t("common.getStarted")
                    : t("common.next")}
                </Button>
              </div>
            </div>

            {/* Skip option */}
            <div className="px-6 pb-5 text-center">
              <button
                onClick={handleSkip}
                className="text-xs text-stone-400 hover:text-stone-600 transition-colors"
              >
                {t("tutorial.skipGuide")}
              </button>
            </div>
          </Card>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
