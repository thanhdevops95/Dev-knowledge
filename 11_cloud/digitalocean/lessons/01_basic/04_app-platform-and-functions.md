# 🚀 App Platform + Functions + DOKS — PaaS + Serverless + K8s

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Managed Databases](03_managed-databases.md), hiểu Docker, K8s cơ bản, Git

> 🎯 *Bài cuối cluster basic — đi qua **App Platform** (PaaS auto-build từ Git, alternative Heroku/Render), **Functions** (serverless), **DOKS** (Managed K8s), **Load Balancer**, **Container Registry**. Bạn sẽ chọn được "deploy stack" cho project tuỳ scale, hands-on App Platform deploy FastAPI từ Git.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **App Platform** là gì, khi nào dùng vs Droplet
- [ ] Deploy app từ **GitHub** lên App Platform (push → live)
- [ ] Cấu hình **App Spec** YAML (services, jobs, databases, env)
- [ ] Hiểu **Functions** serverless DO khi nào dùng
- [ ] Setup **DOKS** Kubernetes cluster cơ bản
- [ ] Dùng **Load Balancer** trước Droplet/DOKS
- [ ] Push image lên **Container Registry**
- [ ] **Decision matrix**: Droplet vs App Platform vs Functions vs DOKS
- [ ] Hands-on deploy FastAPI lên App Platform với auto-deploy

---

## Tình huống — "Tôi không muốn quản OS"

Cuối tuần sếp message:

> *"Internal tool đang chạy Droplet ổn rồi. Giờ team marketing muốn deploy 1 landing page (Next.js) + 1 Telegram bot (Python). Họ không biết Linux, đừng bắt họ học SSH/systemd/nginx. Có cách nào push GitHub là live không?"*

→ **App Platform** chính xác cho case này:
- Push code → DO auto-build → deploy.
- HTTPS auto, scaling auto, log/metric built-in.
- Marketing team chỉ cần thao tác Git, không cần Linux skill.

Bài này dạy chọn đúng "deploy stack" cho từng workload.

---

## 1️⃣ App Platform là gì

🪞 **Ẩn dụ**: *Droplet như **mua đất tự xây nhà** — bạn lo móng, tường, điện, nước. App Platform như **thuê căn hộ chung cư có dịch vụ** — bạn chỉ mang đồ đạc (code) vào, mọi tiện ích (build, HTTPS, scale, log) có sẵn.*

### Định nghĩa

**App Platform** = PaaS (*Platform-as-a-Service* — nền tảng dịch vụ) của DO, ra mắt 2020, là lựa chọn thay thế cho **Heroku / Render / Railway / Fly.io**.

Điều khiến App Platform đáng chú ý nằm ở chỗ: bạn chỉ làm đúng một việc là `git push`, mọi khâu còn lại DO lo hết. Sơ đồ dưới mô tả toàn bộ chặng đường từ lúc bạn đẩy code đến khi có một URL HTTPS chạy thật — không có bước nào bạn phải tự gõ lệnh trên server.

```text
Git push → DO clone → detect stack → Docker build (Buildpack/Dockerfile) → deploy to managed runtime → HTTPS public URL
```

So với quy trình tự dựng trên Droplet (SSH vào máy, kéo code, cài runtime, dựng nginx, xin cert), pipeline này gói gọn tất cả vào một thao tác Git quen thuộc.

### Đặc điểm 2026

Trước khi quyết định có "dọn vào căn hộ" này hay không, bạn cần biết nó trang bị sẵn những gì. Bảng dưới liệt kê các tính năng App Platform hỗ trợ tới năm 2026 — phần lớn là những thứ với Droplet bạn phải tự dựng (HTTPS, scaling, log, cron).

| Tính năng | Hỗ trợ |
|---|---|
| Auto-deploy từ Git | ✅ GitHub, GitLab |
| Buildpack (Node, Python, Ruby, Go, PHP, Static) | ✅ Cloud Native Buildpacks |
| Dockerfile | ✅ |
| Docker Hub / Custom registry | ✅ |
| HTTPS + custom domain | ✅ Auto Let's Encrypt |
| Horizontal scale | ✅ 1-25 instance |
| Vertical resize | ✅ |
| Health check | ✅ |
| Cron job | ✅ "Jobs" component |
| Worker (background) | ✅ "Workers" component |
| Static site | ✅ Free tier 3 site |
| Database | ✅ Managed DB attach |
| Env var + secret | ✅ Encrypted secret |
| Log / metric | ✅ Built-in dashboard |
| Region | 7 region (`nyc`, `ams`, `fra`, `sgp`, `sfo`, `blr`, `syd`) |

### Component types

