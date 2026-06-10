# ⚡ Azure Functions + App Service + Container Apps

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Bài [Azure SQL + Cosmos DB](03_azure-sql-and-cosmosdb.md) ✅, Docker cơ bản, HTTP/REST cơ bản

> 🎯 *Bài cuối của cụm basic. Khi không muốn tự dựng và trông coi máy chủ, Azure cho bạn bốn cửa serverless/PaaS chính: **Azure Functions** (chạy từng *function* theo sự kiện, tương đương AWS Lambda), **App Service** (PaaS cho web app, tương đương Elastic Beanstalk), **Container Apps** (serverless container chuẩn Knative + Dapr, tương đương Cloud Run + Fargate), và **API Management** (cổng API quản lý sẵn). Bài này trả lời câu hỏi quan trọng nhất — khi nào dùng cái nào — rồi đi qua deploy từng bước, cách giảm *cold start* (độ trễ khi instance vừa khởi tạo), Durable Functions cho luồng nhiều bước, custom domain kèm HTTPS tự cấp, và khép lại bằng một pipeline xử lý ảnh chạy thật.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Azure Functions** vs **App Service** vs **Container Apps** vs **AKS**
- [ ] Hiểu **3 Function plan**: Consumption / Premium / Dedicated (App Service Plan)
- [ ] Deploy **Function HTTP trigger** + **Blob trigger** + **Queue trigger**
- [ ] **Durable Functions** — điều phối luồng nhiều bước (chain / fan-out / aggregator)
- [ ] **App Service** — Web App Linux + custom domain + HTTPS tự cấp + deployment slot
- [ ] **Container Apps** — deploy container *scale-to-zero* + Dapr sidecar
- [ ] **API Management** — cổng API quản lý sẵn + product/subscription + rate limit + OpenAPI
- [ ] **Giảm cold start** — Premium plan, Always Ready instance, warm-up
- [ ] Hands-on: pipeline xử lý ảnh (Blob upload → Function resize → Container Apps API)

---

## Tình huống — Acme Shop dựng pipeline ảnh không cần quản máy chủ

Cảnh quen thuộc với bất kỳ ai làm e-commerce: ảnh sản phẩm đổ về liên tục, và mỗi ảnh cần vài kích thước khác nhau cho thumbnail, trang chi tiết, ảnh phóng to. Sếp tóm gọn yêu cầu trong một đoạn:

> *"User upload ảnh → tự động resize 3 size → lưu lại Blob. Backend API public `api.acmeshop.vn` cho mobile/web. Serverless để khỏi quản infra. Mùa sale traffic 100x — phải scale tự động. Cost minimal khi idle."*

Đọc kỹ thì mỗi câu của sếp ứng với một mảnh ghép cụ thể trên Azure, và việc của bạn là chọn đúng dịch vụ cho từng mảnh:

- **Azure Function** bắt sự kiện Blob khi có ảnh upload → resize → lưu lại.
- **Container Apps** chạy FastAPI làm REST API, để rảnh thì co về không (scale-to-zero) cho đỡ tốn tiền.
- **API Management** đứng trước cùng, lo xác thực bằng API key, giới hạn tần suất gọi, và phát hành OpenAPI spec.
- **Cold start** ở mức chấp nhận được cho phần giáp mặt người dùng (chọn Premium plan).

Bài này tháo từng mảnh ra dạy riêng, rồi cuối cùng ráp lại thành một pipeline hoàn chỉnh ở phần hands-on.

---

## 1️⃣ Bốn lựa chọn compute — chọn cửa nào?

Trước khi viết một dòng lệnh nào, bạn phải trả lời được câu hỏi nền tảng: workload này nên chạy ở đâu? Azure có bốn dịch vụ compute hay bị nhầm lẫn, và chọn sai ngay từ đầu thì về sau sửa rất mệt. Một phép so sánh đời thường giúp định hình nhanh sự khác biệt giữa chúng.

🪞 **Ẩn dụ**: *4 dịch vụ như **4 loại phương tiện đi làm** — Functions là **xe máy** (nhỏ, 1 người, đi việc đơn lẻ nhanh); App Service là **xe hơi cá nhân** (chở team, chạy code framework mình quen); Container Apps là **xe ghép Grab** (gọi mới chạy, container bất kỳ); AKS là **đội xe taxi riêng** (full control, đủ chỗ ngồi, vận hành tốn công).*

Bảng dưới đặt cả bốn cạnh nhau theo những tiêu chí mà bạn thực sự cần cân nhắc khi quyết định — đơn vị triển khai, khả năng co về không, độ trễ cold start, và cách tính tiền:

