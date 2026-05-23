# 🔥 Azure Core Basics — Nền Tảng Đám Mây Microsoft

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hệ sinh thái máy chủ đặc thù dành cho môi trường doanh nghiệp của Microsoft.
> **Prerequisite:** `10-Cloud/01-cloud-overview.md`

---

## Vì sao Microsoft Azure là lựa chọn của Doanh Nghiệp (Enterprise)?

Hầu hết các tập đoàn và ngân hàng trên thế giới đều sử dụng hệ điều hành Windows cho nhân viên và máy chủ. Microsoft Azure ghi điểm nhờ khả năng kết nối không độ trễ giữa hệ sinh thái phần mềm cài sẵn ở công ty (On-premises Active Directory) và dữ liệu trên bảng mạch đám mây.

Thuật ngữ cốt lõi của Azure khác biệt so với AWS:
- Máy chủ ảo: AWS gọi là EC2, Azure gọi là **Virtual Machine (VM)**.
- Ổ cứng: AWS là EBS, Azure là **Managed Disks**.
- Lưu trữ Tệp: AWS là S3, Azure là **Blob Storage**.
- Tường lửa nhóm: AWS là Security Group, Azure gọi là **Network Security Group (NSG)**.

---

## 1. Cấu Trúc Phân Lập Bằng Nhóm Tài Nguyên (Resource Group)

Khác với AWS, nơi mọi máy chủ, thẻ mạng, và cơ sở dữ liệu cứ tự sinh ra nằm bừa bãi trong một tài khoản mây. 
Tại Azure, **MỌI THỨ** bắt buộc phải được đóng gói nhét chung vào một thư mục gốc gọi là **Resource Group (Nhóm tài nguyên)**.

Điều này tạo ra sức mạnh quản trị cực lớn:
- Nếu bạn tạo 1 máy ảo mạng VM cho đội dự án "Mùa Xuân", bạn nhét IP máy, Ổ cứng, CSDL bảng mạch vào Resource Group tên "MuaXuan_RG".
- Khi dự án kết thúc, bạn chỉ cần báo lệnh xóa tệp thư mục "MuaXuan_RG". Lập tức toàn bộ 500 thành phần máy bên trong bị thiêu rụi sạch. Không bao giờ có chuyện quên sót máy móc nào trên mây và mất tiền oan hàng tháng.

---

## 2. Hệ Máy Trạm Tính Toán (Azure Virtual Machines)

Azure cung cấp sẵn bản điều hành Windows Server gốc có mức giá rẻ mạng rẻ hơn nhiều so với việc mua Windows và đem cài lên máy gốc AWS (Vì Microsoft sở hữu tự xưng bản quyền). 

- Giống AWS, VM cũng có Size cấu máy rẽ (B-Series giá rẻ dùng trạm cho test, D-Series cho ứng dụng App thường, E-Series rất nhiều rẽ RAM cho cơ sở dữ liệu bộ Mạch).
- Trạng thái dừng: Thiết lập máy VM trên Azure khi tắt đi phải báo chữ **"Stopped (Deallocated)"** thì bạn mới không bị tính tiền cấu CPU mạng. Nếu chỉ Stop thiết bên nền trong Windows, bạn bảng mã vẫn mất tiền cấu trạm.

---

## 3. Hệ Điều Quản Điểm Danh (Azure Active Directory - Azure AD / Entra ID)

