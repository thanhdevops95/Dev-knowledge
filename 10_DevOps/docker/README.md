# 🐳 Docker — Containerization Platform

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> 🎯 *Docker là nền tảng đóng gói app + dependencies thành container — chạy nhất quán mọi nơi. Mọi DevOps modern đều bắt đầu từ Docker.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:

- [ ] Cài Docker + chạy container đầu tiên
- [ ] Quản lý containers (pull/run/stop/rm/logs/exec)
- [ ] Viết Dockerfile build image cho app riêng
- [ ] Dùng Docker Compose cho multi-container app
- [ ] Hiểu volumes, networks, environment variables
- [ ] Apply best practices (caching, security, image size)

---

## 📂 Cấu trúc

### setup/ — Cài đặt

| File | Trạng thái | Note |
|---|---|---|
| ✅ 🌟 [`setup/install-docker.md`](./setup/install-docker.md) | Done | Docker Desktop + Engine 5 OS + verify |

### lessons/01_basic/ — Workflow cơ bản

| # | Bài | Loại | Trạng thái |
|---|---|---|---|
| 00 | [What is Docker](./lessons/01_basic/00_what-is-docker.md) | 🌱 Intro | ✅ 🌟 |
| 01 | [Images & Containers](./lessons/01_basic/01_images-and-containers.md) | 🌳 Lesson | ✅ 🌟 |
| 02 | [Dockerfile basics](./lessons/01_basic/02_dockerfile-basics.md) | 🌳 Lesson | ✅ 🌟 |
| 03 | [Docker Compose](./lessons/01_basic/03_docker-compose.md) | 🌳 Lesson | ✅ 🌟 |
| 04 | Volumes & Networking | 🌳 Lesson | ❌ |
| 05 | Multi-stage builds + Best practices | 🌳 Lesson | ❌ |
| 06 | Registry & Image management | 🌳 Lesson | ❌ |

### lessons/02_intermediate/, 03_advanced/

❌ Chưa có (dự kiến: BuildKit, security hardening, monitoring, Docker Swarm, CI/CD with Docker)

### exercises/, projects/, recipes/

❌ Chưa có (dự kiến: build real app + Dockerfile + Compose, troubleshoot common errors)

---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đi theo |
|---|---|
| 🟢 **Beginner zero-base** | [Setup](./setup/install-docker.md) → [00_what-is-docker](./lessons/01_basic/00_what-is-docker.md) → 01 → 02 → 03 |
| 🟡 **Đã biết container nhưng chưa thạo Compose** | Skim 00-01 → đi sâu [03_docker-compose](./lessons/01_basic/03_docker-compose.md) |
| 🟠 **Senior ôn lại Pythonic best practices** | Skim các bài, focus "Pitfall & Best practice" section |
| 🧭 **DevOps career path** | 4 bài (00-03) là **prerequisite** cho K8s, CI/CD, IaC |

---

## 🌟 Sản phẩm sau bộ Docker basic (4 bài)

Sau 4 bài, bạn có thể:
- Cài Docker trên bất kỳ OS
- Pull + run + manage container nginx/postgres/redis
- Viết Dockerfile cho app Python/Node
- Setup multi-container app với Compose (app + DB + cache)
- Dùng volumes lưu data persistent
- Hiểu service networking trong Compose

→ Đủ skill **dùng Docker daily** cho local dev + deploy đơn giản. Tiếp theo: K8s cho orchestration ở scale.

---

## 💡 Khuyến nghị practice

| Tài nguyên | Mô tả |
|---|---|
| [Awesome Compose](https://github.com/docker/awesome-compose) | 50+ example: MERN, LAMP, FastAPI+Postgres, ... |
| [Play with Docker](https://labs.play-with-docker.com/) | Sandbox 4h online, không cần cài |
| [Docker for Beginners](https://docker-curriculum.com/) | Tutorial step-by-step free |
| [DevOps Roadmap](https://roadmap.sh/devops) | Tổng quan career path |

---

## 🛠️ Tool chains recommend

| Tool | Mục đích | Cài |
|---|---|---|
| **Docker Desktop** | Mac/Win GUI | [setup](./setup/install-docker.md) |
| **OrbStack** (Mac) | Nhanh hơn Docker Desktop nhiều | `brew install orbstack` |
| **dive** | Phân tích layer image | `brew install dive` |
| **hadolint** | Linter Dockerfile | `brew install hadolint` |
| **lazydocker** | Terminal UI quản lý containers | `brew install lazydocker` |
| **VS Code Docker extension** | Manage trong editor | xem [VS Code setup](../../02_Tools/ide/vs-code.md) |

---

## 🤝 Muốn viết thêm bài Docker?

1. Đọc [`../../_Blueprint/README.md`](../../_Blueprint/README.md)
2. Chọn template:
   - Setup → `setup_template.md`
   - Lesson → `lesson_template.md`
3. Tham khảo 4 bài có sẵn làm reference
4. Cập nhật bảng trên + [`../../MASTER-CATALOG.md`](../../MASTER-CATALOG.md)

---

## 📌 Changelog

- **v0.1.0 (16/05/2026)** — Bộ Docker basic đầu tiên: setup + intro + 3 lessons (images/Dockerfile/Compose). Production-ready cho dev daily.
