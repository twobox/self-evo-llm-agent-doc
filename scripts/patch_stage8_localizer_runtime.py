#!/usr/bin/env python3
"""Patch the temporary Stage 8 localizer to replace only Markdown image targets."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts" / "localize_note_images.py"

OLD = '''            count = text.count(old)
            if count != 1:
                raise RuntimeError(f"expected one image reference for {old}, found {count}")
            text = text.replace(old, replacement, 1)
'''

NEW = '''            pattern = re.compile(r"(!\\[[^\\]]*\\]\\()" + re.escape(old) + r"(\\))")
            text, count = pattern.subn(
                lambda match: match.group(1) + replacement + match.group(2),
                text,
                count=1,
            )
            if count != 1:
                raise RuntimeError(f"expected one Markdown image reference for {old}, found {count}")
'''


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    if OLD not in text:
        raise RuntimeError("Stage 8 localizer replacement block was not found")
    PATH.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("Patched Stage 8 localizer to rewrite only Markdown image targets")


if __name__ == "__main__":
    main()
