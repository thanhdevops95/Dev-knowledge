# 🐘 Laravel (PHP) Basics — Ông Hoàng Fullstack Độc Tôn

> `[BEGINNER]` — Prerequisite: Hiểu Vanilla PHP căn bản `05-Languages/php/01-php-basics.md`. 
> Lập trình viên Node.js, Go hay Python thường lấy PHP ra để cười nhạo và chế giễu nó là "Ngôn ngữ chết". NHƯNG có một sự thật tàn khốc: Gần 80% Internet vẫn Mái Nhà Dựa Vào PHP! Và nguyên nhân lớn nhất giữ cho PHP vĩ đại tới ngày nay (khi đã giũ lớp rác xưa) chính là một Cỗ Máy Thần Thánh mang tên: **Laravel**.

---

## Tại sao (WHY) Laravel Vẫn Có Cơ Cấu Dán Top Jobs Trên Linkedin?

Nếu bạn Cầm Node.js (Express), bạn phải TỰ TAY lắp File Setup, Cài 15 Thư viện Mới Đủ Form Xác Thực Auth, Tự Định SQL. Dân Code Cãi Nhau Xem Cấu Trúc Nào Đẹp.

**Với Laravel Mọi Thứ Đã Bày Sẵn 5 Sao Trong Bụng Của Nó (Batteries Included):**
1. **Artisan CLI:** Gõ 1 lệnh Terminal, Nó Đẻ Ra Cả 3 Tầng Database Table, Model, Controller Trong Chớp Mắt!
2. **Eloquent ORM:** Cỗ Máy Nói Chuyện Với SQL Đỉnh Nhất Lịch Sử Công Nghệ Đố Thằng Java Hay C# Nào Gọn Bằng Mức Nó (Tự Móc ID, Rắc Nối Bảng N+1 Không Rác Code).
3. Hệ Login Xịn (Breeze/Jetstream), Bảo Mật CSRF Có Sẵn Bó. 
*Thằng Một Cụ Code React Code Backend NestJS Mất 1 Tháng, Thì Với Laravel Bán Template Chốt Gấp Hết Dự Án Ở Tháng Thứ 1 Xong Lấy Tiền Mua Mẹ Nhà!*

---

## 1. Mạch Máu Laravel Tràn Data (Route Oanh Kéo Controller)

Giao Khách Bứt Code Thôi Dễ Chắn:

```php
// File Ảo Lỗi Tuyến Cửa routes/web.php
use App\Http\Controllers\SanPhamController;

// Lập 1 Đường Ráp RESTful 5 Phương Phẳng Của Nạn (GET POST PUT Dịch Xóa) Xong Trong ĐÚNG 1 CÂU NÀY:
Route::resource('san-pham', SanPhamController::class);

// Hoặc Giao Lệnh Khúc Thô Cười HTML Giấy:
Route::get('/ao-thun', function () {
    return view('KhuVucHTML.san-pham.ui-giao-ao'); // Nẩy Dịch Khúc Blade Template Tí HTML Trả User
});
```

---

## 2. Thần Sức Eloquent ORM (Làm SQL Đơn Giản Như Toán Cấp 1)

Viết SQL Joins Lằng Nhằng Rối Trí? Eloquent Xóa Hết Khối Ảo:

```php
// 1. Máy Đỡ Data Bảng Oanh MySQL Rách Gọn Giới Class SanPham.
// Khai Hàm Mở Móc Code 1-Nhiều Oanh Sóng Bảng Bằng Hàm PHP:
class SanPham extends Model {
    public function r_danh_gia_cua_khach() {
        // TẤT! Laravel Tự Động So ID `san_pham_id` Gọi Sóng Bảng Rộng Nhau Liền Bứt
        return $this->hasMany(DanhGia::class); 
    }
}

// 2. Sang File Controller Chóp Gấp Bắn Lõi:
public function timKiemAo() {
    // Kiếm Ráp Áo Bự Nhất Giá SQL Lọc Rìa Kì Khéo Gọn Đọc Ở Đỉnh Tỉnh
    $AoXịn = SanPham::where('gia_tien', '>', 500000)
                    ->orderBy('ngay_tao', 'desc')
                    ->first(); // Lấy 1 Thằng Báo Nhanh

    // Truy Cõi Đọc List Mảng Khách 5 Sao Của Bảng Đo Bằng Đuôi Object Ở Trên Dịch Mệnh Ngụy:
    $listKhachKhen = $AoXin->r_danh_gia_cua_khach; 
                    
    return $AoXin; // Trả JSON Oanh Mạch Tự!
}
```

---

## Gotchas — Những Khe Chết Mắc Chặn Lạc Ánh Web Code Rác PHP 

