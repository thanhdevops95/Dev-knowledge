# 🔥 Azure Data Basics — Lưu Trữ Dữ Liệu Azure

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hiểu cách vận hành các dịch vụ phụ trợ lưu trữ tại môi trường Azure.
> **Prerequisite:** `10-Cloud/azure/01-azure-core-basics.md`

---

## 1. Dịch Vụ Cơ Sở Dữ Liệu Quan Hệ (Azure SQL Database)

Azure nổi bật nhờ dịch vụ PaaS cho hệ quản trị Microsoft SQL Server. Cung cấp sẵn cơ hội kết nối cho các doanh nghiệp đang dùng SQL Server tại máy văn phòng.

- Tính năng Tự động tối ưu chi phí (**Auto-pause** trong mức Serverless) cho phép hệ CSDL tự tắt để tiết kiệm tiền nếu không có lệnh gọi trong vài giờ.
- Hỗ trợ Elastic Pool: Gom nhiều hệ quản trị CSDL nhỏ (mỗi cái tốn 2 vCores) vào chung một khối dự toán 10 vCores để tiết kiệm tiền phần cứng. (Phù hợp mô hình SaaS đa khách hàng).

---

## 2. Hệ Cơ Sở Dữ Liệu NoSQL Đa Vùng (Azure Cosmos DB)

Nếu Amazon có DynamoDB, thì Azure có **Cosmos DB**. Khác biệt mạng của Cosmos DB là tính toàn cầu hóa cực kỳ xuất sắc.

- Phân tán toàn cầu bằng 1 nút nhấn (Multi-region replication). Bạn gõ 1 dữ liệu người dùng ở Mỹ, nó tự động trích xuất sao lưu 1 bản hiện về máy chủ ở Singapore trong vòng tính bằng mili-giây.
- Hỗ trợ đa dạng hàm Giao Tiếp (Multi-model APIs): Cosmos DB có thể giả lập để tiếp nhận các mã lệnh giống y hệt như MongoDB, Cassandra, hay Gremlin Graph. Bạn không cần sửa Code Node.js cũ lại khi chuyển lên Azure.

---

## 3. Hệ Đệm Lưu Trữ Azure Cache for Redis

Dịch vụ Redis do Azure vận hành theo kiến trúc PaaS thuần. Cấu trúc hoạt động hoàn toàn tương tự ElastiCache bên AWS.
Hệ đệm bảo vệ cho CSDL gốc, tăng tốc độc tải dữ liệu lặp lại.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấu Hình Trực Tiếp Cho Phép Cosmos DB Mở Hàm Địa Chỉ Public Chạm Khởi Gọi Máy Từ Bất Cứ Mạng Nào (All Networks). | Thiết Lập Chặn Cổng Kế Nối Private Endpoint Tại Cấu Hình Tường Lửa Của Cosmos DB. Chỉ Trạm Máy Web Thuộc VNet Mới Được Đọc. | Khối CSDL thường mang thông tin trọng yếu. Đóng bọc Public Access ngăn chặn việc quét mật khẩu DB từ mạng lưới botnet bên ngoài. |
| 2 | Mua Lẻ 5 Dịch Vụ SQL Database Riêng Rẽ Cho 5 Web App Nhỏ Mới Đang Lập Khởi Thử Nghiệm Tốn Kém Cấp CPU Tách Biệt. | Gom Chung Cấu Hình 5 CSDL Đó Vào Cụm Elastic Pool Của Azure Cấu Hình Để Chia Sẻ Chung Phần Cứng. | Bảng phí dịch vụ SQL riêng tốn tối thiểu 15$ - 30$ cho một tháng, nhưng thường 90% thời gian máy rỗng. Ráp chung Elastic Pool tính năng giúp luân chuyển phần cứng lúc rảnh, cắt giảm 70% giá tiền. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Lập Tại Giao Diện Microsoft Azure Portal: Tạo Mới 1 Cụm Azure SQL Server Đi Cùng Một Azure SQL Database. Tại Thẻ Cài Đặt Networking, Nhớ Vận Hành Chặn Public Access Và Thêm IP Hiện Tại Của Bạn Vào Mục Khai Báo Cho Phép Quản Trị Hệ.
- [ ] **Bài 2:** Thiết Lập Tài Khoản Cosmos DB Mới Tại Cấu Cụm Azure. Chọn Thiết Lập Cơ Bản Mã Định (Core SQL API). Lấy Một Lệnh Tải Python SDK Tạm Vào Trạm Máy Local, Áp Viết Đoạn Mã Thiết Code Thêm JSON Text Bảng Score Của Người Chơi Game.

---

## Tài nguyên thêm
- [Phân Trạm Code Kiến Trúc Dữ Liệu Azure Data Architecture Guide](https://learn.microsoft.com/en-us/azure/architecture/data-guide/) — Bảng Liệt Kê Nâng Cao Của Hãng Microsoft Giúp Các Kỹ Sư Công Ty Đưa Quyết Định Phù Hợp Code Chọn Dùng SQL Hay CosmosDB.
