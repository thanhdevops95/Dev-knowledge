# 🛠️ Công cụ Developer — Setup môi trường làm việc

> `[BEGINNER]` — Thiết lập workspace hiệu quả ngay từ đầu

---

## VS Code — Editor phổ biến nhất

### Extensions bắt buộc

```
Prettier - Code formatter          → Tự động format code
ESLint                             → Lint JavaScript/TypeScript
GitLens                           → Xem git history, blame, diff
Error Lens                         → Hiện lỗi ngay trên dòng code
Todo Highlight                     → Highlight TODO, FIXME
Docker                             → Quản lý containers
Remote - SSH                       → Code trên remote server
REST Client                        → Test API ngay trong VS Code
Indent Rainbow                     → Màu sắc indent cho dễ đọc
Material Icon Theme                → Icons đẹp
GitHub Copilot                     → AI pair programmer
```

### Settings quan trọng (`settings.json`)

```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.fontSize": 14,
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', monospace",
    "editor.fontLigatures": true,
    "editor.tabSize": 2,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": true,
    "editor.inlineSuggest.enabled": true,
    "editor.cursorBlinking": "expand",

    "terminal.integrated.fontSize": 13,
    "terminal.integrated.defaultProfile.osx": "zsh",

    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "files.exclude": {
        "**/.git": true,
        "**/node_modules": true,
        "**/__pycache__": true
    },

    "workbench.colorTheme": "One Dark Pro",
    "workbench.startupEditor": "none",

    "[javascript][typescript][typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    },
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

### Shortcuts hay dùng

| Shortcut (Mac) | Tác dụng |
|---|---|
| `Cmd + P` | Quick open file |
| `Cmd + Shift + P` | Command palette |
| `Cmd + /` | Toggle comment |
| `Alt + Click` | Multi cursor |
| `Cmd + D` | Select next occurrence |
| `Ctrl + G` | Jump to line |
| `Cmd + B` | Toggle sidebar |
| `Ctrl + `` ` | Toggle terminal |
| `Cmd + Shift + F` | Search in all files |
| `F12` | Go to definition |
| `Alt + F12` | Peek definition |
| `Shift + F12` | Find all references |
| `F2` | Rename symbol |

---

## Terminal Setup — Zsh + Oh My Zsh

```bash
# Cài Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Cài plugins hữu ích
# zsh-autosuggestions — gợi ý lệnh từ history
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting — highlight cú pháp
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Cài Starship prompt (đẹp và nhanh)
brew install starship
echo 'eval "$(starship init zsh)"' >> ~/.zshrc
```

### `.zshrc` hữu ích

```bash
# Aliases hay dùng
alias ll="ls -la"
alias g="git"
alias gs="git status"
alias gc="git commit -m"
alias gp="git push"
alias gl="git log --oneline --graph"
alias d="docker"
alias dc="docker compose"
alias k="kubectl"

# Python
alias py="python3"
alias pip="pip3"
alias venv="python3 -m venv .venv && source .venv/bin/activate"

# Navigation
alias ..="cd .."
alias ...="cd ../.."
alias dev="cd ~/work"

# Utilities
alias ports="lsof -i -P -n | grep LISTEN"       # Xem port đang dùng
alias ip="ipconfig getifaddr en0"                # Xem IP local
alias flush-dns="sudo dscacheutil -flushcache"  # macOS flush DNS

# Functions
mkcd() { mkdir -p "$1" && cd "$1"; }           # mkdir + cd

# fzf — fuzzy finder
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
```

---

## Git Config

```bash
# ~/.gitconfig
[user]
    name = Jesse
    email = jesse@example.com

[core]
    editor = code --wait
    autocrlf = input
    pager = diff-so-fancy | less --tabs=4 -RFX

[color]
    ui = auto

[alias]
    st = status
    co = checkout
    br = branch
    lg = log --oneline --graph --decorate --all
    undo = reset --soft HEAD~1
    unstage = restore --staged
    discard = restore
    stsh = stash --include-untracked
    nuke = !git reset --hard && git clean -fd

[pull]
    rebase = false

[push]
    default = current

[init]
    defaultBranch = main

[diff]
    tool = vscode

[merge]
    tool = vscode
```

---

## Postman / HTTP Clients

### REST Client (VS Code Extension)

```http
### Đăng nhập
POST http://localhost:8000/auth/login
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "password123"
}

### Lấy profile (dùng biến từ response trên)
GET http://localhost:8000/users/me
Authorization: Bearer {{access_token}}

### Tạo post
POST http://localhost:8000/posts
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "title": "Bài viết mới",
    "content": "Nội dung..."
}
```

---

## Makefile — Automation đơn giản

```makefile
# Makefile
.PHONY: dev build test lint clean docker-up docker-down

dev:
	npm run dev

build:
	npm run build

test:
	npm run test

lint:
	npm run lint

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

# Migrations
migrate:
	python manage.py migrate

migrate-create:
	python manage.py makemigrations

# All in one
setup: docker-up migrate
	@echo "✅ Ready! Run 'make dev' to start"

clean:
	docker compose down -v
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
```

```bash
make dev           # Chạy dev server
make setup         # Setup toàn bộ
make docker-up     # Start containers
```

---

## Useful CLI Tools

```bash
# Cài qua Homebrew (macOS)
brew install \
    bat \          # cat với syntax highlighting
    eza \          # ls đẹp hơn
    fd \           # find nhanh hơn
    ripgrep \      # grep nhanh hơn (rg)
    fzf \          # fuzzy finder
    jq \           # parse JSON trong terminal
    httpie \       # http client đẹp hơn curl
    tldr \         # man page ngắn gọn
    tree \         # xem cấu trúc thư mục
    ncdu           # disk usage analyzer

# Dùng
bat file.py                    # Xem file với syntax highlight
eza -la --git                  # ls với git status
fd "*.py" src/                 # Tìm file Python trong src/
rg "TODO" --type py            # Tìm TODO trong file .py
echo '{"name":"Jesse"}' | jq . # Format JSON
http GET api.example.com/users  # HTTP request đẹp
tldr docker                    # Quick reference
```

---

## Browser DevTools

### Tabs hay dùng

**Elements** — Xem/sửa DOM và CSS realtime
**Console** — Debug JavaScript, log
**Network** — Xem HTTP requests, size, timing
**Performance** — Profile render performance
**Application** — localStorage, cookies, IndexedDB
**Lighthouse** — Audit performance, SEO, accessibility

```javascript
// Console tricks
console.log("Simple log");
console.table([{name: "Alice"}, {name: "Bob"}]);  // Dạng bảng đẹp
console.time("timer"); /* code */ console.timeEnd("timer");
console.group("Group name"); /* logs */ console.groupEnd();
console.trace();  // Stack trace
```

---

## Bài tập thực hành

- [ ] Setup VS Code với tất cả extensions và settings trên
- [ ] Cấu hình Oh My Zsh với aliases cá nhân
- [ ] Tạo Makefile cho project hiện tại
- [ ] Chụp và phân tích Network tab khi load 1 trang web

---

## Tài nguyên thêm

- [VS Code Tips and Tricks](https://code.visualstudio.com/docs/getstarted/tips-and-tricks)
- [Oh My Zsh](https://ohmyz.sh/) — Zsh framework
- [Starship](https://starship.rs/) — Terminal prompt đẹp
- [fzf](https://github.com/junegunn/fzf) — Fuzzy finder cực mạnh
