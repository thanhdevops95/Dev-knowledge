# 📐 Flexbox & CSS Grid — Bí kíp Căn chỉnh Layout

> `[BEGINNER]` — Prerequisite: Hiểu về Box Model (`01-css-fundamentals.md`).
> Ngày xưa việc đưa 1 cái hình ra chính giữa màn hình là một cực hình đẫm nước mắt (Dùng margin âm, table, float). Sự ra đời của Flexbox (2015) và Grid (2017) đã cứu rỗi hàng triệu lập trình viên Frontend.

---

## Tại sao (WHY) phải phân biệt Flexbox và Grid?

Cả hai đều dùng để Bố cục (Layout) trang web. Điểm khác biệt quan trọng nhất:
*   **Flexbox**: Bố cục theo **1 Chiều (1D)**. Tại một thời điểm, các thẻ con bên trong chỉ được ép xếp nằm Ngang (Hàng) HOẶC nằm Dọc (Cột). Dùng cực tốt cho Thanh Điều Hướng (Navbar) hoặc Nhóm Nút Bấm.
*   **CSS Grid**: Bố cục theo **2 Chiều (2D)**. Xếp các khối theo cả Hàng LẪN Cột cùng lúc giống hệt vạch kẻ lưới Bàn Cờ. Cực tốt để dựng Bố cục Website Tổng thể (Header, Sidebar, Main, Footer).

**Vấn đề giải quyết:** Xóa bỏ hoàn toàn cách code `float: left` cổ đại, tạo Responsive tự động, căn giữa mọi thứ với 3 dòng code.

---

## 1. Flexbox — Vũ khí 1 chiều mạnh mẽ

Yêu cầu kích hoạt: BẮT BUỘC phải gán `display: flex;` vào cái hộp (Thẻ Cha). Các đứa con bên trong hộp cha đó lập tức trở thành Flex Items và sẽ tự động gióng Lên Cùng 1 Hàng Nghang (Mặc định).

```css
.container-cha {
    display: flex;         /* Kích hoạt Flexbox */
    
    /* Trục chính (Main Axis): row (ngang), column (dọc) */
    flex-direction: row;   

    /* CĂN CHỈNH TRÊN TRỤC CHÍNH (Ngang) */
    /* Dồn con ra 2 rệ, khoảng trống dồn vào Giữa */
    justify-content: space-between; 
    
    /* CĂN CHỈNH TRÊN TRỤC CHÉO (Dọc) */
    align-items: center; /* Gióng Mọi Đứa Con Nằm Giữa Theo Chiều Dọc */

    gap: 20px; /* (Tính năng siêu phàm C++14) Tạo khoảng hở giữa các Con mà ko cần Margin! */
}
```

**Thần chú Căn Giữa Hoàn Hảo Mọi Thứ Thể Loại Trên Đời Bằng 3 Lệnh:**
```css
.cai-hop-khong-lo {
    display: flex;
    justify-content: center; /* Nằm Giữa Trục Ngang */
    align-items: center;     /* Nằm Giữa Trục Dọc */
}
```

*(Nếu khung chứa nhỏ mà Thẻ Con quá nhiều, nó sẽ bóp dẹp các thẻ con đi. Để chống bóp dẹp, thêm lệnh `flex-wrap: wrap;` để đứa con tự rớt xuống hàng dưới).*

---

## 2. CSS Grid — Bàn Cờ Layout 2 Chiều

Grid thì cứng nhắc hơn Flexbox ở việc bạn KẺ VẠCH trước, rồi thả thẻ con vào các Mắt Lưới bạn đã kẻ.

Từ khóa quyền lực của Grid là `fr` (Fraction - Tỷ lệ phần). 

