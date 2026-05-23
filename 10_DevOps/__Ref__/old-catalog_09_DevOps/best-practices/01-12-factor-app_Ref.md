# 🔥 12-Factor App — Tiêu Chuẩn Vàng Của Ứng Dụng Đám Mây

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu tường tận 12 quy tắc vàng để thiết kế kiến trúc phần mềm không bao giờ sập khi đưa lên hệ Docker hoặc Kubernetes.
> **Prerequisite:** Bất kỳ ngôn ngữ lập trình nào.

---

## The 12-Factor App là gì?

Ra đời bởi các kỹ sư tạo ra nền tảng điện toán mây Heroku, "12-Factor App" (Ứng dụng 12 Yếu tố) là cuốn kinh thánh thiết lập mạng. 
Nếu bạn viết ứng dụng theo tư duy cũ (Lưu tệp tạm thẳng vào ổ cứng Server, để cứng chuỗi kết nối Database vào file Code), bạn sẽ chết đứng khi bắt đầu đưa thư mục code này vào Container Docker (Vì Container tắt cái là ổ xóa sạch).

Tuân thủ phương thức 12-Factor bảo đảm App của bạn có thể ném vào bất cứ máy Ubuntu Linux nào, hay máy Docker, trạm Kubernetes nào nó vẫn chạy trơn tru mạng mượt mà không lỗi.

---

## Giải mã các Yếu Tố Trọng Điểm

Không cần phải nhớ hết 12 bước, DevOps thường quan tâm tuyệt đối đến 5 lõi mạng cấu quy tắc cực hiểm:

### 1- Codebase (Cơ sở Mã Thiết Điểm Duy Nhất)
**Quy tắc:** Chỉ có 1 nhánh lưu kho Git trên Github, nhưng ứng dựng đó được triển khai ra nhiều môi trường (Dev, Staging, Prod bản thật). 
Không có chuyện "Tạo Repo GitHub Dev riêng, tạo Repo Prod riêng rễ". Mọi thứ chỉ chung 1 thư mục code mạng, chạy tách qua tham số của nhánh (Branch).

### 3- Config (Cấu hình môi trường mạng)
**Quy tắc:** "Luôn sử dụng Environment Variables (Biến môi trường) để chứa mật khẩu Password DB". Cấm tuyệt đối băm gõ trực tiếp (Hardcode) mật lệnh API Key vào dòng lệnh file `config.js` đẩy lên Github cho giặc tự lượm. Cấu mạng khi bật Docker lên sẽ gọi nạp biến chữ `ENV` nhét API rẽ tự động sau.

### 4- Backing Services (Dịch vụ hỗ trợ bên ngoại)
**Quy tắc:** Mọi thứ như hệ MySQL lưu mạng, hệ phát Email, hệ Redis phải được xem như "Một cái đường Link cấu kết đính vào thay được". Không cài thẳng MySQL vào bên trong lòng ổ cứng chứa Code. Nếu App kết nối qua Link mạng, K8s xóa Pod App thì CSDL trạm API ở ngoài vẫn toàn thây.

### 6- Processes (Tiến trình mảng không lưu dấu Stateless)
**Quy tắc:** Bản thân bộ khung chạy mạng App (Ví dụ con Node.js API Web) cấm tạo bộ ghi nhớ file rác, dữ liệu khách mua hàng trên ổ lưu (Session lưu thẳng máy). Nó bắt buộc phải là Stateless (Máy vô não rỗng). Nếu cái API Pod chập điện, K8s mở cái Pod số hai, Pod thứ hai đó đọc gọi qua chọc kết rẽ Database để biết rẽ khách vừa đặt cấu mạng gì. Web Server phải thiết thiết vứt đi dễ dàng.

### 11- Logs (Ghi nhận thông báo)
**Quy tắc:** App đừng tự đi viết hệ lệnh bắt file mở `error.log` ghi vào ở ổ cắm máy cục C. App chỉ việc dùng lệnh nén ném chữ đổ ra màn màn cấu máy in tiêu mạng cực Terminal Console (`console.log/stdout`). Hệ công cụ mạng gốc thứ 3 của DevOps như Docker hay EFK sẽ tự đi chụp hứng lấy màn in này và trữ hộ. App không tự quản lý ổ tệp.

