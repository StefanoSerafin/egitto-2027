// Service worker: rende la web app utilizzabile senza rete dopo la prima apertura.
// Generato da tools/costruisci.py (versione e elenco file): non modificare sw.js a mano.
const CACHE = 'egitto-2027-20261009-210159';
const FILE = ["./", "index.html", "manifest.json", "icona-180.png", "css/giorno.css", "css/app.css", "js/app.js", "js/mappa.js", "data/giorni.js", "data/extra.js", "img/g10-maggiore.jpg", "img/g10-minore.jpg", "img/g10-salvataggio.jpg", "img/g11-qarun.jpg", "img/g11-ritratto.jpg", "img/g12-hitan.jpg", "img/g12-magic.jpg", "img/g12-rayan.jpg", "img/g2-cittadella.jpg", "img/g2-khan.jpg", "img/g2-muhammad-ali.jpg", "img/g2-orologio.jpg", "img/g2-sulayman.jpg", "img/g3-chefren.jpg", "img/g3-cheope.jpg", "img/g3-gem.jpg", "img/g3-sfinge.jpg", "img/g4-memphis.jpg", "img/g4-romboidale.jpg", "img/g4-zoser.jpg", "img/g5-karnak.jpg", "img/g5-luxor.jpg", "img/g6-corona.jpg", "img/g6-diamante.jpg", "img/g7-hatshepsut.jpg", "img/g7-memnone.jpg", "img/g7-valle.jpg", "img/g8-edfu.jpg", "img/g8-komombo.jpg", "img/g9-diga.jpg", "img/g9-elefantina.jpg", "img/g9-obelisco.jpg", "img/g9-philae.jpg", "img/outfit-i-0406.jpg", "img/outfit-i-0708.jpg", "img/outfit-palette-ilenia.jpg", "img/outfit-palette-stefano.jpg", "img/outfit-s01.jpg", "img/outfit-s02.jpg", "img/outfit-s03.jpg", "img/outfit-s04.jpg", "img/outfit-s05.jpg", "img/outfit-s06.jpg", "img/outfit-s08.jpg", "img/outfit-s09.jpg", "img/outfit-s10.jpg", "img/outfit-s11.jpg", "img/outfit-s12.jpg", "img/panoramica.jpg"];
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
