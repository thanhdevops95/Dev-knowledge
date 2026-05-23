# 06. Security - SSL/TLS & PKI

[← Availability](05_AVAILABILITY.md) | [Tiếp: APIs →](07_APIS.md)

---

# 📚 Bảng thuật ngữ

Trước khi bắt đầu, hãy làm quen với các thuật ngữ quan trọng sẽ xuất hiện trong bài học này:

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Encryption** | /ɪnˈkrɪpʃən/ | Mã hóa - Quá trình biến đổi dữ liệu thành dạng không đọc được để bảo vệ thông tin |
| **Decryption** | /diːˈkrɪpʃən/ | Giải mã - Quá trình ngược lại của mã hóa, biến dữ liệu đã mã hóa về dạng gốc |
| **SSL** | /ˌes.esˈel/ | Secure Sockets Layer - Giao thức mã hóa cũ (đã lỗi thời) |
| **TLS** | /ˌtiː.elˈes/ | Transport Layer Security - Giao thức mã hóa hiện đại, thay thế SSL |
| **HTTPS** | /ˌeɪtʃ.tiː.tiː.piːˈes/ | HTTP + TLS - Giao thức web được mã hóa |
| **Certificate** | /səˈtɪfɪkət/ | Chứng chỉ số - Giấy chứng nhận danh tính của website |
| **CA** | /ˌsiːˈeɪ/ | Certificate Authority - Tổ chức cấp chứng chỉ số |
| **PKI** | /ˌpiː.keɪˈaɪ/ | Public Key Infrastructure - Hệ thống quản lý khóa công khai và chứng chỉ |
| **mTLS** | /ˌem.tiː.elˈes/ | Mutual TLS - TLS hai chiều, cả client và server đều phải xác thực |
| **Handshake** | /ˈhændʃeɪk/ | Bắt tay - Quá trình hai bên thiết lập kết nối an toàn |
| **Public Key** | - | Khóa công khai - Khóa có thể chia sẻ cho mọi người |
| **Private Key** | - | Khóa riêng tư - Khóa phải giữ bí mật tuyệt đối |
| **Plaintext** | - | Văn bản thuần - Dữ liệu chưa được mã hóa |
| **Ciphertext** | - | Văn bản mã - Dữ liệu đã được mã hóa |
| **Root CA** | - | CA gốc - Tổ chức cấp chứng chỉ cao nhất trong chuỗi tin tưởng |
| **Intermediate CA** | - | CA trung gian - Được Root CA ủy quyền để cấp chứng chỉ |
| **DV** | - | Domain Validation - Chứng chỉ xác minh quyền sở hữu tên miền |
| **OV** | - | Organization Validation - Chứng chỉ xác minh tổ chức |
| **EV** | - | Extended Validation - Chứng chỉ xác minh mở rộng (cao nhất) |
| **Zero Trust** | - | Không tin tưởng - Mô hình bảo mật "không tin ai, luôn xác minh" |

---

# 🎬 Câu chuyện mở đầu: Bức thư bị đọc trộm

Hãy tưởng tượng bạn gửi một bức thư cho ngân hàng với nội dung:

```
"Xin chuyển 10 triệu từ tài khoản của tôi.
Mật khẩu: secret123"
```

Bạn đưa thư cho bưu tá. Nhưng trên đường đi:

1. **Bưu tá tò mò** mở thư ra đọc → Biết mật khẩu của bạn
2. **Kẻ xấu** đổi nội dung thành "chuyển 100 triệu" → Bạn mất tiền
3. **Kẻ giả mạo** gửi thư giả danh ngân hàng cho bạn → Lừa đảo

**Đây chính xác là những gì xảy ra khi bạn gửi data qua Internet mà không có encryption!**

---

# 🤔 Tại sao DevOps cần biết về Security?

## Nỗi đau thực tế

> "Tao vừa deploy xong, sếp hỏi sao website không có ổ khóa xanh?"

> "Khách hàng kêu trình duyệt báo 'Not Secure', họ không dám mua hàng"

> "Certificate expired lúc 2 giờ sáng, website down, bị khách complain"

## Những việc bạn sẽ phải làm

| Tình huống | Kiến thức cần |
|------------|---------------|
| Cài HTTPS cho website | SSL/TLS certificates |
| Debug "Certificate expired" | Certificate lifecycle |
| Setup microservices secure | mTLS |
| Answer "HTTPS là gì?" trong interview | Encryption basics |

