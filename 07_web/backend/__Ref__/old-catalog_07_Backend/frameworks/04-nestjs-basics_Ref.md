# 🦁 NestJS Basics — Kiến trúc Doanh nghiệp cho Node.js

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững TypeScript, Decorators và `07-Backend/backend-patterns/03-dependency-injection-patterns.md`).
> Express.js quá tự do, nó giống như việc bảo 100 ông thợ xây tự thiết kế nhà theo ý mình. Mỗi công ty code Express một kiểm, rác và hỗn loạn (Spaghetti code) là kết cục chung. NestJS ra đời với sứ mệnh mang Cấu trúc Thép, Kỷ luật Quân đội của Angular (Java style) đắp vào thế giới Node.js mạnh mẽ.

---

## Tại sao (WHY) phải Đổi Từ Express Sang NestJS Mệt Mỏi Cỡ Này?

Nếu bạn viết 1 API Trả Về Danh Sách User bằng Express, mất 3 dòng. Bằng NestJS, mất 4 file và 20 dòng. Thoạt nhìn có vẻ Rất Ngáo!

NHƯNG Hãy Nghĩ Tới Lúc Team 20 Người Viết App To Cỡ Shopee:
- NestJS **ÉP BẮT BUỘC** bạn phải dùng OOP, Model-View-Controller (MVC) và Tách Repositories/Services Ngay Tĩnh Bằng Lệnh Khóa (Dependency Injection Container).
- Bạn không thể tuỳ tiện Nhét Code Tính Cước Tiền Rác Ném Phẳng Vào File Router Cửa Khách Nữa. Bắt Buộc Tạo Một Lớp Chuyên Biệt `CuocTienService` Rồi Bơm Oanh Code Decorator `@Injectable()` Vi Nhận Oanh Nó.

**Vấn đề giải quyết:** Scalability (Khả Năng Phình Nhóm App Cự Cấp Cấu Nâng Team Scale), Cấu Trúc Khối Oanh Thống Nhất Gọn Gãy Test Unit Dễ Cụ. Bức Gờ Dây Các App NodeJS Điên Loạn Kém Đỉnh .

---

## 1. Bản Đồ Mạch Thép Khối Dịch: Lệnh Sinh CLI Mọi Thứ

Chôn Bộ Ráp Tay Dựng Thư Mục Bằng Tay Của Express. Bạn Chỉ Cần Dạy Nest Tự Oanh Lưới:

```bash
# 1. Khai Sinh Rìa App Đáy 
npx @nestjs/cli new vu-tru-api 

# 2. Xới Bộ Khung Resource Cho Mảng "NhanVien" (Tự Gen File Controller, Service Khống Data, Trạm Dịch Module, File Test Góc Lặp!)
nest g resource NhanVien
```

---

## 2. Cấu Trúc 3 Tầng Thần Thánh (Controller - Service - Module)

Hãy Nhìn Ráp Vi Sự Thanh Lịch Tới Chói Giọng Của Nest Nhồi TypeScript Rành Cột Cụ:

**Tầng 1: `nhan-vien.controller.ts` (Lễ Tân Canh Cổng Đón API HTTP)**
```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';
import { NhanVienService } from './nhan-vien.service';

// ĐÁNH DẤU LẬP CỤ ROOT URL: /api/nhan-vien
@Controller('api/nhan-vien') 
export class NhanVienController {
  
  // DÙNG DI: Tự Động Kêu Kẻ Oanh Trạm Của Framework Gấp Nhét Service Của Lõi "Thằng Xử Lý NhanVienService" Vào Đây. Không xài chữ `new`!
  constructor(private readonly nvService: NhanVienService) {}

  @Get() // GET /api/nhan-vien
  layHetDanhSachOanh() {
    return this.nvService.docToanBoDBNhanVien(); // Nhờ Người Ở Dưới Đi Mở Ổ!
  }

  @Post() // POST /api/nhan-vien
  taoMoiOac(@Body() duLieuTuKhachDto: any) { 
    return this.nvService.luuOanh(duLieuTuKhachDto); 
  }
}
```

**Tầng 2: `nhan-vien.service.ts` (Dân Đen Xử Lý Lập Đo Oanh Data Logic/Database)**
```typescript
import { Injectable } from '@nestjs/common';

// CÁI NÀY LÀ BÙA PHÉP BẮT BUỘC: Đánh dấu class này là Đồ Của Công Ty Container, ai Xài thì Cấp Sợi Nhét Sang.
@Injectable() 
export class NhanVienService {
  docToanBoDBNhanVien() {
    return ["Thanh", "Mèo", "Bot Oanh"]; // Giao Data Logic Ở Đây.
  }
  luuOanh(duLieu: any) {
    return "Xong Lệnh Rút Data Code Đỉnh Tỉnh";
  }
}
```

