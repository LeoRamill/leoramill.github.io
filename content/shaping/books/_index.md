---
title: Books
layout: shaping-gallery
# Every folder inside this one is a review page and gets this layout on its own
cascade:
  layout: shaping-review
# Sentence under the title (optionally a link)
lead:
  text: "You forget the pages, but you keep the person they made."
  url: ""
hint: click on a cover to read the review
# Items with `rating` (out of 10), `catchphrase` or `review` open a modal on click; the others are static.
# `cover`: a full image URL, or a file name placed in `assets/media/shaping/` (e.g. atomic-habits.jpg).
galleries:
  - title: ""
    kind: book
    label: Book
    items:
      # `page:` takes everything from the folder of the same name: title, cover, rating and text
      - page: seven-habits
      - page: atomic-habits
      - title: Deep Learning
        meta: Ian Goodfellow, Yoshua Bengio, Aaron Courville
---