---

## Gotchas — Những lỗi thiết quản mạng thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình thiết hệ lệnh lập code cài xây ứng tạo 1 tệp `database.json` Mạng nén Code nằm tải kho thiết Github gõ chữ Mạch API Key rẽ trong đó và tải Mạng Git. | Sử thiết lệnh nén Code Báo dụng Thư Giao viện `dotenv` trạm API trong mạng máy Local Đám Lập Rẽ. Đặt API hệ `DB_KEY=xyz` Đám ở file `.env` rẽ không Thiết Quản đẩy Đám GitHub Thiết. | Kẻ thù của DevOps ở công ty là mật khẩu đưa nén GitHub. Báo thiết lộ một mật khẩu Mạch Bảng Đám Mạch MySQL ra thì Hacker Đám Thiết Rẽ thả mạng cài Bitcoin. Áp dụng chuẩn III: Gắn vào biến tham số môi trường ENV. |
| 2 | Code Lưu Dụng Hàm Quản Cài Lưu Cấu Tài Thiết Giỏ Bảng Gọi API Trạm Thông Tin Đăng Nhập Client Thiết Cụm Đám Của Lưới Mảng (Giỏ Lưu Hàm Bảng Gọi Chứa Session Memory RAM) Nằm Vào Ngay Lưới Mã Nền Giao Trực Hệ Máy API. | Đẩy Hàm Code Sửa Trạm Gắn Bộ Lòng Cấu Nhớ Lưới Đám Tạm Vào Gửi Gọi Cất Rẽ Hệ Cấu Cài Máy Phân Bộ Nhớ Lưới Trạm API Gắn Redis Cache Bộ Tách Ngoại Bảng Dịch. | Vi phạm luật Hệ Tiến trình API Stateless yếu Số 6. Khi hệ Giao K8s API Tự Đám Quét Bảng Hợp Thiết Trạm Ở Định Chết API Mệnh 1 Máy API Máy Thường, Toàn Thiết Khách Gọi Lưới Mạng Máy Rẽ Tại Ảo Sẽ Đám Rẽ Hỏi API Gặp Cụm Nén Hiện Đứt Lệnh Máy Thiết Quăng Đăng Rẽ Ra Khỏi Máy Rẽ. Nối Lưu Cache Đám Ở Nền Redis Rẽ Cục. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Thiết Tạo Dùng 1 Tập Dự Án Ứng Mạng App Nodejs API Cấu Cài Hình Khởi Rẽ Thay Mã Cấu Đám Thiết Đổi Cấu Code Gọi Bảng `const dbUrl = "mysql://root:abc@..."` Trạm Thành Cài Giao Cấu Chữ Biến Bảng Cụm Lập Hàm Mạng Hệ `process.env.DATABASE_URL` Của Thiết Hàm Khai Thiết Phủ Biến.  
- [ ] **Bài 2:** Thiết Cầu Thông Dụng Nén Tệp Hệ Mạch Lập Tải Chạy Docker Gắn Giao Bản Mạch Cấu Cài Ứng Nền Rẽ File Chạy Vừa Lưới Sửa Tham Bằng Phân Rẽ API Báo Công Gắn Bằng Bash (`docker run -e DATABASE_URL="mysql://live:123" my-app`). Trạm Mạng API Không Cho Trạm Lập Bị Phá Tham Tệp Trong Container Cũ Giao.  

---

## Tài nguyên thêm
- [The Twelve-Factor App Official Manifesto Định](https://12factor.net/) — Chữ Trang Phân Cấu Mệnh Chính Giao Đám Nền Trạm Phương Rẽ Tham Pháp Định Dịch Cấu Toàn Bộ 12 Luật API Gắn.
- [Beyond the Twelve-Factor App Code OReilly Lưới Bảng Cấu Rẽ](https://www.oreilly.com/library/view/beyond-the-twelve-factor/9781492042631/) — Gương API Thiết Sách Đào Sâu Trạm Lưới Mạch Báo Lệnh Thiết Các Cấp Định Code 15 Giao Bảng Factors Của Giao Kevin API Hoffman Mạch Đám.
