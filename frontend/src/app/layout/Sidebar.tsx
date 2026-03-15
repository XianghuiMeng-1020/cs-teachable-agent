import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  MessageSquare,
  Play,
  BookOpen,
  History,
  Brain,
  LayoutGrid,
  Users,
  FileText,
  BarChart3,
  ChevronLeft,
  ChevronRight,
  Bot,
} from "lucide-react";
import { useAppStore } from "@/stores/appStore";
import { useAuthStore } from "@/stores/authStore";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";
import { ROUTES } from "@/lib/constants";

const studentNav = [
  { to: ROUTES.dashboard, label: "Dashboard", icon: LayoutDashboard },
  { to: ROUTES.teach, label: "Teach TA", icon: MessageSquare },
  { to: ROUTES.test, label: "Test TA", icon: Play },
  { to: ROUTES.mastery, label: "Mastery", icon: BookOpen },
  { to: "/learning-analytics", label: "Analytics", icon: Brain },
  { to: ROUTES.history, label: "History", icon: History },
];

const teacherNav = [
  { to: ROUTES.teacher.overview, label: "Overview", icon: LayoutGrid },
  { to: ROUTES.teacher.students, label: "Students", icon: Users },
  { to: ROUTES.teacher.transcripts, label: "Transcripts", icon: FileText },
  { to: ROUTES.teacher.analytics, label: "Analytics", icon: BarChart3 },
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, mobileMenuOpen, setMobileMenuOpen } = useAppStore();
  const user = useAuthStore((s) => s.user);
  const isTeacher = user?.role === "teacher";
  const nav = isTeacher ? teacherNav : studentNav;

  return (
    <aside
      className={cn(
        "fixed inset-y-0 left-0 z-40 flex h-full flex-col bg-brand-950 text-white shadow-sidebar transition-all duration-300",
        "lg:relative lg:z-auto",
        sidebarCollapsed ? "w-[68px]" : "w-[260px]",
        mobileMenuOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}
      style={{ width: sidebarCollapsed ? "var(--sidebar-collapsed)" : "var(--sidebar-width)" }}
      aria-label="Main navigation"
    >
      <div className="flex h-14 shrink-0 items-center gap-2 px-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/10">
          <Bot className="h-5 w-5 text-white" />
        </div>
        {!sidebarCollapsed && (
          <>
            <span className="font-semibold text-white">CS TA</span>
            <span className="rounded bg-white/20 px-1.5 py-0.5 text-[10px] font-medium text-white/80">
              v1
            </span>
          </>
        )}
      </div>
      <nav className="flex-1 space-y-0.5 px-2 py-3">
        {nav.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            onClick={() => setMobileMenuOpen(false)}
            className={({ isActive }) =>
              cn(
                "flex h-10 items-center gap-3 rounded-lg px-3 text-brand-300 transition-colors hover:bg-white/10 hover:text-white",
                isActive && "border-l-[3px] border-accent-500 bg-white/10 font-medium text-white"
              )
            }
          >
            <Icon className="h-5 w-5 shrink-0" aria-hidden />
            {!sidebarCollapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-white/10 p-2">
        <Button
          variant="ghost"
          size="sm"
          className="h-10 w-full justify-center text-brand-300 hover:bg-white/10 hover:text-white"
          icon={sidebarCollapsed ? ChevronRight : ChevronLeft}
          onClick={toggleSidebar}
        >
          {!sidebarCollapsed && "Collapse"}
        </Button>
      </div>
    </aside>
  );
}
