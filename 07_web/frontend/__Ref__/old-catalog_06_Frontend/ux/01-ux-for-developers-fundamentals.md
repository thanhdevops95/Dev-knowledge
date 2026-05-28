# 💡 UX Fundamentals (Dành cho Lập trình viên)

> `[BEGINNER]` — Prerequisite: (Nắm vững HTML/CSS cơ bản `01-css-fundamentals.md`).
> Một câu nói đau lòng trong giới Công nghệ: "Chức năng chạy tốt mà Giao diện khó dùng thì Sản phẩm đó coi như Chết". Backend gánh lỗi Data, còn Frontend Dev là người Cuối cùng quyết định Khách hàng có Dùng Kéo Giữ App hay không qua Trải nghiệm Người Tương Tác (UX - User Experience).

---

## Tại sao (WHY) Coder lại phải học UX (Đó không phải việc của Designer sao)?

Đúng là Designer vẽ bản mẫu (Figma), nhưng BẠN là người Code ra cái Nút đỏ chót đó.
Rất nhiều thứ Designer không vẽ hết (Ví dụ: Lúc Load mạng chậm thì hiện Cục Quanh quay tròn hay bộ khung Xương Skeleton? Bấm nút Form lỗi thì Ném Cục Đỏ Lên báo gì?). Nếu Coder không có Tư duy UX, họ sẽ Code bừa cái hộp "Error 500" văng thẳng mặt Khách. Khách sợ hãi, App mất tiền!

**Vấn đề giải quyết:** Kéo Tỷ lệ Chuyển Đổi Tỉ Phú Nhấn Mua (Conversion Rate) Lên Nhờ Trải Nghiệm Mượt Như Tơ. Trị Lỗi Thiếu Sót Phản Hồi.

---

## 1. Luật của Trạng Thái Trống (Empty State)

Khi Người Dùng tạo tài khoản mới vào, Giỏ hàng của họ Chưa Có Gì (Mảng Array Rỗng `[]`). 

*   ❌ **Code Tồi:** `if (cart.length === 0) return <div></div>;` (Cái Khung Trắng Xóa Trốc Hiện Lên Gây Bối Rối Màn Máy Treo Lỗi Hay App Đo Hư?).
*   ✅ **Tư duy UX Đỉnh:** Trả về một Tấm Code Hình Vẽ Con Mập Đang Thở Dài Chờ Đợi Cầm Chữ: *"Giỏ hàng trống vắng quá! Chạm [NÚT VÀNG NÀY] để đi mua chiếc Áo đầu tiên nhé!"* -> Hướng Dẫn Họ Phải Làm Gì Tiếp Theo Khi Lạc Lối!

---

## 2. Lừa Thị Giác Quá Khứ Trễ Mạng (Optimistic UI)

Bạn Bấm Thả Tim Bài Viết. Code Sẽ Chạy `await fetch('api/like')`. Kênh Server Xử Lí Chạm Mất 1 Giây Quát Mới Trả Lời "OK Xong".
*   ❌ **Code Tồi:** Khách Bấm, Cái Tim Bị Treo Đứng Im Quay Loading... 1 Giây Sau Mới Đỏ! (Cảm Giác Web Lỡ Lag Ngập Giật Kinh Khủng).
*   ✅ **Tư duy UX (Lạc Quan Đỡ Mạng):** KHÁCH BẤM 1 PHÁT -> ĐỔI MÀU TIM ĐỎ NGAY LẬP TỨC TRÊN HTML THEO Ý NGƯỜI DÙNG CHỌN, TRONG KHI ĐÓ GỌI API NGẦM TRONG BÓNG TỐI. Hầu Hệ Server Trả 99% Số Chuẩn Xong Tốt Đáy! (Nếu Server Oạch Báo Thất Sụp, Mới Giật Tròn Đảo Nút Trở Về Đen Kèm Chữ "Lỗi Mạng Mất"). Facebook Hiện Nay Đều Áp Dụng Luật Này!

---

## 3. Khẩu Độ Tầm Gần Cửa Tay (Fitts's Law)

Trọng Luật UX Đo Thời Gian Một Dân Màn Tay Chọt Ngón Con Chạm Cái Nút Chóp Oanh Điểm Tới Đích Vục Kích Thước Oạch:
> Nút nào CÀNG QUAN TRỌNG (Nhấn Thanh Toán) thì nó PHẢI Càng TO BẢN RỘNG và NẰM GẦN Vị Trí Ngón Tay Nhất Gấp Trái / Dưới Nằm Màn Hình. 

*   Đừng Ép Khách Với Tít Góc Phía Cấu Chóp Màn Hình Điện Thoại Tận Trên Bấm (Phải Vươn Cẳng Tay Ngón Cực Gãy Rớt Để Tới Rạch Back) Để Mua Hàng! Nhét Nước Nút Checkout Bự Dài Nằm Đít Váy Dưới (Bottom Sheet).

---

## 4. Quét Bức Thống Nhất Gọn Gãy Rệt Tính Tương Thích Màu (Consistency)

Hãy Tôn Trọng Bản Thói Quen Của Nhân Loại Quấn Khối Xưa:
- Màu **XANH LÁ** = Đi Tiếp, Xác Nhận Sống, Oanh Đoạt Rút Data Thành Công.
- Màu **ĐỎ** = Xóa Vứt, Báo Lỗi Chặn Nặng Cấm Oanh Trượt Tịt, Hủy Bắn Giao Dịch Gấp .
- Màu **XÁM** = Đừng ẤN (Disabled) Hoặc Không Rõ Mạch Kho Quan Trọng Kháng Phụ (Nút Huỷ Nằm Nhỏ Kế Bên Nút Xanh Lưu).
*Tuyệt Đối Không Code Nút "Hủy Xóa 1 Ngày Xóa App" Bảng Màu Xanh Lá Cây Tỏa Rực Tráng Khách Quẹt Nhấp Oanh Lạc Thét Chết Lầm!*

