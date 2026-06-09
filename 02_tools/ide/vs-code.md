# 🛠️ VS Code — User Guide

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 20/05/2026\
> **OS hỗ trợ:** macOS 10.15+ / Windows 10+ / Linux\
> **Loại:** Tool individual — focused vào VS Code

> 🎯 *User guide đầy đủ cho VS Code — cài, UI tour, settings, extensions, workflows, shortcuts. **CHỈ về VS Code** — so sánh với Cursor/Neovim/JetBrains đã ở [00_what-is-ide.md](./00_what-is-ide.md).*

---

## Tình huống

Bạn đã đọc [00_what-is-ide.md](./00_what-is-ide.md), chọn VS Code làm editor đầu tiên. Tốt — VS Code là default cho ~80% beginner.

File này dẫn bạn:
1. **Cài đúng cách** (5 option theo OS) — 15-30 phút
2. **Hiểu UI** (8 panel chính) — biết click đâu
3. **Cấu hình đẹp** (settings + font + theme) — code 8h không mỏi
4. **Cài extension đáng** (10 must-have) — không cài 50 cái rác
5. **Workflow hay** (debug + git + terminal + multi-root) — năng suất 2x

Cuối bài bạn có VS Code setup production-ready, dùng cho mọi project tiếp theo.

---

## 1️⃣ Vậy VS Code là gì?

**Visual Studio Code (VS Code)** là *code editor* miễn phí, mã nguồn mở của Microsoft, phát hành lần đầu 2015. Khác với IDE nặng (JetBrains, Visual Studio), VS Code **nhẹ** + **linh hoạt qua extension** — bạn tự build editor phù hợp ngôn ngữ và workflow.

🪞 **Ẩn dụ**: VS Code giống **iPhone trống app** — nhỏ gọn ban đầu, cài app (extension) tuỳ thích biến nó thành cái gì cũng được — IDE Python, IDE Go, Markdown editor, Jupyter notebook, terminal multiplexer...

**Số liệu nhanh**:
- ~75% thị phần dev editor (Stack Overflow 2025)
- ~50,000 extension trên Marketplace
- Update mỗi tháng (rolling release)
- Owner: Microsoft, free mãi (kể cả thương mại)

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Min | Recommend |
|---|---|---|
| **OS** | macOS 10.15 / Win 10 / Ubuntu 20.04 | macOS 13+ / Win 11 / Ubuntu 22.04+ |
| **RAM** | 1 GB | 4 GB+ (mở nhiều extension) |
| **Disk** | 500 MB | 2 GB+ (cache + extensions) |
| **Prerequisites** | Không | Git (cài kèm khuyên dùng) |

---

## 3️⃣ Cài VS Code — chọn 1 trong 5 option

### So sánh nhanh

| Option | Cách | Khi nào dùng | Khó |
|---|---|---|---|
| 🅰️ **Installer chính thức** | Tải `.dmg`/`.exe`/`.deb` từ trang chủ | Đơn giản nhất, ai cũng làm được | ⭐ |
| 🅱️ **Homebrew (macOS)** | `brew install --cask visual-studio-code` | Đã có Homebrew | ⭐ |
| 🅲 **winget (Windows)** | `winget install Microsoft.VisualStudioCode` | Windows 10/11 hiện đại | ⭐ |
| 🅳 **Snap (Linux)** | `sudo snap install code --classic` | Ubuntu — đơn giản | ⭐ |
| 🅴 **APT repo (Linux)** | Thêm repo Microsoft → `apt install code` | Ổn định, auto-update | ⭐⭐ |

→ Khuyến nghị **Option A** (installer) cho beginner — đơn giản, không cần biết terminal trước.

### 🅰️ Option A: Installer chính thức (recommend cho beginner)

