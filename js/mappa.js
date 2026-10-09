// js/mappa.js — mappa Leaflet di tutte le tappe, un colore per giorno.
// Stesso schema di copenaghen-2026/js/mappa.js: tile OpenStreetMap senza chiave, Leaflet da unpkg.

const EgittoMappa = (function () {
  let mappa = null;

  function spillo(colore, n) {
    return L.divIcon({
      className: '', iconSize: [26, 26], iconAnchor: [13, 13], popupAnchor: [0, -12],
      html: '<div class="spillo" style="background:' + colore + '">' + n + '</div>',
    });
  }

  function fumetto(g, t) {
    let h = '<div class="fumetto">';
    if (t.foto) h += '<img src="' + t.foto.src + '" alt="">';
    h += '<b>' + t.titolo + '</b><span>Giorno ' + g.n + ', ' + g.data.replace(' 2027', '') + (t.indicativa ? '. Posizione indicativa' : '') + '</span>';
    h += '<a href="#/giorno/' + g.n + '">Apri la giornata</a>';
    h += '<a href="https://www.google.com/maps/search/?api=1&query=' + t.coord[0] + ',' + t.coord[1] + '" target="_blank" rel="noopener">Google Maps</a></div>';
    return h;
  }

  function colore(g) {
    // il giorno dell'eclissi ha la tinta chiara su fondo scuro: sulla mappa usa l'accento
    return g.n === 6 ? g.pal.accento : g.pal.tinta;
  }

  function apri(contenitore, chips) {
    mappa = L.map(contenitore, { zoomControl: true, attributionControl: true });
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18, attribution: '&copy; OpenStreetMap',
    }).addTo(mappa);

    const perGiorno = {};
    const tutti = [];
    GIORNI.forEach(function (g) {
      g.righe.forEach(function (t) {
        if (!t.coord) return;
        L.marker(t.coord, { icon: spillo(colore(g), g.n) }).addTo(mappa).bindPopup(fumetto(g, t), { maxWidth: 230, minWidth: 190 });
        (perGiorno[g.n] = perGiorno[g.n] || []).push(t.coord);
        tutti.push(t.coord);
      });
    });
    L.polyline(tutti, { color: '#555', weight: 2, opacity: .55, dashArray: '4 6' }).addTo(mappa);

    function inquadra(punti) {
      if (punti.length === 1) mappa.setView(punti[0], 13);
      else mappa.fitBounds(punti, { padding: [36, 36], maxZoom: 15 });
    }

    function bottone(etichetta, punti, col) {
      const b = document.createElement('button');
      b.type = 'button';
      b.innerHTML = (col ? '<i style="background:' + col + '"></i>' : '') + etichetta;
      b.addEventListener('click', function () {
        Array.prototype.forEach.call(chips.children, function (x) { x.classList.remove('attiva'); });
        b.classList.add('attiva');
        inquadra(punti);
      });
      chips.appendChild(b);
      return b;
    }

    const primo = bottone('Tutto il viaggio', tutti, null);
    GIORNI.forEach(function (g) {
      if (perGiorno[g.n]) bottone('Giorno ' + g.n, perGiorno[g.n], colore(g));
    });
    primo.classList.add('attiva');
    inquadra(tutti);
  }

  function chiudi() {
    if (mappa) { mappa.remove(); mappa = null; }
  }

  return { apri: apri, chiudi: chiudi };
})();
