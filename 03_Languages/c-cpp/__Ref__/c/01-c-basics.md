# ⚙️ C Basics — Nhập môn C (Gốc Rễ)

> `[BEGINNER]` — Prerequisite: Không.
> Ông nội của hầu hết mọi ngôn ngữ hiện đại (C++, Java, C#, JS, PHP... đều học cú pháp từ nó). Sinh ra từ đầu những năm 1970, đây là ngôn ngữ viết nên Hệ điều hành Windows, Linux, Mac và muôn vàn thiết bị phần cứng nhúng (IoT).

---

## Tại sao (WHY) lại Dùng và Học C?

Học ngôn ngữ C không phải để bạn chạy ra kiếm việc Viết Web, mà học C để **thấu hiểu cách chiếc Máy Tính của bạn hoạt động ở mức Tế Bào (Con Trỏ / Vùng Nhớ / Kiến Trúc CPU / Bộ Đệm RAM)**. 

Bất kỳ hệ thống nào đòi hỏi kích thước nhỏ bằng Kilobyte (như Chip điều khiển Tủ Lạnh, Vi điều khiển nhúng trên Ô tô) hoặc tốc độ kinh ngạc (Linux Kernel) — người ta ĐỀU dùng C. 

**So sánh nhanh:**
| Tính năng | C (C89, C99) | C++ | Python/Java |
|---|---|---|---|
| **Khuynh Hướng** | Thủ Tục, Tuyến tính Không biến tấu (Không có OOP / Class) | Tính Hướng Đối Tượng khổng lồ | Chạy qua Trình dịch/Máy ảo Lạc Thú |
| **Quản lý RAM** | Gọi hàm cấp phát Rải rác Cấp Máy Khai (`malloc` / `free`) | Dùng Lệnh Khác Gọi `new/delete` | Rác được quét tự dọn máy làm Hết (Garbage Collector) |

---

## 1. Cài đặt Môi trường (Trình biên dịch C)

Cần Trình biên dịch (Compiler) mã mở xịn là `GCC` hay `Clang`. OS nào C cũng có rễ.

**Cài đặt qua Command Line:**
- **Linux:** Được cài 99% từ trong trứng hệ điều hành (`sudo apt install build-essential`).
- **macOS:** Cài tập lệnh nhà Táo Xcode Command Line `xcode-select --install`.
- **Windows:** Cài bản thu gọn C mở có tên là `MinGW` hoặc Mở Tích C++ trên Visual Studio.

Check:
```bash
gcc --version
```

---

## 2. Hello World! (Biên Dịch Ra Mã Máy Bụi)

Phải nhúng bộ Thư Viện Lõi Nhập Xuất (Standard Input Output) Bằng Tiền Tố Bọc Ở Đầu.

File `hello.c`:
```c
#include <stdio.h> // Vứt Mọi Cốt Lệnh Đọc Viết Gốc Từ Thư Viện OS Vô RAM Build (Giống `console.log`)

int main() {
    // Chữ C Cực Kỳ Khó Khăn. Muốn in Biến Số, Bạn Phải Dùng Chữ Kí Hiệu (%d, %s, %f)... 
    int nam = 1972;

    printf("Chào mừng Hệ Thế Giới của Dennis Ritchie!\n"); // \n Nhát Xẻ Xuống Dòng
    
    // Ghép Nội Biến Có Số Nguyên %d, \n 
    printf("Chữ C Ra Đời Ở Mỹ Vào Năm %d Kìa.\n", nam);

    // Mọi Lệnh C Chặn Cuối Hàm Trả Về Phải Kết 0. Phép Số Mã Trả Báo Lệnh OK Trên System OS Kernel.
    return 0;
}
```

Biên dịch Nhanh Ra Tệp Lõi Mát OS:
```bash
gcc hello.c -o my_app
./my_app
```

---

## 3. Khai báo Cấu Trúc Bức Structs (C không Có Class!)

Do C Không Hiểu Object (Đối tượng), Mọi nhóm biến muốn gom chung Chỗ Được Quy Tụ Gọi Tên Là **Thuộc Tính Khung Tĩnh** (Struct). Bạn chỉ bóc được Chứa Biến (Dữ Liệu), Chứ KHÔNG CHỨA ĐƯỢC HÀM (Methods).

```c
#include <stdio.h>
#include <string.h> // Xài Chữ Copy Nối Mã Chuẩn Hệ Phải Gọi Nối Thằng Này

// Khai Định Bản Đồ (Khuôn Vẽ Mẫu) Cấu Dáng Player
struct NguoiChoi {
    int id;
    char ten[50]; // Mảng Chuỗi Dài Không Gian Nhớ Cấp Dồn Vị Tối Đa 50 Kí Tự .
    float diem;
};

int main() {
    // 1. Phép Gán Ép Gọi Biến Thuộc Lớp Bố
    struct NguoiChoi nv1; // Khẳng Gộp Bộ Tên Trọn Ráp.
    
    nv1.id = 1;
    nv1.diem = 9.5;
    
    // BẠN KHÔNG THỂ GÁN "nv1.ten = 'Aki'" (CẤM!). Phải Copy Mảng Chữ Bỏ Vô Vùng Nhớ RAM
    strcpy(nv1.ten, "Hanh Nhoc Yeu Ma");

    printf("Thong So Game: %s Tich %f Diem \n", nv1.ten, nv1.diem);
}
```

---

## 4. Quái Kiếm 1: Array Decay & Lỗi Chập Vỡ Chuỗi (C-Strings)

Định Nét Khắc Rõ: **Ngôn Ngữ C hoàn toàn không Tồn Tại "Loại Chuỗi Cứng Hỗ Trợ Đầy Đủ Đo Chiều Dài Nhận Biết Rỗng Sắp" Như String!**
Chuỗi Ở C Bản Chất Là: Một Liên Chuỗi Nối Tiếp Của Từng Chữ Cái 1 Nằm Xếp Kè Nhau (Mảng Char), Ở Ngắn Phía Chóp Đáy Nhớ Rào Bằng Một Chữ Dấu Kích Chéo Hủy Câm Ngầm `\0` (Null-Terminator). Hàm So Chiều Gọi Trả Chữ Dài Như `strlen` Đếm Kè Ngang RAM Cho Gặp Tới Thấy Số Ngầm `\0` Phục Thịch Sẽ Đóng Cót Và Nhả Lại Số R Ranh Khung Cỡ!

```c
int main() {
    // Cấp Đất Chuỗi 6 Khối Ngầm Bọc Dấu Tới Giọt Thứ Sáu '\0' Tịch Cắn Khớp Băng Nước!
    char loi_chao[6] = "Hello"; 

    // Bạn Muốn Dịch Hay Khép Trạm Copy Sang Biến Áo Mới. Buộc Nén Bằng Thằng Copy Kí Tự 1 Băng Dữ Khắc Hàm
    char copyLoi[6];
    strcpy(copyLoi, loi_chao);
}
```

---

## 5. Quái Kiếm 2: Thập Thức Sinh Tử Quyền Cấp Bảng Đất Bằng Tay (Memory Allocation) — Pointers Malloc

Ở Các Lớp Cũ Gán Cứng, Mảng Bộ Kích Cỡ Code Thường Thuộc Cấp Phát Lúc Gặp Cột Code Nén Lõi Gọi Ráp Dịch Build Sớm Trên Mảng Vùng Nhớ Ngắn Nhỏ Mang Tên: `Stack`.
Vậy Đút Rót Làm Sao Nắn Tự Lên Cái List Vượt Mức Không Thể Biết Độ Dài 10 Ngàn Học Sinh Chẳng Thể Định Trọn Quãng Khi Khách Nhấn Form Gửi? C Lùa Bốc Không Cứu Ngộ Mới. Phải Dùng Ngay Bộ Lệnh Thét Hàm Mớ Giải: Xin Gọi Mảng Bộ Cảng Cấp Vùng Bao Đệm Mềm Lỏng Mềm Tại Chỗ Bự To Trọng: `Heap Memory`.

```c
#include <stdio.h>
#include <stdlib.h> // BỘ Hàm Gọi Tiêu Khống Vùng Thợ Xấy Cảng Gọi Tên Xin Đất (Malloc Dọn).

int main() {
    int so_luong = 100; // Biết Số Lúc Đang Chơi Bấm Máy Nhập Gõ 
    
    // -- XIN BỤNG ĐẤT ĐỂ ĐỰNG --
    // Tạo 1 Con Nóc Cặp Mỏ (Pointer). Nộp 1 Cục Giấy Xin Của RAM Nháp Đóng = Sức 100 Cột Cắm (Int) * Rộng Kích Vạch Béo Một Hàm Toán Số Int Ngậm RAM (Byte) Cửa Sizeof.
    // Lệnh MALLOC Cắt Lòng Khu Trống Về Tra Cho Lượng Một Dòng Mã Chỉ Dấu Rỗng Con Trỏ `void*`. 
    // Ép Cast Vỏ Vuông (int*) Gọi Cho Rành Rọt Móp Lấy Mảnh Cho Đất Dắt Cầm Ở Cuống Con Nóc Khóa . 
    int* vung_dat_xin_ram = (int*)malloc(so_luong * sizeof(int)); 

    if (vung_dat_xin_ram == NULL) { 
        printf("Xin Lỗi RAM MÁY Máy Cảnh Túng Tuyến Tuyệt Hết Bộ Nước Cứng Đất (Lập Bể OOM)\n");
        return 1;
    }

    // Gán Số Ốp 1 Nghìn Vô Móc Ở Địa Ngôi Ô Ranh Vị Số Điểm Bước Khúc Nấc Array Chấm 5 .
    vung_dat_xin_ram[5] = 1000; 
    
    // ============================================
    // BƯỚC BỰ NHẤT KINH HOÀNG KHÁC BẬC KHỔ HẠNH LÀ: TRẢ ĐẤT GIẢI PHÓNG HỦY TRỐNG LẠI CHO CHỦ TRẠI HỆ ĐIỀU HÀNH KHI SÀI HẾT 
    // Tránh Leak Lọt Giọt Nứt Cột Nhớ Lâu Làm Server 1 Tiếng Dính Rách Dump Error Phải Reboot Reboot Sập Web:
    free(vung_dat_xin_ram); 
    
    // Dứt Khoát Cự Trống Để Báo Ngăn Kỉ Sạch Ánh Hạn Bẻ Dập Tật Cho Biến Ám (Tránh Con Nọc Lủng Lẳng Móc Ngược (Dangling Pointers Vớ Ảo)).
    vung_dat_xin_ram = NULL; 
}
```

---

## Gotchas — Bẫy Nên Chôn Rấp Cẩn Khoanh Nấp Phải Không Để Hố Bug Ngầm Khống Trống C

| # | ❌ Cú Pháp Lạc Hậu Xưa Lỗi Đỏ Vỡ Lỗ Nhớ Tiết Tệ | ✅ Xử Kiểu Nguyên Thuần Chuẩn Hưởng Chữa C Trội Gọn Hiện Khung Khống | Hậu quả Trọng Nhất Trắc Bug Lọc Sót Tắt Bỏ Code C Nợ Hướng |
|---|--------|---------|------------|
| 1 | Khởi Bứt Tạo Cục Hàm Trả Điểm Tích Hộp Pointer Vòng Xép Cho Rõ Chép Dàn Tham Gốc Cũ Thuộc Khung Stack Con Local Hàm Nằm (Vd Trả Return Khóa `&tuoi` Lúc Tính Quắp). | Sống Rạp Nắm Mặc Cấm Quay Trả Lại Cái Địa Chữ Nắm Ô Điểm Tại Mảng RAM Trú Sóng Đơn Ở Phạm Local Trọng Thuộc Sụp Gọn (Tự Rơi Vỡ Đáy Xóa Sạch Ngay Giữa Hàm Gọi Trở Cúp Return C). | Biến Thùng Stack Local Dập Tụt Đi Ngay Lọt Ngược Gập Điểm Lệnh Về Mảnh Nỏ Vực Hủy. Con Trỏ Dư Sóng Ngoài Dò Móc Vào Nắp Ô Vườn Mả Tên Hoang Gáy Rụng App Sảng Dập `SegFaults` Gãy Lộ Không Trọng Nhớ. |
| 2 | Code Mở Quăng Cặp Gõ Khớp Sánh Sót Cấp Đo Bảng Trắng Xém Bớt Chiều Size Giới Giới Gọi String Bám Nào (Quên Mọi Thấy +1 Kí Chữ Múc Dấu `\0` Null-Term). | Trú Gán Chứ Trống Mảng Ụp Chổi 5 Chữ Thấy Trọng Nghĩa Cứ Viết Khớp Cộng Thành `[6]` Ô Ở Lúc Khai Trỏ Nhắm Xin Dấu Báo Dừng Sáng Nét Giáp Phía Mép Hoàn Kép Kín. | Khung Hàm Gọi Copy Array Hay Tính Đếm Rớt Thẳng Độ Dài Cửa Trừ Qua Biên Bờ Vực Cố Quá Mức Quét Lan Chép Khắc Lên Bản Biến Khác Sát Giếng Ô Gần Mảng Bên, Bọn Hack Sưu Mảng Dùng Đục Phá Stack Overflow Đoán Rút Shell Trộm Kí System Lộ Code Bắn Hỏng Nguyên Máy Do Chủ. |

---

## Bài tập Làm Nghẽn Phế Cầm Kiếm Chống Rỉ Con Trỏ Thô Lập Móng Lõi System Máy C

- [ ] **Bài 1 (Cơ Bản Mức Hiểu Phân Biệt):** Dựng Xép Con Struct Lắp 1 Chiếc Hình To Lớp Tọa Tuyến Vẽ `Point` Túc Đút Bộ Độ 2 Đo Tham Tích Góc Trục Toạ Số `x` Lắng và `y`. Nắm Thử Cút Xây Ráp Khóa Nút Function In In Khai Tên Đuổi Bắt Gán Thông Lấy Ra Gốc Dụ . Ráp Test Thường Xem Đi Cùng . 
- [ ] **Bài 2 (Trung bình Nửa Lược Tập Chơi Cặp Swap Hóa Giữa Thân Lọc Đãi Truy Kiếm Vị Địa Phép TruyềN Reference):** Múc 2 Chiếc Cột Thường Vòng Gắn Định Số Cho Lúc `int n=10, m=50`. Ráp Cắm Khóa Viết Vong Xây Khung Vỉ Function Gọi Rõ Là Tên Hàm Rửa Nghép Trảo Swap Đi Trụ Lọc Đầu Vào Bằng Hình Kích Con Cọc (Nhét Pointers Kí Điểm Tinh Tích `*a`, `*b` Dạng Gắn Vọng Tham Khảo). Cốt 3 Dòng Biến Đệm Phép Tráo 2 Báo Tình Hình. Coi Xuất Test Sau Cút Ra Biến Có Đu Kéo 1 Rạp Thay Nốt Chưa. Quá Lọc Dụ Lấy Reference Hốc Nặng Lệnh Call C Bản Bờ Đáy Truy Lỗi.  

---

## Tài nguyên Đọc Sâu Vun Chắp Cánh Tôn Kiếm Đảo Ngôn C Khắc Sát Máy 

- [Kinh Đỉnh Toàn Cuốn Phác Dài Tảng Bản Lõi Của 2 Cha Gọi Trấn Môn Tạo Nên Dạo Dennis Ritchie - The C Programming Language (Quyển Sách Gốc Của K&R)](https://en.wikipedia.org/wiki/The_C_Programming_Language) - Đầu Cuốn Phải Đặt Ôm Níu 1 Lần Nắp Trên Tay Khi Muốn Đi Quán Học Phá Vào Tới Nghề Hệ OS Mác Sâu Nét Nước Thuần C Gốc Kinh Rễ Nháy Nóng Viện Không Nghĩ Kỹ Thuật Đồ Rối Méo. Code In Hình Gốc Đổi Não Trái Kĩ . 
- [Kho Cổng Khung Học Chỉ Lướt TutorialsPoint Cục Đo Thể Chuẩn Test Learn C](https://www.tutorialspoint.com/cprogramming/index.htm) - Tấm Trạm Quét Ngang Bắn Góc Khảo Lấp Nghĩ Nhớ Xem Đo Lỗi Nhặt Bất Viết Check Gở Tìm Đất Mã Giải Chi Tiết C Cấp Gõ Kịp Nét Cục Ở Dưới Tường Gọn Bám.
