#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tên script: fix-roadmap-links.py
Tác giả: Mr.Rom
Phiên bản: v1.0.0
Mô tả: Tự động quét toàn bộ thư mục 00_roadmaps/career/ và sửa các liên kết tương đối
       trỏ về thư mục Git cũ (01_foundations/version-control/git/) sang thư mục mới (02_tools/git/).
Sử dụng: python3 _scripts/fix-roadmap-links.py
"""

import os

# 1. Xác định đường dẫn gốc dự án và thư mục roadmaps
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CAREER_DIR = os.path.join(REPO_ROOT, "00_roadmaps", "career")

# 2. Cấu hình các chuỗi cần thay thế
REPLACEMENTS = {
    "../../01_foundations/version-control/git/setup/git.md": "../../02_tools/git/setup/git.md",
    "../../01_foundations/version-control/git/": "../../02_tools/git/",
}

def fix_roadmap_links():
    if not os.path.exists(CAREER_DIR):
        print(f"❌ Lỗi: Thư mục career không tồn tại tại: {CAREER_DIR}")
        return

    print(f"🔍 Bắt đầu quét các tệp tin trong: {CAREER_DIR}")
    
    modified_files_count = 0
    total_replacements_count = 0

    # Lặp qua tất cả các file trong thư mục
    for filename in os.listdir(CAREER_DIR):
        if not filename.endswith(".md"):
            continue
            
        file_path = os.path.join(CAREER_DIR, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Thực hiện thay thế
        new_content = content
        file_replacement_count = 0
        
        for old_link, new_link in REPLACEMENTS.items():
            occurrences = content.count(old_link)
            if occurrences > 0:
                new_content = new_content.replace(old_link, new_link)
                file_replacement_count += occurrences
                total_replacements_count += occurrences

        # Ghi lại file nếu có thay đổi
        if file_replacement_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  ✅ Đã sửa {file_replacement_count} liên kết trong: \033[1;32m{filename}\033[0m")
            modified_files_count += 1

    print("\n==================================================")
    print(f"🎉 Hoàn thành kiểm tra!")
    print(f"👉 Số tệp tin đã sửa đổi: {modified_files_count}")
    print(f"👉 Tổng số liên kết đã khôi phục: {total_replacements_count}")
    print("==================================================")

if __name__ == "__main__":
    fix_roadmap_links()
