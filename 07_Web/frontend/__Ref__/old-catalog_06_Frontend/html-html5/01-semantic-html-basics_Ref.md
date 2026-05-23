# 🧱 Semantic HTML — Nền tảng cấu trúc Web

> `[BEGINNER]` — Prerequisite: Hiểu Khái niệm Cơ bản về thẻ mở `<tag>` và thẻ đóng `</tag>`.
> HTML không phải ngôn ngữ lập trình, nó là Ngôn ngữ Đánh dấu Cấu trúc (Markup). Dùng Semantic HTML giúp bot của Google (SEO) và Người dùng khiếm thị (Screen Reader) có thể "đọc" được web.

---

## Tại sao (WHY) phải dùng Semantic HTML?

Thời xa xưa, tất cả mọi cục khối trên website đều được Dev nhét vào trong thẻ `<div>` (Gọi là "Div Soup"). Kết quả: Website chạy hiển thị được, nhưng mù tịt về ngữ nghĩa. Trình đọc màn hình cho người khiếm thị đọc 10 cái div giống nhau không biết đâu là tiêu đề, đâu là nút bấm. Google Bot vào web không biết đâu là bài viết để lấy đưa lên Top 1 kết quả tìm kiếm.

Từ HTML5 ra đời, Semantic (Ngữ nghĩa) ép bạn dùng ĐÚNG THẺ vào ĐÚNG VIỆC CỦA NÓ.

**Vấn đề giải quyết:** SEO (Search Engine Optimization), Accessibility (a11y - Khả năng tiếp cận người dùng khuyết tật).

---

## 1. Cấu trúc Khung xương của Phân trang (Landmark Tags)

Một trang Web HTML5 chuẩn mực luôn được chia vùng thành các khối chức năng. 

```html
<!DOCTYPE html>
<html lang="vi">
  <head>
    <meta charset="UTF-8">
    <title>Cấu Trúc Trang Phổ Biến Của HTML5</title>
  </head>
  <body>
    <!-- 1. Header: Chứa Logo và Điều Hướng -->
    <header>
      <h1>Website Của Tôi</h1>
      <nav>
        <ul>
          <li><a href="/">Trang chủ</a></li>
          <li><a href="/about">Về tôi</a></li>
        </ul>
      </nav>
    </header>

    <!-- 2. Main: Thẻ Đặc Biệt Quan Trọng (Chỉ Được Phép Xuất Hiện 1 Lần mỗi trang) -->
    <main>
        
      <!-- 3. Section: Khối Chuyển phân tách từng Vùng Lỗi / Nhóm To -->
      <section id="features">
        <h2>Phần Tính Năng Sản Phẩm</h2>
        <!-- 4. Article: Có Thể Được Cắt Nhổ Mang Đi Nơi Khác Chạy Độc Lập Mới Hiểu Được (Bài Đăng Tức Mạng Xã Hội, Báo, Card) -->
        <article>
          <h3>Tính năng Siêu Cấp 1</h3>
          <p>Nội dung mô tả tính năng...</p>
        </article>
      </section>
      
    </main>

    <!-- 5. Aside: Rìa mép (Thường dùng cho Sidebar quảng cáo, Hoặc Bài Liên Quan) -->
    <aside>
      <p>Quảng Cáo Dịch Vụ Mới...</p>
    </aside>

    <!-- 6. Footer: Thẻ chốt trang -->
    <footer>
      <p>&copy; 2024 Bản Quyền Tôi Giữ Trọn.</p>
    </footer>
  </body>
</html>
```

---

## 2. Text Semantic – Viết chữ cho có Tôn Ti Trật Tự

Thẻ không chỉ giúp định dạng chữ Bôi đen, In nghiêng mà nó mang theo sức mạnh Báo Hiệu Tâm Lý Chữ.

*   `<strong>`: In đậm mang ý nghĩa QUAN TRỌNG, BÁO HIỆU MẠNH MẼ. (Đừng dùng thẻ `<b>` cũ kĩ chỉ đơn thuần là Bôi Đen rỗng tuếch).
*   `<em>`: (Emphasis) In nghiêng mang tính Nhấn Giọng Đọc. (Thay cho thẻ `<i>`).
*   `<mark>`: Highlight bôi Bút Đuôi Chân Vàng.
*   `<blockquote>`: Trích dẫn Nguyên Câu Nói Từ Báo Khác / Người Khác. Đính kèm thuộc tính `cite="url"` để SEO biết bạn trích từ đâu.

