# ❓ Quiz: CI/CD Basic

> **20 questions about CI/CD, GitLab CI, and GitHub Actions**
>
> *20 câu hỏi về CI/CD, GitLab CI, và GitHub Actions.*

---

## Section 1: CI/CD Concepts (Khái niệm CI/CD)

### Q1

CI stands for? (CI là viết tắt của?)

- a) Container Integration (Tích hợp Container)
- b) Continuous Integration (Tích hợp liên tục)
- c) Code Integration (Tích hợp mã nguồn)
- d) Complete Integration (Tích hợp hoàn toàn)

---

### Q2

CD can mean? (CD có thể là?)

- a) Continuous Delivery (Chuyển giao liên tục)
- b) Continuous Deployment (Triển khai liên tục)
- c) Both a and b (Cả a và b)
- d) Continuous Development (Phát triển liên tục)

---

### Q3

What is the main benefit of CI? (Lợi ích chính của CI là gì?)

- a) Faster deployments (Triển khai nhanh hơn)
- b) Early bug detection (Phát hiện lỗi sớm)
- c) Lower costs (Giảm chi phí)
- d) More features (Nhiều tính năng hơn)

---

### Q4

Which stage typically comes first in a CI/CD pipeline? (Stage nào thường đầu tiên trong pipeline?)

- a) Deploy (Triển khai)
- b) Build (Xây dựng)
- c) Lint/Test (Kiểm tra lỗi/Test)
- d) Release (Phát hành)

---

## Section 2: GitLab CI (Primary Platform)

### Q5

GitLab CI pipeline file is named? (File pipeline GitLab CI tên là?)

- a) .gitlab-pipeline.yml
- b) .gitlab-ci.yml
- c) gitlab-ci.yaml
- d) .ci.yml

---

### Q6

In GitLab CI, what defines the order of execution? (Trong GitLab CI, cái gì định nghĩa thứ tự thực thi?)

- a) jobs (các công việc)
- b) stages (các giai đoạn)
- c) scripts (kịch bản)
- d) variables (biến)

---

### Q7

How to access GitLab Container Registry? (Làm sao truy cập GitLab Container Registry?)

- a) `$DOCKER_REGISTRY`
- b) `$CI_REGISTRY`
- c) `$GITLAB_REGISTRY`
- d) `$CONTAINER_REGISTRY`

---

### Q8

What does `when: manual` do in GitLab CI? (`when: manual` làm gì trong GitLab CI?)

- a) Runs automatically (Chạy tự động)
- b) Requires manual trigger (Cần trigger thủ công)
- c) Skips the job (Bỏ qua job)
- d) Runs on schedule (Chạy theo lịch)

---

### Q9

How to define job dependencies in GitLab CI? (Làm sao định nghĩa dependencies trong GitLab CI?)

- a) `depends_on:`
- b) `requires:`
- c) `needs:`
- d) `after:` (sau khi)

---

### Q10

GitLab CI caching is configured with? (Caching trong GitLab CI được cấu hình bằng?)

- a) `cache:`
- b) `caching:`
- c) `store:`
- d) `save:`

---

### Q11

What is `artifacts` used for in GitLab CI? (`artifacts` dùng để làm gì trong GitLab CI?)

- a) Define variables (Định nghĩa variables)
- b) Store files between jobs (Lưu files giữa các jobs)
- c) Run scripts (Chạy scripts)
- d) Cache dependencies (Cache dependencies)

---

### Q12

How to run a job only on main branch? (Làm sao chạy job chỉ trên branch main?)

- a) `branch: main`
- b) `only: - main`
- c) `if: main`
- d) `when: main`

---

### Q13

What does `$CI_COMMIT_SHORT_SHA` contain? (`$CI_COMMIT_SHORT_SHA` chứa gì?)

- a) Full commit hash (Commit hash đầy đủ)
- b) Short commit hash (Commit hash ngắn)
- c) Branch name (Tên branch)
- d) Project name (Tên project)

---

## Section 3: GitHub Actions (Alternative Platform)

### Q14

GitHub Actions workflow files are stored in? (Files workflow GitHub Actions ở đâu?)