Một app trên App Platform không chỉ là "một web server". Nó được lắp ráp từ nhiều loại *component* (thành phần), mỗi loại đảm nhiệm một vai trò khác nhau giống các phòng ban trong một công ty — có người tiếp khách (Service), có người làm việc hậu trường (Worker), có người chạy việc định kỳ (Job). Bảng dưới điểm qua từng loại và khi nào dùng.

| Type | Mô tả | Use case |
|---|---|---|
| **Service** | Long-running HTTP server | FastAPI, Express, Rails |
| **Worker** | Background process | Celery worker, queue consumer |
| **Job** | One-shot hoặc cron | DB migration, daily report |
| **Static Site** | Static files (HTML/CSS/JS) | Next.js export, Vue/React build |
| **Database** | Attach managed DB | Dev DB nhỏ |
| **Function** | Serverless function | Webhook, light API (xem §3) |

### Pricing tier

Sự tiện lợi có giá của nó, nhưng với App Platform mức giá khá dễ chịu và minh bạch theo từng *tier* (bậc tài nguyên). Đáng chú ý là static site có hẳn bậc miễn phí, còn service nhỏ nhất chỉ từ $5/tháng — rẻ ngang một Droplet cơ bản nhưng đỡ cho bạn toàn bộ phần vận hành.

| Tier | RAM | vCPU | Giá/tháng |
|---|---|---|---|
| **Basic xxs** (static free) | — | — | $0 (3 site) |
| **Basic XXS service** | 512 MB | 1 shared | $5 |
| **Basic XS** | 1 GB | 1 shared | $12 |
| **Basic S** | 2 GB | 1 | $25 |
| **Professional XS** | 1 GB | 1 dedicated | $29 |
| **Professional M** | 4 GB | 2 dedicated | $112 |

→ Mỗi container = 1 instance. Scale horizontal = nhân số instance.

---

## 2️⃣ App Spec — Khai báo declarative

Thay vì click chuột qua từng màn hình cấu hình, App Platform cho bạn mô tả toàn bộ app trong một file `app.yaml` duy nhất — gọi là *App Spec*. Đây là cách tiếp cận *declarative* (khai báo): bạn nói "tôi muốn hệ thống trông như thế này", DO lo phần dựng đúng như mô tả. Bản thân giao diện UI khi bạn cấu hình tay cũng chỉ đang sinh ra file này phía sau, nên nắm App Spec là nắm được "ngôn ngữ gốc" của App Platform.

### Ví dụ — FastAPI service + worker + cron + DB

Ví dụ dưới gói gọn gần như mọi loại component vào một spec: một `service` chạy FastAPI, một `worker` Celery xử lý nền, hai `job` (migrate trước khi deploy và báo cáo hằng ngày), một `static_site` cho landing page, và một `database` Postgres attach kèm. Đọc qua một lượt, bạn sẽ thấy toàn bộ một hệ thống thực tế được khai báo gọn trong vài chục dòng.

```yaml
# .do/app.yaml
name: acmeshop-stack
region: sgp

services:
  - name: api
    github:
      repo: acmeshop/api
      branch: main
      deploy_on_push: true
    source_dir: /
    build_command: pip install -r requirements.txt
    run_command: uvicorn main:app --host 0.0.0.0 --port 8080
    http_port: 8080
    instance_count: 2
    instance_size_slug: apps-s-1vcpu-1gb
    health_check:
      http_path: /health
    routes:
      - path: /
    envs:
      - key: ENV
        value: production
      - key: DATABASE_URL
        type: SECRET
        value: ${db.DATABASE_URL}

workers:
  - name: celery-worker
    github:
      repo: acmeshop/api
      branch: main
    source_dir: /
    build_command: pip install -r requirements.txt
    run_command: celery -A app worker --loglevel=info
    instance_count: 1
    instance_size_slug: apps-s-1vcpu-1gb
    envs:
      - key: DATABASE_URL
        value: ${db.DATABASE_URL}

jobs:
  - name: db-migrate
    kind: PRE_DEPLOY  # chạy trước deploy
    github:
      repo: acmeshop/api
      branch: main
    run_command: alembic upgrade head
    instance_size_slug: apps-s-1vcpu-1gb

  - name: daily-report
    kind: CRON
    schedule: "0 6 * * *"  # 06:00 UTC daily
    github:
      repo: acmeshop/api
      branch: main
    run_command: python scripts/daily_report.py

static_sites:
  - name: marketing
    github:
      repo: acmeshop/landing
      branch: main
    source_dir: /
    build_command: npm run build
    output_dir: /dist
    routes:
      - path: /static

databases:
  - name: db
    engine: PG
    version: "17"
    production: false
    size: db-s-1vcpu-1gb
```

