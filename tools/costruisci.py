#!/usr/bin/env python3
"""Costruisce i dati della web app a partire dalle infografiche.

    python3 tools/costruisci.py

Legge ../infografiche/genera.py (giorni 3-12, stile, foto) e aggiunge qui i giorni
1, 2 e 13, le coordinate per la mappa, le Basi e le Info. Scrive:
  css/giorno.css   stile delle giornate (lo stesso delle infografiche)
  data/giorni.js   const PAL_BASE, GIORNI
  data/extra.js    const BASI, INFO, OUTFIT, CREDITI
  img/*.jpg        copia delle foto usate
  sw.js            elenco dei file per l'uso offline, con versione nuova
"""
import importlib.util, json, os, shutil, subprocess, time

SITO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO_DIR = os.path.join(os.path.dirname(SITO), "infografiche")
spec = importlib.util.spec_from_file_location("genera", os.path.join(INFO_DIR, "genera.py"))
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
E, T, W = G.E, G.T, G.W

# ------------------------------------------------------------ giorno 2 (nelle infografiche è fatto a mano)
FOTO_G2 = {
    "g2-cittadella": ("Jorge Láscar", "CC BY 2.0"), "g2-khan": ("Diego Delso", "CC BY-SA 3.0"),
    "g2-sulayman": ("Amr F. Nagy", "pubblico dominio"), "g2-muhammad-ali": ("kallerna", "CC BY-SA 3.0"),
    "g2-orologio": ("Glenn Ashton", "CC BY-SA 3.0"),
}


def p_cairo():
    return G.profilo(
        '<path d="M0 190V150h36v-10h14v10h40v-10h14v10h40v-10h14v10h40v-10h14v10h396v-10h14v10h40v-10h14v10h40v-10h14v10h40v-10h14v10h22v40z"/>'
        '<rect x="300" y="104" width="220" height="48"/><path d="M312 104a34 34 0 0 1 68 0z"/><path d="M440 104a34 34 0 0 1 68 0z"/>'
        '<path d="M358 96a52 52 0 0 1 104 0v8H358z"/><rect x="408" y="30" width="4" height="16"/>'
        '<path d="M282 152V46l5-36 5 36v106z"/><path d="M528 152V46l5-36 5 36v106z"/>'
        '<rect x="278" y="70" width="18" height="5"/><rect x="524" y="70" width="18" height="5"/>'
        '<rect x="278" y="104" width="18" height="5"/><rect x="524" y="104" width="18" height="5"/>')


def g_altezze_cairo():
    return G.grafico(420, 220, "Confronto di altezze: cupola 52 metri, minareti 82 metri, Duomo di Milano 108 metri",
        '<line class="l" x1="10" y1="180" x2="410" y2="180"/>'
        '<path class="t" d="M40 180v-44a40 34 0 0 1 80 0v44z"/><text class="n" x="80" y="96" text-anchor="middle">52 m</text><text x="80" y="200" text-anchor="middle">cupola</text>'
        '<path class="t" d="M196 180V84l7-27 7 27v96z"/><rect class="t" x="192" y="104" width="22" height="5"/><rect class="t" x="192" y="134" width="22" height="5"/>'
        '<text class="n" x="203" y="46" text-anchor="middle">82 m</text><text x="203" y="200" text-anchor="middle">minareti</text>'
        '<path class="tr" d="M290 180v-58l22-20 10-84 10 84 22 20v58z"/><text x="372" y="60" class="m">108 m</text>'
        '<text x="322" y="200" text-anchor="middle">Duomo di Milano</text><text x="322" y="215" text-anchor="middle" class="m">per confronto</text>')


