const CACHE_NAME = 'musikids-v3'; // Mude para v4, v5 sempre que atualizar o site!
const urlsToCache = [
  '/MusiKids/',
  '/MusiKids/index.html',
  '/MusiKids/jogos/',
  '/MusiKids/livros/',
  '/MusiKids/musicas/'
];

// 1. Instalação e Forçar Ativação
self.addEventListener('install', event => {
  self.skipWaiting(); // Força o SW novo a assumir o controle na hora
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache atualizado para:', CACHE_NAME);
        return cache.addAll(urlsToCache);
      })
  );
});

// 2. Ativação e Limpeza de Lixo
self.addEventListener('activate', event => {
  event.waitUntil(
    clients.claim(), // Faz o SW controlar a página imediatamente
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

// 3. Estratégia Inteligente: Tentar Rede Primeiro para o HTML
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Se for a página principal ou o index, tenta buscar na rede primeiro
  // Isso garante que as melhorias no HTML apareçam na hora!
  if (url.origin === location.origin && (url.pathname === '/MusiKids/' || url.pathname.endsWith('.html'))) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clonedResponse = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clonedResponse));
          return response;
        })
        .catch(() => caches.match(event.request)) // Se a internet cair, usa o cache
    );
  } else {
    // Para imagens e outros arquivos, usa Cache First para ser rápido
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
  }
});
