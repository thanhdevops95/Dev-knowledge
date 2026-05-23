# 🎓 Environment Variables — `$PATH`, `.env`, secrets, scope

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [01_what-is-shell.md](./01_what-is-shell.md), [03_process-and-pid.md](./03_process-and-pid.md)

> 🎯 *Bài CONCEPT — hiểu **environment variable là gì**, **$PATH** đặc biệt thế nào, **scope** (process/session/system), **`.env` file** pattern, **secrets**. Sau bài này bạn hiểu vì sao `command not found` xảy ra, vì sao `.env` không được commit, và cách config app qua env var.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **env var** là gì + được lưu ở đâu trong process
- [ ] Đọc + ghi env var qua `echo $VAR`, `export VAR=value`, `unset VAR`
- [ ] Hiểu **$PATH** — vì sao gõ `python` chạy được mà không cần đường dẫn đầy đủ
- [ ] Phân biệt 3 **scope**: process-level / session / system-wide (persistent)
- [ ] Hiểu **inheritance** — child process kế thừa env từ parent
- [ ] Hiểu **`.env` file** pattern + vì sao KHÔNG commit
- [ ] Phân biệt env var thường vs **secrets**

---

## Tình huống — `command not found` và `.env` đầy mọi project

Bạn vừa cài Python xong. Mở terminal mới, gõ:

```bash
python --version
# zsh: command not found: python ❌
```

Lạ. Cài rồi mà sao không tìm thấy? Search Google: *"add Python to PATH"*. Tutorial bảo:

```bash
export PATH="/usr/local/bin:$PATH"
```

Gõ vào → giờ `python` chạy. Nhưng mở terminal mới → lại không chạy. Vì sao?

Cùng lúc, mọi project bạn clone (FastAPI, Next.js, Django...) đều có file `.env`:
```
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
OPENAI_API_KEY=sk-proj-abc123xyz...
SECRET_KEY=...
```

`.gitignore` luôn có dòng `.env` đầu tiên. Vì sao? Sao không hardcode trong code?

→ Cả 2 hiện tượng đều xoay quanh **environment variables** — chìa khoá config + secrets trong dev. Bài này giải đáp.

---

## 1️⃣ Vậy Environment Variable là gì?

**Trả lời tình huống**: Env var là **biến lưu trong memory của process**, dùng để **config** behavior mà không hardcode trong code. Mỗi process có **bản copy** env riêng. Set lần này không tự động "nhớ" cho lần sau (trừ khi lưu vào file config).

🪞 **Ẩn dụ**: env var giống **bảng ghi chú trên bàn làm việc** của mỗi process. Process cha tạo bàn → cấp bản sao cho con. Con sửa note → bàn cha KHÔNG đổi. Đóng terminal = đóng bàn = note mất.

### Cú pháp cơ bản

```bash
# Đọc 1 env var
echo $HOME
# /Users/rom

echo $USER
# rom

# Tạo / set env var (chỉ trong session hiện tại)
export MY_VAR="hello"
echo $MY_VAR
# hello

# Xoá env var
unset MY_VAR

# List MỌI env var
env

# List env var khớp pattern
env | grep API
```

> 💡 **Quy ước Unix**: env var **TÊN VIẾT HOA** (`HOME`, `PATH`), giữa các từ dùng `_` (`API_KEY`, `DATABASE_URL`). Phân biệt với biến shell thường (lowercase: `my_var`).

### Env var vs Shell variable — phân biệt

```bash
local_var="hello"           # shell variable — chỉ shell hiện tại thấy
export EXPORTED_VAR="hi"     # env var — child process kế thừa
```

| | Shell variable | Environment variable |
|---|---|---|
| Set bằng | `var=value` | `export VAR=value` |
| Child process thấy? | ❌ Không | ✅ Có (inheritance) |
| Dùng khi | Logic shell tạm thời | Config truyền xuống program |
| Đọc bằng | `echo $var` | `echo $VAR` (cú pháp same) |

---

