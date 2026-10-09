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

// Immagini e Leaflet: prima la copia salvata (non cambiano). Pagina, stile, codice e dati: prima la rete,
// così chi è connesso vede sempre l'ultima versione; se la rete manca o tarda oltre 3,5 secondi si usa la copia salvata.
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  const nostra = url.origin === self.location.origin || url.hostname === 'unpkg.com';
  if (!nostra) return; // le tessere della mappa passano sempre dalla rete
  const salvata = function () { return caches.match(e.request, { ignoreSearch: true }); };
  const fissa = url.hostname === 'unpkg.com' || /\.(jpg|jpeg|png)$/i.test(url.pathname);
  if (fissa) {
    e.respondWith(salvata().then(function (r) { return r || fetch(e.request); }));
    return;
  }
  e.respondWith(new Promise(function (risolvi) {
    let fatto = false;
    const attesa = setTimeout(function () {
      salvata().then(function (r) { if (r && !fatto) { fatto = true; risolvi(r); } });
    }, 3500);
    fetch(e.request).then(function (r) {
      clearTimeout(attesa);
      if (r.ok) { const copia = r.clone(); caches.open(CACHE).then(function (c) { c.put(e.request, copia); }); }
      if (!fatto) { fatto = true; risolvi(r); }
    }).catch(function () {
      clearTimeout(attesa);
      salvata().then(function (r) { if (!fatto) { fatto = true; risolvi(r || Response.error()); } });
    });
  }));
});