| Khía cạnh | Functions | App Service | Container Apps | AKS |
|---|---|---|---|---|
| Đơn vị triển khai | Function (1 file) | App (code/container) | Container (Docker) | Pod (Kubernetes) |
| Runtime | Node/Python/Java/.NET/PowerShell | Như trên + Ruby | Bất kỳ (Docker) | Bất kỳ (Docker) |
| Thời gian chạy tối đa | 5 phút mặc định / 10 phút max (Consumption) · 30 phút (Premium) · không giới hạn (Dedicated) | Không giới hạn | Không giới hạn | Không giới hạn |
| Scale to zero | ✅ (Consumption) | ❌ (luôn ≥1) | ✅ | ❌ (cần KEDA) |
| Cold start | 100-1000ms | Không (luôn warm) | 200-3000ms | Không |
| Cách tính tiền | Theo request + GB-s | Theo instance-hour | Theo request + vCPU/RAM-s | Theo node (VM) |
| Hợp nhất cho | Event-driven, tác vụ ngắn | Web app/API tiêu chuẩn | Microservice container, scale-to-zero | Toàn quyền K8s |
| Tương đương AWS | Lambda | Elastic Beanstalk | Fargate / App Runner | EKS |
| Tương đương GCP | Cloud Functions | App Engine | Cloud Run | GKE |

Đọc bảng theo chiều dọc sẽ thấy ngay quy tắc chọn: càng đi từ trái sang phải, bạn càng đổi sự đơn giản lấy sự kiểm soát. Gom lại thành mấy luật ngón tay cái cho 2026:

- Một đoạn xử lý kích hoạt theo sự kiện → **Functions**.
- Web app/API tiêu chuẩn, không bận tâm container → **App Service**.
- Microservice đóng gói container, cần co về không → **Container Apps**.
- Cần toàn quyền Kubernetes, networking phức tạp, custom controller → **AKS**.

---

## 2️⃣ Azure Functions — Serverless theo sự kiện

Quay lại nhu cầu đầu bài: bắt sự kiện ảnh upload rồi resize. Đây đúng là sân nhà của Functions — bạn chỉ viết phần xử lý, còn chuyện máy chủ ở đâu, scale ra sao thì Azure lo. Nhưng trước khi viết code, có một quyết định về tiền bạc và độ trễ phải chốt: chạy trên *plan* nào.

### 3 hosting plan

Mỗi Function App phải gắn vào một hosting plan, và lựa chọn này quyết định ba thứ: có cold start hay không, scale tới đâu, và mạng có vào được VNet riêng tư không. Bảng dưới so ba plan để bạn khớp với từng nhu cầu:

| Plan | Scale | Cold start | Network | Hợp cho |
|---|---|---|---|---|
| **Consumption** | Scale-to-zero, tối đa 200 instance | 100-500ms | Chỉ public | Thuần event-driven, traffic giật cục |
| **Premium (EP1/EP2/EP3)** | Pre-warmed (always ready), không giới hạn | Không | VNet, Private Endpoint | Production, yêu cầu độ trễ thấp |
| **Dedicated (App Service Plan)** | Thủ công (plan Standard/Premium) | Không | VNet | Chạy chung chỗ với App Service, tác vụ dài |

Khác biệt mấu chốt: Consumption rẻ nhất nhưng có cold start và chỉ ra public; Premium trả tiền giữ sẵn instance để xoá hẳn cold start; Dedicated hợp khi bạn đã có sẵn App Service Plan và muốn tận dụng. Hai lệnh dưới tạo lần lượt một Function App Consumption (trả tiền theo lượt chạy) và một Premium plan (giữ sẵn instance + vào được VNet):

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

### Trigger — function được đánh thức bởi cái gì?

Một function không tự chạy; nó ngủ cho tới khi có một *trigger* (sự kiện kích hoạt) đánh thức. Sức mạnh của Functions nằm ở chỗ trigger phủ gần như mọi nguồn sự kiện trên Azure — từ một request HTTP, một file mới trong Blob, cho tới một dòng thay đổi trong Cosmos DB:

| Trigger | Mô tả |
|---|---|
| **HTTP** | REST endpoint |
| **Timer** | Lịch chạy kiểu cron |
| **Blob** | Sự kiện Storage Blob |
| **Queue** | Storage Queue / Service Bus |
| **Event Grid** | Sự kiện pub-sub |
| **Event Hub** | Streaming |
| **Cosmos DB** | Change feed |
| **Service Bus** | Messaging cấp doanh nghiệp |
| **SignalR** | Real-time |
| **Kafka** (preview) | Kafka topic |

### HTTP function (Python v2 model)

Bắt đầu từ trigger đơn giản nhất để làm quen *Python v2 programming model* (mô hình lập trình mới, khai báo function bằng decorator thay vì file `function.json` rườm rà). Function dưới nhận một request GET, đọc tham số `name`, rồi trả lời:

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

Viết xong, đẩy lên cloud chỉ bằng một lệnh của Core Tools:

```bash
# Deploy
func azure functionapp publish func-api-prod
```

### Blob trigger — đúng nhu cầu resize ảnh đầu bài

