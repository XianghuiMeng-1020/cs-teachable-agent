import { lazy, Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import { ProtectedRoute } from "./app/providers/ProtectedRoute";
import { AppShell } from "./app/layout/AppShell";
import { Skeleton } from "./components/ui/Skeleton";
import { ROUTES } from "./lib/constants";

const LandingPage = lazy(() => import("./pages/LandingPage").then((m) => ({ default: m.LandingPage })));
const LoginPage = lazy(() => import("./pages/LoginPage").then((m) => ({ default: m.LoginPage })));
const TeachPage = lazy(() => import("./pages/student/TeachPage").then((m) => ({ default: m.TeachPage })));
const DashboardPage = lazy(() => import("./pages/student/DashboardPage").then((m) => ({ default: m.DashboardPage })));
const TestPage = lazy(() => import("./pages/student/TestPage").then((m) => ({ default: m.TestPage })));
const HistoryPage = lazy(() => import("./pages/student/HistoryPage").then((m) => ({ default: m.HistoryPage })));
const MasteryPage = lazy(() => import("./pages/student/MasteryPage").then((m) => ({ default: m.MasteryPage })));
const LearningAnalyticsPage = lazy(() => import("./pages/student/LearningAnalyticsPage").then((m) => ({ default: m.LearningAnalyticsPage })));
const OverviewPage = lazy(() => import("./pages/teacher/OverviewPage").then((m) => ({ default: m.OverviewPage })));
const TranscriptsPage = lazy(() => import("./pages/teacher/TranscriptsPage").then((m) => ({ default: m.TranscriptsPage })));
const StudentsPage = lazy(() => import("./pages/teacher/StudentsPage").then((m) => ({ default: m.StudentsPage })));
const StudentDetailPage = lazy(() => import("./pages/teacher/StudentDetailPage").then((m) => ({ default: m.StudentDetailPage })));
const AnalyticsPage = lazy(() => import("./pages/teacher/AnalyticsPage").then((m) => ({ default: m.AnalyticsPage })));

function PageFallback() {
  return (
    <div className="space-y-4 p-4">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-32 w-full" />
      <Skeleton className="h-32 w-full" />
    </div>
  );
}

function StudentLayout() {
  return (
    <ProtectedRoute role="student">
      <AppShell />
    </ProtectedRoute>
  );
}

function TeacherLayout() {
  return (
    <ProtectedRoute role="teacher">
      <AppShell />
    </ProtectedRoute>
  );
}









function App() {
  return (
    <Suspense fallback={<PageFallback />}>
      <Routes>
        <Route path={ROUTES.home} element={<LandingPage />} />
        <Route path={ROUTES.login} element={<LoginPage />} />

        <Route element={<StudentLayout />}>
          <Route path={ROUTES.dashboard} element={<DashboardPage />} />
          <Route path={ROUTES.teach} element={<TeachPage />} />
          <Route path={ROUTES.test} element={<TestPage />} />
          <Route path={ROUTES.mastery} element={<MasteryPage />} />
          <Route path={ROUTES.history} element={<HistoryPage />} />
          <Route path="/learning-analytics" element={<LearningAnalyticsPage />} />
        </Route>

        <Route path="teacher" element={<TeacherLayout />}>
          <Route index element={<OverviewPage />} />
          <Route path="students" element={<StudentsPage />} />
          <Route path="students/:userId" element={<StudentDetailPage />} />
          <Route path="transcripts" element={<TranscriptsPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
        </Route>

        <Route path="*" element={<Navigate to={ROUTES.home} replace />} />
      </Routes>
    </Suspense>
  );
}

export default App;
