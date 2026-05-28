# 🏆 Module 2.6: Capstone Project

> **Microservices on Kubernetes with CI/CD and Monitoring**
>
> *Microservices trên Kubernetes với CI/CD và Monitoring*

---

## 🎯 Project Overview (Tổng quan dự án)

Combine all Track 2 knowledge to deploy a production-ready microservices platform.

*Tổng hợp tất cả kiến thức Track 2 để deploy nền tảng microservices production-ready.*

---

## 📋 Requirements (Yêu cầu)

### Architecture (Kiến trúc)

```
┌──────────────────────────────────────────────────────────────┐
│                         Kubernetes                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │
│  │  Frontend   │  │  API Gateway│  │   Backend Services  │   │
│  │  (React)    │──│   (NGINX)   │──│  - Auth Service     │   │
│  └─────────────┘  └─────────────┘  │  - User Service     │   │
│                                    │  - Order Service    │   │
│                                    └─────────────────────┘   │
│                                              │                │
│                    ┌─────────────────────────┼───────┐       │
│                    │                         │       │       │
│              ┌─────▼─────┐  ┌───────────┐  ┌─▼───┐          │
│              │ PostgreSQL│  │   Redis   │  │ RabbitMQ       │
│              └───────────┘  └───────────┘  └─────┘          │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Monitoring Stack                        │    │
│  │  Prometheus │ Grafana │ Loki │ Alertmanager         │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
                               │
                     ┌─────────▼─────────┐
                     │  GitLab CI / Jenkins │
                     └───────────────────┘
```

---

### Deliverables (Sản phẩm bàn giao)

#### 1. Application - Docker Images (Ứng dụng)

- [ ] Frontend container (< 50MB) - multi-stage build
- [ ] Backend services with multi-stage builds (Backend với multi-stage builds)
- [ ] All images pushed to GitLab Container Registry (Tất cả images đã push lên registry)

#### 2. Kubernetes Manifests

- [ ] Deployments with health checks (Deployments với health checks)
- [ ] Services (ClusterIP, LoadBalancer)
- [ ] ConfigMaps & Secrets
- [ ] PersistentVolumeClaims
- [ ] HorizontalPodAutoscaler
- [ ] Ingress configuration (Cấu hình Ingress)

#### 3. CI/CD Pipeline

> Choose GitLab CI (recommended) or Jenkins (Chọn GitLab CI (khuyến nghị) hoặc Jenkins)

**GitLab CI Example:**

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  REGISTRY: $CI_REGISTRY
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA

test:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm test

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $REGISTRY/frontend:$IMAGE_TAG ./apps/frontend
    - docker push $REGISTRY/frontend:$IMAGE_TAG

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -k k8s/staging/
  environment:
    name: staging
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -k k8s/production/
  environment:
    name: production
  when: manual
  only:
    - main
```

**Requirements (Yêu cầu CI/CD):**

- [ ] Automated testing (Test tự động)
- [ ] Docker build & push (Build và push Docker)
- [ ] Kubernetes deployment (Deploy lên Kubernetes)
- [ ] Staging/Production environments (Môi trường Staging/Production)
- [ ] Rollback capability (Khả năng rollback)

#### 4. Monitoring (Giám sát)

- [ ] Prometheus scraping all services
- [ ] Grafana dashboards (minimum 3) (Tối thiểu 3 dashboard):
  - Kubernetes cluster overview
  - Application metrics (Request rate, latency, errors)
  - Infrastructure metrics (CPU, Memory, Disk)
- [ ] Alert rules configured (Đã cấu hình cảnh báo)
- [ ] Logging with Loki or ELK (Logging với Loki hoặc ELK)

---

## 📁 Project Structure (Cấu trúc dự án)

```
capstone-project/
├── apps/
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── src/
│   ├── auth-service/
│   │   ├── Dockerfile
│   │   └── src/
│   └── user-service/
│       ├── Dockerfile
│       └── src/
├── k8s/
│   ├── base/
│   │   ├── deployments/
│   │   ├── services/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   └── dashboards/
│   └── alertmanager/
│       └── alertmanager.yml
├── .gitlab-ci.yml          # GitLab CI (Primary)
├── Jenkinsfile             # Jenkins (Alternative)
└── README.md
```

---

## ✅ Acceptance Criteria (Tiêu chí chấp nhận)

| Requirement (Yêu cầu) | Weight (Trọng số) |
|-----------------------|-------------------|
| All services running on K8s (Tất cả services chạy trên K8s) | 25% |
| CI/CD pipeline working (Pipeline CI/CD hoạt động) | 25% |
| Monitoring stack (Stack giám sát) | 20% |
| Documentation (Tài liệu) | 15% |
| Security best practices (Bảo mật) | 15% |

---

## 📊 Evaluation (Đánh giá)

| Grade (Xếp loại) | Score (Điểm) |
|------------------|--------------|
| Excellent (Xuất sắc) | 90-100% |
| Good (Tốt) | 75-89% |
| Pass (Đạt) | 60-74% |
| Fail (Không đạt) | < 60% |

---

## 🚀 Getting Started (Bắt đầu)

1. Setup Kubernetes cluster - minikube/kind (Thiết lập cluster Kubernetes)
2. Create GitLab project with Container Registry enabled (Tạo project GitLab với Container Registry)
3. Deploy base infrastructure - databases, queues (Deploy hạ tầng cơ bản)
4. Build and deploy applications (Build và deploy ứng dụng)
5. Setup CI/CD pipeline (Thiết lập pipeline CI/CD)
6. Configure monitoring stack (Cấu hình stack giám sát)
7. Document everything (Viết tài liệu)

---

## 📖 Resources (Tài liệu tham khảo)

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Prometheus + Grafana Setup](https://prometheus.io/docs/)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [2.5 Monitoring](../2.5_Monitoring_Logging/) | **2.6 Capstone** | [Track 3](../../Track3_Cloud_Network_Design/) |

---

**Good luck with your capstone! 🏆**

*Chúc may mắn với dự án tổng hợp!*

</div>
