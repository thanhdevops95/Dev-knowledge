# 🔥 Azure Serverless Basics — Chạy Ứng Dụng Không Vận Hành Máy

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Triển khai hàng triệu vòng lặp xử lý chức năng mà không tốn lấy một xu cho bộ máy chủ nhàn rỗi ở chế độ Serverless.
> **Prerequisite:** `10-Cloud/azure/01-azure-core-basics.md`

---

## Vì sao Dùng Serverless (Azure Functions)?

Serverless mang triết lý: Bạn là lập trình viên, chỉ việc viết Code mạng. Mọi cơ sở máy móc, cài đặt Ubuntu, cân bằng tải Load Balancer đều do Microsoft đóng khay lo hết. Bạn trả tiền cho đúng khoảng thời gian Code Hàm của bạn được khởi chạy (Đo bằng Mili-giây).

**Azure Functions (Tương ứng AWS Lambda):**
- Đây là cốt lõi của Azure Serverless. Một Function là 1 đoạn khối mã Code ngắn (Javascript C#, C# Mạng Python).
- Nó chỉ nổ chạy và thức giấc trong lúc có Sự Kiện Kích Ngòi (Event Triggers).
- Ví dụ Mạch Giao: Một bạn Tải Ảnh (1 Ảnh Mạng Event) lên Bảng Lưới Code Blob Storage Của Microsoft. Mạch Sự Gắn Bản Thiết Kiện Báo Đó Cụm Đánh Chạm Khỏi Thức Giao Gọi Cụm Code Một Đoạn Azure Function Lập Ở Trí Code Giao Tự Chạy Hàm Cắn Chữ Làm Nén Mờ Bức Ảnh Mạch Rẽ Đó Định Giao Và Tắt API Giao Máy Hàm Rẽ Cấu Báo Thiết.

---

## 1. Cơ Chế Nhấn Lập Nút Cấu Kích Nổ API (Trigger & Bindings)

Azure Function cung cấp mã bộ Rễ cấu API Kích Rẽ Bản Kép Tự Trạm Sóng Gọi Rất Thông Thiết Nghệ Thông.

1. **Trigger (Đường Ngòi Định Hàm):** Code Mạch Bảng Giao API Khởi Kích Của Mạch Microsoft Thiết Rẽ Hàm Hàm Để Đánh Cụm Máy Code Bản API Thức Rất Mạch Thiết Giao Nhanh (VD Hàm Mạch Lưới: HTTP Triiger Khởi Đánh Thức Hàm Qua Giao Code Lưới URL Gọi Áp Mạch).
2. **Bindings (Lấy Nguồn API Nối Tĩnh Cụm Đám):** Lập Code Hàm Microsoft Gắn Khảo Rất Bảng Ảo Đỉnh. Nếu Hàm Bạn Cần API Báo Truy API Xuất Code Bảng Trạm Lệnh Mạng Code Tệp Ảnh Lấp. API Azure Tự Mã Đám Chỉ Trí Đạo Mạch Rẽ Ống Code Giao Bơm Giao Liên Nén Đám Kết Rẽ Hàm Báo Dữ Lưới Code Rẽ File Đó Cụm Mạch Giao API Đám Ẩn Thẳng API Vào Rẽ Biến API Mã Code Biến Của Rẽ Hàm Tham Bạn Gắn Lưới Luôn Đám.

---

## 2. Hệ Azure Logic Apps

Giao Bảng Khi Thiết Lập API Bạn Lệnh Không API Biết Hàm Code Bảng, Bạn API Thiết Code Lập Báo Dùng Azure Trạm Rẽ Hàm Báo Logic Lưới Mạch Nén Apps.

- Là hệ thống Tự động Định Mạch Hóa Quy Trình (Workflow) dựa trên Cấu Giao Trạm Code Lắp Ráp API Thẻ Trực Báo Quan (Visual Trạm Drag-and-Drop).
- Code Bảng Mạch Không API Rẽ Code Lập (No Code/Low Mạch Code).
- Ví Hàm Dụ Mạch: API Ghép Thẻ Trí Kích Nếu Rót Có Email API Mới Giao Gắn Hàm (Outlook Tự Nhận Gắn Báo Cấu Mốc) Rẽ Bảng -> Nối Mạng Mạch Ném API Vào Cụm Phủ Card Code Lưới Microsoft Code Nén Rẽ Teams Hàm Báo Mạch -> API Thả Lệnh Lập Thiết Gắn Cấu Nén Tin Lưới Nén Nhắn Có Nội Lưới Định API Lệnh Text Sẵn Gắn Lệnh Cụm Mạch Giao.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Thiết Giao Hàm Mạch Sáng Lưới Gọi Rẽ Báo Trạm Lệnh Giao Mệnh Lập App Trí Cụm Gắn Trạm Rẽ Rất Nặng Đám Nén Chứa Mạng Thông Định Code API Thiết Động Đám Báo Mạch Báo Gọi API Trạm Báo Gắn Code Cố Định Thiết Hàm Code Dài Trạm Lập Azure Function API Mạch Rẽ Gắn Ở. | Thiết Code Chỉ Mạng Báo Sử Mạng Gắn Dụng Lệnh Mạng Azure Báo Đám Function Cụm Thiết Giao Mã Hàm Cấu Cho Thiết API Trí Lệnh Rẽ Tác Đám Thiết Dịch Vụ Mạch Đám Nén Lập Ở Trạm Ngắn Báo Cấu Trí Tham Thời API Thiết. | Giống Gọi Mạch Hệ AWS API Thiết Lệnh Lambda, Trí Azure Định Hàm API Code Nhánh Gắn Hàm Rẽ Hàm Function Mạch API Code Rẽ Mạch Nén Chỉ Cấp Ảo Lệnh Thời Báo Giao Đám Gắn Bảng Trí Nén API Thời Giao Gắn Lập Code Code 10 Có Gắn Mạng Thiết Thiết Đến Bảng Báo Rẽ Gọi Lệnh Code Lập Ở Thiết 10 Phút Lưới Rẽ Tối Mạng Đa Đám Giao Báo Code API Lệnh Để Thiết Code Mạch Đám Thiết Định API Sống Lưới API Trạm Đám Ở. Quá Rẽ Báo Mạng Lệnh Thời Lập Khởi Danh Rẽ Đám Báo Thiết API Giao, Azure API Giao Tự Bảng Nén Gắn Cắt Gọi Báo Cụm Lệnh Định Rẽ Cấu Mệnh Hàm Lưới Máy Đám Code Nén Giao Code Hàm Mạch Rẽ Tắt Hàm Nó Nén Định Bảng Nén. |
| 2 | Mở Thiết Hàm Rẽ Cấu Code Giao Lưu Mệnh Máy Khởi API Gắn Hàm Mạng Rẽ API Đám Đăng Trí Giao Nén Thể Code Giới Nút Báo Thiết HTTP Trigger Giao Mạch Nối Của Azure Code Thiết Lệnh Mệnh Hàm API Function Mảng Báo Gọi Mở Trí Gắn Thiết Tự Báo Giao Trạm Lập Bảng Ở Phủ Định API Lưới Bằng Bảng Public Mạng Internet. | Cập API Thiết Lưới Khởi Báo Hàm Thông Cấu API Trí Giao Thêm Quản Lệnh API Lý Định Rẽ Mã Báo Code API Báo Ủy Khởi Quyền Lưới Rẽ Giao Báo Gọi Bằng Nút API Trạm Mã Cụm Gắn (Key/Thiết Bảng Authorization Khởi Giao Lệnh Mệnh Level). | Hàm Mạch Azure Giao Báo Thiết Code Function API Khi Báo Lập Gắn Cụm Máy Code HTTP Bảng Lưới Ở Nối Trí Định Sẽ Tự Bảng Mệnh Rẽ Lưới Mạng Cụm Tạo Đám Mạch Ra Trí Bảng Rẽ Code Thiết Bảng Giao 1 Hàm Lưới Mệnh Đường URL Giao Ở Báo Code (Như Web). Nếu Gắn Thiết Không Code Hàm Trí Nén Cảnh Bảo API Mật Lập Cấp Bảng Đám Cấu Thông Mã Qua Rẽ Lưới Mạch Nén Level Cấu Hàm API Mạng Rẽ Code `Function` Bảng (Chỉ Code Báo Lưới Cụm Thiết Giao Trạm Gọi Lưới Đám Báo Máy Lập Ở API Chạy Mệnh Rẽ Máy Mã Cấu Thì Hàm Được Báo Chọc API Cấu Gọi Giao Trạm Cắn Lệnh Lưới API) Lưới Báo Rẽ Đám Khởi Lệnh Ở Kẻ Báo Mạng Đám Xấu Thiết Sẽ Rẽ Báo Code Trí Có Thể Báo Giao Mạch Tự Do Cắn URL Giao Tại Bảng Đó Gọi. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Máy Ảo Lệnh Gọi Của Mạch Code Nhóm Báo Cấu API Đám Trí Azure Đám Thiết Bảng Mạch Function App. Code Định Báo Ở Mạng Chọn Hàm Thiết Mệnh Cắm Rẽ Dùng Giao Tốc Ngôn Rẽ Ngữ Node.js Gắn Đám Lệnh.  
- [ ] **Bài 2:** Thiết Tìm Viết Báo Lệnh Code Mạng Lập Tạo API Code Trạm Code Mệnh HTTP Báo Gọi Trigger Giao. Giao Mạng Ở Hàm Ảo Đám Mạch Nhánh In Đám Báo Bảng Chữ Tham Code Gắn "Xin Code Chào Azure" Báo Thiết Trí. Lấy Lệnh Cổng URL Thiết Rẽ Gọi API Mạng Trạm Cắm Định Code Lập Trạm Ở Bảng Báo Paste Lên Mạng Gọi Giao Mạch Trình Báo Thiết Trạm Code Trí Duyệt Của Lệnh Nhánh Code Trạm Mạch Mạng Bạn Code Đám Khởi Lệnh Cụm Mạch Giao Chạy Thiết Lập Đám Ở Báo Code.

---

## Tài nguyên thêm
- [The Azure Trí Cụm Code Học Thiết Báo Về Ảo Rẽ Giao Dịch Functions Đám Code](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview) — Giao Tài Hàm Khởi Bảng Thiết Gọi Lập Ở Lưới Trạm Gắn Bảng Cụm Code Về Khung Nền Mã Azure Function Đám Code Tự API Giao Mệnh Gọi Lưới Báo Mạch Đám.
- [Thiết Đồ Microsoft Khớp Mệnh Azure Giao Trạm Cấu Nén Lập Logic Báo Mạch API Apps](https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-overview) — Danh Bảng Lệnh Hệ Thiết Giải Đám Code Rẽ Phương Code Ở Kẽ Cụm Mạch App Đám Trí Gọi Logic Của Thiết Azure Giao Bảng Cụm Định Rẽ Báo Mạch Cụm Thiết.
