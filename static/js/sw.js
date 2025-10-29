// Service Worker básico para PWA del Hotel Inventario
const CACHE_VERSION = 'v1.0.0';
const STATIC_CACHE = `static-${CACHE_VERSION}`;

const APP_SHELL = [
  '/',
  '/dashboard/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/manifest.webmanifest',
  '/static/icons/icon-192.svg',
  '/static/icons/icon-512.svg',
  '/static/icons/maskable-512.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => cache.addAll(APP_SHELL)).then(self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k !== STATIC_CACHE).map((k) => caches.delete(k))
    )).then(self.clients.claim())
  );
});

// Estrategia: Network-first para HTML; Cache-first para estáticos
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  if (req.method !== 'GET') return; // Solo GET

  // Solo manejar peticiones del mismo origen
  if (url.origin !== self.location.origin) return;

  if (req.headers.get('accept') && req.headers.get('accept').includes('text/html')) {
    // Network first para páginas
    event.respondWith(
      fetch(req).then((res) => {
        const resClone = res.clone();
        caches.open(STATIC_CACHE).then((cache) => cache.put(req, resClone));
        return res;
      }).catch(() => caches.match(req).then((cached) => cached || caches.match('/')))
    );
    return;
  }

  // Cache first para estáticos
  event.respondWith(
    caches.match(req).then((cached) => {
      return (
        cached || fetch(req).then((res) => {
          const resClone = res.clone();
          caches.open(STATIC_CACHE).then((cache) => cache.put(req, resClone));
          return res;
        }).catch(() => cached)
      );
    })
  );
});
