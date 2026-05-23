# 🔍 Regex — Regular Expressions

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Tìm kiếm và xử lý text theo pattern

---

## Tại sao cần Regex?

Regex giải quyết bài toán: **"Tìm text khớp với mẫu (pattern) nhất định"**. Thay vì viết hàng chục dòng code `if/else` để kiểm tra email, số điện thoại, hay extract data từ log files, bạn viết 1 dòng regex.

Regex xuất hiện **ở khắp mọi nơi**:
- **Validation**: email, phone, URL, password
- **Search & Replace**: IDE, grep, sed
- **Log parsing**: extract timestamps, IPs, errors
- **Web scraping**: extract data từ HTML
- **Routing**: Express `app.get('/users/:id(\\d+)')`

Nhưng regex có tiếng xấu: "write-only code" — viết xong quên không biết nó làm gì. Bài này giúp bạn **hiểu từng phần** thay vì copy-paste.

---

## 1. Cú pháp cơ bản

### Character Classes — "Ký tự thuộc nhóm nào?"

```
.       Bất kỳ ký tự nào (trừ newline)
\d      Chữ số (digit): 0-9
\D      KHÔNG phải chữ số
\w      Word character: a-z, A-Z, 0-9, _
\W      KHÔNG phải word character
\s      Whitespace: space, tab, newline
\S      KHÔNG phải whitespace
```

### Quantifiers — "Bao nhiêu lần?"

```
*       0 hoặc nhiều lần    (a* → "", "a", "aaa")
+       1 hoặc nhiều lần    (a+ → "a", "aaa", KHÔNG match "")
?       0 hoặc 1 lần        (colou?r → "color" hoặc "colour")
{n}     Đúng n lần          (\d{4} → "2026")
{n,}    Ít nhất n lần       (\d{2,} → "12", "123", "1234")
{n,m}   Từ n đến m lần      (\d{1,3} → "1", "12", "123")
```

### Anchors — "Ở vị trí nào?"

```
^       Đầu string/dòng     (^Hello → match "Hello world")
$       Cuối string/dòng    (world$ → match "Hello world")
\b      Ranh giới từ         (\bcat\b → match "cat" nhưng KHÔNG "category")
```

### Groups & Alternation

```
(abc)   Group: gom lại thành 1 đơn vị
(?:abc) Non-capturing group: gom nhưng không capture
|       Hoặc: (cat|dog) → match "cat" hoặc "dog"
[abc]   Character set: 1 ký tự là a, b, hoặc c
[^abc]  Negated set: 1 ký tự KHÔNG phải a, b, c
[a-z]   Range: 1 ký tự từ a đến z
```

---

## 2. Ví dụ thực tế — Từ đơn giản đến phức tạp

### Email validation

```javascript
// Phân tích từng phần:
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

// ^                    → Bắt đầu string
// [a-zA-Z0-9._%+-]+   → Username: chữ, số, . _ % + - (1+ ký tự)
// @                    → Ký tự @ literal
// [a-zA-Z0-9.-]+      → Domain: chữ, số, . - (1+ ký tự)
// \.                   → Dấu . literal (escape vì . = any char)
// [a-zA-Z]{2,}         → TLD: ít nhất 2 chữ cái (com, org, vn...)
// $                    → Kết thúc string

emailRegex.test('user@example.com');     // true
emailRegex.test('a.b+c@mail.co.uk');     // true
emailRegex.test('invalid@');             // false
```

### Số điện thoại Việt Nam

```javascript
const phoneVN = /^(0|\+84)(3[2-9]|5[6|8|9]|7[0|6-9]|8[1-9]|9[0-9])\d{7}$/;

// (0|\+84)     → Bắt đầu bằng 0 hoặc +84
// (3[2-9]|...) → Đầu số mạng (Viettel: 03x, Mobi: 07x, Vina: 08x...)
// \d{7}        → 7 chữ số còn lại
// Tổng: 10-11 chữ số

phoneVN.test('0912345678');    // true
phoneVN.test('+84912345678');  // true
phoneVN.test('0112345678');    // false (đầu 011 không tồn tại)
```

### Extract data từ log

```javascript
const logLine = '2026-03-04 22:15:30 [ERROR] UserService: Connection timeout after 5000ms';

// Named groups (?<name>...) — dễ đọc hơn!
const logRegex = /(?<date>\d{4}-\d{2}-\d{2}) (?<time>\d{2}:\d{2}:\d{2}) \[(?<level>\w+)\] (?<source>\w+): (?<message>.+)/;

const match = logLine.match(logRegex);
console.log(match.groups);
// {
//   date: '2026-03-04',
//   time: '22:15:30',
//   level: 'ERROR',
//   source: 'UserService',
//   message: 'Connection timeout after 5000ms'
// }
```

### URL parsing

