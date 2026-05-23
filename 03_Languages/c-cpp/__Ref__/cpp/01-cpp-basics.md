# 🚀 C++ Basics — Nhập môn C++

> `[BEGINNER]` — Prerequisite: Hiểu sơ lược về Biến và Hàm (Biết C là một lợi thế).
> Ngôn ngữ cội nguồn của mọi tựa game AAA. Mang sức mạnh bão táp kiểm soát sát phần cứng của C, nhưng cộng thêm hệ thống Lập trình Hướng đối tượng (OOP).

---

## Tại sao (WHY) lại dùng C++?

C++ là sự tiến hóa của C ("C with Classes"). Nó cấp cho lập trình viên quyền kiểm soát vùng nhớ bộ RAM ở mức độ cực đoan (Zero-cost abstraction) đồng thời cung cấp kiến trúc tổ chức code OOP để chịu được các dự án quy mô ngàn triệu dòng.

**Vấn đề giải quyết:** Viết HĐH (Windows/Linux components), Hệ quản trị Cơ sở dữ liệu, Trình duyệt Web (Chrome V8/Blink), và Làm Game (Unreal Engine). Đòi hỏi hiệu năng Micro-seconds.

**So sánh nhanh:**
| Tính năng | C++ | C | Java / C# |
|---|---|---|---|
| **Hiệu năng** | Đỉnh cao, sát kim loại | Đỉnh cao | Rất nhanh nhưng vướng rác rác (GC) |
| **Quản lý bộ nhớ** | Tự cấp phát & giải phóng thủ công (Manual) | Chạy tay 100% | Máy ảo tự động Dọn rác (GC) |
| **Công cụ (Tooling)** | Khá đau đầu (CMake, Makefile) | Cổ điển (Make) | Rất ngon (NuGet, Maven) |

---

## 1. Cài đặt Môi trường (Trình biên dịch & IDE)

C++ là ngôn ngữ **Biên dịch** (Compiled Language). Code của bạn sẽ được dịch một lần ra mã máy Nhị phân (`.exe` hoặc `.out`) chạy trực tiếp trên CPU tương ứng.

**Cài đặt qua Command Line:**
- **Windows:** Cài đặt Visual Studio (Bản xịn của Microsoft) và chọn "Desktop development with C++", hoặc tải bản `MinGW`.
- **macOS:** 
  ```bash
  xcode-select --install # Cài bộ Táo Apple LLVM Clang
  ```
- **Linux:**
  ```bash
  sudo apt install build-essential # Chứa g++ compiler
  ```

Kiểm tra:
```bash
g++ --version
```

---

## 2. Hello World! & Biên dịch

Cấu trúc một file C++ kinh điển. Điểm vỡ lòng: Không có Thư viện chuẩn (C++ Standard Library) thì C++ chẳng in ra được gì.

Tạo file `hello.cpp`:
```cpp
// Thư viện Input/Output Chuẩn (Bắt buộc để xài lệnh in)
#include <iostream> 

int main() {
    // std (Standard) là Vùng không gian tên. 
    // cout = Character Out (Xuất Chuỗi). endl = End Line (Xuống dòng).
    std::cout << "Xin chào C++ Thế Giới!" << std::endl;
    
    // Mọi chương trình chuẩn C/C++ trả về 0 để báo Hệ Điều Hành là Chạy Trơn Tru.
    return 0; 
}
```

**Biên dịch & Chạy chay (Console):**
```bash
g++ hello.cpp -o hello_app.exe  # Lắp Dịch
./hello_app.exe                 # Chạy Mở File Mã Máy (Siêu Tốc Độ Ánh Sáng) 
```

---

## 3. Biến, Vòng lặp & Kiểu Dữ liệu

```cpp
#include <iostream>
#include <string> // C++ Tách Biệt String Ra 1 Khối Thư Viện Chứ Ko Phải Chuẩn Rễ

using namespace std; // MẸO RÚT GỌN (Giúp gõ cout thay vì std::cout dài mỏi tay)

int main() {
    // 1. Khai báo (Kiểu gõ TĨNH Ngặt Nghèo)
    int age = 22;
    float pi = 3.14f;
    bool isDev = true;

    // String của C++ Cực kỳ phức tạp (Nó là cái Cốc Bọc Mảng Chữ Kí Tự Phía Trọng C)
    string name = "Chiến Thần"; 

    // Vòng lặp For 
    for(int i = 0; i < 5; i++) {
        cout << "Lặp " << i << " | ";
    }

    return 0;
}
```

---

## 4. Đặc Đặc Sản Nổi Cộm: Con Trỏ (Pointers) & Tham Chiếu (Reference)