### Deploy

Có spec rồi, bạn đưa nó lên DO bằng `doctl` — CLI chính thức của DigitalOcean. Vòng đời thường gặp là: tạo app lần đầu, rồi mỗi khi sửa spec thì `update`, và xem log khi cần debug. Các lệnh dưới đi theo đúng trình tự đó.

```bash
# Tạo app từ spec
doctl apps create --spec .do/app.yaml

# List apps
doctl apps list

# Get app ID
APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep acmeshop-stack | awk '{print $1}')

# Update khi sửa spec
doctl apps update $APP_ID --spec .do/app.yaml

# Trigger deploy manual
doctl apps create-deployment $APP_ID

# Log
doctl apps logs $APP_ID --type build  # build log
doctl apps logs $APP_ID --type run --follow  # runtime log
```

### Auto-deploy on push

Spec có `deploy_on_push: true` → mọi commit lên `main` → DO clone → build → deploy. Push → live trong 3-5 phút.

---

## 3️⃣ Functions — Serverless

🪞 **Ẩn dụ**: *Functions như **gọi shipper khi cần ship 1 món** — không cần thuê nhân viên cả tháng, chỉ trả tiền theo cuốc.*

Khác với Service (luôn bật, tính tiền cả khi không có khách), Functions chỉ "sống dậy" khi có request rồi tắt đi. Bảng dưới tóm tắt các giới hạn và đặc tính kỹ thuật của DO Functions — đây là những con số quyết định liệu workload của bạn có hợp với mô hình này không.

### Đặc điểm

| | DO Functions |
|---|---|
| **Engine** | OpenWhisk (open source) |
| **Runtime** | Node.js, Python, Go, PHP |
| **Max duration** | Tối đa 15 phút (tương đương AWS Lambda) |
| **Memory** | 128MB - 1GB |
| **Trigger** | HTTP, schedule (cron), web hook |
| **Pricing** | $1.85/1M request + $0.0000185/GB-s |
| **Free tier** | 90,000 GB-s/tháng |

### Khi nào dùng Functions

| Use case | Lý do |
|---|---|
| Webhook receiver (GitHub, Stripe, ...) | Low traffic, on-demand |
| Image resize on-demand | Spawn nhanh, scale tự |
| Scheduled job nhẹ | Cheaper than Droplet idle |
| API endpoint single-purpose | Decoupled khỏi monolith |
| Edge compute trigger | Process event from queue |

### Khi nào KHÔNG dùng

- Long-running > 15 phút → DOKS / Droplet.
- Stateful (WebSocket, SSE long-poll) → App Platform.
- Cold start sensitive (latency p99 < 100ms) → App Platform always-on.

### Hands-on Function

Lý thuyết là vậy, giờ thử viết một function "Hello" thật để thấy nó nhẹ đến mức nào. Toàn bộ quy trình gói trong vài bước: cài plugin serverless, viết một hàm Python `main(args)`, khai báo trong `project.yml`, rồi `deploy`. Để ý cấu trúc — không có server, không có Dockerfile, chỉ một hàm thuần.

```bash
# Init project (cần `doctl serverless` plugin)
doctl serverless install
doctl serverless connect

mkdir hello-fn && cd hello-fn

# Function code
mkdir -p packages/sample
cat > packages/sample/hello.py <<'EOF'
def main(args):
    name = args.get("name", "World")
    return {"body": f"Hello, {name}!"}
EOF

# Project config
cat > project.yml <<'EOF'
packages:
  - name: sample
    functions:
      - name: hello
        runtime: python:default
        web: true
EOF

# Deploy
doctl serverless deploy .

# Invoke
doctl serverless functions invoke sample/hello -p name:Acme
# > Hello, Acme!

# Get URL
doctl serverless functions get sample/hello --url
# > https://faas-sgp1-xxxxx.doserverless.co/api/v1/web/fn-yyyyy/sample/hello
```

---

## 4️⃣ DOKS — DigitalOcean Kubernetes

🪞 **Ẩn dụ**: *Droplet là **căn hộ riêng**, App Platform là **chung cư có dịch vụ**, DOKS là **khu công nghiệp** — bạn có nhiều nhà xưởng (Pod), có quản lý chung (control plane), tự build microservice ecosystem.*

DOKS là *Managed Kubernetes* của DO: bạn không phải tự dựng và vá *control plane* (tầng điều khiển K8s) — DO host phần đó miễn phí, bạn chỉ trả tiền cho worker node. Bảng dưới điểm những đặc tính quan trọng nhất, đặc biệt là các phần được tích hợp sẵn với hệ sinh thái DO (Load Balancer, Volume, Registry).

### Đặc điểm

