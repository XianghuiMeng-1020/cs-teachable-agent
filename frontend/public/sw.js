const CACHE_NAME = 'cs-ta-cache-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  // Add other static assets here
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('[SW] Installation complete');
        return self.skipWaiting();
      })
      .catch((err) => {
        console.error('[SW] Cache failed:', err);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => name !== CACHE_NAME)
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        console.log('[SW] Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip external requests
  if (url.origin !== self.location.origin) {
    return;
  }
  
  // API requests - network only with timeout
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .catch(() => {
          // Return offline fallback for API
          return new Response(
            JSON.stringify({ error: 'Offline', message: 'You are currently offline' }),
            { 
              status: 503, 
              headers: { 'Content-Type': 'application/json' }
            }
          );
        })
    );
    return;
  }
  
  // Static assets - cache first, network fallback
  event.respondWith(
    caches.match(request)
      .then((cached) => {
        if (cached) {
          // Return cached version immediately
          // But also fetch new version in background
          fetch(request)
            .then((response) => {
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, response.clone());
              });
            })
            .catch(() => {}); // Ignore background fetch errors
          
          return cached;
        }
        
        // Not in cache - fetch from network
        return fetch(request)
          .then((response) => {
            // Cache successful responses
            if (response.status === 200) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseClone);
              });
            }
            return response;
          })
          .catch((error) => {
            console.error('[SW] Fetch failed:', error);
            
            // Return offline page for navigation requests
            if (request.mode === 'navigate') {
              return caches.match('/index.html');
            }
            
            throw error;
          });
      })
  );
});

// Background sync for offline form submissions
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-forms') {
    console.log('[SW] Syncing forms...');
    event.waitUntil(syncFormSubmissions());
  }
});

async function syncFormSubmissions() {
  // Implementation for syncing stored form submissions
  // This would require IndexedDB integration
  console.log('[SW] Form sync not yet implemented');
}

// Push notifications (for future use)
self.addEventListener('push', (event) => {
  console.log('[SW] Push received:', event);
  
  const options = {
    body: event.data?.text() || 'New notification from CS TA',
    icon: '/icon-192x192.png',
    badge: '/icon-72x72.png',
    tag: 'cs-ta-notification',
    requireInteraction: true,
  };
  
  event.waitUntil(
    self.registration.showNotification('CS Teachable Agent', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event);
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('/')
  );
});
