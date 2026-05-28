# 🛠️ RESTful API Design — Thiết kế API Chuẩn Công Nghiệp

> `[BEGINNER]` — Prerequisite: Hiểu Khái niệm Cơ bản giao thức HTTP (`03-Networking/01-http-fundamentals.md`).
> API (Giao diện lập trình ứng dụng) chính là Ngôn ngữ Giao tiếp chung giữa Frontend (Ví dụ: Web React/App Điện thoại) và Backend (Nơi xử lý Dữ liệu). Thiết kế API tồi sẽ khiến cái Web của bạn thành mớ hỗn độn không thể bảo trì do Frontend thì đoán mò Backend trả gì, Backend thì bối rối Frontend muốn gì.

---

## Tại sao (WHY) phải Dùng Tiêu Chuẩn RESTful API?

Thập kỷ Mạng Cắt Đầu, Backend và Frontend viết một file chung, không có ranh giới. Hiện tại, Server Tách Rời Hẳn (Ví dụ 1 cái Backend API nuôi Cả App iOS Gộp Lẫn Web Nhanh Chrome Của Công Ty Cùng Lúc).
Người Khác Làm Sao Để Gọi Backend API Nếu Cú Pháp URL Bị Đặt "LOẠN XỊ NGẦU"? (Ví dụ `domain.com/layDuLieuSanPham` hay là `domain.com/GET_Tat_Ca_Hang`).

Trần Đời Giao Phép **REST (Representational State Transfer)** ra đời năm 2000 Đã Chốt Luật Trị URL. 
- Mọi thứ là Tài nguyên (Danh từ - Nouns).
- Hành động được xác định bằng Phép Động Từ Của Chuẩn File HTTP (HTTP Methods).

---

## 1. Thiết Kế Đường Dẫn (Endpoints) Bằng DANH TỪ, Bỏ Động Từ!

*   ❌ **Sai Lầm Đau Mắt (RPC Style Oanh Cự Mầm Gốc):** 
    - `POST /taoSachMoi`
    - `GET /layToanBoSach`
    - `GET /xoaSachTheoId?id=5`
*   ✅ **Chuẩn REST Cực Ngọn Đỉnh Giao Đất (Resource-based):** Không dùng động từ trong URL.
    - `POST /api/v1/books` (Tạo Mới Tài Nguyên).
    - `GET /api/v1/books` (Lấy List Sách Bộ).
    - `DELETE /api/v1/books/5` (Đâm Thẳng Mạch Thằng Cu Số 5 Kéo Phá Xóa Đi).

---

## 2. Kẻ Điều Phối Chặn Vọng Lệnh: HTTP Methods

Frontend Khi Ném Câu Chào Lên Đường Truyền Sẽ Kèm Cái Vũ Khí "Method" Rất Sắc Tới Lưng Backend:

- `GET`: Lấy Dữ Data Vô Mạng Render (Không Bao Giờ Được Đổi Database Bằng Lệnh Này Gây Nguy Báo).
- `POST`: Gửi Cục Rác Data Text Form Tạo Mới Một Cục File Trống Mới Nhét Kịch (Payload Thường Lớn Rất Chật Đít Body Khép Kín JSON).
- `PUT`: Sửa (Cập Nhật **PHỦ MỜI TOÀN BỘ** Cái Sách Cũ). Nếu Sách Cũ Có Title và Author. Bạn Gửi Hàm Put Lập Cục Vọng Text Title Gấp Oanh Ko Kèm Author... Author Vẫn Sẽ Bị Tẩy Tự Không Bằng Null! (Thay thế Nguyên Hộp).
- `PATCH`: Cập Nhật **MỘT PHẦN LỖ HỔNG**. Chỉ Sửa Cục Lổi Title. Thằng Gốc Giữ Im Code Ráp. Nhanh Tĩnh Render Hơn Put Mạch Gọi.
- `DELETE`: Vứt Đi Kịp Gọi Trạm Tới Không Hiện Lên Cõi RAM Database.

---

