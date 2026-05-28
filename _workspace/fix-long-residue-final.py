#!/usr/bin/env python3
"""
Final cleanup of "long" residue from old fictional character bulk-fix:
- Email: long@example.com / long@acmeshop.vn → nguyenvana@*
- SSH/host: long@vps / long@laptop / long@MacBook → user@*
- Path: /Users/long/ → /Users/user/
- Brand: longshop / Long Shop / pg-longshop → acmeshop / Acme Shop / pg-acmeshop
- psql: psql -U longshop / \c longshop → -U acmeshop / \c acmeshop
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

SKIP = ("__Ref__", "_blueprint", "_workspace", "MASTER-CATALOG", "language/vietnamese", "WIP-TRACKER")

PATTERNS = [
    # ── Email patterns ──
    (re.compile(r'\blong@example\.com\b'), 'nguyenvana@example.com'),
    (re.compile(r'\blong@acmeshop\.vn\b'), 'nguyenvana@acmeshop.vn'),
    (re.compile(r'\blong@gmail\.com\b'), 'nguyenvana@gmail.com'),

    # ── SSH/hostname patterns ──
    (re.compile(r'\blong@vps([0-9]?)\b'), r'user@vps\1'),
    (re.compile(r'\blong@laptop\b'), 'user@laptop'),
    (re.compile(r'\blong@MacBook\b'), 'user@laptop'),
    (re.compile(r'\blong@macbook\b'), 'user@laptop'),
    (re.compile(r'\blong@server\b'), 'user@server'),
    (re.compile(r'\blong@host\b'), 'user@host'),
    # ssh long@hostname.foo
    (re.compile(r'ssh long@([a-z0-9._-]+)'), r'ssh user@\1'),

    # ── Path patterns ──
    (re.compile(r'/Users/long/'), '/Users/user/'),
    (re.compile(r'/home/long/'), '/home/user/'),
    (re.compile(r'/Users/long\b'), '/Users/user'),
    (re.compile(r'/home/long\b'), '/home/user'),

    # ── GitHub URL ──
    (re.compile(r'github\.com/long/'), 'github.com/acmeshop/'),
    (re.compile(r'github\.com/long\b'), 'github.com/acmeshop'),

    # ── Brand patterns ──
    (re.compile(r'\bpg-longshop\b'), 'pg-acmeshop'),
    (re.compile(r'\blongshop\b'), 'acmeshop'),
    (re.compile(r'\bLongshop\b'), 'Acmeshop'),
    (re.compile(r'Long Shop\b'), 'Acme Shop'),

    # ── psql/database name ──
    (re.compile(r'-U longshop'), '-U acmeshop'),
    (re.compile(r'\\c longshop'), r'\\c acmeshop'),
    (re.compile(r'database longshop'), 'database acmeshop'),
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
    print(f"\n📊 Long residue final cleanup: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
