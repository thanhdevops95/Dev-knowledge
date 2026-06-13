# 🔧 Configuration Management — Ansible & quản lý cấu hình hệ thống

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 13/06/2026

> 🎯 *Configuration Management (Quản lý cấu hình) là phương pháp tự động hoá việc cài đặt + cấu hình phần mềm trên hàng loạt máy chủ, bảo đảm chúng luôn ở trạng thái mong muốn (desired state) — chống config drift và "snowflake server". Trọng tâm là **Ansible** (agentless, dùng SSH + YAML), cùng góc nhìn so sánh với Chef/Puppet/Salt và cách kết hợp với IaC.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu vì sao cần CM: config drift, snowflake server, và khái niệm cốt lõi **idempotency**
- [x] Phân biệt mô hình **Push vs Pull**, **mutable vs immutable**, và vị trí của CM so với IaC + Container
- [x] Làm chủ **Ansible**: inventory, ad-hoc command, playbook, module, idempotency
- [x] Viết **playbook + roles** tái sử dụng với biến, Jinja2 template, handlers
- [x] Quản lý secret an toàn bằng **Ansible Vault**
- [x] So sánh Ansible/Chef/Puppet/Salt và biết khi nào dùng cái nào, kết hợp với Terraform/Packer
- [x] (Intermediate) **Dynamic inventory** cho cloud, tối ưu hiệu năng + error handling, **testing với Molecule**, vận hành quy mô lớn với **AWX/AAP**

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng Ansible (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Configuration Management là gì`](./lessons/01_basic/00_what-is-configuration-management.md) | 🌱 Intro | ✅ | CM là gì, 3 căn bệnh (config drift / snowflake / "works on my machine"), idempotency, Push vs Pull, mutable vs immutable, landscape 4 tool, CM vs IaC vs Container. |
| **01** | [`Ansible Basics`](./lessons/01_basic/01_ansible-basics.md) | 🌳 Lesson | ✅ | Agentless (SSH + Python), inventory (static/group_vars), ad-hoc command, playbook đầu tiên, module phổ biến, idempotency demo. |
| **02** | [`Playbooks & Roles`](./lessons/01_basic/02_playbooks-and-roles.md) | 🌳 Lesson | ✅ | Cấu trúc playbook (tasks/handlers/notify), biến + precedence, facts, Jinja2 template, đóng gói thành role tái sử dụng. |
| **03** | [`Ansible Vault & Secrets`](./lessons/01_basic/03_vault-and-secrets.md) | 🌳 Lesson | ✅ | Mã hoá biến nhạy cảm với `ansible-vault`, vault trong CI/CD, best practice quản lý secret. |
| **04** | [`Alternatives & When-Which`](./lessons/01_basic/04_alternatives-and-when-which.md) | 🌳 Lesson | ✅ | So sánh Ansible/Chef/Puppet/Salt, mutable vs immutable, kết hợp CM + IaC (Terraform/Packer), CM trong thế giới container. |

### 📖 Lộ trình Intermediate — Quy mô Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ | Thách thức khi quản lý CM ở quy mô hàng trăm node: dynamic infra, hiệu năng, testing, secrets at scale. |
| **01** | [`Dynamic Inventory & Cloud`](./lessons/02_intermediate/01_dynamic-inventory-and-cloud.md) | 🌳 Lesson | ✅ | Inventory plugin cho AWS/GCP, gom node theo tag, thay thế inventory tĩnh trong môi trường co giãn. |
| **02** | [`Advanced Playbooks & Strategies`](./lessons/02_intermediate/02_advanced-playbooks-and-strategies.md) | 🌳 Lesson | ✅ | Tối ưu hiệu năng (forks, pipelining, strategy), error handling (block/rescue/always), rolling update (`serial`), delegation. |
| **03** | [`Testing với Molecule`](./lessons/02_intermediate/03_testing-with-molecule.md) | 🌳 Lesson | ✅ | `ansible-lint` + `yamllint`, test role với **Molecule** (Docker), kiểm tra idempotence, tích hợp CI. |
| **04** | [`AWX/AAP & vận hành quy mô lớn`](./lessons/02_intermediate/04_awx-aap-and-at-scale.md) | 🌳 Lesson | ✅ | **AWX/Ansible Automation Platform** (UI, RBAC, schedule), external secret manager, `ansible-pull`, kết hợp CM + IaC + immutable. |

> ✅ Cụm hoàn chỉnh Basic 5/5 + Intermediate 5/5 (đợt hoàn thiện nhánh DevOps, 06/2026).

---

## 🚀 Lộ trình đề xuất

- **Beginner:** Đọc [Bài 00](./lessons/01_basic/00_what-is-configuration-management.md) để nắm khái niệm + idempotency, rồi thực hành ngay [Ansible Basics](./lessons/01_basic/01_ansible-basics.md) trên 1 VM (cài Nginx). Sau đó nâng lên [Playbooks & Roles](./lessons/01_basic/02_playbooks-and-roles.md) để biết tái sử dụng code, và [Vault](./lessons/01_basic/03_vault-and-secrets.md) để xử lý secret.
- **Intermediate:** Khi quản lý nhiều node trên cloud, học [Dynamic Inventory](./lessons/02_intermediate/01_dynamic-inventory-and-cloud.md); cần deploy zero-downtime + tối ưu thì xem [Advanced Playbooks](./lessons/02_intermediate/02_advanced-playbooks-and-strategies.md); muốn role đáng tin cậy thì [test với Molecule](./lessons/02_intermediate/03_testing-with-molecule.md).

## 🔗 Liên kết cụm liên quan

- [IaC (Terraform)](../iac/) — Terraform **tạo** hạ tầng, Ansible **cấu hình** bên trong; thường kết hợp.
- [Docker](../docker/) & [Kubernetes](../kubernetes/) — hướng immutable/container, giảm (nhưng không xoá) vai trò CM.
- [CI/CD](../ci-cd/) — chạy playbook tự động trong pipeline.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (13/06/2026)** — Hoàn thiện cụm **Basic 5/5** (CM concepts + Ansible basics/playbooks-roles/vault/alternatives). Bổ sung lộ trình Intermediate (đang biên soạn).
- **v1.1.0 (14/06/2026)** — Hoàn thiện cụm **Intermediate 5/5** (overview + dynamic inventory + advanced playbooks/strategies + testing với Molecule + AWX/AAP & scale). Cụm configuration-management hoàn chỉnh.