## 2️⃣ `$PATH` — Biến đặc biệt nhất

**`$PATH`** là env var **quan trọng nhất**. Nó là **list các folder** shell sẽ tìm khi bạn gõ 1 lệnh.

```bash
echo $PATH
# /opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Dấu `:` ngăn các folder. Khi bạn gõ `python`:

```mermaid
graph LR
    A[Bạn gõ 'python'] --> B{Shell tìm trong $PATH<br/>theo thứ tự}
    B --> C[/opt/homebrew/bin/python?]
    C -->|Không| D[/usr/local/bin/python?]
    D -->|Có ✓| E[Chạy /usr/local/bin/python]
    D -->|Không| F[/usr/bin/python?]
    F -->|Có| G[Chạy /usr/bin/python]
    F -->|Không| H[❌ command not found]
```

→ Shell tìm folder **đầu tiên có file `python`** → chạy. Không có ở folder nào → báo `command not found`.

### Vì sao tutorial luôn bảo "add to PATH"?

Khi cài 1 chương trình mới (vd Python, Node, Go), binary đặt ở folder X (vd `/opt/homebrew/bin/python3.11`). Nếu folder X **không trong `$PATH`** → gõ tên chương trình → `command not found`.

**Giải pháp**:
```bash
export PATH="/opt/homebrew/bin:$PATH"
```

Đọc: "Thêm `/opt/homebrew/bin` vào ĐẦU PATH cũ". Folder mới được tìm TRƯỚC folder cũ — quan trọng khi có nhiều version cùng tên (vd Python 2 ở `/usr/bin/python`, Python 3.11 ở `/opt/homebrew/bin/python` — thêm trước để dùng 3.11).

### Check binary đang dùng — `which`

```bash
which python
# /opt/homebrew/bin/python      ← binary thật sự shell sẽ chạy

which -a python
# /opt/homebrew/bin/python      ← tất cả binary "python" trong PATH
# /usr/bin/python               ← theo thứ tự
```

→ Beginner đôi khi cài Python xong vẫn "không chạy" vì shell dùng Python cũ (đầu PATH). `which python` cho biết đang dùng cái nào.

---

## 3️⃣ Scope của env var — 3 mức persistence

| Scope | Phạm vi | Cách set | Persist sau khi đóng? |
|---|---|---|---|
| **Process-level** | Chỉ process đó | `VAR=value <command>` | ❌ Mất sau command |
| **Session (shell hiện tại)** | Shell + child | `export VAR=value` | ❌ Mất khi đóng terminal |
| **System-wide / Persistent** | Mọi terminal future | Ghi vào `~/.zshrc`, `~/.bashrc`, `/etc/environment` | ✅ Còn mãi |

### 1. Process-level — 1 command duy nhất

```bash
DEBUG=1 python app.py
# DEBUG=1 CHỈ tồn tại trong process "python app.py"
# Sau command, DEBUG biến mất khỏi shell
```

Use case: chạy 1-shot với config khác mà không muốn thay đổi shell.

### 2. Session — shell hiện tại + child

```bash
export DEBUG=1
python app.py     # thấy DEBUG=1
python other.py   # vẫn thấy DEBUG=1

# Đóng terminal → DEBUG mất
```

### 3. Persistent — ghi vào file config shell

Trong `~/.zshrc` (zsh) hoặc `~/.bashrc` (bash):

```bash
# ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
export EDITOR="vim"
export NODE_ENV="development"
```

Sau khi sửa → `source ~/.zshrc` hoặc đóng-mở terminal → giờ MỌI terminal mới có biến này.

### System-wide (ít dùng)

| File | Áp dụng cho |
|---|---|
| `~/.zshrc`, `~/.bashrc` | User hiện tại, mọi terminal |
| `~/.profile` | Mọi shell user hiện tại |
| `/etc/environment` | Mọi user trên máy (Linux) |
| `/etc/profile`, `/etc/zshenv` | Mọi user, system-wide |

> ⚠️ KHÔNG sửa `/etc/...` trừ khi biết rõ. Hỏng = mọi user broken.

---

## 4️⃣ Inheritance — Child process kế thừa env từ parent

```mermaid
graph TD
    A[zsh: PATH=A,B,C<br/>HOME=/Users/rom<br/>API_KEY=abc] -->|fork + exec| B[python app.py<br/>= COPY env từ zsh<br/>PATH=A,B,C<br/>HOME=/Users/rom<br/>API_KEY=abc]
    B -->|os.environ['NEW_VAR']='hi'| C[NEW_VAR chỉ trong python<br/>zsh KHÔNG thấy]
