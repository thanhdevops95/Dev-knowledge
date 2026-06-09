# ⚡ GCP Cloud Functions + Cloud Run + API Gateway

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Bài [Cloud SQL & Firestore](03_cloud-sql-and-firestore.md) ✅, Docker cơ bản

> [!NOTE]
> **Mục tiêu bài học:**
> Bài cuối của cụm basic. Trên GCP, *serverless* (không phải lo máy chủ) có hai vai chính: **Cloud Functions** cho từng đoạn hàm rời chạy theo sự kiện, và **Cloud Run** cho cả một *container* phục vụ web/API và tự co về 0 khi rảnh. Đứng trước cửa là **API Gateway** — cổng vào có người gác. Bài này giúp bạn trả lời câu hỏi quan trọng nhất: *khi nào dùng cái nào*, rồi deploy từng phần, xử lý *cold start*, chỉnh *concurrency*, khoá quyền gọi bằng IAM, gắn tên miền riêng, và dựng cổng API có *auth* + giới hạn lưu lượng. Khép lại bằng một pipeline resize ảnh chạy thật từ đầu đến cuối.

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Cloud Functions** vs **Cloud Run** vs **App Engine** (đối chiếu AWS Lambda)
- [ ] Deploy **Cloud Run** từ Dockerfile chỉ với 1 lệnh
- [ ] Hiểu **cold start** và dùng **min instances** để khử nó
- [ ] Dựng **Cloud Functions** chạy theo sự kiện (GCS, Pub/Sub trigger)
- [ ] Chỉnh **concurrency** + memory + CPU cho Cloud Run
- [ ] Cấu hình **IAM invoker** + phân biệt **public** vs **internal**
- [ ] Gắn **custom domain** + HTTPS tự động cho Cloud Run
- [ ] Dựng **API Gateway** với routes + OpenAPI + auth + rate limit
- [ ] Hands-on: ảnh upload lên GCS → Cloud Function resize → Cloud Run API trả URL

---

## Tình huống — Acme Shop và bài toán ảnh sản phẩm

Hình dung một buổi sáng, sếp ghé bàn bạn với một yêu cầu rất "đời":

> *"User upload ảnh → tự động resize 3 size (thumbnail/medium/full) → lưu lại GCS. API public `api.acmeshop.vn` cho mobile app. Serverless để khỏi quản infra. Cost minimal."*

Nghe thì gọn, nhưng nó gói trọn ba mảnh ghép mà bạn sẽ gặp đi gặp lại trong mọi hệ thống serverless. Mỗi mảnh ứng với một dịch vụ GCP:

- **Cloud Function** lắng nghe sự kiện upload lên bucket `acmeshop-uploads/`, resize ảnh rồi lưu ngược lại.
- **Cloud Run** chạy một REST API (FastAPI) cho mobile app gọi vào.
- **API Gateway** đứng trước cùng, lo phần kiểm tra API key và giới hạn lưu lượng.

Cả bài sẽ đi qua từng mảnh một, rồi cuối cùng ráp lại thành pipeline hoàn chỉnh ở phần hands-on. Việc đầu tiên cần làm rõ là: trong ba dịch vụ tính toán của GCP, dùng cái nào cho việc gì.

---

## 1️⃣ Cloud Functions vs Cloud Run vs App Engine

Trước khi gõ một lệnh deploy nào, bạn cần chọn đúng "phương tiện". GCP có ba dịch vụ chạy code không cần quản máy chủ, và chúng khác nhau ở đơn vị triển khai cũng như mức linh hoạt.

🪞 **Ẩn dụ**: ba dịch vụ giống **ba loại xe**. Cloud Functions là **xe máy** — nhỏ gọn, một mình, phóng đi làm một việc đơn lẻ thật nhanh. Cloud Run là **taxi** — gọi mới chạy, tài xế (container) do bạn tự chọn và tự dựng. App Engine là **xe buýt công cộng** — chạy theo tuyến cố định, ít linh hoạt nhưng quen thuộc với hệ thống cũ.

