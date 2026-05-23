# 🎯 Dart Basics — Nhập môn Dart

> `[BEGINNER]` — Prerequisite: Không có (Biết Java/JavaScript là lợi thế).
> Ngôn ngữ client-optimized của Google. Đây là linh hồn của framework đa nền tảng Flutter.

---

## Tại sao (WHY) lại dùng Dart?

Dart là một ngôn ngữ "nổi lên từ cõi chết" nhờ sự bùng nổ của Flutter. Nó được sinh ra ban đầu để thay thế JavaScript trên trình duyệt (nhưng thất bại), sau đó Google hồi sinh nó với mục tiêu cực kỳ rõ ràng: **Tạo ra một ngôn ngữ hoàn hảo để vẽ giao diện người dùng (UI), có khả năng biên dịch sang Native (AOT) cho Tốc độ và biên dịch sát lúc (JIT) để Hot Reload khi phát triển.**

**Vấn đề giải quyết:** Xây dựng ứng dụng di động/desktop/web (thông qua Flutter) từ một Database Code base duy nhất.

**So sánh nhanh:**
| Tính năng | Dart | JavaScript/TypeScript | Java |
|---|---|---|---|
| **Môi trường chính** | Flutter (Mobile, Desktop, Web) | Trình duyệt, Node.js | JVM (Android cũ, Backend) |
| **Kiểu gõ (Typing)** | Tĩnh (Static) ngặt nghèo + Null Safety | Động (JS) / Tĩnh (TS) | Tĩnh ngặt nghèo |
| **Biên dịch** | AOT (chạy thật) & JIT (Dev Hot Reload) | Thông dịch (JIT gốc) | Biên dịch ra Bytecode (JIT) |

---

## 1. Cài đặt Môi trường (SDK & IDE)

Nếu bạn học Dart để làm Flutter, bạn cài đặt trực tiếp Flutter SDK (vì nó đã chứa sẵn Dart bên trong). Nếu chỉ muốn học Dart chay:

**Cài đặt qua Command Line:**
- **Windows:** Cài qua winget hoặc choco.
  ```cmd
  choco install dart-sdk
  ```
- **macOS:** 
  ```bash
  brew tap dart-lang/dart
  brew install dart
  ```

Khởi chạy và kiểm tra:
```bash
dart --version
dart run hello.dart
```

---

## 2. Hello World! & Khai báo biến (Sound Null Safety)

Mọi chương trình Dart **bắt buộc** bắt đầu từ hàm `main()`.

Kịch bản `hello.dart`:
```dart
void main() {
  print("Xin chào Thế giới của Flutter!");

  // 1. var - Trình biên dịch tự hiểu kiểu (Type Inference)
  var name = "Ganyu"; 
  // name = 12; // LỖI (Dart gán cứng kiểu lúc đầu rồi)
  
  // 2. Kiểu dữ liệu tĩnh Rõ Ràng
  int age = 22;
  double height = 1.75;
  bool isDev = true;

  // 3. String Interpolation (Nội suy)
  print('Tên tôi là $name. Năm sau tôi ${age + 1} tuổi!');

  // 4. Hằng số (Có 2 loại rất khác biệt)
  const pi = 3.14;        // Phải biết lúc Compile-time (Viết code xong biến cứng luôn)
  final timeNow = DateTime.now(); // Xác định lúc Runtime nhưng không bao giờ đổi nữa (Chỉ gán 1 lần)
}
```

---

## 3. Hàm (Functions & Tham số)

Điểm MẠNH nhất của Dart dọn đường cho việc viết Widget Flutter lồng nhau (TreeView) đó là hệ thống Tham số cực tốt.

```dart
// Kiểu truyền thống (Rất chán)
int add(int a, int b) {
  return a + b;
}

// Kiểu mũi tên - Arrow Function (Rất tiện cho hàm 1 dòng)
int multiply(int a, int b) => a * b;

// --- SỰ KHÁC BIỆT: THAM SỐ CÓ TÊN (NAMED PARAMETERS) BỌC TRONG { } ---
// Đây là công thức tạo Widget Flutter vì nó rõ ràng!
void createUser({required String name, int age = 18, String? job}) {
  print("User: $name, Tuổi: $age, Nghề: $job");
}

void main() {
  // Nhờ cặp {} ở trên, không cần nhớ thứ tự biến, nhưng phải ghi đúng Tên!
  createUser(name: "Akihiro", job: "Dev"); // Không xài age thì tự lấy 18. Job bị Null.
}
```

---

