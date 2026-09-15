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
      - title: The Social Network
        meta: David Fincher
      - title: La La Land
        meta: Damien Chazelle
      - title: Whiplash
        meta: Damien Chazelle
      - title: Parasite
        meta: Bong Joon Ho
      - title: Nightcrawler
        meta: Dan Gilroy
      - title: Prisoners
        meta: Denis Villeneuve
      - title: Beau Is Afraid
        meta: Ari Aster
      - title: Beautiful Boy
        meta: Felix van Groeningen
      - title: Joker
        meta: Todd Phillips
      - title: The Truman Show
        meta: Peter Weir
      - title: The Grand Budapest Hotel
        meta: Wes Anderson
      - title: The Imitation Game
        meta: Morten Tyldum
      - title: In the Mood for Love
        meta: Wong Kar-wai
      - title: No Country for Old Men
        meta: Joel Coen, Ethan Coen
  - title: TV Series
    kind: series
    label: TV Series
    items:
      - page: black-mirror
      - title: Big Little Lies
        meta: David E. Kelley
        rating: 9.8
      - title: Severance
        meta: Dan Erickson
      - title: Mr. Robot
        meta: Sam Esmail
      - title: Chernobyl
        meta: Craig Mazin
      - title: The Office
        meta: Greg Daniels
      - title: Silicon Valley
        meta: Mike Judge, John Altschuler, Dave Krinsky
      - title: Sherlock
        meta: Mark Gatiss, Steven Moffat
      - title: Death Note
        meta: Tsugumi Ohba, Takeshi Obata
---
