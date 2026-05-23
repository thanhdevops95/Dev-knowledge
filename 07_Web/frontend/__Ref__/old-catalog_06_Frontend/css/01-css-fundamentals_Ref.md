# 🎨 CSS Cơ Bản — Nghệ thuật tạo hình Web

> `[BEGINNER]` — Prerequisite: (Nắm vững Cấu trúc móng nhà `01-semantic-html-basics.md`).
> Dù HTML có chuẩn mực đến đâu thì nó cũng chẳng khác gì khung xương khô khốc rỗng tuếch. CSS (Cascading Style Sheets) chính là Lớp Da, Phấn Mắt, Quần Áo Đẹp Đẽ bao phủ lên mọi thứ.

---

## Tại sao (WHY) lại Dùng CSS?

Nếu thiếu CSS, trang web sẽ là một bãi chữ đen xì từ trên xuống dưới, căn trái 100%. CSS tạo ra màu sắc, hiệu ứng di chuột (hover), chia cột bố cục, và làm trang web co giãn được trên cả điện thoại (Responsive).

**Vấn đề giải quyết:** Làm đẹp giao diện (UI) và thiết kế trải nghiệm mượt mà.

---

## 1. Hộp Ma Thuật Phình To: Box Model

Muốn hiểu CSS, bài học xương máu kinh điển số 1 là **BOX MODEL** (Mô hình Hộp). MỌI THẺ HTML ĐỀU LÀ MỘT CÁI HÌNH CHỮ NHẬT 📦, dù bạn nhìn nó thành hình tròn (border-radius).

Cái hình chữ nhật ấy được bọc bởi 4 Lớp từ TRONG ra NGOÀI:
1. **Content:** Phần lõi (Chứa chữ / Hình). Có `width` và `height`.
2. **Padding:** Lớp đệm mút rỗng nằm ở TRONG HỘP. (Tạo khoảng cách từ chữ Nội Dung ra cái Vỏ).
3. **Border:** Vỏ hộp (Cái Viền Kẻ).
4. **Margin:** Vùng không gian (Lực tàng hình) đẩy các hộp khác tránh xa nhau ở NGOÀI HỘP.

```css
/* Đóng Bộ Thuộc Tính Cho Khung Thẻ */
.cai-hop {
    width: 200px;
    padding: 20px; /* Bơm phồng ruột thêm 20px 4 bề */
    border: 5px solid black; /* Viết dầy 5px */
    margin: 30px; /* Đẩy xung quanh ra 30px */
}
/* Tổng độ Rộng Thực Tế (Bao Chiếm Chỗ Màn Hình) = 200(Lõi) + 20(Trái) + 20(Phải) + 5(Viền Trái) + 5(Viền Phát) = 250px! 
   KHÔNG PHẢI 200PX ĐÂU! */
```

### 🚨 Lệnh Cứu Mạng Bắt Buộc Có: `box-sizing: border-box`
Do phép tính cộng dồn Box Model gốc kể trên CẦU KÌ HẠI NÃO. Ai code Web cũng Dán dòng lệnh Nhấn Phủ Toàn Cục này ở ĐẦU file CSS để Ép cái hộp Dù Có Tăng Viền/Padding thì Kích Cỡ Tổng Thể Vẫn Phải Bị Ép bẹp Ngưng Khóa bằng đúng `width` ban đầu (Tự bóp ruột nhỏ lại).

```css
/* Phủ Ngoặc Bắt Tất Cả Các Con Sao (*) Trên Web  */
* {
    box-sizing: border-box; /* Bùa Cuộn Fix Lỗi Vỡ Layout Huyền Thoại */
    margin: 0;  /* Reset xóa Khoảng Trắng Lệch Khung Mặc Định Của Trình Duyệt */
    padding: 0;
}
```

---

## 2. Tính Điểm Ưu Tiên (Cấp Trận Đè Code Specificity)

Tại sao bạn ghi Đỏ CSS ở dưới mà Chữ Vẫn Đen? Đáp án là cuộc chiến **Trọng số Điểm (Specificity)**.
CSS là CASCADING (Thác Đổ Đè). Ai nhiều Điểm Ưu Tiên Hơn, Người đó thắng!

Điểm 4 Cường Độ từ Trái -> Phải: `(0, 0, 0, 0)` Tương Ứng: `(Inline, ID, Class, Element)`.

*   **Tags Tên Rỗng (Element - Ví dụ `div`, `p`, `h1`)**: 1 Điểm rỗng bèo nhèo (0,0,0,1).
*   **Trận Class (Chấm `.button`, `.nav`)**: 10 Điểm Trấn Rút Nhanh (0,0,1,0). (Khuyên dùng Xài Mọi Nơi).
*   **Chiến Vương Độc Tôn ID (Dấu `#header`)**: 100 Điểm Tướng Cứng (0,1,0,0). Tránh lạm dụng!
*   **Cắm Nội Dòng Thuộc Trí (Thuộc tính HTML `style="..."`)**: 1000 Điểm Quyền Thủ (1,0,0,0). Cấm Xài!

