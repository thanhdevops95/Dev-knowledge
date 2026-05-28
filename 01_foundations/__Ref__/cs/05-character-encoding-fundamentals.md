# 🔤 Character Encoding — Mã hóa ký tự

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu tại sao chữ tiếng Việt đôi khi bị lỗi hiển thị

---

## Tại sao cần học điều này?

Bạn đã bao giờ gặp:
- Mở file thấy `Xin chÃ o` thay vì `Xin chào`?
- Email gửi đi bị lỗi ký tự tiếng Việt?
- Database lưu emoji 💀 thành `????`?

Tất cả do **encoding không đúng**. Hiểu encoding = hết lỗi ký tự.

---

## 1. Máy tính chỉ hiểu số

Máy tính chỉ hiểu **0 và 1** (binary). Để hiển thị chữ, cần bảng quy ước:

```
Ký tự → Số (code point) → Binary → Hiển thị

  'A'  →  65             → 01000001  → A
  'a'  →  97             → 01100001  → a
  '0'  →  48             → 00110000  → 0
  '€'  →  8364           → ...       → €
  '🎉' → 127881          → ...       → 🎉
```

---

## 2. ASCII — Bảng mã đầu tiên (1963)

**ASCII** (American Standard Code for Information Interchange) dùng **7 bit** → 128 ký tự.

```
Bảng ASCII quan trọng:
┌────────┬────────┬────────┬────────┐
│ Ký tự  │  Dec   │  Hex   │  Ghi chú│
├────────┼────────┼────────┼────────┤
│  0-9   │ 48-57  │ 30-39  │ Số     │
│  A-Z   │ 65-90  │ 41-5A  │ In hoa │
│  a-z   │ 97-122 │ 61-7A  │ Thường │
│ Space  │  32    │  20    │ Khoảng trắng │
│ \n     │  10    │  0A    │ Xuống dòng   │
│ \0     │   0    │  00    │ Null (kết thúc string) │
└────────┴────────┴────────┴────────┘
```

**Giới hạn:** Chỉ có tiếng Anh! Không có: à, á, ả, ã, ạ, ü, ñ, 你, 🎉

---

## 3. Unicode — Giải pháp cho mọi ngôn ngữ

**Unicode** gán mỗi ký tự trên thế giới 1 **code point** duy nhất:

```
U+0041  →  A        (Latin)
U+00E0  →  à        (Tiếng Việt)
U+4E2D  →  中       (Tiếng Trung)
U+0410  →  А        (Tiếng Nga)
U+1F600 →  😀       (Emoji)
```

> Unicode hiện có **149,813 ký tự** từ **161 hệ chữ viết**!

**Nhưng Unicode chỉ là bảng mã (code points)** — cần **encoding** để lưu thành bytes.

---

## 4. UTF-8 — Encoding phổ biến nhất (dùng luôn cái này!)

UTF-8 dùng **1-4 bytes** tùy ký tự — tiết kiệm cho tiếng Anh, hỗ trợ mọi ngôn ngữ:

```
Ký tự    Code Point    UTF-8 Bytes      Số bytes
─────    ──────────    ───────────      ────────
  A       U+0041       41               1 byte
  à       U+00E0       C3 A0            2 bytes
  中      U+4E2D       E4 B8 AD         3 bytes
  😀      U+1F600      F0 9F 98 80      4 bytes
```

**Quy tắc UTF-8:**

| Bytes | Dạng binary | Phạm vi |
|---|---|---|
| 1 | `0xxxxxxx` | ASCII (U+0000 → U+007F) |
| 2 | `110xxxxx 10xxxxxx` | Latin mở rộng, Việt |
| 3 | `1110xxxx 10xxxxxx 10xxxxxx` | CJK (Trung, Nhật, Hàn) |
| 4 | `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx` | Emoji, ký tự hiếm |

> 💡 **Quy tắc vàng:** Luôn dùng **UTF-8** cho mọi thứ — code, database, API, file.

---

## 5. So sánh các encoding