Giờ tới trigger giải quyết bài toán của sếp: cứ có ảnh mới rơi vào `uploads/originals/`, function tự thức dậy resize. Điểm đáng chú ý là nó kết nối Storage qua *Managed Identity* (danh tính do Azure quản lý) thay vì nhét chuỗi kết nối vào code — an toàn hơn hẳn:

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

### Giảm cold start

Cold start là cái giá phải trả cho serverless: khi function ngủ lâu, request đầu tiên phải đợi instance khởi tạo. Với tác vụ nền thì không sao, nhưng với API giáp mặt người dùng thì 1-2 giây chờ là khó chấp nhận. Có năm hướng xử lý, đánh đổi giữa hiệu quả và chi phí:

| Cách | Hiệu quả | Chi phí |
|---|---|---|
| Premium plan + min-instances | Hết cold start | Trả tiền cố định |
| Always Ready instance (Premium) | Hết | Trả 1 instance luôn |
| Code warm-up (timer trigger mỗi 5 phút) | Giảm tần suất | Miễn phí |
| Tối ưu kích thước package | Cold nhanh hơn | Miễn phí |
| Chọn runtime hợp lý (Python cold nhanh hơn Java) | Nhanh 30-70% | Miễn phí |

Cách miễn phí dễ làm nhất là cài một timer trigger "đá" function dậy đều đặn, giữ instance luôn ấm:

```python
# Pre-warm: timer trigger every 5 min
@app.schedule(schedule="0 */5 * * * *", arg_name="timer")
def keep_warm(timer: func.TimerRequest):
    logging.info("Warm ping")
```

---

## 3️⃣ Durable Functions — Điều phối luồng nhiều bước

Function đơn lẻ giải quyết tốt việc "một sự kiện → một hành động". Nhưng đời thực thường là chuỗi nhiều bước phụ thuộc nhau: duyệt đơn → trừ tiền → tạo vận đơn, mà giữa các bước có thể phải chờ hàng giờ thậm chí hàng ngày. Viết tay luồng này bằng function thường rất rối state. Durable Functions sinh ra để gánh đúng phần đó.

🪞 **Ẩn dụ**: *Durable Functions như **giấy ủy quyền cho thư ký** — bạn viết workflow tuần tự `Bước 1 → đợi → Bước 2 → ...`; thư ký (Azure runtime) lưu state, đợi event, gọi từng bước dù mất giờ/ngày, không tốn tiền compute trong lúc đợi.*

### Khi nào dùng

Nhận diện được bốn dạng luồng dưới đây là lúc bạn nên nghĩ tới Durable Functions thay vì tự xoay xở:

- Function chain: A → B → C (output A là input B).
- Fan-out / fan-in: chạy song song N task, gom kết quả lại.
- Chờ bất đồng bộ: luồng cần con người duyệt (human approval).
- Workflow chạy dài: hoàn tất đơn hàng kéo dài 3 ngày.

### Pattern: Function chaining

Dạng cơ bản nhất là nối các bước thành chuỗi. Hàm *orchestrator* đóng vai nhạc trưởng — nó dùng `yield` để gọi từng *activity* (bước xử lý thật) và đợi kết quả trước khi sang bước sau; Azure tự lưu state giữa các lần `yield` nên dù process restart, luồng vẫn chạy tiếp đúng chỗ:

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

Khi cần xử lý song song một lô việc rồi gộp kết quả — ví dụ resize cùng lúc cả trăm file — thì dùng fan-out/fan-in. Orchestrator phát N task một lúc rồi `task_all` đợi tất cả xong:

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

Điểm dễ chịu về chi phí: bạn chỉ trả tiền theo mỗi lần activity chạy, còn state của luồng được lưu trong Storage Table (rất rẻ), nên thời gian "ngồi chờ" giữa các bước gần như không tốn gì.

---

## 4️⃣ App Service — PaaS cho Web App

Functions hợp với từng mẩu xử lý theo sự kiện. Nhưng cái backend API `api.acmeshop.vn` mà sếp nhắc tới — một web app đầy đủ, chạy framework quen thuộc — thì App Service mới là chỗ tự nhiên nhất. Đây là PaaS lâu đời và phổ biến nhất của Azure: bạn đẩy code lên, Azure lo phần còn lại.

### Cấu trúc phân tầng

Điều đầu tiên cần nắm là quan hệ giữa *plan* và *app*, vì rất nhiều người mới nhầm hai khái niệm này. Sơ đồ dưới cho thấy nhiều app có thể cùng chạy trên một plan:

```text
App Service Plan: plan-prod-sea (S1, P1v3, ...)
├── Web App: app-api-prod-sea           ← Python FastAPI
├── Web App: app-admin-prod-sea         ← Vue admin
└── Function App: func-cron-prod-sea    ← can co-locate Functions Dedicated
```

Nói gọn: Plan là phần compute (cỡ VM + số replica) — bạn trả tiền cho nó; App là code/container chạy trên plan đó. Một plan có thể gánh nhiều app để chia sẻ tài nguyên.

### Các tier của plan

