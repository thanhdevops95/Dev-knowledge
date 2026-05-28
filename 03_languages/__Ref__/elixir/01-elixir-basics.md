# 💧 Elixir Basics — Nhập môn Elixir

> `[BEGINNER]` — Prerequisite: Không có (Biết đôi chút về FP là một lợi thế).
> Ngôn ngữ Lập trình Hàm (Functional Programming) hiện đại, chạy trên máy ảo Erlang (BEAM). Chuyên gia xử lý tính toán đồng thời (Concurrency) và chịu lỗi (Fault-tolerance).

---

## Tại sao (WHY) lại dùng Elixir?

Elixir thừa hưởng toàn bộ sức mạnh công nghiệp hệ thống viễn thông 30 năm của Erlang nhưng mang hình hài cú pháp thanh lịch học hỏi từ Ruby. Thay vì sợ hãi khi chương trình lỗi (Exceptions), triết lý của Elixir là "Let it crash" (Cứ để nó sập đi) và tự động hồi sinh phần lỗi ngay lập tức mà không làm ảnh hưởng phần còn lại của hệ thống.

**Vấn đề giải quyết:** Xây dựng hệ thống chat realtime (Discord), streaming đa luồng, IoT, thiết kế ứng dụng web siêu mượt bằng Phoenix Framework, đòi hỏi uptime lên tới 99.9999%.

**So sánh nhanh:**
| Tính năng | Elixir | Ruby | Go |
|---|---|---|---|
| **Môi trường** | Máy ảo BEAM (Erlang) | Trình thông dịch Ruby | Biên dịch mã máy Native |
| **Concurrency** | Hàng triệu Tiến trình cô lập siêu nhẹ (Actor Model) | Thiết kế chặn (Blocking/GIL) | Goroutines (CSP) |
| **Mẫu dữ liệu** | Hoàn toàn Bất biến (Immutable) & FP | Hướng Đối Tượng (OOP) | Hướng Cấu Trúc Thủ Tục |

---

## 1. Cài đặt Môi trường (BEAM VM)

Vì Elixir chạy trên máy áo BEAM (Erlang VM), bạn cần cài Erlang trước tiên hoặc dùng package gộp.

**Cài đặt:**
- **macOS:** 
  ```bash
  brew install elixir
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt install erlang elixir
  ```
