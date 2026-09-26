---
title: My Timeline
layout: shaping-academic
lead:
  text: "Where I have been studying and researching, oldest first."
  url: ""
# Every stop on the road is a folder next to this file, and they are read in the order of their
# names — which is why they start with a number:
#
#   00-early/          index.md  + the photographs of that period
#   01-liceo-cavour/   index.md  + photographs
#   02-sapienza/       ...
#
# In each `index.md`: `title` is the place, `period` the span, `school` the degree or role, and the
# text under the front matter is what that time was about. Put photographs (jpg, png, webp) in the
# same folder: two or more turn into a row that scrolls like the one on the homepage, one is shown
# on its own, none and the stop is text only. Photographs are ordered by file name, and
# `captions:` in the stop's front matter maps a file name to the line shown under it.
#
# To add a stop, add a folder; to move one, rename it.
#
# The stops are data for this page, not pages of their own: nothing is published at their URLs.
cascade:
  # `kind: page` so this reaches the stops only: without it the timeline page itself was also
  # never rendered.
  - _target:
      kind: page
    build:
      render: never
      list: local
# A timeline, not a feed: no RSS for this section.
outputs: [HTML]
---
