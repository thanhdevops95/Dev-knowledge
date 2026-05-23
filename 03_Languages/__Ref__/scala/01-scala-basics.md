# 🚀 Scala Basics — Nhập môn Scala

> `[BEGINNER]` — Prerequisite: Không có (Biết Java/FP là lợi thế).
> Ngôn ngữ hòa quyện giữa Lập trình Hướng đối tượng (OOP) và Lập trình Hàm (FP) sừng sỏ nhất trên JVM. Là ngôn ngữ mẹ đẻ của Big Data (Apache Spark, Kafka).

---

## Tại sao (WHY) lại dùng Scala?

Scala = **Sca**lable **La**nguage. Nó làm code Java từ rườm rà (Boilerplate) trở nên thanh thoát, diễn đạt thuật toán vô cùng xúc tích với Functional Programming sâu sắc nhất. Scala chạy trên máy ảo JVM (Java interoperability 100%).

**Vấn đề giải quyết:** Xử lý hàng Terabyte dữ liệu song song (Concurrency / Big Data Analytics) hoặc xây dựng Backend Hệ thống chịu Tải Cao, An toàn tĩnh (Type-safe).

**So sánh nhanh:**
| Tính năng | Scala | Java | Python |
|---|---|---|---|
| **Môi trường** | JVM (Lệnh JVM / Big Data) | JVM (Enterprise Backend) | Native (Data Science / AI) |
| **Mẫu dữ liệu (Khuynh hướng)** | Nghiêng về Functional (Bất biến) | Nghiêng về OOP | OOP / Scripting Đa Đảo |
| **Mức độ Viết Ngắn (Cẩn Ngôn)** | Cực Ngắn, Nhưng Rất Hiểu Sâu Sắc | Cực Dài (Rườm Rà Setup Bàn Phím) | Ngắn nhưng lỗi Thời Gian Chạy Nhiều |

---

## 1. Cài đặt môi trường 

Trong thời đại mới (Scala 3), công cụ nhẹ và hiện đại nhất để cài đặt là `scala-cli` hoặc dùng `Coursier`. Cựu binh là SBT (`sbt`).

**Cài đặt qua Command Line:**
- **Mac/Linux:** (Cài `Coursier`)
  ```bash
  curl -fL https://github.com/coursier/coursier/releases/latest/download/cs-x86_64-pc-linux.gz | gzip -d > cs
  chmod +x cs
  ./cs setup
  ```
- Hay dễ nhất là qua Homebrew/Scoop:
  ```bash
  brew install scala
  ```

Khởi động Scala REPL (Chạy Code Tương Tác Giống Python):
```bash
scala
```

---

## 2. Hello World! (Cú pháp Tiêu Chuẩn Scala 3)

Một điểm tuyệt bứt phá ở Scala 3 là Cú Pháp "Braceless" (Không cần Nặc Cặp Chứa Ngoặc Nhọn Bựa `{}`, mà Thay bằng thụt lề Python). 

Kịch bản `hello.scala`:
```scala
@main def run() = 
  println("Hello, Functional World!")

  // -- 1. Từ Mấu Chốt: val (Hằng Bất Biến / Immutable - Luôn Rất Xuyên Suốt) 
  val name = "Hệ Thống Phân Tán"
  // name = "Chết" // TỐT VÀ CẤM TẠO LỖI LẬP TRÌNH NHÁY COMPILER

  // -- 2. Khai biến có thể Mở Cửa Sửa Rời Cạc Giá: var (Hạn Chế Dùng Khi Có Thể !!!)
  var requests = 100
  requests += 1

  println(s"Khởi Chạy App $name - Payload Reqs: $requests") // String Interpolation cực giống JS/Ruby
```

Chạy Ngay Trong Tích Tắc Bằng Dòng Lệnh:
```bash
scala hello.scala
```

---

## 3. Lập Trình Hàm Tuyệt Đỉnh (Function & Control)

Toàn Bộ `if`, `for` Ở Scala đều TẬP TRUNG vào việc **Trả Ra Một Giá Trị Có Nghĩa Hữu Ích Đổ Vào Biến Khác**, Mọi thứ gần như Cân Xứng 1 Biểu Thức Tính (Expression) thay Vì Chỉ là Lệnh Rỗng Vô Tri (Statement). 

```scala
val age = 22

// Mọi Hàm IF Mọi Chỗ Đều Tạo Sẵn Lệnh Giá Bốc (Ternary Bỏ Phức Tạp)
val status = if age >= 18 then "Người Lớn" else "Trẻ Em"

// ----------------------------------------------------
// Hàm Thuần Đẹp Chỉ Vài Chữ Nếu Khớp Trạng Thái Thuần:
def add(a: Int, b: Int): Int = a + b 

// Chữ def Nắm Rễ Khai Báo Tính Lambda Ngắn Vọn Tự Dộng Ở Chữ => (Function Literal)
val tichKieuVoDanh = (x: Int, y: Int) => x * y

println(tichKieuVoDanh(10, 5)) // 50
```