- **Windows:** Tải file Installer `.exe` từ web [elixir-lang.org](https://elixir-lang.org/install.html).

Ngay lập tức, bạn sẽ có bộ ba công cụ phép thuật cốt lõi:
1. `elixir` (Dùng chạy file `.ex`)
2. `elixirc` (Trình biên dịch file)
3. `iex` (Interactive Elixir - Shell màn hình console siêu xịn xò)

Kiểm tra:
```bash
elixir -v
iex       # Gõ để vào Shell REPL viết code Elixir ngay tại lệnh
```

---

## 2. Hello World! & Sự Bất biến Dữ liệu

Kịch bản `hello.exs` (đuôi `.exs` là file Script sẽ không được biên dịch ra Bytecode tĩnh, chỉ chạy thẳng):

```elixir
# Mọi lệnh in trên màn hình dùng cú pháp tương tự C/Ruby
IO.puts("Xin chào Elixir!")

# 1. Bất biến (Immutability) 
# -- Ở Elixir, MỌI DỮ LIỆU ĐỀU KHÔNG THỂ BỊ THAY ĐỔI SAU KHI TẠO
list = [1, 2, 3]
new_list = list ++ [4, 5] # Chép ra 1 Vùng Nhớ Toàn Vẹn Khác

IO.inspect(list)       # [1, 2, 3] Rõ ràng Mảng List Gốc Vẫn Y Nguyên
IO.inspect(new_list)   # [1, 2, 3, 4, 5]

# Mặc dù ta gán = Mới, Cả Dữ Liệu không biến Hóa bên Dưới. Cái Ta Gán Chỉ Là Đổi Tên Gắn Cái Nhãn (Rebind Biến).
list = ["Mới", "Lại"] 
```

---

## 3. Khớp Mẫu (Pattern Matching) Cực Bá Đạo Vô Vàng Bậc Nhất

Ở đa số ngôn ngữ, dấu `=` là Toán tử Gán (Assignment). Còn ở Elixir, dấu `=` là **Toán Tử Khớp (Match Operator)** (Giống học Đại Số Toán Học lớp 8).

```elixir
# x bằng 1 -> Hợp lý
x = 1

# Ngược lại 1 bằng x -> NẾU LÀ C/Java sẽ báo "Lỗi cú pháp". Nhưng Elixir TRẢ VỀ CHUẨN ĐÚNG! 
# Vì cả 2 vế hoàn toàn Cân Bằng.
1 = x  // OK

# Lấy 1 Chùm Tháo Rỡ Mảng Nhanh: Khớp cả Mảng Vừa Tạo.
[a, b, c] = [10, 20, 30]
IO.puts(a) # In 10

# Bắt Đầu Khớp Lệch Dữ Liệu Sẽ Lỗi Liền Ngay
# [a, b, 20] = [10, 20, 30] // LỖI CRASH (MatchError) Vì Không Khớp Nhau 20 = 30 Đâu Cả!
```

---

## 4. Tẩu Mạch Phép Thuật Toán Tử Ống (Pipe Operator `|>`)

Bạn có muốn nhét kết quả của hàm này Thành Tham Số Hàm Khác Mà không dội ngược não Đọc Mắc Cực Chồng Cục Không?

```elixir
# Code Xưa Bình Thường Hàm Bọc Nhau Trông Gớm Rối Mắt (Đọc Từ Trong Ra Ngoài)
ket_qua = IO.inspect(String.upcase(String.trim("  hello  ")))

# Kỹ Thuật Data Tẩu Ống Nổi Tiếng Của Riêng Elixir: `|>`
# -- Dòng chảy Lấy Chuỗi gốc | Tham Số Ném Liên Tiếp Thẳng Chuyển Đầu Cho Hàm Bọc Kế Vế Sau | Thành Chữ HOA | Bật In. (Đọc Từ Trái Qua Phải Tự Nhiên Tuyệt Đỉnh)
"  hello  " 
|> String.trim() 
|> String.upcase() 
|> IO.inspect()   # In Gọn Gàng Chữ Kìa: "HELLO"
```

---

## 5. Cấu trúc Control (If, Case, Cond)

```elixir
# Kiểu Thuần If / Else 
check_tuoi = if 25 >= 18 do
  "Bạn Lớn"
else
  "Thiếu Nhi Nữa"
end

# CASE - Bậc Thầy Pattern Matching Dòng Khớp Mạnh (Giống Match Của Rust, Scala, Lấy Thay Thế Switch)
ket_qua_danh = {:ok, "Tải Đã Xong Data"} # Đây Gọi Là Tuple Chứa Hạt Thông Tin Phổ Biến Nhất Thế Giới FP

case ket_qua_danh do
  {:ok, data} -> IO.puts("Tuyệt Thành Công, Nhét File Bằng Này Nhé: #{data}")
  {:error, _} -> IO.puts("Có Gì Trật Sai Văng Rồi Không Chịu Trách Nhiệm Chữ Tạm _ Bỏ")
  _ -> IO.puts("Mặc Định Xong Kệ Mọi Món Rơi Cạn Về Xó Catch All Bụi Này Đáy Default Này.")
end
```

---

## 6. Mô Đun và Hàm 

Không có khái niệm Class (Lớp Kế Thừa Hướng Đối Tượng) trong Elixir. Bạn nhét khối Function vào Modules là xong. 

```elixir
defmodule MathApp do
  # Hàm có Tên Gọi Ngoài Gọi Được Mọi Chỗ (Public)
  def cong(a, b) do
    a + b  # Dòng Tính Toán Hết Lệnh Tại Đáy Hàm Là Tự Cột Nhả Ngầm Kết Trả Giá Về (Lược Chữ Mất Implicit Return).
  end

  # Khai Ngắn Function Gọn Tiện Đánh Một Ròng Khép
  def nhan(a, b), do: a * b 
  
  # Hàm Con Đóng Khép Bên Góc Ẩn Dấu Private Không Gọi Góc Phụ (defp)
  defp luy_thua_lam_cung_trong(a), do: a * a 
end

# Khơi Biến Hàm Sài Nhé Nhẹ
IO.puts(MathApp.cong(5, 7)) # Xuất Ấn 12
```

---

## Gotchas — Nạn Sai Cách Ngay Đường Đầu 

| # | ❌ Cú Pháp Cũ Lạc Hậu Tội Kéo Lỗi Lệ | ✅ Code Tư Duy Hành Chức Trơn Trị Nét | Hậu quả Trọng Nhất Trắc Bug Rối Sai Đi |
|---|--------|---------|------------|
| 1 | Cố Sửa Nội Giá Trị 1 Struct Hoặc Vòng Mảng Thay Thuộc Tính Hàm Theo Tính Class Biến Lập. `user.id = 5` Xong Xuất Lỗ | Toàn Cuộc FP Là Bất Biến Nhé (Thuần Mới Tách Mọi Thay Cóp Khác Object Mới Map Toàn Lượng) `%{user \| id: 5}`. | App Hư Gãy Văng Bờ Error Cấm Phép Trắng Thâm Liên Code Của Máy Áo Giống Gỗ Vì Mọi Luồng Sạch Xuyên Lỗi Bật Rỗng Răng. |
| 2 | Nhồi Gọn Tính Hàm Dài Ngoẵng Hàm Gói Quặp Phụ Thuộc Tầm 4 Tầng Ngoặc Khó Đẻ Giữa Hàm Tham. Mắt Không Kịp Xem Rối Nùi Chữ Lồng Hàm Kép. | Áp Xài Dùng Biến Pipe Gắn Giấy Kênh Ống Nước Truyền `\|>`. Suối Trả Đắp Nhẹ Một Rò | Dòng Code Nùi Quanh Đoạn Hàm Sau Đổi Nghề 3 Tháng Không Cấu Trí Nổi Nước Người Đoạn Dev Sau Rối Căm Nuốt Sắp Rẽ Hàng Cũ Khủng Kiếp. |
| 3 | Lấy Tư Cứng Code Hàm Bắt Điều Viện Nổi Thật To Chẻ Lồng Ngắt Bằng `If` Chắn Điều Khoản Đi Liên Chút Kín Mảnh Logic Kiểm Nhiều Mức If Mệt Lắm Nhé. | Thẩm Mỹ Ngôn Nước Elixir Này Ưu Vị Quét Chồng So Thẳng Gọi Parameter (Function Clause Matching Overload) Các Module Case! So Khớp Lẹ Lùng Đầu Mã Đầu Rã Ngang Họng If Rác. | Cây Code If Kênh Cong Trì Viện Rã Nghẽn Nửa Trang Khối Block Chữ Nhận Biến Mỏi Đầu Não Code Bug Sót Logic Trường Hợp Gãy Hoàn Tường. |

---

## Bài tập Tự Gõ Luyện Thay Nếp Cũ Functional

- [ ] **Bài 1 (Khởi Tạo Dễ Thương Máu Nhập):** Khai Tập Vòng Danh Mảng (10 Bước `[1,2,3,4,5]`) Gọi Tấu Đầu Pipe `\|>` Ném Vào Luồng `Enum.map(&(&1 * 10))`. Lướt Đi Phép Vào Xong Đính Nốt `Enum.filter` Che Khớp Lấy Ngõ Tích Chẵn Cầm Bọc Tụ IO Gõ Chạy Ra Khẩu Khắp Console In Đủ Hàng Lên Động.
- [ ] **Bài 2 (Trung bình Map Khớp Module Cấu):** Đặt Làm Cầu Khối Struct Đơn Mảng Key `%{}` Để Giá Định Xe Mô Tổ Màu. Ánh Chạy Rê Tường 1 Hàm Nạp Rời Module (Match Pattern Nhận Điểm Nối Rõ Value `mau: "Đỏ"` Lên Trực Tiếp Parameters Đầu Vào Giữa Rắn) In Hí "Tìm Màu Tuyệt Đỉnh!" Xếp Phân Còn Trường Hàm Cặp Ngược Thả Nốt Xuất Hiện Chặn Nắp Kệ Cứ Hù Dấu Ra "Không Hề Cần."  

---

## Tài nguyên Đọc Sâu Mở Khoá Hơn Thách Thức Ngôi Code Đẹp

- [Trang Chủ Doc Chính Code Nôi Nắm Bản Official Lớn Sáng - Elixir-Lang Crash Run Mảnh Nền Tảng](https://elixir-lang.org/getting-started/introduction.html) - Trót Bài Chỉ Rìa Cơ Bản Lớp Đi Tốc Chạm Bách Trang Hướng Lượng Mầm Cứng Cự Đóng Khái Nguồn Đầu Gốc Tốt Đỉnh.
- [Elixir School Tiếng Viễn Du Nhẹ](https://elixirschool.com) - Mảnh Web Toàn Tri Thức Khuyên Gọn Xếp Thớ Tầng Level Luyện Các Bộ Nn Chăm Hàm Cao Tiên Bồi Tập.
- [Thinking in Elixir Hú Cõi FP Thoát Xác Nôi Java Lệ Chặn OOP Thói Gò Ách](https://thinkinginelixir.com/) - Kênh Gốc Giác Tư Duy Lệ Cứu Dân Xưa Thoát Bò Sang Functional Nhẹ Tuẫn Chuẩn Tiên Lọc.