Chọn tier nào tuỳ vào việc bạn đang ở giai đoạn nào — nghịch thử, staging, hay production cần autoscale và deployment slot. Bảng dưới đi từ free tới isolated:

| Tier | Hợp cho |
|---|---|
| **F1** (Free) | Sandbox, demo (60 phút CPU/ngày) |
| **B1/B2/B3** (Basic) | Dev/staging, không SLA |
| **S1/S2/S3** (Standard) | Production, autoscale, deployment slot |
| **P1v3/P2v3/P3v3** (Premium v3) | Hiệu năng cao, AMD, VNet, private endpoint |
| **I1v2/I2v2/I3v2** (Isolated v2) | ASE dành riêng — compliance/PCI |

Mặc định cho production: bắt đầu nhỏ với **S1**, lên tầm trung thì **P1v3**.

### Các cách deploy

App Service nhận code theo nhiều đường, tuỳ thói quen của team — đẩy thẳng qua git, gửi file ZIP, hay trỏ vào một container image có sẵn. Ba cách phổ biến nhất:

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

### Deployment slot — deploy không downtime

Deploy thẳng lên production là canh bạc: nếu bản mới lỗi, người dùng lãnh đủ. Deployment slot giải quyết bằng cách dựng một bản sao "staging" warm sẵn, test xong mới *swap* (hoán đổi) với production trong tích tắc:

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

Cơ chế đằng sau: code mới đã chạy ấm trên slot staging, lúc swap chỉ là chuyển hướng traffic nên gần như tức thì. Lỡ bản mới có vấn đề thì swap ngược lại là rollback ngay.

### Custom domain + HTTPS tự cấp

Sếp muốn API nằm ở `api.acmeshop.vn`, không phải cái URL `.azurewebsites.net` mặc định. App Service cho gắn custom domain và — quan trọng hơn — cấp luôn chứng chỉ HTTPS miễn phí tự gia hạn, đỡ phải mua cert bên ngoài:

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

Đây là *App Service Managed Certificate* — miễn phí, tự gia hạn. Còn một bước nên làm: ép mọi truy cập về HTTPS để tránh ai đó vào qua HTTP:

```bash
az webapp update --resource-group rg-prod-web --name app-api-prod-sea --https-only true
```

### Xác thực có sẵn (Easy Auth)

Thay vì tự viết code verify token, App Service có *Easy Auth* — bật lên là toàn bộ phần đăng nhập (Entra ID, Google, Facebook...) do nền tảng lo, code chỉ việc đọc thông tin user đã được xác thực:

```bash
# Bật Entra ID auth — code không cần verify token
az webapp auth update \
    --resource-group rg-prod-web \
    --name app-api-prod-sea \
    --enabled true \
    --action LoginWithAzureActiveDirectory \
    --aad-allowed-token-audiences https://app-api-prod-sea.azurewebsites.net
```

Sau khi bật, App Service tự chèn header `X-MS-CLIENT-PRINCIPAL` chứa thông tin user vào mỗi request; code chỉ cần đọc header này. (Lưu ý một cái bẫy về phân quyền sẽ nói ở phần pitfall.)

---

## 5️⃣ Container Apps — Serverless cho container

App Service tiện cho web app chạy code trực tiếp. Nhưng cái REST API của sếp đã đóng gói thành container Docker, lại cần co về không lúc rảnh để tiết kiệm — đó là lúc Container Apps toả sáng. Nó là lớp serverless dựng trên Kubernetes nhưng giấu hết độ phức tạp của K8s đi.

### Container Apps khác App Service container và AKS ở đâu?

Cả ba đều chạy được container, nên dễ phân vân. Khác biệt nằm ở mấy tính năng then chốt — scale-to-zero, Dapr tích hợp sẵn, và mức độ lộ K8s API ra cho bạn:

| Khía cạnh | App Service container | Container Apps | AKS |
|---|---|---|---|
| Scale to zero | ❌ | ✅ | ❌ (cần KEDA) |
| Knative | ❌ | ✅ | thủ công |
| Dapr sidecar | ❌ | ✅ tích hợp sẵn | thủ công |
| Nhiều container/app | ❌ | ✅ (sidecar pattern) | ✅ |
| Truy cập K8s API | ❌ | ❌ | ✅ |
| Cách tính tiền | Theo plan-hour | Theo request + vCPU/RAM-s | Theo node-hour |
| Hợp cho | Web app container đơn giản | Microservice, event-driven, scale-to-zero | K8s workload phức tạp |

Cột giữa cho thấy Container Apps đứng đúng điểm ngọt: có scale-to-zero và Dapr mà không bắt bạn vận hành cả cụm K8s như AKS.

### Khởi tạo

Container Apps gom các app vào một *environment* (bản chất là một cụm K8s do Microsoft quản lý). Hai lệnh dưới tạo environment rồi đặt một Container App vào đó, với `min-replicas 0` để co về không khi rảnh:

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

### Quy tắc auto-scaling (dựa trên KEDA)

