# 🎓 I/O Redirection — stdin, stdout, stderr, `|`, `>`, `<`, `2>&1`

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [03_process-and-pid.md](./03_process-and-pid.md), [04_env-variables.md](./04_env-variables.md)

> 🎯 *Bài CONCEPT cuối cluster computing-environment — hiểu **3 luồng I/O** (stdin/stdout/stderr) + **redirect** (`>`, `<`, `2>&1`) + **pipe** (`|`) + `/dev/null` + `tee`. Sau bài này bạn đọc được mọi lệnh shell phức tạp như `cmd1 | cmd2 > out.txt 2>&1`.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **stdin (0)**, **stdout (1)**, **stderr (2)** — 3 luồng I/O của process
- [ ] Redirect output: `>` (ghi đè), `>>` (append), `2>` (chỉ error), `2>&1` (gộp), `&>` (cả 2)
- [ ] Redirect input: `<` đọc file thay bàn phím
- [ ] **Pipe `|`** — output process này thành input process kế
- [ ] Dùng `/dev/null` để "vứt" output không cần
- [ ] Dùng `tee` để vừa save file vừa hiển thị màn hình
- [ ] Đọc được lệnh phức tạp như `ps aux | grep python | head -5 > result.txt 2>&1`

---

## Tình huống — bạn muốn save log app vào file

App Python của bạn in nhiều log:

```bash
python app.py
```

```
[INFO] Server starting...
[DEBUG] Connecting to DB
[ERROR] Could not connect to Redis
[INFO] Ready on port 5000
```

Bạn muốn:
1. **Lưu output vào file** `app.log` để xem lại — không phải copy-paste thủ công
2. **Tách lỗi (ERROR) ra file riêng** `app-error.log` — dễ debug
3. **Lọc chỉ dòng có "ERROR"** — không phải scroll qua INFO/DEBUG
4. **Vừa thấy trên màn hình + lưu file** cùng lúc

Search Google: gặp lệnh kiểu:

```bash
python app.py > app.log 2> app-error.log
ps aux | grep python | head -5
docker logs container1 2>&1 | tee output.log
```

Những ký hiệu `>`, `2>`, `|`, `2>&1`, `tee` — học 1 lần xài cả đời. Bài này dạy tất cả.

→ Đây là **siêu năng lực** của Unix shell — kết hợp lệnh nhỏ thành workflow mạnh. **Hiểu I/O redirect = mở khoá 80% sức mạnh terminal**.

---

## 1️⃣ Vậy 3 luồng I/O là gì?

**Trả lời tình huống**: mỗi process Unix có **3 luồng (stream)** mặc định:

| FD | Tên | Hướng | Mặc định | Vai trò |
|---|---|---|---|---|
| `0` | **stdin** | Input | Bàn phím | Process đọc data từ đây |
| `1` | **stdout** | Output | Terminal | Process ghi output bình thường |
| `2` | **stderr** | Output | Terminal | Process ghi lỗi / cảnh báo |

```mermaid
graph LR
    K[⌨️ Bàn phím] -->|stdin: 0| P[⚙️ Process<br/>python app.py]
    P -->|stdout: 1<br/>output bình thường| T[📺 Terminal]
    P -->|stderr: 2<br/>error/warning| T
```

**FD** = File Descriptor — số nguyên process dùng để tham chiếu I/O stream. 0, 1, 2 là 3 FD chuẩn của mọi process. Còn dùng cho file thường (FD 3, 4, 5...).

🪞 **Ẩn dụ**: process giống **người làm việc** có:
- **2 tai** (stdin): nghe người khác nói
- **Miệng** (stdout): nói kết quả thường
- **Cờ đỏ** (stderr): giơ lên khi có lỗi/cảnh báo

Mặc định miệng + cờ đỏ đều "hướng vào terminal" → bạn thấy hết. Nhưng có thể **redirect** — bịt miệng vào file, hoặc gửi cờ đỏ sang chỗ khác.

### Vì sao tách stderr khỏi stdout?

Cùng là output, nhưng:
- **stdout**: data "thật" — sản phẩm của process. VD: `ls` in danh sách file.
- **stderr**: thông tin meta — log, warning, error. VD: `ls /nonexistent` in lỗi "No such directory".

**Tách 2 ra**: bạn có thể save data thật vào file, error in màn hình. Không cần parse lẫn lộn.

