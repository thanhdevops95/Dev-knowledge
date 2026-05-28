#!/usr/bin/env python3
# ============================================================================
# Script    : fix-roadmap-links.py
# Purpose   : Fix broken roadmap links in cluster READMEs.
#             - career-guides/ → career/
#             - X_roadmap.md → X_career-roadmap.md (with name mapping)
# Version   : v1.0.0
# Created   : 24/05/2026
# Author    : Mr.Rom
# ============================================================================

import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

# Files with broken roadmap links
TARGET_FILES = [
    ROOT / "10_devops/docker/lessons/02_intermediate/README.md",
    ROOT / "10_devops/kubernetes/README.md",
    ROOT / "10_devops/kubernetes/lessons/02_intermediate/README.md",
    ROOT / "10_devops/ci-cd/README.md",
    ROOT / "10_devops/ci-cd/lessons/02_intermediate/README.md",
    ROOT / "10_devops/observability/README.md",
    ROOT / "10_devops/observability/lessons/02_intermediate/README.md",
    ROOT / "10_devops/iac/README.md",
    ROOT / "10_devops/iac/lessons/02_intermediate/README.md",
    ROOT / "11_cloud/README.md",
    ROOT / "11_cloud/cloud-fundamentals/README.md",
    ROOT / "11_cloud/aws/README.md",
]

# Roadmap name mapping: old basename → new basename
ROADMAP_MAP = {
    "devops-engineer_roadmap.md": "devops-engineer_career-roadmap.md",
    "platform-engineer_roadmap.md": "platform-engineer_career-roadmap.md",
    "sre_roadmap.md": "sre-engineer_career-roadmap.md",
    "cloud-architect_roadmap.md": "cloud-engineer_career-roadmap.md",
    "backend-developer_roadmap.md": "backend-developer_career-roadmap.md",
    "frontend-developer_roadmap.md": "frontend-developer_career-roadmap.md",
    "fullstack-developer_roadmap.md": "fullstack-developer_career-roadmap.md",
    "data-engineer_roadmap.md": "data-engineer_career-roadmap.md",
    "data-scientist_roadmap.md": "data-scientist_career-roadmap.md",
    "ml-engineer_roadmap.md": "ml-engineer_career-roadmap.md",
    "ai-engineer_roadmap.md": "ai-engineer_career-roadmap.md",
    "mobile-developer_roadmap.md": "mobile-developer_career-roadmap.md",
    "security-engineer_roadmap.md": "security-engineer_career-roadmap.md",
    "qa-engineer_roadmap.md": "qa-engineer_career-roadmap.md",
    "game-developer_roadmap.md": "game-developer_career-roadmap.md",
    "blockchain-developer_roadmap.md": "blockchain-developer_career-roadmap.md",
    "zero-to-coder_roadmap.md": "zero-to-coder_career-roadmap.md",
}


def transform(text):
    # 1. Replace folder: career-guides/ → career/
    text = text.replace("00_roadmaps/career-guides/", "00_roadmaps/career/")

    # 2. Replace filenames
    for old, new in ROADMAP_MAP.items():
        text = text.replace(old, new)

    return text


def main():
    changed = 0
    for f in TARGET_FILES:
        if not f.exists():
            print(f"  ⚠️  Not found: {f.relative_to(ROOT)}")
            continue

        original = f.read_text(encoding="utf-8")
        new = transform(original)

        if new != original:
            f.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  ✓ {f.relative_to(ROOT)}")

    print(f"\nDone. {changed}/{len(TARGET_FILES)} files modified.")


if __name__ == "__main__":
    main()
