# 🐍 Python — Programming Language

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> 🎯 *Python — ngôn ngữ lập trình **#1 thế giới 2026** (theo TIOBE/PYPL). Dễ học, đa dụng (web/AI/data/automation). Folder này cover từ "cài Python" tới Python intermediate.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:

- [ ] Cài + cấu hình Python + venv + pip
- [ ] Viết script Python ~50 dòng giải bài toán đời thực
- [ ] Đọc + hiểu code Python 200 dòng bất kỳ
- [ ] Hiểu OOP, exception, decorator, generator
- [ ] Viết test với pytest
- [ ] Đọc tài liệu thư viện Python bất kỳ

---

## 📂 Cấu trúc

### setup/ — Cài đặt + môi trường

| File | Trạng thái | Note |
|---|---|---|
| ✅ 🌟 [`setup/install-python.md`](./setup/install-python.md) | Done | 7 option cài (brew, pyenv, apt, installer, winget, uv) + venv + pip |
| ❌ `setup/poetry-or-uv.md` | Chưa có | Modern package manager |
| ❌ `setup/jupyter-notebook.md` | Chưa có | Notebook setup |

### lessons/01_basic/ — Python từ đầu

| # | Bài | Loại | Trạng thái |
|---|---|---|---|
| 00 | [What is Python](./lessons/01_basic/00_what-is-python.md) | 🌱 Intro | ✅ 🌟 |
| 01 | [Variables & Types](./lessons/01_basic/01_variables-and-types.md) | 🌳 Lesson | ✅ 🌟 |
| 02 | [Control Flow](./lessons/01_basic/02_control-flow.md) | 🌳 Lesson | ✅ 🌟 |
| 03 | [Functions](./lessons/01_basic/03_functions.md) | 🌳 Lesson | ✅ 🌟 |
| 04 | IO & Files (chưa có) | 🌳 Lesson | ❌ |
| 05 | Modules & Packages (chưa có) | 🌳 Lesson | ❌ |
| 06 | Error handling (chưa có) | 🌳 Lesson | ❌ |

### lessons/02_intermediate/ — Đào sâu Python

| # | Bài (dự kiến) | Trạng thái |
|---|---|---|
| 00 | OOP (class, inheritance, polymorphism) | ❌ |
| 01 | Decorators | ❌ |
| 02 | Generators & iterators | ❌ |
| 03 | Comprehensions advanced | ❌ |
| 04 | Type hints + mypy | ❌ |
| 05 | pytest — testing | ❌ |

### lessons/03_advanced/

❌ Chưa có (dự kiến: async/await, concurrency, metaclasses, performance)

### exercises/, projects/, recipes/

❌ Chưa có

---

## 🚀 Lộ trình đề xuất

| Nhu cầu | Đi theo |
|---|---|
| **Học từ đầu** | [Setup](./setup/install-python.md) → [00_what-is-python](./lessons/01_basic/00_what-is-python.md) → 01 → 02 → 03 → ... |
| **Đã biết 1 ngôn ngữ khác** | Skim 00 → đi nhanh qua 01-03 → vào intermediate khi có |
| **Ôn lại cách viết Pythonic** | Skim 01-03 phần "Pitfall & Best practice" |
| **Theo Zero-to-Coder Stage 2** | Setup + 4 bài đầu (00-03) đủ cho Stage 2 (Python cơ bản) |

---

## 🌟 Sản phẩm sau bộ Python basic (4 bài)

Sau setup + 4 bài (00-03), bạn có thể:
- Cài Python + venv + pip
- Hiểu 7 kiểu data: int, float, str, bool, list, dict, tuple, set
- Viết if/for/while + comprehension
- Viết function với args, kwargs, return, lambda
- Đọc + viết script Python ~100 dòng giải bài toán cơ bản

→ Stage 2 zero-to-coder gần đủ — còn thiếu IO/files + module để hoàn thành 100%.

---

## 💡 Khuyến nghị practice

| Tài nguyên | Mô tả |
|---|---|
| [Exercism Python track](https://exercism.org/tracks/python) | 100+ bài tập có mentor review FREE |
| [Codewars](https://www.codewars.com/) | Bài tập gamified — kata |
| [LeetCode Easy](https://leetcode.com/problemset/?difficulty=EASY) | Algorithm cơ bản |
| [Real Python Tutorials](https://realpython.com/) | Tutorial sâu các chủ đề |
| [Automate the Boring Stuff (free book)](https://automatetheboringstuff.com/) | Practical Python automation |

---

## 🛠️ Tool chains recommend

| Tool | Mục đích | Cài |
|---|---|---|
| **VS Code + Python extension** | Editor | [VS Code setup](../../02_tools/ide/vs-code.md) |
| **uv** | Package manager hiện đại | xem [setup §3 🅶](./setup/install-python.md#3️⃣-cách-cài-python) |
| **ruff** | Linter + formatter | `pip install ruff` |
| **mypy** | Static type checker | `pip install mypy` |
| **pytest** | Testing | `pip install pytest` |
| **ipython** | REPL đẹp | `pip install ipython` |

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Bộ Python basic đầu tiên: setup + 4 bài (intro + 3 lesson). Stage 2 zero-to-coder có Python foundation đủ chạy.
