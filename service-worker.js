const CACHE_NAME = 'musikids-v1';
const urlsToCache = [
  '/MusiKids/',
  '/MusiKids/index.html',
  '/MusiKids/jogos/',
  '/MusiKids/livros/',
  '/MusiKids/musicas/'
];

// Instalar Service Worker e fazer cache dos arquivos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache aberto');
        return cache.addAll(urlsToCache);
      })
  );
});

// Ativar Service Worker e limpar caches antigos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Removendo cache antigo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interceptar requisições e servir do cache quando disponível
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Retorna do cache se disponível, senão faz requisição
        return response || fetch(event.request);
      })
  );
});
