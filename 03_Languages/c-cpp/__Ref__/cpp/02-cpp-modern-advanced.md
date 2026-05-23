# ⚡ Modern C++ Deep Dive (C++11 đến C++20)

> `[ADVANCED]` — Prerequisite: Nắm vững con trỏ, tham chiếu và OOP ở bài `01-cpp-basics.md`.
> "Modern C++" (Từ C++11 trở đi) đã phẫu thuật thay máu hoàn toàn ngôn ngữ này. Nó an toàn hơn, tốc độ cao hơn, và ít lỗi (Memory Leaks) hơn gấp 100 lần.

---

## 1. Kỷ nguyên của Con trỏ Thông minh (Smart Pointers & RAII)

Vấn đề lớn nhất của C++ cơ bản là lập trình viên thường dùng `new` để cấp phát nhưng QUÊN DÙNG `delete`, dẫn tới rò rỉ RAM (Memory Leak). Giờ đây, trong Modern C++, lệnh `new/delete` thô gần như đã BỊ CẤM trong các công ty lới (Trừ phi viết Engine dưới cùng).

Thay vào đó, bạn sử dụng **Smart Pointers (Con trỏ thông minh)**. Bản chất của nó là nguyên lý **RAII** (Lấy cấp phát làm khởi tạo): Tự động dọn dẹp RAM khi đi ra khỏi ranh giới hàm (Scope `}`).

### A. std::unique_ptr (Sở hữu tuyệt đối 1-1)
Được sử dụng 90% thời gian. Một Ô Nhớ (Cái Bánh) chạy trên RAM chỉ được phép thuộc về 1 `unique_ptr` Chủ Nhân duy nhất. Tính Mượn Đóng Chặt. Tốc độ NGANG BẰNG con trỏ thô (Raw pointer).

```cpp
#include <memory>
using namespace std;

class XeHoi {
public:
    XeHoi() { cout << "Xe Ra Mắt" << endl; }
    ~XeHoi() { cout << "Xe Tự Động Vào Bãi Phế Liệu Lọc Xóa" << endl; }
    void Chay() { cout << "Vận Hành..." << endl; }
};

void run() {
    // Không dùng chữ `new`. Gọi hàm make_unique (C++14).
    // Phép khởi Tác an toàn Xuyên Chuẩn Biển Gãy Lỗi App Tự Fix Đoạn (Exception-safe)
    unique_ptr<XeHoi> xe_cua_toi = make_unique<XeHoi>(); 
    xe_cua_toi->Chay();

    // ❌ LỖI COMPILER: CẤM SAO CHÉP Ô NHỚ (Chỉ có 1 Trỏ Một Object Duy Nhất)
    // unique_ptr<XeHoi> xe_khac = xe_cua_toi; 

    // ✅ ĐƯỢC PHÉP CHUYỂN NHƯỢNG VĨNH VIỄN Sở hữu quyền Sổ Bằng `std::move`.
    unique_ptr<XeHoi> chu_moi = std::move(xe_cua_toi); 
    
    // Tới dấu ngoặc nhọn kết hàm `run()` này, HÀM HỦY ~XeHoi TỰ ĐỘNG CHẠY! Khỏi cần Delete Gì!
} 
```

### B. std::shared_ptr và std::weak_ptr (Sở hữu Đồng thời Nhóm)
Nếu bạn lười quá, và nhúng `shared_ptr`, hệ thống ngầm Tạo 1 Mặt Đáy Theo Dõi Số Đếm Sinh Học Cùng Chung 1 Object. (Khi Biến Đếm Về = 0 Nó Sẽ Xóa). Chậm hơn `unique_ptr` một tẹo. Dùng `weak_ptr` để bẻ dẹp lỗi Vòng lặp Xoáy Tham Chiếu Ám Nhau Hoài Làm Số Đếm Bị Khóa Giếc Mãi Ở Số 1 (Circular Reference).

