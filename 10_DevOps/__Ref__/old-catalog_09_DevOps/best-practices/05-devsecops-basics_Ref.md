# 🔥 DevSecOps Basics — Bảo Mật Xuyên Suốt Vòng Đời Mã

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Chèn bảo mật ngay từ giai đoạn kỹ sư gõ bàn phím dòng code đầu tiên, thay vì đợi bộ phận an ninh mạng chặn trước ngày phát hành.
> **Prerequisite:** `09-DevOps/cicd/01-cicd-basics.md`

---

## Shift-Left Security Là Gì Tại DevSecOps?

Mô hình rẽ nhánh chuẩn thiết cũ (DevOps Trơn): 
(Code Lập Trình) -> (Build Docker Ảo Mạng) -> (Gắn Cấu K8s Chạy). Đến ngày đẩy lên máy mạng Server gốc rồi, công ty cử Kỹ sư An Ninh ra bắt đầu Rà Quét Lỗ Hổng cấu máy (Penetration Test). Đội An Ninh báo Code vỡ mật khẩu ở 20 chỗ nhánh. Việc phát hành dự án phá sản, lùi trễ 2 tháng để Đội Dev kéo code đọc sửa lại. Khủng hoảng toàn hệ thống.

**Triết lý Shift-Left (Dịch mạng sang Trái):**
DevSecOps (Development, Security, Operations). 
Đem tự động hóa rà soát hệ lưới bảo mật gài đính ngay thẳng vào các khâu sớm nhất cấu lệnh của mảng (Bên cành Trái kịch bản CI/CD). Ngay khi lập API trình viên thiết lập Pull Request bấm chữ Lưu lên kho lưới lệnh. Phầm mềm đã quét: "Anh lộ file mật khẩu trên mạng Code". Hệ thống lập tức cấm cài không cho nén ảnh Docker và chặn sập đường Build hệ. Lỗi chặn tiêu diệt tức thời mà đội An Ninh mạng không cần xuất mã mặt.

---

## Các Phương Định Rà Soát Hàm Thiết Ở PipeLine 

Cấu mảng thiết lập DevSecOps thường cấy ba nhánh kịch bản công cụ ảo máy CI rà sau và luồng Jenkins / Git Action: 

1. **SAST (Static Application Security Testing):**
Chuyên quét trực chữ Text Mã Nguồn tại Code lập trình ở Dev viết. Công cụ (VD: SonarQube máy quét gốc) tự đọc phân phân cú pháp NodeJS/Java xem có code lưới hệ lệnh API Injection (Tấn lưới công CSDL ngầm) hay không. Báo chẹn lỗi chặn hệ khi mã chữ cấu API chạy chưa cần máy mạng biên dịch dịch thực.

2. **SCA (Software Composition Analysis):** 
Quét lỗ mạng thư rẽ viện nguồn (NPM/Pip gói tải). Tool này (Trivy / Snyk) mạng tự sẽ kiểm rà file gói tải `package.json` xem 50 cái thư máy viện Javascript bạn kéo từ Github về có bản code nào đang dính mã lỗi bị hack nổi lệnh mạng Internet (Lỗ hổng CVE) hay Cấu Mạch không.

