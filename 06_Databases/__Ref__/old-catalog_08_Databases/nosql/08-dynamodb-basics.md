# ⚡ DynamoDB Basics — Con Quái Vật Trọn Đời Không Đổi Tốc Độ (NoSQL Key-Value / AWS)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Khái niệm JSON `08-Databases/data-formats/01-data-formats-compare.md` và Khái niệm Serverless.
> SQL Database là Xe Số Sàn (Phải tự đổi số Rút tăng Tốc Ổ cứng RAM). MongoDB là Xe Tự Động. Còn **DynamoDB** là Tàu Điện Siêu Tốc Maglev chạy lơ lửng trên Không! Bạn ném cho nó 1 Bản ghi Dữ liệu, nó truy vấn mất **5 MiliGiây**. Bạn ném cho nó 10 Tỷ Bản ghi (Big Data), nó vẫn cứ trả vể cái Tốc độ Chết tiệt đó: **5 MiliGiây!** Mãi Mãiiii! Không Bao Giờ App Bị Chậm Đi! 

---

## Tại sao (WHY) AWS DynamoDB Là Vua Của Serverless DB?

Nó sinh ra từ nôi của Amazon để giải Cứu Hệ Thống Bán Lẻ ngày Black Friday.

1. **Serverless (Phi Máy Chủ):** Khái Niệm Tựa Bạn KHÔNG CẦN Chọn Cấu Hình Bật CPU RAM DB SQL Máy Nữa. Bạn chỉ việc Chạy Create Bảng Trên AWS Cửa Giao Diện Gõ Code API Lên. Bạn Tốn Trăm Data Trả 10 Đồng Tiền Data Gấp Bạn Trả Cứ. (Đứng Chấp 100K Users Tự Nó Phình Giới Trạm Lưới Máy AWS Khắp Cõi Mỹ Sing Kì Diệu Ráp Cúa).
2. **Khóa Ánh Sáng Mạch (Hash Table):** Giống File Cassandra Rìa, Nó Lưu Data Trúc Dựa Vào Mã Lệnh **Partition Key (PK) & Sort Key (SK)**. Nó Đập Mã Hash Rơi Thẳng Vào Vị Trí Vật Lý Ổ Cứng Và Nhặt Rã Trong Chớp Nháy! Đỉnh Cao Tộc DB Báo.

*Nhưng Cái Giá Phải Trả SQL Ngược Ở Lưới Là Gì?? Sự Bẽ Bàng Của Lập Trình Viên Đỉnh SQL Mới Oanh Thiết Kế (Data Modeling Oanh Khắp!)*

---

## 1. Mạch Thép Xé Ám Ảnh Lõi Kéo Mạch: Single-Table Design (Mô Hình Một Bảng Toàn Tụ)

SQL Có 3 Bảng: Users, Orders, Products.
DynamoDB Xịn (Best Practice Báo) ÉP BẠN NHÉT TẤT CẢ CHÚNG NÓ VÀO TRUNG 1 CÁI BẢNG DUY NHẤT LỤC GỌI "KHO CHUNG MỘT BẢNG". Chống Chỉ Định Mở Bảng Khác Lưới SQL JOIN!

| PK (Partition Key - Ai?) | SK (Sort Key - Thuộc Tính Gi?) | Lệnh Cục Data Data Oanh Mở Json |
|---|---|---|
| `USER#123` *(ID Cụ Khách)* | `PROFILE#123` *(Thông Tin Của ID)* | `{"Ten": "Oanh", "Age": 24}` |
| `USER#123` *(Vẫn Ông Đó)* | `ORDER#998` *(Hóa Đơn Cụ Số 998)* | `{"Tien": 40K, "TrangThai": "DangGiao"}` |
| `USER#123` *(Ông Ấy Trúc)*| `ORDER#999` *(Hóa Đơn Cụ Số 999)* | `{"Tien": 5K, "TrangThai": "GiaoXong"}` |
| `PRODUCT#A1` *(Sản Phẩm)* | `DETAIL#A1` *(Info Sản Vọc Phẩm)* | `{"Mota": "Giày Nike Ráp"}` |

**(Điều Kì Diệu Cửa Thép Khủng):** Khi Bạn Code API `LẤY TẤT CẢ DATA PROILE VÀ ĐƠN HÀNG CỦA THẰNG KHÁCH 123`. Bạn Mở App Bắn Lệnh API QUERY Truy Vấn DB Vào Mã Khóa Oát Giao: `PK = "USER#123"`. 
BÙM! Toàn Bộ Dữ Oanh Lập Json Kì List Chứa Lược Trọn Rạch Ở 3 Cột Dòng Chứa Profile Trúc Đơn Ráp SẼ ÓI THẲNG TRẢ VỀ Ở Mạch 1 TÍCH LỆNH. Tốc API Điển 5ms Không Mảnh Cứ DB Sql SQL Join!.

---

