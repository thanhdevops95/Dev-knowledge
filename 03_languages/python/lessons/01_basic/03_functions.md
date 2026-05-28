# 🎓 Thiết Kế Hàm Và Nghệ Thuật Tái Sử Dụng Mã Nguồn Trong Python

> **Tác giả:** Mr.Rom  
> **Phiên bản:** v3.0.0  
> **Tạo lúc:** 16/05/2026  
> **Cập nhật:** 26/05/2026  
> **Level:** Basic  
> **Tags:** [MUST-KNOW]  
> **Thời lượng đọc:** ~25 phút  
> **Yêu cầu trước:** [Bài 02: Cấu trúc rẽ nhánh và Vòng lặp](./02_control-flow.md)

> [!NOTE]
> **Mục tiêu bài học:**  
> Viết code chạy được là tốt, nhưng viết code sạch sẽ, ngăn nắp và dễ bảo trì là đẳng cấp của một kỹ sư lập trình chuyên nghiệp. Bài học này sẽ giúp bạn làm chủ **Hàm (Function)** — công cụ tối thượng để đóng gói mã nguồn thành các khối logic độc lập, giúp tái sử dụng mã nguồn hiệu quả, tránh trùng lặp code và tổ chức dự án một cách khoa học.

---

## 🎯 Sau Bài Học Này Bạn Sẽ:

- [x] Khởi tạo thành thạo các hàm trong Python bằng từ khóa `def` và `return`.
- [x] Phân biệt rõ ràng và làm chủ hai cơ chế truyền dữ liệu: *Positional* và *Keyword* Arguments.
- [x] Sử dụng linh hoạt các tham số nâng cao: *Default Values*, *`*args`* (Tuple) và *`**kwargs`* (Dictionary).
- [x] Nắm rõ quy tắc vận hành của biến trong bộ nhớ thông qua phạm vi *Local vs Global Scope*.
- [x] Thiết kế tài liệu hướng dẫn sử dụng hàm chuyên nghiệp bằng *Docstring* và *Type Hints*.
- [x] Làm chủ cách viết hàm vô danh *Lambda* cực nhanh cho các logic một dòng.

---

## 💡 Bài Toán Lặp Mã Nguồn: Cơn Ác Mộng Sửa Code Ở 180 Nơi!

Quay trở lại với script tính lương nhân viên ở bài học trước. Bạn đã viết vòng lặp duyệt qua 30 nhân viên để tính thuế bậc thang. Mỗi lượt lặp mất khoảng 10 dòng code tính toán phức tạp.

Đột nhiên, Sếp bước đến và yêu cầu: *"Bây giờ công ty cần làm thêm một báo cáo tổng kết 6 tháng cuối năm. Hãy tính lại toàn bộ lương và thuế của từng nhân viên trong 6 tháng đó để lập báo cáo gửi cơ quan thuế."*

Nếu không biết cách thiết kế Hàm, bạn sẽ phải tiến hành:
*   Copy-paste khối 10 dòng code tính toán đó sang vị trí mới.
*   Lặp lại việc này cho 6 tháng khác nhau trên danh sách 30 nhân viên.
*   **Tổng số chỗ lặp:** Bạn có ít nhất 180 dòng code giống hệt nhau rải rác khắp dự án.

Ngày hôm sau, nhà nước thay đổi luật thuế bậc thang. Bạn phải đi tìm chính xác **180 vị trí** đó để chỉnh sửa thủ công. Chỉ cần gõ sai một ký tự ở một chỗ bất kỳ, toàn bộ báo cáo tài chính sẽ bị sai lệch. 

Để chấm dứt vĩnh viễn cơn ác mộng này, **Hàm (Function)** ra đời! Bạn chỉ cần viết logic tính toán 1 lần duy nhất trong hàm `tinh_luong()`. Tất cả những nơi khác chỉ việc gọi hàm này ra sử dụng. Khi luật thuế thay đổi, bạn chỉ cần sửa **đúng 1 chỗ duy nhất** bên trong hàm.

---

## 1️⃣ Tại Sao Hàm (Function) Là Công Cụ Giải Cứu Bạn Khỏi Việc Copy-Paste?

Viết code mà liên tục copy-paste chính là hành vi vi phạm nguyên tắc vàng số #1 của kỹ nghệ phần mềm: **DRY (Don't Repeat Yourself - Đừng bao giờ lặp lại chính mình)**. 

