#!/usr/bin/env python3
"""
Pass 3 — Replace capitalized Vietnamese names "Rom"/"Lan"/"Hoa" in code samples
→ International placeholder Alice/Bob/Charlie.

Per Blueprint §3.5 v0.5.5: KHÔNG tên riêng. Alice/Bob/Charlie là chuẩn international
placeholder không phải tên cá nhân thật.

Be careful: "Rom" in chrome ROM, "Rom" in "from" (already handled by \b), etc.
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

# Order matters
PATTERNS = [
    # Greet examples - "Hello Rom" / "Hello Lan" / "Hello Hoa"
    (re.compile(r'"Hello Rom!"'), '"Hello Alice!"'),
    (re.compile(r'"Hello Lan!"'), '"Hello Bob!"'),
    (re.compile(r'"Hello Hoa!"'), '"Hello Charlie!"'),
    (re.compile(r'"Hello Rom"'), '"Hello Alice"'),
    (re.compile(r'"Hello Lan"'), '"Hello Bob"'),
    (re.compile(r'"Hello Hoa"'), '"Hello Charlie"'),

    # Dict/object name field
    (re.compile(r'"name": "Rom"'), '"name": "Alice"'),
    (re.compile(r'"name": "Lan"'), '"name": "Bob"'),
    (re.compile(r'"name": "Hoa"'), '"name": "Charlie"'),
    (re.compile(r"'name': 'Rom'"), "'name': 'Alice'"),
    (re.compile(r"'name': 'Lan'"), "'name': 'Bob'"),
    (re.compile(r"'name': 'Hoa'"), "'name': 'Charlie'"),

    # Function call greet("Rom")
    (re.compile(r'greet\("Rom"\)'), 'greet("Alice")'),
    (re.compile(r'greet\("Lan"\)'), 'greet("Bob")'),
    (re.compile(r'greet\("Hoa"\)'), 'greet("Charlie")'),

    # Lists of names
    (re.compile(r'\["Rom", "Lan", "Hoa"\]'), '["Alice", "Bob", "Charlie"]'),
    (re.compile(r"\['Rom', 'Lan', 'Hoa'\]"), "['Alice', 'Bob', 'Charlie']"),

    # Variable assignments name = "Rom"/"Lan"/"Hoa"
    (re.compile(r'(name|user_name|first_name)\s*=\s*"Rom"'), r'\1 = "Alice"'),
    (re.compile(r'(name|user_name|first_name)\s*=\s*"Lan"'), r'\1 = "Bob"'),
    (re.compile(r'(name|user_name|first_name)\s*=\s*"Hoa"'), r'\1 = "Charlie"'),

    # In comments / output samples
    (re.compile(r'# Hello Rom!'), '# Hello Alice!'),
    (re.compile(r'# Hello Lan!'), '# Hello Bob!'),
    (re.compile(r'# Hello Hoa!'), '# Hello Charlie!'),

    # create_user(name="Rom", ...)
    (re.compile(r'name="Rom"'), 'name="Alice"'),
    (re.compile(r'name="Lan"'), 'name="Bob"'),
    (re.compile(r'name="Hoa"'), 'name="Charlie"'),

    # f-string examples
    (re.compile(r'\bRom!"'), 'Alice!"'),

    # Output sample mid-text
    (re.compile(r'\| `name` \| `"Rom"`'), '| `name` | `"Alice"`'),
]


def main():
    md_files = []
    for p in ROOT.rglob("*.md"):
        if "__Ref__" in p.parts:
            continue
        if "_Blueprint" in str(p):
            continue
        if "_workspace" in str(p):
            continue
        if "MASTER-CATALOG" in str(p):
            continue
        if "language/vietnamese" in str(p):
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
    print(f"\n📊 Pass 3: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