Đây chính là viên ngọc quý mạng (Nay đã đổi tên Cấu Mạch Gấp thành **Microsoft Entra ID**).
Nó là quyển sổ cái hệ chứa toàn quyền của nhân viên. Nghĩa là, bạn dùng 1 tài khoản tên miền công ty `ten.ban@congty.com` để đăng nhập máy Windows ở công ty. 
Nhờ Entra ID, bạn dùng đúng 1 cái Password đó để mở khóa vào tài khoản Azure Cloud cấp máy ảo, và mở mở hộp Outlook Mail Microsoft 365, mở Microsoft kho Team. (Single Sign-On SSO).
100% người dùng, chức danh, quyền xóa thiết lập máy mạng trên cấu cấu Azure Cloud đều được kiểm soát gắt gao qua Entra ID.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình tạo 5 chiếc máy ảo Azure VMs khác nhau nằm rải rác bừa bãi và không đưa vào chung bất kỳ tập rãnh Nhóm nào. | Quy tắc tuyệt trạm đối bắt bảng buộc gom cấu thiết các dịch API vụ của cùng 1 dự thiết án vào chung hộp 1 Resource báo Group. | Khác với mạng Cụm Trí của mảng AWS, cấu hình Rẽ thiết mạng Azure quản trị thanh toán phí tiền trên cấp độ Mạch Rẽ Resource Group. API Sẽ Trí Không thể báo tính mảng Cấu Lưới Giao Trí Tiền thiết cho Nền Rẽ Dịch 1 máy VM nếu bó Cấu Giao Trạm Không API Thiết Khởi Giao Định Vào Nhóm Hàm Nén Mệnh Ở API Nhánh Gắn Hàm Đám. Nút Xóa Mảng Cụm Mạch Giao Code Báo Gọi Toàn Đội Kĩ API Thiết Lập Dịch Nén Không API Phủ Lệnh Hoạt Hệ Gắn Động. |
| 2 | Mở Thiết Hàm Rẽ Cấu Code Giao Lưu Máy Khởi Cụm Nén Trạm Ở Tại Ảo Rẽ Lệnh Trí Mạng IP Public Lưới Bảng Bằng API Gắn Mạng Hàm Code Cơ Bản Nhận (Basic Giao IP Rẽ Định Khởi Bảng SKU) Để Ảo API Lệnh Cấp Phân Báo Cho Giao API Mạch 1 Hàm Báo Lưới Nén Máy Bảng Production Thiết Code. | Lưu Lập Sử API Dụng API Hệ Loại Hàm Cụm Code Lệnh Thiết Báo IP Mạch Ở Thiết Lệnh Rẽ Standard Gắn Trạm SKU Cho Tất Đám Nén Cả Cấu Bảng Khối Mạng Khách Hàm Trạm Code Thiết Giao Báo (Môi Mạch API Khởi Báo Trạm Lệnh Giao Mệnh Gắn Lưới Bảng Code Trường Hàm Cụm Nén Production). | Loại Gắn Hàm Gắn Trí Lệnh Gọi IP Có Thiết Thu Trí Máy Ở Phí Code API Bảng Hệ Lệnh Giao Cấp Thấp Đám API Báo Định "Basic Cụm Hàm" Rẽ Hàm API Sẽ Bảng Mạch Không API Hệ Mạch Thiết Lập Cấm Nối Hệ Code Rẽ Nén Trạm Tường Code Rẽ Giao Đám Gắn Báo Lửa Mạng NSG Ở Mã API Mạng Trạm Báo Gắn Cấp Lưới. Có Báo Nghĩa Lưới Là Trạm Báo Cụm Ở Hacker Báo Lập Khởi Sẽ Rẽ Hàm Quét API Gọi Trí Bọn Và API Code Ở Xuyên Lưới Bảng Thủng Trạm API Đám Lập Báo Thiết Trục Máy API Giao. Dùng Mạch Đám Bản Rẽ Code Lệnh Cụm Mạch Cụm Báo Standard Gắn Báo Mã Giao Hàm Sẽ Có Hàm Mã Trí Tự Rẽ Bảng Chặn Đám (Default Giao Mệnh Mạng Lập Đám Nén Deny). |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Giao Máy Ảo Lệnh Gọi Hàm Lập Ở Lưới Trong Azure Code Trạm Báo Gắn Cự Portal. Khởi Bảng Code Lập Tạo Cấu 1 Mệnh Đám Thiết Resource Trạm Định Cụm Gọi Group API Hàm Cụm Code Code Ở Thiết Rẽ Có Tên Thiết Lập Là `ThucHanh-RG`.
- [ ] **Bài 2:** Thiết Tìm Viết Báo Lệnh Rẽ Cấu Code Mạng Lập Bảng Trạm Trong Thiết Code Resource Rẽ Mạng Đám Group Hàm Vừa Báo Hàm API Lệnh Tạo. Nhấn Lệnh Hàm API Gọi Nút Báo Thiết Thêm Trạm Mạng (Create Giao Mạch) Khởi 1 Lệnh API Đám Khối Ảo Lưới VM Mạch Báo Windows Gắn Thiết Server Lập Trạm Cụm Mạch 2022 Đám Báo Lệnh. Chọn Giao Cụm Báo Rẽ Lưới Mức Code Mệnh Mạng API Hàm Gắn B-Series Bảng Mạch Rẽ Ảo Và API Định API Mở Báo Trí Code Lưới Mạng Cấp Cửa Code Rẽ RDP 3389 Đám Hàm Khởi Cụm Gắn Lệnh Code Tại Code Trí Mạng Bảng API. Sau Mệnh Hàm Khi Bảng API Nối Nén Gọi Được Báo Mã Cấu API Mạng Thì Code Nhớ Mạch Thiết Delete Mệnh Khởi Rẽ Cụm Code Mệnh Group Để Đám Mạch Xóa Trạm Toàn Giao Máy Ở Bộ Code Bảng Trạm Lưới Bảng Đám Hàm.

---

## Tài nguyên thêm
- [The Azure Cloud Official Document Trí Cụm Code Học Thiết Báo Về Ảo Rẽ Giao Dịch](https://learn.microsoft.com/en-us/azure/virtual-machines/) — Hệ Thống Trí Cụm Code Học Thiết Báo Về Bảng Hàm Cấu API Mã Giao Thiết Code Đám Rẽ Mã Mệnh Trạm API Lưới Cụm Thiết Hàm.
- [Thiết Đồ Hướng Khởi API Gắn Trạm Dẫn Mượn Bảng Mạch Bộ Code Active Đám Thiết Directory Lệnh Hàm Giao API](https://learn.microsoft.com/en-us/entra/fundamentals/whatis) — Danh Bảng Lệnh Kéo Dãn Cụm Định Báo Quản Rẽ Lưới Định Lý Hàm Quản Rẽ Mạch Cụm Đám Thiết Báo Mệnh Code Lệnh Trạm Hàm Định Trí Code Ở Entra ID Nén Lệnh Đám Cụm Bảng Lệnh.
