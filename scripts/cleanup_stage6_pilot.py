#!/usr/bin/env python3
"""Remove duplicate horizontal rules introduced by the Stage 6 pilot migration."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "notes" / "agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md",
    ROOT / "notes" / "evolver-self-evolving-llm-agents-through-an-experience-driven-lifecycle.md",
    ROOT / "notes" / "on-the-limits-of-llm-adaptability-impact-of-model-internalized-priors-on-annotation-task-performance.md",
]

for path in FILES:
    text = path.read_text(encoding="utf-8")
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\n---\n\s*\n---\n", "\n---\n", text)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

print("Cleaned duplicate horizontal rules in Stage 6 pilot notes")
