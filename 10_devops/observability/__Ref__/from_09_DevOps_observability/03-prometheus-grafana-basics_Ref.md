# 🔥 Prometheus & Grafana Basics — Cặp Bài Trùng Giám Sát Cấu Hình

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu về giải pháp giám sát thông số hệ thống và vẽ biểu đồ đo lường tốt nhất dành cho Cloud Native.
> **Prerequisite:** `09-DevOps/observability/01-observability-fundamentals.md`

---

## Tại sao Prometheus và Grafana lại đi chung với nhau?

Để giám sát hiệu năng của máy chủ, ta cần công cụ lấy số liệu liên tục mỗi giây (Ví dụ: CPU đang 80%, RAM dùng 2GB).
1. **Prometheus:** Đóng vai trò là cái "Kho chứa số". Nó rất giỏi ở việc đi sang các máy chủ khác (Scraping), hỏi thăm các ứng dụng "Cho tới xin số CPU", và mang số liệu đó về lưu vào cơ sở dữ liệu dạng chuỗi thời gian (Time-series Database). Tuy nhiên, màn hình giao diện của Prometheus rất xấu và cơ bản.
2. **Grafana:** Đóng vai trò là "Bảng vẽ đồ họa". Nó không tự đi lấy số, nó chỉ kết nối vào kho biến số của Prometheus, lấy các con số đó múa bút vẽ ra các đồ thị (Biểu đồ đường, Khối lượng đo Gauge, Biểu đồ thanh) cực kì lộng lẫy và dễ báo cáo cho giám đốc.

Hai ứng dụng này bổ trợ lẫn nhau, làm thành tiêu chuẩn vàng trong mọi dự án Kubernetes và Hệ thống máy chủ ngày nay.

---

## 1. Cơ Chế Lấy Số Liệu Dạng Kéo (Pull Model) Của Prometheus 

Khác với các ứng dụng đời cũ bắt cái máy tính bị tính toán phải chủ động Push (Đẩy) cấu số liệu về máy trắc quang gây nặng hệ thống.
Prometheus dùng chiêu **Pull (Kéo lấy)**. 

Bất kỳ ứng dụng nào muốn cho điểm số cũng phải tự mở cửa 1 cái cổng mạng HTTP tên là `/metrics` ở địa chỉ API của mình (Ví dụ `http://10.0.0.2:8080/metrics`).
Prometheus theo một tệp tin cấu hình sẽ tự đi dạo qua máy đó mỗi 15 giây.
- Bước 1: Prometheus gõ `/metrics`.
- Bước 2: Ứng dụng trả về 1 trang chữ text thống kê rất đơn giản hiển thị số lượng bộ nhớ, tổng số người ấn nút mua hàng.
- Bước 3: Prometheus cắn phần thông tin đó mang về hệ nhét vào kho lịch sử.
Ứng dụng hoàn toàn nhẹ gánh, nếu Prometheus có hỏng mạng, ứng dụng vẫn chạy bình thường.

---

## 2. Ngôn Ngữ Bóc Lọc PromQL (Prometheus Query Language)

Grafana cũng không tự biết lấy cái biểu đồ nào để vẽ. Người DevOps phải gõ câu lệnh kéo thông biến định từ Prometheus bằng mã truy vấn gốc mang tên `PromQL`.

Nhìn thì khó nhưng nguyên tắc cốt lõi: Tên của tham biến + Mốc thời bộ lọc.
```promql
# Hiển thị số lượng RAM đang dùng (thông số trực tiếp điểm số)
process_resident_memory_bytes

# Tìm Lọc Tham Cấu Lệnh: Chỉ lấy CPU của hệ máy có nhãn Job là API
process_cpu_seconds_total{job="backend-api"}

# Tính Tốc Độ Gia Tăng (Lệnh Rate): Đếm số lỗi Error trong 5 phút qua xem nó tăng bao nhiêu lần trên 1 giây
rate(http_requests_total{status="500"}[5m])
```

---

## Gotchas — Những lỗi thiết quản mạng thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấu hình cho Prometheus tự động quét thu lượm dữ liệu của các máy con bằng cách thiết lập thời đại kỳ Scraping Interval siêu nhanh, khoảng độ gõ lấy số liệu kéo liên tục 1 giây/lần. | Tôn trọng sự cân bằng, cài đặt cấu thời điểm định quét Pull máy tính khoảng từ 15 giây hoặc dài 30 giây rẽ một lần. | Việc chọc máy `/metrics` mỗi một giây tạo ra 1 khối lượng rác dữ liệu khổng lồ (Do Prometheus ghi tất thông tin vào Time-series). Chỉ tầm 1 ngày ổ cứng Prometheus sẽ cháy RAM hoàn toàn. Khoảng giãn cách 15s đủ cho việc dựng đồ họa. |
| 2 | Code lấy đo điểm cài trên máy Grafana, dùng các câu lệnh hàm kéo trích PromQL quá phức tạp sử dụng nhiều biến số nhân như `rate()` nhưng không có bộ giới hạn Mốc Rào lọc `[]`. | Gắn chặt giới hạn tính toán theo thời mốc lưới (Ví dụ trong vòng quét số `[5m]`). | Lệnh `rate()` bắt máy phải tính sự thay đổi tốc độ tăng trưởng. Nếu báo không báo mốc ngoặc vuông, Prometheus tự đào hệ tính số từ 1 năm trước đến hiện tại gây treo toàn hệ CSDL của khối Prometheus và Grafana báo lỗi Gateway Timed Out. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cài máy ảo Docker Compose tải đủ cụm ứng cài cả 2 hộp máy `Prometheus` và hộp đồ mạng `Grafana` kết nối chúng từ đầu. Cấu hình Grafana khai báo bộ Data Source gọi Data gốc trỏ vào cái IP của Prometheus.
- [ ] **Bài 2:** Thiết lập một Node.js app nhỏ dùng thư viện cài biến số mạng `prom-client` gõ hàm xả định cổng số tại biến API `/metrics` và chỉnh Prometheus quét vào cái địa chỉ cổng HTTP của thư viện.
- [ ] **Bài 3:** Lập lệnh Dashboard đồ thị mạng rẽ ở trong phần giao diện công cụ Grafana. Lấy thẻ Widget tạo 1 bảng biểu lệnh theo quy mẫu Line Chart (Đường Chỉ Cụt). Gõ ô Query chữ mảng báo lệnh lấy mạng bằng PromQL lệnh thiết của bài số Hai báo.

---

## Tài nguyên thêm
- [Prometheus Official Documentation Design Cấu Tích](https://prometheus.io/docs/introduction/overview/) — Điểm tra tài liệu móng cơ của CSDL Prometheus cài mảng lệnh.
- [Grafana Tutorial Dashboard Đồ Đám Lưới Thiết Kế Báo Trạm](https://grafana.com/docs/grafana/latest/getting-started/build-first-dashboard/) — Lập lệnh giao quản học trang cấu hình giao lưới đồ họa thiết kĩ biểu của hãng màn thiết.
