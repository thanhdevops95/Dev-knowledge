#!/usr/bin/env python3
"""
Audit script — kiểm tra mọi lesson file vi phạm Blueprint v0.5.4.

Rules audit:
1. §3.6 — Header → Code ngay (không lead-in)
2. §3.7 — English-heavy (bullet/table EN-only, comments code EN)
3. §3.8 — Comments code không đánh số bước (khi nhiều bước)
4. §3.9 — Mở bài định nghĩa khô (không có Tình huống)
5. §3.10 — Ẩn dụ chỉ 1 lần
6. §3.11 — Pitfall không dùng ✅❌
7. §2.3 — Thiếu câu dẫn liền mạch giữa sections
8. §3.1 — Thuật ngữ EN không có VN trong ngoặc

Output: JSON report per file với danh sách vi phạm + line numbers.
"""

import re
import os
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

# Common English words that are OK to have un-translated (technical or proper nouns)
EN_OK = set("""
HTTP HTTPS API REST GraphQL JSON YAML XML CSV SQL NoSQL CRUD ACID JWT OAuth OIDC
Docker Kubernetes K8s Git GitHub GitLab Linux macOS Windows Unix
Python JavaScript TypeScript Go Rust Java Ruby PHP C++ Bash Shell
Node npm pip cargo
HTML CSS DOM React Vue Angular
Postgres PostgreSQL MySQL MongoDB Redis SQLite
AWS GCP Azure DigitalOcean Cloudflare Lambda EC2 S3 IAM
true false null None void
GET POST PUT DELETE PATCH OPTIONS HEAD
README LICENSE CHANGELOG TODO FIXME
""".split())


def find_lesson_files():
    lessons = []
    for p in ROOT.rglob("*.md"):
        if "__Ref__" in p.parts:
            continue
        if "lessons" in p.parts or "Skills-for-me" in p.parts:
            # Only lessons folder
            if "/lessons/" in str(p):
                lessons.append(p)
    return sorted(lessons)


def check_situation_open(content):
    """§3.9 — Bài có "Tình huống" hoặc câu hỏi gợi mở ở đầu không?"""
    # Find first H2 after metadata
    lines = content.split("\n")
    after_goals = False
    for i, line in enumerate(lines):
        if line.startswith("## 🎯 Sau bài này"):
            after_goals = True
            continue
        if after_goals and line.startswith("## "):
            # First H2 after Goals
            heading = line[3:].strip()
            if any(kw in heading.lower() for kw in [
                "tình huống", "vì sao", "tại sao", "câu chuyện",
                "bạn đã", "vấn đề", "khi nào cần",
            ]):
                return True, None
            # Check if next 5 lines have problem-driven intro
            block = "\n".join(lines[i:i+15])
            if any(kw in block.lower() for kw in [
                "bạn đã bao giờ", "tưởng tượng", "hãy", "tháng trước",
                "tình huống", "sếp", "thử nghĩ",
            ]):
                return True, None
            return False, f"line {i+1}: '{heading}' — mở bằng định nghĩa khô"
    return None, None  # no goals section


