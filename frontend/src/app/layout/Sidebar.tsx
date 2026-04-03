import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  MessageSquare,
  Play,
  BookOpen,
  BookOpenCheck,
  History,
  Brain,
  LayoutGrid,
  Users,
  FileText,
  BarChart3,
  ClipboardList,
  Activity,
  Shield,
  ChevronLeft,
  ChevronRight,
  Repeat,
  FileBarChart,
  Users2,
} from "lucide-react";
import { useTranslation } from "react-i18next";
import { useAppStore } from "@/stores/appStore";
import { useAuthStore } from "@/stores/authStore";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";

const studentNav = [
  { to: ROUTES.dashboard, labelKey: "nav.dashboard", icon: LayoutDashboard },
  { to: ROUTES.teach, labelKey: "nav.teach", icon: MessageSquare },
  { to: ROUTES.test, labelKey: "nav.test", icon: Play },
  { to: ROUTES.practice, labelKey: "nav.practice", icon: BookOpenCheck },
  { to: "/review", labelKey: "nav.review", icon: Repeat },
  { to: "/collaborate", labelKey: "nav.collaborate", icon: Users2 },
  { to: ROUTES.mastery, labelKey: "nav.mastery", icon: BookOpen },
  { to: "/learning-analytics", labelKey: "nav.analytics", icon: Brain },
  { to: "/report", labelKey: "nav.report", icon: FileBarChart },
  { to: ROUTES.history, labelKey: "nav.history", icon: History },
];

const teacherNav = [
  { to: ROUTES.teacher.overview, labelKey: "nav.overview", icon: LayoutGrid },
  { to: ROUTES.teacher.students, labelKey: "nav.students", icon: Users },
  { to: ROUTES.teacher.transcripts, labelKey: "nav.transcripts", icon: FileText },
  { to: ROUTES.teacher.analytics, labelKey: "nav.analytics", icon: BarChart3 },
  { to: ROUTES.teacher.assessments, labelKey: "nav.assessments", icon: ClipboardList },
  { to: ROUTES.teacher.metrics, labelKey: "nav.metrics", icon: Activity },
  { to: ROUTES.teacher.proctoring, labelKey: "nav.proctoring", icon: Shield },
];

export function Sidebar() {
  const { t } = useTranslation();
  const { sidebarCollapsed, toggleSidebar, mobileMenuOpen, setMobileMenuOpen } = useAppStore();
  const user = useAuthStore((s) => s.user);
  const isTeacher = user?.role === "teacher";
  const nav = isTeacher ? teacherNav : studentNav;

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 flex h-full flex-col border-r border-stone-200/80 dark:border-stone-700/80 bg-white dark:bg-surfaceDark-card transition-all duration-300",
        "lg:relative lg:z-auto",
        sidebarCollapsed ? "w-[68px]" : "w-[260px]",
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}
      aria-label="Main navigation"
    >
      {/* Logo */}
      <div className="flex h-14 shrink-0 items-center gap-2.5 border-b border-stone-200/80 dark:border-stone-700/80 px-4">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-brand-700">
          <BookOpen className="h-4 w-4 text-white" />
        </div>
        {!sidebarCollapsed && (
          <div className="flex flex-col">
            <span className="text-[15px] font-semibold text-stone-900 dark:text-stone-100">{t("common.artsCs")}</span>
            <span className="text-[10px] text-stone-400 dark:text-stone-500">{t("common.artsCsFull")}</span>
          </div>
        )}
      </div>

      {/* Section label */}
      {!sidebarCollapsed && (
        <div className="px-4 pt-5 pb-2">
          <p className="text-[11px] font-semibold uppercase tracking-widest text-stone-400 dark:text-stone-500">
            {isTeacher ? t("nav.instructor") : t("nav.learning")}
          </p>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 space-y-0.5 overflow-y-auto px-2 py-1">
        {nav.map(({ to, labelKey, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            onClick={() => setMobileMenuOpen(false)}
            className={({ isActive }) =>
              cn(
                "flex h-10 items-center gap-3 rounded-lg px-3 text-sm font-medium text-stone-500 transition-all duration-150",
                "hover:bg-stone-100 hover:text-stone-900",
                isActive && "bg-brand-50 text-brand-800 hover:bg-brand-100",
                sidebarCollapsed && "justify-center px-0"
              )
            }
          >
            <Icon className="h-[18px] w-[18px] shrink-0" aria-hidden />
            {!sidebarCollapsed && <span>{t(labelKey)}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <div className="border-t border-stone-200/80 dark:border-stone-700/80 p-2">
        <button
          type="button"
          onClick={toggleSidebar}
          className={cn(
            "flex h-9 w-full items-center gap-2 rounded-lg px-3 text-sm text-stone-400 dark:text-stone-500 transition-colors hover:bg-stone-100 dark:hover:bg-stone-800 hover:text-stone-600 dark:hover:text-stone-400",
            sidebarCollapsed && "justify-center px-0"
          )}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <>
              <ChevronLeft className="h-4 w-4" />
              <span>{t("common.collapse")}</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
