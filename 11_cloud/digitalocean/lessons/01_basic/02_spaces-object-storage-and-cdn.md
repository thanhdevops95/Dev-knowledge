# 🗄️ Spaces — Object Storage + CDN built-in

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~18 phút\
> **Prerequisites:** [01_droplets-and-volumes](01_droplets-and-volumes.md) ✅, hiểu HTTP/REST cơ bản, đã dùng S3/GCS thì càng tốt

> 🎯 *Bài 02 đi sâu **Spaces** — object storage của DO, **S3-compatible** (dùng được mọi SDK S3). Spaces có **CDN built-in** miễn phí. Bạn sẽ học: object storage là gì, Spaces vs S3 so sánh, signed URL (presigned), lifecycle, CORS, hands-on host static site + private file delivery.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Spaces** là gì, vì sao S3-compatible quan trọng
- [ ] So sánh **Spaces vs AWS S3 vs Cloudflare R2** cost & feature
- [ ] Tạo Space + upload/download bằng `s3cmd`/`aws-cli`/SDK
- [ ] Tạo **Spaces Access Key** an toàn (không dùng PAT)
- [ ] Generate **Presigned URL** cho file private
- [ ] Bật **CDN** Spaces (free) + custom domain
- [ ] Setup **Lifecycle policy** auto-delete file cũ
- [ ] Config **CORS** cho web upload trực tiếp
- [ ] Hands-on host static site + secure file delivery

---

## Tình huống — User uploads avatar + invoice PDF

Sếp giao:

> *"Internal tool có 2 use case storage: (1) user upload avatar (public, hiển thị mọi nơi); (2) hệ thống xuất hóa đơn PDF (private, chỉ user sở hữu xem được). Đừng để PDF nằm trên Droplet — chật disk và mất nếu Droplet chết. Dùng object storage gì rẻ, simple, không phải AWS."*

DO **Spaces** fit hoàn hảo:
- $5 flat = 250GB + 1TB transfer.
- S3-compatible → dùng `aws-cli`, `boto3`, mọi tool.
- CDN free đi kèm.
- Presigned URL cho private file.

Bài này dạy đủ để build production.

---

## 1️⃣ Object Storage là gì, vì sao cần

🪞 **Ẩn dụ**: *Object Storage như **nhà kho trên cao** — đồ xếp theo "key" (mã thẻ), không có thư mục thật (chỉ ảo bởi tên có `/`), số lượng vô hạn, không quan tâm thứ tự, lấy ra theo URL. Block Storage (Volume) thì như **ổ cứng laptop** — có thư mục thật, có random access nhanh nhưng dung lượng cố định.*

### So sánh 3 loại storage cloud

| | Block Storage | File Storage | Object Storage |
|---|---|---|---|
| **Đại diện DO** | Volume | (không có managed) | Spaces |
| **Truy cập** | Cấp block (SSD) | NFS/SMB | HTTP REST |
| **Mount được** | Có (1 Droplet) | Có (multi) | Không (qua API) |
| **Dung lượng** | 1-16 TB | TB → PB | Vô hạn |
| **Latency** | < 1 ms | 1-10 ms | 50-200 ms |
| **Giá/GB/tháng** | $0.10 | (n/a) | $0.02 |
| **Phù hợp** | DB, OS disk | Shared filesystem | Static asset, backup, log, media |

### Khi nào dùng Object Storage

- Static assets: ảnh, video, CSS, JS, font.
- User-generated content: avatar, attachment, upload.
- Backup: DB dump, server snapshot tarball.
- Log archive: gzip log lưu trữ dài hạn.
- Data lake: parquet/csv để query sau.
- Static website hosting.

### Khi nào KHÔNG dùng

- Database (cần random read fast, ACID) → Block Storage / Managed DB.
- File hệ thống cần POSIX (vd: Postgres data dir) → Volume.
- Truy cập latency cực thấp (< 10ms) → Volume + cache.

---

## 2️⃣ Spaces là gì — DO Object Storage

### Định nghĩa

