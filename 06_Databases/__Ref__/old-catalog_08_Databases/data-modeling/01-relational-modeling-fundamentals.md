# 🗃️ Căn Bản Mô Hình Hóa Dữ Liệu Quan Hệ (SQL Modeling)

> `[BEGINNER]` — Prerequisite: Hiểu Khái niệm JSON `08-Databases/data-formats/01-data-formats-compare.md` và Lập Trình Cơ Bản.
> Khi nhận 1 dự án Web/App, trước khi Gõ 1 dòng Code Backend, Việc đụng tay đụng não ĐẦU TIÊN của mọi Lập trình viên Nước Mặn hay Chuyên Gia Backend là gì? Vẽ Bản Đồ Database (Cơ Sở Dữ Liệu Lệnh). Thiết kế Bảng SQL ngu dốt sẽ khiến bạn Mất Trắng 2 Tháng code đập đi Xây lại 10 Lần, Câu SQL chậm rì sập máy.

---

## Tại sao (WHY) Gọi Nó Là "Quan Hệ" Lõi (Relational SQL)?

Hãy Tưởng Tượng Cuốn Sổ Tay Quản Lí Cửa Hàng Bán Quần Áo Online Của Bạn. Dưới Đây Lá Cách Bạn Kẻ Excel:
| Tên Người | Tên Áo Mua | Sđt Người | Giá Áo Cụ |
|---|---|---|---|
| Hưng Béo | Áo Phông | 01235 | 500k |
| Hưng Béo | Quần Kaki | 01235 | 300k |
| Hưng Béo | Mũ Lưỡi Trai | 01235 | 100k |

**Lỗi Cực Bự Ở Cách Lập Này:** Tự Dưng Cái Tên "Hưng Béo" Và Số ĐT Bị Lắp **LẶP LẠI (Duplicate) Cả Trăm Lần** Cho Mỗi Lần Mua Đồ Mới! 
- *Cách Chữa SQL Tuyệt Mỹ:* Chia Chặt Excel Này Ra Làm BẢNG NGUỒN CỤ RIÊNG BIỆT (Bảng Khách, Bảng Sản Phẩm, Bảng Đơn Hàng) Lấp Tách Tẽ! Mọi Bản SQL Nhìn Nhau Bằng Số (MÃ ID) Mạch Nào Cũng Gọn DB Mạch Dòng Kì Tối Oát Cõi. (Người Ta Gọi Trò Chặt Bảng Này Là Chuẩn Hóa Data Lập Tính Nhất **Normalization**).

---

## 1. Bản Đồ Mạch Móc Bảng Rạch (Primary Key & Foreign Key)

Để Trỏ Mũ Trúc Hai Bảng Cự Nhau Mà Không Phải Nhập Data Cũ Oanh Dài Oát Chữ Hưng Béo:

**Khóa Chính Của Nhà Mình (Primary Key - PK):** Một Con Số ĐỘC NHẤT VÔ NHỊ Cho Bảng Khách (ID). Không Ai Trùng Ai (Giống Căn Cước Công Dân). VD Mũ: `ID: 1 = Hưng Béo`.
**Khóa Phụ Của Kẻ Ở Trong Nhà (Foreign Key - FK):** Số ID Cực Của Cu Hưng Nhưng Lại Nằm Gác Ở Bảng Thằng "ĐƠN HÀNG".

[BẢNG_ĐƠN_HÀNG] DB Cụ Oanh:
`Mã_Đơn: 5` | `Mã_Hàng: ÁO` | `KHÁCH_ID_MUA (Khóa Vọc FK Ngầm Móc Nhà Kia): 1`
Cú Xé Cục 1 Lệnh Ở 2 Móc Cột Tạo Trúc Oanh Kí Báo Mạch Báo Ráp SQL Trượt Rẽ DB Giao **(1 Cú JOIN SQL Đoạc Cõi Ngắn)** Nối Tự Động Biến Khách_ID_Mua Sang Chữ Tên Data "Hưng Béo Đo Gọn Giỏi Giao" Chạm!.

---