GIORNO_2 = dict(n=2, file="", data="giovedì 29 luglio 2027", titolo="Il Cairo dopo i faraoni",
  pal=G.pal("#EEF1EA", "#14302A", "#1F6B55", "#D5E2DA", "#A8771A", "#4F6660", dt="#E3C27A"), profilo=p_cairo,
  filo="Sette secoli di storia islamica in una fortezza e in un mercato: da Saladino che si difende dai Crociati a Muhammad Ali che inventa l'Egitto moderno.",
  righe=[
   E("969", "", "I Fatimidi fondano il Cairo. Tre anni dopo nasce al-Azhar, ancora oggi moschea e università."),
   T("1176", "prima tappa", "Cittadella del Cairo", "Iniziata da Saladino contro i Crociati, ampliata da Mamelucchi e Ottomani",
     "La fortezza sulla collina da cui si è governato l'Egitto, qualunque fosse la dinastia al potere.",
     ["Le mura e le torri di Saladino", "Il panorama sul Cairo: con aria limpida si vedono le piramidi", "Le due moschee al suo interno, lontane fra loro tre secoli"],
     numero=("700", "anni come sede del potere, fino al 1874"),
     wiki=[W("Cittadella del Cairo"), W("Saladino"), W("Sultanato mamelucco", "Mamelucchi")],
     foto=("g2-cittadella", "Le mura della Cittadella del Cairo", "Le mura della Cittadella, con un minareto e una cupola che spuntano dall'interno.")),
   E("1250", "", "Prendono il potere i Mamelucchi, ex soldati schiavi. Governeranno per oltre 250 anni."),
   T("1382", "seconda tappa", "Bazaar di Khan el-Khalili", "Fondato dall'emiro al-Khalili come caravanserraglio per i mercanti",
     "Il mercato storico del Cairo: nato per le carovane delle spezie, non ha mai chiuso.",
     ["Le vie divise per mestiere: spezie, rame, lanterne, profumi", "Il caffè El Fishawy, aperto da oltre due secoli", "La moschea di al-Azhar, a pochi passi"],
     nota=("Come si compra.", "Il primo prezzo è un invito a trattare. Si offre meno della metà, si sorride e si è pronti ad andarsene."),
     numero=("640", "anni di commercio ininterrotto"),
     wiki=[W("Khan el-Khalili"), W("Moschea di al-Azhar"), W("Fatimidi")],
     foto=("g2-khan", "Una via del bazaar di Khan el-Khalili di sera", "Il bazaar di sera, fra lanterne e collane.")),
   E("1517", "", "Gli Ottomani conquistano l'Egitto, che diventa una provincia governata da Istanbul."),
   T("1528", "dentro la Cittadella", "Moschea di Sulayman Pascià", "Costruita undici anni dopo la conquista ottomana",
     "La prima moschea in stile ottomano d'Egitto: piccola, raccolta, con cupole basse al posto dei grandi cortili mamelucchi.",
     ["Le cupole rivestite di ceramica verde", "Gli interni dipinti e il minareto sottile a matita"],
     numero=("1ª", "moschea ottomana costruita in Egitto"),
     wiki=[W("Sulayman Pasha Mosque", "Moschea di Sulayman Pascià (in inglese)", "en")],
     foto=("g2-sulayman", "Cortile della moschea di Sulayman Pascià", "Il cortile, con le cupole basse dello stile ottomano.")),
   E("1811", "", "Muhammad Ali invita i capi mamelucchi a una festa nella Cittadella e li fa massacrare. Da quel giorno governa da solo."),
   T("1830–48", "dentro la Cittadella", "Moschea di Muhammad Ali", "Detta Moschea di Alabastro, voluta dal fondatore dell'Egitto moderno",
     "La sagoma che domina il Cairo. Copia le moschee imperiali di Istanbul per dire che l'Egitto non prende più ordini da lì.",
     ["Il rivestimento in alabastro, dentro e nel cortile", "La cupola centrale circondata da quattro semicupole",
      "La tomba di Muhammad Ali, a destra dell'ingresso", "La torre dell'orologio nel cortile"],
     nota=("L'orologio e l'obelisco.", "Nel 1845 il re di Francia regalò l'orologio in cambio dell'obelisco di Luxor, oggi in Place de la Concorde a Parigi. L'obelisco è ancora in piedi; l'orologio non ha quasi mai funzionato.", "g2-orologio"),
     grafico=g_altezze_cairo, numero=("82 m", "l'altezza dei due minareti, i più alti del Cairo storico"),
     wiki=[W("Moschea di Muhammad Ali"), W("Mehmet Ali", "Muhammad Ali"), W("Obelisco di Luxor")],
     foto=("g2-muhammad-ali", "La Moschea di Muhammad Ali vista dall'esterno", "La moschea vista dalla spianata della Cittadella.")),
   E("1874", "", "Il governo scende in città, a Palazzo Abdin. La Cittadella diventa caserma, poi museo."),
  ],
  chiusura=[("In moschea", "Spalle e ginocchia coperte per tutti, foulard sui capelli per le donne. Ci si toglie le scarpe."),
            ("Il caldo", "La Cittadella è una spianata senza ombra: cappello e acqua."),
            ("Il cielo", "Oggi nessun legame con l'astronomia. È la giornata che spiega cosa è successo nei 1.300 anni dopo l'ultimo tempio.")])

GIORNO_1 = dict(n=1, data="mercoledì 28 luglio 2027", titolo="Arrivo al Cairo", pal=G.SABBIA, profilo=None,
  filo="Volo dall'Italia e trasferimento in hotel, nel centro della città. Il Cairo è la più grande città dell'Africa: oltre venti milioni di abitanti nell'area metropolitana.",
  righe=[], chiusura=[("Visto", "Si ottiene all'arrivo ed è compreso nella quota. Con la carta d'identità servono due foto tessera: meglio il passaporto."),
                      ("Bagaglio", "Solo a mano: un trolley e uno zaino a testa."), ("Domani", "Cittadella e bazaar: abiti coprenti per le moschee.")])