---

# 📖 Phần 1: Encryption cơ bản

## Encryption là gì?

> **Ẩn dụ đời thường:**
>
> Encryption giống như **viết thư bằng mật mã**. Bạn và người nhận có một "khóa giải mã". Ai không có khóa sẽ chỉ thấy chữ vô nghĩa.

**Encryption** = Biến đổi data thành dạng không đọc được (ciphertext), chỉ người có "khóa" mới đọc được.

```
Không encryption:        Có encryption:
"Mật khẩu: abc123"  →    "Xf9#kL2@mN..."
(Ai cũng đọc được)       (Chỉ vô nghĩa)
```

---

## Vấn đề khi KHÔNG có encryption

```
┌────────────────────────────────────────────────────────────┐
│         KHI BẠN GỬI MẬT KHẨU KHÔNG MÃ HÓA                  │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Bạn                    Kẻ xấu                   Server    │
│   │                       │                        │        │
│   │ ─"Password: abc123"───┼───────────────────────►│       │
│   │                       │                        │        │
│   │                  👀 Đọc được!                  │        │
│   │                  Thấy "abc123"                 │        │
│   │                                                         │
│                                                             │
│  ⚠️ Vấn đề:                                                │
│  • Kẻ xấu thấy mật khẩu của bạn                            │
│  • Kẻ xấu có thể sửa nội dung                              │
│  • Kẻ xấu có thể giả danh server                           │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

## Giải pháp: Encryption

```
┌────────────────────────────────────────────────────────────┐
│         KHI BẠN GỬI MẬT KHẨU ĐÃ MÃ HÓA                     │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Bạn                    Kẻ xấu                   Server    │
│   │                       │                        │        │
│   │ ─"Xf9#kL2@mN..."──────┼───────────────────────►│       │
│   │                       │                        │        │
│   │                  🤷 Không hiểu!               │        │
│   │                  Chỉ thấy rác                  │        │
│   │                                                │        │
│   │                                     Giải mã:   │        │
│   │                                  "abc123" ✓    │        │
│                                                             │
│  ✅ Giải quyết:                                            │
│  • Kẻ xấu chỉ thấy dữ liệu vô nghĩa                        │
│  • Không thể sửa nội dung (sẽ bị phát hiện)               │
│  • Có thể verify danh tính server                          │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 🔑 Hai loại "khóa"

### Loại 1: Symmetric Encryption (Khóa đối xứng)

> **Ẩn dụ:** Giống như **khóa cửa nhà** - cùng một chìa để khóa và mở.

```
┌────────────────────────────────────────────────────────────┐
│              SYMMETRIC ENCRYPTION                           │
│              (Giống khóa cửa nhà)                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Bạn gửi:                      Người nhận:                  │
│                                                             │
│  "Hello"                       "Hello"                      │
│     │                             ▲                         │
│     ▼ Khóa                       │ Mở khóa                  │
│  ┌───────┐                    ┌───────┐                    │
│  │ Chìa  │                    │ Chìa  │                    │
│  │ ABC   │ ◄── CÙNG MỘT ────► │ ABC   │                    │
│  └───────┘      CHÌA          └───────┘                    │
│     │                             ▲                         │
│     ▼                             │                         │
│  "Xf93d" ────────────────────► "Xf93d"                     │
│                                                             │
│  ✅ Ưu điểm: Nhanh                                         │
│  ❌ Nhược điểm: Làm sao đưa chìa cho người nhận an toàn?   │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Vấn đề:** Nếu bạn gửi "chìa khóa" qua Internet, kẻ xấu cũng thấy được!

### Loại 2: Asymmetric Encryption (Khóa bất đối xứng)

> **Ẩn dụ:** Giống như **hộp thư có khe nhỏ**:
>
> - Ai cũng có thể BỎ thư vào khe (public key)
> - Chỉ bạn có chìa khóa để MỞ hộp thư (private key)

```
┌────────────────────────────────────────────────────────────┐
│              ASYMMETRIC ENCRYPTION                          │
│              (Giống hộp thư có khe)                         │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Người gửi:                    Bạn (người nhận):            │
│                                                             │
│  "Hello"                       "Hello"                      │
│     │                             ▲                         │
│     ▼ Bỏ vào khe                 │ Mở hộp                   │
│  ┌───────────────┐            ┌─────────────────┐          │
│  │ PUBLIC KEY    │            │ PRIVATE KEY     │          │
│  │ (khe hộp thư) │            │ (chìa mở hộp)   │          │
│  │ Ai cũng biết  │            │ Chỉ bạn có!     │          │
│  └───────────────┘            └─────────────────┘          │
│     │                             ▲                         │
│     ▼                             │                         │
│  "Xf93d" ────────────────────► "Xf93d"                     │
│                                                             │
│  ✅ Ưu điểm: Public key có thể chia sẻ công khai           │
│  ❌ Nhược điểm: Chậm hơn symmetric                         │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### HTTPS dùng CẢ HAI