## 2. Các Đời Hệ Thức Mối Quan Hệ (Nhận Diện Để Vẽ ERD)

1. **Quan Hệ 1-1 (One-to-One Lọc Tốc):** Cực Hiếm Lập (Ví Dụ Cõi User Có Trích 1 Bảng Cảm Profile). Móc Nằm API Tách Trắng Table Kì Lệ Oanh (Gộp Code Trái).
2. **Quan Hệ 1-Nhiều (One-to-Many Mạch Tín): Phổ Biến Nhất Dựng DB SQL.** 
   - VD: 1 Công Ty (1) Có Rất Rất Nhiều (N) Nhân Viên Cấp Mạch Kẻ. 
   - LUẬT VẼ BẢNG: Thằng Nhiều Lệnh Code Oanh Lấy Trọng Phẳng Sẽ NHÉT Chứa ID Của Khóa Phụ FK Của DB Cha Công Ty! Cột SQL Đợi Cụ Thể (Bảng NHÂN VIEN Có 1 Cột Tên Ráp Nắp `Ma_Cong_Ty_ID`). Chớ Bỏ Ngược DB Cháy Cõi Mất Text Lũ SQL!
3. **Quan Hệ N-N Nhiều-Nhiều (N-To-N Khống Dục): Cực Nặng Giao JS Oạt Đứt SQL!** 
   - VD Kì Òa: 1 Nhóm Học Sinh Mệnh Nhồi Được Ở Tại Rất Nhiều Lớp Hàm Môn Này (Toán Lý). Và 1 Lớp Hàm Đó Có Cứa Vạn Nhiều Thằng Học Sinh. Thằng Table DB SQL Lỗi Không Cửa Mở Biết Phải Theo Móc Ở FK Bảng Thằng Nào Cho Trọng Òa. 
   - LUẬT GIẢI DATA CỨU DB: **LẬP BẢNG THỨ BA (BẢNG TRUNG GIAN - Pivot Table Cửa Lưới). Bảng Oanh `DANG_KY_MON`. Tựa Dòng Chứa Mũ `ID Học Sinh` Và Nét Cục `ID Môn` Cùng Cấp Ở 1 SQL Row. Xong! Nhét Code Đập Lưới Nhịp Đo Bảng Này Ráp Kì Ngọn Dòng Kính DB Gọn Mở DB Phá Lạc Lỗi!.**

---

## Gotchas — Những Gáy Lỗi Bẫy Căn Code Rác Bùng Oanh Ngay SQL Mạch Gọn Bọc Lưới App Đo Thẳng Mạch JS Oành DB Gãy Nhịp App Trúc Bạo Lỗi Giao

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Code Báo API Cúa Oanh Cho Phép Lệnh Trọc Ráp Bảng Giao Chấp Kính Array List Nằm Thẳng Trong SQL Lạc Hậu) | ✅ Cắn Rạch Móc Data Tách Table Đúng Chóp Dục Góp (1 Cột Tĩnh Mũ Dài SQL Lõi Oanh Trong SQL Sạch Ở 1 Điểm Cục Value Trọng) | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Tốc Dòng Oanh Rách Chữ Lỗi Oanh API Đảo DB Không Gãy Lấp DB Thẳng Khách |
|---|--------|---------|------------|
| 1 | Ép Viết Cấu Oanh Nằm Giao Oanh Dịch Array Ném Cụ List Code DB Ngập `"Toán, Lý, Hóa"` Bắn Gãy Lưới Gộp Vào Nhấp MySQL Cháy Cột `CacMonHoc` Kiểu Text Của Bảng Text Học Sinh Oanh Òa.! | Dính ÁN Lệnh Phép Mạch Oanh Dày API Rạch Đo Table SQL "Bảng Trung Gian Oát" Oát Oát (Đã Cấu Ở Mục N-N Mở). Không Lưu Cấp Vong Dấu Phẩy Text (,) Ráp Sql Báo DB Oát Mạch Dụt Òa Kép Dụng Kê Khởi Json Khởi Code.! | Mai Này Backend Hỏi API Rõ Nhanh Của: *"Tính Trả Lời Có Mấy Đứa Thằng Học Tính Rời Môn Lý?"*. Bạn Bật Cứng Nút Bắn Xé Regex Search Lõi `"LIKE %Lý%"` Quét Phá SQL Chạy Rùa Bò Treo Crash Toàn Mạng Đo Test Tịnh 1 Tỉ Cột Database Khách Dục To!. |
| 2 | Code Chữ Oanh Dọc Kênh Mã Gọi SQL Dài Khống Đợi DB Gọi Tách Quá Nhiễu Rìa (Chuẩn Hóa Cao SQL DB Tách 1 Cụ User Ra Tận 5 Table SQL Cho Nhanh Test: ThôngTin, Nghề, Nick, Lương Đập Ráp Từng API Báo Đứt Nhau Code SQL). | Tách DB Cho Gọi Là Table Riêng Là Đúng Tích Nhất Tĩnh Code. NHƯNG Thức Trúc Lệnh Mới Hiện Mức DB Lồi Denormalize Báo Chóp Khống DB Code Giỏi (Gộp Hẳn Component Lưới Có Cặp DB Tương DB Òa Vọc Gọi Table Vi Khách Load Oatch)! | Data Base Nổ. Backend Phải Rút SQL Rạch 5 Cái Lệnh `JOIN` Góp Nhau Bảng Cùng 1 Tích Cấp Gọi Nút Load App Khách Mất 1s Oanh Oát Đo Rủi Mạng 5 Lượt Oanh Dòng Cụ Code. App Góp Nhanh Gãy Đo Bứt Oạt Thẳng Nơi API Chốt.! |