Bảng dưới so từng tiêu chí. Hãy đọc theo cột "Best for" trước để nắm nhanh vai trò, rồi mới soi các con số kỹ thuật:

| Aspect | Cloud Functions | Cloud Run | App Engine |
|---|---|---|---|
| Unit | Function (1 file) | Container | App (auto-build) |
| Runtime | Node/Python/Go/Java/Ruby/.NET/PHP | Any (Docker) | Standard runtimes + custom (flex) |
| Max duration | Gen1: 540s (9 phút) / Gen2: tới 60 phút | 60 phút | Unlimited (with caveats) |
| Scale to zero | ✅ | ✅ | ✅ (Standard) |
| Concurrency per instance | 1 (Gen1) / 1-1000 (Gen2) | 1-1000 | Auto |
| Trigger | HTTP + 30+ event sources | HTTP + Pub/Sub/Eventarc | HTTP |
| Cold start | 100-500ms | 50-300ms (nhẹ hơn) | 500-2000ms (Standard) |
| Pricing | Per invocation + GB-s | Per request + vCPU/RAM-s | Per instance-hour or request |
| Best for | Đoạn hàm chạy theo sự kiện | Web app/API đóng gói container | Migrate hệ thống cũ |

Điểm rút ra rất rõ ràng: thời lượng chạy, concurrency và độ linh hoạt runtime của Cloud Run đều bằng hoặc vượt hai cái còn lại. Vì vậy mặc định **2026** là dùng **Cloud Run** cho mọi web app/API mới, dùng **Cloud Functions Gen2** cho các đoạn hàm chạy theo sự kiện, còn App Engine chỉ giữ lại cho hệ thống cũ.

### Cloud Functions Gen2 (2024+) thực chất là Cloud Run đội lốt

Tại sao Gen2 lại "ngon" hơn Gen1 đến vậy? Vì Gen2 được build ngay trên runtime của Cloud Run. Nó thừa hưởng toàn bộ ưu điểm của Cloud Run — timeout dài hơn, concurrency cao hơn, chia tải giữa các *revision* (phiên bản triển khai) — chỉ khác ở chỗ bạn viết một hàm thay vì cả container. Hiểu được điều này, bạn sẽ thấy ranh giới giữa "Function" và "Run" ngày càng mờ; chọn cái nào chủ yếu là chọn cách đóng gói code.

---

## 2️⃣ Cloud Run — serverless theo kiểu container

Cloud Run nhận vào một container và lo phần còn lại: tự co giãn theo lưu lượng, cấp HTTPS, co về 0 khi không ai gọi. Có hai cách đưa code lên: để Cloud Run tự build từ source, hoặc bạn tự viết Dockerfile rồi build trước.

### Deploy từ source (Cloud Run tự build)

Cách nhanh nhất khi bạn chưa có Dockerfile. Cloud Run dùng *Buildpacks* (bộ quy tắc tự dựng container từ source) để đoán môi trường và đóng gói giúp bạn:

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

Khi bạn cần kiểm soát chính xác môi trường (hệ thư viện, phiên bản), tự viết Dockerfile là lựa chọn rõ ràng hơn. Build image, đẩy lên *Artifact Registry* (kho chứa container của GCP), rồi trỏ Cloud Run vào đó:

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

### Các flag cấu hình thường gặp

Mỗi lệnh deploy đều xoay quanh một nhóm flag quyết định tài nguyên và quyền truy cập. Đây là những flag bạn sẽ chạm tới mỗi ngày:

| Flag | Mô tả |
|---|---|
| `--memory=512Mi` | RAM per instance (128Mi - 32Gi) |
| `--cpu=1` | vCPU (0.08 - 8) |
| `--concurrency=80` | Request đồng thời/instance (default 80, max 1000) |
| `--max-instances=10` | Hard cap (chống cost runaway) |
| `--min-instances=1` | Pre-warm (chống cold start) |
| `--timeout=300s` | Max request time |
| `--allow-unauthenticated` | Public; bỏ flag = require IAM invoker |
| `--vpc-connector=my-conn` | Truy cập VPC resource (Cloud SQL, Redis) |