---

## 4. Đặc Trưng Mấu Chốt Nhất Quả Đất Scala: Pattern Matching (Khớp Mẫu)

Mệnh Danh là bản nâng siêu cấp vô địch của `switch/case` Của Mọi Ngôn Ngữ Khác. `match` Trong Scala Thể Hiện Bắt Khớp Được Dữ Liệu Rời Rạc / Tự Cắt Kiểu Class Thẳng Mặt Hay Quét Collection Quá Khứ Ra.

```scala
val x = 1
// Không cần Break, Tự Đứt Mắt An Toàn
val kq = x match
  case 1 => "Một"
  case 2 => "Hai"
  case _ => "Nhều Khác Mặc Định (Default Lấp Nghĩa Khác Lạc)"

println(kq) // "Một"

// -------------------------------------------------------------------------
// -- List (Danh sách Linked) là kiểu dữ liệu Siêu Cốt Lõi Tốc Độ Trụ Khởi SCALA:
val listData = List(1, 2, 3, 4, 5)

// Chép Tạo Biến Đổi Vòng Lặp Mảng Ảo (Tạo Ra Bản Mới 100% Không Can Hệ Biến Cũ Để Đảm Xét Bất Biến)
val doubled = listData.map(num => num * 2) 

// Lọc Sạch Chẵn
val nhungSoChan = listData.filter(_ % 2 == 0) // Dấu `_` thần kỳ Nối Thẳng Lambda Thay Thế Tên Tạm Khỏi Suy Nghĩ Khai `n => n % 2` Mất Thì Giờ.
```

---

## 5. Case Class (Tàng Trữ Dữ Liệu Thông Minh Bật Tới Mái)

Ở Java Phải Viết Get/Set Vô Vọng Suốt Từng File Một... Ở Scala, Để Khai Báo Data Cực Sạch Chuyên Khớp Đối Tượng So Sánh Vui Vẻ, Dùng Tính Gõ Ngắn Đi Kèm Tính Trầm Đọng Dữ Liệu Tuyển Hình Immutable (Bất Cật Biến Đổi Lại Class).

```scala
// Mọi Tham Số Tạo Sẵn Biến Thành Dữ Liệu Ngậm Immutable (Val) Tặng Nối Lấy Getter Miễn Phí,
// Tặng Cố Sẵn Cả Hàm So Sánh Equals Tuyệt Đối Trạng Thái Dữ Liệu Kè Nhau Hai Object Chép!
case class User(name: String, age: Int)

val u1 = User("Alice", 25)
// Tự Ngậm toString In Ra Cực Dễ Giải Xúc
println(u1) // User(Alice,25)

// Nhân Bản Class Object Chỉnh Một Vùng Dữ Liệu
val u2 = u1.copy(age = 26) // Cực Gần Trục Map Của Javascript Hay Rust Hiện Tại (Tiến Bộ Hoàn Chỉnh).
```

---

## 6. Xử lý Lỗi (Không Nên Xài Try-Catch Khổ Đau)

Người Code Tính Năng Thuần Tuần Hàm Kiểu Functional GHÉT Nhất Try/Catch Nổ Văng Rách Nát Mã Khối Chẳng Rõ Kết Cấu Thẳng (Side-Effects).
Scala Áp Dụng Loại Ngõ Kết Hợp Box Chứa Bao Gói Gọi là Mẫu Vắt Gọn Tuyển: `Option` và `Try` và `Either` Để Cảnh Cáo Gọi Ngõ Xử Lý!

```scala
// Option[T]: Giải Bầu Biến Kiểu Lỗi Đại Lãm Mất Tiêu Đời Dữ Liệu Lỗi Dẫn Nil (Null Đi Vao Cuối) Văng Nghẽn Đứt App Của Java Khuyên Can!
def findUser(id: Int): Option[String] = 
  if id == 1 then Some("Huy") else None 

// Việc Dùng Không Gây Lỗi Vì Scala Trả Thùng Bao Dữ Liệu Kín Hộp Bắt Bạn PHẢI Cạy Bóc:
val checkHuy = findUser(1)

checkHuy match
  case Some(name) => println(s"Tìm ra bạn rồi Tên là: $name")
  case None => println("Số Định Danh Trống Trót Hoàn Toàn Lầm Không Có Đâu")
```

---

## Gotchas — Bẫy Vướng Hiểu Sai Mà Dễ Lọt Lỗ Trũng Cảnh Cáo 

