# Module 08: CI (Continuous Integration)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **CI** | - | Continuous Integration - Tích hợp liên tục, merge code thường xuyên |
| **Pipeline** | - | Đường ống - Chuỗi các bước tự động từ code đến deploy |
| **Build** | - | Biên dịch/đóng gói code thành artifact |
| **Test** | - | Kiểm thử tự động code |
| **Artifact** | - | Sản phẩm của quá trình build (jar, docker image) |
| **Workflow** | - | Luồng công việc - Định nghĩa các jobs trong CI |
| **Job** | - | Công việc - Một nhóm steps chạy trên một runner |
| **Step** | - | Bước - Một lệnh hoặc action đơn lẻ |
| **Runner** | - | Máy thực thi jobs (GitHub-hosted hoặc self-hosted) |
| **Trigger** | - | Sự kiện kích hoạt pipeline (push, PR, schedule) |
| **Matrix** | - | Ma trận - Test trên nhiều phiên bản/OS |
| **Secret** | - | Bí mật - Biến môi trường an toàn (API keys, passwords) |
| **Lint** | - | Kiểm tra style và lỗi code tĩnh |

---

## 🎬 Câu chuyện mở đầu

Team của bạn có 5 developers. Mỗi người làm feature riêng, merge vào main vào cuối tuần...

**Thứ 6:** Cả 5 merge code cùng lúc → 50 conflicts → mất cả weekend fix.

**Thứ 2:** Test phát hiện 3 bugs, nhưng không biết bug từ feature nào.

Đây là vấn đề của **"Integration Hell"**.

**CI (Continuous Integration)** giải quyết bằng cách: merge thường xuyên, test tự động, phát hiện lỗi sớm.

---

## 📖 CI là gì? (Định nghĩa từ gốc)

### Trước hết: Integration là gì?

**Integration = Kết hợp code từ nhiều developers thành một codebase hoạt động.**

Khi nhiều người cùng làm việc trên một project:

- Developer A sửa file X
- Developer B cũng sửa file X
- Khi cả hai merge → **Conflict!**

```
Dev A: function login() { return true; }
                    ↓ merge conflict ↓
Dev B: function login() { return false; }
```

**Integration cũ (không có CI):**

| Bước | Vấn đề |
|------|--------|
| Develop 2 tuần | Code diverge rất xa |
| Merge cuối sprint | 100+ conflicts |
| Fix conflicts | Mất 2-3 ngày |
| Test thủ công | "Ai đã break build?" |

### Continuous Integration giải quyết

> **CI = Merge code thường xuyên (hàng ngày hoặc nhiều lần/ngày) + Test tự động mỗi lần merge**

**Hai nguyên tắc chính:**

1. **Merge thường xuyên:** Thay vì merge cuối tuần, merge mỗi ngày → Conflicts nhỏ, dễ fix
2. **Test tự động:** Mỗi merge đều chạy tests → Biết ngay code nào break

```
Không có CI:                        Có CI:
Dev → Dev → Dev → MERGE → TEST     Dev → MERGE+TEST → Dev → MERGE+TEST
     (2 tuần)      (pain)               (liên tục, nhỏ)
```

**Kết quả:**

| Không có CI | Có CI |
|-------------|-------|
| "Integration day" đau đớn | Integration liên tục, không đau |
| Bug phát hiện sau 2 tuần | Bug phát hiện trong 10 phút |
| "Ai break the build?" | Git commit hash cho thấy ai, khi nào |
| Test thủ công, bỏ sót | Test tự động, consistent |

### CI trong thực tế

**CI Pipeline** là chuỗi các bước tự động chạy mỗi khi có code mới:

```
Developer pushes code
        │
        ▼
┌─────────────────────────────────────┐
│           CI PIPELINE               │
├─────────────────────────────────────┤
│  1. Clone code                      │
│  2. Install dependencies            │
│  3. Run linter (check style)        │
│  4. Run unit tests                  │
│  5. Run integration tests           │
│  6. Build artifact (Docker image)   │
│  7. Security scan                   │
└─────────────────────────────────────┘
        │
        ▼
   ✅ Pass → Ready for merge/deploy
   ❌ Fail → Block merge, notify developer
```