```bash
ls /etc /nonexistent
# /etc:
# passwd ssh ...
# ls: cannot access '/nonexistent': No such file or directory
```

→ Mắt thường: 2 dòng cùng terminal. Nhưng máy biết "passwd ssh..." là stdout, "ls: cannot..." là stderr.

---

## 2️⃣ Redirect Output — `>`, `>>`, `2>`, `2>&1`

### Cú pháp tổng quát

5 ký hiệu cơ bản. Đọc xong block dưới, bạn sẽ phân biệt được "ghi đè" (`>`) vs "nối thêm" (`>>`), tách lỗi (`2>`) vs gộp vào (`2>&1`):

```
<command> > <file>          # stdout → file (ghi đè)
<command> >> <file>         # stdout → file (append, nối thêm)
<command> 2> <file>         # stderr → file
<command> 2>&1              # gộp stderr vào stdout
<command> &> <file>         # cả stdout + stderr → file (shortcut)
```

### Ví dụ thực tế

Cách tốt nhất hiểu cú pháp là xem code chạy thật. 4 ví dụ dưới cover 4 use case phổ biến nhất: lưu output, append log, tách lỗi ra file riêng, gộp tất cả vào 1 file:

```bash
# Lưu output ls vào file (ghi đè nếu file tồn tại)
ls /etc > files.txt
cat files.txt    # xem nội dung

# Append (nối thêm) thay vì ghi đè
date >> log.txt        # thêm 1 dòng date vào cuối log.txt

# Tách error ra file riêng
ls /etc /nonexistent > output.txt 2> errors.txt
cat output.txt   # chỉ list /etc (stdout)
cat errors.txt   # chỉ dòng "cannot access" (stderr)

# Gộp cả 2 vào 1 file
ls /etc /nonexistent > everything.txt 2>&1
# Hoặc shortcut:
ls /etc /nonexistent &> everything.txt
```

### Giải mã `2>&1` — ký hiệu hay gặp nhất

Bạn sẽ thấy ký hiệu `2>&1` trong rất nhiều script + tutorial Unix. Trông khó hiểu nhưng nghĩa đơn giản — đây là cách "đọc" nó:

```
2>&1
│  │
│  └── tham chiếu FD 1 (stdout)
└── FD 2 (stderr) redirect ĐẾN
```

Đọc: *"Stderr (2) gửi đến cùng nơi stdout (1) đang đi"*.

```bash
# Sai thứ tự
ls /etc /nonexistent 2>&1 > all.txt    # ❌ stderr ra terminal, stdout vào file

# Đúng thứ tự — quan trọng!
ls /etc /nonexistent > all.txt 2>&1    # ✓ stdout → file, sau đó stderr → file
```

**Lý do**: shell xử lý redirect **từ trái sang phải**. `> all.txt` đặt stdout vào file → sau đó `2>&1` đặt stderr vào "chỗ stdout đang đi" = file. Ngược lại, `2>&1` trước → stderr trỏ vào terminal (vì stdout chưa redirect) → sau đó `> all.txt` chỉ đổi stdout.

→ Modern shortcut: `&> all.txt` — đơn giản hơn `> all.txt 2>&1`.

### Bảng tổng hợp

Mọi cú pháp redirect ở section này gom vào bảng cheat dưới — in ra dán cạnh máy 1 tuần là quen:

| Cú pháp | Tác dụng |
|---|---|
| `cmd > file` | stdout → file (ghi đè) |
| `cmd >> file` | stdout → file (append) |
| `cmd 2> file` | stderr → file |
| `cmd 2>> file` | stderr → file (append) |
| `cmd > file 2>&1` | Cả stdout + stderr → file |
| `cmd &> file` | Same (shortcut bash 4+/zsh) |
| `cmd > /dev/null` | Vứt stdout |
| `cmd 2> /dev/null` | Vứt stderr |
| `cmd &> /dev/null` | Vứt cả 2 (chạy "im lặng") |

---

## 3️⃣ Redirect Input — `<` đọc file thay bàn phím

Cú pháp: `<command> < <file>`

```bash
# Sort dòng trong file
sort < data.txt
# Tương đương: cat data.txt | sort

# Đếm dòng
wc -l < /etc/passwd

# Gửi nội dung file qua mail (như nhập từ bàn phím)
mail user@example.com < message.txt
```

