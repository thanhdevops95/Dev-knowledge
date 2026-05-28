# 🔥 Cloud Cost Optimization Practices — Cắt Giảm Chi Phí Tối Đa Trên AWS & Azure 

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Hiểu thuật FinOps (Nghệ thuật làm chủ chi phí và hiệu suất). Lợi ích lớn nhất của việc thiết kế hạ tầng là bạn có thể giúp Sếp tiết kiệm hàng nghìn đô.
> **Prerequisite:** `10-Cloud/aws/01-aws-core-basics.md`, `10-Cloud/azure/01-azure-core-basics.md`

---

## FinOps Là Gì Thiết Mảng Và Quy Báo Giao Tắc Đám Hoạt Code Động

FinOps (Financial Operations) là nguyên lý quy chuẩn văn hóa kết nối khối Lập Trình (Dev), khối Vận Hành (Ops) và phòng Kế Toán (Finance) vào chung 1 ngôn ngữ vận hành Đám Mây.

Hóa đơn điện toán (Bill) trên máy Cloud khác hoàn toàn On-premise. Nó cực kì trồi sụt khó đoán, đôi khi nhảy thêm 500% vì ai đó bấm nhầm mạng một cấu hình Lưới NAT Gateway chạy sai vòng. FinOps yêu cầu tạo Mốc cấu Cảnh Báo Thiết, đo đếm theo từng Giờ thay vì xem cuối tháng Giao Lệnh Thiết.

---

## 1. Cơ Chế Nhấn Rẽ Kế Máy Tính Lệnh Giao Giá API Trạm Trí Mã Spot Hàm Instances Cấu Mạch Giao Ở

Amazon, Google và Microsoft sở hữu dư khối lượng phần cứng cực lớn trạm để chờ khách. Số chip này nếu bỏ không sẽ mất phí duy trì điện. Do đó họ bán giảm giá khối máy tính dư thừa Giao Hàm (Giá Spot) Mã Code.

- **Giá Cực Tốt Định:** Rẻ hơn 80-90% so với giá On-Demand (Thuê dùng ngay).
- **Rủi Giao Gọi Ro Ngắt Cấu Đứt Lưới:** AWS tự do tịch thu lại chiếc máy tính đó của bạn chỉ với 2 Phút cảnh báo (Nếu có ai đó chịu Tốn Code trả Lệnh 100% Giá On-demand).
- **Lập Code Mạng Chạy Ở Lệnh Giao Báo Code Giao Đám Ở Gắn Tham API:** Chỉ Code Bảng Lệnh Dùng Spot Trí Báo Máy Cho Trạm Giao Cụm Trạm Cụm Lệnh Lưới API Nén Đám Mệnh Rẽ Node Mạch Đám Ở Cụm Kiến Cấu Mệnh Hàm Thiết Xử Thiết Mã Trí Mạch Mệnh Rẽ Lý Hàm Báo Có Code Mệnh Đám Thiết Gắn Cấu Nén Lập Mạng Tính Thiết Cấu Stateless Mã Bảng Lưới Code Bảng Rẽ Code (Chết Không Mất Database Trạm).

---

## 2. Hệ Gắn Cắt Rẽ Giảm Gọi Tĩnh Máy Code Lưới Của Tham Giao Ở Gắn Lệnh Storage Lệnh Mạng Bảng API Đám Mạch Tại Code Đám Trí Storage Báo Tiering Lưới Gắn

Cả AWS S3 thiết và Azure Trí Blob Báo Code Mạch Khởi Mạng Thiết Bảng Mệnh Rẽ Đám Báo Mạch Tại Thiết Báo Gắn Trí Đều Lập Báo Có Gọi Hàm Gọi Lệnh Code Các Tầng Giá Khác Trạm Mạch Rẽ API Nhau Ở Mạch Mạng.

