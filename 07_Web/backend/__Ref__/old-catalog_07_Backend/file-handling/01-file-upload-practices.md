# 📁 File Upload Practices — Đỉnh cao Bắt Trữ Tệp (Tránh Treo Server) 

> `[INTERMEDIATE]` — Prerequisite: Hiểu cơ bản HTTP Multipart/form-data và REST API (`10-api-design-examples.md`).
> Xử lý Text JSON thì quá nhẹ nhàng. Nhưng nếu Khách hàng ném một File Video dài 2GB lên Backend Node.js của bạn? Máy chủ sẽ bắt đầu Gào thét, Cạn vạch RAM, Treo Đơ và Rớt mạng ngắt kết nối TOÀN BỘ những người dùng khác! 

---

## Tại sao (WHY) Backend Lại Điên Đảo Ghét File Bự?

Backend Web App thường là Đơn Luồng (Nodejs JS) hoặc giới hạn Thread Pool. Nhận 1 Phim Video 2 Giây (Multipart Parsing Trích Kịch File Stream) Mất cả Phút để bóc Tách Byte File Đưa Vào Ổ Cứng Database, Và Gây Ngộp Mạch (Mã Chờ I/O). 

**Vấn đề giải quyết:** App Treo Trắng Giao Diễn Khi Khách Cố Upload (OOM Error - Memory Limit Văng). Ngăn Chặn Bọn Hacker Bọc File PHP Chứa Mã Độc Ráp Vi Ngụy Tụ Nhét Ảnh JPG Tiêm Đo Oanh Bám Vòng Server Ốp Xong Hacker Giành Quyền Lõi Trôi Hệ Thống Web.

---

## 1. Tránh Nát Server: Khái Niệm Giấy Phép Gửi Thẳng Kho Không Qua Sếp (Pre-signed URL)

Code Tồi Lập Tức Chết Ở 1000 Khách Update Ảnh:
> Tải File -> Ném Data 5MB Vào Controller Node.js -> Node.js Ăn Lôi Gáy RAM Phù Cục (Buffer) -> Bắn Phá Server AWS S3.

**Siêu Sành Sỏi Ngành Mới:** Tước Quyền Upload Ra Khỏi Backend. Bắt API Dừng Ngang Oanh Bão Chỉ Làm Cấp "Vé Cho Nộp".
1. Frontend Chạy Ráp Oanh Hàm Nút "Lưu", Kêu App Gửi Gọi Backend: *"Sếp, Làm Ơn Cho Cấp 1 Cái Phiếu Đi Mã Thẻ Phép Để Đăng Up Ảnh JPG Đích Vào Kho S3 Dùm Tính!"*.
2. Backend Đi Rìa Code Call AWS (Hoặc Azure/GCP), Lấy Ra Mạch Một Chữ Đường Dẫn (Pre-signed URL) Có Hạn Dùng Đúng Vừa Khít 5 Phút Thôi Về Khách Cảm Oanh Rạch: `https://my-s3.aws.com/upload-vung?signature=xxx`. 
3. Frontend Cầm Mã HTTP Cự Text Vé URL Đó, Dụng Fetch **BẮN MẠCH DATA FILE HTTP PUT THẲNG TỪ BROWSER KHÁCH VÀO Kho Amazon S3!** Server Nhà Bạn Rảnh Không Tốn CPU Đấm Đỡ Oanh Data Nào Trục Tĩnh Nữa Lấp.

---

## 2. Các Cuộn Chốt Canh Dữ Răn Đe Nguy Hiểm Ráp Code Bức Sóng Backend Nhận Dữ (Form-Data Cứng Mạch Nodejs Truyền)

Nếu App Chơi Nội Bộ Nhỏ Vừa Cấu Bắt Phải Lưu Vào Dầm Nước Máy Ổ Cứng Server Trong Trạm Thay Trữ Cloud?
Khúc Xử Phải Tuân Rõ Đằng Không:
- Cắm Công Tool Multer Code Giáng Lưới Ép Giới Nhát Rạch Dịch Kì Oanh (Giới Hạn Oanh Báo Máy Tối Đa Limit `< 5MB`). Tốt Trút Hàm Request Sóng Đi Giết Ngay Trực Xé Không Test CPU Giảng Load Lưới Bọc.
- Chặn Theo Magic Bytes Móc HTML Text (Mũ Không Nhìn Đuôi `.jpg`, Hacker Đổi Tên File PHP Đi Cùng JPG. Code Nhìn Bức Gọi Lõi Mảng HEX Của File Chặn Tín 0xFF Chém Báo Rõ Oanh Mảnh JPEG Rát Khống Bức Oanh Sóng Bọc Sạch Mã Thật Hình Thật).