| | DOKS |
|---|---|
| **Control plane** | Free (DO host) |
| **Worker nodes** | Bill như Droplet thường |
| **K8s version** | 1.30, 1.31, 1.32 (lag 1-2 version sau upstream) |
| **CNI** | Cilium |
| **Storage CSI** | DO Volume native |
| **LB integration** | DO LB auto-provision khi `Service type=LoadBalancer` |
| **Registry** | DO Container Registry tích hợp |
| **Auto-scaling** | Cluster Autoscaler + HPA |

### Khi nào dùng DOKS

- Team > 5 dev, microservice > 5 services.
- Đã có expertise K8s.
- Cần feature K8s-specific: NetworkPolicy, sidecar pattern, advanced rolling update, GitOps Argo CD.
- Workload portable (sẽ migrate vendor sau).

### Khi nào KHÔNG DOKS

- Monolith app đơn giản → App Platform / Droplet.
- Team chưa biết K8s → học cost lớn, App Platform tốt hơn.

### Hands-on DOKS

Phần dưới dựng một cluster thật từ con số không: tạo cluster với node pool tự co giãn, lưu kubeconfig để `kubectl` trỏ đúng cluster, rồi deploy một nginx và expose ra ngoài. Điểm hay nhất nằm ở bước cuối — chỉ cần khai báo `Service type=LoadBalancer`, DO sẽ tự dựng một Load Balancer thật và gán IP công khai, bạn không phải động tay.

```bash
# Tạo cluster
doctl kubernetes cluster create acmeshop-prod \
    --region sgp1 \
    --version 1.32.x-do.0 \
    --node-pool "name=pool-1;size=s-2vcpu-4gb;count=2;auto-scale=true;min-nodes=2;max-nodes=5" \
    --wait

# Save kubeconfig
doctl kubernetes cluster kubeconfig save acmeshop-prod

# Verify
kubectl get nodes
# NAME            STATUS   ROLES    AGE   VERSION
# pool-1-xxxxx    Ready    <none>   3m    v1.32.x

# Deploy sample
kubectl create deployment nginx --image=nginx:1.27 --replicas=3
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# DO tự provision LB
kubectl get svc nginx
# NAME    TYPE           EXTERNAL-IP       PORT(S)
# nginx   LoadBalancer   138.197.xxx.xxx   80:30000/TCP

curl http://138.197.xxx.xxx
# Welcome to nginx!
```

### Cost example

Chi phí DOKS là tổng của worker node, Load Balancer và Volume — control plane không tính tiền. Bảng dưới là một cấu hình production tối thiểu thực tế để bạn hình dung con số mỗi tháng.

| Component | Cost |
|---|---|
| Control plane | $0 free |
| 2 worker `s-2vcpu-4gb` | $24 × 2 = $48 |
| Load Balancer (1) | $12 |
| Persistent Volume (50GB) | $5 |
| **Total** | ~$65/tháng |

So với AWS EKS: riêng *control plane* đã tốn ~$73/tháng ($0.10/giờ) trước khi tính worker node. DOKS miễn phí control plane nên với cùng quy mô sẽ rẻ hơn rõ.

---

## 5️⃣ Load Balancer — L4/L7 managed

Khi bạn chạy nhiều Droplet để có sẵn sàng cao (*high availability*), cần một "người gác cổng" đứng trước phân phối request và loại bỏ máy nào đang hỏng. DO Load Balancer làm đúng việc đó dưới dạng *managed* — bạn không phải tự dựng nginx/HAProxy rồi lo cấu hình TLS, health check. Bảng dưới liệt kê những gì nó hỗ trợ sẵn.

### Đặc điểm

| | DO Load Balancer |
|---|---|
| **Type** | L4 (TCP) + L7 (HTTP/HTTPS) |
| **TLS termination** | ✅ Auto Let's Encrypt hoặc custom |
| **Health check** | HTTP/TCP every 5-60s |
| **Sticky session** | ✅ Cookie-based |
| **HTTP/2** | ✅ |
| **WebSocket** | ✅ |
| **Pricing small** | $12/tháng (10k concurrent conn) |
| **Pricing medium** | $24 |
| **Pricing large** | $48 |

### Khi nào dùng

- HA 2+ Droplet → cần LB phân phối.
- Auto TLS cho domain (thay tự setup nginx + certbot).
- Health check + auto remove unhealthy backend.
- Front DOKS expose Service type=LoadBalancer.

### Tạo Load Balancer