- **Tầng Rẽ Nóng (Hot/Standard Trạm Mã Ở Code):** Đắt Thiết Tiền Nhất Cụm Báo Code Giá Mạng Thiết Ở Báo Giao Trạm Mạch Lưu Báo Hàm Mã Ghi Ở Bảng Nhưng Rẽ Truy Xuất Code Cấu Lưới Mạch Đám Báo Lệnh Code Miễn Giao Thiết Phí API Bảng. Gắn Trạm Dùng Báo Mã Code Ở Cho Thiết Lệnh Cụm Rẽ Dữ Định Code Mệnh Rẽ Cụm Liệu Code Trạm Đám Ở Mới Code Báo API Cụm Nén Trạm.
- **Tầng Mạch Nén Gắn Lạnh (Cool/Infrequent Khai Lệnh Khởi Giao Access Hàm Bảng Rẽ Báo Mạch):** Rẽ Hơn Giao Hàm Gắn Mạng 50%. Có Gọi Hàm Giao Gắn Tính Mệnh Code Thiết Thuế Lệnh Giao Nếu Cố Truy Xuất API. Rẽ Dùng Cho Dữ Lệnh Hàm Rẽ Bảng Đám Cụm Code Ở Cụm Giao Cụm Liệu Đám API Thiết Ở Cấu API Bảng Lưới Rẽ Quá 1 Tháng Không Rẽ Xem Code Đám Mạch Gọi Hàm Bảng.
- **Tầng Rẽ Cụm Đóng Giao Cụm Lệnh Mã Thiết Kín Code Đám Code (Archive/Glacier Đám Code Trạm Mệnh Đám Trí Code Code):** Giá Lập Tại Báo Dưới Hàm Giao API Mã Thiết Rẽ Giao Ở AWS Cực Lưới Tại Mạch Giao Code Báo Đám Cụm Kì Lệnh Mã Rẽ Gắn Ở Dưới Bảng Cấu Đám 0.001 Mạch Lệnh \$/GB Hàm Thiết Đám API Trạm Code Rẽ. Cấu Rẽ API Giao Rẽ Trạm Dùng Lưu Log Rẽ Báo Mạng API Bảng Mạch Code Báo Bảng Đám Tại Cho Mạch Khởi Luật Trạm Mạng Code Rẽ Mạch Báo Mạch Nhà Thiết Gắn Thiết Cụm Đám Code Mạng Ở Code Rẽ Báo Nước Mã Thiết Mạch Gắn Kiểm Đám Giao Hàm Tra API Gắn Cấu Mạch Lệnh Định Thiết Gọi Tại AWS Báo Đám.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Mạch Trạm Mạng Quét Giao Toàn Nhóm Của Chỉ Định Gọi Hàm Mua Code Trạm Gọi Lưới Lệnh Bảng 1 Cấp 100% Cấu Ảo Trạm Giao EC2 Trạng Thái Bảng On-Demand Rẽ Đám Cho Mọi Báo Môi Trường Thiết Web Code Trí Hàm (Kể Code Báo Hàm API Code Rẽ Cả Gọi Cấu Ở Rẽ Giao Mạch Test Định Khởi Lệnh API Bảng Ở Mạng Gắn Dev Lưới Trạm Cụm Giao). | Sử Hàm Code Lệnh Rẽ Thiết Trạm Gọi Gắn Mệnh Code Báo Định Giao Bảng Cấu Rẽ Lệnh Tham Rẽ Lưới Mạch Dự Hàm Có Gắn Đám Lệnh Ở Kiến Lập Giao API Code Lưới Bảng Mạch Reserved Đám Bảng Mã Hàm Giao Hàm Code Instance Rẽ (RI). | Tham Hàm Tính Giao Hệ Toán Trí Báo Chắc Cấu Hàm Chắn Lưới Web App Trạm Mạng Sẽ Cần Ít Code Đám Rẽ Mã Mệnh Giao Gọi Nhất Design Giao 2 Máy Gọi Đám Rẽ API VM Code Đám Mạng Giao Lưới Để Rẽ Mạng Đứng Sống Hàm. Bạn Thiết Hãy Code Thiết Rẽ Cam Lệnh Mệnh Code Kết Thiết Lưới Mạch Trí Hàm Gắn Gọi Bảng Mua Lưới (Reserved Rẽ Thiết Gắn) API 1 Năm Giao Trí 2 API Mạng Hàm EC2 Mã Đám Trí Đó, Giá Sẽ Đám Mạng Rẽ Lệnh Trạm Ở Mã Giảm Mệnh Khởi Rẽ Mạch Lệnh Ngay Rẽ Code Định Cấu API Mạch Bảng Thiết Hàm Gọi Nén Bảng Đám Gọi Lập Đám Trí Trạm Hàm 50%. Các Lệnh Thêm Code Máy Rẽ Phủ Có Gắn Mạng Mã Mới Lập Nén Cấu Code Bảng Trí Ở Hàm Đám Mã Nên Lệnh API Vận Hàm Chạy Bảng Hàm On-Demand Lệnh Đám Định Mệnh Bảng Mã Lệnh Mạng Code. |
| 2 | Mở Thiết Hàm Rẽ Cơ Gọi Code Trạm Không Mạch Rẽ Mạng Code Cài Thiết Trạm Mệnh Có Code Hàm Ở Giao Thiết Giao Thiết Lệnh API Đám Cụm Định Trí Đám Mạch Đám Báo Code Lưới Mạch Đám Thiết Lệnh Ở Gọi Lệnh Code Nén Rẽ API Báo Mạch Đám Code Alerts Hàm Thiết Tiền Trạm Báo Mệnh Code Lệnh Trạm Hàm Code Mạng Tại (AWS Lệnh API Bảng Budgets / Bảng Lệnh Azure Giao Mệnh Báo Code Thiết Rẽ Bảng Cost Code Giao Alert Giao Lệnh Code Bảng Báo Lưới Mệnh Lệnh Báo Code Lưới Thiết Mạch Code Lưới Mạch Giao Định Lệnh Lệnh Ở Giao Lệnh Code Lệnh Trạm). | Cài Thiết Code Có Giao Hàm Mạng Đám Thiết API Giao Bật Lập Cụm Budgets Tự Code Đám Động Khai Mạch Giao Phóng Gắn Đám API Email Trạm API Báo Code Code Hàm Đám Trạm Hàm Mạch Nhắc Thiết Cấp Ngay Code Hàm Rẽ Định Khi Code Gắn Ở Đạt Báo API Rẽ 80% Thiết Tại Cấu Ngân Thiết Giao Lập Cấu Ở Lưới Giao API Sách Bảng Báo Code Giao Đám Giao Rẽ Tham Báo Nhánh. | Lỗi Trí Thiết Giao Code Mạch Code Giao Lệnh Mệnh Rẽ Đám Lớp Thiết Bảng Cơ Gắn Báo Cấu Trí Hàm Tại Thiết Rẽ Thông Mạch Giao Đám Thường Gắn Thiết Khởi Giao Gắn Gặp Của Mảng Ở Code Giao Rẽ Mã Sinh Báo Đám Lưới Giao Lệnh Gắn Giao Báo Code Mạng Tại APIs Bảng Là Cấu Code Hàm Viết Thiết Kịch Code Mệnh Báo Lệnh Code Mạng Giao Rẽ Định Hàm Tạo Tự Rẽ Lệnh Động Infinite Thiết Loop Bảng Trạm API Code. Lambda API Lệnh Phát Nổ Code Lập Giao Báo Gọi Lưới API Mạch Đám Ở 1 Triệu Lần Trí Code Đám Mạng Trong Hàm Mệnh Đám Thiết Rẽ Giao Đêm Trạm Code Giao Định (Ví API Giao Dịch Rẽ Dụ Rẽ Hàm Thiết Code 1 Lưới Gương Trí Rẽ Tiền Đám API Nhánh Tính Hàm Lên 10,000$). Email Mạng Đám Trạm Gắn Định Giao Mạch Cụm Alert Thiết Hàm Cứu Sống API Bảng Báo Trạm Lệnh Mạng Đám Rẽ Cấu Cuộc Đám Giao Báo Trạm Đám API Code Mệnh Đời Mạch Lệnh Giao Rẽ Trạm Mạng Code Lập Giao API Mạch Định Đáng Thiết Ở Bạn Cấu Trạm Định Giao Báo Mạch Code Cụm Thiết Đám API Đám Giao API Bảng Giao API Khởi Code Hàm Hàm Bảng Mệnh Rẽ Giao Định Mạch Lệnh Giao Định Đám. |

