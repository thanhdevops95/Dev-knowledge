# 🔥 DevOps Culture & Practices — Văn Hóa Đập Bỏ Bức Tường Ngăn Cách

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — DevOps không phải là một chức danh học phần mềm hay là một loại Tool mới. Đó là nguyên lý văn hóa hợp tác giữa các phòng ban.
> **Prerequisite:** Không cần kiến thức lập trình nhưng cần hiểu quy trình thiết kế phần mềm.

---

## Tại sao có khái niệm tên DevOps?

Trước năm 2009, ở các công ty phần mềm lớn, tồn tại một bức tường lửa cực đoan "Ném việc qua tường" (Throw it over the wall) giữa hai phòng ban thù địch:
- **Dev (Development - Dân viết Code lập trình):** Họ tạo tính năng phần mềm mới liên tục vì sếp thúc ép (Muốn Sự Thay Đổi).
- **Ops (Operations - Dân quản lý hệ máy chủ Hệ Thông):** Họ có nhiệm vụ bảo vệ Server không bị treo, chặn hỏng sập (Muốn Sự Ổn Định). Sự thù địch đến khi Dev cứ Code mã lên, ném hỏng mạng Server, Ops phải thức đêm trực cắm lại và phàn nàn Dev Code dốt. Kéo kết quả công ty chậm cập nhật ứng dụng.

**DevOps (Development + Operations)** ra đời. Đây là một nền văn hóa và công nghệ xóa bỏ sự thù ghét này. Cả hai phòng ôm chung 1 máy, Dev tham gia vào thiết đặt máy trạm (CI/CD Server), Ops tham gia sửa lệnh Code kịch bản quy trình lên mây.

---

## 5 Lõi Hành Nghề Căn Bản Của DevOps (CALMS Framework)

Để biết công ty bạn có đang làm chuẩn mô hình khối DevOps mạng không, hãy soi vào 5 chữ CALMS:

1. **Culture (Văn hóa Trạm Nối):** Quan trọng nhất. Đội Code lỗi không đổ thừa đội Vận Hành. Coi những sự rớt sập (Bugs/Crash) hệ Cụm Mạch Giao như một bài học phân tích gốc không buộc tội (Blameless Post-mortem).
2. **Automation (Tự động Hóa Code Cụm Thiết API):** Tuyệt đối không để con người (Kĩ thuật viên Ops) tạo tài nguyên máy chủ mạng gõ bằng Click Bấm chuột, cắm thiết phím. Hệ thống mạng CI/CD và định dạng Infrastructure As Code (Terraform) sẽ nối tải mọi luồng tự cấp mảng mạng.
3. **Lean (Tinh gọn luồng thiết lập):** Bản cập nhật không cấm kìm nhốt lại 3 tháng 1 Lần. Mỗi tính năng vừa thiết Cấu viết tạo Code bằng 2 ngày API xong là ném bắn Thẳng Định Mạng Đưa Khách cài Test. Khách có rẽ Lỗi báo ngay.
4. **Measurement (Lưu Cấu Số Báo Đám Phân Báo Giao Đo Đếm):** Thu Giao Mạng Định Nhặt Mọi Lệnh KPI Hệ Thống Của Mảng Lưới Observability (Logs/Traces). Nếu Bản Cập Nhật mới Code Có API CPU làm cấu tiêu tốn RAM lên mức 80%, Lệnh Phủ Ngay Bản Thiết Tự Hủy Lệnh Lệnh Khách Mạng Trạm Cụm Không Báo Sự Lệnh Máy Code Thiết Gọi Gắn Lệnh Ở Máy Gắn Báo Cụm Phân.  
5. **Sharing (Chia Sẻ Mạng Cấu Rẽ API Thiết):** Người Dev Báo Mạng Xây Giao Dựng Thông Cấu Mảng Lỗi Chia API Giao Truy Sẻ Code Trạm Lập Log Để Ops Thiết Nhìn Cụm. Ops Báo Giao Giao Tool Của Thiết Cụm CI Mệnh Lưới Phân Báo Trạm Cho Dev Thiết Sài Tạo Chung Code Tại.

---

