import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { useAppStore } from "@/stores/appStore";
import { LearningReport } from "@/components/reports/LearningReport";
import { EmptyState } from "@/components/ui/EmptyState";
import { Button } from "@/components/ui/Button";
import { FileText, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";
import { ROUTES } from "@/lib/constants";

export function ReportPage() {
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
          icon={FileText}
          title={t("report.noTA", { defaultValue: "请先创建教学代理" })}
          description={t("report.noTADesc", { defaultValue: "您需要先创建一个教学代理才能查看学习报告。" })}
          action={
            <Link to={ROUTES.dashboard}>
              <Button icon={Sparkles}>
                {t("report.createTA", { defaultValue: "创建教学代理" })}
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
            {t("report.title", { defaultValue: "学习报告" })}
          </h1>
          <p className="text-stone-500 dark:text-stone-400 mt-1">
            {t("report.desc", { defaultValue: "查看您的学习进度、掌握情况和学习建议。" })}
          </p>
        </div>
      </div>

      <LearningReport taId={currentTaId} />
    </motion.div>
  );
}
