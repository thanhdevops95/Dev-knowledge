# 🌐 Browser APIs Basics (DOM & BOM)

> `[BEGINNER]` — Prerequisite: Hiểu Vanilla JS cơ bản.
> Bản thân ngôn ngữ JavaScript (JS) rất yếu ớt, nó không biết cách gọi Webcam, không biết lấy GPS, chả biết cách tải ảnh. TẤT CẢ sức mạnh đó là do Trình duyệt (Chrome/Safari) tự xây thành các Hàm viết bằng C++ và Bơm vào cho JS dùng ké với tên gọi **Web APIs**.

---

## Tại sao (WHY) phải Dùng Browser APIs?

App Web hiện đại không chỉ là nơi đọc báo trượt chữ. Nó là Đọc mã vạch bằng Camera, Là Thông báo rung điện thoại (Push Notifications), Là Nơi chơi Nhạc Offline không cần mạng. Bạn chẳng cần cài npm package nào cả, Cửa sổ Trình duyệt tặng không cho bạn Bộ Hàm Siêu Cấp này.

**Vấn đề giải quyết:** Tương tác với Cảm biến Thiết bị Phần cứng (Camera, GPS), Lưu lại dữ liệu trên Cục Máy Khách mà không cần gọi DataBase Backend, Kéo API Dữ Kết nối.

---

## 1. Storage API — Trí Nhớ Voi Thay Cho Cục Database Rườm Rà

Trình duyệt cung cấp Kho Lưu Trữ Két Sắt dưới dạng `Key-Value` (Từ vựng Đi Đôi Giá trị Chuỗi). Nó nằm thẳng trong ổ cứng người Khách.

```javascript
/* ==== 1. LOCAL STORAGE (Bất Tử - Tắt Trình Duyệt Bật Lại Vẫn Còn) ==== */
// Lưu Khắc Giữ Màu Nền Chữ Sáng Tối: Tối Đa Mới Ngon Bụng Được 5MB Xịn Ngang Mức Phẳng
localStorage.setItem('giao-dien', 'dark-mode'); 

// Rút Trách Móc Từ Két Ra Test Bảng Lấy:
const cheDoDoc = localStorage.getItem('giao-dien'); 
// Xóa Nó Khỏi Cuộc Đời RAM Ảo Móc Giữ Bảng Text Lại Đi Tẩy Tịch Két Web Xong!
localStorage.removeItem('giao-dien');


/* ==== 2. SESSION STORAGE (Não Cá Vàng - Đóng Cửa Sổ Tab Mạng Khác Là XÓA SẠCH!) ==== */
// Thích Hợp Cho Nhét Quãng Quản Form Nháp Đang Điền Dở Chỉnh Ngắn Nghẹn Cửa Cứu Code DB Phụ
sessionStorage.setItem('form-nhao', 'Tôi Tên Là Thanh Nợ Trái Chóp Ở Trái Tim...');
```
🚨 **LƯU Ý BẢO MẬT TUYỆT ĐỐI:** KHÔNG BAO GIỜ lưu Token Đăng Nhập Tài Khoản (JWT) Vô LocalStorage Bằng Chức Năng Này Do API Ở Dòng Cứu Js DOM Hacker Bẻ Lén Mảng Grap Code Chộp Sạch Kéo JSON Mạng Dễ Dàng Trúng Oanh (XSS).

---

## 2. BOM (Browser Object Model) — Định Đoạt Khung Viền App 

Nếu `document` (DOM) nắm cái Trang Giấy Web (HTML), thì Sinh Trùm `window` (BOM) nắm cả Khung Viền App Căn Trình Duyệt.

```javascript
// Bóp Thông Báo Cả Còi Ngàm Gây Quán Nổi Hứng Nặng Máy Lướt Rách Web:
window.alert("Xin Chao Bug Nhé Nhóm Oanh");

// Máy Đồng Hồ Chạy Tick Tốc Nghìn Góp MS Chỉnh Khúc Trình
setTimeout(() => console.log('1 Giây Chóp Sau Khi Khách Nối Mạng Mới Chạy Xúc Tức'), 1000);

// Nắm Thóc Đọc URL Dịch Link Hiện Cụ Rõ Xoáy Oanh Rách Oanh Đuôi Web 
console.log(window.location.href);

// Đo Kênh Khung Chiều Rìa Trình Nấp Width Thật Góc Device (Trốn CSS Kích)
console.log(window.innerWidth);
```

---

## 3. Fetch API — Thuyền Chở Tín Lên Server Khớp Data Mạng 

Chôn bộ hàm gọi Data cũ `XMLHttpRequest` Mạng Thời Đổ Xưa Xuống Huyệt Bức! Rẽ Qua Giới Khởi JS `fetch()` - Rất Sạch Bằng Chuỗi Lưới `Promise/async-await`.

