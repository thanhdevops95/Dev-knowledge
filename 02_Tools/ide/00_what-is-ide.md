# 🛠️ IDE / Editor — Chọn loại nào cho mình?

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 20/05/2026\
> **Loại:** Tool category — overview + so sánh + khuyến nghị\
> **Đọc trước:** Không bắt buộc

> 🎯 *Trước khi cài editor đầu tiên, bạn cần biết "thị trường có gì + chọn cái nào theo profile của mình". File này so sánh 7 editor/IDE phổ biến + recommend theo case. Cài chi tiết → đi vào từng file riêng (`vs-code.md`, `cursor.md`, ...).*

---

## Tình huống — beginner đứng trước "choice paralysis"

Bạn được sếp giao project mới: *"Cài editor đi, ngày mai bắt đầu."*

Bạn Google "best code editor 2026". Kết quả:
- 📰 Blog A: *"VS Code is the best"*
- 📰 Blog B: *"Why I switched from VS Code to Cursor"*
- 📰 Blog C: *"Neovim — once you go modal, you don't go back"*
- 📰 Blog D: *"JetBrains pays for itself in 1 month"*
- 📰 Reddit: 47 comments, 8 different opinions

→ **Choice paralysis**. Mỗi blog viết bởi 1 người có context khác. Bạn không biết blog nào nói về **profile của bạn**.

File này giải quyết: liệt kê **mọi lựa chọn chính**, so sánh **theo tiêu chí khách quan**, khuyến nghị **theo profile cụ thể**. Đọc 10 phút → pick đúng cái, không hối tiếc 6 tháng sau.

---

## 1️⃣ Trước tiên — IDE khác Editor thế nào?

Đây là chỗ beginner hay nhầm:

| | **Editor** | **IDE** (Integrated Development Environment) |
|---|---|---|
| Bản chất | Phần mềm chỉnh sửa text + plugin tuỳ chọn | Bộ tích hợp: editor + debugger + build + test + DB tool... |
| Trọng lượng | Nhẹ (50-300 MB RAM) | Nặng (1-3 GB RAM) |
| Linh hoạt | Cao — tự build qua extension | Thấp — có sẵn theo ngôn ngữ chính |
| Ví dụ | VS Code, Sublime, Vim, Neovim | IntelliJ IDEA, PyCharm, Visual Studio, Xcode |
| Phù hợp | Beginner, đa ngôn ngữ, scripting | Pro dev 1 ngôn ngữ, project lớn, enterprise |

🪞 **Ẩn dụ**: Editor giống **dao Thuỵ Sĩ** (1 con dao + nhiều lưỡi gắn thêm) — gọn nhẹ, linh hoạt. IDE giống **bộ dụng cụ thợ mộc** (15 cái tool riêng trong hộp) — to nặng, nhưng từng cái sắc và mạnh trong việc riêng.

> 💡 Ranh giới ngày càng mờ. **VS Code** + 20 extension = gần như IDE. **IntelliJ Ultimate** + plugin = gần như editor đa năng. Khái niệm này hữu ích nhưng đừng cứng nhắc.

---

## 2️⃣ Thị trường hiện có gì (2026)?

7 lựa chọn chính, chia 3 nhóm:

### Nhóm 1: Editor đa năng (lightweight, plugin-based)

| Editor | Owner | Free? | OS | Đặc trưng |
|---|---|---|---|---|
| **VS Code** ⭐ | Microsoft | ✅ Free | Mac/Win/Linux | Phổ biến nhất (~75% thị phần dev), ecosystem extension lớn nhất |
| **Cursor** | Anysphere | 💸 $20/tháng (free tier nhẹ) | Mac/Win/Linux | Fork VS Code + AI native (Claude/GPT built-in) |
| **Zed** | Zed Industries | ✅ Free | Mac/Linux (Win soon) | Cực nhanh (Rust + GPU), collab realtime |
| **Sublime Text** | Sublime HQ | 💸 $99 (free unlimited trial) | Mac/Win/Linux | Cực nhẹ, mở file 10GB không lag |

### Nhóm 2: Modal editor (terminal, keyboard-driven)

| Editor | Free? | Đặc trưng |
|---|---|---|
| **Neovim** | ✅ Free | Modal (vim keybinding), config bằng Lua, chạy qua SSH ngon |
| **Helix** | ✅ Free | Modal post-vim — Kakoune-inspired, batteries included |

### Nhóm 3: IDE chuyên ngành (heavy, full-feature)

