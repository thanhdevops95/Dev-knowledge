# 🔢 Hệ thống số — Binary, Hex, Float

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu cách máy tính biểu diễn số và tại sao 0.1 + 0.2 ≠ 0.3

---

## Tại sao cần học điều này?

- Tại sao `0.1 + 0.2 == 0.30000000000000004` trong JavaScript?
- Tại sao mã màu CSS là `#FF5733`?
- Tại sao IP address là 4 số từ 0-255?
- `int` chứa được số lớn nhất bao nhiêu?

Tất cả liên quan đến cách máy tính **biểu diễn số**.

---

## 1. Hệ nhị phân (Binary) — Nền tảng mọi thứ

Máy tính chỉ hiểu **0** và **1** (on/off, true/false). Mọi dữ liệu đều là binary.

```
Hệ 10 (quen thuộc):  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11...
Hệ  2 (binary):      0, 1, 10, 11, 100, 101, 110, 111, 1000...

Ví dụ: 13 trong binary
13 = 8 + 4 + 0 + 1
   = 1×2³ + 1×2² + 0×2¹ + 1×2⁰
   = 1101₂
```

**Đổi decimal → binary:** Chia liên tục cho 2, lấy dư từ dưới lên:

```
13 ÷ 2 = 6 dư 1  ↑
 6 ÷ 2 = 3 dư 0  │
 3 ÷ 2 = 1 dư 1  │ Đọc từ dưới lên
 1 ÷ 2 = 0 dư 1  │
                  → 1101
```

**Đơn vị:**
- **1 bit** = 0 hoặc 1
- **1 byte** = 8 bits → biểu diễn 0-255 (2⁸ = 256 giá trị)
- **1 KB** = 1024 bytes
- **1 MB** = 1024 KB
- **1 GB** = 1024 MB

---

## 2. Hệ thập lục phân (Hexadecimal)

Hex dùng **16 ký tự**: 0-9 và A-F. Gọn hơn binary rất nhiều.

```
Dec:  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15
Hex:  0  1  2  3  4  5  6  7  8  9   A   B   C   D   E   F
Bin: 0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111
```

**1 ký tự hex = 4 bits**, 2 ký tự hex = 1 byte. Vì vậy hex rất phổ biến:

```
Mã màu CSS:  #FF5733
             FF = 255 (Red)
             57 = 87  (Green)
             33 = 51  (Blue)

Địa chỉ bộ nhớ: 0x7FFE42A0

MAC address: 00:1A:2B:3C:4D:5E

Unicode: U+1F600 = 😀
```

---

## 3. Hệ bát phân (Octal)

Dùng 8 ký tự (0-7). Ít gặp, nhưng Linux permissions dùng octal:

```
chmod 755 file.sh

7 = rwx (read + write + execute)   cho owner
5 = r-x (read + execute)           cho group
5 = r-x (read + execute)           cho others

7 = 111₂ = 4+2+1
5 = 101₂ = 4+0+1
```

---

## 4. Số nguyên có dấu — Two's Complement

Máy tính dùng **two's complement** để biểu diễn số âm:

```
Với 8 bits (1 byte):
 0 = 00000000
 1 = 00000001
 127 = 01111111  ← Giá trị dương lớn nhất

-1 = 11111111    ← Đảo bit + cộng 1
-2 = 11111110
-128 = 10000000  ← Giá trị âm nhỏ nhất
```

**Phạm vi số nguyên:**

| Kiểu | Bits | Phạm vi | Giá trị max |
|---|---|---|---|
| `int8` | 8 | -128 → 127 | 127 |
| `int16` | 16 | -32,768 → 32,767 | ~32K |
| `int32` | 32 | -2.1 tỷ → 2.1 tỷ | ~2.1B |
| `int64` | 64 | -9.2×10¹⁸ → 9.2×10¹⁸ | ~9 triệu triệu triệu |
| `uint8` | 8 | 0 → 255 | 255 |
| `uint32` | 32 | 0 → 4.29 tỷ | ~4.3B |

> ⚠️ **Integer Overflow:** Khi vượt quá giới hạn, số "quay vòng" — `127 + 1 = -128` (int8)!

---

## 5. Số thực — IEEE 754 (Floating Point)

