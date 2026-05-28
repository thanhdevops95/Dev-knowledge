#!/usr/bin/env python3
"""
Final cleanup of remaining fictional names:
- Python lessons (Rom/Lan/Hoa in f-strings, tuples, dicts not caught by pass3)
- Web frontend lessons (Mai in JSX, JS objects)
- Anywhere else still showing Mai/Lan/Hoa/Hung/Bình/Châu

Per Blueprint v0.5.5 §3.5.
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

# Specific patterns for remaining residue
PATTERNS = [
    # ── Python f-strings ──
    (re.compile(r'f"Hello Rom!'), 'f"Hello Alice!'),
    (re.compile(r'f"Hello Lan!'), 'f"Hello Bob!'),
    (re.compile(r'f"Hello Hoa!'), 'f"Hello Charlie!'),

    # ── Python function call with args ──
    (re.compile(r'greet\("Rom",'), 'greet("Alice",'),
    (re.compile(r'greet\("Lan",'), 'greet("Bob",'),
    (re.compile(r'greet\("Hoa",'), 'greet("Charlie",'),
    (re.compile(r'\bHi Rom!'), 'Hi Alice!'),
    (re.compile(r'\bHi Lan!'), 'Hi Bob!'),
    (re.compile(r'\bHi Hoa!'), 'Hi Charlie!'),
    (re.compile(r'\bChào Rom!'), 'Chào Alice!'),
    (re.compile(r'\bChào Lan!'), 'Chào Bob!'),
    (re.compile(r'\bChào Hoa!'), 'Chào Charlie!'),

    # ── Tuples / lists ──
    (re.compile(r'\("Rom", "Lan", "Hoa", "Tom"\)'), '("Alice", "Bob", "Charlie", "Tom")'),
    (re.compile(r'\["Rom", "Lan", "Hoa", "Tom"\]'), '["Alice", "Bob", "Charlie", "Tom"]'),
    (re.compile(r'\("Rom", "Lan", "Hoa"\)'), '("Alice", "Bob", "Charlie")'),
    (re.compile(r'\["Rom", "Lan", "Hoa"\]'), '["Alice", "Bob", "Charlie"]'),
    (re.compile(r"\('Rom', 'Lan', 'Hoa'\)"), "('Alice', 'Bob', 'Charlie')"),

    # ── Comment lines ──
    (re.compile(r'# Rom, Lan, Hoa, Tom đều 3 ký tự'), '# Alice, Bob, Charlie, Tom — 5/3/7/3 ký tự'),

    # ── Equality checks ──
    (re.compile(r'name == "Rom"'), 'name == "Alice"'),
    (re.compile(r'name == "Lan"'), 'name == "Bob"'),
    (re.compile(r'name == "Hoa"'), 'name == "Charlie"'),

    # ── Dict-like patterns ──
    (re.compile(r'^Lan: (\d+)', re.MULTILINE), r'Bob: \1'),
    (re.compile(r'^Hoa: (\d+)', re.MULTILINE), r'Charlie: \1'),
    (re.compile(r'^Rom: (\d+)', re.MULTILINE), r'Alice: \1'),

    # ── JavaScript / React JSX ──
    (re.compile(r'obj\.name = "Mai";'), 'obj.name = "Bob";'),
    (re.compile(r'<Greeting name="Mai" />'), '<Greeting name="Bob" />'),
    (re.compile(r"name: 'Mai',"), "name: 'Bob',"),
    (re.compile(r"avatar: '/mai\.jpg'"), "avatar: '/bob.jpg'"),
    (re.compile(r"name: \"Mai\""), 'name: "Bob"'),

    # ── HTML/A11y story Mai character ──
    (re.compile(r"## Tình huống — Bạn viết form login, Mai bị mù bẩm sinh không dùng được"),
     "## Tình huống — Bạn viết form login, đồng nghiệp mù bẩm sinh không dùng được"),
    (re.compile(r"→ Trông OK trên Chrome\. Mai \(developer mù\) test bằng screen reader \(NVDA\):"),
     "→ Trông OK trên Chrome. Đồng nghiệp (developer mù) test bằng screen reader (NVDA):"),
    (re.compile(r"Mai bảo:"), "Họ bảo:"),
]


def main():
    md_files = []
    for p in ROOT.rglob("*.md"):
        if "__Ref__" in p.parts:
            continue
        if "_blueprint" in str(p):
            continue
        if "_workspace" in str(p):
            continue
        if "MASTER-CATALOG" in str(p):
            continue
        md_files.append(p)

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
    print(f"\n📊 Final cleanup: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
