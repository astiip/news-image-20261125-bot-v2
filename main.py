"""Entrypoint for The Wednesday Herald (news-image-20261125 v2).

Renders the page with render.py, keeps entry.png in this repo, and
also copies it to MAKEFUN_OUTPUT_DIR. That variable may name a
directory (``out``) or a file path (``/output/entry.png``); the
default is /output/entry.png.
"""

import os
import shutil
from pathlib import Path

import render


def main():
    rendered = render.main()
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    target = Path(raw)
    if target.suffix.lower() != ".png":
        target = target / "entry.png"
    if target.resolve() != rendered.resolve():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(rendered, target)
    print(f"wrote {rendered} ({rendered.stat().st_size} bytes)")
    print(f"copied to {target}")
    return target


if __name__ == "__main__":
    main()
