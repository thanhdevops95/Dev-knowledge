# ✏️ Vim & Neovim — Text Editor trong Terminal

> `[BEGINNER → INTERMEDIATE]` — Prerequisite: `01-terminal-basics.md`
> Editor mạnh nhất cho server, SSH, và developer productivity.

---

## Tại sao cần học Vim?

- Server production **không có GUI** — Vim/Vi có sẵn trên **mọi Linux/macOS**
- **SSH** vào server → cần edit config → Vim là lựa chọn duy nhất
- Vim keybindings có trong **mọi editor** (VS Code, JetBrains, Obsidian)
- Tốc độ editing **nhanh hơn đáng kể** khi thành thạo — tay không rời keyboard

> **"Vim has a steep learning curve, but the plateau is very high."** — Bạn sẽ khổ 2 tuần đầu, nhưng sau đó editing nhanh gấp 3x.

---

## 1. Modes — 4 chế độ của Vim

Vim hoạt động dựa trên **modes** — khác biệt lớn nhất so với các editor khác:

```
┌──────────────────────────────────────────┐
│                                          │
│   NORMAL ←──── ESC ────── INSERT         │
│      │                      ↑            │
│      │    i, a, o, I, A, O  │            │
│      │                      │            │
│      ├──── v, V, Ctrl+V ──→ VISUAL       │
│      │                                   │
│      └──── : ──────────────→ COMMAND      │
│                                          │
└──────────────────────────────────────────┘
```

| Mode | Vào bằng | Thoát bằng | Dùng để |
|---|---|---|---|
| **NORMAL** | `ESC` | — | Di chuyển, xóa, copy, paste |
| **INSERT** | `i`, `a`, `o` | `ESC` | Gõ text |
| **VISUAL** | `v`, `V`, `Ctrl+V` | `ESC` | Chọn text |
| **COMMAND** | `:` | `Enter` / `ESC` | Lưu, thoát, tìm/thay |

---

## 2. Survival Kit — Sống sót ngày đầu

```
# MỞ FILE:
vim file.txt        # Mở file (tạo nếu chưa có)
vim +20 file.txt    # Mở ở dòng 20

# LƯU & THOÁT (từ Normal mode):
:w                  # Save (write)
:q                  # Quit
:wq                 # Save & quit
:q!                 # Quit WITHOUT saving ⚠️
ZZ                  # Save & quit (shortcut)
ZQ                  # Quit without saving (shortcut)

# VÀO INSERT MODE:
i                   # Insert trước cursor
a                   # Insert sau cursor
o                   # Insert dòng mới bên dưới
O                   # Insert dòng mới bên trên
I                   # Insert đầu dòng
A                   # Insert cuối dòng

# THOÁT INSERT MODE:
ESC                 # Về Normal mode
Ctrl+[              # Tương tự ESC (gần hơn)
jk                  # Custom mapping phổ biến
```

---

## 3. Movement — Di chuyển (Normal mode)

```
# ── Cơ bản ──
h  j  k  l          # ← ↓ ↑ → (thay vì arrow keys)

# ── Từ ──
w                    # Next word (đầu)
b                    # Previous word (đầu)
e                    # Next word (cuối)
W  B  E              # Word bao gồm cả dấu (WORD)

# ── Dòng ──
0                    # Đầu dòng
^                    # Ký tự đầu tiên (không phải whitespace)
$                    # Cuối dòng
gg                   # Đầu file
G                    # Cuối file
5G  hoặc :5          # Đến dòng 5

# ── Màn hình ──
Ctrl+D               # Scroll down nửa trang
Ctrl+U               # Scroll up nửa trang
Ctrl+F               # Scroll down 1 trang
Ctrl+B               # Scroll up 1 trang
H                    # Top of screen
M                    # Middle of screen
L                    # Bottom of screen
zz                   # Center current line on screen

# ── Tìm ký tự trên dòng ──
f{char}              # Jump TO character (forward)
F{char}              # Jump TO character (backward)
t{char}              # Jump BEFORE character
;                    # Repeat last f/F/t/T
```

