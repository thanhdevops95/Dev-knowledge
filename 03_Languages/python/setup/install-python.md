# Python — Cài đặt + venv + pip

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026\
> **OS hỗ trợ:** macOS / Linux / Windows\
> **Thời lượng cài:** ~15-30 phút\
> **Khó:** ⭐⭐ Medium (vì có version + venv)

> 🎯 *Cài Python 3.11+ trên máy + biết dùng `venv` cô lập dependency từng project + `pip` cài thư viện. Đây là nền tảng cho Stage 2 zero-to-coder.*

---

## 1️⃣ Python là gì + Khi nào cài

**Python** là ngôn ngữ lập trình phổ biến #1 (theo TIOBE/PYPL 2025). Dùng cho:
- Web backend (Django, FastAPI, Flask)
- Data science / ML (NumPy, Pandas, scikit-learn, PyTorch)
- Automation / scripting (system admin, web scraping)
- AI / LLM (LangChain, OpenAI SDK)

**Khi nào cài**: Stage 2 zero-to-coder. Hoặc bất kỳ project nào cần Python.

**Khi nào KHÔNG cần**: chỉ làm frontend pure JS (nhưng vẫn nên biết để chạy script tooling).

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Min | Recommend |
|---|---|---|
| OS | macOS 10.13 / Win 10 / Ubuntu 20+ | macOS 13+ / Win 11 / Ubuntu 22+ |
| Disk | 200 MB | 1 GB (kèm packages) |
| Python version | 3.10+ | **3.11 hoặc 3.12** (2026) |
| Prerequisites | Không | Terminal cơ bản, VS Code |

> ⚠️ **KHÔNG dùng Python 2** — đã EOL (end-of-life) 2020. Mọi tutorial mới dùng Python 3.

---

## 3️⃣ Cách cài Python

### So sánh nhanh

| OS | Option | Khi nào dùng | Khó |
|---|---|---|---|
| macOS | 🅰️ Homebrew | Đã có brew, update dễ | ⭐ |
| macOS | 🅱️ python.org installer | Đơn giản, không cần brew | ⭐ |
| macOS / Linux | 🅲 **pyenv** ⭐ | **RECOMMEND** — manage nhiều version | ⭐⭐ |
| Linux Ubuntu | 🅳 apt | Phổ biến (nhưng thường version cũ) | ⭐ |
| Windows | 🅴 python.org installer | Phổ biến nhất | ⭐ |
| Windows | 🅵 winget | Modern | ⭐ |
| Windows / Mac / Linux | 🅶 uv ⭐ | Modern (2024+), fastest | ⭐⭐ |

→ **Beginner**: Option 🅱️ (Mac) hoặc 🅴 (Windows) — đơn giản nhất.\
→ **Intermediate**: Option 🅲 (`pyenv`) — manage nhiều version Python cho nhiều project.\
→ **Modern 2026**: Option 🅶 (`uv`) — fast, replace pip + venv + pyenv.

---

### 🅰️ macOS — Homebrew

```bash
brew install python@3.12
```

Verify:

```bash
python3 --version
# Python 3.12.0
```

> 💡 **Lưu ý macOS**: `python` (không có 3) thường vẫn là Python 2 system — dùng `python3` thay vì `python`. Hoặc alias trong `~/.zshrc`: `alias python=python3`.

### 🅱️ macOS — python.org installer

