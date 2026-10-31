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
# I social, come nel footer della piattaforma (D218 del repository arsdocendi).
YOUTUBE = "https://www.youtube.com/@ArsDocendi_edu"
FACEBOOK = "https://www.facebook.com/profile.php?id=61596075901718"
# I due loghi come tracciati SVG nella pagina: il sito non carica niente da
# fuori. Tracciati di Simple Icons (CC0).
LOGO_YOUTUBE = "M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
LOGO_FACEBOOK = "M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"

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
    <div class="piede__social">
      <div>
        <p class="piede__social-titolo">Seguici su YouTube e Facebook</p>
        <p class="piede__social-testo">Video di notizie e guide sulla formazione.</p>
      </div>
      <div class="piede__social-pulsanti">
        <a class="piede__social-pulsante" href="{YOUTUBE}?sub_confirmation=1" target="_blank" rel="noopener"><svg class="piede__social-logo piede__social-logo--youtube" viewBox="0 0 24 24" aria-hidden="true"><path d="{LOGO_YOUTUBE}"/></svg>Iscriviti al canale</a>
        <a class="piede__social-pulsante" href="{FACEBOOK}" target="_blank" rel="noopener"><svg class="piede__social-logo piede__social-logo--facebook" viewBox="0 0 24 24" aria-hidden="true"><path d="{LOGO_FACEBOOK}"/></svg>Segui la pagina</a>
      </div>
    </div>
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
