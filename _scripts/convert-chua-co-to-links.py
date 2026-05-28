#!/usr/bin/env python3
"""
convert-chua-co-to-links.py
Author: Mr.Rom
Date: 2026-05-26

Converts ALL backtick-path `(chưa có)` references in career roadmap files
into proper markdown links with 🚧 status marker.

Pattern:  — `XX_Category/module/` (chưa có)
Target:   — [`XX_Category/module/`](../../XX_Category/module/) 🚧

Also handles special cases per file (non-backtick patterns).
"""

import re
from pathlib import Path

CAREER_DIR = Path(__file__).resolve().parent.parent / "00_roadmaps" / "career"

# --- Path mapping for special cases ---
# Some paths in backticks are L3+ (subtopics within an L2 module)
# They need to link to the L2 parent instead.
PATH_MAP = {
    "10_devops/iac/terraform/": "10_devops/iac/",
    "10_devops/iac/ansible/": "10_devops/iac/",
    "10_devops/gitops/argocd/": "10_devops/gitops/",
    "03_languages/python/lessons/02_intermediate/": "03_languages/python/",
}


def resolve_path(raw_path: str) -> str:
    """Resolve a raw path from backticks to the correct link target."""
    # Strip trailing slash for lookup, but keep it in output
    clean = raw_path.rstrip("/") + "/"
    if clean in PATH_MAP:
        return PATH_MAP[clean]
    return clean


def process_generic_backtick_chua_co(content: str) -> tuple[str, int]:
    """
    Replace pattern:
      — `XX/path/` (chưa có)
      hoặc `XX/path/` (chưa có)
    with:
      — [`XX/path/`](../../XX/path/) 🚧
      hoặc [`XX/path/`](../../XX/path/) 🚧
    """
    # Match: (— or hoặc) followed by space, backtick path, space, (chưa có)
    pattern = r'(—|hoặc) `([^`]+/)`? \(chưa có\)'
    count = 0

    def replacer(m):
        nonlocal count
        prefix = m.group(1)       # — or hoặc
        raw_path = m.group(2)     # e.g. 07_web/backend/python-fastapi/
        resolved = resolve_path(raw_path)
        link_target = f"../../{resolved}"
        count += 1
        return f'{prefix} [`{raw_path}`]({link_target}) 🚧'

    new_content = re.sub(pattern, replacer, content)
    return new_content, count


def process_special_cases(filename: str, content: str) -> tuple[str, int]:
    """Handle per-file special cases that don't match the generic pattern."""
    count = 0

    if filename == "backend-developer_career-roadmap.md":
        # Line 65: "[Postman](../../02_tools/) hoặc Bruno (chưa có) — test API"
        # Remove "(chưa có)" only — Bruno is a tool name, not a link
        old = "hoặc Bruno (chưa có) — test API"
        new = "hoặc Bruno — test API"
        if old in content:
            content = content.replace(old, new)
            count += 1

        # Line 100: "✅ + OOP (chưa có)"
        old = "✅ + OOP (chưa có)"
        new = "✅ + OOP 🚧"
        if old in content:
            content = content.replace(old, new)
            count += 1

    elif filename == "devops-engineer_career-roadmap.md":
        # Line 54: existing link with "— chưa có" at end (no backtick path)
        old = "advanced (process, permission, systemd) — chưa có"
        new = "advanced (process, permission, systemd) 🚧"
        if old in content:
            content = content.replace(old, new)
            count += 1

    elif filename == "ml-engineer_career-roadmap.md":
        # Line 135: "[Kubernetes basics](../../10_devops/) (chưa có)"
        # Fix link target + remove (chưa có) + add 🚧
        old = "[Kubernetes basics](../../10_devops/) (chưa có)"
        new = "[Kubernetes basics](../../10_devops/kubernetes/) 🚧"
        if old in content:
            content = content.replace(old, new)
            count += 1

        # Line 136: "[Airflow](../../14_data-engineering/) (chưa có)"
        old = "[Airflow](../../14_data-engineering/) (chưa có)"
        new = "[Airflow](../../14_data-engineering/airflow-and-orchestration/) 🚧"
        if old in content:
            content = content.replace(old, new)
            count += 1

    elif filename == "platform-engineer_career-roadmap.md":
        # Line 56: "[Terraform](../../10_devops/iac/) (chưa có)"
        # Link is already correct, just remove (chưa có) and add 🚧
        old = "[Terraform](../../10_devops/iac/) (chưa có)"
        new = "[Terraform](../../10_devops/iac/) 🚧"
        if old in content:
            content = content.replace(old, new)
            count += 1

    return content, count


def process_file(filepath: Path) -> dict:
    """Process a single career roadmap file."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    total = 0

    # 1. Handle special cases first (before generic, to avoid double-processing)
    content, special_count = process_special_cases(filepath.name, content)
    total += special_count

    # 2. Handle generic backtick pattern
    content, generic_count = process_generic_backtick_chua_co(content)
    total += generic_count

    # Write only if changed
    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return {
        "file": filepath.name,
        "generic": generic_count,
        "special": special_count,
        "total": total,
        "changed": content != original,
    }


def main():
    print("=" * 60)
    print("Convert (chưa có) → markdown links + 🚧")
    print(f"Directory: {CAREER_DIR}")
    print("=" * 60)

    files = sorted(CAREER_DIR.glob("*_career-roadmap.md"))
    print(f"\nFound {len(files)} career roadmap files.\n")

    grand_total = 0
    results = []

    for f in files:
        result = process_file(f)
        results.append(result)
        if result["total"] > 0:
            print(f"  ✅ {result['file']}: {result['total']} conversions "
                  f"(generic={result['generic']}, special={result['special']})")
            grand_total += result["total"]
        else:
            print(f"  ⏭️  {result['file']}: no changes")

    print(f"\n{'=' * 60}")
    print(f"Total conversions: {grand_total}")
    print(f"Files modified: {sum(1 for r in results if r['changed'])}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