Container Apps dùng KEDA (*K8s Event-Driven Autoscaler*) để scale theo tải thật chứ không chỉ theo CPU. Bạn có thể scale theo số request HTTP đồng thời, hoặc theo độ dài hàng đợi Service Bus — rất hợp với worker xử lý nền:

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

### Revision + chia traffic

Mỗi lần update, Container Apps tạo một *revision* (bản chụp bất biến) mới. Bật chế độ nhiều revision rồi chia phần trăm traffic cho phép bạn làm *canary* — thả 10% người dùng sang bản mới để theo dõi trước khi mở hết:

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

Dapr (*Distributed Application Runtime*) chạy như một sidecar cạnh app, cung cấp các pattern phân tán phổ biến — quản lý state, pub-sub, đọc secret, binding — qua một HTTP API thống nhất. Cái lợi: code gọi `localhost` thay vì gọi thẳng dịch vụ Azure, nên dễ chuyển sang cloud khác. Bật Dapr cho một Container App:

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

Cụ thể, app gọi `http://localhost:3500/v1.0/state/statestore` thay vì gọi Storage trực tiếp — nhờ vậy code không dính chặt vào một cloud nào, đổi backend chỉ cần đổi cấu hình Dapr.

---

## 6️⃣ API Management — Cổng API quản lý sẵn

Đến đây bạn đã có backend chạy trên Container Apps. Nhưng phơi nó thẳng ra Internet thì thiếu kiểm soát: ai cũng gọi được, không giới hạn tần suất, không xác thực. API Management đứng trước cùng làm "người gác cổng" lo hết những việc đó.

🪞 **Ẩn dụ**: *API Management như **lễ tân tòa nhà cao cấp** — kiểm tra ID (auth, JWT), giới hạn khách vào/giờ (rate limit), chỉ phòng nào (route), ghi sổ chi tiết (analytics + monitoring), tự hiển thị bảng dịch vụ (developer portal).*

### So sánh các tier

Chi phí APIM nhảy bậc rất mạnh theo tier, nên chọn đúng từ đầu giúp tránh trả thừa. Bảng dưới đi từ Consumption (trả theo lượt gọi, hợp startup) tới Premium (production đa vùng):

| Tier | Hợp cho | Chi phí |
|---|---|---|
| **Consumption** | Trả theo request, dev/PoC | $0.04 / 10k call |
| **Developer** | Single instance, dev/staging | $50/tháng |
| **Basic / Standard / Premium** | Production scale, VNet, multi-region | $147 - $2,795/tháng |

Với một startup như Acme Shop, Consumption là điểm khởi đầu hợp lý. Khi lên production cần VNet, nên nhắm Standard v2 (ra từ 2024+, có VNet integration).

### Quy trình

Dựng APIM đi theo năm bước có thứ tự, từ tạo instance tới gắn policy bảo vệ:

1. Tạo APIM instance.
2. Import backend (OpenAPI spec hoặc Function App / App Service).
3. Định nghĩa **Product** (gom nhiều API thành một gói).
4. Định nghĩa **Subscription** (cấp API key cho từng consumer).
5. Gắn **Policy** (rate limit, transform, auth).

### Dựng APIM

Hai lệnh dưới tạo một instance Consumption rồi import một OpenAPI spec làm API đầu tiên:

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

### Ví dụ policy — rate limit + JWT validate

Sức mạnh thật của APIM nằm ở *policy* — các luật XML chèn vào luồng request/response. Policy dưới minh hoạa một cấu hình production điển hình: kiểm JWT ở đầu vào, giới hạn 100 request/phút và 10000 request/ngày mỗi subscription, rồi thêm CORS header ở đầu ra:

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

Giống App Service, APIM cũng cho gắn domain riêng; điểm khác là chứng chỉ thường lấy từ Key Vault để quản lý tập trung:

```bash
az apim hostname configuration create \
    --resource-group rg-prod-apim \
    --service-name apim-acmeshop-prod \
    --hostname api.acmeshop.vn \
    --certificate-source KeyVault \
    --key-vault-id https://kv-prod.vault.azure.net/secrets/api-cert
```

---

## 🛠️ Hands-on — Pipeline resize ảnh chạy từ đầu đến cuối

Lý thuyết từng phần đã đủ; giờ ráp tất cả thành một thứ chạy thật, đúng yêu cầu của sếp ở đầu bài.

### Mục tiêu

User upload `originals/<file>` → Function tự resize → lưu `resized/{thumb,medium,full}/<file>`. Container Apps API trả về URL các size. APIM đứng trước, chặn bằng API key kèm rate limit. Đi từng bước một.

### Bước 1 — Storage Account + Container

Trước tiên dựng nơi chứa ảnh. Tạo resource group, một Storage Account (tắt public access cho an toàn), và một container tên `uploads`:

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

Tiếp theo dựng Function App chạy Consumption (rẻ, scale-to-zero) và cấp cho nó danh tính hệ thống. Sau đó gán quyền `Storage Blob Data Contributor` để function ghi được ảnh đã resize mà không cần chuỗi kết nối:

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

