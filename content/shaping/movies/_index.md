---
title: Movies
layout: shaping-gallery
# Every folder inside this one is a review page and gets this layout on its own
cascade:
  layout: shaping-review
lead:
  text: "Watch more movies. Live more lives."
  url: ""
# Link shown after the first gallery (e.g. your Letterboxd list)
more:
  text: if you want more
  url: https://letterboxd.com/
galleries:
  - title: ""
    kind: movie
    label: Movie
    items:
      # `page:` takes everything from the folder of the same name: title, cover, rating and text
      - page: interstellar
      - page: forrest-gump
      - page: foe

  - title: TV Series
    kind: series
    label: TV Series
    items:
      - page: black-mirror

---
