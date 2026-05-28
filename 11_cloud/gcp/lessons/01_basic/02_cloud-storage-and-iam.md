# 📦 GCP Cloud Storage + IAM

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [01_compute-engine-and-disks](01_compute-engine-and-disks.md) ✅

> 🎯 *Bài 02. Cloud Storage (GCS) = object storage, analog AWS S3. IAM = permission system thực sự work khi áp dụng đúng. Bài này dạy: bucket type, storage class, lifecycle, versioning, signed URL, IAM vs bucket-level ACL, uniform vs fine-grained, CMEK encryption, Object Versioning/Retention. Hands-on upload + signed URL + static hosting.*

## 🎯 Sau bài này bạn sẽ

- [ ] Chọn đúng **storage class** (Standard/Nearline/Coldline/Archive) per use case
- [ ] Dùng **uniform bucket-level access** thay vì ACL (best practice 2026)
- [ ] Tạo **signed URL** thời hạn cho upload/download direct
- [ ] Setup **Object Lifecycle Management** (auto-archive sau N ngày)
- [ ] Bật **Object Versioning** + **Retention Policy** (compliance)
- [ ] Configure **CORS** cho web app upload trực tiếp
- [ ] Mã hóa **CMEK** (Customer-Managed Encryption Key) qua Cloud KMS
- [ ] Phân biệt **IAM role** vs **legacy ACL**
- [ ] Setup static website hosting + Cloud CDN

---

## Tình huống — Acme Shop cần object storage

Sếp:

> *"Acme Shop cần: lưu ảnh sản phẩm (10M ảnh, 200 GB), user upload ảnh đại diện (direct browser → GCS), backup database (cold storage 7 năm compliance), static site `static.acmeshop.vn`. Cost optimization mạnh + compliance audit logs đầy đủ."*

Bạn cần:
- 3 bucket khác nhau (`acmeshop-products`, `acmeshop-uploads`, `acmeshop-backups`).
- Storage class phù hợp (Standard / Coldline).
- Signed URL cho direct upload từ frontend.
- Lifecycle rule chuyển Standard → Coldline → Archive theo thời gian.
- Retention 7 năm cho backup (compliance).
- IAM giới hạn ai làm gì.

→ Bài này dạy toàn bộ.

---

## 1️⃣ Cloud Storage cơ bản

🪞 **Ẩn dụ**: *Cloud Storage như **kho hàng tự phục vụ vô hạn của Google** — bạn không cần quan tâm kệ nào, kho nào; bạn chỉ cần dán nhãn (object name) cho gói hàng. Có 4 loại kệ giá tiền khác nhau (Standard/Nearline/Coldline/Archive) — bạn chọn tùy tần suất lấy hàng.*

### Khái niệm

| Khái niệm | Mô tả |
|---|---|
| **Bucket** | Top-level container (tên unique global, gắn 1 project) |
| **Object** | File + metadata |
| **Object name** | Path-like, e.g. `products/img-1234.jpg` (không có folder thật) |
| **Location** | Region (`asia-southeast1`), Dual-region (`asia1`), Multi-region (`asia`) |
| **Storage class** | Standard / Nearline / Coldline / Archive |

### Storage classes 2026

| Class | Cost storage/GB-month | Cost retrieval/GB | Min duration | Khi dùng |
|---|---|---|---|---|
| **Standard** | $0.020 (multi) / $0.020 (regional) | Free | None | Active data, < 1 month |
| **Nearline** | $0.010 | $0.010 | 30 days | Backup truy cập < 1/tháng |
| **Coldline** | $0.004 | $0.020 | 90 days | Archive, < 1/quarter |
| **Archive** | $0.0012 | $0.050 | 365 days | Compliance, < 1/year |

→ **Lifecycle**: bắt đầu Standard, tự transition sang Nearline/Coldline/Archive theo tuổi object.

### Location types

| Type | Mô tả | Cost | Use case |
|---|---|---|---|
| **Regional** | 1 region (e.g. `asia-southeast1`) | Rẻ nhất | Latency-sensitive single-region |
| **Dual-region** | 2 region cụ thể (e.g. `asia1` = Tokyo + Osaka) | Mid | DR cross-region |
| **Multi-region** | Continent (`asia`, `us`, `eu`) | Cao | Global reach, public assets |