---

## 🔧 GitHub Actions

### Tại sao GitHub Actions?

- **Free** cho public repos
- **Integrated** với GitHub
- **YAML** config (simple)
- **Marketplace** với 1000s actions
- **Matrix builds** (multiple OS/versions)

### Cấu trúc

```
.github/
└── workflows/
    ├── ci.yml
    ├── deploy.yml
    └── release.yml
```

### Workflow cơ bản

Đây là ví dụ một CI workflow hoàn chỉnh cho Node.js project. Hãy đi qua từng phần:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Run lint
        run: npm run lint
```

**Giải thích từng phần:**

| Section | Ý nghĩa |
|---------|---------|
| `name: CI` | Tên workflow - hiển thị trong GitHub UI |
| `on: push/pull_request` | Khi nào chạy - push hoặc PR vào main/develop |
| `runs-on: ubuntu-latest` | Môi trường chạy - Ubuntu VM mới nhất |
| `uses: actions/checkout@v4` | Action có sẵn - clone repo vào runner |
| `uses: actions/setup-node@v4` | Cài đặt Node.js version 18 với npm cache |
| `run: npm ci` | Chạy command - "ci" nhanh hơn "install" cho CI |

> 💡 **Tip:** Dùng `npm ci` thay vì `npm install` trong CI - nó nhanh hơn và đảm bảo sử dụng exact versions từ package-lock.json.

### Triggers (on)

**Triggers** định nghĩa KHI NÀO workflow chạy. Có nhiều loại:

```yaml
on:
  # 1. Push vào specific branches
  push:
    branches: [main]
    paths:              # Chỉ chạy khi files này thay đổi
      - 'src/**'
      - 'package.json'
  
  # 2. Pull requests vào main
  pull_request:
    branches: [main]
  
  # 3. Schedule - chạy theo lịch (UTC time)
  schedule:
    - cron: '0 0 * * *'  # Daily midnight UTC
    # Dùng cho: nightly builds, dependency updates
  
  # 4. Manual trigger - chạy thủ công từ UI
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

**Các trigger phổ biến:**

| Trigger | Use case |
|---------|----------|
| `push` | Test mỗi commit |
| `pull_request` | Gate cho merge (phải pass mới merge được) |
| `schedule` | Nightly builds, security scans |
| `workflow_dispatch` | Manual deploys, release |
| `release` | Khi tạo GitHub Release |

### Jobs và Steps

**Jobs** chạy song song (parallel) trừ khi bạn dùng `needs`. **Steps** trong một job chạy tuần tự (sequential).

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."
  
  test:
    runs-on: ubuntu-latest
    needs: build  # ← Chờ build xong mới chạy
    steps:
      - run: echo "Testing..."
  
  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]  # ← Chờ CẢ HAI xong
    if: github.ref == 'refs/heads/main'  # ← Chỉ deploy trên main
    steps:
      - run: echo "Deploying..."
```

**Hiểu về job dependencies:**

```
                    ┌────────────┐
                    │   build    │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │   test     │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
    (only on main) │  deploy    │
                    └────────────┘
```

> 💡 **Best practice:** Sử dụng `if:` để control khi nào job chạy. Ví dụ: chỉ deploy khi push vào main, không phải PR.

### Environment Variables & Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production
    
    steps:
      - name: Deploy to server
        env:
          SSH_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          echo "$SSH_KEY" > key.pem
          chmod 600 key.pem
          ssh -i key.pem user@server "deploy.sh"
```

---

## 📦 Complete CI Pipeline

### Python Project

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest flake8
      
      - name: Lint with flake8
        run: flake8 . --max-line-length=120
      
      - name: Test with pytest
        run: pytest --cov=app tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Docker Build & Push

```yaml
name: Docker CI

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            myuser/myapp:latest
            myuser/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 📝 Tổng kết Module 08

### Bạn đã học

✅ CI là gì và tại sao cần  
✅ GitHub Actions basics  
✅ Workflow triggers  
✅ Jobs và dependencies  
✅ Secrets management  
✅ Docker builds trong CI  

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành CI](LABS.md)**
