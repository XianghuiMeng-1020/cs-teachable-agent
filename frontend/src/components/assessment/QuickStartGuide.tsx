import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { X, MousePointer2, Puzzle, Send, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/Button";

const STORAGE_KEY = "assessment-quick-start-dismissed";

interface QuickStartGuideProps {
  onDismiss?: () => void;
}

export function QuickStartGuide({ onDismiss }: QuickStartGuideProps) {
  const { t } = useTranslation();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    try {
      setVisible(localStorage.getItem(STORAGE_KEY) !== "1");
    } catch {
      setVisible(true);
    }
  }, []);

  if (!visible) return null;

  const dismiss = () => {
    setVisible(false);
    try {
      localStorage.setItem(STORAGE_KEY, "1");
    } catch {}
    onDismiss?.();
  };

  return (
    <div className="relative overflow-hidden rounded-xl border border-brand-200 bg-gradient-to-br from-brand-50 to-white p-5 shadow-card">
      <button
        onClick={dismiss}
        className="absolute top-3 right-3 rounded-md p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-600 transition-colors"
      >
        <X className="h-4 w-4" />
      </button>

      <h3 className="font-serif text-lg font-semibold text-stone-900 mb-1">{t("practice.quickStart")}</h3>
      <p className="text-sm text-stone-500 mb-4">{t("practice.quickStartDesc")}</p>

      <div className="grid gap-3 sm:grid-cols-3">
        <StepCard
          step="01"
          stepLabel={t("practice.step")}
          title={t("practice.stepPick")}
          caption={t("practice.stepPickDesc")}
          icon={MousePointer2}
          color="brand"
          delay="0s"
        />
        <StepCard
          step="02"
          stepLabel={t("practice.step")}
          title={t("practice.stepSolve")}
          caption={t("practice.stepSolveDesc")}
          icon={Puzzle}
          color="amber"
          delay="0.1s"
        />
        <StepCard
          step="03"
          stepLabel={t("practice.step")}
          title={t("practice.stepCheck")}
          caption={t("practice.stepCheckDesc")}
          icon={Send}
          color="emerald"
          delay="0.2s"
        />
      </div>

      <div className="mt-4 flex items-center gap-3">
        <Button size="sm" onClick={dismiss}>{t("practice.gotIt")}</Button>
        <span className="text-xs text-stone-400">{t("practice.reopenHint")}</span>
      </div>
    </div>
  );
}

function StepCard({
  step,
  stepLabel,
  title,
  caption,
  icon: Icon,
  color,
  delay,
}: {
  step: string;
  stepLabel: string;
  title: string;
  caption: string;
  icon: React.ElementType;
  color: "brand" | "amber" | "emerald";
  delay: string;
}) {
  const bgMap = { brand: "bg-brand-100", amber: "bg-amber-100", emerald: "bg-emerald-100" };
  const textMap = { brand: "text-brand-700", amber: "text-amber-700", emerald: "text-emerald-700" };

  return (
    <div
      className="rounded-lg border border-stone-200/80 bg-white p-3.5 animate-fade-in-up"
      style={{ animationDelay: delay }}
    >
      <div className="flex items-center gap-2 mb-2">
        <div className={`flex h-7 w-7 items-center justify-center rounded-md ${bgMap[color]}`}>
          <Icon className={`h-3.5 w-3.5 ${textMap[color]}`} />
        </div>
        <span className="text-[10px] font-bold uppercase tracking-wider text-stone-400">{stepLabel} {step}</span>
      </div>
      <h4 className="text-sm font-semibold text-stone-800">{title}</h4>
      <p className="mt-1 text-xs leading-relaxed text-stone-500">{caption}</p>
    </div>
  );
}

export function QuickStartButton({ onClick }: { onClick: () => void }) {
  const { t } = useTranslation();
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 rounded-md border border-stone-200 px-2.5 py-1 text-xs font-medium text-stone-500 hover:bg-stone-50 transition-colors"
    >
      <CheckCircle className="h-3 w-3" />
      {t("practice.quickStart")}
    </button>
  );
}