---

## 2️⃣ IAM — Uniform vs Fine-grained access

### Uniform bucket-level access (RECOMMEND 2026)

- IAM **only** — không có ACL per object.
- Đồng nhất: nếu user có quyền với bucket → có quyền với mọi object.
- **Default 2026** + bắt buộc cho mọi bucket mới production.

```bash
# Bật uniform khi tạo
gcloud storage buckets create gs://acmeshop-products \
    --uniform-bucket-level-access \
    --location=asia-southeast1
```

### Fine-grained (legacy)

- IAM **+** ACL per object.
- Phức tạp, dễ leak permission.
- Tránh trừ khi migration từ S3 ACL.

### Predefined roles GCS

| Role | Quyền |
|---|---|
| `roles/storage.objectViewer` | Đọc object |
| `roles/storage.objectCreator` | Tạo object (không sửa/xóa) |
| `roles/storage.objectUser` | Đọc/tạo/xóa object trong bucket |
| `roles/storage.admin` | Full bucket + object |
| `roles/storage.legacyBucketReader` | List object (legacy) |

### Grant role

```bash
# Grant user view object
gcloud storage buckets add-iam-policy-binding gs://acmeshop-products \
    --member="user:thien.le@acmeshop.vn" \
    --role="roles/storage.objectViewer"

# Grant service account upload
gcloud storage buckets add-iam-policy-binding gs://acmeshop-uploads \
    --member="serviceAccount:upload-sa@acmeshop-prod.iam.gserviceaccount.com" \
    --role="roles/storage.objectCreator"

# Public bucket (cẩn thận!)
gcloud storage buckets add-iam-policy-binding gs://acmeshop-static \
    --member="allUsers" \
    --role="roles/storage.objectViewer"
```

### `allUsers` vs `allAuthenticatedUsers`

- `allUsers` = Internet ai cũng access (public).
- `allAuthenticatedUsers` = bất kỳ Google account nào sign-in.
- → **Public bucket** chỉ dùng cho static asset; **không** chứa data nhạy cảm.

### Public Access Prevention

Bật để **chặn public access** ngay cả khi vô ý grant `allUsers`:

```bash
gcloud storage buckets update gs://acmeshop-products \
    --public-access-prevention
```

→ **Default 2026** cho bucket private.

---

## 3️⃣ Signed URL — Direct upload/download

🪞 **Ẩn dụ**: *Signed URL như **vé một lần vào kho** — backend cấp vé có timestamp expiry; khách hàng cầm vé tự vào lấy/đưa hàng mà không cần thẻ nhân viên (credential).*

### Pattern phổ biến

1. Frontend yêu cầu backend "tôi muốn upload file".
2. Backend dùng SA generate **signed URL** valid 5 phút.
3. Frontend `PUT` trực tiếp lên signed URL (không qua backend).
4. Backend save metadata vào DB.

→ Lợi: backend không tải file, scale tốt, không lưu credential trên client.

### Generate signed URL (Python SDK)

```python
from datetime import timedelta
from google.cloud import storage

client = storage.Client()
bucket = client.bucket("acmeshop-uploads")
blob = bucket.blob(f"users/{user_id}/avatar.jpg")

# Signed URL cho PUT (upload)
url = blob.generate_signed_url(
    version="v4",
    expiration=timedelta(minutes=5),
    method="PUT",
    content_type="image/jpeg",
)
# → return URL cho frontend
```

### Generate signed URL (gsutil/gcloud)

```bash
gcloud storage sign-url gs://acmeshop-uploads/products/img-1.jpg \
    --duration=5m \
    --http-verb=GET \
    --private-key-file=sa-key.json
```

### CORS cho web app

```bash
cat > cors.json <<EOF
[
  {
    "origin": ["https://acmeshop.vn"],
    "method": ["GET", "PUT", "POST"],
    "responseHeader": ["Content-Type", "x-goog-meta-foo"],
    "maxAgeSeconds": 3600
  }
]
EOF

gcloud storage buckets update gs://acmeshop-uploads --cors-file=cors.json
```

