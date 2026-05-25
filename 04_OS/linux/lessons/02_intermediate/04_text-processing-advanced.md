# 🎓 Text Processing — grep, sed, awk + pipe combos

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Linux View File Content](../01_basic/03_view-file-content.md), [IO Redirection](../../../../01_Foundations/computing-environment/lessons/01_basic/05_io-redirection.md)

> 🎯 *Master 3 tool **Unix power**: **`grep`** (search), **`sed`** (substitute), **`awk`** (process). Plus `sort`/`uniq`/`cut`/`tr`/`wc`/`xargs`. Sau bài này bạn cào log production 10GB, transform JSON, parse CSV trong terminal — không cần script.*

## 🎯 Sau bài này bạn sẽ

- [ ] Master **`grep`** + regex + flags (`-i`, `-r`, `-v`, `-c`, `-A/B`, `-E`)
- [ ] Dùng **`sed`** substitute + xoá dòng + insert
- [ ] Dùng **`awk`** filter cột + tính tổng + format output
- [ ] Combine **`sort`**, **`uniq -c`**, **`cut`**, **`tr`**, **`wc`**
- [ ] Dùng **`xargs`** chuyển stdout thành argument
- [ ] Phân biệt **regex types** (BRE / ERE / PCRE)
- [ ] 5 case thực tế: count log error, top IP, parse CSV, find big file, mass rename

---

## Tình huống — Bạn debug log production 10GB

Server crash. Bạn check log nginx:

```bash
ls -lh /var/log/nginx/access.log
# -rw-r--r-- 1 root adm 10.2G ... access.log
```

10 GB log. Bạn muốn:
1. Đếm bao nhiêu **request 5xx error**.
2. Tìm **top 10 IP** request nhiều nhất.
3. Filter request **chỉ trong 30 phút trước crash**.
4. Tìm pattern lỗi (`OutOfMemoryError`).
5. Replace mọi IP private trong export ra `0.0.0.0`.

Bạn thử mở vim:
```bash
vim access.log
# Mở 10 phút, RAM 12GB, máy lag
```

Senior chỉ:
> *"Đừng load full log. Dùng `grep`, `awk`, `sort`. Streaming text processing là superpower Unix — 70 năm tuổi, vẫn vô địch."*

→ Bài này dạy bạn **xử lý text như chuyên gia**.

---

## 1️⃣ `grep` — Search

🪞 **Ẩn dụ**: *`grep` như **kính lúp** — bạn cầm đi qua đống giấy (file), kính giúp chỉ những dòng có chữ bạn tìm. Thêm các flag (`-i`, `-n`, `-r`) = kính lúp thông minh hơn (không phân biệt hoa thường, in số dòng, soi cả thư mục con).*

### Cơ bản

12 flag thường dùng nhất. Đừng nhớ hết — quen vài flag chính (`-i`, `-n`, `-r`, `-v`, `-A/-B/-C`) là đủ 95% cases:

```bash
grep "error" file.log                    # Tìm dòng có "error"
grep -i "error" file.log                 # Case-insensitive
grep -n "error" file.log                 # Show line number
grep -c "error" file.log                 # Đếm số dòng match
grep -v "error" file.log                 # INVERT — dòng KHÔNG có "error"
grep -l "error" *.log                    # Chỉ liệt kê **file** có match
grep -r "TODO" src/                      # Recursive search dir
grep -w "the" file                        # Whole word (không match "their")
grep -A 3 "error" file.log               # Show 3 dòng SAU match
grep -B 3 "error" file.log               # Show 3 dòng TRƯỚC match
grep -C 3 "error" file.log               # Cả trước + sau
grep --color "error" file                # Highlight match (default trong nhiều distro)
```

### Regex

Khi pattern phức tạp hơn (vd: tìm IP, số điện thoại, format ngày), thêm `-E` (extended regex) hoặc `-P` (Perl regex):

```bash
grep -E "error|warning" file              # ERE (extended regex), `|` = or
grep -E "^[0-9]+" file                    # Dòng bắt đầu bằng số
grep -E "[0-9]{3}-[0-9]{4}" file          # Pattern phone US
grep -P "(?<=user_id=)\d+" file           # Perl regex (lookbehind) — `-P`

# Inverse search nhiều pattern
grep -vE "test|debug" file                # Skip test + debug
```

### Search file ignoring binary

```bash
grep -I "error" *                          # Skip binary file
grep -a "error" binary                     # Force treat as text
```

### Stream từ stdin