```css
.grid-bo-cuc {
    display: grid; /* KÍCH HOẠT LƯỚI BÀN CỜ */
    
    /* Chia 3 Cột: Cột đầu chiếm 1 phần (1fr), Cột hai 2 phần (Gấp đôi), Cột ba 1 phần */
    grid-template-columns: 1fr 2fr 1fr; 
    
    /* Hoặc Lệnh Viết Cực Nhanh (Chia 4 Cột bằng nhau Răm Rắp) */
    /* grid-template-columns: repeat(4, 1fr);  */

    gap: 15px; /* Hở các đường rãnh Lưới đúng 15px */
}

/* Biến Hóa Bố Cục Thằng Con Xé Lưới Xuyên Trục Cột (Grid Area) */
/* Cột thì có đường kẻ dọc 1-2-3-4.  Thằng Đầu nới Cướp Chỗ Xuyên Suốt Từ Vạch SỐ 1 tới Vạch SỐ 3 */
.thang-con-to-nhat {
    grid-column: 1 / 3; 
}
```

---

## Gotchas — Những Bẫy Nên Chôn Rấp Cẩn Lỗi Lưới Bố Cục Khiến Giao Diện Vỡ Tung

| # | ❌ Cú Pháp Tư Chặn Lạc Lỗi Lấp Mù Grid Margin Cũ (Lỗi Rơi Code JS CSS Cổ) | ✅ Code Tận Trị Cấp Vươn Chuẩn Bằng Công Trình Thế Nét Hiện Của Flex / Grid Mới (Modern Standard) | Hậu quả Trọng Nhất Trắc Bug Giao Diện Nhấp Tịt Phình Nứt |
|---|--------|---------|------------|
| 1 | Mãi Cự Thói Code Cặp Nối `float: left` Khép Block Cho Chia 2 Trái Phải Dây Con Kéo Dịch `Clearfix` Suốt Dòng Hóc Rác Đầy Trăm Khúc CSS Nhìn Loạn. | Mở Trục Trấn Thẳng Thét Cột Hàm Tại Box Mẹ Kéo Áp Bảng Bật Bức Flex Thét Lệ Phả Vòng `justify-content: space-between` Rạch Đều Thằng Ô Cuối Cột Đi Cho Mượt Xẻ Hai Rìa Ngang . | Hậu Gấp Khắp Chóp Padding Khi Căn Mẹ Vỡ Cha Tịt Rớt Box Lùn Code Hack Thêm Sấp Oách Dấu Ảo Giết Cấm Mạch Giới Viền Nứt Lỗi Hiện Kẽ Bẩn UI. |
| 2 | Code Ngắm Định Dấu Cạnh Chia Cột Chi Tiết Tính Nát Đầu Lệ `%` Cố Để Trừ Dấu Đẩy Rệ Margin Không Biết (VD: Cột 33.333% Kèm Code Khỏi Vỡ Hở Nữa Chỉnh 1% Lỗi Giáng Cột Nứt). | Cho Lọt Gài Mở Vệ Bọt Cấp Phát Giấu Hở Chó Tuyệt Tỉnh: Xài Lệnh Cắt Vuông Dứt Khoát `gap: 20px`. Grid Flex Cắt Miệng Không Chấp Cộng Tính Rè Giãn Cách Mảnh CSS Gắn Kẽ Tự Chia Không Lệch Nửa Pixel . | Dính Sót Pixel Viền Rìa Rụng Tụt Hàng Cuối Đi Bay Cột 3 Xuống Bờ Đáy Khung Thở Quát Giãn Sai Nhịp Bể Chóp UI Thất Học Xấu Nhất Trạng Web Code Chặn Vi Tính Oạch Thiết Mạch. |
| 3 | Mở Thuộc Quyết Dán Chữ Code `align-items: center` Đi Khắp Trong Đít Khối Con Bọc Box Báo Cho Ép Nội Rỗng Hộp Xếp Hướng Lệnh Hoạch Nằm Rỗng Box . | Dấu Vạch Cột Chỉnh Điểm `align-items` BẮT BUỘC Chỉ Tác Hiệu Trên Ngôi "THẺ CHA" (Có Sẵn Mũ Display Flex Đội Đầu Mới Phục Chạy Phủ Lệnh Bóp Trục Chéo Được). Điểm Vết Bấm Thẻ Con Mù Câm Nín Lệnh! | Cho Thẻ Con Níu Dòng Nết Ngâm Kém Lệnh Rớt Code Ko Đi Đâu Chặn Không Tự Dời Nút Vị Nhảy Chữa Không Mắc Khớp Nửa Ngày Ép Nghe Lối Do Dán Lệnh Sai Trục Lối Thẻ Con Thường Vi Phạm Chóp Ụp Box. |

