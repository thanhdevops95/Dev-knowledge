# 🐘 PHP Basics — Nhập môn PHP

> `[BEGINNER]` — Prerequisite: Không có (Biết cơ bản HTML là một lợi thế).
> Ngôn ngữ script Server-side huyền thoại, cung cấp sức mạnh cho hơn 75% website trên thế giới.

---

## Tại sao (WHY) lại dùng PHP?

PHP (PHP: Hypertext Preprocessor) được sinh ra ban đầu để làm ngôn ngữ nhúng vào HTML. Ngày nay, cùng với sự phát triển của chuẩn OOP, Composer và các Framework như Laravel / Symfony, PHP cực kỳ mạnh mẽ cho hệ thống Backend.

**Vấn đề giải quyết:** Xây dựng website trọn gói Server-Side Rendering (SSR) / JSON APIs siêu tốc độ phát triển.

**So sánh nhanh:**
| Tính năng | PHP | Node.js | Java / C# |
|---|---|---|---|
| **Môi trường** | Server-side web (Web-first) | JS chạy Server | Đa nền tảng, Enterprise |
| **Kiến trúc** | Multi-process/thread per request (Chết ở đâu kệ nó, Req khác vẫn sống) | Đơn luồng (Event Loop) | Multi-thread pool |
| **Hệ sinh thái** | Laravel, WordPress đè bẹp web | REST API, Realtime | Hệ thống phức tạp, Cấu trúc strict |

---

## 1. Cài đặt môi trường

Sự tiện lợi lớn nhất của PHP: Deploy ở đâu cũng chạy được (Shared Hosting). 
Ở môi trường Dev (Máy tính cá nhân), bạn nên dùng XAMPP / LAMP hoặc Docker.