```bash
# Tạo LB với Droplet backend
doctl compute load-balancer create \
    --name acmeshop-lb \
    --region sgp1 \
    --droplet-ids 123,456 \
    --forwarding-rules "entry_protocol:https,entry_port:443,target_protocol:http,target_port:8000,certificate_id:CERT_ID" \
    --forwarding-rules "entry_protocol:http,entry_port:80,target_protocol:http,target_port:8000" \
    --health-check "protocol:http,port:8000,path:/health,check_interval_seconds:10"

# DNS: api.acmeshop.vn → LB IP (CNAME hoặc A)
```

### Auto TLS certificate

```bash
# Tạo cert managed Let's Encrypt
doctl compute certificate create \
    --type lets_encrypt \
    --name acmeshop-cert \
    --dns-names api.acmeshop.vn

# Use cert_id trong forwarding-rules
```

DO auto-renew Let's Encrypt cert (60 ngày trước expire).

---

## 6️⃣ Container Registry

Nếu App Platform và DOKS là nơi *chạy* image, thì Container Registry là nơi *cất* chúng — một kho Docker image private nằm ngay trong DO, tích hợp sẵn với DOKS để kéo image không cần khai báo credential thủ công. Các lệnh dưới đi trọn vòng đời: tạo registry, login Docker, tag và push image, rồi nối vào cluster.

```bash
# Tạo registry (1 registry / account, không phải / project)
doctl registry create acmeshop --subscription-tier basic

# Login Docker
doctl registry login

# Tag + push
docker tag my-app:latest registry.digitalocean.com/acmeshop/my-app:v1.0.0
docker push registry.digitalocean.com/acmeshop/my-app:v1.0.0

# Pull
docker pull registry.digitalocean.com/acmeshop/my-app:v1.0.0

# List repos
doctl registry repository list

# Integrate với DOKS (auto pull secret)
doctl registry kubernetes-manifest | kubectl apply -f -
```

### Pricing

| Tier | Storage | Bandwidth | Giá |
|---|---|---|---|
| **Starter** | 500 MB | 500 MB | $0 (free, 1 repo) |
| **Basic** | 5 GB | 5 GB | $5/tháng |
| **Professional** | 100 GB | 100 GB | $20/tháng |

→ So với Docker Hub Pro ($5 = unlimited public), DO Registry chỉ thắng khi cần private + tích hợp DOKS.

---

## 7️⃣ Decision matrix — Chọn stack nào

Tới đây bạn đã quen mặt từng "deploy stack". Câu hỏi thực tế còn lại là: với một workload cụ thể, chọn cái nào? Không có đáp án "tốt nhất" tuyệt đối — chỉ có "hợp nhất với hoàn cảnh". Bảng dưới ánh xạ từng loại workload phổ biến sang lựa chọn phù hợp, kèm lý do ngắn gọn để bạn tự suy luận cho case của mình.

### Bảng quyết định

| Workload | Best fit | Lý do |
|---|---|---|
| Static landing page | Static Site (App Platform) | Free, CDN sẵn |
| Personal blog | Static Site | Free |
| Single FastAPI app, < 10k req/day | App Platform Service | Push GitHub, auto-deploy |
| FastAPI + Postgres + Worker | App Platform (full stack) | All-in-one |
| Custom OS / kernel tune | Droplet | App Platform không cho SSH OS |
| Webhook receiver | Functions | Pay-per-request |
| Daily cron job nhẹ | Functions hoặc App Platform Job | Functions rẻ hơn nếu < 90k GB-s |
| Microservice 10+ services | DOKS | K8s flexibility |
| ML training | GPU Droplet | App Platform không GPU |
| Self-host DB (cần extension custom) | Droplet | Managed DB không cho |
| WebSocket long-connection | App Platform / Droplet | Functions không phù hợp |
| Internal tool team < 20 | App Platform | Simple, no infra ops |
| Bandwidth-heavy CDN | Spaces + CDN | Free CDN bandwidth |

### Migration path

Lựa chọn stack không cố định một lần là xong — nó tiến hóa theo quy mô team và traffic. Sơ đồ dưới phác lộ trình điển hình: bắt đầu đơn giản nhất có thể, chỉ "lên đời" khi thực sự chạm trần của bậc hiện tại. Đây là kim chỉ nam tránh over-engineering ngay từ đầu.

```text
Solo dev / MVP:    Static Site / App Platform (Basic)
↓ scale traffic
Small team:        App Platform (Pro) + Managed DB
↓ need flexibility
Mid team:          Droplet + LB + Managed DB
↓ scale services
Large team:        DOKS + Managed DB + Spaces + CDN
↓ need vendor diverse
Enterprise:        Multi-cloud (DO + AWS + ...)
```

---

## 🛠️ Hands-on — Deploy FastAPI lên App Platform

### Mục tiêu

1. Có GitHub repo FastAPI nhỏ.
2. Deploy lên App Platform với DB attach.
3. Push commit → auto-redeploy.