Là Khủng hoảng Bất Tận Của Sinh Viên IT Toàn Cầu. 
Ở các ngôn ngữ Bậc Cao, Biến LƯU GIÁ TRỊ. Ở C/C++, **Con Trỏ LÀ BIẾN LƯU GHI ĐỊA CHỈ Ô NHỚ RAM KHÁC**.

```cpp
int main() {
    int diem_so = 10;
    
    // -- CON TRỞ (Thêm sao *) --
    // '&' Toán Tử lấy Địa Chỉ Nhớ Của Thằng Biến diem_so (Ví dụ 0x2af3)
    int* pointer_diem = &diem_so; 

    cout << pointer_diem;  // In ra Ô Nhớ: 0x7ffd19...
    cout << *pointer_diem; // In Rút Gọi Về Mốc Mái Giá Trị Ô Ấy Chỉ Tới (Dereference) -> 10.

    // -- THAM CHIẾU (Thêm & đằng sau Loại Kiểu Dữ Liệu ở Tên Khai Báo Biến) --
    // Sinh ra để Viết Thay Dấu * Gây Đau Não Đọc Rối Sớm (Giống Đặt Bí Danh Bí Nick Sang Thẳng Mốc Gốc Không Sao Chép Mới Mảnh Dữ Bản Khác).
    int& alias_diem = diem_so; 
    alias_diem = 100; // Thay Bí Danh Gốc -> Biến Gốc Cực Tăng 

    cout << diem_so; // GIỜ 100 RỒI ĐẤY 
}
```

---

## 5. Mảng (Array) & Siêu Mảng Chuẩn STL `std::vector`

Mảng nguyên gốc `int arr[5]` cực kì RÁC vì nó Cứng Ngắc, Phải Gõ Số Size Ban Đầu và Rất Đau Thương Khi Vượt Biên. Thay cất Cút Khỏi Nó. **HÃY DÙNG `vector` LÒNG C++ STL CHUẨN**.

```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() {
    // Mảng Vector Co Giãn Lò Xo Gốc Đội RAM Tự Động Rất Êm 
    vector<int> danh_sach = {1, 2, 3};
    
    danh_sach.push_back(4); // Đuốc Biển Bơm Vô Ngay Cuối
    
    // Vòng lặp C++ Phiên Bản Code Cập Theo Nghĩa Mật Mới Thảo Nguyên Dễ: (Range-based for)
    for(int so : danh_sach) {   
        cout << so << " ";
    }
}
```

---

## 6. Lập Trình Hướng Đối Tượng & Nhớ (Memory Rác)

Điểm Tác Lớn Của Các Hạng Đỉnh Là Tính Xây Class (Kế Thừa Nhiều `Multiple Inheritance` - Thứ Mọi Thằng Con IT Khác Trối Bỏ Bớt Thay Cắt Vì Nhức Rối Giăng Chéo).

```cpp
#include <iostream>
using namespace std;

class Animal {
private:
    string thong_tin_bi_mat_giau_kin; 

public:
    string Name;

    // Constructor Khởi Bộ Hàm
    Animal(string name) {
        Name = name;
        cout << "Động vật Sinh Ra Nè!" << endl;
    }

    // Tội Oán Chống Chạy Ngầm Tràn Rác Mát (Destructor Hàm Hủy Lúc Thoáng Đứt Đập Cát Bụi Đời Object)
    ~Animal() {
        cout << "Nó Chết Rồi!" << endl;
    }
};

int main() {
    Animal dog("Rex Dũng"); 

    // CHÚ GIẢI THỰC TẾ: Bắn Ra Dấu New Gọi Hàm RAM Phân Ra Heap Riêng (Dạo Lấy Dynamic Memory Rỗng Máy)
    Animal* cat = new Animal("Mèo Đen Khoang");
    
    // KẾT ĐỨT ẢO LỤC NGU VỚ CHIẾC LỖI TỨ CHỨNG:
    // NẾU BẠN KHÔNG GỌI DẤU DELETE LÊN THẰNG CON TRỎ NEW NÀY KHI ĐÓNG APP: BỘ NHỚ RAM BẠN MẤT TRẮNG CHO TỚI LÚC TẮT MÁY (Memory Leak)
    delete cat; 
}
```

---

## Gotchas — Bẫy Nên Chôn Rấp Cẩn Khoanh Nấp Phải Không Để Hố Bug Ngầm