🪞 **Ẩn dụ**: bịt bàn phím của process, đút file vào miệng nó. Process tưởng đang nhận input từ bàn phím nhưng thực ra đọc file.

### Heredoc — input nhiều dòng inline

```bash
cat << EOF
Line 1
Line 2
Line 3
EOF
```

`<<EOF ... EOF` = inline input nhiều dòng. Useful khi script cần truyền block text.

```bash
mysql -u root -p mydb << EOF
SELECT * FROM users WHERE id = 1;
DELETE FROM logs WHERE created_at < NOW() - INTERVAL 30 DAY;
EOF
```

---

## 4️⃣ Pipe `|` — Lệnh này thành input lệnh kế

**Pipe** là **ký hiệu mạnh nhất** Unix. Cú pháp: `cmd1 | cmd2` — stdout của `cmd1` thành stdin của `cmd2`. Sơ đồ dưới mô phỏng dòng chảy data qua chuỗi 3 lệnh:

```mermaid
graph LR
    A[ps aux] -->|stdout| B[grep python]
    B -->|stdout| C[head -5]
    C -->|stdout| T[📺 Terminal]
```

### Ví dụ classic

```bash
# Tìm process Python đang chạy
ps aux | grep python

# Top 10 file lớn nhất trong /var
du -ah /var | sort -rh | head -10

# Đếm số file .py trong project
find . -name "*.py" | wc -l

# Tìm error trong log
cat app.log | grep ERROR | head -20

# Sort + dedupe + count
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head
# ↑ Top IP truy cập nhiều nhất
```

🪞 **Ẩn dụ**: pipe giống **dây chuyền sản xuất**. Mỗi máy nhận đầu vào từ máy trước, xử lý, đẩy sang máy kế. **Triết lý Unix**: "Mỗi chương trình làm 1 việc duy nhất, làm tốt việc đó. Ghép qua pipe để giải bài toán phức tạp."

### Pipe vs Redirect — phân biệt

| | `>` (redirect) | `|` (pipe) |
|---|---|---|
| Đích đến | File trên disk | Process khác |
| Tốc độ | Chậm hơn (ghi disk) | Nhanh (RAM only) |
| Ví dụ | `ls > files.txt` | `ls | grep '.py'` |

---

## 5️⃣ `/dev/null` — Vực sâu vứt output

`/dev/null` là **file đặc biệt** Unix — đọc thì trống, ghi thì biến mất. Dùng để **vứt** output không cần.

```bash
# Chạy lệnh nhưng KHÔNG hiện gì
ls /etc > /dev/null

# Chạy ngầm, không hiện error
some-command 2> /dev/null

# Chạy hoàn toàn im lặng (cả output + error)
some-command &> /dev/null
some-command > /dev/null 2>&1   # cùng nghĩa

# Use case: cron job — không spam mail
0 * * * * /scripts/backup.sh > /dev/null 2>&1
```

🪞 **Ẩn dụ**: `/dev/null` giống **hố đen** — gì rơi vào cũng biến mất, không ai biết. Tài liệu Unix gọi là "the bit bucket".

**Khi nào dùng?**
- Cron job — không muốn email mỗi lần chạy
- Background process — chỉ care exit code, không care output
- Test có lỗi không (chỉ check stderr): `cmd 2>&1 >/dev/null | grep -q error`

---

## 6️⃣ `tee` — Vừa hiển thị vừa lưu file

`tee` đọc stdin, **ghi RA CẢ 2 NƠI**: stdout (terminal) + file.

```bash
# Vừa thấy log trên màn hình, vừa lưu vào file
python app.py | tee app.log

# Append thay vì ghi đè
python app.py | tee -a app.log

# Lưu vào NHIỀU file cùng lúc
echo "deploy started" | tee log1.txt log2.txt log3.txt
```

🪞 **Ẩn dụ**: `tee` giống **chữ T** trong ống nước — 1 dòng chảy vào, 2 dòng chảy ra (terminal + file). Đó là lý do tên `tee`.

### Use case thực tế

```bash
# Cài chương trình đòi sudo + muốn lưu output
sudo make install 2>&1 | tee install.log

# Chạy test, vừa xem realtime vừa save
pytest -v 2>&1 | tee test-result.log

# Apply sudo bằng tee (write vào file chỉ root đọc/ghi được)
echo "127.0.0.1 myhost" | sudo tee -a /etc/hosts
# Vì sao? `echo > /etc/hosts` bị deny (shell redirect không sudo)
# `sudo tee` chạy với root → ghi được
```