| IDE | Owner | Free tier | Ngôn ngữ chính |
|---|---|---|---|
| **JetBrains IDEs** (IntelliJ/PyCharm/WebStorm/...) | JetBrains | ✅ Community (limited) / 💸 Ultimate $169/năm | Java, Python, JS, Go, Rust... mỗi IDE riêng |
| **Visual Studio** | Microsoft | ✅ Community / 💸 Pro $1199/năm | C#, .NET, C++ Windows |
| **Xcode** | Apple | ✅ Free | Swift, Objective-C (iOS/macOS only) |
| **Android Studio** | Google | ✅ Free | Kotlin, Java (Android only) |

---

## 3️⃣ Bảng so sánh 7 lựa chọn chính

| Tiêu chí | VS Code | Cursor | Zed | Neovim | IntelliJ Ultimate | Sublime | Xcode |
|---|---|---|---|---|---|---|---|
| **Chi phí** | Free | $20/mo | Free | Free | $169/năm | $99 once | Free |
| **OS** | Mac/Win/Linux | Mac/Win/Linux | Mac/Linux | Mọi OS | Mac/Win/Linux | Mac/Win/Linux | Mac only |
| **Tốc độ khởi động** | ~3s | ~3s | <1s ⚡ | <1s ⚡ | ~10s 🐢 | <1s ⚡ | ~5s |
| **RAM khi mở project** | ~500MB | ~600MB | ~200MB | ~50MB | ~2GB | ~150MB | ~1GB |
| **Tích hợp AI native** | Copilot (paid) | ⭐ Claude+GPT built-in | (Zed AI sắp có) | qua plugin | qua plugin | Không | Không |
| **Ecosystem extension** | ⭐⭐⭐ Lớn nhất (~50k) | ⭐⭐⭐ (= VS Code) | ⭐ Nhỏ | ⭐⭐ Đa dạng | ⭐⭐ JetBrains marketplace | ⭐⭐ Khá | ⭐ Apple ecosystem |
| **Cấu hình** | UI / settings.json | UI / settings.json | UI / TOML | Lua/Vim script (khó) | UI / properties | JSON | UI (ít options) |
| **Curve học** | Dễ (1 tuần) | Dễ (giống VS Code) | Trung bình | **Khó** (1-3 tháng) | Trung bình | Dễ | Trung bình |
| **Refactor mạnh?** | OK (qua extension) | OK | Yếu | Yếu | ⭐⭐⭐ Tốt nhất | OK | OK |
| **Debug visual?** | ✅ Tốt | ✅ Tốt | Có | Khó | ⭐⭐⭐ Tốt nhất | Không | ✅ |
| **Phù hợp ngôn ngữ** | Mọi ngôn ngữ | Mọi ngôn ngữ | Mọi ngôn ngữ | Mọi ngôn ngữ | Java/Python/JS specific | Mọi text | Swift only |
| **Cộng đồng VN** | ⭐ Lớn nhất | Đang lên | Nhỏ | Nhỏ | Có | Nhỏ | iOS-only |

> 💡 Mọi con số trên là **chỉ định trung bình** — máy/setup khác nhau cho con số khác. Đừng cãi nhau vì 100MB RAM.

---

## 4️⃣ Khuyến nghị theo profile

### 🟢 Case 1: Beginner zero-base (chưa từng cài editor)

→ **VS Code** (Option default cho ~80% beginner)

**Lý do**:
- Phổ biến nhất → mọi tutorial Việt Nam dùng VS Code → dễ follow
- Free + Microsoft maintain → không lo dừng support
- Đa ngôn ngữ → đổi nhánh (Backend → Frontend → Data) không phải đổi editor
- Curve học thấp — vừa code vừa quen extension
- Có Copilot khi sẵn sàng trả $10/tháng

→ Cài chi tiết: [vs-code.md](./vs-code.md) ✅

### 🟡 Case 2: Đã code 6 tháng, muốn AI mạnh hơn Copilot

→ **Cursor** (paid $20/tháng nhưng đáng)

**Lý do**:
- Hiểu **toàn codebase** chứ không chỉ file đang mở (RAG built-in)
- Tab autocomplete nhanh hơn Copilot ~2x
- Chat side panel với Claude 4.x / GPT
- Composer mode — viết feature mới từ description
- Switch từ VS Code cực dễ — import settings 1 click

→ Cài chi tiết: [cursor.md](./cursor.md) (chưa có)

