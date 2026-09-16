---
# Leave the homepage title empty to use the site title
title: ""
date: 2026-09-14
type: landing

design:
  # Default section spacing
  spacing: "5rem"

sections:
  # 1. Dark hero with the Meteor background (the "gioco di sfondi" of the epalu template),
  #    laid out like riccardocadei: round avatar + name + tagline + social icons.
  - block: profile-hero
    id: hero
    content:
      username: admin
      button:
        text: View CV
        url: /cv/
    design:
      css_class: dark home-no-veil
      # The lightest wash the text survives: measured, 0.28-0.32 puts every block on the page at or
      # above the 4.5:1 body text needs (News is the tightest at 4.6:1). It is this light only
      # because the muted greys were lifted first — see `.home-no-veil` in custom.css; with the
      # theme's own greys the same reading needed 0.68.
      background:
        gradient_start: "rgba(10, 8, 16, 0.28)"
        gradient_end: "rgba(10, 8, 16, 0.32)"
        gradient_angle: 180
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
      # The lightest wash the text survives: measured, 0.28-0.32 puts every block on the page at or
      # above the 4.5:1 body text needs (News is the tightest at 4.6:1). It is this light only
      # because the muted greys were lifted first — see `.home-no-veil` in custom.css; with the
      # theme's own greys the same reading needed 0.68.
      background:
        gradient_start: "rgba(10, 8, 16, 0.28)"
        gradient_end: "rgba(10, 8, 16, 0.32)"
        gradient_angle: 180
    content:
      username: admin
      # Placeholder cover (generated). Replace with your own photo, e.g. `cover.jpg` in `assets/media/`.
      image: cover.svg
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
      # The lightest wash the text survives: measured, 0.28-0.32 puts every block on the page at or
      # above the 4.5:1 body text needs (News is the tightest at 4.6:1). It is this light only
      # because the muted greys were lifted first — see `.home-no-veil` in custom.css; with the
      # theme's own greys the same reading needed 0.68.
      background:
        gradient_start: "rgba(10, 8, 16, 0.28)"
        gradient_end: "rgba(10, 8, 16, 0.32)"
        gradient_angle: 180

  # 4. Selected projects (cards), dark for now.
  - block: collection
    id: projects
    content:
      title: Selected Projects
      text: 'Browse [all projects](project/).'
      count: 4
      filters:
        folders:
          - project
        featured_only: true
    design:
      view: article-grid
      columns: 2
      css_class: dark home-no-veil
      # The lightest wash the text survives: measured, 0.28-0.32 puts every block on the page at or
      # above the 4.5:1 body text needs (News is the tightest at 4.6:1). It is this light only
      # because the muted greys were lifted first — see `.home-no-veil` in custom.css; with the
      # theme's own greys the same reading needed 0.68.
      background:
        gradient_start: "rgba(10, 8, 16, 0.28)"
        gradient_end: "rgba(10, 8, 16, 0.32)"
        gradient_angle: 180

  # 5. Closing dark section (second background of the epalu template) with a call to action.
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
      # The lightest wash the text survives: measured, 0.28-0.32 puts every block on the page at or
      # above the 4.5:1 body text needs (News is the tightest at 4.6:1). It is this light only
      # because the muted greys were lifted first — see `.home-no-veil` in custom.css; with the
      # theme's own greys the same reading needed 0.68.
      background:
        gradient_start: "rgba(10, 8, 16, 0.28)"
        gradient_end: "rgba(10, 8, 16, 0.32)"
        gradient_angle: 180
      # Heavier tint than the hero: the same fixed background re-emerges, darker
---
