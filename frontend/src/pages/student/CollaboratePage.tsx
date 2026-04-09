import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { useAppStore } from "@/stores/appStore";
import { CollaborationPanel } from "@/components/collaboration/CollaborationPanel";
import { getTA } from "@/api/client";

export function CollaboratePage() {
  const { t } = useTranslation();
  const currentTaId = useAppStore((s) => s.currentTaId);
  const { data: taData } = useQuery({
    queryKey: ["ta", currentTaId, "detail"],
    queryFn: () => getTA(currentTaId!),
    enabled: currentTaId != null,
  });
  const domainId = taData?.domain_id || "python";

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6 h-[calc(100vh-var(--topbar-height)-48px)]"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-stone-900 dark:text-stone-100">
            {t("collaborate.title", { defaultValue: "协作学习" })}
          </h1>
          <p className="text-stone-500 dark:text-stone-400 mt-1">
            {t("collaborate.desc", { defaultValue: "与其他同学一起教学，分享经验，共同进步。" })}
          </p>
        </div>
      </div>

      <div className="h-[calc(100%-80px)]">
        <CollaborationPanel domainId={domainId} />
      </div>
    </motion.div>
  );
}
