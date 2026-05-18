# Visual Studio Code — Cài đặt chi tiết

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **OS hỗ trợ:** macOS 10.15+ / Windows 10+ / Linux (Ubuntu 20.04+, Debian, Fedora, Arch...)\
> **Thời lượng cài:** ~15-30 phút (cài + setup extension + theme)\
> **Khó:** ⭐ Easy

> 🎯 *VS Code là editor miễn phí phổ biến nhất thế giới, dùng được cho mọi ngôn ngữ. Bài này hướng dẫn cài + cấu hình ban đầu + extension cần thiết cho beginner.*

---

## 1️⃣ VS Code là gì + Khi nào cài

**Visual Studio Code (VS Code)** là *code editor* miễn phí, mã nguồn mở của Microsoft. Khác với IDE nặng (JetBrains, Visual Studio), VS Code nhẹ + linh hoạt qua hệ thống **extension** — bạn tự build editor phù hợp.

**Khi nào nên cài:**
- ✅ Bạn là **beginner** — VS Code là chuẩn ngầm cho người mới
- ✅ Code đa ngôn ngữ (Python, JS, Go, ...) trong cùng 1 editor
- ✅ Cần làm việc với Git visual + terminal tích hợp
- ✅ Muốn dùng AI assistant (Copilot, Codeium, Continue)
- ✅ Cộng tác qua *Live Share*

**Khi nào KHÔNG cần** (dùng cái khác):
- ❌ Bạn quen Vim/Neovim → dùng [Neovim setup](./neovim.md) (chưa có)
- ❌ Bạn cần IDE chuyên ngành — vd: full Java/Kotlin → [IntelliJ setup](./intellij.md) (chưa có)
- ❌ Bạn thích AI-first → cài [Cursor setup](./cursor.md) (chưa có — fork VS Code, tốt hơn cho AI)
- ❌ Server không có GUI → dùng `vim` hoặc `nano`

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Min | Recommend |
|---|---|---|
| **OS** | macOS 10.15 / Windows 10 / Ubuntu 20.04 | macOS 13+ / Windows 11 / Ubuntu 22.04+ |
| **RAM** | 1 GB | 4 GB+ (khi mở nhiều extension) |
| **Disk** | 500 MB | 2 GB+ (cache + extensions) |
| **Prerequisites** | Không | Git (cài kèm khuyên dùng) |

---

## 3️⃣ Cách cài — chọn 1 trong N option

### So sánh nhanh

| Option | Cách | Khi nào dùng | Khó |
|---|---|---|---|
| 🅰️ **Installer chính thức** | Tải `.dmg`/`.exe`/`.deb` từ trang chủ | Đơn giản nhất, ai cũng làm được | ⭐ |
| 🅱️ **Homebrew (macOS)** | `brew install --cask visual-studio-code` | Đã có Homebrew, dễ update sau | ⭐ |
| 🅲 **winget (Windows)** | `winget install Microsoft.VisualStudioCode` | Windows 10/11 hiện đại, native package manager | ⭐ |
| 🅳 **Snap (Linux)** | `sudo snap install code --classic` | Ubuntu — đơn giản nhất | ⭐ |
| 🅴 **APT repo (Linux Debian/Ubuntu)** | Thêm repo Microsoft → `apt install code` | Ổn định, auto-update qua hệ thống | ⭐⭐ |

→ Mình recommend **Option A** (installer) cho beginner — đơn giản, ai cũng làm được, không cần biết terminal trước.

---

### 🅰️ Option A: Installer chính thức (recommend cho beginner)

**Phù hợp**: Mọi beginner, không cần cài tool nào trước.

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

**Bước 4**: Mở VS Code lần đầu → có thể bỏ qua wizard, lát mình cấu hình bên dưới.

**Pros**:
- Đơn giản nhất, không cần biết terminal
- Có wizard hướng dẫn

**Cons**:
- Update phải tự click "Restart to update" — không tự động như package manager

---

### 🅱️ Option B: Homebrew (macOS)

**Phù hợp**: Đã cài [Homebrew](../../package-managers/setup/homebrew.md) (chưa có bài). Update sau dễ.

```bash
brew install --cask visual-studio-code
```

Mở:

```bash
open -a "Visual Studio Code"
# hoặc đơn giản
code .
```

**Pros**: Update bằng `brew upgrade` cùng với mọi app khác — gọn.\
**Cons**: Cần cài Homebrew trước (1 lần).

---

### 🅲 Option C: winget (Windows 10/11)

**Phù hợp**: Windows 10/11 đời mới (winget đi kèm). Mở **PowerShell** chạy:

```powershell
winget install Microsoft.VisualStudioCode
```

**Pros**: Native, không cần download installer thủ công.\
**Cons**: Windows < 10 không có.

---

### 🅳 Option D: Snap (Ubuntu)

```bash
sudo snap install code --classic
```

→ `--classic` cần thiết vì VS Code cần truy cập filesystem rộng.