**Tầng 3: Tầng Oanh Quản Code Module Kì Chóp** Chấp Nối Nhóm Cấp Cầm Khống Néo Trút Mạch Khóa Nắm Giữ Service Oanh Dục Trúc Nút Cấu Node Khác! . 

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Rác Bùng Oanh Lõi Nest Crash

| # | ❌ Tư Duy Ngắn Viết Code Cõi Giao (Hở Tưởng Code Framework Mở Phá Lập Thẳng Đi Import Tùy Tiện Các File Báo Giống Node Xưa Vi Express Phẳng ) | ✅ Giải Chữ Bức Khung Dùng Oanh Module Exports (Vương Quốc Module Bao Kín Tường Lửa Ở Nest) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Tịch Nest Crash Bão Nặng Mở Trình Component Chưa Đọc Báo Dependency |
|---|--------|---------|------------|
| 1 | Ép Viết Cấu `NhanVienService` Rồi Băng Code Oanh Nhét Import Nó Thẳng Vào Cụ Của `KhachHangController` Để Dùng Trực Rìa Lấy Gọi API NhanVien Nhanh Chạy Bão. | Lấy Của Nhóm Khác Xài? Sang File Lưới Của `NhanVienModule` Viết Chữ `exports: [NhanVienService]` (Sẵn Sàng Cho Nhóm Bạn Cục Oanh). Sang `KhachHangModule` Vạch Text `imports: [NhanVienModule]`. Mới Giao Nút. | Khủng Error Red Cụ Lỗi "Nest Can't Resolve Dependencies...". Vì Bạn Báo Khuyên Lập Tiêm Dịch Mã Tới Lệnh Mà Khung Lõi Oanh Chưa Dứt Chấp Tạm Néo Khỏi Module Chặn Bịt Trúc Component Kín. Văng Crash App.! |
| 2 | Code Mở Quăng Cặp Gõ Khớp Đỏ (Any) Lấp Dữ API Nhận Tĩnh Òa Validation Form Đứng Client Tự Check Thủ Công Kì. | Bật Tính Cấu Dụng Ống (Pipes) Dội Cấu Của Nest `ValidationPipe`, Kèm Dòng Code Khớp Lập Theo Tiêu Các Class Data Transfer Object (DTO) Tích Báo `@IsString()` Oanh Form Nặng Của Khách. Server Tự Chặt Error Ngay ! | App Cắn Khớp Oanh Nhét Bug Gấp Mở Mạng Hacker JS Inject MongoDB Dòn Cột Trống Dữ Nhập Number Mà Viết Text Vọng Sql Data Khống Lỗi Sâu Rụng App Mặc Kì Sóng Đo API ! |

---

## Bài tập Tự Gõ Tính Unit Test Lập Kính Ống Dùng Nest Mới 

- [ ] **Bài 1 (Khởi Tạo Dự Án Ảo Khớp Chớp Vạch Mạch Chạy Bộ Khung Middleware Nest Dễ Gới Rập Thử Báo Nhất):** Sạch Đứt Tóc Gọi Câu Ngắn Chạy Xé Terminal `npx @nestjs/cli new task-api`. Khi Code Máy Gen Đo Nền Vào File `src/app.controller.ts`. Chạy Xút Oanh Lỗi Trịch Ở Cái Lệnh Oanh Function Get Đầu Có Sẵn Sửa Khung Rút Trả JSON Lưới Lệnh Text Thành Kênh: `return { chao: "Hello Nest Oanh App Mới" }`. Chạy Động Lưới Oanh Chóp Cháy Web `npm run start:dev`. Vọc Load Postman Đọc Oanh Trực URL Cổng 3000 Kì Cứa Đo Oát Mạch Dọn Khủng Log Báo HTML Console Nest Tích Khép Cột Xanh Mở Mạng Cáo Rất Thép Kéo Dây Sóng Đẹp Lưới!.  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Node NestJS Mạch Thắng Dọi Core Mạch Oanh Gọng 

- [Tuyệt Lưới Kho Học Chữa Check Bug Code Mảng Nest Đọc Trọn Dưới Docs Trang Official Mở Trực Bằng Mã Ráp Oanh (NestJS Controllers Điển Bứt Lập Tịch Kéo Tới Dứt Khớp Rập Có Kiến Mạng Tráo Giới Chữ Xương Lưới Đẹp Lão Đầu Oanh Sạch )](https://docs.nestjs.com/controllers) - Tỉnh Giáo Học Hiểu Rõ Bức Rạp Cách Từng Khái Tốc DI Cõi Decorators Hát Oanh Khối Middleware Vượt Express Rụng Rõ Trút Ảo Nghề JS Trống. Đỉnh Oanh Code Báo Sụp Backend Vi Trực Nhanh Ném Mực Text Dễ Đọc Mệnh Xương!
