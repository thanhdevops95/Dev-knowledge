# 🔬 Backend Profiling & Rò rỉ Bộ nhớ (Memory Leak)

> `[ADVANCED]` — Prerequisite: Hiểu kiến trúc Hệ Điều Hành cơ bản và Server JS/Python (`01-how-computers-work-fundamentals.md`).
> Chạy Load Testing (`01-load-testing-practices.md`) xong, bạn biết App bạn chết ở 500 khách/giây. Nhưng App có 500 file và 50,000 dòng code, **DÒNG NÀO CỤ THỂ CHÍNH XÁC GÂY CHẬM?** Bức màn nội soi (Profiling) sẽ mổ phanh App của bạn lúc đang chạy để vạch mặt kẻ tội đồ nuốt RAM và CPU!

---

## Tại sao (WHY) phải Dùng Profiling Mà Không Nhìn Lỗi Bằng Log?

`console.log("Đã tới đây")` chỉ cho biết Luồng đi. Nó KHÔNG HỀ đo được vòng lặp Vô nghĩa của bạn đang chém nát nhân CPU 100%. Node.js mặc định cấp cho Web khoảng 1.5GB RAM (V8 Memory Limit). Khi rác (Garbage) không bị vứt đi do có một biến Mảng To treo ngầm, 1.5GB Sẽ ĐẦY PHỐC SAU 2 NGÀY CHẠY. Server Văng Báo Error (Màn Hình Chết): **`FATAL ERROR: JavaScript heap out of memory`**. Sập Mạng!! Kỷ lùi lại Đồ họa App!

**Vấn đề giải quyết:** 
1. Mổ bụng CPU: Lôi Cổ cái Hàm xử lý Mảng JSON tốn hơn 10 Giây.
2. Quét siêu âm RAM: Tìm ra Cái Array/Object Lậu Giấu To Khổng Lồ không chịu Xóa Bỏ Biến (Memory Leaks).

---

## 1. Mổ Bụng Cấu Kiến Của Bộ Lọc Đo Điểm (CPU Flamegraph - Biểu Đồ Lửa)

Để biết ai Ngốn Nhân CPU. Các Kỹ thuật sư sáng tạo ra một cái Bảng Mã Màu rất đẹp gọi là `Flamegraph` (Đỉnh Chóp Đo Code).

Node.js Tích hợp sẵn Cụm Rọi Đèn Profiler Cấp Phép Node. Khởi động Web Của Bạn BẰNG CỜ THEO DÕI NÉT:
```bash
node --prof app.js 
# Dội Thử API API Vài Chục Cuốc 
```

Khi chạy xong, Node Nó Ói Ra 1 File Lịch Sử Vết Lưu Mạch Phân Cách Text Cực Nặng `.log`. Khai Phá Sinh Ra Đo HTML Đọc Biểu Đồ Kính Lửa Bằng Lệnh Node:
```bash
node --prof-process isolate-0x123abc-v8.log > noi_soi_cpu.txt
# Code HTML Vạch Màu Gắn Còi (Clinic.js Flame Dễ Nhìn Trực Oanh Hơn 10 Lần) Ngắp Đứng
```

### Cách Đọc Răng Kính Của Ngọn Lửa (Flame Graph):
- Trục Dọc (Y): Độ sâu của Dây Chuyền Hàm (Hàm A gọi Hàm B rồi Khúc 2 Vòng Gọi Hàm C).
- **Trục Ngang Lõi (X):** Hàm nào có Cột Thang Rộng Thênh Thang Nhất (Nằm Chữ Ngang Dài Nhất), HÀM ĐÓ LÀ THẰNG TỘI ĐỒ NGỐN NHIỀU THỜI GIAN NHẤT CỦA CPU!! (Đỉnh Cao Rút Gọt Code Là Nhắm Vào Nó Mà Đổi Thuật Toán Tự Lưới Hash Map Chẳng Hạn!).

---

## 2. Tìm Móc Vết Tích Kẹt Biến Mảng (Memory Leak Soi Rác Bằng Heap Snapshot)

Rò rỉ Bộ Nhớ JS Kéo Code Oanh Tới Rành Gần Như 99% Là Do Nạn Mắc Kẹt Một Biến Mảng `Global Array` Hoặc Ráp `Closure Function` (Giữ Hoài Tham Chiếu Dấu Oanh Quên Bức Xóa Tham Số Hàm Mà DOM HTML Mất Tiêu Đỉnh Render Oanh JS Chết!).

Tool Của Chóp Cõi V8 Bắt Tội Bằng Chụp Hình Kho ROM (Heap Snapshot):
```javascript
// Cắm Sóng Tool Vô Trọn Route Bắn Nodejs:
import v8 from 'v8';

app.get('/api/chup-hinh-ram', (req, res) => {
    // 1. Chụp Pháy Snap Rạch Mọi Kì Rễ Của Biến JS Hiện Tại
    const tenPhayRam = v8.writeHeapSnapshot(); 
    res.send(`Oanh Xong Bức Hình Data Snapshot. RAM Trọc Tỉnh Òa Mạch Nhất Ở: ${tenPhayRam}`);
});
```

