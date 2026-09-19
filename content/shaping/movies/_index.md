---
title: "Movies & Series"
layout: shaping-gallery
# Every folder inside this one is a review page and gets this layout on its own
cascade:
  layout: shaping-review
lead:
  text: "Watch more movies. Live more lives by projecting yourself into a body and mind other than your own."
  url: ""

galleries:
  - title: Movies
    kind: movie
    label: Movie
    items:
      # `page:` takes everything from the folder of the same name: title, cover, rating and text
      - page: forrest-gump
      - page: foe

  - title: Series
    kind: series
    label: Series
    # Nothing listed here by name: every folder in this one whose `gallery` is `series` joins the
    # wall on its own, which is how Osmosis arrives.
    items: []

# Link shown after the first gallery (e.g. your Letterboxd list)
more:
  text: if you want more
  url: https://letterboxd.com/

---