---

## 4️⃣ Object Lifecycle Management

Tự transition + delete object theo rule.

### Ví dụ rule

```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {"age": 30}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "COLDLINE"},
        "condition": {"age": 90}
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "ARCHIVE"},
        "condition": {"age": 365}
      },
      {
        "action": {"type": "Delete"},
        "condition": {"age": 2555}
      }
    ]
  }
}
```

```bash
gcloud storage buckets update gs://acmeshop-backups \
    --lifecycle-file=lifecycle.json
```

→ Standard 30 ngày → Nearline → 90 ngày → Coldline → 365 ngày → Archive → 7 năm → Delete.

### Tiết kiệm điển hình

| Object age | Class | Cost reduction vs Standard |
|---|---|---|
| 0-30 ngày | Standard | 0% |
| 30-90 | Nearline | −50% |
| 90-365 | Coldline | −80% |
| > 365 | Archive | −94% |

→ Backup 7 năm chi phí giảm ~85% so với để Standard.

---

## 5️⃣ Versioning + Retention Policy

### Object Versioning

Bật để giữ phiên bản cũ khi overwrite/delete:

```bash
gcloud storage buckets update gs://acmeshop-products --versioning
```

- `gsutil ls -a gs://bucket` để xem version cũ.
- Restore: `gcloud storage cp gs://bucket/file.jpg#1234567890 gs://bucket/file.jpg`.

### Retention Policy (compliance)

Lock object — **không thể delete trước khi hết retention**:

```bash
# Set 7 năm retention
gcloud storage buckets update gs://acmeshop-backups \
    --retention-period=220752000  # 7 years in seconds

# Lock policy (KHÔNG hoàn tác được!)
gcloud storage buckets update gs://acmeshop-backups --lock-retention-policy
```

→ Phục vụ SOC2, GDPR, HIPAA. Sau lock, ngay cả Org Admin cũng không delete được.

---

## 6️⃣ Encryption — Default + CMEK + CSEK

| Type | Mô tả | Khi dùng |
|---|---|---|
| **Google-managed (default)** | GCS tự encrypt, key Google quản | 95% workload |
| **CMEK** (Customer-Managed Encryption Key) | Key trong Cloud KMS, Google encrypt với key đó | Compliance, audit key access |
| **CSEK** (Customer-Supplied) | Bạn cung cấp key mỗi request | High security, không khuyến nghị (operational pain) |

### CMEK setup

```bash
# Tạo keyring + key trong KMS
gcloud kms keyrings create acmeshop-keyring --location=asia-southeast1
gcloud kms keys create gcs-key \
    --keyring=acmeshop-keyring \
    --location=asia-southeast1 \
    --purpose=encryption

# Grant GCS service agent encrypt/decrypt
PROJECT_NUMBER=$(gcloud projects describe acmeshop-prod --format='value(projectNumber)')
gcloud kms keys add-iam-policy-binding gcs-key \
    --keyring=acmeshop-keyring \
    --location=asia-southeast1 \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gs-project-accounts.iam.gserviceaccount.com" \
    --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"

# Set default key cho bucket
gcloud storage buckets update gs://acmeshop-products \
    --default-encryption-key=projects/acmeshop-prod/locations/asia-southeast1/keyRings/acmeshop-keyring/cryptoKeys/gcs-key
```

→ Mọi object mới tự encrypt với CMEK. Disable key → object không decrypt được (kill switch).

---

## 7️⃣ Static website hosting + Cloud CDN

### Bucket static site

```bash
# Tạo bucket
gcloud storage buckets create gs://static.acmeshop.vn \
    --location=asia-southeast1 \
    --uniform-bucket-level-access

# Upload files
gcloud storage cp -r ./build/* gs://static.acmeshop.vn/

# Set public read
gcloud storage buckets add-iam-policy-binding gs://static.acmeshop.vn \
    --member="allUsers" \
    --role="roles/storage.objectViewer"

# Set website config
gcloud storage buckets update gs://static.acmeshop.vn \
    --web-main-page-suffix=index.html \
    --web-error-page=404.html
```

