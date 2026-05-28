# Git — Cài đặt + cấu hình ban đầu

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **OS hỗ trợ:** macOS / Linux / Windows\
> **Thời lượng cài:** ~10-15 phút\
> **Khó:** ⭐ Easy

> 🎯 *Git là hệ thống version control được dùng bởi 90%+ developer trên thế giới. Bài này hướng dẫn cài + cấu hình ban đầu trên 3 OS.*

---

## 1️⃣ Git là gì + Khi nào cài

**Git** là hệ thống **distributed version control** (kiểm soát phiên bản phân tán) — lưu lịch sử code của bạn, cho phép quay lại version cũ, làm việc nhóm, xử lý conflict.

**Khi nào nên cài**: NGAY LẬP TỨC nếu bạn là coder. Mọi project (kể cả 1 file) nên track bằng Git.

**Khi nào KHÔNG cần**: dùng GUI tool 100% (SourceTree, GitHub Desktop) — nhưng vẫn cần cài Git CLI làm backend.

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Tối thiểu | Recommend |
|---|---|---|
| **OS** | macOS 10.14 / Win 8.1 / bất kỳ Linux | macOS 13+ / Win 11 / Ubuntu 22+ |
| **Disk** | 50 MB | 500 MB (kèm Git LFS sau) |
| **Prerequisites** | Không | Account [GitHub](https://github.com) |

---

## 3️⃣ Cài Git

### So sánh nhanh

| OS | Option | Khi nào dùng |
|---|---|---|
| macOS | 🅰️ Homebrew | Đã có Homebrew, update dễ |
| macOS | 🅱️ Xcode CLI tools | Không cần Homebrew, nhanh nhất |
| Linux Ubuntu/Debian | 🅲 `apt` | Phổ biến nhất |
| Linux Fedora | 🅳 `dnf` | Fedora users |
| Windows | 🅴 Git for Windows | Phổ biến nhất + kèm Git Bash |
| Windows | 🅵 winget | Windows 10/11 |

### 🅰️ macOS — Homebrew (recommend)

```bash
brew install git
```

### 🅱️ macOS — Xcode CLI tools

```bash
xcode-select --install
```

→ Popup GUI hỏi "Install" → click → đợi 5-10 phút. Git có sẵn sau khi xong.

### 🅲 Linux — Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y git
```

### 🅳 Linux — Fedora/RHEL

```bash
sudo dnf install -y git
```

### 🅴 Windows — Git for Windows (recommend)

1. Tải [Git for Windows](https://git-scm.com/download/win) → cài
2. Trong installer, **đảm bảo tích các option sau** (mặc định OK):
   - ✅ "Git Bash Here" trong Explorer
   - ✅ "Use Git from the command line and also from 3rd-party software" (PATH)
   - ✅ Default editor: VS Code (nếu đã cài) hoặc Vim
   - ✅ "Override the default branch name" → `main` (thay master)
   - ✅ "Checkout Windows-style, commit Unix-style line endings"
3. Sau cài: dùng **Git Bash** hoặc PowerShell

### 🅵 Windows — winget

```powershell
winget install --id Git.Git -e --source winget
```

---

## 4️⃣ Verify cài đúng

```bash
git --version
```

Kết quả:

```
git version 2.45.0
```

Nếu báo `command not found` (Mac/Linux) hoặc `not recognized` (Windows):
- Mac/Linux: cài lại theo §3, đảm bảo `/usr/local/bin` trong PATH
- Windows: chạy lại installer + tích "Use Git from command line"

---

## 5️⃣ Cấu hình ban đầu (BẮT BUỘC trước khi commit)

Git cần biết bạn là ai để gắn vào commit. Chạy 3 lệnh sau **NGAY sau khi cài**:

```bash
git config --global user.name "Tên Của Bạn"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

> ⚠️ **Email phải khớp** với email GitHub nếu sau này muốn commit hiện tên/avatar trên GitHub. Nếu muốn ẩn email, dùng `<id>+<username>@users.noreply.github.com` (GitHub Settings → Emails).

### Cấu hình recommend (tùy chọn)

```bash
# Default editor (VS Code)
git config --global core.editor "code --wait"

# Pull strategy mặc định (rebase thay vì merge)
git config --global pull.rebase true

# Auto setup remote khi push lần đầu
git config --global push.autoSetupRemote true

# Color output
git config --global color.ui auto

# Alias rút gọn (làm việc nhanh hơn)
git config --global alias.s "status -sb"
git config --global alias.l "log --oneline --graph --decorate -20"
git config --global alias.co checkout
git config --global alias.br branch
```

Xem lại config đã set:

```bash
git config --global --list
```

---

## 6️⃣ Extensions / GUI tools phổ biến

### 🌟 VS Code Git extensions (must-have nếu dùng VS Code)

| Extension | Vai trò |
|---|---|
| **Git built-in** | VS Code có sẵn — không cần cài thêm |
| **GitLens** (`eamodio.gitlens`) | Visualize blame, history, file timeline |
| **Git Graph** (`mhutchie.git-graph`) | Graph view của commit history |
| **GitHub Pull Requests** (`github.vscode-pull-request-github`) | Review PR trong VS Code |

### 🌟 GUI tools độc lập (nếu muốn)

| Tool | OS | Phù hợp |
|---|---|---|
| **GitHub Desktop** | Mac/Win | Beginner — UI đơn giản |
| **SourceTree** | Mac/Win | Free, đầy đủ tính năng |
| **GitKraken** | Mac/Win/Linux | UI đẹp, paid for private repo |
| **Fork** | Mac/Win | Nhẹ, nhanh |
| **lazygit** | Terminal | Power user, keyboard-driven |

> 💡 Beginner: bắt đầu với CLI + GitLens. GUI tools cài thêm khi cần xem history visual.

### 🌟 GitHub CLI (recommend)

```bash
# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# Linux
# Theo https://github.com/cli/cli#installation
```

Login:

```bash
gh auth login
```

→ Tạo/clone/review PR từ terminal — cực tiện sau này.

---

## 7️⃣ Lỗi thường gặp

### ❌ Lỗi 1: `Please tell me who you are`

```
*** Please tell me who you are.
Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

- **Triệu chứng**: chạy `git commit` báo lỗi này
- **Nguyên nhân**: chưa cấu hình `user.name` + `user.email`
- **Fix**: chạy 2 lệnh trong error message (§5)

### ❌ Lỗi 2: `fatal: not a git repository`

- **Triệu chứng**: chạy `git status` báo lỗi
- **Nguyên nhân**: đang đứng trong folder chưa init git
- **Fix**: `git init` để tạo repo, hoặc `cd` vào folder đã có repo

### ❌ Lỗi 3: SSL certificate error (Windows hay gặp)

```
fatal: unable to access ... SSL certificate problem
```

- **Nguyên nhân**: corporate proxy / firewall block
- **Fix tạm**: `git config --global http.sslVerify false` (KHÔNG khuyên — chỉ tạm)
- **Fix đúng**: cài CA cert của công ty vào Git

### ❌ Lỗi 4: Line endings (CRLF vs LF)

```
warning: LF will be replaced by CRLF
```

- **Nguyên nhân**: Windows dùng CRLF, Mac/Linux dùng LF — Git phải convert
- **Fix**:
  - Windows: `git config --global core.autocrlf true` (convert khi checkout)
  - Mac/Linux: `git config --global core.autocrlf input` (KHÔNG convert)
- **Tốt nhất**: thêm `.gitattributes` vào repo:
  ```
  * text=auto
  ```

### ❌ Lỗi 5: `git push` lỗi authentication (GitHub bỏ password 2021)

```
remote: Support for password authentication was removed
```

- **Nguyên nhân**: GitHub không cho dùng password để push từ 2021
- **Fix**: dùng 1 trong 2 cách:
  - **HTTPS + Personal Access Token (PAT)**: GitHub Settings → Developer settings → Personal access tokens → tạo token → dùng thay password
  - **SSH key**: setup trong bài [`ssh-key-github.md`](./ssh-key-github.md) (chưa có)

---

## 8️⃣ Update + Uninstall

### Update

| Cách cài | Update |
|---|---|
| Homebrew | `brew upgrade git` |
| Xcode CLI | macOS Software Update tự update |
| apt | `sudo apt update && sudo apt upgrade git` |
| Git for Windows | Mở Git Bash → `git update-git-for-windows` |
| winget | `winget upgrade Git.Git` |

### Uninstall

| OS | Cách |
|---|---|
| macOS (brew) | `brew uninstall git` |
| Linux | `sudo apt remove git` hoặc `sudo dnf remove git` |
| Windows | Settings → Apps → Uninstall "Git" |

> ⚠️ Uninstall **KHÔNG xóa** config global ở `~/.gitconfig`. Nếu muốn xóa hết: `rm ~/.gitconfig ~/.git-credentials`.

---

## 9️⃣ Alternative VCS (so sánh)

| VCS | Mô hình | Phù hợp |
|---|---|---|
| **Git** (đang nói) | Distributed | 95% project hiện đại |
| **Mercurial (hg)** | Distributed | Facebook, Mozilla dùng |
| **Subversion (SVN)** | Centralized | Legacy enterprise |
| **Perforce** | Centralized | Game dev (file lớn) |
| **Fossil** | Distributed + wiki + bug tracker tích hợp | Solo dev |

→ Beginner 2026: **chỉ Git**. Học hg/svn khi gặp legacy project.

---

## 🔗 Liên kết

### Bài học dùng Git

- [What is Git (intro)](../lessons/01_basic/00_what-is-git.md) — sau khi cài xong, đọc bài này tiếp
- [Git init + first commit](../lessons/01_basic/01_init-and-first-commit.md)

### Setup liên quan

- [SSH key cho GitHub](./ssh-key-github.md) (chưa có) — sau khi cài xong Git
- [GitHub Desktop](./github-desktop.md) (chưa có) — GUI client

### Tài nguyên ngoài

- [Pro Git Book (free)](https://git-scm.com/book/vi/v2) — tiếng Việt!
- [GitHub Skills](https://skills.github.com/) — interactive courses

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — setup Git đầy đủ 9 section theo `setup_template.md`.