GIORNO_13 = dict(n=13, data="lunedì 9 agosto 2027", titolo="Rientro in Italia", pal=G.SABBIA, profilo=None,
  filo="Trasferimento in aeroporto e volo di rientro. Le date pubblicate da SiVola arrivano al 10 agosto: secondo gli orari dei voli l'arrivo in Italia può essere la sera del 9 o il giorno dopo.",
  righe=[], chiusura=[("Liquidi", "Profumi e spezie liquide oltre i 100 ml non passano nel bagaglio a mano.")])

# ------------------------------------------------------------ coordinate (titolo della tappa -> lat, lon)
COORD = {
    "Cittadella del Cairo": (30.0299, 31.2611), "Bazaar di Khan el-Khalili": (30.0477, 31.2622),
    "Moschea di Sulayman Pascià": (30.0312, 31.2626), "Moschea di Muhammad Ali": (30.0287, 31.2599),
    "Piramide di Cheope": (29.9792, 31.1342), "Piramidi di Chefren e Micerino": (29.9761, 31.1308),
    "Grande Sfinge": (29.9753, 31.1376), "Grande Museo Egizio": (29.9949, 31.1193),
    "Piramide a gradoni di Zoser": (29.8713, 31.2165), "Memphis": (29.8494, 31.2550),
    "Piramide romboidale di Dahshur": (29.7903, 31.2094),
    "Tempio di Karnak": (25.7188, 32.6573), "Tempio di Luxor": (25.6995, 32.6391),
    "Totalità": (25.7000, 32.6370),
    "Valle dei Re": (25.7402, 32.6014), "Tempio di Hatshepsut": (25.7382, 32.6065), "Colossi di Memnone": (25.7206, 32.6105),
    "Tempio di Horus a Edfu": (24.9779, 32.8734), "Tempio di Kom Ombo": (24.4521, 32.9284),
    "Tempio di Iside a Philae": (24.0253, 32.8844), "Diga Alta di Assuan": (23.9706, 32.8773),
    "Obelisco Incompiuto": (24.0769, 32.8955), "Elefantina e l'isola di Kitchener": (24.0850, 32.8870),
    "Tempio Maggiore": (22.3372, 31.6258), "Tempio Minore": (22.3382, 31.6267),
    "L'oasi di El Fayoum": (29.4042, 30.4833),
    "Wadi El Rayan": (29.2117, 30.4213), "Al Mudawwarah e il Magic Lake": (29.2000, 30.3700), "Wadi al-Hitan": (29.2708, 30.0439),
}
# posizioni non verificate sul posto: in mappa compaiono come indicative
INDICATIVE = {"Totalità", "L'oasi di El Fayoum", "Wadi El Rayan", "Al Mudawwarah e il Magic Lake"}

