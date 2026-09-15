# mini-me: pipeline di modifica

Script Python (OpenCV/NumPy/SciPy) che ha prodotto l'attuale `assets/media/mini-me.png`
a partire dal render originale del surfer:

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