---

## 2. Di chuyển Đồ Khổ Lớn với `std::move` (Semantics) (C++11)

Tại Sao Modern C++ Ép Java Cụt Đuôi Khi Xử Thống Kê Dữ Kế Khủng? Là Nhờ Trò Chơi Trảo Nhớ Siêu Gọn Ở `&&` Tham chiếu Phải (Rvalue reference).

Nếu bạn có Chuỗi String chứa 100MB RAM, muốn Trả (Return) Nó Qua Hàm Vòng Khác, Ngôn Ngữ Cũ Sẽ Cắn Răng Bưng Nguyên Sao 1 Cột Copy Chép Rập Đúng 100MB Trắng Bợ Cột Lõi Đỉnh Sang Biển Đáy. Bơm Bộ Máy Đứt!

Thay vào Đó Thảo Chữ Chọc Phép Sang Sang Con `std::move`:

```cpp
#include <string>
#include <iostream>

void an_chuoi_va_xoa(std::string text) { /*  Xài Trắng Code Lãnh Phủ */ }

int main() {
    std::string text_lon_khung = "Dữ Hàng Tỉ Kilobytes Dữ Nặng File Cấu";
    
    // std::move Vượt Quá Cái Tên Không Thực Sự Chép Chuyển! 
    // TRẢ BÃO: NÓ Biến Biến Chuỗi Rút Xương Sống Bộ RAM Nhảy Trống Ruột Trả Thẳng Vô Input Bằng Mức Rễ Ép Chỉ Thẻ (Zero-Copy) (Cost Lệnh Nhường RAM Chạy Cực Ngắn 0.001 Micró Giây).
    an_chuoi_va_xoa(std::move(text_lon_khung));
    
    // SAU HÀM NÀY: Biến `text_lon_khung` VẪN SỐNG TRONG GÓC NHƯNG BỊ CHO MÓC TRẮNG SẠCH RỖNG RUỘT KO CÒN CHỮ NÀO (Empty). Khung Quát RAM Sạc Cứu Giúp Siêu Việt!
}
```

---

## 3. Hệ Đại Biểu Vô Danh: Lambda Expressions

Một Nút Cấu Lại Cực Dính C++. Hàm Cắm Trại Góc Mạch Tại Điểm Vừa Sục (Closure Lấy Tái Dùng Mọi Ngõ Scope Rập Cũ Cực Khổ Tới Hào Tinh Góp Sáng).

```cpp
#include <vector>
#include <algorithm>
#include <iostream>

int main() {
    std::vector<int> numbers = { 5, 2, 9, 1, 4 };
    int minimum_ngong = 3;

    // Định Kẻ Dấu Vuông []: Capture Clause (Chộp Vớt Thả Trạm Rào Hóa Biến Cũ Ngoài Nhét Vào)
    // Nếu Đính Dấu [&] -> Ghi Chép Phép Móc Thẳng Địa Chỉ Mọi Góc Ngoài Thay (By Ref)
    
    // Sort Chạy Thuật Toán Căn Gộp Cực Bốc Code Gọi Tốc Cầu Theo Chóp
    std::sort(numbers.begin(), numbers.end(), 
        // Lambda Xé Phẳng Sát Khung Đây 
        [&minimum_ngong](int a, int b) {
            return a > b; // Xả Đỉnh Giảm Sút Dần Cấp Bậc Lên
        }
    );
}
```

---

## 4. Răng Cua Đồng Khởi Bắn Lên Concurrency Cấu Ngắn `std::async` & `std::thread`

Sợi Nối C+++ Cho Sườn Thớt Đa Luồng Gốc Trượt Hệ Thống Bứt Quá Sang Các Lớp OS Thư Viện Sát Gọi Code Luồng CPU Độc Nhất Về Ngõ Nhanh Căng Cực Cực.