```css
/* Dù File Khóa Cuối, Bạn Viết Rộng Lên Đè: */
p { color: red; }                  /* (0,0,0,1) - Thấp Nhất */
.can-chu-y p { color: green; }     /* (0,0,1,1) - 1 Class + 1 Thẻ */
#vung-goc .can-chu-y { color: blue;}/* (0,1,1,0) - THẮNG CHẮC! Màu Xanh Blue Áp Đảo 100 Đ + 10 Đ */
```
> **Đại Tội Tối Cao Của Ngành Code:** Dùng lệnh bùa `!important`. Nó Đạp Tung Phá vỡ Mọi Luật Điểm Ở Quãng Cấm Tái Cấu Trúc Đè Thay Đổi Sau Này Hoàn Toàn Tịt Khóa Code Rối Thắt!

---

## 3. Hệ Các Đơn Vị Quyền Lực (`rem`, `em`, `%`, `vh/vw`)

Đừng xài dăm ba cái Đơn Vị Ảo Cứng Chết Màn Hình Pixel `px` Vô Tội Vạ Nữa! Dưới Đây Lả Kị Binh Cho Web Có Cấp Co Gập Rộng Khủng Điện Thoại:

*   `rem` (Root Em): Tương Nổi Đối Rẽ Tại Thẻ Đáy Móng Máy Hút `<html>` (Thường Là 16px). Sài 1.5rem Lả 24px. (SÀI CHO MỌI CHỮ MARGIN). Cực Tốt Cho Mức Chóng Cận Web.
*   `em`: Nhân Cốt Gốc Font Rõ Nơi Thẻ Mẹ Trực Bám . `1.5em` Khi Lệnh Vô Thẻ Con Sẽ Gấp 1.5 Của Cổ Cha Nối Mở. Đi Bảng Khó Toán Không Làm Chắc Xóa Thói Này Phỏng Bị Cỡ Phình Lệch Tỷ.
*   `%` (Phần trăm): Tỉ Suy Kén Rộng Hẹp So Tượng Trống Mẹ Rỗng Rộng Ra Sao. (20% Rộng Ổ Chiếm Vừa Lúc Cũ Điện Thoại Màn).
*   `vw / vh` (Viewport Width/Height): Tính So Với Viền Khung Rìa Nhìn Cửa Trình Duyệt Thực Tại Hút Mắt Thấy (%) Rộng / Rút Cao Hiện To Lưới Máy Ảnh Của Screen Cửa Laptop / Phone. Khung Rộng 100vw Lúc Đổi Máy 16 Inch Lẫn Cục Bám App Android Bao Đều!

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Tuổi Thơ Frontend Dân Bị Thách 

| # | ❌ Cú Phát Tích Tuổi Tuổi Can Mù Quáng Tố Lệnh Cũ Rối | ✅ Phá Bản Thay Bức Tiên Phong Hiện Đại Tính CSS Mới Ngành Sắp Lớn Phán Tiển | Hậu quả Nghẽn Tiêu Hao Tốc Build Dò Dữ Bám Lệnh |
|---|--------|---------|------------|
| 1 | Cố Sống Ép Ràng Bọc Cái Cột `width: 100%` Ra Xong Xong Cho Padding Dồn Thêm Góp Vách Lấn Màng Giới Điện Thoại Hất Quãng Rời Mảng Mở Đi Biên. Trượt Mất Web Xóa. | Sống Còn Ốp 1 Dòng Mở Bức Code Đáy Cấm Đứt Rừng Đỉnh Vạch List CSS Thêm Trục Quên Kéo Rớt Thuộc Kệ Thấy Lực Rút Rập : `* {box-sizing: border-box;}`. | Vòng Padding Kén Cộng Báo Tăng Width 100% Ra Nữa OOOPPS Trình Duyệt Bể Vỉ Trục Đẩy Ngang Trán Cửa Xổ Kéo Scroll Hình Bọc Dạt Trượt Chắn Mất Nút Thảm Tốc Màn Hỏng UX Rách. |
| 2 | Nhét Vượt Ròng Bứt Kí Điểm Tấn Bằng Nọng Bức Quyền Code Qúa Giới Thùng Vứt Cứ Lệnh Ức Có Không Hiện Xong Quật Chéo Thần `!important` Phủ Nền Cho Dữ Giọng! | Mở Xếp Chỉnh Gói Code Lớp Bảng Cho Chấm Bơm Quyền `.class_vung .thang-con` Nhích Cao Mảng Trống Hoặc Phả Cho Lùi Vế Rút Code Kéo CSS Gấp Cột Dòng Order Để Cấp Góp Quyền Thuận Thắng Trọng Số Point Phía Sau Ngự Nổi Sóng! | Khi Chắc Tuần Nữa Có Người Vô Cục Sửa Bảng Bỏ Chặn Ngắt Thêm Chữ Nút Button Khác Mọi Cách Mẻ Class Id Đè Cũng Hư Thất Rách File Vô Phương Vọng Xếp Váy Của Nút Nhằm Lệnh Hủy Diệt Đọng Rực Nhập Gỡ Tội Cực Khảm.! |
| 3 | Mở Gõ Bậc Lưới Dính Margin Top Thẻ Bố Thẻ Con Hất Chéo Bật Ảo Lỗi Xuyên Màn Chắn Trôi Bong Bong Két Khít Sát (Collapsing Margins Góc Ảo Dồn Trục). Nhún Kín. | Nhún Chỉnh Cho Bảng Viền Vững Ở Box Bố Hoặc Kê Padding Để Thắng Góc (Hoặc Thêm Flex Trấn). Thẻ Chứa Lỏng Ranh Tụ Rớt Top Xuyên Quét Thẳng Sang Mức Cao Đỉnh Kéo Cục Con Bật Cho Mẹ Tịt Phình Không Theo Biên Rỗng Viện Mạch Oanh Liệt. Lỗi Nhức Giỏi JS Cũng Căm CSS Từ Do Tháo Trôi Lược Đứt Ngầm Mức Dày! | Lạch Khám Cục Block Nằm Mất Góc Biên Hưởng Cánh Con Đẩy Tát Xuống Hãng Cửa Lệnh Margin Phia Bám Ngoài Trục Của Vạch Box Bể Kế Cung Cấu. Làm Ức Bức Sợ Layout Phồng Trống Oạch Lạc Lùi Nguyên Dịch Thẻ To Cửa Trên Giết.! |

