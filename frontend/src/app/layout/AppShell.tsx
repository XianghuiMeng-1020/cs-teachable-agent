import { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { listTA, createTA } from "@/api/client";
import { useAppStore } from "@/stores/appStore";
import { NetworkStatus } from "@/components/ui/NetworkStatus";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

const PAGE_NAMES: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/teach": "Teach TA",
  "/test": "Test TA",
  "/practice": "Practice",
  "/mastery": "Mastery",
  "/history": "History",
  "/learning-analytics": "Analytics",
  "/teacher": "Overview",
  "/teacher/students": "Students",
  "/teacher/transcripts": "Transcripts",
  "/teacher/analytics": "Analytics",
  "/teacher/assessments": "Assessments",
  "/teacher/metrics": "Learning Analytics",
  "/teacher/proctoring": "Proctoring Dashboard",
};

export function AppShell() {
  const location = useLocation();
  const path = location.pathname;
  const pageName =
    PAGE_NAMES[path] ??
    (path.startsWith("/teacher/students/")
      ? "Student Detail"
      : path.startsWith("/practice/")
        ? "Assessment"
        : "TeachAgent");
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
      toast.error(err?.message ?? "Failed to create TA. Please try again.");
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
      {mobileMenuOpen && (
        <button
          type="button"
          className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm lg:hidden"
          aria-label="Close menu"
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
