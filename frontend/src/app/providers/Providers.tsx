import * as React from "react";
import { useNavigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster, toast } from "sonner";
import { TooltipProvider } from "@/components/ui/Tooltip";
import * as api from "@/api/client";
import { useAuthStore } from "@/stores/authStore";
import { ROUTES } from "@/lib/constants";
import { getJwtExpiration } from "@/lib/utils";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 30_000, refetchOnWindowFocus: true },
  },
});

const JWT_EXPIRY_WARN_MS = 5 * 60 * 1000; // warn when less than 5 min left
const JWT_CHECK_INTERVAL_MS = 60 * 1000; // check every minute

function Auth401Handler({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const logout = useAuthStore((s) => s.logout);
  const token = useAuthStore((s) => s.token);
  React.useEffect(() => {
    api.setOnUnauthorized(() => {
      logout();
      navigate(ROUTES.login, { replace: true });
    });
    return () => api.setOnUnauthorized(null);
  }, [logout, navigate]);

  React.useEffect(() => {
    if (!token) return;
    const t = setInterval(() => {
      const exp = getJwtExpiration(token);
      if (!exp) return;
      const remainingMs = exp * 1000 - Date.now();
      if (remainingMs > 0 && remainingMs < JWT_EXPIRY_WARN_MS) {
        toast.warning("Session expiring soon. Save your work and log in again if needed.");
      }
    }, JWT_CHECK_INTERVAL_MS);
    return () => clearInterval(t);
  }, [token]);
  return <>{children}</>;
}

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider delayDuration={300}>
        <Auth401Handler>
          {children}
          <Toaster 
            position="top-center"
            richColors 
            closeButton 
            toastOptions={{
              className: "max-w-[90vw] sm:max-w-md",
            }}
          />
        </Auth401Handler>
      </TooltipProvider>
    </QueryClientProvider>
  );
}