### 🟠 Case 3: Java/Kotlin dev (project enterprise)

→ **IntelliJ IDEA Ultimate** (paid $169/năm)

**Lý do**:
- Refactor Java/Kotlin mạnh nhất thị trường (đổi tên class → cập nhật 200 file tự động không lỗi)
- Debugger Java tốt nhất
- DB tool tích hợp (không cần DBeaver riêng)
- Spring Boot support tốt nhất
- Bù lại $169 trong 1 tháng năng suất

→ Cài chi tiết: [intellij.md](./intellij.md) (chưa có)

### 🟣 Case 4: Power user, làm việc qua SSH/server

→ **Neovim**

**Lý do**:
- Chạy trong terminal — SSH vào server là dùng được luôn
- Cực nhẹ, không cần GUI
- Keyboard-driven 100% — năng suất sau khi quen
- Config Lua flex — distro như LazyVim/AstroNvim có sẵn

⚠️ **Cảnh báo**: Curve học **rất khó** (1-3 tháng để hiệu suất ngang VS Code). Đừng chọn Neovim làm editor đầu tiên.

→ Cài chi tiết: [neovim.md](./neovim.md) (chưa có)

### 🔵 Case 5: Mac M-series, thích minimal + nhanh

→ **Zed**

**Lý do**:
- Viết bằng Rust + dùng GPU → nhanh hơn VS Code 3-5x cảm nhận được
- UI minimal, dễ chịu mắt
- Collab realtime built-in (Google Docs cho code)
- AI sắp có

**Nhược**: Ecosystem extension nhỏ, chưa có Windows.

### ⚪ Case 6: iOS / macOS dev

→ **Xcode** (bắt buộc)

Không có lựa chọn — submit App Store yêu cầu Xcode. Cài chỉ làm bạn miss-out gì cả vì Apple toolchain lock-in.

### 🟤 Case 7: Cần edit file 10GB log

→ **Sublime Text**

Không IDE nào mở file 10GB ngon như Sublime. $99 once = sản phẩm bạn dùng cả đời.

---

## 5️⃣ Câu hỏi beginner hay hỏi

### "Tôi nên cài 1 hay nhiều editor cùng lúc?"

Cả hai đều OK. Phổ biến:
- **1 editor chính** (vd VS Code) cho 90% công việc
- **+ Vim/nano trong terminal** cho edit nhanh file SSH server
- **+ Neovim** nếu đang học modal editing

→ Đừng để có 5 editor mở 1 lúc — phân tâm.

### "Cursor đắt — có đáng?"

Tính nhanh:
- Cursor $20/tháng × 12 = **$240/năm**
- Lương dev junior VN ~25M/tháng → 1 ngày ~830k VND → khoảng **$33/ngày**
- → Cursor = **7 ngày lương** mỗi năm

Nếu Cursor tiết kiệm bạn **8 giờ/tháng** (rất khả thi với AI tốt), đáng. Beginner có thể tạm dùng free tier 2 tuần thử, không vội trả.

### "Nên bắt đầu với JetBrains hay VS Code?"

Beginner → **VS Code**. Lý do:
1. Tutorial VN nhiều hơn cho VS Code
2. JetBrains ăn RAM nhiều — máy yếu khổ
3. JetBrains mỗi IDE riêng (PyCharm khác WebStorm) — đổi nhánh phải đổi IDE
4. VS Code đủ tốt cho 80% nhu cầu

Sau 1-2 năm, nếu vào team Java → đổi sang IntelliJ. Đủ thời gian học cả 2.

### "Vim/Neovim — học có đáng?"

Modal editing là **kỹ năng cả đời** — học 1 lần dùng mãi. Nhưng curve khó. Khuyến nghị:
1. **Năm 1**: VS Code + `vscodevim` extension — học vim shortcut từng chút
2. **Năm 2+**: Khi quen → thử Neovim riêng

Đừng học Neovim ngay năm 1 — sẽ quit IT trước.

---

## 6️⃣ Đi vào từng tool

> 💡 Mỗi tool guide riêng chỉ **focused vào chính nó** — không so sánh nữa (so sánh đã ở file này).