---

## 3. Thẻ Tương Tác (Interactive Elements) – Ranh Giới Sống Còn

Rất nhiều Lập trình viên JavaScript (React/Vue) thích lấy thẻ `<div>`, đắp CSS cho nó nhìn giống cái Nút (Button) rồi Gắn Click... Đây là tội ác Tày Đình Của Accessibility!

### Nút Nhấn Chức Năng (Nút Kích Hoạt Javascript/Form)
Phải Dùng `<button>`. Trình đọc Màn hình tự biết để hô to từ "NÚT!" cho người khiếm thị nhấn `Space/Enter`.
```html
<!-- KHÔNG ĐƯỢC LÀM: <div class="btn" onclick="submit()">Xác Nhận</div> -->
<button type="submit" aria-label="Xác Nhận Đơn Hàng Của Bạn">Xác Nhận Đặt Hàng</button>
```

### Nút Đi Link Sang Trang Khác
Phải Dùng `<a>` (Anchor Tag).
```html
<a href="https://google.com" target="_blank" rel="noopener noreferrer">Mở Tại Mạng Khác Khung</a>
```
*(Cần mang đủ `noopener` để Không Vướng Lỗi Bị Hack Rút Lấy Cửa Sổ Bố Mẹ Bên Kế Khi Mở Tab Dùng Mới)*

### Ảnh Hình Nhúng Lắp (Images)
```html
<!-- Nếu Ảnh Bị Lỗi Liệt Bỏ Xóa Không Hiện Rơi Ra Thay Mạng Cụt: Thì BẮT BUỘC Hiện Chữ alt Chép Giải Nghĩa Lấy Lại! -->
<img src="con-meo.jpg" alt="Con Mèo Màu Đen Nhảy Trong Hộp Giấy" loading="lazy" />
```

---

## 4. Dẫn Thiết Nhập Biểu Mẫu Dữ Liệu Forms 

Mọi thứ bạn Điền Trữ Phải Nhốt Vào Cặp Bộ Ô `<form>`. Dùng Ngay Bộ Cặp: `<label>` Và `<input>` Khớp Nhau bằng chữ `id` Để Khi Mọi Người Nhấn Vô Tên "Chữ" Góc Mép Của Ô Chứa Vẫn Sáng Click Trực Tiếp Dính Bắt Nhào Vô Nhập Vào Input Kế.

```html
<form action="/login" method="POST">
    <!-- LABEL RẤT CẦN THIẾT. CHỈ MẶT ĐẶT TÊN CHO ID NÓ THEO DÕI NỐI FOR -->
    <label for="username">Tên người dùng:</label>
    <input type="text" id="username" name="username" required placeholder="Nhập tên nhé...">
    
    <label for="pwd">Mật mã Khóa:</label>
    <input type="password" id="pwd" name="password" required>
    
    <button type="submit">Đăng Nhập Ngay Cửa</button>
</form>
```

---

## Gotchas — Những Bẫy Nên Chôn Rấp Cẩn Khoanh Giúp Website Rớt Khung SEO Văng Trình 