# ------------------------------------------------------------ Basi e Info
BASI = {
 "tempo": [
  ("Unificazione", "c. 3100 a.C.", "Alto e Basso Egitto diventano un regno, capitale Memphis.", "Memphis"),
  ("Antico Regno", "c. 2686–2181 a.C.", "L'età delle piramidi.", "Saqqara, Dahshur, Giza"),
  ("Medio Regno", "c. 2055–1650 a.C.", "Tebe emerge, bonifica del Fayoum.", "Karnak, El Fayoum"),
  ("Nuovo Regno", "c. 1550–1069 a.C.", "L'impero: Hatshepsut, Tutankhamon, Ramses II.", "Luxor, Karnak, Valle dei Re, Abu Simbel"),
  ("Epoca tolemaica", "332–30 a.C.", "Re greci che costruiscono templi all'egizia.", "Edfu, Kom Ombo, Philae"),
  ("Epoca romana e bizantina", "30 a.C.–641 d.C.", "Fine dei culti antichi.", "Philae, Colossi di Memnone"),
  ("Epoca islamica", "dal 641 d.C.", "Fondazione del Cairo, Saladino, Mamelucchi, Ottomani.", "Cittadella, Khan el-Khalili"),
  ("Egitto moderno", "dal 1805", "Muhammad Ali, poi la Diga di Assuan.", "Moschea di Alabastro, Diga Alta"),
 ],
 "sovrani": [
  ("Zoser", "2670 a.C.", "Prima piramide, a Saqqara."), ("Snefru", "2613–2589 a.C.", "Padre di Cheope, piramidi di Dahshur."),
  ("Cheope, Chefren, Micerino", "2589–2503 a.C.", "Le tre piramidi di Giza."),
  ("Hatshepsut", "1479–1458 a.C.", "Donna faraone: obelischi di Karnak, Deir el-Bahari."),
  ("Amenhotep III", "1390–1352 a.C.", "Tempio di Luxor, Colossi di Memnone."),
  ("Tutankhamon", "1336–1327 a.C.", "Il tesoro al Grande Museo Egizio."),
  ("Seti I", "1294–1279 a.C.", "Sala ipostila di Karnak, la tomba più bella della Valle."),
  ("Ramses II", "1279–1213 a.C.", "Abu Simbel, Luxor, Memphis: 66 anni di regno."),
 ],
 "dei": [
  ("Ra", "Falco con disco solare", "Il Sole."), ("Amon", "Uomo con due alte piume", "Dio di Tebe, re degli dèi."),
  ("Osiride", "Mummia verde con corona", "Signore dei morti."), ("Iside", "Donna con trono sul capo", "Madre e maga, associata a Sirio."),
  ("Horus", "Falco", "Figlio di Iside, dio dei faraoni."), ("Hathor", "Donna con corna e disco", "Amore, musica, maternità."),
  ("Nut", "Donna arcuata sopra la terra", "Il cielo: ingoia e partorisce il Sole."), ("Ptah", "Mummia con scettro", "Dio creatore di Memphis."),
  ("Sobek", "Coccodrillo", "Il Nilo e la sua forza."), ("Seshat", "Donna con stella sul capo", "Misura e orientamento dei templi."),
 ],
 "cielo": [
  ("I punti cardinali", "Le piramidi sono orientate a nord con un errore di pochi primi d'arco, ottenuto osservando le stelle."),
  ("Le stelle imperiture", "Le stelle vicine al polo non tramontano mai: erano la destinazione dell'anima del re."),
  ("Sirio e il calendario", "La prima apparizione di Sirio all'alba, a metà luglio, annunciava la piena del Nilo e il capodanno. Da qui l'anno di 365 giorni."),
  ("I decani e le 24 ore", "Trentasei gruppi di stelle scandivano la notte in dodici parti. La nostra giornata di 24 ore viene da lì."),
  ("Gli allineamenti solari", "Molti templi puntano al sorgere del Sole nei solstizi o in date scelte."),
 ],
 "glossario": [
  ("Mastaba", "Tomba a forma di parallelepipedo basso, antenata della piramide."), ("Pilone", "Portale monumentale con due torri inclinate, facciata dei templi."),
  ("Sala ipostila", "Sala con il tetto retto da file di colonne."), ("Obelisco", "Monolite a punta, simbolo di un raggio di Sole."),
  ("Cartiglio", "Ovale che racchiude il nome del faraone nei geroglifici."), ("Nilometro", "Pozzo o scala graduata per misurare la piena del Nilo."),
  ("Levata eliaca", "Primo giorno in cui una stella torna visibile all'alba."), ("Feluca", "Barca a vela tradizionale del Nilo."),
 ],
}
# voci di Wikipedia in italiano per ogni argomento delle Basi (esistenza verificata il 9 ottobre 2026)
BASI_WIKI = {
 "Unificazione": [W("Periodo Protodinastico (Egitto)", "Periodo protodinastico"), W("Narmer")],
 "Antico Regno": [W("Antico Regno (Egitto)", "Antico Regno")], "Medio Regno": [W("Medio Regno (Egitto)", "Medio Regno")],
 "Nuovo Regno": [W("Nuovo Regno (Egitto)", "Nuovo Regno")], "Epoca tolemaica": [W("Egitto tolemaico")],
 "Epoca romana e bizantina": [W("Egitto (provincia romana)", "Egitto romano")], "Epoca islamica": [W("Storia dell'Egitto arabo")],
 "Egitto moderno": [W("Storia dell'Egitto moderno"), W("Mehmet Ali", "Muhammad Ali")],
 "Zoser": [W("Djoser", "Zoser")], "Snefru": [W("Snefru")], "Cheope, Chefren, Micerino": [W("Cheope"), W("Chefren"), W("Micerino")],
 "Hatshepsut": [W("Hatshepsut")], "Amenhotep III": [W("Amenofi III", "Amenhotep III")], "Tutankhamon": [W("Tutankhamon")],
 "Seti I": [W("Seti I")], "Ramses II": [W("Ramses II")],
 "Ra": [W("Ra")], "Amon": [W("Amon")], "Osiride": [W("Osiride")], "Iside": [W("Iside")], "Horus": [W("Horus")], "Hathor": [W("Hathor")],
 "Nut": [W("Nut (mitologia)", "Nut")], "Ptah": [W("Ptah")], "Sobek": [W("Sobek")], "Seshat": [W("Seshat")],
 "I punti cardinali": [W("Piramidi egizie"), W("Archeoastronomia")],
 "Le stelle imperiture": [W("Astro circumpolare", "Stelle circumpolari"), W("Testi delle piramidi")],
 "Sirio e il calendario": [W("Sirio"), W("Levata eliaca"), W("Calendario egizio")],
 "I decani e le 24 ore": [W("Astronomia egizia")],
 "Gli allineamenti solari": [W("Complesso templare di Karnak", "Karnak"), W("Abu Simbel")],
 "Mastaba": [W("Mastaba")], "Pilone": [W("Pilone (architettura egizia)", "Pilone")], "Sala ipostila": [W("Ipostilo", "Sala ipostila")],
 "Obelisco": [W("Obelisco")], "Cartiglio": [W("Cartiglio (Antico Egitto)", "Cartiglio")], "Nilometro": [W("Nilometro")],
 "Levata eliaca": [W("Levata eliaca")], "Feluca": [W("Feluca (imbarcazione)", "Feluca")],
}
# linea del tempo grafica: nome del periodo -> (anno di inizio, anno di fine, foto in img/, colore, giorni in cui lo si incontra)
# anni negativi = avanti Cristo; le foto sono quelle già usate nelle giornate
TEMPO_GRAFICO = {
 "Unificazione": (-3100, -2686, "g4-memphis", "#7A4B2A", [4]),
 "Antico Regno": (-2686, -2181, "g3-chefren", "#A8771A", [3, 4]),
 "Medio Regno": (-2055, -1650, "g11-qarun", "#2F6B3F", [5, 11]),
 "Nuovo Regno": (-1550, -1069, "g10-maggiore", "#9A3B1E", [5, 7, 10]),
 "Epoca tolemaica": (-332, -30, "g8-edfu", "#4D6A2A", [8, 9]),
 "Epoca romana e bizantina": (-30, 641, "g9-philae", "#1B5E7A", [7, 9]),
 "Epoca islamica": (641, 1805, "g2-cittadella", "#1F6B55", [2]),
 "Egitto moderno": (1805, 2027, "g9-diga", "#1F3A6E", [2, 9]),
}
INFO = {
 "notti": [("28–31 luglio", "4 notti", "Il Cairo, hotel in centro"), ("1–5 agosto", "5 notti", "Nave MS Royal Ruby II; le prime due ferma a Luxor"),
           ("6 agosto", "1 notte", "Il Cairo, dopo Abu Simbel"), ("7 agosto", "1 notte", "El Fayoum"), ("8 agosto", "1 notte", "El Fayoum o Il Cairo: da confermare"), ("9 agosto", "forse in volo", "Rientro: arrivo in Italia il 9 sera o il 10, secondo gli orari")],
 "compreso": ["Voli dall'Italia, solo bagaglio a mano", "Tasse aeroportuali", "Voli interni Cairo–Luxor e Assuan–Cairo", "Visto all'arrivo",
              "Tutti i trasferimenti con mezzo privato climatizzato", "Ingressi ai siti dell'itinerario", "Coordinatore dall'Italia",
              "Egittologo in italiano", "Pensione completa in nave", "Mezza pensione al Cairo e a El Fayoum, tranne la notte del 6 agosto", "Polizze sanitaria, bagaglio e annullamento"],
 "escluso": ["Bevande e pasti non citati", "Ingresso all'interno della Grande Piramide", "Mance: 10 € a persona al giorno, 110 € in totale"],
 "aperti": ["Da dove si osserva l'eclissi: nave, riva o altro", "Dove si dorme la notte dell'8 agosto", "Compagnia aerea, aeroporto e orari",
            "Nomi degli hotel", "Quali tombe della Valle dei Re sono comprese", "Costo dell'eventuale bagaglio in stiva"],
}


