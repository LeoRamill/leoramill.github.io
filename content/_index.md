---
# Leave the homepage title empty to use the site title
title: ""
date: 2026-09-14
type: landing

design:
  # Default section spacing, applied inline to every section but the hero (which sets its own 0).
  # Was 5rem top and bottom: two sections then stacked 10rem of empty picture between the last line
  # of one and the heading of the next, which on a page of short sections reads as five separate
  # pages rather than one. 2.5rem still separates them clearly and lets two fit on a screen.
  spacing: "2.5rem"

sections:
  # 1. Dark hero with the Meteor background (the "gioco di sfondi" of the epalu template),
  #    laid out like riccardocadei: round avatar + name + tagline + social icons.
  - block: profile-hero
    id: hero
    content:
      username: admin
      # The epigraph under the button, written one character at a time as the background pushes in,
      # finished exactly where the push-in lands — and unwritten scrolling back up, since what is
      # shown is a function of the scroll position and not of a timer.
      motto: "🌌 Per Aspera Ad Astra 🔭"
      # The word on the invitation to scroll at the foot of the first screen. It fades out as soon
      # as the scroll it asks for begins, and clicking it goes straight to the content. Remove the
      # line and the invitation goes with it.
      scroll_hint: scroll
      button:
        text: View CV
        url: /cv/
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.
      # Fixed background shared by the whole page (see `layouts/partials/blox/profile-hero.html`).
      # With `video` set, the layer is the video: it plays once and rests on its last frame, and
      # zooms in as the first screen scrolls away. Remove the three video lines to go back to the
      # Meteor image.
      fixed_background:
        filename: Meteor.svg
        color: "#000000"
        video: hero.mp4
        video_small: hero-small.mp4
        video_webm: hero.webm
        poster: hero-poster.jpg
        # With `frames`, the camera walks in with the scroll instead (frames of the push-in in
        # `assets/media/hero-frames/1280/` and `/720/`), the hero stays pinned for the walk, and
        # `hold` is the rest of the clip, looping for good once the camera has arrived. Remove
        # these three lines to go back to the video simply playing on its own.
        frames: hero-frames
        hold: hero-hold.mp4
        hold_webm: hero-hold.webm
      spacing:
        # No padding of its own: in the scroll-scrubbed mode the hero sets its height itself
        padding: [0, 0, 0, 0]

  # 2. Full-width cover photo + italic bio (as on riccardocadei's homepage), dark for now.
  - block: cover-bio
    id: about
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.
    content:
      username: admin
      # A folder under `assets/media/` turns the cover into a row that scrolls sideways, the same
      # row the photography page uses. It needs two photographs to become one — with fewer, the
      # block falls back to `image` below, because a strip that cannot scroll is worse than a
      # single picture. So the switch is made by dropping files in `assets/media/covers/`.
      folder: covers
      # The fallback, and what shows while the folder holds fewer than two photographs.
      image: covers/03_cover.JPG
      # A line shown under whichever photograph is in the middle, keyed by file name. Leave a file
      # out and it simply has no caption — the line collapses rather than holding a gap open.
      captions:
        01_Luminosità.JPG: 'Oslo, Norway. 2023: First trip outside Italy, First Photo'
        02_surf.jpeg: 'San Juan, Philippines. 2024: First Surf Lesson'
        03_cover.JPG: 'Corfù, Greece. 2024: The Sea of Thoughts, Best Pic'
        04_sapienza_grad.JPG: 'Rome, Italy. 2024: Bachelor Graduation'
        05_Turin.jpg: 'Turin, Italy. 2024: New chapter, new friendships'
        defense.png: 'Sophia Antipolis, France. 2026: Defense at EURECOM'
      alt: Per Aspera Ad Astra
      # Leave `text` empty to use the biography written in `content/authors/admin/_index.md`
      text: ""

  # 3. "Selected News" timeline fed by `content/news/`, dark for now.
  - block: news-list
    id: news
    content:
      title: Selected News
      count: 6
      more:
        text: All news
        url: /news/
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.

  # 4. "Selected Publication" — the newest entries of `content/publication/`, same markup as the
  #    Publications page (see `layouts/partials/blox/entry-list.html`), dark for now.
  - block: entry-list
    id: publications
    content:
      title: Selected Publication
      count: 3
      more:
        text: All publications
        url: /publication/
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.

  # 5. "Selected Projects" — the featured entries of `content/project/`, in the same list as
  #    Publications above rather than the theme's card grid, so the two read as one page.
  - block: entry-list
    id: projects
    content:
      title: Selected Projects
      section: project
      count: 4
      featured_only: true
      more:
        text: All projects
        url: /project/
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.

  # 6. Closing dark section (second background of the epalu template) with a call to action.
  - block: markdown
    id: contact
    content:
      title: ""
      text: |
        <div class="contact-cta">
          <h2>Let's talk</h2>
          <p>Reach out for any constructive discussion, collaboration, or just to talk about AI, art and photography.</p>
          <a class="contact-cta__btn" href="mailto:leonardvincentramil@icloud.com">Send me an e-mail</a>
        </div>
    design:
      css_class: dark home-no-veil
      # No per-section wash here. The veil is one scrim on the fixed layer itself
      # (`.site-fixed-bg--frames::after` in custom.css), at the same 0.56 these five boxes used to
      # carry each. Five stacked translucent boxes meet at four boundaries, and a boundary that
      # lands on a fractional device pixel is antialiased from both sides — a faint horizontal line
      # across the page. One viewport-sized fixed box has no boundaries to land anywhere.
      # Heavier tint than the hero: the same fixed background re-emerges, darker
---
