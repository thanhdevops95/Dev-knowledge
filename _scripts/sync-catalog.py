#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Tên script: sync-catalog.py
# Tác giả: Mr.Rom
# Phiên bản: v1.0.0
# Mô tả: Tự động quét kho tri thức và đồng bộ hoá MASTER-CATALOG.md
#        với trạng thái thực tế của hệ thống tập tin.
# ==============================================================================

import os
import re
import sys
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATALOG_PATH = os.path.join(REPO_ROOT, "MASTER-CATALOG.md")

L1_DIRECTORIES = [
    "00_roadmaps",
    "01_foundations",
    "02_tools",
    "03_languages",
    "04_os",
    "05_networking",
    "06_databases",
    "07_web",
    "08_mobile",
    "09_architecture",
    "10_devops",
    "11_cloud",
    "12_security",
    "13_ai-ml",
    "14_data-engineering",
    "15_specialized",
    "16_career-soft-skills"
]

IGNORED_DIRS = {
    "__Ref__", "_blueprint", "_scripts", "_assets", "_workspace",
    ".git", ".gemini", "scratch", "brain", "node_modules"
}

IGNORED_FILES = {
    "README.md", "CONTRIBUTING.md", "MASTER-CATALOG.md", "_idea-overview.md"
}

# Regex to safely clean title
def clean_title(title):
    title = re.sub(r'^#\s*', '', title)
    title = re.sub(r'^[^\w\s#+.-]+\s*', '', title)
    return title.strip()

def adjust_description_links(desc, file_path):
    if not desc:
        return desc
    file_dir = os.path.dirname(file_path)
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2).strip()
        url_clean = url.split("#")[0].strip()
        
        if not url_clean or url_clean.startswith(("http://", "https://", "mailto:", "ftp:", "javascript:")) or url_clean.startswith(("#", "/")):
            return match.group(0)
            
        resolved = os.path.normpath(os.path.join(file_dir, url_clean))
        anchor = ""
        if "#" in url:
            anchor = "#" + url.split("#", 1)[1]
            
        return f"[{text}]({resolved}{anchor})"
        
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, desc)

# Function to parse metadata from a file
def parse_file_metadata(file_path):
    abs_path = os.path.join(REPO_ROOT, file_path)
    if not os.path.exists(abs_path):
        return None
    
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Get H1
    h1_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
    title = clean_title(h1_match.group(1)) if h1_match else "Untitled"
    
    # Parse metadata block (typically lines starting with >)
    meta_lines = []
    for line in content.split('\n'):
        if line.strip().startswith('>'):
            meta_lines.append(line.strip())
        elif line.strip() == '---' or line.strip().startswith('#'):
            if meta_lines:
                break
        elif line.strip() == '':
            continue
        else:
            if meta_lines:
                break
                
    meta_text = '\n'.join(meta_lines)
    
    author_match = re.search(r'\*\*(?:Tác giả|Author):\*\*\s*([^\r\n\\]+)', meta_text)
    version_match = re.search(r'\*\*(?:Phiên bản|Version):\*\*\s*([^\r\n\\]+)', meta_text)
    level_match = re.search(r'\*\*(?:Level):\*\*\s*([^\r\n\\]+)', meta_text)
    tags_match = re.search(r'\*\*(?:Tags):\*\*\s*([^\r\n\\]+)', meta_text)
    status_match = re.search(r'\*\*(?:Status|Trạng thái):\*\*\s*([^\r\n\\]+)', meta_text)
    
    # Description parsing
    desc = None
    desc_match = re.search(r'>\s*🎯\s*(.*)', meta_text)
    if desc_match:
        desc = desc_match.group(1).strip()
        if desc.startswith('*') and desc.endswith('*'):
            desc = desc[1:-1].strip()
        if desc.endswith('\\'):
            desc = desc[:-1].strip()
        desc = adjust_description_links(desc, file_path)
            
    # Determine status icon
    status = "✅"
    status_text = status_match.group(1).strip().replace('\\', '') if status_match else ""
    if status_text:
        st_lower = status_text.lower()
        if "placeholder" in st_lower or "wip" in st_lower or "🚧" in st_lower:
            status = "🚧"
        elif "chưa" in st_lower or "skeleton" in st_lower or "❌" in st_lower:
            status = "❌"
        elif "cập nhật" in st_lower or "outdated" in st_lower or "🔄" in st_lower:
            status = "🔄"
            
    is_must_know = False
    tags_text = tags_match.group(1).strip() if tags_match else ""
    if tags_text and "must-know" in tags_text.lower():
        is_must_know = True
        
    return {
        "path": file_path,
        "title": title,
        "author": author_match.group(1).strip().replace('\\', '') if author_match else None,
        "version": version_match.group(1).strip().replace('\\', '') if version_match else None,
        "level": level_match.group(1).strip().replace('\\', '') if level_match else None,
        "status": status,
        "status_text": status_text,
        "must_know": is_must_know,
        "desc": desc
    }