Ghi nhớ hai flag "an toàn" quan trọng nhất: `--max-instances` chặn hoá đơn leo thang, và việc *bỏ* `--allow-unauthenticated` để mặc định khoá quyền gọi. Cả hai sẽ quay lại ở phần cạm bẫy.

### Khử cold start

*Cold start* là độ trễ khi Cloud Run phải khởi tạo một instance mới từ con số 0 — instance đầu tiên sau khi đã co về 0 luôn chậm hơn. Với endpoint người dùng nhìn thấy, độ trễ này gây khó chịu. Có vài cách đánh đổi giữa tốc độ và chi phí:

| Cách | Hiệu quả | Cost |
|---|---|---|
| `--min-instances=1` | Khử hẳn cold start | Trả tiền cố định cho 1 instance |
| **Startup CPU boost** | Cold start nhanh ~2x | +20% pricing |
| Tối ưu kích thước image | Pull nhanh hơn | Miễn phí |
| Concurrency cao | Ít instance hơn = ít cold start | Miễn phí |

Cách rẻ nhất luôn nên làm trước là tối ưu image và nâng concurrency (miễn phí); chỉ khi vẫn chưa đủ mới trả thêm tiền cho `--min-instances=1` hoặc bật CPU boost:

```bash
# Bật startup CPU boost
gcloud run services update acmeshop-api \
    --cpu-boost \
    --region=asia-southeast1
```

### Chia tải giữa các revision (canary)

Mỗi lần deploy, Cloud Run tạo một *revision* mới. Bạn có thể cho revision mới nhận một phần nhỏ lưu lượng trước (canary release) để kiểm chứng an toàn trước khi đẩy 100%:

```bash
# Deploy revision mới, 10% traffic
gcloud run services update-traffic acmeshop-api \
    --to-revisions=acmeshop-api-v2=10,acmeshop-api-v1=90 \
    --region=asia-southeast1
```

### Gắn tên miền riêng + HTTPS

Cuối cùng, để mobile app gọi vào `api.acmeshop.vn` thay vì URL `*.run.app` khó nhớ, bạn map tên miền cho service. Điểm hay là HTTPS được cấp tự động qua chứng chỉ do Google quản lý — bạn không phải tự lo certificate:

```bash
# Map domain (HTTPS auto qua Google-managed cert)
gcloud run domain-mappings create \
    --service=acmeshop-api \
    --domain=api.acmeshop.vn \
    --region=asia-southeast1

# Lấy DNS records để add vào DNS provider
```

---

## 3️⃣ Cloud Functions — chạy theo sự kiện

Nếu Cloud Run hợp với cả một API, thì Cloud Functions hợp với một việc nhỏ kích hoạt bởi một sự kiện: có file upload thì resize, có message vào queue thì xử lý. Bạn chỉ viết đúng phần logic, GCP lo phần "khi nào chạy".

### HTTP function

Dạng đơn giản nhất là một hàm phản hồi request HTTP. `functions_framework` là thư viện chuẩn của GCP để biến một hàm Python thành endpoint:

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

### Trigger từ Cloud Storage (chạy theo sự kiện)

Đây chính là trái tim của bài toán resize ảnh: mỗi khi có file mới được tạo trong bucket, GCS bắn ra một *cloud event* và hàm được gọi với thông tin file đó. Chú ý chi tiết quan trọng — dùng `img.copy()` cho mỗi size để giữ nguyên ảnh gốc, nếu thu nhỏ in-place trực tiếp lên `img` thì các size sau sẽ bị nhỏ theo và sai:

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

    # Resize 3 sizes (copy mỗi lần để không thu nhỏ in-place ảnh gốc)
    for size_name, dim in [("thumb", 150), ("medium", 600), ("full", 1200)]:
        copy = img.copy()
        copy.thumbnail((dim, dim))
        buf = io.BytesIO()
        copy.save(buf, format="JPEG", quality=85)
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

### Trigger từ Pub/Sub