Hãy xem sự khác biệt:

*   **Khi không dùng Hàm (Lặp code xấu xí):**
    ```python
    # In ra câu chào cho 3 học viên khác nhau
    print("Chào mừng học viên Nguyễn Văn Nam đến với lớp học Python!")
    print("Chào mừng học viên Trần Thị Bình đến với lớp học Python!")
    print("Chào mừng học viên Lê Văn Cường đến với lớp học Python!")
    ```
    *Vấn đề:* Nếu bạn muốn đổi chữ "lớp học Python" thành "khóa học Lập trình Web", bạn phải đi sửa thủ công 3 dòng khác nhau.

*   **Khi đóng gói logic vào một Hàm (Sạch đẹp, nhất quán):**
    ```python
    def chao_mung(ten_hoc_vien):
        print(f"Chào mừng học viên {ten_hoc_vien} đến với lớp học Python!")

    chao_mung("Nguyễn Văn Nam")
    chao_mung("Trần Thị Bình")
    chao_mung("Lê Văn Cường")
    ```
    *Lợi ích:* Chỉ cần thay đổi 1 dòng duy nhất bên trong định nghĩa của hàm `chao_mung`, toàn bộ câu chào trên toàn hệ thống sẽ tự động cập nhật theo!

### 3 lợi ích cốt lõi nhất của việc sử dụng Hàm:
1.  **Tái sử dụng tối đa (Reusability):** Viết 1 lần duy nhất, gọi sử dụng ở hàng ngàn nơi khác nhau trong hệ thống.
2.  **Khử trừu tượng (Abstraction):** Người sử dụng hàm (Caller) chỉ cần biết hàm đó có công dụng gì và truyền tham số gì vào. Họ hoàn toàn không cần bận tâm bên trong hàm đó xử lý toán học phức tạp ra sao.
3.  **Dễ dàng kiểm thử (Testability):** Một chương trình được chia nhỏ thành các hàm độc lập sẽ cực kỳ dễ dàng viết mã kiểm thử tự động (Unit Test) để đảm bảo không bao giờ xảy ra lỗi.

---

## 2️⃣ Bản Chất Của Hàm: Chiếc Máy Xay Sinh Tố Logic Trong Lập Trình

> [!NOTE]
> **Ẩn dụ sư phạm:**  
> Hãy nghĩ về Hàm giống như một chiếc **máy xay sinh tố**.  
> *   **Đầu vào (Input - Parameters):** Các loại trái cây bạn bỏ vào máy (dâu, chuối, xoài).  
> *   **Vận hành bên trong (Logic - Body):** Lưỡi dao quay để xay nhuyễn trái cây.  
> *   **Đầu ra (Output - Return Value):** Ly sinh tố thơm ngon bạn rót ra để thưởng thức.  
> Cùng một chiếc máy xay (hàm), bạn bỏ hoa quả nào thì sẽ nhận về loại nước ép tương ứng đó.

### Anatomy (Cấu trúc giải phẫu) của một khối Hàm chuẩn mực trong Python:

Một hàm Python chuẩn công nghiệp gồm có 7 thành phần cấu tạo:

```python
def tinh_tong_tien(don_gia, so_luong):
    """
    Tính toán tổng tiền thanh toán hóa đơn.
    """
    tong_tien = don_gia * so_luong
    return tong_tien
```

| Thành phần cấu trúc | Vai trò thực tế trong lập trình |
| :--- | :--- |
| **`def`** | Từ khóa bắt buộc báo hiệu cho Python biết ta chuẩn bị khai báo một hàm mới. |
| **`tinh_tong_tien`** | Tên của hàm, được đặt bằng chữ thường cách nhau bởi dấu gạch dưới (snake_case). |
| **`(don_gia, so_luong)`** | **Tham số (Parameters):** Các khe tiếp nhận thông tin đầu vào cho hàm. |
| **`:`** | Dấu hai chấm bắt buộc để mở ra khối lệnh của hàm (phải thụt lề 4 dấu cách bên dưới). |
| **`"""..."""`** | **Docstring:** Chuỗi văn bản mô tả chức năng của hàm, giúp IDE hiển thị gợi ý thông minh khi rê chuột vào. |
| **Body (Thân hàm)** | Khối logic thụt lề thực hiện các phép tính toán chính. |
| **`return`** | Từ khóa trả về giá trị đầu ra (kết quả) cho người gọi hàm sử dụng. |

