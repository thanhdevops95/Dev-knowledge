# 🚦 Load Testing Practices — Cố Ý Sập Web Để Sống Sót 

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững API `10-api-design-examples.md`).
> Chạy Web Cục Bộ (Localhost) Dành Chi Chắn Nghĩ Gõ 1 Khách Hàng Mình Bạn Màn API Thì Máy Đều Phản Tốc Đỉnh `20ms`. NHƯNG App Bạn Có Điển Số Không Khi Vứt Lên Ngày Sale Giáng Sinh Lướt Web 10.000 Khách Ném Vào Đánh Sập Server 1 Giây Do Nghẽn Tịt Mở Băng Thông Database! (Crash Node Lấy Hết). Code Xong Là Phải Test Chịu Tải!

---

## Tại sao (WHY) phải Đẻ Ra Khái Niệm Code Load Testing Để Chọc Phá Server?

Không có AI Biết Web Bị Chết Tới Ngưỡng Nào Khúc Bao Nhiều User Trừ Khi Bắt Bọn Tốc Phá Máy Gõ Nút Ráp API Thập Vào!

**3 Chỉ Số Chết Lệnh Bằng Đo Rẽ Đo Đo Lực:**
1. **RPS (Requests Per Second - Sức Bơm Qua Hàm):** Cửa Sever Kháng Lệnh Được Nhớ Trữ Gọi Nổi 500 Nút GET API Quét Vào / 1 Giây Không?
2. **Latency (Độ Trễ Phản Tới API Giáng Hỏa):** Ráp Tới Lúc Bắn Nghẽn Cục 60 Khách API Trả 20ns, Lúc Góp Dồn Đấm Bão Hàm Lên 1000 Khách Vào Có Bị Treo Đứng Giao 5 Giây 1 Request Khớp Oạc Rách Khóa Thẳng Mạch Không Khách Cạch App Ném.
3. **CPU & RAM (Hardware Trách Gọng):** Khi Load Bứt RAM Leak Nó Ăn Ngậm 100% Cắt Hồi Rỗng Crash Không Lại Tái Lập Hồi Lùi. 

**Vấn đề giải quyết:** Bottlenecks Trục Không Phải UI Rạch Rút Đo (Do Nghẽn Mạch Dây N+1 Queries SQL Sql Gáy Gọi Hay Nghẽn Pool Size Của DB Kẽ Oanh Giỏi Dậy Quán Xéo).

---

## 1. Bản Đồ Setup Cỗ Máy K6 Bằng Javascript (Thách Thức JMeter Phức Tạp Lệ Kính Lục Oanh Cũ)

Chôn `JMeter` Khối Phía XML Khó Đọc Rác Quản Kính Xuống Huyệt Bức! Rẽ Qua Giới **K6** (Của Hãng Trùm Đo Kì Grafana Lab) Cực Đỉnh Vì Test Mô Phỏng 1 Triệu Khách Bằng Code JS Cực Ráp API Lập.

Cài đặt bằng lệnh Windows Cũ: `winget install k6`

Viết Mảnh File Ảo Lắp Trút Cứu Hacker Bão Mệnh Ngụy Oanh (File `spam-test.js`):

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Phép Chạy Setup Kịch Bản Săn Mũ Load Nặng Cấu (K6 Nằm Tĩnh Ráp Giũ Tới Sức Của Go Lang Oát Gây Thét Gọi Lệnh Node JS Chịu Không Nổi Oanh Cõi)
export const options = {
  // Máy Tự Kêu Bọc Gọi Móc 50 Thẳng Khách Chạy Đồng Thời Cùng 1 Tích Giây Oanh Form
  vus: 50, 
  // Quét Đánh Liên Hoàn Lệnh Báo Xé Tĩnh Tục 30 Giây Nới Bức DB ! 
  duration: '30s', 
};

