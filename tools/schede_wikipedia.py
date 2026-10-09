#!/usr/bin/env python3
"""Prepara le schede mostrate dall'app prima di aprire un link a Wikipedia.

    python3 tools/schede_wikipedia.py      (richiede la rete; lanciare DOPO tools/costruisci.py)

Per ogni voce di Wikipedia collegata nell'app (giornate e Basi) raccoglie:
  - descrizione breve, introduzione e immagine principale da Wikipedia;
  - dati strutturati (date, misure, luogo, autori...) da Wikidata;
  - i punti dell'app in cui la voce è citata.
Scrive data/schede.js (const SCHEDE). Nessun testo è scritto a mano: è una sintesi automatica.
L'immagine non viene scaricata: l'app la carica da Wikimedia solo quando c'è la rete.
"""
import json, os, re, time, urllib.error, urllib.parse, urllib.request

SITO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "egitto-2027-schede/1.0 (web app personale di viaggio)"}
SEZIONI = {"tempo": "Linea del tempo", "sovrani": "I sovrani", "dei": "Gli dèi", "cielo": "Il cielo degli Egizi", "glossario": "Glossario"}

# proprietà di Wikidata mostrate nella scheda, nell'ordine di priorità
PROP = [
    ("P585", "Data"), ("P571", "Costruzione o fondazione"), ("P1619", "Apertura"), ("P569", "Nascita"), ("P570", "Morte"),
    ("P2348", "Epoca"), ("P2047", "Durata"), ("P2048", "Altezza"), ("P2043", "Lunghezza"), ("P2049", "Larghezza"),
    ("P2046", "Superficie"), ("P2067", "Massa"), ("P2234", "Volume"), ("P1082", "Abitanti"),
    ("P84", "Architetto"), ("P88", "Committente"), ("P112", "Fondatore"), ("P61", "Scopritore"), ("P575", "Scoperta"),
    ("P825", "Dedicato a"), ("P186", "Materiale"), ("P149", "Stile"), ("P1435", "Tutela"),
    ("P131", "Si trova a"), ("P276", "Luogo"), ("P119", "Sepoltura"), ("P22", "Padre"), ("P25", "Madre"), ("P26", "Coniuge"),
    ("P1215", "Magnitudine apparente"), ("P2583", "Distanza dalla Terra"), ("P31", "Tipo"),
]
UNITA = {"Q11573": "m", "Q828224": "km", "Q25343": "m²", "Q712226": "km²", "Q35852": "ha", "Q191118": "t", "Q11570": "kg",
         "Q11574": "s", "Q7727": "min", "Q25235": "ore", "Q25517": "m³", "Q4243638": "km³", "Q531": "anni luce", "Q12129": "parsec",
         "Q174728": "cm", "Q3710": "piedi", "Q577": "anni", "Q573": "giorni"}
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]
# ritocchi a mano dove il dato automatico è palesemente sbagliato
CORREZIONI = {"it:Basilosaurus": {"descr": "Genere estinto di cetacei"}}
ABBR = ["a.C.", "d.C.", "ca.", "c.", "n.", "es.", "cfr.", "ecc.", "sec.", "pp.", "p.", "S.", "St.", "Dr.", "No.", "e.g.", "i.e.", "fl.", "r.", "lett.", "ar.", "gr."]


def get(url):
    for attesa in (0, 15, 45):
        time.sleep(attesa)
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise RuntimeError("troppe richieste: riprovare più tardi")


def api(sito, **p):
    p.update(format="json", formatversion="2")
    time.sleep(0.6)
    return get(f"https://{sito}/w/api.php?" + urllib.parse.urlencode(p))


def blocchi(lista, n):
    for i in range(0, len(lista), n):
        yield lista[i:i + n]


def costante(testo, nome):
    """Estrae il valore JSON di «const NOME = ...;» da un file di dati."""
    i = testo.index(f"const {nome} = ") + len(f"const {nome} = ")
    return json.JSONDecoder().raw_decode(testo, i)[0]


def collegamenti():
    """Tutti i link a Wikipedia dell'app: {(lingua, titolo): [(testo, indirizzo interno)]}."""
    giorni = costante(open(os.path.join(SITO, "data", "giorni.js"), encoding="utf-8").read(), "GIORNI")
    basi = costante(open(os.path.join(SITO, "data", "extra.js"), encoding="utf-8").read(), "BASI")
    out = {}

    def aggiungi(html, dove):
        for lingua, t in re.findall(r"https://(it|en)\.wikipedia\.org/wiki/([^\"]+)", html):
            chiave = (lingua, urllib.parse.unquote(t).replace("_", " "))
            if dove not in out.setdefault(chiave, []):
                out[chiave].append(dove)

    for g in giorni:
        for r in g["righe"]:
            if r["k"] == "t":
                aggiungi(" ".join(r["wiki"]), (f"Giorno {g['n']}: {r['titolo']}", f"#/giorno/{g['n']}"))
    for sezione, voci in basi.items():
        for v in voci:
            aggiungi(v[-1], (f"Basi: {SEZIONI[sezione]}", "#/basi"))
    return out