# ------------------------------------------------------------ Outfit (consigli raccolti su ChatGPT, 9 ottobre 2026)
# L'app è condivisa con i compagni di viaggio: niente nomi propri, solo «Donna» e «Uomo».
OUTFIT = {
 "intro": "Una valigia essenziale: capi leggeri, traspiranti, lavabili e abbinabili fra loro. Conta più la protezione dal sole che la quantità di vestiti.",
 "regole": [
  ("Guardaroba da 7–8 giorni", "Da riusare nelle due settimane, con un piccolo bucato a metà viaggio. Non quattordici cambi completi."),
  ("Solo bagaglio a mano", "Un trolley da cabina e uno zaino a testa, niente bagaglio in stiva. Peso e dimensioni ammessi dipendono dalla compagnia, anche sui voli interni: conviene restare 1–2 kg sotto il limite, che può comprendere il peso del trolley."),
  ("Moschee", "Capi che coprano spalle e ginocchia."),
  ("Siti e deserto", "Pantaloni leggeri, maniche lunghe ariose e scarpe chiuse servono più di canottiere e pantaloncini."),
 ],
 # massima media di agosto, minima media, record di agosto (tabelle climatiche di Wikipedia in inglese, lette il 9 ottobre 2026)
 "clima": [("Il Cairo", "34,9 °C", "Minima media 24,3 °C. Record di agosto 43,4 °C."),
           ("El Fayoum", "38,6 °C", "Minima media 25,1 °C."),
           ("Luxor", "41,2 °C", "Minima media 25,6 °C. Record di agosto 47,0 °C."),
           ("Assuan", "41,9 °C", "Minima media 27,9 °C. Record di agosto 48,6 °C."),
           ("Abu Simbel", "40,2 °C", "Minima media 25,7 °C. Valore da modello climatico, non da stazione.")],
 "clima_nota": "Massime medie di agosto sul trentennio 1991–2020: sono medie, non previsioni, e nelle ondate di caldo si sale di parecchi gradi. Il tratto più duro è fra l'1 e il 6 agosto: Karnak, Luxor, Valle dei Re, Edfu, Kom Ombo, Assuan e Abu Simbel.",
 "caldo": [
  "Abituarsi per gradi a camminare col caldo estivo, senza simulare condizioni estreme.",
  "Bere con regolarità, senza aspettare la sete: col caldo secco il sudore evapora subito e non ci si accorge di quanta acqua si perde.",
  "Cappello, occhiali UV e crema SPF 50+, da riapplicare.",
  "Ombra e pause al fresco nelle ore centrali, per quanto lo permette il programma.",
  "Pasti leggeri e regolari, senza trascurare i sali.",
 ],
 "palette": [("Donna", "Avorio, sabbia, salvia e azzurro polvere. Abiti e pantaloni fluidi, camicie leggere."),
             ("Uomo", "Sabbia, pietra, verde oliva e blu navy. Pantaloni tecnici, camicie e polo leggere.")],
 "palette_nota": "Con questi colori tutti i capi si abbinano, e rendono bene anche nelle foto fra templi, pietra dorata e deserto.",
 "priorita": [("Donna", "Due ottime camicie leggere a maniche lunghe, un pantalone tecnico traspirante, un cappello davvero protettivo e scarpe già rodate."),
              ("Uomo", "Due pantaloni tecnici davvero leggeri, due camicie a maniche lunghe protettive e un buon cappello.")],
 # come vestirsi per situazione: (titolo, indicazioni, [nomi delle foto in img/outfit-*.jpg])
 "situazioni": [
  ("Fra i templi, in pieno sole", "È la situazione di quasi tutti i giorni. Camicia o maglia a maniche lunghe, chiara e leggera (meglio se UPF 50+), pantaloni lunghi tecnici o di lino, cappello a tesa larga, occhiali da sole e scarpe chiuse con suola aderente. Niente cotone pesante.", ["s03", "s05", "s10"]),
  ("In moschea e in città", "Spalle e ginocchia coperte per entrambi, quindi niente bermuda e canottiere; per le donne un foulard per i capelli. Scarpe facili da sfilare all'ingresso.", ["s02", "s09"]),
  ("Nel deserto", "Pantaloni tecnici lunghi, camicia protettiva, scarpe da camminata con suola scolpita, cappello ben fissato e foulard antipolvere. Tessuti che non trattengono la sabbia. Niente bermuda, abiti svolazzanti, sandali o infradito.", ["s04", "s11", "s12", "i-0708"]),
  ("In nave e la sera", "Camicia di lino o polo con un pantalone pulito; nelle ore di riposo bermuda e sandali comodi. Per le donne abito lungo leggero o pantalone morbido con blusa. Niente abiti da sera impegnativi.", ["s08", "i-0406"]),
  ("In volo e nei trasferimenti", "Capi comodi che non stringono e non si sgualciscono, le scarpe chiuse ai piedi per risparmiare spazio e uno strato leggero a portata di mano per l'aria condizionata di aerei, bus e musei.", ["s01"]),
  ("Il giorno dell'eclissi", "Il completo più protettivo che avete: si può restare fermi a lungo all'aperto con il Sole a picco. Nello zaino gli occhiali certificati e un piccolo asciugamano tecnico.", ["s06"]),
 ],
 # liste con le spunte: (identificativo, titolo, [(gruppo, [voci])])
 "liste": [
  ("donna", "La valigia, donna", [
   ("Nel trolley", ["3 magliette tecniche leggere e traspiranti", "2 camicie ampie a manica lunga, in lino leggero o tessuto tecnico",
                    "1 blusa o maglietta a manica corta, più curata per la sera", "2 pantaloni lunghi leggeri, di cui almeno uno tecnico",
                    "1 pantalone morbido o gonna midi per crociera e cene", "1 abito leggero midi o maxi, per città e sera", "1 costume da bagno",
                    "7 cambi di intimo, con un reggiseno sportivo", "4 paia di calze tecniche leggere", "1 pigiama estivo leggerissimo",
                    "1 cardigan o felpa ultraleggera per l'aria condizionata"]),
   ("Indosso in viaggio", ["1 pantalone lungo comodo e leggero", "1 maglietta traspirante", "Scarpe da camminata chiuse, già collaudate", "1 paio di calze", "1 strato leggero per l'aereo"]),
   ("Scarpe e sole", ["Sandali comodi con suola stabile e cinturino posteriore", "Cappello a tesa larga, meglio con protezione per il collo",
                      "Foulard grande e leggero per moschee, polvere e sole", "Occhiali da sole UV400", "Burrocacao con protezione solare"]),
  ]),
  # stessa struttura e stesse quantità della lista donna, con i capi equivalenti
  ("uomo", "La valigia, uomo", [
   ("Nel trolley", ["3 magliette tecniche leggere e traspiranti", "2 camicie a manica lunga, in lino leggero o tessuto tecnico",
                    "1 polo o camicia a manica corta, più curata per la sera", "2 pantaloni lunghi leggeri, di cui almeno uno tecnico",
                    "1 pantalone chino leggero per crociera e cene", "1 bermuda per la nave e i momenti informali", "1 costume da bagno",
                    "7 cambi di intimo tecnico, ad asciugatura rapida", "4 paia di calze tecniche leggere", "1 pigiama estivo leggerissimo",
                    "1 felpa ultraleggera o camicia più consistente per l'aria condizionata"]),
   ("Indosso in viaggio", ["1 pantalone lungo comodo e leggero", "1 maglietta traspirante", "Scarpe da camminata chiuse, già collaudate", "1 paio di calze", "1 strato leggero per l'aereo"]),
   ("Scarpe e sole", ["Sandali comodi con suola stabile e cinturino posteriore", "Cappello a tesa larga, meglio con protezione per il collo",
                      "Foulard o scaldacollo leggero per polvere e sole", "Occhiali da sole UV400", "Burrocacao con protezione solare"]),
  ]),
  ("comune", "In comune, da dividere con chi viaggia con te", [
   ("Igiene e salute", ["Spazzolino, dentifricio, deodorante e detergenti in formato viaggio", "Crema solare SPF 50+ per viso e corpo", "Repellente per insetti",
                        "Gel igienizzante e fazzoletti", "Salviette umidificate e una piccola scorta di carta igienica", "Cerotti normali e per vesciche",
                        "Farmaci personali nella confezione originale", "Kit sanitario concordato con medico o farmacista", "Bustine di sali reidratanti",
                        "Detersivo in fogli o sapone per i piccoli bucati"]),
   ("Nello zaino", ["Passaporto, documenti di viaggio, assicurazione e copie offline", "Telefono, cavi, adattatore universale e caricatore",
                    "Power bank conforme alle regole della compagnia aerea", "Borraccia leggera, da riempire solo con acqua sicura",
                    "Ventaglio pieghevole o piccolo ventilatore ricaricabile", "Asciugamano tecnico per il sudore", "Sacchetti per i panni sporchi e organizer comprimibili",
                    "Custodia antipolvere per telefono e dispositivi", "Occhiali certificati ISO 12312-2 per l'eclissi", "Filtro solare certificato per binocolo o fotocamera, solo se serve"]),
  ]),
 ],
 "evitare": ["Jeans pesanti", "Scarpe nuove da inaugurare in Egitto", "Grandi confezioni di cosmetici", "Un secondo paio di scarpe sportive"],
 "zaino": "Nello zaino personale, mai nel trolley: documenti, medicinali essenziali, occhiali per l'eclissi, elettronica e un cambio minimo.",
 "fonte": "Consigli e immagini raccolti su ChatGPT il 9 ottobre 2026. Temperature: normali climatiche 1991–2020 (NOAA e servizio meteorologico egiziano) dalle tabelle di Wikipedia; Abu Simbel da Climate-Data.org. Liquidi in cabina: i limiti dipendono da aeroporti e compagnia.",
}