```

**Quy tắc**:
1. Child process **nhận bản COPY** env từ parent lúc khởi tạo
2. Child sửa env → **chỉ child thấy** (không ảnh hưởng parent)
3. Parent sửa env sau đó → child cũng KHÔNG thấy (đã copy xong)

🪞 **Ẩn dụ**: parent cho con **bản photocopy** sổ ghi chú. Con viết thêm trong bản photocopy → bản gốc parent không đổi. Parent viết thêm trong bản gốc sau đó → con đã đi rồi, không biết.

### Hệ quả thực tế

```bash
# Terminal 1
export API_KEY="secret123"
python app.py    # app thấy API_KEY ✓

# Terminal 2 (mở mới — KHÁC shell process)
python app.py    # app KHÔNG thấy API_KEY ❌ — terminal 2 chưa export
```

→ Mỗi terminal là 1 shell process riêng. Set env ở terminal 1 không tự động truyền sang terminal 2.

---

## 5️⃣ File `.env` — Pattern phổ biến trong dev

App production (đặc biệt Node.js, Python web) thường **load env từ file `.env`** thay vì hardcode hoặc gõ `export` mỗi lần.

### Cấu trúc `.env`

```bash
# .env (root project)
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=sk-proj-abc123xyz...
JWT_SECRET=super-long-random-string
DEBUG=true
PORT=5000
```

Quy ước:
- Tên: `KEY=value`, KHÔNG space xung quanh `=`
- Comment: `#` đầu dòng
- KHÔNG cần quote `"..."` (trừ khi value có space)
- Value cùng dòng (không multi-line trừ vài tool support)

### App đọc `.env` qua library

| Ngôn ngữ | Library |
|---|---|
| Python | `python-dotenv` (`from dotenv import load_dotenv; load_dotenv()`) |
| Node.js | `dotenv` (`require('dotenv').config()`) |
| Go | `godotenv` |
| Rust | `dotenvy` |

Sau khi load, app dùng `os.getenv('DATABASE_URL')` (Python) hoặc `process.env.DATABASE_URL` (Node) như env thường.

### Vì sao có pattern này?

| Lý do | Giải thích |
|---|---|
| **Tách config khỏi code** | Code commit lên GitHub, config (`.env`) giữ local — khác máy/môi trường khác config |
| **Secrets không leak** | API key, DB password không vào git history |
| **Dev/Staging/Prod** | Mỗi môi trường có `.env` riêng, code KHÔNG đổi |
| **Quick override** | Sửa `.env` → restart app → áp dụng. Không cần rebuild code |

### `.env.example` — File mẫu commit lên git

```bash
# .env.example (commit OK — chỉ có KEY, không value)
DATABASE_URL=
REDIS_URL=
OPENAI_API_KEY=
JWT_SECRET=
DEBUG=
PORT=
```

→ Dev mới clone repo: copy `.env.example` → `.env` → điền value thật. KHÔNG bao giờ commit `.env`.

```
# .gitignore (BẮT BUỘC có)
.env
.env.local
.env.*.local
*.env
```

---

## 6️⃣ Secrets vs Config thường

KHÔNG phải env var nào cũng là secret. Phân biệt:

| | Config thường | Secret |
|---|---|---|
| Ví dụ | `DEBUG=true`, `PORT=5000`, `NODE_ENV=dev` | `API_KEY`, `JWT_SECRET`, DB password |
| Leak có sao? | Không sao | 💀 Tốn $$$, mất data, bị hack |
| Lưu ở đâu | `.env` (commit `.env.example`) | `.env` ở dev. **Production**: vault tool |

