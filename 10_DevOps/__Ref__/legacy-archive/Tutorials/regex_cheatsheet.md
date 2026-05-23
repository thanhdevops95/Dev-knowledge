# Regex Cheatsheet

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Regular Expression (Regex) là pattern để tìm kiếm và thao tác với văn bản.

---

## 🔤**KÝ TỰ CƠ BẢN**

| Pattern | Ý nghĩa | Ví dụ match |
|---------|---------|-------------|
| `a` | Ký tự 'a' | a |
| `abc` | Chuỗi 'abc' | abc |
| `.` | Bất kỳ ký tự nào (trừ newline) | a, b, 1, @ |
| `\.` | Dấu chấm literal | . |

---

## 🔢**LƯỢNG TỬ (QUANTIFIERS)**

| Pattern | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| `a*` | 0 hoặc nhiều 'a' | "", a, aa, aaa |
| `a+` | 1 hoặc nhiều 'a' | a, aa, aaa |
| `a?` | 0 hoặc 1 'a' | "", a |
| `a{3}` | Chính xác 3 'a' | aaa |
| `a{2,4}` | Từ 2 đến 4 'a' | aa, aaa, aaaa |
| `a{2,}` | Ít nhất 2 'a' | aa, aaa, aaaa... |

### Greedy vs Non-greedy

| Pattern | Ý nghĩa |
|---------|---------|
| `a*` | Greedy (lấy nhiều nhất có thể) |
| `a*?` | Non-greedy (lấy ít nhất có thể) |
| `a+?` | Non-greedy + |

---

## 📦**NHÓM KÝ TỰ (CHARACTER CLASSES)**

| Pattern | Ý nghĩa | Tương đương |
|---------|---------|-------------|
| `[abc]` | a hoặc b hoặc c | |
| `[^abc]` | Không phải a, b, c | |
| `[a-z]` | Chữ thường | |
| `[A-Z]` | Chữ hoa | |
| `[0-9]` | Số | |
| `[a-zA-Z]` | Chữ cái | |
| `[a-zA-Z0-9]` | Chữ và số | |

### Shorthand Classes

| Pattern | Ý nghĩa | Tương đương |
|---------|---------|-------------|
| `\d` | Số | `[0-9]` |
| `\D` | Không phải số | `[^0-9]` |
| `\w` | Word character | `[a-zA-Z0-9_]` |
| `\W` | Không phải word | `[^a-zA-Z0-9_]` |
| `\s` | Whitespace | `[ \t\n\r\f\v]` |
| `\S` | Không phải whitespace | `[^ \t\n\r\f\v]` |

---

## 📍**VỊ TRÍ (ANCHORS)**

| Pattern | Ý nghĩa |
|---------|---------|
| `^` | Đầu dòng/chuỗi |
| `$` | Cuối dòng/chuỗi |
| `\b` | Word boundary |
| `\B` | Không phải word boundary |

### Ví dụ

```regex
^hello      # Bắt đầu bằng "hello"
world$      # Kết thúc bằng "world"
^hello$     # Chính xác "hello"
\bword\b    # Từ "word" riêng biệt
```

---

## 🔀**NHÓM VÀ THAM CHIẾU**

### Groups

| Pattern | Ý nghĩa |
|---------|---------|
| `(abc)` | Nhóm capture |
| `(?:abc)` | Nhóm non-capture |
| `(a\|b)` | a hoặc b |

### Backreferences

```regex
(abc)\1     # "abc" lặp lại: matches "abcabc"
(\w+)\s\1   # Từ lặp lại: matches "hello hello"
```

### Named Groups (Python)

```regex
(?P<name>\w+)     # Named group
(?P=name)         # Reference named group
```

---

## 🔍**LOOKAHEAD & LOOKBEHIND**

| Pattern | Ý nghĩa |
|---------|---------|
| `a(?=b)` | 'a' theo sau bởi 'b' (không capture 'b') |
| `a(?!b)` | 'a' KHÔNG theo sau bởi 'b' |
| `(?<=b)a` | 'a' đứng sau 'b' |
| `(?<!b)a` | 'a' KHÔNG đứng sau 'b' |

### Ví dụ

```regex
\d+(?=€)         # Số trước dấu € (100 trong "100€")
(?<=\$)\d+       # Số sau dấu $ (100 trong "$100")
password(?!123)  # "password" không theo sau bởi "123"
```