# ------------------------------------------------------------ testo
def pulisci(t):
    t = re.sub(r"\[[^\]]*\]", "", t.replace("\n", " "))

    def par(m):
        c = m.group(1)
        if re.search(r"[ɐ-ʯͰ-Ͽ֐-ۿἀ-῿\U00013000-\U0001342F]", c) or \
           re.search(r"pronuncia|AFI|in arabo|in greco|in copto|in egizio|traslitterat|ascolta|in lingua|IPA", c, re.I):
            return ""
        return "(" + c + ")"

    for _ in range(3):
        t = re.sub(r"\(([^()]*)\)", par, t)
    t = re.sub(r"[\u0370-\u03FF\u0590-\u06FF\u1F00-\u1FFF\U00013000-\U0001342F]+[\u200e\u200f]*\??", "", t)
    t = t.replace("..", ".")
    t = re.sub(r"\(\s*[;,]\s*", "(", t)
    t = re.sub(r"\(\s*\)", "", t)
    t = re.sub(r"\s+([,;.:])", r"\1", t)
    return re.sub(r"\s{2,}", " ", t).strip()


def frasi(t, massimo=5, caratteri=780):
    for a in ABBR:
        t = t.replace(a, a.replace(".", "∯"))
    t = re.sub(r"\b([A-Z])\.", r"\1∯", t)  # iniziali
    pezzi = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Ý«\"“])", t)
    out, tot = [], 0
    for p in pezzi:
        p = p.replace("∯", ".").strip()
        if len(p) < 25:
            continue
        if out and (tot + len(p) > caratteri or len(out) >= massimo):
            break
        out.append(p)
        tot += len(p)
    return out


# ------------------------------------------------------------ Wikidata
def numero(s):
    s = s.lstrip("+")
    if "." in s:
        intero, dec = s.split(".")
        dec = dec.rstrip("0")
    else:
        intero, dec = s, ""
    neg = intero.startswith("-")
    intero = intero.lstrip("-")
    if len(intero) > 4:
        intero = f"{int(intero):,}".replace(",", ".")
    return ("−" if neg else "") + intero + ("," + dec[:2] if dec else "")


def tempo(v):
    m = re.match(r"([+-])(\d+)-(\d\d)-(\d\d)", v["time"])
    if not m:
        return None
    anno, mese, giorno, prec = int(m.group(2)), int(m.group(3)), int(m.group(4)), v.get("precision", 9)
    coda = " a.C." if m.group(1) == "-" else ""
    if prec >= 11 and mese and giorno:
        return f"{giorno} {MESI[mese - 1]} {anno}{coda}"
    if prec == 10 and mese:
        return f"{MESI[mese - 1]} {anno}{coda}"
    if prec == 9:
        return f"{anno}{coda}"
    if prec in (7, 8):
        return f"intorno al {anno}{coda}"
    return None


def valore(snak, etichette):
    if snak.get("snaktype") != "value":
        return None
    dv = snak["datavalue"]
    if dv["type"] == "wikibase-entityid":
        return etichette.get(dv["value"]["id"])
    if dv["type"] == "time":
        return tempo(dv["value"])
    if dv["type"] == "quantity":
        u = dv["value"]["unit"].rsplit("/", 1)[-1]
        unita = "" if u == "1" else UNITA.get(u) or etichette.get(u) or ""
        if unita == "s":
            sec = round(float(dv["value"]["amount"]))
            if sec >= 60:
                return f"{sec // 60} min {sec % 60} s"
        return (numero(dv["value"]["amount"]) + " " + unita).strip()
    return None


def migliori(claims):
    pref = [c for c in claims if c.get("rank") == "preferred"]
    return pref or [c for c in claims if c.get("rank") != "deprecated"]


