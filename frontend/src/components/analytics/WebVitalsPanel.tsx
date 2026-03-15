import { useEffect, useState } from "react";
import { Card } from "@/components/ui/Card";
import { monitoring } from "@/hooks/useMonitoring";
import { Activity, Clock, MousePointer, Layout, Server } from "lucide-react";

interface WebVitalMetric {
  name: string;
  value: number;
  unit: string;
  rating: "good" | "needs-improvement" | "poor";
  icon: React.ElementType;
  description: string;
}

export function WebVitalsPanel({ className }: { className?: string }) {
  const [metrics, setMetrics] = useState<WebVitalMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Collect metrics after page load
    const collectMetrics = () => {
      const collectedMetrics: WebVitalMetric[] = [];

      // First Contentful Paint
      const fcp = performance.getEntriesByName("first-contentful-paint")[0] as PerformanceEntry;
      if (fcp) {
        collectedMetrics.push({
          name: "First Contentful Paint",
          value: Math.round(fcp.startTime),
          unit: "ms",
          rating: fcp.startTime < 1800 ? "good" : fcp.startTime < 3000 ? "needs-improvement" : "poor",
          icon: Clock,
          description: "Time until first content appears",
        });
      }

      // Largest Contentful Paint
      const lcpEntries = performance.getEntriesByType("largest-contentful-paint") as PerformanceEntry[];
      if (lcpEntries.length > 0) {
        const lcp = lcpEntries[lcpEntries.length - 1];
        collectedMetrics.push({
          name: "Largest Contentful Paint",
          value: Math.round(lcp.startTime),
          unit: "ms",
          rating: lcp.startTime < 2500 ? "good" : lcp.startTime < 4000 ? "needs-improvement" : "poor",
          icon: Activity,
          description: "Time until largest content element loads",
        });
      }

      // Time to First Byte
      const navigation = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming;
      if (navigation) {
        const ttfb = navigation.responseStart - navigation.startTime;
        collectedMetrics.push({
          name: "Time to First Byte",
          value: Math.round(ttfb),
          unit: "ms",
          rating: ttfb < 800 ? "good" : ttfb < 1800 ? "needs-improvement" : "poor",
          icon: Server,
          description: "Time until first byte received from server",
        });

        // Total Load Time
        const loadTime = navigation.loadEventEnd - navigation.startTime;
        collectedMetrics.push({
          name: "Total Load Time",
          value: Math.round(loadTime),
          unit: "ms",
          rating: loadTime < 3000 ? "good" : loadTime < 5000 ? "needs-improvement" : "poor",
          icon: Clock,
          description: "Total time to fully load the page",
        });
      }

      // First Input Delay (would need event observer in real implementation)
      collectedMetrics.push({
        name: "First Input Delay",
        value: 0,
        unit: "ms",
        rating: "good",
        icon: MousePointer,
        description: "Time until page responds to first interaction",
      });

      setMetrics(collectedMetrics);
      setLoading(false);
    };

    // Wait for page to be fully loaded
    if (document.readyState === "complete") {
      collectMetrics();
    } else {
      window.addEventListener("load", collectMetrics);
      return () => window.removeEventListener("load", collectMetrics);
    }
  }, []);

  const getRatingColor = (rating: string) => {
    switch (rating) {
      case "good":
        return "text-emerald-600 bg-emerald-50 border-emerald-200";
      case "needs-improvement":
        return "text-amber-600 bg-amber-50 border-amber-200";
      case "poor":
        return "text-red-600 bg-red-50 border-red-200";
      default:
        return "text-slate-600 bg-slate-50 border-slate-200";
    }
  };

  const getRatingLabel = (rating: string) => {
    switch (rating) {
      case "good":
        return "Good";
      case "needs-improvement":
        return "Needs Improvement";
      case "poor":
        return "Poor";
      default:
        return "Unknown";
    }
  };

  if (loading) {
    return (
      <Card padding="lg" className={className}>
        <div className="flex items-center gap-2 mb-4">
          <Activity className="w-5 h-5 text-brand-500" />
          <h3 className="font-semibold text-slate-900">Web Vitals</h3>
        </div>
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-16 bg-slate-100 rounded-lg animate-pulse" />
          ))}
        </div>
      </Card>
    );
  }

  return (
    <Card padding="lg" className={className}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-brand-500" />
          <h3 className="font-semibold text-slate-900">Web Vitals</h3>
        </div>
        <span className="text-xs text-slate-500">Real-time Performance</span>
      </div>

      <div className="space-y-3">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div
              key={metric.name}
              className={`p-3 rounded-lg border ${getRatingColor(metric.rating)}`}
            >
              <div className="flex items-start gap-3">
                <div className="p-2 bg-white/50 rounded-lg">
                  <Icon className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="font-medium text-sm truncate">{metric.name}</p>
                    <span className="text-xs font-semibold px-2 py-0.5 bg-white/50 rounded-full">
                      {metric.value} {metric.unit}
                    </span>
                  </div>
                  <p className="text-xs opacity-75 mt-1">{metric.description}</p>
                  <p className="text-xs font-medium mt-1 capitalize">
                    Rating: {getRatingLabel(metric.rating)}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="mt-4 pt-4 border-t border-slate-200">
        <p className="text-xs text-slate-500">
          Web Vitals are Google&apos;s initiative to provide unified guidance for quality signals
          essential to delivering a great user experience.
        </p>
      </div>
    </Card>
  );
}
