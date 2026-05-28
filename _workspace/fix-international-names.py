#!/usr/bin/env python3
"""
Replace international placeholder names (Alice/Bob/Charlie/David/Eve/Frank/Grace)
→ Vietnamese placeholder convention (Nguyen Van A/Le Van B/Tran Van C/...)

Per Blueprint v0.5.7 §3.5: KHÔNG tên riêng bất kể ngôn ngữ.
User feedback (24/05/2026):
> "hạn chế dùng tên riêng, thôi không phải tiếng việt, bên dùng bạn, đồng nghiệp...
> Còn các ví dụ cần tên thì bạn A bạn B Nguyen Van A Le Van B Tran Van C kiểu vậy"

Mapping:
  Alice    → Nguyen Van A
  Bob      → Le Van B
  Charlie  → Tran Van C
  David    → Pham Van D
  Eve      → Hoang Van E
  Frank    → Vu Van F
  Grace    → Bui Van G

  Lowercase versions (in emails, URLs):
  alice    → nguyenvana
  bob      → levanb
  charlie  → tranvanc
  david    → phamvand
  eve      → hoangvane
  frank    → vuvanf
  grace    → buivang
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

# Skip these directories
SKIP_DIRS = ("__Ref__", "_blueprint", "_workspace", "language/vietnamese")

# Mapping (longest first to avoid prefix collision)
NAME_MAP = [
    ("Charlie", "Tran Van C"),
    ("Alice",   "Nguyen Van A"),
    ("David",   "Pham Van D"),
    ("Frank",   "Vu Van F"),
    ("Grace",   "Bui Van G"),
    ("Bob",     "Le Van B"),
    ("Eve",     "Hoang Van E"),
]

LOWER_MAP = [
    ("charlie", "tranvanc"),
    ("alice",   "nguyenvana"),
    ("david",   "phamvand"),
    ("frank",   "vuvanf"),
    ("grace",   "buivang"),
    ("bob",     "levanb"),
    ("eve",     "hoangvane"),
]

# Patterns
PATTERNS = []
for old, new in NAME_MAP:
    # Whole word match — but NOT inside larger words (e.g., "Alicea", "BobCat")
    # Use word boundary
    PATTERNS.append((re.compile(rf'\b{old}\b'), new))

for old, new in LOWER_MAP:
    # Lowercase versions appear in emails (alice@ex.com) and URLs
    PATTERNS.append((re.compile(rf'\b{old}\b(?=@|\.com|\.vn|\.jpg|\.png|/)'), new))


def should_skip(path: Path) -> bool:
    s = str(path)
    for skip in SKIP_DIRS:
        if skip in s:
            return True
    return False


def main():
    md_files = []
    for p in ROOT.rglob("*.md"):
        if should_skip(p):
            continue
        if "MASTER-CATALOG" in p.name:
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
    print(f"\n📊 International names → VN placeholder: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
