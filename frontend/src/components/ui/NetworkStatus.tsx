import { useEffect, useState, useCallback } from "react";
import { Wifi, WifiOff, RefreshCw, AlertCircle } from "lucide-react";
import { setOnNetworkStatusChange, setOnRetry } from "@/api/client";

export function NetworkStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [isRetrying, setIsRetrying] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    // Register network status callback
    setOnNetworkStatusChange((online) => {
      setIsOnline(online);
      if (!online) {
        setShowBanner(true);
      }
    });

    // Register retry callback
    setOnRetry((attempt, max) => {
      setIsRetrying(true);
      setRetryCount(attempt);
      setShowBanner(true);
    });

    const handleOnline = () => {
      setIsOnline(true);
      setShowBanner(true);
      // Hide after 3 seconds when back online
      setTimeout(() => setShowBanner(false), 3000);
    };

    const handleOffline = () => {
      setIsOnline(false);
      setShowBanner(true);
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
      setOnNetworkStatusChange(null);
      setOnRetry(null);
    };
  }, []);

  const handleDismiss = useCallback(() => {
    setShowBanner(false);
    setIsRetrying(false);
  }, []);

  if (!showBanner) return null;

  // Retry indicator
  if (isRetrying && isOnline) {
    return (
      <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
        <div className="bg-amber-50 border border-amber-200 rounded-lg shadow-lg px-4 py-2 flex items-center gap-3">
          <RefreshCw className="w-4 h-4 text-amber-600 animate-spin" />
          <span className="text-sm text-amber-800">
            Retrying... (attempt {retryCount}/3)
          </span>
        </div>
      </div>
    );
  }

  // Offline banner
  if (!isOnline) {
    return (
      <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
        <div className="bg-rose-50 border border-rose-200 rounded-lg shadow-lg px-4 py-3 flex items-center gap-3">
          <WifiOff className="w-5 h-5 text-rose-600" />
          <div className="flex-1">
            <p className="text-sm font-medium text-rose-900">You are offline</p>
            <p className="text-xs text-rose-700">
              Please check your internet connection
            </p>
          </div>
          <button 
            onClick={handleDismiss}
            className="text-rose-600 hover:text-rose-800 text-xs"
          >
            Dismiss
          </button>
        </div>
      </div>
    );
  }

  // Back online success message
  return (
    <div className="fixed top-16 left-1/2 -translate-x-1/2 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
      <div className="bg-emerald-50 border border-emerald-200 rounded-lg shadow-lg px-4 py-2 flex items-center gap-2">
        <Wifi className="w-4 h-4 text-emerald-600" />
        <span className="text-sm text-emerald-800">
          Back online
        </span>
      </div>
    </div>
  );
}

// Hook for using network status
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return isOnline;
}