```javascript
const urlRegex = /^(?<protocol>https?):\/\/(?<host>[^\/]+)(?<path>\/[^?#]*)?(?:\?(?<query>[^#]*))?(?:#(?<hash>.*))?$/;

const url = 'https://example.com/users/123?sort=name&page=2#section1';
const { groups } = url.match(urlRegex);
// groups = {
//   protocol: 'https',
//   host: 'example.com',
//   path: '/users/123',
//   query: 'sort=name&page=2',
//   hash: 'section1'
// }
```

---

## 3. Search & Replace

```javascript
// Replace cơ bản
'Hello World'.replace(/world/i, 'Regex');  // 'Hello Regex'

// Replace ALL (flag g = global)
'aaa bbb aaa'.replace(/aaa/g, 'xxx');  // 'xxx bbb xxx'

// Replace với captured groups ($1, $2...)
'John Smith'.replace(/(\w+) (\w+)/, '$2, $1');  // 'Smith, John'

// Replace với function
'hello world'.replace(/\b\w/g, (char) => char.toUpperCase());
// 'Hello World'

// Practical: camelCase → kebab-case
'backgroundColor'.replace(/[A-Z]/g, m => `-${m.toLowerCase()}`);
// 'background-color'

// Sanitize HTML
const dangerous = '<script>alert("XSS")</script>';
dangerous.replace(/<\/?script[^>]*>/gi, '');
// 'alert("XSS")'
```

---

## 4. Regex trong Python

Python dùng module `re` với cú pháp tương tự:

```python
import re

# Match
email = "user@example.com"
if re.match(r'^[\w.+-]+@[\w-]+\.[\w.]{2,}$', email):
    print("Valid email")

# Find all matches
text = "Call 0912345678 or 0987654321 for info"
phones = re.findall(r'0\d{9}', text)
# ['0912345678', '0987654321']

# Named groups
log = "2026-03-04 ERROR: disk full"
match = re.match(r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>\w+): (?P<msg>.+)', log)
print(match.group('level'))  # 'ERROR'

# Replace
result = re.sub(r'\d{4}-\d{4}', '****-****', 'Card: 1234-5678')
# 'Card: ****-****'

# Compile for reuse (nhanh hơn khi dùng nhiều lần)
pattern = re.compile(r'\b\d{3}-\d{3}-\d{4}\b')
matches = pattern.findall(text)
```

---

## 5. Tips & Gotchas

### Greedy vs Lazy

```javascript
// Greedy (default): match NHIỀU NHẤT có thể
'<div>Hello</div><div>World</div>'.match(/<div>.*<\/div>/);
// '<div>Hello</div><div>World</div>'  ← Match TẤT CẢ!

// Lazy (?): match ÍT NHẤT có thể
'<div>Hello</div><div>World</div>'.match(/<div>.*?<\/div>/);
// '<div>Hello</div>'  ← Chỉ match cái đầu
```

### Lookahead & Lookbehind

Kiểm tra context **mà không capture** vào kết quả:

```javascript
// Lookahead (?=...): "followed by..."
// Tìm số theo sau bởi "px"
'16px 24rem 32px'.match(/\d+(?=px)/g);  // ['16', '32']

// Negative lookahead (?!...): "NOT followed by..."
'16px 24rem 32px'.match(/\d+(?!px)/g);  // ['24']

// Lookbehind (?<=...): "preceded by..."
// Tìm giá trị sau dấu $
'Price: $99.99, Tax: $8.50'.match(/(?<=\$)\d+\.?\d*/g);  // ['99.99', '8.50']
```

### Performance

```
❌ Catastrophic backtracking:
  Pattern: (a+)+b    Input: "aaaaaaaaaaac"
  → Regex engine thử HÀNG TRIỆU combinations → hang!

✅ Fix: Viết pattern đơn giản, tránh nested quantifiers
  Dùng atomic groups, possessive quantifiers khi có thể
  Hoặc dùng string methods (includes, startsWith) khi regex quá phức tạp
```

---

## Regex Cheatsheet

```
BASICS:          QUANTIFIERS:      GROUPS:           FLAGS:
.  any char      *   0+            (abc)  capture    g  global
\d digit         +   1+            (?:ab) non-cap    i  case-insensitive
\w word char     ?   0 or 1        (?<n>) named      m  multiline
\s whitespace    {n} exact n       [abc]  set        s  dotAll
\b word bound    {n,m} range       [^ab]  neg set
^  start         *?  lazy          a|b    or
$  end
```

---

## Bài tập thực hành

- [ ] Validation: email, phone VN, password strength
- [ ] Extract: parse CSV line, extract URLs from text
- [ ] Replace: camelCase ↔ snake_case converter
- [ ] Log parser: extract date, level, message from log files

---

## Tài nguyên thêm

- [regex101.com](https://regex101.com/) — Build & test regex TRỰC QUAN (phải dùng!)
- [RegexOne](https://regexone.com/) — Interactive tutorial
- [Regex Crossword](https://regexcrossword.com/) — Puzzle game
