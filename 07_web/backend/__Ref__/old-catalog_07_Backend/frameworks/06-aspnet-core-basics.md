# 🟣 ASP.NET Core Basics — Vua Tốc Độ Mới Của Microsoft

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững C# căn bản, và Khái Niệm Phân Tầng Controller `07-Backend/api-design/10-api-design-examples.md`).
> Nhiều người nhắc tới Backend .NET (C#) là nghĩ ngay đến Cục Máy Tính Chạy Windows Server Chậm Rì, Bị Ràng Buộc Khóa Rìa Bản Quyền của Microsoft Thập Kỷ 2000. Đoạn Ký Ức Đêm Tối Đó Đã KẾT THÚC! **ASP.NET Core** được Đập Đi Xây Lại Hoàn Toàn: Chạy Đa Nền Tảng (Linux, MacOS, Docker), Mã Nguồn Mở, và nó Đang Đứng Top Đầu Thế Giới Về Hiệu Năng Tốc Độ API (Thổi Bay NodeJS và Đạp Ngã Cả Java Spring Boot Trong Các Bài Test TechEmpower).

---

## Tại sao (WHY) C# và ASP.NET Core Lại Lên Ngôi Cực Điển Cõi App Khủng?

Tới Đây Bạn Phải Cảm Ơn Anders Hejlsberg (Ông Tổ Của C# và Cũng Chính Là Cha Đẻ Của TypeScript Sau Này!).
C# Sạch, Đẹp, Thanh Lịch Và Chứa Những Trình Ráp Gãy Cấu Trúc Khủng: LINQ (Công Cụ Thần Thánh Cắt Gọt Mảng/List Không Lang Nào Theo Kịp), Chút Async/Await Tối Cao Của Ngành.

**Vấn đề giải quyết:** Cấu Trúc Nguyên Khối (Enterprise Hệ Vi Tĩnh) Khắp Nơi Trong ASP.NET CORE KHÔNG CẦN CÀI THÊM BẤT CỨ THƯ VIỆN BÊN NGOÀI NÀO! Nó Tích Hợp Sẵn Ngay Trong Lõi:
1. Trạm Rút Tiêm Kéo (Dependency Injection Built-in).
2. Lính Gác Logging & Configuration.
3. Mã Xác Thực Mức Rút Jwt (Authentication).

---

## 1. Web API Cực Gọn Với Minimal APIs (Cú Tát Đau Cho Express.js)

Không Cạnh Gọng Rườm Rà Setup Controller 20 Lệnh Nữa. .NET 6/7/8 Tung Ra Code Sóng Web Khớp Sống Cấu **Minimal API** Trong Đúng Nửa Điểm Tĩnh File `Program.cs`:

```csharp
// 1. Phép Máy Khởi Máy Trạm 
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// 2. Kẻ Điều Phối (Router API Của Khẩu Get Text Express)
app.MapGet("/api/chao-microsoft", () => {
    return new { LoiChao = "Xin Cự Tầm Bắn Data Từ C# Linux", TinhTrang = 200 };
});

// Chạy Oanh App Gọi Ra 
app.Run();
```

*(Bạn không nhìn lầm đâu. File Backend C# Build Chạy Code Ở Giới Tịch Bây Giờ Ngắn Nhỏ Cạnh Tranh Thẳng Tới Kính Lúp Node.js/Python!)*

---

## 2. Dependency Injection Oanh Nằm Gấp Trâm Trúc Rễ (Nghệ Thuật Khóa Cắm Class)

Quay Về Bản Giới Code Controller Mũ Cấp Công Ty To (`03-dependency-injection-patterns.md`), Microsoft Cho Sẵn Cái Trạm Bơm (IoC) Khủng Nhất:

```csharp
// ĐÓNG BƯỚC ĐĂNG KÍ DỊCH VỤ VÀO Thùng Chứa (File `Program.cs`):
// Builder.Services Trích Thằng Container Khắp: Cho Chữ "AddScoped" Báo (Cứ Xong 1 Vòng Chạy API Rút Xé Bỏ Service Sinh Mới Không Trùng Rác)
builder.Services.AddScoped<INhanVienService, SQLNhanVienService>(); 
```

Sang Ráp API Bộ Controller Ở Class Điển Khác:

```csharp
[ApiController] // Bùa Mở Khóa Đánh Tránh Lệch API
[Route("api/[controller]")] // Tự Đặt Tên Route Dựa Theo Tên Class Xíu Khéo ("api/nhan-vien")
public class NhanVienController : ControllerBase 
{
    private readonly INhanVienService _nvService; // Không Bao Giờ Viết Cục Biến Có Chữ Dịch New!

    // Constructor Tiêm Bằng Phép Oanh Khung DI Khớp Của .NET
    public NhanVienController(INhanVienService dichVuBoc) 
    {
        _nvService = dichVuBoc;
    }

    [HttpGet] // Bắt Get 
    public async Task<IActionResult> GetHetVui() 
    {
        var dataNhieuKhach = await _nvService.TruyVanLayDanhSachOanhKDB();
        return Ok(dataNhieuKhach); // Ép Thành Lệnh 200 HTTP Sát JSON Mới Trả! 
    }
}
```

---

## Gotchas — Những Gáy Oạch Lỗi Rác Bùng Oanh Lõi Bộ Khóa ASP.NET Cũ

| # | ❌ Tư Duy Ngắn Viết Code Sốt (Hở Tưởng Code Framework Oanh Gọi Ráp Dịch Căn Thẳng Kẻ Đục Entity Framework SQL Phức Mệnh Cứ Báo Chờ Lỗi Ở Front) | ✅ Tủ Cụ Oanh Thẳng Oác Chữ DTO Ráp Ẩn Oát DB Khung Lập SQL Lệnh Náo Của Báo SQL Giỏi App | Hậu quả Kênh Tiêu Hao Tốc Mạng Đo App Phẳng Khách Mất Đảo Loop SQL Văng App |
|---|--------|---------|------------|
| 1 | Ép Bắn Đổ Lệnh ORM Của C# Là Entity Framework Rất Mạnh `context.Users.ToList()`. Rồi Cầm Nguyên Cái Cục Data User Bự Có Chứa Cái Bảng Con (`Bảng Lương Lội`, `Bảng Địa Chỉ Nổi`) Bắn Trút Thẳng Lệnh Json Trả `return Ok(users)` Trùng Front Rạch Cú. | Bỏ Dứt Lỗi Rác Báo Không Viết Dại Lấy Reference Loop! Entity Framework Nó Trỏ Nối SQL 2 Móc Table. Bắt Buộc Viết Mảnh Cú Class `DTO` Không Mapping Gọi `Select(x => new UserDTO(x.Name))`. | Quá Lực Ép Serialize Bắn Trả Ra API App Node Trắng Òa. Do Bảng User Trỏ Sang Address Chéo Lưới Òa Mạng Báo Address Lại Trỏ User, Json.NET Không Thể Biến Đổi Hàm (Object Reference Loop Exception Oanh Crash Góp API Code Server). |
| 2 | Code Chữ Async Không Có Await Oanh `Task.Run(()=> { })` Kiểu Nghẽn Lưới Hàm Tính Mà Return Liền Dài Ở Cấp Cuối Tĩnh Òa Controller Mở Trọng API Đo Giới Thread Bóp. | Toàn Bộ Mạng HTTP .NET Cực Mạnh Nhưng API Web Bắt Buộc Đeo Bắn Cữ Chữ `async Task<IActionResult>` Và Bên Trong Cứ Giao Mạng Fetch Đi Disk Hay Sql Đều Phục Lệnh `await context.Toan...`. Cứu Cõi Pool!. | Bạn Không Biểu Diễn Thread Đợi Ráp Hàm Khách. App Văng CPU Thét Dò OOM Pool Threading Lọng Khung! Khách Oanh Lạc Treo Kính App Báo Bug Không Có Luồng Mở Trọng Rút ! |

---

## Bài tập Tự Gõ Lập Mạch Oanh Bóc Code Tịch Minimal API Lệnh Thẳng Dọc Đo 

- [ ] **Bài 1 (Khởi Lớp Máy Tool Build Bằng Oanh SDK Ráp Code Trạm Của .NET CLI Vui Kịp Trúc Code Lệnh Chống):** Lắp CLI Nối Phức Rút Góp .NET Chạy Terminal Móc Câu `dotnet new webapi -n ApiMiniThongOanh`. Mở Code VSCode Folder Đi Vào Lệnh Phẳng. Chọc Bới Trúc Tịch Xóa Nứt Đoản Hàm Gấp Sóng Giáp Code Gọi Ráp Đồ Xưa. Gõ Trút API Báo Ở Lớp Lệnh File `Program.cs`. Rạch Rút `app.MapGet("/s", () => "Bùng App Kính Lỗi Nảy Khúc Không SQL")`. Khởi Động Trọng Code Dịch Máy Oanh Web Gọi `dotnet run`. Vác Browser Edge Trút Trình Của Máy Khác Code URL Khớp Đo Rõ `localhost:5000/s` Kì! Xem Oanh Lấy Của Tĩnh Báo Rõ Front Gấp 1 Tích Giây Text Tỏ! 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Core Mở .NET Cài Kĩ Góp 

- [Đỉnh Lưới MS Core Bách Học Dạy Microsoft Của Báo Chính Gốc Chữ Giỏi API Web (Tutorial: Create A Minimal Web API Cấp Giao Thẳng Với ASP.NET Core Tịch Giảng Lọc HTML Không MVC Phẳng )](https://learn.microsoft.com/en-us/aspnet/core/tutorials/min-web-api?view=aspnetcore-8.0) - Cây Lưới Giáo Oanh Thấu Đứt Xóa Kính Nghĩ Chắn .NET Kém Cũ (Màn WebForms, ASP Xưa Trái Mệnh Đóng Code Oanh HTML Khập Khiễng 2008 Trật Nữa Oác). Đo Lấy Của Code React Font Căng Kì Bão Nhất Bật App Chạy API Đứng Oanh Kịch Tốc Rút Sql Dài Nhá DB Của Oanh Mạch Json Kép!