### Bước 1 — Repo

Một app FastAPI tối thiểu cần đúng ba thứ: code (`main.py`), danh sách dependency (`requirements.txt`), và file App Spec (`.do/app.yaml`). Cấu trúc thư mục dưới đây là tất cả những gì bạn cần đẩy lên GitHub.

```text
acmeshop/api-mini/
├── main.py
├── requirements.txt
└── .do/
    └── app.yaml
```

```python
# main.py
from fastapi import FastAPI
import os, asyncpg

app = FastAPI()
DATABASE_URL = os.environ["DATABASE_URL"]

@app.get("/")
def root():
    return {"message": "Hello from App Platform!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-test")
async def db_test():
    conn = await asyncpg.connect(DATABASE_URL)
    version = await conn.fetchval("SELECT version()")
    await conn.close()
    return {"postgres": version}
```

```text
# requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.32.0
asyncpg==0.30.0
```

```yaml
# .do/app.yaml
name: acme-api-mini
region: sgp

services:
  - name: api
    github:
      repo: acmeshop/api-mini
      branch: main
      deploy_on_push: true
    source_dir: /
    build_command: pip install -r requirements.txt
    run_command: uvicorn main:app --host 0.0.0.0 --port 8080
    http_port: 8080
    instance_count: 1
    instance_size_slug: apps-s-1vcpu-512mb
    health_check:
      http_path: /health
    routes:
      - path: /
    envs:
      - key: DATABASE_URL
        value: ${db.DATABASE_URL}

databases:
  - name: db
    engine: PG
    version: "17"
    production: false
    size: db-s-1vcpu-1gb
```

### Bước 2 — Push GitHub

```bash
git init
git add .
git commit -m "Initial FastAPI App Platform"
git remote add origin git@github.com:acmeshop/api-mini.git
git push -u origin main
```

### Bước 3 — Authorize DO + GitHub

```text
UI: Apps → Create App → GitHub → Authorize DO GitHub App
Select repo: acmeshop/api-mini
```

### Bước 4 — Deploy

```bash
# Từ CLI
doctl apps create --spec .do/app.yaml

# DO sẽ:
# 1. Provision Postgres dev (~3 phút)
# 2. Build container từ buildpack Python (~2 phút)
# 3. Deploy service
# 4. Issue Let's Encrypt cert
# 5. Public URL: acme-api-mini-xxxxx.ondigitalocean.app
```

### Bước 5 — Verify

```bash
# Get app URL
APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep acme-api-mini | awk '{print $1}')
URL=$(doctl apps get $APP_ID --format LiveURL --no-header)
echo $URL

curl $URL
# {"message":"Hello from App Platform!"}

curl $URL/db-test
# {"postgres":"PostgreSQL 17.0 ..."}
```

### Bước 6 — Push update → auto-redeploy

```bash
# Sửa main.py
sed -i '' 's/Hello/Xin chào/' main.py
git commit -am "VN greeting"
git push

# Wait ~3 phút
# DO clone → build → deploy mới → swap traffic zero-downtime

curl $URL
# {"message":"Xin chào from App Platform!"}
```

### Bước 7 — Custom domain

```bash
# Trong UI: App → Settings → Domains → Add Domain
# Domain: api.acmeshop.vn
# DO show CNAME target → bạn add ở DNS provider

# Sau 5-30 phút, DO issue Let's Encrypt cert, domain live HTTPS
```

→ **Kết quả**: API live HTTPS, auto-deploy mỗi commit, DB tự attach, zero ops.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. App Platform `port` không bind 0.0.0.0

**Bẫy**: Run command `uvicorn main:app --port 8080` (mặc định bind 127.0.0.1) → health check fail.

**Fix**: Luôn `--host 0.0.0.0 --port 8080`. App Platform inject `PORT` env var, dùng `--port $PORT` cho dynamic.

### 2. Quên expose port khớp config

**Bẫy**: `http_port: 8080` trong spec nhưng app listen 5000 → 502.

**Fix**: Match port chính xác. Hoặc dùng `$PORT` env var.

### 3. Build buildpack fail vì version Python sai

**Bẫy**: App cần Python 3.13 nhưng buildpack default 3.12.

**Fix**: Add `.python-version` hoặc `runtime.txt` (`python-3.13.0`) hoặc dùng Dockerfile.

### 4. App Platform secret leak qua log

**Bẫy**: `print(os.environ['SECRET_KEY'])` → log dashboard có secret.

**Fix**: Tag secret `type: SECRET` trong spec → DO masked trong log. App đừng log secret.

### 5. Functions cold start latency

**Bẫy**: Function chưa được gọi 5 phút → cold start lần sau 500-2000ms.

