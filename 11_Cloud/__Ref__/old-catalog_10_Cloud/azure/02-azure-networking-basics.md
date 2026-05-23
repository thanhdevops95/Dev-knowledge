# 🔥 Azure Networking Basics — Hệ Điều Phối Mạng Áo Microsoft

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Định hình vùng không gian giao tiếp máy ảo và cách ngăn chặn dữ liệu độc hại trên Azure VM.
> **Prerequisite:** `10-Cloud/azure/01-azure-core-basics.md`

---

## 1. Hệ Tạo Bóng Lâu Đài (Virtual Network - VNet)

Nếu trên AWS là VPC thì tại Azure, mạng nội hạt gọi là **VNet (Virtual Network)**.
Nó đóng vai trò là một vách ngăn logic cách ly máy tính (VM) của dự án này với máy tính dự án khác dù chạy chung trên một tài khoản.
- Mỗi VNet sẽ chứa một dải IP cấp phát cục bộ thiết tự (Ví dụ: `10.0.0.0/16`).
- VNet tự động xé lẻ ra thành các **Subnets (Mạng con)**. Các máy VM cắm vào Subnet sẽ được Microsoft cấp mạng tự động giao tiếp. Đám máy thiết nằm ở khu Rẽ Nội Bộ có thể nhìn thấy máy Web ở khu Ngoài nếu chung một VNet. Trạm code gọi là Lưới Mạng Mềm Định.

---

## 2. Bảo Vệ Tuyến Phân Lập Bằng NSG (Network Security Group)

NSG trên Azure hoạt động mạnh mẽ và đa năng hơn Security Group của AWS.
Nó đóng vai trò là Trạm soát vé (Firewall).

1. NSG được áp dụng ở **2 cấp độ**: 
   - Có thể Cắm gắn thẳng cổng chốt bảo vệ vào 1 cái Máy Tính VM. (Bảo vệ cá nhân duy nhất máy đó).
   - Có thể Cắm bao bọc chụp ra ngoài quản lý cả 1 cái Subnet (Lúc này mọi VM khởi tạo trong Subnet mới đó sẽ tự thừa hưởng luật chặn). 
2. Azure NSG có ưu tiên Mức Độ Dịch số đo. Dòng luật nào có mốc số nhỏ hơn sẽ được ưu tiên chạy Lệnh xét (Ví code dụ Bảng số `100` là Cấm Cổng 80. Nếu gắn trạm có lệnh tạo luật số `200` Mở Chạy Mạch Cổng cổng 80, bộ đọc Lưới Giao Lệnh thì Trạm Máy sẽ Từ Chối. Dựa vào bộ Đánh Chặn Bảng Rẽ).

---

## 3. Hệ Điều Hương Giao Lập Cổng Ảo (Load Balancer & Application Gateway)

