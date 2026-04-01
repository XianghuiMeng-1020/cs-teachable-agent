import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Outlet, useLocation } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { listTA, createTA } from "@/api/client";
import { useAppStore } from "@/stores/appStore";
import { NetworkStatus } from "@/components/ui/NetworkStatus";
import { UserGuide } from "@/components/onboarding/UserGuide";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function AppShell() {
  const { t } = useTranslation();
  const location = useLocation();
  const path = location.pathname;

  const PAGE_NAMES: Record<string, string> = {
    "/dashboard": t("nav.dashboard"),
    "/teach": `${t("nav.teach")} ${t("common.teachableAgent")}`,
    "/test": `${t("nav.test")} ${t("common.teachableAgent")}`,
    "/practice": t("nav.practice"),
    "/mastery": t("nav.mastery"),
    "/history": t("nav.history"),
    "/learning-analytics": t("nav.analytics"),
    "/teacher": t("nav.overview"),
    "/teacher/students": t("nav.students"),
    "/teacher/transcripts": t("nav.transcripts"),
    "/teacher/analytics": t("nav.analytics"),
    "/teacher/assessments": t("nav.assessments"),
    "/teacher/metrics": t("nav.metrics"),
    "/teacher/proctoring": t("nav.proctoring"),
  };

  const pageName =
    PAGE_NAMES[path] ??
    (path.startsWith("/teacher/students/")
      ? t("nav.studentDetail", { defaultValue: "Student Detail" })
      : path.startsWith("/practice/")
        ? t("nav.assessment", { defaultValue: "Assessment" })
        : t("common.teachableAgent"));
  const queryClient = useQueryClient();

  const { data: taList = [], isSuccess: taListLoaded } = useQuery({
    queryKey: ["ta", "list"],
    queryFn: listTA,
  });

  const createTAMutation = useMutation({
    mutationFn: () => createTA("python"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ta", "list"] });
    },
    onError: (err: Error) => {
      toast.error(err?.message ?? t("topbar.failedCreateTA"));
    },
  });

  const { currentTaId, setCurrentTaId, mobileMenuOpen, setMobileMenuOpen } = useAppStore();
  useEffect(() => {
    if (taList.length > 0 && (currentTaId == null || !taList.some((t) => t.id === currentTaId))) {
      setCurrentTaId(taList[0].id);
    }
  }, [taList, currentTaId, setCurrentTaId]);

  useEffect(() => {
    if (taListLoaded && taList.length === 0 && !createTAMutation.isPending) {
      createTAMutation.mutate();
    }
  }, [taListLoaded, taList.length, createTAMutation.isPending]);

  return (
    <div className="flex h-screen overflow-hidden bg-surface">
      <NetworkStatus />
      <UserGuide />
      {mobileMenuOpen && (
        <button
          type="button"
          className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm lg:hidden"
          aria-label={t("common.close")}
          onClick={() => setMobileMenuOpen(false)}
        />
      )}
      <Sidebar />
      <div className="flex flex-1 flex-col min-w-0">
        <TopBar pageName={pageName} taList={taList} onMenuClick={() => setMobileMenuOpen(true)} />
        <main className="mx-auto flex-1 overflow-auto px-4 py-6 sm:px-6 lg:px-8 max-w-[var(--content-max-width)] w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