## 4. Bảo vệ Biến Rỗng (Sound Null Safety)

Kể từ Dart 2.12, biến không bao giờ được phép mang giá trị `null` trừ khi bạn chủ động gắn cờ `?` vào nó!

```dart
void main() {
  String text;
  // print(text); // Lỗi Compile (Biến chưa được đổ Data)

  String? nameCoTheNull; // Có cờ ?, cho phép rỗng
  nameCoTheNull = null;  // OK hợp lệ

  // ======================================
  // 1. Gọi an toàn (Toán tử ?.) - Tránh Crash App (Billion Dollar Mistake)
  print(nameCoTheNull?.length); // Nếu null thì in ra chữ null (Chứ ko làm Sập App).

  // 2. Toán Tử Cung Cấp Mặc Định (Toán tử ??) 
  String nameDungDeIn = nameCoTheNull ?? "Khách Vô Danh"; // Nếu lởm null, đắp chữ Khách vào
  print(nameDungDeIn);

  // 3. Toán tử Dằn Mặt Khẳng Định CHẮC CHẮN nó KHÔNG NULL (Bang operator !)
  // print(nameCoTheNull!.length); // Nếu Nó Cứ Null Mà Ép Chạy Bằng ! -> DẪN TỚI CRASH SẬP APP 
}
```

---

## 5. Danh Sách Collection (List, Set, Map)

Dart gỡ rối các cấu trúc dữ liệu theo cách hiện đại nhưng vẫn mang hơi hướng Java.

```dart
// --- MẢNG (LIST) DÙNG DẤU [ ] 
// Mặc định gọi là List (Không kêu mảng Array vì nó tự Động Co Giãn Mọi Nơi)
List<String> fruits = ["Táo", "Cam"];
fruits.add("Chuối");

// Spread Operator CỰC MẠNH (Dải mảng vào mảng khác)
List<String> total = ["Mít", ...fruits]; // Mít, Táo, Cam, Chuối

// --- TỪ ĐIỂN (MAP/DICTIONARY) DÙNG DẤU { } CHỨA KEY:VALUE 
Map<String, int> scores = {
  "Toán": 10,
  "Văn": 8
};
scores["Anh"] = 9; // Thêm key
print(scores["Toán"]); // In 10

// Viết IF ngay bên trong Khai Báo Mảng (Collection If - RẤT Hữu Dụng làm UI Flutter)
bool showAdminMenu = true;
var menus = [
  "Trang chủ",
  "Liên hệ",
  if (showAdminMenu) "Cài Đặt Quản Trị Hệ Thống"
];
```

---

## 6. Lập Trình Hướng Đối Tượng & Mixin

Kiểu Hướng Đối Tượng thuần túy. Class trong Dart tự ngầm định sinh Factory Khởi tạo, Không cần tốn quá nhiều dòng mã để khai biến.

```dart
class Animal {
  String name; // Constructor yêu cầu có rào chắn 

  // Cú pháp ngắn Constructor:
  Animal(this.name);

  void speak() {
    print("$name đang kêu.");
  }
}

class Dog extends Animal {
  // Gọi về Constractor cha 
  Dog(String tenCuaCun) : super(tenCuaCun); 
  
  @override
  void speak() => print("$name sủa Gâu Gâu!");
}

// ------ ĐẶC SẢN DART: MIXIN ------
// Một dạng Code Snippets cấy mã (Tính năng Bơi) bám thẳng vào mọi thứ Class khác mà Không Phải Kế Thừa Gốc
mixin Swimmer {
  void swim() => print("Tôi đang Bơi này!");
}

class Duck extends Animal with Swimmer {
  Duck() : super("Vịt xám");
}

void main() {
  var vit = Duck();
  vit.speak(); // Kêu của Animal Kế Bố Mẹ
  vit.swim();  // Tính Tạt Chéo Bơi Của Mixin Trợ Giúp Vây Cánh
}
```

---

## Gotchas — Những Bẫy Rớt Hay Gặp Của Người Mới 

