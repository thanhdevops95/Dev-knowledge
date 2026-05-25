# ⚡ Azure Functions + App Service + Container Apps

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~23 phút\
> **Prerequisites:** Bài [03_azure-sql-and-cosmosdb](03_azure-sql-and-cosmosdb.md) ✅, Docker basic, HTTP/REST basic

> 🎯 *Bài 04 (cuối basic). Serverless + PaaS trên Azure có 4 lựa chọn chính: **Azure Functions** (single function event-driven, analog Lambda), **App Service** (PaaS web app, analog Elastic Beanstalk), **Container Apps** (serverless container Knative + Dapr, analog Cloud Run + Fargate), **API Management** (managed API gateway). Bài này dạy: khi nào dùng cái nào, deploy step-by-step, cold start mitigation, Durable Functions cho workflow, custom domain + HTTPS auto, hands-on image processing pipeline.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Azure Functions** vs **App Service** vs **Container Apps** vs **AKS**
- [ ] Hiểu **3 Function plans**: Consumption / Premium / Dedicated (App Service Plan)
- [ ] Deploy **Function HTTP trigger** + **Blob trigger** + **Queue trigger**
- [ ] **Durable Functions** — workflow orchestration (chain/fan-out/aggregator)
- [ ] **App Service** — Web App Linux + custom domain + HTTPS auto + slot deployment
- [ ] **Container Apps** — deploy container scale-to-zero + Dapr sidecar
- [ ] **API Management** — managed gateway + product/subscription + rate limit + OpenAPI
- [ ] **Cold start mitigation** — Premium plan, Always Ready instance, warm-up
- [ ] Hands-on: image processing pipeline (Blob upload → Function resize → Container Apps API)

---

## Tình huống — Acme Shop image pipeline serverless

Sếp:

> *"User upload ảnh → tự động resize 3 size → lưu lại Blob. Backend API public `api.acmeshop.vn` cho mobile/web. Serverless để khỏi quản infra. Mùa sale traffic 100x — phải scale tự động. Cost minimal khi idle."*

Bạn cần:

- **Azure Function** Blob trigger khi upload → resize → save.
- **Container Apps** chạy FastAPI cho REST API (scale-to-zero).
- **API Management** front + auth API key + rate limit + OpenAPI spec.
- **Cold start** chấp nhận được cho user-facing (Premium plan).

Bài này dạy từng phần + hands-on full pipeline.

---

## 1️⃣ Compute decision tree — 4 lựa chọn

🪞 **Ẩn dụ**: *4 dịch vụ như **4 loại phương tiện đi làm** — Functions là **xe máy** (nhỏ, 1 người, đi việc đơn lẻ nhanh); App Service là **xe hơi cá nhân** (chở team, chạy code framework mình quen); Container Apps là **xe ghép Grab** (gọi mới chạy, container bất kỳ); AKS là **đội xe taxi riêng** (full control, đủ chỗ ngồi, vận hành tốn công).*

| Aspect | Functions | App Service | Container Apps | AKS |
|---|---|---|---|---|
| Unit | Function (1 file) | App (code/container) | Container (Docker) | Pod (Kubernetes) |
| Runtime | Node/Python/Java/.NET/PowerShell | Same + Ruby | Any (Docker) | Any (Docker) |
| Max duration | 10 phút (Consumption) / 30 phút (Premium) / unlimited (Dedicated) | Unlimited | Unlimited | Unlimited |
| Scale to zero | ✅ (Consumption) | ❌ (always ≥1) | ✅ | ❌ (need KEDA) |
| Cold start | 100-1000ms | None (warm) | 200-3000ms | None |
| Pricing | Per request + GB-s | Per instance-hour | Per request + vCPU/RAM-s | Per node (VM) |
| Best for | Event-driven, short tasks | Standard web app/API | Container microservices, scale-to-zero | Full K8s control |
| Analog AWS | Lambda | Elastic Beanstalk | Fargate / App Runner | EKS |
| Analog GCP | Cloud Functions | App Engine | Cloud Run | GKE |

→ **Decision rules 2026**:
- Event-driven snippet → **Functions**.
- Standard web app/API, ít care container → **App Service**.
- Container microservice, scale-to-zero → **Container Apps**.
- Full K8s, complex networking, custom controllers → **AKS**.

---