1. Tải từ [python.org/downloads](https://www.python.org/downloads/) — chọn version 3.12.x
2. Mở file `.pkg` → cài như app thường
3. Verify trong Terminal: `python3 --version`

### 🅲 macOS / Linux — pyenv (RECOMMEND nếu cần nhiều version)

`pyenv` cho phép cài + switch nhanh nhiều version Python.

**Cài pyenv**:

```bash
# macOS
brew install pyenv

# Linux
curl https://pyenv.run | bash
```

Thêm vào `~/.zshrc` (hoặc `~/.bashrc`):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

Restart shell:

```bash
source ~/.zshrc
```

**Cài Python qua pyenv**:

```bash
pyenv install 3.12.0
pyenv global 3.12.0
```

Verify:

```bash
python --version
# Python 3.12.0
```

Set version cụ thể cho 1 project:

```bash
cd my-project
pyenv local 3.11.5    # tạo file .python-version
```

→ Khi vào folder này, Python tự switch sang 3.11.5.

### 🅳 Linux — apt (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

> ⚠️ apt thường có Python version cũ hơn (vd Ubuntu 22.04 có 3.10). Cần version mới → dùng pyenv hoặc deadsnakes PPA:
> ```bash
> sudo add-apt-repository ppa:deadsnakes/ppa
> sudo apt install python3.12
> ```

### 🅴 Windows — python.org installer (RECOMMEND beginner)

1. Tải từ [python.org/downloads/windows](https://www.python.org/downloads/windows/) — version 3.12.x
2. Chạy installer:
   - ✅ **BẮT BUỘC TÍCH** "Add python.exe to PATH" (ô ở dưới)
   - ✅ Tích "Use admin privileges when installing py.exe"
   - Click "Install Now"
3. Verify trong PowerShell:
   ```powershell
   python --version
   pip --version
   ```

> ⚠️ Nếu quên tích "Add to PATH" → chạy lại installer chọn "Modify" → tích.

### 🅵 Windows — winget

```powershell
winget install Python.Python.3.12
```

### 🅶 Modern 2024+ — uv (FASTEST)

[`uv`](https://github.com/astral-sh/uv) là tool mới của Astral (làm ruff), thay `pip` + `venv` + `pyenv` — nhanh hơn 10-100x.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cài Python + tạo venv:

```bash
uv python install 3.12      # cài Python
uv venv                      # tạo .venv
uv pip install requests      # cài package
```

→ Nếu mới học, dùng pip/venv truyền thống trước. Quen rồi switch sang `uv` cho tốc độ.

---

## 4️⃣ Verify cài đúng

```bash
python --version          # hoặc python3 --version trên Mac
```

```
Python 3.12.0
```

```bash
pip --version             # hoặc pip3
```

```
pip 23.x.x from /usr/local/lib/python3.12/site-packages/pip
```

Thử chạy Python interactive (REPL):

```bash
python
```

```
Python 3.12.0 (main, Oct  2 2023, ...)
>>> print("Hello, Python!")
Hello, Python!
>>> exit()
```

→ Cả 2 lệnh trên work = cài thành công.

---

## 5️⃣ Cấu hình ban đầu

### Tạo virtual environment (venv) cho project

**⚠️ Quy tắc vàng**: KHÔNG cài package vào Python system. Luôn dùng `venv` cho mỗi project.

**Vì sao?**
- Project A cần `requests 2.28`, project B cần `requests 2.31` → conflict nếu cài chung
- Cài global → "ô nhiễm" system Python → khó uninstall
- Khi đổi máy → không biết project nào cần gì

**Cách dùng venv**:

```bash
cd my-project
python -m venv .venv           # tạo virtual env trong folder .venv
```

Activate venv:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

→ Prompt sẽ có `(.venv)` ở đầu, báo bạn đang trong venv.

Cài package trong venv:

```bash
pip install requests
```

Save dependencies vào `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Cài lại từ requirements (vd trên máy khác):

```bash
pip install -r requirements.txt
```

Deactivate khi xong:

```bash
deactivate
```

> 💡 **Best practice**: thêm `.venv/` vào `.gitignore` (KHÔNG commit venv lên Git — chỉ commit `requirements.txt`).

### Cấu hình recommend

#### Alias `python` thay `python3` (macOS)

Trong `~/.zshrc`:

```bash
alias python=python3
alias pip=pip3
```

#### Default editor

Khi `git commit` không có message, Python sẽ mở editor. Set default:

```bash
git config --global core.editor "code --wait"
```

#### pip config — index mirror nhanh hơn (tùy chọn)

Nếu pip chậm:

```bash
# ~/.pip/pip.conf (Mac/Linux) hoặc %APPDATA%\pip\pip.ini (Windows)
[global]
index-url = https://pypi.org/simple/
timeout = 60
```

---

## 6️⃣ Extensions / tools phổ biến

### Trong VS Code (xem [VS Code setup §6](../../editor/setup/vs-code.md#6️⃣-extensions-phổ-biến))

| Extension | Vai trò |
|---|---|
| **Python** (`ms-python.python`) | Microsoft chính thức — linting, debug, intellisense |
| **Pylance** (`ms-python.vscode-pylance`) | Type checker + autocomplete cực mạnh |
| **Jupyter** (`ms-toolsai.jupyter`) | Notebook trong VS Code |
| **Ruff** (`charliermarsh.ruff`) | Linter + formatter siêu nhanh (thay flake8 + black) |
| **autoDocstring** (`njpwerner.autodocstring`) | Tự gen docstring khi gõ `"""` |

### Tool dòng lệnh nên cài

| Tool | Mục đích | Cài |
|---|---|---|
| **uv** | Package manager hiện đại | xem §3 🅶 |
| **ruff** | Linter + formatter | `pip install ruff` |
| **mypy** | Static type checker | `pip install mypy` |
| **pytest** | Testing framework | `pip install pytest` |
| **ipython** | REPL đẹp hơn `python` | `pip install ipython` |

### IDE alternative (nếu cần IDE chuyên sâu Python)

- **PyCharm Community** (free) — JetBrains, IDE Python chuyên sâu
- **PyCharm Professional** ($$) — kèm Django + DB tools

---

## 7️⃣ Lỗi thường gặp

### ❌ Lỗi 1: `python: command not found` (Mac/Linux)

- **Triệu chứng**: gõ `python` → "command not found"
- **Nguyên nhân**: Mac/Linux có `python3` chứ không có `python` mặc định
- **Fix**: dùng `python3` thay `python`, hoặc alias trong `~/.zshrc`

### ❌ Lỗi 2: `'python' is not recognized` (Windows)

- **Triệu chứng**: PowerShell báo lỗi sau cài
- **Nguyên nhân**: quên tích "Add to PATH" khi cài
- **Fix**: chạy lại installer → Modify → tích "Add to environment variables"

### ❌ Lỗi 3: `pip install` báo `permission denied`

```
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

- **Nguyên nhân**: cài vào system Python (không có quyền) thay vì venv
- **Fix**: tạo venv + activate trước khi pip install (xem §5)
- **TRÁNH**: `sudo pip install` — gây "ô nhiễm" system Python

### ❌ Lỗi 4: SSL certificate error khi pip install

```
WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
```

- **Nguyên nhân**: thường gặp khi cài bằng pyenv mà OpenSSL chưa đủ
- **Fix Mac**:
  ```bash
  brew install openssl@3
  CFLAGS="-I$(brew --prefix openssl@3)/include" \
  LDFLAGS="-L$(brew --prefix openssl@3)/lib" \
  pyenv install 3.12.0
  ```

### ❌ Lỗi 5: Venv activate không work trên Windows PowerShell

```
.venv\Scripts\Activate.ps1 : File ... cannot be loaded because running scripts is disabled
```

- **Fix** (chạy 1 lần với PowerShell admin):
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

### ❌ Lỗi 6: Project bị conflict version Python

```
This project requires Python 3.11 but you have 3.9
```

- **Fix**: dùng `pyenv` hoặc `uv` để switch version (xem §3 🅲/🅶)

---

## 8️⃣ Update + Uninstall

### Update

| Cách cài | Update |
|---|---|
| Homebrew | `brew upgrade python@3.12` |
| python.org | Tải installer version mới + cài đè |
| pyenv | `pyenv install 3.12.1 && pyenv global 3.12.1` |
| apt | `sudo apt upgrade python3` |
| winget | `winget upgrade Python.Python.3.12` |
| uv | `uv python install 3.12.1` |

### Uninstall

| OS | Cách |
|---|---|
| macOS (brew) | `brew uninstall python@3.12` |
| macOS (installer) | Chạy installer → "Uninstall", hoặc xoá `/Library/Frameworks/Python.framework` |
| Linux | `sudo apt remove python3` |
| Windows | Settings → Apps → Uninstall "Python 3.12" |

> ⚠️ KHÔNG uninstall **system Python** (Python đi kèm OS, đặc biệt Linux) — sẽ hỏng hệ thống.

---

## 9️⃣ Alternative (so sánh ngôn ngữ tương tự)

| Ngôn ngữ | Strength | Phù hợp ai |
|---|---|---|
| **Python** (đang nói) | Dễ học, đa dụng, hệ sinh thái lớn | Beginner, data, AI, automation |
| **JavaScript / Node.js** | Web frontend + backend, async tốt | Web dev |
| **Go** | Compiled, concurrent, gọn | Backend, DevOps tools |
| **Rust** | Memory safe, zero-cost abstraction | System programming, performance |
| **Ruby** | Đẹp, Rails | Web (Rails ecosystem) |

→ Beginner 2026: **chọn Python** — easiest + most versatile.

---

## 🔗 Liên kết

### Bài học dùng Python

- [What is Python](../lessons/01_basic/00_what-is-python.md) — sau khi cài xong, đọc bài này tiếp
- [Variables and types](../lessons/01_basic/01_variables-and-types.md)

### Setup liên quan

- [VS Code + Python extension](../../editor/setup/vs-code.md#6️⃣-extensions-phổ-biến)
- (sắp có) `setup/poetry-or-uv.md` — modern package management
- (sắp có) `setup/jupyter-notebook.md` — notebook setup

### Tài nguyên ngoài

- [Python Official Docs](https://docs.python.org/3/) — official
- [Real Python](https://realpython.com/) — tutorial chất lượng
- [Python Packaging Guide](https://packaging.python.org/en/latest/) — venv, pip, build, publish

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên — setup Python 7 option (Homebrew, pyenv, apt, installer, winget, uv) + venv + pip + 6 lỗi thường gặp.