def main():
    link = collegamenti()
    print(len(link), "voci collegate")
    pagine = {}  # (lingua, titolo) -> dati
    for lingua in ("it", "en"):
        titoli = sorted(t for (l, t) in link if l == lingua)
        for gruppo in blocchi(titoli, 20):
            d = api(f"{lingua}.wikipedia.org", action="query", redirects="1", titles="|".join(gruppo),
                    prop="extracts|pageimages|pageprops|description", exintro="1", explaintext="1", exlimit="20",
                    piprop="thumbnail", pithumbsize="640", pilimit="20", ppprop="wikibase_item")
            q = d["query"]
            alias = {x["to"]: x["from"] for x in q.get("normalized", []) + q.get("redirects", [])}
            for p in q["pages"]:
                titolo = p["title"]
                while titolo in alias and (lingua, titolo) not in link:
                    titolo = alias[titolo]
                if (lingua, titolo) not in link:
                    titolo = next((t for t in gruppo if t.lower() == p["title"].lower()), titolo)
                pagine[(lingua, titolo)] = p
    # Wikidata: affermazioni, poi etichette dei valori
    qid = {k: p.get("pageprops", {}).get("wikibase_item") for k, p in pagine.items()}
    entita = {}
    for gruppo in blocchi(sorted({q for q in qid.values() if q}), 45):
        entita.update(api("www.wikidata.org", action="wbgetentities", ids="|".join(gruppo), props="claims|descriptions", languages="it|en")["entities"])
    servono = set()
    for e in entita.values():
        for pid, _ in PROP:
            for c in migliori(e.get("claims", {}).get(pid, []))[:3]:
                dv = c["mainsnak"].get("datavalue", {})
                if dv.get("type") == "wikibase-entityid":
                    servono.add(dv["value"]["id"])
                elif dv.get("type") == "quantity":
                    u = dv["value"]["unit"].rsplit("/", 1)[-1]
                    if u != "1" and u not in UNITA:
                        servono.add(u)
    etichette, etichette_en = {}, {}
    for gruppo in blocchi(sorted(servono), 45):
        for i, e in api("www.wikidata.org", action="wbgetentities", ids="|".join(gruppo), props="labels", languages="it|en")["entities"].items():
            lab = e.get("labels", {})
            etichette[i] = (lab.get("it") or {}).get("value")
            etichette_en[i] = (lab.get("en") or lab.get("it") or {}).get("value")

    schede, senza = {}, []
    for (lingua, titolo), dove in sorted(link.items()):
        p = pagine.get((lingua, titolo))
        if not p or p.get("missing"):
            senza.append(f"{lingua}:{titolo}")
            continue
        e = entita.get(qid.get((lingua, titolo)) or "", {})
        # descrizione e valori solo nella lingua della scheda: meglio un campo vuoto che una riga in inglese in una scheda italiana
        descr = (e.get("descriptions", {}).get(lingua) or {}).get("value") or (p.get("description") if lingua == "en" else "") or ""
        umano = any(c["mainsnak"].get("datavalue", {}).get("value", {}).get("id") == "Q5" for c in e.get("claims", {}).get("P31", []))
        fatti = []
        for pid, nome in PROP:
            if umano and pid in ("P2048", "P2067", "P31"):
                continue
            vals = []
            for c in migliori(e.get("claims", {}).get(pid, []))[:3]:
                v = valore(c["mainsnak"], etichette if lingua == "it" else etichette_en)
                if v and v not in vals and v.lower() != "umano":
                    vals.append(v)
            if vals:
                fatti.append([nome, ", ".join(vals)])
            if len(fatti) == 6:
                break
        schede[f"{lingua}:{titolo}"] = {
            "titolo": p["title"], "lingua": lingua, "descr": descr[:1].upper() + descr[1:],
            "img": p.get("thumbnail", {}).get("source"), "fatti": fatti, "punti": frasi(pulisci(p.get("extract", ""))),
            "dove": [list(x) for x in dove],
            "url": f"https://{lingua}.wikipedia.org/wiki/" + urllib.parse.quote(titolo.replace(" ", "_"), safe="_(),"),
        }
    for k, c in CORREZIONI.items():
        if k in schede:
            schede[k].update(c)
    testo = "// Generato da tools/schede_wikipedia.py il " + time.strftime("%d/%m/%Y") + ": non modificare a mano.\n" \
            + "const SCHEDE_DATA = " + json.dumps(time.strftime("%d/%m/%Y")) + ";\n" \
            + "const SCHEDE = " + json.dumps(schede, ensure_ascii=False, indent=1) + ";\n"
    open(os.path.join(SITO, "data", "schede.js"), "w", encoding="utf-8").write(testo)
    print(len(schede), "schede scritte;", "senza pagina:", senza or "nessuna")
    print("senza immagine:", sum(1 for s in schede.values() if not s["img"]), "| senza dati:", sum(1 for s in schede.values() if not s["fatti"]),
          "| senza punti:", [k for k, s in schede.items() if not s["punti"]])


if __name__ == "__main__":
    main()
