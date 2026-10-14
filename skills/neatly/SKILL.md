---
name: neatly
description: Make HTML pages that look designed by a person, not generated. Covers six kinds of page - report, slide deck, dashboard, landing page, docs and personal homepage - in four design systems (neatly, editorial, warm, night) that share one set of components and a single swappable accent colour. Use whenever the user asks for an HTML page, report, one-pager, write-up, presentation, slides, pitch deck, dashboard, landing page, product page, docs or guide page, personal site, portfolio or about-me page, or asks to make an existing HTML page look better or less like AI.
---

# Neatly

Every page is one self-contained HTML file. The look comes from `neatly.css`, which is already inlined in each layout, plus an optional design system on top. You pick a layout, write the content with the components below, and `make.py` assembles and checks the page.

## 1. Pick the layout

| The user wants | Layout | Notes |
|---|---|---|
| A report, review, analysis, memo, write-up, research summary | `layouts/report.html` | Long read with a contents rail, numbers strip, figures |
| Slides, a deck, a pitch, a presentation | `layouts/deck.html` | 16:9 slides, arrow keys, prints to PDF one slide per page |
| A dashboard, metrics overview, admin or status page | `layouts/dashboard.html` | Sidebar, four KPIs, chart panels, table, activity |
| A landing page, product page, homepage, waitlist | `layouts/landing.html` | Hero with line art, features, pricing, FAQ, closing call |
| Docs, a guide, a tutorial, an API or setup page | `layouts/docs.html` | Left nav, steps with code blocks, "On this page" rail |
| A personal site, portfolio, about-me or link page | `layouts/personal.html` | Name and one-line value, work grid, experience, links, contact |

If the request fits none of them, use the report layout and drop the parts you do not need. Do not ask the user which layout; choose.

## 1b. Pick the design system

All four share the same components, so any layout works in any system. Default to `neatly` unless the user's words point elsewhere; do not ask.

| System | Feels like | Pick it for |
|---|---|---|
| `neatly` (default) | Neutral grey, Montserrat, graph-paper line art | Reports, docs, dashboards, anything work-like |
| `editorial` | Big black type, hairline rules, square corners | Personal brands, portfolios, opinionated launches |
| `warm` | Cream paper, round shapes, Nunito | Consumer apps, small shops, friendly personal sites |
| `night` | Dark, crisp, Manrope | Developer tools, AI products, anything "techy" |

Pass it to `make.py` with `--system editorial`. Each system has its own default accent; `--accent` overrides it.

## 2. Make the file

Read the body of the layout you picked. Line 2 of the file says which line `<body>` is on; read from there to the end (about 80 lines). Never read the lines above it: they are the design system and you do not change them.

Write your page's body (everything that goes inside `<body>`) to a scratch file, using the layout's blocks: replace every `TODO`, delete blocks you do not need, duplicate blocks you need more of. Then build the page:

```bash
python3 <skill-dir>/scripts/make.py report body.html ./q3-review.html --title "Q3 product review"
```

`make.py` copies the layout's design system, adds the chosen system (`--system warm`), puts your body in, sets the title, and runs the checker. Add `--accent e4572e` for a brand colour. Switching systems later is one rebuild from the same body file. To revise, edit the page directly or rebuild from the body file. Page-specific CSS goes in a `<style>` at the top of the body and uses `var(--nt-*)` tokens only.

Restyling an existing page: copy the closest layout, then move the content into it. Do not paste `neatly.css` on top of the old page's CSS.

Finished pages for every layout are in the repository's `examples/` folder (https://github.com/kehaoran-ai/neatly/tree/main/examples). Look at one when you are unsure how a block should look.

## 3. Write the content

The design only works with plain, specific writing.

- Headings are sentences that state the point, with a number when there is one: "Activation doubled in Q3 after we shortened onboarding", not "Q3 results" and not "Activation doubled. Here is why."
- No two-part slogans ("Write first. Organise never."), no "not X, but Y", no rhetorical questions as headings.
- Sentence case everywhere. No all-caps labels, no emoji, no exclamation marks, at most two em dashes per page.
- Skip stock words: seamless, unlock, elevate, leverage, supercharge, game-changer, cutting-edge.
- Every number needs its unit, and a comparison when the user gave one: "41% (+19 pts vs Q2)". A metric without a comparison simply has no `.nt-delta`.
- Use only what the user gave you. Do not add causes, explanations, quotes, names or numbers they did not provide. If a layout part needs facts you do not have (author, date, brand, a byline, a quote, next steps), delete that part instead of filling it in. Invent sample data only when the user asks for a mock-up, and then keep it consistent across the page.
- Keep a diagram, table or steps block only if it shows something the text does not.
- On slides, keep headings to about 60 characters (two lines) and put one thing under each: a number strip, a chart, a diagram or a short list.
- Footers, kickers and labels can stay empty when you have nothing true to put there. An empty footer span is fine.
- Colour a change by whether it is good, not by its sign: fewer support tickets is `.nt-delta.is-good`.

## 4. Use the components

Full list with markup: `reference/components.md`. The ones that carry the look:

- `.nt-metrics` > `.nt-metric` for 2 to 5 headline numbers. One strip per page.
- `.nt-figure` > `.nt-frame.nt-grid` > `svg.nt-line` for diagrams: graph paper, crop marks, 1.5px ink lines. Put `class="is-accent"` on the one part the reader must look at.
- `svg.nt-chart` with `data-chart`, `data-series`, `data-labels` for line and bar charts. `neatly.js` draws them. `data-accent` picks the highlighted series.
- `.nt-note` for a conclusion or warning. `.nt-steps` for sequences. `.nt-table` inside `.nt-table-wrap` for data.

Rules the checker enforces:

- One accent colour. It marks the current item, links, and the one thing in a figure that matters. It is never a big button or a background.
- The primary button is ink (`.nt-btn--primary`). At most one per screen.
- Not every block goes in a card. Never a row of exactly three cards.
- No serif or italic headings, no gradients, glows, blur or glass, no coloured left borders, no dark mode.

## 5. Check and look

`make.py` already ran the checker. After any later edit, run it again:

```bash
python3 <skill-dir>/scripts/check.py ./q3-review.html
```

Fix every error. Fix warnings unless you have a reason. The checker reads the code, not the picture, so if you can see the page (a browser tool or a screenshot), look at it once for text running out of boxes and charts that read wrong. Then open the page for the user (`open ./q3-review.html` on macOS) and tell them the path.

## Changing the accent

Put this at the top of `<body>`:

```html
<style>:root { --nt-accent: #e4572e; }</style>
```

Soft, line and ink variants are derived from it. To preview a colour without editing, open the page with `?accent=e4572e`. Pick a colour with enough contrast on white (darker than about `#888` in lightness). Leave the greys alone.
