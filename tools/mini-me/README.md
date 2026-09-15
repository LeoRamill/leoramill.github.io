# mini-me: script di ritocco

Due script, uno per render. Ogni volta che `assets/media/mini-me.png` viene rigenerato da zero
le coordinate vanno rimisurate, perche' sono in pixel dell'immagine.

## headscale.py - render attuale (surfista con occhiali, muta blu/arancio)

Rimette in proporzione testa e corpo e ripristina lo sfondo trasparente:

- la testa passava per 2,6 teste di figura, un rapporto da bobblehead; ridotta del 30% arriva
  a 3,2 teste, in linea con la versione precedente del mini-me;
- la riduzione e' una deformazione morbida ancorata al mento appoggiato sul collo della muta:
  dentro la maschera della testa la scala e' piena, fuori e' identita', e la fascia di
  transizione cade sullo sfondo e sulle spalle. Non restano buchi da riempire;
- lo sfondo bianco torna trasparente. Le sacche chiuse dentro la figura (i vuoti fra i ciuffi
  di capelli, quello fra le gambe) non si raggiungono dai bordi: si riconoscono perche' la carta
  e' piatta e neutra, mentre schiuma dell'onda e bianco della tavola sono superfici illuminate
  con escursione locale ~15 e dominante blu. I bordi sfumati vengono smontati dal bianco, cosi'
  non resta alone su fondo scuro.

```bash
python3 -m venv .venv && .venv/bin/pip install numpy opencv-python-headless scipy
git show cd4730d:assets/media/mini-me.png > /tmp/mini-me-src.png
.venv/bin/python tools/mini-me/headscale.py /tmp/mini-me-src.png assets/media/mini-me.png --scale 0.70
```

`--scale` regola quanto rimpicciolire la testa (0,70 = attuale; 0,80 e' piu' conservativo).
`--keep-white` salta il ritaglio dello sfondo. Le coordinate della testa sono `HEAD_POLY` e
`PIVOT` in cima allo script.

## edit.py - render precedente (ragazzo in costume, poi muta arancio e glacier)

Ha prodotto la versione del mini-me in uso fino al commit "change photo", a partire dal
render originale del surfer. Non si applica al render attuale, resta come storia:

- tavola (modello 3D): la sezione trasversale e' un deck bombato chiuso da un rail a quarto di cerchio,
  piu' largo sul lato vicino e ridotto a una lama su quello lontano per la prospettiva. La stampa "tribal"
  stile Catch Surf (`pattern.py`) e' mappata per lunghezza d'arco, quindi si comprime sul rail, e si ferma
  prima del bordo lasciando il rail bianco come nella tavola di riferimento. Sotto il profilo inferiore
  viene dipinta la parete laterale che da' spessore al volume, con luce diffusa, riflesso speculare lungo
  il rail, rimbalzo dell'acqua sul fondo, ombra delle gambe sul deck e ombra di contatto sull'onda;
- muta: corpo e gambe arancio, maniche e pantaloncino glacier, cuciture scure a collo, polsi,
  caviglie e spalle (recolor via gradient map sulla luminanza della pelle);
- proporzioni: testa ridotta del 13% e mano sinistra del 14% (warp "pinch" ancorato a collo e polso);
- pulizia: due sacche bianche opache rimaste dal vecchio flood-fill (sotto il braccio destro e tra
  le gambe) rese trasparenti, defringe dei bordi semitrasparenti.

L'input deve essere il render ORIGINALE, non il file già modificato:

```bash
python3 -m venv .venv && .venv/bin/pip install pillow numpy opencv-python-headless scipy
git show d196639:assets/media/mini-me.png > /tmp/mini-me-original.png
.venv/bin/python tools/mini-me/edit.py /tmp/mini-me-original.png assets/media/mini-me.png --debug
```

Colori della muta: liste `ORANGE` / `GLACIER` in `edit.py`; palette della tavola in cima a `pattern.py`.
Geometria della tavola in `edit.py`: `Rr` (raggio del rail, vicino/lontano), `crown` (bombatura del deck),
`thick` (spessore della parete laterale), `Lv`/`Vv` (direzioni di luce e vista).
`--debug` scrive anche le maschere; `BDEBUG=1` salva le mappe di `q`, luce, riflesso e ombre.
Le coordinate (poligono tavola, collo, polsi, caviglie, pantaloncino) sono in pixel dell'immagine 1086x1448.