### Production: KHÔNG dùng `.env` cho secrets

Trên server thật, secrets phải lưu trong **secret manager**:

| Tool | Cloud |
|---|---|
| **AWS Secrets Manager** / Parameter Store | AWS |
| **GCP Secret Manager** | Google Cloud |
| **Azure Key Vault** | Azure |
| **HashiCorp Vault** | Self-hosted, multi-cloud |
| **Kubernetes Secrets** | K8s cluster |
| **Doppler** / **1Password Secrets Automation** | SaaS |

→ App đọc secret từ tool này lúc start (qua SDK), KHÔNG file `.env` plain text.

> 💡 Tại sao? File `.env` plain text trên server = ai SSH vào đều đọc được. Secret manager + IAM = chỉ app authorized mới đọc, có audit log, rotate keys dễ.

---

## 7️⃣ Env var trong context Docker

Container Docker là 1 process — kế thừa env theo cùng pattern. 3 cách set:

### 1. Trong Dockerfile (build-time)

```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
```

→ Hardcode trong image — không đổi được khi run. Phù hợp config KHÔNG đổi giữa env.

### 2. Khi `docker run` (runtime)

```bash
docker run -e DATABASE_URL=postgres://... -e API_KEY=secret myapp
```

Hoặc dùng file env:
```bash
docker run --env-file .env myapp
```

→ Tách secret khỏi image. **Cách production**.

### 3. Trong `docker-compose.yml`

```yaml
services:
  app:
    image: myapp
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}   # đọc từ .env file ở host
    env_file:
      - .env
```

> 💡 Compose tự đọc `.env` ở root project — KHÔNG cần `--env-file`.

→ Học sâu Docker env handling: [10_DevOps/docker/lessons/01_basic/03_docker-compose.md](../../../../10_DevOps/docker/lessons/01_basic/03_docker-compose.md) §6.

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Set env trong shell mà app vẫn không thấy

```bash
export API_KEY="secret"
# Open IDE (mở từ Spotlight/Dock, KHÔNG từ terminal)
# App trong IDE ❌ không thấy API_KEY
```

- **Lý do**: app mở từ Spotlight/Dock = launchd parent, KHÔNG inherit từ shell. Chỉ child process của shell đó mới thấy.
- **Cách tránh**:
  - Mở app từ terminal: `code .`, `idea .` → IDE = child của shell
  - Ghi env vào file persistent (`~/.zshrc`)
  - Set qua launchd plist (Mac advanced)

### ❌ Pitfall: Commit `.env` lên public repo

```bash
git add .         # ❌ include .env
git push          # ❌ secrets leak lên GitHub
```

- **Hậu quả**: bots scan + dùng API key trong vài phút → bill cloud $$$ → account compromised
- **Cách tránh**:
  - **TRƯỚC `git init`**: tạo `.gitignore` có `.env`
  - Dùng `git status` trước `git add` xem có gì
  - Nếu lỡ commit → KHÔNG đủ chỉ `git rm` — phải **rotate ALL secrets** + dùng `git filter-repo` xoá history
- **Tool ngăn ngừa**: `pre-commit` hook + `gitleaks` scan tự động

### ❌ Pitfall: Sửa `.zshrc` xong gõ env mới ngay

```bash
# Sửa .zshrc thêm export
echo 'export NEW=hi' >> ~/.zshrc

# Gõ ngay
echo $NEW
# (empty) ❌
```

- **Lý do**: `.zshrc` chỉ chạy lúc khởi tạo shell. Sửa file không tự reload.
- **Cách fix**: `source ~/.zshrc` hoặc đóng-mở terminal.

### ❌ Pitfall: Override `$PATH` mất binary cũ

```bash
export PATH="/my/custom/bin"   # ❌ Bỏ qua $PATH cũ
# Giờ shell không tìm thấy ls, cat, git, ...!
```