**Bước 1**: Vào [code.visualstudio.com](https://code.visualstudio.com/)

Trang chủ tự detect OS và hiển thị nút download phù hợp.

**Bước 2**: Tải installer
- **macOS**: file `.zip` → mở → kéo VS Code vào Applications
- **Windows**: file `VSCodeUserSetup-x64-<version>.exe` → chạy
- **Linux (.deb)**: file `code_*.deb` → `sudo dpkg -i code_*.deb`
- **Linux (.rpm)**: file `code-*.rpm` → `sudo rpm -i code-*.rpm`

**Bước 3 (Windows)**: Trong installer, **TÍCH 4 ô sau**:

- [x] Add "Open with Code" action to Windows Explorer file context menu
- [x] Add "Open with Code" action to Windows Explorer directory context menu
- [x] Register Code as an editor for supported file types
- [x] Add to PATH (recommended)

→ 4 ô này giúp dùng VS Code thuận tiện hơn nhiều. Đừng skip.

**Bước 4**: Mở VS Code lần đầu → có thể bỏ qua wizard, lát mình cấu hình ở §6.

### 🅱️ Option B: Homebrew (macOS)

```bash
brew install --cask visual-studio-code
```

Mở:

```bash
code .
```

### 🅲 Option C: winget (Windows 10/11)

Mở **PowerShell**:

```powershell
winget install Microsoft.VisualStudioCode
```

### 🅳 Option D: Snap (Ubuntu)

```bash
sudo snap install code --classic
```

→ `--classic` cần thiết vì VS Code cần truy cập filesystem rộng.

### 🅴 Option E: APT repo (Debian/Ubuntu)

```bash
# 1. Cài Microsoft GPG key
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg

# 2. Thêm repo
echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null

# 3. Cài
sudo apt update
sudo apt install code
```

---

## 4️⃣ Verify cài đúng

Mở terminal (hoặc PowerShell trên Windows):

```bash
code --version
```

Output mong đợi:

```
1.92.0
abc123def456
x64
```

3 dòng = OK. Nếu báo `command not found`:

- **macOS**: Mở VS Code → `Cmd+Shift+P` → gõ "Shell Command: Install 'code' command in PATH" → Enter
- **Windows**: chạy lại installer, đảm bảo TÍCH "Add to PATH"
- **Linux**: thường tự có sau install

Verify mở GUI:

```bash
code .
```

→ VS Code mở folder hiện tại. Thấy giao diện = OK.

---

## 5️⃣ UI Tour — Hiểu mọi panel

VS Code chia màn hình thành 7 phần. Hiểu mỗi phần làm gì để không "click bừa".

```
┌─────────────────────────────────────────────────────────────────┐
│ ① Menu bar (File / Edit / View / ...)                           │
├──┬───────────────────────┬──────────────────────────────────────┤
│  │ ② Side Bar            │ ③ Editor (multi-tab)                 │
│ ⓪│   Explorer / Search   │   - Code window                       │
│  │   Source Control      │   - Multi-cursor                      │
│ A │   Run & Debug         │   - Split view                        │
│ c │   Extensions          │                                       │
│ t │                       │                                       │
│ i │                       │                                       │
│ v │                       │                                       │
│ i │                       ├──────────────────────────────────────┤
│ t │                       │ ④ Panel (Terminal / Problems /        │
│ y │                       │    Output / Debug Console)            │
│   │                       │                                       │
├──┴───────────────────────┴──────────────────────────────────────┤
│ ⑤ Status bar (Git branch / Errors / Line:Col / Encoding / ...)  │
└─────────────────────────────────────────────────────────────────┘
   ⓪ Activity Bar (icons dọc bên trái)
```

### ⓪ Activity Bar (bên trái, dọc)

5 icon mặc định, click chuyển panel ở Side Bar:

| Icon | Tên | Phím tắt | Để làm gì |
|---|---|---|---|
| 📂 | Explorer | `Cmd/Ctrl+Shift+E` | Cây file của project |
| 🔍 | Search | `Cmd/Ctrl+Shift+F` | Tìm/replace toàn project |
| 🔀 | Source Control | `Cmd/Ctrl+Shift+G` | Git changes, stage, commit, push |
| 🐞 | Run & Debug | `Cmd/Ctrl+Shift+D` | Chạy + debug code |
| 📦 | Extensions | `Cmd/Ctrl+Shift+X` | Tìm + cài + quản extension |

Click chuột phải Activity Bar → "Hide" để giấu bớt icon ít dùng.

### ② Side Bar (content theo Activity Bar đang chọn)

- **Explorer**: file tree. Click chuột phải file → New File / Rename / Reveal in Finder.
- **Search**: tìm text trong toàn project. Hỗ trợ regex (button `.*`).
- **Source Control**: changes hiện tại, click `+` để stage, viết commit message, click ✓ để commit.
- **Run & Debug**: profile debug (cần `launch.json`).
- **Extensions**: tab "Installed" / "Recommended" / "Marketplace".

### ③ Editor area (giữa)

- **Multi-tab**: nhiều file mở cùng lúc, drag thứ tự
- **Split editor**: `Cmd/Ctrl + \` chia đôi, làm việc 2 file song song
- **Breadcrumb**: trên cùng — đường dẫn folder + tên symbol hiện tại
- **Multi-cursor**: `Option/Alt + Click` để thêm cursor; `Cmd/Ctrl + D` để select word tiếp theo cùng

### ④ Panel (dưới editor)

- **Terminal** (`Ctrl + \``) — terminal tích hợp, chạy bash/zsh/PowerShell
- **Problems** — lỗi + warning từ extension (TypeScript, ESLint, ...)
- **Output** — log từ extension và build task
- **Debug Console** — REPL khi debug