## 2️⃣ Azure Functions — Event-driven serverless

### 3 hosting plans

| Plan | Scale | Cold start | Network | Use case |
|---|---|---|---|---|
| **Consumption** | Scale-to-zero, max 200 instance | 100-500ms | Public only | Pure event-driven, traffic bursty |
| **Premium (EP1/EP2/EP3)** | Pre-warmed (always ready), unlimited | None | VNet, Private Endpoint | Production, low-latency requirement |
| **Dedicated (App Service Plan)** | Manual (Standard/Premium AS plan) | None | VNet | Co-locate với App Service, long-running |

```bash
# Consumption (pay per execution)
az functionapp create \
    --resource-group rg-prod-fn \
    --name func-resize-prod \
    --consumption-plan-location southeastasia \
    --storage-account stacmeprodfn \
    --runtime python \
    --runtime-version 3.12 \
    --functions-version 4 \
    --os-type Linux

# Premium plan (always-ready + VNet)
az functionapp plan create \
    --resource-group rg-prod-fn \
    --name plan-fn-premium-prod \
    --location southeastasia \
    --sku EP1 \
    --is-linux true \
    --min-instances 1 \
    --max-burst 20

az functionapp create \
    --resource-group rg-prod-fn \
    --name func-api-prod \
    --plan plan-fn-premium-prod \
    --storage-account stacmeprodfn \
    --runtime python \
    --runtime-version 3.12 \
    --functions-version 4
```

### Triggers

| Trigger | Mô tả |
|---|---|
| **HTTP** | REST endpoint |
| **Timer** | Cron schedule |
| **Blob** | Storage Blob event |
| **Queue** | Storage Queue / Service Bus |
| **Event Grid** | Pub-sub event |
| **Event Hub** | Streaming |
| **Cosmos DB** | Change feed |
| **Service Bus** | Enterprise messaging |
| **SignalR** | Real-time |
| **Kafka** (preview) | Kafka topic |

### HTTP function (Python v2 model)

```python
# function_app.py
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="hello", methods=["GET"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "world")
    logging.info(f"Hello {name}")
    return func.HttpResponse(f"Hello, {name}!", status_code=200)
```

```bash
# Deploy
func azure functionapp publish func-api-prod
```

### Blob trigger

```python
@app.blob_trigger(
    arg_name="myblob",
    path="uploads/originals/{name}",
    connection="AzureWebJobsStorage"
)
def resize_image(myblob: func.InputStream):
    from PIL import Image
    import io
    from azure.storage.blob import BlobServiceClient
    from azure.identity import DefaultAzureCredential
    import os

    logging.info(f"Blob trigger: {myblob.name}, size {myblob.length} bytes")

    img = Image.open(io.BytesIO(myblob.read()))
    base_name = myblob.name.split("/")[-1]

    # Connect storage qua Managed Identity
    account_url = os.environ["STORAGE_ACCOUNT_URL"]
    cred = DefaultAzureCredential()
    bsc = BlobServiceClient(account_url, credential=cred)
    container = bsc.get_container_client("uploads")

    for name, dim in [("thumb", 150), ("medium", 600), ("full", 1200)]:
        copy = img.copy()
        copy.thumbnail((dim, dim))
        buf = io.BytesIO()
        copy.save(buf, format="JPEG", quality=85)
        out = container.get_blob_client(f"resized/{name}/{base_name}")
        out.upload_blob(buf.getvalue(), overwrite=True,
                        content_type="image/jpeg")
```

### Cold start mitigation

| Cách | Hiệu quả | Cost |
|---|---|---|
| Premium plan + min-instances | Zero cold start | Constant pay |
| Always Ready instance (Premium) | Zero | Pay 1 instance always |
| Code warm-up (timer trigger every 5 min) | Reduce frequency | Free |
| Optimize package size | Faster cold | Free |
| Right runtime (Python > Java cold time) | 30-70% faster | Free |

```bash
# Pre-warm: timer trigger every 5 min
@app.schedule(schedule="0 */5 * * * *", arg_name="timer")
def keep_warm(timer: func.TimerRequest):
    logging.info("Warm ping")
```

---

## 3️⃣ Durable Functions — Workflow orchestration

