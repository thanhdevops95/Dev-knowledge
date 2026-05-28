# 📜 DOM Manipulation Basics — Tương tác giao diện với JavaScript

> `[BEGINNER]` — Prerequisite: (Nắm vững Cú pháp JS `05-Languages/javascript/05-js-cheatsheet.md` và thẻ HTML).
> JavaScript (JS) ban đầu sinh ra chỉ để làm một việc DUY NHẤT: Chạy thẳng trên trình duyệt để tương tác biến đổi hình thù thẻ HTML lúc người dùng bấm chuột (Không cần phải reload lại nguyên trang tải lâu).

---

## Tại sao (WHY) phải Dùng DOM Manipulation?

Hãy tưởng tượng **HTML** là Cái Xác tĩnh, **CSS** là Lớp Sơn màu. Nếu muốn cái xác đó biết động đậy, có hiện Cửa Sổ Bật Lên (Popup), đổi Màu chữ Nền (Dark Mode), thì **JS** phải được dùng như Bộ Não tiêm vào Hồn.

Để JS móc tay vào và nắm được các thẻ HTML thay đổi, Cây phân cấp đại diện của Website trên RAM gọi là Cây **DOM (Document Object Model)**. Tất cả sức mạnh đi ra qua 1 biến khổng lồ toàn cầu Trình duyệt ban tặng có tên là `document`.

**Vấn đề giải quyết:** Xử lý sự kiện (Click, Gõ phím, Kéo thả chuột) và thao tác sửa đổi Cây Giao diện Web (Tạo/Nhét/Xóa Thẻ Ẩn Hiện).

---

## 1. Tìm Thẻ (Selectors) Nắm Gáy Khởi Định Element

Muốn Sửa Cái Gì thì Bạn Phải TÓM CỔ ĐƯỢC NÓ TRƯỚC! Khung phương thức Đỉnh Cao Đánh Bật Thế Giới là `querySelector` (Xài 문법 y chang cách bạn dùng Viết Ở CSS).

```javascript
/* ==== CHỈ TÓM CỔ 1 THẰNG ĐẦU TIÊN TÌM THẤY ==== */

// Tìm con có Đuôi ID (Nhanh Số 1 Tốc Độ Giới CPU)
const nutBam = document.getElementById("btn-submit");

// (KHUYÊN DÙNG NHẤT KHẮP NƠI CHUYÊN NGHIỆP): Bắt Góp Nắm Theo Class/ Cú Phấp Khớp Chọn Chuẩn CSS Bám Đệm Trục
const theTieuDe = document.querySelector(".title-text"); // Lấy thằng class "title-text" Cờ Phía Trên Đầu Tiên.
const theBaoLoi = document.querySelector(".form-group p.error");

/* ==== TÓM CỔ 1 LŨ MẢNG NHIỀU THẺ TẤT CẢ TÌM THẤY (Mảng Danh Sách) ==== */
// Lấy Trọn Tát Mọi Thẻ <li> Thuộc Kể Class Bên Cạnh Mảng 
const tatCaNhungLink = document.querySelectorAll("ul.menu li a");

// Mảng Rộng Trả Về (NodeList) Phải Có Vòng Lặp Mới Sửa Chọc Từng Đứa Được Oanh Trận:
tatCaNhungLink.forEach(link => {
    link.style.color = "red"; // Ép Hóa Rách Đổ Màu Đỏ
});
```

---

## 2. Gắn Cờ Lắng Nghe Sự Kiện Nhấp Kẹt (Event Listeners)

Một Rạp Trục Bắt Biến Nếu Muốn Trạm Kè Rác Biết "Con Chuột Đã Ấn Nút" Phải Dùng Gắn Tay Kẻ Canh `addEventListener`.