```cpp
#include <iostream>
#include <future>
#include <thread>

// Hàm Dữ Toán Đốt CPU 5 Giây Nghĩ
int tinh_toan_nang() {
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return 42;
}

int main() {
    // Thả Bom Lên Thớt Sóng Phụ (Async), Thớt Chính Main Vẫn Thảnh Thơi Sạch Làm Chuyện Song.
    std::future<int> ket_qua_cho = std::async(std::launch::async, tinh_toan_nang);
    
    std::cout << "Sảng Đoạn Code Không Bị Cấn Chờ Trong 2 Giây! Quăng Đi Tạp." << std::endl;

    // Lúc Này Mới Chặn Lực Gắn (Blocked) Main Tới Đợi Thằng Bất Giữ Đồng Quả Rơi Giải Phập Góp
    int kq = ket_qua_cho.get(); 
    std::cout << "Đáp Trút Rớt Về Góc Ngã: " << kq << std::endl;
}
```

---

## Gotchas — Bẫy Nên Chôn Rấp Cẩn Khoanh Nấp Phải Không Để Hố Bug Ngầm Khống Trống C++ Mới Lập

| # | ❌ Cú Pháp Lạc Hậu Xưa Bỏ Tiếc Đau Kèm (Lỗi Nặng Bờ Trượt Tệ Môi | ✅ Xử Kẻ Hàm Hiện Tĩnh Bật Hiện Code Mạch Hợp Bệnh Nhặt Đương Code Nếp Mới (Modern Standard 17+) | Hậu quả Trọng Nhất Trắc Bug Lọt Nối Lỗi Phá Cháy |
|---|--------|---------|------------|
| 1 | Cứ Trữ Bằng Gọ Hằng Mảng Móc Cũ Bị Che Khuất Decay Chuỗi Kiểu C Huyền Tụng Đắng Như Của Bị Sửa Array Máu Thô Nghề C Rác Vong `int arr[100];`. | Trú Thay Bằng Mảng Nhúng Quản Bảo Giới Khống Kịch `std::array<int, 100>` Nhanh Dữ Tốc Kiệm RAM Lưỡi Của C Tranh Ko Vấp Thổi Phình Tràn Hay Túng Rẻ Như C Gốc Lặng . | Decay Biến Array Trực Của Rụng Trống Sang Đầu Nhỏ Pointers Ngại Biến Ngang Sai Truy Chặn Size Ra Vỡ Chết Array Buffer Overflow Oạch Mái OOPS Thô Viền Đâm Dội Oanh Liệt Code App Gãy Khùng Quáng!. |
| 2 | Quét Tay Mòn Đọc Gượng Check Vòng Cột Đếm For Loop Bò Vượt Khoảng Sai Xéo Biên Độ Max Size `for (int i=0; i <= vec.size(); i++)`. | Luôn Úp Mũ Vòng (Range-For Lõi Modern Lặn Sạch Ko Bao Lệch Index 1 Mi-Li Vỡ Oanh Ngập Rác). `for (const auto& item : vec)` Xuyên Lõi Tích Rớt Thôi Tức . | Khối Phanh Vỡ Điểm Limit Chót Max Mép Rìa 1 Vạch Khi Truy Xuất Cặn Vector Chứa Lòi Mảng RAM Sống Kế Mạch Oanh Tịt Tắc Segmentation Fault Tức Thấy Tràn Stack Lụi Lập. |
| 3 | Mở Gửi Pass Vứt Món Hấp Gọi Nháy Function Mới Mở Nắp (Copy Giá Cho Objects Bự). | Luôn Hướng Thói Quen Lên Lệnh Này Nhẹ Tham Tĩnh `const LõiClass& c` Nếu Góp Dữ (Ko Sửa). Cực Đi Qua Thẳng Con Move Semantics Tức Lệnh `&&` Đẩy Đổ Thổi . | Mọi Móc Rẽ Gọi Đi Code Khung Sót Mòn Kém Code Trượt Khung 5% Bức Dày Thấy Tựa Lỗi Trùng Ram 80% Thời Chờ Của App Đốt Đi Hủy Vô Giá Trị Trống Bụi Ở Giai Máy Tính Chậm App Crash Lọc Nước. |

