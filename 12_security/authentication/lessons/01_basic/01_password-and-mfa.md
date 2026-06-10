# 🔑 Mật khẩu + Xác thực 2 lớp (MFA)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Bài [00 - Authentication là gì](00_what-is-authentication.md) ✅. Không cần biết crypto trước, mình sẽ giới thiệu khi đến.

> 🎯 *Bài trước bạn đã biết 3 yếu tố xác thực (mật khẩu, vật bạn cầm, sinh trắc học). Bài này đi sâu vào 2 yếu tố đầu — vì sao mật khẩu plain text là thảm hoạ, dùng "băm" (hashing) thế nào cho đúng, làm sao thêm lớp xác thực thứ 2 (TOTP/Passkey) để chống bị chiếm tài khoản. Cuối bài: bạn migrate được DB user từ mật khẩu cũ sang chuẩn 2026, thêm được Passkey cho admin.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu vì sao không bao giờ lưu mật khẩu plain text — và "băm" (*hash*) cho đúng là làm gì
- [ ] Cài + dùng **Argon2id** — thuật toán băm mật khẩu chuẩn 2026 — với tham số phù hợp máy chủ của bạn
- [ ] Check mật khẩu user vừa đặt có nằm trong danh sách bị lộ không (qua *haveibeenpwned API*)
- [ ] Thêm xác thực 2 lớp (MFA) bằng **TOTP** (mã 6 số đổi mỗi 30 giây)
- [ ] Hiểu **Passkey** (chuẩn mới, không bị lừa đảo) và cài cho admin Acme Shop
- [ ] Sinh + verify **backup codes** — chìa khoá dự phòng khi user mất điện thoại
- [ ] Thiết kế luồng "quên mật khẩu" an toàn (chống bị chiếm tài khoản)
- [ ] Migrate 100k user từ hash cũ (SHA-256) sang Argon2id mà không downtime

---

## Tình huống — DB Acme Shop bị "lộ", chuyện gì sẽ xảy ra?

Tháng trước, một công ty bán lẻ Việt Nam bị hacker xâm nhập database. Trong DB có cột `password_hash` lưu mật khẩu user dạng:

```
e10adc3949ba59abbe56e057f20f883e
```

Đây là chuỗi 32 ký tự — kết quả của thuật toán **MD5** băm chuỗi `123456`. Nhìn có vẻ "đã mã hoá rồi", nhưng:

- Mất **0,3 giây** để hacker tra ngược ra `123456` (vì MD5 cũ + mật khẩu phổ biến).
- Bằng máy tính có *GPU* (card đồ hoạ), hacker thử được **20 tỉ mật khẩu mỗi giây**.
- 90% user bị lộ tài khoản trong vòng 1 tiếng.

Sếp Acme Shop đẩy email:

> *"Mình vừa nghe vụ kia. Check lại đi — DB mình dùng gì để lưu mật khẩu? Nếu MD5/SHA cũ thì chuyển ngay. Audit Q3 yêu cầu **Argon2id**. Đồng thời rollout **Passkey** cho admin để chống phishing. Migration không downtime, không bắt user reset. Bạn làm tuần này."*

Bạn nhận spec, mở bài này. 5 việc cần xử:

1. Hiểu vì sao MD5/SHA cũ là "thảm hoạ" — và Argon2id khác như nào.
2. Cài Argon2id với tham số chuẩn cho server của Acme Shop.
3. Migrate DB cũ sang Argon2id mà không bắt 100k user reset password.
4. Check mật khẩu mới có bị lộ ở data breach khác không.
5. Thêm MFA: TOTP cho user thường (tự chọn), Passkey **bắt buộc** cho admin.

Mình sẽ đi qua từng phần. Bắt đầu từ "băm mật khẩu là gì, vì sao mỗi loại khác nhau".

---

## 1️⃣ Băm mật khẩu — tại sao cần, làm thế nào cho đúng

### Tại sao không lưu mật khẩu plain text

🪞 **Ẩn dụ**: *Lưu mật khẩu plain text như viết PIN ngân hàng vào tờ giấy dán trên cửa nhà. Ai đi qua cũng đọc được. Hash giống "khoá nó vào két sắt mà chính bạn cũng không mở được" — chỉ kiểm tra được "chìa khoá này đúng không" mà không lấy lại được mật khẩu gốc.*

Khi user nhập mật khẩu lần đầu (lúc đăng ký), server **không lưu mật khẩu** — server lưu **dấu vân tay** của mật khẩu đó (gọi là *hash*). Đặc tính của hash:

- **Một chiều**: từ mật khẩu → hash dễ. Nhưng từ hash → mật khẩu **không thể đảo ngược trực tiếp** (về mặt toán học).
- **Lặp lại**: cùng mật khẩu → luôn ra cùng hash (deterministic). Lúc user login, server hash mật khẩu user gõ vào, so sánh với hash trong DB.

Nghe có vẻ ổn. Nhưng hacker có 1 cách: **đoán + thử**. Hacker thử băm `123456`, `password`, `qwerty`, ... lần lượt và so sánh với hash leak. Mỗi giây hacker thử được hàng tỉ mật khẩu (với GPU).

→ Vì thế thuật toán băm mật khẩu **phải đủ chậm** để hacker không brute-force được — đó là điểm khác biệt giữa MD5 (nhanh, dễ crack) và Argon2id (chậm có chủ ý, khó crack).

### So sánh các thuật toán băm — vì sao phải chọn đúng

Có nhiều thuật toán băm, nhưng không phải cái nào cũng dùng được cho mật khẩu. Bảng dưới phân biệt rõ:

| Thuật toán | Năm ra | Chống GPU | Tốn RAM khi băm? | Nhận xét |
|---|---|---|---|---|
| **MD5** | 1991 | ❌ Không | Không | **Đã vỡ** — không bao giờ dùng cho mật khẩu |
| **SHA-256 trần** | 2001 | ❌ Không | Không | Là *hash mã hoá* (cryptographic hash), nhưng quá nhanh — không dùng cho mật khẩu |
| **PBKDF2** | 2000 | ⚠️ Yếu | Không | Chỉ dùng khi compliance bắt buộc (FIPS, banking cũ) |
| **bcrypt** | 1999 | ✅ Tốt | Ít (~4 KB) | Đã trưởng thành, OK để dùng fallback |
| **scrypt** | 2009 | ✅ Tốt | Có (tuỳ chỉnh được) | Tốt nhưng Argon2 mới hơn |
| **Argon2id** | 2015 | ✅ Rất tốt | Có (tuỳ chỉnh) | **Mặc định 2026** — thắng cuộc thi Password Hashing Competition |

→ Điểm mấu chốt: **chống GPU** + **tốn RAM**. GPU mạnh tính toán nhưng ít bộ nhớ — buộc thuật toán dùng nhiều RAM thì GPU không brute-force được nhanh. Argon2id làm điều này tốt nhất.

Trong bài này mình dùng **Argon2id**. Lát nữa khi viết code, mình sẽ giải thích tham số `memory_cost` chính là cách "buộc tốn RAM" đó.

### Argon2 có 3 biến thể — chọn cái nào

Argon2 có 3 phiên bản hơi khác nhau, tuỳ tình huống bảo mật:

- **Argon2d** — chống GPU brute-force tốt nhất, nhưng dễ bị tấn công kênh phụ (*side-channel attack* — kẻ tấn công đo thời gian/điện năng tiêu thụ để đoán dữ liệu bí mật).
- **Argon2i** — chống side-channel tốt, nhưng GPU brute-force kém hơn 1 chút.
- **Argon2id** — kết hợp cả 2, lấy ưu điểm mỗi loại. **Mặc định khuyến nghị**.

→ Web/mobile app bình thường → dùng **Argon2id**. Chỉ Argon2d/i khi có yêu cầu compliance đặc biệt.

---