🪞 **Ẩn dụ**: *Durable Functions như **giấy ủy quyền cho thư ký** — bạn viết workflow tuần tự `Bước 1 → đợi → Bước 2 → ...`; thư ký (Azure runtime) lưu state, đợi event, gọi từng bước dù mất giờ/ngày, không tốn tiền compute trong lúc đợi.*

### Use cases

- Function chain: A → B → C (output A là input B).
- Fan-out / fan-in: parallel execute N tasks, gom kết quả.
- Async waiting: human approval flow.
- Long-running workflow: order fulfillment 3 ngày.

### Pattern: Function chaining

```python
import azure.functions as func
import azure.durable_functions as df

app = func.FunctionApp()

# Orchestrator
@app.orchestration_trigger(context_name="context")
def order_workflow(context: df.DurableOrchestrationContext):
    order = context.get_input()

    # Bước 1: validate
    valid = yield context.call_activity("validate_order", order)
    if not valid:
        return {"status": "rejected"}

    # Bước 2: charge payment
    payment = yield context.call_activity("charge_payment", order)

    # Bước 3: ship
    shipping = yield context.call_activity("create_shipment", order)

    return {"status": "complete", "payment": payment, "shipping": shipping}

# Activities
@app.activity_trigger(input_name="order")
def validate_order(order: dict) -> bool:
    return order.get("total", 0) > 0

@app.activity_trigger(input_name="order")
def charge_payment(order: dict) -> dict:
    # Call Stripe / Adyen
    return {"txn_id": "abc"}

@app.activity_trigger(input_name="order")
def create_shipment(order: dict) -> dict:
    return {"tracking": "VN1234"}

# HTTP trigger to start
@app.route(route="orders")
@app.durable_client_input(client_name="client")
async def start(req: func.HttpRequest, client: df.DurableOrchestrationClient) -> func.HttpResponse:
    order = req.get_json()
    instance_id = await client.start_new("order_workflow", client_input=order)
    return client.create_check_status_response(req, instance_id)
```

### Pattern: Fan-out / Fan-in

```python
@app.orchestration_trigger(context_name="context")
def batch_resize(context):
    files = yield context.call_activity("list_files", None)

    # Fan-out: parallel
    tasks = [context.call_activity("resize_one", f) for f in files]
    results = yield context.task_all(tasks)

    # Fan-in: aggregate
    return {"resized": len(results), "files": results}
```

→ Cost: pay per activity invocation; state lưu trong Storage Table (cheap).

---

## 4️⃣ App Service — PaaS Web App

### Hierarchy

```
App Service Plan: plan-prod-sea (S1, P1v3, ...)
├── Web App: app-api-prod-sea           ← Python FastAPI
├── Web App: app-admin-prod-sea         ← Vue admin
└── Function App: func-cron-prod-sea    ← can co-locate Functions Dedicated
```

→ Plan = compute (VM size + replica count). App = code/container chạy trên plan.

### Plan tiers

| Tier | Use case |
|---|---|
| **F1** (Free) | Sandbox, demo (60 CPU min/day) |
| **B1/B2/B3** (Basic) | Dev/staging, no SLA |
| **S1/S2/S3** (Standard) | Production, autoscale, deployment slots |
| **P1v3/P2v3/P3v3** (Premium v3) | High perf, AMD, VNet, private endpoint |
| **I1v2/I2v2/I3v2** (Isolated v2) | Dedicated ASE — compliance/PCI |

→ Production default: **S1** small, **P1v3** medium.

### Deploy options

```bash
# A. Git deploy
az webapp deployment source config-local-git \
    --resource-group rg-prod-web \
    --name app-api-prod-sea

# Add remote rồi git push

# B. ZIP deploy
az webapp deploy \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --src-path ./build.zip \
    --type zip

# C. Container
az webapp create \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --plan plan-prod-sea \
    --deployment-container-image-name myregistry.azurecr.io/api:v1
```

### Deployment slots (zero-downtime deploy)

```bash
# Tạo staging slot
az webapp deployment slot create \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --slot staging

# Deploy code mới lên staging
az webapp deploy --slot staging --resource-group rg-prod-web --name app-api-prod-sea --src-path build-v2.zip --type zip

# Test staging URL: app-api-prod-sea-staging.azurewebsites.net

# Swap với production (zero downtime, can rollback)
az webapp deployment slot swap \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --slot staging --target-slot production
```

→ Production app = warm instance staging, traffic switch instant. Rollback: swap ngược.