**Fix**:
- Keep warm: cron ping mỗi 4 phút.
- Hoặc dùng App Platform always-on cho latency-sensitive.

### 6. DOKS LB cost surprise

**Bẫy**: Tạo 5 `Service type=LoadBalancer` → 5 LB × $12 = $60 hidden.

**Fix**:
- Dùng **Ingress controller** (nginx-ingress, Traefik) → 1 LB serve nhiều domain.
- Hoặc consolidate Service.

### 7. Registry storage tích lũy

**Bẫy**: Push image mỗi commit → 1000 image × 500MB = 500GB → vượt tier.

**Fix**:
- Garbage collection policy (DO Registry built-in): keep latest 10 tags + prune cũ.
- CI clean tag cũ trước push.

### 8. App Platform region hạn chế cho DB attach

**Bẫy**: App ở `sgp` nhưng managed DB attach buộc region nào DO chọn → có thể cross-region latency.

**Fix**: App + DB cùng region. Verify `region` field trong spec.

### 9. Buildpack timeout 15 phút

**Bẫy**: Build phụ thuộc nặng (npm install ~20 phút trên slow tier) → fail.

**Fix**:
- Tier Pro build mạnh hơn.
- Cache dependency (App Platform có cache).
- Dùng Dockerfile multi-stage chia rõ.

### 10. `deploy_on_push` accidentally on main

**Bẫy**: Push trực tiếp lên `main` (bypass review) → production deploy bug.

**Fix**:
- Branch protection rules GitHub (require PR + review).
- Hoặc dùng staging branch trong spec, manual promote prod.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** App Platform khác Droplet ở điểm cốt lõi nào?

<details>
<summary>💡 Đáp án</summary>

- **Droplet**: IaaS, bạn quản OS, runtime, build, deploy, scaling.
- **App Platform**: PaaS, DO quản OS + runtime + build pipeline + HTTPS + scaling, bạn chỉ push code.

App Platform = "Heroku-on-DO". Trade-off: simple nhưng kém linh hoạt (không SSH, không custom kernel).

</details>

**Q2.** Khi nào chọn Functions thay vì App Platform Service?

<details>
<summary>💡 Đáp án</summary>

- Workload **intermittent** (vài lần / giờ) → Functions rẻ hơn (pay-per-invocation).
- Service **always-on** → App Platform luôn tính tiền dù không có traffic.
- Functions limit 15 phút runtime, cold start ~1s → không hợp WebSocket / latency-sensitive.

</details>

**Q3.** DOKS với 0 worker có cost không?

<details>
<summary>💡 Đáp án</summary>

Control plane **free**. Worker bill như Droplet. Nếu cluster có 0 worker → control plane $0, nhưng cluster không chạy gì.

Cost optimization: dùng cluster autoscaler `min-nodes=1, max-nodes=10` để off-peak chỉ 1 worker.

</details>

**Q4.** Load Balancer trước Droplet có lợi gì so SSL ở Droplet?

<details>
<summary>💡 Đáp án</summary>

1. **Multi-Droplet HA**: LB phân phối + health check, 1 Droplet chết → tự bypass.
2. **TLS termination at LB**: Droplet không cần cert, không phải renew.
3. **WAF integration**: dễ thêm Cloudflare đứng trước LB.
4. **Zero-downtime resize**: thay Droplet backend không downtime DNS.

Cost $12/tháng đáng giá cho production.

</details>

**Q5.** Migration path: từ Droplet single → App Platform khi nào?

<details>
<summary>💡 Đáp án</summary>

Migrate khi:
- Team ops nhỏ, không muốn quản OS.
- Đã có Dockerfile sẵn (App Platform dùng được).
- Cần auto-deploy mỗi commit.
- Không cần SSH OS để debug.

