#!/usr/bin/env python3
"""Assemble the demo site into dist/ (deployed to neatly.kehaoran.ai).

    python3 scripts/build.py && python3 scripts/site.py
    wrangler pages deploy dist --project-name neatly --branch main

dist/ holds the site's front page, the five examples and the five starting
layouts, all single files, so every page on the site is exactly what the
skill produces.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

shutil.rmtree(DIST, ignore_errors=True)
shutil.copytree(ROOT / "site", DIST)
shutil.copytree(ROOT / "examples", DIST / "examples")
shutil.copytree(ROOT / "skills" / "neatly" / "layouts", DIST / "layouts")
for f in sorted(DIST.rglob("*")):
    if f.is_file():
        print(f.relative_to(DIST))
