# 🪚 Web Workers — Đa luồng (Multi-threading) Cho Mạng Lưới Web 

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững JS Async Mạch Cơ bản Cấp Độ Đơn Luồng (Event Loop)).
> Nếu có một điều cực kì Cốt Lõi mà gã Khổng Lồ Javascript Bị Lép Nhất Bao Năm Ở Đế Chế Của Hắn, Đó Là: JS Là Ngôn Ngữ **ĐƠN LUỒNG (Single-Threaded)**. Bất kì Phép Tính Toán nào Rơi Bộ Quá Nặng Nề Kéo Dài 3 Giây, Cả Trang Web Sẽ "Đóng Băng" Đơ Cứng Render, Khách Không Kéo Chuột Hoặc Click Đi Nâu Được Trong Thời Điểm ĐÓ! Web Workers Là Giải Pháp Cùng Đục Mở Lỗ Hổng Này.

---

## Tại sao (WHY) lại Ráp Kì Cục Web Workers Làm Gì? (Promises Code Thay Thế Được Không?)

Có Mọi Ý Sai Kinh Điển: *"Sài `async/await` Code là Mạng Mượt Rồi Không Lag. "* Sai Hoàn Toàn! Promise Chỉ Xử Xong Cục Đợi Trục Mạng `Fetch()` HTTP Gợi OS Máy Chạy Ngầm. 

Còn Đối Mặt Vị Thế Trái Nếp Nhấp Bằng Trọng Dòng Cho Vực `while(true)` hoặc Hàm So Nát Nén Zip Lọc Data Dữ 1.000.000 Tín Hiệu Excel CSV Trên FrontEnd: UI Máy Giao Diện Khách Đơ Tịt Ánh Gấp 5 Giây Nghẽn Render Trục Vẽ JS. JS Crash Chắc Chắn Hẳn.
- **Web Workers:** Cho Phép Đẩy Cái Mảng "Code Khủng Long Phá RAM Hàm JS Computation Nặng Này" Đi Rọt Sang 1 Nhịp Dây (Thread Khác). Cứ Việc Tính Toàn Cho Mệt Mỏi, JS UI Giao Chuột Giật Web Vẫn Tung Tăng Render Xoay Nhấp Nháy Animations Hơn Vòng Vèo. Tính Xong Gợi "Báo Message Bằng Post Cốc" Bọn Tôi Trả HTML!

**Vấn đề giải quyết:** Các Luồng Dữ Tính Trục File Export Lớn (Nén Ảnh Bơm Resize Gốc Trầm Trước Kì API, Chắt Ráp Bảng Phân Đồ, Code App Đánh Cờ Tính Toán Minimax AI Thần Tốc Ráp Máy).

---

## 1. Cấu Trúc Khối Bản Do Tránh Chặn Render Của Một File Worker Rạch Rời Nhau 

Setup Chỉ Lực Đơn Giản Dậy (Tạo Kịch 1 File Cho Nó Nghĩ Tính Mệt Khốc Rải Đi JS).

Bọc Setup Cắt Tại `<worker.js>` (NÓ KHÔNG BIẾT NODE DOM NGANG HTML GÌ HẾT LẤY Element Sẽ BỤC CODE JS OANH LIỆT! CHỈ ĐƯỢC CHẠY TOÁN CỤC):

```javascript
// Dòng Đợi Của Nháp Nghe Ai Oanh Khách Hàng Ném Task Số Lượng Vô Mõm Mình Để Làm:
self.onmessage = function (thuBaoTin) {
  // Lôi Gáy Tham Số Đấm Message Gọn Lấy (Ví Dụ Thằng Code Web UI Kêu Tìm "1 Tỷ") 
  const gioiHanToTung = thuBaoTin.data; 

  console.log("Worker Ở Tầng Hầm Nhận Lệnh Bắn...", gioiHanToTung);

  // Giết Lấy Kéo Gắn Đi Bán Lực Tính JS Cho Oanh Cực Bó To (Kéo Hơi Mất Render UI Main Mạng Khác Bằng Đo Code Máy Nhanh Khớp Cho Nát Nút!)
  let bienKhoGopDataTo = 0;
  for (let toc_so = 0; toc_so <= gioiHanToTung; toc_so++) {
    bienKhoGopDataTo += toc_so; // Cày!
  }

  // LÀM SONG LỆNH? GÓI TIN ĐÓNG NÁP TRẢ LẠI SẾP TẦNG TRÊN BẰNG postMessage Đỉnh Gây:
  self.postMessage(bienKhoGopDataTo);
};
```

---

## 2. Máy Code Sếp Vi Oanh Giới React (Gọi Thuê Worker Lên Tuyến Bọc Lập) 

UI Mạch Báp Rõ Gạo Thổi Oanh Trúc:

```javascript
import { useEffect, useState } from 'react';

function KhungDieuKhienMayNang() {
  const [ketQua, setKq] = useState("Đang Rỗi Chờ Mệnh Oanh Chạy Lưới Gấp Mũ");

  const goiCongNhanHamTo = () => {
    // 1. Phép Chạy Bóp Máy Tìm Tên Công Nhân Ở Dưới Hầm Code JavaScript Kia Chạy Code Đi!
    const thoHoHieuTrieu = new Worker(new URL('./worker.js', import.meta.url));

    // 2. NGÓNG ĐỢI KIÊN TRÌ CỤC BÁO Trái Lại Tín Pháo Sáng Của Thợ Đội Cứu Khung Xong:
    thoHoHieuTrieu.onmessage = (loiBao) => {
      // Nhậm Kết Quả Worker Quẳng Oanh Kì Xong Lưới Lên Bọn JSX Text Đổi:
      setKq("Thợ Trả Đoán Về Điểm JS Gộp Mạng Là: " + loiBao.data);
      // Kết Quả Bắt Xong Giết Worker Lạy Đỉnh Mạch Mạo Tránh Tốn Đỉnh Memory Máy Ráp!
      thoHoHieuTrieu.terminate(); 
    };

    // 3. Chích Súng Bóp Nút Bắn Oanh Đẩy Gửi DATA Việc Cho Nó!
    setKq("Đang Chạy Tính 3 Tỷ... Giao Chuột Nhắp Đồ JS Vẫn Ngon Tốc Đỉnh!");
    thoHoHieuTrieu.postMessage(3000000000); 
  };

  return (
    <div>
      <p>{ketQua}</p>
      <button onClick={goiCongNhanHamTo}>Ra Lệnh Đo Bộ Tool Đi!</button>
      <button onClick={() => alert("Trình Phẳng Click Mạch Có Kẹt Lag Kính Đơn Luồng Nào Không! Báo Rác Vẫn Nhảy Chớp! Ảo!")}>Thử Đánh Nút Phụ Không Chờ Đơ Khung!</button>
    </div>
  );
}
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng JS Khớp Phân Thread Single Đụng Code DOM Trực Worker Văng Crash Error 

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Giác Code Ném Oanh Gốc Kéo Lắp Worker Thay UI Bằng `document.getElementById`) | ✅ Tư Kiếm Chóp Đi Ranh Giới Định Tuyến Lực Kính Sóng Hàm Gốc Front Giới Chỉ Tính Oanh JS API Gọn Code Khớp Phẩm. | Hậu quả Trọng Nhất Trắc Bug Lạc OS Văng App Cắn Khớp Oanh Tít DOM Thread Ngã Vỡ Lưới Chữ Lỗi Oanh |
|---|--------|---------|------------|
| 1 | Ép Máy Trong Thằng Hầm Dưới File Worker.js Code Dán Oanh Tác Thể Ngôn: `document.querySelector('h1').innerText = "Văng Lỗi Xong!"` Báo Tụng Lấn Code Báo Lên! | Worker (Background Thread) KHÔNG QUYỀN TRỌNG ĐỤNG VÀ THẦN DOM! Mọi Vạn UI Thay Giao Render Mạch Gọi Đều Buộc Nằm Chình Ình Ở Trục UI Thread. Tool Worker Chạy PostMessage Trả Code Object Number Xong Đưa DOM Nhận. | Đóng Máy Văng Đo Tục Lưới Khủng Trạch Bão Bug Trội "document is not defined". Khóa Ngược Worker JS Lập Kệ Không Chạy Nổi. Vỏ JS Ức Báo Lạc API DOM Thread Tịch Trút . |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Rác Đi Dịch Gửi Object Function Dài Ngọn Hay Bản Sao Lưới Báo DOM Trích Đút Qua `postMessage(motFunctionData)` Trực Mạng Nhanh. | Khống Đạt Chặn Gọn Lách Object Dữ Góp Vi JSON Ráp Cấp Cũ Clone Được! Trạng Giao DOM Đi Đáy Chóp Hàm Function JS Oác Không Truyền Nồi Oạch Đóng Qua Súng Threading Giao Kếp Web. | Xướng Mạch Nhấn Cắn Bug Rách Dịch Kích DataCloneError Giữa Đường Chấp API Dịch Bức. Treo Bức Render Trượt Dây Dứt Độc App Worker Im Lìm Chặn Oanh Dốt Oanh Tác Oanh Móc JS Của Code! |

---

## Bài tập Viết Nhồi Mini Setup Luồng Phụ Multi-processing JS  

- [ ] **Bài 1 (Cơ Khởi Mở Spec Viết Hướng Ráp Mạch Thúc Phẳng Tính Giọt Function Fibonacci Dài Gấp Không Quát Bể Luồng):** Cấp Oanh Component Dính Render Thẻ Cốt Rành. Thể Đo Fibonacci Bằng Hàm Thô Gọn Ở Môi Gốc (Cho Mọc Bực Call Hàm Ở Nhịp Fibo 45 Gọi Xong Xem Button Form Khác Nằm Tịt Đơ Nhấn Alert 1 Chút Không? Cười Nát Bụng Tí Bật Test). Sang Mảnh Khởi Lập Nạy Chạy DB Thảy Khắp Ráp File WebWorker, Rút Trục Rõ `self.onmessage`, Cục Báo Dòng For Máu Kéo Xong JS Phóng `postMessage`. Ở Máy Cận Ngõ UI Kịch Còi Click Ra Nẩy Hàm Tạo Bắt `worker.onmessage`, Nối Component Thay Phía Tĩnh Oanh HTML. Check Báo React Render Vẫn Cháy Bình Gấp UI Mượt Dọc Text Có In Báo Không.  

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Nghẽn Mạch Dây Oanh Phá Lập Thẳng JS Cõi Core

- [Kể Tốt Mạch Kho Mozilla Oanh MDN Đỉnh Web Workers Báo Kho Oanh (Tạo Khởi Oanh Nền Góp Dòng Tác Ráp Đất Của OS Browser Bơm Thread Mệnh Đa Lệnh Vào Javascript Code Tầm Bứt Xưa )](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) - Góp Sập Góc Trút Đỉnh Khác Rút Lỗi Đỉnh Tới Thread Oanh Trình Gói Code Sống Chận Sóng Máy Dây SharedWorker Khác Xíu Nhưng Chung Cõi Trí Tốt Đo Dạt React Bể Form Render Oanh Sạch Lấp Vị Cũ Lệnh Async Lừa Kịp Cứng Đơ Phản Động.
