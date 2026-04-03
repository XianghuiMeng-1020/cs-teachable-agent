import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { useAppStore } from "@/stores/appStore";
import { SpacedRepetitionPanel } from "@/components/learning/SpacedRepetitionPanel";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { BookOpen, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import { ROUTES } from "@/lib/constants";

export function ReviewPage() {
  const { t } = useTranslation();
  const currentTaId = useAppStore((s) => s.currentTaId);

  if (!currentTaId) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="py-12"
      >
        <EmptyState
          icon={BookOpen}
          title={t("review.noTA", { defaultValue: "请先创建教学代理" })}
          description={t("review.noTADesc", { defaultValue: "您需要先创建一个教学代理才能开始间隔重复复习。" })}
          action={
            <Link to={ROUTES.dashboard}>
              <Button icon={Sparkles}>
                {t("review.createTA", { defaultValue: "创建教学代理" })}
              </Button>
            </Link>
          }
        />
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-stone-900 dark:text-stone-100">
            {t("review.title", { defaultValue: "间隔重复复习" })}
          </h1>
          <p className="text-stone-500 dark:text-stone-400 mt-1">
            {t("review.desc", { defaultValue: "根据遗忘曲线科学安排复习，巩固您的学习成果。" })}
          </p>
        </div>
      </div>

      <SpacedRepetitionPanel taId={currentTaId} />
    </motion.div>
  );
}
