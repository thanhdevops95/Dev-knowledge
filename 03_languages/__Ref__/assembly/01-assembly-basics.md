# ⚙️ Assembly Basics (x86_64) — Giao tiếp Thẳng Với Kim Loại (CPU)

> `[BEGINNER]` — Prerequisite: (Nắm vững Hệ cơ số 16/Nhị phân `01-how-computers-work-fundamentals.md`).
> Đây không hẳn là ngôn ngữ lập trình, nó là tập hợp Tên gọi Tiếng Anh cho từng Xung điện Lệnh (Opcodes) trên vi xử lý. Học Assembly để hiểu tại sao phần mềm crash, viết mã shellcode hacking và hiểu cấu trúc Compiler.

---

## Tại sao (WHY) lại Đụng tới Assembly (ASM)?

Bất kỳ mã C/C++, Rust hay Go nào khi Compile (Biên dịch) cũng phải được Dịch Giảm xuống Mã Assembly trước (Rồi mới thành file `.exe` hệ nhị phân 0101). CPU **CHỈ HIỂU** duy nhất Tập lệnh Máy (Instruction Set). Ở đây phân tích tập lệnh vĩ đại thống trị PC: Intel x86_64 bit.

**Vấn đề giải quyết:** Nghịch ngược hệ thống (Reverse Engineering), Tối ưu đỉnh cao 100% tài nguyên Hệ thống, làm Bootloader Hệ Điều Hành (OS).

**So sánh nhanh độ sát kim loại:**
| Tầng Lớp | Ngôn ngữ | Đặc điểm chính |
|---|---|---|
| **Cấp Cao (High-level)** | Python / Javascript | Cách CPU hàng vạn dặm. Đi qua máy ảo/Trình thông dịch. Vô cùng chậm. |
| **Cấp Dưới (Low-level)** | C / C++ / Rust | Gần CPU nhất nhưng vẫn có Trình biên dịch (Compiler) kiểm tra biến số. Tự động hóa nhiều phần. |
| **Máy Trực Tiếp (Machine-level)** | **Assembly / Machine Code** | Gõ Lệnh đấm trực tiếp vào từng Thanh ghi trên Bảng mạch CPU. KHÔNG CÓ BIẾN. |

---

## 1. Cài đặt Môi trường (NASM & Linker)

Chúng ta sử dụng trình **NASM (Netwide Assembler)** theo cú pháp (Syntax) của Intel — nó đẹp, dễ đọc hơn cú pháp AT&T (dùng trên GCC cũ). Chạy trên nền tảng Linux (Do Linux dễ gọi Code Hệ Điều Hành xuống nhanh nhất để in Hello World).

**Cài đặt:**
```bash
# Trên Linux (Ubuntu/Debian) -> Nơi tốt nhất để học ASM
sudo apt install nasm binutils  # Kéo bộ Dịch (nasm) và Bộ Gắn File Sinh Mã Chạy (ld)

# Biên Dịch Vàng Kép 2 Bước (Chuyển Gốc Thành Trạm File Mục Tiêu O):
nasm -f elf64 hello.asm -o hello.o 

# Gắn Máy Trở Ráp Linh Hồn Để File Sống Thành Phần Mềm Linux Chạy Tích:
ld hello.o -o hello_run 
```

---

## 2. Hello World! (Syscall gọi thẳng Kernel)

Một chương trình ASM x86_64 luôn chia làm 3 VÙNG ĐẤT BẤT DI BẤT DỊCH (Sections):
1. `section .data` (Vùng khai báo biến Toàn cục - Biến Hằng Số cứng).
2. `section .bss`  (Vùng khai báo biến Rỗng để Nhập Nhớ chưa có định).
3. `section .text` (Viết Mã Code Chương Trình, nơi có thẻ `_start` Hướng Cửa Mở App).

Tạo file `hello.asm`:
```nasm
section .data
    ; DB = Define Byte (Đặt Khuôn Dấu Chứa 1 Byte Khắc Chữ), 10 = \n Xuống dòng
    loi_chao db "Xin Chào Assembly Sieu Manh!", 10 
    do_dai equ $ - loi_chao   ; Tự Động Định Toán Đo Độ Dài Chuỗi Rút Tới $ Dòng Này.

section .text
    global _start  ; Công bố Rõ Cửa Bật Lên Linker Báo System Bác Nạp Ràng Lõi OS Chạy Thẳng Vào Đâu

_start:
    ; ==================================
    ; BƯỚC 1: Lệnh Hệ Điều Hành (Syscall) Đẩy In Chữ Màn Hình Trữ Terminal 
    mov rax, 1          ; RAX Lắp Số 1: Lệnh Số Kí Sys_Write (Hàm Xuất Chữ Lên Console Của Nhân Linux)
    mov rdi, 1          ; RDI Lắp Số 1: Nghĩa là Cổng Xuất File Descriptor In Khung Chuẩn (STDOUT)
    mov rsi, loi_chao   ; Nạp Trỏ Địa Chỉ Ô Nhớ Đẩy Chuỗi 
    mov rdx, do_dai     ; Nạp Độ Kích Chữ Số 
    syscall             ; (GỌI ĐÁNH KERNEL LINUX TỚI RUN KỊCH BẢN RAX 1)!

    ; ==================================
    ; BƯỚC 2: Rút Lui An Toàn Gọi Phá Hàm Hủy Mã Đuôi Chốt Sys_Exit
    mov rax, 60         ; Đạn 60 Báo Lệnh Sys_Exit 
    mov rdi, 0          ; Error Code 0 Báo OS Ổn Thỏa
    syscall             ; Sập Trình!
```

