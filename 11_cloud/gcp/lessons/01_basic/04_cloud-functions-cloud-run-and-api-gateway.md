# ⚡ GCP Cloud Functions + Cloud Run + API Gateway

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [03_cloud-sql-and-firestore](03_cloud-sql-and-firestore.md) ✅, Docker basic

> 🎯 *Bài 04 (cuối basic). Serverless trên GCP có 2 vai chính: **Cloud Functions** (single function, event-driven), **Cloud Run** (container, HTTP/event, scale-to-zero). API Gateway = managed entry point. Bài này dạy: khi nào dùng cái nào, deploy step-by-step, cold start, concurrency, IAM invoker, custom domain, API Gateway routes + auth + rate limit. Hands-on image resize pipeline.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Cloud Functions** vs **Cloud Run** vs **App Engine** (so sánh AWS Lambda)
- [ ] Deploy **Cloud Run** từ Dockerfile (1 command)
- [ ] Hiểu **cold start** + dùng **min instances** để chống
- [ ] Setup **Cloud Functions** event-driven (GCS, Pub/Sub trigger)
- [ ] Configure **concurrency** + memory + CPU cho Cloud Run
- [ ] Setup **IAM invoker** + **public** vs **internal**
- [ ] **Custom domain** + HTTPS auto cho Cloud Run
- [ ] **API Gateway** với routes + OpenAPI + auth + rate limit
- [ ] Hands-on: GCS image upload trigger → Cloud Function resize → Cloud Run API

---

## Tình huống — Acme Shop image pipeline

Sếp:

> *"User upload ảnh → tự động resize 3 size (thumbnail/medium/full) → lưu lại GCS. API public `api.acmeshop.vn` cho mobile app. Serverless để khỏi quản infra. Cost minimal."*

Bạn cần:
- **Cloud Function** trigger khi upload lên `acmeshop-uploads/` bucket → resize → save lại.
- **Cloud Run** FastAPI cho REST API public.
- **API Gateway** front + auth API key + rate limit.

Bài này dạy từng phần + hands-on full pipeline.

---

## 1️⃣ Cloud Functions vs Cloud Run vs App Engine

🪞 **Ẩn dụ**: *3 dịch vụ như **3 loại xe**: Cloud Functions là **scooter** (nhỏ, 1 mình, đi nhanh việc đơn lẻ); Cloud Run là **taxi** (gọi mới chạy, tài xế tùy chọn — container bạn build); App Engine là **xe bus công cộng** (chạy theo tuyến cố định, ít linh hoạt).*

| Aspect | Cloud Functions | Cloud Run | App Engine |
|---|---|---|---|
| Unit | Function (1 file) | Container | App (auto-build) |
| Runtime | Node/Python/Go/Java/Ruby/.NET/PHP | Any (Docker) | Standard runtimes + custom (flex) |
| Max duration | 540s (Gen2 = 60 min) | 60 phút | Unlimited (with caveats) |
| Scale to zero | ✅ | ✅ | ✅ (Standard) |
| Concurrency per instance | 1 (Gen1) / 1-1000 (Gen2) | 1-1000 | Auto |
| Trigger | HTTP + 30+ event sources | HTTP + Pub/Sub/Eventarc | HTTP |
| Cold start | 100-500ms | 50-300ms (lighter) | 500-2000ms (Standard) / cold-load |
| Pricing | Per invocation + GB-s | Per request + vCPU/RAM-s | Per instance-hour or request |
| Best for | Event-driven snippet | Container web app/API | Legacy migration |

→ **2026 best practice**: dùng **Cloud Run** cho mọi web app/API mới; **Cloud Functions Gen2** cho event-driven snippet; App Engine chỉ legacy.

### Cloud Functions Gen2 (2024+) = Cloud Run dưới mui

Gen2 build trên Cloud Run runtime → benefit từ Cloud Run features (longer timeout, higher concurrency, traffic split).

---

## 2️⃣ Cloud Run — Container serverless

### Deploy từ source (auto-build)

```bash
# Cloud Run tự build container từ source bằng Buildpacks
gcloud run deploy acmeshop-api \
    --source=. \
    --region=asia-southeast1 \
    --allow-unauthenticated \
    --memory=512Mi \
    --cpu=1 \
    --max-instances=10 \
    --concurrency=80
```

### Deploy từ Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
```

```bash
# Build + push lên Artifact Registry
gcloud builds submit --tag=asia-southeast1-docker.pkg.dev/acmeshop-prod/api/acmeshop-api:v1

# Deploy Cloud Run
gcloud run deploy acmeshop-api \
    --image=asia-southeast1-docker.pkg.dev/acmeshop-prod/api/acmeshop-api:v1 \
    --region=asia-southeast1
