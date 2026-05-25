#!/usr/bin/env python3
"""
Targeted Long character fix — phiên bản 3.
Học từ pass 2: viết regex CAREFUL hơn để tránh inconsistency capitalization.

Quy tắc:
1. "Long" sau dấu chấm/đầu dòng/sau heading → "Bạn"
2. "Long" giữa câu → "bạn"
3. "của Long" → "của bạn"
4. Heading "Tình huống — Long ..." → "Tình huống — bạn ..." (lowercase vì sau —)
5. Vai trò: "Long, junior dev" → "Bạn, junior dev"
"""

import re
import sys
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/Dev-knowledge")

FILES = [
    "01_Foundations/version-control/git/lessons/01_basic/01_init-and-first-commit.md",
    "01_Foundations/version-control/git/lessons/01_basic/02_branching-and-merging.md",
    "01_Foundations/version-control/git/lessons/01_basic/03_remote-and-github.md",
    "01_Foundations/version-control/git/lessons/01_basic/04_undo-and-recovery.md",
    "02_Tools/git-clients/github-desktop.md",
    "02_Tools/git-clients/github.md",
    "02_Tools/git-clients/gitlab.md",
    "10_DevOps/docker/lessons/01_basic/00_what-is-docker.md",
    "10_DevOps/docker/lessons/01_basic/01_images-and-containers.md",
    "10_DevOps/docker/lessons/01_basic/02_dockerfile-basics.md",
    "10_DevOps/docker/lessons/01_basic/03_docker-compose.md",
]


def fix_long(text):
    """Replace Long → bạn/Bạn theo context."""
    # Capitalize at sentence start
    # Pattern 1: After . ? ! \n + optional spaces + "Long"
    text = re.sub(r"(^|[.!?]\n*|\n+)(\s*)Long\b", r"\1\2Bạn", text)

    # Pattern 2: "→ Long" (after arrow)
    text = re.sub(r"(→\s*)Long\b", r"\1Bạn", text)

    # Pattern 3: "## ... Long ..." in heading - lowercase since after —
    text = re.sub(r"(##[^\n]*?— )Long\b", r"\1bạn", text)
    # Special: "## Tình huống — tối ... của Long"
    text = re.sub(r"(của )Long\b", r"\1bạn", text)

    # Pattern 4: Mid-sentence "Long" → "bạn"
    # After common Vietnamese mid-sentence positions: chỉ, là, sẽ, đã, có, không, mà, và, với, cho, từ, tới
    text = re.sub(r"(\b(?:chỉ|là|sẽ|đã|có|không|mà|và|với|cho|từ|tới|của|như|tại|về|sau|trước|cùng) )Long\b", r"\1bạn", text)

    # Pattern 5: "Long," at start of sentence/dialogue
    text = re.sub(r"(^|\n)Long,", r"\1Bạn,", text)

    # Pattern 6: Catch-all remaining "Long" → "bạn" (mid-sentence default)
    # Be careful: don't replace "Long-lived", "Long-form", etc.
    text = re.sub(r"\bLong\b(?!-)", "bạn", text)

    # Cleanup: "**Bước X** — bạn" lowercase (was Bước inline)
    # Cleanup any double-replacements that may have made standalone "bạn" mid-sentence into uppercase
    text = re.sub(r"([.!?]\s+)bạn\b", lambda m: m.group(1) + "Bạn", text)
    text = re.sub(r"(\n)bạn\b", lambda m: m.group(1) + "Bạn", text)

    return text


def main():
    for fname in FILES:
        path = ROOT / fname
        if not path.exists():
            print(f"✗ Missing: {fname}")
            continue
        text = path.read_text()
        before = len(re.findall(r"\bLong\b", text))
        new_text = fix_long(text)
        after = len(re.findall(r"\bLong\b", new_text))
        path.write_text(new_text)
        print(f"✓ {fname}: {before} → {after} occurrences")


if __name__ == "__main__":
    main()