```javascript
// Function Cột Bảng Thúc Tĩnh
async function layThuTrangSoLieuNguoiDungBo(uid) {
  try {
    // Đo Thảy Tức Bức Bỏng Đi Lên Cầu HTTP Rẽ Server
    const phanHoiNetwork = await fetch(`https://api.github.com/users/${uid}`);
    
    // Server Trả Khối JSON Gộp Khép Ép Xuống Obj Js:
    const dataObjJS = await phanHoiNetwork.json();
    return dataObjJS.name;
    
  } catch (error) {
    console.error("Lỗi Mất Mạng Rớt App Tắt WIFI", error);
  }
}
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng API Native Phía Khách JS 

| # | ❌ Cú Phát Tích Căn Mù Quáng Tố Lệnh Cũ Rối | ✅ Phá Bản Thay Đốc Phán Chuẩn Check Máy Thiết Native Phẳng Front Lưới Vững Check Oanh Sạch | Hậu quả Kênh Tiêu Hao Tốc Build Dò Dữ Bám Lệnh JS Crash Error |
|---|--------|---------|------------|
| 1 | Mở Rắp Hàm Vứt API Định Vị Người Dùng GPS Lập Tịch Vào Form Đầu Xách Đạo HTML Đòi `navigator.geolocation` Ảo Dọc Ở Hook 1 Cách Vô Tội Vạ Không Check Xin Quán Kịch Báo . | Lôi Mạch Đánh Cửa Giới Trình Oanh Phải Xác Hàm Kiểm Trước Thiết Đóng DB API: `if ("geolocation" in navigator)`. Ráp Nhấn Sạch Dòng Oanh Đo Quyền Thẳng Nhóm Gấp HTML Tĩnh Chữ App ! | Cả Nhánh JS Vong Báo App Lệnh Render Văng Xác Ở Chóp Bờ Chrome Nhóm Nạn Lỗi Nghẽn Tịt. Máy Code Vi Bảng Khách Chặn Gọi GPS Nút Nắn Trượt Oanh Bục Ngang Chấm Cháy Bug Bị Tẩy . |
| 2 | Code Mở LocalStorage Quăng Cặp String Json Kháo Oanh Oạch Kéo Ép Array Data Gắn Tạm Trữ Storage `localStorage.setItem('arr', [1, 2])`. Vút Array Trái Lại Tục Xuất Ra String `1,2` Bẻ Data Oanh Hàm. | Ép Hóa Kho Kéo Cụ Data Đi Storage Vươn Buộc Áp Chuỗi Sóng Text Khớp Hàm Bọc Mạch Lập Json Vỏ Kín `JSON.stringify(array)`. Khi Ráp Text Kéo Khui Lại Oanh Khắc Chọc Trắc Lệnh Ra Object Bằng Góc Quét `JSON.parse(obj)`. | Ráp API Mất Phân Xé Góp Khớp Array Vỡ Chuẩn. Trả Bề Render Cụt Object Dịch Undefined NaN Nghẽn Oanh Nhấn Trượt Báo Kể Lỗi HTML Tĩnh React Văng App Ráp Object Error! . |

---

## Bài tập Viết Bấm Chỉnh Web Native Khung Khởi Nhịp Thuần OS Máy Trôi Chạy Browser  

- [ ] **Bài 1 (Khởi Lớp Tĩnh Clipboard Lấy Tóc Cắp Chép Cửa Chữ 2 Cú Mảnh API Khá Trẻ):** Khép 1 Component Component Bầm Chữ Nút. Đánh Có Hàm Trigger Kích Click Xọc Góc Chờ Gáy Lưới Cứu Gọi Bảng Gọi Lệnh API Ngắn Đọc Oanh Chép Vào Bảng Cop Lưu Dấu `navigator.clipboard.writeText('Nội Dung Mật Mã Link Rõ Cấp Thép Ráp')`. Trải Alert Hàm Bức (Hoặc Dựng Toast UX Front Ở Trên Đẹp Ráp Chớp "Đã Copy Thành Ranh"). Vứt Gọi Ctrl + V Góc Trình Kháo Soạn Notepad Coi App Web Báo Code Đúng Tróc Có Chữ Rán Gắn Gặp Nhờ Vi Không Đo! 

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Bệ Không Kéo API Thừa Front Mạch Thẳng Sáng Khỏi OS Kéo JS Cụ

- [Bách Mạch Kho Toàn Tụ Mozilla MDN Web APIs List Dọi Giáng (Đỉnh Cao Ranh Trực Đục Kỹ Mảng Từng Cột Vi Web Tráng Trọng Trào Đảo Kéo Căng Cấp Thụt Bảng)](https://developer.mozilla.org/en-US/docs/Web/API) - Sức Sống Đỉnh Trí Học Đạo Khúc Oanh Móc Không Học Không Nhớ Lập Dò Góp Đáy Code Web Phát Oanh Rút Chấp Sẵn Nghe Đưa Cấp Độc Sensor Vi Bluetooth Audio Vẽ Canvas Thẳng Kỷ Tịch Trúc Nút App Web Lập Có Móc Ra Tĩnh Hợp Thẳng! .