- **Cách đúng**: luôn nối với PATH cũ:
  ```bash
  export PATH="/my/custom/bin:$PATH"   # ✓ thêm trước
  export PATH="$PATH:/my/custom/bin"   # ✓ thêm sau
  ```

### ✅ Best practice: Secret rotation định kỳ

- API keys, DB passwords → rotate (đổi) **mỗi 90 ngày**
- Audit log: ai access secret, khi nào
- Dev không bao giờ biết secret production (chỉ dev/staging secrets)
- Production secrets QUẢN bằng vault tool, không file `.env`

---

## 🧠 Self-check

**Q1.** Bạn `export API_KEY=abc` ở terminal 1. Mở terminal 2 mới, `echo $API_KEY` ra gì?

<details>
<summary>💡 Đáp án</summary>

**Rỗng** (không có gì).

Mỗi terminal là 1 shell process riêng. Set env ở terminal 1 chỉ affect terminal 1 + child process của nó. Terminal 2 là shell process khác, không thấy.

Để mọi terminal đều có → ghi `export API_KEY=abc` vào `~/.zshrc` (hoặc `.bashrc`) → mỗi terminal khởi tạo sẽ load.

</details>

**Q2.** Gõ `python` báo `command not found`. Bạn cài Python rồi. Vì sao? Cách check?

<details>
<summary>💡 Đáp án</summary>

**Lý do**: folder chứa binary `python` KHÔNG có trong `$PATH`. Shell tìm trong các folder của PATH theo thứ tự, không thấy `python` ở folder nào → báo `command not found`.

**Cách check**:
```bash
echo $PATH                  # xem PATH gồm folder nào
which python                # xem binary đang dùng (nếu có)
ls /opt/homebrew/bin | grep python    # xem binary thực sự ở đâu
```

**Fix**: thêm folder chứa Python vào PATH:
```bash
export PATH="/opt/homebrew/bin:$PATH"
# Ghi vào ~/.zshrc để persist
```

</details>

**Q3.** Vì sao `.env` được `.gitignore` mọi project?

<details>
<summary>💡 Đáp án</summary>

**3 lý do**:
1. **Bảo mật**: `.env` chứa secrets (API keys, DB passwords). Commit lên GitHub public = leak → bot scan + dùng → mất tiền/data
2. **Per-machine config**: mỗi dev có DB local khác nhau, port khác nhau. `.env` của mỗi máy KHÁC nhau.
3. **Per-environment**: dev / staging / production có config khác. KHÔNG share `.env` qua git.

Thay vào đó: commit `.env.example` (chỉ có KEY, không value) làm mẫu. Dev mới clone repo → copy `.env.example` → `.env` → điền value local.

</details>

**Q4.** Phân biệt `VAR=value` và `export VAR=value`.

<details>
<summary>💡 Đáp án</summary>

- **`VAR=value`** (không `export`): **shell variable**. Chỉ shell hiện tại thấy. Child process KHÔNG kế thừa.
- **`export VAR=value`**: **environment variable**. Cả shell hiện tại + mọi child process kế thừa.

Demo:
```bash
local_var="hello"
export EXP_VAR="hi"

# Trong cùng shell:
echo $local_var    # hello ✓
echo $EXP_VAR      # hi ✓

# Tạo subshell:
bash -c 'echo "local=$local_var, exp=$EXP_VAR"'
# local=, exp=hi
# local_var không truyền sang child shell
```

→ App muốn nhận env phải dùng `export`. Variable shell tạm chỉ cần `var=value`.

</details>

---

## ⚡ Cheatsheet

| Lệnh | Mục đích |
|---|---|
| `echo $VAR` | Đọc env var |
| `export VAR=value` | Set env var trong session |
| `unset VAR` | Xoá env var |
| `env` | List tất cả env var |
| `env \| grep PATTERN` | Filter env var |
| `printenv VAR` | Đọc 1 env var (giống `echo $VAR`) |
| `VAR=value <cmd>` | Set env var CHỈ cho 1 command |
| `which <cmd>` | Xem binary nào shell sẽ chạy |
| `which -a <cmd>` | Tất cả binary cùng tên trong PATH |
| `source ~/.zshrc` | Reload file config |