```

### Configuration

| Flag | Mô tả |
|---|---|
| `--memory=512Mi` | RAM per instance (128Mi - 32Gi) |
| `--cpu=1` | vCPU (0.08 - 8) |
| `--concurrency=80` | Request đồng thời/instance (default 80, max 1000) |
| `--max-instances=10` | Hard cap (chống cost runaway) |
| `--min-instances=1` | Pre-warm (chống cold start) |
| `--timeout=300s` | Max request time |
| `--allow-unauthenticated` | Public; bỏ flag = require IAM invoker |
| `--vpc-connector=my-conn` | Access VPC resource (Cloud SQL, Redis) |

### Cold start mitigation

| Cách | Hiệu quả | Cost |
|---|---|---|
| `--min-instances=1` | Eliminate cold start | Pay constant for 1 instance |
| **Startup CPU boost** | 2x faster cold start | +20% pricing |
| Optimize image size | Faster pull | Free |
| Concurrency cao | Less instance = less cold | Free |

```bash
# Bật startup CPU boost
gcloud run services update acmeshop-api \
    --cpu-boost \
    --region=asia-southeast1
```

### Traffic split (canary)

```bash
# Deploy revision mới, 10% traffic
gcloud run services update-traffic acmeshop-api \
    --to-revisions=acmeshop-api-v2=10,acmeshop-api-v1=90 \
    --region=asia-southeast1
```

### Custom domain + HTTPS

```bash
# Map domain (HTTPS auto qua Google-managed cert)
gcloud run domain-mappings create \
    --service=acmeshop-api \
    --domain=api.acmeshop.vn \
    --region=asia-southeast1

# Lấy DNS records để add vào DNS provider
```

---

## 3️⃣ Cloud Functions — Event-driven

### HTTP function

```python
# main.py
import functions_framework

@functions_framework.http
def hello(request):
    return f"Hello, {request.args.get('name', 'world')}"
```

```bash
gcloud functions deploy hello \
    --gen2 \
    --runtime=python312 \
    --region=asia-southeast1 \
    --source=. \
    --entry-point=hello \
    --trigger-http \
    --allow-unauthenticated
```

### GCS trigger (event-driven)

```python
# main.py
import functions_framework
from google.cloud import storage
from PIL import Image
import io

@functions_framework.cloud_event
def resize_image(cloud_event):
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]

    if not file_name.startswith("originals/"):
        return  # Chỉ xử lý originals/

    client = storage.Client()
    src_bucket = client.bucket(bucket_name)
    src_blob = src_bucket.blob(file_name)

    # Download
    img_bytes = src_blob.download_as_bytes()
    img = Image.open(io.BytesIO(img_bytes))

    # Resize 3 sizes
    for size_name, dim in [("thumb", 150), ("medium", 600), ("full", 1200)]:
        img.thumbnail((dim, dim))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        out_blob = src_bucket.blob(f"resized/{size_name}/{file_name.split('/')[-1]}")
        out_blob.upload_from_string(buf.getvalue(), content_type="image/jpeg")

    print(f"Resized {file_name}")
```

```bash
gcloud functions deploy resize_image \
    --gen2 \
    --runtime=python312 \
    --region=asia-southeast1 \
    --source=. \
    --entry-point=resize_image \
    --trigger-bucket=acmeshop-uploads \
    --trigger-event-filters="type=google.cloud.storage.object.v1.finalized"
```

### Pub/Sub trigger

```bash
gcloud functions deploy process_order \
    --gen2 \
    --runtime=python312 \
    --trigger-topic=order-events \
    --entry-point=process_order
```

### Event sources phổ biến

| Trigger | Use case |
|---|---|
| HTTP | API endpoint nhỏ |
| Cloud Storage | File upload → resize/process |
| Pub/Sub | Message queue |
| Firestore | Document write → trigger |
| Eventarc | Cross-service event routing |
| Cloud Scheduler | Cron |

---

## 4️⃣ API Gateway

🪞 **Ẩn dụ**: *API Gateway như **lễ tân tòa nhà** — kiểm tra ID (auth), giới hạn số lượng người vào/giờ (rate limit), chỉ đường tới đúng phòng (route), ghi sổ khách (log).*

### Setup workflow

1. Viết **OpenAPI 3 spec** mô tả routes.
2. `gcloud api-gateway api-configs create` tạo config.
3. `gcloud api-gateway gateways create` tạo gateway endpoint.
4. Update DNS / call gateway URL.

### OpenAPI spec ví dụ

```yaml
# openapi.yaml
swagger: "2.0"
info:
  title: acmeshop-api
  description: Acme Shop API
  version: 1.0.0
host: api.acmeshop.vn
schemes:
  - https
