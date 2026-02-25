const CACHE_NAME = 'musikids-v7.3';
const urlsToCache = [
  '/MusiKids/',
  '/MusiKids/index.html',
  '/MusiKids/js/musicas_data.js',
  '/MusiKids/musicas/'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(cacheNames.map(c => { if(c !== CACHE_NAME) return caches.delete(c); }));
    })
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (url.hostname.includes('youtube.com')) return;
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
