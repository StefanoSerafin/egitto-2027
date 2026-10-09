// Service worker: rende la web app utilizzabile senza rete dopo la prima apertura.
// Generato da tools/costruisci.py (versione e elenco file): non modificare sw.js a mano.
const CACHE = 'egitto-2027-__VERSIONE__';
const FILE = __FILE__;
const LEAFLET = ['https://unpkg.com/leaflet@1.9.4/dist/leaflet.css', 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    // Leaflet è facoltativo: se non si scarica, l'app funziona lo stesso senza mappa
    c.addAll(LEAFLET).catch(function () {});
    return c.addAll(FILE);
  }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (nomi) {
    return Promise.all(nomi.filter(function (n) { return n !== CACHE; }).map(function (n) { return caches.delete(n); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  const nostra = url.origin === self.location.origin || url.hostname === 'unpkg.com';
  if (!nostra) return; // le tessere della mappa passano sempre dalla rete
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(function (r) {
    return r || fetch(e.request);
  }));
});
