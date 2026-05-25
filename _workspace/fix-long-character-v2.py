#!/usr/bin/env python3
"""
Bulk fix fictional character "Long" → "bạn"/"mình" theo context.
Audit miss được vì grep cũ chỉ kiểm Mai/longshop.

Patterns replace:
- "Long bắt tay" → "Bạn bắt tay"
- "Long làm cùng bạn" → "Mình làm cùng bạn"  (sentence about author)
- "của Long" → "của bạn"
- "cùng Long" → "cùng bạn"
- "Long mở/đã/viết/check/deploy/debug/từng" → "Bạn ..."
- "Long ngồi/ghi" → "Bạn ngồi/ghi"
- "Long sếp" → "Sếp bạn"
- "Tình huống — Long ..." → "Tình huống — Bạn ..."
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

# Patterns: (regex, replacement) — ORDER MATTERS
PATTERNS = [
    # "Long làm cùng bạn" — Mr.Rom đồng hành, "Long" là tác giả nói chuyện
    (re.compile(r"\bLong (làm cùng bạn|cùng bạn|đồng hành|đi cùng)\b"), r"Mình \1"),

    # Subject opening sentences: "Long ..."
    (re.compile(r"\bLong (bắt tay|mở|làm|đã|viết|check|deploy|debug|từng|ngồi|ghi|là|sẽ|đang|nhận|chạy|cài|setup|push|pull|commit|merge|verify|gửi|gọi|test|fix|tạo|copy|paste|click|sửa|đọc|hỏi|trả lời|thử|thấy|nghĩ|biết|hiểu|chọn|pick|gặp|cần|muốn|phải|nên)\b"), r"Bạn \1"),

    # Possessive: "của Long" → "của bạn"
    (re.compile(r"\bcủa Long\b"), "của bạn"),

    # With Long: "cùng Long", "sau Long", "với Long"
    (re.compile(r"\b(cùng|sau|trước|với|cho|tới|đến|từ|qua|về|gửi|cho) Long\b"), r"\1 bạn"),

    # "Tình huống — Long ..." in heading
    (re.compile(r"(Tình huống[^\n]*?)\bLong\b", re.IGNORECASE), r"\1bạn"),

    # "Long là <role>" / "Long từng <action>"
    (re.compile(r"\bLong (là (?:một|một người|backend|frontend|devops|sysadmin|admin|dev|engineer))"), r"Bạn \1"),

    # "Long sếp" — fictional company hierarchy
    (re.compile(r"\bLong sếp\b"), "Sếp bạn"),

    # Standalone "Long," at start of dialogue
    (re.compile(r"^Long,\s+", re.MULTILINE), "Bạn, "),

    # Long. (period end)
    (re.compile(r"\bLong\.(?=\s|$)"), "bạn."),
]


def fix_content(content):
    original = content
    changes = []
    for pattern, replacement in PATTERNS:
        new_content, n = pattern.subn(replacement, content)
        if n > 0:
            changes.append((pattern.pattern[:50], n))
        content = new_content

    # Capitalize sentence start "bạn" → "Bạn"
    content = re.sub(r"(\.|\?|\!|\n)\s+bạn\b", lambda m: m.group(0)[:-3] + "Bạn", content)
    content = re.sub(r"^bạn\b", "Bạn", content)

    return content, changes, content != original


def main():
    # Find all .md files (skip __Ref__)
    md_files = [p for p in ROOT.rglob("*.md") if "__Ref__" not in p.parts]

    total_changed = 0
    total_subs = 0
    for path in md_files:
        try:
            content = path.read_text()
        except:
            continue

        if "Long" not in content:
            continue

        # Skip Blueprint files (they mention Long in §3.5 rule example)
        rel = str(path.relative_to(ROOT))
        if "_Blueprint" in rel:
            continue

        new_content, changes, was_changed = fix_content(content)

        if was_changed:
            path.write_text(new_content)
            total_changed += 1
            subs = sum(c[1] for c in changes)
            total_subs += subs
            print(f"✓ {rel}: {subs} subs")

    print(f"\n📊 Fixed {total_changed} files, {total_subs} total substitutions")


if __name__ == "__main__":
    main()