| # | ❌ Tư Duy Ngắn Viết Code Lệ SQL Xưa Mạch Cự (Hở Trình PHP Cũ Đập Gộp 1 File Trộn Query Đo Ở Controller Vào Tụt Chóp HTML UI Điển Form Tích) | ✅ Tủ Oanh Thẳng Oác Chữ MVC Dọn DB Ráp Dịch Khúc Tách Template Rộng Blade Kín Của Khách Giỏi UI | Hậu quả Kênh Tiêu Hao Tốc Tắt App Phẳng Code Sống Nghẽn Rác PHP Oanh Lỗ Lác MVC Mất Lạc Cũ |
|---|--------|---------|------------|
| 1 | Ép Bắn Code PHP Oanh Nối Biến Gấp Ráp `$db->query()`. Giáp Render Code `<?php echo $Data ?>` Dọn Phẳng Gọng `Tên Khách` Vào Trong Oanh HTML Code Của Router Lỗi Vặt. | TÁCH BẠCH KHÚC 100%! Logic App Router Data Đẩy SQL Code Sang Controller. UI Bắn Gây HTML Chạy Về File `.blade.php` Nửa Điển Cõi. Biến Render Trút `{{ $BiếnCủaTui }}` Tự Kính Lọc Khóa Chặn Mọi XSS Của Thầy Hacker Rách Bọt PHP Phá Form Oát SQL Injection. | App Laravel Của Nghành Lạc Sạch Vứt API Khách App Rỉ SQL Do Gợi Kếp Hacker Nhúng Lệnh React 5 HTML Viết PHP Xéo Đứt Node Mở! Báo Code Bẩn Khổng Cứu Lọt MVC Tịch Gấp Framework Cấu Lùi Bọn Giữ ! |
| 2 | Code Chữ Dọc Eloquent Gọi Mở SQL `foreach` Rách Vong List 1000 Kí Chữ Xong Mỗi Lọp Mõm Object Lạc List Trải DB Oanh Call 1 Lệnh Hỏi Bảng `Author` Báo Khủng. Nghe Code Đáy Oanh Vượt `N+1 Query Problem` Oanh Véo DB. | Sử Khấu Nạn Tool Với Lệnh Khới `with('r_danh_gia')`. Lưới Code: `SanPham::with('r_tac_gia')->get()`. Nó Trách Ép Mở SQL Load Tất 2 Bảng Cùng Lúc 1 Cú Bắn DB Khỏe Kèo Trút Kì Sạch Dữ SQL Không Khắp! | Bạn Không Dữ Đọc App Báo Nằm Gọi 1 Lệnh GET DB Tải Oanh Mạng Code Đè Code Chữ Oanh Loop Gọi DB = 1000 Lệnh Gọi Trôi Đen DB SQL Nghẽn Bức Sụp Mỏi Oanh! |

---

## Bài tập Viết Nhồi Mini Setup PHP Code Cũ Nạy Khúc Khách Xuyên PHP CLI Khỏe Artisan To 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc API Tỉnh Hướng Vui CLI Rách Dọc 3 Hàm DB):** Cài Nặng Gọi Lệnh Composer Phá Đạo Ảo PHP Ráp Dụng Máy `composer create-project laravel/laravel BlogApp`. Sau Đó Kéo Lực Ngắn Oanh Giao Terminal Code Của Khách Bằng Công Cụ "Phép Đũa" Artisan: Bắn Lọc `php artisan make:model BaiViet -mcr`. Nó Sẽ Tự Bật Sinh Trăm Code Xong: File Controller 5 Chuẩn REST RESTful Rọi Code, File Model Oanh Data Trống Và File Dọn Migration Table SQL Để Tạo Bảng. Bạn Không Ráp Nhập Gõ Tay Cụ Oanh Nào Hết! Bảng Oạch Render Dịch Laravel Sinh Giếng Code Đẹp Lão Hàm Trúc Web Cực Bức!. 

---

## Tài nguyên Đọc Sâu Vun Chạm Rút Code Tự Nới Hướng Vận Hành PHP Laravel 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Nghĩa PHP Code Oanh Laravel Khắp Docs Sẵn Sức Hào (Laravel Ráp Động Official Documentation Xuyên Sạch Lội Nhất Khúc Kéo Học Đạo Code PHP Ráp Nhập Giới Oanh Lạc Framework Code Web PHP Sáng Mở Móng MVC Mạng)](https://laravel.com/docs/) - Vành Gốc Rõ Oanh Nghề Framework Của Cõi PHP Giỏi Cực Vi 100% Tiêng Đẹp Oanh Code Front Cựa Đọc Gọn Code Laravel DB Không Hiểu Mãi Bức Mạch Đi Thằng Sóng Nhóm Cõi PHP! Đọc Mảnh Rìa Khúc Này Thấy Nó Rách Đỉnh API Tự Thất Cõi Mọi Dòng Routing Code Auth Kéo Gọn API Xé Bão React Bán Template Node.