---

## 🐍**PYTHON REGEX**

### Import và cơ bản

```python
import re

# Tìm kiếm
result = re.search(r'\d+', 'hello 123 world')
if result:
    print(result.group())  # '123'

# Tìm tất cả
results = re.findall(r'\d+', 'a1 b2 c3')
print(results)  # ['1', '2', '3']

# Check match ở đầu
result = re.match(r'hello', 'hello world')

# Check match toàn bộ
result = re.fullmatch(r'\d+', '123')
```

### Thay thế

```python
# Replace
text = re.sub(r'\d+', 'X', 'a1 b2 c3')
print(text)  # 'aX bX cX'

# Replace với function
def double(match):
    return str(int(match.group()) * 2)

text = re.sub(r'\d+', double, 'a1 b2 c3')
print(text)  # 'a2 b4 c6'

# Replace với limit
text = re.sub(r'\d+', 'X', 'a1 b2 c3', count=2)
print(text)  # 'aX bX c3'
```

### Split

```python
parts = re.split(r'\s+', 'hello   world  foo')
print(parts)  # ['hello', 'world', 'foo']

# Split với limit
parts = re.split(r'\s+', 'a b c d', maxsplit=2)
print(parts)  # ['a', 'b', 'c d']
```

### Compile (tối ưu)

```python
pattern = re.compile(r'\d+')

# Sử dụng pattern đã compile
result = pattern.search('hello 123')
results = pattern.findall('a1 b2 c3')
```

### Flags

```python
# Case insensitive
re.search(r'hello', 'HELLO', re.IGNORECASE)
re.search(r'hello', 'HELLO', re.I)

# Multiline (^ $ match mỗi dòng)
re.search(r'^hello', 'world\nhello', re.MULTILINE)
re.search(r'^hello', 'world\nhello', re.M)

# Dotall (. match cả newline)
re.search(r'a.b', 'a\nb', re.DOTALL)
re.search(r'a.b', 'a\nb', re.S)

# Verbose (có thể comment)
pattern = re.compile(r'''
    \d+      # digits
    \s*      # optional whitespace
    \w+      # word
''', re.VERBOSE)
```

### Groups

```python
# Capture groups
match = re.search(r'(\w+)@(\w+)\.(\w+)', 'user@email.com')
print(match.group(0))  # 'user@email.com' (toàn bộ)
print(match.group(1))  # 'user'
print(match.group(2))  # 'email'
print(match.groups())  # ('user', 'email', 'com')

# Named groups
match = re.search(r'(?P<user>\w+)@(?P<domain>\w+)', 'user@email')
print(match.group('user'))  # 'user'
print(match.groupdict())    # {'user': 'user', 'domain': 'email'}
```

---

## 📋**PATTERNS THƯỜNG DÙNG**

### Email

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

### Số điện thoại Việt Nam

```regex
^(0|\+84)[0-9]{9}$
```

### URL

```regex
https?://[^\s]+
```

### IP Address

```regex
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b
```

### Date (DD/MM/YYYY)

```regex
\d{2}/\d{2}/\d{4}
```

### Time (HH:MM)

```regex
\d{2}:\d{2}
```

### Password (ít nhất 8 ký tự, có chữ hoa, thường, số)

```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$
```

### HTML Tag

```regex
<([a-z]+)([^>]*)>(.*?)</\1>
```

### Số có dấu phẩy

```regex
\d{1,3}(,\d{3})*(\.\d+)?
```

### Hex Color

```regex
#[0-9A-Fa-f]{6}
```

### Vietnamese characters

```regex
[a-zA-ZàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]+
```

---

## 🧪**TEST REGEX ONLINE**

| Tool | URL |
|------|-----|
| Regex101 | https://regex101.com |
| RegExr | https://regexr.com |
| Debuggex | https://www.debuggex.com |

---

## ⚠️**LƯU Ý**

### Escape characters

Các ký tự cần escape: `\ . ^ $ * + ? { } [ ] ( ) |`

```python
# Tìm dấu chấm literal
re.search(r'\.', 'hello.world')

# Hoặc dùng re.escape()
pattern = re.escape('$100.00')  # '\$100\.00'
```

### Raw string trong Python

Luôn dùng `r''` để tránh escape characters:

```python
# Sai
re.search('\\d+', '123')

# Đúng
re.search(r'\d+', '123')
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
