# ⚙️ Track 2: Orchestration & Automation

[![Duration](https://img.shields.io/badge/Duration-6--8%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)
[![Prerequisites](https://img.shields.io/badge/Prerequisites-Track%201-green?style=flat-square)](../Track1_Foundation_StaticWeb/)

> **Level Up DevOps Skills** - Master Docker Compose, Kubernetes, Jenkins, and Monitoring stack.
>
> *Nâng cao kỹ năng DevOps - Thành thạo Docker Compose, Kubernetes, Jenkins và Monitoring.*

---

## 🎯 Track Objectives (Mục Tiêu)

After completing Track 2, you will (Sau khi hoàn thành Track 2, bạn sẽ):

- ✅ Build multi-container applications with Docker Compose (Xây dựng ứng dụng đa container)
- ✅ Optimize Docker images - multi-stage builds, caching (Tối ưu Docker images)
- ✅ Set up CI/CD pipelines with Jenkins (Thiết lập CI/CD với Jenkins)
- ✅ Deploy and manage applications on Kubernetes (Deploy ứng dụng trên K8s)
- ✅ Implement monitoring with Prometheus & Grafana (Triển khai monitoring)
- ✅ Centralized logging with ELK Stack (Logging tập trung với ELK)
- ✅ **Deploy microservices architecture on Kubernetes cluster** (Deploy microservices trên K8s)

---

## 🤔 Why This Track? (Tại sao học Track này?)

After Track 1, you can run 1 container. But real apps have **web + api + database + cache** - you need tools to manage them.

*Sau Track 1, bạn đã biết chạy 1 container. Nhưng ứng dụng thực tế có **web + api + database + cache** - cần công cụ để quản lý.*

| Container count (Số lượng) | Method (Phương pháp) | Note (Ghi chú) |
|---------------------------|----------------------|----------------|
| 1-3 | `docker run` | OK for development *(OK cho development)* |
| 5-20 | Docker Compose | Multi-container apps |
| 20-1000+ | Kubernetes | Production orchestration |

**Goal of this Track:** You will deploy microservices + monitoring on Kubernetes cluster.

*Điểm đến của Track này: Bạn sẽ deploy microservices + monitoring lên Kubernetes cluster.*

---

## 📋 Prerequisites (Điều kiện tiên quyết)

Before starting Track 2, you should complete (Trước khi bắt đầu Track 2, bạn cần hoàn thành):

- ✅ **Track 1: Foundation & Static Web**
- ✅ Understand Docker fundamentals (Hiểu Docker cơ bản)
- ✅ Have experience with GitLab CI/CD (Có kinh nghiệm với GitLab CI/CD)
- ✅ Familiar with Linux command line (Quen thuộc với Linux)

---

## 📚 Module List (Danh Sách Modules)

| # | Module | Duration (Thời gian) | Description (Mô tả) |
|---|--------|----------------------|---------------------|
| 2.1 | [Docker Advanced](./2.1_Docker_Advanced/) | 1 week | Multi-stage builds, optimization, security (Tối ưu images, bảo mật) |
| 2.2 | [Docker Compose](./2.2_Docker_Compose/) | 1 week | Multi-container apps, networking, volumes (Ứng dụng đa container) |
| 2.3 | [Jenkins](./2.3_Jenkins/) | 1-2 weeks | CI/CD pipelines, Jenkinsfile, plugins (Pipelines tự động hóa) |
| 2.4 | [Kubernetes Core](./2.4_Kubernetes_Core/) | 2 weeks | Pods, Deployments, Services, Ingress (Thành phần cốt lõi K8s) |
| 2.5 | [Monitoring & Logging](./2.5_Monitoring_Logging/) | 1-2 weeks | Prometheus, Grafana, ELK Stack (Giám sát & Ghi log) |
| 2.6 | [**Capstone Project**](./2.6_Capstone_Project/) | 1 week | 🎯 Microservices on Kubernetes (Microservices trên K8s) |

---

## 🗓️ Suggested Schedule (Lịch Trình Đề Xuất)

### Week 1: Docker Advanced

```
Day 1-2: Multi-stage builds, build optimization (Tối ưu build đa tầng)
Day 3-4: Docker networking deep dive (Chuyên sâu mạng Docker)
Day 5-7: Security best practices, scanning (Bảo mật & quét lỗ hổng)
```

### Week 2: Docker Compose

```
Day 1-2: Compose fundamentals, services (Cơ bản về Compose)
Day 3-4: Networking, volumes, dependencies (Mạng, ổ đĩa, phụ thuộc)
Day 5-7: Environment management, overrides (Quản lý môi trường)
```

### Week 3-4: Jenkins

```
Week 3: Jenkins setup, basic pipelines (Cài đặt & pipeline cơ bản)
Week 4: Advanced pipelines, shared libraries, agents (Pipeline nâng cao)
```

### Week 5-6: Kubernetes Core

```
Week 5: K8s architecture, Pods, Deployments (Kiến trúc K8s)
Week 6: Services, Ingress, ConfigMaps, Secrets (Mạng & Cấu hình)
```

### Week 7: Monitoring & Logging

```
Day 1-3: Prometheus setup, metrics collection (Cài đặt Prometheus)
Day 4-5: Grafana dashboards (Biểu đồ Grafana)
Day 6-7: ELK Stack, log aggregation (Tập trung log với ELK)
```

### Week 8: Capstone Project

```
Day 1-2: Architecture design (Thiết kế kiến trúc)
Day 3-5: Implementation (Triển khai)
Day 6-7: Testing, documentation (Kiểm thử & tài liệu)
```

---

## 🛠️ Tools Used (Công cụ sử dụng)

| Tool | Purpose (Mục đích) | Documentation |
|------|-------------------|---------------|
| **Docker Compose** | Multi-container orchestration (Điều phối đa container) | [docs.docker.com](https://docs.docker.com/compose/) |
| **Jenkins** | CI/CD automation server (Máy chủ tự động hóa CI/CD) | [jenkins.io](https://www.jenkins.io/doc/) |
| **Kubernetes** | Container orchestration (Điều phối container quy mô lớn) | [kubernetes.io](https://kubernetes.io/docs/) |
| **Minikube/Kind** | Local K8s cluster (Cluster K8s cục bộ) | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/) |
| **kubectl** | K8s CLI (Công cụ dòng lệnh K8s) | [kubernetes.io/docs/reference/kubectl](https://kubernetes.io/docs/reference/kubectl/) |
| **Prometheus** | Metrics & alerting (Thu thập chỉ số & cảnh báo) | [prometheus.io](https://prometheus.io/docs/) |
| **Grafana** | Visualization (Trực quan hóa dữ liệu) | [grafana.com](https://grafana.com/docs/) |
| **Elasticsearch** | Log storage (Lưu trữ log) | [elastic.co](https://www.elastic.co/guide/) |
| **Fluentd/Filebeat** | Log collection (Thu thập log) | [fluentd.org](https://docs.fluentd.org/) |
| **Kibana** | Log visualization (Giao diện xem log) | [elastic.co](https://www.elastic.co/guide/en/kibana/) |

---

## 🎯 Capstone Project Preview (Xem trước Dự án Capstone)

### **Microservices Deployment on Kubernetes (Triển khai Microservices trên Kubernetes)**

At the end of this track, you will deploy a complete microservices application with CI/CD and monitoring.

*Cuối Track này, bạn sẽ deploy ứng dụng microservices hoàn chỉnh với CI/CD và monitoring.*

You will build (Bạn sẽ xây dựng):

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                        Ingress Controller                     │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               │                                     │
│         ┌─────────────────────┼─────────────────────┐              │
│         │                     │                     │              │
│         ▼                     ▼                     ▼              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│  │  Frontend   │      │   API       │      │   Auth      │        │
│  │  Service    │ ───▶ │   Gateway   │ ───▶ │   Service   │        │
│  └─────────────┘      └─────────────┘      └─────────────┘        │
│                               │                                     │
│         ┌─────────────────────┼─────────────────────┐              │
│         │                     │                     │              │
│         ▼                     ▼                     ▼              │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│  │   User      │      │   Product   │      │   Order     │        │
│  │   Service   │      │   Service   │      │   Service   │        │
│  └─────────────┘      └─────────────┘      └─────────────┘        │
│         │                     │                     │              │
│         └─────────────────────┼─────────────────────┘              │
│                               ▼                                     │
│                      ┌─────────────┐                               │
│                      │  Database   │                               │
│                      │  (MongoDB)  │                               │
│                      └─────────────┘                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │           Monitoring Stack (Prometheus + Grafana)            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Features (Tính năng)

- 🔄 **CI/CD Pipeline** with Jenkins (với Jenkins)
- 🐳 **Containerized** microservices
- ☸️ **Kubernetes** deployment
- 📊 **Monitoring** with Prometheus & Grafana (với Prometheus & Grafana)
- 📝 **Logging** with ELK Stack (với ELK Stack)
- 🔐 **Secrets management** with K8s Secrets (với K8s Secrets)

👉 **[View Capstone Details →](./2.6_Capstone_Project/)** | **[Xem chi tiết →](./2.6_Capstone_Project/)**

---

## 📊 Evaluation (Đánh Giá)

### Module Completion Criteria (Tiêu chí hoàn thành Module)

| Criteria | Requirement |
|----------|-------------|
| Labs | Complete 100% hands-on labs (Hoàn thành 100% bài thực hành) |
| Quiz | Score ≥ 70% (Đạt ≥ 70% điểm quiz) |
| Exercises | Complete ≥ 80% exercises (Hoàn thành ≥ 80% bài tập) |
| Project | Submit and get reviewed (Submit và được review) |

### Track Completion Criteria (Tiêu chí hoàn thành Track)

- ✅ Complete all 5 modules (Hoàn thành tất cả 5 modules)
- ✅ Submit Capstone Project
- ✅ Demo microservices running on K8s

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [Track 1: Foundation](../Track1_Foundation_StaticWeb/) | **Track 2** | [Track 3: Cloud](../Track3_Cloud_Network_Design/) |

---

## 📖 Getting Started (Bắt Đầu)

```bash
# Start with Module 2.1 (Bắt đầu với Module 2.1)
cd 2.1_Docker_Advanced
cat README.md
```

**📚 Start learning:** [2.1 Docker Advanced →](./2.1_Docker_Advanced/)

---

<div align="center">

**🚀 Level up your DevOps skills! 🚀**

*Nâng cao kỹ năng DevOps của bạn!*

</div>
