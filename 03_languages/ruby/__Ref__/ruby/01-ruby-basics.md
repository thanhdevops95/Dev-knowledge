# 💎 Ruby Basics — Nhập môn Ruby

> `[BEGINNER]` — Prerequisite: Không có.
> Ngôn ngữ được thiết kế để tối ưu hóa "sự hạnh phúc của lập trình viên" (Developer Happiness). Cực kỳ thanh lịch và linh hoạt.

---

## Tại sao (WHY) lại dùng Ruby?

Ruby là ngôn ngữ hướng đối tượng thuần túy (mọi thứ đều là object). Cú pháp của Ruby đọc giống hệt tiếng Anh, không yêu cầu dấu chấm phẩy và dấu ngoặc nhọn ở khắp nơi. Framework Web nổi tiếng nhất của nó là **Ruby on Rails** đã định hình khái niệm MVC hiện đại cho tới nay (Kể cả Laravel, Django đều học tập theo Rails).

**Vấn đề giải quyết:** Xây dựng logic Server Backend (Web App / Scripts) và Tooling một cách nhanh chóng với số dòng code ít nhất có thể.

**So sánh nhanh:**
| Tính năng | Ruby | Python | PHP |
|---|---|---|---|
| **Cú pháp** | Linh hoạt, đọc như tiếng Anh tự nhiên | Strict, dùng lùi lề (Indentation) | Giống C/C++, bắt đầu biến bằng `$` |
| **Hệ sinh thái** | Rails là ông vua Web | Data, AI, Scripts | Web-SSR (WordPress, Laravel) |
| **Triết lý** | TIMTOWTDI (Nhiều cách làm một việc) | Dấu cách thống nhất 1 cách làm | Thực dụng, Copy \u0026 Paste |

---

## 1. Cài đặt môi trường

Tuyệt đối không nên cài Ruby bằng công cụ package mặc định của OS (như `apt` hay `brew` gốc) vì nó sẽ can thiệp vào Ruby Hệ thống do HĐH quy định. Hãy dùng Version Manager.

**Cài đặt:**
- **macOS/Linux**: Cài `rbenv` (hoặc `rvm`). 
  ```bash
  # Tải bằng brew 
  brew install rbenv
  
  # Liệt kê ver
  rbenv install -l
  rbenv install 3.3.0
  rbenv global 3.3.0
  ```