### Cách gọi thực thi hàm (Function Call)
Khi bạn chỉ khai báo `def`, hàm vẫn nằm yên lặng trong bộ nhớ chưa chạy. Để đánh thức nó, bạn phải gọi tên hàm kèm theo dấu ngoặc đơn và truyền các giá trị thực tế vào:

```python
# Gọi hàm tinh_tong_tien với đơn giá 150000 và số lượng 3
hoa_don = tinh_tong_tien(150000, 3)
print(hoa_don)  # Kết quả: 450000
```

---

## 3️⃣ Thực Hành: Từng Bước Xây Dựng Những Khối Hàm Đầu Tiên

### 🛠️ 3.1 Hàm tối giản nhất: Không tham số đầu vào, không giá trị trả về
Dạng hàm này chỉ đơn thuần gom các lệnh in màn hình thông thường để tránh viết lại nhiều lần:

```python
def hien_thi_banner():
    print("========================================")
    print("       HỆ THỐNG QUẢN LÝ NHÂN SỰ         ")
    print("========================================")

# Gọi hàm chạy nhanh
hien_thi_banner()
```

---

### 🛠️ 3.2 Hàm có tiếp nhận tham số đầu vào
```python
# Biến 'ten' được gọi là Tham số (Parameter)
def chao_hoc_vien(ten):
    print(f"Chào mừng học viên {ten} đã quay trở lại!")

# Giá trị truyền vào "Nam" được gọi là Đối số (Argument)
chao_hoc_vien("Nam")
```

---

### 🛠️ 3.3 Cách truyền đối số theo vị trí (Positional) và theo tên (Keyword)

Khi hàm của bạn có nhiều tham số đầu vào, Python hỗ trợ hai cách truyền đối số vô cùng linh hoạt:

```python
def chia_keo(so_keo, so_nguoi):
    return so_keo / so_nguoi

# Cách 1: Truyền theo vị trí (Positional Arguments) - Bắt buộc đúng thứ tự
print(chia_keo(10, 2))  # Kết quả: 5.0 (10 cái kẹo chia cho 2 người)

# Cách 2: Truyền theo tên biến (Keyword Arguments) - Tự do đổi thứ tự cực kỳ rõ ràng
print(chia_keo(so_nguoi=2, so_keo=10))  # Kết quả vẫn là 5.0
```

> [!TIP]
> **Lời khuyên thực chiến từ Mr.Rom:**  
> Đối với các hàm có từ 3 tham số trở lên, bạn nên luôn luôn sử dụng **Keyword Arguments** (truyền theo tên biến) để giữ cho code luôn rõ ràng, mạch lạc, tránh việc người đọc code phải liên tục quay lại định nghĩa để xem biến nào đứng trước, biến nào đứng sau.

---

### 🛠️ 3.4 Thiết lập giá trị mặc định cho tham số (Default Parameters)
Giúp hàm trở nên vô cùng linh hoạt: Nếu người dùng không truyền giá trị vào thì hàm sẽ tự động lấy giá trị mặc định đã định nghĩa sẵn.

```python
# Thiết lập câu chào mặc định là "Chào bạn"
def gui_thong_bao(ten, loi_chao="Chào bạn"):
    print(f"{loi_chao}, {ten}!")

gui_thong_bao("Nam")                   # Lấy mặc định: Chào bạn, Nam!
gui_thong_bao("Bình", "Rất vui được gặp") # Ghi đè: Rất vui được gặp, Bình!
```

---

### 🛠️ 3.5 Sử dụng `*args` để truyền số lượng đối số vị trí không giới hạn (Tuple)
Khi bạn thiết kế một hàm tính toán nhưng không thể biết trước người dùng sẽ truyền vào bao nhiêu con số:

```python
# Dấu sao * giúp thu thập tất cả đối số truyền vào gom lại thành một Tuple
def tinh_tong_tat_ca(*danh_sach_so):
    tong = 0
    for so in danh_sach_so:
        tong += so
    return tong

print(tinh_tong_tat_ca(1, 2, 3))        # Kết quả: 6
print(tinh_tong_tat_ca(10, 20, 30, 40)) # Kết quả: 100
```

---