| # | ❌ Tránh (Sai Hoặc Tư Duy Ngược Lối) | ✅ Cần Làm (Code Chuẩn Dart / Flutter) | Hậu quả Trọng Điểm Do Sự Cẩu Thả |
|---|--------|---------|------------|
| 1 | Ép Bằng Ép Đè Biến `!` Khi Nó Bị Trống Giữa Dòng Chạy Bằng Quen Mui Rỉ Sắt Vượt Rào Cản Biên Giới Rỗng Dữ Liệu Lỗi Máy. | Rào Kín Lệnh Với Chấm Hỏi Kéo Vòng `.?.` Hoặc Có Nếu Phủ Kiểm Chắc Block Chữ `if (a != null)`. | App Flutter Người Dùng Đang Xem Trên IPhone Màn Sập Đột Chớp Báo Khung Crashed Nghẽn Liền Tay Nghĩ Lỗi Tội Khởi Nhớ Chập Sờ Bể Khung Null Check Exception!. |
| 2 | Code Danh Thằng Cấu Tham Số Thẳng 1 Cọc Theo Thằng C/Java Trống Kê Hú Chẳng Chứa Chú Thích Ở Kế. Hàm Lõ Rõ `add(2,5,3,true)`. | Khỏi Sợ Tốn Công Khung Dấu Hoặc Cong Bọc Thẳng Cánh Để Named Parameter Cho Chức Nó `widgetCaiKhung({required id, canVe=true})`. | Dòng Code Sau Tháng Nửa Mở Cửa Xem Gặp Hàm Bỏ Bảy Tám Chữ Số Liền Phẳng Cửa Kể Cả Người Code Lại Lộn Mù Chẳng Hiểu Cả Biến Khúc Trống Hàng Truyền Rứa Nghĩa Rì Nếu Java Vướng Khổ Cực Phải Xem IDE Phép Dò Giải. |
| 3 | Khai Sẵn Biến Lõm Bắt Đầu Chứa Kích Vừa Xong (E.g: Widget Tĩnh Hoặc Dòng Số ID Mã) Vẫn Theo Lẽ Khai `var` Dùng. | Nêm Bôi Quét Mảng Dám Trông Xong Hạn Sẵn Ngay Chuyển Thẳng Ngai Về Góc Từ `final` Dựng (Hoặc Cột `const` Tĩnh Nếu Lọc Đặt Không Thể Lệ Làng Chế Rỗng Runtime). | Mảng Trình Mất Mơ Build App Ở Giai Máy Tính Chậm Tốc Gánh Gấp Rưỡi Chỉ Vì Dart Nó Sắp Nhận Build Tự Văng Compiler Thời Nhanh Từng Phút Optimize Rác Ra Rìa Ngăn Máy RAM Hơi Nặng. |

---

## Bài tập Tự Tay Gõ Khẳng Trình Dữ Cơ Bản Nhập Đất Flutter

- [ ] **Bài 1 (Khởi Tạo Dễ Thương Mỏng Chạy Mạch):** Bọc 1 Kho Khóa Cấu Trúc Khối Object Class Định Mô Cho Điện Thoại (`Smartphone`). Đúc Bằng Cấu Constructor Có Bỏ Ngăn Ràng Trọng Dấu Nhọn Nóng Đòi Lên Chấp Tên Hãng `{required name, ram, giaTienTrungBinH}`. Ngẫm Xong Viết Phương Hát (Void Print Info Thông Tin Đẹp Mắt Ra Nhờ Ràng Nháy Kéo Nội Suy Chuỗi Gộp \$Biến). Gọi Hàm Run.
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Gộp):** Khai Lợp Bản Tạo List Mảng Gồm Danh Nối Lộn Xộn Cả 1 Tới N Lệnh Bắt Biến Co `map` (Nhân Tất Các Phần Chữ Số Đôi Văng Về Hàm Mới Khác Array). Duyệt Kết Foreach Ráp Phối IF Khi Collection Hiện Chỉ Nhè 5. 

---

## Tài nguyên Đọc Sâu Mở Khoá Cơ Chế Vững

- [Dart.dev Language Tour Gốc Toàn Bách Dịch](https://dart.dev/guides/language/language-tour) - Đi dạo một lèo Sợi Chân Thực Nét Code Nguyên Thể Từ Team Gốc Google Lập.
- [Cấu Trúc Tuyên Khuyến Do And Dont Effective Dart](https://dart.dev/effective-dart) - Cẩm nang Hành Xử Để Mọi Dòng Trình Gõ Ra Phản Xạ Như Sách Sáng Trong Ngôn Ngữ Này (Đọc Cảnh Trước Trấn Bất Khi Nào Ghé Chế App Hậu Flutter Bự).
- [DartPad Editor Chơi PlayGround Hỏa Tốc Sáng Rõ Xóa IDE Nhanh](https://dartpad.dev/) - Trình Web Không Cần Chạy Cài Giết Tốn Lỗi Chạy Đập Máy Chơi Cốt Test Viết Cấu Hạng Thuật Thuần Phép Thẳng Cửa Sổ.