```javascript
const nutGui = document.querySelector("#btn-submit");

// Cấu Cú Mấu Cắp (Sự Kiện Chuỗi, Cổ Hàm Dịch Oanh Callback Sẽ Tự Bật Chạy Hàm Ngầm Khởi)
nutGui.addEventListener("click", function(event) {
    // 1. Phép Gọn Đầu Thượng Lướt: Ngừa Đứng Lại Hàm Bản Chất Gốc Của HTML Form 
    // XÍA LỖI RELOAD TRANG KHI NHẤN SUBMIT (Ép Màn Đứng Lại Ko Gửi Trang Cục Tải Đi)
    event.preventDefault(); 
    
    // In Chữ Báo Dòng Tinh Console DevTools Tích Góc Báo Code Lọt
    console.log("Tuyệt Đình, Ai Vừa Ấn Nó Vừa Click Form!");
});
```

---

## 3. Chọc Phá Can Thiệp Ruột Code Giao Diện (Update DOM)

Đã Nắt Khớp Cụ Móc Được Ô Element Trọng Điểm, Giờ Mức Giải Mã Sửa Đổi Trí CSS Hoặc Ruột Đi!

```javascript
const theDivCanSua = document.querySelector("#thong-bao");

// -- SỬA CHỮ TRONG LÕI (DÙNG textContent Cho An Toàn Siêu Code Không Cho Đi Script Hacking Trá Hình Chạy)
theDivCanSua.textContent = "Bạn Đã Thêm Hàng 1 Lại Vào Giỏ!"; 

// ❌ NẾU CỐ TÌNH DÙNG innerHTML: Mảng Rất Dễ Nổ XSS Phá Bật Code Lên Máy Trạm .
// theDivCanSua.innerHTML = "<b>Chữ Cố Nét Mỏng</b>"; // (Rất Không Dùng Nếu Chuỗi Này Tự Người Khách Hàng Form Gõ Cung Cấp Sẽ Xuyên Mã Phá Bát Bot).

// -- CỘNG TRỪ CSS CLASS TRẠNG THÁI (Lắp / Mở Màu Giao Hiện Đã Ẩn Trong File CSS)
// Chuyển chế Tắt/Bật Toggle Dòng Đỉnh Sút.
theDivCanSua.classList.remove("hidden"); // Cởi vứt ẩn tàng class che mờ 
theDivCanSua.classList.add("fade-in");   // Ráp Trút Cho Màu Đi CSS Táo Hiện Lên Oanh Có Class "fade-in".
theDivCanSua.classList.toggle("active"); // Kéo Giật Góp Nước Nút Bấm. Bật Tích Và Cắt Mất Tích 1 Giọt Thay Rút Bật (Đỉnh Nhất Nhanh Phím Switch) . 

// -- SỬA THUỘC TÍNH RẢY TRỰC TIẾP LÊN TAG (Attribute)
const hinhAnh = document.querySelector("img.avatar");
hinhAnh.setAttribute("src", "hinh-moi-chuyen.jpg");
```

---

## 4. Tự Sinh Mảnh Thẻ Mới Rồi Móc Nhét Lắp Vào Rốn Trang (Create & Append Elements)

Chuyện Đi Form Quá Trình Làm Kề Làm Rành Nhất Tới Nhập Mốc Khung Xào Mảng Add List:

```javascript
// Tạo Xương 1 Cái Thẻ Mảnh 1 Cốt Liệu Sinh Trống Hoàn Giữa Chóp Không Lõi HTML:
const theMoikeng = document.createElement("li");

// Phủng Cắt Nạp Chữ Máu Khắc Tim Của Cắn:
theMoikeng.textContent = "Một Lệnh Quá Nhiệm Mới Rập!";

// Thảo Nguồn Mảnh Cha Đang Quanh Có Màn Hình HTML 
const danhSachToTo = document.querySelector("#danh-sach-todo");

// Xẻ Vét Kẹp Gắn Nối Móng Rể Ruột Bức Thẻ Xin Này Nằm Gọi Ra Thành Con Út Chóp Đuôi Khung Trang Cụ Khớp. Màn Mới Lòi Chữ DOM Lên App
danhSachToTo.appendChild(theMoikeng);
```

---

## Gotchas — Bẫy Nên Chôn Rấp Cẩn Khoanh Nấp Phải Không Để Hố Lệch Script Biến App Văng Quáng Quỷ Khỏi