paths:
  /products:
    get:
      summary: List products
      operationId: listProducts
      x-google-backend:
        address: https://acmeshop-api-xyz.run.app/products
      security:
        - api_key: []
      responses:
        '200':
          description: OK
securityDefinitions:
  api_key:
    type: "apiKey"
    name: "x-api-key"
    in: "header"
```

### Deploy

```bash
# Create API
gcloud api-gateway apis create acmeshop-api

# Create config
gcloud api-gateway api-configs create acmeshop-config-v1 \
    --api=acmeshop-api \
    --openapi-spec=openapi.yaml

# Create gateway
gcloud api-gateway gateways create acmeshop-gw \
    --api=acmeshop-api \
    --api-config=acmeshop-config-v1 \
    --location=asia-southeast1
```

### Rate limit

```yaml
# Trong OpenAPI
x-google-quota:
  metricCosts:
    "read-quota": 1
```

```bash
# Set quota
gcloud services configure-quotas --service=acmeshop-api.endpoints \
    --quotas=read-quota=1000  # 1000 requests/min
```

### Custom domain

DNS record:
```
api.acmeshop.vn → CNAME → acmeshop-gw-<hash>.gateway.dev
```

---

## 🛠️ Hands-on — Image resize pipeline end-to-end

### Mục tiêu

User upload ảnh lên `acmeshop-uploads/originals/` → Cloud Function resize → lưu `resized/{thumb,medium,full}/`. Cloud Run API trả URL các size. API Gateway front với auth.

### Bước 1 — Bucket

```bash
gcloud storage buckets create gs://acmeshop-uploads \
    --location=asia-southeast1 \
    --uniform-bucket-level-access
```

### Bước 2 — Cloud Function resize

```bash
# Tạo source
mkdir -p resize-fn && cd resize-fn
cat > main.py <<'EOF'
import functions_framework
from google.cloud import storage
from PIL import Image
import io

@functions_framework.cloud_event
def resize_image(cloud_event):
    bucket_name = cloud_event.data["bucket"]
    file_name = cloud_event.data["name"]
    if not file_name.startswith("originals/"):
        return
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    img = Image.open(io.BytesIO(blob.download_as_bytes()))
    for name, dim in [("thumb", 150), ("medium", 600), ("full", 1200)]:
        copy = img.copy()
        copy.thumbnail((dim, dim))
        buf = io.BytesIO()
        copy.save(buf, format="JPEG", quality=85)
        out = bucket.blob(f"resized/{name}/{file_name.split('/')[-1]}")
        out.upload_from_string(buf.getvalue(), content_type="image/jpeg")
EOF
cat > requirements.txt <<'EOF'
functions-framework==3.5.0
google-cloud-storage==2.16.0
Pillow==10.3.0
EOF

# Deploy
gcloud functions deploy resize-image \
    --gen2 \
    --runtime=python312 \
    --region=asia-southeast1 \
    --source=. \
    --entry-point=resize_image \
    --trigger-bucket=acmeshop-uploads
```

### Bước 3 — Cloud Run API

```bash
mkdir -p api && cd api
cat > main.py <<'EOF'
from fastapi import FastAPI
from google.cloud import storage

app = FastAPI()
client = storage.Client()

@app.get("/products/{pid}/images")
def images(pid: str):
    bucket = client.bucket("acmeshop-uploads")
    sizes = {}
    for name in ["thumb", "medium", "full"]:
        sizes[name] = f"https://storage.googleapis.com/acmeshop-uploads/resized/{name}/{pid}.jpg"
    return sizes
EOF
cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
RUN pip install fastapi uvicorn google-cloud-storage
COPY . .
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
EOF

# Deploy
gcloud run deploy acmeshop-api \
    --source=. \
    --region=asia-southeast1 \
    --memory=512Mi \
    --concurrency=80 \
    --max-instances=10 \
    --no-allow-unauthenticated
```

### Bước 4 — API Gateway

(Xem section 4.)

### Bước 5 — Test

```bash
# Upload ảnh
echo "test" > test.jpg
gcloud storage cp test.jpg gs://acmeshop-uploads/originals/test.jpg

# Đợi 5s → Function trigger
gcloud storage ls gs://acmeshop-uploads/resized/
# → thumb/test.jpg, medium/test.jpg, full/test.jpg

# Gọi API
curl https://acmeshop-gw-xyz.gateway.dev/products/test/images \
    -H "x-api-key: YOUR_KEY"