```bash
journalctl -u nginx | grep "5\d\d"        # Pipe từ command khác
cat *.log | grep "error" | wc -l           # Count line
```

### Bạn count error log

```bash
$ grep -c "ERROR" /var/log/myapp/app.log
1247

$ grep -cE "5[0-9]{2}" /var/log/nginx/access.log    # 5xx codes
342
```

### Performance

```bash
LC_ALL=C grep "pattern" huge.log          # 3-5x nhanh hơn (UTF-8 → ASCII)
ripgrep (rg)                                # Modern alternative, 10x nhanh
```

→ `rg` (ripgrep) là **grep modern** — respect `.gitignore`, parallel, Rust speed. `brew install ripgrep` hoặc `apt install ripgrep`.

---

## 2️⃣ `sed` — Stream Editor (substitute)

### Substitute — pattern phổ biến nhất

```bash
sed 's/old/new/' file                     # Thay first match mỗi dòng
sed 's/old/new/g' file                    # `g` = global, thay all
sed 's/old/new/2' file                    # Chỉ thay match 2nd
sed 's/old/new/gI' file                   # case-insensitive (g + I)

# In-place edit
sed -i 's/old/new/g' file                 # Sửa file luôn (DANGER!)
sed -i.bak 's/old/new/g' file             # Backup file.bak trước

# Print only matching
sed -n 's/old/new/p' file                 # `n` no print default, `p` print match
```

### Delete lines

```bash
sed '5d' file                              # Xoá dòng 5
sed '2,5d' file                            # Xoá dòng 2-5
sed '/pattern/d' file                      # Xoá dòng match
sed '/^$/d' file                           # Xoá dòng rỗng
sed '/^#/d' file                           # Xoá dòng comment
```

### Insert / Append / Replace dòng

```bash
sed '5i NEW_LINE' file                    # Insert TRƯỚC dòng 5
sed '5a NEW_LINE' file                    # Append SAU dòng 5
sed '5c NEW_LINE' file                    # REPLACE dòng 5
sed -i '/pattern/a\new line' file          # Append sau pattern match
```

### Print specific lines

```bash
sed -n '10,20p' file                       # In dòng 10-20 (như head/tail combo)
sed -n '/pattern/p' file                   # In dòng match (như grep, ít dùng)
sed -n '$=' file                           # Print line count
```

### Multiple commands

```bash
sed -e 's/foo/bar/g' -e 's/baz/qux/g' file
sed 's/foo/bar/g; s/baz/qux/g' file
```

### Regex extended

```bash
sed -E 's/[0-9]+/NUM/g' file              # ERE regex (group, +, ?, |)
sed -E 's/(\w+)@(\w+)/USER@DOMAIN/g' file
```

### bạn masking IP private trong export

```bash
sed -E 's/192\.168\.[0-9]+\.[0-9]+/0.0.0.0/g' access.log > masked.log
```

> ⚠️ **`sed -i`** rất nguy hiểm khi pattern bug — sửa file production sai pattern. **Luôn test không `-i` trước**.

---

## 3️⃣ `awk` — Programming language nhỏ trong CLI

`awk` chia dòng thành **fields** (cột) theo delimiter, xử lý từng record. Kết hợp filter + transform + tính toán.

### Cấu trúc

```bash
awk 'pattern { action }' file
```

- `pattern` (optional) — chỉ apply action khi match.
- `action` — `{ print $1; sum += $2 }`.

### Print cột

```bash
$ cat data.txt
Nguyen Van A 28 Hanoi
Le Van B   25 Hanoi
Tran Van C 35 Saigon

$ awk '{print $1}' data.txt              # Cột 1
Nguyen Van A
Le Van B
Tran Van C

$ awk '{print $2, $3}' data.txt           # Cột 2 + 3
28 Hanoi
25 Hanoi
35 Saigon

$ awk '{print $NF}' data.txt              # Cột cuối ($NF = number of fields)
$ awk '{print NR, $0}' data.txt           # Line number + full line
```

| Variable | Ý nghĩa |
|---|---|
| `$0` | Cả dòng |
| `$1`, `$2`, ... | Cột 1, 2, ... |
| `$NF` | Cột cuối |
| `NR` | Number of Record (số dòng đã đọc) |
| `NF` | Number of Fields (số cột) |
| `FS` | Field Separator (default whitespace) |
| `OFS` | Output Field Separator |

### Filter