# Function to scan the filesystem for all .md files in L1 folders
def scan_filesystem():
    files_by_l1_l2 = {}
    for l1 in L1_DIRECTORIES:
        files_by_l1_l2[l1] = {}
        l1_dir = os.path.join(REPO_ROOT, l1)
        if not os.path.exists(l1_dir):
            continue
            
        for root, dirs, files in os.walk(l1_dir):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            
            for file in files:
                if not file.endswith(".md") or file in IGNORED_FILES:
                    continue
                    
                rel_path = os.path.relpath(os.path.join(root, file), REPO_ROOT)
                # Determine L2 directory name
                parts = rel_path.split(os.sep)
                if len(parts) <= 2:
                    # Skip files directly under L1 root folder (e.g. L1/00_overview.md)
                    continue
                    
                l2 = parts[1]
                    
                # Skip __Ref__ at any depth
                if any(p in IGNORED_DIRS for p in parts):
                    continue
                    
                meta = parse_file_metadata(rel_path)
                if meta:
                    if l2 not in files_by_l1_l2[l1]:
                        files_by_l1_l2[l1][l2] = []
                    files_by_l1_l2[l1][l2].append(meta)
                    
    return files_by_l1_l2

def main():
    print("🔍 Bắt đầu quét hệ thống tập tin...")
    fs_files = scan_filesystem()
    
    total_found = sum(len(files) for l2_dict in fs_files.values() for files in l2_dict.values())
    print(f"📊 Tìm thấy {total_found} tệp tin markdown hợp lệ trong kho.")
    
    # Read MASTER-CATALOG.md
    if not os.path.exists(CATALOG_PATH):
        print(f"❌ Không tìm thấy {CATALOG_PATH}")
        sys.exit(1)
        
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog_lines = f.readlines()
        
    updated_lines = []
    current_l1 = None
    current_l2 = None
    in_l1_section = False
    l2_heading_regex = re.compile(r'^####\s+([^/]+)/')
    grouped_l2_heading_regex = re.compile(r'^####\s+([a-zA-Z0-9_, -/]+)')
    
    i = 0
    while i < len(catalog_lines):
        line = catalog_lines[i]
        
        # Detect H2 sections to track if we are in L1 listing
        if line.startswith("## "):
            if "Theo L1" in line:
                in_l1_section = True
            else:
                in_l1_section = False
                current_l1 = None
                current_l2 = None
            updated_lines.append(line)
            i += 1
            continue
            
        if not in_l1_section:
            updated_lines.append(line)
            i += 1
            continue
            
        # Detect L1 section
        if line.startswith("### "):
            l1_match = re.search(r'^###\s+(\d{2}_[a-zA-Z0-9_-]+)', line)
            if l1_match:
                current_l1 = l1_match.group(1).strip()
                current_l2 = None
                print(f"  Đang quét mục L1: {current_l1}")
            else:
                current_l1 = None
            updated_lines.append(line)
            i += 1
            continue
            
        if current_l1 is None:
            updated_lines.append(line)
            i += 1
            continue
            
        # Detect grouped L2 headings (like #### javascript-typescript/, go/, rust/)
        grouped_match = grouped_l2_heading_regex.match(line)
        if grouped_match and "," in line:
            heading_content = grouped_match.group(1).strip()
            # Split by comma to see if we have multiple L2s
            l2_parts = [p.strip().rstrip('/') for p in heading_content.split(',')]
            l2_parts = [p for p in l2_parts if p]
            
            # Check if any of these L2s has content in filesystem
            has_any_content = False
            active_l2s = []
            inactive_l2s = []
            
            for p in l2_parts:
                if p in fs_files.get(current_l1, {}):
                    has_any_content = True
                    active_l2s.append(p)
                else:
                    inactive_l2s.append(p)
            
            if has_any_content:
                # We need to split!
                print(f"    ✂️ Tách đề mục gộp: '{heading_content}' vì bắt đầu có bài học.")
                
                # Check what is the next line - typically it is "❌ Chưa có content."
                next_line = ""
                if i + 1 < len(catalog_lines):
                    next_line = catalog_lines[i+1].strip()
                    
                # Skip the "❌ Chưa có content." line if we are splitting
                skip_next = False
                if "Chưa có content" in next_line:
                    skip_next = True
                
                # For each active L2, output its own heading and files
                for act in active_l2s:
                    updated_lines.append(f"#### {act}/\n")
                    # List all files for this L2
                    for f_meta in sorted(fs_files[current_l1][act], key=lambda x: x['path']):
                        # Generate catalog line
                        status_icon = f_meta['status']
                        must_know_icon = " 🌟" if f_meta['must_know'] else ""
                        # Calculate path relative to L2 directory
                        # E.g. 03_languages/csharp/lessons/01_basic/00_what-is-csharp.md -> lessons/01_basic/00_what-is-csharp.md
                        rel_to_l2 = f_meta['path']
                        prefix_l1_l2 = f"{current_l1}/{act}/"
                        if rel_to_l2.startswith(prefix_l1_l2):
                            rel_to_l2 = rel_to_l2[len(prefix_l1_l2):]
                            
                        desc_str = f" — {f_meta['desc']}" if f_meta['desc'] else ""
                        updated_lines.append(f"- {status_icon}{must_know_icon} [`{rel_to_l2}`]({f_meta['path']}){desc_str}\n")
                        # Mark as visited/processed
                        f_meta['visited'] = True
                    updated_lines.append("\n")
                    
                # If there are still inactive L2s, group them back
                if inactive_l2s:
                    inactive_heading = ", ".join([f"{p}/" for p in inactive_l2s])
                    updated_lines.append(f"#### {inactive_heading}\n")
                    updated_lines.append("❌ Chưa có content.\n\n")
                
                i += 2 if skip_next else 1
                continue
            else:
                # Keep as is
                updated_lines.append(line)
                i += 1
                continue
                
        # Detect single L2 heading (#### docker/)
        l2_match = l2_heading_regex.match(line)
        if l2_match:
            current_l2 = l2_match.group(1).strip()
            updated_lines.append(line)
            i += 1
            continue
            
        # Parse list items inside L2 section
        if current_l2 and line.strip().startswith("- "):
            # Check if this line has a markdown link
            link_match = re.search(r'\[`([^`]+)`\]\(([^)]+)\)', line)
            if link_match:
                rel_path_in_link = link_match.group(2).strip()
                # Verify if this file exists in filesystem
                # We match it with our fs_files dict
                found_meta = None
                for l2_name, files in fs_files.get(current_l1, {}).items():
                    for f in files:
                        if f['path'] == rel_path_in_link:
                            found_meta = f
                            break
                    if found_meta:
                        break
                        
                if found_meta:
                    # Update status, title, description in the line
                    status_icon = found_meta['status']
                    must_know_icon = " 🌟" if found_meta['must_know'] else ""
                    # Check if original had new/hot tag so we preserve or update
                    new_tag = " 🆕" if "🆕" in line else ""
                    hot_tag = " 🔥" if "🔥" in line else ""
                    
                    rel_to_l2 = found_meta['path']
                    prefix_l1_l2 = f"{current_l1}/{current_l2}/"
                    if rel_to_l2.startswith(prefix_l1_l2):
                        rel_to_l2 = rel_to_l2[len(prefix_l1_l2):]
                    elif rel_to_l2.startswith("00_roadmaps/"):
                        # E.g. career roadmaps
                        rel_to_l2 = os.path.basename(rel_path_in_link)
                        
                    desc_str = f" — {found_meta['desc']}" if found_meta['desc'] else ""
                    new_line = f"- {status_icon}{must_know_icon}{new_tag}{hot_tag} [`{rel_to_l2}`]({found_meta['path']}){desc_str}\n"
                    updated_lines.append(new_line)
                    found_meta['visited'] = True
                    print(f"    ✅ Đồng bộ: {rel_path_in_link} (Trạng thái: {status_icon})")
                else:
                    # Dead link or untracked file, keep as is but print warning
                    print(f"    ⚠️ Cảnh báo: Link trong catalog không tồn tại trên đĩa: {rel_path_in_link}")
                    updated_lines.append(line)
            else:
                # Check if it is a "planned" ❌ line
                if "❌" in line:
                    # Find any backticked paths
                    backtick_paths = re.findall(r'`([^`]+)`', line)
                    active_paths = []
                    remaining_paths = []
                    
                    for bp in backtick_paths:
                        # Check if file now exists
                        full_bp_path = os.path.join(current_l1, current_l2, bp)
                        # Find in fs_files
                        found = False
                        for f in fs_files.get(current_l1, {}).get(current_l2, []):
                            if f['path'] == full_bp_path:
                                found = True
                                # This planned file is now a real file! We generate its line
                                status_icon = f['status']
                                must_know_icon = " 🌟" if f['must_know'] else ""
                                desc_str = f" — {f['desc']}" if f['desc'] else ""
                                new_line = f"- {status_icon}{must_know_icon} [`{bp}`]({f['path']}){desc_str}\n"
                                updated_lines.append(new_line)
                                f['visited'] = True
                                print(f"    🆕 Kích hoạt bài mới: {f['path']} (Trạng thái: {status_icon})")
                                break
                        if not found:
                            remaining_paths.append(bp)
                            
                    if remaining_paths:
                        # Reconstruct the ❌ line with remaining paths
                        paths_str = ", ".join([f"`{p}`" for p in remaining_paths])
                        # Preserve description if it exists
                        desc_part = ""
                        if " — " in line:
                            desc_part = " — " + line.split(" — ", 1)[1]
                        elif " - " in line:
                            desc_part = " - " + line.split(" - ", 1)[1]
                        updated_lines.append(f"- ❌ {paths_str}{desc_part}\n")
                else:
                    updated_lines.append(line)
            i += 1
            continue
            
        # If we reach end of L2 block (a new heading or ---)
        if current_l2 and (line.startswith("#### ") or line.startswith("---") or line.startswith("### ")):
            # Append any unvisited files for this L2
            unvisited = [f for f in fs_files.get(current_l1, {}).get(current_l2, []) if not f.get('visited')]
            if unvisited:
                print(f"    ➕ Thêm {len(unvisited)} bài học mới phát hiện vào mục {current_l1}/{current_l2}:")
                for f_meta in sorted(unvisited, key=lambda x: x['path']):
                    status_icon = f_meta['status']
                    must_know_icon = " 🌟" if f_meta['must_know'] else ""
                    rel_to_l2 = f_meta['path']
                    prefix_l1_l2 = f"{current_l1}/{current_l2}/"
                    if rel_to_l2.startswith(prefix_l1_l2):
                        rel_to_l2 = rel_to_l2[len(prefix_l1_l2):]
                    elif rel_to_l2.startswith("00_roadmaps/"):
                        rel_to_l2 = os.path.basename(f_meta['path'])
                        
                    desc_str = f" — {f_meta['desc']}" if f_meta['desc'] else ""
                    updated_lines.append(f"- {status_icon}{must_know_icon} [`{rel_to_l2}`]({f_meta['path']}){desc_str}\n")
                    f_meta['visited'] = True
                    print(f"      + {f_meta['path']}")
            current_l2 = None
            
        updated_lines.append(line)
        i += 1
        
    # Check if there are any completely unvisited files in filesystem (folders not yet in catalog)
    # We will output them or add them
    for l1, l2_dict in fs_files.items():
        for l2, files in l2_dict.items():
            unvisited = [f for f in files if not f.get('visited')]
            if unvisited:
                print(f"⚠️ Phát hiện L2 mới hoặc bài học chưa được đăng ký trong Catalog: {l1}/{l2}")
                # We need to insert these files under L1 section in updated_lines
                # Let's find where current L1 is in updated_lines
                l1_idx = -1
                for idx, line in enumerate(updated_lines):
                    if line.startswith(f"### {l1}"):
                        l1_idx = idx
                        break
                
                if l1_idx != -1:
                    # Find the end of this L1 section (where the next H3 starts or ---)
                    end_idx = -1
                    for idx in range(l1_idx + 1, len(updated_lines)):
                        if updated_lines[idx].startswith("### ") or updated_lines[idx].startswith("---"):
                            end_idx = idx
                            break
                            
                    if end_idx != -1:
                        # Insert before the separator
                        insert_lines = []
                        if l2 != "root":
                            insert_lines.append(f"\n#### {l2}/\n")
                        for f_meta in sorted(unvisited, key=lambda x: x['path']):
                            status_icon = f_meta['status']
                            must_know_icon = " 🌟" if f_meta['must_know'] else ""
                            rel_to_l2 = f_meta['path']
                            prefix_l1_l2 = f"{l1}/{l2}/"
                            if rel_to_l2.startswith(prefix_l1_l2):
                                rel_to_l2 = rel_to_l2[len(prefix_l1_l2):]
                            elif rel_to_l2.startswith("00_roadmaps/"):
                                rel_to_l2 = os.path.basename(f_meta['path'])
                                
                            desc_str = f" — {f_meta['desc']}" if f_meta['desc'] else ""
                            insert_lines.append(f"- {status_icon}{must_know_icon} [`{rel_to_l2}`]({f_meta['path']}){desc_str}\n")
                            f_meta['visited'] = True
                            print(f"    ➕ Đã chèn tự động {f_meta['path']}")
                        
                        # Insert list
                        updated_lines[end_idx:end_idx] = insert_lines
                        
    # Now let's recalculate statistics
    # Count:
    # - Total active files (excl. README, etc.): all files found in fs
    # - Done files: fs files with status ✅
    # - WIP files: fs files with status 🚧 or 🔄
    # - Planned (Chưa có) files: count all ❌ entries inside the final updated_lines
    total_files = total_found
    done_files = 0
    wip_files = 0
    must_know_files = 0
    
    for l1, l2_dict in fs_files.items():
        for l2, files in l2_dict.items():
            for f in files:
                if f['status'] == "✅":
                    done_files += 1
                elif f['status'] in ["🚧", "🔄"]:
                    wip_files += 1
                if f['must_know']:
                    must_know_files += 1
                    
    # Count ❌ entries
    planned_count = 0
    # Let's count occurrences of ❌ in updated_lines but exclude Key section
    in_key_section = True
    for line in updated_lines:
        if "## 📚 Theo L1" in line:
            in_key_section = False
        if not in_key_section:
            if "❌" in line:
                # Count matches of planned files. 
                # A line like - ❌ `file1.md`, `file2.md` has len(findall) paths
                matches = re.findall(r'`([^`]+)`', line)
                if matches:
                    planned_count += len(matches)
                elif "Chưa có content" in line:
                    # Grouped L2 with no content
                    # We can parse L2 folder count
                    pass
                else:
                    planned_count += 1
                    
    print(f"\n📈 Thống kê mới:")
    print(f"  - Tổng số bài thực tế (đã tạo): {total_files}")
    print(f"  - ✅ Done: {done_files}")
    print(f"  - 🚧 WIP: {wip_files}")
    print(f"  - ❌ Chưa có (dự kiến): {planned_count}")
    print(f"  - 🌟 MUST-KNOW: {must_know_files}")
    
    # Update Statistics Table in updated_lines
    # Find statistics block
    stats_start = -1
    for idx, line in enumerate(updated_lines):
        if "## 📊 Thống kê tổng" in line:
            stats_start = idx
            break
            
    if stats_start != -1:
        # Locate table rows and update them
        # Typically:
        # | Chỉ số | Giá trị |
        # |---|---|
        # | Tổng số bài | 210 |
        # | ✅ Done | 210 |
        # | 🚧 WIP | 0 |
        # | ❌ Chưa có | Lessons (Phase 2) + Lab series (Phase 3) |
        # | 🌟 MUST-KNOW | 210 ... |
        # Let's rewrite these lines dynamically
        for idx in range(stats_start + 1, stats_start + 15):
            if idx >= len(updated_lines):
                break
            if "Tổng số bài" in updated_lines[idx]:
                updated_lines[idx] = f"| Tổng số bài | {total_files} |\n"
            elif "✅ Done" in updated_lines[idx]:
                percent = (done_files / total_files * 100) if total_files else 0
                updated_lines[idx] = f"| ✅ Done | {done_files} ({percent:.1f}%) |\n"
            elif "🚧 WIP" in updated_lines[idx]:
                updated_lines[idx] = f"| 🚧 WIP | {wip_files} |\n"
            elif "❌ Chưa có" in updated_lines[idx]:
                updated_lines[idx] = f"| ❌ Chưa có | {planned_count} (dự kiến) |\n"
            elif "🌟 MUST-KNOW" in updated_lines[idx]:
                updated_lines[idx] = f"| 🌟 MUST-KNOW | {must_know_files} |\n"
                
    # Update MUST-KNOW list at the end
    # Find H2 section
    must_know_start = -1
    for idx, line in enumerate(updated_lines):
        if "## 🌟 Danh sách MUST-KNOW (toàn kho)" in line:
            must_know_start = idx
            break
            
    if must_know_start != -1:
        # Find where it ends (next H2 or end of file)
        must_know_end = len(updated_lines)
        for idx in range(must_know_start + 1, len(updated_lines)):
            if updated_lines[idx].startswith("## ") or updated_lines[idx].startswith("---") and idx > must_know_start + 5:
                must_know_end = idx
                break
                
        # Generate new MUST-KNOW list grouped by L1
        new_must_know_lines = ["\nBài MUST-KNOW xếp theo L1 để dễ xem cho từng roadmap:\n\n"]
        
        # Get all must know files
        all_must_know = []
        for l1 in L1_DIRECTORIES:
            l1_mk = []
            for l2, files in fs_files.get(l1, {}).items():
                for f in files:
                    if f['must_know']:
                        l1_mk.append(f)
            if l1_mk:
                new_must_know_lines.append(f"### {l1}\n")
                for f in sorted(l1_mk, key=lambda x: x['path']):
                    status_icon = f['status']
                    new_must_know_lines.append(f"- 🌟 {status_icon} [`{f['path']}`]({f['path']}) — {f['title']}\n")
                new_must_know_lines.append("\n")
                
        # Replace the old list
        updated_lines[must_know_start + 1:must_know_end] = new_must_know_lines
        
    # Bump catalog version & date in metadata
    meta_start = -1
    for idx, line in enumerate(updated_lines):
        if line.startswith("# 📊 Master Catalog"):
            meta_start = idx
            break
            
    if meta_start != -1:
        current_date = datetime.now().strftime("%d/%m/%Y")
        for idx in range(meta_start + 1, meta_start + 10):
            if idx >= len(updated_lines):
                break
            if "Phiên bản:" in updated_lines[idx] or "Version:" in updated_lines[idx]:
                # Extract version and bump minor
                v_match = re.search(r'v(\d+)\.(\d+)\.(\d+)', updated_lines[idx])
                if v_match:
                    major = int(v_match.group(1))
                    minor = int(v_match.group(2))
                    patch = int(v_match.group(3))
                    new_minor = minor + 1
                    updated_lines[idx] = f"> **Phiên bản:** v{major}.{new_minor}.0\n"
                    print(f"📈 Bump catalog version to v{major}.{new_minor}.0")
            elif "Cập nhật:" in updated_lines[idx] or "Updated:" in updated_lines[idx]:
                updated_lines[idx] = f"> **Cập nhật:** {current_date}\n"
                
    # Save the updated catalog
    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
        
    print(f"💾 Đã cập nhật và lưu danh mục tại {CATALOG_PATH} thành công!")

if __name__ == "__main__":
    main()
