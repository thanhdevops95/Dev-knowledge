# ☁️ Azure

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Cụm Basic hoàn chỉnh (5/5 bài)

> 🎯 *Microsoft Azure là nhà cung cấp đám mây lớn thứ hai thế giới, nắm khoảng 24% thị phần (Q1 2026). Đây là lựa chọn mạnh nhất trong môi trường doanh nghiệp (*enterprise*), đặc biệt khi hệ thống đã gắn chặt với Windows và hệ sinh thái Microsoft (Active Directory, Office 365, SQL Server). Cụm Basic dẫn bạn đi qua những dịch vụ nền tảng — Virtual Machines, Blob Storage, Azure SQL, Functions — đủ để tự dựng và triển khai một ứng dụng nhỏ trên Azure.*

---

## 🚀 Bắt đầu nhanh

Bạn đang cần giải quyết vấn đề nào? Chọn nhanh theo nhu cầu rồi nhảy thẳng vào bài tương ứng:

- **Azure là gì, tạo tài khoản và cấu hình ban đầu thế nào?** → [Azure — Tổng quan + account setup + az CLI](lessons/01_basic/00_what-is-azure-overview.md).
- **Dựng máy chủ ảo (Virtual Machine) đầu tiên và gắn ổ đĩa cho nó?** → [Azure VM + Managed Disks — Compute foundation](lessons/01_basic/01_virtual-machines-and-disks.md).
- **Lưu trữ file trên Blob Storage và phân quyền truy cập bằng RBAC?** → [Azure Blob Storage + RBAC](lessons/01_basic/02_blob-storage-and-rbac.md).
- **Dùng cơ sở dữ liệu được quản lý sẵn (Azure SQL và Cosmos DB)?** → [Azure SQL + Cosmos DB](lessons/01_basic/03_azure-sql-and-cosmosdb.md).
- **Chạy code không cần máy chủ (serverless) với Functions và App Service?** → [Azure Functions + App Service + Container Apps](lessons/01_basic/04_functions-and-app-service.md).

---

## 📖 Lessons — Cụm Basic (5 bài)

Năm bài dưới đây đi theo trình tự một dự án thực tế: hiểu cách Azure tổ chức tài nguyên, dựng máy chủ và ổ đĩa, lưu trữ file và phân quyền, gắn cơ sở dữ liệu, rồi chuyển sang mô hình serverless. Cả 5 đều là nền móng cho mọi kiến trúc trên Azure.

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [Azure — Tổng quan + account setup + az CLI](lessons/01_basic/00_what-is-azure-overview.md) | Cách phân cấp tài nguyên (Subscription, Management Group, Resource Group), công cụ `az` CLI và định danh Entra ID |
| 01 | [Azure VM + Managed Disks — Compute foundation](lessons/01_basic/01_virtual-machines-and-disks.md) | Các dòng máy ảo (B/D/E/F series), Managed Disks, nhân bản tự động bằng VMSS và ưu đãi Hybrid Benefit |
| 02 | [Azure Blob Storage + RBAC](lessons/01_basic/02_blob-storage-and-rbac.md) | Tầng lưu trữ (access tier), vòng đời (lifecycle), link tải có thời hạn (SAS), phân quyền RBAC/ABAC và mã hoá CMK |
| 03 | [Azure SQL + Cosmos DB](lessons/01_basic/03_azure-sql-and-cosmosdb.md) | Mô hình giá DTU/vCore, Hyperscale, Cosmos DB đa giao diện (multi-API) và các mức nhất quán (consistency) |
| 04 | [Azure Functions + App Service + Container Apps](lessons/01_basic/04_functions-and-app-service.md) | Các gói Consumption/Premium, Durable Functions, Container Apps và cổng API (APIM) |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [11_cloud](../README.md) — trang tổng của mảng điện toán đám mây.
- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../cloud-fundamentals/) — các khái niệm chung (region, AZ, mô hình dịch vụ) áp dụng cho mọi nhà cung cấp.

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **So sánh nhà cung cấp khác:** [AWS](../aws/) và [GCP](../gcp/) — đối chiếu dịch vụ tương đương để hiểu Azure đứng ở đâu.
- 🏗️ **Tự động hoá hạ tầng:** [IaC — Infrastructure as Code](../../10_devops/iac/) — dựng tài nguyên Azure bằng code (Terraform có provider riêng cho Azure) thay vì click tay trên Portal.
- ☸️ **Điều phối container:** [Kubernetes — Container Orchestration Platform](../../10_devops/kubernetes/) — bối cảnh cho dịch vụ AKS (Kubernetes được quản lý trên Azure).

### 🌐 Tài nguyên tham khảo khác

- [Trang tài liệu chính thức của Azure](https://learn.microsoft.com/azure/) — nguồn tham khảo gốc đầy đủ nhất.
- [Microsoft Learn](https://learn.microsoft.com/training/) — nền tảng học và luyện thi chứng chỉ chính thức của Microsoft.
- [Tài khoản Azure miễn phí](https://azure.microsoft.com/free/) — đăng ký để có credit dùng thử và các dịch vụ luôn-miễn-phí.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Azure-specific: Entra ID, Hybrid Benefit, Cosmos DB multi-API, Container Apps Knative.
- **v2.0.0 (01/06/2026)** — Việt hoá narrative toàn bộ prose (block 🎯, mục Bắt đầu nhanh, mô tả bảng Lessons); bỏ cột "Thời lượng" + cụm "~103 phút đọc" (field thời lượng đã loại toàn kho); đổi field "Status" → "Trạng thái"; chuẩn hoá link-text = tiêu đề H1 thực của bài đích; tái cấu trúc mục Liên kết theo 3 sub chuẩn (🧭 Định hướng lộ trình học / 🧩 Các chủ đề có thể bạn quan tâm / 🌐 Tài nguyên tham khảo khác) để đồng bộ với cụm AWS.
