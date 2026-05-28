#!/usr/bin/env python3
# ============================================================================
# Script    : fix-long-character.py
# Purpose   : Bulk-fix "Long" character + "Mai" colleague + "longshop" brand
#             across DevOps lesson files. Replace with generic "bạn"/"team"
#             style and "Acme Shop" brand. Protect technical English terms.
# Version   : v1.0.0
# Created   : 24/05/2026
# Updated   : 24/05/2026
# Author    : Mr.Rom
# ============================================================================

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")
TARGET_DIRS = [
    ROOT / "10_devops/kubernetes/lessons",
    ROOT / "10_devops/ci-cd/lessons",
    ROOT / "10_devops/observability/lessons",
    ROOT / "10_devops/iac/lessons",
    ROOT / "10_devops/docker/lessons",
]

# Technical English terms that contain "long" — MUST NOT be touched
# Use unique placeholders before transformation, restore after
PROTECTED = [
    "Long Polling", "long polling",
    "Long-lived", "long-lived", "Long lived", "long lived",
    "Long-Term", "Long Term", "long-term", "long term", "Long-term",
    "Long-running", "long-running", "Long running", "long running",
    "Long-Lived", "Longest", "longest",
]

# Brand renames: longshop → acmeshop (all variants)
BRAND_MAP = [
    ("longshop.vn", "acmeshop.vn"),
    ("longshop-tf-state", "acmeshop-tf-state"),
    ("longshop-prod", "acmeshop-prod"),
    ("longshop-staging", "acmeshop-staging"),
    ("longshop-dev", "acmeshop-dev"),
    ("longshop/", "acmeshop/"),
    ("LongShop", "AcmeShop"),
    ("Longshop", "Acmeshop"),
    ("Long Shop", "Acme Shop"),
    ("longshop", "acmeshop"),
    ("long-shop", "acme-shop"),
    ("github.com/long/", "github.com/acme/"),
    ("hub.docker.com/u/long", "hub.docker.com/u/acme"),
    ("/long/myapp", "/acme/myapp"),
]

# Character "Long" — replace as subject/possessive
# Order matters: longer phrases first
CHARACTER_MAP = [
    # Meta-references to story arc
    ("Long story arc", "story arc"),
    ("Long story", "story arc"),
    ("Long ship", "Bạn ship"),
    # Possessive / object forms
    (" của Long.", " của bạn."),
    (" của Long,", " của bạn,"),
    (" của Long ", " của bạn "),
    (" của Long)", " của bạn)"),
    ("của Long:", "của bạn:"),
    ("cho Long ", "cho bạn "),
    ("cho Long.", "cho bạn."),
    ("cho Long,", "cho bạn,"),
    ("với Long ", "với bạn "),
    ("với Long.", "với bạn."),
    ("với Long,", "với bạn,"),
    ("tới Long ", "tới bạn "),
    ("đến Long ", "đến bạn "),
    ("như Long ", "như bạn "),
    # Parenthetical "(và bạn)" pattern — keep as is, just remove Long
    ("Long (và bạn)", "Bạn"),
    ("(và Long)", ""),
    # Subject "Long " at sentence start (after period, exclamation, or newline)
    # Will use regex below
]

# "Mai" colleague — replace with "đồng nghiệp" / "Bạn cùng team"
MAI_MAP = [
    ("Mai pull về máy không chạy", "đồng nghiệp pull về máy không chạy"),
    ("Mai pull về", "đồng nghiệp pull về"),
    ("Mai bị", "đồng nghiệp bị"),
    ("Mai join", "đồng nghiệp join"),
    ("Mai đã join", "đồng nghiệp đã join"),
    ("Mai chưa", "đồng nghiệp chưa"),
    ("Mai dùng", "đồng nghiệp dùng"),
    ("Mai mở", "đồng nghiệp mở"),
    ("Mai cài", "đồng nghiệp cài"),
    ("Mai vào", "đồng nghiệp vào"),
    ("Mai run", "đồng nghiệp run"),
    ("Mai sợ", "đồng nghiệp ngại"),
    ("Mai upgrade", "đồng nghiệp upgrade"),
    ("Mai gặp", "đồng nghiệp gặp"),
    ("Mai sẽ", "đồng nghiệp sẽ"),
    ("Mai là", "đồng nghiệp là"),
    ("Mai cùng", "đồng nghiệp cùng"),
    ("Mai onboard", "đồng nghiệp onboard"),
    ("máy Mai ", "máy đồng nghiệp "),
    ("máy Mai.", "máy đồng nghiệp."),
    ("máy Mai,", "máy đồng nghiệp,"),
    ("Mai (", "đồng nghiệp ("),
    ("Mai —", "đồng nghiệp —"),
    ("Mai,", "đồng nghiệp,"),
    ("Mai.", "đồng nghiệp."),
    ("Mai:", "đồng nghiệp:"),
    ("Mai ", "đồng nghiệp "),
    ("của Mai", "của đồng nghiệp"),
    ("**Mai**", "**đồng nghiệp**"),
    ("Mai**", "đồng nghiệp**"),
]


def protect(text):
    """Replace PROTECTED terms with unique placeholders."""
    placeholders = {}
    for i, term in enumerate(PROTECTED):
        placeholder = f"\x00PROTECT{i}\x00"
        if term in text:
            text = text.replace(term, placeholder)
            placeholders[placeholder] = term
    return text, placeholders


def unprotect(text, placeholders):
    """Restore PROTECTED terms from placeholders."""
    for placeholder, original in placeholders.items():
        text = text.replace(placeholder, original)
    return text


def transform(text):
    text, placeholders = protect(text)

    # Brand replacements
    for old, new in BRAND_MAP:
        text = text.replace(old, new)

    # Mai colleague
    for old, new in MAI_MAP:
        text = text.replace(old, new)

    # Long character (literal patterns)
    for old, new in CHARACTER_MAP:
        text = text.replace(old, new)

    # Any remaining standalone "Long" → "bạn" (lowercase)
    # Then post-process to capitalize at sentence starts
    text = re.sub(r"\bLong\b", "bạn", text)

    # Capitalize "bạn" / "đồng nghiệp" at sentence starts
    # Sentence start = beginning of text, after newline, or after .!?:
    def cap_word(word):
        if word == "bạn":
            return "Bạn"
        if word == "đồng":
            return "Đồng"
        return word

    text = re.sub(
        r"(^|\n|[.!?]\s+|^[-*]\s+|\n[-*]\s+)(bạn|đồng)(\b)",
        lambda m: m.group(1) + cap_word(m.group(2)) + m.group(3),
        text,
        flags=re.MULTILINE,
    )

    # Fix mid-sentence "Bạn" → "bạn" (when not at sentence start)
    # Negative lookbehind: not preceded by sentence-starter
    text = re.sub(
        r"(?<=[a-zà-ỹđ,;) ]) Bạn(?= [a-zà-ỹđ])",
        " bạn",
        text,
    )

    text = unprotect(text, placeholders)
    return text


def main():
    files = []
    for d in TARGET_DIRS:
        if d.exists():
            files.extend(d.rglob("*.md"))

    print(f"Found {len(files)} markdown files in scope")
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
