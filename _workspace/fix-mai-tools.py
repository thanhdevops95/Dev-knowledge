#!/usr/bin/env python3
"""
Replace Mai/Hùng/Hung fictional names in:
- 02_Tools/git-clients/ (github.md, github-desktop.md, README.md, 00_what-is-git-hosting.md)
- 04_OS/linux/ text-processing sample data

Per Blueprint v0.5.5 §3.5: KHÔNG tên riêng.
Use generic role: "đồng nghiệp" for character, "Alice/Bob" for sample data.
"""

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

# Specific files to target (avoid risky bulk replace on whole tree)
FILES = [
    "02_Tools/git-clients/github.md",
    "02_Tools/git-clients/00_what-is-git-hosting.md",
    "02_Tools/git-clients/README.md",
    "02_Tools/git-clients/github-desktop.md",
    "02_Tools/git-clients/codeberg.md",  # only if has Mai (not Đức)
    "04_OS/linux/lessons/02_intermediate/04_text-processing-advanced.md",
]

PATTERNS = [
    # ── Mai as character in narrative ──
    # "Mai (junior ...)" — descriptive
    (re.compile(r"Mai \(junior FE dev\)"), "đồng nghiệp (junior FE dev)"),
    (re.compile(r"Mai \(FE dev\)"), "Đồng nghiệp FE dev"),

    # Section headers using Mai
    (re.compile(r"## 6️⃣ Pull Request Workflow — bạn \+ Mai collab"), "## 6️⃣ Pull Request Workflow — bạn + đồng nghiệp collab"),
    (re.compile(r"### Mai làm feature mới qua PR"), "### Đồng nghiệp làm feature mới qua PR"),
    (re.compile(r"### Mai sửa theo feedback"), "### Đồng nghiệp sửa theo feedback"),
    (re.compile(r"## Tình huống — Mai sợ terminal"), "## Tình huống — Đồng nghiệp sợ terminal"),

    # Sentence-level
    (re.compile(r"setup PR workflow với Mai"), "setup PR workflow với đồng nghiệp"),
    (re.compile(r"PR workflow chi tiết với bạn\+Mai"), "PR workflow chi tiết với bạn+đồng nghiệp"),
    (re.compile(r"PR workflow bạn\+Mai"), "PR workflow bạn+đồng nghiệp"),
    (re.compile(r"Mai approve mới merge được"), "đồng nghiệp approve mới merge được"),
    (re.compile(r"Mai phải sửa"), "đồng nghiệp phải sửa"),
    (re.compile(r"Mai phải fix test"), "đồng nghiệp phải fix test"),
    (re.compile(r"bài lesson Mai join project \(bạn story\)"), "bài lesson đồng nghiệp join project"),
    (re.compile(r"bài lesson Mai join project"), "bài lesson đồng nghiệp join project"),
    (re.compile(r"Mai sợ CLI"), "đồng nghiệp sợ CLI"),
    (re.compile(r"Mai sợ terminal"), "đồng nghiệp sợ terminal"),

    # github-desktop.md story arc
    (re.compile(r"Tiếp bạn story\. Mai \(junior FE dev\) đã follow git lessons \+ setup GitHub account\. Nhưng terminal đen kịt với 50 lệnh khiến Mai stress\. Mỗi lần Mai cần commit, phải:"),
     "Tiếp story. 1 đồng nghiệp junior FE đã follow git lessons + setup GitHub account. Nhưng terminal đen kịt với 50 lệnh khiến họ stress. Mỗi lần cần commit, phải:"),
    (re.compile(r"5 dòng cho 1 commit\. Mai prefers \*\*GUI\*\*"), "5 dòng cho 1 commit. Họ prefer **GUI**"),
    (re.compile(r"Bài này dạy Mai \(và bạn\) dùng \*\*GitHub Desktop\*\*"), "Bài này dạy bạn dùng **GitHub Desktop**"),
    (re.compile(r"\*\*Mai \(FE dev\)\*\*: dùng GitHub Desktop song song VS Code\."), "**Đồng nghiệp FE**: dùng GitHub Desktop song song VS Code."),
    (re.compile(r"tình huống Mai sợ CLI"), "tình huống đồng nghiệp sợ CLI"),

    # 00_what-is-git-hosting.md link description
    (re.compile(r"bài lesson Mai join project"), "bài lesson đồng nghiệp join project"),

    # README.md description
    (re.compile(r"Mai sợ CLI, 5-phần UI"), "đồng nghiệp sợ CLI, 5-phần UI"),

    # github.md L23 — long sentence
    (re.compile(r"setup PR workflow với Mai → publish portfolio Pages"), "setup PR workflow với đồng nghiệp → publish portfolio Pages"),

    # ── text-processing-advanced.md sample data ──
    # "Mai  25 Hanoi" / "Hung 35 Saigon" → "Bob  25 Hanoi" / "Charlie 35 Saigon"
    (re.compile(r"^Mai(\s+)(\d+)(\s+)(Hanoi|Saigon|Danang)", re.MULTILINE), r"Bob\1\2\3\4"),
    (re.compile(r"^Hung(\s+)(\d+)(\s+)(Hanoi|Saigon|Danang)", re.MULTILINE), r"Charlie\1\2\3\4"),
    (re.compile(r"\bMai\b(?=\s*\|)"), "Bob"),  # table column
    (re.compile(r"\bHung\b(?=\s*\|)"), "Charlie"),
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
    print(f"\n📊 Mai/Hung tools fix: {total} replacements")


if __name__ == "__main__":
    main()