# ------------------------------------------------------------ esportazione
def esporta_giorno(g, crediti):
    righe = []
    for r in g["righe"]:
        if r[0] == "e":
            righe.append({"k": "e", "anno": r[1], "piccolo": r[2], "testo": r[3]})
            continue
        t = r[1]
        d = {"k": "t", "anno": t["anno"], "piccolo": t["piccolo"], "titolo": t["titolo"], "quando": t["quando"], "breve": t["breve"],
             "guarda": t["guarda"], "cielo": t["cielo"], "numero": t["numero"], "wiki": list(t["wiki"]),
             "grafico": t["grafico"]() if t["grafico"] else None, "nota": None, "foto": None}
        if t["nota"]:
            d["nota"] = {"t": t["nota"][0], "x": t["nota"][1], "img": None}
            if len(t["nota"]) > 2 and copia(t["nota"][2], crediti, g["n"], t["titolo"]):
                d["nota"]["img"] = "img/" + t["nota"][2] + ".jpg"
        if t["foto"] and copia(t["foto"][0], crediti, g["n"], t["titolo"]):
            d["foto"] = {"src": "img/" + t["foto"][0] + ".jpg", "alt": t["foto"][1], "did": t["foto"][2]}
        if t["titolo"] in COORD:
            d["coord"] = list(COORD[t["titolo"]])
            d["indicativa"] = t["titolo"] in INDICATIVE
        righe.append(d)
    return {"n": g["n"], "data": g["data"], "titolo": g["titolo"], "filo": g["filo"], "pal": g["pal"],
            "profilo": g["profilo"]() if g.get("profilo") else None, "righe": righe, "chiusura": g["chiusura"]}


