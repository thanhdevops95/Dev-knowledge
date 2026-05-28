# 🛠️ GitHub Desktop — GUI client cho người ghét CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 24/05/2026\
> **Loại:** Tool individual — focused vào GitHub Desktop\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) (chọn GitHub), [github.md](./github.md) (GitHub web)

> 🎯 *GUI client chính thức của GitHub — clone/commit/push/PR qua giao diện đồ hoạ, không cần gõ `git` trên terminal. Phù hợp beginner sợ CLI hoặc designer/non-dev cần đóng góp code.*

---

## Tình huống — Đồng nghiệp sợ terminal

Tiếp story. 1 đồng nghiệp junior FE đã follow git lessons + setup GitHub account. Nhưng terminal đen kịt với 50 lệnh khiến họ stress. Mỗi lần cần commit, phải:

```bash
git status      # gì thay đổi?
git diff        # diff trông sao?
git add file1.js file2.js
git commit -m "..."
git push
```

→ 5 dòng cho 1 commit. Họ prefer **GUI** — click, drag, type message → done.

Bạn bảo: *"Cài GitHub Desktop. Cùng repo, cùng PR — chỉ là giao diện thân thiện hơn."*

Bài này dạy bạn dùng **GitHub Desktop** — GUI chính thức của GitHub, free, đẹp, có mọi tính năng cốt lõi.

---

## 1️⃣ Vậy GitHub Desktop là gì?

**GitHub Desktop** là **GUI client** chính thức của GitHub, free, có cho Mac + Windows + Linux (beta). Dùng để clone/commit/push/PR qua giao diện đồ hoạ, **không cần gõ `git` trên terminal**.

🪞 **Ẩn dụ**: GitHub Desktop giống **Photos app** trên Mac/Win — cùng dữ liệu, cùng iCloud, nhưng UI dễ dùng hơn so với gõ `imageio.imread()` trong Python. Cùng repo Git, chỉ là cách tương tác khác.

