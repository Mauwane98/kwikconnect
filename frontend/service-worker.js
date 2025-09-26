// frontend/service-worker.js

const CACHE_NAME = 'kwik-connect-v1';
const STATIC_CACHE = 'static-v1';
const DYNAMIC_CACHE = 'dynamic-v1';
const API_CACHE = 'api-v1';

// Assets that must be available offline
const CRITICAL_ASSETS = [
  '/',
  '/index.html',
  '/offline.html',
  '/styles/tailwind.css',
  '/assets/icons/logo.png',
  '/assets/icons/offline.png',
  '/scripts/main.js',
  '/scripts/offline.js'
];

// Assets that should be cached but aren't critical
const ASSETS_TO_CACHE = [
  '/styles/main.css',
  '/assets/images/background.jpg',
  ...CRITICAL_ASSETS
];

// API routes to cache
const API_ROUTES = [
  '/api/vendors/nearby',
  '/api/products/popular',
  '/api/categories'
];

// IndexedDB setup for offline data
const dbName = 'KwikConnectDB';
const dbVersion = 1;

// Open IndexedDB
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(dbName, dbVersion);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // Create object stores for offline data
      if (!db.objectStoreNames.contains('orders')) {
        db.createObjectStore('orders', { keyPath: 'id', autoIncrement: true });
      }
      if (!db.objectStoreNames.contains('vendors')) {
        db.createObjectStore('vendors', { keyPath: 'id' });
      }
      if (!db.objectStoreNames.contains('products')) {
        db.createObjectStore('products', { keyPath: 'id' });
      }
    };
  });
}

// Install event: cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    Promise.all([
      // Cache static assets
      caches.open(STATIC_CACHE).then(cache => {
        console.log('Service Worker: Caching critical assets');
        return cache.addAll(CRITICAL_ASSETS);
      }),
      
      // Cache non-critical assets
      caches.open(DYNAMIC_CACHE).then(cache => {
        console.log('Service Worker: Caching non-critical assets');
        return cache.addAll(ASSETS_TO_CACHE);
      }),

      // Initialize IndexedDB
      openDB().then(() => {
        console.log('Service Worker: IndexedDB initialized');
      })
    ])
  );
  self.skipWaiting();
});

// Activate event: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('Service Worker: Clearing old cache');
            return caches.delete(cache);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Fetch event: handle different types of requests
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(event));
    return;
  }

  // Static assets
  if (request.method === 'GET') {
    event.respondWith(handleStaticRequest(event));
    return;
  }

  // POST requests (e.g., new orders)
  if (request.method === 'POST') {
    event.respondWith(handlePostRequest(event));
    return;
  }
});

// Handle API requests with network-first strategy
async function handleApiRequest(event) {
  const request = event.request;
  
  try {
    // Try network first
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.ok) {
      const cache = await caches.open(API_CACHE);
      cache.put(request, response.clone());
      
      // Also store in IndexedDB for offline access
      if (request.url.includes('/api/vendors') || request.url.includes('/api/products')) {
        const data = await response.clone().json();
        const db = await openDB();
        const tx = db.transaction([getStoreNameFromUrl(request.url)], 'readwrite');
        const store = tx.objectStore(getStoreNameFromUrl(request.url));
        await Promise.all(data.map(item => store.put(item)));
      }
    }
    
    return response;
  } catch (error) {
    console.log('Network request failed, trying cache', error);
    
    // Try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // If not in cache, try IndexedDB
    if (request.url.includes('/api/vendors') || request.url.includes('/api/products')) {
      const db = await openDB();
      const tx = db.transaction([getStoreNameFromUrl(request.url)], 'readonly');
      const store = tx.objectStore(getStoreNameFromUrl(request.url));
      const data = await store.getAll();
      
      if (data.length > 0) {
        return new Response(JSON.stringify(data), {
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    // Return offline data
    return new Response(
      JSON.stringify({ error: 'You are offline', offline: true }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  }
}

// Handle static asset requests with cache-first strategy
async function handleStaticRequest(event) {
  const cache = await caches.open(STATIC_CACHE);
  const cachedResponse = await cache.match(event.request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(event.request);
    cache.put(event.request, response.clone());
    return response;
  } catch (error) {
    // If offline and request is for a page, return offline page
    if (event.request.headers.get('accept').includes('text/html')) {
      return caches.match('/offline.html');
    }
    
    throw error;
  }
}

// Handle POST requests with background sync
async function handlePostRequest(event) {
  const request = event.request;
  
  try {
    // Try to send immediately
    return await fetch(request);
  } catch (error) {
    // If offline, store in IndexedDB for later
    const db = await openDB();
    const tx = db.transaction('orders', 'readwrite');
    const store = tx.objectStore('orders');
    
    const serializedRequest = {
      url: request.url,
      method: request.method,
      headers: Array.from(request.headers.entries()),
      body: await request.clone().text(),
      timestamp: new Date().getTime()
    };
    
    await store.add(serializedRequest);
    
    // Register for background sync
    if ('sync' in self.registration) {
      await self.registration.sync.register('sync-orders');
    }
    
    return new Response(JSON.stringify({
      offline: true,
      message: 'Order saved for later submission'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Helper function to get store name from URL
function getStoreNameFromUrl(url) {
  if (url.includes('/vendors')) return 'vendors';
  if (url.includes('/products')) return 'products';
  return 'general';
}
});