| Tool | User guide |
|---|---|
| **VS Code** | [📄 vs-code.md](./vs-code.md) ✅ — cài + UI tour + settings + extensions + workflow |
| **Cursor** | [📄 cursor.md](./cursor.md) (chưa có) — AI-native fork VS Code |
| **Neovim** | [📄 neovim.md](./neovim.md) (chưa có) — modal editor terminal |
| **JetBrains** | [📄 jetbrains.md](./jetbrains.md) (chưa có) — IntelliJ/PyCharm/WebStorm/... |
| **Zed** | [📄 zed.md](./zed.md) (chưa có) — Rust + GPU editor |
| **Sublime Text** | [📄 sublime.md](./sublime.md) (chưa có) — lightweight |
| **Xcode** | [📄 xcode.md](./xcode.md) (chưa có) — iOS/macOS only |

---

## 7️⃣ Alternative khác (ít phổ biến nhưng đáng biết)

| Tool | Đặc biệt khi |
|---|---|
| **Fleet** (JetBrains) | JetBrains thử làm "VS Code killer" — distributed, đẹp. Chưa stable. |
| **Lapce** | Rust editor giống Zed nhưng community OSS |
| **Pulsar** (Atom revival) | Tiếp tục Atom sau GitHub kill |
| **Emacs** | Org-mode + extensible cực sâu. Curve cao. Cộng đồng nhỏ ở VN |
| **Eclipse** | IDE Java cổ điển, free. Bị IntelliJ vượt mọi mặt 2018+ |
| **Replit** | Cloud IDE — code trong browser, share dễ. Tốt cho dạy/học |
| **GitHub Codespaces** | VS Code chạy trong cloud, container per project |

---

## 8️⃣ Tích hợp AI — Bảng đối chiếu (2026)

| Editor | AI tích hợp | Free? |
|---|---|---|
| **VS Code** | Copilot (Microsoft/GitHub) | $10/mo |
| **Cursor** | ⭐ Claude + GPT built-in, RAG codebase | $20/mo |
| **Windsurf** (Codeium) | Codeium AI built-in | Free tier + paid |
| **Zed** | Zed AI (Anthropic backed) — sắp ra | TBD |
| **JetBrains** | JetBrains AI Assistant | $100/năm |
| **Neovim** | Avante.nvim / Copilot.lua plugin | Theo plugin |

→ **2026 trend**: AI-native editor (Cursor/Windsurf) dần ăn thị phần VS Code+Copilot. Nhưng cốt lõi vẫn ổn — VS Code mainstream cho 80% người.

---

## 9️⃣ Cấu hình khuyến nghị chung (mọi editor)

Không phụ thuộc editor nào — đây là setting "đáng làm với mọi tool":

### Font

- **Khuyến nghị**: Fira Code / JetBrains Mono / Cascadia Code (có ligature)
- Size: 14-16pt (laptop), 13-14pt (desktop 4K)
- Line height: 1.5-1.7

### Theme

- Dark mode (mặc định mọi editor 2026) — đỡ mỏi mắt 8h/ngày
- Nếu mắt khoẻ + thích sáng: One Light, GitHub Light

### Keybinding

- Học **3 phím tắt/tuần**, đừng cố nhớ 50 cùng lúc
- Print cheatsheet, dán bàn

### Settings sync

- Bật ngay — đổi máy không phải setup lại
- VS Code/Cursor: dùng GitHub account để sync
- JetBrains: dùng JetBrains Account

---

## 🔗 Liên kết

- 🧭 [Zero to Coder Stage 1](../../00_Roadmaps/career/zero-to-coder_career-roadmap.md#stage-1--tools-tối-thiểu-2-3-tuần) — beginner gọi editor đầu tiên
- 📚 [Git lesson 00 — what is Git](../../01_Foundations/version-control/git/lessons/01_basic/00_what-is-git.md) — editor + git tích hợp
- 🛠️ [Terminal emulators category](../terminal-emulators/) (chưa có) — companion category, dùng cùng editor

### Tài nguyên ngoài

- [Stack Overflow Developer Survey](https://survey.stackoverflow.co/) — số liệu thị phần editor mỗi năm
- [Awesome VS Code](https://github.com/viatsko/awesome-vscode) — extension + theme curated
- [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/) — quản lý nhiều IDE 1 chỗ
- [VimAwesome](https://vimawesome.com/) — Vim/Neovim plugins
- [Awesome Cursor](https://github.com/topics/cursor-ai) — Cursor rules + prompts

---

## 📌 Changelog

- **v1.0.0 (20/05/2026)** — Bản đầu tiên. Tool category đầu tiên hoàn chỉnh trong kho — demo 2-level pattern (category + individual). So sánh 7 editor chính + 7 alternative. 7 case khuyến nghị theo profile. Bảng AI integration 2026.