**Cài đặt độc lập (CLI):**
- **Windows**: Tải File zip tại [php.net](https://windows.php.net/download/), giải nén và ném `php.exe` vào System PATH.
- **macOS**: `brew install php`
- **Linux (Ubuntu)**: `sudo apt install php-cli`

Kiểm tra:
```bash
php -v # Lên PHP 8.1+ là chuẩn đời mới (Modern PHP)
```

---

## 2. Hello World

Tạo file `index.php`:
```php
<?php
// Mọi code PHP đều phải nằm trong thẻ mở này (Nếu file 100% PHP không cần thẻ đóng)
echo "Xin chào, Thế giới Web!\n"; 

$name = "Aki";
echo "Chào bạn " . $name . "!"; // Dùng dấu . để nối chuỗi
```

Chạy file:
```bash
# Máy local
php index.php

# PHP có sẵn Web Server mini để test (Chạy tại: http://localhost:8000)
php -S localhost:8000
```

---

## 3. Cú pháp Cơ bản

### Biến, Kiểu dữ liệu & Ép kiểu định danh (Type Hinting)

Biến trong PHP **BẮT BUỘC** phải bắt đầu bằng dấu `$`.

```php
<?php
$is_admin = true;          // Boolean
$age = 25;                 // Integer
$price = 10.99;            // Float / Double
$message = 'Chuỗi thuần';  // Dấu nháy đơn (Không nội suy biến)
$welcome = "Hi $message";  // Dấu nháy kép (Có nội suy trực tiếp biến -> "Hi Chuỗi thuần")

// Chế độ MẠNH (Strict Types) ở PHP 7+ (Nêm đặt ở dòng đầu tiên của File)
declare(strict_types=1);

// Dấu : ở hàm đại diện cho Return Type (Rất giống TypeScript)
function add(int $a, int $b): int {
    return $a + $b;
}

// $result = add("5", 5); LỖI NGAY TỨC KHẮC Type Error! 
```

### Điều khiển luồng (If / For)

```php
// Toán tử ++, ==, === giống hệt C++ / Javascript
if ($age >= 18) {
    echo "Người lớn";
} elseif ($age >= 13) {     // Chú ý PHP viết liền elseif
    echo "Thiếu niên";
} else {
    echo "Trẻ em";
}

// Vòng lặp
for ($i = 0; $i < 5; $i++) {
    echo $i;
}
```

---

## 4. Collections (Mảng — Trái tim của PHP)

Kiểu Array của PHP cực kỳ linh hoạt (Nó vừa là List, Vừa là HashSet, Vừa là Map/Dict).

```php
// Mảng tuần tự (Indexed Array)
$fruits = ["Táo", "Cam", "Chuối"]; // PHP 5.4+ dùng [] thay vì array()
$fruits[] = "Nho";                 // Cách Nhanh nhất đẩy (Push) 1 phần tử vào cuối.
echo $fruits[0];                   // Táo

// Mảng kết hợp (Associative Array) = Tương đương Map / Dict
$user = [
    "id" => 1,
    "name" => "Nguyễn Văn A",
    "roles" => ["admin", "editor"]
];

echo $user["name"];

// Duyệt mảng Foreach cực tiện
foreach ($user as $key => $value) {
    // $value nếu là Mảng thì phải dump nó ra
    echo "$key: " . (is_array($value) ? implode(',', $value) : $value) . "\n";
}
```

---

## 5. OOP (Lập trình Hướng đối tượng)

PHP là ngôn ngữ Hướng Đối Tượng chuẩn (Rất giống Java).
Các từ khóa `class`, `public`, `private`, `protected`, `interface`, `trait` đều có đủ.

```php
class Animal {
    private string $name;
    
    // PHP 8+: Constructor Property Promotion (Viết tắt khai báo tham số tự gán vào thuộc tính)
    public function __construct(private int $age, string $name) {
        $this->name = $name; // $this là con trỏ chỉ vào chính class 
    }

    public function speak(): string {
        return "Tôi là {$this->name}, {$this->age} tuổi.";
    }
}

class Dog extends Animal {
    public function bark(): string {
        return "Gâu gâu! " . $this->speak();
    }
}

$dog = new Dog(5, "Rex"); // Khởi tạo bằng lệnh `new`
echo $dog->bark();
```

---

## 6. Xử lý Lỗi (Error Handling)

PHP phân chia rõ Exception (Lỗi có thể xử lý) và Error (Lỗi hệ thống). PHP 7+ gom cả 2 vào chung Interface `Throwable`.

```php
try {
    $db = new PDO("mysql:host=localhost;dbname=test"); // Cố nối DB
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    // Tính toán mạo hiểm
    $res = 10 / 0; 
} catch (DivisionByZeroError $e) { // Bắt đích danh loại Lỗi (PHP 8)
    echo "Lỗi toán học: " . $e->getMessage();
} catch (\Throwable $e) {      // Backtick \ để gọi Interface gốc ở Root namespace
    echo "Lỗi chung chung: Loi CSDL hoặc Code"; // Log lại
} finally {
    echo "Luôn chay qua dòng này (Thường để Cleanup resource)";
}
```

---

## Gotchas — Những Lỗi PHP hay gặp

| # | ❌ Cú pháp Cũ / Lỗi Sai | ✅ Cú pháp Đúng / Hiện đại | Hậu quả của Việc Làm Sai |
|---|--------|---------|------------|
| 1 | Dùng `==` | Dùng `===` | `0 == "0"` là True, `0 == "a"` là True (PHP < 8). PHP tự ép dấu siêu ảo ma gây ra các bug logic bảo mật rất chết người. Dùng `===` để so sánh CẢ Kiểu. |
| 2 | Code SQL thô bạo: `query("SELECT * FROM u WHERE id=$id")` | Dùng Data Binding chuẩn: `$stmt = $pdo->prepare("SELECT * FROM u WHERE id=?"); $stmt->execute([$id]);` | Dẫn thẳng tới lỗ hổng kinh điển lộ Toàn bộ Data Web: Lỗi **SQL Injection**. Tuyệt đối không nhét mảng/biến String sống vào SQL. |
| 3 | Không dùng `namespace` ở đầu File. | Khai báo `namespace App\Models;` chuẩn nếp PSR-4. | Trùng lặp tên Hàm `function add()` trùng với Hàm thư viện người ta tạo -> Web dập báo lỗi Fatal Redeclare. |
| 4 | Cấu hình máy chủ cài Web tĩnh Nginx mà quên FPM | Phải cài và nối FastCGI `php-fpm` vô Nginx. | Lướt URL trang thấy Hiện nguyên vẹn cái màn hình chứa Code gốc PHP Passwords Data thay vì xuất ra HTML. |

---

## Bài tập Thực hành Nhập môn

- [ ] **Bài 1 (Dễ):** Viết script in ra bảng cửu chương từ 1 đến 9 sử dụng vòng lặp `for` nén lồng nhau.  
- [ ] **Bài 2 (Trung bình):** Xây dựng một Class `User` lưu Mảng `[]` các `Task`. Có hàm thêm Task, hàm hoàn thành Task (Đánh giấu cờ `completed = true`). Móc vào `foreach` in Menu ra Console `echo` như Todo App.
- [ ] **Bài 3 (Khó):** (I/O Cơ bản) - Ghi một mảng PHP thành JSON và save vào file hệ thống bằng lệnh `file_put_contents`. Tiếp tục, đọc lại JSON đó thông qua cờ giải mã Mảng Hỗn Hợp bằng `json_decode(file_get_contents(), true)`. 

---

## Tài nguyên Mở rộng
- [PHP Khóa học (PHP The Right Way)](https://phptherightway.com/) - Sách thánh của lập trình viên PHP. Bật mí mọi quy tắc Framework hiện đại nhất.
- [Hệ sinh thái Composer](https://getcomposer.org/) - Package Manager độc nhất của PHP mà bạn BẮT BUỘC RẤT CẦN thiết phải hiểu (Chứa hàng triệu thư viện Laravel rải ở Packagist).
- [Laracasts](https://laracasts.com/) - Nền tảng video học Laravề và PHP gốc cực xịn xò với thầy Jeffrey Way.