Khi muốn xử lý message từ một hàng đợi, bạn trỏ hàm vào một *topic* Pub/Sub. Mỗi message đẩy vào topic sẽ gọi hàm một lần:

```bash
gcloud functions deploy process_order \
    --gen2 \
    --runtime=python312 \
    --trigger-topic=order-events \
    --entry-point=process_order
```

### Các nguồn sự kiện phổ biến

Cloud Functions không chỉ nghe HTTP và GCS. Bảng dưới liệt kê những nguồn trigger bạn sẽ dùng nhiều nhất, kèm tình huống điển hình:

| Trigger | Use case |
|---|---|
| HTTP | API endpoint nhỏ |
| Cloud Storage | File upload → resize/process |
| Pub/Sub | Message queue |
| Firestore | Document write → trigger |
| Eventarc | Định tuyến sự kiện cross-service |
| Cloud Scheduler | Cron |

---

## 4️⃣ API Gateway

Hai dịch vụ trên đã lo phần xử lý. Còn ai đứng cửa kiểm soát ai được gọi, gọi bao nhiêu, đi tới đâu? Đó là vai của API Gateway.

🪞 **Ẩn dụ**: API Gateway giống **lễ tân toà nhà** — kiểm tra giấy tờ (auth), giới hạn số người vào mỗi giờ (rate limit), chỉ đường tới đúng phòng (route), và ghi sổ khách (log). Backend của bạn (Cloud Run) chỉ tập trung làm việc, mọi thứ "gác cổng" giao hết cho lễ tân.

### Quy trình dựng

Quy trình gồm bốn bước gọn, đi từ mô tả routes đến endpoint chạy thật:

1. Viết **OpenAPI 2.0 spec** mô tả routes (lưu ý: GCP API Gateway chỉ nhận Swagger 2.0).
2. `gcloud api-gateway api-configs create` tạo config từ spec.
3. `gcloud api-gateway gateways create` tạo gateway endpoint.
4. Cập nhật DNS hoặc gọi thẳng vào URL của gateway.

### Ví dụ OpenAPI spec

Lưu ý quan trọng: GCP API Gateway **chỉ hỗ trợ OpenAPI 2.0 (Swagger)**, chưa nhận OpenAPI 3 — nên file dưới khai báo `swagger: "2.0"`. Khối `x-google-backend` là phần mở rộng riêng của Google để trỏ route tới backend Cloud Run:

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

### Triển khai gateway

Có spec rồi, ba lệnh dưới biến nó thành một gateway sống: tạo API, tạo config từ spec, rồi dựng gateway gắn config đó:

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

### Giới hạn lưu lượng (rate limit)

Để chặn một client gọi quá nhiều, bạn khai báo *quota* ngay trong OpenAPI bằng các phần mở rộng `x-google-management` / `x-google-quota`. Sau khi deploy config, giá trị quota cụ thể được quản qua Cloud Console (mục Quotas) hoặc Service Management API — GCP không có một lệnh `gcloud` đơn lẻ để set rate limit cho gateway:

```yaml
# Trong OpenAPI: khai báo metric + quota cho operation
x-google-management:
  metrics:
    - name: "read-requests"
      displayName: "Read requests"
      valueType: INT64
      metricKind: DELTA
  quota:
    limits:
      - name: "read-limit"
        metric: "read-requests"
        unit: "1/min/{project}"
        values:
          STANDARD: 1000  # 1000 requests/phút/project
```

Sau khi deploy, vào **Cloud Console → APIs & Services → Quotas** để xem và điều chỉnh giá trị limit của managed service. Không có lệnh `gcloud services configure-quotas` cho việc này — đừng đi tìm.

### Tên miền riêng

Cuối cùng, trỏ tên miền của bạn về endpoint của gateway bằng một bản ghi CNAME:

```text
api.acmeshop.vn → CNAME → acmeshop-gw-<hash>.gateway.dev
```

---

## 🛠️ Hands-on — pipeline resize ảnh từ đầu đến cuối