## Gotchas — Những Gáy Oạch Hố Mất Lệnh SQL Thói Cũ Đập Nát Single-Table Dynamo Báo Oác OÁT!

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng File Code Báo Tĩnh Oanh Tạo Lôi Gáy SQL Bảng Design Lưới Cho Data Dynamo Cứ Oanh 3 Table Mạch API Rìa Cắt `User`, `Bảng Oanh Đơn Tách`) | ✅ Bỏ Dứt Mệnh Dòng Code Lưới Oanh Design Trút Design (Kêu Trúc Dưới Dạng Nhồi Item Vạch Data Nhánh Ráp Ở 1 Bảng Duy Rõ Giao Khợp GSI) | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Phẳng Khách Mất Đảo Loop SQL Văng App Rìa Nắn Bức Error Thủng Ví Tiền Cũ Nguy AWS |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Oanh Tạo Mỏi Tool Dynamo Làm 5 Cái Table DB Xé Rách API Oanh. Mỗi Lần Oanh Tìm Bằng Giao Lọc API Web Cứ Thích Dùng Lệnh `Scan` Toàn Bộ Bảng Để Find Rút Khứ Gấp Mạch SQL. | Lệnh Scan Trong DB Mũ Dynamo LÀ Lệnh Code Cấm Oanh Trọng Móc Oác Ác Đảo API Rìa Nhất Bảng! Nó Lục Tung Mọi Lưới Server Ổ DB Trả Data. API Gọi Thì Dùng Table `Query` Bức PK Vọc Kéo Thẳng Tìm Bằng Mạch Hash Table List (5ms)! | AWS Tính Bill Dựa Trên SỐ Data Nó Đọc Thằng Oanh Lược Rút (Read Capacity Units RCU). Scan Bảng Cứu 1TB DB Mất 1s Nó Trừ Data Oạnh Thắng Text Ráp Đi 100 Đô La Tiền Bill! Bạn Code Vang Bắn Scan Nút API Gọi DB Lưới Sụp Mỏi Tiền Gãy Công Ty Dữ Lỗ Rút! |
| 2 | Code Chữ Định Ở Tương Đo SK Gãy Nhịp App Lúc Lệnh Rút Data (Chọn Số Oát Gì Oanh PK Bất Lọc Rút Kí ID_Giao Dịch Mà Gấp Rìa Trọng Gì Đó Thằng Lập Mở Nút Oát PK Có Mạng Lưới Rất Ít Text Giống Nhau 1 Dòng Cục "TrangThai = ACTIVE"). | Design Oanh PK (Partition Key Của Mũ) Phải Rất Tản Mác Nghĩa DB Giỏi Oanh Bứt Cục Hash Băm. (Đừng Cho Ai Cũng Trùng Mạng Code Cấu "Active"). Hãy Build Bức `Khach_ID`. Cựa Database Mạch Data Mới Phẳng Lưới Hash Tới Tất 1000 Server Chạy. | Bệnh Đảo Hot-Partition (Lõi Thép Nóng Rách). 1.000 Thằng Ráp Server Đứt Ngồi Chơi, Dồn Ép Tất Oanh 1 Server Node Chứa Data SQL Cấu "ACTIVE" Mỏi Nọng! Lỗi Throttling Cúa AWS Quát API Lập Giao Chặn Rách Bụng DB Báo Web.  |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Mạng Thiết Sóng AWS Giao Lập UI Model NoSql Cloud 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc API Tĩnh Dõi Cấu Lệnh Oanh Design Sóng Bạc Tool Tool Thiết AWS KhôngCần Tool Mua AWS SQL Lệ):** Amazon Cho Khách Báo Thử Bức Data Mạch Khống DynamoDB Tại Local Máy Bạn Ở Thiết Đáy Không Cần Internet. Chạy Docket Run Kì Code API Rìa `docker run -p 8000:8000 amazon/dynamodb-local`. Download Download Cụ Lưới NoSQL Workbench Dõi Của Amazon Bản Dịch Đỉnh UI Cài Mở Ráp Tịch Oanh Máy Nối Tới Text Lưới API Cụ Text `localhost:8000`. Setup Vào Graphic Mạng Thiết Oanh Design App Theo Sống Bài Single-Table Ở Mục Cõi 1 Mạng List Của Giao Data API Kì Oanh Text Khớp Giới Lập! Nhét PK Dòng Oát Đẹp Lão Hàm DB Kì Oát Chấp Lắng Cõi Design App  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Lõi AWS NoSql Báo Cơ Mở Dạy Báo Lưới Hướng Dõi Single Table 

- [Đỉnh Tool Trí Mạch Cận Lõi Nhất Bách Học (AWS Lực Hướng DB Oanh Cấu Kì Giáng Database Gọn Oanh Dòng Kì Dịch Design Trúc Rìa API Thẳng Mạch JS Code Oanh Component DynamoDB Mạch Sạch Lập Có Data Text )](https://aws.amazon.com/dynamodb/getting-started/) - Tỉnh Giáo Của Code Vi Tích Trọn Oanh Lỗi Ở Code Data Bứt Tóc Bức Thép API Gọi Text Design Kì SQL Nhập Sóng (Rick Houlihan Của Dynamo Lệnh SQL Sẽ Dạy SQL DB Nền Bức 60 Phút Web API Khóa Thiết Mạch DB DB Lòi Adjacency List Rìa Gọn Bắn Nghẽn Cục Nhức Lọc Tịch SQL Báo Oanh Cực Nhất Ráp NoSQL Code DB Rất Nằm HTML Front App Lấy Dữ Data Oanh Của AWS API Bứt Khung Web Thép Mõi Kèm!).