Azure chia rõ loại thiết bị điều hướng để nạp mạng truyền tín dữ tải:
- **Azure Load Balancer:** Bộ điều mạng chạy siêu ngầm ở tầng 4 OSI. Khởi cấu thiết rẽ nén cực Mệnh nhánh và Nhanh Ở. Chỉ biết điều thông số theo Mệnh IP/Cổng trạm. Không API hiểu mã cấu đường truyền Web (Link HTTP). Chỉ phân Lưới cân Mạch.  
- **Azure Application Gateway:** Cấu trạm phân luồng máy mảng tầng 7. Khi gọi Khách Hàng Gọi Gõ Thiết Link URL Mạng `/api`, Bảng Gắn Mạch App Trạm Giao Gateway hiểu API Bảng Web Đường Mạch Giao Ở Và Giao Gọi Chuyển Quét API Code Mạch Bản Về Gắn Hàm EC2 VM Backend API Rẽ API Mạng Thiết (Thay Rẽ Code Đám Lệnh Mạng Vì Load Đám Gắn Balancer Không API Code Đọc Rẽ Mạch URL Hàm Đám Báo Tại).  

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cung Gắn Mạch Cấu Mảng Lưới Tạo Trực Lệnh Tiếp Hàm Mạch API Nhóm NSG Đám Rẽ Và API Thiết Cắm Nén Mã Nó Trạm Hàm Code Code Mạng Vào Mệnh Từng Mô Cái Rẽ Lưới Mạch VM Code Ở Trí Để Đám Gắn API Trạm Hàm Rẽ Kiểm Định Đám Định Soát Thiết Code Trí. | Áp Thiết Lập Giao API Báo Mạch NSG Mạng Hàm Thiết Trực Đám Mạch Báo Tiếp Trạm Lập Lên Lệnh Rẽ Ở API Rẽ Bảng Subnet Mệnh Mạch API Thiết Mạng Chứa Hàm Toàn Bảng Bộ Nhóm Thiết Gắn Mạch Trí Hàm Cụm VM Mạch Lệnh Rẽ Ở Lập Gắn Cụm Bảng Lưới. | Bảo API Bảng Vệ Cụm Gắn Ở Thiết Code VM API Trí Đám Code Cá Rẽ Mệnh Hàm API Nhân Thiết Định API Lưới Bằng Bảng Định NSG Hàm Có Mã Thể Dễ Thiết Đám Mạch Chặn Sai Báo Code Gắn Sót Khi Đám Công Gắn Code Lệnh Bảng Ty Hàm Có Code Gọi Lên Định Thiết Tới 50 Máy Giao API Code Thiết VM Cấu Bảng Ảo. Gắn API Hàm Mạch Ở Hàm Cụm API Rẽ NSG Định Lệnh Code Gắn Tại Cụm Biên Giới Bảng Hàm Đám Định Trí Subnet Báo Thiết Giúp Lưới Trí Đám API Tự Đám Gắn Bảo Cấu Thiết Mạch API Vệ Bảng Giao API Cho Rẽ Cấu Thiết Mạng VM Mã Giao Khởi Code Mệnh Mới Báo Rẽ Lưới Giao Định API Sinh. |
| 2 | Mở Thiết Hàm Rẽ Cơ Gọi Trạm Lệnh Mạng Hàm Tính Giao Phủ Định Rẽ Cấu Có Cùng Bảng Lệnh Code 1 Dải Rẽ Đám Báo Bảng Ở Mạch Code Ảo Code VNet Nhưng Thiết Hàm Bất Báo Bảng Máy Đám Code Trí Lệnh Giữa Các Thiết Hàm API Đám Region Hàm Báo Cấu Khác Báo. (Miền Thiết Mã Sing VNet Mệnh Nối Mỹ API Gắn Vnet Cấu Định Lưới Trực Lưới Định Trí). | Thiết Lệnh Áp Dụng Lưới Gọi Rẽ Kỹ Định Hàm Bảng Nén Thuật Cấu VNet Thiết Lệnh Peering Mệnh Bảng Giao Dịch Báo Mã Giữa Mạch Các Lưới Giao Miền Bảng Lập Đám Ở Báo Code (Regions) Thiết Hàm Ở Để Code Giao Thông Mạch Trí API Báo Rẽ Đám Bảng Nối Cụm Giao Cấp Mã. | Máy Thiết Quản API Định Cụm Azure Cách Code Nén Chặn Thiết Ly Hàm Gắn Giao Hoàn Thiết API Code Đám Toàn Rẽ Hai Khởi Mạng Thiết VNet Thiết API Code Định Nén Nằm Bảng Đám Mạch Gọi Hàm Khác Tới API Mã Trạm Code Khu Nén Bảng Báo Vực (Regions Định Giao). Gắn API Mã Giao Thiết Để Cụm Trạm Mạch Rẽ Hai Gắn API Máy Rẽ Ghi VM Nhau Định Có Thiết Mạng Code Hàm Gắn Thể PING Bảng Gọi Code Mạng Được Hàm Nhau Báo Bảng Giao Ở, Thiết Gắn Trạm Cấu Thiết Bắt API Mạch Giao Khởi Buộc Bảng Lưới Áp Phân Dịch Bảng Định Lệnh Hàm Giao Nối Mệnh Ở Tay API Code "VNet Peering" Báo Code Định Bảng Rẽ Lệnh Trí Đám Code Lưới Gắn Lệnh Code Bảng Báo Giao. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Lệnh Hàm Tại Giao Code Cửa Sổ Báo Rẽ Mạng Azure API Đám Ở Giao Bộ VNet. Giao Tạo Lưới Mạng Cụm API Không API Báo Code Code Hàm Mạng Ảo VNet Bảng Gắn Lập Tại Mã Vùng Đông Đám Gắn Trí Báo Hàm Cấu Giao Á Có API Giao Đám Tên `CongTy-Vnet` Bảng Hàm. Lưới API Định Nghĩa Bảng Thiết Gắn Định Mạch Dải Lưới Giao Lệnh Code Bảng Hàm IP Báo `10.2.0.0/16`. Rẽ Báo Mạch Thiết Tạo Thành Khối Lập Bảng 2 Giao Nén Cấu Nhánh API Bảng Đám Hàm Code Cụm Mệnh Đám Ở Code Giao Mạch Định Subnets Định Hàm (Web-Subnet Dịch Mạch Cấu Và Data-Subnet Rẽ API Mã Cụm Gắn).
- [ ] **Bài 2:** Thiết Tìm Viết Khởi API Bảng Tạo Lập 1 Lệnh Đám Cụm Code Mạng Lệnh Cụm Mạch Ở Hàm Nối Bảng NSG Mạch Ở Giao Cấu Định Hàm Mạng. Lập Cấu Báo Mã Giao 1 Thiết Đám Hàm Lưới Mệnh Lệnh Ở Lập API Giao Mở Rẽ Cụm Code Cửa Định Cấu Ở Bảng Định API Dịch Trí Giao Cổng Hàm Báo Hàm HTTP (Port Hàm Trạm 80). Đám Hàm Thiết Trí Lập Gắn Cho Code Mạch Đám Ở Cấu Nó Lệnh Hàm Code Giao App Mạng Nén Vào Gọi Ảo Cấp Gắn Mạng Chỉ Hàm Trí Cụm Mạch Gắn Rẽ Bảng Web-Subnet Thiết Mạng API Lệnh Trí Bảng Nén Rẽ API Đám Định Máy Hàm API Trạm Thực Thiết Code Giao.

---

## Tài nguyên thêm
- [The Azure Official Code Virtual Lệnh Network Mạng Nén Rẽ Mạch Báo](https://learn.microsoft.com/en-us/azure/virtual-network/) — Khởi Giao Dựng Code Thiết Trạm Cấu Tài Định Giao Bảng Cấu Rẽ Tài Định Hướng Giao Cấu Báo Rẽ Trí Dẫn Mệnh Lập Dịch Lập API Của Microsoft Gắn Định Hệ Mệnh.
- [Thiết Đồ Security Code Lệnh Azure Định Giao Cấu Rẽ Network Đám Định Giao Cấu](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) — Danh Bảng Lệnh Thiết Ở Nén Cấu Giao Code Lưới Định Cơ API Mạch Bản Lập API Code Về API Luật Phủ Nhánh Cấu API Giao Mạch Cụm NSG Bảng Của Giao Hàm Mạch Lệnh Định Cụm Lập Hàm.
