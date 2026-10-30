#!/usr/bin/env python3
"""Compone le pagine del sito da sorgenti/: testata, piede e icone sono scritti
una volta sola qui, il contenuto di ogni pagina sta in sorgenti/pagine/ e i
blocchi che ricorrono in più pagine in sorgenti/pezzi/, richiamati con {pezzo:nome}.

Uso, dalla cartella del sito:  python3 componi.py
Le pagine composte (index.html e <pagina>/index.html) si versionano: GitHub
Pages le serve così come sono, senza nessuna costruzione dalla sua parte.
Solo libreria standard.
"""
import pathlib
import re

RADICE = pathlib.Path(__file__).resolve().parent
PAGINE = RADICE / "sorgenti" / "pagine"
PEZZI = RADICE / "sorgenti" / "pezzi"

PIATTAFORMA = "https://formazione.arsdocendi.it/login/"
PRIVACY = "https://formazione.arsdocendi.it/admin/tool/policy/viewall.php"
EMAIL = "formazione@arsdocendi.it"
CONTATTI = "https://formazione.arsdocendi.it/user/contactsitesupport.php"

MENU = [
    ("", "Home"),
    ("servizi/", "Servizi"),
    ("come-lavoriamo/", "Come lavoriamo"),
    ("per-chi/", "Per chi"),
    ("referenze/", "Referenze"),
    ("chi-siamo/", "Chi siamo"),
]

# Icone disegnate a tratto su griglia 24x24, usate con <use href="#i-nome">.
ICONE = {
    "spunta-cerchio": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>',
    "spunta": '<path d="M5 12.5 9.5 17 19 7"/>',
    "freccia": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "accedi": '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4M10 16l4-4-4-4M14 12H4"/>',
    "progetto": '<path d="M4 20l4-1L19 8a2.1 2.1 0 0 0-3-3L5 16l-1 4z"/><path d="M14 7l3 3"/>',
    "schermo": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
    "edificio": '<path d="M3 21h18M5 21V10M19 21V10M9 21V10M15 21V10M2 10l10-6 10 6z"/>',
    "attestato": '<circle cx="12" cy="9" r="5"/><path d="m9 13.5-1.5 7.5L12 19l4.5 2-1.5-7.5"/>',
    "scuola": '<path d="M3 21h18M5 21V11l7-5 7 5v10M10 21v-5h4v5M12 6V3h3"/>',
    "rete": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5 5.8 16.8M12 11.5l6.2 5.3"/>',
    "istituzione": '<path d="M3 21h18M4 17h16M6 17v-6M10 17v-6M14 17v-6M18 17v-6M3 11h18L12 4z"/>',
    "posta": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m3.5 6 8.5 7 8.5-7"/>',
    "luogo": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}


def icone_svg():
    simboli = "".join(
        f'<symbol id="i-{n}" viewBox="0 0 24 24">{p}</symbol>' for n, p in ICONE.items()
    )
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{simboli}</svg>'


def corrente(p, attuale):
    return ' aria-current="page"' if p == attuale else ""


def testata(su, attuale):
    voci = "".join(f'<a href="{(su + p) or './'}"{corrente(p, attuale)}>{t}</a>' for p, t in MENU)
    return f"""<a class="salta" href="#contenuto">Vai al contenuto</a>
<header class="testata">
  <div class="contenitore testata__riga">
    <a class="testata__logo" href="{su or './'}"><img src="{su}assets/loghi/arsdocendi-orizzontale.svg" alt="Ars Docendi, formazione per la scuola" width="171" height="48"></a>
    <nav class="menu" aria-label="Principale">{voci}</nav>
    <div class="testata__azioni">
      <button class="pulsante-menu" type="button" aria-expanded="false" aria-controls="menu-mobile" aria-label="Menu"><svg class="icona"><use href="#i-menu"/></svg></button>
      <a class="pulsante pulsante--fantasma" href="{PIATTAFORMA}"><svg class="icona"><use href="#i-accedi"/></svg>Accedi</a>
      <a class="pulsante pulsante--primario" href="{su}contatti/">Richiedi una consulenza</a>
    </div>
  </div>
  <nav class="menu-mobile" id="menu-mobile" aria-label="Principale, schermo stretto">{voci}<a href="{su}contatti/"{corrente("contatti/", attuale)}>Contatti</a></nav>
</header>"""


