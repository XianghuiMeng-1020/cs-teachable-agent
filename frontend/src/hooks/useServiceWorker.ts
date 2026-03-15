import { useEffect, useState, useCallback } from 'react';
import { toast } from 'sonner';

interface ServiceWorkerState {
  isSupported: boolean;
  isRegistered: boolean;
  isOffline: boolean;
  updateAvailable: boolean;
}

export function useServiceWorker() {
  const [state, setState] = useState<ServiceWorkerState>({
    isSupported: 'serviceWorker' in navigator,
    isRegistered: false,
    isOffline: !navigator.onLine,
    updateAvailable: false,
  });

  // Register Service Worker
  useEffect(() => {
    if (!('serviceWorker' in navigator)) {
      console.log('[SW] Service Worker not supported');
      return;
    }

    const registerSW = async () => {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js', {
          scope: '/',
        });

        console.log('[SW] Registered:', registration);
        setState(prev => ({ ...prev, isRegistered: true }));

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('[SW] Update available');
                setState(prev => ({ ...prev, updateAvailable: true }));
                toast.info('Update available! Refresh to get the latest version.', {
                  action: {
                    label: 'Refresh',
                    onClick: () => window.location.reload(),
                  },
                  duration: 10000,
                });
              }
            });
          }
        });

        // Listen for messages from SW
        navigator.serviceWorker.addEventListener('message', (event) => {
          console.log('[SW] Message received:', event.data);
          
          if (event.data.type === 'OFFLINE') {
            setState(prev => ({ ...prev, isOffline: true }));
          } else if (event.data.type === 'ONLINE') {
            setState(prev => ({ ...prev, isOffline: false }));
          }
        });

      } catch (error) {
        console.error('[SW] Registration failed:', error);
      }
    };

    registerSW();

    // Listen for online/offline events
    const handleOnline = () => {
      setState(prev => ({ ...prev, isOffline: false }));
      toast.success('You are back online!');
    };

    const handleOffline = () => {
      setState(prev => ({ ...prev, isOffline: true }));
      toast.warning('You are offline. Some features may be limited.', {
        duration: 5000,
      });
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Function to manually check for updates
  const checkForUpdates = useCallback(async () => {
    if (!('serviceWorker' in navigator)) return;

    try {
      const registration = await navigator.serviceWorker.ready;
      await registration.update();
      toast.success('Checking for updates...');
    } catch (error) {
      console.error('[SW] Update check failed:', error);
      toast.error('Failed to check for updates');
    }
  }, []);

  // Function to skip waiting and activate new SW
  const skipWaiting = useCallback(async () => {
    if (!('serviceWorker' in navigator)) return;

    const registration = await navigator.serviceWorker.ready;
    
    if (registration.waiting) {
      registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    }
    
    window.location.reload();
  }, []);

  return {
    ...state,
    checkForUpdates,
    skipWaiting,
  };
}

// Hook for network status
export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [connectionType, setConnectionType] = useState<string>('unknown');

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Get connection info if available
    const connection = (navigator as any).connection;
    if (connection) {
      setConnectionType(connection.effectiveType || 'unknown');
      
      connection.addEventListener('change', () => {
        setConnectionType(connection.effectiveType || 'unknown');
      });
    }

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return { isOnline, connectionType };
}
