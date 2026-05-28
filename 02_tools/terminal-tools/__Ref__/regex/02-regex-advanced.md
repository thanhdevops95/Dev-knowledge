# 🔍 Regex Advanced — Biểu thức chính quy nâng cao

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-regex-basics.md`
> Lookahead, lookbehind, named groups, backreferences, và practical patterns.

---

## 1. Groups & Backreferences

### Capturing Groups

```python
import re

# Capturing groups: (pattern)
# Cho phép trích xuất và tái sử dụng
match = re.match(r'(\d{4})-(\d{2})-(\d{2})', '2024-03-15')
print(match.group(0))   # '2024-03-15' (full match)
print(match.group(1))   # '2024' (year)
print(match.group(2))   # '03' (month)
print(match.group(3))   # '15' (day)
```

### Named Groups

```python
# Named groups: (?P<name>pattern) — dễ đọc hơn
pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
match = re.match(pattern, '2024-03-15')
print(match.group('year'))    # '2024'
print(match.group('month'))   # '03'
print(match.groupdict())      # {'year': '2024', 'month': '03', 'day': '15'}

# Trong JavaScript
const pattern = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match = '2024-03-15'.match(pattern);
console.log(match.groups.year);   // '2024'
```

### Non-capturing Groups

```python
# Non-capturing: (?:pattern) — group nhưng KHÔNG capture
# Dùng khi cần group cho logic nhưng không cần lấy giá trị

# ❌ Thừa capturing groups
re.findall(r'(https?)://(www\.)?(.+)', url)  # 3 groups captured

# ✅ Chỉ capture domain
re.findall(r'(?:https?)://(?:www\.)?(.+)', url)  # Chỉ 1 group
```

### Backreferences

```python
# \1, \2... tham chiếu lại captured group

# Tìm từ lặp liên tiếp: "the the" hoặc "is is"
pattern = r'\b(\w+)\s+\1\b'
text = "the the cat sat on on the mat"
print(re.findall(pattern, text))  # ['the', 'on']

# HTML tag matching: đảm bảo close tag = open tag
pattern = r'<(\w+)>.*?</\1>'
print(re.findall(pattern, '<b>bold</b> <i>italic</i>'))
# ['b', 'i']
```

---

## 2. Lookahead & Lookbehind — Zero-width Assertions

Lookahead/Lookbehind **kiểm tra pattern xung quanh** mà **không consume** ký tự — như "nhìn trộm" mà không ăn.

### Positive Lookahead `(?=...)`

"Match X chỉ khi **theo sau** bởi Y"

```python
# Tìm số chỉ khi theo sau bởi "px"
re.findall(r'\d+(?=px)', '14px 20em 30px 5rem')
# ['14', '30'] — match số, nhưng "px" KHÔNG nằm trong kết quả

# Tìm password có ít nhất 1 chữ hoa, 1 số, 8+ ký tự
pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
print(bool(re.match(pattern, 'Hello123!')))  # True
print(bool(re.match(pattern, 'hello123')))   # False (no uppercase)
```

### Negative Lookahead `(?!...)`

"Match X chỉ khi **KHÔNG** theo sau bởi Y"

```python
# Tìm "foo" KHÔNG theo sau bởi "bar"
re.findall(r'foo(?!bar)', 'foobar foobaz foo')
# ['foo', 'foo'] — "foobar" bị loại

# File không phải .test.js
re.findall(r'\w+(?!\.test)\.js', 'app.js utils.test.js main.js')
# Matches: app.js, main.js
```

### Positive Lookbehind `(?<=...)`

"Match X chỉ khi **trước** bởi Y"

```python
# Tìm số sau dấu $
re.findall(r'(?<=\$)\d+', 'Price: $50 or €30')
# ['50'] — chỉ match số sau $