```
Bước 1: Dùng Asymmetric để trao đổi "khóa bí mật" an toàn
Bước 2: Dùng Symmetric với "khóa bí mật" đó để mã hóa data (nhanh)
```

---

## 🧪 Thực hành ngay: Xem encryption hoạt động

**Thử 1: Xem website có dùng HTTPS không**

```bash
# Mở trình duyệt, vào google.com
# Nhìn thanh địa chỉ:
# 🔒 = HTTPS (encrypted)
# ⚠️ = HTTP (không encrypted)
```

**Thử 2: Xem certificate của website**

Click vào 🔒 → "Connection is secure" → "Certificate is valid"

Bạn sẽ thấy:

- Tên website (example.com)
- Ai cấp certificate (Let's Encrypt, DigiCert...)
- Ngày hết hạn

**Thử 3: Dùng command line**

```bash
# Xem certificate của Google
echo | openssl s_client -connect google.com:443 2>/dev/null | head -20

# Kết quả (một phần):
# subject=CN = *.google.com
# issuer=O = Google Trust Services, CN = WR2
```

---

# 📖 Phần 2: SSL/TLS là gì?

Hãy cùng tìm hiểu về các giao thức bảo mật quan trọng như SSL, TLS, và mTLS. Từ góc độ "bức tranh toàn cảnh" của system design, đây là chủ đề mà mọi DevOps engineer cần nắm vững vì nó liên quan trực tiếp đến bảo mật của mọi ứng dụng web.

## SSL (Secure Sockets Layer)

**SSL** viết tắt của **Secure Sockets Layer**, là giao thức dùng để mã hóa và bảo mật các giao tiếp diễn ra trên Internet. SSL được phát triển lần đầu vào năm 1995 bởi Netscape nhưng đã bị ngừng sử dụng (deprecated) để nhường chỗ cho TLS (Transport Layer Security).

### Tại sao vẫn gọi là "SSL certificate" nếu nó đã lỗi thời?

Đây là câu hỏi mà nhiều người mới học thường thắc mắc. Hầu hết các nhà cung cấp certificate vẫn gọi chúng là "SSL certificates", đó là lý do tại sao cách gọi này vẫn tồn tại. Điều này tương tự như việc chúng ta vẫn gọi "cuộn băng" dù không còn dùng băng cassette nữa - đó đơn giản là thói quen ngôn ngữ.

### Tại sao SSL lại quan trọng?

Ban đầu, dữ liệu trên web được truyền đi dưới dạng **văn bản thuần** (plaintext) mà bất kỳ ai cũng có thể đọc được nếu họ chặn bắt được tin nhắn đó. Hãy tưởng tượng bạn gửi mật khẩu ngân hàng qua Internet mà ai cũng đọc được - đó là vấn đề nghiêm trọng!

SSL được tạo ra để giải quyết vấn đề này và bảo vệ quyền riêng tư của người dùng. Bằng cách mã hóa mọi dữ liệu truyền giữa người dùng và máy chủ web, SSL còn ngăn chặn một số loại tấn công mạng bằng cách không cho kẻ tấn công can thiệp vào dữ liệu trong quá trình truyền.

## TLS (Transport Layer Security)

**Transport Layer Security**, hay **TLS**, là giao thức bảo mật được sử dụng rộng rãi, được thiết kế để đảm bảo quyền riêng tư và bảo mật dữ liệu cho các giao tiếp trên Internet. TLS phát triển từ giao thức mã hóa trước đó là SSL.

Mục đích sử dụng chính của TLS là mã hóa giao tiếp giữa các ứng dụng web và máy chủ. Mỗi khi bạn thấy "HTTPS" trong thanh địa chỉ của trình duyệt, đó là TLS đang hoạt động.

### Ba thành phần chính của TLS

Giao thức TLS thực hiện ba nhiệm vụ chính:

1. **Mã hóa (Encryption)**: Ẩn dữ liệu đang được truyền khỏi các bên thứ ba. Kẻ tấn công chỉ thấy dữ liệu vô nghĩa.

2. **Xác thực (Authentication)**: Đảm bảo rằng các bên trao đổi thông tin đúng là người mà họ tuyên bố. Bạn biết chắc mình đang nói chuyện với ngân hàng thật, không phải kẻ giả mạo.

3. **Toàn vẹn (Integrity)**: Xác minh rằng dữ liệu không bị giả mạo hoặc sửa đổi. Nếu ai đó thay đổi dữ liệu trên đường truyền, hệ thống sẽ phát hiện.

## Thuật ngữ cần biết

| Thuật ngữ | Ý nghĩa đơn giản | Ẩn dụ |
|-----------|------------------|-------|
| **SSL** | Secure Sockets Layer - Giao thức mã hóa cũ | Phiên bản cũ, như Windows XP |
| **TLS** | Transport Layer Security - Giao thức mã hóa mới | Phiên bản mới, như Windows 11 |
| **HTTPS** | HTTP + TLS = Website được mã hóa | HTTP mặc áo giáp |
| **Certificate** | Giấy chứng nhận danh tính | CMND của website |

## TLS Versions

| Phiên bản | Năm | Tình trạng | Ghi chú |
|-----------|-----|------------|---------|
| SSL 2.0 | 1995 | ❌ Đã chết | Đừng dùng |
| SSL 3.0 | 1996 | ❌ Đã chết | Đừng dùng |
| TLS 1.0 | 1999 | ❌ Đã chết | Đừng dùng |
| TLS 1.1 | 2006 | ❌ Đã chết | Đừng dùng |
| **TLS 1.2** | 2008 | ✅ **Dùng được** | Phổ biến hiện nay |
| **TLS 1.3** | 2018 | ✅ **Tốt nhất** | Nên dùng |

Điều quan trọng cần nhớ là các trình duyệt lớn đã ngừng hỗ trợ TLS 1.0 và 1.1. Nếu máy chủ của bạn chỉ hỗ trợ những phiên bản cũ này, người dùng sẽ thấy lỗi khi truy cập.

---

## TLS hoạt động như thế nào? (Đơn giản hóa)

> **Ẩn dụ: Hai người lạ muốn nói chuyện bí mật**

Hãy tưởng tượng bạn (Client) muốn nói chuyện bí mật với Ngân hàng (Server), nhưng có người nghe lén xung quanh.

```
┌────────────────────────────────────────────────────────────┐
│            TLS HANDSHAKE (Bắt tay làm quen)                │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  BẠN (Client)                     NGÂN HÀNG (Server)       │
│                                                             │
│  ① "Xin chào, tôi muốn                                      │
│     nói chuyện an toàn"  ─────────────────────────────►    │
│                                                             │
│                          ◄─────────────────────────────    │
│                              ② "OK, đây là CMND của tôi    │
│                                 (certificate) và           │
│                                 hộp thư công cộng          │
│                                 (public key)"              │
│                                                             │
│  ③ Bạn kiểm tra CMND:                                      │
│     - Tên có đúng "Ngân hàng ABC"?                         │
│     - Có phải do cơ quan uy tín cấp?                       │
│     - Còn hạn không?                                        │
│                                                             │
│  ④ Bạn tạo "mật khẩu bí mật"                               │
│     và bỏ vào hộp thư của họ ──────────────────────────►   │
│     (chỉ họ mở được)                                        │
│                                                             │
│                          ◄─────────────────────────────    │
│                              ⑤ "OK, tôi đã mở hộp thư      │
│                                 và lấy được mật khẩu.      │
│                                 Giờ ta dùng nó để          │
│                                 mã hóa cuộc trò chuyện"    │
│                                                             │
│  ⑥ Từ giờ, cả hai dùng                                     │
│     "mật khẩu bí mật" để                                   │
│     mã hóa mọi thứ          ◄══════════════════════════►   │
│                                                             │
│  Người nghe lén chỉ thấy: "Xk29#mL!@..." (vô nghĩa)        │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 🧪 Thực hành: Xem TLS handshake thực tế

```bash
# Xem quá trình TLS handshake với Google
curl -v https://google.com 2>&1 | grep -E "TLS|SSL|subject|issuer"
```

**Output mẫu:**

```
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* subject: CN=*.google.com
* issuer: O=Google Trust Services, CN=WR2
```

**Giải thích:**

- `TLSv1.3`: Đang dùng TLS version 1.3
- `Client hello / Server hello`: Bước chào hỏi
- `subject: CN=*.google.com`: Certificate cho domain google.com
- `issuer: Google Trust Services`: Ai cấp certificate

---

# 📖 Phần 3: Certificate và PKI

## Certificate là gì?

> **Ẩn dụ:** Certificate = **CMND/Passport của website**
>
> Khi bạn vào ngân hàng, nhân viên yêu cầu xem CMND để xác nhận bạn là ai.
> Khi bạn vào website, browser kiểm tra certificate để xác nhận đây đúng là website đó.

### Thông tin trong Certificate

| Thông tin | Ví dụ | Giống như |
|-----------|-------|-----------|
| Subject (Tên) | CN=google.com | Họ tên trong CMND |
| Issuer (Nơi cấp) | DigiCert | Công an cấp CMND |
| Valid From | Jan 1, 2024 | Ngày cấp |
| Valid To | Dec 31, 2024 | Ngày hết hạn |
| Public Key | RSA 2048-bit | Địa chỉ hộp thư công cộng |

---

## PKI là gì?

**PKI = Public Key Infrastructure** = Hệ thống cấp và xác nhận CMND cho website

> **Ẩn dụ: Hệ thống cấp CMND**
>
> - **Bộ Công an** (Root CA): Cơ quan cao nhất, ai cũng tin tưởng
> - **Công an Tỉnh** (Intermediate CA): Được Bộ ủy quyền cấp CMND
> - **CMND của bạn** (Certificate): Do Công an Tỉnh cấp

```
┌────────────────────────────────────────────────────────────┐
│               CẤU TRÚC TIN TƯỞNG (Chain of Trust)          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────┐           │
│  │              ROOT CA                         │           │
│  │  (Bộ Công an - ai cũng tin tưởng)           │           │
│  │                                              │           │
│  │  Ví dụ: DigiCert, Let's Encrypt             │           │
│  │  Được cài sẵn trong browser/OS              │           │
│  └───────────────────┬─────────────────────────┘           │
│                      │ cấp phép                             │
│                      ▼                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │          INTERMEDIATE CA                     │           │
│  │  (Công an Tỉnh - được ủy quyền)             │           │
│  │                                              │           │
│  │  Ví dụ: DigiCert SHA2 Extended Validation   │           │
│  │  Cấp certificate cho website                 │           │
│  └───────────────────┬─────────────────────────┘           │
│                      │ cấp                                  │
│                      ▼                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │          YOUR CERTIFICATE                    │           │
│  │  (CMND của website bạn)                      │           │
│  │                                              │           │
│  │  Ví dụ: CN=yourwebsite.com                  │           │
│  │  Cài trên server của bạn                     │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  Browser verify: Certificate → Intermediate → Root         │
│  Nếu Root có trong trust store → Tin tưởng ✓              │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 🧪 Thực hành: Xem certificate chain

```bash
# Xem certificate chain của Google
echo | openssl s_client -connect google.com:443 -showcerts 2>/dev/null | \
  grep -E "s:|i:"
```

**Output:**

```
s:CN = *.google.com                    ← Website certificate
i:O = Google Trust Services, CN = WR2  ← Intermediate CA
s:O = Google Trust Services, CN = WR2  ← Intermediate
i:CN = GlobalSign Root CA              ← Root CA
```

**Giải thích chain:**

1. Website `*.google.com` được cấp bởi `Google Trust Services`
2. `Google Trust Services` được cấp bởi `GlobalSign Root CA`
3. `GlobalSign Root CA` có sẵn trong browser → Tin tưởng!

---

# 📖 Phần 4: Các loại Certificate

## So sánh các loại

| Loại | Xác minh gì? | Thời gian | Giá | Dùng khi |
|------|--------------|-----------|-----|----------|
| **DV** (Domain) | Bạn có sở hữu domain | Vài phút | Miễn phí | Blog, side project |
| **OV** (Organization) | + Công ty có thật | Vài ngày | $$ | Business |
| **EV** (Extended) | + Xác minh kỹ lưỡng | Vài tuần | $$$ | Ngân hàng, e-commerce |

### DV (Domain Validation) - Phổ biến nhất

> **Ẩn dụ:** Như kiểm tra email - "Bạn có access email <admin@domain.com> không?"

**Cách xác minh:**

1. CA gửi email đến <admin@yourdomain.com>
2. Bạn click link xác nhận
3. Xong, bạn có certificate!

**Dùng ở đâu:** Blog, website cá nhân, side project

**Provider miễn phí:** Let's Encrypt

### OV (Organization Validation)

> **Ẩn dụ:** Như xác minh doanh nghiệp - kiểm tra đăng ký kinh doanh

**Cách xác minh:**

- Xác minh domain (như DV)
- - Kiểm tra công ty có đăng ký kinh doanh
- - Gọi điện xác nhận

**Dùng ở đâu:** Website công ty, dịch vụ business

### EV (Extended Validation)

> **Ẩn dụ:** Như xin visa đi Mỹ - kiểm tra mọi thứ rất kỹ

**Cách xác minh:**

- Tất cả của OV
- - Kiểm tra địa chỉ văn phòng
- - Xác minh người đại diện pháp lý
- - Nhiều bước xác minh khác

**Dùng ở đâu:** Ngân hàng, tài chính, e-commerce lớn

---

## 🧪 Thực hành: Xem certificate hết hạn khi nào

```bash
# Kiểm tra ngày hết hạn certificate
echo | openssl s_client -connect google.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Output:
# notBefore=Jan  8 08:25:00 2024 GMT  ← Ngày bắt đầu
# notAfter=Apr  1 08:24:59 2024 GMT   ← Ngày hết hạn
```

**Dùng script kiểm tra nhiều domain:**

```bash
# Tạo file check_cert.sh
for domain in google.com github.com facebook.com; do
  expiry=$(echo | openssl s_client -connect $domain:443 2>/dev/null | \
    openssl x509 -noout -enddate | cut -d= -f2)
  echo "$domain expires: $expiry"
done
```

---

# 📖 Phần 5: mTLS (Mutual TLS)

## mTLS là gì?

**Mutual TLS**, hay **mTLS**, là phương thức **xác thực hai chiều**. mTLS đảm bảo rằng các bên ở hai đầu của kết nối mạng đúng là người mà họ tuyên bố bằng cách xác minh rằng **cả hai đều có private key chính xác**. Thông tin trong các TLS certificate tương ứng của họ cung cấp thêm xác minh.

Trong TLS thông thường, chỉ có server phải chứng minh danh tính - client có thể là bất kỳ ai. Điều này tương tự như khi bạn vào quán cafe: quán có biển hiệu để bạn biết đây là quán thật, nhưng quán không cần biết bạn là ai.

mTLS khác ở chỗ: **CẢ client VÀ server đều phải chứng minh danh tính** - giống như khi bạn vào căn cứ quân sự, bạn phải có thẻ để chứng minh bạn được phép vào.

```
┌────────────────────────────────────────────────────────────┐
│              TLS THƯỜNG vs mTLS                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  TLS THƯỜNG (Vào quán cafe):                                │
│  ┌────────┐                          ┌────────┐            │
│  │  Bạn   │  "Cho tôi vào"           │  Quán  │            │
│  │  (?)   │ ──────────────────────►  │  (✓)   │            │
│  │        │                          │ (có biển)│           │
│  └────────┘                          └────────┘            │
│  Quán không cần biết bạn là ai                              │
│                                                             │
│  ─────────────────────────────────────────────────         │
│                                                             │
│  mTLS (Vào căn cứ quân sự):                                 │
│  ┌────────┐                          ┌────────┐            │
│  │  Bạn   │  "Đây là thẻ của tôi"    │  Căn cứ │           │
│  │  (✓)   │ ◄──────────────────────► │  (✓)   │            │
│  │ (có thẻ)│  "Đây là giấy phép"     │ (có biển)│           │
│  └────────┘                          └────────┘            │
│  CẢ HAI phải chứng minh danh tính                          │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

## Tại sao cần dùng mTLS?

mTLS giúp đảm bảo rằng **lưu lượng truy cập được bảo mật và đáng tin cậy theo cả hai hướng** giữa client và server. Điều này cung cấp thêm một lớp bảo mật cho người dùng khi đăng nhập vào mạng hoặc ứng dụng của tổ chức.

Đặc biệt quan trọng, mTLS còn xác minh các kết nối với **các thiết bị client không tuân theo quy trình đăng nhập**, như các thiết bị Internet of Things (IoT). Một chiếc camera IoT không thể nhập username/password như người dùng, nhưng nó có thể trình certificate để chứng minh nó là thiết bị hợp lệ.

Ngày nay, mTLS được sử dụng phổ biến bởi **microservices** hoặc các hệ thống phân tán trong mô hình **bảo mật zero trust** để các dịch vụ xác minh lẫn nhau. Trong kiến trúc zero trust, không có dịch vụ nào được "tin tưởng mặc định" - mỗi request đều phải được xác thực.

## Khi nào dùng mTLS?

| Use case | Tại sao |
|----------|---------|
| **Microservices** | Service A gọi Service B - cả hai phải xác minh identity để đảm bảo không có service giả mạo trong hệ thống |
| **Zero Trust Architecture** | "Never trust, always verify" - không tin bất kỳ ai, kiểm tra tất cả |
| **IoT Devices** | Thiết bị phải chứng minh nó là thiết bị thật vì không thể login như người dùng |
| **B2B API Security** | Partner phải có certificate để gọi API của bạn, đảm bảo chỉ authorized partners mới access được |

---

# 🔧 Troubleshooting: Lỗi thường gặp

## Lỗi 1: "Certificate has expired"

**Bạn thấy:** Browser hiện cảnh báo đỏ

**Nguyên nhân:** Certificate đã hết hạn

**Cách sửa:**

```bash
# Kiểm tra ngày hết hạn
echo | openssl s_client -connect yourdomain.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Nếu hết hạn: Renew certificate
# Với Let's Encrypt:
sudo certbot renew
```

**Phòng ngừa:** Set up auto-renewal và monitoring

---

## Lỗi 2: "Certificate not trusted"

**Bạn thấy:** "Your connection is not private"

**Nguyên nhân có thể:**

1. Self-signed certificate (tự ký, không có CA)
2. Intermediate certificate bị thiếu
3. Certificate cho domain khác

**Debug:**

```bash
# Xem certificate chain
echo | openssl s_client -connect yourdomain.com:443 2>&1 | \
  grep -E "verify|depth|subject|issuer"
```

**Cách sửa:**

- Dùng certificate từ CA uy tín (Let's Encrypt miễn phí)
- Đảm bảo cài đủ intermediate certificates

---

## Lỗi 3: "SSL_ERROR_PROTOCOL_ERROR"

**Nguyên nhân:** Server chỉ support TLS versions cũ mà browser từ chối

**Debug:**

```bash
# Test TLS 1.2
openssl s_client -connect yourdomain.com:443 -tls1_2

# Test TLS 1.3
openssl s_client -connect yourdomain.com:443 -tls1_3
```

**Cách sửa:** Update server config để support TLS 1.2 trở lên

---

## Lỗi 4: "Certificate does not match domain"

**Nguyên nhân:** Certificate cấp cho domain khác

**Debug:**

```bash
# Xem certificate dành cho domain nào
echo | openssl s_client -connect yourdomain.com:443 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|DNS:"
```

**Cách sửa:** Tạo certificate với đúng domain name

---

# 📝 Tổng kết: Những gì bạn đã học

| Khái niệm | Hiểu đơn giản |
|-----------|---------------|
| **Encryption** | Biến data thành mật mã, chỉ người có "chìa khóa" đọc được |
| **TLS** | Giao thức mã hóa cho web (HTTPS dùng TLS) |
| **Certificate** | CMND của website, chứng minh danh tính |
| **CA** | Cơ quan cấp "CMND" cho website |
| **PKI** | Hệ thống tin tưởng từ Root CA → Intermediate → Your cert |
| **mTLS** | Cả client và server đều phải chứng minh danh tính |

---

## 🎯 Quick Reference: Commands hay dùng

```bash
# Xem certificate của website
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -text

# Xem ngày hết hạn
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Xem certificate chain
echo | openssl s_client -connect example.com:443 -showcerts

# Test TLS handshake (verbose)
curl -v https://example.com 2>&1 | grep -E "TLS|SSL"
```

---

[← Availability](05_AVAILABILITY.md) | [Tiếp: APIs →](07_APIS.md)