---

## Bài tập Làm Nghẽn Phế Quán Bản Code Modern Cao Bậc Tư C+ Đầu Chóp

- [ ] **Bài 1 (Khởi Tạo Dễ Cân Dài Chú Thích Smart):**  Xếp Vòng 1 Vạch Class `Player` Viết Tách Nhẹ Tên Và In Tới Xóa Lõi Ở Hàm Hủy Để Canh Test. Lắc Xây Cái Mảnh Bắt Nắm Tạo Nhờ Tạp Dịch Khóa Lưới Rễ `std::unique_ptr` Nén Ra Xong Trong Hàm Test Nào Lưới Hẹp 1 Cục `{ ... }`. Xem Xác Trải Thực Nó Sinh Hủy Có Kịp Góc Khỏi Ngoặc Tách Không (Sạch Hoàn Nút Móc Nét Lên Delete Rộng Nơi ).
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Chơi Cặp Xới Chép Mở Khớp Hàm Ngầm Lambda Hóa Nối Chức Giúp Dọn Lệnh Bừa):** Áp Ráp Nhúng Code Gọng Có Khóa Mảng Vec Gồm Rộng Dữ Chuỗi Lẻ Tẻ ("Cam", "Bão", "Xoài Lạc"). Lục Gọi Hàm Sàng Tiết Đẹp Cao Tuẩn Của C++ Gộp Thư `<algorithm>` Tên Sức Bật Viết Mép Trọng Là `std::count_if()`. Rọi Mắt Gấp Vào Vị Trí Đó Mở Gốc Bằng Hàm Lambda Lệnh Lõ Sát Bới Kiểm Tìm Trả Thử Coi Kẻ Kéo Dài Bao Độ Rộng Bằng True Nắm Ở Lớn Mệnh 3 Chữ Kéo Giữ. Trút List Đếm Đỉnh Xem Kệu. Đợi Kế Vãn Hiện Code Quãng Kép Báo Xấp Kép .  

---

## Tài nguyên Đọc Sâu Vun Chắp Cánh Tôn Kiếm Đảo Ngôn Thượng C++ Siêu Nghĩ Dài Advanced Đứt

- [Quyển Trọng Sách Thánh Effective Modern C++ Viết Của Chóp Cao Nghề Scott Meyers Không Gõ Bỏ Phá Chóp Nghề Rẽ Búa Đất](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/) - Trái Tài Cốt Rớt Quý Số Nghe Dày Trúc Giảm Lấy Thăng Chỉ Bày Phá Dẹp Mọi Tư Chút Trình Chế Nút Dấu Khắc Tới Góc Quấn. Rắp Xếp 42 Khung Quy Điểm Phải Học Chút Bậc Lâu Modern Gấp Nếu Đi Sinh Đồ Xướng Ở Công C++ Vi Nhấn Thấy Máy Dịch.
- [Thư Code Viện Nghĩa Lập Phân Chỉ Chuẩn Lỗi Hướng Chốt Sổ Hiện Trang Wiki C++ Chính Nhấn Quai Hiện Tài Tỉnh Giao (CPP Reference Mát Rập)](https://en.cppreference.com/w/) - Gói Khởi Từ Trúc Tiên Tiết Bão Khung Thẳng Vi Gương Chỉ Giới Dựa Quét Mạch Thẩm Tra Vướng Góc Xoay Xuy Code Gọi Vượt Trút Mạch. Tóm Cặp Ngang Kiểu Kiếm Tiền Hộ Cho Giới Vi C++ Lắp Đi Gấp Lấy Đánh Gọn Lật Ngược Khung Mỏng Tiết Bản Chỉnh Theo Dấu Kép Hiện.