# Extract domain from email
re.findall(r'(?<=@)[\w.]+', 'user@gmail.com admin@company.org')
# ['gmail.com', 'company.org']
```

### Negative Lookbehind `(?<!...)`

"Match X chỉ khi **KHÔNG** trước bởi Y"

```python
# Tìm số KHÔNG có dấu - trước (positive numbers)
re.findall(r'(?<!-)\b\d+', 'temp: 25 -10 30 -5')
# ['25', '0', '30', '5'] — hmm, cần refine
# Better: (?<![-])\b\d+\b
```

### Tổng hợp Lookaround

```
(?=X)   Positive Lookahead   — "followed by X"
(?!X)   Negative Lookahead   — "NOT followed by X"
(?<=X)  Positive Lookbehind  — "preceded by X"
(?<!X)  Negative Lookbehind  — "NOT preceded by X"

Mẹo nhớ:
  = positive (phải có)
  ! negative (không được có)
  < lookBEHIND (nhìn về trước)
  (không <) lookAHEAD (nhìn về sau)
```

---

## 3. Greedy vs Lazy vs Possessive

```python
text = '<b>bold</b> and <i>italic</i>'

# Greedy (mặc định): match nhiều nhất có thể
re.findall(r'<.+>', text)
# ['<b>bold</b> and <i>italic</i>'] — quá nhiều!

# Lazy (?): match ÍT nhất có thể
re.findall(r'<.+?>', text)
# ['<b>', '</b>', '<i>', '</i>'] — đúng ý ⭐

# Possessive (+): match nhiều nhất, KHÔNG backtrack
# (Python re module không hỗ trợ, nhưng regex module có)
# import regex
# regex.findall(r'<.++>', text)  # No match (no backtrack)
```

| Quantifier | Greedy | Lazy | Possessive |
|---|---|---|---|
| `*` | `.*` | `.*?` | `.*+` |
| `+` | `.+` | `.+?` | `.++` |
| `?` | `X?` | `X??` | `X?+` |
| `{n,m}` | `.{2,5}` | `.{2,5}?` | `.{2,5}+` |

---

## 4. Flags / Modifiers

```python
# Python flags
re.IGNORECASE  # or re.I — case insensitive
re.MULTILINE   # or re.M — ^ $ match line start/end
re.DOTALL      # or re.S — . matches newline too
re.VERBOSE     # or re.X — allow comments & whitespace

# Combine flags
re.findall(r'hello', text, re.IGNORECASE | re.MULTILINE)

# Inline flags
re.findall(r'(?i)hello', text)     # Case insensitive
re.findall(r'(?m)^start', text)    # Multiline
```

### VERBOSE — Regex với comments!

```python
# Complex regex mà con người có thể đọc được
email_pattern = re.compile(r"""
    ^                   # Start of string
    [\w.+-]+            # Username: letters, digits, .+-
    @                   # @ symbol
    [\w-]+              # Domain name
    \.                  # Dot
    [a-zA-Z]{2,}        # TLD (2+ letters)
    $                   # End of string
""", re.VERBOSE)

print(bool(email_pattern.match("user@example.com")))   # True
print(bool(email_pattern.match("invalid@.com")))        # False
```

---

## 5. Practical Patterns — Patterns thực tế

### Validation

```python
# Email (simplified — RFC 5322 quá phức tạp)
email = r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$'

# URL
url = r'https?://[\w.-]+(?:\.[\w.-]+)+[\w\-._~:/?#\[\]@!$&\'()*+,;=]*'

# IPv4
ipv4 = r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'

# Phone (Vietnamese)
phone_vn = r'^(?:\+84|0)(?:3[2-9]|5[2689]|7[06-9]|8[1-9]|9[0-9])\d{7}$'

# Password: 8+ chars, 1 uppercase, 1 lowercase, 1 digit, 1 special
password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

# Date (YYYY-MM-DD)
date = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
```

### Extraction

```python
# Extract all hashtags from text
hashtags = re.findall(r'#(\w+)', 'Love #Python and #regex!')
# ['Python', 'regex']

# Extract key-value pairs from log
log = 'user=admin action=login ip=192.168.1.1'
pairs = dict(re.findall(r'(\w+)=(\S+)', log))
# {'user': 'admin', 'action': 'login', 'ip': '192.168.1.1'}

