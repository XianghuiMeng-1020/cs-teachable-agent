import { useNetworkStatus } from "@/hooks/useServiceWorker";
import { Wifi, WifiOff } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function OfflineIndicator() {
  const { isOnline } = useNetworkStatus();

  return (
    <AnimatePresence>
      {!isOnline && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          className="fixed top-0 left-0 right-0 z-50 bg-amber-500 text-white px-4 py-2 text-center text-sm font-medium shadow-lg"
        >
          <div className="flex items-center justify-center gap-2">
            <WifiOff className="w-4 h-4" />
            <span>You are offline. Some features may be limited.</span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

export function OnlineIndicator() {
  const { isOnline } = useNetworkStatus();

  return (
    <AnimatePresence>
      {isOnline && (
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.3 }}
          className="fixed top-0 left-0 right-0 z-50 bg-emerald-500 text-white px-4 py-2 text-center text-sm font-medium shadow-lg"
        >
          <div className="flex items-center justify-center gap-2">
            <Wifi className="w-4 h-4" />
            <span>Back online!</span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
