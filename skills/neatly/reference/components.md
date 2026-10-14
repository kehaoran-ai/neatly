# Neatly components

Every class starts with `nt-`. Modifiers on a component start with `is-` or `--`. The layouts in `../layouts/` use all of these; copy from there when you can.

## Tokens

Use these in page-only CSS instead of raw values.

| Token | Use |
|---|---|
| `--nt-accent` | The one colour. Change it to rebrand the page. |
| `--nt-accent-soft`, `--nt-accent-line`, `--nt-accent-ink` | Derived from the accent: tinted background, border, text on tint. |
| `--nt-paper`, `--nt-surface`, `--nt-sunken` | Page, white surfaces, wells. |
| `--nt-line`, `--nt-line-strong` | Hairlines, stronger borders. |
| `--nt-ink`, `--nt-ink-2`, `--nt-ink-3` | Text, secondary text, captions. |
| `--nt-good`, `--nt-bad`, `--nt-warn` (+ `-soft`) | Status only. |
| `--nt-1` … `--nt-9` | Spacing: 4, 8, 12, 16, 24, 32, 48, 64, 96 px. |
| `--nt-radius-sm`, `--nt-radius`, `--nt-radius-lg` | 6, 10, 14 px. |
| `--nt-sans`, `--nt-mono` | The two font stacks. There is no serif. |

## Text

| Markup | What it is |
|---|---|
| `<div class="nt-kicker"><b>02</b>Section name</div>` | Small line above a heading. The bold part is a short index or period (`02`, `Q3`, `Sep`), the rest says what kind of page or section it is. Drop it if there is nothing useful to say. |
| `<p class="nt-lede">` | The sentence under a title. |
| `.nt-muted`, `.nt-faint`, `.nt-small`, `.nt-mono` | Secondary text, captions, small size, monospace. |
| `<span class="nt-mark">` | Highlighter for the one phrase that matters. Once or twice per page. |
| `<article class="nt-prose">` | Long text with a comfortable line length. |

## Blocks

**Numbers strip**, 2 to 5 items. The `.nt-delta` line is optional:

```html
<div class="nt-metrics">
  <div class="nt-metric"><b>41%</b><span>Activated in week one</span><span class="nt-delta is-good">+19 pts</span></div>
  <div class="nt-metric"><b>3:40</b><span>Time to first note</span><span class="nt-delta is-good">−62%</span></div>
</div>
```

**Note**, for a conclusion, decision or warning. Variants `--accent`, `--warn`, `--bad`:

```html
<div class="nt-note"><b>Decision</b><p>Keep the new flow for all sign-ups.</p></div>
```

**Steps**, numbered with a spine. `is-current` marks the step that matters:

```html
<ol class="nt-steps">
  <li><h4>Add the package</h4><p class="nt-muted">One line.</p></li>
  <li class="is-current"><h4>Send your first note</h4><p class="nt-muted">One line.</p></li>
</ol>
```

**Table**: always wrap it, so it scrolls on phones. Right-align numbers with `is-num`.

```html
<div class="nt-table-wrap"><table class="nt-table">
  <thead><tr><th>Cohort</th><th class="is-num">Sign-ups</th></tr></thead>
  <tbody><tr><td>3 Aug</td><td class="is-num">2,140</td></tr></tbody>
</table></div>
```

**Code** with a header and copy button. Colour tokens by hand: `.k` keyword, `.s` string, `.c` comment.

```html
<div class="nt-code">
  <div class="nt-code-head">terminal<button class="nt-copy" data-copy="#c1">Copy</button></div>
  <pre id="c1">$ npm install example</pre>
</div>
```

**Quote**:

```html
<figure class="nt-quote"><blockquote>“The words of a real person.”</blockquote><figcaption>Name · role</figcaption></figure>
```

**FAQ**: `<div class="nt-faq"><details><summary>Question</summary><div>Answer.</div></details></div>`

**Cards**: `.nt-card` for things that need a frame, `.nt-card--featured` for the one recommended option. Use them for plans or a short set of choices, not for every block.

## Small parts

| Markup | What it is |
|---|---|
| `<a class="nt-btn nt-btn--primary">` | The main action, ink. One per screen. |
| `.nt-btn`, `.nt-btn--quiet`, `--sm`, `--lg` | Other buttons and sizes. |
| `<span class="nt-tag">` + `--accent`, `--good`, `--bad`, `--warn` | Status pill. Add `<span class="nt-dot"></span>` inside for a dot. |
| `<span class="nt-label">v2.1</span>` | Framed mono label for versions and IDs. |
| `<div class="nt-seg"><button aria-pressed="true">30 days</button>…</div>` | Segmented switch. `neatly.js` toggles it. |
| `<span class="nt-avatar">MC</span>` | Initials in a circle. |
| `<span class="nt-delta is-good">+4%</span>` | A change. `is-good` is green and `is-bad` is red, chosen by meaning, not by sign: −30% tickets is `is-good`. Leave both off for a neutral change. |
| `<kbd>⌘K</kbd>` | Key. |

## Figures and line art

Graph paper, crop marks and line art are the signature of the system. Use them for any diagram: flows, before and after, architecture, a product sketch.

