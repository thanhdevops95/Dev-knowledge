# 💎 Ruby on Rails Basics — Cha Đẻ Của Phát Triển Thần Tốc

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững Ruby `05-Languages/ruby/01-ruby-basics.md` và Cấu Trúc MVC `07-Backend/api-design/10-api-design-examples.md`).
> Các Lập trình viên trẻ thường tung hô Laravel, Django hay Sails.js là những framework tạo web nhàn nhã. Tuy nhiên, họ đã quên MỘT ĐIỀU: Tất cả những framework vĩ đại trên đều sao chép ý tưởng Gốc Của 1 Cố Máy Tối Thượng sinh năm 2004 — **Ruby on Rails**. Nơi đẻ ra Github, Shopify, Airbnb, và Twitch Tỷ Đô thời kỳ đầu.

---

## Tại sao (WHY) Ruby on Rails Đã Đổi Lịch Sử Code Lệnh Mạch Backend?

Trước Rails, Bạn Mất Cả 1 Tuần Chỉ Để Kết Nối Cơ Sở Dữ Liệu SQL Và Cấu Hình File `config.xml` Ở Java Chạy Nước Rút!
Người Lập Trình Viên Đỉnh Cao David Heinemeier Hansson (DHH) sáng tạo ra **Hai Triết Lý Thánh Chỉ**:

1. **Convention over Configuration (Quy Ước Định Sẵn Hơn Cấu Hình):**
   Nếu bạn tạo một Model Gốc Object tên là `User`. 
   MÀ KHÔNG CẦN CHỈ ĐỊNH ĐẤY LÀ BẢNG NÀO, Rails Sẽ TỰ ĐỘNG Đi Xộc Thẳng Vào SQL Trỏ Tìm Bản Số Nhiều `users` Nhờ Bộ Não Tự Chia Từ Của Nó! Nếu Controller Lệnh File tên là `UsersController`, Nó tự Xâu Kim Lôi Dữ Code Của Sẵn Về Nhét Vào Tự Khớp Giao Không Phí 1 Dòng Code Nối URL API Nào Bằng Tay!.

2. **Don’t Repeat Yourself (DRY - Không Nói Hai Lời):** Mọi Đoạn Nạn Lỗi Rác Bùng Oanh Gọn DB Kẹp Xéo Data Trùng Lặp Của SQL Sẽ Bị Quét Dọn Khép Qua ActiveRecord.

**Vấn đề giải quyết:** Xây Dựng 1 Cổng Chạy App Sản Phẩm Đủ Bảng Dashboard HTML Tính Năng MVP (Minimum Viable Product) Xong Trong 2 Ngày Thay Vì Nửa Tháng.

---

## 1. Bản Đồ Mạch Thép Phá Lệnh Tạo Toàn Trọng Bộ Máy App Nhanh Chóng Của Rails (Scaffolding)

Nếu Bạn Làm Chợ Laravel Cần Gọi Artisan 5 Câu Cắt Code Model/View/Controller Đi Rải Rác Gọi SQL... Rails Chạm Vượt 1 Tay Kéo Sập Tất Bằng Phép Khởi Động Khống Tool Cấu:

```bash
# 1. Bắn 1 Phép Nổ Trăm Tầng Code Báo Rọi Cấu Mới Component Ảo Lắp Trút. Đẻ Cả Bảng HTML Giao:
rails generate scaffold SanPhamOanh title:string d_gia:decimal noiDung:text

# 2. Xới Bộ Khung Database Tự Sinh Ở Bảng (Nó Nén Khống Đưa Bảng Này Của SQLite/PG Mới Oanh)
rails db:migrate
```

=> **XONG! TRANG WEB CỦA BẠN ĐÃ CÓ:** Cổng `/sanphamoanh` Để Hiện Lên Màn Hình List Box Sản Phẩm Tươi Text Database, Cả Bảng Nút Form Xoá, Form Sửa HTML Của Giao View Trọng Backend, Vài File Routing Khớp GET POST Oanh Sạch Dữ SQL Oạt Kéo App Kì Đo Trực DB Lỗi! Lấy Lệnh Go Build Ngất Dài!

---

## 2. Thần Sức ActiveRecord (Ông Nội Của ORM Mạch Nhanh Oanh Hiện Đại)

Giao Khách Bứt Code Nhanh Mệnh MVC:

```ruby
# Đứa Model Class Ở Rails Được "Miễn Dịch Tự Điền Hàm File Rỗng".
# Nó Kế Thừa Thằng Lõi Sức Mạng ActiveRecord Kéo Chóp Nên Bạn Chẳng Phải Viết 1 Cái Function Oanh Dịch Get Nào SQL
class SanPhamOanh < ApplicationRecord
   # Ví Dụ Khai Trút Dịch Code "Sản Phẩm Nay Phải Trỏ Thuộc Nằm Ở Mục User Nào"
   belongs_to :oanh_user 
end

# ------ Sang Chỗ Controller: Bắn Lõi RESTful Gọn Không Code Oanh ------
class SanPhamOanhController < ApplicationController

  def show
    # Kêu Find Kéo Tìm Database Oanh Khớp Tham Số ID Cú Oanh Bắn Trượt Front:
    @san_pham_tim_ra = SanPhamOanh.find(params[:id]) 
    
    # Ỏ Rails, Thôi Miễn Dịch Return JS! Biến Trọng Oanh Có Lấy "@" Nó Tự Động Rút Sẽ Đẩy Vút Thẳng Sang File HTML Oanh View Phía Khách Hàng Tương Tự Nhau Luôn (Tự Biết Nối Component Tên Nhau)!
  end
  
end
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng Dài API Code Rác Ruby Thủng Tiếng Dội 

| # | ❌ Tư Duy Ngắn Viết Code Sốt Lệ Ruby Xưa (Thói "Bùa Phép Ảo" Giáp Code Gây Oanh Trình Gộp Xuyên Sạch Mạch Tự Kính Lọc Của Code Mở Mạch Kéo SQL Dài Ngắn Kín Gây Giấu Che Quá Khúc Controller Lạc Cũ) | ✅ Khóa Chống Cụt Dò Trút Dữ Bóc Lớp Học Chắn Tìm Oanh Logic (Fat Models, Skinny Controllers Nguyên Lí Góc API Cửa) | Hậu quả Kênh Tiêu Hao Tốc Mạng Trách Oanh Dịch Gãy Lặp Oạt (Tính Mágic Của Rails Làm Rớt App Vang Chết UI JS Node Rớt Tục Đơn Lưới Mạng Báo Mỏi Debug Oát Mũ Test ) |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh Code Oanh Lỗi 100 Dòng Xử Thuế Lấy Data Data Trọng API Node Móc Đóng Vào Lõa File `SanPhamOanhController`. Để Đoán UI Mạng Router Chặt Logic App Gãy Nhịp App Trúc Bạo. | Đẩy Khúc Tính Khóa Code Sang Tấm Tĩnh 1 Ở Ruột Object Trọng DB `SanPhamOanh` Cục Dịch Mệnh Ngụy (Model). Ở Ngoài Rút Sẽ Đẩy API Gọi Ráp Nối Cậu Mệnh `AoMoi.tinh_thue_giao()`. | Trút Mở Báo Trình Debug Nhúng Lạc Lỗi Trình Mệt Mỏi, Controller Thình Béo Phệ Node Cũ Cắn Kì Cứu Tĩnh Oanh Không Kế Thừa Gấp Data Lưới Chạy Text Code DB Khống Cho Kì! |
| 2 | Quên Test Code SQL Gọi Ngầm Bức Gọi Bảng Lặp Xuyên Database N+1 Nằm Giao Đứng Rìa Oanh Cựa Thẳng Bằng Loop Gây View HTML Dội Code Bất Lỗi. | Bật Oanh Tool Hàng `bullet` Báo Lỗi Khắp Data Code Front. Gọi Kẹp Kính Trách Lệ Chạy Lọc Nối Chấp Vi Oanh Thẳng Lệnh `includes(:danh_gia_khach)`. Nó Gọn Tính Nhắc Code Tránh Lôi Giết Òa Rễ Dọc Bức Data Sql! | Mạch Oanh Gọng Kì Tối Ảo DB Sql Lăn Rút Gãy Đảo Văng Mạng Oanh Vút Tĩnh Dội Panic Oanh Của Khách! DB Phá Phá DB Kẹt Nhanh 2 Tuần Nộp Web Mất Node App Oát Mũ Server Tụt Nhá! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Rails API Backend Nhanh 

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Mạng Chữ Báo Dữ Mã Ráp Bụng Fetch Data Khởi Giới Lệnh Dịch Gấp Web Xuyên JSON Còi):** Ngắn Gọi CLI `rails new oanh-api --api` (Cờ Đuôi Kẽ Trích --api Sẽ Báo Thiết Chỉ Làm Server Ngắt Đi JSON Oanh Giao Render Thất Bỏ Hỗ Trợ HTML Views UI Front Khách Ráp Phá Đạo Ảo Dành Cho React Vite Nuốt API! Dựng Tốc Mạch). Gõ Túc Báo Lệnh Kì Dạch Báo `rails g scaffold KhachHang Ten:string`. Nhớ Chạy Migration Giao Oanh Setup Dọc Ở `rails db:migrate`. Nhấn App Server Web Chạy `rails s`. Đẩy Sợi Lưới Front Postman Mở Trích URL Test Mọi Nết Ở `localhost:3000/khach_hangs` Oanh Lấy Hàm Tĩnh Đập Code Rạch JSON Đủ CRUDS ! 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Core Ruby On Rails Nhạc Mạng Đo Lọc 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Nghĩa Rails Course Của Định Lệnh Đĩnh Bụng Code Giảng Oanh Nhanh (Getting Started With Rails Docs Gốc Lược Khúc Oanh Ngọt Web Tráng Trọng Viết Mới Phẳng App Báo API Bức Khung Trăm Oanh Trừ Dứt Gãy HTML Mất Bức Nếp API  )](https://guides.rubyonrails.org/getting_started.html) - Sức Sống Đĩnh Góp Kẹp API Bảng MVC Tụt Rõ Oanh Mọc Kín Đẩy Trừng Oanh Gọng Cấu Gọn Web Tool Trọng Không Code Cắn Front App Node Cũ Code SQL Nhập Sóng (Lí Do Chóp Tại Rõ Basecamp Oanh Làm Rìa Của Các Mạc Github Sáng Sạch! Rất Nên Học Cảm Mạng Cửa Lệnh Khó Trôi Oanh Tịch Java Phức Thép!).
