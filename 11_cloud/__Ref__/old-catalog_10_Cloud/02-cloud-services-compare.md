# ☁️ Cloud Services Compare — So Sánh Hệ Cung Cấp Đám Mây

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Phân tích sự khác biệt về thuật ngữ dịch vụ của ba ông lớn để kỹ sư có thể chuyển giao công việc nhanh chóng.
> **Prerequisite:** `10-Cloud/01-cloud-overview.md`

---

## Đại Chiến Tam Quốc Của Điện Toán Đám Mây

Thị phần điện toán đám mây thế giới (Đầu năm 2024) được chia thành ba mảng rõ rệt thuộc về:
1. **Amazon Web Services (AWS):** Kẻ dẫn đầu trị giá lớn nhất (Khoảng 31% thị phần). Hệ sinh thái dịch vụ nhiều nhất lịch sử. Khuyết điểm là giao diện cấu hình quá cũ kĩ, phức tạp, và nhồi nhét cực kì khó thao tác.
2. **Microsoft Azure:** Theo sát số hai (Khoảng 25% thị phần). Lựa chọn số 1 của doanh nghiệp khối quản trị nhà nước, khối doanh nghiệp có sẵn máy trạm dùng Windows và C#, bộ SQL Server chuyển lên mạng chung một hệ quản trị Active Directory.
3. **Google Cloud Platform (GCP):** Đứng thứ ba (Khoảng 11% thị phần). Sở hữu ưu đãi công nghệ mạnh nhất về Xử lý Mảng dữ liệu Lớn (BigQuery) và đào tạo công cụ Mạng lưới máy Trí Tuệ Nhân Tạo (AI). Máy chủ máy K8s mượt nhất gốc tự xưng GKE. 

Nhìn chung, cả 3 nhà cung cấp đều bán những phần cứng chức năng như nhau (Ram ảo, CPU ảo, Ổ cứng mạng), nhưng họ đặt tên khác biệt để định dạng đặc trưng.

---

## 1. Dịch Vụ Mảng Lưu Trữ Dữ Liệu Tĩnh (Object Storage)

Kho lưu trữ không giới hạn mạng lưới dung lượng, dùng để chứa Ảnh, Video, File tải lên của người dùng. Trả tiền theo từng chữ MegaByte.

- **AWS:** Amazon S3 (Simple Storage Service). 
- **Azure:** Azure Blob Storage.
- **GCP:** Google Cloud Storage.

---

## 2. Hệ Máy Trạm Điện Toán Tính Toán Bộ Xử Lý (Compute)

Thành phần trọng yếu lõi, là những chiếc máy tính ảo cấp phát HĐH Linux hoặc Windows.

- **AWS:** Amazon EC2 (Elastic Compute Cloud).
- **Azure:** Azure Virtual Machines.
- **GCP:** Google Compute Engine (GCE).

---

## 3. Hệ Máy Ảo Hệ Quản Trị Container (Kubernetes)

Hạ tầng cung cấp mạng và điều phối các bộ máy mạng theo cụm tiêu chuẩn Docker.

- **AWS:** Amazon EKS (Elastic Kubernetes Service). Nổi tiếng khó cài đặt phần mạng bảo mật phân luồng.
- **Azure:** Azure Kubernetes Service (AKS). Vượt trội khả năng tự kết nối vào nền tảng quản trị người dùng.
- **GCP:** Google Kubernetes Engine (GKE). Do Google sáng tạo ra chuẩn mảng Kubernetes nên Dịch Vụ Mạng Cụm của Google được giới kỹ sư coi là dễ vận hành và cao cấp nhất.

---

## 4. Hạ Tầng Hàm Ảo (Serverless)

Bạn viết một nhành code Node.js tải lên, máy trạm tự hiểu xử lý API và tắt điện. Trả tiền mốc từng Mili-giây chạy ứng dụng.

- **AWS:** AWS Lambda. Chín muồi nhất cấu mạng tốc độ hàm khởi động.
- **Azure:** Azure Functions. 
- **GCP:** Google Cloud Functions. 

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Lập kiến trúc dự án mạng đa mây (Multi-Cloud) dàn trải lấy máy chủ EC2 ở mạng Amazon, và lưu Database vào kho rẽ mảng kết trên mạng nội bộ Azure CosmosDB. | Hạn chế tối đa kết nối truyền phát dữ liệu API mạng chéo hai nhà cung cấp thiết bị mây khác nhau. | Nhà cung cấp thiết bị ảo thường miễn phí hoàn toàn tiền kéo truyền Data Vào hệ (Ingress) nhưng đánh thuế cực cao chi phí truyền Dữ Liệu Ra cục ngoài (Egress). Việc luân chuyển mạng chéo API giữa 2 hãng AWS-Azure tiêu tốn băng thông phí kinh khủng. |
| 2 | Chủ quan gọi máy ảo tạo ứng dụng tại bất kỳ cụm vùng thông tin (Cloud Region) nào trên thế giới có giá thuê máy ảo rẻ nhất để tiết kiệm kinh phí. | Tính toán gọi thiết thiết lập máy trạm ảo ưu tiên phân nằm chung hoặc sát nách trung tâm người dùng tiêu thụ nhất (Ví dụ tập trung tại cụm AWS Singapore). | Mỗi khu vực cụm thiết bị máy chủ đặt tại 1 nước có giá điện lưới khác nhau. Máy Bắc Mỹ rẻ hơn Singapore. Tuy nhiên mạng tín hiệu truyền kết bằng cáp quang đi ngầm đại dương sẽ tạo độ trễ mạng cực cao mạng (Lên lưới báo tới cấu 300ms Ping). Lập trình viên thiết kế giao lưu cần cân bằng Trễ mạng so với tiết kiệm 10% giá tiền. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết lập mở tệp công cụ trình duyệt tạo đăng nhập mốc tại cả 3 trang bảng biểu tính tiền hãng (AWS Pricing Calculator, Azure Pricing Calculator, GCP Pricing Calculator).
- [ ] **Bài 2:** Thiết lập truy xuất máy ước lượng báo thiết giá thuê 1 tháng cho một cấu hình máy trạm ảo 2 lõi CPU ảo (2 vCPU) và 8 GB RAM cài hệ điều hành Ubuntu Linux ở vị trí máy trạm Singapore. Tính lệch báo giá mạng tiền đô hai hãng.

---

## Tài nguyên thêm
- [Phân Trạm So Sánh Tổng Thể Mác Bản Thiết Dụng Cloud Services Compare Mạng](https://aws.amazon.com/compare/) — Bảng quy chụp đối đồ thông định dạng từ chuẩn báo của Amazon cho mạng khách hệ.
- [Thiết Đồ Microsoft Azure versus AWS and GCP](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/azure-vs-aws/) — Lập lệnh góc hệ nhìn thông bản máy chuyên do tổ chức Microsoft định tính hướng khách hàng.