| Encoding | Bytes/ký tự | Đặc điểm |
|---|---|---|
| **ASCII** | 1 | Chỉ tiếng Anh, 128 ký tự |
| **UTF-8** | 1-4 | **Chuẩn internet** — tương thích ASCII |
| **UTF-16** | 2-4 | Dùng trong JavaScript, Java, Windows |
| **UTF-32** | 4 | Mỗi ký tự đều 4 bytes — đơn giản nhưng tốn bộ nhớ |
| **ISO-8859-1** | 1 | Tây Âu (Latin-1) — không hỗ trợ tiếng Việt |
| **Windows-1252** | 1 | Giống ISO-8859-1 nhưng thêm vài ký tự |

---

## 6. Base64 — Mã hóa binary thành text

Khi cần gửi dữ liệu binary (ảnh, file) qua kênh text-only (email, JSON):

```
Binary data:  01001000 01100101 01101100 01101100 01101111
                    ↓ Base64 encode ↓
Text:         "SGVsbG8="

Dùng bảng: A-Z (0-25), a-z (26-51), 0-9 (52-61), + (62), / (63)
Padding:   = khi cần đệm cho đủ 3 bytes
```

```python
import base64

# Encode
encoded = base64.b64encode(b"Hello World")
print(encoded)   # b'SGVsbG8gV29ybGQ='

# Decode
decoded = base64.b64decode(encoded)
print(decoded)   # b'Hello World'
```

**Base64 KHÔNG phải mã hóa bảo mật!** Ai cũng có thể decode.

---

## 7. BOM (Byte Order Mark)

BOM là bytes đặc biệt ở đầu file để chỉ encoding:

| Encoding | BOM bytes |
|---|---|
| UTF-8 | `EF BB BF` (thường không cần) |
| UTF-16 BE | `FE FF` |
| UTF-16 LE | `FF FE` |

> ⚠️ UTF-8 **không nên** có BOM. Nếu thấy file có `\xEF\xBB\xBF` ở đầu → xóa đi.

---

## 8. Các bug thường gặp (Mojibake)

**Mojibake** = hiển thị ký tự sai do encoding không khớp:

```
# Bug 1: Mở file UTF-8 bằng encoding Latin-1
"Xin chào"  →  "Xin chÃ o"

# Bug 2: Database không dùng utf8mb4
"Hello 😀"  →  "Hello ????"

# Bug 3: Python 2 không xử lý Unicode
>>> "Việt Nam"  →  UnicodeError! 💥
```

**Cách fix:**

```python
# Luôn khai báo encoding khi mở file
with open("data.txt", encoding="utf-8") as f:
    text = f.read()

# MySQL: dùng utf8mb4 (không phải utf8!)
# CREATE DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# HTTP response: set header
# Content-Type: text/html; charset=utf-8
```

---

## Các lỗi thường gặp

```
❌ Sai: "UTF-8 và Unicode là cùng 1 thứ"
✅ Đúng: Unicode = bảng mã (số), UTF-8 = cách lưu số đó thành bytes

❌ Sai: Dùng MySQL "utf8" cho emoji
✅ Đúng: MySQL "utf8" chỉ hỗ trợ 3 bytes → Dùng "utf8mb4" (4 bytes cho emoji)

❌ Sai: "len('café') = 4"
✅ Đúng: Tùy encoding — len tính bytes hay ký tự? Python 3: 4 ký tự, nhưng 5 bytes UTF-8
```

---

## Bài tập thực hành

- [ ] Kiểm tra encoding của file bất kỳ bằng `file -i tên_file` (Linux) hoặc Notepad++ → Encoding menu
- [ ] Viết script Python đổi encoding file từ Latin-1 sang UTF-8
- [ ] Tạo chuỗi có emoji, Base64 encode rồi decode lại
- [ ] Mở cùng 1 file bằng 2 encoding khác nhau → quan sát mojibake

---

## Tài nguyên thêm

- [The Absolute Minimum Every Developer Must Know About Unicode](https://tonsky.me/blog/unicode/) — Giải thích hay nhất
- [UTF-8 Everywhere](https://utf8everywhere.org/) — Tại sao UTF-8 là chuẩn duy nhất nên dùng
- [Unicode Table](https://unicode-table.com/) — Tra cứu mọi ký tự Unicode
