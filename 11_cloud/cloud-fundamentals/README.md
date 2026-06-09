# ☁️ Cloud Fundamentals — Nền tảng điện toán đám mây

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 01/06/2026\
> **Status:** ✅ Basic 5/5 hoàn thành

> 🎯 *Cụm nền tảng của `11_cloud/`. Trước khi đụng vào AWS, GCP hay Azure, bạn cần hiểu những khái niệm chung mà mọi nhà cung cấp đám mây đều chia sẻ: cloud là gì, hạ tầng đặt ở đâu, mạng nội bộ vận hành ra sao, lưu dữ liệu vào đâu, và ai chịu trách nhiệm bảo mật phần nào. Năm bài dưới đây đi từ bức tranh tổng quan đến từng trụ cột hạ tầng, dùng ví dụ AWS làm minh hoạ nhưng tư duy thì áp dụng được cho mọi vendor.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua cụm này, bạn sẽ:

- [ ] Định nghĩa được cloud computing chuẩn NIST và phân biệt 3 mô hình dịch vụ *IaaS / PaaS / SaaS*
- [ ] Hiểu cách hạ tầng đám mây trải khắp toàn cầu qua *Region*, *Availability Zone* và *Edge*
- [ ] Dựng được mạng riêng trong đám mây với *VPC*, subnet, gateway và security group
- [ ] Chọn đúng loại lưu trữ (*block / object / file*) và đúng loại cơ sở dữ liệu cho từng nhu cầu
- [ ] Nắm *Shared Responsibility Model* — biên giới trách nhiệm bảo mật giữa bạn và nhà cung cấp
- [ ] Tránh được các cấu hình sai phổ biến gây rò rỉ dữ liệu (public bucket, port mở ra Internet...)

---

## 📂 Cấu trúc Chương trình học

Cụm này hiện tập trung ở mức Basic — đủ để bạn có nền vững trước khi học sâu vào từng nhà cung cấp cụ thể. Năm bài được sắp tuần tự, mỗi bài là một trụ cột hạ tầng và đều giả định bạn đã đọc bài liền trước.

### 📖 Lessons Basic — Năm trụ cột nền tảng (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Cloud computing là gì?`](./lessons/01_basic/00_what-is-cloud-computing.md) | 🌱 Intro | ✅ 🌟 | Định nghĩa cloud chuẩn NIST, 3 mô hình *IaaS/PaaS/SaaS*, mô hình triển khai *public/private/hybrid*, lịch sử 1999–2026, so sánh AWS/GCP/Azure và khi nào chọn cloud vs on-prem. |
| **01** | [`Regions, Availability Zones, Edge`](./lessons/01_basic/01_regions-availability-zones-edge.md) | 🌳 Lesson | ✅ 🌟 | Phân biệt *Region* / *AZ* / *Edge*, vai trò *CDN*, bài toán *latency*, các bậc dự phòng (single-AZ → multi-region) và cách chọn region đúng theo khách hàng + compliance. |
| **02** | [`Cloud Networking`](./lessons/01_basic/02_cloud-networking.md) | 🌳 Lesson | ✅ 🌟 | Dựng mạng riêng trong đám mây: *VPC*, subnet public/private, Internet Gateway vs NAT, route table, *Security Group* vs *NACL*, peering, VPN và Direct Connect. |
| **03** | [`Storage & Databases`](./lessons/01_basic/03_storage-and-databases.md) | 🌳 Lesson | ✅ 🌟 | Landscape lưu trữ (*block/object/file*, S3, EBS, EFS) và cơ sở dữ liệu được quản lý (RDS, Aurora, DynamoDB), cùng ma trận quyết định cache, search, queue. |
| **04** | [`Cloud Security & Shared Responsibility`](./lessons/01_basic/04_cloud-security-and-shared-responsibility.md) | 🌳 Lesson | ✅ 🌟 | *Shared Responsibility Model*, nền tảng *IAM*, mã hoá at-rest/in-transit, quản lý secret, các khung tuân thủ (SOC2, GDPR...) và những sự cố rò rỉ điển hình. |

---

## 🚀 Lộ trình đề xuất

- **Mới bắt đầu với cloud:** học tuần tự từ [Bài 00](./lessons/01_basic/00_what-is-cloud-computing.md) → 01 → 02 → 03 → 04. Mỗi bài xây trên bài trước nên đừng nhảy cóc.
- **Đã quen một vendor, muốn hệ thống lại tư duy:** đọc nhanh bài 00 rồi tập trung vào [Bài 02 (Networking)](./lessons/01_basic/02_cloud-networking.md) và [Bài 04 (Security)](./lessons/01_basic/04_cloud-security-and-shared-responsibility.md) — hai chỗ dễ sai nhất khi lên production.
- **Sau khi xong cụm này:** chuyển sang một nhà cung cấp cụ thể trong `11_cloud/` (AWS, GCP, Azure) hoặc đi sâu vào *serverless* và *cloud-cost-management*.

---

## 🌐 Tài nguyên tham khảo khác

| Tài nguyên | Vai trò | Liên kết |
|---|---|---|
| **NIST SP 800-145** | Định nghĩa chuẩn về cloud computing và các mô hình dịch vụ | [NIST](https://csrc.nist.gov/pubs/sp/800/145/final) |
| **AWS Well-Architected** | Khung 6 trụ cột thiết kế hệ thống cloud tốt | [AWS Docs](https://aws.amazon.com/architecture/well-architected/) |
| **Cloud Shared Responsibility** | Mô hình phân chia trách nhiệm bảo mật giữa vendor và khách hàng | [AWS Model](https://aws.amazon.com/compliance/shared-responsibility-model/) |

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Bản skeleton: tạo thư mục cụm + ghi chú cấu trúc dự kiến.
- **v1.0.0 (01/06/2026)** — Chuyển README sang dạng audience-facing: thêm mục tiêu tổng, bảng danh mục 5 bài Basic, lộ trình đề xuất và tài nguyên tham khảo; cập nhật trạng thái cụm sang hoàn thành.
