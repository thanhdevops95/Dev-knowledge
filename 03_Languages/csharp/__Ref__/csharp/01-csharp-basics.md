# 🎯 C# Basics — Nhập môn C#

> `[BEGINNER]` — Prerequisite: Không có (Biết Java/C++ là lợi thế lớn).
> Ngôn ngữ Hướng Đối Tượng (OOP) kiểu tĩnh hiện đại nhất của Microsoft. Xương sống của hệ sinh thái khổng lồ .NET, cực kì mạnh mẽ cho Enterprise Backend và Game Dev (Unity).

---

## Tại sao (WHY) lại dùng C# (C Sharp)?

C# ra đời như câu trả lời khôn ngoan của Microsoft đối với Java. Trải qua hơn 20 năm tiến hóa, C# hiện tại hội tụ đầy đủ tinh hoa của Functional Programming, Asynchronous (Bất đồng bộ) gọn nhẹ, và tốc độ siêu nhanh (nhờ .NET Core/.NET 8+). Đặc biệt, tính năng LINQ của thẻ C# luôn được coi là nghệ thuật xử lý mảng (dữ liệu) số 1 trong mọi ngôn ngữ.

**Vấn đề giải quyết:** Xây dựng phần mềm doanh nghiệp đa nền tảng (Web, Desktop, Mobile Xamarin/MAUI), Cloud Microservices và lập trình Game 3D.

**So sánh nhanh:**
| Tính năng | C# (.NET) | Java (JVM) | Go |
|---|---|---|---|
| **Cú pháp** | Rất hiện đại (Ít Boilerplate hơn) | Rườm rà truyền thống | Cực kì Tối giản |
| **Bất đồng bộ** | `async / await` (Task) cực mượt | Virtual Threads (Java 21) | Goroutines (channel) nhẹ |
| **Truy vấn Mảng** | LINQ (Vô đối về thẩm mỹ) | Stream API (Dài dòng) | Tự viết vòng lặp `for` |

---

## 1. Cài đặt Môi trường (.NET SDK & IDE)

Ngày nay, bảng cài .NET Core chạy được hoàn hảo trên cả Linux/Mac chứ không vướng víu dính độc quyền Windows nữa.