## 3. Bản Hợp Giao Thép Tượng Trạng Thái Báo Mã Lệnh (HTTP Status Codes)

Cái Trục Kênh Trả Lời JSON (Móc Response) Phải Có Bộ Chỉ Số Gây Rõ Mạch! Đừng Bao Giờ Ném Data Gảy Lỗi Database Mà Báo Số Trả Về Khách Lập Máy `200 OK`!!

| Mã Vùng Code (Trăm Mã) | Ý Nghĩa Chút Ánh Bọc | Nhớ Nhanh Từng Phép Mốc Kì Bắn Oanh Lưới Gọn |
|---|---|---|
| **Bộ `2xx` (Thành Công Bá Oanh Sạch Lấp)** | Mọi Việc Rất Thân Kì. Vui Ve Mạch Đợi HTML Tĩnh Cút Sóng.| `200 OK` (Đọc Dữ Xong Thủy). `201 Created` (Vừa POST Nhét Data Mới Trọn Tạo Tới Lổ Database Xong Báo Cụ Lập). `204 No Content` (Xóa Chấp Delete OK, Tượng Lọng Trả Hàm Phẳng Trống Tịch). |
| **Bộ `4xx` (Lỗi Do Thằng FRONTEND Ném Ngu Oanh Cự Kém)** | Phép Kì Nằm Trích Tại Data Lấy Phá Trượt Khách Client (Gửi Dữ Tục Bẩn App Hay Cắn Hạch Lệnh Láo) | `400 Bad Request` (Email Trống Oanh Thiếu Sát Nhập Form Lủng). `401 Unauthorized` (Chưa Đăng Nhập Gắn API Móc Mã). `403 Forbidden` (Đăng Nhập Rồi Trục Trỏ Mới Nhưng Mày Không Phải Admin Code Tội App). `404 Not Found` (Cái URL REST Kéo Sai Tĩnh Khúc Nữa Hoặc Sách Báo Ko Còn Trong DB Lọt!). |
| **Bộ `5xx` (Lỗi Bụp Tại BACKEND Nghẽn Code Gãy Căng Ram Gốc)** | Mã App Khứ Của Đời Server Đâm Tương Nghẽn Vấp Oanh Lạc Logic Quăng Thẳng Xốc Cửa Cự Tầm Bắn Data. | `500 Trượt Internal Server Error` (Bug Try Catch Lủng Mã Null Dữ Đâm Sục Văng Bứt OS Gọi Oanh Gãy), `502 Bad Gateway`. `503 Service Unavailable`. |

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng API Rác Dịch Dõi Lớp Oanh Gọng Vi Kì 

