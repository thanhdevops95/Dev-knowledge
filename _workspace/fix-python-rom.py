#!/usr/bin/env python3
"""
Aggressive replace of remaining "Rom" instances in Python lessons.
Only affects 03_Languages/python/lessons/ where Rom is used as code sample data.

Per Blueprint v0.5.5 §3.5: KHÔNG tên riêng. Use Alice/Bob/Charlie standard.
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge/03_Languages/python/lessons")

# Whole-word "Rom" → "Alice" — context-aware
# But we must NOT touch "Mr.Rom" (author signature)
PATTERNS = [
    # Quoted strings (most safe)
    (re.compile(r'"Rom"'), '"Alice"'),
    (re.compile(r"'Rom'"), "'Alice'"),
    # In output/comments (Rom followed by , ! or end of line)
    (re.compile(r'\bRom!'), 'Alice!'),
    (re.compile(r'\bRom\b(?![a-zA-Z\.])'), 'Alice'),  # word boundary, not followed by . (Mr.Rom)
    # "Lan", "Hoa"
    (re.compile(r'"Lan"'), '"Bob"'),
    (re.compile(r"'Lan'"), "'Bob'"),
    (re.compile(r'"Hoa"'), '"Charlie"'),
    (re.compile(r"'Hoa'"), "'Charlie'"),
    (re.compile(r'\bLan\b'), 'Bob'),
    (re.compile(r'\bHoa\b'), 'Charlie'),
]


def main():
    md_files = list(ROOT.rglob("*.md"))
    total = 0
    for path in md_files:
        text = path.read_text()
        orig = text
        file_n = 0
        for pat, rep in PATTERNS:
            text, n = pat.subn(rep, text)
            file_n += n
        if text != orig:
            path.write_text(text)
            total += file_n
            print(f"✓ {path.relative_to(ROOT.parent.parent.parent)}: {file_n} subs")
    print(f"\n📊 Python Rom cleanup: {total} replacements")


if __name__ == "__main__":
    main()