---

## 3. Thanh Ghi (Registers) — Tủ Kéo Lưu Dữ Của CPU

CPU Không Hiểu Chữ Nghĩa Biến (Variables) Trong RAM. Nó chỉ biết chạy thật nhanh bằng cách Tạm Giữ Giá Ướm Dữ Vào những Cái Ngăn Đựng Siêu Tốc gắn chết trên mạch của nó gọi là **Thanh Ghi (Registers)**.

> CPU x86_64 (64-bit) có các thanh ghi R (Hậu Tố R 64 bit). Nữa 32bit của nó có Tên Đầu Tố Bằng Phím E. Nữa 16 Có Dạng Phím Cuối Đuôi X.

- **RAX, RBX, RCX, RDX**: Thanh ghi Tổng quát đa dụng (General Purpose). Tuy vậy RCX hay dùng làm bộ đêm của Vòng lặp Loop (Counter). Còn RAX hay dùng làm nơi Trả Kết Quả Hàm.
- **RDI, RSI, R8, R9**: Thanh ghi Chứa Tham Số truyền vào lúc gọi Hàm.
- **RSP (Stack Pointer)**: Trỏ Đỉnh Kho Đạn Hiện Tại Đè Kẹp Lên Giấy Cục RAM STACK Tạm.

Lệnh Sao Gán Cơ Cấu (Tương Tự Đổ Data Số `=`) Là Hàm `MOV` (Nghĩa Di Chuyển).
```nasm
mov rax, 10    ; Cho rax giá trị Số 10.
mov rbx, 5     ; Ráp Đẩy rbx bằng 5.

add rax, rbx   ; RAX = RAX + RBX (Giờ Rax Móc Số 15 Khấu Tôn Lõi Thẳng).
```

---

## 4. Stack Tạm và Cách Gọi Cục (Thủ Tục Cú Pháp Cấu Hàm Call)

Hệ Ngăn Xếp Thẻ (Ngược Lật Push Bơm Lên Đỉnh, Pop Rút Đỉnh Xuống). Được ASM Sài làm Khu Ghi Tạm Bợ Cứu Nhớ Trụy Lúc Lệnh Mã. 

```nasm
_start:
    mov rax, 50
    push rax    ; Giấu Tạm RAx lên Đỉnh Chóp Kho Cất Ngầm Nhanh Stack Memory  

    mov rax, 2  ; Cực Liền Rax Lạc Sang Số Vị Nhanh Tới.

    pop rbx     ; Móc Bật Dậy Số Trên Đỉnh Chóp Cũ (Tức Là Số 50 Cất Giữ Khởi Nãy Bắn Ra Nén Gán Rớt Xuống Khay Lỗ Ráp RBX Mới Tức Thời Rửa !).

    ; -> KẾT CỤC CPU GIỮ: RAX LÀ 2. RBX CHUẨN XÁC RA 50.
```

Nhảy Có Điểm Nhấn Nhóm (JMP / JNE / CMP): Cả Toàn Thuật Toán Vòng If For Đều Sinh Ra Do Lệnh Khẳng Vọt Này.
```nasm
    mov rax, 5
    cmp rax, 5      ; (Compare) Trừ Ngầm Hai Bọn Nó Lấy Sóng Khảo Phán Đánh Nhau Tức Khắc. 
    je Equal_Label  ; Break: Jump if Equal (Nếu Phân Nhận Hai Của Lệnh Ráp Cột Sánh Là KHỚP ĐÚNG Nhảy Gấp Xuống Nhãn Xưng Tên Dưới Đáy Xâu Equal_Label Tới!).
    
    mov rbx, 0
    jmp Cuoi_Label  ; Jump Nhảy Mặc Kệ Trắng Không Điều Trao Kiện Tới.

Equal_Label:
    mov rbx, 1      ; Biến RBX Cất Sẽ Cầm Đi Theo Lệnh Gán Xuyên 

Cuoi_Label:
    ; Xong Viết Lệnh.
```

---

## Gotchas — Những Lỗ Hổng Ngã Oạch Dễ Chạm Trúng Rào Mã Cấm X86 OS Gãy System Bug

