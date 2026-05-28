# 📦 Python Packaging & Project Setup

> `[INTERMEDIATE]` — Prerequisite: `01-python-basics.md`
> Setup project structure, virtual environments, dependencies, và packaging.

---

## 1. Virtual Environments

```bash
# ── venv (built-in, recommended) ──
python -m venv .venv                # Create
source .venv/bin/activate           # Activate (Linux/macOS)
.venv\Scripts\activate              # Activate (Windows)
deactivate                          # Deactivate

# ── pyenv — multiple Python versions ──
pyenv install 3.12.0
pyenv local 3.12.0                  # Set version for this project
pyenv virtualenv 3.12.0 myproject   # Create virtualenv
pyenv activate myproject

# ── conda (data science) ──
conda create -n myenv python=3.12
conda activate myenv
conda install pandas numpy
```

---

## 2. Project Structure

```
my-project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── models.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_models.py
├── docs/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .env.example
├── pyproject.toml          # Modern config ⭐
├── README.md
└── Makefile                # Common commands
```

---

## 3. pyproject.toml — Modern Python Config

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov",
    "ruff",      # Linter + formatter
    "mypy",      # Type checking
    "pre-commit",
]

[project.scripts]
myapp = "my_package.cli:main"    # Entry point

# ── Tool configs ──
[tool.ruff]
target-version = "py310"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"

[tool.mypy]
python_version = "3.10"
strict = true
```

---

## 4. Dependency Management

```bash
# ── pip + requirements.txt ──
pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt

# ── pip-tools (recommended cho reproducibility) ──
pip install pip-tools
# requirements.in → requirements.txt (pinned versions)
echo "requests>=2.28" > requirements.in
pip-compile requirements.in          # Generate locked requirements.txt
pip-sync requirements.txt            # Install exact versions

# ── Poetry (all-in-one) ──
poetry init
poetry add requests pydantic
poetry add --group dev pytest ruff
poetry install
poetry run pytest
poetry build                         # Create wheel + sdist
poetry publish                       # Upload to PyPI

# ── uv (Rust-based, ultra fast) ──
uv pip install requests              # 10-100x faster than pip
uv venv                              # Create venv
uv pip sync requirements.txt
```

---

## 5. Code Quality Tools

```bash
# ── Ruff (linter + formatter, fast!) ──
ruff check .                   # Lint
ruff format .                  # Format (replaces black)

# ── Type checking ──
mypy src/                      # Static type analysis

# ── Pre-commit hooks ──
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy

pre-commit install              # Setup hooks
pre-commit run --all-files      # Run manually
```

---

## 6. Makefile — Common Commands

```makefile
.PHONY: install test lint format clean

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache dist build *.egg-info
```

---

## Gotchas

| # | ❌ Sai | ✅ Đúng |
|---|--------|---------|
| 1 | `pip install` globally | Luôn dùng virtualenv |
| 2 | `pip freeze` vào requirements.txt | Dùng pip-tools hoặc Poetry lock file |
| 3 | `setup.py` / `setup.cfg` | Dùng `pyproject.toml` (PEP 621) |
| 4 | Commit `.venv/` | Thêm `.venv/` vào `.gitignore` |

---

## Tài nguyên thêm

- [Python Packaging Guide](https://packaging.python.org/) — Official guide
- [Poetry Docs](https://python-poetry.org/docs/) — Poetry documentation
- [Ruff](https://docs.astral.sh/ruff/) — Fast Python linter
- [uv](https://github.com/astral-sh/uv) — Ultra-fast pip replacement