### Custom domain + HTTPS auto

```bash
# Add custom domain (DNS phải CNAME tới <app>.azurewebsites.net)
az webapp config hostname add \
    --resource-group rg-prod-web \
    --webapp-name app-api-prod-sea \
    --hostname api.acmeshop.vn

# Create managed cert (free auto-renew)
az webapp config ssl create \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --hostname api.acmeshop.vn

# Bind cert
az webapp config ssl bind \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --certificate-thumbprint <thumb> \
    --ssl-type SNI
```

→ Free managed cert (App Service Managed Certificate), auto-renew. HTTPS Only redirect:

```bash
az webapp update --resource-group rg-prod-web --name app-api-prod-sea --https-only true
```

### Authentication built-in (Easy Auth)

```bash
# Bật Entra ID auth — code không cần verify token
az webapp auth update \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --enabled true \
    --action LoginWithAzureActiveDirectory \
    --aad-allowed-token-audiences https://app-api-prod-sea.azurewebsites.net
```

→ App Service inject header `X-MS-CLIENT-PRINCIPAL` với user info. Code chỉ đọc header.

---

## 5️⃣ Container Apps — Serverless container

### Khác Container Apps vs App Service container vs AKS

| Aspect | App Service container | Container Apps | AKS |
|---|---|---|---|
| Scale to zero | ❌ | ✅ | ❌ (cần KEDA) |
| Knative | ❌ | ✅ | manual |
| Dapr sidecar | ❌ | ✅ built-in | manual |
| Multi-container per app | ❌ | ✅ (sidecar pattern) | ✅ |
| K8s API access | ❌ | ❌ | ✅ |
| Pricing | Per plan-hour | Per request + vCPU/RAM-s | Per node-hour |
| Use case | Simple containerized web app | Microservice, event-driven, scale-to-zero | Complex K8s workload |

### Setup

```bash
# Container Apps environment (= K8s cluster managed by Microsoft)
az containerapp env create \
    --name cae-prod-sea \
    --resource-group rg-prod-app \
    --location southeastasia

# Tạo Container App
az containerapp create \
    --name ca-api-prod \
    --resource-group rg-prod-app \
    --environment cae-prod-sea \
    --image myregistry.azurecr.io/api:v1 \
    --target-port 8000 \
    --ingress external \
    --min-replicas 0 \
    --max-replicas 10 \
    --cpu 0.5 --memory 1Gi
```

### Auto-scaling triggers (KEDA-based)

```bash
# Scale theo HTTP concurrent request
az containerapp update \
    --name ca-api-prod \
    --resource-group rg-prod-app \
    --scale-rule-name http-rule \
    --scale-rule-type http \
    --scale-rule-http-concurrency 50

# Scale theo Service Bus queue length
az containerapp update \
    --name ca-worker-prod \
    --resource-group rg-prod-app \
    --scale-rule-name sb-rule \
    --scale-rule-type azure-servicebus \
    --scale-rule-metadata queueName=orders messageCount=10 \
    --scale-rule-auth "connection=service-bus-conn"
```

### Revision + traffic split

```bash
# Mỗi update tạo revision mới
az containerapp update \
    --name ca-api-prod \
    --resource-group rg-prod-app \
    --image myregistry.azurecr.io/api:v2

# Multiple-revision mode để có 2 revision cùng lúc
az containerapp revision set-mode \
    --name ca-api-prod \
    --resource-group rg-prod-app \
    --mode multiple

# Split traffic 90/10
az containerapp ingress traffic set \
    --name ca-api-prod \
    --resource-group rg-prod-app \
    --revision-weight ca-api-prod--v1=90 ca-api-prod--v2=10
```

### Dapr sidecar

= state, pub-sub, secret, binding pattern qua HTTP sidecar.

```bash
az containerapp create \
    --name ca-orders-prod \
    --resource-group rg-prod-app \
    --environment cae-prod-sea \
    --image myregistry.azurecr.io/orders:v1 \
    --enable-dapr \
    --dapr-app-id orders \
    --dapr-app-port 8000
```

App gọi `http://localhost:3500/v1.0/state/statestore` thay vì gọi Storage trực tiếp → portable cross-cloud.

---

## 6️⃣ API Management — Managed gateway

