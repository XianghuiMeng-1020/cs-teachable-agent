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
} from "lucide-react";
import { useAppStore } from "@/stores/appStore";
import { useAuthStore } from "@/stores/authStore";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";

const studentNav = [
  { to: ROUTES.dashboard, label: "Dashboard", icon: LayoutDashboard },
  { to: ROUTES.teach, label: "Teach TA", icon: MessageSquare },
  { to: ROUTES.test, label: "Test TA", icon: Play },
  { to: ROUTES.practice, label: "Practice", icon: BookOpenCheck },
  { to: ROUTES.mastery, label: "Mastery", icon: BookOpen },
  { to: "/learning-analytics", label: "Analytics", icon: Brain },
  { to: ROUTES.history, label: "History", icon: History },
];

const teacherNav = [
  { to: ROUTES.teacher.overview, label: "Overview", icon: LayoutGrid },
  { to: ROUTES.teacher.students, label: "Students", icon: Users },
  { to: ROUTES.teacher.transcripts, label: "Transcripts", icon: FileText },
  { to: ROUTES.teacher.analytics, label: "Analytics", icon: BarChart3 },
  { to: ROUTES.teacher.assessments, label: "Assessments", icon: ClipboardList },
  { to: ROUTES.teacher.metrics, label: "Metrics", icon: Activity },
  { to: ROUTES.teacher.proctoring, label: "Proctoring", icon: Shield },
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, mobileMenuOpen, setMobileMenuOpen } = useAppStore();
  const user = useAuthStore((s) => s.user);
  const isTeacher = user?.role === "teacher";
  const nav = isTeacher ? teacherNav : studentNav;

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 flex h-full flex-col border-r border-stone-200/80 bg-white transition-all duration-300",
        "lg:relative lg:z-auto",
        sidebarCollapsed ? "w-[68px]" : "w-[260px]",
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}
      aria-label="Main navigation"
    >
      {/* Logo */}
      <div className="flex h-14 shrink-0 items-center gap-2.5 border-b border-stone-200/80 px-4">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-brand-700">
          <BookOpen className="h-4 w-4 text-white" />
        </div>
        {!sidebarCollapsed && (
          <div className="flex flex-col">
            <span className="text-[15px] font-semibold text-stone-900">ARTS-CS</span>
            <span className="text-[10px] text-stone-400">AI Resistant Teaching</span>
          </div>
        )}
      </div>

      {/* Section label */}
      {!sidebarCollapsed && (
        <div className="px-4 pt-5 pb-2">
          <p className="text-[11px] font-semibold uppercase tracking-widest text-stone-400">
            {isTeacher ? "Instructor" : "Learning"}
          </p>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 space-y-0.5 overflow-y-auto px-2 py-1">
        {nav.map(({ to, label, icon: Icon }) => (
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
            {!sidebarCollapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <div className="border-t border-stone-200/80 p-2">
        <button
          type="button"
          onClick={toggleSidebar}
          className={cn(
            "flex h-9 w-full items-center gap-2 rounded-lg px-3 text-sm text-stone-400 transition-colors hover:bg-stone-100 hover:text-stone-600",
            sidebarCollapsed && "justify-center px-0"
          )}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <>
              <ChevronLeft className="h-4 w-4" />
              <span>Collapse</span>
            </>
          )}
        </button>
      </div>
    </aside>
  );
}
