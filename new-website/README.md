# new-website

Sito personale di Leonard Vincent Ramil costruito con [Hugo Blox](https://hugoblox.com) (template *Academic CV*, lo stesso della cartella `epalu.github.io-main`) ma con la home impostata come quella di `riccardocadei.github.io-master`: icone social a sinistra nella barra di navigazione, avatar tondo con nome e tagline, foto di copertina, bio in corsivo, "Selected News" e pubblicazioni selezionate.

Il "gioco di sfondi" del template epalu è mantenuto: hero scuro con `Meteor.svg`, sezione bianca, sezione grigia, sezione bianca, chiusura scura con `stacked-peaks.svg`. Tutto è responsive (telefono e desktop) e supporta la modalità chiara/scura.

## Come lanciarlo in locale

Servono [Hugo extended 0.126.3](https://github.com/gohugoio/hugo/releases/tag/v0.126.3) e Go (i temi vengono scaricati come Hugo Modules).

```bash
cd new-website
hugo server
```

## Dove modificare i contenuti

| Cosa | File |
|---|---|
| Nome, tagline, affiliazioni, link social, bio | `content/authors/admin/_index.md` |
| Foto profilo | `content/authors/admin/avatar.jpg` (ora l'avatar GitHub) |
| Foto di copertina | `assets/media/cover.svg` (segnaposto generato: sostituiscilo con una tua foto, es. `cover.jpg`, e aggiorna `content/_index.md`) |
| Sezioni della home (ordine, sfondi, testi) | `content/_index.md` |
| News (una per file) | `content/news/*.md` |
| Progetti | `content/project/*/index.md` |
| Pagina CV | `content/cv/index.md` (per un PDF: mettilo in `static/uploads/` e punta il pulsante dell'hero in `content/_index.md`) |
| Menu | `config/_default/menus.yaml` |
| Logo nella navbar | `assets/media/icon.jpg` |
| Colore accento, footer, logo | `config/_default/params.yaml` |
| Titolo e URL del sito | `config/_default/hugo.yaml` |

## Blocchi custom

I tre blocchi che riproducono il layout di riccardocadei stanno in `layouts/partials/blox/`:

- `profile-hero.html`: avatar + nome + tagline + icone social + pulsante CV.
- `cover-bio.html`: foto di copertina + bio in corsivo (prende il testo dalla pagina autore).
- `news-list.html`: elenco news con badge della data.

La barra di navigazione con le icone social a sinistra è in `layouts/partials/components/headers/navbar.html`. Gli stili di tutti questi elementi (incluse le regole per mobile) sono in `assets/css/custom.css`.

## Deploy

Il workflow `.github/workflows/publish.yaml` pubblica su GitHub Pages a ogni push su `main`; `netlify.toml` permette in alternativa il deploy su Netlify. Se il sito vive in una propria repo, spostare il contenuto di questa cartella nella root della repo.

## Dati da verificare

I contenuti sono stati compilati dal profilo GitHub pubblico (LinkedIn non era raggiungibile). Da controllare in particolare: le date delle news, l'anno di inizio del Master a EURECOM, le lingue nel CV, e la sezione Pubblicazioni (rimossa perché non ce ne sono: per riattivarla basta ricreare `content/publication/` e aggiungere il blocco `collection` con `view: citation` in `content/_index.md`).
