# mini-me: pipeline di modifica

Script Python (OpenCV/NumPy/SciPy) che ha prodotto l'attuale `assets/media/mini-me.png`
a partire dal render originale del surfer:

- tavola: stampa "tribal" stile Catch Surf (teal, rosa, viola, nero, panna) proiettata in
  prospettiva sul deck con omografia, mantenendo le ombre del render (`pattern.py` disegna la texture);
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
Le coordinate (poligono tavola, collo, polsi, caviglie, pantaloncino) sono in pixel dell'immagine 1086x1448.