def copia(slug, crediti, n, titolo):
    src = os.path.join(INFO_DIR, "foto", slug + ".jpg")
    if not os.path.exists(src):
        return False
    shutil.copyfile(src, os.path.join(SITO, "img", slug + ".jpg"))
    if slug in G.FOTO:
        file, autore, licenza = G.FOTO[slug]
    else:
        autore, licenza = FOTO_G2[slug]
    crediti.append({"giorno": n, "tappa": titolo, "autore": autore, "licenza": licenza})
    return True


def basi_con_wiki():
    """Aggiunge in coda a ogni voce delle Basi l'elenco dei link a Wikipedia; segnala le voci senza link."""
    out = {}
    for sezione, voci in BASI.items():
        out[sezione] = []
        for v in voci:
            assert v[0] in BASI_WIKI, "manca il link Wikipedia per: " + v[0]
            if sezione == "tempo":
                da, a, img, colore, giorni = TEMPO_GRAFICO[v[0]]
                out[sezione].append({"nome": v[0], "date": v[1], "testo": v[2], "dove": v[3], "da": da, "a": a, "img": "img/" + img + ".jpg",
                                     "colore": colore, "giorni": giorni, "wiki": ", ".join(BASI_WIKI[v[0]])})
            else:
                out[sezione].append(list(v) + [", ".join(BASI_WIKI[v[0]])])
    return out