🪞 **Ẩn dụ**: *API Management như **lễ tân tòa nhà cao cấp** — kiểm tra ID (auth, JWT), giới hạn khách vào/giờ (rate limit), chỉ phòng nào (route), ghi sổ chi tiết (analytics + monitoring), tự hiển thị bảng dịch vụ (developer portal).*

### Tier comparison

| Tier | Use case | Cost |
|---|---|---|
| **Consumption** | Pay-per-request, dev/PoC | $0.04 per 10k call |
| **Developer** | Single instance, dev/staging | $50/month |
| **Basic / Standard / Premium** | Production scale, VNet, multi-region | $147 - $2,795/month |

→ Consumption phù hợp startup. Production: Standard v2 (mới 2024+, VNet integration).

### Workflow

1. Create APIM instance.
2. Import backend (OpenAPI spec hoặc Function App / App Service).
3. Define **Product** (collection of APIs).
4. Define **Subscription** (API key per consumer).
5. Apply **Policy** (rate limit, transform, auth).

### Setup APIM

```bash
# Consumption tier
az apim create \
    --name apim-acmeshop-prod \
    --resource-group rg-prod-apim \
    --location southeastasia \
    --publisher-email ops@acmeshop.vn \
    --publisher-name "Acme Shop" \
    --sku-name Consumption

# Import OpenAPI spec
az apim api import \
    --resource-group rg-prod-apim \
    --service-name apim-acmeshop-prod \
    --api-id orders \
    --path orders \
    --specification-url https://api-spec.acmeshop.vn/orders.yaml \
    --specification-format OpenApi
```

### Policy ví dụ — rate limit + JWT validate

```xml
<!-- Policy XML -->
<policies>
  <inbound>
    <!-- JWT validate -->
    <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
      <openid-config url="https://login.microsoftonline.com/<tenant>/v2.0/.well-known/openid-configuration" />
      <audiences><audience>api://acmeshop</audience></audiences>
    </validate-jwt>

    <!-- Rate limit 100 req/min per subscription -->
    <rate-limit-by-key calls="100" renewal-period="60"
                       counter-key="@(context.Subscription.Id)" />

    <!-- Quota 10000 req/day -->
    <quota-by-key calls="10000" renewal-period="86400"
                  counter-key="@(context.Subscription.Id)" />

    <!-- Forward to backend -->
    <set-backend-service base-url="https://api-prod.azurewebsites.net" />
  </inbound>
  <outbound>
    <!-- Add CORS header -->
    <set-header name="Access-Control-Allow-Origin" exists-action="override">
      <value>https://shop.acmeshop.vn</value>
    </set-header>
  </outbound>
</policies>
```

### Custom domain

```bash
az apim hostname configuration create \
    --resource-group rg-prod-apim \
    --service-name apim-acmeshop-prod \
    --hostname api.acmeshop.vn \
    --certificate-source KeyVault \
    --key-vault-id https://kv-prod.vault.azure.net/secrets/api-cert
```

---

## 🛠️ Hands-on — Image resize pipeline end-to-end

### Mục tiêu

User upload `originals/<file>` → Function resize tự động → save `resized/{thumb,medium,full}/<file>`. Container Apps API trả URL các size. APIM front với API key + rate limit.

### Bước 1 — Storage Account + Container

```bash
az group create --name rg-prod-pipeline --location southeastasia

az storage account create \
    --name stacmeprodpipe \
    --resource-group rg-prod-pipeline \
    --location southeastasia \
    --sku Standard_LRS --kind StorageV2 \
    --allow-blob-public-access false

az storage container create \
    --account-name stacmeprodpipe \
    --name uploads --auth-mode login
```

### Bước 2 — Function App (Consumption)

```bash
az functionapp create \
    --resource-group rg-prod-pipeline \
    --name func-resize-prod-001 \
    --consumption-plan-location southeastasia \
    --storage-account stacmeprodpipe \
    --runtime python --runtime-version 3.12 \
    --functions-version 4 --os-type Linux \
    --assign-identity '[system]'

# Grant Function Identity access Storage
FUNC_PRINCIPAL=$(az functionapp identity show -n func-resize-prod-001 -g rg-prod-pipeline --query principalId -o tsv)
az role assignment create \
    --assignee $FUNC_PRINCIPAL \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-prod-pipeline/providers/Microsoft.Storage/storageAccounts/stacmeprodpipe"
```

### Bước 3 — Function code