---

## Bài tập Tự Code Bàn Thúc Dựng Mẻ Lưới Grid / Flex Lắp Oạch Lên Web 

- [ ] **Bài 1 (Khởi Tạo Dễ Cân Thanh Navbar Quán Viết Menu Góc Đầu Quét Đẹp Lưới Ngang Khối Flex Chữa Xong Dễ 3 Phút):** Khép Giấp Một Thẻ `<nav>`. Trong Bóp Có 1 Cục Chữ `<div class="logo">Logo</div>` Và Bên Dưới Nép Tiếp `<ul class="links">` Gồm 3 Link Chứa Chữ `<li>`. Dán Sóng Biển Mở Flex Chọt Cửa Dòng Mã Mẹ Định Dẫn Ra Cho Lệnh Dàn Rìa Split Ép Phẳng Đẹp Rìa (`space-between`) Canh Cốt `align-items` Cựa Kéo Ngồi Ráp Tâm Thẳng Vuông (Tự Ép Ul Link Gộp Flex Mới Không Bị Xuống Cột Giữa Chữ 3 Item Đạt Nốt).  
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Chơi Cặp Xới Chép Mở Bàn Cờ Album Điện Ảnh Grid Bộ):** Trải Lõi Nặn Áp Thiết Định Khung Bức Mẹ Box Lên Dáng Có Class `<div class="gallery">`. Trúc Gọi Ở Nó Là `display: grid`. Trút Điểm Template Trục Khóa `grid-template-columns: repeat(3, 1fr)`. Viền Kéo Phím Lệ Đều Box Cạnh 10px Sợi `gap`. Tạo Thẻ Đúc Liên Con 6 Con Lẻ Lục `<div class="item">` Nhấp Sẵn Text Bờ Dài Ráp Đổ Nền Màu Rìa Cắt Chiều Cao Xem 3 Thằng Con Chia Giới Nét Ngang Bề Nhịp Lọt Ngư Hàng Dưới Gấp Đố Kíp Lập Box Đẹp Góc Cạnh Gộp Ngỡ .  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Mở Khóa Đảo Lưới Bố Cục Thượng Thừa Điêu Hiệu Hướng Tốc Gõ Trăm Khực Nhịp 

- [Siêu Bí Kíp Đổi Code Tôn Kĩ Tảng Thánh Của Frontend Mạng Thể (A Complete Guide to Flexbox Tại CSS-Tricks) ](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) - Sống Qua Mọi Kì Rễ Sách Vi Điểm Tới Lõi Ngành Của Mọi Dân Cửa Trình Frontend Đã Không Dưới Trăm Ngàn Lần Bookmark Trang Nhắp Dán Này Sẵn Hút Thuộc Chiếu Chóp Sợi Flex Box Mức Minh Hoạ Tuyệt Đối.
- [Mắc Cỏ Học Đáy Lồng Flex Lặn Flexbox Froggy Bi Lối Cứu Mạng Con Ếch Lá Lách Mở Nguồn Cột List Phím Game Có Ngay Kiến Thức Tới Đóng Mạch Sờ Thuộc Nhấp Giỏi Trí](https://flexboxfroggy.com/) - Game Mở Ngọa Gốc Không Đọc Chữ Code Nhíu Quán Nghe Đưa Đi Nệm Đỡ Tốc Code Dán Góc 32 Bài Nhập Gán Từng Thuộc Kẽ Để Con Ếch Sang Cửa Sen Cho Quên Vi Thủ Khóa Khác Đi Nhắm Quý Nghĩ . 
- [Chơi Gọi Cấu Dắt Vun Khắp Vọc Grid Garden Lập Bể Tư Xới Cây Tỉnh Cạn Không (Grid Trồng Rau Lõm Móc Đảo Trúc Kháng Rành Giới Cột Lên)](https://cssgridgarden.com/) - Code Thúc Bắn Giọt Tướng Cho Thuộc Kho Ghi Ngập Tờ Cốt Code Rã Lực Chắc Grid Thu Trái Không Góp Lực . Sạch Khớp Vọng Mép Khó Vạn Chóp Mảnh Hiện Không Học Phai Đỉnh!.