```bash
awk '$2 > 30' data.txt                    # Cột 2 > 30
awk '/Hanoi/' data.txt                    # Dòng match "Hanoi"
awk '$3 == "Hanoi" && $2 < 30' data.txt   # Combine
awk 'NR > 1' data.txt                     # Bỏ dòng đầu (skip header)
awk 'NR > 1 && NR <= 100' data.txt        # Dòng 2-100
```

### Tính toán

```bash
# Tổng cột 2
awk '{sum += $2} END {print sum}' data.txt

# Trung bình
awk '{sum += $2; n++} END {print sum/n}' data.txt

# Max
awk 'NR == 1 {max = $2} $2 > max {max = $2} END {print max}' data.txt

# Count by group (cột 3 = city)
awk '{count[$3]++} END {for (city in count) print city, count[city]}' data.txt
# Output:
# Hanoi 2
# Saigon 1
```

### Custom delimiter

```bash
# Parse /etc/passwd (delimiter `:`)
awk -F: '{print $1, $7}' /etc/passwd       # username + shell
# Output:
# root /bin/bash
# www-data /usr/sbin/nologin
# ...

# CSV
awk -F, '$3 > 100 {print $1, $3}' sales.csv

# Multiple delimiter
awk -F'[,;]' '{print $1, $2}' data
```

### bạn parse nginx access.log

Format: `IP - user [time] "method URL HTTP" status size`:
```
192.168.1.1 - - [23/May/2025:14:00:00] "GET /api HTTP/1.1" 200 1234
192.168.1.2 - - [23/May/2025:14:00:01] "POST /login HTTP/1.1" 401 567
```

```bash
# Top 10 IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# 5xx errors
awk '$9 >= 500 {print $0}' access.log     # $9 = status (offset by 1 cho timestamp)

# Tổng bytes serve
awk '{sum += $NF} END {print sum/1024/1024, "MB"}' access.log
```

---

## 4️⃣ `sort` / `uniq` / `cut` / `tr` / `wc`

### `sort`

```bash
sort file                                  # Alphabetical
sort -r file                                # Reverse
sort -n file                                # Numeric (1, 2, 10 thay vì 1, 10, 2)
sort -h file                                # Human sizes (1K, 2M, 3G)
sort -k 2 file                              # Sort theo cột 2
sort -t, -k 3 file.csv                      # CSV — cột 3
sort -u file                                # Unique
sort | uniq                                  # = sort -u (uniq cần input sorted)
```

### `uniq`

```bash
sort file | uniq                            # Unique lines
sort file | uniq -c                          # Count duplicates
sort file | uniq -c | sort -rn               # Top N (most frequent)
sort file | uniq -d                          # Chỉ in dòng bị trùng
sort file | uniq -u                           # Chỉ in dòng KHÔNG bị trùng
```

### `cut`

```bash
cut -d, -f1,3 file.csv                      # Cột 1+3 của CSV
cut -d: -f1 /etc/passwd                     # Username
cut -c1-10 file                              # Ký tự 1-10
echo "abc-def-ghi" | cut -d- -f2             # def
```

### `tr` (translate)

```bash
echo "HELLO" | tr 'A-Z' 'a-z'               # → hello
echo "hello" | tr -d ' '                     # Xoá ký tự
echo "a,b,c" | tr ',' '\n'                   # Thay , thành newline
tr -s ' ' < file                              # Squeeze (compress multiple spaces)
cat file | tr -d '\r'                         # Xoá Windows CR
```

### `wc` (word count)

```bash
wc file                                      # Lines, words, chars
wc -l file                                    # Lines only
wc -w file                                    # Words
wc -c file                                    # Bytes
wc -L file                                    # Longest line length
```

---

## 5️⃣ `xargs` — Stdout thành argument

```bash
ls | xargs rm                                # Run rm trên mỗi file
find . -name "*.log" -mtime +30 | xargs rm   # Xoá log >30 ngày

# Quote-safe (filename có space)
find . -name "*.txt" -print0 | xargs -0 rm

# Parallel — 4 process song song
ls *.png | xargs -P 4 -I {} convert {} {}.webp

# Manual placeholder
echo "a b c" | xargs -n 1 echo               # n=1: 1 arg mỗi lần
# a
# b
# c
```

### Vs while loop

```bash
# xargs (đơn giản)
ls *.log | xargs gzip

# while loop (phức tạp hơn, xử lý mỗi item riêng)
ls *.log | while read f; do
    gzip "$f"
    echo "Compressed $f"
done
```

---