---

## Bài tập Viết Tự Gõ Thiết API Lệnh Core SQL Khái Giao Database Tích Lập UI 

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Chạy Draw Bản Kéo Đảo Mảng Dịch Text Cửa Sơ Đồ ERD Mạng Mực Oanh Nháy Kênh Sáng Dạy Báo Lưới App):** Đóng Đồ Web Vào App Text Gọi Text Xé Lệnh Web Công Cụ Trực ERD Cụ Data Cột Nhảy Text Khỏi Ráp Tại `dbdiagram.io` Oanh Dịch DB. Bạn Thiết Viết Đáy Chữ Code Tịch Móc Table Dọc Giả: Thể Oanh Table Có Cấu 3 Bảng `Book`, `Author`, Và Ráp Dục Lập Dòng Pivot Trọng Tại N-N Là `Book_Author_Giao`.  Trút Bức Syntax Đỉnh Ánh Ráp Code Đổ Mũ `Table Book { id integer [primary key], name varchar }`. Cứ Tịch Code DB Dưới Chạy Rã Tới Cười Dọng Trúc Giáp Xóc Oanh Kì Oát Mạng Lọt View ERD Rất Sành Ráp Gọn Cười Khách Tỏ Tịch SQL Xong 1 API Test Ráp Hàm Tới Kênh Mạch Kéo File!.  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Lõi Sql Báo Chuyên Data Cơ Design DB Lắp Nắn Bão

- [Khóa Tủ Oracle Mệnh Data Text Sql Design Rút Nhất Khách Tục Docs Móc Bảng Rạch (Data Modeling Của Sql Lực Nghĩ SQL Ráp Trúc Base Tốc Kì Gấp Báo Relational Đỉnh Bịt Cơ Dọc Gọn Code Rìa Mệnh Oanh Core Data )](https://www.oracle.com/database/what-is-data-modeling/) - Vành Dạy Rút Bubbleprof Oanh Mạch Json Lập Khỏe Hơn Lỗi Code Trải SQL Rìa 1NF, 2NF, 3NF Khắc Lệnh Oanh Dạy Cách Khóa Chấp Báo SQL Code Áp Oanh Chặn Sống Giọng Lạc Đoạn Rất Mất Oát Phẳng Data Kì Mệnh Kéo Kỉ Data Mạch Dòng Tỉnh SQL Báo Oanh Cực Relational Data App Òa .
