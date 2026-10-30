# arsdocendi.it — sito pubblico

Sito statico servito da GitHub Pages sul dominio `arsdocendi.it` (decisione D215 nel repository `arsdocendi`).

## Come si modifica

1. Si cambia il contenuto in `sorgenti/pagine/` (una pagina per file; in testa, nei commenti, percorso, titolo e descrizione). Testata, piede, menu, icone e indirizzi comuni stanno in `componi.py`.
2. Si compongono le pagine: `python3 componi.py`. Lo script deve dire `pagine composte: 8`.
3. Anteprima: `python3 -m http.server 8080`, poi `http://localhost:8080`.
4. Commit e push su `main`: GitHub Pages pubblica da solo in un paio di minuti.

Le pagine composte (`index.html`, `*/index.html`, `404.html`) si versionano: GitHub non costruisce niente.

## Regole

- Nessun servizio esterno: niente Google Fonts, CDN, statistiche o moduli che inviano dati. Il sito non usa cookie.
- Colori e caratteri vengono dal brand (`assets/sito.css`); caratteri e loghi sono copie di quelli del repository `arsdocendi`.
- I numeri della home si rileggono con `scripts/conta-numeri-sito.php` del repository `arsdocendi`: niente numeri a occhio.