Giờ ráp cả ba mảnh lại. Mục tiêu: user upload ảnh lên `acmeshop-uploads/originals/`, Cloud Function tự resize và lưu vào `resized/{thumb,medium,full}/`, Cloud Run API trả về URL từng size, và API Gateway đứng trước lo phần auth.

### Bước 1 — Tạo bucket

Đầu tiên là nơi chứa ảnh. Bật *uniform bucket-level access* để quản quyền nhất quán ở cấp bucket thay vì từng object:

```bash
gcloud storage buckets create gs://acmeshop-uploads \
    --location=asia-southeast1 \
    --uniform-bucket-level-access
```

### Bước 2 — Cloud Function resize

Tiếp theo dựng hàm resize. Toàn bộ source được tạo inline rồi deploy ngay — chú ý vẫn dùng `img.copy()` cho từng size để không thu nhỏ in-place ảnh gốc:

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

Giờ tới API trả URL các size cho mobile app. Dockerfile pin sẵn `ENV PORT=8080` để vừa chạy được trên Cloud Run (Cloud Run tự set `PORT`) vừa chạy được khi test local:

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
ENV PORT=8080
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

Phần gateway dùng đúng quy trình OpenAPI + 3 lệnh `gcloud` ở mục 4 phía trên — trỏ `x-google-backend` về URL Cloud Run vừa deploy, rồi tạo API/config/gateway.

### Bước 5 — Kiểm tra

Cuối cùng là chạy thử cả vòng. Upload một file lên `originals/`, đợi vài giây để Function trigger, rồi kiểm tra thư mục `resized/` và gọi API qua gateway:

```bash
# Upload ảnh
echo "test" > test.jpg
gcloud storage cp test.jpg gs://acmeshop-uploads/originals/test.jpg

# Đợi vài giây → Function trigger
gcloud storage ls gs://acmeshop-uploads/resized/
# → thumb/test.jpg, medium/test.jpg, full/test.jpg

# Gọi API
curl https://acmeshop-gw-xyz.gateway.dev/products/test/images \
    -H "x-api-key: YOUR_KEY"
```

Nếu thấy ba file trong `resized/` và API trả về JSON các URL, pipeline đã chạy đúng từ đầu đến cuối. Trước khi tổng kết, hãy điểm qua những chỗ dễ vấp nhất trong thực chiến.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Cloud Run mặc định public khi quên `--allow-unauthenticated`

> [!WARNING]
> Đây là lỗi bảo mật phổ biến nhất với người mới: quên rằng `--allow-unauthenticated` mở endpoint cho cả thế giới.

- ❌ **Cạm bẫy:** Thêm `--allow-unauthenticated` cho tiện rồi quên gỡ → ai cũng gọi được endpoint.
- ✅ **Best practice:** Mặc định dùng `--no-allow-unauthenticated`; đặt gateway/IAP đứng trước; mobile app verify qua Firebase Auth.

### 2. Cold start lâu với endpoint người dùng

- ❌ **Cạm bẫy:** P95 latency lên tới 2s mỗi khi cold start, người dùng cảm nhận rõ.
- ✅ **Best practice:** Dùng `--min-instances=1` cho các endpoint quan trọng người dùng nhìn thấy; kết hợp `--cpu-boost`.

### 3. Function chạy quá thời gian cho phép

- ❌ **Cạm bẫy:** Function Gen1 xử lý file vượt 540s → bị timeout.
- ✅ **Best practice:** Chuyển sang Gen2 (hỗ trợ tới 60 phút); hoặc đẩy việc nặng sang một Cloud Run job thay vì Function.

### 4. Cloud Function tự gọi chính nó thành vòng lặp

- ❌ **Cạm bẫy:** Trigger bucket → hàm ghi ngược vào cùng bucket → trigger lại → vòng lặp vô tận, hoá đơn leo thang.
- ✅ **Best practice:** Lọc theo prefix (chỉ xử lý `originals/`); ghi output vào bucket khác hoặc subfolder không gắn trigger.

### 5. Kết nối Cloud SQL từ Cloud Run