```bash
mkdir resize-fn && cd resize-fn
func init --python --worker-runtime python -m V2

cat > function_app.py <<'EOF'
import azure.functions as func
import logging
import io, os
from PIL import Image
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.blob_trigger(arg_name="blob",
                  path="uploads/originals/{name}",
                  connection="AzureWebJobsStorage")
def resize_image(blob: func.InputStream):
    logging.info(f"Resize trigger: {blob.name}, {blob.length} bytes")
    img = Image.open(io.BytesIO(blob.read()))
    base = blob.name.split("/")[-1]

    cred = DefaultAzureCredential()
    bsc = BlobServiceClient(
        "https://stacmeprodpipe.blob.core.windows.net",
        credential=cred)
    container = bsc.get_container_client("uploads")

    for name, dim in [("thumb", 150), ("medium", 600), ("full", 1200)]:
        copy = img.copy()
        copy.thumbnail((dim, dim))
        buf = io.BytesIO()
        copy.save(buf, format="JPEG", quality=85)
        container.get_blob_client(f"resized/{name}/{base}") \
            .upload_blob(buf.getvalue(), overwrite=True,
                         content_type="image/jpeg")
    logging.info(f"Done {base}")
EOF

cat > requirements.txt <<'EOF'
azure-functions
azure-identity
azure-storage-blob
Pillow
EOF

# Deploy
func azure functionapp publish func-resize-prod-001
```

### Bước 4 — Container Apps API

```bash
# ACR (Azure Container Registry)
az acr create --resource-group rg-prod-pipeline \
    --name acracmeshopprod --sku Basic --admin-enabled true

# Build + push image
mkdir api && cd api
cat > main.py <<'EOF'
from fastapi import FastAPI
import os

app = FastAPI()
ACCOUNT = "stacmeprodpipe"

@app.get("/health")
def health(): return {"ok": True}

@app.get("/products/{pid}/images")
def images(pid: str):
    base = f"https://{ACCOUNT}.blob.core.windows.net/uploads/resized"
    return {name: f"{base}/{name}/{pid}.jpg"
            for name in ["thumb", "medium", "full"]}
EOF

cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY main.py .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

az acr build --registry acracmeshopprod \
    --image api:v1 .

# Container Apps env + app
az containerapp env create \
    --name cae-prod-sea \
    --resource-group rg-prod-pipeline \
    --location southeastasia

az containerapp create \
    --name ca-api-prod \
    --resource-group rg-prod-pipeline \
    --environment cae-prod-sea \
    --image acracmeshopprod.azurecr.io/api:v1 \
    --target-port 8000 --ingress external \
    --min-replicas 0 --max-replicas 5 \
    --cpu 0.5 --memory 1Gi \
    --registry-server acracmeshopprod.azurecr.io \
    --registry-username $(az acr credential show -n acracmeshopprod --query username -o tsv) \
    --registry-password $(az acr credential show -n acracmeshopprod --query passwords[0].value -o tsv)
```

### Bước 5 — API Management

```bash
az apim create \
    --name apim-acmeshop-prod \
    --resource-group rg-prod-pipeline \
    --location southeastasia \
    --publisher-email ops@acmeshop.vn \
    --publisher-name "Acme Shop" \
    --sku-name Consumption

# Lấy CA URL
CA_URL=$(az containerapp show -n ca-api-prod -g rg-prod-pipeline --query properties.configuration.ingress.fqdn -o tsv)

az apim api create \
    --resource-group rg-prod-pipeline \
    --service-name apim-acmeshop-prod \
    --api-id images \
    --path images \
    --display-name "Image API" \
    --protocols https \
    --service-url "https://$CA_URL" \
    --subscription-required true
```

### Bước 6 — Test pipeline

```bash
# Upload ảnh original
echo "binary-data" > test.jpg
az storage blob upload \
    --account-name stacmeprodpipe \
    --container-name uploads \
    --name originals/test.jpg \
    --file test.jpg \
    --auth-mode login

# Đợi 5-30s → Function trigger
sleep 15
az storage blob list \
    --account-name stacmeprodpipe \
    --container-name uploads \
    --prefix resized/ --auth-mode login --output table
# → resized/thumb/test.jpg, resized/medium/test.jpg, resized/full/test.jpg

# Call API qua APIM (cần subscription key)
SUB_KEY=$(az apim subscription show ... --query primaryKey -o tsv)
APIM_URL=$(az apim show -n apim-acmeshop-prod -g rg-prod-pipeline --query gatewayUrl -o tsv)
curl "$APIM_URL/images/products/test/images" \
    -H "Ocp-Apim-Subscription-Key: $SUB_KEY"
```