---

## 4. Editing — Chỉnh sửa (Normal mode)

### Verb + Motion = Action

Vim editing = **operator** + **motion**. Ví dụ: `d` (delete) + `w` (word) = `dw` (delete word).

```
# ── Operators (Verbs) ──
d                    # Delete (cut)
c                    # Change (delete + enter insert mode)
y                    # Yank (copy)

# ── Combinations ──
dw                   # Delete word
d$  hoặc D           # Delete to end of line
dd                   # Delete entire line
3dd                  # Delete 3 lines
diw                  # Delete inner word (không kèm space)
daw                  # Delete a word (kèm space)
di"                  # Delete inside quotes: "hello" → ""
da"                  # Delete including quotes: "hello" → (nothing)
di(                  # Delete inside parentheses
dit                  # Delete inside HTML tag

# ── Change (delete + insert) ──
cw                   # Change word
ciw                  # Change inner word
ci"                  # Change inside quotes
cc                   # Change entire line
C                    # Change to end of line

# ── Yank (copy) ──
yw                   # Yank word
yy                   # Yank line
3yy                  # Yank 3 lines

# ── Paste ──
p                    # Paste after cursor
P                    # Paste before cursor

# ── Undo / Redo ──
u                    # Undo
Ctrl+R               # Redo
.                    # Repeat last command ⭐
```

### Text Objects — "inner" và "around"

```
i = inner (bên trong, không kèm delimiters)
a = around (bao gồm cả delimiters)

ciw    # Change inner word:     "hello world" → "| world"
caw    # Change a word:         "hello world" → "|world"
ci"    # Change inner quotes:   "hello" → "|"
ca"    # Change around quotes:  "hello" → |
ci(    # Change inner parens:   (hello) → (|)
ci{    # Change inner braces:   {hello} → {|}
cit    # Change inner tag:      <p>hello</p> → <p>|</p>
```

---

## 5. Search & Replace

```
# ── Tìm kiếm ──
/pattern             # Search forward
?pattern             # Search backward
n                    # Next match
N                    # Previous match
*                    # Search word under cursor (forward)
#                    # Search word under cursor (backward)
:noh                 # Clear search highlighting

# ── Tìm & Thay ──
:s/old/new/          # Replace first on current line
:s/old/new/g         # Replace ALL on current line
:%s/old/new/g        # Replace ALL in file
:%s/old/new/gc       # Replace ALL with confirmation
:10,20s/old/new/g    # Replace in lines 10-20
```

---

## 6. Visual Mode — Chọn text

```
v                    # Character-wise selection
V                    # Line-wise selection
Ctrl+V               # Block (column) selection ⭐

# Sau khi chọn:
d                    # Delete selected
y                    # Yank (copy) selected
>                    # Indent right
<                    # Indent left
~                    # Toggle case
u                    # Lowercase
U                    # Uppercase

# Block selection (Ctrl+V):
# 1. Ctrl+V → select column
# 2. I → type text → ESC
# → Text inserted on ALL selected lines! ⭐
```

---

## 7. Buffers, Windows, Tabs

```
# ── Buffers (files đang mở) ──
:e file.txt          # Open file in new buffer
:ls                  # List buffers
:bn                  # Next buffer
:bp                  # Previous buffer
:bd                  # Delete (close) buffer

# ── Windows (splits) ──
:sp file.txt         # Horizontal split
:vsp file.txt        # Vertical split
Ctrl+W h/j/k/l      # Navigate between windows
Ctrl+W =             # Equal size windows
Ctrl+W _             # Maximize current window
Ctrl+W q             # Close window

# ── Tabs ──
:tabnew file.txt     # New tab
gt                   # Next tab
gT                   # Previous tab
:tabclose            # Close tab
```

---

## 8. Neovim — Vim hiện đại

