# ☁️ GCP (Google Cloud Platform)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Cụm Basic hoàn chỉnh (5/5 bài)

> 🎯 *Google Cloud Platform (GCP) là nhà cung cấp đám mây lớn thứ ba thế giới, nắm khoảng 11% thị phần (Q1 2026), mạnh nhất ở mảng dữ liệu, AI và hạ tầng mạng. Cụm Basic tập trung vào 5 dịch vụ cốt lõi — Compute Engine, Cloud Storage, Cloud SQL, Firestore và Cloud Run — đủ phủ ~95% workload thực tế. Học xong, bạn sẽ tự deploy được một ứng dụng nhỏ lên GCP.*

---

## 🚀 Bắt đầu nhanh

Bạn đang tìm câu trả lời cho vấn đề nào? Chọn nhanh theo nhu cầu rồi nhảy thẳng vào bài tương ứng:

- **GCP là gì, tạo tài khoản và cấu hình ban đầu thế nào?** → [GCP — Tổng quan + account setup + gcloud CLI](lessons/01_basic/00_what-is-gcp-overview.md).
- **Dựng máy chủ ảo Compute Engine và quản lý ổ đĩa Persistent Disk?** → [GCP Compute Engine + Persistent Disks](lessons/01_basic/01_compute-engine-and-disks.md).
- **Lưu trữ file trên Cloud Storage và phân quyền bằng IAM?** → [GCP Cloud Storage + IAM](lessons/01_basic/02_cloud-storage-and-iam.md).
- **Dùng cơ sở dữ liệu được quản lý sẵn (Cloud SQL và Firestore)?** → [GCP Cloud SQL + Firestore](lessons/01_basic/03_cloud-sql-and-firestore.md).
- **Chạy code không cần máy chủ (serverless) với Cloud Functions, Cloud Run và API Gateway?** → [GCP Cloud Functions + Cloud Run + API Gateway](lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md).

---

## 📖 Lessons — Cụm Basic (5 bài)

Năm bài dưới đây đi theo trình tự một dự án thực tế: hiểu tổng quan GCP, dựng máy chủ và ổ đĩa, lưu trữ và phân quyền, gắn cơ sở dữ liệu, rồi chuyển sang mô hình serverless. Cả 5 đều là nền móng cho mọi kiến trúc trên GCP.

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [GCP — Tổng quan + account setup + gcloud CLI](lessons/01_basic/00_what-is-gcp-overview.md) | Cấu trúc Org/Folder/Project, gcloud CLI, IAM và Free Tier |
| 01 | [GCP Compute Engine + Persistent Disks](lessons/01_basic/01_compute-engine-and-disks.md) | Loại máy (machine type), MIG, Live Migration và Spot VM |
| 02 | [GCP Cloud Storage + IAM](lessons/01_basic/02_cloud-storage-and-iam.md) | Storage class, signed URL, vòng đời (lifecycle) và CMEK |
| 03 | [GCP Cloud SQL + Firestore](lessons/01_basic/03_cloud-sql-and-firestore.md) | HA, read replica, Auth Proxy và Security Rules |
| 04 | [GCP Cloud Functions + Cloud Run + API Gateway](lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) | Gen2, scale-to-zero, cold start và traffic split |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [11_cloud](../README.md) — trang tổng của mảng điện toán đám mây.
- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../cloud-fundamentals/) — các khái niệm chung (region, AZ, mô hình dịch vụ) áp dụng cho mọi nhà cung cấp.

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **Nhà cung cấp khác:** [AWS](../aws/) và [Azure](../azure/) — hai vendor lớn còn lại, đối chiếu dịch vụ tương đương với GCP.
- 🏗️ **Tự động hoá hạ tầng:** [IaC — Infrastructure as Code](../../10_devops/iac/) — dựng tài nguyên GCP bằng code thay vì click tay trên Console.
- ☸️ **Điều phối container:** [Kubernetes — Container Orchestration Platform](../../10_devops/kubernetes/) — bối cảnh cho dịch vụ GKE (Kubernetes được quản lý trên GCP).

### 🌐 Tài nguyên tham khảo khác

- [Trang tài liệu chính thức của GCP](https://cloud.google.com/docs) — nguồn tham khảo gốc đầy đủ nhất.
- [Cloud Skills Boost](https://www.cloudskillsboost.google/) — nền tảng học và luyện thi chứng chỉ chính thức của Google Cloud.
- [GCP Free Tier](https://cloud.google.com/free) — chương trình dùng thử và gói miễn phí của Google Cloud.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. GCP vendor-specific cluster thứ hai của 11_cloud (sau AWS). GCP-specific: Live Migration, IAP, Firestore Security Rules, Cloud Run scale-to-zero.
- **v2.0.0 (01/06/2026)** — Việt hoá block 🎯 và mục Bắt đầu nhanh; bỏ cột "Thời lượng" + cụm "~103 phút đọc" (field thời lượng đã loại toàn kho); đổi field "Status" → "Trạng thái"; chuẩn hoá link-text = tiêu đề H1 thực của bài đích; tái cấu trúc mục Liên kết theo 3 sub chuẩn (🧭 Định hướng lộ trình học / 🧩 Các chủ đề có thể bạn quan tâm / 🌐 Tài nguyên tham khảo khác).
