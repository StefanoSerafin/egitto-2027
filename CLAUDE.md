# egitto-2027 (sito) — istruzioni per Claude Code

## Cos'è
Web app per iPhone e iPad del viaggio in Egitto di Stefano e Ilenia (28 luglio – 10 agosto 2027 secondo
le date pubblicate; il programma ha 13 giorni, rientro il 9 con arrivo forse il 10;
SiVola con Luca Perri, eclissi totale del 2 agosto). Presenta le 13 giornate con schede dei
luoghi, foto, grafici e link a Wikipedia, più mappa, basi culturali e informazioni pratiche.

Stesso schema di `Personali/Copenaghen/sito/`: multi-file, niente build a runtime, dati in
`data/*.js` come `const` caricati con `<script src>` (funziona anche da `file://`), routing a hash.

## Da dove vengono i contenuti
I contenuti NON si scrivono qui a mano. La fonte è una sola:

- `../infografiche/genera.py` — giorni 3–12: testi, tavolozze, sagome, grafici, elenco foto.
- `tools/costruisci.py` — aggiunge i giorni 1, 2 e 13, le coordinate della mappa, le Basi e le Info,
  poi scrive `data/giorni.js`, `data/extra.js`, `css/giorno.css`, copia le foto in `img/` e
  rigenera `sw.js` con una versione nuova.

Per cambiare un testo: modificarlo in `genera.py` (o in `costruisci.py` per giorni 1/2/13, Basi,
Info), poi lanciare `python3 ../infografiche/genera.py && python3 tools/costruisci.py`.
`css/giorno.css`, `data/*.js` e `sw.js` sono generati: non modificarli a mano.

## File scritti a mano
- `index.html` — ossatura e barra delle schede (Giorni, Mappa, Basi, Outfit, Info).
- `css/app.css` — solo le parti dell'app (schede, elenco giorni, mappa, liste).
- `js/app.js` — router e viste. La tavolozza del giorno si applica impostando le variabili CSS.
- `js/mappa.js` — `EgittoMappa`: Leaflet da unpkg (unica eccezione no-CDN, come Copenaghen),
  tessere OpenStreetMap senza chiave, uno spillo per tappa con il numero del giorno.
- `tools/sw.modello.js` — modello del service worker.

## Uso offline e aggiornamenti
`sw.js` salva tutti i file alla prima apertura in https. Immagini e Leaflet si leggono dalla copia salvata;
pagina, stile, codice e dati si chiedono prima alla rete (con ripiego sulla copia salvata se la rete manca o
tarda oltre 3,5 s), così un iPhone connesso vede subito l'ultima versione. La mappa richiede sempre la rete.
Su iPhone l'app aggiunta alla Home ha una memoria separata da Safari: provare lì, non solo nel browser.
Mai link che aprono un file (immagine, PDF) nella stessa finestra: nell'app a tutto schermo non c'è il tasto indietro.

## Regole
- La vista Giorni mostra `img/panoramica.jpg`, ricavata da `../Egitto 2027_ Sotto il Sole Nero_corretta.png`
  (locandina fatta da Stefano, con il doppio «Giorno 12» della striscia unito da Claude in un'unica intestazione). La vecchia `Infografica viaggio.PNG` non si usa più.
- La scheda Outfit (`OUTFIT` in `costruisci.py`) contiene i consigli raccolti su ChatGPT il 9 ottobre 2026,
  organizzati per situazione e NON per giorno (scelta di Stefano: «un giorno vale l'altro»):
  testi più le immagini `img/outfit-*.jpg`, ritagliate una volta dalle schermate (Stefano conferma che sono
  generate da ChatGPT e utilizzabili). Non hanno una sorgente nel progetto: non cancellarle da `img/`.
- **Mai** mettere nel repo prezzi pagati, acconti, numeri di prenotazione, documenti, telefoni.
  Solo itinerario, schede culturali e informazioni già pubbliche sulla pagina SiVola.
- Foto **solo** con licenza libera da Wikimedia Commons, elencate in `genera.py` (`FOTO`) e
  creditate nella vista Crediti. Chiedere conferma a Stefano prima di scaricarne di nuove.
- Target iPhone Safari: `addEventListener` dentro `DOMContentLoaded`, caselle di spunta native
  con `label`, niente funzioni che chiedano permessi.
- Le coordinate in `COORD` (`costruisci.py`) non sono verificate sul posto; quelle in
  `INDICATIVE` compaiono in mappa come «posizione indicativa».

## Stato
Pubblicata il 9 ottobre 2026: repo `github.com/StefanoSerafin/egitto-2027`, GitHub Pages su
`https://stefanoserafin.github.io/egitto-2027/`. Provata in Chrome a larghezza telefono; su iPhone
e iPad va ancora verificata, compreso l'uso offline.

## Aggiornare il sito
Repo annidato con remote proprio, escluso dal `.gitignore` della root del workspace.
Dopo `tools/costruisci.py`: `git add -A && git commit && git push`. Pages serve il branch `main`,
cartella `/ (root)`; `.nojekyll` è presente.