### Bước 3 — Code Function

Giờ viết code thật cho function. Đoạn dưới khởi tạo project Python v2 model, viết Blob trigger resize ra ba size, khai báo dependency, rồi deploy:

```bash
mkdir resize-fn && cd resize-fn
func init --worker-runtime python --model V2

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

Function lo phần resize; giờ dựng REST API trả URL ảnh. Tạo registry (ACR), build và push image FastAPI, rồi deploy lên Container Apps với scale-to-zero:

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

Đặt APIM trước Container App để quản lý truy cập. Tạo instance Consumption, lấy FQDN của Container App làm backend, rồi tạo API yêu cầu subscription key:

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

Khâu cuối: kiểm chứng cả dây chuyền. Upload một ảnh original, đợi function tự kích hoạt, liệt kê các file đã resize, rồi gọi API qua APIM (cần subscription key):

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

# Lấy subscription id rồi lấy primary key
SUB_ID=$(az apim subscription list \
    --resource-group rg-prod-pipeline \
    --service-name apim-acmeshop-prod \
    --query "[0].name" -o tsv)
SUB_KEY=$(az apim subscription show \
    --resource-group rg-prod-pipeline \
    --service-name apim-acmeshop-prod \
    --sid "$SUB_ID" --query primaryKey -o tsv)

# Call API qua APIM (cần subscription key)
APIM_URL=$(az apim show -n apim-acmeshop-prod -g rg-prod-pipeline --query gatewayUrl -o tsv)
curl "$APIM_URL/images/products/test/images" \
    -H "Ocp-Apim-Subscription-Key: $SUB_KEY"
```

### Bước 7 — Dọn dẹp

Xoá toàn bộ resource group là cách nhanh và sạch nhất để khỏi tốn tiền sau khi thử xong:

```bash
az group delete --name rg-prod-pipeline --yes --no-wait
```

→ **Kết quả**: Pipeline Blob → Function → Container Apps → APIM hoạt động end-to-end.

---

## 💡 Cạm bẫy thường gặp & Best practice

Phần này gom những chỗ dễ vấp nhất khi vận hành thật. Mỗi mục theo công thức quen thuộc: nêu cái bẫy, rồi cách chữa.

### ❌ Cạm bẫy: Cold start lâu cho Functions giáp mặt người dùng

**Bẫy**: Consumption plan + API giáp mặt người dùng → P95 latency lên 1-2s.

**Fix**:
- Premium plan + min-instances ≥ 1.
- Always Ready instance trong Premium.
- Tối ưu kích thước package (gỡ dev dependency).
- Health check endpoint chạy cron mỗi 5 phút.

### ❌ Cạm bẫy: Function hết giờ giữa chừng

**Bẫy**: Consumption mặc định 5 phút, tối đa 10 phút → tác vụ xử lý ảnh dài bị cắt ngang.

**Fix**:
- Premium: 30 phút.
- Dedicated (App Service Plan): không giới hạn.
- Hoặc dùng **Durable Functions** + chia thành activity nhỏ.
- Hoặc dùng **Container Apps Job** cho batch.

### ❌ Cạm bẫy: Blob trigger bỏ sót sự kiện (do polling)

**Bẫy**: Blob trigger trên Consumption dùng polling — có thể trễ 1-10 phút khi storage có nhiều blob.

**Fix**:
- Dùng **Event Grid** trigger thay Blob trigger → event-driven, độ trễ dưới một giây.
- Hoặc Premium plan kết hợp Event Grid.

### ❌ Cạm bẫy: App Service rebuild lúc deploy gây downtime

**Bẫy**: Deploy code Python → App Service tự rebuild → downtime 5-10 phút (nếu chạy single instance).

**Fix**:
- **Deployment slot** + swap (không downtime).
- Chạy multi-instance từ B1 trở lên.
- Deploy bằng container thì không rebuild.

### ❌ Cạm bẫy: Custom domain không tự có HTTPS

**Bẫy**: Map domain `api.acmeshop.vn` → HTTP chạy được, HTTPS báo lỗi (chưa có cert).

**Fix**:
- Bật **App Service Managed Certificate** (miễn phí, tự gia hạn).
- Hoặc mang cert riêng vào qua Key Vault.
- Kiểm: bật `--https-only true`.

### ❌ Cạm bẫy: Container Apps cold start lớn

**Bẫy**: `min-replicas=0` → request đầu phải chờ 1-3s pull image.

**Fix**:
- `min-replicas=1` cho endpoint giáp mặt người dùng.
- Image nhỏ hơn (Alpine, distroless).
- Dùng ACR cùng region (pull nhanh hơn).

### ❌ Cạm bẫy: APIM Consumption không có VNet

**Bẫy**: APIM Consumption rẻ nhưng không hỗ trợ VNet integration → không gọi được backend qua private endpoint.