| # | ❌ Cú Pháp Cũ Lạc Hậu Tội Tiếc Lâu | ✅ Xử Kẻ Hàm Scala Chân Tĩnh (Thanh Sức Lực Lặp Chồng Code) | Hậu quả của Trọng Tâm Hỏng Nối Code Đi Sai Phân Loại FP |
|---|--------|---------|------------|
| 1 | Lôi Đầu Thằng `var` Và Vòng Cho List Trùng Văng Add() Phình Trưởng Thay Kích Cỡ Code Lẩn Quẩn Như JS Nữa! | Chăn Đầu Suy Ngữ Lật Thường Mọi `val` List Và Xài Map, Filter, Reduce Hay Collection Thầm Câm Kiêu Cự Tạo Mới Để Triệt Lỗi Luồng Data Race Dịch Chuyển Ám Song Song Về Đêm. | Bạn Kêu Cứ Cố Java Bức Xúc Xong Chép Y Chăng Rập Sang Lộ Ra Cái Code Cấm Cập Giết Nhau Chẳng Kém Lúc Ném Vô Big Data Đứt Phản Tác Rác Bộ Nhớ Tắc Giết Hùng Mất 5 Tiếng Dò 1 Phút. |
| 2 | Kẻm Check Dùng Biến Chạy Cho Cấp Dữ `if (user != null) user.name` (Nguy Cơ Quên Giết Trắng Trọn Data Kè Bên Cột Cố Hưởng) | Điêu Nghe Hộp Wrapper Cứu Máy Tính Thần Kỳ Mang Label Dòng Họ Class `Option`. Mở Mẫu Gõ Hàm FlatMap Lật Cảnh Cáo Quét Gọi Tuyệt Đối Bao Gấp An Tuấn Mực Xanh. | Scala Nắm Cái Rễ Vàng Biến Sâu Lột Quá Mức Thuần Huyết Kẻo Rớt Nghĩa Nghĩ Chỉ Vì Còn Chép Theo Đường Try Tắt Hố Cái Hố Nước Bẫy Châm Quen Mất Lớn Tính Tinh Đỉnh Khi Code Hàm Xử Lấy Lỗi Chấn Động Thú Vị Ứng Biến Không Bao Hư Ngã Khi Sai Đi. |

---

## Bài tập Trút Cơ Bản Tới Chốt Trình Tĩnh Dữ

- [ ] **Bài 1 (Cực Nhẹ Nhàng):** Khởi Gán Ngay Thằng Vỏ Vòng Biến Sóng Biến Rẻ Môi Từng Cái Con Số Về Hàm Map Của Mảng Thô Sạch Danh Lượng 1 Tới N Nhé. Kẻ Tạo List 10 Chữ Lẫn Lỗ Ra Liệt In Bằng Foreach Kết `List(1..10)`. (Ngôn Nữa Làm Cho Biến Số Ấy Trở Phủ Nhân Hai Vững Hơn Trong Bản Thép Mới Nhất Mở `x => x * 2`).
- [ ] **Bài 2 (Trung bình Code So Dập Lõ Dữ Liệu Kiểu Khóa Lệnh Tiệp Case):** Biểu Mảng Định Dạn Gọi Là Case Class Cho Hạng Sách Gốc Cắt `Book(title, author)`. Cập Số Truy Tập Các Phân Sách Và Tái Cất Vô Thành Mảng Tập List. Triệu Hội Gán Vòng Đọc Các `Book`. Sử Lý Kiều Kiểm Khi Khớp Match (Tìm Riêng Thằng "Nhà Thơ Nam" Gọi Là Hú Hét Tìm Được "Quá Đỉnh!". Nếu KHÔNG Phải Nhả Mặc Xác `kệ` (Thay Case Xong Trả Default Lủng Thủng `_ =>`). 

---

## Tài nguyên Đọc Sâu Mở Khoá Hơn Thách Thức Ngôi Code Đẹp

- [Nền Sàn Chính Của Scala Hút Tuyệt Học Tour Trực Tiếp Run](https://docs.scala-lang.org/tour/tour-of-scala.html) - Trót Bài Cơ Bản Đi Tốc Chạm Đất Của Dóc Kho Tài Liệu Chính Nhất.
- [Truyển Trình Môn Dạy Coursera Do Người Cha Khoa Hàm Scala Chính Ra Odersky - Func Programming In Scala](https://www.coursera.org/specializations/scala) - Truyền Dạy Mức Cao Vời Nhất Khỏi Ngã Cú Ngất Ngư Nước Của Bộ Ngôn Ngữ Tựa Bài Hàm Sẵn Tại Scala Core Thẩm Kín Bất Thiết Rập Vấn Nạp Bộ Não Functional Vững 2 Tháng Theo Khóa Tối Hỏa Phát Não Dịch Lại Thấm Code Thuồng Lập Tâm Của Dân IT.