### Bước 7 — Cleanup

```bash
az group delete --name rg-prod-pipeline --yes --no-wait
```

→ **Kết quả**: Pipeline Blob → Function → Container Apps → APIM hoạt động end-to-end.

---

## ⚠️ Pitfalls

### 1. Cold start lâu cho user-facing Functions

**Bẫy**: Consumption plan + user-facing API → P95 latency 1-2s.

**Fix**:
- Premium plan + min-instances ≥ 1.
- Always Ready instance trong Premium.
- Optimize package size (remove dev dependencies).
- Health check endpoint cron mỗi 5 phút.

### 2. Function timeout

**Bẫy**: Consumption max 10 phút → image processing dài bị cut.

**Fix**:
- Premium: 30 phút.
- Dedicated (App Service Plan): unlimited.
- Hoặc dùng **Durable Functions** + activity nhỏ.
- Hoặc dùng **Container Apps Job** cho batch.

### 3. Blob trigger missing event (poll-based)

**Bẫy**: Consumption Blob trigger dùng polling — có thể delay 1-10 phút khi storage có nhiều blob.

**Fix**:
- Dùng **Event Grid** trigger thay vì Blob trigger → event-driven sub-second.
- Hoặc Premium plan với Event Grid.

### 4. App Service auto-rebuild khi deploy

**Bẫy**: Deploy code Python → App Service auto-rebuild → 5-10 phút downtime (single instance).

**Fix**:
- **Deployment slot** + swap (zero-downtime).
- Multi-instance từ B1 trở lên.
- Container deploy không rebuild.

### 5. Custom domain không HTTPS auto

**Bẫy**: Map domain `api.acmeshop.vn` → HTTP work, HTTPS error (no cert).

**Fix**:
- Bật **App Service Managed Certificate** (free, auto-renew).
- Hoặc bring own cert qua Key Vault.
- Check: `--https-only true`.

### 6. Container Apps cold start lớn

**Bẫy**: `min-replicas=0` → request đầu chờ 1-3s pull image.

**Fix**:
- `min-replicas=1` cho user-facing endpoint.
- Smaller image (Alpine, distroless).
- Use ACR same region (faster pull).

### 7. APIM Consumption tier không VNet

**Bẫy**: APIM Consumption rẻ nhưng không hỗ trợ VNet integration → không call backend private endpoint.

**Fix**:
- Backend qua public endpoint + APIM IP whitelist.
- Hoặc upgrade Standard v2 (mới 2024+, support VNet).

### 8. Easy Auth không validate token claim

**Bẫy**: Easy Auth chỉ verify signature; không check `role` claim → user không phải admin vẫn vào admin endpoint.

**Fix**:
- App logic check role từ header `X-MS-CLIENT-PRINCIPAL`.
- Hoặc dùng APIM với `validate-jwt` + `required-claims`.

### 9. Function App share Storage Account = race

**Bẫy**: Nhiều Function App share 1 Storage Account → lease conflict, slow.

**Fix**:
- 1 Storage Account riêng cho mỗi Function App (default tạo qua portal đã correct).
- Tách `AzureWebJobsStorage` (internal state) vs data storage.

### 10. Cost runaway no max-replicas

**Bẫy**: Container Apps không set `max-replicas` → bot attack → 1000 replica → $$$.

**Fix**:
- Luôn set `--max-replicas`.
- Front WAF (Front Door / APIM) rate limit.
- Budget alert.

---

## 🎯 Self-check