# Extract numbers with optional decimal
numbers = re.findall(r'-?\d+\.?\d*', 'temp: 36.5 -10 100.99')
# ['36.5', '-10', '100.99']
```

### Search & Replace

```python
# camelCase → snake_case
text = 'getUserName getItemById'
snake = re.sub(r'([a-z])([A-Z])', r'\1_\2', text).lower()
# 'get_user_name get_item_by_id'

# Remove duplicate whitespace
clean = re.sub(r'\s+', ' ', '  hello   world  ').strip()
# 'hello world'

# Mask credit card: 1234-5678-9012-3456 → ****-****-****-3456
masked = re.sub(r'\d{4}-\d{4}-\d{4}-', '****-****-****-', cc)

# Template interpolation
template = "Hello {name}, you are {age} years old"
data = {'name': 'An', 'age': '25'}
result = re.sub(r'\{(\w+)\}', lambda m: data.get(m.group(1), m.group(0)), template)
# 'Hello An, you are 25 years old'
```

---

## 6. Performance — Tránh Catastrophic Backtracking

```python
# ❌ Evil regex — exponential backtracking!
evil = r'(a+)+$'   # Nested quantifiers
# Input: "aaaaaaaaaaaaaaaaX" → HÀNG GIỜ xử lý!

# ❌ Another evil regex
evil2 = r'([a-z]+)*!'
# Input: "aaaaaaaaaaaaaaaa" → catastrophic backtracking

# ✅ Fix: sử dụng atomic groups hoặc tránh nested quantifiers
safe = r'a+$'           # Không lồng quantifiers
safe2 = r'[a-z]+!'      # Removed unnecessary group

# ✅ Quy tắc tránh backtracking:
# 1. KHÔNG dùng nested quantifiers: (a+)+ , (a*)*
# 2. Dùng possessive quantifier khi có thể: a++
# 3. Dùng atomic groups: (?>a+)
# 4. Test với regex101.com — xem bước match
```

---

## 7. Regex trong các ngôn ngữ

| Feature | Python `re` | JavaScript | Java | Go |
|---|---|---|---|---|
| Named groups | `(?P<name>)` | `(?<name>)` | `(?<name>)` | `(?P<name>)` |
| Lookbehind | ✅ Variable | ✅ (ES2018) | ✅ Variable | ❌ |
| Possessive | ❌ (dùng `regex` module) | ❌ | ✅ | ❌ |
| Unicode `\p{L}` | ❌ (dùng `regex` module) | ✅ (with /u) | ✅ | ✅ |
| VERBOSE mode | ✅ `re.X` | ❌ | ✅ `(?x)` | ❌ |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Validate email bằng regex hoàn hảo | Dùng regex đơn giản + gửi confirmation email | RFC 5322 email regex dài 6000+ ký tự |
| 2 | Parse HTML bằng regex | Dùng HTML parser (BeautifulSoup) | HTML không regular → regex KHÔNG ĐỦ |
| 3 | `.*` khi muốn non-greedy | Dùng `.*?` (lazy) hoặc character class | Greedy ăn quá nhiều |
| 4 | Quên escape dots `.` | `\.` để match literal dot | `.` match BẤT KỲ ký tự nào |
| 5 | Nested quantifiers `(a+)+` | Flatten: `a+` | Catastrophic backtracking |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Viết regex validate: email, phone VN, strong password. Test edge cases.
- [ ] **Bài 2 (Trung bình):** Extract key-value pairs từ log file (format: `[timestamp] key=value`)
- [ ] **Bài 3 (Khó):** Viết regex converter: camelCase ↔ snake_case ↔ kebab-case
- [ ] **Bài 4 (Khó):** Viết regex cho markdown parser: `**bold**`, `*italic*`, `[link](url)`, `` `code` ``

---

## Tài nguyên thêm

- [regex101.com](https://regex101.com/) — Online regex tester với explanation ⭐
- [regexr.com](https://regexr.com/) — Visual regex tool
- [Mastering Regular Expressions (Friedl)](https://www.oreilly.com/library/view/mastering-regular-expressions/9780596528126/) — The regex bible
- [ReDOS — Regular Expression Denial of Service](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS) — Security
- [regex crossword](https://regexcrossword.com/) — Fun regex puzzles