- ❌ **Cạm bẫy:** Cố connect Cloud SQL trực tiếp từ Cloud Run mà không có đường mạng → fail.
- ✅ **Best practice:** Dùng `--add-cloudsql-instances=acmeshop-prod:asia-southeast1:acmeshop-db` (Cloud Run mount Unix socket) hoặc VPC Connector + private IP.

### 6. API Gateway không cache, backend gánh hết tải

- ❌ **Cạm bẫy:** Mọi request đều forward thẳng xuống → backend chịu toàn bộ tải.
- ✅ **Best practice:** Đặt Cloud CDN trước API Gateway cho các GET có thể cache; hoặc dùng Memorystore Redis cache trong backend.

### 7. Concurrency mặc định = 1 ở Function Gen1

- ❌ **Cạm bẫy:** Gen1 mặc định concurrency 1 → 1000 request đồng thời = 1000 instance → chi phí dội lên.
- ✅ **Best practice:** Dùng Gen2 (mặc định concurrency 1 nhưng tune được lên tới 1000) để gom request vào ít instance hơn.

### 8. Chi phí leo thang khi thiếu `--max-instances`

> [!WARNING]
> Một đợt bot tấn công có thể đẩy hệ thống scale lên hàng nghìn instance — và hoá đơn theo cùng.

- ❌ **Cạm bẫy:** Không set `--max-instances` → bot attack → scale 1000 instance → hoá đơn $1000+ trong một giờ.
- ✅ **Best practice:** Luôn set `--max-instances`; bật Cloud Armor rate limit ở tầng trước.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] So sánh Cloud Functions vs Cloud Run vs App Engine cho 3 use case khác nhau?
- [ ] Deploy Cloud Run từ Dockerfile + gắn custom domain HTTPS?
- [ ] Dựng Cloud Function trigger từ GCS upload → resize ảnh?
- [ ] Setup API Gateway với OpenAPI + API key auth?
- [ ] Nêu 3 cách khử cold start kèm trade-off chi phí?
- [ ] Chia tải canary 10% → 100% trên Cloud Run?
- [ ] Kết nối Cloud SQL từ Cloud Run đúng cách?

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Bảng gom các lệnh hay dùng nhất, để bạn copy nhanh khi thực chiến mà không phải cuộn lại cả bài:

| Việc cần làm | Lệnh |
|---|---|
| Deploy Cloud Run từ source | `gcloud run deploy <svc> --source=. --region=<r>` |
| Deploy Cloud Run từ image | `gcloud run deploy <svc> --image=<registry>/<img>:<tag> --region=<r>` |
| Bật startup CPU boost | `gcloud run services update <svc> --cpu-boost --region=<r>` |
| Canary 10% revision mới | `gcloud run services update-traffic <svc> --to-revisions=<new>=10,<old>=90` |
| Map custom domain | `gcloud run domain-mappings create --service=<svc> --domain=<d>` |
| Deploy HTTP function (Gen2) | `gcloud functions deploy <fn> --gen2 --runtime=python312 --trigger-http` |
| Deploy GCS-trigger function | `gcloud functions deploy <fn> --gen2 --trigger-bucket=<bucket>` |
| Deploy Pub/Sub function | `gcloud functions deploy <fn> --gen2 --trigger-topic=<topic>` |
| Tạo API Gateway config | `gcloud api-gateway api-configs create <cfg> --api=<api> --openapi-spec=openapi.yaml` |
| Tạo gateway | `gcloud api-gateway gateways create <gw> --api=<api> --api-config=<cfg> --location=<r>` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Cloud Run** | Chạy container serverless | Dịch vụ chạy container, co về 0, hỗ trợ HTTP + event |
| **Cloud Functions** | Hàm chạy theo sự kiện | Dịch vụ chạy từng hàm rời, kích hoạt bởi event |
| **App Engine** | Nền tảng ứng dụng (PaaS) | PaaS truyền thống, chủ yếu dùng cho hệ thống cũ (2026) |
| **Concurrency** | Số request đồng thời | Số request một instance xử lý cùng lúc |
| **Cold start** | Độ trễ khởi tạo | Độ trễ khi instance khởi tạo từ con số 0 |
| **Min instances** | Số instance giữ ấm | Giữ sẵn instance để tránh cold start |
| **Startup CPU boost** | Tăng CPU lúc khởi động | Cấp gấp đôi CPU trong vài giây đầu để cold start nhanh hơn |
| **Traffic split** | Chia tải lưu lượng | Phân % lưu lượng giữa các revision (canary) |
| **Revision** | Phiên bản triển khai | Một phiên bản cụ thể của service Cloud Run |
| **API Gateway** | Cổng API | Cổng quản lý request dựa trên OpenAPI |
| **OpenAPI 2.0 (Swagger)** | Đặc tả REST API | Định dạng spec mô tả REST API; GCP API Gateway chỉ nhận bản 2.0 |
| **Eventarc** | Định tuyến sự kiện | Định tuyến event cross-service trong GCP |
| **Buildpacks** | Bộ tự dựng container | Tự build container từ source mà không cần Dockerfile |
| **Artifact Registry** | Kho chứa artifact | Registry chứa container/package của GCP |
| **VPC Connector** | Cầu nối VPC | Cho phép serverless truy cập resource trong VPC |
| **Cloud Run job** | Tác vụ batch | Tác vụ chạy một lần/theo lịch (không phải service HTTP) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [GCP Cloud SQL + Firestore](03_cloud-sql-and-firestore.md)
- ↑ **Về cụm:** [GCP — README cụm](../../README.md)
- ➡️ **Bài tiếp theo:** Intermediate (GKE Autopilot, Vertex AI, BigQuery deep) — đang xây dựng

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS Lambda + API Gateway](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — dịch vụ tương đương trên AWS để đối chiếu
- 🐳 [Docker cơ bản](../../../../10_devops/docker/) — build image cho Cloud Run
- 🔁 [CI/CD cơ bản](../../../../10_devops/ci-cd/) — deploy Cloud Run từ pipeline

### 🌐 Tài nguyên tham khảo khác

- 📖 [Cloud Run docs](https://cloud.google.com/run/docs)
- 📖 [Cloud Functions Gen2](https://cloud.google.com/functions/docs/concepts/version-comparison)
- 📖 [Cloud Run + Cloud SQL](https://cloud.google.com/sql/docs/postgres/connect-run)
- 📖 [API Gateway docs](https://cloud.google.com/api-gateway/docs)
- 📖 [OpenAPI 2.0 specification](https://swagger.io/specification/v2/)
- 📖 [Cloud Build docs](https://cloud.google.com/build/docs)
- 📖 [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- 📖 [Buildpacks](https://buildpacks.io/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) GCP. Cloud Functions Gen2 + Cloud Run + App Engine compare + cold start mitigation + traffic split canary + custom domain + API Gateway OpenAPI + rate limit + hands-on image resize pipeline GCS→Function→Cloud Run + 8 pitfalls. Hoàn thành GCP basic cluster.
- **v2.0.0 (01/06/2026)** — Viết lại sang văn phong narrative (lời dẫn trước mỗi bảng/code, câu phân tích sau, ẩn dụ, mạch WHY→WHAT→HOW); chuẩn hoá heading framework + Glossary 3 cột + nav marker ⬅️/➡️/↑ với link-text là tiêu đề thực; đổi "Prerequisites" → "Yêu cầu trước"; thêm Cheatsheet; chuyển pitfall sang dạng ❌ Cạm bẫy / ✅ Best practice. Fix kỹ thuật: làm rõ timeout Gen1 540s vs Gen2 60 phút; sửa block resize §3 dùng img.copy() cho đúng logic; thay lệnh sai gcloud services configure-quotas bằng quota qua OpenAPI x-google-management + Console; sửa nhãn "OpenAPI 3" → "OpenAPI 2.0 (Swagger)" cho khớp spec và giới hạn thực của API Gateway; thêm ENV PORT=8080 vào Dockerfile hands-on.