### 🛠️ 3.6 Sử dụng `**kwargs` để truyền số lượng đối số đặt tên không giới hạn (Dictionary)
Dấu hai sao `**` thu thập tất cả các đối số dạng đặt tên `key=value` truyền vào gom lại thành một Dictionary:

```python
def luu_ho_so_nhan_vien(**thong_tin):
    for key, value in thong_tin.items():
        print(f"Trường {key}: {value}")

luu_ho_so_nhan_vien(ten="Nam", tuoi=28, role="Leader", chi_nhanh="Hà Nội")
```

---

### 🛠️ 3.7 Cách sử dụng lệnh `return` để trả kết quả đầu ra

Từ khóa `return` có nhiệm vụ xuất giá trị kết quả của hàm ra ngoài và lập tức **kết thúc hoàn toàn** sự hoạt động của hàm đó (bỏ qua mọi dòng code phía dưới lệnh return).

#### Trả về nhiều giá trị cùng lúc cực kỳ dễ dàng:
Python tự động đóng gói nhiều giá trị trả về thành một Tuple và cho phép người gọi phân rã (unpack) cực đẹp:

```python
def tinh_toan_hinh_chu_nhat(dai, rong):
    chu_vi = (dai + rong) * 2
    dien_tich = dai * rong
    return chu_vi, dien_tich  # Trả về 2 giá trị cùng lúc dưới dạng Tuple

# Phân rã kết quả trả về trực tiếp thành 2 biến độc lập
cv, dt = tinh_toan_hinh_chu_nhat(10, 5)
print(f"Chu vi: {cv} | Diện tích: {dt}")
```

#### Sử dụng kỹ thuật Early Return (Thoát sớm để tránh lồng code)
Thay vì viết các cấu trúc `if/else` lồng nhau nhiều tầng phức tạp, hãy sử dụng `return` sớm để loại bỏ các trường hợp lỗi trước:

```python
# Style lồng if rườm rà:
def chia_so(a, b):
    if b != 0:
        return a / b
    else:
        return None

# Style Premium sử dụng Early Return cực gọn:
def chia_so_premium(a, b):
    if b == 0:
        return None  # Thoát hàm ngay lập tức nếu chia cho 0
    return a / b     # Logic chính nằm sạch đẹp ở ngoài không bị lồng lề
```

---

## 4️⃣ Phạm Vi Hoạt Động Của Biến (Scope): Ranh Giới Local Và Global

Biến trong Python được quản lý theo các phạm vi hoạt động cực kỳ nghiêm ngặt:

*   **Biến toàn cục (Global Scope):** Khai báo ở ngoài cùng của file code. Tất cả mọi nơi, bao gồm cả bên trong các hàm, đều có thể đọc được giá trị của biến này.
*   **Biến cục bộ (Local Scope):** Khai báo bên trong một hàm cụ thể. Biến này **chỉ tồn tại** và sử dụng được bên trong hàm đó. Khi hàm kết thúc chạy, biến này sẽ bị xóa sạch khỏi bộ nhớ.

```python
bien_global = 100    # Biến toàn cục

def test_scope():
    bien_local = 50  # Biến cục bộ
    print(bien_global)  # Đọc biến global thoải mái
    print(bien_local)   # Đọc biến local thoải mái

test_scope()
print(bien_local)   # ❌ Sụp đổ ngay! Lỗi NameError vì bien_local không hề tồn tại ở ngoài hàm
```

> [!WARNING]
> **Tránh lạm dụng từ khóa `global` để sửa đổi biến toàn cục:**  
> Python cho phép bạn dùng từ khóa `global bien_global` bên trong hàm để sửa đổi trực tiếp biến ngoài hệ thống. Tuy nhiên, trong môi trường làm việc chuyên nghiệp, việc này được ví như một "tội ác" vì nó gây ra các side-effect (tác dụng phụ ngầm) cực kỳ khó kiểm soát và khó debug.  
> **Giải pháp chuẩn mực:** Hãy thiết kế hàm nhận dữ liệu qua tham số đầu vào và trả kết quả ra ngoài qua `return` (được gọi là *Pure Function* - Hàm thuần khiết).

---

## 5️⃣ Docstring Và Type Hints: Nghệ Thuật Viết Hàm Tự Giải Thích Bản Thân

Trong dự án lớn, code của bạn sẽ được đọc bởi nhiều người khác. Hãy sử dụng Docstring và Type Hints để biến hàm của bạn thành một tác phẩm nghệ thuật tự giải thích bản thân.

