#!/usr/bin/env python3
"""
Bulk fix username/hostname fictional residue → generic.

Rule (Blueprint §3.5 v0.5.5):
- KHÔNG dùng tên riêng `rom`, `long`, `mai`, `hung` (kể cả lowercase)
- Dùng generic: `user`, `admin`, `dev`, `deploy`

Patterns to fix:
- /Users/rom/ → /Users/user/
- /home/rom/ → /home/user/
- /home/long/ → /home/user/
- chown rom → chown user
- chown long → chown user
- user rom / adduser rom → user / adduser user
- rom@laptop / rom@macbook → user@laptop
- long@laptop → user@laptop
- " rom " (in ls -l output) → " user "
- " long " (same)
- AllowUsers rom → AllowUsers user
- AllowUsers long → AllowUsers user
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

PATTERNS = [
    # Home paths
    (r"/Users/rom/", "/Users/user/"),
    (r"/Users/rom\b", "/Users/user"),
    (r"/home/rom/", "/home/user/"),
    (r"/home/rom\b", "/home/user"),
    (r"/home/long/", "/home/user/"),
    (r"/home/long\b", "/home/user"),
    (r"/home/mai/", "/home/user/"),
    (r"/home/hung/", "/home/user/"),

    # chown / chgrp
    (r"\bchown rom\b", "chown user"),
    (r"\bchown long\b", "chown user"),
    (r"\bchown -R rom\b", "chown -R user"),
    (r"\bchown -R long\b", "chown -R user"),

    # SSH connection user@host
    (r"\brom@laptop\b", "user@laptop"),
    (r"\brom@macbook\b", "user@laptop"),
    (r"\brom@server\b", "user@server"),
    (r"\bromg@", "user@"),  # typo guard
    (r"\blong@laptop\b", "user@laptop"),
    (r"\blong@macbook\b", "user@laptop"),
    (r"\blong@server\b", "user@server"),
    (r"\blong@deploy\b", "user@server"),
    (r"\bmai@", "user@"),
    (r"\bhung@", "user@"),

    # SSH config
    (r"\bAllowUsers rom\b", "AllowUsers user"),
    (r"\bAllowUsers long\b", "AllowUsers user"),
    (r"\bAllowUsers rom deploy\b", "AllowUsers user deploy"),
    (r"\bAllowUsers long deploy\b", "AllowUsers user deploy"),

    # adduser / useradd
    (r"\badduser rom\b", "adduser user"),
    (r"\buseradd rom\b", "useradd user"),
    (r"\badduser long\b", "adduser user"),
    (r"\buseradd long\b", "useradd user"),

    # ls -l output: " 1 rom admin " → " 1 user admin "
    (r"(\d+ )rom( \w+ )", r"\1user\2"),
    (r"(\d+ )long( \w+ )", r"\1user\2"),

    # Standalone "rom" / "long" in shell context (be careful)
    # Comments like "# user 'rom' login" → "# user login"
    (r"user 'rom'", "user"),
    (r"user 'long'", "user"),
    (r"user `rom`", "user"),
    (r"user `long`", "user"),

    # Possessive in narrative (already in §3.5 §3.10 fixed but residue from rom)
    (r"\bowner = rom\b", "owner = user"),
    (r"\bowner = long\b", "owner = user"),

    # `chown user:user`
    (r"\bchown rom:rom\b", "chown user:user"),
    (r"\bchown long:long\b", "chown user:user"),
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
        if "language/vietnamese" in str(p):  # may contain "rom" as part of fromVietnamese
            continue
        md_files.append(p)

    total_replacements = 0
    files_fixed = 0
    for path in md_files:
        try:
            text = path.read_text()
        except:
            continue
        orig = text
        file_changes = 0
        for pat, rep in PATTERNS:
            new_text, n = re.subn(pat, rep, text)
            if n > 0:
                file_changes += n
            text = new_text
        if text != orig:
            path.write_text(text)
            files_fixed += 1
            total_replacements += file_changes
            print(f"✓ {path.relative_to(ROOT)}: {file_changes} subs")

    print(f"\n📊 Fixed {files_fixed} files, {total_replacements} replacements")


if __name__ == "__main__":
    main()
