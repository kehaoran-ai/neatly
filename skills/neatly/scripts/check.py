#!/usr/bin/env python3
"""Check a Neatly page for the things that make HTML look AI-made.

    python3 check.py page.html [more.html ...]

Errors break the look and must be fixed. Warnings are usually right; fix them
unless you have a reason. Exit code 1 when any page has an error.
Only the page's own CSS and markup are checked; the injected neatly.css and
neatly.js blocks are skipped.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

CSS_BLOCK = re.compile(r"/\* neatly\.css:start \*/.*?/\* neatly\.css:end \*/", re.S)
JS_BLOCK = re.compile(r"/\* neatly\.js:start \*/.*?/\* neatly\.js:end \*/", re.S)
SYS_BLOCK = re.compile(r"/\* neatly-system:start \*/.*?/\* neatly-system:end \*/", re.S)

SERIF = re.compile(r"font(?:-family)?\s*:[^;}]*\b(serif|Georgia|Times|Playfair|Instrument Serif|Fraunces|Lora|Merriweather|DM Serif|Cormorant|Libre Baskerville)\b", re.I)
BANNED_FONTS = re.compile(r"font(?:-family)?\s*:[^;}]*\b(Inter|Geist|Poppins|Space Grotesk)\b", re.I)
WORDS = re.compile(r"\b(seamless(?:ly)?|unlock|elevate|leverage|game[- ]changer|supercharge|revolutioni[sz]e|effortless(?:ly)?|cutting[- ]edge|delve|in today's|let's dive|here's why|here is why|the best part)\b", re.I)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, classes)
        self.text = []           # (text, tags in stack)
        self.children = {}       # parent id -> [(tag, class, style)] of its direct children
        self.parents = []        # unique ids of open elements
        self.next_id = 0
        self.heading_em = 0
        self.has_viewport = False
        self.has_title = False
        self.lang = False
        self.uses_neatly = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag == "html" and a.get("lang"):
            self.lang = True
        if tag == "meta" and a.get("name") == "viewport":
            self.has_viewport = True
        if tag == "title":
            self.has_title = True
        if "nt-" in cls:
            self.uses_neatly = True
        if tag in ("em", "i") and any(t in ("h1", "h2", "h3") for t, _ in self.stack):
            self.heading_em += 1
        if self.parents:
            self.children.setdefault(self.parents[-1], []).append((tag, cls, a.get("style", "")))
        if tag in ("br", "img", "input", "meta", "link", "hr", "source", "wbr", "path", "rect", "circle", "line", "polyline", "polygon", "ellipse"):
            return
        self.next_id += 1
        self.stack.append((tag, cls))
        self.parents.append(self.next_id)

    def handle_endtag(self, tag):
        while self.stack:
            t, _ = self.stack.pop()
            self.parents.pop()
            if t == tag:
                break

    def handle_data(self, data):
        if data.strip() and not any(t in ("script", "style", "pre", "code", "kbd") for t, _ in self.stack):
            self.text.append(data)


def check(path):
    raw = Path(path).read_text(encoding="utf-8")
    errors, warns = [], []
    if "neatly.css:start" not in raw:
        errors.append("neatly.css is not inlined. Start from a file in layouts/ so the markers are there.")
    page = SYS_BLOCK.sub("", CSS_BLOCK.sub("", JS_BLOCK.sub("", raw)))
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", page, re.S)) + "\n" + "\n".join(re.findall(r'style="([^"]*)"', page))

    p = Page()
    p.feed(page)
    text = " ".join(p.text)

    if not p.has_viewport: errors.append('Missing <meta name="viewport">. The page will not fit phones.')
    if not p.has_title: errors.append("Missing <title>.")
    if not p.lang: warns.append('Add lang to <html>, for example <html lang="en">.')
    if not p.uses_neatly: errors.append("No nt- classes in the markup. Build the page from Neatly components.")

    # Type
    for m in SERIF.finditer(css):
        if "sans-serif" not in m.group(0).lower() or re.search(r"\bserif\b(?!-)", m.group(0).replace("sans-serif", "")):
            errors.append(f"Serif font in page CSS ({m.group(1)}). Neatly uses one sans for everything.")
            break
    if m := BANNED_FONTS.search(css):
        errors.append(f"Font {m.group(1)} is the default AI look. Keep var(--nt-sans).")
    if p.heading_em:
        errors.append(f"{p.heading_em} italic phrase(s) inside headings. Write the heading as one plain sentence.")
    if re.search(r"font-style\s*:\s*italic", css):
        warns.append("font-style: italic in page CSS. Italics read as decoration here; drop them.")
    if re.search(r"text-transform\s*:\s*uppercase", css, re.I):
        errors.append("text-transform: uppercase. Use sentence case.")
    if re.search(r"letter-spacing\s*:\s*[0-9.]+em", css):
        errors.append("letter-spacing in em. Keep letter-spacing at 0.")
    caps = [w for w in re.findall(r"\b[A-Z]{2,}(?:\s+[A-Z]{2,})+\b", text) if len(w) > 7 and "TODO" not in w]
    if caps:
        errors.append(f"All-caps text: {caps[0]!r}. Use sentence case.")

    # Colour and depth
    if re.search(r"prefers-color-scheme\s*:\s*dark", css):
        errors.append("Dark mode styles found. Neatly is light only.")
    if re.search(r"border-left\s*:\s*[2-9]px\s+solid", css):
        errors.append("Thick left border. Coloured side bars are the most common AI tell; use .nt-note instead.")
    if re.search(r"(radial|conic)-gradient|linear-gradient\([^)]*(#|rgb|hsl)", css):
        errors.append("Gradient in page CSS. Use flat tokens; the only texture is .nt-grid.")
    if re.search(r"backdrop-filter|filter\s*:\s*blur|text-shadow", css):
        errors.append("Blur, glass or text shadow. Remove it.")
    if re.search(r"box-shadow\s*:[^;]*\b([2-9]\d|\d{3})px", css):
        warns.append("Large box-shadow. Use var(--nt-shadow) or a hairline border.")
    raw_colours = set(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)", re.sub(r"--nt-accent\s*:\s*#[0-9a-fA-F]{3,8}", "", css)))
    if raw_colours:
        warns.append(f"Raw colours in page CSS ({', '.join(sorted(raw_colours)[:3])}). Use var(--nt-*) tokens so the accent swap works.")
    if re.search(r"nt-btn[^\"]*\"[^>]*style=\"[^\"]*background\s*:\s*var\(--nt-accent", page):
        errors.append("Accent-coloured button. Primary actions are ink (.nt-btn--primary).")

    # Layout
    for kids in p.children.values():
        # Neatly's own cards and the usual names other pages use for them.
        cards = [k for k in kids if re.search(r"(^|[\s_-])(card|tile)([\s_-]|$)", k[1])]
        if len(cards) == 3 and len(kids) == 3:
            errors.append("A row of exactly three cards. Use two, four, or a list without cards.")
            break
    n_cards = len(re.findall(r'class="[^"]*\bnt-card\b', page))
    if n_cards > 8:
        warns.append(f"{n_cards} cards. Not every block needs a frame; use hairlines and space.")
    n_accent = len(re.findall(r"is-accent|nt-tag--accent|nt-card--featured|nt-mark\b", page))
    if n_accent > 12:
        warns.append(f"{n_accent} accent marks. The accent should point at the few things that matter.")

    # Words
    if EMOJI.search(text):
        errors.append("Emoji in the text. Remove them.")
    if (n := text.count("—")) > 2:
        warns.append(f"{n} em dashes. Use a comma, a colon or a new sentence.")
    if m := WORDS.search(text):
        warns.append(f"Stock phrase {m.group(0)!r}. Say the specific thing instead.")
    if text.count("!") > 1:
        warns.append("Exclamation marks. State the fact.")
    if "TODO" in text:
        errors.append("TODO placeholders left in the page.")
    return errors, warns


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    failed = False
    for path in argv:
        if not Path(path).is_file():
            print(f"FAIL  {path}  (file not found)")
            failed = True
            continue
        errors, warns = check(path)
        status = "FAIL" if errors else "ok"
        print(f"{status}  {path}  ({len(errors)} errors, {len(warns)} warnings)")
        for e in errors: print(f"  error  {e}")
        for w in warns: print(f"  warn   {w}")
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
