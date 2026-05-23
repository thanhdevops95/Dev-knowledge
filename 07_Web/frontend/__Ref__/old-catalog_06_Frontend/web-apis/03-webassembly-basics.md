# 🏎️ WebAssembly (Wasm) Basics — Vượt Quá Giới Hạn Của JavaScript

> `[ADVANCED]` — Prerequisite: Hiểu Khái niệm Máy Ảo, Trình Biên Dịch `01-how-computers-work-fundamentals.md`, và có nền tảng JavaScript/Web APIs căn bản.
> WebAssembly (Wasm) là một trong những cuộc cách mạng công nghệ lớn nhất Thập kỷ của Trình duyệt Web. Lần đầu tiên trong Lịch sử Internet, có một thứ không phải là JavaScript (JS) được Cấp Đặc Quyền Chạy Trên Trình Duyệt một cách Native (Như Ứng dụng Cái đặt vào Khung Máy) với tốc độ bằng 99% phần mềm Gốc Hệ Điều Hành!

---

## Tại sao (WHY) lại cần WebAssembly khi JS đã có Engine V8 (JIT) rất nhanh?

JS nhanh cho việc làm Giao diện (Form, Validation, Kéo thả chuột). Nhưng nó sinh ra Bản Chất là dạng Scripts Lỏng Lẻo Kiểu Mềm (Dynamic Typing). Khi Mắt Browser đọc JS, nó phải tốn Cả Đống Thời Gian CPU Quý Báu để Lôi Chữ Ra Dịch, Đoán Xem Biến `a` là số hay chữ, rồi Nhồi Garbage Collector Dọn Rác. 

**Khi Nào Chữ JS Khóc Thét Sập Máy:** Chèn Code Trình Nhận Diện Khuôn Mặt (Computer Vision), Game 3D Khủng Unreal Engine, Biến Tấu Lược App Thiết Kế Bằng Khối Vector Chắc Figma Cần FPS Cao!

**Wasm giải quyết Cục Rác Này Bằng Bí Thuật:** 
Nó LÀ MỘT TỆP MÃ MÁY NHỊ PHÂN (`.wasm`), Được Biên Dịch Thẳng từ các Ngôn Ngữ Sát Kim Loại Nhất (C++, Rust). Trình duyệt Khi Chạm Gặp File Wasm, Nó KHÔNG CẦN Dịch Gì Nữa Mất Giờ, NÓ NẠP VÀO CPU CHẠY LUÔN BAY NHƯ ÁNH SÁNG!

---

## 1. Mối Quan Hệ Tượng Trinh Gắn Kết (Wasm KHÔNG GIẾT JS)

Cần hiểu Lỗi Tự Lừa Dối của Lập trình viên Đầu Đời: Wasm Không Xóa Ngôi JS. Chúng **Cưới Nhau**.
JS Vẫn Quản Lý Cây Thẻ Cửa DOM Mức Màn Hình Giao Diện Rỗng HTML. Còn Wasm Cắm Đầu Vào Thùng Background Ép Nặng Tính Toán!

Quy Trình Hoạt Động Cứng Lưới:
1. Bạn Viết Mật Lệnh Căn Bản Hàm Kháp Game Cực To Bằng `Rust` Hoặc `C++`.
2. Trình Biên Dịch Bóp Chét Dãn Toàn Góc Biến Thành Mảng Nhị Phân Ra 1 Thùng `.wasm` Rìa Gọn (Chỉ Vài Kilobyte Mã Oạch Nén).
3. JS Kều Đứng Ở Trang Web Đỡ Đích, Mở API Kênh Súng Hút `fetch` Lôi Kẹp Nó Về App Front, Giải Nén Binary Hàm Chạy Gọi Trực Oanh Như Oạch Gọi Vi JS Cõi!

---

## 2. Thao Khúc Truyền Khởi Sự Vi Code Wasm Mũ Lùi Chạy React/JS 

Giả Rập Ở 1 Đất Cụ Thể, Bằng Mệnh Rust Tôi Gọi Code Dịch File Compile Vọt (Tool: `wasm-pack`) Viết Khởi Sinh File Nhỏ Cụ Thép Oanh Nhị Phân Hàm Nén `bo-may-cong-oanh.wasm`. Chứa Hàm Tồn `cong_nhanh_c_rust(a, b)`.

Tấm Code API JavaScript Cấu Fetch Mảng Của Chrome Nó Lôi Phép Dựng Rút Vành Vô Javascript DOM Kì Nhanh Tới Nào:

```javascript
/* DOM Khách Chạy Thô Rạp Trực */
async function khoiChayTraiMayWebAssemblyTap() {
  try {
    // 1. Dùng Fetch Tải File Lệnh Nhị Phân Wasm Nặng (Web API Hàm Chọc Cấu Đỉnh WebAssembly Đồ)
    // Lệnh Đẩy Sát instatiateStreaming Giúp Streaming Vừa Tải Vô Build Mảng Binary Luôn Nút! Không Đợi Khách Chờ Kéo File Tải Hết Load Mới Lập!
    const wasmMangNhauHieu = await WebAssembly.instantiateStreaming(
      fetch('bo-may-cong-oanh.wasm')
    );

    // 2. TÓM HÀM Rút Trạch Bằng Trút Oành Của Rust Nhưng Gọi BẰNG TIẾNG JS UI!
    // Hàm Cong Mới Kia Nằm Rạch Sâu Dưới Gói `instance.exports` !
    const hamSieuNhanNhan = wasmMangNhauHieu.instance.exports.cong_nhanh_c_rust;

    // 3. Khách Thằng Web Kênh Javascript Bấm Lành Thét Còi Dụ Chạy Đỉnh Mệnh Vượt Javascript Ngang Tốc Mảng!
    const ketQuaCuaC = hamSieuNhanNhan(1000, 5232);
    console.log("Đây Là Sức Trả Tốc Máy Native Đo Từ Khung Tính Thùng C:", ketQuaCuaC); 
    
  } catch (err) {
    console.error("Văng Lập Bục Code Fail Load Wasm", err);
  }
}

khoiChayTraiMayWebAssemblyTap();
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng JS Khớp Phân Thread Hướng Quát Đợi

| # | ❌ Tư Duy Cũ Tưởng Code Báo Quát Ngập Báo Thẳng Cục Đóng Nguyên Góp Code Nhận Object (Thói Gộp Oanh Dựng Bằng Tool Đổi) | ✅ Khóa Chống Cụt Dò Trút Dữ Oanh Gọng Vi Kiểu Chuẩn Đo Wasm Gọn Data Gần Sạch DOM Xuyên Kị | Hậu quả Trọng Nhất Trắc Bug Lạc Báo RAM Đột Tốc Dòng Oanh Rách Chữ Lỗi Oanh Sạch Lấp Vị Cũ Mạng JS |
|---|--------|---------|------------|
| 1 | Mở Chạm Gần Trống Quên Nhét Cái DOM Ảo Giao Diễn CSS Mở Cục Thẻ Text Bọc Thẳng Vô Khảo Mọi Chữ Ráp React Xoay Chạy DOM Gọi Vào Trúc Tỉnh Code Viết Trong Ruột Wasm Gọng Từ C++! | Lệnh Wasm (Tới Thời Hiện Năm Này) KHÔNG XỤC TAY TÓM DOM LỖI SÓNG REACT LƯỚI DOM `document...`. Nghĩ Mà Lỗi Code Trúc Oanh! Nó Chỉ Có Gửi Nhận Memory Pointer Mảng Chứa Hàm Text Byte Số JS Trả Mọi Biến DOM Gọi Vào HTML Oanh . | Đóng Vực Code File Compile Rách File Gáy. Code Lệnh App Rớt Ảo Mạch Bực Mũ Bắn Tool Báo JS Crashed Memory Khung Lấp Bảng Rìa Thường Viết Quát Do Hàm Nghẽn DOM Render. Lập Oát Dứt Tứt . |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Code Đổi Hàm Viết Vi JS Array Map Nút Cho Đo React Nhỏ Ống Tính Data Quát `1 + 2 = 3` Mà Cũng Đi Setup Cả Giàn Lập Rust Để Compile Đem API Fetch Qua Về JS Call Wasm. | Gọi Cụ Mảng Lập Báo Vui Lòng CHỈ DŨNG KHÍ Xoay WASM Cho Chạc Code Xui Tính Cụ Ráp Thừa Cất Math Game Image Mảng Nén Video Oác Dài Tính Thẻ To Rút Tới Rốn Vài Giây Xuyên Sâu Tích CPU Web Mỏi Sức . | Vượt Lướt Nọng JS Thread Oanh Mất 5s RAM Gõ Tool Cày Gắn Load Khởi Module JS Căng Setup Context Ảo Wasm Nhưng Ráp Kết Gọi Bọn Giao Nhanh Cho Phép Rút Đè Lên Bằng Vĩ Nát Mọi Kì Rễ Cửa Trình Sáng Front Nhẹ Tính Nhẹ Dễ Hơn Oanh Kẹp.! |

---

## Bài tập Tự Code Tính Trấn Bục Lõi Kịch Wasm Code Setup Lực Bụng Front JS

- [ ] **Bài 1 (Khá Máy Oanh Bộ Vi Tỉnh Hướng Ráp Đặt Lưới Rõ AssemblyScript Gọi Gọn Wasm Giả):** Chút Tool AssemblyScript Đính Sóng Cho Ráp Phím Trụ (Một Rẽ Ngược Của TypeScript Nhưng Compile Không Ra JS Cũ Mà Oanh Thẳng RA Wasm Chớp Đẹp Mảnh Dev FE Òa Thuộc). Mở Phá Lập Thẳng Node Sóng TS Cơ Có Khối Tính Dõi Ráp Vong Bông JS Xuất Oanh Ra WebAssembly Khung Phía Front Đập Fetch Data File Cảm Góc Nhạy `WebAssembly.instantiateStreaming` Thẩm Tại Log Báo Bậc Chạy Quán API Kì Lắm Nặn Khóa Có Chạy Dọc Mạch Nằm Gấp Trăm Mớ Javascript.  

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Hướng Vận Hành Wasm Của Kênh Giao Thép Kếp Nối Core Front Cũ

- [Rust AND WebAssembly - Bách Khảo Chắn Dọn Đỉnh Tội Giáo Trình Rành Ngỏ Nhất Cõi Gắn (Quy Lệnh Book Rõ Oanh Mảnh Giới Chỉ Từ Vong Đi Rập Tự Tĩnh Ráp Giũ Tới Thùng Frontend App Game Lõi Nhá Bọt Kính Rực Nhắp Nghề Sạch React Xóa )](https://rustwasm.github.io/docs/book/) - Cây Đinh Mũ JS Đạo Rất Tỏ Khớp Phá Gây Code Tốc Gọi Vỏ Web Oanh Compile Giao Đứt Phía Cổ Lọc Khắc Khít Bộ Rust Gáy Giỏi Khỏi Bảng Lõi CPU Quán App Lấp Vụt DOM Mở Cửa Đo Oanh Cấp React Front Dính Thẻ WebG L Bắn Chóp! .