- [ ] So sánh Functions vs App Service vs Container Apps vs AKS cho 4 use case khác nhau?
- [ ] Function plan Consumption vs Premium vs Dedicated — chọn cho event-driven, user-facing, long-running?
- [ ] Deploy Function với Blob trigger + Managed Identity access Storage — flow?
- [ ] Durable Function pattern chain vs fan-out — code example?
- [ ] App Service deployment slot swap — zero-downtime deploy như thế nào?
- [ ] Container Apps min-replicas=0 vs 1 — trade-off cost vs latency?
- [ ] Container Apps Dapr sidecar — lợi ích gì?
- [ ] APIM policy `validate-jwt` + `rate-limit-by-key` — bảo vệ backend như thế nào?
- [ ] Cold start mitigation 4 cách — chọn theo budget?
- [ ] Cost estimate: 1M req/tháng Function Consumption vs Container Apps?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Azure Functions** | Serverless function — event-driven |
| **Consumption plan** | Pay-per-execution, scale-to-zero |
| **Premium plan** | Always-ready, VNet, no cold start |
| **App Service** | PaaS web app (code or container) |
| **App Service Plan** | Compute layer (VM size + count) |
| **Web App** | App chạy trên Plan |
| **Deployment slot** | Pre-prod copy, swap zero-downtime |
| **App Service Managed Certificate** | Free SSL auto-renew |
| **Easy Auth** | Built-in auth (Entra ID, Google, Facebook) |
| **Container Apps** | Serverless container, Knative + Dapr |
| **Container Apps Environment** | Group container apps share VNet + Log Analytics |
| **Revision** | Immutable snapshot Container App |
| **Traffic split** | % traffic cross revision (canary) |
| **KEDA** | K8s Event-Driven Autoscaler |
| **Dapr** | Distributed application runtime (sidecar) |
| **AKS** | Azure Kubernetes Service |
| **API Management (APIM)** | Managed API gateway |
| **Product / Subscription** | APIM hierarchy: nhóm API + key per consumer |
| **Policy** | APIM XML rule (auth, rate, transform) |
| **Durable Functions** | Function workflow orchestration (chain/fan-out) |
| **Cold start** | Latency khi instance khởi tạo |
| **Always Ready instance** | Premium plan pre-warmed |
| **ACR** | Azure Container Registry |
| **Blob trigger** | Function trigger khi Blob create/update |
| **Event Grid trigger** | Event-driven sub-second latency |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [03_azure-sql-and-cosmosdb](03_azure-sql-and-cosmosdb.md)
- ↑ Cluster Azure: [Azure README](../../README.md)
- 🔜 Intermediate (sắp viết): AKS, Bicep, ARM, Service Bus deep, Front Door + WAF, Cost optimization

### Cross-reference
- ☁️ [AWS Lambda + API Gateway](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — analog Functions + APIM
- ☁️ [GCP Cloud Functions + Cloud Run + API Gateway](../../../gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) — analog
- 🐳 [Docker basic](../../../../10_DevOps/docker/) — image build cho Container Apps
- 🔁 [CI/CD basic](../../../../10_DevOps/ci-cd/) — deploy serverless từ pipeline
- 🧭 [Cloud Engineer roadmap](../../../../00_Roadmaps/career/cloud-engineer_career-roadmap.md)

### Tài nguyên ngoài (2026)
- 📖 [Azure Functions docs](https://learn.microsoft.com/azure/azure-functions/)
- 📖 [Python v2 programming model](https://learn.microsoft.com/azure/azure-functions/functions-reference-python)
- 📖 [Durable Functions](https://learn.microsoft.com/azure/azure-functions/durable/)
- 📖 [App Service docs](https://learn.microsoft.com/azure/app-service/)
- 📖 [Deployment slots](https://learn.microsoft.com/azure/app-service/deploy-staging-slots)
- 📖 [Container Apps docs](https://learn.microsoft.com/azure/container-apps/)
- 📖 [Container Apps + Dapr](https://learn.microsoft.com/azure/container-apps/dapr-overview)
- 📖 [API Management docs](https://learn.microsoft.com/azure/api-management/)
- 📖 [APIM policy reference](https://learn.microsoft.com/azure/api-management/api-management-policies)
- 📖 [Compute decision tree](https://learn.microsoft.com/azure/architecture/guide/technology-choices/compute-decision-tree)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 04 (cuối basic) Azure. Functions (Consumption/Premium/Dedicated) + 10+ trigger + Durable Functions chain/fan-out + App Service Plan + Web App + deployment slot + custom domain + Easy Auth + Container Apps Knative + Dapr + revision traffic split + APIM Consumption + policy JWT/rate-limit + decision tree 4 compute options + hands-on image pipeline Blob→Function→Container Apps→APIM + 10 pitfalls. Hoàn thành Azure basic cluster 5/5.