**Pros**: 1 lệnh, auto-update.\
**Cons**: Snap khởi động chậm hơn deb một chút (cảm nhận được trên máy cũ).

---

### 🅴 Option E: APT repo (Debian/Ubuntu — dài hơn nhưng tốt nhất cho Linux)

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

**Pros**: Tích hợp tốt nhất với Ubuntu, auto-update qua `apt upgrade`.\
**Cons**: 6 bước, không dành cho beginner Linux.

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

## 5️⃣ Cấu hình ban đầu (settings)

### Cấu hình tối thiểu (BẮT BUỘC)

Mở **Command Palette**: `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Win/Linux) → gõ "Settings" → chọn "Preferences: Open Settings (UI)".

Hoặc edit file `settings.json` trực tiếp (`Cmd+Shift+P` → "Preferences: Open User Settings (JSON)"):

```json
{
  // Hiển thị
  "editor.fontSize": 14,
  "editor.fontFamily": "'Fira Code', 'Monaco', monospace",
  "editor.fontLigatures": true,
  "editor.lineNumbers": "on",
  "editor.minimap.enabled": false,
  "editor.wordWrap": "on",

  // Indent
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": true,

  // Save
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "editor.formatOnSave": true,

  // Terminal tích hợp
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.osx": "zsh",

  // Workspace
  "workbench.startupEditor": "none",
  "workbench.colorTheme": "Default Dark Modern",
  "workbench.iconTheme": "vs-seti"
}
```

### Cấu hình recommend (tùy chọn)

| Setting | Giá trị | Vì sao |
|---|---|---|
| `editor.fontFamily` | `Fira Code` / `JetBrains Mono` / `Cascadia Code` | Font có *ligature* — đẹp + dễ đọc operator |
| `editor.formatOnSave` | `true` | Tự format code khi save → consistent |
| `files.autoSave` | `afterDelay` | Tự save sau 1s — không sợ mất code |
| `editor.minimap.enabled` | `false` | Tắt minimap cho màn hình hẹp |
| `workbench.colorTheme` | `Default Dark Modern` | Theme tối mặc định (mới, đẹp) |

### Font Fira Code (nếu chọn)

Cài font trước khi setting `fontFamily`:
- macOS: `brew install --cask font-fira-code`
- Linux: `sudo apt install fonts-firacode`
- Windows: tải từ [github.com/tonsky/FiraCode/releases](https://github.com/tonsky/FiraCode/releases), giải nén, click chuột phải file .ttf → Install for all users

---

## 6️⃣ Extensions phổ biến

### 🌟 Must-have (beginner cài ngay)

| Extension | Chức năng | Vì sao cài |
|---|---|---|
| **GitLens** (`eamodio.gitlens`) | Visualize Git history, blame, file timeline | Hiểu code do ai viết, khi nào, vì sao |
| **Prettier** (`esbenp.prettier-vscode`) | Format JS/TS/HTML/CSS/Markdown | Code đẹp tự động |
| **Error Lens** (`usernamehw.errorlens`) | Hiển thị lỗi/warning ngay tại dòng | Beginner thấy lỗi sớm |
| **Material Icon Theme** (`pkief.material-icon-theme`) | Icon đẹp cho file/folder | Dễ scan file tree |
| **Code Spell Checker** (`streetsidesoftware.code-spell-checker`) | Phát hiện typo trong code/comment | Tránh sai chính tả var/function |

### ✅ Recommend (theo ngôn ngữ)

| Ngôn ngữ | Extension | Lý do |
|---|---|---|
| **Python** | `ms-python.python` + `ms-python.vscode-pylance` | Microsoft chính thức, đủ tool |
| **JavaScript/TypeScript** | `dbaeumer.vscode-eslint` | Linter chuẩn |
| **Go** | `golang.go` | Microsoft + Go team chính thức |
| **Rust** | `rust-lang.rust-analyzer` | LSP chuẩn |
| **Docker** | `ms-azuretools.vscode-docker` | Quản lý container trong UI |
| **YAML** | `redhat.vscode-yaml` | Schema validation |
| **Markdown** | `yzhang.markdown-all-in-one` | TOC, preview, shortcuts |

### 🟡 Optional (cài sau khi quen)

- `vscodevim.vim` — Vim keybinding (nếu muốn học Vim trong VS Code)
- `vscode-icons.vscode-icons` — alternative cho Material Icon Theme
- `oderwat.indent-rainbow` — màu hóa indent
- `aaron-bond.better-comments` — color comments TODO/FIXME/NOTE

### ❌ Skip (popular nhưng overkill)

- `liveshare.vsliveshare` — chỉ cài khi cần pair programming
- `wakatime.vscode-wakatime` — tracking time, không thiết yếu

### Cài extension qua command line

```bash
code --install-extension eamodio.gitlens
code --install-extension esbenp.prettier-vscode
code --install-extension ms-python.python
# ... etc
```

Hoặc viết script `install-extensions.sh` để chạy 1 lần khi setup máy mới.

---

## 7️⃣ Lỗi thường gặp

### ❌ Lỗi 1: `code: command not found` trong terminal

- **Triệu chứng**: Gõ `code .` → terminal báo lỗi
- **Nguyên nhân**: VS Code chưa thêm vào PATH
- **Cách fix**:
  - **macOS**: Mở VS Code GUI → `Cmd+Shift+P` → gõ "Shell Command: Install 'code' command in PATH" → Enter. Đóng terminal mở lại.
  - **Windows**: Chạy lại installer, tích "Add to PATH". Hoặc thủ công thêm `C:\Users\<user>\AppData\Local\Programs\Microsoft VS Code\bin` vào PATH.
  - **Linux**: Thường tự có. Nếu chưa: `sudo ln -s /usr/share/code/bin/code /usr/local/bin/code`

### ❌ Lỗi 2: Extension không load / "Loading..."

- **Triệu chứng**: Cài extension nhưng không hoạt động
- **Nguyên nhân**: Cache cũ, hoặc conflict version
- **Cách fix**:
  ```
  Cmd+Shift+P → "Developer: Reload Window"
  ```
  Nếu vẫn lỗi → uninstall extension → restart VS Code → cài lại.

### ❌ Lỗi 3: Format on save không chạy

- **Triệu chứng**: Save file mà code không tự format
- **Nguyên nhân**: Chưa chọn default formatter cho ngôn ngữ đó
- **Cách fix**: Click chuột phải trong file → "Format Document With..." → "Configure Default Formatter" → chọn (vd Prettier).

### ❌ Lỗi 4: Settings sync không hoạt động

- **Triệu chứng**: Bật Settings Sync mà settings không sync giữa máy
- **Nguyên nhân**: Chưa đăng nhập GitHub / Microsoft account
- **Cách fix**: `Cmd+Shift+P` → "Settings Sync: Turn On..." → đăng nhập GitHub.

### ❌ Lỗi 5: Mở folder lớn → VS Code chậm/treo

- **Triệu chứng**: Mở folder >10000 file → VS Code load mãi
- **Nguyên nhân**: Tự index toàn bộ + watch file changes
- **Cách fix**: Thêm vào `settings.json`:
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

---

## 8️⃣ Update + Uninstall

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

> ⚠️ **Cẩn thận**: Xóa `~/.vscode` và `~/Library/Application Support/Code` (Mac) sẽ mất **tất cả extension + settings**. Nếu muốn giữ → chỉ uninstall app, không xóa folder settings.

---

## 9️⃣ Khi nào KHÔNG nên dùng VS Code — Alternative

| Editor | Strength | Phù hợp ai |
|---|---|---|
| **VS Code** (đang nói) | Free, hệ extension lớn, đa ngôn ngữ, AI sẵn (Copilot) | Đa số dev (>70% thị phần) |
| **Cursor** ([setup](./cursor.md) chưa có) | Fork VS Code + AI-native (built-in Claude/GPT, hiểu codebase) | Coder dùng AI heavy |
| **Neovim** ([setup](./neovim.md) chưa có) | Cực nhẹ, chạy trong terminal, keyboard-driven | Power user, làm việc qua SSH |
| **IntelliJ IDEA** (chưa có setup) | IDE Java/Kotlin chuyên sâu | Java/Kotlin/Android dev |
| **JetBrains PyCharm** | IDE Python chuyên sâu | Python heavy dev cần refactor mạnh |
| **Zed** | Cực nhanh (Rust + GPU), collab realtime | Macbook M-series, thích minimal |
| **Sublime Text** | Cực nhẹ, mở file lớn nhanh | Edit text/log nhanh, không full IDE |

> 💡 **Khuyến nghị 2026**: Beginner → **VS Code** đầu tiên. Sau 6 tháng → thử Cursor để có AI mạnh hơn nếu thích. Sau 2-3 năm → có thể thử Neovim/IntelliJ cho specialized work.

---

## 🔗 Liên kết

### Bài học dùng VS Code

- (Sẽ có) [`02_Tools/editor/lessons/01_basic/00_vs-code-shortcuts.md`](../lessons/) — phím tắt phải nhớ
- (Sẽ có) [`02_Tools/editor/lessons/01_basic/01_debugging-in-vs-code.md`](../lessons/)
- [Zero to Coder Roadmap — Stage 1](../../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-cơ-bản-2-3-tuần) link tới bài này

### Tài nguyên ngoài

- [VS Code Official Docs](https://code.visualstudio.com/docs) — chính thức, đầy đủ nhất
- [VS Code Extension Marketplace](https://marketplace.visualstudio.com/) — tìm extension
- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks) — official cheatsheet
- [Awesome VS Code](https://github.com/viatsko/awesome-vscode) — curated list extensions + themes
- [VS Code Keyboard Shortcuts (PDF)](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf) — in ra dán bàn

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — setup guide đầu tiên trong kho. Dogfood `setup_template.md`.
