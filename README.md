# website

Sito personale di Leonard Vincent Ramil costruito con [Hugo Blox](https://hugoblox.com) (template *Academic CV*) con la home ispirata al sito di Riccardo Cadei: icone social a sinistra nella barra di navigazione, avatar tondo con nome e tagline, foto di copertina, bio in corsivo, "Selected News" e progetti selezionati.

Lo sfondo `Meteor.svg` è un unico strato fisso dietro tutta la pagina: le sezioni chiare lo coprono, quelle scure (hero e chiusura) sono tinte semitrasparenti che lo lasciano riaffiorare con intensità diverse mentre si scorre. Si configura nel blocco `profile-hero` di `content/_index.md` (`design.fixed_background`: `filename` in `assets/media/`, oppure `false` per disattivarlo); le tinte sono i `gradient_start`/`gradient_end` di ogni sezione scura. Tutto è responsive (telefono e desktop) e supporta la modalità chiara/scura.

## Come lanciarlo in locale

Servono [Hugo extended 0.126.3](https://github.com/gohugoio/hugo/releases/tag/v0.126.3) e Go (i temi vengono scaricati come Hugo Modules).

```bash
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

## Sezione "Shaping"

Pagina ispirata a faustozamparelli.com/shaping: un mini-me fluttuante circondato da quattro icone che portano alle sotto-pagine (libri, film, YouTube, Spotify) e la scritta "currently" che al passaggio del mouse diventa "old" e porta alla pagina degli studi.

| Cosa | File |
|---|---|
| Testi, icone-orbita e link della pagina principale | `content/shaping/_index.md` |
| Immagine del mini-me | metti `mini-me.png` (768×1365, sfondo trasparente) in `assets/media/`: sostituisce da solo il segnaposto `mini-me.svg` |
| Libri, film, video, canzoni (griglie di card) | `content/shaping/books.md`, `movies.md`, `videos.md`, `songs.md` (lista `galleries` → `items` con `title`, `meta`, `cover` URL, `url`, `note`) |
| Percorso di studi | `content/shaping/academic.md` (lista `stops`) |
| Layout e stili | `layouts/_default/shaping*.html`, sezione "Shaping" in `assets/css/custom.css` |

## Blocchi custom

I tre blocchi che riproducono quel layout stanno in `layouts/partials/blox/`:

- `profile-hero.html`: avatar + nome + tagline + icone social + pulsante CV.
- `cover-bio.html`: foto di copertina + bio in corsivo (prende il testo dalla pagina autore).
- `news-list.html`: elenco news con badge della data.

La barra di navigazione con le icone social a sinistra è in `layouts/partials/components/headers/navbar.html`. Gli stili di tutti questi elementi (incluse le regole per mobile) sono in `assets/css/custom.css`.

## Deploy

Il workflow `.github/workflows/publish.yaml` pubblica su GitHub Pages a ogni push su `main` (il sito sarà su `https://leoramill.github.io/website/`; in Settings → Pages la sorgente deve essere "GitHub Actions"). `netlify.toml` permette in alternativa il deploy su Netlify.

## Dati da verificare

I contenuti sono stati compilati dal profilo GitHub pubblico (LinkedIn non era raggiungibile). Da controllare in particolare: le date delle news, l'anno di inizio del Master a EURECOM, le lingue nel CV, e la sezione Pubblicazioni (rimossa perché non ce ne sono: per riattivarla basta ricreare `content/publication/` e aggiungere il blocco `collection` con `view: citation` in `content/_index.md`).