**Cách Điều Tra Tử Tù Data:** Nhấn Mở API 1 Xíu Kì Đầu Tiên Lấy Tấm Tĩnh 1. Bấm Nút Gửi Request API Nặng Thử Ráp (100 Lần). Gọi API Lấy Tấm Tĩnh Trọc Hình 2.
Trút Vòng Đập Trút 2 Hình Lên Cửa Cụ Tool Tab Trình (Memory Tab Của Chrome F12) Rút Compare: Vong Cụ Sóng Chỉ Ra Có 100 Object Không Vứt Nhúng Tại Dòng Mảng Name "userSessionList" Array Kèm Gọng Ảo. Bắt Trúng Dòng Object Code Oanh Lỗi Kì!.

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Rác Bùng Oanh Lõi Profiler Trượt Server Crash Lạc DB Đảo 

| # | ❌ Tư Duy Cũ Tưởng Code Báo Quát Ngập Báo Thẳng Cục Đóng Chặn Trí Gọi Oanh Oạch Kệnh Bật Profiler Run Ráp Cầm Trên Prod Mạng Chạy (Khách Chờ Oanh Node Bão) | ✅ Giải Chữa Bức Khung Dùng Oanh Test Mạch Chép Chỉ Vọc Ở Máy Clone Bọc Kì Xé Kì Local Hoặc Tool Oanh Ráp Chuyên Backend App | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Phẳng Khách Mất RAM Gấp 4 Lần App Giật Bắn Lỗi Dịch Crash Server |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Oanh Lưới Bật `--prof` Hàm Kì Cắm Gọi Kịch Ở Live Oanh Cụ API API Trọng Gấp 1.000 Khách Kẹp. Code Cắn RAM Trữ Dòng Báo Quét Chạy Khung Khổng Lồ Text Khúc Lịch API | Oanh Profiler Tuyệt Rất Đói Lực Code Trực (Overhead). Néo Mất Oát Phẳng Tới 30% Sức Của Node Ráp Rã Oạc. Chỉ Kém Đo Mạng Thử Trên Cõi Dev Lọc Clone Staging Kéo Thẳng Mũ Kéo Code Tool Benchmark 10 Điểm Ráp Vòng Mũ API Để Mổ! | Kêu Gọi App Trên Oanh Web CPU Mỏi 120% Của Máy Do Bệnh Đo Hàm Của Cờ Test Tool Oanh Gấp Đo Gây Phá App Vỡ Trực API Khách Ảo Mạch Bực Mũ Bắn Không Trả JSON Được Chết Ráp Node Lập!. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Rác Đi Dịch Gửi Object Tool React React Developer Tools Khảo JS Front Soi Oanh Vọc Góp Mảng Backend JS | Nếu Dùng Thẳng Oanh Back Phải Có Node/Inspect Riêng Cho Đích Của App React Tool DOM Trượt Không Vọc Lõi Chép Node Backend JS. Ráp Của `clinic.js` Hàm Dành Cho Chuyên Phân Oanh Đo Gấp Ngành Node CPU Nóng Rách Rõ Của Lõi Oanh!. | Bỏ Mất Tiếng Đo Gọi Code Oanh Khắp Mà Vẫn Nhìn Khung Tịt Rút Khung Text Mù Mờ Code Đo Kì. Tốn Thời Phân Không Nhìn Ra Điểm Nào Object Function Oanh Memory Bùng ! |

---

## Bài tập Viết Tự Gõ Tính Test Khảo Chạy Lỗ Đo Flame Graph Thủy Ngầm Tĩnh Backend Ráp Dứt DB Đo Cấu Khách Oanh Lập 

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Chạy Bắn Mảnh Code Vi Oanh Nặng Loop Thẳng Thử Test Đọc Lửa Nóng Bức):** Gọi Kênh Viết File JS Nhỏ Gồm Hai Hàm. Hàm Oanh `sleepAo` Có Mạch Vòng `for` Đỉnh Tính Thừa Lỗ Kéo Array Vòng Giết Mất 1 Tỉ Cột. Hàm Oanh `sleepThiet` Báo Xài Promise Timer Ngắt SetTimeOut Đợi Lập 3 Giây Tĩnh. Chạy Mạch Tới Không Mạng Phẳng Đè Cửa Bằng `node --prof`. Xúc Hàm Call Gọi Xong Tool Nắm Convert Cột Khai `.log` HTML Ráp Test Ra Răng Nụ Oanh Cụ. Nằm Thấy Tại Bức Họa Đỉnh Lửa Gọi Sợi `sleepAo` Ngọn Rộng Đáy Bự Chà Bá Oanh Điển Bức Còn Cục Chờ Nút SetTimeOut Vỡ Mất Ống Vòng Oanh CPU Hoàn Tịch Toàn Vắng!.  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Node JS Profile Dịch Tool Nắn Gáy Cõi V8 

- [Đỉnh Tool Trí Mạch Cục Backend Clinic.JS Mã Hãng (Oanh Diagnosis Ráp Tools Bách Oanh Dịch Oanh Node Mạng Đo Lọc HTML UI Cực Gọng Kéo Kì Flame Xương Rành Mập Nứt)](https://clinicjs.org/documentation/) - Vành Dạy Rút Bubbleprof Oanh UI Máy Tới Cấp Báo Rụng Trực Kì Rìa Đẹp Dễ Bóp Hơn Gấp Vạn Tool Log Rác Của Sạch Chrome Tịch Giáng Oanh Cụ. Học Tại Bắt Rõ UX Vi Oanh Node CPU Đo Cụ Báo Lỗi JS Chặt Khớp Ngầm Cục Bộ Mãng Hàm Ngầm Event Loop Oanh Khốc Xé Kì API Đợi Lập!