### File config persist

| File | Khi nào load |
|---|---|
| `~/.zshrc` | Mỗi khi mở zsh interactive |
| `~/.bashrc` | Mỗi khi mở bash interactive (Linux) |
| `~/.bash_profile` | Mỗi khi mở bash login (Mac) |
| `~/.profile` | Mọi shell user (fallback) |
| `/etc/environment` | System-wide (Linux) |

### Env var thường gặp

| Variable | Ý nghĩa |
|---|---|
| `$HOME` | Home folder user (`/Users/rom`) |
| `$USER` | Tên user |
| `$PATH` | List folder shell tìm command |
| `$SHELL` | Path shell hiện tại |
| `$EDITOR` | Editor mặc định (vim, nano, code) |
| `$LANG` | Locale (vd `en_US.UTF-8`) |
| `$PWD` | Working directory hiện tại |
| `$OLDPWD` | Working directory trước đó |
| `$HOSTNAME` | Tên máy |
| `$TMPDIR` | Folder temp |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Environment Variable | Biến môi trường | Biến lưu trong memory process, dùng config |
| Shell variable | Biến shell | Biến chỉ shell hiện tại thấy, không inherit |
| Export | Xuất khẩu | Cho child process kế thừa biến |
| `$PATH` | (giữ EN) | List folder shell tìm command |
| Inheritance | Kế thừa | Child process nhận env từ parent |
| Subshell | Shell con | Process shell mới spawn từ shell hiện tại |
| `.env` | (giữ EN) | File text chứa `KEY=value`, KHÔNG commit |
| `.env.example` | (giữ EN) | File mẫu commit, chỉ có KEY, không value |
| Secret | Bí mật | Env var nhạy cảm (API key, password) |
| Vault | Két | Tool quản lý secrets (HashiCorp Vault, AWS Secrets Manager) |
| `dotenv` | (giữ EN) | Library load `.env` thành env var |
| 12-factor app | (giữ EN) | Methodology: config qua env var, KHÔNG hardcode |
| Rotate | Xoay vòng | Đổi secret định kỳ để giảm rủi ro leak |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan trong kho

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [03_process-and-pid.md](./03_process-and-pid.md) — Process concept (env theo process) |
| ➡️ Bài tiếp | [05_io-redirection.md](./05_io-redirection.md) — chưa có |
| 📚 Git `.gitignore` cho `.env` | [Git lesson 01](../../../version-control/git/lessons/01_basic/01_init-and-first-commit.md) §3 |
| 🐳 Env var trong Docker | [Docker Compose lesson](../../../../10_DevOps/docker/lessons/01_basic/03_docker-compose.md) §6 |
| 🛠️ Customize shell `.zshrc` | [02_Tools/shell/](../../../../02_Tools/shell/) (chưa có content) |

### Tài nguyên ngoài

- [The Twelve-Factor App — III. Config](https://12factor.net/config) — chuẩn vàng config qua env var
- [dotenv (Node.js)](https://github.com/motdotla/dotenv) — library phổ biến nhất
- [python-dotenv](https://github.com/theskumar/python-dotenv) — cho Python
- [HashiCorp Vault](https://www.hashicorp.com/products/vault) — secret manager open-source
- [gitleaks](https://github.com/gitleaks/gitleaks) — scan repo tránh leak secret
- [direnv](https://direnv.net/) — tự load `.env` khi `cd` vào project (tool hay cho dev)

---

## 📌 Changelog

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster basic computing-environment 5/6 bài. Cover: env var concept, $PATH với mermaid lookup flow, 3 scope (process/session/persistent), inheritance parent-child với mermaid, `.env` pattern + `.env.example`, secrets vs config thường, vault tools, env trong Docker (3 cách), 5 pitfall + 4 self-check + cheatsheet 10 env var phổ biến.
