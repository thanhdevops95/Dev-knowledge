#!/usr/bin/env python3
# ============================================================================
# Script    : fix-meta-files.py
# Purpose   : Replace "Long story arc" / "Long " character refs in
#             MASTER-CATALOG.md and WIP-TRACKER.md changelog entries.
# Version   : v1.0.0
# Created   : 24/05/2026
# Author    : Mr.Rom
# ============================================================================

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")
FILES = [
    ROOT / "MASTER-CATALOG.md",
    ROOT / "_workspace/WIP-TRACKER.md",
]

PROTECTED = [
    "Long Polling", "long polling",
    "Long-lived", "long-lived", "Long lived", "long lived",
    "Long-Term", "Long Term", "long-term", "long term", "Long-term",
    "Long-running", "long-running", "Long running", "long running",
]

REPLACEMENTS = [
    ('"Long story arc"', "story arc"),
    ("Long story arc", "story arc"),
    ("Long story", "story arc"),
    ("Long debug", "bạn debug"),
    ("Long đổi", "bạn đổi"),
    ("Long mua", "bạn mua"),
    ("Long quản lý", "bạn quản lý"),
    ("Long ship", "bạn ship"),
    ("Long viết", "bạn viết"),
    ("Long deploy", "bạn deploy"),
    ("Long join", "bạn join"),
    ("Long phải", "bạn phải"),
    ("Mai pull", "đồng nghiệp pull"),
    ("Mai mù", "đồng nghiệp"),
    ("Long ", "bạn "),
    ("Mai ", "đồng nghiệp "),
]


def protect(text):
    placeholders = {}
    for i, term in enumerate(PROTECTED):
        ph = f"\x00P{i}\x00"
        if term in text:
            text = text.replace(term, ph)
            placeholders[ph] = term
    return text, placeholders


def unprotect(text, placeholders):
    for ph, original in placeholders.items():
        text = text.replace(ph, original)
    return text


def transform(text):
    text, placeholders = protect(text)
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    text = unprotect(text, placeholders)
    return text


def main():
    for f in FILES:
        if not f.exists():
            continue
        original = f.read_text(encoding="utf-8")
        new = transform(original)
        if new != original:
            f.write_text(new, encoding="utf-8")
            print(f"  ✓ {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
