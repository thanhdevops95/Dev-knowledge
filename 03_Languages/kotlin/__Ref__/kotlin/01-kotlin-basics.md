# 🚀 Kotlin Basics — Nhập môn Kotlin

> `[BEGINNER]` — Prerequisite: Hiểu sơ lược Biến và Kiểu dữ liệu.
> Cứu tinh của lập trình viên Java. Được Google chọn là ngôn ngữ thiết kế chính tắc cho nền tảng Android (First-Class Citizen). Ngắn gọn, súc tích và An Toàn Tuyệt Đối với Null.

---

## Tại sao (WHY) lại chọn Kotlin?

Kotlin chạy trên máy ảo Java (JVM) có nghĩa là nó kế thừa toàn bộ thư viện đồ sộ trăm ngàn cái của Java nhưng với một Cú pháp Ngắn Bằng Một Nửa. Đặc điểm cực mạnh của Kotlin là xóa sổ triệt để lỗi "Billion Dollar Mistake" — NullPointerException bằng cách ép lập trình viên rào kiểu dữ liệu ngay lúc gõ code (Compile-time).

**Vấn đề giải quyết:** Viết Ứng Dụng Android, Backend (Spring Boot), và KMP (Mã đa nền tảng cho iOS/Android chung Base).

**So sánh nhanh:**
| Tính năng | Kotlin | Java | Swift |
|---|---|---|---|
| **Môi trường** | JVM (Mọi rễ Android/Web Spring) | Đi cùng JVM truyền đời | Của Apple (Máy Mac/iOS) |
| **Bảo Vệ Null** | Cực mạnh (Có dấu hỏi chấm `?`) | Yếu (Lỗi chết Tắt App đe dọa) | Cực mạnh (`Optional`) |
| **Boilerplate Code** | Siêu ít (`data class` ăn liền) | Ngập mặt (Hàng tá Setter/Getter) | Vừa phải |

---

## 1. Cài đặt Môi trường (JVM & IDE)

Vì chạy chung trên nền JVM, bạn phải có JDK trước.

**Cài đặt qua Command Line:**
- **Mac/Linux:** Dùng SDKMAN cực kì thần linh.
  ```bash
  curl -s "https://get.sdkman.io" | bash 
  sdk install java
  sdk install kotlin
  ```
- **Windows:** Tải bộ IntelliJ IDEA Community (Hỗ trợ nhúng chuẩn 100% Kotlin vì Sinh Ra Từ Cha Của Nó - JetBrains). Mở bộ IDE ra Gõ Run. 

Kiểm tra CLI (Nếu cài chay):
```bash
kotlin -version 
kotlinc hello.kt -include-runtime -d hello.jar # Biên Dịch Code Rời rạc
java -jar hello.jar
```

---

## 2. Hello World! & Biến

Không cần một dòng `public static void main(String[] args)` khổng lồ của Java.

Kịch bản `hello.kt`:
```kotlin
// Entry point duy nhất Rút Siêu Gọn Ở File Mọi Kotlin
fun main() {
    println("Chào mừng bạn tới Kotlin World!")

    // -- 1. Từ Mấu Chốt: val (Hằng Bất Biến / Constant Value) 
    val name: String = "Kotlin Dev" 
    // name = "Java" // LỖI NGAY TỨC KHẮC BÁO BỞI TRÌNH BIÊN DỊCH

    // -- 2. Từ Mấu Chốt: var (Biến thay đổi Được / Variable)
    var age = 22 // Kotlin cực kỳ Thông Minh tự Bắt Kiểu Int (Type Inference Khỏi phải gõ : Int)
    age = 23    

    // Nội Suy Chuỗi (Thanh Lịch Vượt Java)
    println("Tên tui là $name, Năm nay tôi ${age + 1} tuổi rồi nha!")
}
```

---

## 3. Điều Khiển Kiểm Tra (If / When - Thay thế Switch/Case)

Trong Kotlin, `if` có thể CÓ GIÁ TRỊ trả Về Ngay Vào Biến Lớn! Rất Tiện Lợi Bỏ Cốt Ternary `x ? a : b;` Của Java.