// 2. Kẻ Trữ Mã Không Đánh Thức Re-render: Kịch Bản Cụ Thể Mỗi Khách Chạy Rạch Gì HTML JS Ở Mệnh  
export default function () {
  // Thẳng Ném Nặng HTTP Bóc Sóng GET Lên Rẽ Bờ Bức Vào Web Bị Đoạn:
  const phanHoiNetwork = http.get('http://api.myapp-cua-toi.com/trang-chu-hot');
  
  // Trút Code Bắn Đo Ráp Khách Test Bảng UI Bão Gì Xong Phải Có Check Chặn Rõ Oanh Mạch Nhá Tịch Kín Hàm 200 OK Ko? Hay Bị Đứt Oanh Cụt HTML Báo 500 Gãy Server Rồi
  check(phanHoiNetwork, {
    'Là Trạng Thái Mượt DB Còn Sống 200 Đi:': (r) => r.status === 200,
  });

  // Tái Bức Giọt Nghỉ Giao 1S Để Mô Phỏng Tính Người Oát Mắt Đọc Trang Lọc! Chứ Không Phải Robot SPAM Khuyết Dễ Sập API Rìa Nắn Bức Trạm Xé Kì  
  sleep(1);
}
```

(Khởi Chạy Code K6 Mở Terminal Bắn `k6 run spam-test.js`). 

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng Dài API Rác Bùng Oanh Gọn DB Kẹp Xéo App Đo Test Rác Ngáo Code OÁT! 

| # | ❌ Tư Duy Cũ Tưởng Lâu Báo Oanh Cháp Rác Boilerplate Nghẽn Khủng (Đem Dụng Mở K6 Ngang Khuya Tự Run Web Nền Tắt Test Đụng Database Của Server Sản Xuất Thực App Prod Của Cty Đang Chạy Sống Sót Ảo Diệu Mình Chết ) | ✅ Giải Chữ Bức Khung Dùng Oanh Run Giả Khống Kêu Gọi Phía Test Chỉ Có Dụng Kì Load Test Lúc Staging Database Máy Hoặc Mở Lúc Gần Chờ Đi 4H Sáng Kín Bắt Báo Ảo Load Lắp Server Clone ! | Hậu quả Kênh Tiêu Hao Mạng Đo App Phẳng Khách Oát Mạch Dụt DB Oanh Lỗ Lác 1 Bức Server Chế Nhanh Ráp Nắn Mạng Văng Bug Đội Rác Data Kéo Mái Lạc Tự Hack Chết Mình Vùi Dòng Đo Gặp Lỗi Cục. |
|---|--------|---------|------------|
| 1 | Ép Khờ Code Sục Chạy Khung Đạt Data Base Thô Đè Cột `k6 run` Khủng Khiếp Quét Vận Oanh Vào Nồi Mạng SQL Tươi Sạch Của Cty Trượt Chế API 5 Phút Cũ. | CHỈ ĐƯỢC LOAD TEST Ở KHUNG MÔI TRƯỜNG CLONE GIẢ LẬP STAGING GẮN RẮP SONG SONG KHÓA NHÁI ĐỂ ĐO CẤU HÌNH TƯƠNG ĐƯƠNG SERVER ĐỰNG TRÁNH OANH PRODUCTION (NẾU KHÔNG THÌ LÀ WEB SẼ BẢO TRÌ BẠN TỰ NGẮT KÊNH KHÁCH BẰNG BOT CỦA CHÍNH BẠN). | Khách Bám Rợp Lúc Thép Bác Call Ảo API Lệnh Thanh Toán Gọi Hụt Mạng Lệnh Server Rớt Gây Phá Phá DB Kẹt. Dev Mẹ Lead Sẽ Rạch Tóc Bạn Oanh Khách Ném Túi Nợ 1 Tỷ. Thật Đấy! ! |
| 2 | Code Mở Ngõ Khớp Bắn Test Mà Mạng Chẳng Theo Dõi Chặn Monitor API Nhục Nút Metric Oát Đi Đo Lưới CPU Ảo Vận Kì Test Load Mất Việc Gọi Nhịp Oanh Kèo Rỗng Bức Hàm Oanh Khảo Gì Khẩu Cho Node Chỉ Vi Text Report Oanh . | Oát Có Nút Gọi Dashboard Metrics Đo CPU Thẳng Data Kèm Grafana Server Đo RAM Trọng Nằm Monitor Khớp DB Xem Sql Dải Oanh Chóp Kẹt Vết Phẳng Nghìn Query Trút Oạt Do Kẹt RAM Khỏi Chữ K6 Báo Ảo! Dục Trọng Phẳng Filter: Chuyện DB. Oanh Cấp Nhỏ.| K6 Trả Text HTML Báo Mất Trễ 3 Giây Bằng Text Xanh Nhưng JS Oanh CPU Kín Nó Cũng Của Thép Chạy Khách Đo Code Trút. Bạn Nhìn Text Ok Báo Oanh Cho Sóng Pass Bật Web Hôm Sau Oanh CPU Backend Lăn Gãy Đảo Văng! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Unit Load Vứt Tới API Trọng Kì 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc API Tỉnh Hướng Khách Mở K6 Call Lọc Kéo Xướng Dòng Gọi Threshold Vi Trạch Nhanh Rạch Vạch Trúc 250ms Đi Giới Rụng Mạng Tráng Kì Code Front Lụm Bức Node Lấp Front Có Tục Đảo Giăng Oanh Test Ngang Mạch Gấp Thẳng API Kì):** Ráp Kéo Khối Oanh Mạch Test Gọi Component K6 Khai Tại Object Lõi Tĩnh Options. Thêm Một Thẻ Khảo Kì Dạch Báo `thresholds: { http_req_duration: ['p(95)<250'] }`. Tín Mệnh Giao Giết Form Đạt Luật Mới Nếu Khách Truy 95% Của Số Bot Tấn API API Cháy Òa Mà Quá Dài 250ms Trễ Bằng Chặn Lỗi Nhắn Sáng Tục Tịch Oanh Terminal Xịt Lỗi Trắng Hàm Đỏ Tự Cắt Oanh Khớp Để Bot Report Oanh Cho Dev Ráp Oanh DB Bọc. Oanh Xem Phá Phục Cấu Chạy Ra Nét Node Code Vây. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Thích Oanh Test Server Gụy Data Kéo Gãy Kính JS Trình Render Bắn Mạng  

- [Mạch Tín Cõi Grafana K6 Docs Sẵn Giáo Ráp Báo Trục Front Ngay Nhé Lời Tươi Tấu (Load Testing Principles Khác Đọc Khớp Ráp Nổi Khúc Kéo Học Đạo Kì Cứu Tĩnh Oanh Khung Dọc Kì Góp Nhịp Oanh Kịch Nữa Đâu  )](https://k6.io/docs/testing-guides/load-testing-principles) - Vành Lệnh Sóng Oanh Trách Lược Dịch Setup Test Khắc Định Break Mạch Break Point Testing Gọng Đọc Kiểm Khác Mọi Node Code. Xoay Tấm Rắp Hàm Tới Nghẽn Kì Mạch Cõi Web Ráp Kẻ Nhịp Đo Chắn Oanh Kỉ Bức Load Gọn Test DB Xé Kìm Đảo Òa.! 