### Cloud CDN trước bucket

```bash
# Backend bucket
gcloud compute backend-buckets create static-backend \
    --gcs-bucket-name=static.acmeshop.vn \
    --enable-cdn

# URL map + HTTPS LB (tương tự bài 01)
```

→ Cache global, latency thấp, miễn phí egress giữa GCS và Cloud CDN cùng region.

---

## 🛠️ Hands-on — 3 bucket use case Acme Shop

### Mục tiêu

3 bucket: `products` (ảnh public + CDN), `uploads` (user direct upload signed URL), `backups` (7 năm retention).

### Bước 1 — Bucket products

```bash
gcloud storage buckets create gs://acmeshop-products \
    --location=asia-southeast1 \
    --uniform-bucket-level-access \
    --default-storage-class=STANDARD

gcloud storage buckets add-iam-policy-binding gs://acmeshop-products \
    --member="allUsers" \
    --role="roles/storage.objectViewer"
```

### Bước 2 — Bucket uploads (private, signed URL)

```bash
gcloud storage buckets create gs://acmeshop-uploads \
    --location=asia-southeast1 \
    --uniform-bucket-level-access \
    --public-access-prevention

# CORS cho web upload
echo '[{"origin":["https://acmeshop.vn"],"method":["PUT","POST"],"responseHeader":["Content-Type"],"maxAgeSeconds":3600}]' > cors.json
gcloud storage buckets update gs://acmeshop-uploads --cors-file=cors.json

# Service account cho backend generate signed URL
gcloud iam service-accounts create upload-signer
gcloud storage buckets add-iam-policy-binding gs://acmeshop-uploads \
    --member="serviceAccount:upload-signer@acmeshop-prod.iam.gserviceaccount.com" \
    --role="roles/storage.objectCreator"
```

Backend Python:

```python
from flask import Flask, jsonify
from google.cloud import storage
from datetime import timedelta

app = Flask(__name__)
client = storage.Client()

@app.route("/get-upload-url")
def get_upload_url():
    bucket = client.bucket("acmeshop-uploads")
    blob = bucket.blob(f"avatars/{user_id}.jpg")
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=5),
        method="PUT",
        content_type="image/jpeg",
    )
    return jsonify({"upload_url": url})
```

### Bước 3 — Bucket backups (7-year retention + lifecycle)

```bash
gcloud storage buckets create gs://acmeshop-backups \
    --location=asia-southeast1 \
    --uniform-bucket-level-access \
    --default-storage-class=STANDARD

# Lifecycle (Section 4 example)
gcloud storage buckets update gs://acmeshop-backups --lifecycle-file=lifecycle.json

# Retention 7 năm
gcloud storage buckets update gs://acmeshop-backups --retention-period=220752000
# Lock (sau khi verify chính xác!)
# gcloud storage buckets update gs://acmeshop-backups --lock-retention-policy
```

### Bước 4 — Verify

```bash
# Upload test
echo "hello" > test.txt
gcloud storage cp test.txt gs://acmeshop-products/test.txt
curl https://storage.googleapis.com/acmeshop-products/test.txt
# → hello

# Try delete trong backups trước retention
gcloud storage cp test.txt gs://acmeshop-backups/test.txt
gcloud storage rm gs://acmeshop-backups/test.txt
# → Error: retention policy not met
```

---

## ⚠️ Pitfalls

### 1. Bucket name leak

**Bẫy**: Bucket name global unique → đặt tên dễ guess (`mycompany-backup`) → attacker enumerate.

**Fix**: Đặt tên + random suffix: `acmeshop-backups-7f3a9c`.

### 2. `allUsers` grant nhầm

**Bẫy**: Test public access → forget revoke → bucket public Internet.

**Fix**: Bật **Public Access Prevention** mọi bucket trừ static asset.

### 3. ACL legacy vs IAM mixing

**Bẫy**: Bucket fine-grained ACL + IAM → permission xung đột.

**Fix**: Migrate sang **uniform bucket-level access**.

### 4. Storage class wrong → cost balloon

