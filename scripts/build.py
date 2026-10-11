#!/usr/bin/env python3
"""Inject the current neatly.css / neatly.js into every layout and example.

Pages keep the design system between markers so each file stays a single,
double-clickable HTML file:

    /* neatly.css:start */ ... /* neatly.css:end */
    /* neatly.js:start */  ... /* neatly.js:end */

Run after editing skills/neatly/neatly.css or neatly.js:
    python3 scripts/build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "neatly"
CSS = (SKILL / "neatly.css").read_text(encoding="utf-8").strip()
JS = (SKILL / "neatly.js").read_text(encoding="utf-8").strip()

def inject(text, name, body):
    pat = re.compile(r"(/\* " + re.escape(name) + r":start \*/).*?(/\* " + re.escape(name) + r":end \*/)", re.S)
    return pat.sub(lambda m: m.group(1) + "\n" + body + "\n" + m.group(2), text)

SIGN = re.compile(r"<!-- Neatly page:.*?-->\n")

def signpost(text):
    """Line 2 tells an agent where the content starts, so it never has to read the CSS."""
    text = SIGN.sub("", text)
    head, rest = text.split("\n", 1)
    line = (head + "\n" + rest).split("\n").index(next(l for l in rest.split("\n") if l.startswith("<body"))) + 2
    note = (f"<!-- Neatly page: your content goes in the body element, which opens on line {line}. "
            "Everything above it is the design system: leave it as it is, except the title. -->\n")
    return head + "\n" + note + rest

pages = sorted(list((SKILL / "layouts").glob("*.html")) + list((ROOT / "examples").glob("*.html")) + list((ROOT / "site").glob("*.html")))
for p in pages:
    t = p.read_text(encoding="utf-8")
    n = inject(inject(t, "neatly.css", CSS), "neatly.js", JS)
    n = signpost(n)
    if n != t:
        p.write_text(n, encoding="utf-8")
        print("updated", p.relative_to(ROOT))
print(f"{len(pages)} pages checked")