## 6️⃣ Regex types — BRE / ERE / PCRE

| Type | Tool | Khác biệt |
|---|---|---|
| **BRE** (Basic) | `grep`, `sed` mặc định | `\(`, `\)`, `\?`, `\+`, `\|` cần escape |
| **ERE** (Extended) | `grep -E`, `sed -E`, `awk` | `(`, `)`, `?`, `+`, `\|` không escape |
| **PCRE** (Perl) | `grep -P`, Python `re`, Perl | Most powerful: `\d`, lookbehind, named groups |

### Ví dụ phân biệt

```bash
# BRE
grep "color\|colour" file

# ERE (gọn hơn)
grep -E "color|colour" file

# PCRE (advanced)
grep -P "(?<=user_id=)\d+" file       # Lookbehind — chỉ số sau "user_id="
```

→ **Khuyên dùng ERE** (`-E`) cho daily — cú pháp giống regex các ngôn ngữ khác.

### Character class

```
\d, [0-9]     digit
\w, [a-zA-Z0-9_]   word char
\s, [ \t\n]   whitespace
.             bất kỳ (trừ newline)
^             đầu dòng
$             cuối dòng
\b            word boundary
```

### Quantifier

```
?    0 hoặc 1
*    0 trở lên
+    1 trở lên
{n}  đúng n lần
{n,} ít nhất n
{n,m} từ n-m
```

---

## 7️⃣ 5 case thực tế

### Case 1 — Top 10 IP request nhiều nhất

```bash
awk '{print $1}' /var/log/nginx/access.log \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -10
```

Output:
```
12345 203.0.113.1
8765 198.51.100.42
...
```

### Case 2 — Count error mỗi giờ

```bash
grep "ERROR" app.log | awk '{print $1, $2}' | cut -c1-13 | sort | uniq -c
# 2025-05-23T14   42
# 2025-05-23T15   18
# 2025-05-23T16   100
```

### Case 3 — Parse CSV — tổng doanh thu theo region

```bash
awk -F, 'NR > 1 {region[$3] += $5} END {for (r in region) print r, region[r]}' sales.csv | sort -k2 -rn
# North 1500000
# South 850000
# East 720000
```

### Case 4 — Find big file

```bash
find / -type f -size +100M 2>/dev/null | xargs ls -lh | sort -k5 -rh | head
# -rw-r--r-- 1 root root  2.3G  ...  /var/log/huge.log
# -rw-r--r-- 1 root root  1.1G  ...  /tmp/coredump
```

### Case 5 — Mass rename `.JPG` → `.jpg`

```bash
# Method 1: rename
rename 's/\.JPG$/.jpg/' *.JPG

# Method 2: bash loop
for f in *.JPG; do mv "$f" "${f%.JPG}.jpg"; done

# Method 3: find + xargs
find . -name "*.JPG" | while read f; do mv "$f" "${f%.JPG}.jpg"; done
```

---

## 8️⃣ bạn's debug pipeline

> *"5 phút trước crash, log có pattern gì? Group by minute, show top error message."*

```bash
journalctl -u myapp --since "5 min ago" \
  | grep "ERROR" \
  | awk '{print $1, $2, substr($0, index($0, "ERROR"))}' \
  | cut -c1-20,40-100 \
  | sort | uniq -c | sort -rn | head -20
```

→ Pipeline 5 tool. Đây là daily devops/SRE.

---

## ⚠️ 5 pitfall hay vướng

1. **`sed -i` không backup** → sửa file production sai pattern = mất data. **Luôn `sed -i.bak`** hoặc dry-run trước.
2. **`grep` regex BRE quên escape** → `grep "foo|bar"` không match (vì `|` trong BRE là literal). Dùng `-E`.
3. **`xargs` với filename có space** → broken. Dùng `find ... -print0 | xargs -0`.
4. **`sort | uniq -c` quên sort trước** → uniq chỉ dedupe **adjacent line**. Cần sort trước.
5. **`awk -F,` không quote field** → field chứa comma trong quote (`"a,b",c`) bị split sai. Dùng tool CSV proper (`csvkit`, `miller`).

---

## ✅ Self-check

1. Đếm số dòng error trong file (case-insensitive)?
2. Sửa `localhost` thành `127.0.0.1` trong mọi file `.conf` (in-place, backup `.bak`)?
3. Top 5 user activity trong `/var/log/auth.log` (parse user từ pattern)?
4. CSV `data.csv` cột `id,name,price`. Tổng `price` của row có `price > 100`?
5. Khác BRE và ERE?