- **Windows**: [RubyInstaller](https://rubyinstaller.org/).

Kiểm tra:
```bash
ruby -v
irb       # Khởi động Ruby Interactive Shell (Cực xịn để test Lệnh nhanh)
```

---

## 2. Hello World

Tạo file `hello.rb`:
```ruby
# hello.rb
puts "Hello World"          # In ra kèm tự xuống dòng (\n)
print "Hello "              # In ra Không xuống dòng
p "World"                   # In ra chính xác Format cho Debugger ("World" có nháy)

name = "Aki"
puts "Chào mừng bạn #{name}!" # Rất giống JavaScript Template String
```

Chạy file:
```bash
ruby hello.rb
```

---

## 3. Biến, Cú pháp cơ bản & Blocks

### Biến và Kiểu dữ liệu (Tất cả là Object!)

Trong Ruby, Số `1` cũng là một Đối Tượng, có phương thức riêng. Không có kiểu nguyên thủy.

```ruby
age = 25              # Số nguyên (Fixnum)
pi = 3.14             # Float
name = "Bình"         # String

# Symbol — Siêu đặc thù của Ruby (Biểu thị bằng dấu hai chấm trước)
# Nếu bạn tạo 10 string "error", Ruby tốn Memory 10 chỗ.
# Nhưng :error (Symbol) chỉ duy nhất 1 Ô NHỚ tiết kiệm CỰC KỲ, dùng rất nhiều với Hashes.
status = :active     

# Gọi phương thức của Số (Vì nó là Object/Class)
puts 5.even?      # false
puts 5.next       # 6
```

### Điều khiển Luồng (If / Unless)

```ruby
age = 15

if age >= 18
  puts "Người lớn"
elsif age >= 13     # LƯU Ý LÀ elsif (Viết liền, không có chữ e thứ 2)
  puts "Mới lớn"
end

# Sự thanh lịch của Ruby: Viết If một dòng ngược ở đằng sau (Postfix If)
puts "Bạn được uống Bia" if age >= 21

# Unless (Thay vì if !condition làm não rối)
unless age >= 18
  puts "Cấm Vô! Chỉ dành cho Trên 18"
end
```

### Triết lý Trọng tâm Ruby: BLOCKS

Block là linh hồn của Ruby. Block gom nhóm một khối Code `do ... end` và ném thẳng khối lệnh đó vào Hàm để Chạy Thay Cho Vòng Lặp.

```ruby
# Vòng lặp For kiểu truyền thống RẤT ÍT dùng ở Ruby
for i in 1..5 do
  puts i
end

# ✅ Các lập trình viên Ruby CHUẨN dùng Block gọi phương thức .times() hoặc .each()
5.times do |i|
  puts "Anh yêu em lần thứ #{i}"  # Chạy 5 lần!
end

# Lặp qua mảng Collection
["Táo", "Cam", "Chuối"].each do |qua|
  puts qua
end

# Cú pháp ngắn nếu khối lệnh do ... end chỉ có 1 dòng dùng `{ }`
3.times { |i| puts "Ngắn gọn #{i}" } 
```

---

## 4. Collections (Arrays & Hashes)

```ruby
# ===== Array (Mảng Động) =====
words = ["A", "B", "C"]
words.push("D")       # Thêm vào cuối 
words << "E"          # Toán tử Shovel siêu cưa (Nhanh và rất Cool, Y Chang Push)

# API Map (Select) Trả Về Mảng Mới biến Lỗi thành Số
numbers = [1, 2, 3]
squares = numbers.map { |n| n * n } # [1, 4, 9]

# Tìm Kiếm Chắt Kỹ (Select) = Array.Filter ở JS
evens = numbers.select { |n| n.even? } # Lấy Số chẵn


# ===== Hash (Từ Điển / Map / Object) =====
user = {
  "name" => "Nam",    # Key là String
  "age" => 20
}

# Tuy nhiên, Hash chuẩn hiện đại DÙNG SYMBOL tiết kiệm và đẹp mắt hơn:
config = {
  host: "localhost",  # (Hiểu Rút Gọn của :host => "localhost")
  port: 3306
}

puts config[:host]    # Cách đọc ra Value localhost
```

---

## 5. OOP (Lập trình Hướng đối tượng)

Ruby thiết kế OOP Cực Kì nghiêm khắc ẩn Mọi Biến Gốc thành tính Đóng Gói (Private). Bạn chỉ tương tác với Biến ngoài qua các phương thức lộ ra (Setter / Getter). Tuy nhiên có Cú pháp rút gọn.

```ruby
class Person
  # Tự động Generate (Getter) và (Setter) tương ứng cho Biến Private bên dưới
  attr_accessor :name, :age 

  # Dấu @ ám chỉ Thuộc Tính của Class / Instance Variable (this.)
  def initialize(name, age) # (Hàm Construct Khởi Tạo)
    @name = name
    @age = age  
  end

  # Phương thức Class (Trả về Chuỗi Cuối Cùng, KO CẦN chữ return)
  def introduce
    "Xin chào, tôi là #{@name}" # Chữ Dòng Cuối Tự Ngầm Trả Về Hàm
  end
end

user = Person.new("Hùng", 25)
user.age = 26 # Gõ .age có ngay Setter/Getter tạo sẵn qua Accessor 
puts user.introduce
```

Chữ `return` ở cuối Hàm trong Ruby có thể được Mặc Định Lược Bỏ (Implicit Return). Ruby tự ngầm định gán Câu Lệnh chạy ra kết quả Cuối Cùng là Kết Quả Xuất Hàm.

---

## 6. Xử lý Lỗi (Exceptions)

```ruby
begin
  # Bắt đầu Đoạn Nguy Hiểm
  puts 10 / 0
rescue ZeroDivisionError => e # Bắt Đích Nhắm 
  puts "Lỗi tính toán: #{e.message}"
rescue StandardError => e     # Bắt Chuẩn Lỗi Chung
  puts "Lỗi lạ"
ensure
  puts "Chạy Cho Cùng Trời Cạn Đất Dù Code Bể Chìm - Để Đóng Resource"
end
```

---

## Gotchas — Những Lỗi Hay Gặp 

| # | ❌ Tránh (Sai Làm Đau Đầu) | ✅ Cần (Khắc Phục Chuẩn) | Hậu quả của Việc Làm Sai |
|---|--------|---------|------------|
| 1 | Khởi tạo 1 Chuỗi liên tục String: `a = "Chào" \n a << "Bạn"` trong Vòng lặp. | Phải hiểu String dùng Ô nhớ Heap độc lập liên tiếp, Lặp sinh ra Rác GC. | Tốn GBs Ram. Nên dùng Mảng đẩy Chuỗi sau rồi cuối dùng `.join` |
| 2 | Code vòng lặp theo phong cách `for i in 0...arr.length` quen tay theo Python/C. | Viết `arr.each do \|item\|` / `map/select`. | Khiến bạn không tận dụng API cao cấp Array (Idiomatic Ruby), Code nhát, Lỗi tràn viền OutOfIndex. |
| 3 | Sửa Mảng Mốc (Gốc) lúc Duyệt Bằng `.each`. | Tuyệt tối dùng Lọc Copy Mảng ra ngoài `.select`. | Văng Đủ Thể Loại Lỗi Nil vì độ dài Mốc Rớt do Trừ Đi 1. |
| 4 | Lầm Tưởng `return` Bật Ra Khỏi Iterator Lặp qua Block `map/each`. | Dùng lệnh Ngắt ngang Vòng lặp của Method Iterator là `next` (tiếp tục) hoặc `break` (ngừng). | Nó làm gãy (Crash Block Hàm mẹ cha) nếu Quăng `return` Lên Đời Cao. |

---

## Bài tập Thực hành

- [ ] **Bài 1 (Dễ):** Tạo 1 file in số lẻ (Sự kết hợp: `50.times` với `.odd?` của Số Object).  
- [ ] **Bài 2 (Trung bình):** Xây dựng Mảng Danh sách Từ Điển `Hash` lưu 5 Xe Cộ (Màu Sắc `:color`, Hãng Xe `:brand`). Gọi thủ thuật `Array.each` hoặc `select`. In ra Hãng Xe Chỉ Của Màu Đỏ.
- [ ] **Bài 3 (Khó):** (Hệ Thống Lớp Kế Thừa). Chạy Class Shape chứa Diên Tích bằng 0. Class `Rectangle` (Chữ nhật) nhận `@width`, `@height` và hàm Mở Rộng Kế Thừa Của Nó Override Lại Diện Tích Trả Hàm. Gọi Chạy Instance `new` ra Xem Lại Chuẩn Output.  

---

## Tài nguyên Mở rộng
- [Ruby in 20 Minutes](https://www.ruby-lang.org/en/documentation/quickstart/) - Cẩm nang 20 phút chạy gốc Trang Chủ Cực Xịn Xò.
- [Ruby Koans](http://rubykoans.com/) - Luyện Code Ruby theo Thiền Giác Ngộ (Chạy test liên tục cho não linh hoạt syntax).
- [The Ruby Programming Language](https://www.oreilly.com/library/view/the-ruby-programming/9780596516178/) - Sách Mộc Bản Của Matz (Cha Đẻ của Ruby. Kinh Thư Căn Bản Tốt Nhất Mọi Thời Đại).
