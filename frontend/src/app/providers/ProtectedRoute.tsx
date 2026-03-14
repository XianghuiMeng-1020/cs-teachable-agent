import * as React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import { ROUTES } from "@/lib/constants";

type Role = "student" | "teacher";

interface ProtectedRouteProps {
  children: React.ReactNode;
  role?: Role;
}

export function ProtectedRoute({ children, role }: ProtectedRouteProps) {
  const { token, user } = useAuthStore();
  const location = useLocation();

  if (!token && !user) {
    return <Navigate to={ROUTES.login} state={{ from: location }} replace />;
  }

  if (role && user?.role !== role) {
    return <Navigate to={user?.role === "teacher" ? ROUTES.teacher.overview : ROUTES.dashboard} replace />;
  }

  return <>{children}</>;
}
