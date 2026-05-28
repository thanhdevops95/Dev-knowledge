#!/usr/bin/env python3
"""
Fix SQL fundamentals lesson files: replace Vietnamese names in table data
→ international placeholders (Alice/Bob/Charlie/David/Eve/Frank/Grace).

Per Blueprint §3.5 v0.5.5: KHÔNG tên riêng. Names are needed as table data,
use international standard placeholders.

Mapping (consistent across all SQL lessons):
  user 1 'bạn' → 'Alice'
  Mai → Bob
  Hùng → Charlie
  Lan → David
  Bình → Eve
  Châu → Frank
  Đức → Grace
"""

import re
from pathlib import Path

FILES = [
    "06_databases/sql-fundamentals/lessons/01_basic/00_what-is-sql.md",
    "06_databases/sql-fundamentals/lessons/01_basic/01_select-and-filter.md",
    "06_databases/sql-fundamentals/lessons/01_basic/02_aggregations.md",
    "06_databases/sql-fundamentals/lessons/01_basic/03_joins.md",
    "06_databases/sql-fundamentals/lessons/01_basic/04_insert-update-delete.md",
    "06_databases/sql-fundamentals/lessons/01_basic/05_schema-design-basics.md",
]

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

# Patterns ordered so longer/safer ones come first.
# IMPORTANT: do NOT replace "bạn" globally — that's 2nd-person pronoun.
# Only replace "bạn" in known table contexts.
PATTERNS = [
    # ── SQL string literals (single-quoted, inside INSERT) ──
    (re.compile(r"'Mai'"), "'Bob'"),
    (re.compile(r"'Hùng'"), "'Charlie'"),
    (re.compile(r"'Lan'"), "'David'"),
    (re.compile(r"'Bình'"), "'Eve'"),
    (re.compile(r"'Châu'"), "'Frank'"),
    (re.compile(r"'Đức'"), "'Grace'"),

    # ── Email examples specific to names ──
    (re.compile(r"'lan@ex\.com'"), "'david@ex.com'"),
    (re.compile(r"'chau@ex\.com'"), "'frank@ex.com'"),
    (re.compile(r"'duc@ex\.com'"), "'grace@ex.com'"),

    # ── Output rows (table-formatted, names followed by spaces and |) ──
    # Run replace on full-word boundaries
    (re.compile(r"\bMai\b"), "Bob"),
    (re.compile(r"\bHùng\b"), "Charlie"),
    (re.compile(r"\bLan\b"), "David"),
    (re.compile(r"\bBình\b(?!\s+thường)"), "Eve"),  # avoid "Bình thường" idiom
    (re.compile(r"\bChâu\b"), "Frank"),
    (re.compile(r"\bĐức\b"), "Grace"),

    # ── 'MAI' uppercased ──
    (re.compile(r"\bMAI\b"), "BOB"),

    # ── 'bạn' as user-1 name in table output rows ──
    # Only in clear table contexts: "bạn  |" or "bạn |" or "(bạn,"
    (re.compile(r"'bạn'"), "'Alice'"),
    # Table rows like "Bạn   | Mai" or "Bạn | Hanoi"
    (re.compile(r"^Bạn(\s+\|)", re.MULTILINE), r"Alice\1"),
    (re.compile(r"\| 1 \| Bạn"), "| 1 | Alice"),
    (re.compile(r"\(1, 'bạn'"), "(1, 'Alice'"),

    # ── '→ Bạn, Mai, Lan có order' ── (specific phrase referring to row data)
    (re.compile(r"→ Bạn, Bob, David có order\."), "→ Alice, Bob, David có order."),
    (re.compile(r"→ Bạn, Mai, Lan có order\."), "→ Alice, Bob, David có order."),

    # ── '(bạn, Mai)' style row pair refs ──
    (re.compile(r"\(bạn, Bob\)"), "(Alice, Bob)"),
    (re.compile(r"\(Bob, bạn\)"), "(Bob, Alice)"),
    (re.compile(r"`\(bạn, Bob\)`"), "`(Alice, Bob)`"),
    (re.compile(r"`\(Bob, bạn\)`"), "`(Bob, Alice)`"),

    # ── LIKE pattern explanations ──
    # '%a%' Mai, Lan, Bình, Châu → patterns may break with new names
    # We'll regenerate LIKE pattern table entries manually via separate edits
]


def main():
    total = 0
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"⚠️  Missing: {rel}")
            continue
        text = path.read_text()
        orig = text
        file_n = 0
        for pat, rep in PATTERNS:
            text, n = pat.subn(rep, text)
            file_n += n
        if text != orig:
            path.write_text(text)
            total += file_n
            print(f"✓ {rel}: {file_n} subs")
    print(f"\n📊 SQL names fix: {total} replacements")


if __name__ == "__main__":
    main()