## 2️⃣ Cài Argon2id trong code — tham số chuẩn 2026

### Cài thư viện

Argon2 không có sẵn trong Python tiêu chuẩn — cần cài thư viện riêng. Mình dùng `argon2-cffi` (phổ biến nhất, được Python community maintain):

```bash
pip install argon2-cffi
```

Sau khi cài, thư viện đã sẵn sàng dùng. Verify nhanh:

```python
from argon2 import PasswordHasher
ph = PasswordHasher()
print(ph.hash("test123"))
```

Nếu thấy chuỗi bắt đầu bằng `$argon2id$v=19$...` thì cài thành công.

### Hiểu 3 tham số quan trọng

`PasswordHasher()` ở trên dùng tham số mặc định. Trong production, bạn nên **tự đặt tham số** để cân bằng giữa "đủ chậm để chống hacker" và "đủ nhanh để user không khó chịu khi login":

- `time_cost` — số **vòng lặp băm**. Càng cao càng chậm crack (vì hacker thử mỗi mật khẩu phải lặp cùng số vòng), nhưng cũng chậm login.
- `memory_cost` — **bộ nhớ RAM** thuật toán dùng khi băm (đơn vị KiB). Cao = chống GPU mạnh (GPU ít RAM hơn CPU).
- `parallelism` — số **luồng CPU** chạy song song. Phụ thuộc CPU server có bao nhiêu core.

Mục tiêu khi tune: ~500ms cho mỗi lần hash trên server thật. Login user chờ nửa giây = chấp nhận được. Quá nhanh (<100ms) = hacker brute-force được. Quá chậm (>2s) = UX kém + dễ bị DoS (hacker spam login để server overload).

### Code khởi tạo

Đây là cấu hình **chuẩn 2026** cho server cỡ trung bình (4 vCPU AWS t3.medium / DigitalOcean Premium 4 GB):

```python
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,         # 3 vòng lặp băm
    memory_cost=65536,   # 64 MiB RAM — đủ để chống GPU
    parallelism=4,       # 4 luồng song song
    hash_len=32,         # độ dài hash (32 byte = 256 bit)
    salt_len=16,         # độ dài salt ngẫu nhiên (16 byte)
)
```

`PasswordHasher` ở đây là instance dùng chung toàn app — khởi tạo 1 lần, dùng mọi nơi cần hash/verify mật khẩu. `hash_len` và `salt_len` để mặc định cũng ổn.

→ Sau khi setup, đo thử thời gian thật trên máy chủ của bạn để tinh chỉnh:

```python
import time

start = time.perf_counter()
ph.hash("test123")
elapsed = time.perf_counter() - start
print(f"Hash mất: {elapsed*1000:.0f}ms")
```

Nếu kết quả < 200ms → tăng `memory_cost` lên 131072. Nếu > 1 giây → giảm `time_cost` xuống 2.

### 4 profile tham khảo

Mỗi loại máy chủ phù hợp tham số khác nhau. Đây là 4 profile phổ biến để bạn tham khảo:

| Loại máy chủ | `time_cost` | `memory_cost` | `parallelism` | Thời gian hash |
|---|---|---|---|---|
| Máy ảo nhỏ (2 vCPU, 4 GB RAM) | 3 | 65536 (64 MiB) | 4 | ~0,3-0,5s |
| Server hiện đại (4-8 vCPU) | 4 | 131072 (128 MiB) | 4-8 | ~0,5-1s |
| Bảo mật cao (banking, admin) | 5 | 262144 (256 MiB) | 8 | 1-2s |
| Mobile / edge (Raspberry Pi) | 2 | 32768 (32 MiB) | 2 | ~0,2s |

→ Acme Shop chạy AWS `t3.medium` (4 vCPU, 4 GB) → pick profile 2 trở lên. Tăng `memory_cost` lên 128 MiB nếu free RAM còn nhiều.

### Băm + verify một mật khẩu thật

Có instance `ph` rồi, giờ băm mật khẩu khi user đăng ký:

```python
# Lúc user đăng ký
mat_khau_user_nhap = "Bk!2026secure"  # ví dụ
hash_de_luu_db = ph.hash(mat_khau_user_nhap)
print(hash_de_luu_db)
```

Kết quả có dạng:

```
$argon2id$v=19$m=65536,t=3,p=4$3vKZ1tQ...$wJ8YqL...
```

Format này chứa **mọi thông tin cần thiết**: thuật toán (`argon2id`), version (`19`), tham số (`m=65536,t=3,p=4`), salt ngẫu nhiên (`3vKZ...`), và hash thật (`wJ8YqL...`). Lưu nguyên chuỗi này vào cột `password_hash` trong DB.

Lúc user login, mình verify như sau:

```python
from argon2 import exceptions

mat_khau_user_go = "Bk!2026secure"  # user gõ vào lúc login
hash_trong_db = "$argon2id$v=19$m=65536,t=3,p=4$..."  # đọc từ DB

try:
    ph.verify(hash_trong_db, mat_khau_user_go)
    print("Đúng mật khẩu — cho login")
except exceptions.VerifyMismatchError:
    print("Sai mật khẩu — từ chối")
```

`ph.verify()` tự đọc tham số (`m`, `t`, `p`) + salt từ hash trong DB → băm lại mật khẩu user gõ với cùng tham số → so sánh. Nếu khớp → return, nếu không khớp → throw `VerifyMismatchError`.

### Tự động "rehash" khi tham số bị outdated

Bạn có thể **đổi tham số** Argon2 sau này (ví dụ năm 2027 server mạnh hơn, bạn tăng `memory_cost` lên 256 MiB). Vấn đề: hash cũ trong DB vẫn dùng tham số cũ. Làm sao migrate?

Argon2 hỗ trợ pattern này gọi là *rehash trong-place*:

```python
def login_voi_auto_rehash(email, mat_khau):
    user = db.lay_user_theo_email(email)
    if not user:
        # Verify dummy để tránh tấn công đo thời gian (timing attack)
        ph.verify("$argon2id$v=19$m=65536,t=3,p=4$dummy$dummy", mat_khau)
        raise SaiThongTinDangNhap()

    try:
        ph.verify(user.password_hash, mat_khau)
    except exceptions.VerifyMismatchError:
        raise SaiThongTinDangNhap()

    # Mật khẩu đúng — check tham số trong hash có còn chuẩn không
    if ph.check_needs_rehash(user.password_hash):
        # Tham số đã cũ — băm lại với tham số mới rồi update DB
        user.password_hash = ph.hash(mat_khau)
        db.luu(user)
        log.info(f"Đã rehash mật khẩu cho user_id={user.id}")

    return user
```

→ Pattern này có 2 điểm hay cần để ý:

1. **Dummy verify** ở dòng `ph.verify("$argon2id$...dummy$dummy", ...)` — khi user không tồn tại, mình vẫn chạy 1 lần verify giả để **thời gian phản hồi giống nhau** dù user có hay không. Nếu không có dòng này, hacker đo thời gian phản hồi sẽ biết được username nào tồn tại (*username enumeration* qua *timing attack* — đoán dữ liệu qua thời gian).

2. **Auto-rehash** — mỗi lần user login thành công, kiểm tra hash có dùng tham số mới nhất không. Nếu không → rehash + update DB. Migration **tự động, không cần migration script riêng**.

---

## 3️⃣ Mật khẩu mạnh — chính sách + check bị lộ

### Chính sách mật khẩu — NIST 2024 đã đổi

Ngày xưa các app bắt user đặt mật khẩu phải có chữ hoa + chữ thường + số + ký tự đặc biệt + đổi mỗi 90 ngày. NIST (cơ quan tiêu chuẩn Mỹ) năm 2024 ra hướng dẫn mới — gần như đảo ngược các quy tắc cũ:

| Quy tắc cũ | Quy tắc mới (NIST SP 800-63B-4, final 09/2024) |
|---|---|
| Tối thiểu 6-8 ký tự | **Tối thiểu 8 ký tự** (memorized secret); với *single-factor password*, verifier SHALL yêu cầu **≥ 15** và SHOULD hỗ trợ tới **≥ 64** |
| Phải có hoa + thường + số + ký tự đặc biệt | **Bỏ yêu cầu này** (độ dài quan trọng hơn) |
| Bắt đổi mỗi 90 ngày | **Bỏ** (chỉ đổi khi nghi bị lộ) |
| Cấm dán (paste) password vào ô input | **Bắt buộc cho phép paste** (giúp user dùng password manager) |
| Câu hỏi bảo mật ("tên thú cưng") | **Không khuyến nghị** (dễ tra trên mạng xã hội) |
| (không có) | **Bắt buộc chặn top 10k mật khẩu phổ biến + danh sách bị lộ** |

→ Nguyên lý mới: **dài đánh thắng phức tạp**. Mật khẩu `correct horse battery staple` (28 ký tự, dễ nhớ) an toàn hơn `P@s5w0rd!` (9 ký tự khó nhớ).

### Code validate mật khẩu

Áp dụng quy tắc mới vào code, mình check 3 điều: độ dài, không trong top mật khẩu phổ biến, không bị lộ ở data breach:

```python
# Chuẩn hoá lower-case khi nạp file để khớp với mk.lower() lúc check.
# Nếu file chứa entry có chữ hoa (Password1, Qwerty123) mà chỉ lower 1 đầu
# thì sẽ không bao giờ khớp -> lọt mật khẩu phổ biến (false negative).
COMMON_PASSWORDS = {dong.strip().lower() for dong in open("top10k_breached.txt")}

def validate_mat_khau(mk: str) -> tuple[bool, str | None]:
    """Trả về (ok, thông điệp lỗi nếu fail)."""
    if len(mk) < 8:
        return False, "Mật khẩu phải dài tối thiểu 8 ký tự"
    if len(mk) > 64:
        return False, "Mật khẩu quá dài (tối đa 64 ký tự)"
    if mk.lower() in COMMON_PASSWORDS:
        return False, "Mật khẩu quá phổ biến, chọn cái khác"
    so_lan_bi_lo = check_breach(mk)
    if so_lan_bi_lo > 0:
        return False, f"Mật khẩu này đã bị lộ trong {so_lan_bi_lo:,} vụ data breach. Chọn mật khẩu khác."
    return True, None
```

Function `check_breach()` mình sẽ viết ở section dưới — gọi tới *haveibeenpwned API* để check.

Pattern dùng `set()` cho `COMMON_PASSWORDS` quan trọng: tra cứu trong set là O(1) — dù danh sách 10k mật khẩu thì check chỉ mất < 1 microsecond. Đừng dùng `list` (sẽ chậm dần khi danh sách to).

### Check mật khẩu bị lộ — qua haveibeenpwned (HIBP)