```html
<figure class="nt-figure">
  <div class="nt-frame nt-grid">
    <svg class="nt-line" viewBox="0 0 640 200" role="img" aria-label="What the diagram shows">
      <path d="M200 100 H272"/><path d="M264 94 L272 100 L264 106"/>
      <rect x="60" y="72" width="140" height="56" rx="8" class="is-paper"/><text x="80" y="104">Sign up</text>
      <g class="is-accent"><rect x="280" y="72" width="140" height="56" rx="8" class="is-soft"/><text x="300" y="104">One question</text></g>
    </svg>
  </div>
  <figcaption><b>Fig. 1</b>What the reader should notice.</figcaption>
</figure>
```

Inside `svg.nt-line` every shape becomes a 1.5px ink line with no fill.

- `is-paper` fills a shape white, so lines behind it are hidden. Draw connecting lines first, boxes after.
- `is-accent` (on a shape or a `<g>`) turns it accent. Use it once per figure.
- `is-soft` fills with the accent tint. `is-faint` makes a line light grey. `stroke-dasharray="4 4"` makes it dashed.
- `<text>` is 13px semibold. `<text class="is-mono">` is the small grey caption under a label.
- Arrows are two short paths: the line, then a chevron at the end. Arrows point where things go.
- Keep boxes in a row the same size, and leave at least 16px between a label and any line.

## Charts

`neatly.js` draws into an empty `<svg class="nt-chart">` and redraws on resize.

| Attribute | Meaning |
|---|---|
| `data-chart` | `line` (default) or `bars` |
| `data-series` | One array, or an array of arrays for line charts: `[[...this year],[...last year]]` |
| `data-labels` | X labels. Use `""` to skip a label; otherwise labels are thinned to fit. |
| `data-accent` | Index of the series drawn in the accent. Others are dashed grey. |
| `data-highlight` | Bars only: JSON array of accent bar indexes, for example `[1]` or `[0,3]`. Default is the last bar. |
| `data-height` | Height in px, default 240. |
| `data-unit` | Suffix on the y ticks, added as is: `%`, or `" s"` with its own space. |
| `data-area="false"` | No fill under the accent line. |

A bar chart has one series and needs no legend: the x labels name the bars and the accent bar is the one the heading talks about. For two values (August vs September) a bar chart with two bars is fine; so is a `.nt-metrics` strip, which is often clearer.

Sparkline: `<svg class="nt-spark is-accent" data-spark="[3,4,6,5,8]"></svg>`. Legend: `<div class="nt-legend"><span><i class="is-accent"></i>2026</span><span><i class="is-faint"></i>2025</span></div>`.

## Page chrome

- `.nt-topbar > .nt-wrap.nt-row` with `.nt-brand`, `.nt-grow` (spacer) and a `.nt-nav`.
- `.nt-wrap` centres content at 1120px; add `is-wide` for 1320px.
- `.nt-split` two columns, `.nt-cols` with `style="--cols:4"` for N columns, `.nt-row` for a wrapping row.
- `.nt-section` vertical rhythm between landing sections.
- `.nt-footer > .nt-wrap.nt-row`.
- `.nt-noprint` hides an element when printing.

## Layout-specific classes

- Report: `.nt-report-head`, `.nt-byline`, `.nt-report` (contents + article), `.nt-toc[data-toc]`, `.nt-chart-frame`, `.nt-chart-head`.
- Deck: `body.nt-deck`, `section.nt-slide` (first one `is-active`), `.nt-slide-body`, `.nt-slide-foot` with an empty `.nt-num` (filled in as 03 / 08), `.nt-deck-hint`. The layout has four slide patterns: title, numbers, chart, and a closing statement for an ask or decision. A plan with goals that have no numbers fits `.nt-steps` on a slide.
- Dashboard: `.nt-app`, `.nt-side` (links with `aria-current="page"`, `.nt-side-label`, `.nt-count`, `.nt-side-foot`), `.nt-main`, `.nt-main-head`, `.nt-panel` (`-head`, `-body`), `.nt-kpis` > `.nt-kpi` (`-label`, `-value`), `.nt-board`, `.nt-hbar` with `style="--v:38%"`, `.nt-feed`.
- Landing: `.nt-nav`, `.nt-hero`, `.nt-actions`, `.nt-install`, `.nt-section-head`, `.nt-features` > `.nt-feature`, `.nt-pricing` > `.nt-price` (`-amount`), `.nt-checks`, `.nt-cta`.
- Personal: `.nt-profile` (with `.nt-role`, `.nt-bio`, `.nt-actions`, and `.nt-portrait` as an `<img>` or `is-initials`), `.nt-works` > `a.nt-work` (`.nt-work-thumb`, `.nt-work-meta`), `ol.nt-timeline` (`time` + `h4` + `p`), `.nt-linklist`, `a.nt-mailto`.
- Docs: `.nt-search`, `.nt-docs`, `.nt-docs-nav`, `.nt-docs-main`, `.nt-crumbs`, `.nt-pager`, and `.nt-toc[data-toc]` as the right rail.

## Design systems

`systems/editorial.css`, `systems/warm.css` and `systems/night.css` load after `neatly.css` (inside the `neatly-system` block of the page) and only change tokens plus a few component details. Write pages against the tokens and classes above and they work in every system. Never hard-code colours in page CSS: in `night` the paper is dark and the ink is light.