```python
# Type Hints: Khai báo tham số phai là float, và kết quả trả về cũng là float
def tinh_bmi(can_nhat: float, chieu_cao: float) -> float:
    """
    Tính toán chỉ số khối cơ thể BMI.
    
    Args:
        can_nhat: Cân nặng tính bằng kg.
        chieu_cao: Chiều cao tính bằng mét.
        
    Returns:
        Chỉ số BMI định dạng số thực.
    """
    return can_nhat / (chieu_cao ** 2)
```

Khi bạn gõ hàm `tinh_bmi` ở một file khác trong VS Code và mở dấu ngoặc đơn, VS Code sẽ tự động hiển thị một khung popup cực kỳ Premium giải thích chi tiết toàn bộ các dòng ghi chú trên để người dùng sử dụng chính xác 100%!

---

## 6️⃣ Hàm Vô Danh Lambda: Giải Pháp Nhanh Cho Những Logic Một Dòng

Hàm **Lambda** là dạng hàm ẩn danh (không có tên gọi), được viết cực kỳ ngắn gọn trên một dòng duy nhất để phục vụ cho các tính toán nhanh tức thì.

Cú pháp: `lambda <tham_số>: <biểu_thức_tính>`

```python
# Định nghĩa hàm tính bình phương thông thường:
def binh_phuong(x):
    return x ** 2

# Viết gọn lại bằng Lambda:
binh_phuong_lambda = lambda x: x ** 2

print(binh_phuong_lambda(5))  # Kết quả: 25
```

### Ứng dụng thực tế tuyệt vời của Lambda trong việc sắp xếp dữ liệu phức tạp:
Hàm Lambda cực mạnh khi dùng làm tham số trung gian cho các hàm hệ thống như `sorted()`:

```python
ds_hoc_vien = [
    {"ten": "Nam", "diem": 85},
    {"ten": "Bình", "diem": 95},
    {"ten": "Cường", "diem": 90}
]

# Sắp xếp học viên theo thứ tự điểm số tăng dần bằng cách truyền hàm lambda trỏ vào trường 'diem'
ds_sap_xep = sorted(ds_hoc_vien, key=lambda hoc_vien: hoc_vien["diem"])
print(ds_sap_xep)
# Kết quả sắp xếp đúng chuẩn: Nam (85) -> Cường (90) -> Bình (95)
```

---

## 🛠️ Giải Quyết Bài Toán Thực Tế: Tái Cấu Trúc Script Tính Lương Bằng Hàm

Bây giờ, chúng ta sẽ áp dụng toàn bộ nghệ thuật thiết kế Hàm, Docstring, Type Hints để tái cấu trúc lại toàn bộ hệ thống tính toán lương bậc thang của công ty. Chúng ta sẽ đóng gói toàn bộ logic phức tạp vào trong một hàm duy nhất và gọi sử dụng lặp đi lặp lại một cách cực kỳ ngăn nắp!

Hãy tạo file `tinh_luong_chuyen_nghiep.py` và chạy đoạn code đỉnh cao sau:

```python
# tinh_luong_chuyen_nghiep.py - Hệ thống quản lý lương sử dụng hàm chuyên nghiệp
# Tác giả: Mr.Rom

# Bước 1: Định nghĩa hàm xử lý lõi (Core Logic) đạt chuẩn Premium 5 sao
def tinh_luong_thuc_nhan(ten: str, luong_gio: float, gio_lam: float) -> dict:
    """
    Tính toán chi tiết tổng lương gốc, thuế bậc thang và số tiền thực nhận của nhân viên.
    
    Args:
        ten: Họ và tên nhân viên.
        luong_gio: Mức lương tính theo giờ (VND).
        gio_lam: Tổng số giờ làm việc thực tế trong tháng.
        
    Returns:
        Một Dictionary chứa đầy đủ kết quả báo cáo chi tiết đã tính toán.
    """
    # Tính lương gốc
    luong_goc = luong_gio * gio_lam
    
    # Áp dụng công thức thuế bậc thang chuẩn quy định
    if luong_goc < 5000000:
        thue_suat = 0.0
    elif luong_goc <= 10000000:
        thue_suat = 0.10
    elif luong_goc <= 20000000:
        thue_suat = 0.15
    else:
        thue_suat = 0.20
        
    # Tính toán chi tiết
    tien_thue = luong_goc * thue_suat
    thuc_nhan = luong_goc - tien_thue
    
    # Đóng gói kết quả trả về
    return {
        "nhan_vien": ten,
        "luong_goc": luong_goc,
        "thue_suat": thue_suat,
        "tien_thue": tien_thue,
        "thuc_nhan": thuc_nhan
    }

# Bước 2: Chuẩn bị dữ liệu danh sách nhân viên
danh_sach_nhan_vien = [
    {"ten": "Nguyễn Văn Nam", "luong_gio": 150000, "gio_lam": 160},
    {"ten": "Trần Thị Bình", "luong_gio": 80000, "gio_lam": 50},
    {"ten": "Lê Văn Cường", "luong_gio": 200000, "gio_lam": 120}
]

# Bước 3: Duyệt và gọi hàm xử lý cực kỳ ngắn gọn, sạch đẹp
print("=========================================================================")
print("                   BẢNG LƯƠNG NHÂN VIÊN (DÙNG HÀM)                      ")
print("=========================================================================")

for nv in danh_sach_nhan_vien:
    # Gọi hàm xử lý lõi và nhận về dictionary kết quả
    bao_cao = tinh_luong_thuc_nhan(
        ten=nv["ten"],
        luong_gio=nv["luong_gio"],
        gio_lam=nv["gio_lam"]
    )
    
    # In báo cáo ra màn hình
    print(f"Nhân viên: {bao_cao['nhan_vien']:<15} | "
          f"Lương gốc: {bao_cao['luong_goc']:>10:,.0f} VND | "
          f"Thuế ({bao_cao['thue_suat']*100:>2.0f}%): {bao_cao['tien_thue']:>9:,.0f} VND | "
          f"Thực nhận: {bao_cao['thuc_nhan']:>10:,.0f} VND")

print("=========================================================================")
```

Hãy mở Terminal và gõ: `python3 tinh_luong_chuyen_nghiep.py`. 
Bạn sẽ thấy code chạy vô cùng mượt mà. Hãy để ý xem phần thân của vòng lặp `for` bây giờ đã trở nên ngắn gọn và dễ hiểu đến mức nào! Bất kỳ ai nhìn vào cũng có thể hiểu ngay chương trình đang làm gì. Đó chính là sức mạnh kỳ diệu của việc thiết kế Hàm!

---

## ⚡ Những "Cạm Bẫy" Thiết Kế Hàm Kinh Điển Và Tiêu Chuẩn Viết Code Chuẩn Mực

### ❌ Cạm bẫy 1: Thiết lập giá trị mặc định là một kiểu dữ liệu có thể sửa đổi (Mutable Default Parameter)
```python
def them_san_pham(ma_sp, danh_sach=[]):  # ❌ CỰC KỲ NGUY HIỂM!
    danh_sach.append(ma_sp)
    return danh_sach
```
*   **Nguyên nhân:** Danh sách mặc định `[]` chỉ được khởi tạo **đúng 1 lần duy nhất** khi chương trình nạp hàm vào bộ nhớ RAM. Các lượt gọi hàm sau đó nếu không truyền danh sách vào sẽ dùng chung (chia sẻ) vùng nhớ này, dẫn đến dữ liệu của các lượt gọi bị trộn lẫn vào nhau!
*   **Giải pháp chuẩn mực:** Hãy đặt giá trị mặc định là `None` và khởi tạo list mới an toàn bên trong thân hàm:
    ```python
    def them_san_pham_safe(ma_sp, danh_sach=None):
        if danh_sach is None:
            danh_sach = []
        danh_sach.append(ma_sp)
        return danh_sach
    ```

### ❌ Cạm bẫy 2: Hàm quá dài và ôm đồm quá nhiều nhiệm vụ (God Function)
Một hàm dài hơn 100 dòng code xử lý từ xác thực thông tin, ghi file, gửi email cho đến ghi nhận vào cơ sở dữ liệu sẽ vô cùng khó đọc, khó kiểm thử và cực kỳ dễ sinh lỗi.
*   **Giải pháp:** Áp dụng nguyên tắc **Single Responsibility (Đơn nhiệm)**: Một hàm chỉ nên làm duy nhất một nhiệm vụ và làm thật xuất sắc nhiệm vụ đó. Nếu hàm quá dài, hãy chủ động phân tách nó ra thành 3 - 4 hàm con nhỏ độc lập.