**Spaces** = object storage của DO, ra mắt 2017, **API S3-compatible**. Mỗi "Space" = "bucket" trong S3 terminology.

### Đặc điểm 2026

| Đặc điểm | Mô tả |
|---|---|
| **Pricing flat** | $5/tháng: 250GB storage + 1TB outbound transfer + unlimited upload |
| **Vượt** | $0.02/GB extra storage, $0.01/GB extra transfer |
| **API** | S3-compatible (Signature V4), dùng được AWS SDK |
| **CDN built-in** | Free, edge presence ~25 PoP global |
| **Region** | 4 region: `nyc3`, `sfo3`, `ams3`, `sgp1`, `fra1`, `syd1` |
| **Max object size** | 5 TB |
| **TLS** | Bắt buộc HTTPS endpoint |
| **Versioning** | Không có (khác S3) |
| **Lifecycle** | Có (Bucket Lifecycle Policy — expire object after N days) |

### Endpoint pattern

```
https://<space-name>.<region>.digitaloceanspaces.com/<object-key>
```

Ví dụ:
```
https://acmeshop-uploads.sgp1.digitaloceanspaces.com/avatars/user-123.jpg
```

CDN endpoint (nhanh hơn cho global):
```
https://<space-name>.<region>.cdn.digitaloceanspaces.com/<object-key>
```

---

## 3️⃣ Spaces vs S3 vs R2 — Comparison

| | DO Spaces | AWS S3 | Cloudflare R2 |
|---|---|---|---|
| **Base price** | $5/tháng (250GB + 1TB) | $0 base + $0.023/GB | $0 base + $0.015/GB |
| **Storage** | $0.02/GB (vượt 250GB) | $0.023/GB Standard | $0.015/GB |
| **Outbound to internet** | $0.01/GB (vượt 1TB) | $0.09/GB | **$0** (free egress!) |
| **PUT/POST** | Included | $0.005/1k | $4.50/1M |
| **GET** | Included | $0.0004/1k | $0.36/1M |
| **CDN built-in** | ✅ Free | ❌ (CloudFront separate) | ✅ Free |
| **Versioning** | ❌ | ✅ | ✅ |
| **Lifecycle** | ✅ | ✅ | ✅ |
| **S3 SDK** | ✅ | ✅ | ✅ |
| **Compliance** | SOC 2 | SOC2, HIPAA, PCI, FedRAMP, ... | SOC 2 |

### Cost example — 500GB storage, 5TB outbound/tháng

| Vendor | Cost |
|---|---|
| **DO Spaces** | $5 base + ($250GB × $0.02 = $5) + (4TB × $0.01 = $40) = **$50** |
| **AWS S3** | (500GB × $0.023 = $11.50) + (5TB × $0.09 = $460) = **$471.50** |
| **Cloudflare R2** | (500GB × $0.015 = $7.50) + $0 egress = **$7.50** |

→ **DO Spaces** sweet spot cho workload 100-500GB + 1-5TB outbound. **R2** thắng tuyệt đối nếu egress là dominant. **S3** chỉ chọn khi đã ở AWS ecosystem.

> ⚠️ **2026 trend**: nhiều team migrate từ S3 → R2 để cắt egress. DO Spaces vẫn vững vì simple + có CDN sẵn.

---

## 4️⃣ Tạo Space + upload đầu tiên

### Bước 1 — Tạo Space

```bash
# CLI
doctl spaces create acmeshop-uploads \
    --region sgp1

# Hoặc UI: Spaces → Create Bucket → name + region + ACL
```

> ⚠️ Space name phải **unique global** (như S3 bucket). Đặt rõ: `<company>-<purpose>` (vd `acmeshop-uploads`, `acmeshop-static`).

### Bước 2 — Tạo Spaces Access Key

**KHÔNG dùng PAT** cho Spaces — tạo key riêng:

```
UI: API → Spaces Keys → Generate New Key
Name: "acmeshop-uploads-app"
Scope:
  - Read & Write: chọn 1 Space cụ thể (least privilege)
  - Hoặc Full Access (cẩn thận)
```

Copy `Access Key` + `Secret Key` (chỉ show 1 lần).