---

## 7️⃣ Kết hợp — đọc lệnh phức tạp

Giờ bạn nên đọc được:

### Ví dụ 1
```bash
ps aux | grep python | head -5 > result.txt 2>&1
```

Phân rã:
1. `ps aux` — list mọi process
2. `| grep python` — chỉ giữ dòng có "python"
3. `| head -5` — giữ 5 dòng đầu
4. `> result.txt` — stdout (5 dòng python) → file
5. `2>&1` — stderr cũng vào file đó (nếu có lỗi)

### Ví dụ 2
```bash
docker logs my-container 2>&1 | grep ERROR | tail -20 | tee errors.log
```

Phân rã:
1. `docker logs my-container 2>&1` — log container, gộp stderr vào stdout
2. `| grep ERROR` — chỉ dòng có ERROR
3. `| tail -20` — 20 dòng cuối
4. `| tee errors.log` — vừa in màn hình vừa lưu file

### Ví dụ 3
```bash
curl -s https://api.example.com/users | jq '.[].email' | sort -u > emails.txt
```

Phân rã:
1. `curl -s ...` — fetch JSON từ API (silent mode)
2. `| jq '.[].email'` — extract email field từ JSON
3. `| sort -u` — sort + dedupe
4. `> emails.txt` — lưu file

→ **Đây là "data pipeline trong terminal"** — combine 4 tool thành 1 workflow.

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: `> file` ghi đè file đang đọc

```bash
sort data.txt > data.txt   # ❌ data.txt bị wipe TRƯỚC khi sort đọc
```

- **Lý do**: shell mở `data.txt` để ghi (truncate = 0 bytes) TRƯỚC khi chạy `sort`. `sort` mở file thấy rỗng → kết quả rỗng → ghi rỗng. **Mất data**.
- **Cách tránh**:
  ```bash
  sort data.txt > data.sorted.txt && mv data.sorted.txt data.txt
  # Hoặc tool có flag in-place: sort -o data.txt data.txt
  ```

### ❌ Pitfall: Quên `2>&1`, error không vào file

```bash
python app.py > app.log
# Nếu app crash, error in màn hình (KHÔNG vào app.log)
```

- **Cách đúng**:
  ```bash
  python app.py > app.log 2>&1
  # Hoặc:
  python app.py &> app.log
  ```

### ❌ Pitfall: Pipe đến tool không hỗ trợ stdin

```bash
ls -la | open    # ❌ `open` không đọc stdin
```

- **Lý do**: không phải tool nào cũng đọc từ stdin. Có tool chỉ đọc từ argument file path.
- **Cách workaround**: dùng `xargs` để convert stdin → arguments
  ```bash
  ls *.txt | xargs open       # đúng — xargs truyền filenames làm argument
  ```

### ❌ Pitfall: Thứ tự `2>&1` sai

```bash
cmd 2>&1 > file     # ❌ stderr vẫn ra terminal, chỉ stdout vào file
cmd > file 2>&1     # ✓ cả 2 vào file
```

- **Quy tắc**: redirect xử lý **trái → phải**. Đặt `2>&1` SAU `> file`.

### ❌ Pitfall: Buffer khi pipe

```bash
tail -f log.txt | grep ERROR
# Output có thể delay vài giây — vì grep buffer trước khi flush
```

- **Lý do**: khi stdout là pipe (không phải terminal), nhiều tool dùng line/block buffering thay vì flush ngay.
- **Cách fix**:
  ```bash
  tail -f log.txt | grep --line-buffered ERROR   # grep flush mỗi dòng
  tail -f log.txt | stdbuf -oL grep ERROR        # generic solution
  ```

### ✅ Best practice: Cron job với log proper

Cron mặc định gửi email cho admin mỗi khi job có output. Spam mail nhanh chóng. Pattern chuẩn: redirect cả output + error vào file log, để file log đó cho log rotation xử:

```cron
# ❌ Sai: spam email mỗi giờ (mọi output cron mail cho admin)
0 * * * * /scripts/backup.sh

# ✓ Đúng: lưu output vào file, không spam mail
0 * * * * /scripts/backup.sh > /var/log/backup.log 2>&1
```

### ✅ Best practice: Stream log lớn qua `tee` thay vì redirect