def js(nome, valore):
    return f"const {nome} = " + json.dumps(valore, ensure_ascii=False, indent=1) + ";\n"


def main():
    for d in ("css", "data", "img"):
        os.makedirs(os.path.join(SITO, d), exist_ok=True)
    crediti = []
    # panoramica del viaggio: la locandina fatta da Stefano, ridotta per il telefono
    pan = os.path.join(os.path.dirname(SITO), "Egitto 2027_ Sotto il Sole Nero_corretta.png")
    if os.path.exists(pan):
        subprocess.run(["sips", "-Z", "1800", "-s", "format", "jpeg", "-s", "formatOptions", "78", pan,
                        "--out", os.path.join(SITO, "img", "panoramica.jpg")], check=True, capture_output=True)
    # immagini degli outfit: ritagliate una volta dalle schermate di ChatGPT e tenute in img/outfit-*.jpg
    OUTFIT["foto"] = sorted(f[len("outfit-"):-4] for f in os.listdir(os.path.join(SITO, "img")) if f.startswith("outfit-"))
    giorni = [esporta_giorno(g, crediti) for g in [GIORNO_1, GIORNO_2] + G.GIORNI + [GIORNO_13]]
    open(os.path.join(SITO, "data", "giorni.js"), "w", encoding="utf-8").write(js("PAL_BASE", G.SABBIA) + js("GIORNI", giorni))
    open(os.path.join(SITO, "data", "extra.js"), "w", encoding="utf-8").write(js("BASI", basi_con_wiki()) + js("INFO", INFO) + js("OUTFIT", OUTFIT) + js("CREDITI", crediti))
    open(os.path.join(SITO, "css", "giorno.css"), "w", encoding="utf-8").write(
        "/* Generato da tools/costruisci.py a partire da infografiche/genera.py: non modificare a mano. */\n" + G.CSS % G.SABBIA)
    file = ["./", "index.html", "manifest.json", "icona-180.png", "css/giorno.css", "css/app.css", "js/app.js", "js/mappa.js",
            "data/giorni.js", "data/extra.js", "data/schede.js"] + sorted("img/" + f for f in os.listdir(os.path.join(SITO, "img")) if f.endswith(".jpg"))
    sw = open(os.path.join(SITO, "tools", "sw.modello.js"), encoding="utf-8").read()
    sw = sw.replace("__VERSIONE__", time.strftime("%Y%m%d-%H%M%S")).replace("__FILE__", json.dumps(file, ensure_ascii=False))
    open(os.path.join(SITO, "sw.js"), "w", encoding="utf-8").write(sw)
    print(len(giorni), "giorni,", len(crediti), "foto,", len(file), "file in cache offline")


if __name__ == "__main__":
    main()