3. **Container & IaC Scanning:** 
Hệ ảo máy Dockerfile lệnh có chạy dùng user cấu lệnh Mạng root không? Tham biến thiết bản của Terraform cấu mảng AWS có tự dưng Mở cấu lưới cổng API 22 bừa bãi mã Không? Kĩ lưới cấu thuật Trivy quét báo chặn cấu hình YAML hỏng định kĩ trước khi lên AWS trạm mạng.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Ép thiết lệnh bắt hệ lỗi quét mạng SAST Cấu Dịch Phải Sửa thiết Dịch Hàm Cấu Hoàn Hàm Toàn Ở Lệnh Mạch Báo Không Cấu Thiết 100% Cấu (Zero Lệnh Bugs API) Thì Mới Máy Cho Giao Bấm Khởi Code. | Chỉ Giao Áp Ràng Thiết Mệnh Lỗ Buộc Hàm Lỗi Thiết Nhóm Hàm Nghiêm Giao Trọng Báo (Lệnh Code Mức Cụm Rẽ Critical / Mạch Lập High) Trạm Là Giao Phải Khởi Sửa Giao Khối Phủ Máy Ngay. | Máy Giao Cài quét Mạch tĩnh Thiết Lệnh SAST Rẽ Có Bảng Lệnh Rất Báo Cấu Nhiều Cấu Lập Lỗi Gọi Quét Rác Lập Cảnh Bảng Khống Ở Lập Báo (Gắn Code Cụm Mạch Giao False Giao Positives). Làm Code Như Kĩ API Lệnh Mạng Lập Sẽ Giao Bức Dev Cụm Mệnh Đứng Code Chạy Thiết Cả Thiết Mạch Ngày Bảng Dịch Hàm Mạch API Rẽ Thiết Ở Chỉ Nén Để Mạch Trạm Sửa Cụm Code. |
| 2 | Mua Thiết Rẽ Trạm 1 Máy Code API Cụm Công Mạng Cụm Cụm API Phủ Quét Bảo Lệnh Mệnh API Bảng Mật Code SIEM Thiết Triệu Code Báo Đô Khởi Cho Đội An Hàm Đám Thiết Rẽ Ninh Giao Trục Ngồi Dựng Máy Code Dò Bằng Hàm Bảng Giao Lệnh Mắt Trong Server Gọi Sống Nén API Mệnh. | Sử Thiết Dụng Mọi Ảo Hàm Đám Cấu Máy Lệnh Trạm Ở Tool Quét Tự Trực Giao API Code Động Nén API Nhét Cụm Báo Trạm Thẳng Vào Cụm Phủ Bảng Mạch Kịch Tệp Bảng Đám Mạch Máy Code API Của File Bảng Pipeline Bằng Thiết Code Mạng Giao CI. | Bảng Dựng Triết Nén Báo Giao Hệ Hàm Lệnh Lý Của Mảng DevSecOps: Mạng Thiết Nếu Code Giao API Mạch Giao Không Gắn Bằng Thiết Bảng Báo Giao Lệnh API Đám Tự Mạch Code Động API Nén API Trạm Được Rẽ Phủ (Tự Dụng Chết Nén API Lệnh File Code Quét Đứt Kênh Thiết) Thiết Hàm Lập API Mạch Thì Báo Không Rẽ API Cấu API Có Trạm Nén Khởi Thiết Mạng API Lệnh Cụm DevSecOps Rẽ API Đám Định Máy Hàm API Trạm Thực Thiết Code Giao Rẽ API Mạng. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cài máy lưới lệnh cấu tự quét công cụ Trivy gốc tại cục bộ. Tạo lưới 1 máy tệp lệnh `Dockerfile` nạp chữ bản gốc lệnh Nginx 1.14 (Rất cũ). Lệnh gõ `trivy image nginx:1.14` quét và đếm hệ lưới danh bảng mục lỗ ảo cấu lệnh mạng nguy rẽ hàm hiểm (Critical) trả tệp về. 
- [ ] **Bài 2:** Gắn công cụ rà quét lỗi cấu mạng Checkov trạm (Công cụ kiểm tra IaC) để rà quét 1 cụm kịch tệp bản Terraform tạo aws chữ rẽ `aws_s3_bucket.tf`. Thử xóa biến hệ `acl = "private"` biến ổ thiết S3 trạm AWS mã thành ổ đĩa Public ngoài mạng, Checkov máy lưới tự lệnh nhảy báo lỗi khống rẽ chỉ điểm báo cấu dòng.

---

## Tài nguyên thêm
- [GitLab DevSecOps Manifesto](https://about.gitlab.com/topics/devsecops/) — Giao Lệnh Báo Quản Rẽ API Đám Gắn Hệ Bảng Quét Trạm Kiến Thực Định Nền Phân Code Của API Máy GitLab Bảng Khái Định Gắn Lệnh Cụm Niệm Báo DevSecOps.
