// js/app.js — navigazione a schede e viste. I contenuti arrivano da data/giorni.js e data/extra.js.

document.addEventListener('DOMContentLoaded', function () {
  const vista = document.getElementById('vista');
  const schede = document.getElementById('schede');
  const VARS = { carta: '--carta', inchiostro: '--inchiostro', tinta: '--tinta', chiaro: '--tinta-chiaro', accento: '--accento', tenue: '--tenue', dt: '--dt' };
  const PARTENZA = new Date(2027, 6, 28);
  const CHIAVE_VALIGIA = 'egitto_valigia';

  function tavolozza(p) {
    Object.keys(VARS).forEach(function (k) { document.documentElement.style.setProperty(VARS[k], p[k]); });
    const m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', p.carta);
  }

  function giornoDiOggi() {
    const oggi = new Date(); oggi.setHours(0, 0, 0, 0);
    return Math.round((oggi - PARTENZA) / 86400000) + 1; // 1 = giorno di partenza
  }

  // ------------------------------------------------------------ viste
  function vistaGiorni() {
    const n = giornoDiOggi();
    let conto = '';
    if (n < 1) conto = '<p class="conto"><b>' + (1 - n) + '</b>' + (1 - n === 1 ? 'giorno' : 'giorni') + ' alla partenza</p>';
    else if (n <= 13) conto = '<p class="conto"><b>Giorno ' + n + '</b><a href="#/giorno/' + n + '">Apri la giornata di oggi</a></p>';
    let h = '<header><p class="giorno">28 luglio – 10 agosto 2027</p><h1>Egitto 2027</h1>'
      + '<p class="filo">Tredici giorni con Luca Perri: dal Cairo ad Abu Simbel, l\'eclissi totale a Luxor e le balene fossili del deserto.</p>'
      + conto + '</header>'
      + '<figure class="foto panoramica"><a href="#/locandina"><img src="img/panoramica.jpg" alt="Locandina del viaggio: mappa dell\'Egitto con le tappe, la fascia dell\'eclissi e i giorni"></a>'
      + '<figcaption>Il viaggio in una pagina: tocca per ingrandire.</figcaption></figure>'
      + '<ul class="elenco">';
    GIORNI.forEach(function (g) {
      const prima = g.righe.filter(function (r) { return r.foto; })[0];
      h += '<li><a href="#/giorno/' + g.n + '"' + (g.n === n ? ' class="oggi"' : '') + '>'
        + '<span class="num" style="color:' + (g.n === 6 ? g.pal.accento : g.pal.tinta) + '">' + g.n + '</span>'
        + '<span><span class="tit">' + g.titolo + '</span><span class="dat">' + g.data.replace(' 2027', '') + '</span></span>'
        + (prima ? '<img src="' + prima.foto.src + '" alt="" loading="lazy">' : '<span></span>') + '</a></li>';
    });
    return h + '</ul>';
  }

  function riga(r) {
    if (r.k === 'e') {
      return '<div class="riga evento"><div class="anno">' + r.anno + '<small>' + r.piccolo + '</small></div><p>' + r.testo + '</p></div>';
    }
    let h = '<article class="riga tappa"><div class="anno">' + r.anno + '<small>' + r.piccolo + '</small></div><div>'
      + '<h2>' + r.titolo + '</h2><p class="quando">' + r.quando + '</p>';
    if (r.foto) h += '<figure class="foto"><img src="' + r.foto.src + '" alt="' + r.foto.alt.replace(/"/g, '&quot;') + '" loading="lazy"><figcaption>' + r.foto.did + '</figcaption></figure>';
    h += '<p class="breve">' + r.breve + '</p><h3>Da guardare</h3><ul>' + r.guarda.map(function (g) { return '<li>' + g + '</li>'; }).join('') + '</ul>';
    if (r.cielo) h += '<p class="nota cielo"><strong>Il cielo.</strong> ' + r.cielo + '</p>';
    if (r.nota) {
      const testo = '<strong>' + r.nota.t + '</strong> ' + r.nota.x;
      h += r.nota.img ? '<div class="nota con-foto"><p>' + testo + '</p><img src="' + r.nota.img + '" alt="" loading="lazy"></div>' : '<p class="nota">' + testo + '</p>';
    }
    if (r.grafico) h += r.grafico;
    if (r.numero) h += '<p class="numero"><b>' + r.numero[0] + '</b><span>' + r.numero[1] + '</span></p>';
    if (r.wiki.length) h += '<p class="wiki">Su Wikipedia: ' + r.wiki.join(', ') + '</p>';
    return h + '</div></article>';
  }

  function vistaGiorno(n) {
    const g = GIORNI.filter(function (x) { return x.n === n; })[0];
    if (!g) return vistaGiorni();
    tavolozza(g.pal);
    let h = '<a class="torna" href="#/">Tutti i giorni</a><header><p class="giorno">Giorno ' + g.n + ', ' + g.data + '</p><h1>' + g.titolo + '</h1>'
      + '<p class="filo">' + g.filo + '</p>' + (g.profilo || '') + '</header>';
    if (g.righe.length) h += '<section class="linea">' + g.righe.map(riga).join('') + '</section>';
    h += '<section class="chiusura' + (g.righe.length ? '' : ' viaggio') + '"><h2>Sul posto</h2><dl>'
      + g.chiusura.map(function (c) { return '<dt>' + c[0] + '</dt><dd>' + c[1] + '</dd>'; }).join('') + '</dl></section>';
    h += '<nav class="passi">' + (n > 1 ? '<a href="#/giorno/' + (n - 1) + '">Giorno ' + (n - 1) + '</a>' : '<span></span>')
      + (n < GIORNI.length ? '<a href="#/giorno/' + (n + 1) + '">Giorno ' + (n + 1) + '</a>' : '<span></span>') + '</nav>';
    return h;
  }

  function vistaMappa() {
    if (typeof L === 'undefined') {
      return '<header style="padding:28px 16px"><h1>Mappa</h1><p class="filo">La mappa ha bisogno della connessione. Le giornate e le schede funzionano anche senza rete.</p></header>';
    }
    return '<div class="chips" id="chips"></div><div id="mappa"></div>'
      + '<p class="mappa-nota">La linea tratteggiata unisce le tappe in ordine di visita: non è il percorso reale. Alcune posizioni sono indicative.</p>';
  }

  function vistaLocandina() {
    return '<div class="loc-barra"><a href="#/">Tutti i giorni</a><span>Scorri di lato, tocca per ingrandire</span></div>'
      + '<div class="loc-area" id="locArea"><img src="img/panoramica.jpg" alt="Locandina del viaggio: mappa dell\'Egitto con le tappe, la fascia dell\'eclissi e i giorni"></div>';
  }

  function voci(lista, fn) { return '<ul class="voci">' + lista.map(function (v) { return '<li>' + fn(v) + '</li>'; }).join('') + '</ul>'; }

  function vistaBasi() {
    function wiki(v) { return '<span class="wiki-riga">Su Wikipedia: ' + v[v.length - 1] + '</span>'; }
    return '<header><h1>Le basi</h1><p class="filo">Quello che serve per orientarsi fra tremila anni di storia, prima di entrare nel primo tempio.</p></header>'
      + '<section class="sezione"><h2>Linea del tempo</h2>' + voci(BASI.tempo, function (v) { return '<b>' + v[0] + '</b><em>' + v[1] + '</em><span>' + v[2] + ' Lo vedrete a: ' + v[3] + '.</span>' + wiki(v); }) + '</section>'
      + '<section class="sezione"><h2>I sovrani da riconoscere</h2>' + voci(BASI.sovrani, function (v) { return '<b>' + v[0] + '</b><em>' + v[1] + '</em><span>' + v[2] + '</span>' + wiki(v); }) + '</section>'
      + '<section class="sezione"><h2>Gli dèi</h2>' + voci(BASI.dei, function (v) { return '<b>' + v[0] + '</b><span>' + v[1] + '. ' + v[2] + '</span>' + wiki(v); }) + '</section>'
      + '<section class="sezione"><h2>Il cielo degli Egizi in cinque idee</h2><ul class="voci numerate">' + BASI.cielo.map(function (v) { return '<li><b>' + v[0] + '</b><span>' + v[1] + '</span>' + wiki(v) + '</li>'; }).join('') + '</ul></section>'
      + '<section class="sezione"><h2>Glossario</h2>' + voci(BASI.glossario, function (v) { return '<b>' + v[0] + '</b><span>' + v[1] + '</span>' + wiki(v); }) + '</section>';
  }

  function leggiValigia() { try { return JSON.parse(localStorage.getItem(CHIAVE_VALIGIA)) || {}; } catch (e) { return {}; } }

  function spunte(idLista, gruppi) {
    const fatte = leggiValigia();
    let h = '';
    gruppi.forEach(function (gruppo) {
      h += '<h3>' + gruppo[0] + '</h3><ul class="spunte">' + gruppo[1].map(function (v) {
        const chiave = (idLista + '|' + v).replace(/"/g, '&quot;');
        return '<li><label><input type="checkbox" data-voce="' + chiave + '"' + (fatte[idLista + '|' + v] ? ' checked' : '') + '><span>' + v + '</span></label></li>';
      }).join('') + '</ul>';
    });
    return h;
  }

  function ul(l) { return '<ul class="elenco-semplice">' + l.map(function (v) { return '<li>' + v + '</li>'; }).join('') + '</ul>'; }

  function vistaOutfit() {
    const O = OUTFIT;
    let h = '<header><h1>Outfit</h1><p class="filo">' + O.intro + '</p></header>'
      + '<section class="sezione"><h2>Le regole</h2>' + voci(O.regole, function (v) { return '<b>' + v[0] + '</b><span>' + v[1] + '</span>'; }) + '</section>'
      + '<section class="sezione"><h2>Il clima</h2>' + voci(O.clima, function (v) { return '<b>' + v[0] + '</b><em>' + v[1] + '</em><span>' + v[2] + '</span>'; })
      + '<p class="quando" style="margin-top:10px">' + O.clima_nota + '</p><h3>Come reggere il caldo</h3>' + ul(O.caldo) + '</section>'
      + '<section class="sezione"><h2>I colori</h2><div class="coppia">' + O.palette.map(function (v) {
        const nome = 'palette-' + v[0].toLowerCase();
        return '<figure class="foto">' + (O.foto.indexOf(nome) >= 0 ? '<img src="img/outfit-' + nome + '.jpg" alt="Capi nei colori consigliati per ' + v[0] + '" loading="lazy">' : '')
          + '<figcaption><b>' + v[0] + '</b> ' + v[1] + '</figcaption></figure>';
      }).join('') + '</div>'
      + '<p class="quando" style="margin-top:10px">' + O.palette_nota + '</p><h3>Su cosa investire</h3>'
      + voci(O.priorita, function (v) { return '<b>' + v[0] + '</b><span>' + v[1] + '</span>'; }) + '</section>'
      + '<section class="sezione"><h2>Come vestirsi</h2>' + O.situazioni.map(function (v) {
        return '<div class="situazione"><h3>' + v[0] + '</h3><p>' + v[1] + '</p><div class="look-riga">'
          + v[2].filter(function (n) { return O.foto.indexOf(n) >= 0; }).map(function (n) { return '<img src="img/outfit-' + n + '.jpg" alt="" loading="lazy">'; }).join('')
          + '</div></div>';
      }).join('') + '</section>';
    O.liste.forEach(function (l) {
      h += '<section class="sezione"><h2>' + l[1] + '</h2>' + spunte(l[0], l[2]) + '</section>';
    });
    h += '<section class="sezione"><h2>Da lasciare a casa</h2>' + ul(O.evitare) + '<p style="margin-top:12px">' + O.zaino + '</p>'
      + '<p class="fonte">Le spunte restano su questo dispositivo. ' + O.fonte + '</p></section>';
    return h;
  }

  function vistaInfo() {
    return '<header><h1>Info</h1><p class="filo">Dove si dorme, cosa è compreso e cosa resta da chiarire.</p></header>'
      + '<section class="sezione"><h2>Le notti</h2>' + voci(INFO.notti, function (v) { return '<b>' + v[0] + '</b><em>' + v[1] + '</em><span>' + v[2] + '</span>'; }) + '</section>'
      + '<section class="sezione"><h2>La quota</h2><h3>Compreso</h3>' + ul(INFO.compreso) + '<h3>Non compreso</h3>' + ul(INFO.escluso) + '</section>'
      + '<section class="sezione"><h2>Valigia</h2><p><a href="#/outfit">Liste con le spunte e consigli nella scheda Outfit</a></p></section>'
      + '<section class="sezione"><h2>Da chiarire</h2>' + ul(INFO.aperti) + '</section>'
      + '<section class="sezione"><h2>Fonti</h2><p><a href="https://www.sivola.it/viaggi/egitto-eclissi-perri" target="_blank" rel="noopener">Pagina del viaggio su SiVola</a></p>'
      + '<p><a href="#/crediti">Crediti delle foto</a></p><p class="fonte">Date e misure storiche non sono state riverificate una per una.</p></section>';
  }

  function vistaCrediti() {
    return '<a class="torna" href="#/info">Info</a><header><h1>Crediti delle foto</h1><p class="filo">Tutte le foto vengono da Wikimedia Commons, con licenza libera. Sono state ridimensionate.</p></header>'
      + '<section class="sezione">' + voci(CREDITI, function (c) { return '<b>' + c.tappa + '</b><span>Giorno ' + c.giorno + '. ' + c.autore + ', ' + c.licenza + '</span>'; })
      + '<p class="fonte">Mappa: © OpenStreetMap.</p></section>';
  }

  // ------------------------------------------------------------ navigazione
  function mostra() {
    const r = (location.hash || '#/').slice(1);
    const m = r.match(/^\/giorno\/(\d+)/);
    let scheda = 'giorni';
    EgittoMappa.chiudi();
    tavolozza(PAL_BASE);
    vista.className = 'pagina';
    if (m) vista.innerHTML = vistaGiorno(Number(m[1]));
    else if (r === '/locandina') { vista.className = 'pagina piena'; vista.innerHTML = vistaLocandina(); }
    else if (r === '/mappa') { scheda = 'mappa'; vista.className = 'pagina piena'; vista.innerHTML = vistaMappa(); }
    else if (r === '/basi') { scheda = 'basi'; vista.innerHTML = vistaBasi(); }
    else if (r === '/outfit') { scheda = 'outfit'; vista.innerHTML = vistaOutfit(); }
    else if (r === '/info') { scheda = 'info'; vista.innerHTML = vistaInfo(); }
    else if (r === '/crediti') { scheda = 'info'; vista.innerHTML = vistaCrediti(); }
    else vista.innerHTML = vistaGiorni();

    Array.prototype.forEach.call(schede.querySelectorAll('a'), function (a) {
      a.classList.toggle('attiva', a.getAttribute('data-scheda') === scheda);
    });
    window.scrollTo(0, 0);
    if (scheda === 'mappa' && document.getElementById('mappa')) {
      EgittoMappa.apri(document.getElementById('mappa'), document.getElementById('chips'));
    }
  }

  vista.addEventListener('click', function (e) {
    if (e.target.parentNode && e.target.parentNode.id === 'locArea') e.target.parentNode.classList.toggle('grande');
  });

  // Le schede funzionano sempre, anche quando l'indirizzo non cambia (per esempio Giorni mentre si è già sui giorni)
  schede.addEventListener('click', function (e) {
    const a = e.target.closest ? e.target.closest('a') : null;
    if (a && a.getAttribute('href') === (location.hash || '#/')) mostra();
  });

  vista.addEventListener('change', function (e) {
    const voce = e.target.getAttribute && e.target.getAttribute('data-voce');
    if (!voce) return;
    const fatte = leggiValigia();
    if (e.target.checked) fatte[voce] = 1; else delete fatte[voce];
    try { localStorage.setItem(CHIAVE_VALIGIA, JSON.stringify(fatte)); } catch (err) { /* navigazione privata: la spunta vale solo ora */ }
  });

  window.addEventListener('hashchange', mostra);
  mostra();

  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    const giaControllata = !!navigator.serviceWorker.controller;
    let ricaricata = false;
    navigator.serviceWorker.addEventListener('controllerchange', function () {
      if (giaControllata && !ricaricata) { ricaricata = true; location.reload(); }
    });
    navigator.serviceWorker.register('sw.js').then(function (reg) { reg.update(); }).catch(function () {});
  }
});
