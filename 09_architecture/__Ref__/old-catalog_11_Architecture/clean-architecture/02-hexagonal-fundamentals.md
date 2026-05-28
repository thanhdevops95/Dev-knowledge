# 🔥 Hexagonal Architecture — Kiến Trúc Lục Giác (Ports & Adapters)

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Một hiện thân khác của Clean Architecture nhằm nhấn mạnh việc cắm rút chức năng như cổng USB.
> **Prerequisite:** `11-Architecture/clean-architecture/01-clean-architecture-fundamentals.md`

---

## Từ Kiến Trúc Củ Hành (Clean) Đến Kiến Trúc Lục Giác

Hexagonal Architecture, được chế tác bởi Alistair Cockburn, còn có tên gọi nguyên thủy là **Ports and Adapters** (Cổng và Bộ Chuyển Đổi).
Thay vì tập trung vào chia 4 vòng tròn như Clean Architecture, mô hình Lục Giác chia hệ thống làm hai mảng phân bổ cực kì đối lập: **Bên Trong** (Phần lõi nghiệp vụ) và **Bên Ngoài** (Mọi thứ kết nối với nó).

Hình lục giác (6 Cạnh) chỉ là biểu tượng thị giác để thể hiện ứng dụng có nhiều Cổng kết nổi ở các hướng khác nhau (Cổng API, Cổng GUI, Cổng Database). Bản chất lõi không cắm chặt vào bất cứ hệ thống nào.

---

## Cơ Chế Giao Tiếp Bằng Cổng Phích Cắm (Ports & Adapters)

Toàn bộ sức mạnh của Lục Giác xoay quanh 2 loại thiết bị kết nối. Ứng dụng nghiệp vụ thuần túy nằm ở trung tâm và công bố các "Cổng". Còn thế giới bên ngoài (Web, SQL, Kafka) sẽ tạo ra các "Phích Cắm" để nối vào cái cổng đó.

1. **Ports (Cổng chờ nằm trong lõi Lục Giác):**
   Là các Bản giao ước (Interface) viết bằng code Thuần (Vd: `interface IUserRepository` hứa sẽ có hàm lưu dữ liệu, nhưng không ghi rõ lưu bằng MySQL hay lưu tệp Text).
2. **Adapters (Bộ Chuyển Chân Cắm nằm ở ngoài lõi):**
   Là các đối tượng cụ thể (Vd: `Class MongoUserRepository implements IUserRepository`). Class này dùng lệnh của thư viện MongoDB, nặn luồng thông số và tuân thủ đúng giao ước mà Cổng Interface yêu cầu.

Nhờ kĩ thuật này, Lõi ứng dụng điều khiển lưu dữ liệu thông qua cái "Cổng", thay vì gọi Đích danh tên của đối tượng "Bộ chuyển đổi". Khi cần thay thế MongoDB sang PostgreSQL, kĩ sư chỉ đúc lại 1 cái "Phích cắm chuyển Adapter PostgreSQL" mới và nhét vào cái "Cổng", Hệ Lõi ở giữa không biết và không cần quan tâm sự đổi thay này.

---

## Phân Phân Nhóm Thể Loại Cổng Lập (Driving và Driven)

1. **Driving / Primary (Cổng Gọi Vào Mạng):** Giao diện chịu tải lệnh xuất phát từ người khách gọi vào. (Ví dụ: Web API Controller HTTP). API này gọi vào Cổng Lạc Nghiệp (Use Case) để đánh thức hệ thống tâm mạch.
2. **Driven / Secondary (Cổng Gắn Ra Ngoài):** Là nhóm cổng xuất kết nối ra nền tảng sau lưng Lục Giác. Ví dụ: Lõi ứng dụng chạy xong và cần lưu DB, lõi sẽ bắn dữ liệu qua Cổng Secondary để đánh thức ổ đĩa lưu cơ sở.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Khai Báo Object Framework Lõi Phân Ở Đáy Nghiệp Vụ Sử Dụng Class Trực Tiếp Địch Danh `MySQLDatabase`. | Áp Dụng Lưới Cắm Theo Hình Thức Interface Cắt Trục (Inversion of Control - Đảo Ngược Sự Phụ Thuộc). | Core Business không thể tham chiếu đến Thư Viện DB. Bằng cách định nghĩa 1 Interface tại Core Business, và để Adapter DB Triển khai kế thừa Interface đó, luồng chạy thực thi là Core gọi Interface (Trống Nỗng) và Framework nạp ngòi Code Class Thật vào Interface lúc khởi chạy. Lõi không gục gạch DB. |

---

## Bài tập thực hành luyện kỹ năng

- [ ] **Bài 1:** Thiết lập một Cổng (Interface) `NotificationPort.ts` chứa duy nhất một giao diện hàm `send(userId, message)`. Không định nghĩa chi tiết. Nằm trong phân mục Cốt lõi Lục Giác.
- [ ] **Bài 2:** Thiết lập 2 Bộ kết nối Adapter. Một cái là `EmailAdapter` chứa code gửi thư dùng hàm SendGrid, 1 cái là `SMSAdapter` chứa giao diện AWS SNS bắn tin nhắn. Cả hai Adapter dùng lệnh kế thừa và tuân thủ quy tắc của `NotificationPort`.

---

## Tài nguyên thêm
- [The Hexagonal Architecture Guide Origin](https://alistair.cockburn.us/hexagonal-architecture/) — Bài định tính Cấu trúc danh tiếng do chính kỹ sư Lục Giác Alistair Cockburn ghi chép và mô tả gốc.
