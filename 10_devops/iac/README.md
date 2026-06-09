# 🏗️ IaC — Infrastructure as Code

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 26/05/2026

> 🎯 *Infrastructure as Code (Quản lý hạ tầng bằng code) định nghĩa toàn bộ tài nguyên hệ thống (máy chủ, mạng, cơ sở dữ liệu) dưới dạng mã nguồn. Giúp loại bỏ hoàn toàn việc click tay thủ công, bảo đảm hạ tầng có thể tái tạo nhanh chóng, nhất quán và quản lý phiên bản qua Git.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu triết lý IaC, mô hình Declarative vs Imperative và các công cụ trong hệ sinh thái
- [x] Làm chủ cú pháp **HCL (HashiCorp Configuration Language)**, viết code provisioning hạ tầng cloud
- [x] Quản lý an toàn file trạng thái (**Terraform State**) và thiết lập Remote Backend (S3 + DynamoDB) để làm việc nhóm
- [x] Thiết kế hạ tầng tái sử dụng thông qua cách đóng gói và versioning **Terraform Modules**
- [x] Áp dụng các quy trình bảo mật (tfsec, checkov) và dự toán chi phí tài nguyên (Infracost)
- [x] Sử dụng **Terragrunt** để giữ code DRY (Don't Repeat Yourself) khi quản lý multi-environment
- [x] Thiết lập workflow GitOps cho hạ tầng bằng cách triển khai tự động **Atlantis** thông qua Pull Request
- [x] Xử lý sự cố lệch cấu hình (State Drift) và import tài nguyên có sẵn một cách an toàn
- [x] Có góc nhìn so sánh sâu sắc với các giải pháp thay thế: Pulumi, AWS CDK, CDKTF, và Crossplane

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng Terraform (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`What is IaC`](./lessons/01_basic/00_what-is-iac.md) | 🌱 Intro | ✅ 🌟 | IaC là gì, tại sao cần, phân biệt Declarative vs Imperative, tổng quan các công cụ chính 2026. |
| **01** | [`Terraform Basics`](./lessons/01_basic/01_terraform-basics.md) | 🌳 Lesson | ✅ 🌟 | Làm chủ cú pháp HCL: providers, resources, data sources, variables, outputs, locals và lifecycle. |
| **02** | [`State & Backend`](./lessons/01_basic/02_state-and-backend.md) | 🌳 Lesson | ✅ 🌟 | State file là gì, cấu hình Remote Backend (S3 + DynamoDB locking) để tránh xung đột khi chạy chung. |
| **03** | [`Modules & Workspaces`](./lessons/01_basic/03_modules-and-workspaces.md) | 🌳 Lesson | ✅ 🌟 | Đóng gói code thành Modules tái sử dụng, truyền input/output, so sánh module local vs Git/Registry. |
| **04** | [`Best Practices & Alternatives`](./lessons/01_basic/04_best-practices-and-alternatives.md) | 🌳 Lesson | ✅ 🌟 | Security scanning (checkov, tfsec), tính cost (Infracost), tích hợp CI/CD và so sánh với Pulumi/CDK. |

### 📖 Lộ trình Intermediate — Quy trình chuyên sâu Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ 🌟 | Bức tranh tổng quát về các vấn đề phức tạp khi quản lý IaC ở quy mô doanh nghiệp lớn. |
| **01** | [`Terragrunt DRY Multi-Env`](./lessons/02_intermediate/01_terragrunt-dry-multi-env.md) | 🌳 Lesson | ✅ 🌟 | Sử dụng **Terragrunt** để giảm thiểu trùng lặp code khi quản lý 3 envs × 5 regions × 5 modules. |
| **02** | [`Atlantis GitOps for IaC`](./lessons/02_intermediate/02_atlantis-gitops-for-iac.md) | 🌳 Lesson | ✅ 🌟 | Tự động hóa chạy plan/apply trực tiếp trên Pull Request của GitHub/GitLab thông qua **Atlantis**. |
| **03** | [`State Advanced & Drift`](./lessons/02_intermediate/03_state-advanced-and-drift.md) | 🌳 Lesson | ✅ 🌟 | Xử lý lệch cấu hình thực tế (drift), đổi tên module, import tài nguyên có sẵn và phục hồi state lỗi. |
| **04** | [`Pulumi, CDK & Crossplane`](./lessons/02_intermediate/04_pulumi-cdk-crossplane.md) | 🌳 Lesson | ✅ 🌟 | Nghiên cứu sâu các phương án thay thế: Viết code hạ tầng bằng ngôn ngữ lập trình thật hoặc chạy K8s-native CRD. |

---

## 🚀 Lộ trình đề xuất

*   **Beginner:** Bắt đầu bằng việc thực hành viết code Terraform local tạo máy ảo trên AWS/GCP theo [Bài 01](./lessons/01_basic/01_terraform-basics.md), học cách lưu state ở [Bài 02](./lessons/01_basic/02_state-and-backend.md) rồi đóng gói module ở [Bài 03](./lessons/01_basic/03_modules-and-workspaces.md).
*   **Intermediate:** Khi phải quản lý nhiều môi trường (dev, staging, prod), hãy chuyển sang học **Terragrunt (Bài 01 intermediate)** để tránh lặp code, kết hợp setup **Atlantis (Bài 02 intermediate)** để thiết lập quy trình duyệt PR an toàn cho team.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
- **v1.0.0 (26/05/2026)** — Hoàn thiện mục lục chi tiết cho module Infrastructure as Code, kết nối đầy đủ các bài học Basic & Intermediate hiện có.