---

## 🧠 Thử Thách Trí Tuệ: Kiểm Tra Kiến Thức Của Bạn

**Câu hỏi 1:** Điều gì xảy ra nếu một hàm trong Python chạy hết các dòng lệnh mà hoàn toàn không có lệnh `return` nào?
<details>
<summary>💡 Xem lời giải thích từ Mr.Rom</summary>

Khi một hàm không có lệnh `return` cụ thể (hoặc chỉ có từ khóa `return` trống rỗng không đi kèm giá trị), Python sẽ tự động trả về giá trị đặc biệt **`None`** (đại diện cho giá trị rỗng, kiểu dữ liệu `NoneType`).
</details>

**Câu hỏi 2:** Sự khác biệt giữa `*args` và `**kwargs` khi định nghĩa hàm là gì?
<details>
<summary>💡 Xem lời giải thích từ Mr.Rom</summary>

*   `*args` dùng để gom tất cả các đối số truyền theo vị trí (*Positional*) chưa được chỉ định thành một **Tuple**.
*   `**kwargs` dùng để gom tất cả các đối số truyền theo tên biến (*Keyword*) chưa được định nghĩa trước thành một **Dictionary**.
</details>

---

## 📋 Bảng Tra Cứu Nhanh (Cheatsheet) Về Thiết Kế Hàm

```python
# 1. Khai báo hàm chuẩn mực đầy đủ Docstring và Type Hints
def tinh_luong_net(gross: float, thue: float = 0.10) -> float:
    """Tính lương thực nhận sau khi trừ thuế thu nhập."""
    if gross <= 0:
        return 0.0  # Early Return
    return gross * (1 - thue)

# 2. Truyền tham số không giới hạn
def log_thong_tin(*messages, **metadata):
    # messages là tuple, metadata là dict
    print(f"Báo cáo: {messages} | Siêu dữ liệu: {metadata}")

# 3. Viết nhanh hàm vô danh Lambda
tinh_thue_nhanh = lambda gross: gross * 0.10
```

---

## 📚 Thuật Ngữ Cần Nhớ (Glossary)

*   **Function (Hàm):** Khối mã nguồn có tên dùng để đóng gói logic tái sử dụng.
*   **Parameter (Tham số):** Biến được định nghĩa trong khai báo của hàm để tiếp nhận dữ liệu đầu vào.
*   **Argument (Đối số):** Giá trị thực tế được truyền vào tham số của hàm khi gọi thực thi.
*   **Positional Argument (Đối số vị trí):** Đối số được truyền theo đúng thứ tự sắp đặt của các tham số.
*   **Keyword Argument (Đối số từ khóa):** Đối số được truyền bằng cách chỉ định rõ ràng tên tham số (`ten_bien=gia_tri`).
*   **Docstring:** Chuỗi văn bản bọc trong ba dấu nháy kép đặt đầu hàm để viết tài liệu hướng dẫn.
*   **Pure Function (Hàm thuần khiết):** Hàm chỉ xử lý dựa trên tham số đầu vào và trả kết quả ra ngoài, hoàn toàn không làm thay đổi bất kỳ trạng thái hay biến nào ở môi trường bên ngoài.

---

## 🔗 Liên kết & Tài nguyên học tập tiếp theo

### 🧭 Định hướng lộ trình học:
*   ⬅️ **Bài trước:** [Bài 02: Làm chủ Cấu trúc rẽ nhánh và Vòng lặp](./02_control-flow.md)
*   ➡️ **Bài tiếp theo:** [Bài 04: Thao tác File & Hệ thống Xử lý ngoại lệ IO (Sắp ra mắt)](#)
*   🧭 **Tấm bản đồ tổng quan:** [Zero to Coder Career Roadmap](../../../../00_roadmaps/career/zero-to-coder_career-roadmap.md)

### 🌐 Tài nguyên học tập chất lượng bên ngoài:
*   [Defining Your Own Functions in Python](https://realpython.com/defining-your-own-python-function/) — Hướng dẫn chi tiết từ Real Python.
*   [Python Functions - W3Schools](https://www.w3schools.com/python/python_functions.asp) — Thực hành tương tác hàm cơ bản.
*   [PEP 257 Docstring Conventions](https://peps.python.org/pep-0257/) — Tiêu chuẩn viết docstring của Python Software Foundation.