### Bước 3 — Config `s3cmd` (hoặc `aws-cli`)

#### Option A: s3cmd

```bash
brew install s3cmd

s3cmd --configure
# Access Key: <paste>
# Secret Key: <paste>
# Default Region: US (chấp nhận default, DO không quan tâm)
# S3 Endpoint: sgp1.digitaloceanspaces.com
# DNS-style bucket+hostname: %(bucket)s.sgp1.digitaloceanspaces.com
# Encryption password: (để trống)
# Test access: y
```

#### Option B: aws-cli (S3 compatible)

```bash
aws configure --profile do-spaces
# AWS Access Key ID: <DO key>
# AWS Secret Access Key: <DO secret>
# Default region: us-east-1  (placeholder)
# Default output: json

# Dùng phải kèm endpoint
aws s3 ls --endpoint-url=https://sgp1.digitaloceanspaces.com --profile do-spaces
```

#### Option C: boto3 (Python)

```python
import boto3
from botocore.client import Config

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='sgp1',
    endpoint_url='https://sgp1.digitaloceanspaces.com',
    aws_access_key_id='DO_ACCESS_KEY',
    aws_secret_access_key='DO_SECRET_KEY',
    config=Config(signature_version='s3v4'),
)

# Upload
client.upload_file('avatar.jpg', 'acmeshop-uploads', 'avatars/user-123.jpg')

# Download
client.download_file('acmeshop-uploads', 'avatars/user-123.jpg', 'local.jpg')

# List
for obj in client.list_objects_v2(Bucket='acmeshop-uploads')['Contents']:
    print(obj['Key'], obj['Size'])
```

### Bước 4 — Upload/download cơ bản

```bash
# Upload file
s3cmd put avatar.jpg s3://acmeshop-uploads/avatars/user-123.jpg

# Upload với public ACL
s3cmd put avatar.jpg s3://acmeshop-uploads/avatars/user-123.jpg --acl-public

# Download
s3cmd get s3://acmeshop-uploads/avatars/user-123.jpg ./local.jpg

# List
s3cmd ls s3://acmeshop-uploads/
s3cmd ls s3://acmeshop-uploads/avatars/

# Sync folder
s3cmd sync ./public/ s3://acmeshop-uploads/public/ --acl-public --delete-removed

# Delete
s3cmd del s3://acmeshop-uploads/avatars/user-123.jpg

# Set bucket public read (để serve static)
s3cmd setacl s3://acmeshop-uploads --acl-public
```

---

## 5️⃣ Presigned URL — Private file delivery

🪞 **Ẩn dụ**: *Presigned URL như **vé giữ chỗ tạm thời** — bạn đưa cho khách "vé này có hiệu lực 1 giờ, dùng 1 lần để vào kho lấy đúng món đó". Sau 1 giờ vé hết hạn, không vào được.*

### Vấn đề

PDF hóa đơn user A **không** được để user B xem. Nhưng nếu để Space private hoàn toàn → user không tải được vì không có Spaces key.

→ **Presigned URL**: backend generate URL có signature + expire ngắn (vd 1 giờ), gửi user. User dùng URL đó GET file (qua HTTP thường), hết giờ là vô hiệu.

### Generate presigned URL

#### Python (boto3)

```python
url = client.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'acmeshop-uploads',
        'Key': f'invoices/{user_id}/2026-05-invoice.pdf'
    },
    ExpiresIn=3600,  # 1 giờ
)
print(url)
# https://acmeshop-uploads.sgp1.digitaloceanspaces.com/invoices/u123/2026-05-invoice.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...&X-Amz-Expires=3600&X-Amz-Signature=abc123
```

#### CLI

```bash
aws s3 presign s3://acmeshop-uploads/invoices/u123/2026-05-invoice.pdf \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --expires-in 3600 \
    --profile do-spaces
```

### Presigned URL cho upload (user upload trực tiếp lên Spaces)

Bypass backend, save bandwidth:

```python
# Backend tạo URL upload
url = client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'acmeshop-uploads',
        'Key': f'avatars/{user_id}.jpg',
        'ContentType': 'image/jpeg',
    },
    ExpiresIn=600,  # 10 phút
)
# Trả URL cho frontend
```

Frontend:
```javascript
// User chọn file, upload trực tiếp lên Spaces
const file = document.querySelector('input[type=file]').files[0];
await fetch(presignedUrl, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': 'image/jpeg' }
});
```

→ **Lợi ích**: backend không phải proxy file → giảm tải, giảm bandwidth Droplet.

### Best practices

| BP | Lý do |
|---|---|
| Expire ngắn (5-60 phút) | Limit replay attack |
| Include `Content-Type` khi upload | Tránh user upload file lạ |
| Validate size sau upload | User có thể bypass UI limit |
| Re-generate URL cho mỗi request | Không cache, không share |
| Log generation (audit) | Forensic khi leak |

---

## 6️⃣ CDN built-in — Free edge delivery

### Bật CDN

```
UI: Spaces → <space-name> → Settings → CDN → Enable
TTL: 3600 (default) — tùy nhu cầu
Custom domain: cdn.acmeshop.vn (optional)
```

Hoặc CLI:

```bash
doctl spaces cdn create acmeshop-uploads \
    --ttl 3600
```

### Custom domain CDN

```
1. UI bật CDN → "Add Custom Subdomain"
2. Nhập: cdn.acmeshop.vn
3. DO tạo SSL cert auto (Let's Encrypt)
4. Bạn add CNAME ở DNS:
   cdn.acmeshop.vn → acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com
5. Wait 5-30 phút, SSL active
```

### Endpoint khác biệt

| Loại | URL | Khi dùng |
|---|---|---|
| Origin | `https://acmeshop-uploads.sgp1.digitaloceanspaces.com/avatar.jpg` | Internal, debug |
| CDN | `https://acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com/avatar.jpg` | Public, faster global |
| Custom | `https://cdn.acmeshop.vn/avatar.jpg` | Production, branded |

### Purge cache

```bash
# Purge 1 file
doctl spaces cdn flush <CDN_ID> --files /avatars/user-123.jpg

# Purge all
doctl spaces cdn flush <CDN_ID> --files "*"
```

> ⚠️ Purge mất 1-2 phút propagate edge. Production update file → versioning trong key (`avatar-v2.jpg`) tốt hơn purge.

---

## 7️⃣ Lifecycle policy — Auto-delete

```bash
# Tạo lifecycle JSON
cat > lifecycle.json <<EOF
{
  "Rules": [
    {
      "ID": "delete-temp-after-7days",
      "Status": "Enabled",
      "Filter": { "Prefix": "temp/" },
      "Expiration": { "Days": 7 }
    },
    {
      "ID": "delete-logs-after-90days",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Expiration": { "Days": 90 }
    }
  ]
}
EOF

# Apply
aws s3api put-bucket-lifecycle-configuration \
    --bucket acmeshop-uploads \
    --lifecycle-configuration file://lifecycle.json \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces

# Verify
aws s3api get-bucket-lifecycle-configuration \
    --bucket acmeshop-uploads \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces
```

Lifecycle áp dụng async (DO scan daily) — chấp nhận trễ vài giờ.

---

## 8️⃣ CORS — Web upload trực tiếp