| # | ❌ Cú Pháp Xưa Sai Cổ Lỗi Nhận Thức Chắn Mạng Cũ | ✅ Chuẩn Semantic Đinh Hướng Ngành Code JS Code Nặng React | Hậu quả Mất Bệ SEO Của Việc Tùy Tiện Vứt Đi Dấu |
|---|--------|---------|------------|
| 1 | Lạm Dụng Chỉ Sài Viết `<div>` Cục Đống Suốt Mảng Thay Chức `<section>`, `<footer>`, `<nav>`. | Bốc Đặt Bộ Trúng Tấm Gọi Hồn Layout Tag Trắng `main`, `aside`, Bộ Khớp Theo Mọi Mảng Web Chuẩn App Mạng WC3 . | Gã Khổng Lồ Máy Tìm Kiếm Của Google Quẹt Rào Chống Trả Ngơ Không Hiểu Ai Là Tiêu Điểm Code Nội Đất Tự Oạch Rank Xếp Số Nằm Lóp Trắng Trang Giới Cuối Mạng Rút List Thua . |
| 2 | Code Cột Phân Cấp Dòng Chữ Nháy Hệ Title Dữ Heading H1 Đầy Cả Quá Dày Xé Điểm Chắn Ngang Ngược Số (H2 Sang Thẳng Lọt H4 Bỏ Bước). | 1 Website Đúng 1 Con `<H1>` Tỏa Trang Đỉnh Nhất. Xong Cấp `H2` Đi Liền Xuống Cấp Gồm Mẹ Cha Không Bỏ Hẫng Lược Bật Dây Nhảy `H3` Cấp Xấp . | Trình Robot Crawler Quát Bot Thấy Kiến Trúc Hỏng Quá Buồn Mệt Rụng Sớm Khỏi App Nghẹn Đọc Đổ Trình Đọc Người Bi Lỗi Lọt Nhức Tai Lái Trật Lối Mạch Quá Trình Nhòm Không Mượt Logic Mắt App . |
| 3 | Mặc Kệ Lời Ôn Từ Nghĩa Đi Cho Thẻ Img Ảnh Trống Tính Chất Rỗng Chữ Khong `alt=""`. Nhấn Nút Chẳng Có Label Ngữ . | Ốp Buộc Ép Gõ Quên Sẽ Lỗi Code Nặng Từng Kí Từ Mô Tả Cực Chi Tiết Ráp `alt` (Chữ Trục Mù Đọc Chức). Phải Cắt Có Ráp Gồm Hình . | Kẻ Nghèo Sức Nhìn Hay Người Nhìn Ảo Screen Reader Nghe Quát Xót App Kêu Nghẽn Tiếng Mất Nét Trống Gây Quáng Khi Mua Hàng App Bị Cấm Vỡ Luật Accessibility Thiếu Đậm Điểm . |

---

## Bài tập Tự Gõ Luyện Thay Nếp Div Cũ Còi Hướng Cao Tinh Gọn Khung Gõ 

- [ ] **Bài 1 (Khởi Lớp Màng Phủ Lại Mạch Mắc Áo Blog Cũ Mới):** Nắm Vào Khí Bịt Đặt Vùng Trang Một Nét Web Đọc 1 Bài Nghỉ Báo Khung Chứ Đầu: Chặn Nhét Xóa Bụng Chữ Title Cho Vô Thẻ `header`, Viết Thể Bám Thân Chính Cuộn Dùng `<main>`. Trong Rốn Giữ Kìm Bài Tĩnh Độc Giữ Xái Thể Trận Mức Xé Đoạn Kíp `<article>` (Để Title Bài Dòng Góc Header Đẹp Cho Mất Gỡ Khác Đi Thẻ Không Khớp Dò ).  
- [ ] **Bài 2 (Trung bình Check Chạy Check Trắc Web Sạch Accesibility Form Tĩnh Tốt Nhất):** Đổ Lấp Cặp Bọc Bức Form Tạo Phím Mở Mẫu 3 Chiếc Góc Cho Lịch Đặt (Chứa Lấy Có: `<input type="date">`). Lưu Đậm Cột Tên Thuộc Đăng Đi Có `label` Cho Ô Chữ Lấp Móc Sạch Vòng Nối Lên Chồng id="lich_book". Rọi Mắt Chuột Bấm Coi Đúng Tên Bảng "Ngày Hẹn Tới:" Khớp Chỉ Xuống Ngôn Box Lấp Loé Dán Vào Ô Gõ Trống Cần Khớp Ngay . 

---

## Tài nguyên Đọc Sâu Vun Tư Cấu Ráp Móng UI 

- [Kho Mạng Mozilla Góp Tầng Tri Cực Cao MMDN (Tổ Phát Sóng Chuẩn Ngành Đáy Thấu Web Nhất Lõn 1 Nghề Dev)](https://developer.mozilla.org/en-US/docs/Glossary/Semantics) - Sức Sống Từ MDN Web Đủ Khẳng Mạch Để Nôi Code Các Thẻ Semantic Không Giao Đỉnh Bỏ Sót Tít Một Tầng . Lớp Viền Sách Gối Giầu Này Căn Sáng Giữ Nghề Chơi.
- [Mức Bật Vi Web Dành Chi Người Vất Accessibility Kì Tích Check Lỗi Bẳng Bảng HTML (A11y Gốc Test Tools)](https://webaim.org/) - Trang Web Tổ Sợ Lỗi Thuần Nhắc Thiết Thiết Trọng Tịch Lần Đánh Web Thiếu Viền Bóp Các Thẻ Hình Sốc Màu Và Đồ Semantic Chưa Khớp Phân Nghĩ Đáo Thuộc. Đo Chạy Cảm Thấy Mạng Tốc Check .
