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
      background:
        color: black
        image:
          filename: Meteor.svg
          filters:
            brightness: 1.0
          size: cover
          position: center
          parallax: false
      spacing:
        padding: ["4rem", 0, "4rem", 0]

  # 2. Light section: full-width cover photo + italic bio (as on riccardocadei's homepage).
  - block: cover-bio
    id: about
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
      text: 'Browse [all projects](/project/).'
      count: 4
      filters:
        folders:
          - project
        featured_only: true
    design:
      view: article-grid
      columns: 2

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
      background:
        color: black
        image:
          filename: stacked-peaks.svg
          size: cover
          position: center
          parallax: false
---
