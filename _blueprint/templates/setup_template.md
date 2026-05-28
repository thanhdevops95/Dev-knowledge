# <Tool / Software / Extension> — Cài đặt chi tiết

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** DD/MM/YYYY\
> **Cập nhật:** DD/MM/YYYY\
> **OS hỗ trợ:** macOS / Linux / Windows (chỉ rõ phiên bản min)\
> **Thời lượng cài:** ~X phút\
> **Khó:** ⭐ Easy / ⭐⭐ Medium / ⭐⭐⭐ Hard

> 🎯 *<1-2 câu: tool này là gì, dùng làm gì. Người mới đọc xong block này biết "có cần cài không".>*

---

## 1️⃣ <Tool> là gì + Khi nào cài

<Giới thiệu ngắn — 1 đoạn>

**Khi nào nên cài:**
- ✅ <Use case 1>
- ✅ <Use case 2>

**Khi nào KHÔNG cần (dùng cái khác):**
- ❌ <Anti-use case> → dùng [<alternative>](./<other-setup>.md)

---

## 2️⃣ Yêu cầu hệ thống

| Yêu cầu | Min | Recommend |
|---|---|---|
| OS | <vd: macOS 12+> | <vd: macOS 14+> |
| RAM | 4 GB | 8 GB+ |
| Disk | 500 MB | 2 GB+ |
| Prerequisites | <vd: Xcode CLI tools> | <vd: Xcode + Homebrew> |

---

## 3️⃣ Cách cài — chọn 1 trong N option

### So sánh nhanh

| Option | Cách | Khi nào dùng | Khó |
|---|---|---|---|
| 🅰️ **<Option A>** | <vd: Homebrew> | Đơn giản nhất, dễ update | ⭐ |
| 🅱️ **<Option B>** | <vd: DMG installer> | Khi không có Homebrew | ⭐ |
| 🅲 **<Option C>** | <vd: Build from source> | Cần version mới nhất / customize | ⭐⭐⭐ |

→ Mình recommend **<option A>** cho beginner.

---

### 🅰️ Option A: <Cách 1>

**Phù hợp**: <ai/tình huống>

**Bước 1**: <prerequisite nếu cần>

```bash
<command>
```

**Bước 2**: <cài>

```bash
<command>
```

Output mong đợi:

```
<output mẫu>
```

**Pros**: <điểm mạnh>\
**Cons**: <điểm yếu>

---

### 🅱️ Option B: <Cách 2>

(tương tự cấu trúc Option A)

---

### 🅲 Option C: <Cách 3>

(tương tự)

---

## 4️⃣ Verify cài đúng

```bash
<command kiểm tra version hoặc tool đã có>
```

Output mong đợi:

```
<version string hoặc help text>
```

Nếu **không** ra output như trên → xem [§7 Lỗi thường gặp](#7️⃣-lỗi-thường-gặp).

---

## 5️⃣ Cấu hình ban đầu (settings)

### Cấu hình tối thiểu (BẮT BUỘC)

```bash
<command set config>
```

Hoặc edit file `~/.config/<tool>/config`:

```
<config content>
```

### Cấu hình recommend (tùy chọn)

| Setting | Giá trị | Vì sao |
|---|---|---|
| `<key1>` | `<value>` | <reason> |
| `<key2>` | `<value>` | <reason> |

---

## 6️⃣ Extensions / Plugins phổ biến

<!-- Section này có khi tool support extension (VS Code, Vim, browser, ...). Bỏ nếu không áp dụng. -->

| Extension | Chức năng | Nên cài? |
|---|---|---|
| <name 1> | <làm gì> | 🌟 Must-have |
| <name 2> | <làm gì> | ✅ Recommend |
| <name 3> | <làm gì> | 🟡 Optional |
| <name 4> | <làm gì> | ❌ Skip (lý do) |

### Cài extension

```bash
<command cài>
```

---

## 7️⃣ Lỗi thường gặp

### ❌ Lỗi 1: `<error message>`

- **Triệu chứng**: <mô tả>
- **Nguyên nhân**: <vì sao>
- **Cách fix**:
  ```bash
  <command fix>
  ```

### ❌ Lỗi 2: `<error message>`

(tương tự)

### ❌ Lỗi 3: `<error message>`

(tương tự)

---

## 8️⃣ Update + Uninstall

### Update lên version mới

```bash
<command update>
```

### Uninstall hoàn toàn

```bash
<command uninstall>
```

> ⚠️ **Cẩn thận**: <điểm cần lưu ý khi uninstall — vd: data có bị xóa không, config có bị giữ không>

---

## 9️⃣ Khi nào KHÔNG nên dùng + Alternative

| Tool | So sánh | Phù hợp ai |
|---|---|---|
| **<tool đang nói>** | <strength> | <ai> |
| <Alternative 1> | <strength> | <ai> |
| <Alternative 2> | <strength> | <ai> |

---

## 🔗 Liên kết

### Bài học dùng tool này
- [<Lesson 1>](../../<L1>/<L2>/lessons/01_basic/<file>.md)
- [<Lesson 2>](...)

### Tài nguyên ngoài
- [<Official docs>](<URL>) — chi tiết option cài
- [<Awesome list>](<URL>) — extension/plugin tổng hợp
- [<Community forum>](<URL>) — hỏi đáp khi gặp lỗi không có trong §7

---

## 📌 Changelog

- **v1.0.0 (DD/MM/YYYY)** — Bản đầu tiên.