Nếu frontend (https://acmeshop.vn) upload trực tiếp lên Spaces (https://acmeshop-uploads.sgp1...) → browser block do CORS.

### Config CORS

```bash
cat > cors.json <<EOF
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://acmeshop.vn", "http://localhost:3000"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
EOF

aws s3api put-bucket-cors \
    --bucket acmeshop-uploads \
    --cors-configuration file://cors.json \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces
```

> ⚠️ **Đừng** dùng `AllowedOrigins: ["*"]` — security risk. Always list origin cụ thể.

---

## 🛠️ Hands-on — Static site + Private invoice

### Mục tiêu

1. Host static site `https://www.acmeshop.vn` từ Space.
2. Backend tạo presigned URL cho user tải hóa đơn private.

### Phần A — Static site

```bash
# Tạo Space riêng cho static
doctl spaces create acmeshop-static --region sgp1

# Upload site (assume folder ./dist)
s3cmd sync ./dist/ s3://acmeshop-static/ \
    --acl-public \
    --delete-removed \
    --add-header="Cache-Control:public, max-age=3600"

# Bật CDN
doctl spaces cdn create acmeshop-static --ttl 3600

# Custom domain → cdn.acmeshop.vn → CNAME
```

Static site được serve ở `https://acmeshop-static.sgp1.cdn.digitaloceanspaces.com/index.html`.

> Note: DO Spaces chưa có "static website hosting mode" với index.html default ở root như S3. Nếu cần, đứng trước bằng Cloudflare + Page Rules để rewrite.

### Phần B — Private invoice (FastAPI)

```python
# app.py
from fastapi import FastAPI, HTTPException, Depends
import boto3
from botocore.client import Config
import os

app = FastAPI()

s3 = boto3.client(
    's3',
    region_name='sgp1',
    endpoint_url='https://sgp1.digitaloceanspaces.com',
    aws_access_key_id=os.environ['DO_SPACES_KEY'],
    aws_secret_access_key=os.environ['DO_SPACES_SECRET'],
    config=Config(signature_version='s3v4'),
)

@app.get("/invoice/{invoice_id}/download")
def download_invoice(invoice_id: str, user_id: str = Depends(get_current_user)):
    # Kiểm tra invoice thuộc user
    invoice = db.get_invoice(invoice_id)
    if invoice.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    # Generate presigned URL
    key = f"invoices/{user_id}/{invoice_id}.pdf"
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'acmeshop-uploads', 'Key': key},
        ExpiresIn=600,  # 10 phút
    )
    return {"download_url": url, "expires_in": 600}
```

```bash
# Test
curl -H "Authorization: Bearer TOKEN" \
    https://api.acmeshop.vn/invoice/INV-2026-001/download
# > {"download_url":"https://acmeshop-uploads.sgp1...?X-Amz-...","expires_in":600}
```

User browser GET `download_url` → tải PDF. URL hết hạn sau 10 phút.

### Phần C — Upload avatar (presigned PUT)

```python
@app.post("/avatar/upload-url")
def get_avatar_upload_url(user_id: str = Depends(get_current_user)):
    key = f"avatars/{user_id}.jpg"
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'acmeshop-uploads',
            'Key': key,
            'ContentType': 'image/jpeg',
            'ACL': 'public-read',  # avatar public
        },
        ExpiresIn=600,
    )
    public_url = f"https://acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com/{key}"
    return {"upload_url": url, "public_url": public_url}
```

Frontend:
```javascript
const { upload_url, public_url } = await fetch('/avatar/upload-url').then(r => r.json());
await fetch(upload_url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': 'image/jpeg', 'x-amz-acl': 'public-read' }
});
console.log("Avatar at:", public_url);
```

→ **Kết quả**: backend không phải proxy file, user upload trực tiếp lên Spaces qua CDN edge nhanh nhất.

---

## ⚠️ Pitfalls

### 1. Dùng PAT thay vì Spaces Access Key

**Bẫy**: Lấy PAT (Personal Access Token) làm key cho s3cmd → không hoạt động.

**Fix**: Spaces có **API key riêng** (UI → API → Spaces Keys). PAT chỉ cho doctl/DO API, không phải S3 API.

### 2. Region wrong endpoint

**Bẫy**: Space ở `sgp1`, dùng endpoint `nyc3.digitaloceanspaces.com` → 404.

**Fix**: Endpoint phải khớp region: `<region>.digitaloceanspaces.com`.

### 3. Quên bật public-read khi serve asset

**Bẫy**: Upload mặc định private → user không view được → 403.

**Fix**: `s3cmd put --acl-public` hoặc set bucket policy public-read.

### 4. CORS `AllowedOrigins: ["*"]`

**Bẫy**: Wildcard origin → bất kỳ site nào cũng upload được → CSRF risk.

**Fix**: List domain cụ thể. Dev allow `http://localhost:3000`, prod chỉ `https://acmeshop.vn`.

### 5. Presigned URL expire quá dài

**Bẫy**: Expire 7 ngày → user share URL → ai cũng tải được trong 7 ngày.

**Fix**: Expire ngắn (5-60 phút). Long-term sharing → tạo URL mới khi cần.

### 6. Không versioning + overwrite production

**Bẫy**: Spaces **không có versioning**. Upload `index.html` mới → file cũ mất, không rollback được.

**Fix**: 
- Versioning trong key: `index-v2.html`.
- Hoặc deploy 2 stage: `dist/v1/`, `dist/v2/`, switch bằng symlink CDN.
- Backup quan trọng: weekly sync sang S3/B2 độc lập.

### 7. Lifecycle delete data quan trọng

**Bẫy**: Rule "delete after 7 days" áp dụng prefix `temp/` nhưng nhầm path → mất data thật.

**Fix**: Test lifecycle ở dev Space trước. Verify với `aws s3api get-bucket-lifecycle-configuration`.

### 8. CDN cache stale

**Bẫy**: Update `style.css` → user vẫn thấy cũ vì CDN cache 1 giờ.

**Fix**:
- Versioning trong filename: `style-v123.css`.
- Hoặc purge CDN: `doctl spaces cdn flush ID --files "/style.css"`.
- Or set Cache-Control khi upload: `--add-header "Cache-Control:no-cache"`.

### 9. Multipart upload không cleanup

**Bẫy**: Upload file lớn fail giữa chừng → part dở dang vẫn được tính storage.

**Fix**: Lifecycle rule abort incomplete multipart:
```json
{ "ID": "abort-incomplete", "Status": "Enabled",
  "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 } }
```

### 10. Bandwidth ngược (download to Droplet) tính tier transfer

**Bẫy**: App trên Droplet GET ảnh từ Spaces về resize → tính bandwidth Spaces outbound.

**Fix**:
- Cùng region: dùng **internal network** `https://<space>.<region>.digitaloceanspaces.com` (DO không tính transfer intra-region từ 2024).
- Hoặc serve thẳng qua CDN cho user, không proxy qua Droplet.

---

## 🧠 Self-check

**Q1.** Spaces khác Volume thế nào?

<details>
<summary>💡 Đáp án</summary>

- Volume = block storage, mount vào 1 Droplet, latency thấp, dung lượng cố định.
- Spaces = object storage, truy cập qua HTTP API, không mount, dung lượng vô hạn, latency cao hơn (50-200ms).
- Volume cho DB/OS disk; Spaces cho asset/backup.

</details>

**Q2.** Khi nào dùng Presigned URL?

<details>
<summary>💡 Đáp án</summary>

Khi file cần private (chỉ user có quyền xem) nhưng vẫn muốn user tải/upload trực tiếp từ Spaces (bypass backend proxy):
- Download: hóa đơn, file riêng tư của user.
- Upload: user upload avatar trực tiếp lên Spaces, backend chỉ tạo URL.

</details>

**Q3.** CDN của Spaces khác với CloudFront?

<details>
<summary>💡 Đáp án</summary>

- DO CDN: **free**, đi kèm Space, ~25 PoP, ít option cấu hình.
- CloudFront: tính phí $0.085/GB outbound, ~400 PoP, nhiều option (geo block, signed cookies, edge functions Lambda@Edge).

Spaces CDN đủ dùng cho web/asset cơ bản. Cần advanced (geo block, A/B test edge) → CloudFront hoặc Cloudflare đứng trước Spaces.

</details>

**Q4.** Lifecycle policy DO Spaces có gì khác S3?

<details>
<summary>💡 Đáp án</summary>

DO Spaces lifecycle hỗ trợ:
- Expire after N days.
- Abort incomplete multipart.

KHÔNG hỗ trợ (khác S3):
- Transition storage class (DO chỉ 1 class, không có Glacier).
- Noncurrent version expiration (DO không có versioning).

</details>

**Q5.** Vì sao **không** dùng `AllowedOrigins: ["*"]` trong CORS?

<details>
<summary>💡 Đáp án</summary>

Cho phép mọi origin upload/read → attacker site có thể CSRF (lừa user click → upload junk file dưới tên user) hoặc scrape data. Always list origin production cụ thể.

</details>

---

## ⚡ Cheatsheet

| Mục đích | Lệnh |
|---|---|
| Tạo Space | `doctl spaces create NAME --region sgp1` |
| Config s3cmd | `s3cmd --configure` (endpoint: `sgp1.digitaloceanspaces.com`) |
| Upload | `s3cmd put file s3://SPACE/key` |
| Upload public | `s3cmd put file s3://SPACE/key --acl-public` |
| Sync folder | `s3cmd sync ./dist/ s3://SPACE/ --acl-public` |
| Download | `s3cmd get s3://SPACE/key file` |
| List | `s3cmd ls s3://SPACE/` |
| Delete | `s3cmd del s3://SPACE/key` |
| Set ACL bucket | `s3cmd setacl s3://SPACE --acl-public` |
| Bật CDN | `doctl spaces cdn create NAME --ttl 3600` |
| Purge CDN | `doctl spaces cdn flush ID --files "/path"` |
| Presigned URL (Python) | `client.generate_presigned_url('get_object', Params=..., ExpiresIn=600)` |
| Set lifecycle | `aws s3api put-bucket-lifecycle-configuration --bucket ... --endpoint-url=...` |
| Set CORS | `aws s3api put-bucket-cors --bucket ... --endpoint-url=...` |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| **Object Storage** | Lưu trữ đối tượng | Storage theo key-value qua HTTP, không POSIX |
| **Space** | (giữ nguyên) | "Bucket" trong DO terminology |
| **Object** | Đối tượng | 1 file trong Space, có key + data + metadata |
| **Key** | Khoá | Đường dẫn đầy đủ identify object (`avatars/user-123.jpg`) |
| **Bucket** | (giữ nguyên) | Term chung S3 = Space trong DO |
| **S3-compatible** | Tương thích S3 API | Dùng được AWS SDK/CLI để gọi |
| **Presigned URL** | URL ký sẵn | URL có signature + expire, cho phép GET/PUT bypass auth |
| **CDN** | Mạng phân phối nội dung | Edge cache giảm latency global |
| **Origin** | Nguồn gốc | Server gốc lưu file (Space) |
| **PoP** | Point of Presence | Edge location của CDN |
| **TTL** | Time to Live | Thời gian cache trước khi refresh |
| **ACL** | Access Control List | Quyền truy cập (public-read, private) |
| **CORS** | Cross-Origin Resource Sharing | Header cho phép browser request cross-domain |
| **Lifecycle policy** | Chính sách vòng đời | Quy tắc auto-action (expire, transition) |
| **Multipart upload** | Upload nhiều phần | Chia file lớn thành chunks, upload song song |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [01_droplets-and-volumes](01_droplets-and-volumes.md)
- → Tiếp: [03_managed-databases](03_managed-databases.md)
- ↑ Cluster DigitalOcean: [DigitalOcean README](../../README.md)

### Cross-reference
- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — so sánh
- ☁️ [GCP Cloud Storage](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md) — so sánh
- 🐍 [boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — Python SDK S3

### Tài nguyên ngoài (2026)
- 📖 [DO Spaces docs](https://docs.digitalocean.com/products/spaces/)
- 📖 [Spaces API reference](https://docs.digitalocean.com/reference/api/spaces-api/)
- 📖 [s3cmd usage](https://s3tools.org/usage)
- 📖 [Spaces vs S3 comparison](https://www.digitalocean.com/blog/spaces-vs-s3)
- 📖 [Cloudflare R2 docs](https://developers.cloudflare.com/r2/) — alternative
- 📖 [DO CDN docs](https://docs.digitalocean.com/products/spaces/how-to/enable-cdn/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu. Object storage concept + Spaces S3-compatible + comparison S3/R2 + Access Key + s3cmd/boto3 + presigned URL + CDN built-in + Lifecycle + CORS + hands-on static site + private invoice + 10 pitfalls.