def check_header_to_code(content):
    """§3.6 — Header → code/list/table ngay không có lead-in 2+ câu."""
    issues = []
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if not re.match(r"^#{2,4} ", line):
            continue
        # Skip section headers Blueprint allows code-only
        heading = line.lstrip("#").strip()
        if any(kw in heading for kw in [
            "Cheatsheet", "Glossary", "Liên kết", "Changelog",
            "Sau bài này", "Tài nguyên", "Self-check", "Mục tiêu",
        ]):
            continue
        # Check next non-blank lines
        next_idx = i + 1
        while next_idx < len(lines) and not lines[next_idx].strip():
            next_idx += 1
        if next_idx >= len(lines):
            continue
        next_block = "\n".join(lines[next_idx:next_idx+5])
        # If first content is code block or table or bullet → check if there's lead-in
        first_line = lines[next_idx].strip()
        if first_line.startswith("```") or first_line.startswith("|") or first_line.startswith("- "):
            # Look back from header — count text lines until previous header
            prev_lines = []
            for j in range(i-1, max(0, i-15), -1):
                if re.match(r"^#{2,4} ", lines[j]):
                    break
                if lines[j].strip():
                    prev_lines.append(lines[j])
            # Now look forward — count text BEFORE the code/table/bullet
            forward_text = []
            for j in range(i+1, next_idx):
                if lines[j].strip():
                    forward_text.append(lines[j])
            # If between header and code/table, there's no paragraph text (≥ 2 sentences)
            if not forward_text or sum(len(t) for t in forward_text) < 80:
                issues.append({
                    "line": i+1,
                    "heading": heading[:60],
                    "first_content": first_line[:50],
                })
    return issues


def check_english_comments(content):
    """§3.7 — Comments trong code block toàn EN."""
    issues = []
    in_code = False
    lang = None
    code_lines = []
    code_start = 0
    for i, line in enumerate(content.split("\n")):
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                lang = line.strip()[3:].strip()
                code_start = i + 1
                code_lines = []
            else:
                # End of code block
                if lang in ("python", "py", "bash", "sh", "javascript", "js", "ts", "typescript"):
                    en_comments = 0
                    total_comments = 0
                    for cl in code_lines:
                        s = cl.strip()
                        if s.startswith("#") or s.startswith("//"):
                            total_comments += 1
                            # Check if has Vietnamese diacritics
                            if not re.search(r"[ăâđêôơưàáảãạèéẻẽẹìíỉĩịòóỏõọùúủũụỳýỷỹỵÀ-ỹ]", s):
                                # Allow short EN like # install
                                comment_text = re.sub(r"^[#/]+\s*", "", s).strip()
                                if len(comment_text) > 20 and not any(kw in comment_text.lower() for kw in [
                                    "install", "verify", "init", "setup", "config", "todo", "fixme",
                                    "import", "export", "test"
                                ]):
                                    en_comments += 1
                    if en_comments >= 3:
                        issues.append({
                            "line": code_start,
                            "lang": lang,
                            "en_comments_count": en_comments,
                            "total_comments": total_comments,
                        })
                in_code = False
                code_lines = []
        elif in_code:
            code_lines.append(line)
    return issues


def check_metaphor_count(content):
    """§3.10 — Bài có WHAT section nào nhưng metaphor < 2 lần dùng."""
    metaphor_count = content.count("🪞")
    h2_count = len([l for l in content.split("\n") if re.match(r"^##\s+\d+", l) or l.startswith("## 1️⃣") or l.startswith("## 2️⃣")])
    if h2_count >= 3 and metaphor_count < 2:
        return {"metaphor_count": metaphor_count, "concept_section_count": h2_count}
    return None


def check_pitfall_format(content):
    """§3.11 — Pitfall section dùng ✅❌ hay không."""
    pitfall_idx = content.find("## ⚠️")
    if pitfall_idx == -1:
        pitfall_idx = content.find("## 💡 Pitfall")
    if pitfall_idx == -1:
        return None
    pitfall_section = content[pitfall_idx:pitfall_idx+5000]
    # Check if has at least 2 ✅ and 2 ❌
    plus_count = pitfall_section.count("✅")
    minus_count = pitfall_section.count("❌")
    if plus_count < 2 or minus_count < 2:
        return {"plus_count": plus_count, "minus_count": minus_count}
    return None