Khi chạy deploy/build dài (vd `npm run build`), nếu redirect thuần `>file` bạn **không thấy gì** trên terminal — phải mở file mới biết tiến độ. Dùng `tee` để xem song song:

```bash
# Vừa thấy log real-time, vừa lưu file
npm run build 2>&1 | tee build-$(date +%Y%m%d-%H%M).log
```

→ Bonus: timestamp trong tên file giúp đỡ overwrite log cũ.

---

## 🧠 Self-check

**Q1.** Phân biệt `cmd > file` và `cmd >> file`?

<details>
<summary>💡 Đáp án</summary>

- **`>`** — **Ghi đè** (overwrite). Mở file ở mode write, truncate (xoá nội dung cũ) → ghi mới.
- **`>>`** — **Append** (nối thêm). Mở file ở mode append → ghi vào cuối file, giữ nội dung cũ.

Demo:
```bash
echo "Line 1" > log.txt    # log.txt = "Line 1"
echo "Line 2" > log.txt    # log.txt = "Line 2"  ← ghi đè
echo "Line 3" >> log.txt   # log.txt = "Line 2\nLine 3"  ← append
```

Use case `>>`: ghi log liên tục (date, status) không mất history.

</details>

**Q2.** `cmd > /dev/null 2>&1` nghĩa là gì?

<details>
<summary>💡 Đáp án</summary>

**Chạy `cmd` hoàn toàn im lặng** — vứt cả output thường + error.

Phân rã:
1. `> /dev/null` — stdout (FD 1) → `/dev/null` (vứt)
2. `2>&1` — stderr (FD 2) → "cùng nơi stdout đang đi" = `/dev/null`

Kết quả: KHÔNG có gì ra terminal/log. Phù hợp cron job, background daemon.

Shortcut tương đương: `cmd &> /dev/null`

</details>

**Q3.** Đọc lệnh `cat /var/log/syslog | grep ssh | tail -10 | tee ssh-recent.log`

<details>
<summary>💡 Đáp án</summary>

Lấy **10 dòng cuối** liên quan **ssh** trong syslog, vừa in màn hình vừa lưu file.

Phân rã từng bước:
1. `cat /var/log/syslog` — đọc toàn bộ syslog ra stdout
2. `| grep ssh` — lọc chỉ giữ dòng có "ssh"
3. `| tail -10` — giữ 10 dòng cuối (gần nhất)
4. `| tee ssh-recent.log` — in ra terminal (stdout) + ghi vào file `ssh-recent.log`

→ Use case: debug login ssh gần đây.

</details>

**Q4.** Vì sao `sort data.txt > data.txt` làm mất data?

<details>
<summary>💡 Đáp án</summary>

**Thứ tự thực thi shell**:

1. Shell parse lệnh, thấy `> data.txt`
2. Shell **mở `data.txt` ở mode write** → **TRUNCATE** file (xoá rỗng) NGAY
3. Shell chạy `sort data.txt` → `sort` mở `data.txt` thấy file **đã rỗng** → output rỗng
4. Output rỗng ghi vào `data.txt` (đã rỗng)
5. **Kết quả: data.txt = rỗng. Data gốc mất hoàn toàn.**

**Cách đúng**: ghi ra file tạm, rồi replace:
```bash
sort data.txt > data.sorted.txt && mv data.sorted.txt data.txt
```

Hoặc dùng tool support in-place:
```bash
sort -o data.txt data.txt   # sort có flag -o ghi out
sed -i 's/old/new/g' file   # sed có -i in-place
```

</details>

---

## ⚡ Cheatsheet

### Output redirect

| Cú pháp | Tác dụng |
|---|---|
| `cmd > file` | stdout → file (ghi đè) |
| `cmd >> file` | stdout → file (append) |
| `cmd 2> file` | stderr → file |
| `cmd 2>> file` | stderr → file (append) |
| `cmd > file 2>&1` | Cả stdout + stderr → file |
| `cmd &> file` | Same shortcut (bash 4+/zsh) |
| `cmd > /dev/null` | Vứt stdout |
| `cmd 2> /dev/null` | Vứt stderr |
| `cmd &> /dev/null` | Chạy im lặng hoàn toàn |

### Input redirect

