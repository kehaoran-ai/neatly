#!/usr/bin/env python3
"""Build a Neatly page from a layout and the body you wrote, then check it.

    python3 make.py <layout> <body.html> <out.html> [--title "Page title"] [--accent e4572e] [--system warm] [--lang zh-CN]

<layout>    report, deck, dashboard, landing, docs or personal
--system    neatly (default), editorial, warm or night, or a path to your own .css
<body.html> the markup that goes inside <body>, nothing else
<out.html>  the page to write; it is overwritten

The design system is copied from the layout untouched. The checker runs at the
end and the exit code is the checker's.
"""
import argparse
import re
import subprocess
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAYOUTS = HERE.parent / "layouts"
SYSTEMS = HERE.parent / "systems"
SYSTEM_BLOCK = re.compile(r"(/\* neatly-system:start \*/).*?(/\* neatly-system:end \*/)", re.S)


def main():
    ap = argparse.ArgumentParser(add_help=True, usage=__doc__)
    ap.add_argument("layout")
    ap.add_argument("body")
    ap.add_argument("out")
    ap.add_argument("--title")
    ap.add_argument("--accent", help="hex colour without #, for example e4572e")
    ap.add_argument("--system", default="neatly", help="design system: neatly, " + ", ".join(p.stem for p in sorted(SYSTEMS.glob("*.css"))))
    ap.add_argument("--no-check", action="store_true", help="skip the checker (used by live previews)")
    ap.add_argument("--lang", help="page language for <html lang>, e.g. zh-CN, en, ja")
    a = ap.parse_args()

    layout = LAYOUTS / f"{a.layout}.html"
    if not layout.is_file():
        sys.exit(f"Unknown layout {a.layout!r}. Pick one of: {', '.join(p.stem for p in sorted(LAYOUTS.glob('*.html')))}")
    page = layout.read_text(encoding="utf-8")
    if a.system != "neatly":
        # A bundled system by name, or your own system file by path.
        sys_css = Path(a.system) if a.system.endswith(".css") else SYSTEMS / f"{a.system}.css"
        if not sys_css.is_file():
            sys.exit(f"Unknown design system {a.system!r}. Pick one of: neatly, {', '.join(p.stem for p in sorted(SYSTEMS.glob('*.css')))}")
        css = sys_css.read_text(encoding="utf-8").strip()
        page = SYSTEM_BLOCK.sub(lambda m: m.group(1) + "\n" + css + "\n" + m.group(2), page, count=1)
    body = Path(a.body).read_text(encoding="utf-8").strip()
    # Accept a body that still has its own <body> wrapper.
    body = re.sub(r"^\s*<body[^>]*>|</body>\s*$", "", body).strip()

    m = re.compile(r"(<body[^>]*>)(.*)(</body>)", re.S).search(page, page.index("</head>"))
    if a.accent:
        a.accent = a.accent.lstrip("#")
        if not re.fullmatch(r"[0-9a-fA-F]{3,8}", a.accent):
            sys.exit("--accent takes a hex colour without #, for example e4572e")
        body = f"<style>:root {{ --nt-accent: #{a.accent}; }}</style>\n{body}"
    page = page[:m.start()] + m.group(1) + "\n" + body + "\n" + m.group(3) + page[m.end():]
    if a.lang:
        if not re.fullmatch(r"[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*", a.lang):
            sys.exit("--lang takes a language tag such as zh-CN or en")
        page = re.sub(r'<html lang="[^"]*">', f'<html lang="{a.lang}">', page, count=1)
    if a.title:
        page = re.sub(r"<title>[^<]*</title>", lambda _: f"<title>{escape(a.title)}</title>", page, count=1)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}", flush=True)
    if a.no_check:
        return 0
    return subprocess.call([sys.executable, str(HERE / "check.py"), str(out)])


if __name__ == "__main__":
    sys.exit(main())