Không migrate khi:
- Cần process system custom (systemd unit, cron OS-level).
- Cần persistent local storage (App Platform ephemeral).
- DB self-host trên cùng Droplet (App Platform không cho).

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh |
|---|---|
| Tạo App | `doctl apps create --spec .do/app.yaml` |
| Update App | `doctl apps update APP_ID --spec .do/app.yaml` |
| Deploy trigger | `doctl apps create-deployment APP_ID` |
| Log runtime | `doctl apps logs APP_ID --type run --follow` |
| Log build | `doctl apps logs APP_ID --type build` |
| List app | `doctl apps list` |
| Functions deploy | `doctl serverless deploy .` |
| Functions invoke | `doctl serverless functions invoke pkg/fn` |
| Tạo DOKS | `doctl kubernetes cluster create NAME --region sgp1 --node-pool "..."` |
| Save kubeconfig | `doctl kubernetes cluster kubeconfig save NAME` |
| Tạo LB | `doctl compute load-balancer create --name N --droplet-ids ...` |
| Tạo Let's Encrypt cert | `doctl compute certificate create --type lets_encrypt --dns-names ...` |
| Tạo Registry | `doctl registry create NAME --subscription-tier basic` |
| Login Docker | `doctl registry login` |
| Push image | `docker push registry.digitalocean.com/NAME/IMG:TAG` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **App Platform** | (giữ nguyên) | PaaS DO, build từ Git auto |
| **PaaS** | Nền tảng dịch vụ | Platform-as-a-Service — DO lo runtime |
| **Buildpack** | (giữ nguyên) | Auto-detect stack, build image không cần Dockerfile |
| **App Spec** | Khai báo app | YAML mô tả app (services, jobs, DB, env) |
| **Service** | Dịch vụ | Long-running HTTP component |
| **Worker** | Tiến trình nền | Background process (no HTTP) |
| **Job** | Tác vụ | One-shot hoặc cron component |
| **Functions** | (giữ nguyên) | Serverless function của DO (OpenWhisk-based) |
| **DOKS** | (giữ nguyên) | DigitalOcean Kubernetes Service |
| **Control plane** | Tầng điều khiển | K8s master node — API, scheduler, etcd |
| **Worker node** | Nút công nhân | K8s node chạy Pod |
| **Cluster Autoscaler** | Tự co giãn cụm | Add/remove worker node theo load |
| **HPA** | Tự co giãn ngang | Horizontal Pod Autoscaler — scale Pod replica |
| **Load Balancer** | Cân tải | Phân phối request đến backend |
| **TLS termination** | Kết thúc TLS | LB decrypt HTTPS, gửi HTTP plain đến backend |
| **Container Registry** | Kho image | Private Docker registry |
| **Ingress** | Lối vào | K8s resource route HTTP đến Service |
| **Cold start** | Khởi động lạnh | Function lần đầu invoke chậm vì spawn container |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Managed Databases — Postgres / MySQL / Redis / MongoDB / Kafka](03_managed-databases.md)
- ↑ **Về cụm:** [DigitalOcean](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [Lambda + API Gateway — Nhập môn Serverless](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — so sánh serverless với AWS
- ☸️ [Kubernetes](../../../../10_devops/kubernetes/) — nền tảng đứng sau DOKS
- 🐳 [Docker](../../../../10_devops/docker/) — Dockerfile, image dùng cho App Platform và Registry
- 🐍 [FastAPI](../../../../07_web/backend/python-fastapi/) — stack mẫu trong phần hands-on

### 🌐 Tài nguyên tham khảo khác

- [DO App Platform docs](https://docs.digitalocean.com/products/app-platform/) — tài liệu gốc của App Platform.
- [App Spec reference](https://docs.digitalocean.com/products/app-platform/reference/app-spec/) — đặc tả đầy đủ file `app.yaml`.
- [DO Functions docs](https://docs.digitalocean.com/products/functions/) — hướng dẫn serverless Functions.
- [DOKS docs](https://docs.digitalocean.com/products/kubernetes/) — tài liệu Managed Kubernetes.
- [DO Load Balancer](https://docs.digitalocean.com/products/networking/load-balancers/) — cấu hình cân tải.
- [DO Container Registry](https://docs.digitalocean.com/products/container-registry/) — kho image private.
- [Cloud Native Buildpacks](https://buildpacks.io/) — cơ chế build image không cần Dockerfile.
- [DO vs Heroku vs Render](https://www.digitalocean.com/blog/app-platform-comparison) — so sánh các PaaS.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu. App Platform PaaS + App Spec YAML + Functions serverless + DOKS K8s + Load Balancer + Container Registry + Decision matrix Droplet/App-Platform/Functions/DOKS + hands-on FastAPI App Platform auto-deploy + 10 pitfalls.
- **v1.1.0 (01/06/2026)** — Sửa lỗi số liệu (App Platform "3 region" → 7 region khớp danh sách; Functions Max duration bỏ chú thích tự mâu thuẫn; viết lại câu so sánh EKS control plane cho rõ nghĩa). Đổi field metadata "Prerequisites" → "Yêu cầu trước"; chuẩn hoá header Glossary 3 cột; chuẩn hoá nav (⬅️/↑ + link-text theo tiêu đề H1 thực, 3 sub-heading chuẩn). Bổ sung ngôn ngữ `text` cho 3 fence thiếu; thêm lời dẫn trước các bảng và code block (đặc điểm App Platform, component, pricing, App Spec, Functions, DOKS, Load Balancer, Registry, decision matrix, hands-on) cho mạch đọc liền lạc.
