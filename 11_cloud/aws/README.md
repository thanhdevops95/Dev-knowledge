# ☁️ AWS

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Cụm Basic hoàn chỉnh (5/5 bài)

> 🎯 *Amazon Web Services (AWS) là nhà cung cấp đám mây lớn nhất thế giới, nắm khoảng 32% thị phần (Q1 2026). Cụm Basic tập trung vào 5 dịch vụ cốt lõi — EC2, S3, IAM, RDS, Lambda — đủ phủ ~95% workload thực tế. Học xong, bạn sẽ tự deploy được một ứng dụng production nhỏ lên AWS.*

---

## 🚀 Bắt đầu nhanh

Bạn đang tìm câu trả lời cho vấn đề nào? Chọn nhanh theo nhu cầu rồi nhảy thẳng vào bài tương ứng:

- **AWS là gì, tạo tài khoản và cấu hình ban đầu thế nào?** → [AWS Overview — Service landscape + Account setup 2026](lessons/01_basic/00_what-is-aws-overview.md).
- **Dựng máy chủ ảo EC2 đầu tiên và cho nó tự co giãn (auto-scale)?** → [EC2 + EBS — Compute foundation](lessons/01_basic/01_ec2-and-ebs-compute.md).
- **Lưu trữ file trên S3, phân quyền IAM và phát hành link tải có thời hạn (presigned URL)?** → [S3 deep + IAM fundamentals](lessons/01_basic/02_s3-deep-and-iam.md).
- **Dùng cơ sở dữ liệu được quản lý sẵn (RDS và DynamoDB)?** → [RDS + DynamoDB — Managed databases](lessons/01_basic/03_rds-and-dynamodb.md).
- **Chạy code không cần máy chủ (serverless) với Lambda và API Gateway?** → [Lambda + API Gateway — Serverless intro](lessons/01_basic/04_lambda-and-api-gateway.md).

---

## 📖 Lessons — Cụm Basic (5 bài)

Năm bài dưới đây đi theo trình tự một dự án thực tế: hiểu tổng quan AWS, dựng máy chủ, lưu trữ và phân quyền, gắn cơ sở dữ liệu, rồi chuyển sang mô hình serverless. Cả 5 đều được gắn tag MUST-KNOW vì là nền móng cho mọi kiến trúc trên AWS.

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [AWS Overview — Service landscape + Account setup 2026](lessons/01_basic/00_what-is-aws-overview.md) | Bản đồ ~20 dịch vụ tier 1, tạo tài khoản, ARN, IAM Identity Center và Free Tier |
| 01 | [EC2 + EBS — Compute foundation](lessons/01_basic/01_ec2-and-ebs-compute.md) | Các loại instance, AMI, ổ đĩa EBS, Auto Scaling Group (ASG) và mô hình giá spot/RI |
| 02 | [S3 deep + IAM fundamentals](lessons/01_basic/02_s3-deep-and-iam.md) | Bucket policy, IAM policy, presigned URL, vòng đời (lifecycle) và versioning |
| 03 | [RDS + DynamoDB — Managed databases](lessons/01_basic/03_rds-and-dynamodb.md) | RDS Postgres Multi-AZ, Aurora, thiết kế bảng DynamoDB và ma trận quyết định |
| 04 | [Lambda + API Gateway — Serverless intro](lessons/01_basic/04_lambda-and-api-gateway.md) | Cách kích hoạt (trigger) Lambda, hiện tượng cold start và so sánh API Gateway HTTP với REST |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [11_cloud](../README.md) — trang tổng của mảng điện toán đám mây.
- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../cloud-fundamentals/) — các khái niệm chung (region, AZ, mô hình dịch vụ) áp dụng cho mọi nhà cung cấp.

### 🧩 Các chủ đề có thể bạn quan tâm

- 🏗️ **Tự động hoá hạ tầng:** [IaC — Infrastructure as Code](../../10_devops/iac/) — dựng tài nguyên AWS bằng code thay vì click tay trên Console.
- ☸️ **Điều phối container:** [Kubernetes — Container Orchestration Platform](../../10_devops/kubernetes/) — bối cảnh cho dịch vụ EKS (Kubernetes được quản lý trên AWS).

### 🌐 Tài nguyên tham khảo khác

- [Trang tài liệu chính thức của AWS](https://docs.aws.amazon.com/) — nguồn tham khảo gốc đầy đủ nhất.
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) — bộ nguyên tắc thiết kế kiến trúc tốt trên AWS.
- [AWS Skill Builder](https://skillbuilder.aws/) — nền tảng học và luyện thi chứng chỉ chính thức của AWS.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. AWS vendor-specific deep cluster đầu tiên của 11_cloud.
- **v2.0.0 (01/06/2026)** — Việt hoá toàn bộ prose điện tín (block 🎯, Bắt đầu nhanh, mô tả bảng Lessons); bỏ cột "Thời lượng" + cụm "~103 phút đọc" (field thời lượng đã loại toàn kho); đổi field "Status" → "Trạng thái"; chuẩn hoá link-text = tiêu đề H1 thực của bài đích; tái cấu trúc mục Liên kết theo 3 sub chuẩn (🧭 Định hướng lộ trình học / 🧩 Các chủ đề có thể bạn quan tâm / 🌐 Tài nguyên tham khảo khác).
