#!/usr/bin/env python3
"""
Pass 2 fix — residual 'rom' lowercase patterns missed by pass 1.

Patterns:
- `# rom` (output of echo $USER) → `# user`
- `rom@MacBook` / `rom@laptop` / `rom@<host>` → `user@<host>`
- "Linux user 'rom'" / 'Mac user "rom"' → "Linux user", "Mac user"
- `→ Users → rom → Desktop` (narrative path explanation) → `→ Users → user → Desktop`
- `1 rom  staff` (ls -l output) → `1 user  staff`
- `rom@example.com` → `dev@example.com`
- `rom@acmeshop.vn` → `dev@acmeshop.vn`
- `user="rom"` / `user: rom` → `user="alice"` / `user: alice`
- "rom@MacBook" prompt → "user@laptop"
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

PATTERNS = [
    # Comment with just "# rom" (output sample)
    (re.compile(r"^# rom$", re.MULTILINE), "# user"),

    # rom@<host> patterns
    (re.compile(r"\brom@MacBook\b"), "user@laptop"),
    (re.compile(r"\brom@example\.com\b"), "dev@example.com"),
    (re.compile(r"\brom@acmeshop\.vn\b"), "dev@acmeshop.vn"),

    # ls -l output: " N rom  staff "
    (re.compile(r"( \d+ )rom(  staff\b)"), r"\1user\2"),
    (re.compile(r"( \d+ )rom( staff\b)"), r"\1user\2"),

    # "Linux user 'rom'" / "Mac user 'rom'" / 'user "rom"'
    (re.compile(r'\b(Linux|Mac|user)\s+user\s+["\']rom["\']'), r"\1 user"),
    (re.compile(r'\buser\s+["\']rom["\']'), "user"),

    # Narrative paths
    (re.compile(r"→ Users → rom → "), "→ Users → user → "),
    (re.compile(r"từ Desktop về rom"), "từ Desktop về home"),

    # File tree comments
    (re.compile(r'home folder của user "rom"'), "home folder của user"),
    (re.compile(r'\(Linux user "rom"\)'), ""),
    (re.compile(r'\(Mac user "rom"\)'), ""),

    # ASCII tree └── rom/
    (re.compile(r"└── rom/(\s+)←(\s+)= ~\s+\(Linux user \"rom\"\)"), r"└── user/\1← \2 = ~  (Linux home folder)"),
    (re.compile(r"└── rom/(\s+)←(\s+)= ~\s+\(Mac user \"rom\"\)"), r"└── user/\1← \2 = ~  (Mac home folder)"),
    (re.compile(r"└── rom/\s+← home folder của user \"rom\" \(= ~\)"), r"└── user/   ← home folder của user (= ~)"),
    (re.compile(r"└── rom/(\s+)← home folder"), r"└── user/\1← home folder"),

    # Inline data examples in Python: user="rom"
    (re.compile(r'user="rom"'), 'user="alice"'),
    (re.compile(r'user: rom\b'), 'user: alice'),
    (re.compile(r'email rom@example\.com'), 'email dev@example.com'),
    (re.compile(r'email: rom@example\.com'), 'email: dev@example.com'),
    (re.compile(r'"rom@example\.com"'), '"dev@example.com"'),

    # Helm/k8s email
    (re.compile(r'email: rom@acmeshop\.vn'), 'email: dev@acmeshop.vn'),

    # Docker LABEL maintainer
    (re.compile(r'maintainer="rom@example\.com"'), 'maintainer="dev@example.com"'),
    (re.compile(r'maintainer="rom@'), 'maintainer="dev@'),

    # Prompt at top of file
    (re.compile(r'^rom@MacBook'), "user@laptop"),

    # Table cell: | `rom` | User name |
    (re.compile(r"\| `rom` \| User name"), "| `user` | User name"),
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
    print(f"\n📊 Pass 2: {fixed} files, {total} replacements")


if __name__ == "__main__":
    main()