Đây là lý do `0.1 + 0.2 ≠ 0.3`:

```
Cấu trúc float 64-bit (double):
┌──┬───────────┬──────────────────────────────────────────────┐
│S │ Exponent  │                Mantissa (Fraction)           │
│1 │  11 bits  │                52 bits                       │
└──┴───────────┴──────────────────────────────────────────────┘
 Sign                              
 0 = dương
 1 = âm
```

**Vấn đề:** Nhiều số thập phân **không thể biểu diễn chính xác** trong binary:

```python
# 0.1 trong binary = 0.000110011001100110011... (lặp vô hạn!)
>>> 0.1 + 0.2
0.30000000000000004

>>> 0.1 + 0.2 == 0.3
False
```

**Cách xử lý:**

```python
# Cách 1: So sánh với epsilon
abs(0.1 + 0.2 - 0.3) < 1e-9  # True

# Cách 2: Dùng Decimal (chính xác cho tiền tệ!)
from decimal import Decimal
Decimal('0.1') + Decimal('0.2') == Decimal('0.3')  # True

# Cách 3: Lưu tiền bằng số nguyên (cents)
total = 10 + 20  # 10 cents + 20 cents = 30 cents
```

**Giá trị đặc biệt:**

| Giá trị | Ý nghĩa | Ví dụ |
|---|---|---|
| `Infinity` | Vô cực | `1.0 / 0.0` |
| `-Infinity` | Âm vô cực | `-1.0 / 0.0` |
| `NaN` | Not a Number | `0.0 / 0.0`, `sqrt(-1)` |

```python
>>> float('inf') > 999999999
True

>>> float('nan') == float('nan')
False  # NaN không bằng chính nó!
```

---

## 6. Phép toán Bitwise

Thao tác trực tiếp trên từng bit — cực nhanh:

| Phép | Ký hiệu | Ví dụ (5 = 101, 3 = 011) | Kết quả |
|---|---|---|---|
| AND | `&` | `101 & 011` | `001` (1) |
| OR | `\|` | `101 \| 011` | `111` (7) |
| XOR | `^` | `101 ^ 011` | `110` (6) |
| NOT | `~` | `~101` | `010` (đảo) |
| Left Shift | `<<` | `101 << 1` | `1010` (10) |
| Right Shift | `>>` | `101 >> 1` | `10` (2) |

**Tricks phổ biến:**

```python
# Kiểm tra chẵn/lẻ (nhanh hơn n % 2)
n & 1 == 0  # Chẵn
n & 1 == 1  # Lẻ

# Nhân/chia 2 bằng shift (nhanh hơn * /)
n << 1      # n × 2
n >> 1      # n ÷ 2 (làm tròn xuống)

# Kiểm tra lũy thừa 2
n > 0 and (n & (n - 1)) == 0  # True nếu n = 2^k

# Swap 2 số không cần biến tạm
a ^= b; b ^= a; a ^= b
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng float để lưu tiền → 19.99 + 0.01 = 20.000000000001
✅ Đúng: Dùng integer (cents) hoặc Decimal

❌ Sai: So sánh float bằng == 
✅ Đúng: Dùng abs(a - b) < epsilon

❌ Sai: Quên overflow → Y2K bug (năm 2000), Unix 2038 problem
✅ Đúng: Chọn kiểu dữ liệu đủ lớn, validate input
```

---

## Bài tập thực hành

- [ ] Đổi thủ công: 42 → binary → hex → octal
- [ ] Giải thích tại sao `0.1 + 0.2 != 0.3` bằng code Python
- [ ] Viết hàm kiểm tra số có phải lũy thừa 2 không (dùng bitwise)
- [ ] Tính chmod `644` nghĩa là gì? Owner/Group/Others có quyền gì?

---

## Tài nguyên thêm

- [Floating Point Visually Explained](https://fabiensanglard.net/floating_point_visually_explained/) — Minh họa IEEE 754
- [Two's Complement (Wikipedia)](https://en.wikipedia.org/wiki/Two%27s_complement) — Giải thích chi tiết
- [What Every Programmer Should Know About Floating-Point](https://floating-point-gui.de/) — Tổng hợp vấn đề float
