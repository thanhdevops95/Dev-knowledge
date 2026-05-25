#!/usr/bin/env python3
# ============================================================================
# Script    : fix-awkward-pass3.py
# Purpose   : Fix awkward patterns from previous bulk replacements:
#             - "Sau bài này Bạn" → "Sau bài này bạn" (mid-clause)
#             - English-style possessive "của Bạn X" → "X của bạn"
#             - "Bạn write" → "Bạn viết" (fix Anglicized verbs)
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

# Direct heading replacements
HEADING_FIXES = [
    # mid-clause "Bạn" → "bạn"
    ("Sau bài này Bạn sẽ", "Sau bài này bạn sẽ"),

    # English-style possessive at heading start — restructure
    ("## 9️⃣ của Bạn first CI/CD", "## 9️⃣ Pipeline CI/CD đầu tiên của bạn"),
    ("## 9️⃣ của Bạn structure", "## 9️⃣ Structure của bạn"),
    ("## 9️⃣ của Bạn production setup", "## 9️⃣ Production setup của bạn"),
    ("## 1️⃣0️⃣ của Bạn full setup", "## 1️⃣0️⃣ Full setup của bạn"),
    ("## 1️⃣1️⃣ của Bạn production setup — Summary", "## 1️⃣1️⃣ Production setup của bạn — Summary"),
    ("## 1️⃣5️⃣ của Bạn first real Terraform — AWS VPC + EC2", "## 1️⃣5️⃣ Real Terraform đầu tiên của bạn — AWS VPC + EC2"),
    ("## 8️⃣ Production setup — của Bạn stack", "## 8️⃣ Production setup — Stack của bạn"),
    ("### của Bạn setup", "### Setup của bạn"),

    # Anglicized verbs after "Bạn" → Vietnamese verb
    ("Bạn write GitLab pipeline", "Bạn viết GitLab pipeline"),

    # Awkward Bạn at start of section that's actually a step
    ("## 8️⃣ Bạn expose FastAPI + React production", "## 8️⃣ Expose FastAPI + React production"),
    ("## 8️⃣ Bạn install observability stack", "## 8️⃣ Cài observability stack"),
    ("## 9️⃣ Bạn deploy FastAPI lên kind", "## 9️⃣ Hands-on — Deploy FastAPI lên kind"),
    ("## 9️⃣ Bạn deploy FastAPI production-grade", "## 9️⃣ Hands-on — Deploy FastAPI production-grade"),
    ("## 9️⃣ Bạn apply config + secrets cho FastAPI", "## 9️⃣ Hands-on — Apply config + secrets cho FastAPI"),

    # CI/CD specific
    ("## 1️⃣2️⃣ Bạn write GitLab pipeline tương đương", "## 1️⃣2️⃣ Hands-on — Viết GitLab pipeline tương đương"),

    # IaC heading where "Bạn" feels like awkward subject of imperative
    # (leave the ones that make sense as actor)
]

# Generic regex fixes
GENERIC_FIXES = [
    # "Bạn write" mid-content → "Bạn viết"
    (r"\bBạn write\b", "Bạn viết"),
    # Awkward "của Bạn" mid-sentence → "của bạn"
    (r"\bcủa Bạn\b(?!'s)", "của bạn"),
    (r"\bcho Bạn\b", "cho bạn"),
    (r"\bvới Bạn\b", "với bạn"),
    (r"\btới Bạn\b", "tới bạn"),
    (r"\bđến Bạn\b", "đến bạn"),
]


def transform(text):
    for old, new in HEADING_FIXES:
        text = text.replace(old, new)
    for pattern, replacement in GENERIC_FIXES:
        text = re.sub(pattern, replacement, text)
    return text


def main():
    files = []
    for d in TARGET_DIRS:
        if d.exists():
            files.extend(d.rglob("*.md"))

    changed = 0
    for f in sorted(files):
        original = f.read_text(encoding="utf-8")
        new = transform(original)
        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ✓ {f.relative_to(ROOT)}")
    print(f"\nDone. {changed}/{len(files)} files modified.")


if __name__ == "__main__":
    main()