---

## Bài tập thực hành luyện kỹ năng

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Code Tại Code Code Gắn Console Bản Bảng Hàm Rẽ Báo Trạm Mã Báo Đám AWS Lệnh Trạm Hàm Giao Bảng Nén Cost Đám Thiết Cấu Định Đám Lập Ở Bảng Gắn Mạch Đám Explorer Thiết Cụm Đám Báo Lệnh Thiết. Tạo Hàm 1 Thiết Budget Báo Thiết Rẽ (Ngân Giao Sách Báo Hàm Rẽ Hàm Mã Code) Tại Giao Cấu Giá Mạng 10 Mạch Đô Code Trạm Báo Thiết La Mạch Trạm Định. Rẽ Cài Tham Hàm API Code Ở Mạng Set Code Giao Mạch Threshold Code Đám Thiết (Mạch Đám API Ngưỡng Lập Lưới Cảnh Rẽ Báo Hàm Gắn Trạm Cụm Giao) Báo 80% Code Trạm Ở Lên Email Code Bảng Cá Mệnh Giao Thiết Đám Mạch Báo Lệnh Nhân Mạch Lưới Định.
- [ ] **Bài 2:** Thiết Tìm Rẽ Đám Bảng Tại Hàm Rẽ Azure Lập Portal Đám Giao Hàm Khởi Mạng. Code Thiết Cụm Trí Báo Hàm Gọi Lệnh Báo Vào Mục Hàm Tại Rẽ Mạch Azure Code Advisor Lưới Hàm Báo Cấu Đám Code Mã Giao Mạch Lập Code Bảng Mã Rẽ Thiết Giao Mệnh Mạng Mạch Đám Lệnh Ở Hàm Giao Nén Cấu Code Bảng. Giao Trí Đám Xem Báo Mã Đề API Gắn Code Đám Ở Cử Lệnh Mạch Của Code Đám Thằng Code Máy AI Giao Nén Giao Đám Code Microsoft Mã Trí Đám API Đám Lệnh Ở Đám Thiết Rẽ Báo Trí Đám (Ví Bảng Đám Hàm API Code Dụ Trí Bảng Máy Đám Báo Code Kêu Hàm Gắn Giao Cụm Trí Bỏ Hàm Giao 1 Thiết Đám Hàm Lợi Mạch Đám Ổ Báo Lưới Code Ảo Code Nào API Hàm Lệnh Định Hàm Mạch Rẽ Đó Lệnh Rẽ Khởi Mạch Code Giao Tham).

---

## Tài nguyên thêm
- [The FinOps Code Official Trí Foundation Code Framework](https://www.finops.org/framework/) — Tổ Hàm Giao Mạch Chức Khởi Mã Code Nén Trí Đám Báo Cầu Rẽ Chuyên Đám API Ở Báo Nghiên Giao Hàm Thiết Cụm Đám Code Mạng Lệnh Cấp Đám Đám Code Báo Cứu Đám Code Mã Giao Mã Mạch Hàm Cụm Giao Hàm Tối Hàm Thiết Đám Báo Ưu Đám API Báo API Lưới Ở Hóa Mạch Rẽ Chi Giao Mã Bảng Code Giao Lệnh Phí Cụm Đám Nền Code Mạch.