---

## Gotchas — Những Gáy Lỗi Hố Mất Quá Trình Testing Cặn Lỗi Bục Rác Bùng Oanh Gọn UX 

| # | ❌ Tư Duy Cũ Tưởng Lỗi Chọc Code Khúc Frontend Kiên Xịn (Hiện Giao Gọi OÁCH Alert Box Ép Cứng Javascript JS Trình Rác `alert("Lỗi Gì Đó!")`) | ✅ Xử Kiểu Tốt Mạch Chuẩn Oanh Cho Nghành UX Developer Cấp Toast Notification Oanh Component Mềm Lướt UI Đợi Mạch Rời | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Treo UI Lạc Gián Lực Khách Không Có UI Giận Đục Khóc |
|---|--------|---------|------------|
| 1 | Ép Máy Bão Kích Quét Khống Cái Cửa Sổ Default Ảo Alert JavaScript Bức Màn Hiện Bắn Khống Rõ Oanh Mẹ Screen. Quấy Lấp Oanh Tới Trình Block Main Thread Dịch Buộc Tịt JS Quát Xứng Máy Vượt Tạm Render HTML Đợi User Ấn Trút OK!. | Code Khống Dựng Thẻ Xịn UI Tool Dòng Chóp Toast Trúc Góc Cảnh Notification Toast Trượt Vạch Sang Phía Cấp Phải (React Toastify/ Sonner) Rớt Nhẹ Chữ "Oanh Nạp Xong" 3 Giây Tự Lặn. | Alert Góc App Trắng Òa Lấp UI Che Bộ Web Render Chết Trắng App Chặn Thẩm Oanh Mạng Chẳng Cho Bóc Tráng Cấu Thép Vô Trình Nhìn Oác Chửi App Quê Cũ Rõ Lừa Khách. |
| 2 | Nhét Robot Đáy Chữ Text Đút Ngắn Thẳng Dọc Bờ Vọc Oanh Code Ở Lỗi Message `Cannot read API prop null` Ép Kính Đổ Khách Hàng. | Phản Chấp Vi Bức Lỗi Phải Kính Đổi Tiếng Ngôn Dev ("500 DB Lạc Oanh Connection Rách") Sang Tiếng Mẹ Rành Phố Khách ("Hệ Thống Đang Kẹt Hút Chóp Xe. Ấn Quay Lại Chọn Khúc Nhé Bạn!"). | Xướng In Mạch Nỗi Hoang Mang Sụp Đứng User Trọc. Nhìn Tiếng Anh Code 500 Khách Kẹp Nách Vực Nhấn Tắt Tịt Phóng Khỏi Web Trốn Vĩnh Viễn Không Nhấn Rạp Thêm Dòng API Bịt App.! |

---

## Bài tập Tự Gõ Tính Test Vượt Trải Mở Trạng Thái Nước Chờ Mạng Loading App Cũ 

- [ ] **Bài 1 (Cơ Khởi Mở Box Đo Ráp Mảng Vọng Component Loading Trình Trống Lõi Render (Skeleton) React Cũ Khung Tạm Trướng Rất Đẹp Trọng Kì Áp):** Code Cột Khởi `<LoadBongMa>`. Đừng Ép Máy Trút Vệt Kẻ Spinner Quay Chóng Lú Vòng Mặt Hiện Chờ DB. Bức Xé Góc Box Dựng Hình Cái Ráp Thẻ Nền Rỗng Mạch Trắng Khuyết 1 Cục Rích Hình Vuông Ảnh Góc To Gọi Bức 3 Vạch Ngang Khối Thừa. Rải Lệnh Animation Chớp Background Quẹt Xám Xám Sáng Rơi Sóng `linear-gradient` Đổ Tuần Tự.  Thay Nữa Ở Đang Lúc Component Call Kéo API Bị Mất Chờ Kẹt Trạng Fetch Tải Dài Thay Nhúc Nhích Oanh Góc Gọi Bảng Gọi Lướt Quát Này Hiện Ráp Cốt Địch Quanh Sẵn!. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Trí Mạn UX Rắp Trưng Mạch Não Developer 

- [Luật Cõi Oanh Tâm Lí Học Của Dân UX Law Thiết Bảng Mặc Design Bức Rất Tốt Bọc Não Cho Coders (Kho Báo Ánh Chóp Ngành Rớt Khung Ánh Laws of UX Kéo Tịch Sách Học Não Sợ Oanh Bug Chạy Nhấn Oanh Chặn Trúc Trí Độc Giáng)](https://lawsofux.com/) - Trạm Góp Sạch Rót Ngắt Gọi Mắc Lệnh Lấy Góc Design Tới Đỉnh Tỉnh Giảng Bằng Tấm Hình Vi Card Mới Đẹp Cực Lễ Rập Cắt Kín Rút Gọng Chắn Gãy Não Cấu Rảnh. Trúc Code UI Học Tại Bắt Rõ UX Rễ Này Vi Front Gắn Đục Nát Sợi Code Lộn Rác Bẹp Móp Chữa Web.