| Cú pháp | Tác dụng |
|---|---|
| `cmd < file` | Đọc file làm stdin |
| `cmd << EOF ... EOF` | Heredoc inline |
| `cmd <<< "string"` | Here-string |

### Pipe + Tee

| Cú pháp | Tác dụng |
|---|---|
| `cmd1 | cmd2` | stdout cmd1 → stdin cmd2 |
| `cmd1 |& cmd2` | Cả stdout + stderr của cmd1 vào cmd2 (bash 4+) |
| `cmd | tee file` | In terminal + lưu file |
| `cmd | tee -a file` | Tee mode append |
| `cmd | tee f1 f2 f3` | Lưu nhiều file cùng lúc |

### Common patterns

| Pattern | Use case |
|---|---|
| `ps aux \| grep <name>` | Tìm process |
| `tail -f log.txt \| grep ERROR` | Watch log realtime |
| `cmd \| sort \| uniq -c \| sort -rn` | Count + sort frequency |
| `find . \| xargs grep <text>` | Search text in many files |
| `curl -s URL \| jq '.field'` | Parse JSON từ API |
| `cmd 2>&1 \| tee out.log` | Save full output |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| stdin | Standard input | FD 0, input mặc định từ bàn phím |
| stdout | Standard output | FD 1, output mặc định ra terminal |
| stderr | Standard error | FD 2, error/log output ra terminal |
| File Descriptor (FD) | Mô tả file | Số nguyên process dùng tham chiếu I/O stream |
| Redirect | Chuyển hướng | Đổi đích của stream sang file/process khác |
| Pipe | Ống | `|` — nối stdout process này → stdin process kế |
| `/dev/null` | (giữ EN) | "Hố đen" — vứt output |
| `tee` | (giữ EN) | Tool đọc stdin, ghi cả terminal + file |
| Heredoc | (giữ EN) | `<<EOF ... EOF` — input nhiều dòng inline |
| Here-string | (giữ EN) | `<<<` — input 1 string |
| `xargs` | (giữ EN) | Convert stdin → arguments cho lệnh khác |
| Buffer | Đệm | Tool tích trữ output trước khi flush — gây delay khi pipe |
| Unix philosophy | Triết lý Unix | "Mỗi tool làm 1 việc nhỏ, ghép qua pipe" |

---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan trong kho

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [04_env-variables.md](./04_env-variables.md) — Env vars |
| ➡️ Bài tiếp | Cluster basic computing-environment hết — tiếp `02_intermediate/` (chưa có: shell job control, signal trap, advanced redirect, ...) |
| 📚 Lệnh `grep`/`awk`/`sed` cụ thể | `04_OS/linux/lessons/01_basic/` (chưa có bài text processing) |
| 🛠️ Customize shell pipe | [02_Tools/shell/](../../../../02_Tools/shell/) (chưa có) |

### Tài nguyên ngoài

- [Bash Reference Manual — Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) — chính thức
- [Bash Pitfalls — I/O](http://mywiki.wooledge.org/BashPitfalls) — common mistakes
- [Pipeline Programming with Pipe](https://en.wikipedia.org/wiki/Pipeline_(Unix)) — lịch sử pipe
- [Explainshell](https://explainshell.com/) — paste lệnh phức tạp, hiển thị mọi phần làm gì
- [The Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) — triết lý gốc của pipe culture

---

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm 5 lead-in trước code/bảng/diagram (cú pháp tổng quát, ví dụ thực tế, giải mã `2>&1`, bảng tổng hợp, pipe diagram), bổ sung ✅ Best practice thứ 2 (stream log lớn qua tee).
- **v1.0.0 (23/05/2026)** — Bản đầu tiên — **đóng cluster basic computing-environment 6/6**. Cover: 3 streams (stdin/stdout/stderr) với mermaid + ẩn dụ "2 tai, miệng, cờ đỏ", redirect `>`/`>>`/`2>`/`2>&1`/`&>`, giải mã thứ tự `2>&1` quan trọng, input redirect `<` + heredoc, pipe `|` với mermaid dây chuyền + so sánh redirect vs pipe, `/dev/null` "hố đen", `tee` "chữ T", 3 ví dụ kết hợp phức tạp (ps|grep|head, docker logs|grep|tee, curl|jq|sort), 5 pitfall (sort vào chính nó, quên 2>&1, tool không stdin, thứ tự 2>&1, buffer pipe), 4 self-check, cheatsheet đầy đủ + common patterns.
