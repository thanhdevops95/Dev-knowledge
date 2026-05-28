# 🐳 Docker — Containerization Platform

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 26/05/2026

> 🎯 *Docker là nền tảng đóng gói app + dependencies thành container — chạy nhất quán mọi nơi. Mọi DevOps modern đều bắt đầu từ Docker.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu bản chất Container vs VM và kiến trúc Docker
- [x] Quản lý container thành thạo thông qua bộ lệnh CRUD container
- [x] Tự viết Dockerfile tối ưu để đóng gói ứng dụng cá nhân
- [x] Thiết lập môi trường chạy đa dịch vụ (App + DB + Cache) qua Docker Compose
- [x] Nắm vững các kỹ thuật tăng tốc build với BuildKit & Advanced Multi-stage
- [x] Đảm bảo an toàn chuỗi cung ứng hình ảnh (Image Security Scanning)
- [x] Tối ưu dung lượng image siêu nhỏ bằng Distroless và Scratch
- [x] Vận hành hệ thống Private Container Registry ở quy mô production

---

## 📂 Cấu trúc Chương trình học

### ⚙️ Setup — Cài đặt ban đầu
*   ✅ 🌟 [`setup/install-docker.md`](./setup/install-docker.md) — Cài đặt Docker Desktop & Engine trên macOS, Windows, Linux và kiểm tra cài đặt.

### 📖 Lessons Basic — Quy trình cơ bản (4 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`What is Docker`](./lessons/01_basic/00_what-is-docker.md) | 🌱 Intro | ✅ 🌟 | Tại sao có Docker, Container khác VM thế nào, mô hình Image/Container/Registry. |
| **01** | [`Images & Containers`](./lessons/01_basic/01_images-and-containers.md) | 🌳 Lesson | ✅ 🌟 | Dạy **8 lệnh CRUD container** cơ bản dùng hàng ngày (pull, run, stop, exec, etc.). |
| **02** | [`Dockerfile basics`](./lessons/01_basic/02_dockerfile-basics.md) | 🌳 Lesson | ✅ 🌟 | Dạy cách viết Dockerfile từ base image để tự build image cho ứng dụng của bạn. |
| **03** | [`Docker Compose`](./lessons/01_basic/03_docker-compose.md) | 🌳 Lesson | ✅ 🌟 | Dạy cách thiết lập và điều phối cụm multi-container app bằng 1 file YAML duy nhất. |

### 📖 Lessons Intermediate — Chuyên sâu Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ 🌟 | Giới thiệu các khía cạnh cần giải quyết khi đưa Docker lên production thực tế. |
| **01** | [`BuildKit & Advanced Multistage`](./lessons/02_intermediate/01_buildkit-and-multistage-advanced.md) | 🌳 Lesson | ✅ 🌟 | Sử dụng **BuildKit** để cache mount, secret mount, tăng tốc build và build multi-platform. |
| **02** | [`Image Security & Supply Chain`](./lessons/02_intermediate/02_image-security-supply-chain.md) | 🌳 Lesson | ✅ 🌟 | Bảo mật chuỗi cung ứng: Quét lỗ hổng với **Trivy**, xuất **SBOM** và ký số image với **Cosign**. |
| **03** | [`Optimization & Distroless`](./lessons/02_intermediate/03_optimization-and-distroless.md) | 🌳 Lesson | ✅ 🌟 | Phân tích layer bằng **dive**, tối ưu dung lượng và bảo mật với base image **distroless/scratch**. |
| **04** | [`Registry Production Patterns`](./lessons/02_intermediate/04_registry-production-patterns.md) | 🌳 Lesson | ✅ 🌟 | Vận hành Private Registry (Harbor, ECR, GHCR), quản lý tag immutable và garbage collection. |

---

## 🚀 Lộ trình đề xuất

*   🟢 **Beginner (Chưa biết gì):** Học tuần tự: [Setup](./setup/install-docker.md) → [Bài 00](./lessons/01_basic/00_what-is-docker.md) → Bài 01 → Bài 02 → Bài 03.
*   🟡 **Đã biết cơ bản nhưng muốn tối ưu:** Tập trung học ngay cụm **Lessons Intermediate (00 - 04)** để nắm kỹ năng thu nhỏ image và bảo mật nâng cao.
*   🧭 **Lộ trình DevOps chuyên nghiệp:** Hoàn thành toàn bộ 10 bài học này làm bước đệm bắt buộc trước khi chuyển sang học Kubernetes.

---

## 💡 Tài nguyên & Công cụ hỗ trợ

| Công cụ | Vai trò | Lệnh cài đặt nhanh |
|---|---|---|
| **dive** | Phân tích layer và độ hao phí dung lượng của Image | `brew install dive` |
| **hadolint** | Linter kiểm tra lỗi cú pháp và best practices Dockerfile | `brew install hadolint` |
| **lazydocker** | Giao diện Terminal cực đẹp để quản lý Container/Volume/Network | `brew install lazydocker` |
| **Awesome Compose** | Thư viện 50+ mẫu Docker Compose có sẵn | [GitHub Repo](https://github.com/docker/awesome-compose) |

---

## 📌 Changelog

- **v1.0.0 (26/05/2026)** — Cập nhật mục lục đầy đủ bao gồm cả cấu phần Basic và cụm bài học Intermediate Production-ready.
- **v0.1.0 (16/05/2026)** — Bản khởi sinh sơ bộ chỉ chứa lộ trình Basic.