- a) .github/actions/
- b) .github/workflows/
- c) .workflows/
- d) workflows/

---

### Q15

In GitHub Actions, `runs-on: ubuntu-latest` specifies? (`runs-on: ubuntu-latest` chỉ định gì?)

- a) Docker image (Ảnh Docker)
- b) Runner OS (Hệ điều hành Runner)
- c) Node version (Phiên bản Node)
- d) Branch name (Tên nhánh)

---

### Q16

How to access secrets in GitHub Actions? (Làm sao truy cập secrets trong GitHub Actions?)

- a) `$SECRETS.NAME`
- b) `${{ secrets.NAME }}`
- c) `secrets.NAME`
- d) `$secrets.NAME`

---

### Q17

What does `actions/checkout@v4` do? (`actions/checkout@v4` làm gì?)

- a) Create checkout (Tạo checkout)
- b) Clone repository (Sao chép kho lưu trữ)
- c) Push code (Đẩy mã lên)
- d) Delete code (Xóa mã)

---

## Section 4: Comparison (So sánh)

### Q18

Which platform uses `stages:` to define pipeline structure? (Platform nào dùng `stages:` để định nghĩa cấu trúc pipeline?)

- a) GitHub Actions
- b) GitLab CI
- c) Both (Cả hai)
- d) Neither (Không platform nào)

---

### Q19

Which platform has built-in Container Registry? (Platform nào có Container Registry tích hợp?)

- a) GitHub only (Chỉ GitHub)
- b) GitLab only (Chỉ GitLab)
- c) Both (Cả hai)
- d) Neither (Không platform nào)

---

### Q20

For scheduled pipelines, which statement is correct? (Với pipeline theo lịch, statement nào đúng?)

- a) Only GitLab supports scheduling (Chỉ GitLab hỗ trợ)
- b) Only GitHub supports scheduling (Chỉ GitHub hỗ trợ)
- c) Both support scheduling through UI (Cả hai hỗ trợ qua UI)
- d) Neither supports scheduling (Không platform nào hỗ trợ)

---

## 📝 Answers (Đáp án)

<details>
<summary>Click to view answers (Click để xem đáp án)</summary>

### Section 1: CI/CD Concepts

| Q | Answer | Explanation (Giải thích) |
|---|--------|--------------------------|
| 1 | b | Continuous Integration |
| 2 | c | CD can mean both Delivery and Deployment |
| 3 | b | CI helps catch bugs early through automated testing |
| 4 | c | Linting and testing usually come first |

### Section 2: GitLab CI

| Q | Answer | Explanation (Giải thích) |
|---|--------|--------------------------|
| 5 | b | GitLab CI config file is `.gitlab-ci.yml` |
| 6 | b | `stages:` defines execution order |
| 7 | b | `$CI_REGISTRY` contains registry URL |
| 8 | b | `when: manual` requires manual trigger |
| 9 | c | `needs:` defines job dependencies |
| 10 | a | `cache:` configures caching |
| 11 | b | Artifacts store files between jobs |
| 12 | b | `only: - main` runs only on main branch |
| 13 | b | Short commit hash (first 8 characters) |

### Section 3: GitHub Actions

| Q | Answer | Explanation (Giải thích) |
|---|--------|--------------------------|
| 14 | b | `.github/workflows/` directory |
| 15 | b | Runner operating system |
| 16 | b | `${{ secrets.NAME }}` syntax |
| 17 | b | Clones the repository to runner |

### Section 4: Comparison

| Q | Answer | Explanation (Giải thích) |
|---|--------|--------------------------|
| 18 | b | Only GitLab CI uses `stages:` |
| 19 | c | Both have container registries |
| 20 | c | Both support scheduled pipelines |

### Score Guide (Hướng dẫn chấm điểm)

| Score | Level (Mức độ) |
|-------|----------------|
| 18-20 | Expert (Chuyên gia) ⭐⭐⭐ |
| 14-17 | Proficient (Thành thạo) ⭐⭐ |
| 10-13 | Intermediate (Trung bình) ⭐ |
| < 10 | Need more practice (Cần luyện thêm) |

</details>

---

**[← Back to README](./README.md)** | **[View Labs →](./LABS.md)**
