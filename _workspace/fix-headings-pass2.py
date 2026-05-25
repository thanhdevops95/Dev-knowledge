#!/usr/bin/env python3
# ============================================================================
# Script    : fix-headings-pass2.py
# Purpose   : Second pass — fix awkward headings + bạn's possessive artifacts
#             created by the bulk Long→bạn replacement.
# Version   : v1.0.0
# Created   : 24/05/2026
# Author    : Mr.Rom
# ============================================================================

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")
TARGET_DIRS = [
    ROOT / "10_DevOps/kubernetes/lessons",
    ROOT / "10_DevOps/ci-cd/lessons",
    ROOT / "10_DevOps/observability/lessons",
    ROOT / "10_DevOps/iac/lessons",
    ROOT / "10_DevOps/docker/lessons",
]

# Fix "bạn's X" English possessive — convert to "X của bạn" pattern
POSSESSIVE_MAP = [
    ("bạn's multi-team setup", "multi-team setup của bạn"),
    ("bạn's full FastAPI workflow", "Full FastAPI workflow của bạn"),
    ("bạn's deploy strategy decision", "Deploy strategy decision của bạn"),
    ("bạn's full PR pipeline", "Full PR pipeline của bạn"),
    ("bạn's stack decision", "Stack decision của bạn"),
    ("bạn's k8s manifests", "K8s manifests của bạn"),
    ("bạn's Terraform", "Terraform của bạn"),
    ("Bạn's", "của bạn:"),
    ("bạn's", "của bạn"),
]


def fix_headings(text):
    # Apply possessive fixes
    for old, new in POSSESSIVE_MAP:
        text = text.replace(old, new)

    # Capitalize "bạn" at heading start: "## 🎯 bạn ..." or "## bạn ..." or "## 1️⃣ bạn ..."
    # Pattern: line starts with #, then heading prefix (emoji/text), then "bạn "
    def cap_heading(m):
        return m.group(1) + "Bạn " + m.group(2)

    text = re.sub(
        r"^(#{1,6} .{0,40}? )bạn ([a-zà-ỹđA-ZÀ-ỸĐ])",
        cap_heading,
        text,
        flags=re.MULTILINE,
    )

    # Heading starting directly with "bạn"
    text = re.sub(
        r"^(#{1,6} )bạn ",
        r"\1Bạn ",
        text,
        flags=re.MULTILINE,
    )

    # "## Tình huống — bạn" → "## Tình huống — Bạn"
    text = re.sub(
        r"(— )bạn ",
        r"\1Bạn ",
        text,
    )

    return text


def main():
    files = []
    for d in TARGET_DIRS:
        if d.exists():
            files.extend(d.rglob("*.md"))

    changed = 0
    for f in sorted(files):
        original = f.read_text(encoding="utf-8")
        new = fix_headings(original)
        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ✓ {f.relative_to(ROOT)}")
    print(f"\nDone. {changed}/{len(files)} files modified.")


if __name__ == "__main__":
    main()