**Fix**:
- Để backend qua public endpoint + whitelist IP của APIM.
- Hoặc nâng lên Standard v2 (ra từ 2024+, hỗ trợ VNet).

### ❌ Cạm bẫy: Easy Auth không kiểm claim của token

**Bẫy**: Easy Auth chỉ verify chữ ký; không kiểm claim `role` → user không phải admin vẫn vào được admin endpoint.

**Fix**:
- App tự kiểm role từ header `X-MS-CLIENT-PRINCIPAL`.
- Hoặc dùng APIM với `validate-jwt` + `required-claims`.

### ❌ Cạm bẫy: Nhiều Function App share một Storage Account

**Bẫy**: Nhiều Function App dùng chung 1 Storage Account → tranh chấp lease, chậm.

**Fix**:
- Mỗi Function App một Storage Account riêng (tạo qua portal mặc định đã đúng).
- Tách `AzureWebJobsStorage` (state nội bộ) khỏi storage chứa data.

### ❌ Cạm bẫy: Không set max-replicas khiến chi phí phình to

**Bẫy**: Container Apps không set `max-replicas` → bị tấn công bot → bung 1000 replica → hoá đơn khổng lồ.

**Fix**:
- Luôn set `--max-replicas`.
- Đặt WAF (Front Door / APIM) phía trước để rate limit.
- Bật budget alert.

---

## 🧠 Tự kiểm tra (Self-check)

Tự trả lời được mười câu dưới nghĩa là bạn đã nắm được phần xương sống của bài. Câu nào còn lăn tăn thì quay lại đúng section tương ứng:

- [ ] So sánh Functions vs App Service vs Container Apps vs AKS cho 4 use case khác nhau?
- [ ] Function plan Consumption vs Premium vs Dedicated — chọn cho event-driven, giáp mặt người dùng, chạy dài?
- [ ] Deploy Function với Blob trigger + Managed Identity truy cập Storage — luồng thế nào?
- [ ] Durable Function pattern chain vs fan-out — ví dụ code?
- [ ] App Service deployment slot swap — deploy không downtime ra sao?
- [ ] Container Apps min-replicas=0 vs 1 — đánh đổi chi phí vs độ trễ?
- [ ] Container Apps Dapr sidecar — lợi ích gì?
- [ ] APIM policy `validate-jwt` + `rate-limit-by-key` — bảo vệ backend thế nào?
- [ ] Bốn cách giảm cold start — chọn theo budget?
- [ ] Ước lượng chi phí: 1 triệu request/tháng trên Function Consumption vs Container Apps?

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Gom các lệnh hay dùng nhất cho bốn cửa serverless/PaaS của bài — `az functionapp ...`, `az webapp ...`, `az containerapp ...` và `az apim ...`.