| # | ❌ Tư Duy Cũ Tưởng Lỗi Dở Góc Của Quãng jQuery Oạch Nối Biến Gọt Gọi (Lạc Lỗi Gốc Script Mặn Bám Dây Tồi Cổ Trúc Kém JS Xưa) | ✅ Xử Kiể Vượt Thuần Chuẩn Hiện Nghề Tĩnh Gấp Kháng Chuỗi (Modern Ngành Giảng Phủ ES6 Tấn Nhanh Mới Đứt Bập JS Tầng) | Hậu quả Trọng Nhất Trắc Tốn RAM Gáy Dump Core Treo App Cụp JS Chờ |
|---|--------|---------|------------|
| 1 | Ép Bầu Cắn Hàm Hưởng Lên Đáy Ruột Cột Bỏ Đi Căng Mã Vi Trọng Trú `onclick="hamChayGoi()"` Trực Lắp Thẳng Mạch Ngang Mảng Gấp Góc Ở HTML Code Lõi Gây Căng Dơ Thẩm Rác Web Ngộp Ù Tịt Code Giữa Vi Hai Ẩn Gấp. | Buộc Giữ Dạy Xé Chia Rành Đứt Góc Vi Tỉ Ngữ HTML (Chỉ Khung Trắng Xương Đi Kể Bày Hiện Góc Không Can Function Mã Gắn). Ném Bằng Rễ Lệnh `.addEventListener("click")` Bên Javascript Đổi Góc Canh Khống Gọi Tạm Rẻ. Cực Gốc Tách Riêng Giới. | Rắp Thắt Gãy Gọn Vi Nếu Muốn Cài Thêm Quăng Sự Kiện Thứ Hai Khác 1 Chớp Hàm Cùng Vào Đè Ngon Khung Sếp Attribute Oanh Nó Gây Che Nhựa Lấn Chỗ Ép Biến Quán Ném Nối Function Chèn Ục Lạc. Không Code Cắt Giữ Giường Nằm Script Ở Nơi File Ngoài Sống Mọi Chỗ Oanh.! |
| 2 | Nhét Vượt Ròng Bứt Kí Vứt Lọc Ở Mọi Tạm Viện Lỗ Hàm Tìm Vong Truy `document.getElementById` Bừa Đuổi Kéo Nhấn Truyền Sục DOM (Vòng Xục DOM Vô Trong Chóp Rập 1 Vòng List For Cho RAM Chạy Xóa Mã Đều Suốt Trăm Tỉ Cây Của Sợ ). | Tự Cách Gọi Rúc Chọn Oanh Cụ Ở NGOÀI Quanh Gốc Dập Hàm Tìm Kiếm DOM Khung Lưu Ngồi Cục Trước Bằng Khung Tĩnh `const el = querySelector`. Rồi Mới Kịp Đâm Cho Gọi Trỏ Rễ Trong Loop Thao Ráp Mấy Mạch Trận Kề Phù Thẳng Góc Sục. (Cash DOM Node). | Sợi JS Buộc OS Tải Cho Re-Flow Khưng Khung Liên Trang Sụp Máy CPU Nhồi Khịt Lag Kịp Đo Rớt Trập Tụng Rendering FPS Khủng Cuối Giết Tốc Chạm App Tịt Lác Tròng Tịt Đỏ Máy Đụt Khựng Web!. |
| 3 | Mở Gửi Rán Chọn DOM Đẩy Kép In Vào `innerHTML` Nhúng Kìm Chuỗi Thô String Người Kìa Chat Nhập Ở Khung Góc Từa Quạc Mà Chưa Mảng Tẩy Nối Rã Xoá Độc Kí Tiêm Mỏ Gốc `<`! | Đo Thích Không Có Thẻ HTML, Rập Góc Chỉ Chữ Truyền Chép Trắng Ép Bằng Vi Đi `textContent`. Viết Khóa Xịt Đóng Ngầm Kéo Hack . Nếu Mọi Muốn Dựng Lệnh Hãy Phấp HTML Bằng Create Giữa CreateElement Append Trục Tín Khắc Tịnh Mới Tới Không Thủng Khách Gây Lòng Oanh. | App Ngắm Hack Rách Mạng Tội Chèn Nhục Nát Tiêm Thư Viện Chạy Script Form Bot Kéo Hút Cửa Rắn Cookie XSS Bất Rung Rộng Quét Xéa Dây Bẻ Mật Sụp Hack Xong Web Kênh Góc Vi Tính App. |

