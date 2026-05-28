#!/usr/bin/env python3
# ============================================================================
# Script    : check-broken-links.py
# Purpose   : Quét toàn bộ repo và kiểm tra tất cả các liên kết tương đối (.md)
#             xem có bị broken link nào không.
# Author    : Mr.Rom
# ============================================================================

import os
import re
from pathlib import Path

ROOT = Path("/Users/rom/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/04_Knowledge/dev-knowledge")

def find_md_files():
    md_files = []
    for p in ROOT.rglob("*.md"):
        # Bỏ qua thư mục .git, __Ref__, _blueprint, và các file trong _workspace
        if any(part in p.parts for part in [".git", "__Ref__", "_workspace", "_blueprint"]):
            continue
        md_files.append(p)
    return sorted(md_files)

def check_links_in_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    # Regex tìm link markdown: [text](path)
    # Loại trừ link http/https và anchor thuần túy (#anchor)
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
    matches = link_pattern.findall(content)
    
    broken_links = []
    for text, path in matches:
        path = path.strip()
        # Bỏ qua link internet
        if path.startswith(("http://", "https://", "mailto:", "ftp:")):
            continue
        # Bỏ qua anchor link trong cùng 1 file
        if path.startswith("#"):
            continue
        
        # Tách phần anchor (#...) nếu có
        clean_path = path.split("#")[0]
        if not clean_path:
            continue
            
        # Tính toán đường dẫn tuyệt đối
        target_path = (file_path.parent / clean_path).resolve()
        
        # Kiểm tra xem file hoặc folder đích có tồn tại không
        if not target_path.exists():
            # Thử thêm .md nếu target_path không tồn tại và không có ext
            if not target_path.suffix and not target_path.exists():
                target_path_with_md = target_path.with_suffix(".md")
                if target_path_with_md.exists():
                    continue
            broken_links.append((path, text))
            
    return broken_links

def main():
    print("🔍 Bắt đầu quét kiểm tra broken links...")
    files = find_md_files()
    print(f"Tổng số file markdown cần quét: {len(files)}")
    
    total_broken = 0
    files_with_broken = 0
    
    for f in files:
        broken = check_links_in_file(f)
        if broken:
            files_with_broken += 1
            rel_file = f.relative_to(ROOT)
            print(f"\n📂 File: {rel_file}")
            for path, text in broken:
                total_broken += 1
                print(f"  ❌ Broken Link: '{path}' (Anchor Text: '{text}')")
                
    print("\n" + "="*50)
    if total_broken == 0:
        print("🎉 Tuyệt vời! Không phát hiện bất kỳ broken link tương đối nào trong các file tri thức.")
    else:
        print(f"⚠️  Phát hiện {total_broken} broken link(s) tại {files_with_broken} file(s).")
        
if __name__ == "__main__":
    main()
