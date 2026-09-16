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
      css_class: dark
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
        # `hold` is the rest of the clip, played once the camera has arrived. Remove these three
        # lines to go back to the video simply playing on its own.
        frames: hero-frames
        hold: hero-hold.mp4
        hold_webm: hero-hold.webm
      # Light translucent tint: the meteors show through clearly here
      background:
        gradient_start: "rgba(15, 8, 24, 0.30)"
        gradient_end: "rgba(15, 8, 24, 0.50)"
        gradient_angle: 180
      spacing:
        # No padding of its own: in the scroll-scrubbed mode the hero sets its height itself
        padding: [0, 0, 0, 0]

  # 2. Light section: full-width cover photo + italic bio (as on riccardocadei's homepage).
  - block: cover-bio
    id: about
    design:
      css_class: section-solid
    content:
      username: admin
      # Placeholder cover (generated). Replace with your own photo, e.g. `cover.jpg` in `assets/media/`.
      image: cover.svg
      alt: Per Aspera Ad Astra
      # Leave `text` empty to use the biography written in `content/authors/admin/_index.md`
      text: ""

  # 3. Soft grey section: "Selected News" timeline fed by `content/news/`.
  - block: news-list
    id: news
    content:
      title: Selected News
      count: 6
      more:
        text: All news
        url: /news/
    design:
      css_class: section-alt

  # 4. White section: selected projects (cards).
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
      css_class: section-solid

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
      css_class: dark
      # Heavier tint than the hero: the same fixed background re-emerges, darker
      background:
        gradient_start: "rgba(8, 4, 14, 0.72)"
        gradient_end: "rgba(8, 4, 14, 0.82)"
        gradient_angle: 180
---