<details>
<summary>Gợi ý đáp án</summary>

1. `grep -ic "error" file.log` (-i case-insensitive, -c count).

2. `sed -i.bak 's/localhost/127.0.0.1/g' *.conf` — `-i.bak` lưu backup `.conf.bak`.

3. ```bash
   grep "Accepted" /var/log/auth.log \
     | awk '{print $9}' \
     | sort | uniq -c | sort -rn | head -5
   ```

4. ```bash
   awk -F, 'NR > 1 && $3 > 100 {sum += $3} END {print sum}' data.csv
   ```

5. **BRE** = Basic Regex (default `grep`, `sed`). Trong BRE, `(`, `)`, `?`, `+`, `|` là **literal** — cần `\` để có meta nghĩa. **ERE** = Extended Regex (`grep -E`, `sed -E`, `awk`). Mặc định `(`, `)`, `?`, `+`, `|` là **meta** — gọn hơn, giống regex các ngôn ngữ khác.
</details>

---

## ⚡ Cheatsheet

### grep top patterns

```bash
grep "kw" file                     grep -i "kw" file (case-insens)
grep -r "kw" dir/                  grep -v "kw" file (invert)
grep -c "kw" file (count)          grep -n "kw" file (line num)
grep -A 3 -B 3 "kw" file (context)
grep -E "kw1|kw2" file (regex)     grep -P "(?<=x=)\d+" file (Perl)
```

### sed top patterns

```bash
sed 's/old/new/g' file             sed -i.bak 's/old/new/g' file
sed -n '10,20p' file               sed '/pattern/d' file
sed '5a New line' file             sed -E 's/[0-9]+/NUM/g' file
```

### awk top patterns

```bash
awk '{print $1}' file               awk -F, '{print $2}' file.csv
awk '$3 > 100' file                 awk '/pattern/ {action}' file
awk '{sum += $2} END {print sum}' file
awk '{count[$1]++} END {for (k in count) print k, count[k]}' file
```

### Pipeline combos

```bash
# Top N frequent
... | sort | uniq -c | sort -rn | head -10

# Filter + count
grep "pattern" file | wc -l

# Field aggregate
awk -F, '$3 > 100' file.csv | wc -l

# Mass rename
find . -name "*.JPG" -print0 | xargs -0 -I {} mv {} {}.jpg
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`grep`** | Search pattern trong text |
| **`sed`** | Stream editor — substitute/insert/delete |
| **`awk`** | Mini programming language cho text processing |
| **`sort`** | Sort lines |
| **`uniq`** | Remove duplicates (cần sorted input) |
| **`cut`** | Extract column |
| **`tr`** | Translate characters |
| **`wc`** | Word/line/byte count |
| **`xargs`** | Convert stdout to argument |
| **BRE / ERE / PCRE** | 3 loại regex syntax |
| **`-i`** (sed) | In-place edit |
| **`-E`** (grep/sed) | ERE — gọn hơn BRE |
| **`-P`** (grep) | PCRE — most powerful |
| **`ripgrep` (`rg`)** | Modern grep, 10x faster |
| **`miller`** | Modern CSV/TSV/JSON tool |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Package Management](03_package-management.md)
- ↑ Cluster: [linux README](../../README.md)

### Cross-reference
- [Linux view file content (basic)](../01_basic/03_view-file-content.md) — cat/less/head/tail
- [IO redirection](../../../../01_Foundations/computing-environment/lessons/01_basic/05_io-redirection.md) — pipe `|` + redirect `>`

### External
- 📖 [GNU grep manual](https://www.gnu.org/software/grep/manual/grep.html)
- 📖 [sed by example](https://www.grymoire.com/Unix/Sed.html)
- 📖 [AWK programming — Bruce Barnett](https://www.grymoire.com/Unix/Awk.html)
- 📖 [ripgrep guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
- 📖 [Miller — CSV/JSON power tool](https://miller.readthedocs.io/)

---

> 🎯 *Cluster Linux intermediate 5/5 đóng. Bạn giờ vận hành server Linux production-grade: permission + systemd + SSH + package + text processing. Bài kế tiếp có thể vào `03_advanced` (kernel tuning, eBPF) hoặc cluster khác.*

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm ẩn dụ "kính lúp" cho `grep`, 2 lead-in trước code (cơ bản + regex), fix grammar "bạn count" → "Bạn count" + "(và bạn)" duplicate.