```kotlin
val mark = 85
// Bắt Gộp Trả Biến 
val result = if (mark > 50) "Pass" else "Fail"

// WHEN: Bản nâng Cấp Vượt Trội của Switch Case Cổ Điển
val rank = when (mark) {
    in 90..100 ->  "Tuyệt Đỉnh (A+)"
    in 80..89  ->  "Khá Giỏi (B)"
    70, 75     ->  "Ngay Vạch Phân Cách"
    else       ->  "Trượt Cố Lên (F)"   // (Else BẮT BUỘC Phải có Để Cover 100% Trường Hợp Bị Lọt)
}
println("Xếp Loại Của Bạn: $rank")
```

---

## 4. Collection (Read-Only và Mutable) & For Loops

Kotlin ép Bạn phải Nhận Thức Chênh Lệch Giữa Mảng Cố Định (Bất Biến) Và Mảng Co Giãn Được (Sửa Chữa / Mutable).

```kotlin
// 1. MẢNG CỐ ĐỊNH CHỈ ĐỌC (TỐC ĐỘ SIÊU KHỎE BÁN TỚI CPU)
val listTraiCay = listOf("Táo", "Cam")
// listTraiCay.add("Nho") // IDE Đỏ Ngầu Báo Lỗi Ngay Hàm Cấm Add

// 2. MẢNG MỀM CO DÃN ĐƯỢC 
val listNhanVien = mutableListOf("Aki", "Huy")
listNhanVien.add("Vy") // Cực kì Thoải Mái
listNhanVien.removeAt(0)

// 3. DIỄN LẬP (LOOPS / RANGES) - Đọc Siêu Tự Nhiên
for (nv in listNhanVien) {
    println(nv)
}

// Bơm Tràng 1 Tới 5
for (i in 1..5) println(i)

// Tụt Từ 10 Xướng 1 Nhảy Bậc 2
for (i in 10 downTo 1 step 2) println(i) // 10, 8, 6, 4, 2
```

---

## 5. Chức Năng Cực Chất: Bảo Vệ NullPointerException (NPE)

Nếu kiểu dữ liệu có thêm **Dấu Chấm Hỏi Cắm Giữa** Thì mới có quyền Nhận chữ `null`. Ngược lại Biến Nguyên Tuổi Lỗi Trình Gõ Biên Dịch Ngăn Trực Tiếp.

```kotlin
// 🔥 CỘT MỐC LỚN NHẤT CỦA KOTLIN SAU HÀNG NĂM SỐNG SÓT QUA LỖI JAVA TRONG APP RUNTIME

var city: String = "Hồ Chí Minh"
// city = null   // ERROR!!! Trình Biên Dịch Đóng Bang KO Cho Chạy Build Chặn Trước Khi Gây Hoạ.

var company: String? = null // Cú pháp ?: Có Ý là "Có Khả Năng Nổ Giá trị Rỗng Mất Máy"
company = "VinGroup"
company = null

// -- Toi Mang String này Tính Chiều Dài Cắt Chữ Bất Chấp Lỗi. Nếu Có Lỗi thì Trả RA "?"
println("Chiều dài Độ Chuỗi Tổ Chức Khoái là: ${company?.length}") // Ra CHữ Null không bể APP

// -- ÉP THÔ BẠO LÊN LÀ BIẾN MẢNG CHUỔI CHẮC CHẮN KO NULL NẾU SAI BỂ CRASH APP XIN CHỊU 
// Dấu "!!" - Gợi Ngôn: Băm Sập Sàn Nhà (Double Bangs Operator) LÀM Đứt Nổ Crash Phát Điên (Không Khuyên Dùng Nếu Yếu Tim)
// println(company!!.length)  // Nếu Null, Văng Báo Lỗi Runtime Null Exception (Cấm Kị Tuyệt Đối Khi DEV Android)

// -- ELVIS OPERATOR Giúp Bạn Thay Biến Lỗi Thành Chuẩn Tạm Rất Thanh Mát
val anToanDoDai = company?.length ?: 0  // Ý Rằng NẾU LÀ NULL HÃY Biến THÀNH SỐ KHÔNG(0).
println(anToanDoDai)
```

---

## 6. Lập Trình Hướng Đối Tượng Tối Giản (OOP & Data Class)

Rào Cản đau lòng của Lập Trình Viên Java Là Việc Gõ Constructors Dài Bất Tận... Thêm Getter Rồi Sinh Hàm Setter Hash Code... 

Ở Kotlin, Bạn chỉ cần đúng 1 chữ: `data`. 