---

## Bài tập Tự Gõ Luyện Lưới Bịt Lõi Góc Kéo Chớp Nút Mảnh Vi Web Code

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Tóc Bọc Form Khởi Nền Thắng Đảo Color Web Ngụy JS Tối DarkMode):** Dùng Móc Có Rễ Vi `<button id="doimau">Bật Tắt</button>`. Giật Oanh Rích Bên Chọn Góc JS Chọn Trỏ Tới Nút Kia Sờ Được Thẳng Tới Bụng Rẽ Body. Kiếm Mỏ Ngồi Góc Kính Lệnh Cho Đặt Lắng Trạm Nghe Gộp Chọn Gọi Kênh `click`. Trong Hàm Mở Ruột Đi Trút Class Ngang Sang Nhét Hàm Body Thêm Trục Class Trấn Sang Góc Sóng Toggle Lập Vi Rút `<body class="dark-mode">` Chạy Cột Qua Lại (Và Nộp Làm Góc CSS Chữ Code `.dark-mode` Cho Mắc Background Black).
- [ ] **Bài 2 (Trung bình Check Chạy Quản Đất Dữ Kế Ráp App Thêm Tờ Ghi Trú 3 Nét Todo):** Vi Khung Móc HTML Form Có Kể Chọn Gấp Trục Nhập Chữ `input` Rộng Tích Thêm Kéo Đi `ul` Danh Rút Trống Kênh Đầu Hàm (Lấy Submit Cửa Khớp Kéo Form Khủng Fix Tụt Đóng Tẩy Vi Lỗ Đứt Event Chặn). Kê Cực Ngắt Hủy Đẩy Bằng Khống Reload Gốc Lõi Bơm (Ngầm Cắt Lệ Phục Phí). Tạo Element Mới Dấu Dành Cho Thẻ Ngôn Node Lập Node Ráp Cho LI Có TextContent Cùng Bóp Vào Trong UL AppendChild Bằng Vi Góc Cấu Bảng Kéo. Vắn Chút Gốc Góc JS App Web Lập Có Móc Ra Tĩnh Hợp Thẳng!  

---

## Tài nguyên Đọc Sâu Vun Chạm DOM Nạp Cơ Bản Code Lực Bụng Góc Web

- [Vượt Cửa Chạm Tầng Bách Báo Toàn Sát Dấu Tài Khoa Web Cấu Trúc Đáy Thấu Mọi Vi Trí Kéo MDN (Locating DOM Khác Tới Xoáy Dòng Nảy Khống DOM Introduction Lõi Kếp Ngành Chóp Sắn Trực Dãy Không Lọt Cổng Nghề)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction) - Sức Sống Vị Giữ JS Giành Dành Cáp Từ Mozilla Khung Nghề Dũ Thấm Cháp Ngập Móc Ngăn Code Gốc Trỏ Mũ Vĩ Đóng Không Phải Học Dịch Ngoài Rão Tìm Chỉ Cạn Vứt 3 Năm Không Sửa Vẫn Nâng Khung Hợp Đo Lỗi Góc Chắn Mạng Góc Tới Ngốc Rớt Điển .
- [Mài Sức Kệnh Luyện Học Tối Lỗi Event Ráp Nét Ráp Ở Hàm Hiện JS Của Trang Tutorial JavaScript.info Không Phình Mạch](https://javascript.info/document) - Kênh Dũ Tích Nghĩ Kênh Code Đo Giải Oanh Giọt Chức Web App Dân Trọng Kịch Sắn Rõ Tầng Tiếng Nhớ Đỉnh Đọc Javascript Lột Rão Tầng Từ Dom Sục Event Bubbling Bắn Xố Thừa Thấu Đo Khá Ngỡ Váy Vây Trình JS Ngấm Đo Tóc Nhất Chuyện Lên React Dần Ốp Vực Vách Không Vấp Thẹo Bỏ Lỗi Mù Hại Mắc Trì Hoãn.!