def check_english_heavy_bullets(content):
    """§3.7 — Bullet list toàn EN không có VN."""
    issues = []
    lines = content.split("\n")
    in_bullet_block = False
    bullet_block = []
    bullet_start = 0
    for i, line in enumerate(lines):
        is_bullet = re.match(r"^\s*[-*]\s", line)
        if is_bullet:
            if not in_bullet_block:
                in_bullet_block = True
                bullet_start = i + 1
                bullet_block = []
            bullet_block.append(line)
        else:
            if in_bullet_block and len(bullet_block) >= 3:
                # Check if all bullets are short EN
                en_only = 0
                for b in bullet_block:
                    text = re.sub(r"^\s*[-*]\s+", "", b).strip()
                    text = re.sub(r"`[^`]+`", "", text)  # remove code
                    text = re.sub(r"\*\*[^*]+\*\*", "", text)  # remove bold
                    text = re.sub(r"[^\w\s]", " ", text)  # remove special chars
                    if text and not re.search(r"[ăâđêôơưàáảãạèéẻẽẹìíỉĩịòóỏõọùúủũụỳýỷỹỵÀ-ỹ]", text):
                        en_only += 1
                if en_only >= len(bullet_block) * 0.7 and len(bullet_block) >= 3:
                    issues.append({
                        "line": bullet_start,
                        "bullet_count": len(bullet_block),
                        "en_only_count": en_only,
                    })
            in_bullet_block = False
            bullet_block = []
    return issues


def audit_file(path):
    try:
        content = path.read_text()
    except Exception as e:
        return {"error": str(e)}

    rel = str(path.relative_to(ROOT))
    issues = {}

    # Skip non-lesson files
    if path.name in ("README.md", "_glossary.md", "99_cheatsheet.md"):
        return None

    # §3.9 — Tình huống mở bài
    ok, msg = check_situation_open(content)
    if ok is False:
        issues["situation_open"] = msg

    # §3.6 — Header → code ngay
    h2c = check_header_to_code(content)
    if h2c:
        issues["header_to_code"] = h2c[:5]  # limit

    # §3.7 — English comments
    enc = check_english_comments(content)
    if enc:
        issues["english_comments"] = enc[:5]

    # §3.10 — Ẩn dụ ít
    metaphor = check_metaphor_count(content)
    if metaphor:
        issues["low_metaphor"] = metaphor

    # §3.11 — Pitfall không ✅❌
    pitfall = check_pitfall_format(content)
    if pitfall:
        issues["pitfall_no_yes_no"] = pitfall

    # §3.7 — Bullet EN-only
    enb = check_english_heavy_bullets(content)
    if enb:
        issues["english_heavy_bullets"] = enb[:5]

    return {"file": rel, "issues": issues, "total_issues": sum(
        len(v) if isinstance(v, list) else 1 for v in issues.values()
    )} if issues else None


def main():
    files = find_lesson_files()
    print(f"Auditing {len(files)} lesson files...")

    results = []
    for f in files:
        r = audit_file(f)
        if r:
            results.append(r)

    # Sort by total_issues desc
    results.sort(key=lambda x: -x["total_issues"])

    # Summary stats
    stats = defaultdict(int)
    by_violation = defaultdict(list)
    for r in results:
        for k in r["issues"]:
            stats[k] += 1
            by_violation[k].append(r["file"])

    print(f"\n📊 SUMMARY — {len(results)}/{len(files)} files have issues\n")
    print(f"{'Vi phạm':<35} | {'Số file':>8} | {'%':>5}")
    print("-" * 60)
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        pct = v / len(files) * 100
        print(f"{k:<35} | {v:>8} | {pct:>4.1f}%")

    print(f"\n🔥 TOP 20 files most issues:\n")
    for r in results[:20]:
        print(f"  {r['total_issues']:>3} | {r['file']}")

    # Save full report
    out = ROOT / "_workspace" / "audit-blueprint-v0.5.4-report.json"
    out.write_text(json.dumps({
        "total_files": len(files),
        "files_with_issues": len(results),
        "stats": dict(stats),
        "results": results,
    }, ensure_ascii=False, indent=2))
    print(f"\n✅ Full report: {out}")


if __name__ == "__main__":
    main()