def invito(su):
    return f"""<section class="invito">
  <div class="contenitore">
    <div>
      <h2>Stai preparando il piano di formazione?</h2>
      <p>Raccontaci di cosa ha bisogno la tua scuola: ne parliamo con un referente, anche online.</p>
    </div>
    <a class="pulsante pulsante--primario pulsante--grande" href="{su}contatti/">Richiedi una consulenza<svg class="icona"><use href="#i-freccia"/></svg></a>
  </div>
</section>"""


def piede(su):
    return f"""<footer class="piede">
  <div class="contenitore">
    <div class="piede__griglia">
      <div>
        <img class="piede__logo" src="{su}assets/loghi/arsdocendi-chiaro-solo-nome.svg" alt="Ars Docendi" width="156" height="44">
        <p class="piede__testo">Ente accreditato MIUR per la formazione del personale scolastico.</p>
      </div>
      <div>
        <h2>Ars Docendi</h2>
        <ul>
          <li><a href="{su}servizi/">Servizi</a></li>
          <li><a href="{su}come-lavoriamo/">Come lavoriamo</a></li>
          <li><a href="{su}referenze/">Referenze</a></li>
          <li><a href="{su}chi-siamo/">Chi siamo</a></li>
        </ul>
      </div>
      <div>
        <h2>Piattaforma</h2>
        <ul>
          <li><a href="{PIATTAFORMA}">Accedi ai corsi</a></li>
          <li><a href="{su}contatti/">Contatti</a></li>
        </ul>
      </div>
      <div>
        <h2>Informazioni</h2>
        <ul>
          <li><a href="{PRIVACY}">Privacy e cookie</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <p class="piede__fondo">© 2026 Ars Docendi · Life Training S.r.l. · Piazza Impastato 3, 87100 Cosenza · P. IVA e C.F. 03611680780</p>
  </div>
</footer>"""


def componi(sorgente):
    testo = sorgente.read_text(encoding="utf-8")
    meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", testo.split("\n\n", 1)[0]))
    corpo = re.sub(r"\A(?:<!--.*?-->\s*)+", "", testo, flags=re.S)
    percorso = meta["percorso"]
    # La 404 si serve a qualunque profondità: lì i percorsi partono dalla radice.
    su = "/" if sorgente.stem == "404" else "../" * percorso.count("/")
    # I blocchi comuni a più pagine (numeri, clienti, servizi, fasi) stanno una volta sola in sorgenti/pezzi/.
    corpo = re.sub(r"\{pezzo:([\w-]+)\}", lambda m: (PEZZI / f"{m[1]}.html").read_text(encoding="utf-8").strip(), corpo)
    corpo = corpo.replace("{su}", su).replace("{piattaforma}", PIATTAFORMA).replace("{email}", EMAIL).replace("{contatti}", CONTATTI)
    titolo = meta["titolo"]
    pagina = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{meta['descrizione']}">
<link rel="icon" href="{su}assets/loghi/arsdocendi-sigillo.svg" type="image/svg+xml">
<link rel="preload" href="{su}assets/fonts/SourceSerif4-Semibold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{su}assets/fonts/AtkinsonHyperlegibleNext-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{su}assets/sito.css">
<script src="{su}assets/sito.js" defer></script>
</head>
<body>
{icone_svg()}
{testata(su, percorso)}
<main id="contenuto">
{corpo.strip()}
</main>
{invito(su) if meta.get("invito", "si") == "si" else ""}
{piede(su)}
</body>
</html>
"""
    uscita = RADICE / percorso / "index.html" if percorso else RADICE / "index.html"
    if sorgente.stem == "404":
        uscita = RADICE / "404.html"
    uscita.parent.mkdir(parents=True, exist_ok=True)
    uscita.write_text(pagina, encoding="utf-8")
    return uscita


if __name__ == "__main__":
    fatte = [componi(s) for s in sorted(PAGINE.glob("*.html"))]
    for f in fatte:
        print(f.relative_to(RADICE))
    print(f"pagine composte: {len(fatte)}")