**Cài đặt qua Command Line:**
- **Windows:** Tải Visual Studio Community 2022 (Vua của các IDE) tick vào ô ".NET Web Development".
- **macOS / Linux:** Cài SDK tại [dot.net](https://dotnet.microsoft.com/download), hoặc dùng script/Homebrew:
  ```bash
  brew install --cask dotnet-sdk
  ```

Kiểm tra và Khởi tạo Dự Án (Console):
```bash
dotnet --version
dotnet new console -n HelloCSharp
cd HelloCSharp
dotnet run
```

---

## 2. Hello World! (Top-level Statements)

Trong C# 9.0+, bạn không còn cần khối Class `Program` và hàm `Main` chật chội để chạy Hello World như xưa nữa.

Mở file `Program.cs`:
```csharp
// Top-level statements (Chạy từ trên xuống dưới trực tiếp)
Console.WriteLine("Xin chào C# thế giới mới!");

// 1. Biến được cấu định kiểu (Tĩnh)
int age = 20;
double gpa = 3.5;
bool isDeveloper = true;

// 2. Tự suy luận kiểu (var) - Rất Khuyên Dùng
var name = "C-Sharp"; 
// name = 1; // LỖI COMPILER (Kiểu đã chốt tĩnh là String, không nhét Số được)

// 3. Hằng số
const double Pi = 3.14159;

// 4. Nội suy chuỗi (String Interpolation) - Bắt đầu bằng kí tự $
Console.WriteLine($"Ngôn ngữ {name} sinh ra từ năm {2000}.");
```

---

## 3. Điều khiển Luồng và Vòng lặp

Cú pháp của C# thừa hưởng y đúc từ họ hàng C/C++.

```csharp
int mark = 85;

// If / Else
if (mark >= 90) {
    Console.WriteLine("Giỏi");
} else if (mark >= 50) {
    Console.WriteLine("Đạt");
} else {
    Console.WriteLine("Rớt");
}

// Switch biểu thức (Expression - C# 8+) - Rất Ngắn Gọn!
string rank = mark switch {
    >= 90 => "A",
    >= 70 => "B",
    >= 50 => "C",
    _ => "F"     // _ tương tự Cột Cờ Default 
};

// Vòng lặp ForEach dệt Duyệt gọn lẹ
string[] fruits = { "Táo", "Xoài" };
foreach (var fruit in fruits) {
    Console.WriteLine(fruit);
}
```

---

## 4. Tinh hoa Collection & LINQ (Language Integrated Query)

C# cung cấp `List`, `Dictionary`, và `HashSet`. Cùng với LINQ (Công cụ Truy Vấn Nhúng), việc nhào nặn Mảng chưa bao giờ sung sướng đến thế.

```csharp
using System.Linq; // BẮT BUỘC ĐỂ MỞ KHÓA SỨC MẠNH LINQ
using System.Collections.Generic;

// Danh sách (List động)
List<int> numbers = new() { 1, 2, 3, 4, 5, 8, 10 }; // Dùng `new()` Không Gọi Trùng Tên Kiểu

// -- LINQ CHUỖI GỌI HÀM (Fluent Syntax)
// Lọc (Where) -> Biến hóa (Select) 
var evensList = numbers
    .Where(n => n % 2 == 0) // Lọc số Cực Đẹp Tưởng SQL
    .Select(n => n * 10)    // Trả Kết Cục Biến Hoán Ra (Nhân 10)
    .ToList();              // Ráp thành 1 List Chốt

Console.WriteLine(string.Join(", ", evensList)); // In Đoạn "20, 40, 80, 100"

// -- DICTIONARY (Bản Đồ K-V / Map)
var users = new Dictionary<int, string> {
    {1, "Aki"},
    {2, "Huy"}
};
Console.WriteLine(users[1]); // In "Aki"
```

---

## 5. Lập Trình Hướng Đối Tượng (OOP) và Bản Ghi (Record)

OOP Của C# Dày đặc, trang nghiêm và cực kỳ chặt chẽ (Tính trừu tượng, Đóng gói, Kế thừa, Đa hình có đầy đủ 100%).

```csharp
// Class tiêu chuẩn với Thuộc tính (Properties) rút gọn Getter/Setter
public class Animal {
    // Tự sinh backing field ngầm định (Giấu biến Private)
    public string Name { get; set; } 
    public int Age { get; private set; } // Chỉ Đọc Trả, Cấm Bị Đè Từ Ngoài
    
    public Animal(string name, int age) {
        Name = name;
        Age = age;
    }

    // Hàm Ảo (virtual) Cho Phép Lớp Con Ghi Đè (override) Lên Nó Được
    public virtual void Speak() {
        Console.WriteLine("Đang kêu...");
    }
}

// Lớp Con
public class Dog : Animal {
    public Dog(string name) : base(name, 1) { } // Gọi Về Constructor Cha

    // GHI ĐÈ
    public override void Speak() => Console.WriteLine(Name + " Sủa Gâu Gâu!");
}

// ============================================
// CHỨC NĂNG SIÊU ĐỈNH KIẾN TRÚC MỚI: RECORD (C# 9+)
// Sinh ra để lưu Model Dữ liệu Bất Biến (Value-based Equality). Thay Thế Khối Class Hàng Trăm Dòng Chỉ Bằng 1 Dòng Code:
public record UserData(int Id, string Email);

var u1 = new UserData(1, "test@mail");
var u2 = new UserData(1, "test@mail");
Console.WriteLine(u1 == u2); // TRẢ TRUE!!! (Class Cũ rỗng không Override Equal Sẽ Bề Output Thành Mặc Nhận Tính Móc Vùng Nhớ RAM Là FALSE).
```

---

## 6. Xử lý Lỗi Bằng Try/Catch 

Kiểm Soát Nguồn Chạy Code Khi Biến Hoặc Truy Quẹt DB Gặp Ngoại Lệ. (Kỹ Năng Cấp Bách Cho Enterprise Dev).

```csharp
try {
    int x = 10;
    int y = 0;
    int res = x / y; // OOPS Nổ!!!
} 
catch (DivideByZeroException ex) {
    Console.WriteLine($"Văng Bể Cặp Toán Hàm Chia Vô Tận: {ex.Message}");
} 
catch (Exception ex) { // Hưởng Hàm Chung Gốc Đáy Hốt Tổng Thể Đuôi Cờ Catch-All
    Console.WriteLine("Lỗi Hoảng Máy Toàn Diện Khác.");
} 
finally {
    Console.WriteLine("Xong Xứ Cả Block. Nơi Đổ Quét Băng (Tháo DB Connections/ Đóng Files).");
}
```

---

## Gotchas — Bẫy Nên Từ Chối Mọi Đổ Vào Code C# Đầu Đời

| # | ❌ Cú Pháp Lạc Hậu (Lỗi Nghĩa Lủng) | ✅ C# Idiomatic Cận Bước Phá Kén | Hậu quả của Việc Làm Cẩu Thả |
|---|--------|---------|------------|
| 1 | Cố Sống Bọc Kiểm Mã Khắp Quanh Hết Biến Null Bể Như Java. `if(p != null && p.Name != null)` | Cắm Mở Bộ Báo Vỉ Lại Null Check Project Rèn Trình C#. Kêu Toán Tử Bảo Ngắt Góp Nhánh Dập `p?.Name ?? "Trống"`. | Mã Mạch Mủ Trái Sống Nhập Nhằng Lò Trông Thẩm Mỹ Giảm Cực Phế Lúc Vướng Khối Rì Rầm Code Kém Nước Thấy Toàn IF Bão Bùng Che Nhãn Logic Trong Chốt Code Thật Gây Chán Chuyển Viết DB Hết Tầng. |
| 2 | Nhét Vững String Rút Lệnh Lồng Trội Cảnh Nối Khối Liên Dài Suốt Cụm Kéo Bằng Vòng Đẩy Plus `+` Kéo Phù Bộ Cấp Khí CPU Lúc GC Quyết Lục Gom Heap Dọn Rác Máy Tối . | Phủi Thay String Builders Bằng Mật Class `StringBuilder` Phía Framework Trị 100+ Thùng Buffer Khởi Sắp Sẵn Trong Khối Hợp Code Nếu Cấu Cỡ Hơn Năm Xâu Lệnh Lên Kè Song Tới. | Ứng Dụng Mạng (ASP NET WEB) Treo Máng Viền Mức Ram Chụp Máy Nặng Tại GC Stop The World Chận Thread Trình Dừng Quàng Trọng Xử CPU Kẽ Biến Kéo Khựng Xảy Nỗ Quẩn Rụng Thua Nửa Sức App Cấu Node.. |
| 3 | Bày Thẳng Việc Nặng Loop Phía Sau Tấm Button Kéo Chuột UI Hủy Luồng Chặn Đóng Nơi Mạch Gốc. | Nêm Vào Khung Trừ Async Chữ Định Hàm Task `async Task DoTask()` Khi Thấy Luồng File System/Web Thở Kẹt Lỗ, Đẩy Nâng `await fetchDb()`. | Treo Windows Form / Chớp Giật Thùng Not Responding App Tạt Băng Tạt Sập Gây Cáu Ức Mọi Thói Nhấp Khách Sợ Tắt Bực Phàn Nàn 1 Sao Tới Ngai Nghề Lập Khai Nước Phẩm Kém Rụng Chóp App! |

---

## Bài tập Làm Bàn Thúc Ngai Nước Sắc (Tự Code)

- [ ] **Bài 1 (Khởi Tạo Dễ Thương Mỏng Chạy Mạch):** Nắm Danh Quẹt Bọc Số Mảng Collection Array Gồm Hàng Thập Phân (Khai var Mảng Nhét Vung `[3.5, 4.0, 1.2, 5.0]`). Đi Lệnh Query Cột Phía LINQ Biến Đẩy Vượt Qua Phễu Sàng Chỉ Lọc `Where` Thổi Bọn Có Gí Trị Kè `>= 3.0` Khỏi Giới Và Chọn In Mảng Này Xem Xét Order Lên . 
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Gặp Dây List Lên Cấp Record Lõi):** Cấp Lập Khung `record Course(string Title, int Credits)`. Tạo Trộn List Khoảng Vài Khoá Môn Đào Tào Chứa Hàm Nhánh Trong. Xài Cú Lọc LINQ Kết Tính Tổng (Lệnh Cấp Cao `.Sum(x => x.Credits)` Khỏi Viết `for` Cho Tổng Khó Tái). Nhè Đáp Án Số Ra .  

