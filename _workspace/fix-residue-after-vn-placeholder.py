#!/usr/bin/env python3
"""
Fix residue patterns after Alice/Bob/etc → Nguyen Van A/Le Van B replacement:

1. Emails: long@ex.com → nguyenvana@ex.com (and lan@/chau@/duc@ leftovers)
2. UPPER() output: LONG → NGUYEN VAN A
3. LIKE patterns referencing fictional names: '%long%', '%alice%' → '%nguyen%'
4. Orphan "bạn" / "Bạn" still acting as user-1 name in SQL output → "Nguyen Van A"
5. "1 | bạn |" table cells → "1 | Nguyen Van A |"
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

SKIP = ("__Ref__", "_blueprint", "_workspace", "MASTER-CATALOG", "language/vietnamese")

PATTERNS = [
    # ── Emails with old name prefixes ──
    (re.compile(r"'long@ex\.com'"), "'nguyenvana@ex.com'"),
    (re.compile(r"long@ex\.com"), "nguyenvana@ex.com"),
    (re.compile(r"'lan@ex\.com'"), "'phamvand@ex.com'"),
    (re.compile(r"lan@ex\.com"), "phamvand@ex.com"),
    (re.compile(r"'chau@ex\.com'"), "'vuvanf@ex.com'"),
    (re.compile(r"chau@ex\.com"), "vuvanf@ex.com"),
    (re.compile(r"'duc@ex\.com'"), "'buivang@ex.com'"),
    (re.compile(r"duc@ex\.com"), "buivang@ex.com"),

    # ── UPPER() output residue ──
    (re.compile(r"\| LONG\b"), "| NGUYEN VAN A"),
    (re.compile(r"name_upper\s*\n[-+\s|]+\n([^\n]+)\| LONG"), r"name_upper\n-----------\n\1| NGUYEN VAN A"),

    # ── LIKE patterns with fictional names ──
    (re.compile(r"LIKE\s+'%long%'"), "LIKE '%nguyen%'"),
    (re.compile(r"ILIKE\s+'%long%'"), "ILIKE '%nguyen%'"),
    (re.compile(r"ILIKE\s+'%alice%'"), "ILIKE '%nguyen%'"),
    (re.compile(r"LIKE\s+'%alice%'"), "LIKE '%nguyen%'"),
    (re.compile(r"LOWER\('%long%'\)"), "LOWER('%nguyen%')"),
    (re.compile(r"LOWER\('%alice%'\)"), "LOWER('%nguyen%')"),

    # ── Orphan "bạn"/"Bạn" as user-1 name in SQL output rows ──
    # " 1 | bạn |" pattern (table cells, narrow column)
    (re.compile(r"(\| 1 \| )bạn(\s+\|)"), r"\1Nguyen Van A\2"),
    (re.compile(r"(\|\s+1\s+\| )bạn(\s+\|)"), r"\1Nguyen Van A\2"),
    # "1 | bạn |" without spaces
    (re.compile(r"^(\s*1\s*\|\s*)bạn(\s*\|)", re.MULTILINE), r"\1Nguyen Van A\2"),

    # Aligned table cell where "bạn" is name column (5+ wide)
    # " bạn      | long@ex.com" - narrow context
    (re.compile(r"^(\s*)bạn(\s+\|\s+)nguyenvana@", re.MULTILINE), r"\1Nguyen Van A\2nguyenvana@"),
    (re.compile(r"^bạn(\s+\|\s+)(28|2[0-9])(\s+\|)", re.MULTILINE), r"Nguyen Van A\1\2\3"),
]


def should_skip(path: Path) -> bool:
    s = str(path)
    for tag in SKIP:
        if tag in s:
            return True
    return False


def main():
    md_files = [p for p in ROOT.rglob("*.md") if not should_skip(p)]

    total = 0
    fixed = 0
    for path in md_files:
        try:
            text = path.read_text()
        except:
            continue
        orig = text
        file_n = 0
        for pat, rep in PATTERNS:
            text, n = pat.subn(rep, text)
            file_n += n
        if text != orig:
            path.write_text(text)
            fixed += 1
            total += file_n
            print(f"✓ {path.relative_to(ROOT)}: {file_n} subs")
    print(f"\n📊 Residue fix: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