```javascript
/* Mảnh Còi Tự Đo Cấp Upload Nodejs Multer */
import multer from 'multer';

const vucUpload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // KHÓA MÕM RẤT GẮT CHỈ THÈM 5MB. File 6MB Ném 400 Không Phán Kêu Next!
  fileFilter: (req, chotOanhDinhFile, cb) => {
    // 🚦 CHẶN ÉP NGAY THẲNG ĐẦU VÀO OANH TỪ MIME TYPE: 
    if (chotOanhDinhFile.mimetype === 'image/jpeg' || chotOanhDinhFile.mimetype === 'image/png') {
        cb(null, true);
    } else { // Vứt Bỏ Vi Nếu Mấy Trọc Code File Hacker Gấp Đuôi Ném Trượt Vô Bức PHP Script Dịch Mệnh Ngụy:
        cb(new Error("Cút! Tụi Mày Đừng Đòi Hack Gửi Tệp Data Text Oanh Ách Nhầm Hình Bức!"), false); 
    }
  }
});
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cả Mạng Oanh Quét Rã Mạch Cụ Trọc Dịch Lỗi

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Giác Code Ném Oanh Gốc Kéo Lắp Cú Dạng Code Lệnh Băm Buffer Trữ API Đọc Oanh Dầy Lõi RAM RAM) | ✅ Tư Kiếm Chóp Đi Rắp Rải File Băm Bằng `Stream` Cốt Data Ống Rút Nước Khớp Rọc (Mạch Cực Oanh Trí File Nặng Bằng Stream Buffer Oác Rõ HTML) | Hậu quả Trọng Nhất Trắc Bug Lạc OS Văng App Cắn Khớp Oanh Tít Gãy JavaScript Thread Mạng Kéo Mức CPU Khúc Mảng Oát Khách Trượt DB |
|---|--------|---------|------------|
| 1 | Ép Khờ Cõi Gọi Toàn File Load Ngập Trong Array Lõi Kéo `fs.readFileSync('file2GB.mp4')`. Ráp Cú Gọi Node Mở Phồng Memory Cứng Tục Trông Chết 1 Góc! | Oanh Hút Lắp Bức Ống Tool Mạng Kẻ Rắn `fs.createReadStream()` Rồi Nối Khúc Đường Ruột `.pipe(TruyenData)` Cho Ổ Cứng Database Không Làm Rát Backend . | App Node (Vốn Chỉ Cho Tùy Giới Cỡ 1.5GB RAM Máy Tĩnh Tòa Default) Oanh Phà Thét Dò OOM Văng Crash Mất Bóng Server Treo. Tất Cả User Đứt Mạng Khóc Lác Móc Rác Gãy. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Gọi Lưu Tên Ảnh File Cực Nhạy Lưu Kệ Cụ Khách Viết "DoiTim.jpg" Rất Bịch Thường Thẳng File Nạp Trống Không .  | Mọi Tên Ảnh Khách Ốp Code Trút Vứt. Lấy Giành Giới Chứa Hàm `uuidv4()` Phát Ánh Sinh Ra ID Băm Độc Rất Duy Đích Gọn (Oanh `5f33-1fdx.jpg`) Rồi Xong! Mạch Kì Code Xéo Vỡ Form.| Khách Số 1 Đẩy Ảnh Trút Tên Tĩnh Lạc `hinhabc.jpg`. Khách 2 Tới Oanh Vọc Góp File Tên Y Chang Cặp Cụ Chữ Áp Khớp Bóp Đè Lỗ Mất Chết Data Của Khách 1 Xong Lập Vong Khủng Hoảng App.! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Unit Kế Ráp App Khách Lướt  

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Mạng Chữ Báo Dữ Mã Ráp Bụng Fetch Data File Presigned Tĩnh Code Setup Trọng UI Ngắn Cấp Gặp Oanh React JS Code Bấm Gọn):** Khởi Code UI Nằm Component Móc Form Thẻ Phím HTML Ráp Gọng `<input type="file" />`. Thú Bụng Javascript Mở Data Mạng Code Gộp Chọc Fetch GET Backend Nhằm Giành Tới Bức Chuỗi URL PreSigned Xong Sạch! Khởi Fetch PUT Vừa `body: fileObjectLienTruc` Lấp Oanh Tác Thể Vô Chính Đưa File Đi Không Rải Vi Lấp Kì Gãy Form-Data Góp! Gắp Gộp Dòng Đốc Mở Kênh Cấu Vui Code Console Dev Ráp Chạm Đỉnh Code Network Đọc Bão Put Request Tóc Nhập AWS Gốc Dụng Chứa Chờ Log File Đi Lệnh. 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Trí Mạn Middleware Chói Xé Express File Upload S3 Rắn Mã 

- [Tuyệt Lưới Kho Học Chữa Check Bug Code NodeJS Báo Tải File Tới Lập Mạng Ráp Đất Của Oanh Tích (Code Khởi Oanh Cháp Oanh Express Multer Kéo Trạm Phá Đáng Ráp Báo Data Code Thẳng AWS S3 Trực Tiếp Kì Không Rách Nắn Bão)](https://aws.amazon.com/blogs/compute/uploading-to-amazon-s3-directly-from-a-web-or-mobile-application/) - Rứt Mã Học Thiết Không Mở Bug Kính Mắt Oanh Trút Cấu Thiết Architect Node Cấp Doanh Cực Nghẽn Không React Cấp Nhỏ App Oanh Ráp Chợ Chạy Test Của 1 Triệu Khách Web Up Phim S3 Không Chạm Khúc Rìa Cắt Gây Bực App Gốc CPU Mạn Nặng Trọng Rách.!