**Số liệu nhanh**:
- Free, open source ([github/desktop](https://github.com/desktop/desktop))
- Owner: Microsoft (GitHub team)
- ~5-10% dev GitHub dùng (CLI vẫn dominant)
- Update mỗi 2-4 tuần

### Khi nào nên dùng GitHub Desktop?

| ✅ Dùng khi | ❌ KHÔNG dùng khi |
|---|---|
| Beginner sợ CLI | Đã quen `git` CLI — không cần switch |
| Designer / Non-dev đóng góp code (vd sửa README, image) | Cần git advanced (rebase interactive, cherry-pick complex) |
| Visualize diff + commit history trực quan | CI/CD automation (cần CLI/script) |
| Quick commits trên Mac/Windows | Server SSH không GUI |
| Muốn drag-drop file thay gõ `git add` | Workflow team yêu cầu signed commits + advanced rebase |

> 💡 **Khuyến nghị**: dùng GitHub Desktop 1-3 tháng đầu để quen Git workflow. Khi tự tin → chuyển dần sang CLI cho tốc độ + power.

---

## 2️⃣ Cài GitHub Desktop

### macOS

```bash
brew install --cask github
```

Hoặc tải từ [desktop.github.com](https://desktop.github.com).

### Windows

```powershell
winget install GitHub.GitHubDesktop
```

Hoặc tải `.exe` từ [desktop.github.com](https://desktop.github.com).

### Linux (community fork — KHÔNG official)

Official chưa support Linux. Cộng đồng có fork:
- [shiftkey/desktop](https://github.com/shiftkey/desktop) — `.deb` / `.rpm` / Flatpak

```bash
# Ubuntu / Debian
wget https://github.com/shiftkey/desktop/releases/download/release-3.4.3-linux1/GitHubDesktop-linux-amd64-3.4.3-linux1.deb
sudo dpkg -i GitHubDesktop-linux-amd64-3.4.3-linux1.deb
```

### Sign in

1. Mở GitHub Desktop
2. **File → Options → Accounts** (Mac: GitHub Desktop → Settings → Accounts)
3. Click **Sign in** trong GitHub.com section
4. Browser tự mở → authorize
5. Quay lại app → đã sign in

> 💡 **2FA**: nếu bật 2FA (recommended, xem [github.md §2.2](./github.md)), browser sẽ hỏi code 2FA lúc sign in.

---

## 3️⃣ UI Tour — Hiểu 5 phần chính

```
GitHub Desktop layout:
┌──────────────────────────────────────────────────────────────────┐
│ ① Repo switcher │ ② Branch switcher │ ③ Fetch/Push button     │
├─────────────────┬────────────────────────────────────────────────┤
│ ④ Changes /     │                                                │
│   History       │  ⑤ Diff view (changes/file content)            │
│   panel         │                                                │
│                 │                                                │
│   - File 1 ☑    │  + new line                                    │
│   - File 2 ☑    │  - old line                                    │
│   - File 3 ☐    │                                                │
│                 │                                                │
├─────────────────┤                                                │
│ Commit message  │                                                │
│ Summary:        │                                                │
│ Description:    │                                                │
│ [Commit button] │                                                │
└─────────────────┴────────────────────────────────────────────────┘
```

| Phần | Chức năng |
|---|---|
| ① **Repo switcher** | Chọn repo (top-left). Add local folder hoặc clone từ GitHub |
| ② **Branch switcher** | Chuyển branch, tạo branch mới, xoá branch |
| ③ **Fetch / Push / Pull** | Sync với remote (top-right). Hiển thị "Push 2 commits" khi có local commits chưa push |
| ④ **Changes / History panel** | Tab **Changes**: file đã sửa, tick để stage. Tab **History**: list commits trên branch hiện tại |
| ⑤ **Diff view** | Hiển thị diff file đang chọn — màu xanh `+` line thêm, đỏ `-` line xoá |

### Top menu — actions quan trọng

| Menu | Items |
|---|---|
| **File** | Add Local Repository, Clone Repository, Options/Settings |
| **Edit** | Undo, Cut/Copy/Paste, Select All |
| **View** | Show Changes / History / Repository |
| **Repository** | Push, Pull, Fetch, Open in Terminal, Open in Editor |
| **Branch** | New Branch, Compare to Branch, Merge, Rebase |
| **Help** | Documentation, Report Issue |

---

## 4️⃣ Workflow basic — Clone → Commit → Push

### Clone repo từ GitHub

3 cách:

**Cách 1 — Từ GitHub Desktop**:
1. File → **Clone Repository...** (`Cmd/Ctrl + Shift + O`)
2. Tab **GitHub.com** → list repo bạn có access
3. Chọn repo + path local
4. Click **Clone**

**Cách 2 — Từ GitHub web**:
1. Trên trang repo, click **`<> Code`** dropdown
2. Click **"Open with GitHub Desktop"**
3. Browser hỏi "Open GitHub Desktop?" → Open
4. App mở + tự clone

**Cách 3 — Từ URL**:
1. Copy URL repo (vd `https://github.com/user/repo`)
2. File → Clone Repository → tab URL → paste
3. Clone

### Add local repo (đã có sẵn)

1. File → **Add Local Repository...**
2. Browse tới folder local (đã `git init` hoặc clone từ trước)
3. Add

### Sửa code + commit

1. Sửa file trong editor (VS Code, ...). GitHub Desktop tự detect changes.
2. Quay lại app → tab **Changes** hiển thị file đã sửa
3. **Tick file** muốn stage (vd `login.js`, bỏ qua `notes.txt`)
4. Xem diff ở panel bên phải
5. Viết **Summary** (commit message) — ngắn gọn 50 ký tự
6. (Optional) **Description** — chi tiết nếu cần
7. Click **Commit to main** (hoặc branch hiện tại)

### Push lên remote

- Sau commit, nút **Fetch** đổi thành **Push origin (1)** ở top-right
- Click → sync lên GitHub

> 💡 **Auto-fetch**: GitHub Desktop tự fetch remote mỗi 10 phút. Nếu remote có commit mới, nút sẽ thành **Pull origin (N)**.

---

## 5️⃣ Pull Request workflow

### Tạo PR

1. Tạo branch mới: **Branch → New Branch** (hoặc `Cmd/Ctrl + Shift + N`)
   - Name: `feature/add-search`
   - Base: `main`
2. Sửa code + commit trên branch này (như §4)
3. **Push branch** (nút top-right hiện "Publish branch" nếu lần đầu)
4. Sau push, banner xuất hiện: **"Create Pull Request"** → click
5. Browser mở trang PR trên GitHub → điền title + description → Create

### Review PR (của bạn)

GitHub Desktop hiển thị:
- **Pull Requests** tab (top-left, gần branch switcher)
- List PR mở trong repo

Click 1 PR → **Checkout** branch của PR đó local → review code trong editor → comment trên GitHub web → approve.

> 💡 Một số action vẫn cần GitHub web (comment inline, approve formal). GitHub Desktop là helper, không replace web UI cho code review.

### Merge PR

1. Trên GitHub web: click **Merge pull request** (như [github.md §6](./github.md))
2. Quay lại Desktop → **Fetch** → branch `main` có commit mới
3. Switch branch về `main` → **Pull origin**
4. Delete branch local: **Branch → Delete... → confirm**

---

## 6️⃣ Branching qua GUI

### Tạo branch

- **Branch → New Branch** (`Cmd/Ctrl + Shift + N`)
- Hoặc click branch switcher → "**New Branch**"

### Switch branch

- Click branch switcher → chọn branch
- Nếu có **uncommitted changes**, app hỏi:
  - **Leave my changes on `<current>`** — tự stash changes
  - **Bring my changes to `<new>`** — chuyển changes sang branch mới

### Merge branch (manual)

1. Switch sang branch ĐÍCH (vd `main`)
2. **Branch → Merge into Current Branch...**
3. Chọn branch SOURCE (vd `feature/x`)
4. **Merge `feature/x` into `main`**
5. Nếu conflict → app hiện file conflict + nút "Open in editor" để fix

### Compare branches

- **Branch → Compare to Branch** → chọn branch khác
- Hiển thị commits khác biệt giữa 2 branch — useful trước khi merge

---

## 7️⃣ GitHub Desktop vs VS Code Source Control

**Tại sao mention?** Vì VS Code cũng có **Source Control panel built-in** — cũng GUI cho git, miễn phí.

| Tiêu chí | GitHub Desktop | VS Code Source Control |
|---|---|---|
| **Cài kèm** | App riêng | Built-in VS Code |
| **Phù hợp** | Beginner, designer, non-dev | Dev đã dùng VS Code |
| **GitHub integration** | ⭐⭐⭐ Tích hợp sâu (PR list, fork, ...) | ⭐ Cơ bản (qua extension GitHub Pull Requests) |
| **Diff UI** | ⭐ Clean, focused | ⭐⭐ Đẹp + side-by-side |
| **Merge conflict** | ⭐ Open editor để fix | ⭐⭐⭐ Built-in 3-way merge editor cực mạnh |
| **Multi-repo** | Switch 1 lần 1 repo | Workspace mở nhiều repo |
| **Footprint** | App ~200 MB riêng | Đã có VS Code, không thêm |

→ **Khuyến nghị**:
- **Đồng nghiệp FE dev**: dùng GitHub Desktop song song VS Code. Desktop cho overview repo + PR list. VS Code Source Control cho daily commit.
- **bạn (BE dev quen CLI)**: dùng `git` CLI + VS Code Source Control khi cần visual diff. Không cần GitHub Desktop.

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Commit qua Desktop nhưng user.email khác Git CLI

GitHub Desktop có settings email riêng (File → Options → Git). Nếu sửa email trong Desktop khác email trong `~/.gitconfig`, commit có thể không match GitHub account → không hiện contribution graph.

**Cách tránh**: Cùng email ở 2 nơi. Settings → Git → "Use my GitHub account name and email address".

### ❌ Pitfall: Force push qua Desktop

GitHub Desktop **có** option Force Push (hold Shift khi click Push button trong vài tình huống). Cảnh báo: force push lên branch shared = mất commits đồng nghiệp.

**Cách tránh**: Đọc warning dialog trước khi force push. Setup branch protection trên `main` để chặn.

### ❌ Pitfall: Không support advanced git operations

GitHub Desktop **KHÔNG hỗ trợ**:
- Interactive rebase (`git rebase -i`)
- Cherry-pick (basic có nhưng limited)
- Submodules (lazy support)
- Worktrees
- Sparse checkout

→ Cần các operation này → mở terminal: **Repository → Open in Terminal**.

### ✅ Best practice: Dùng Desktop để học, sau switch CLI

Roadmap khuyến nghị:
1. **Tuần 1-4** beginner: dùng Desktop để hiểu git workflow visual
2. **Tuần 5+**: pair Desktop + VS Code Source Control. Hiểu lệnh git ngầm chạy.
3. **3-6 tháng**: chuyển dần sang CLI cho speed + automation
4. **1 năm+**: CLI chính, Desktop chỉ khi cần GUI overview (vd review PR list)

---

## 🧠 Self-check

**Q1.** Lần đầu commit qua GitHub Desktop. App hỏi "Sign in to GitHub" → bạn chưa setup gì → sign in fail. Vì sao?

<details>
<summary>💡 Đáp án</summary>

**Có thể vì**:
1. **Chưa có account GitHub** — đăng ký trước ở github.com
2. **2FA chưa setup auth method** — phải có authenticator app sẵn sàng nhập code
3. **Browser block popup** — GitHub Desktop mở browser để OAuth, browser block redirect

**Cách fix**:
- Tạo account GitHub trước (xem [github.md §2.1](./github.md))
- Cài 2FA + có authenticator app trên phone
- Allow popup cho `desktop.github.com` trong browser
- Hoặc dùng PAT token thay OAuth: File → Options → Git → manually set credentials

</details>

**Q2.** Bạn dùng GitHub Desktop để commit nhưng GitHub contribution graph không ghi nhận?

<details>
<summary>💡 Đáp án</summary>

**99% là do email không match**. Contribution graph chỉ ghi commit có email trùng với 1 trong các email verify trên GitHub account.

**Check**:
```bash
git config user.email   # email Git CLI dùng
```

Hoặc trong GitHub Desktop: **Options → Git → email**.

**Fix**:
- Set Desktop dùng email account: Options → Git → "Use my GitHub account name and email address"
- Hoặc set thủ công cùng email đã verify trên GitHub (Settings → Emails)

→ Sau khi fix, commit MỚI sẽ hiện contribution. Commit cũ vẫn không hiện trừ khi rebase với email mới.

</details>

**Q3.** Cần làm `git rebase -i HEAD~3` để squash 3 commit. GitHub Desktop có làm được không?

<details>
<summary>💡 Đáp án</summary>

**Một phần**. GitHub Desktop có **Squash Commits** (Branch → Squash Commits) chọn nhiều commit liền nhau để gộp. Đủ cho 80% use case.

Nhưng **interactive rebase đầy đủ** (reorder, edit message từng commit, drop) — KHÔNG có trong UI. Cần mở terminal:

**Repository → Open in Terminal** → gõ `git rebase -i HEAD~3` như thường.

→ Đây là **pitfall §7.3**: Desktop là 80/20 — cover phần lớn workflow, advanced cần CLI.

</details>

---

## ⚡ Cheatsheet

### Keyboard shortcuts (Mac / Win)

| Action | Mac | Win |
|---|---|---|
| Clone Repository | `Cmd+Shift+O` | `Ctrl+Shift+O` |
| Add Local Repository | `Cmd+O` | `Ctrl+O` |
| New Branch | `Cmd+Shift+N` | `Ctrl+Shift+N` |
| Switch Branch | `Cmd+B` | `Ctrl+B` |
| Push | `Cmd+P` | `Ctrl+P` |
| Pull | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Fetch | `Cmd+Shift+T` | `Ctrl+Shift+T` |
| Open in External Editor | `Cmd+Shift+A` | `Ctrl+Shift+A` |
| Open in Terminal | `` Cmd+` `` | `` Ctrl+` `` |
| View Repository | `Cmd+1` | `Ctrl+1` |
| View Changes | `Cmd+2` | `Ctrl+2` |
| View History | `Cmd+3` | `Ctrl+3` |

### Common workflows

| Task | Cách trong Desktop |
|---|---|
| Clone repo | File → Clone, chọn từ list GitHub.com |
| Commit changes | Changes tab → tick file → write summary → Commit |
| Push to GitHub | Top-right "Push origin" button |
| Tạo PR | Push branch → click "Create Pull Request" banner |
| Switch branch | Branch switcher (top) → chọn |
| Merge branch | Switch sang ĐÍCH → Branch → Merge into Current |
| Revert commit | History → right-click commit → Revert |
| Stash changes | Switch branch khi có changes → "Leave my changes on..." |
| Open external editor | Repository → Open in External Editor |
| Open in terminal | Repository → Open in Terminal |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| GUI client | GUI client | Phần mềm có giao diện đồ hoạ cho git |
| Diff | Khác biệt | Hiển thị dòng thêm/xoá khi sửa file |
| Summary | Tóm tắt | Dòng đầu commit message (50 ký tự) |
| Description | Mô tả | Phần dài commit message sau summary |
| Publish branch | Đẩy nhánh | Push branch local lên GitHub lần đầu |
| Stash | Cất tạm | Lưu thay đổi tạm khi switch branch |
| Fetch | Tải | Sync remote info, không merge |
| Pull | Kéo | Fetch + merge |
| Push | Đẩy | Upload commit lên remote |
| Conflict | Xung đột | Khi 2 branch sửa cùng dòng |
| Squash | Nén | Gộp nhiều commit thành 1 |
| Force push | Đẩy ép | Ghi đè history remote (DANGER) |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh git hosting
- 🛠️ [github.md](./github.md) — GitHub web user guide (account, PR, Actions, ...)
- 🛠️ [VS Code Source Control](../ide/vs-code.md#git-tích-hợp-không-cần-cli) — alternative GUI trong VS Code
- 🎓 [Git basic 5 lessons](../../01_foundations/version-control/git/lessons/01_basic/) — bạn story arc concept
- 🧭 [Zero to Coder Stage 1](../../00_roadmaps/career/zero-to-coder_career-roadmap.md) — beginner cài git tools

### Tài nguyên ngoài

- [GitHub Desktop Docs](https://docs.github.com/en/desktop) — chính thức, đầy đủ
- [GitHub Desktop GitHub repo](https://github.com/desktop/desktop) — source code + issues
- [shiftkey/desktop (Linux fork)](https://github.com/shiftkey/desktop) — Linux community build
- [GitKraken](https://www.gitkraken.com/) — alternative GUI client (paid, mạnh hơn)
- [Sourcetree](https://www.sourcetreeapp.com/) — Atlassian GUI (free, hỗ trợ cả GitHub + Bitbucket)
- [Fork](https://git-fork.com/) — fast GUI client (paid)

---

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4 §3.5. Bulk replace fictional character "bạn" → "bạn"/"Bạn"/"Mình" theo context (generic role thay tên riêng tự bịa). Nội dung kỹ thuật giữ nguyên.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool individual #2 trong git-clients/. Cover: tình huống đồng nghiệp sợ CLI → §1 GitHub Desktop là gì + khi nào dùng → §2 Install 3 OS → §3 UI tour 5 phần + diagram → §4 Workflow clone/commit/push → §5 PR workflow → §6 Branching qua GUI → §7 So sánh với VS Code Source Control. 4 pitfall + 3 self-check + cheatsheet shortcut.
