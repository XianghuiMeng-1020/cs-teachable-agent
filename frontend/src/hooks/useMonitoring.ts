// Performance and Error Monitoring Hook
// Can be easily integrated with Sentry, LogRocket, or other monitoring services

import { useEffect, useCallback, useRef } from 'react';

interface PerformanceMetrics {
  fcp?: number; // First Contentful Paint
  lcp?: number; // Largest Contentful Paint
  fid?: number; // First Input Delay
  cls?: number; // Cumulative Layout Shift
  ttfb?: number; // Time to First Byte
}

interface MonitoringConfig {
  dsn?: string;
  environment?: string;
  release?: string;
  enabled?: boolean;
}

class MonitoringService {
  private static instance: MonitoringService;
  private config: MonitoringConfig = { enabled: false };
  private metrics: PerformanceMetrics = {};

  static getInstance(): MonitoringService {
    if (!MonitoringService.instance) {
      MonitoringService.instance = new MonitoringService();
    }
    return MonitoringService.instance;
  }

  init(config: MonitoringConfig) {
    this.config = { ...this.config, ...config };
    
    if (this.config.enabled) {
      this.setupErrorTracking();
      this.setupPerformanceTracking();
      this.setupWebVitals();
    }
  }

  private setupErrorTracking() {
    // Global error handler
    window.addEventListener('error', (event) => {
      this.captureException(event.error, {
        type: 'error',
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      });
    });

    // Unhandled promise rejection handler
    window.addEventListener('unhandledrejection', (event) => {
      this.captureException(event.reason, {
        type: 'unhandledrejection',
      });
    });
  }

  private setupPerformanceTracking() {
    // Navigation timing
    window.addEventListener('load', () => {
      setTimeout(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        
        if (navigation) {
          this.captureMetric('page_load_time', navigation.loadEventEnd - navigation.startTime);
          this.captureMetric('dom_interactive', navigation.domInteractive - navigation.startTime);
          this.captureMetric('dom_complete', navigation.domComplete - navigation.startTime);
        }
      }, 0);
    });
  }

  private setupWebVitals() {
    // First Contentful Paint
    const observerFCP = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'first-contentful-paint') {
          this.metrics.fcp = entry.startTime;
          this.captureMetric('fcp', entry.startTime);
        }
      }
    });
    
    try {
      observerFCP.observe({ entryTypes: ['paint'] });
    } catch (e) {
      console.warn('FCP observer not supported');
    }

    // Largest Contentful Paint
    const observerLCP = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const lastEntry = entries[entries.length - 1];
      this.metrics.lcp = lastEntry.startTime;
      this.captureMetric('lcp', lastEntry.startTime);
    });

    try {
      observerLCP.observe({ entryTypes: ['largest-contentful-paint'] });
    } catch (e) {
      console.warn('LCP observer not supported');
    }

    // First Input Delay
    const observerFID = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const fidEntry = entry as PerformanceEventTiming;
        this.metrics.fid = fidEntry.processingStart - fidEntry.startTime;
        this.captureMetric('fid', this.metrics.fid);
      }
    });

    try {
      observerFID.observe({ entryTypes: ['first-input'] });
    } catch (e) {
      console.warn('FID observer not supported');
    }

    // Cumulative Layout Shift
    let clsValue = 0;
    const observerCLS = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        const layoutShift = entry as any;
        if (!layoutShift.hadRecentInput) {
          clsValue += layoutShift.value;
        }
      }
      this.metrics.cls = clsValue;
      this.captureMetric('cls', clsValue);
    });

    try {
      observerCLS.observe({ entryTypes: ['layout-shift'] });
    } catch (e) {
      console.warn('CLS observer not supported');
    }
  }

  captureException(error: Error | unknown, context?: Record<string, any>) {
    if (!this.config.enabled) return;

    const errorInfo = {
      error: error instanceof Error ? {
        name: error.name,
        message: error.message,
        stack: error.stack,
      } : error,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    };

    // Send to monitoring service or console in development
    if (process.env.NODE_ENV === 'production') {
      // Here you would send to Sentry/LogRocket/etc
      console.error('[Monitoring] Exception:', errorInfo);
    } else {
      console.error('[Monitoring] Exception:', errorInfo);
    }
  }

  captureMessage(message: string, level: 'info' | 'warning' | 'error' = 'info', context?: Record<string, any>) {
    if (!this.config.enabled) return;

    const logInfo = {
      message,
      level,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href,
    };

    if (process.env.NODE_ENV === 'production') {
      console.log(`[Monitoring] ${level}:`, logInfo);
    } else {
      console.log(`[Monitoring] ${level}:`, logInfo);
    }
  }

  captureMetric(name: string, value: number, unit?: string) {
    if (!this.config.enabled) return;

    const metric = {
      name,
      value,
      unit,
      timestamp: new Date().toISOString(),
      url: window.location.href,
    };

    // Send to analytics service
    if (process.env.NODE_ENV === 'production') {
      console.log('[Monitoring] Metric:', metric);
    }
  }

  setUser(userId: string, email?: string, username?: string) {
    if (!this.config.enabled) return;

    const userInfo = { userId, email, username };
    console.log('[Monitoring] User set:', userInfo);
  }

  getMetrics(): PerformanceMetrics {
    return { ...this.metrics };
  }
}

// React Hook for monitoring
export function useMonitoring(config?: MonitoringConfig) {
  const monitoringRef = useRef(MonitoringService.getInstance());

  useEffect(() => {
    if (config) {
      monitoringRef.current.init(config);
    }
  }, [config]);

  const trackError = useCallback((error: Error, context?: Record<string, any>) => {
    monitoringRef.current.captureException(error, context);
  }, []);

  const trackEvent = useCallback((eventName: string, properties?: Record<string, any>) => {
    monitoringRef.current.captureMessage(eventName, 'info', properties);
  }, []);

  const trackMetric = useCallback((name: string, value: number) => {
    monitoringRef.current.captureMetric(name, value);
  }, []);

  const setUser = useCallback((userId: string, email?: string, username?: string) => {
    monitoringRef.current.setUser(userId, email, username);
  }, []);

  const getMetrics = useCallback(() => {
    return monitoringRef.current.getMetrics();
  }, []);

  return {
    trackError,
    trackEvent,
    trackMetric,
    setUser,
    getMetrics,
  };
}

// Component render time tracking
export function useRenderTime(componentName: string) {
  const startTime = useRef(performance.now());

  useEffect(() => {
    const endTime = performance.now();
    const renderTime = endTime - startTime.current;
    
    MonitoringService.getInstance().captureMetric(
      `render_time_${componentName}`,
      renderTime,
      'ms'
    );
  }, [componentName]);
}

// API call tracking
export function useApiTracking() {
  const trackApiCall = useCallback(async <T,>(
    apiName: string,
    apiCall: () => Promise<T>
  ): Promise<T> => {
    const startTime = performance.now();
    
    try {
      const result = await apiCall();
      const duration = performance.now() - startTime;
      
      MonitoringService.getInstance().captureMetric(
        `api_${apiName}_success`,
        duration,
        'ms'
      );
      
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      
      MonitoringService.getInstance().captureMetric(
        `api_${apiName}_error`,
        duration,
        'ms'
      );
      
      MonitoringService.getInstance().captureException(error, {
        apiName,
        duration,
      });
      
      throw error;
    }
  }, []);

  return { trackApiCall };
}

// Export singleton for direct use
export const monitoring = MonitoringService.getInstance();