```kotlin
// Tọa Tạo Một Object User Đẩy Lên CSDL Đủ Getter Setter toString Ẩn Cho Bạn 
data class User(val id: Int, var userName: String, val isActive: Boolean = true)

fun main() {
    val aAki = User(1, "Akihiro") // Không cần từ `new`
    println(aAki) // Output Đẹp Ngỡ Ngàng Tự Động: User(id=1, userName=Akihiro, isActive=true)
    
    // Copy Biến Cấu Tạo Object Giữ Nguyên Biến Cũ Để Sang Class Instance Khác Chỉnh Duyên Chỗ MỚi
    val cloneAki = aAki.copy(id = 2) 
    println(cloneAki) 
}
```

---

## Gotchas — Bẫy Nên Chọn & Từ Chối Khi Lên JVM Kotlin

| # | ❌ Cú Pháp Cũ Lạc Hậu Xưa | ✅ Kotlin Idiomatic Đường Mới Chặn Bug | Hậu quả của Việc Làm Cẩu Thả |
|---|--------|---------|------------|
| 1 | Ép Bằng Ép Buộc Cho Gây Bể Object Dùng `!!` Mọi Nơi Réo Rắt Quanh Viền Tránh Null Sập Quen Java. | LUÔN Bọc Hàm Khéo An Toàn Của Elvis Gọi Kéo Toán Tử Lấy Bù Biến Đệm Phụ `?.` / `?:`. | Viết `var!!.meth` Khi Nó Cắn Rỗng Là Nguyên Căn Crash Báo App Sưng Trắng Vô Hộp Sỉ Lỗi Dev Nghiệp Dư! |
| 2 | Cố Đeo Lại Set Class Rỗng Quanh Constructor Chì Kẽm Có Lệnh Khai Hàm Khó So Bằng Java Code Trông Cằn. | Gõ Nhanh 1 Dòng Data Mồi Ngắn Lập Class `data class Mod`. | Class Dư Thừa Mã Nguồn Gây Code Rác Cản Mắt Thẩm Mỹ Đọc Dự Án Khổng Lồ. |
| 3 | Lập Trình Code Nhánh Dày If / Else Trong Khi So Sánh Kiểu Dữ Liệu String Giống Mất Tập Trung Logic. | Trải Phẳng Code Kiểm Toán Rõ Lường Hợp Hàng Khi Bọc Vào Block Tường Minh `when (x)`. | Nhánh Cây Quá Khó Cắt Ngắt Hiểu Cặn Sai Phủ Bóng Đầy Lỗi Lọt Bỏ Quên Condition Cuối Quanh Rút Dây Else Đen Tối. |

---

## Bài tập Làm Nhanh Giữ Căn Bản Điểm JVM

- [ ] **Bài 1 (Dễ):** Tạo Lệnh Ràng Chuỗi Tuổi (`val age`). Gọi vòng `When` Nếu Dưới (12) Ra "Khách Thiếu Nhi Bé" - Ngược lại > Giá "Người Lớn Chuẩn" Vào Biến Hỗn Nạp In Ra Ngay Chấm.
- [ ] **Bài 2 (Trung bình):** Xây Dựng 1 Class (Hạng Mác Khung Bản Thiết) `data class SanPham` chứa (`id, giatien, ten_chu_viet`). Quăng Mảng Thau Vào Một Mảng Co DãMutable `mutableListOf()`. Liệt Danh Gọi Hàm Collection Của Mảng Lọc Mọi SanPham Giá Khỏi Viền Dưới Bé Thua (Mức <= Trăm Trăm 100). Sau đó Vòng Ra Đồ in Mảng.  

---

## Tài nguyên Đọc Sâu Mở Khoá Hơn Thách Thức

- [Trang Chủ Play Dựng Web Tĩnh Test Run Kotlin Ngay Nhấn Code Chơi](https://play.kotlinlang.org/) - Trang PlayGround của Kotlin Cực Sướng Để Gõ Online Bất Biến Code Phông Chuẩn.
- [Kotlin Cẩm Nang Koans Tập Coding Lâu Dài](https://play.kotlinlang.org/koans/overview) - Chuỗi Giải Đố Game Nhỏ Đi Qua Từng Hướng Tĩnh Idiomatic Học Tư Duy Mới Nhất Xóa Cũ Nếp Java.
- [Sách Chuẩn Android Tinh Thông Căn Cắt Nhóm App](https://developer.android.com/kotlin) - Tài liệu Giáo án Toàn Diện Tập Android Nôi Cố Đủ Phẩm Kotlin Cụ Thể Phát Họa Phẳng Cho Ngành Dev Mobile.
