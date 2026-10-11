# Neatly

HTML pages from your AI that look like a person designed them.

Neatly is a skill for Claude Code and other agents. Ask for a report, a slide deck, a dashboard, a landing page or a docs page, and you get one self-contained HTML file in a calm, consistent style: neutral grey, one sans typeface, line-art diagrams on graph paper, and a single accent colour you can change in one line.

**Live demo: [neatly.kehaoran.ai](https://neatly.kehaoran.ai)** · English · [简体中文](README.zh-CN.md)

![A report made with Neatly](docs/screenshots/report.png)

## Why

Ask any model for an HTML page and you can tell it was generated: purple-to-blue gradients, a glowing hero, a row of three cards with emoji icons, serif headlines with one italic word, all-caps labels, "Unlock seamless productivity". Neatly gives the model one visual system to work inside, five layouts to start from, writing rules, and a checker that catches those habits before you see the page.

## Five layouts, one look

| Layout | For | Example |
|---|---|---|
| Report | Reviews, analyses, memos, research write-ups | [report.html](https://neatly.kehaoran.ai/examples/report.html) |
| Deck | Pitches and presentations, 16:9, prints to PDF | [deck.html](https://neatly.kehaoran.ai/examples/deck.html) |
| Dashboard | Metrics overviews and status pages | [dashboard.html](https://neatly.kehaoran.ai/examples/dashboard.html) |
| Landing page | Product pages and launches | [landing.html](https://neatly.kehaoran.ai/examples/landing.html) |
| Docs | Guides, setup and API pages | [docs.html](https://neatly.kehaoran.ai/examples/docs.html) |

| | |
|---|---|
| ![Deck](docs/screenshots/deck.png) | ![Dashboard](docs/screenshots/dashboard.png) |
| ![Landing page](docs/screenshots/landing.png) | ![Docs](docs/screenshots/docs.png) |

Every example is a single file. Open it on the demo site, or download it and double-click; there is nothing to build. On the demo site you can also switch the accent colour and open the starting file behind each example.

## Install

**Claude Code**

```
/plugin marketplace add kehaoran-ai/neatly
/plugin install neatly@neatly
```

**Any agent that reads skills** (Claude Code, Codex, Cursor and others)

```bash
npx skills add kehaoran-ai/neatly
```

**By hand**

```bash
git clone https://github.com/kehaoran-ai/neatly
cp -r neatly/skills/neatly ~/.claude/skills/
```

## Use

Just ask. The skill picks the layout.

```
Make an HTML report on our September sales: revenue 18,400 dollars, up 12%,
oat milk went from 21% to 34% of orders after we dropped the surcharge.
```

```
Turn these notes into a 6-slide deck for Monday's team meeting.
```

```
Make this page look better.   (with an existing HTML file)
```

The agent copies a layout, writes the content, runs the checker and opens the page.

## Change the colour

Everything follows one token. Add this line at the top of the page's `<body>`:

```html
<style>:root { --nt-accent: #e4572e; }</style>
```

To try a colour without editing, open any page with `?accent=e4572e` on the URL.

## The checker

```bash
python3 skills/neatly/scripts/check.py page.html
```

It fails a page for serif or italic headlines, Inter and Geist, gradients, glow and glass, coloured side bars, a row of exactly three cards, all-caps text, emoji, dark-mode styles, leftover placeholders and a missing viewport. It warns about raw colours, heavy shadows, too many cards or accents, em dashes and stock phrases like "seamless" and "unlock".

## Without an agent

`skills/neatly/neatly.css` works on its own. Copy a file from `skills/neatly/layouts/`, replace the `TODO`s and open it. `neatly.js` is optional and draws the charts, runs the slides, and handles copy buttons and the contents highlight. [`reference/components.md`](skills/neatly/reference/components.md) lists every class.

## What is inside

```
skills/neatly/
  SKILL.md              how the agent uses Neatly
  neatly.css            the visual system, inlined into every page
  neatly.js             charts, slides, copy buttons, contents (optional)
  layouts/              five starting files
  reference/            component reference
  scripts/make.py       builds a page from a layout and a body
  scripts/check.py      the checker
examples/               five finished pages
scripts/build.py        re-inlines the CSS and JS after you edit them
```

Fonts: Montserrat from Google Fonts, with system fallbacks. No other dependencies.

## License

MIT, by [Ke Haoran](https://github.com/kehaoran-ai).
