# 🌐 Multi-cloud Strategies

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026

> 🎯 *Khi một hệ thống không còn đặt trọn niềm tin vào một nhà cung cấp đám mây duy nhất, bạn bước vào thế giới multi-cloud: dùng đồng thời nhiều cloud (AWS, GCP, Azure) để tránh phụ thuộc một vendor, tăng độ bền và tối ưu chi phí. Cụm bài này đi từ lý do nên (và không nên) làm multi-cloud, cách thoát khỏi vendor lock-in, cho tới cách nối mạng — danh tính — Kubernetes — disaster recovery xuyên nhiều cloud, kèm một case study di chuyển hệ thống từ AWS sang GCP.*

---

## 🚀 Bắt đầu nhanh

Nếu mới làm quen với chủ đề, bạn nên đọc tuần tự từ bài 00 để nắm bức tranh tổng thể trước khi đi vào từng mảng kỹ thuật.

- [Multi-cloud Overview — Định nghĩa, lý do, khi nên/không nên 2026](lessons/01_basic/00_what-is-multi-cloud-overview.md)
- [Vendor Lock-in & Portability — 4 chiều khoá, abstraction layer, exit cost](lessons/01_basic/01_vendor-lock-in-and-portability.md)
- [Cross-cloud Network & Identity — Transit, VPN, Federation, Vault sync](lessons/01_basic/02_multi-cloud-network-and-identity.md)
- [Kubernetes Multi-cloud — Anthos, Azure Arc, Cluster API, Service Mesh](lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md)
- [Multi-cloud — Disaster Recovery + Architecture Patterns](lessons/01_basic/04_disaster-recovery-and-architecture-patterns.md)

---

## 📖 Danh mục bài học — Cụm Basic

Năm bài dưới đây xây dựng theo mạch từ tư duy chiến lược tới kiến trúc thực thi. Mỗi bài tự đứng độc lập, nhưng đọc theo thứ tự sẽ liền mạch nhất.

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [Multi-cloud overview](lessons/01_basic/00_what-is-multi-cloud-overview.md) | Định nghĩa, lý do nên/không nên dùng multi-cloud, survey 2026 và các anti-pattern thường gặp |
| 01 | [Lock-in & Portability](lessons/01_basic/01_vendor-lock-in-and-portability.md) | Bốn chiều của vendor lock-in, abstraction layer giúp di động, và chi phí *egress fee* khi rời cloud |
| 02 | [Network & Identity](lessons/01_basic/02_multi-cloud-network-and-identity.md) | Nối mạng xuyên cloud bằng Transit Gateway, Megaport; đồng bộ danh tính qua Identity Federation và Vault |
| 03 | [Kubernetes Multi-cloud](lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md) | Lớp Kubernetes di động: Anthos, Azure Arc, EKS Anywhere, Cluster API và Karmada |
| 04 | [DR & Architecture Patterns](lessons/01_basic/04_disaster-recovery-and-architecture-patterns.md) | Bốn pattern disaster recovery, chỉ số RTO/RPO, lựa chọn native/portable/agnostic và case study AWS→GCP |

→ Phần thực hành (*hands-on*) trải dài khoảng **6–8 giờ** nếu bạn làm trọn vẹn các bài lab.

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [Cloud — Tổng quan các nền tảng đám mây](../README.md)
- ☁️ **Nền tảng từng vendor:** [AWS](../aws/), [GCP](../gcp/), [Azure](../azure/)

### 🧩 Các chủ đề có thể bạn quan tâm

- 💰 **Tối ưu chi phí:** [Cloud Cost Management](../cloud-cost-management/) — quản lý và cắt giảm chi phí khi chạy nhiều cloud
- 🏗️ **Hạ tầng dưới dạng code:** [IaC với Terraform](../../10_devops/iac/) — quản lý nhiều provider bằng một bộ cấu hình
- ☸️ **Điều phối container:** [Kubernetes (Intermediate)](../../10_devops/kubernetes/lessons/02_intermediate/) — nền tảng cho lớp Kubernetes di động
- 📊 **Vận hành & độ tin cậy:** [SRE Practices](../../10_devops/observability/lessons/02_intermediate/04_sre-practices.md) — RTO/RPO và quan sát hệ thống đa cloud

### 🌐 Tài nguyên tham khảo khác

- [Crossplane](https://www.crossplane.io/) — control plane mã nguồn mở để quản lý hạ tầng đa cloud bằng Kubernetes API.
- [Anthos](https://cloud.google.com/anthos) — nền tảng quản lý Kubernetes xuyên cloud của Google.
- [Azure Arc](https://azure.microsoft.com/services/azure-arc/) — đưa dịch vụ Azure ra mọi hạ tầng (on-prem, AWS, GCP).
- ↑ **Về cụm:** [Cluster API (CAPI)](https://cluster-api.sigs.k8s.io/) — chuẩn khai báo để dựng và vận hành cluster Kubernetes ở mọi nơi.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Strategic + architectural focus.
- **v1.1.0 (01/06/2026)** — Việt hoá dòng mô tả tổng quan cho người đọc; bỏ field Status và cột Thời lượng (loại bỏ ước tính thời gian đọc); chuẩn hoá phần Liên kết theo 3 sub-heading (Định hướng / Chủ đề liên quan / Tài nguyên khác) với link-text = tiêu đề bài thực.