| # | ❌ Cú Pháp Tư Chặn Gặp (Lỗ Tử Tiếc Đau) | ✅ Phá Bản Thay Phương Diện C++ Mới | Hậu quả Cẩu Hưởng Máu Rớt Tụt Trình Chạy |
|---|--------|---------|------------|
| 1 | Cứ Nhè Nối Cắm Viết Viết Lệnh `new` Mọi Nẻo Nặn Lấy Hàm Đối Và Đẩy Tay Kèm File Nhớ Gọi Hộ Bằng Mức Xóa Cho RAM Hư Thuộc `delete`. | Dùng Sạch Dấu Nhóm Giữ Ngai Độc Nhất Nhớ Đi Kèm Nét Xóa Rửa Tư Động Rỗng (Của Khung Gói C++11 Trở Căng Tái Hiện Sạch Gọi Thông Sinh Rác Rễ `std::unique_ptr`). | Đi Khỏi Lỗi Vi Quãng Báo Treo Nạp Full Thẻ Cháy Máy Ram Chóng Văng Do Tràn Bộ Nhớ App Web (Mã Kéo Lệnh Nổi Ngang Chặn Hủy Ko Bao Tới Tầng Dọn Rác Rơi Nước Chót Kèo Đi Đứng Gáy Khục Tít Lỗ Memory Leak). |
| 2 | Kẹt Trái Trọng Chui Tham Thường Vết Vòng Cho Struct (Object List Bền To Nặng Cân Mấy Chục KB Data Gửi Truyền Sốt Một Số Đòi Sang Kế Function Sát Bên). `void send(User u)` | Nén Trỏ Phỏng Sát Cạnh Gắn Vào Lượng Không Biến Hóa Địa Copy Thấy (Tham Giá Không Quyền Chạm Phá Constant Viết `void send(const User& u)`). Kẻ Cột Mối Bí Ngầm Qua Không Xáo Chép Code RAM Phẳng Nét Dính. | Nếu Cực Viết Nhẹ Giá Mảng Object Data 20MB Trăm Lượt Sẽ Tự Sắp Khung Nhét Sạch Nhát Coppy Data Qua Miệng Rìa RAM Tốn Lặp Đút Cho Máy Trắng Load Rớt Cột Chóp Chạm Trục Frame Dây. Tụt 0 Tốc Văng Gãy Mỏi. |

---

## Bài tập Làm Bàn Thúc Luyện Oái Tỉnh Táo C+ Đầu Chóp

- [ ] **Bài 1 (Khởi Tạo Dễ Cân Dài Số Nhỏ Nắm):** Làm Vector Dọc Ghi Chứa List Tên Học Sinh Ráp Gọi Lệnh Push Tên Bỏ "Nam". For Kiểu Quét Nhặt Tới Cuối Danh Bằng Vòng (`for(string t : vec)`). Đi Sóng Dòng Gọi `cout` Sổ Ra Kèm Dấu `endl`. Giữ Rất Bình Vòng Lượt In.  
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Chơi Tính Rõ Gọi OOP Có Thuế Hủy):** Nắm Một Lõi Quản Nhớ Sinh Class Ô Đựng Lính `Hero`. Góp Tầm Một Trỏ Mã Trống Dynamic New Thuộc Số Trong Ngực (Làm Lúc Construct Nộp Vào Gán Thẳng Mớ New). Rập Test Khẳng Nếu Có Hủy Ghi Dấu Câu In Biển Báo Ở Đáy Thấu Destructor Bứt Hàm `~Hero() Đã Thu Kiếm`. Chạy Ở Mạch Biển Khúc Đoạn Hàm Dưới (Main Tự Khúc Xong 1 Instance Hết Ngay Gọi Thu Xem Lệnh Mệnh Ngự Không Bật Cửa Lỗ Của Hàm Hủy Tự Oạch Xóa ).  

---

## Tài nguyên Đọc Sâu Vun Chắp Cánh Tôn Kiếm Đốc Giáo Ngôn Thượng C++ Giới Đạo

- [Khối Khung Rễ Lớn Tới Tất Nền Hợp Bộ Tóm Rõ Chi Tiết Reference Ngành CPP Toàn](https://en.cppreference.com/w/) - Thánh Kinh Wiki Tóm Chi Đóng Dấu Đều Khổ Viết Sát Mới Nhất Quặn Trọng Nhất Chuẩn Quốc ISO C++.
- [Trang Chủ Nắm Điệu C++ Của Thầy Tổng Microsoft Docs Đập Cho Tốt Khung Mã Vi Windows (Cực Nhuần C++ Ráp Tỉ Lõi)](https://learn.microsoft.com/en-us/cpp/?view=msvc-170) - Rót Nghĩa Cặn Góc Ngồi Viết C++ Gắn Studio Chuẩn Bài Nghề Nghiệp Khổ Luyện Code System Thắt Ống Thâm Ảo Giữa Lỗi Linker Sâu Vàng Tới Tới Code Đi Tách Nhanh Mạch Phát Bội Kênh Hướng Dẫn Kéo Lên Trẻ Tới Đi.
