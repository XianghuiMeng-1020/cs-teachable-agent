import { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import { HelpCircle, X, ChevronRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface ContextualHelpProps {
  pageKey: "dashboard" | "teach" | "test" | "practice" | "mastery" | "history" | "analytics";
}

const SEEN_KEY_PREFIX = "arts_cs_help_seen_";

export function ContextualHelp({ pageKey }: ContextualHelpProps) {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [showBubble, setShowBubble] = useState(false);
  const bubbleTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    const seenKey = `${SEEN_KEY_PREFIX}${pageKey}`;
    const seen = sessionStorage.getItem(seenKey);
    if (!seen) {
      const timer = setTimeout(() => {
        setShowBubble(true);
        sessionStorage.setItem(seenKey, "true");
        bubbleTimer.current = setTimeout(() => setShowBubble(false), 4000);
      }, 1500);
      return () => {
        clearTimeout(timer);
        if (bubbleTimer.current) clearTimeout(bubbleTimer.current);
      };
    }
  }, [pageKey]);

  const title = t(`help.${pageKey}.title`);
  const content = t(`help.${pageKey}.content`);
  const steps = t(`help.${pageKey}.steps`, { returnObjects: true }) as string[];

  const handleToggle = () => {
    setIsOpen((prev) => !prev);
    setShowBubble(false);
    if (bubbleTimer.current) clearTimeout(bubbleTimer.current);
  };

  return (
    <>
      {/* Floating help button */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end gap-2">
        {/* Auto-show bubble hint */}
        <AnimatePresence>
          {showBubble && !isOpen && (
            <motion.div
              initial={{ opacity: 0, y: 10, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 10, scale: 0.9 }}
              className="rounded-xl bg-white px-4 py-3 shadow-xl border border-stone-200 max-w-[240px] text-sm text-stone-600"
            >
              <button
                onClick={() => setShowBubble(false)}
                className="absolute -top-1.5 -right-1.5 rounded-full bg-stone-100 p-0.5 text-stone-400 hover:text-stone-600"
              >
                <X className="w-3 h-3" />
              </button>
              <p>{content}</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Help button */}
        <button
          onClick={handleToggle}
          className={`flex items-center gap-2 rounded-full px-4 py-2.5 text-sm font-medium shadow-lg transition-all duration-200 hover:scale-105 ${
            isOpen
              ? "bg-stone-800 text-white"
              : "bg-white text-brand-700 border border-stone-200 hover:bg-brand-50"
          }`}
        >
          {isOpen ? (
            <X className="w-4 h-4" />
          ) : (
            <HelpCircle className="w-4 h-4" />
          )}
          <span>{t("help.btnTitle")}</span>
        </button>
      </div>

      {/* Help panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="fixed bottom-16 right-4 z-50 w-80 rounded-2xl bg-white shadow-2xl border border-stone-200 overflow-hidden"
          >
            {/* Panel header */}
            <div className="bg-gradient-to-r from-brand-500 to-brand-600 px-5 py-4 text-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <HelpCircle className="w-5 h-5" />
                  <h3 className="font-semibold">{title}</h3>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 hover:bg-white/20 rounded-full transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Panel content */}
            <div className="p-5">
              <p className="text-sm text-stone-600 leading-relaxed mb-4">{content}</p>

              {Array.isArray(steps) && steps.length > 0 && (
                <div className="space-y-2.5">
                  {steps.map((stepText, i) => (
                    <div key={i} className="flex items-start gap-2.5">
                      <div className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-brand-100 text-xs font-bold text-brand-700 mt-0.5">
                        {i + 1}
                      </div>
                      <p className="text-sm text-stone-600 leading-relaxed">{stepText}</p>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-4 pt-3 border-t border-stone-100">
                <button
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-1 text-xs font-medium text-brand-600 hover:text-brand-700 transition-colors"
                >
                  {t("common.close")}
                  <ChevronRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