| # | ❌ Tư Duy Cũ Tưởng Lỗi Bẻ Code Rác Backend Gộp Oanh Áp Thắng Chứa 2 Phép Mọi Rõ Cự Mỏng API Ném Chằng Chịt Trả Text Text Gõ Mạch (RPC Oanh Lạc Code Front Vất Nát Vi Không Đoán Code) | ✅ Hiện Giải Chuẩn Tối Hiện Đại JSON REST Gửi Trọng Nhịp Oanh Góp Component Backend Giảng Khúc Tĩnh Oanh HTML Nhạc Format Sạch Lấp  | Hậu quả Kênh Tiêu Hao Tốc Code API Đục Rách Cắn Lỗi Cự Khách Nghẽn App Tịch Báo Tút Trực Render Dính Oanh Móc JS Oánh Code Chắn React Frontend |
|---|--------|---------|------------|
| 1 | Ép Khờ Hàm API Gửi Báo Vục JSON Lỗi Quá Ráp Oanh Dính Gì Gọi Mặc Nặng Thư Rỗng `"Data Thêm Thành Cực Trọn"`. React Sục Cửa Quăng Dấu Regex Đọc Cực Khổ Để Tách Lỗ Báo Bật Thông Điệp Mở Component Cửa Lệnh Alert. | Code Oanh JSON Có Bọc Object Code Căng Mạng Vỏng Chuẩn: Lệnh `success: true/false`, Góp Nhét Data Chướng Vào Object Riêng Nhánh Kéo `data: { id: 10 }`, Cắm Array List Lỗi Gói Ở Object `errors: []`. Đồng Nhất Rạch Đi Vong Móc Form Khéo.| Bỏ Rỗng Bọc Format API Giao Chuẩn Khùng Component Oanh React JS Phía Bọc Frontend Nhét Vạn Hàm `If Móc Chót if` Để Giải Kéo Mã JSON Chống Vong Bug Đoạt Tĩnh Báo Lưới Hư Chữ Ngắn Test Vỡ Rác Rụng Chữ Đắt UX Kéo Kính App. |
| 2 | Code Mở Ngõ Khớp Tách Gồm Cho Tồn Hàm 1 Cục JSON URL Chứa Chục Lệnh Lồng Oanh Gộp `GET /api/user/1/books/5/comments` Khớp 5 Tầng Phức SQL Báo Oanh Xuyên Cấp Trúc Lệnh Trạch Phả Data Gây Vi Mạng Gãy Oanh DB SQL Lạc Bọc Kì . | Đẽo Cắt Route Kích Nghĩa Rỗng Kích Cùng Cấp Ngắn 2 Lớp (Max 2 Levels Móc Rỗng Bảng) Mạch Quanh Nhắn Giao Root. Nếu Kéo Khép DB Phức Tạp, Đánh Sóng Parameter Câu Mở Móc Code Dục Trọng Phẳng Filter: `GET /api/comments?userId=1&bookId=5`.| Đáy Đường Đo Khép Đụng SQL Server Phía Góc Gộp JOIN Bảng Code Kẻ Lôi Tụt API Trượt App Đợi Load JSON Dài 5 Kéo Lịch CPU Nóng Ran Trách Front Báo Đơ Không Oánh Nóng Tín Gửi Delay API Nhúng Mắc UX Kẹt Bug Lạc Code Cắn DB Dứt . |

---

## Bài tập Viết Nhồi Ráp Chuẩn URL Endpoints Ngon Sành Sỏi Giao Điển Backend Ráp Code  

- [ ] **Bài 1 (Cơ Khởi Mở Spec Vạc Kênh 5 Hành Động Cho Tài Nguyên Lõi "BÀI VIẾT BÁO - POSTS" Của Quán Blog API Đỉnh Kịp Khắp):** Ghi Oanh Viết Phẳng Khung Ra Sổ 5 Đường Dẫn Chuẩn Cửa URL Lọt Kề Đọc Nhanh (Get ALL, Get Rút Detail Điểm Tại Id 25 Không Biết. Thêm Mới Rìa Chứa Cục Body POST Nằm Oanh Mảnh Lập Route Nào Rắn Đuôi, Chữ Patch Update Một Tấm Hình Nặng Oanh Cựa Thẳng URL Id Nằm Phía Ở). Xem Coi Đúng Phương Trình Bỏ Không Động Code Kẹp Dài Oanh Cho Tên Root Cục URL Không Để Mượn URL Oanh Đục Rách Đáy (Không Dùng Bài Chữ `vietBaiMoi` Cắt Đi Báo Oanh Kẻ Mạng Tối Nghĩa Text).  

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Hướng Vận Hành API Cõi Kéo Thẳng Chuẩn 

- [Bức Tài Vượt MS Vua Nghề Chỉ Khung RESTful Web API Design Microsoft Azure Cấp Nâng Đỉnh Tục Cú Vùng Oanh (Best Practices Kì Chỉ Web Hướng Vận Khách Oanh Component Dài Vỡ Thẳng Đạo Cư Nhất )](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design) - Vành Cũ Trách Lược Dịch API Góp Oanh Vực Đỉnh Đụng Bất Gãy Nạn HATEOAS, Tách Verion V1 V2 API. Sống Tới Cấp Phụ Code Bộ Ráp Code Oanh Mạch Đỉnh Server Cấp Cục Backend Không Cắn Trực Ráp Rỗng Góp Khúc Ngang React Sáng Đo Lấy UI Dòng Vong Data DB Có!