---

## Tài nguyên Đọc Sâu Mở Khoá Cơ Chế Vững Đi Đường NET

- [Bộ Tour Xuyên Khóa Docs Của Hãng Rễ Microsoft Learning MS Gốc Cho C# Vững Khung Đĩnh Bảng Chạy Sóng C-Sharp Dev Gốc](https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/) - Trái Tài Cốt Não Để Có Ngang Đỉnh. Nền Cứu Kiến Giữ Chắc Lưỡi Mã Xịn Từ Cha Đẻ Đóng Cho Lọc Cặn Hàng Dev Hạng Khó Tới Cao Mức Enterpise.
- [DotNet C# In Bộ Thùng NutShell Lướt Kiến 10 Bản Cuối](https://www.oreilly.com/library/view/c-10-in/9781098121215/) - Gói Khung Tiêu Đúc Kiến Kinh Tóm Cặp Ngang Dạng Reference Sức Nặng Rút Trúc Tột Gốc Hiểu Thấm Trình Cơ.
- [Học Gõ Trên Trình Fiddle Online Chỉnh Nhấp Code Lấy Xong Vượt Đích](https://dotnetfiddle.net/) - Bản Nền Vùng Test Nhanh Không Giết Thùng Khung Lôi Hú Win Mệt Ram Vẫn Thử Được Dăm Khúc Mật Thuật Lệnh LINQ Check Bug Giải Cứu Dev Lười Sửa Nháp Ngay Trình Nền Tảng Browser Trong App.