```

---

## ⚠️ Pitfalls

### 1. Cloud Run public mặc định với `--allow-unauthenticated`

**Bẫy**: Quên flag → ai cũng gọi được endpoint.

**Fix**: Default `--no-allow-unauthenticated`; gateway/IAP front; mobile app dùng Firebase Auth verify.

### 2. Cold start lâu cho user-facing

**Bẫy**: P95 latency 2s khi cold start.

**Fix**: `--min-instances=1` cho user-facing endpoint quan trọng; `--cpu-boost`.

### 3. Function timeout

**Bẫy**: Function process file > 540s (Gen1) → timeout.

**Fix**: Gen2 hỗ trợ 60 phút; hoặc trigger Cloud Run job thay vì Function.

### 4. Cloud Function tạo loop

**Bẫy**: Trigger bucket → ghi vào cùng bucket → trigger lại → infinite loop.

**Fix**: Check prefix; ghi vào bucket khác hoặc subfolder không trigger.

### 5. Cloud SQL từ Cloud Run

**Bẫy**: Connect Cloud SQL từ Cloud Run trực tiếp → no VPC.

**Fix**: Dùng `--add-cloudsql-instances=acmeshop-prod:asia-southeast1:acmeshop-db` (Cloud Run mounts Unix socket) hoặc VPC Connector + private IP.

### 6. API Gateway không cache

**Bẫy**: Mọi request đều forward → backend chịu tải.

**Fix**: Cloud CDN trước API Gateway cho GET cacheable; hoặc Memorystore Redis cache trong backend.

### 7. Concurrency = 1 default Function Gen1

**Bẫy**: Gen1 default concurrency 1 → 1000 req = 1000 instance → cost cao.

**Fix**: Gen2 default concurrency 1 nhưng có thể tune lên 1000.

### 8. Cost runaway no `--max-instances`

**Bẫy**: Bot attack → scale 1000 instance → $1000+ bill 1 giờ.

**Fix**: Luôn set `--max-instances`; bật Cloud Armor rate limit.

---

## 🎯 Self-check

- [ ] So sánh Cloud Functions vs Cloud Run vs App Engine cho 3 use case?
- [ ] Deploy Cloud Run từ Dockerfile + custom domain HTTPS?
- [ ] Cloud Function trigger GCS upload → resize ảnh?
- [ ] Setup API Gateway với OpenAPI + API key auth?
- [ ] Cold start mitigation 3 cách + trade-off cost?
- [ ] Traffic split canary 10% → 100% trên Cloud Run?
- [ ] Connect Cloud SQL từ Cloud Run đúng cách?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Cloud Run** | Serverless container, scale-to-zero, HTTP + event |
| **Cloud Functions** | Serverless function, event-driven |
| **App Engine** | PaaS truyền thống (legacy 2026) |
| **Concurrency** | Số request đồng thời/instance |
| **Cold start** | Latency khi instance khởi tạo từ 0 |
| **Min instances** | Pre-warm tránh cold start |
| **Startup CPU boost** | 2x CPU trong 10s đầu để cold start nhanh |
| **Traffic split** | Phân chia % traffic giữa revisions (canary) |
| **API Gateway** | Managed gateway, OpenAPI-based |
| **OpenAPI 3 (Swagger)** | Spec format mô tả REST API |
| **Eventarc** | Event routing cross-service GCP |
| **Buildpacks** | Auto-build container từ source (không cần Dockerfile) |
| **Artifact Registry** | Container/package registry GCP |
| **VPC Connector** | Cho serverless access VPC resource |
| **Cloud Run job** | Một-time/scheduled batch job (không phải service HTTP) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [03_cloud-sql-and-firestore](03_cloud-sql-and-firestore.md)
- ↑ Cluster GCP: [GCP README](../../README.md)
- 🔜 (Intermediate sắp viết): GKE Autopilot, Vertex AI, BigQuery deep

### Cross-reference
- ☁️ [AWS Lambda + API Gateway](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — analog
- 🐳 [Docker basic](../../../../10_devops/docker/) — image build cho Cloud Run
- 🔁 [CI/CD basic](../../../../10_devops/ci-cd/) — deploy Cloud Run từ pipeline

### Tài nguyên ngoài (2026)
- 📖 [Cloud Run docs](https://cloud.google.com/run/docs)
- 📖 [Cloud Functions Gen2](https://cloud.google.com/functions/docs/concepts/version-comparison)
- 📖 [Cloud Run + Cloud SQL](https://cloud.google.com/sql/docs/postgres/connect-run)
- 📖 [API Gateway docs](https://cloud.google.com/api-gateway/docs)
- 📖 [OpenAPI specification](https://swagger.io/specification/v2/)
- 📖 [Cloud Build docs](https://cloud.google.com/build/docs)
- 📖 [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- 📖 [Buildpacks](https://buildpacks.io/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) GCP. Cloud Functions Gen2 + Cloud Run + App Engine compare + cold start mitigation + traffic split canary + custom domain + API Gateway OpenAPI + rate limit + hands-on image resize pipeline GCS→Function→Cloud Run + 8 pitfalls. Hoàn thành GCP basic cluster.
