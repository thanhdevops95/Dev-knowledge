# ✏️ _BaiTap - Bài Tập & Exercises

---

## 📋 Mô Tả

Thư mục này chứa **các bài tập, exercises, và solutions** từ nhiều nguồn. Dùng để **tham khảo khi viết bài tập** cho DevOps-Journey.

---

## 📁 Cấu Trúc

```
_BaiTap/
├── DevOps-1_Exercises/       # Exercises theo lessons (55 items)
│   ├── Exercises01-foundation/
│   ├── Exercises02-scm-and-ci/
│   ├── Exercises03-containerization-and-orchestration/
│   ├── Exercises04-cm-and-iac/
│   ├── Exercises05-monitoring-logging-alerting/
│   ├── Exercises06-cloud-platforms/
│   └── Final-project/
│
└── Devops-Exercises/         # Bộ exercises lớn (345 items)
    ├── topics/               # Bài tập theo chủ đề
    ├── certificates/         # Tài liệu chứng chỉ
    ├── coding/               # Bài tập coding (Python)
    ├── scripts/              # Scripts hỗ trợ
    └── tests/                # Unit tests
```

---

## 📚 Chi Tiết Từng Nguồn

### 📘 DevOps-1_Exercises

**Đặc điểm:** Exercises theo từng lesson, mỗi bài có file `SOLUTION.md`.

| Thư mục | Nội dung |
|---------|----------|
| `Exercises01-foundation/` | What is DevOps, Linux CLI, Scripting, Networking |
| `Exercises02-scm-and-ci/` | Git Version Control, CI/CD Theory |
| `Exercises03-containerization-and-orchestration/` | Docker, Kubernetes |
| `Exercises04-cm-and-iac/` | Ansible, Terraform |
| `Exercises05-monitoring-logging-alerting/` | Prometheus/Grafana, EFK |
| `Exercises06-cloud-platforms/` | AWS Core Services |
| `Final-project/` | Dự án tổng hợp |

**Cấu trúc mỗi exercise:**

```
XX-topic/
├── SOLUTION.md    # Đáp án và hướng dẫn
└── (các file bổ sung nếu có)
```

---

### 📗 Devops-Exercises

**Đặc điểm:** Bộ exercises **RẤT LỚN** với 345+ items, được tổ chức theo topics.

#### Topics chính

| Topic | Số câu hỏi | Mô tả |
|-------|------------|-------|
| `aws/` | Nhiều | EC2, S3, VPC, IAM... |
| `azure/` | Nhiều | Azure services |
| `containers/` | Nhiều | Docker, containerd |
| `kubernetes/` | Nhiều | K8s concepts, kubectl |
| `git/` | Nhiều | Git commands, workflows |
| `linux/` | Nhiều | Commands, permissions, processes |
| `shell/` | Nhiều | Bash scripting |
| `python/` | Nhiều | Python for DevOps |
| `cicd/` | Nhiều | CI/CD concepts |
| `openshift/` | Nhiều | OpenShift specific |
| `prometheus/` | Nhiều | Monitoring |
| `terraform/` | Nhiều | IaC |
| `ansible/` | Nhiều | Configuration management |

#### Files đáng chú ý

| File | Mô tả | Kích thước |
|------|-------|------------|
| `README.md` | Tổng hợp câu hỏi (184KB) | **RẤT LỚN** |
| `README.vi.md` | Phiên bản tiếng Việt (16KB) | Có sẵn tiếng Việt |
| `FAQ.vi.md` | FAQ tiếng Việt | Có sẵn tiếng Việt |
| `prepare_for_interview.md` | Chuẩn bị phỏng vấn | Hữu ích |

---

## 🔍 Cách Sử Dụng

### Khi cần tham khảo câu hỏi theo topic

```bash
# Xem câu hỏi Linux
open Devops-Exercises/topics/linux/

# Xem câu hỏi Docker
open Devops-Exercises/topics/containers/

# Xem câu hỏi Kubernetes
open Devops-Exercises/topics/kubernetes/
```

### Khi cần xem đáp án

```bash
# Đáp án từ DevOps-1
open DevOps-1_Exercises/Exercises01-foundation/02-linux-cli/SOLUTION.md
```

### Khi cần câu hỏi tiếng Việt

```bash
open Devops-Exercises/README.vi.md
open Devops-Exercises/FAQ.vi.md
```

---

## ⭐ Khuyến Nghị

| Mục đích | Tham khảo |
|----------|-----------|
| Viết QUIZ.md | `Devops-Exercises/README.md` - Nhiều câu hỏi mẫu |
| Viết EXERCISES.md | `DevOps-1_Exercises/` - Có solutions |
| Scenarios thực tế | `Devops-Exercises/topics/` - Theo topic |
| Câu hỏi phỏng vấn | `Devops-Exercises/prepare_for_interview.md` |

---

## 📊 Thống Kê

| Nguồn | Số items | Có solution |
|-------|----------|-------------|
| DevOps-1_Exercises | 55 | ✅ Có |
| Devops-Exercises | 345+ | Một phần |

---

*Cập nhật: 2025-12-28*
