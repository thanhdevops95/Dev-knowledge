# Hướng dẫn VSCode Tips & Tricks

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp phím tắt, extensions và cài đặt hữu ích cho Visual Studio Code.

---

## ⌨️**PHÍM TẮT THƯỜNG DÙNG**

### Di chuyển & Chọn

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + G` | Nhảy đến dòng số |
| `Ctrl + P` | Mở file nhanh (Quick Open) |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + D` | Chọn từ tiếp theo giống nhau |
| `Ctrl + Shift + L` | Chọn TẤT CẢ từ giống nhau |
| `Alt + Click` | Thêm cursor ở vị trí click |
| `Ctrl + L` | Chọn cả dòng |
| `Ctrl + Shift + K` | Xóa dòng |
| `Alt + ↑/↓` | Di chuyển dòng lên/xuống |
| `Shift + Alt + ↑/↓` | Nhân đôi dòng lên/xuống |
| `Ctrl + /` | Comment/Uncomment |
| `Ctrl + Shift + /` | Block comment |

### Tìm kiếm & Thay thế

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + F` | Tìm trong file |
| `Ctrl + H` | Tìm và thay thế |
| `Ctrl + Shift + F` | Tìm trong toàn bộ project |
| `Ctrl + Shift + H` | Thay thế trong toàn bộ project |
| `F3` / `Shift + F3` | Tìm tiếp / Tìm trước |

### File & Editor

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + N` | File mới |
| `Ctrl + S` | Lưu file |
| `Ctrl + Shift + S` | Lưu tất cả |
| `Ctrl + W` | Đóng tab |
| `Ctrl + Shift + T` | Mở lại tab vừa đóng |
| `Ctrl + Tab` | Chuyển tab |
| `Ctrl + \` | Chia đôi editor |
| `Ctrl + 1/2/3` | Chuyển sang editor 1/2/3 |
| `Ctrl + B` | Ẩn/hiện sidebar |
| `Ctrl + J` | Ẩn/hiện terminal |
| `Ctrl + `` ` | Mở terminal |

### Code Navigation

| Phím tắt | Chức năng |
|----------|-----------|
| `F12` | Go to Definition |
| `Alt + F12` | Peek Definition |
| `Shift + F12` | Find All References |
| `Ctrl + Shift + O` | Go to Symbol |
| `Ctrl + -` | Quay lại vị trí trước |
| `Ctrl + Shift + -` | Tiến tới vị trí sau |

### Formatting

| Phím tắt | Chức năng |
|----------|-----------|
| `Shift + Alt + F` | Format document |
| `Ctrl + K Ctrl + F` | Format selection |
| `Ctrl + ]` | Indent dòng |
| `Ctrl + [` | Outdent dòng |

---

## 🧩**EXTENSIONS KHUYÊN DÙNG**

### Python Development

| Extension | Mô tả |
|-----------|-------|
| **Python** (Microsoft) | Cần thiết cho Python |
| **Pylance** | IntelliSense nâng cao |
| **Python Debugger** | Debug Python |
| **autopep8** hoặc **Black** | Auto format code |
| **isort** | Sắp xếp import |

### Productivity

| Extension | Mô tả |
|-----------|-------|
| **GitLens** | Xem ai sửa dòng code, lịch sử git |
| **Git Graph** | Visualize git branch |
| **Error Lens** | Hiện lỗi ngay trên dòng code |
| **Todo Tree** | Highlight TODO, FIXME |
| **Bracket Pair Colorizer** | Tô màu ngoặc |
| **indent-rainbow** | Tô màu indent |
| **Path Intellisense** | Gợi ý đường dẫn file |
| **Auto Rename Tag** | Tự động đổi tên tag HTML/XML |

### Theme & Icons

| Extension | Mô tả |
|-----------|-------|
| **One Dark Pro** | Theme tối phổ biến |
| **Dracula Official** | Theme Dracula |
| **Material Icon Theme** | Icon đẹp cho file |
| **vscode-icons** | Icon file/folder |

### Snippets & Utilities

| Extension | Mô tả |
|-----------|-------|
| **Code Spell Checker** | Kiểm tra chính tả |
| **Prettier** | Format HTML/CSS/JS |
| **Live Server** | Chạy web server local |
| **REST Client** | Test API trong VSCode |
| **Thunder Client** | Postman trong VSCode |

---

## ⚙️**CÀI ĐẶT HỮU ÍCH**

Mở Settings: `Ctrl + ,` hoặc `File > Preferences > Settings`

### settings.json mẫu

```json
{
    // ===== EDITOR =====
    "editor.fontSize": 14,
    "editor.fontFamily": "'Fira Code', 'Consolas', monospace",
    "editor.fontLigatures": true,
    "editor.tabSize": 4,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,
    "editor.cursorBlinking": "smooth",
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.smoothScrolling": true,
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true,
    "editor.linkedEditing": true,
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": true,
    "editor.stickyScroll.enabled": true,
    
    // ===== FILES =====
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": true,
        "**/node_modules": true
    },
    
    // ===== TERMINAL =====
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    
    // ===== PYTHON =====
    "python.formatting.provider": "autopep8",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "[python]": {
        "editor.tabSize": 4,
        "editor.formatOnSave": true
    },
    
    // ===== WORKBENCH =====
    "workbench.colorTheme": "One Dark Pro",
    "workbench.iconTheme": "material-icon-theme",
    "workbench.startupEditor": "none",
    "workbench.tree.indent": 16,
    
    // ===== GIT =====
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    
    // ===== EXPLORER =====
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false
}
```

---

## 🐞**DEBUG PYTHON**

### Tạo file launch.json

1. Nhấn `F5` hoặc vào Run > Start Debugging
2. Chọn "Python File"
3. VSCode tạo file `.vscode/launch.json`

### launch.json mẫu

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: main.py",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal"
        }
    ]
}
```

### Phím tắt Debug

| Phím tắt | Chức năng |
|----------|-----------|
| `F5` | Start/Continue Debug |
| `F9` | Toggle Breakpoint |
| `F10` | Step Over |
| `F11` | Step Into |
| `Shift + F11` | Step Out |
| `Shift + F5` | Stop Debug |
| `Ctrl + Shift + F5` | Restart Debug |

---

## 📁**WORKSPACE SETTINGS**

Tạo file `.vscode/settings.json` trong folder dự án để có settings riêng.

### Ví dụ cho dự án Python

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
    "python.formatting.provider": "black",
    "editor.rulers": [80, 120],
    "files.exclude": {
        "**/__pycache__": true,
        "**/venv": true
    }
}
```

---

## 🔥**MẸO HAY**

### 1. Multi-cursor editing
- `Ctrl + Alt + ↑/↓`: Thêm cursor ở dòng trên/dưới
- `Ctrl + D`: Chọn từ tiếp theo giống nhau
- `Ctrl + Shift + L`: Chọn tất cả từ giống nhau

### 2. Rename Symbol
- `F2`: Đổi tên biến/hàm ở tất cả nơi sử dụng

### 3. Quick Fix
- `Ctrl + .`: Hiện gợi ý sửa lỗi

### 4. Emmet (HTML/CSS)
- Gõ `div.container>ul>li*5` rồi `Tab` → Tạo HTML nhanh

### 5. Zen Mode
- `Ctrl + K Z`: Chế độ tập trung, ẩn hết sidebar

### 6. Snippets tự tạo
- File > Preferences > Configure User Snippets

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