| Mục đích | Lệnh |
|---|---|
| Tạo Function App Consumption | `az functionapp create -g <rg> --name <func> --consumption-plan-location southeastasia --storage-account <st> --runtime python --runtime-version 3.12 --functions-version 4 --os-type Linux` |
| Tạo Premium plan (always-ready + VNet) | `az functionapp plan create -g <rg> --name <plan> --sku EP1 --is-linux true --min-instances 1 --max-burst 20` |
| Function App + Managed Identity | `az functionapp create ... --assign-identity '[system]'` |
| Deploy Function (Core Tools) | `func azure functionapp publish <func>` |
| Tạo Web App từ container | `az webapp create -g <rg> --name <app> --plan <plan> --deployment-container-image-name <image>` |
| ZIP deploy Web App | `az webapp deploy -g <rg> --name <app> --src-path ./build.zip --type zip` |
| Tạo deployment slot | `az webapp deployment slot create -g <rg> --name <app> --slot staging` |
| Swap slot (zero downtime) | `az webapp deployment slot swap -g <rg> --name <app> --slot staging --target-slot production` |
| Custom domain + managed cert | `az webapp config hostname add ...` · `az webapp config ssl create ...` · `az webapp update ... --https-only true` |
| Bật Easy Auth (Entra ID) | `az webapp auth update -g <rg> --name <app> --enabled true --action LoginWithAzureActiveDirectory` |
| Tạo Container Apps environment | `az containerapp env create --name <cae> -g <rg> --location southeastasia` |
| Tạo Container App scale-to-zero | `az containerapp create --name <ca> -g <rg> --environment <cae> --image <image> --target-port 8000 --ingress external --min-replicas 0 --max-replicas 10 --cpu 0.5 --memory 1Gi` |
| Scale rule theo HTTP / Service Bus | `az containerapp update ... --scale-rule-type http --scale-rule-http-concurrency 50` |
| Chia traffic giữa revision (canary) | `az containerapp ingress traffic set --name <ca> -g <rg> --revision-weight <r1>=90 <r2>=10` |
| Bật Dapr sidecar | `az containerapp create ... --enable-dapr --dapr-app-id <id> --dapr-app-port 8000` |
| Tạo APIM Consumption | `az apim create --name <apim> -g <rg> --publisher-email <email> --publisher-name "<name>" --sku-name Consumption` |
| Import OpenAPI vào APIM | `az apim api import -g <rg> --service-name <apim> --api-id <id> --path <path> --specification-url <url> --specification-format OpenApi` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Azure Functions** | Hàm serverless | Chạy từng function theo sự kiện |
| **Consumption plan** | Gói trả theo lượt | Pay-per-execution, scale-to-zero |
| **Premium plan** | Gói cao cấp | Always-ready, VNet, không cold start |
| **App Service** | Dịch vụ web PaaS | PaaS cho web app (code hoặc container) |
| **App Service Plan** | Gói compute | Lớp compute (cỡ VM + số lượng) |
| **Web App** | Ứng dụng web | App chạy trên Plan |
| **Deployment slot** | Khe triển khai | Bản pre-prod, swap không downtime |
| **App Service Managed Certificate** | Chứng chỉ tự quản | SSL miễn phí, tự gia hạn |
| **Easy Auth** | Xác thực có sẵn | Auth tích hợp (Entra ID, Google, Facebook) |
| **Container Apps** | Container serverless | Container serverless, Knative + Dapr |
| **Container Apps Environment** | Môi trường Container Apps | Nhóm app dùng chung VNet + Log Analytics |
| **Revision** | Bản chụp | Snapshot bất biến của Container App |
| **Traffic split** | Chia traffic | Chia % traffic giữa các revision (canary) |
| **KEDA** | Bộ autoscale theo sự kiện | K8s Event-Driven Autoscaler |
| **Dapr** | Runtime ứng dụng phân tán | Distributed application runtime (sidecar) |
| **AKS** | Kubernetes của Azure | Azure Kubernetes Service |
| **API Management (APIM)** | Cổng API quản lý sẵn | Managed API gateway |
| **Product / Subscription** | Gói API / Đăng ký | Phân tầng APIM: nhóm API + key cho consumer |
| **Policy** | Luật xử lý | Luật XML của APIM (auth, rate, transform) |
| **Durable Functions** | Function điều phối luồng | Orchestration luồng (chain/fan-out) |
| **Cold start** | Khởi động nguội | Độ trễ khi instance vừa khởi tạo |
| **Always Ready instance** | Instance giữ sẵn | Instance pre-warmed của Premium plan |
| **ACR** | Registry container Azure | Azure Container Registry |
| **Blob trigger** | Kích hoạt theo Blob | Function chạy khi Blob được tạo/cập nhật |
| **Event Grid trigger** | Kích hoạt theo Event Grid | Event-driven, độ trễ dưới một giây |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Azure SQL + Cosmos DB](03_azure-sql-and-cosmosdb.md)
- ↑ **Về cụm:** [Azure](../../README.md)
- 🔜 **Tiếp theo (sắp viết):** Cụm Intermediate — AKS, Bicep, ARM, Service Bus deep, Front Door + WAF, Cost optimization

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS Lambda + API Gateway](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — tương đương Functions + APIM
- ☁️ [GCP Cloud Functions + Cloud Run + API Gateway](../../../gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) — đối chiếu
- 🐳 [Docker basic](../../../../10_devops/docker/) — build image cho Container Apps
- 🔁 [CI/CD basic](../../../../10_devops/ci-cd/) — deploy serverless từ pipeline
- 🧭 [Cloud Engineer roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác

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

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bài 04 (cuối basic) Azure. Functions (Consumption/Premium/Dedicated) + 10+ trigger + Durable Functions chain/fan-out + App Service Plan + Web App + deployment slot + custom domain + Easy Auth + Container Apps Knative + Dapr + revision traffic split + APIM Consumption + policy JWT/rate-limit + decision tree 4 compute options + hands-on image pipeline Blob→Function→Container Apps→APIM + 10 pitfalls. Hoàn thành Azure basic cluster 5/5.
- **v2.0.0 (01/06/2026)** — Viết lại toàn bộ prose sang tiếng Việt narrative theo gold-standard: thêm lời dẫn trước mỗi bảng/code/list và câu bắc cầu giữa các section, giữ nguyên ẩn dụ. Sửa lỗi QA: `func init` đúng cú pháp (`--worker-runtime python --model V2`, bỏ `--python` thừa); viết đủ lệnh lấy APIM subscription key (bỏ `...` cắt giữa lệnh, lấy `--sid` từ `az apim subscription list`); làm rõ Consumption timeout (mặc định 5 phút, tối đa 10 phút) ở bảng decision và pitfall. Chuẩn hoá heading framework, metadata field "Yêu cầu trước", Glossary 3 cột, nav marker `⬅️/↑/🔜` + 3 sub-heading chuẩn. Giữ nguyên 100% code/số liệu/cấu trúc 8 phần.
- **v2.0.1 (10/06/2026)** — Bổ sung mục Tra cứu nhanh (Cheatsheet) cho đồng bộ với cụm Azure.