**Bẫy**: Đặt object active vào Coldline (90 ngày min duration) → mỗi lần access retrieval $0.020/GB + early-delete penalty.

**Fix**: Active data → Standard; archive → Lifecycle auto-transition.

### 5. Retention Policy lock nhầm

**Bẫy**: Lock retention 100 năm → muốn delete bucket = không được, ngay cả Org Admin.

**Fix**: Verify thật kỹ + test với retention ngắn trước khi lock production.

### 6. Signed URL leak

**Bẫy**: Log signed URL vào file → ai đọc log có quyền upload/download trong khoảng thời gian.

**Fix**: Không log URL; expiration ngắn (5-15 phút).

### 7. CMEK key disable / delete

**Bẫy**: Key bị disable → object không decrypt → app down.

**Fix**: KMS key có "Scheduled destroy delay" (30 ngày default). Audit log alert khi key disable.

### 8. CORS mở `*`

**Bẫy**: `"origin": ["*"]` cho dev → quên revert → CSRF attack vector.

**Fix**: Production luôn whitelist domain cụ thể.

---

## 🎯 Self-check

- [ ] Chọn storage class cho 3 use case: product image active, monthly backup, 7-year compliance?
- [ ] Generate signed URL `PUT` thời hạn 5 phút?
- [ ] Setup CORS cho domain `acmeshop.vn` upload trực tiếp?
- [ ] Lifecycle Standard → Nearline 30d → Coldline 90d → Archive 365d → Delete 7y?
- [ ] Bật CMEK với Cloud KMS?
- [ ] Phân biệt Uniform vs Fine-grained access?
- [ ] Retention policy 7 năm + lock — khi nào dùng?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **GCS** | Google Cloud Storage |
| **Bucket** | Container top-level (tên unique global) |
| **Object** | File trong bucket |
| **Storage class** | Standard / Nearline / Coldline / Archive |
| **Location** | Regional / Dual-region / Multi-region |
| **Uniform bucket-level access** | IAM-only, không có ACL per object |
| **Fine-grained access** | IAM + ACL legacy |
| **Public Access Prevention** | Chặn public grant ngay cả khi vô ý |
| **Signed URL** | URL có expiration cho direct upload/download |
| **Lifecycle** | Rule auto-transition/delete object theo tuổi |
| **Object Versioning** | Giữ phiên bản cũ khi overwrite/delete |
| **Retention Policy** | Khóa object không delete được trước N giây |
| **CMEK** | Customer-Managed Encryption Key (qua KMS) |
| **CSEK** | Customer-Supplied Encryption Key (provide mỗi request) |
| **Cloud CDN** | CDN service trên Google backbone |
| **`allUsers`** | Public Internet |
| **`allAuthenticatedUsers`** | Bất kỳ Google account |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [01_compute-engine-and-disks](01_compute-engine-and-disks.md)
- → Tiếp: [03_cloud-sql-and-firestore](03_cloud-sql-and-firestore.md) *(sắp viết)*
- ↑ Cluster GCP: [GCP README](../../README.md)

### Cross-reference
- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — analog
- 🔁 [CI/CD basic](../../../../10_devops/ci-cd/) — pipeline upload artifact lên GCS

### Tài nguyên ngoài (2026)
- 📖 [Cloud Storage docs](https://cloud.google.com/storage/docs)
- 📖 [Storage classes](https://cloud.google.com/storage/docs/storage-classes)
- 📖 [Uniform bucket-level access](https://cloud.google.com/storage/docs/uniform-bucket-level-access)
- 📖 [Signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls)
- 📖 [Object Lifecycle](https://cloud.google.com/storage/docs/lifecycle)
- 📖 [Retention Policy](https://cloud.google.com/storage/docs/bucket-lock)
- 📖 [CMEK](https://cloud.google.com/storage/docs/encryption/customer-managed-keys)
- 📖 [CORS config](https://cloud.google.com/storage/docs/cross-origin)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 02 GCP basic. Storage class 4 + location 3 type + uniform vs fine-grained + signed URL + CORS + Lifecycle + Versioning + Retention Policy + CMEK + static site + Cloud CDN + hands-on 3 bucket use case + 8 pitfalls.