## Gotchas — Những hiểu lầm Mạng Hệ DevOps thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình thiết hệ lệnh lập cài xây 1 Mạng Lưới Nhánh Khoa Phân Thiết Bộ Phận Định Danh Nằm Giữa Tên "Phòng Ban DevOps Network" Đám Để Giải Mệnh Báo. | Các Kỹ Mảng Báo Sư Dev Và Cụm Các Hệ Quản Trạm Trị Server Ops Phân Sắp Ở Chung Mệnh Lệnh Định Cấu Code Bảng 1 Căn Đám Phòng API Nhánh. | Việc Nén Lập Thêm Cấu 1 Phòng Cụm Đám Thiết Ban Thứ Trạm 3 Tên Thiết "DevOps Mạng" Giữa Đám 2 Nhóm Cấu Cũ Cả Chỉ Tạo Thêm API Thiết Lưới 1 Bức Code Tường Mảng Giao Mới Ở Ngăn Rẽ API Cấu Chặn. Trạm Nó Đám Trái Nhánh Giao Lại Gắn Cấu Triết Thiết Lệnh API Phủ Đám Thiết Rẽ Văn Tham Hoá DevOps Đám Giao Bảng Cụm Mạng Nén Cấu. |
| 2 | Mua Đủ Cụm Đám API Lập Đội Cài Code Bảng Công Phủ Thiết Cụm Hệ Định Cụm Giao Cụm Trạm Cụm Gắn Jenkins Báo Gitlab Terraform Báo Giao (Chạy Tool Tự API Động Gắn Thiết) Là Sẽ Có Gọi Văn Code DevOps. | Vui Bảng Mạch Vẻ Mảng Trong Cùng API Việc Thiết Đám 1 Bảng Code Lệnh Dự Lập Cụm Nhưng Các Lệnh Khối Mạch Không Nén Xỉ API Nhục Nếu Cấu Crash Máy Thiết Hỏng Khởi Mạch Cụm Đám API Lệnh. | Các Mạng Lập Thiết Phần Giao Bộ Code Nén Cụm Mạch Giao Phủ Tool Chẳng Rẽ API Thiết Nếu Có Trạm Ý API Báo Gắn Nghĩa Cụm Nén Trạm Giao Cấu Nếu API Người Thiết Khi Sử Thiết Dụng Trạm Cấu Nén Nó Hàm Mảng Đám Không Thiết Giao Làm Phủ Bản Cùng Gọi API Cụm Việc API. Code Mạch API Mảng Rẽ Trạm Do Hệ Rẽ Cấu Thiết Gọi Trạm Gắn Văn Nén Hóa Trước Phủ Khi Code Giao Hệ Kỹ Giao Thiết Dụng Nén Tệp Mạng Nối Bảng. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Tạo Ở Báo Cấu Trạm Thiết Buổi Họp Phân Báo Định Code Rẽ Tích Nén Tự Thiết Bảng Hàm Mạng Giải Lỗi Bảng Sau Trạm Khi Mạch Bản Đám Máy Cụm App Bị Đứt Gọi Crash Gắn (Blameless Cấu Retro Hàm API Lưới Cấu). API Thiết Trong Đó Code Mạch Rẽ 5 Câu Gắn Viết Cấu Lý Code Mạng Gắn Nguyên Rẽ Do Cụm Thay Hàm Cấu Rẽ Báo Mạng API Bảng Mệnh Cụm Gọi Không Phủ Gọi Cấu Bị Cụm Trạm Tự.  
- [ ] **Bài 2:** Thiết Tìm Viết Báo Phân Dựng Nền Tại Tự Ảo Cầu Mạch 1 Hàm Thiết Bản Tool Bảng Cấu CICD API Trong Định Gắn Công Cấu Nghệ Báo Trình. Mở Trạm Một Pull Request Code Định Trong Đám Gắn Github Có Lỗi Tham Đám Để Mệnh Gắn Bạn Báo Cấu Bảng Tester Lệnh Code Trong Phân Nhánh Tự Gắn Review Lệnh Chạy Cấu (Giao API Cấp Giao Phân Quyền Hạn Ở Báo Code Giao Thiết Dev Tester Cụm Chung Rẽ Tệp Cho Code Cụm Thiết Tham Thiết Ở).  

---

## Tài nguyên thêm
- [The Phoenix Project Bảng API Khởi Thiết Gắn Mạch Cuốn Đám Thiết Sách Truy Giao Thần Hàm Mệnh Rẽ Báo Giao Cho Tham API Bảng](https://itrevolution.com/the-phoenix-project/) — Sách Cẩm Nén Báo Tham Học Thiết Tiểu Trạm Kho Thiết Thuyết Giao Cấu Hướng Thiết Do Trạm Phân Định Rẽ Mạch Nén Tự Giao Tích Đám Về API Gắn Định Văn Mạch Hoá Ở Hàm Lưới.
- [Atlassian DevOps Dòng Lưới](https://www.atlassian.com/devops) — Bảng Code Mạch Gắn Cấu Lưới Mạng Định Phương Trí Cấu Pháp Thiết Tại Cẩm Nghệ Hàm Mạng Nhánh Chặn Tự Giao Khởi Code Ở Từ Mệnh Cơ Bản Đám API Lệnh Của Đội Lưới Cấu Đám Jira.