[Have I Been Pwned](https://haveibeenpwned.com) là dịch vụ public lưu **15+ tỉ mật khẩu** đã bị lộ qua các vụ data breach (LinkedIn, Adobe, Yahoo, ...). Họ cung cấp API miễn phí để check 1 mật khẩu có trong danh sách không.

🪞 **Ẩn dụ**: *HIBP như sổ danh sách đen của ngân hàng — trước khi cho user đặt mật khẩu mới, mình check sổ này. Nếu mật khẩu đã từng "ra đường" rồi → từ chối, bắt chọn cái khác.*

Vấn đề: gửi mật khẩu thẳng lên server của HIBP = mất an toàn. May là họ dùng *k-anonymity* (ẩn danh nhóm k phần tử) — kỹ thuật bảo mật cho phép check mà không lộ mật khẩu thật.

Cách hoạt động:

1. Client tính SHA-1 của mật khẩu (40 ký tự hex).
2. Client gửi **chỉ 5 ký tự đầu** của hash lên HIBP — gọi là *hash prefix*.
3. HIBP trả về **danh sách 300-700 hash** có prefix giống (cùng "nhóm k").
4. Client tự so sánh 35 ký tự còn lại trong nhóm để xem mật khẩu có bị lộ không.

→ Server HIBP **không bao giờ thấy mật khẩu thật** — chỉ thấy prefix có thể trùng với hàng nghìn người. Privacy preserved.

Code triển khai:

```python
import hashlib
import requests

def check_breach(mat_khau: str) -> int:
    """Trả về số lần mật khẩu này xuất hiện trong data breach. 0 = chưa bị lộ."""
    # Bước 1: tính SHA-1 (HIBP yêu cầu thuật toán này — không phải vì SHA-1 an toàn,
    # mà vì legacy + đủ để chia nhóm k-anonymity)
    sha1_full = hashlib.sha1(mat_khau.encode()).hexdigest().upper()
    prefix_5_ky_tu = sha1_full[:5]
    phan_con_lai = sha1_full[5:]

    # Bước 2: gửi prefix lên HIBP, không gửi full hash
    try:
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix_5_ky_tu}",
            headers={"User-Agent": "Acme-Shop-Auth"},
            timeout=3,
        )
    except requests.RequestException:
        # API HIBP down — fail-open (cho user đặt mật khẩu). Bù lại bằng check COMMON_PASSWORDS local.
        return 0

    if resp.status_code != 200:
        return 0

    # Bước 3: HIBP trả về danh sách "SUFFIX:COUNT" — mỗi dòng 1 mục
    for line in resp.text.splitlines():
        suffix, count_str = line.split(":")
        if suffix == phan_con_lai:
            return int(count_str)  # Bị lộ! Trả về số lần
    return 0  # Không thấy trong danh sách → an toàn
```

Lưu ý quan trọng: nếu API HIBP down (network lỗi, rate limit), mình *fail-open* — cho user đặt mật khẩu vẫn. Đây là **đánh đổi**: nếu fail-closed (chặn user) thì attacker DoS API HIBP sẽ làm app mất khả năng đăng ký. Để giảm rủi ro, mình duy trì danh sách local `top10k_breached.txt` (bổ sung) check trước.

---

## 4️⃣ Xác thực 2 lớp (MFA) — vì sao + chọn loại nào

### Vì sao mật khẩu thôi không đủ

Dù bạn dùng Argon2id + chính sách mật khẩu mạnh + check breach, vẫn có **3 cách hacker chiếm tài khoản** mà chỉ mật khẩu không chống được:

1. **Phishing** — hacker tạo trang giả `acmesh0p.vn` (số 0 thay chữ o), user gõ đúng email + password vào → hacker có mật khẩu thật.
2. **Credential stuffing** — user dùng cùng mật khẩu cho nhiều site. Site khác bị lộ → hacker thử cùng mật khẩu trên Acme Shop.
3. **Keylogger / malware trên máy user** — hacker đọc được mọi phím gõ, bắt được mật khẩu.

→ Cách chống: **thêm lớp xác thực thứ 2 (MFA)**. Dù hacker có mật khẩu, cần thêm "vật bạn cầm" (điện thoại, Yubikey) mới login được.

### So sánh các loại MFA

Không phải MFA nào cũng giống nhau. 3 thế hệ chính:

| Loại MFA | Cơ chế | An toàn | UX |
|---|---|---|---|
| **SMS OTP** | Server gửi 6 số qua SMS | ⚠️ Yếu — bị *SIM swap* (hacker lừa nhà mạng đổi SIM của bạn sang điện thoại họ) | Tốt — ai cũng có SMS |
| **TOTP** (Time-based OTP) | App authenticator (Google Authenticator, Authy) tự sinh 6 số đổi mỗi 30s | ✅ Tốt — không cần network, không bị SIM swap | Trung bình — user phải mở app, gõ số |
| **WebAuthn / Passkey** | Khoá mã hoá lưu trong điện thoại, xác thực bằng vân tay/Face ID | ✅ Tốt nhất — không thể bị phishing | Tốt nhất — chỉ chạm vân tay 1 lần |

→ Khuyến nghị 2026:
- **WebAuthn/Passkey là chính** — đặc biệt admin Acme Shop bắt buộc dùng.
- **TOTP là fallback** — cho user chưa hỗ trợ Passkey.
- **SMS OTP chỉ khi không còn lựa chọn** — vì rủi ro SIM swap.

Bài này mình triển khai cả 2 (TOTP + Passkey). SMS không hướng dẫn vì khuyến nghị chuyển khỏi nó.

---

## 5️⃣ TOTP — Mã 6 số đổi mỗi 30 giây

### TOTP hoạt động ra sao

🪞 **Ẩn dụ**: *TOTP như đồng hồ Casio đồng bộ với server — cả 2 cùng nhìn đồng hồ + cùng "công thức bí mật" (secret) → cùng ra mã 6 số. Mã đổi mỗi 30 giây để hacker chụp màn hình không kịp dùng. Hacker không có secret → không tính được mã, dù họ có biết đồng hồ.*

Cơ chế (theo chuẩn RFC 6238 — đây là document chính thức của *Internet Engineering Task Force* quy định TOTP):

```
1. Lúc setup: server tạo 1 secret ngẫu nhiên (20 byte, ~32 ký tự base32),
   chia sẻ với điện thoại user qua QR code.

2. Cứ 30 giây, server và điện thoại đều tính:
   số_giây_hiện_tại_chia_30 = floor(unix_time / 30)
   mã_6_số = HMAC-SHA1(secret, số_giây_hiện_tại_chia_30) → lấy 6 chữ số cuối

3. User gõ mã 6 số vào app. Server tính mã của chính nó. So sánh.
   Trùng → cho login. Không trùng → từ chối.
```

→ Vì server và điện thoại đều có secret + đồng hồ → tự tính được mã giống nhau mà **không cần network** (điện thoại offline cũng dùng được Authenticator).

### Cài thư viện TOTP

Mình dùng 2 thư viện:
- `pyotp` — tính + verify mã TOTP (chuẩn RFC 6238)
- `qrcode` — sinh QR code để user scan bằng app authenticator

```bash
pip install pyotp qrcode[pil]
```

### Bước setup: tạo secret + show QR cho user

Khi user lần đầu bật MFA, mình tạo secret + show QR. User mở app Google Authenticator → scan QR → app lưu secret + bắt đầu sinh mã.

```python
import pyotp
import qrcode
import io, base64

def bat_dau_setup_totp(user):
    """Sinh secret, lưu DB, return QR cho frontend hiện."""
    # 1. Sinh secret 32 ký tự base32 ngẫu nhiên
    secret = pyotp.random_base32()

    # 2. Lưu secret vào DB — NHƯNG phải MÃ HOÁ trước (đừng plaintext)
    user.totp_secret_encrypted = ma_hoa_voi_kms(secret)
    user.totp_da_verify = False  # chưa verify mã đầu, đánh dấu "đang setup"
    db.luu(user)

    # 3. Sinh URI chuẩn cho app Authenticator
    #    Format: otpauth://totp/Acme%20Shop:email?secret=XXX&issuer=Acme%20Shop
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="Acme Shop",
    )

    # 4. Convert URI thành QR code PNG → base64 để embed vào trang web
    qr = qrcode.make(uri)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "qr_png_base64": qr_base64,  # frontend hiển thị: <img src="data:image/png;base64,...">
        "secret_text": secret,        # show fallback nếu user không scan được QR
    }
```

3 điểm quan trọng cần để ý:

- **Secret mã hoá trước khi lưu DB**: nếu DB bị lộ, secret plaintext = hacker có mã TOTP của mọi user → MFA vô nghĩa. Mã hoá bằng KMS (AWS KMS, GCP KMS, hoặc HashiCorp Vault).
- **Cờ `totp_da_verify = False`**: bước này chỉ tạo secret, **chưa enable MFA**. User phải verify được mã đầu mới enable thật (tránh trường hợp user scan lỗi, lưu app không nhận, bị lock-out vĩnh viễn).
- **`provisioning_uri`** dùng format chuẩn — app authenticator nào (Google, Authy, 1Password, Bitwarden) cũng đọc được.

### Bước verify: user gõ mã đầu để confirm setup

Sau khi user scan QR, app authenticator hiển thị mã 6 số. User gõ vào để confirm setup OK:

```python
def verify_setup_totp(user, ma_user_go):
    """User gõ mã lần đầu để xác nhận setup OK."""
    secret = giai_ma_kms(user.totp_secret_encrypted)
    totp = pyotp.TOTP(secret)

    if totp.verify(ma_user_go, valid_window=1):
        # Mã đúng → enable MFA chính thức
        user.totp_da_verify = True

        # Sinh backup codes (mình sẽ làm ở section 6)
        backup_codes = sinh_backup_codes(user)
        db.luu(user)

        return {"da_bat_mfa": True, "backup_codes": backup_codes}
    raise MaTotpSai()
```

Tham số `valid_window=1` quan trọng — nó cho phép sai số ±30 giây giữa đồng hồ server và đồng hồ điện thoại user. Vì:

- Điện thoại user có thể lệch giờ vài giây (đặc biệt máy chưa sync NTP).
- User gõ mã hơi chậm — đến lúc bấm submit thì mã đã đổi.

→ `valid_window=1` chấp nhận mã hiện tại + mã 30s trước + mã 30s sau (tổng cửa sổ 90s). Không nên đặt > 2 (vì hacker có nhiều thời gian guess).

### Bước login: user đăng nhập kèm mã TOTP

Khi user đã enable MFA, luồng login thành 2 bước:

```python
def login_voi_mfa(email, mat_khau, ma_totp=None):
    user = login_voi_auto_rehash(email, mat_khau)  # Section 2 đã làm

    if user.totp_da_verify:
        # User có bật MFA — bắt buộc verify mã
        if not ma_totp:
            return {"can_mfa": True, "loai": "totp"}  # frontend show form nhập mã

        secret = giai_ma_kms(user.totp_secret_encrypted)
        if not pyotp.TOTP(secret).verify(ma_totp, valid_window=1):
            # Check backup code trước khi reject (mình làm ở section 6)
            if not verify_backup_code(user, ma_totp):
                audit_log("mfa_fail", user.id)
                raise MaTotpSai()

        audit_log("mfa_success", user.id)

    return tao_session(user)
```

Pattern này có 1 chỗ tinh tế: lần đầu user gọi `login_voi_mfa()` chỉ với email + password, server return `{"can_mfa": True}` — đây là tín hiệu cho frontend hiện form nhập mã TOTP. User gõ mã, gọi lại endpoint với `ma_totp` → server verify, return session token.

→ **Đừng trả lỗi 401 ở bước này** — vì 401 nghĩa "sai mật khẩu". Mật khẩu đã đúng rồi, chỉ thiếu mã MFA. Frontend cần phân biệt 2 trạng thái khác nhau để UX rõ ràng.

---

## 6️⃣ Backup codes — Chìa khoá dự phòng

User có thể mất điện thoại, đổi máy mất app authenticator, hoặc đơn giản là quên. Nếu chỉ có TOTP → user bị lock-out vĩnh viễn.

→ Giải pháp: **backup codes** — sinh sẵn 10 mã dùng-một-lần lúc setup MFA. User in ra giấy hoặc lưu vào password manager. Lúc mất điện thoại, dùng 1 mã backup để login.

🪞 **Ẩn dụ**: *Backup codes như chìa khoá dự phòng cất trong tủ kính của nhà — chỉ đập kính lấy khi cấp cứu. Dùng xong là vứt (one-time).*

### Sinh + lưu backup codes

```python
import secrets

def sinh_backup_codes(user, so_luong=10):
    """Sinh N backup codes, lưu hash vào DB, return plaintext 1 lần cho user."""
    ma_plaintext = []
    for _ in range(so_luong):
        # 10 ký tự, dùng secrets (an toàn cryptography) thay random thường
        ma = secrets.token_urlsafe(8)[:10]
        ma_plaintext.append(ma)

    # Hash từng mã trước khi lưu DB (giống password — nếu DB lộ, mã backup vẫn an toàn)
    for ma in ma_plaintext:
        db.them_backup_code(
            user_id=user.id,
            code_hash=ph.hash(ma),  # dùng cùng Argon2 từ section 2
            da_dung=False,
        )

    return ma_plaintext  # Show 1 lần cho user — bảo họ in/lưu kỹ
```

3 điểm cần để ý:

- **`secrets.token_urlsafe()` thay `random.choice()`** — `random` chuẩn Python không phải *cryptography-secure* (có thể đoán được). `secrets` module sinh số ngẫu nhiên an toàn từ OS-level entropy.
- **Hash mã trước khi lưu** — y hệt password. Nếu DB lộ, hacker thấy hash backup code = chưa lộ mã thật.
- **Show 1 lần duy nhất** — sau khi return, mã plaintext biến mất khỏi server. User phải in/lưu ngay.

### Verify khi user dùng backup code

```python
def verify_backup_code(user, ma_user_go):
    """User gõ backup code (10 ký tự) thay vì mã TOTP. Check rồi vô hiệu hoá."""
    for bc in user.cac_backup_codes:
        if bc.da_dung:
            continue  # Mã đã dùng — bỏ qua

        try:
            ph.verify(bc.code_hash, ma_user_go)
            # Mã đúng → mark là đã dùng, không cho dùng lại
            bc.da_dung = True
            bc.thoi_diem_dung = datetime.utcnow()
            db.luu(bc)

            audit_log("backup_code_used", user.id)

            # Cảnh báo nếu còn ít backup
            so_con_lai = user.so_backup_chua_dung()
            if so_con_lai < 3:
                gui_email(user, f"Bạn còn {so_con_lai} backup codes. Sinh mới để dự phòng.")

            return True
        except exceptions.VerifyMismatchError:
            continue  # Không phải mã này — thử mã tiếp theo

    return False  # Không match mã nào
```

Pattern *loop qua từng backup code* + *Argon2.verify từng cái* nghe có vẻ chậm — nhưng vì mỗi user chỉ có ~10 backup codes, mỗi verify ~500ms → tổng worst case 5 giây. Chấp nhận được cho 1 sự kiện hiếm gặp (user mất điện thoại). Production có thể optimize bằng cách thêm column `prefix` (4 ký tự đầu mã) để filter trước khi verify đầy đủ.

---

## 7️⃣ Passkey — Xác thực không bị phishing

Bây giờ là phần hay nhất: **Passkey** (chuẩn WebAuthn của W3C). Đây là cách xác thực **phishing-resistant** — kể cả khi user gõ đúng credentials vào trang giả `acmesh0p.vn`, hacker vẫn không login được.

🪞 **Ẩn dụ**: *Passkey như chìa khoá số gắn cứng với địa chỉ nhà — chỉ mở được cửa nhà `acmeshop.vn`, không mở được nhà `acmesh0p.vn` dù trông giống y hệt. Hacker copy được mọi thứ trừ "địa chỉ thật của chìa khoá".*

### Vì sao Passkey chống phishing

Khi user setup Passkey lần đầu:

1. Điện thoại (hoặc Yubikey) sinh **cặp khoá public/private** ngẫu nhiên.
2. Private key **không bao giờ rời điện thoại** — chỉ Touch ID/Face ID mới mở khoá dùng được.
3. Public key gửi lên server Acme Shop, lưu vào DB user.
4. Server lưu cả **domain `acmeshop.vn`** vào credential — đây là điểm quan trọng.

Khi login, server gửi 1 thử thách (*challenge* — chuỗi ngẫu nhiên), điện thoại **dùng private key ký challenge** + gửi chữ ký về server. Server verify chữ ký bằng public key đã lưu.

→ Trick là: trình duyệt **tự kiểm tra domain hiện tại có khớp với domain lúc đăng ký không**. Khi user vào `acmesh0p.vn` (giả), trình duyệt thấy domain khác `acmeshop.vn` (thật) → từ chối dùng Passkey. Hacker không lừa được.

So sánh với TOTP: user nhìn mã 6 số là cứ gõ vào — không biết trang giả hay thật. TOTP **bị phishing được**. Passkey thì không.

### Kiến trúc

```
Trình duyệt user ←──── navigator.credentials.create() ────→ Authenticator
                                                          (Touch ID / Face ID / Yubikey)
                                                                 ↓
                                                          Sinh cặp khoá public/private
                                                          Lưu private vào secure element
                                                          Return public key + attestation
                                                                 ↓
Server Acme Shop lưu: (user_id, credential_id, public_key, domain="acmeshop.vn")
```

Khi login:

```
Server → challenge ngẫu nhiên → Trình duyệt → Authenticator
                                                  ↓ (Touch ID mở khoá)
                                                  ↓ Ký challenge với private key
                                                  ↓
                              Trình duyệt → Server: chữ ký
                                                  ↓
                              Server verify chữ ký bằng public key → cho login
```

### Cài thư viện

Mình dùng thư viện `webauthn` của Duo Security (phổ biến + maintain tốt):

```bash
pip install webauthn
```

### Bước 1: User bấm "Đăng ký Passkey" — server tạo options

```python
from webauthn import generate_registration_options
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

def bat_dau_dang_ky_passkey(user):
    """Tạo options cho frontend gọi navigator.credentials.create()."""
    options = generate_registration_options(
        rp_id="acmeshop.vn",            # Relying Party ID = domain
        rp_name="Acme Shop",            # Tên hiển thị cho user khi confirm
        user_id=str(user.id).encode(),  # User ID (bytes)
        user_name=user.email,
        user_display_name=user.ho_va_ten,

        # Yêu cầu authenticator hỗ trợ resident key (= Passkey thật, lưu trong device)
        authenticator_selection=AuthenticatorSelectionCriteria(
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        ),

        # Loại trừ Passkey user đã đăng ký rồi (tránh đăng ký trùng)
        exclude_credentials=[
            {"id": c.credential_id, "type": "public-key"}
            for c in user.cac_passkey
        ],
    )

    # Lưu challenge vào session để verify bước sau
    session["passkey_challenge"] = options.challenge

    return options.dict()
```

→ Server trả về `options` chứa `challenge` ngẫu nhiên + domain + thông tin user. Frontend dùng object này gọi WebAuthn API của browser.

### Bước 2: Frontend gọi WebAuthn API

JavaScript trên trang web:

```javascript
// 1. Lấy options từ server
const optionsResp = await fetch("/auth/passkey/register/begin", { method: "POST" });
const options = await optionsResp.json();

// 2. Convert challenge từ base64 thành ArrayBuffer (yêu cầu của browser API)
options.challenge = base64ToArrayBuffer(options.challenge);
options.user.id = base64ToArrayBuffer(options.user.id);

// 3. Gọi browser API — browser sẽ show prompt vân tay/Face ID
const credential = await navigator.credentials.create({ publicKey: options });

// 4. Gửi credential về server để verify + lưu
await fetch("/auth/passkey/register/finish", {
    method: "POST",
    body: JSON.stringify({
        id: credential.id,
        rawId: arrayBufferToBase64(credential.rawId),
        type: credential.type,
        response: {
            clientDataJSON: arrayBufferToBase64(credential.response.clientDataJSON),
            attestationObject: arrayBufferToBase64(credential.response.attestationObject),
        },
    }),
});
```

→ User chỉ thấy 1 thứ: prompt Touch ID/Face ID. Chạm vân tay → xong. UX cực mượt.

### Bước 3: Server verify credential + lưu

```python
from webauthn import verify_registration_response

def hoan_tat_dang_ky_passkey(user, credential_data):
    """Verify credential từ frontend, lưu vào DB."""
    verification = verify_registration_response(
        credential=credential_data,
        expected_challenge=session["passkey_challenge"],
        expected_origin="https://acmeshop.vn",
        expected_rp_id="acmeshop.vn",
    )

    # Lưu credential vào DB
    db.them_passkey(
        user_id=user.id,
        credential_id=verification.credential_id,
        public_key=verification.credential_public_key,
        sign_count=verification.sign_count,
        ten_thiet_bi=request.headers.get("User-Agent"),  # "iPhone 15 Pro", "MacBook Air"
    )

    return {"thanh_cong": True}
```

`verify_registration_response` làm 4 việc quan trọng đằng sau:
- Verify challenge khớp với cái server đã gửi (chống replay attack — hacker chụp old response thử dùng lại).
- Verify origin khớp `https://acmeshop.vn` (chống phishing).
- Verify chữ ký trên credential (chống tampering).
- Trả về `credential_id` + `public_key` để mình lưu DB.

### Login với Passkey

Tương tự, login có 3 bước (server sinh challenge → browser ký → server verify). Code đầy đủ trong [docs WebAuthn của Duo](https://duo-labs.github.io/py_webauthn/) — pattern y hệt registration, chỉ đổi `generate_authentication_options` + `verify_authentication_response`.

→ Production tip: Passkey **không thay thế hoàn toàn mật khẩu** ở giai đoạn đầu — vì user mất thiết bị thì không login được. Pattern phổ biến: cho user setup Passkey **kèm** mật khẩu, sau đó verify Passkey thay TOTP (mạnh hơn TOTP, UX mượt hơn).

---

## 8️⃣ Luồng "Quên mật khẩu" an toàn

Luồng quên mật khẩu là **điểm yếu nhất** của nhiều app — nếu thiết kế sai, hacker bypass được mọi MFA.

🪞 **Ẩn dụ**: *"Quên mật khẩu" như đổi chìa khoá nhà — nguy hiểm vì attacker có thể giả "Tôi mất chìa". Phải verify đúng chính chủ qua nhiều factor + có khoảng "cool-down" sau khi đổi.*

### Anti-pattern: chỉ email link

```
1. User bấm "Quên mật khẩu" + nhập email
2. Email link reset → user click → đặt password mới
3. Cho login
```

Vấn đề: nếu email user bị chiếm (qua phishing, malware) → hacker click link → có account dù user đã bật MFA. **MFA bị bypass**.

### Pattern an toàn (chi tiết bằng số)

```
1. User bấm "Quên mật khẩu" + nhập email
2. Server rate-limit: max 3 lần / email / 1 giờ (chống spam)
3. Server gửi email link với token:
   - Token ngẫu nhiên 32 ký tự (cryptographically secure)
   - Hết hạn sau 15 phút
   - Dùng 1 lần (single-use)
   - (Tuỳ chọn) gắn IP — chỉ click từ IP request được
4. User click link
5. NẾU user có bật MFA → bắt verify MFA NGAY (TOTP hoặc Passkey) trước khi đổi
6. User đặt mật khẩu mới (qua validate Section 3)
7. Invalidate TẤT CẢ session đang active (logout mọi thiết bị khác)
8. Đặt cool-down 24h: chặn các hành động nhạy cảm (rút tiền, đổi email, tắt MFA)
9. Gửi email + SMS cảnh báo: "Mật khẩu vừa được reset từ IP X, vùng Y"
```

Mỗi bước có lý do:

- **Bước 2 (rate limit)**: chống hacker spam email reset cho mọi user, gây phiền hoặc DoS hệ thống email.
- **Bước 3 (token random 32 ký tự, 15 phút)**: token đoán được = bypass. 32 ký tự cryptographically random + 15 phút expire = không brute-force được.
- **Bước 5 (MFA-required)**: điểm chốt. Email bị chiếm vẫn không đủ — cần thêm điện thoại (TOTP) hoặc vân tay (Passkey).
- **Bước 7 (invalidate sessions)**: nếu hacker đã login từ trước, mật khẩu đổi sẽ kick họ ra. Đừng để hacker tiếp tục dùng session cũ.
- **Bước 8 (cool-down 24h)**: nếu reset là do hacker (chưa biết), không cho họ làm tiếp các action nguy hiểm trong 24h. User chính chủ có thời gian phát hiện + can thiệp.
- **Bước 9 (cảnh báo)**: user thấy email "có người vừa reset password từ Nga" → biết bị tấn công, gọi support ngay.

### Code triển khai

```python
import secrets, hashlib
from datetime import datetime, timedelta

def yeu_cau_quen_mat_khau(email):
    """User bấm 'Quên mật khẩu' — gửi email reset."""
    # Bước 2: rate limit
    if not rate_limit_check(f"forgot:{email}", max=3, window_giay=3600):
        raise HTTPException(429, "Quá nhiều yêu cầu, thử lại sau 1 giờ")

    user = db.lay_user_theo_email(email)
    if not user:
        # Không lộ "email tồn tại hay không" — vẫn return 200
        return {"message": "Nếu email tồn tại, link reset đã được gửi"}

    # Bước 3: sinh token an toàn
    token_plain = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token_plain.encode()).hexdigest()

    db.them_reset_token(
        user_id=user.id,
        token_hash=token_hash,  # Hash để DB leak vẫn an toàn
        het_han_luc=datetime.utcnow() + timedelta(minutes=15),
        ip_request=request.client.host,
    )

    gui_email(
        user.email,
        f"Click link để reset: https://acmeshop.vn/reset?token={token_plain}"
    )
    audit_log("password_reset_requested", user.id)

    return {"message": "Nếu email tồn tại, link reset đã được gửi"}


def reset_mat_khau(token_plain, mat_khau_moi, ma_mfa=None):
    """User click link, đặt mật khẩu mới."""
    token_hash = hashlib.sha256(token_plain.encode()).hexdigest()
    rt = db.lay_reset_token(token_hash)

    if not rt or rt.het_han_luc < datetime.utcnow() or rt.da_dung:
        raise HTTPException(400, "Token không hợp lệ hoặc đã hết hạn")

    user = db.lay_user_theo_id(rt.user_id)

    # Bước 5: nếu user có MFA → bắt verify trước khi đổi password
    if user.totp_da_verify or user.cac_passkey:
        if not ma_mfa:
            return {"can_mfa": True, "loai": user.danh_sach_mfa()}
        if not verify_mfa(user, ma_mfa):
            raise HTTPException(401, "MFA sai")

    # Bước 6: validate + đặt mật khẩu mới
    ok, loi = validate_mat_khau(mat_khau_moi)
    if not ok:
        raise HTTPException(400, loi)

    user.password_hash = ph.hash(mat_khau_moi)
    db.luu(user)

    # Bước 7: invalidate mọi session
    db.xoa_tat_ca_session(user.id)

    # Đánh dấu token đã dùng
    rt.da_dung = True
    db.luu(rt)

    # Bước 8: cool-down 24h
    user.cool_down_den = datetime.utcnow() + timedelta(hours=24)
    db.luu(user)

    audit_log("password_reset_done", user.id)

    # Bước 9: cảnh báo
    gui_email(
        user.email,
        f"Mật khẩu vừa được reset từ IP {request.client.host}. Nếu không phải bạn, liên hệ support ngay."
    )

    return {"thanh_cong": True}
```

---

## 🛠️ Hands-on — Migrate 100k user Acme Shop từ SHA-256 sang Argon2id

Mục tiêu cuối cùng: migrate DB Acme Shop có 100k user dùng SHA-256 → Argon2id, **không downtime**, **không bắt user reset**.

### Bước 1: Thêm cột `hash_algo` vào DB

```sql
ALTER TABLE users
  ADD COLUMN hash_algo VARCHAR(20) DEFAULT 'sha256';
```

Mọi user cũ tự động có `hash_algo='sha256'`. User mới đăng ký sẽ set `hash_algo='argon2id'`.

### Bước 2: Sửa hàm login để hỗ trợ cả 2 hash

```python
import hashlib
from argon2 import PasswordHasher, exceptions

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

def login(email, mat_khau):
    user = db.lay_user_theo_email(email)
    if not user:
        # Dummy verify — tránh timing attack lộ email tồn tại hay không
        ph.verify("$argon2id$v=19$m=65536,t=3,p=4$dummy$dummy", mat_khau)
        raise SaiThongTinDangNhap()

    if user.hash_algo == "sha256":
        # Verify hash cũ (legacy)
        hash_cu = hashlib.sha256(mat_khau.encode()).hexdigest()
        if hash_cu != user.password_hash:
            raise SaiThongTinDangNhap()

        # ✨ ĐIỂM CHÍNH: upgrade tại chỗ
        user.password_hash = ph.hash(mat_khau)
        user.hash_algo = "argon2id"
        db.luu(user)
        log.info(f"Đã upgrade hash của user_id={user.id} sang Argon2id")

    elif user.hash_algo == "argon2id":
        try:
            ph.verify(user.password_hash, mat_khau)
        except exceptions.VerifyMismatchError:
            raise SaiThongTinDangNhap()

        # Trong tương lai nếu nâng tham số Argon2id → cũng auto-rehash
        if ph.check_needs_rehash(user.password_hash):
            user.password_hash = ph.hash(mat_khau)
            db.luu(user)

    return tao_session(user)
```

→ Pattern này hay ở chỗ: **migration tự động xảy ra mỗi lần user login**. Sau 3-6 tháng, ~95% user (những người login ít nhất 1 lần) sẽ tự động chuyển sang Argon2id. Còn lại 5% là user inactive — mình có thể force reset hoặc deprecate sau.

### Bước 3: Theo dõi tiến độ migration

```sql
-- Chạy hàng tuần để xem còn bao nhiêu user cũ
SELECT hash_algo, COUNT(*) as so_user
FROM users
GROUP BY hash_algo;
```

Kết quả mẫu:

```
hash_algo  | so_user
-----------+--------
sha256     |  12,453
argon2id   |  87,547
```

→ Sau 6 tháng, nếu còn user SHA-256 thì gửi email "Đăng nhập lại để bảo mật" + 1 năm sau force reset hoặc xoá tài khoản (sau khi backup).

### Bước 4: Verify trong test environment

Trước khi deploy production, test pattern trên staging:

```python
# Test 1: User cũ SHA-256 login lần đầu → DB phải chuyển sang argon2id
test_user_cu = User(email="cu@test.com",
                     password_hash=hashlib.sha256(b"oldpass").hexdigest(),
                     hash_algo="sha256")
db.luu(test_user_cu)

login("cu@test.com", "oldpass")
assert db.lay_user_theo_email("cu@test.com").hash_algo == "argon2id"  # ✅ đã upgrade

# Test 2: User cũ login lần 2 → vẫn OK với hash mới
login("cu@test.com", "oldpass")  # không throw

# Test 3: User không tồn tại → phải mất thời gian ≈ login thật (chống timing attack)
import time
t1 = time.perf_counter()
try: login("khong-ton-tai@test.com", "anything")
except: pass
t1 = time.perf_counter() - t1
assert t1 > 0.1  # > 100ms = đã chạy dummy verify
```

---

## ⚠️ Các bẫy thường gặp

### 1. Argon2 tham số quá nhẹ
- **Triệu chứng**: `time_cost=1, memory_cost=16384` → hash mất < 50ms.
- **Hậu quả**: GPU brute-force vẫn được.
- **Cách tránh**: target ~500ms trên server thật. Tăng `memory_cost` lên 128 MiB nếu hash quá nhanh.

### 2. Lưu secret TOTP plaintext trong DB
- **Triệu chứng**: cột `totp_secret` trong DB là chuỗi base32 không mã hoá.
- **Hậu quả**: DB lộ = hacker có mã TOTP của mọi user = MFA vô nghĩa.
- **Cách tránh**: mã hoá secret bằng KMS (AWS KMS, GCP KMS, Vault) trước khi lưu.

### 3. `valid_window` quá cao
- **Triệu chứng**: `valid_window=5` (chấp nhận ±150s).
- **Hậu quả**: hacker có 5 phút để brute-force mã (nhiều thử hơn).
- **Cách tránh**: `valid_window=1` (±30s) là đủ. NTP sync server đồng hồ.

### 4. Backup codes plaintext trong DB
- **Triệu chứng**: lưu thẳng `["abc12345", "def67890", ...]`.
- **Hậu quả**: DB leak = mọi backup code lộ.
- **Cách tránh**: hash với Argon2 (cùng như password).

### 5. Quên mật khẩu không cần MFA
- **Triệu chứng**: user click email reset → đổi password ngay không verify MFA.
- **Hậu quả**: email bị chiếm = full takeover dù user có MFA.
- **Cách tránh**: nếu user đã setup MFA → bắt verify MFA trong luồng reset.

### 6. Passkey `rp_id` sai cấu hình
- **Triệu chứng**: app có nhiều subdomain (`api.acmeshop.vn`, `admin.acmeshop.vn`), Passkey không dùng được cross-subdomain.
- **Hậu quả**: user đăng ký Passkey trên `acmeshop.vn` không login được `admin.acmeshop.vn`.
- **Cách tránh**: set `rp_id="acmeshop.vn"` (domain cha) — Passkey work với mọi subdomain.

### 7. Session không invalidate sau đổi mật khẩu
- **Triệu chứng**: user đổi password, các thiết bị cũ vẫn login được.
- **Hậu quả**: nếu hacker đã có session, đổi password không kick được họ.
- **Cách tránh**: `db.xoa_tat_ca_session(user.id)` ngay sau khi đổi password.

### 8. Dùng `random` thay `secrets`
- **Triệu chứng**: `random.choice()` để sinh token.
- **Hậu quả**: `random` không cryptographically secure — hacker đoán được next token nếu biết seed.
- **Cách tránh**: luôn dùng `secrets` module cho mọi giá trị nhạy cảm.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Vì sao không lưu mật khẩu plain text, mà phải băm? Nếu hash one-way thì server làm sao verify khi user login?

<details>
<summary>💡 Đáp án</summary>

- Lưu plain text = DB lộ → mọi mật khẩu lộ ngay → user mất các tài khoản khác (vì user thường dùng chung mật khẩu).
- Hash one-way: server không lấy lại được mật khẩu gốc, nhưng có thể **băm lại** mật khẩu user gõ vào lúc login + so sánh với hash đã lưu. Cùng input → cùng hash (deterministic).
</details>

**Q2.** Vì sao MD5/SHA-256 không dùng cho mật khẩu được, dù chúng đúng là *one-way hash*?

<details>
<summary>💡 Đáp án</summary>

MD5/SHA-256 thiết kế để **nhanh** (verify dữ liệu lớn). Với GPU, hacker thử được hàng tỉ mật khẩu/giây → brute-force xong < 1 giờ cho mật khẩu phổ biến. Argon2id chậm có chủ ý + tốn RAM → GPU brute-force kém hiệu quả.
</details>

**Q3.** TOTP và Passkey đều là MFA. Vì sao Passkey **chống phishing** mà TOTP **không**?

<details>
<summary>💡 Đáp án</summary>

- TOTP: user nhìn mã 6 số trong app + gõ vào trang web. Nếu trang web là giả (`acmesh0p.vn`), user vẫn gõ → hacker thu được mã + dùng login site thật trong 30s.
- Passkey: browser **tự check domain** trước khi cho phép dùng credential. Trang giả → credential không kích hoạt → user không thể "lỡ tay" cho hacker mã.
</details>

**Q4.** Vì sao trong luồng login mình có dòng `ph.verify("$argon2id$...dummy$dummy", password)` khi user không tồn tại?

<details>
<summary>💡 Đáp án</summary>

Chống *timing attack* (tấn công đo thời gian). Nếu user tồn tại → mình verify hash (mất ~500ms). Nếu không tồn tại → mình trả lỗi ngay (~1ms). Hacker đo thời gian phản hồi sẽ biết "email này có trong hệ thống". Dummy verify đảm bảo cả 2 trường hợp đều ~500ms → hacker không phân biệt được.
</details>

**Q5.** Migration SHA-256 → Argon2id mà không bắt user reset — cơ chế gì?

<details>
<summary>💡 Đáp án</summary>

Pattern **upgrade-tại-chỗ** (in-place upgrade): khi user login, mật khẩu plain text **đang có trong RAM** (user vừa gõ vào). Mình:
1. Verify hash cũ với mật khẩu vừa gõ.
2. Nếu đúng → băm lại bằng Argon2id, ghi đè vào DB.
3. Đánh dấu `hash_algo='argon2id'`.

Lần login kế tiếp dùng hash mới luôn. Sau 6 tháng, ~95% user (active) tự chuyển. User inactive xử sau.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Code Python |
|---|---|
| Khởi tạo hasher | `ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)` |
| Hash mật khẩu | `ph.hash(mat_khau)` |
| Verify mật khẩu | `ph.verify(hash_trong_db, mat_khau)` (throw nếu sai) |
| Check rehash cần thiết | `ph.check_needs_rehash(hash_trong_db)` |
| Sinh secret TOTP | `pyotp.random_base32()` |
| Verify mã TOTP | `pyotp.TOTP(secret).verify(ma, valid_window=1)` |
| Sinh token an toàn | `secrets.token_urlsafe(32)` |
| Check HIBP breach | `requests.get(f"https://api.pwnedpasswords.com/range/{sha1_5_ky_tu_dau}")` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| Hash | Băm | Hàm 1 chiều: input → output cố định, không thể đảo ngược trực tiếp |
| Argon2id | Argon2id (giữ nguyên) | Thuật toán băm mật khẩu thắng cuộc thi PHC 2015, mặc định 2026 |
| Salt | Muối | Chuỗi ngẫu nhiên thêm vào mật khẩu trước khi băm, chống tấn công bằng bảng tra cứu (rainbow table) |
| Pepper | Tiêu | Bí mật toàn server (lưu env/KMS) thêm vào hash, lớp bảo vệ phụ |
| MFA | Xác thực 2 lớp | Multi-Factor Authentication — yêu cầu ≥ 2 yếu tố khác loại |
| TOTP | Mã 6 số đổi mỗi 30s | Time-based One-Time Password — chuẩn RFC 6238 |
| HOTP | Mã 6 số đếm theo lượt | HMAC-based OTP — alternative TOTP, dùng counter thay timestamp |
| WebAuthn | API xác thực web chuẩn W3C | Cho phép trình duyệt dùng vân tay/face ID/Yubikey |
| Passkey | Passkey | Tên thương hiệu (Apple/Google) cho WebAuthn |
| Phishing | Lừa đảo | Trang giả mạo dụ user gõ credentials |
| SIM swap | Cướp số điện thoại | Hacker lừa nhà mạng đổi SIM của bạn sang điện thoại họ |
| Timing attack | Tấn công thời gian | Đoán dữ liệu bí mật qua đo thời gian phản hồi |
| Side-channel attack | Tấn công kênh phụ | Đoán dữ liệu qua đo điện năng, thời gian, âm thanh — không bẻ mã trực tiếp |
| Credential stuffing | Nhồi credentials | Hacker dùng mật khẩu lộ từ site khác thử login site mới |
| Rainbow table | Bảng tra cứu | DB hash phổ biến đã tính sẵn — chống bằng salt |
| k-anonymity | Ẩn danh trong nhóm k | Kỹ thuật privacy: thay vì gửi hash đầy đủ, gửi prefix → trộn với k phần tử khác |
| `valid_window` | Cửa sổ hợp lệ | Số window (mỗi 30s) chấp nhận quanh thời điểm hiện tại |
| `rp_id` | Relying Party ID | Domain định danh của bên xác thực — quan trọng cho Passkey chống phishing |
| `sign_count` | Bộ đếm chữ ký | Tăng mỗi lần Passkey ký challenge — chống replay |

---

## 🔗 Liên kết & Tài nguyên

### Bài tiếp theo trong kho
- [02 — OAuth 2.1 + OIDC](02_oauth-and-oidc.md) — đăng nhập qua Google/Apple/Facebook
- [03 — JWT + Session deep](03_jwt-and-sessions-deep.md) — sau khi user verify mật khẩu/MFA, cấp token thế nào
- [04 — Federation + SSO](04_federation-sso-and-idp.md) — enterprise: dùng Keycloak làm IdP cho cả công ty

### Bài liên quan trong kho
- ↑ **Về cụm:** [00 — Authentication là gì](00_what-is-authentication.md) — nền tảng AuthN vs AuthZ
- 🛡️ [OWASP A07 — Auth failures](../../../owasp-top-10/lessons/01_basic/04_auth-failures-logging-and-ssrf.md) — overview
- 🛡️ [OWASP A02 — Crypto failures](../../../owasp-top-10/lessons/01_basic/02_crypto-failures-and-secure-design.md) — encryption deep

### Tài nguyên ngoài (đọc thêm)
- 📖 [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) — chuẩn vàng về băm mật khẩu
- 📖 [NIST SP 800-63B-4 (final 09/2024)](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b-4.pdf) — guideline chính thức Mỹ
- 📖 [Argon2 spec (PHC)](https://github.com/P-H-C/phc-winner-argon2) — spec gốc + reference implementation
- 📖 [haveibeenpwned API docs](https://haveibeenpwned.com/API/v3) — k-anonymity workflow
- 📖 [RFC 6238 — TOTP](https://datatracker.ietf.org/doc/html/rfc6238) — chuẩn TOTP gốc
- 📖 [WebAuthn Guide](https://webauthn.guide/) — tutorial WebAuthn cơ bản
- 📖 [Passkeys.dev](https://passkeys.dev/) — tài liệu Apple/Google về Passkey
- 📖 [py_webauthn docs](https://duo-labs.github.io/py_webauthn/) — thư viện Python được dùng trong bài

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên (đã bị thay thế bởi v2.0.0 do vi phạm Blueprint).
- **v2.0.0 (24/05/2026)** — Rewrite hoàn toàn theo Blueprint v0.5.3. Lý do: bản v1.0.0 vi phạm §3.6 (header → code ngay không lead-in) + §3.7 (English-heavy, comments code English). Bản này: mỗi code block có 2-3 câu lead-in giải thích "vì sao" + "expect gì", comments code tiếng Việt, mọi thuật ngữ EN xuất hiện lần đầu đều italic + dịch + giải thích, định nghĩa "trả lời tình huống" thay định nghĩa khô. Nội dung kỹ thuật giữ nguyên (Argon2id, TOTP, Passkey, recovery flow, migration pattern).
- **v2.1.0 (07/06/2026)** — Fix QA: (1) sửa bug case-mismatch trong `COMMON_PASSWORDS` — nạp file `top10k_breached.txt` đã lower-case để khớp với `mk.lower()` lúc check (tránh lọt mật khẩu phổ biến có chữ hoa, false negative); (2) chuẩn hoá trích dẫn NIST: ghi rõ **SP 800-63B-4 (final 09/2024)**, tách ngữ cảnh "min 8 cho memorized secret / SHALL ≥ 15 cho single-factor password / SHOULD ≥ 64", sửa link tài nguyên từ bộ -3 cũ sang bản -4 chính thức.
- **v2.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