> 💡 Terminal tích hợp **CỰC TIỆN** — không phải mở Terminal app riêng. Mở bằng `` Ctrl+` `` (backtick).

### ⑤ Status Bar (dưới cùng)

Đọc trái sang phải:
- **Branch hiện tại** (vd `main`) — click để switch branch
- **Sync status** (↑↓ với arrow) — click để push/pull
- **Problems indicator** (number errors/warnings) — click để mở Problems panel
- **Encoding** (vd `UTF-8`) — click đổi encoding
- **Line endings** (LF / CRLF)
- **Indentation** (Spaces:2 hoặc Tab Size:4)
- **Language mode** (vd `Python`) — click đổi syntax highlight

### Command Palette — "thanh ma thuật"

`Cmd/Ctrl + Shift + P` — search MỌI lệnh VS Code:
- `> reload` → reload window
- `> theme` → đổi theme
- `> snippet` → tạo snippet
- `> git` → mọi lệnh git

→ **Phím tắt quan trọng nhất**. Không nhớ shortcut → mở Command Palette gõ.

---

## 6️⃣ Cấu hình ban đầu (settings)

### Mở settings

3 cách:
1. **UI Settings**: `Cmd/Ctrl + ,` — search + click
2. **JSON Settings**: `Cmd/Ctrl + Shift + P` → "Preferences: Open User Settings (JSON)"
3. **Workspace Settings**: cùng vậy nhưng "Open Workspace Settings (JSON)" — chỉ áp dụng cho project hiện tại

### Cấu hình tối thiểu khuyến nghị (paste vào `settings.json`)

```json
{
  // Hiển thị
  "editor.fontSize": 14,
  "editor.fontFamily": "'Fira Code', 'JetBrains Mono', 'Monaco', monospace",
  "editor.fontLigatures": true,
  "editor.lineNumbers": "on",
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",
  "editor.cursorBlinking": "smooth",
  "editor.smoothScrolling": true,
  "editor.bracketPairColorization.enabled": true,

  // Indent
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": true,
  "editor.renderWhitespace": "boundary",

  // Save
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "editor.formatOnSave": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  // Terminal tích hợp
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.defaultProfile.linux": "bash",

  // Workspace
  "workbench.startupEditor": "none",
  "workbench.colorTheme": "Default Dark Modern",
  "workbench.iconTheme": "vs-seti",
  "workbench.editor.enablePreview": false,

  // Performance
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/objects/**": true,
    "**/dist/**": true,
    "**/build/**": true,
    "**/venv/**": true,
    "**/__pycache__/**": true
  },

  // Git
  "git.autofetch": true,
  "git.confirmSync": false,

  // Telemetry (privacy)
  "telemetry.telemetryLevel": "off"
}
```

### Settings sync giữa nhiều máy

Bật ngay — đổi máy không phải setup lại:

`Cmd/Ctrl + Shift + P` → "Settings Sync: Turn On..." → đăng nhập GitHub account.

VS Code sync: settings, keybindings, snippets, extensions, UI state qua tất cả máy bạn login.

### Font Fira Code (recommend)

Font có ligature (`==`, `=>`, `!=` thành ký hiệu đẹp):

- **macOS**: `brew install --cask font-fira-code`
- **Linux**: `sudo apt install fonts-firacode`
- **Windows**: tải từ [github.com/tonsky/FiraCode/releases](https://github.com/tonsky/FiraCode/releases), giải nén, right-click file `.ttf` → Install for all users

Alternative tốt: **JetBrains Mono**, **Cascadia Code**, **MonoLisa** (paid).

### Theme đẹp

`Cmd/Ctrl + K, Cmd/Ctrl + T` để mở theme switcher.

Khuyến nghị 2026:
- **Default Dark Modern** (built-in, đẹp + balanced)
- **One Dark Pro** (Atom-inspired, ấm)
- **Dracula Official** (purple, popular)
- **Tokyo Night** (modern, contrast cao)
- **GitHub Light** (nếu thích sáng)

---

## 7️⃣ Extensions — Cài gì, skip gì?

### 🌟 Must-have (beginner cài ngay — 10 cái)

| Extension | ID | Chức năng |
|---|---|---|
| **GitLens** | `eamodio.gitlens` | Visualize Git history, blame inline |
| **Prettier** | `esbenp.prettier-vscode` | Format JS/TS/HTML/CSS/Markdown |
| **Error Lens** | `usernamehw.errorlens` | Hiển thị lỗi/warning ngay tại dòng |
| **Material Icon Theme** | `pkief.material-icon-theme` | Icon đẹp cho file/folder |
| **Code Spell Checker** | `streetsidesoftware.code-spell-checker` | Phát hiện typo |
| **Indent Rainbow** | `oderwat.indent-rainbow` | Màu hoá indent — đỡ nhầm |
| **Better Comments** | `aaron-bond.better-comments` | Color comment TODO/FIXME/NOTE |
| **Path Intellisense** | `christian-kohler.path-intellisense` | Autocomplete đường dẫn file |
| **Auto Rename Tag** | `formulahendry.auto-rename-tag` | Đổi tên HTML/XML tag tự động |
| **Bracket Pair Colorizer** | (built-in từ 2022) | Match brackets bằng màu |

### ✅ Theo ngôn ngữ (cài khi cần)

| Ngôn ngữ | Extension |
|---|---|
| **Python** | `ms-python.python` + `ms-python.vscode-pylance` |
| **JavaScript/TypeScript** | `dbaeumer.vscode-eslint` |
| **Go** | `golang.go` |
| **Rust** | `rust-lang.rust-analyzer` |
| **Docker** | `ms-azuretools.vscode-docker` |
| **Kubernetes** | `ms-kubernetes-tools.vscode-kubernetes-tools` |
| **YAML** | `redhat.vscode-yaml` |
| **Markdown** | `yzhang.markdown-all-in-one` + `bierner.markdown-mermaid` |
| **Java** | `vscjava.vscode-java-pack` (bộ Microsoft) |

### 🤖 AI Coding

| Extension | Free tier | Đặc trưng |
|---|---|---|
| **GitHub Copilot** | Free cho student/OSS, $10/mo cá nhân | Autocomplete mạnh |
| **Continue** | Free | Open source, hỗ trợ Claude/local LLM |
| **Codeium** | Free | Free autocomplete tốt |
| **Tabnine** | Free tier | Local model option |

### 🟡 Optional (cài sau khi quen)

- `vscodevim.vim` — Vim keybinding (nếu muốn học modal editing)
- `humao.rest-client` — gọi REST API thẳng trong VS Code
- `gruntfuggly.todo-tree` — gom mọi TODO trong codebase
- `vincaslt.highlight-matching-tag` — highlight tag HTML khớp
- `wayou.vscode-todo-highlight` — highlight TODO/FIXME

### ❌ Skip (popular nhưng overkill cho beginner)

- `liveshare.vsliveshare` — chỉ cài khi cần pair programming
- `wakatime.vscode-wakatime` — tracking time, không thiết yếu
- Đa số "icon pack" trùng nhau — chỉ cần 1

### Cài qua command line

```bash
# Cài 1 extension
code --install-extension eamodio.gitlens

# Cài bulk (script setup máy mới)
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension usernamehw.errorlens
code --install-extension ms-python.python
# ... etc
```

### Sao lưu danh sách extension

```bash
# Export
code --list-extensions > vscode-extensions.txt

# Import (máy mới)
cat vscode-extensions.txt | xargs -L 1 code --install-extension
```

---

## 8️⃣ Workflows phổ biến

### Workflow 1 — Mở project nhanh

```bash
cd ~/projects/myapp
code .                    # mở folder hiện tại
code file.py              # mở 1 file riêng
code --diff a.py b.py     # so sánh 2 file
code --reuse-window .     # mở vào window đang có thay vì window mới
```

### Workflow 2 — Git tích hợp (không cần CLI)

Side Bar → Source Control (`Cmd/Ctrl + Shift + G`):
1. Xem changes (diff inline)
2. Click `+` bên file để stage
3. Gõ commit message ở textbox trên
4. Click ✓ để commit
5. Click `Sync` để push + pull cùng lúc

→ Với **GitLens** cài: hover lên dòng code thấy ai sửa khi nào.

### Workflow 3 — Debug Python

1. Cài Python extension
2. Mở file `.py`
3. Click margin bên trái số dòng → tạo breakpoint đỏ
4. `F5` để start debug
5. Hiện debugger UI:
   - **Continue** / **Step over** / **Step into** / **Step out**
   - **Variables** panel — xem giá trị
   - **Watch** — track expression
   - **Debug Console** — REPL với context hiện tại

→ Tương tự cho JS/TS/Go/Java.

### Workflow 4 — Multi-cursor edit (sửa nhiều chỗ cùng lúc)

| Cần | Cách |
|---|---|
| Sửa từ X thành Y trong toàn file | `Cmd/Ctrl + D` lặp lại để select tất cả X → gõ Y |
| Thêm cursor cụ thể | `Option/Alt + Click` chỗ muốn thêm |
| Cursor xuống dòng dưới cùng cột | `Option/Alt + Cmd/Ctrl + ↓` |
| Selection mọi dòng có pattern | `Cmd/Ctrl + Shift + L` (sau khi đã select 1 word) |

### Workflow 5 — Remote development (SSH/Container/WSL)

3 extension Microsoft đáng cài:

| Extension | Mục đích |
|---|---|
| `ms-vscode-remote.remote-ssh` | Mở folder qua SSH như local |
| `ms-vscode-remote.remote-containers` | Dev trong Docker container |
| `ms-vscode-remote.remote-wsl` | Dev trong WSL (Windows) |

→ Sau khi cài, `F1` → "Remote-SSH: Connect to Host..." → nhập `user@host` → editor mở folder remote, terminal tự đi vào server.

### Workflow 6 — Tasks & Build

Tạo file `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run app",
      "type": "shell",
      "command": "python main.py",
      "group": "build"
    },
    {
      "label": "Run tests",
      "type": "shell",
      "command": "pytest -v",
      "group": "test"
    }
  ]
}
```

`Cmd/Ctrl + Shift + B` → chọn task để chạy. Không phải gõ lệnh lại.

### Workflow 7 — Snippets (code template)

`Cmd/Ctrl + Shift + P` → "Snippets: Configure User Snippets" → chọn ngôn ngữ → định nghĩa:

```json
{
  "Python class template": {
    "prefix": "pyclass",
    "body": [
      "class ${1:ClassName}:",
      "    def __init__(self, ${2:args}):",
      "        ${3:pass}",
      ""
    ],
    "description": "Tạo class Python"
  }
}
```

Gõ `pyclass` trong file `.py` → Tab → expand. `$1`, `$2`, `$3` là vị trí cursor sẽ nhảy qua.

---

## 9️⃣ Shortcuts cheatsheet

### 🌟 10 phím tắt phải nhớ (Mac / Win-Linux)

| Mục đích | Mac | Win/Linux |
|---|---|---|
| Command Palette (lệnh ma thuật) | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Quick Open file | `Cmd+P` | `Ctrl+P` |
| Toggle terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| Toggle Side Bar | `Cmd+B` | `Ctrl+B` |
| Search trong file | `Cmd+F` | `Ctrl+F` |
| Search trong toàn project | `Cmd+Shift+F` | `Ctrl+Shift+F` |
| Comment line | `Cmd+/` | `Ctrl+/` |
| Multi-cursor (select next match) | `Cmd+D` | `Ctrl+D` |
| Đi tới symbol/function | `Cmd+Shift+O` | `Ctrl+Shift+O` |
| Format document | `Shift+Option+F` | `Shift+Alt+F` |

### 📋 Cheatsheet đầy đủ

In ra dán bàn:
- **Mac**: [keyboard-shortcuts-macos.pdf](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)
- **Win**: [keyboard-shortcuts-windows.pdf](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf)
- **Linux**: [keyboard-shortcuts-linux.pdf](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf)

### Custom keybinding

`Cmd/Ctrl + K, Cmd/Ctrl + S` → mở Keyboard Shortcuts UI → search command → click pencil để rebind.

---

## 🔟 Troubleshooting

### ❌ `code: command not found` trong terminal

- **macOS**: VS Code → `Cmd+Shift+P` → gõ "Shell Command: Install 'code' command in PATH" → Enter. Đóng terminal mở lại.
- **Windows**: chạy lại installer, tích "Add to PATH". Hoặc thủ công thêm `C:\Users\<user>\AppData\Local\Programs\Microsoft VS Code\bin` vào PATH.
- **Linux**: thường tự có. Nếu chưa: `sudo ln -s /usr/share/code/bin/code /usr/local/bin/code`

### ❌ Extension không load / "Loading..."

```
Cmd/Ctrl + Shift + P → "Developer: Reload Window"
```

Nếu vẫn lỗi → uninstall extension → restart VS Code → cài lại.

### ❌ Format on save không chạy

Click chuột phải trong file → "Format Document With..." → "Configure Default Formatter" → chọn (vd Prettier).

Hoặc thêm trong settings.json per language:

```json
"[python]": {
  "editor.defaultFormatter": "ms-python.python",
  "editor.formatOnSave": true
}
```

### ❌ Settings sync không hoạt động

`Cmd/Ctrl+Shift+P` → "Settings Sync: Turn On..." → đăng nhập GitHub.

### ❌ Mở folder lớn → VS Code chậm/treo

Thêm vào `settings.json`:

```json
"files.watcherExclude": {
  "**/node_modules/**": true,
  "**/.git/objects/**": true,
  "**/dist/**": true,
  "**/build/**": true,
  "**/venv/**": true,
  "**/__pycache__/**": true
}
```

### ❌ VS Code ăn RAM 4GB+ với folder nhỏ

- Disable extension không dùng: Extensions panel → click ⚙️ → Disable (per workspace)
- Có extension memory leak — check với `Cmd+Shift+P` → "Developer: Show Running Extensions"
- Disable `editor.semanticHighlighting` nếu file nặng

### ❌ Copilot suggestion không hiện

- Check status bar — biểu tượng Copilot phải sáng
- `Cmd+Shift+P` → "GitHub Copilot: Check status"
- Đăng nhập lại nếu cần

---

## 1️⃣1️⃣ Update + Uninstall

### Update VS Code

| Cách cài | Update |
|---|---|
| Option A (Installer) | VS Code tự báo có update → click "Restart to update" |
| Option B (Homebrew) | `brew upgrade --cask visual-studio-code` |
| Option C (winget) | `winget upgrade Microsoft.VisualStudioCode` |
| Option D (Snap) | `sudo snap refresh code` |
| Option E (APT) | `sudo apt update && sudo apt upgrade code` |

### Uninstall hoàn toàn

| OS | Cách |
|---|---|
| **macOS** | Kéo "Visual Studio Code" từ Applications vào Trash. Xóa settings: `rm -rf ~/.vscode ~/Library/Application\ Support/Code` |
| **Windows** | Settings → Apps → Uninstall "Visual Studio Code". Xóa settings: `%APPDATA%\Code` |
| **Linux** | `sudo apt remove code` (deb) hoặc `sudo snap remove code` (snap). Xóa settings: `rm -rf ~/.config/Code ~/.vscode` |

> ⚠️ **Cẩn thận**: Xóa folder settings = mất **tất cả extension + settings**. Nếu muốn giữ → chỉ uninstall app, không xóa folder settings.

---

## 1️⃣2️⃣ Cấu hình khuyến nghị cho từng vai trò

### Profile A — Python dev

Extensions: Python pack + Pylance + Ruff + Black + GitLens + Error Lens + Material Icon

Settings thêm:

```json
"[python]": {
  "editor.defaultFormatter": "charliermarsh.ruff",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  }
},
"python.testing.pytestEnabled": true
```

### Profile B — Web frontend (React/TS)

Extensions: ESLint + Prettier + Auto Rename Tag + Tailwind CSS IntelliSense + ES7+ React snippets

```json
"[typescriptreact]": {
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true
},
"emmet.includeLanguages": {"javascript": "javascriptreact"}
```

### Profile C — DevOps / IaC

Extensions: Docker + Kubernetes + YAML + Terraform + Ansible + Remote-SSH

```json
"[yaml]": {
  "editor.defaultFormatter": "redhat.vscode-yaml",
  "editor.tabSize": 2
}
```

### Profile D — Data Engineer

Extensions: Python + Jupyter + SQL Tools + Rainbow CSV + Data Wrangler

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-ide.md](./00_what-is-ide.md) — So sánh VS Code với Cursor/Neovim/JetBrains
- 🧭 [Zero to Coder Stage 1](../../00_roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-tối-thiểu-2-3-tuần) — beginner cài VS Code đầu tiên
- 📚 [Git lesson 00](../git/lessons/01_basic/00_what-is-git.md) — Git + VS Code tích hợp (GitLens extension)

### Cursor — alternative AI-first

- `cursor.md` (chưa có) — Cursor là fork VS Code + Claude/GPT built-in, công thức "switch khi nào"

### 🌐 Tài nguyên tham khảo khác

- [VS Code Official Docs](https://code.visualstudio.com/docs) — chính thức
- [VS Code Tips & Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks) — official cheatsheet
- [Extension Marketplace](https://marketplace.visualstudio.com/) — tìm extension
- [Awesome VS Code](https://github.com/viatsko/awesome-vscode) — curated extension list
- [VS Code GitHub Discussions](https://github.com/microsoft/vscode/discussions) — community Q&A

---

## 📌 Nhật ký thay đổi (Changelog)

- **v2.0.0 (20/05/2026)** — **Restructure thành full tool guide** (move từ `02_tools/ide/vs-code.md`):
  - Title: "VS Code — Cài đặt chi tiết" → "**VS Code — User Guide**"
  - Mở bằng tình huống thay vì khô
  - Thêm §5 **UI Tour** (ASCII layout + 7 panel chi tiết + Command Palette)
  - Thêm §8 **Workflows** (Git tích hợp, Debug, Multi-cursor, Remote SSH, Tasks, Snippets — 7 workflow)
  - Thêm §9 **Shortcuts cheatsheet** (10 must-know + link PDF official)
  - Thêm §12 **Profile cấu hình** theo vai trò (Python/Frontend/DevOps/Data)
  - Bổ sung 4 must-have extensions (Indent Rainbow, Better Comments, Path Intellisense, Auto Rename Tag)
  - Bổ sung AI Coding section (Copilot, Continue, Codeium, Tabnine)
  - Fix relative paths sau khi move (depth 3 → 2: `../../../` → `../../`)
  - Bỏ section so sánh editor cuối (đã có ở [00_what-is-ide.md](./00_what-is-ide.md))
- **v1.0.0 (16/05/2026)** — Bản đầu tiên ở `02_tools/ide/vs-code.md` — setup guide.