**Neovim** (nvim) là fork hiện đại của Vim với:
- **Lua config** thay vì VimScript
- **Built-in LSP** (Language Server Protocol)
- **Tree-sitter** parser cho syntax highlighting chính xác
- Plugin ecosystem mạnh hơn

### Config cơ bản (~/.config/nvim/init.lua)

```lua
-- Options
vim.opt.number = true           -- Line numbers
vim.opt.relativenumber = true   -- Relative line numbers
vim.opt.tabstop = 4             -- Tab width
vim.opt.shiftwidth = 4          -- Indent width
vim.opt.expandtab = true        -- Spaces instead of tabs
vim.opt.clipboard = "unnamedplus" -- System clipboard
vim.opt.ignorecase = true       -- Case insensitive search
vim.opt.smartcase = true        -- Unless uppercase used
vim.opt.termguicolors = true    -- True colors

-- Keymaps
vim.g.mapleader = " "           -- Space as leader key
vim.keymap.set("i", "jk", "<ESC>")  -- jk to escape
vim.keymap.set("n", "<leader>w", ":w<CR>")  -- Space+w to save
vim.keymap.set("n", "<leader>q", ":q<CR>")  -- Space+q to quit
```

### Essential Neovim Plugins

| Plugin | Chức năng |
|---|---|
| **lazy.nvim** | Plugin manager (lazy-loading) |
| **telescope.nvim** | Fuzzy finder (files, grep, buffers) |
| **nvim-lspconfig** | Language Server Protocol |
| **nvim-cmp** | Autocompletion |
| **nvim-treesitter** | Enhanced syntax highlighting |
| **oil.nvim** | File explorer |
| **gitsigns.nvim** | Git integration |
| **which-key.nvim** | Keybinding helper |

---

## 9. Vim trong VS Code

```json
// settings.json — VS Code Vim extension
{
  "vim.enable": true,
  "vim.insertModeKeyBindings": [
    { "before": ["j", "k"], "after": ["<Esc>"] }
  ],
  "vim.normalModeKeyBindings": [
    { "before": ["<leader>", "w"], "commands": ["workbench.action.files.save"] },
    { "before": ["<leader>", "e"], "commands": ["workbench.action.toggleSidebarVisibility"] }
  ],
  "vim.leader": "<space>",
  "vim.useSystemClipboard": true,
  "vim.hlsearch": true
}
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Ở INSERT mode liên tục | Chỉ vào INSERT khi cần gõ, ESC ngay | Normal mode = mode chính |
| 2 | Dùng arrow keys | Dùng h/j/k/l | Nhanh hơn, tay không rời home row |
| 3 | Delete từng ký tự | Dùng text objects: `diw`, `ci"` | Xóa theo "đơn vị" (word, sentence, block) |
| 4 | Học hết keybindings cùng lúc | Học vài keys/tuần, dùng đến thuộc | Spaced repetition hiệu quả hơn |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Mở file, edit, save, quit — lặp lại 10 lần
- [ ] **Bài 2 (Dễ):** Di chuyển chỉ bằng h/j/k/l + w/b/e — không dùng arrow keys
- [ ] **Bài 3 (Trung bình):** Dùng `ci"`, `di(`, `caw` để edit code — practice text objects
- [ ] **Bài 4 (Trung bình):** Setup Neovim basic config với LSP cho 1 ngôn ngữ
- [ ] **Bài 5 (Khó):** Hoàn thành [Vim Adventures](https://vim-adventures.com/) hoặc `vimtutor`

---

## Tài nguyên thêm

- **`vimtutor`** — Built-in tutorial (chạy `vimtutor` trong terminal)
- [Vim Adventures](https://vim-adventures.com/) — Game học Vim
- [Practical Vim (Drew Neil)](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/) — Best Vim book
- [ThePrimeagen — Vim playlist](https://www.youtube.com/c/ThePrimeagen) — YouTube
- [Neovim Kickstart](https://github.com/nvim-lua/kickstart.nvim) — Neovim starter config
- [Vim Cheat Sheet](https://vim.rtorr.com/) — Visual reference