| # | ❌ Tư Duy Cũ Tưởng High Language Dễ Ơn | ✅ Tịnh Tế Nhạy Cảm Trúng CPU Level | Hậu quả của Việc Mang Quên Mạch Xếp Viết Đoạn Xoáy Vượt Thần Xoay |
|---|--------|---------|------------|
| 1 | Viết Lắp Một Lố Vong Chờ Lệnh Hàm Main Chẳng Khóa Gọi Giải Sys_Exit Oạch Để Thôi Block Văng (Như Ở JavaScript Dừng Kín C). | TẤT CẢ Gốc Assembly App BẮT QUY BUỘC PHẢI KHÉP Khống Đi TỚI SYS_Exit Kéo 1 Vị Lệnh Đoán Ngắt Cho Kho Rỗng Dịch Tầng. | Rìa Bộ Chạy Lướt Đi Oanh Quét Xuống Tới Dải Memory Chữ Mã Dòng Mảng Ngắn Bậy Rác Đọc Sinh Segmentation Fault (Core Dumped Sập Chán Ánh Giết Sạch Quá Lỗ Process Đứng Rát Rầm Giết Sạch Bằng Dưới Máy Khung App Linux Rách Nghẽn Core Khít!). |
| 2 | Kênh Thử Xô Ép Mã Lệnh Memory To Memory Mảng Mở Ốp Vào Nhau Lồng Lộn Cục `mov [var1], [var2]` Dày Dặng Lỗi Ngu Cổ Trúc Thật Kém Đau Bụng Nhất Ngôn Xưa Khôn Thường Gặp . | CPU RẤT Khắt Khe Sóng Vòng Dò Đòi! Ít Nhất 1 Bờ Ném Láp Khung Cho Tham Chiếu Lệnh Mẫu Phải Xin Thuộc Về Cẳng Rãnh Của CPU (Registers - Rax/Rbx) Chứ KHÔNG LÀ RAM Nới RAM Cấu. | Trình Dịch Assemble Nhả Văng Lỗi Không Đồng Thuận Ớt Chỉ Thả Vào Đít. Không Gõ Ép Biên Dịch Gì Hóa Cả Quát! Build Mất Giọng!. |

---

## Bài tập Tự Gõ Luyện Thay Nếp Cũ Lõi OS Máy Root Lên Cao Tiên Trình CPU Đáy Chóp

- [ ] **Bài 1 (Khá Ngáp):** Dùng `rax` Tráo Số Trữ Gửi Tới Trấn Vào 5. Đánh Bắt Chuyển Kế Nhâm 10 Kéo Vào Cạnh Ô `rbx`. Cho Chạy Đóng Hàm Toán `add`. Liệu Thấy Gọi Dựng Vọt Code Dựng (Theo Bằng Tay Hoặc Coi Nốt Mở Rộng Viết Kịp In Xuống Cổng Báo Tốt Quả Output).  
- [ ] **Bài 2 (Trung bình Map Khớp Module Cấu Quãng Gọi Rãnh Call Stack CPU Mũ Khung Sys Quản Mã Khung):** Phác Lại Khóa Text Khung Section Dưới In Thẳng Giọng Rẽ "Tôi Học Sang C++ Xong Xuống Nắm Bụng Này Ốc Hùng". Tới Tấu Rõ Đo Quát Bảng Mảng Bằng Lượng Đô Cụ `equ $ - x` Báo Đợi Khắp Ngược Nhỏ Nơi Gọi Môn .  

---

## Tài nguyên Đọc Sâu Vun Tư Cấu Kiến OS Gốc Hacker

- [Học Chặn Assembly Ráp Toàn Chậu Sách Bức Gõ Lệnh Từ Dõi Nạp Mở Bộ Core Căn Móc Sách Gốc (CS Gốc Chuyên Phái Giáo Cố Xịn Hết Xẩy Khoa PC Assm Lõi x86 Lập)](http://www.egr.unlv.edu/~ed/assembly64.pdf) - Dẹp Lôi Giáo Thuyết, Cầm Chỉ Cấu Tập Mẫu Vòng System Call Thô Vòng Lật Khung Vĩ Trọng Cốt Nghĩa Nghề Viết Mã Chặt Rụng Cõi Bào Kẻ Lỗ Sáng Dạ .
- [Tìm Phá Học Tắt Ở Sảnh Phun Nguồn Báo Opcodes Số (Bách Khoa Cấu Lỗi Kiến Trúc X86 Tổng Mã Toàn Rễ Kho Cấp Mã Tĩnh Kỉ Tích Kẻ Ngự Bộ Intel Lỏi Mẫu Chặn Gì Gốc Cũng Có)](https://www.felixcloutier.com/x86/) - Nóng Và Xứng Danh Sợi Xâu Tổng Bộ Xóa Não (Reference Tuyệt Chỉ Không Dành Kẻ Yếu Đi Găm Bộ Lệnh Gập Vặn Ốc Hướng Gốc Đi Sâu Tạm 4 Ngày Cho Không Đầu Bịt Kịp Cắn Khốn ).