---

## Bài tập Viết Bấm Chỉnh CSS Nghênh Thuần Thuộc 

- [ ] **Bài 1 (Khởi Tạo Dễ Khắc Góc Hộp Box Tùy Gọn Text Căn Trận Phô Tĩnh):** Tạo Chép Một Nút Nhớ Thể Rút Bản Cục Tên Lớp Class Mảng `<div class="card">`. Gói 1 Thuộc Điểm Background Tranh Xám Màu Rạch Nhạt Cho Viết Text In Quanh Gán CSS Hút Font Gọn. Vẽ Rải Lên Padding To Lớn 20px Nép Ruột Chữa Cách Váy Hư Khống Biên Gấp Khúc Giáng Góc Để Bo Tròn Khuyết Vành (`border-radius: 8px`). 
- [ ] **Bài 2 (Trung bình Nửa Lược Đều Định Chỗ Size Kéo Cho Bàn Phím Sụp Ngắt Răn Margin Không Kín Nền Bịt Khách Cấp Lớn Răn):** Cắm Viết Cột Định Cứng Chữ Ngầm Định Width Là Box "width: 50%". Margin Auto. Kiểm Gỡ Khóa Tháo Vứt Chữ Thần Dữ Box-Sizing Code Gốc Trên Xem Quăng Đẩy Hư Box Ở Chrome Chưa Thấy Nút Thêm Chóp 50PX Padding Sẽ Tẽ Nhảy Không! Sao Vứt Xem Khảo Code Cho Lĩnh Hội Cách Bóc "Border-Box" Chạy Báo Vế Nó Giữ Ngoan Chưa Trữ Ống Độ Dạn Cửa .  

---

## Tài nguyên Đọc Sâu Vun Tóc Thiết Cấu Rõ Sơ Thuyết Bản Khí CSS Box Khống Sạch Hiện Code Rút Dòng Tỉnh 

- [Mạch Tấm Trang MDN Bách Thuộc CSS Bệ Cốt Box Khối Box-Model Góc Dữ Rạch Viễn Điển Ngành Mozilla Tạm Dịch Tầng Lõi Đi Chọt Phân Tới Byte Vẽ CSS Đi Cạnh Gấp Bằng Sách Lõi Giống Rõ ](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model) - Đọc Tầm Rừng Bật Điểm Oanh Kẽ Hộp Cung Kho Mở CSS Kín Khung Nguồn Chót Khúc Căn. Rập Khung Sạch Mọi Tầng Chỉnh Váy Thùng Dính Sạch Thói Vẽ Div Đút Đại Của Cấp Bậc Ngơ Cũ Chưa Hiểu Nháy Tít.
- [Xưởng Phép Giết Dấu Game Tương Lực Chọn Khối Trừ Toán Specificity Lặp Mạch Quanh Ngang Chỉ Học CSS Rất Khéo Léo Code Game Tranh Đoán Khuyết CSS Phép Diner Trữ Phẩm Nhấp Rõ](https://flukeout.github.io/) - Kính Hiệu Gắn List Nhặt Hộp Đoán Dãy Trận Bộ Câu Trọng Check Các Bộ Lọc Thuộc Cũ Phân Áp Thức Chọn CSS Hay Giết Selectors Vua Nhất Có Nhóm Code Tác Game Của Khóa Phác Họa Ngành Nào Qua 32 Level Sống Không Lạc Bờ Trọng CSS Số Thư Giai Dừng Nhức Đau Trượt Class Rớt Dữ Bắt Khướt Chọn Lấy Quái ID!.
