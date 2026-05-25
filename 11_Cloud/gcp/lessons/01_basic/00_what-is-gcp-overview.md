# ☁️ GCP — Tổng quan + account setup + gcloud CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** Đã xong [Cloud Fundamentals](../../../cloud-fundamentals/) ✅, hiểu Region/AZ/IaaS-PaaS-SaaS

> 🎯 *Bài đầu tiên của GCP cluster. Bạn đã hiểu cloud chung; giờ học **Google Cloud Platform** — vendor đứng top-3 (sau AWS, Azure). Bài này dạy: GCP là gì, services tier 1, account hierarchy (Org → Folder → Project), gcloud CLI setup, Free Tier, billing alert. Không deep từng service (bài 01-04 sẽ làm).*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **GCP khác AWS/Azure** ở điểm nào, vì sao chọn GCP
- [ ] Biết **20 services tier 1** của GCP và analog với AWS
- [ ] Tạo **GCP account** an toàn (MFA, billing alert, không leak key)
- [ ] Hiểu **Org → Folder → Project** hierarchy
- [ ] Cài đặt **gcloud CLI** + auth + config + multi-account
- [ ] Biết **Free Tier 2026** GCP cho gì
- [ ] Setup **Cloud IAM baseline** cho 1 user

---

## Tình huống — Bạn vừa được giao tài khoản GCP của công ty

Bạn vào company chat sáng thứ Hai:

> Sếp: *"Team backend mình đang trên AWS, nhưng dự án ML mới chạy trên GCP vì BigQuery + Vertex AI mạnh hơn. Bạn nhận account GCP rồi setup chuẩn nhé. Tuần sau deploy model."*

Bạn login GCP Console lần đầu → bị overwhelm:
- 100+ services trong dropdown.
- "Project" là gì? Sao mỗi resource phải nằm trong project?
- "Organization" có khác AWS "Account" không?
- gcloud CLI khác `aws` CLI sao?
- Billing setup ở đâu? Free Tier có những gì?
- Service account khác user account ra sao?

→ Bài này lấp đầy: GCP fundamentals + setup baseline secure + gcloud working.

---

## 1️⃣ GCP là gì, khác AWS/Azure thế nào

🪞 **Ẩn dụ**: *AWS như **siêu thị có 200 mặt hàng** — đa dạng, đôi khi rối; Azure như **bộ combo với Microsoft 365** — tiện cho doanh nghiệp Windows; GCP như **cửa hàng kỹ sư Google** — ít sản phẩm hơn nhưng tinh, network + data + AI là thế mạnh tuyệt đối.*

### Định nghĩa

**GCP** (Google Cloud Platform) = nhà cung cấp public cloud của Google, ra mắt 2008 (App Engine), mở rộng IaaS từ 2012 (Compute Engine). Hiện top-3 market share (~11% Q1 2026, sau AWS ~32% và Azure ~24%).

### Điểm mạnh GCP 2026

| Điểm mạnh | Vì sao | Ví dụ service |
|---|---|---|
| **Data + Analytics** | BigQuery serverless data warehouse vô địch | BigQuery, Dataflow, Pub/Sub, Looker |
| **AI / ML** | TPU custom chip + Vertex AI all-in-one | Vertex AI, AutoML, Gemini API, TPU |
| **Network** | Google global backbone — Tier 1 ISP | Cloud CDN, Network Service Tier Premium |
| **Kubernetes** | K8s sinh ra ở Google → GKE mature nhất | GKE Autopilot, Anthos |
| **Pricing** | Sustained-use discount + committed-use auto | CUDs lên tới 57% off |
| **Live migration** | Hot-migrate VM không downtime khi maintenance | Compute Engine |

### Điểm yếu / Trade-off

| Yếu | Hệ quả |
|---|---|
| Ít service hơn AWS (~150 vs 250+) | Niche workload thiếu lựa chọn |
| Vendor lock mạnh với BigQuery/Spanner | Migration khó |
| Documentation chất lượng không đều (so AWS) | Học mất thời gian hơn |
| Hỗ trợ Windows kém Azure | Stack Windows nên dùng Azure |
| Marketplace ecosystem nhỏ hơn AWS | Ít 3rd-party SaaS tích hợp sẵn |

### Khi nào chọn GCP

| Use case | Chọn GCP nếu |
|---|---|
| Data warehouse + analytics | Cần BigQuery serverless SQL on petabyte data |
| ML / AI production | Cần Vertex AI managed + TPU |
| Kubernetes-native stack | GKE Autopilot tốt nhất hiện tại |
| Container-first apps | Cloud Run = serverless container (Knative-based) |
| Multi-cloud strategy | Anthos để federate AWS+GCP+on-prem |
| Startup cost-sensitive | Free Tier + $300 trial credit rộng rãi |

---

## 2️⃣ GCP Services tier 1 (must-know)

Có hơn 150 services. **Tier 1** (cần biết ngay) = ~20 services chiếm 90% workload.

### Compute (chạy code)

| Service | Mô tả | Analog AWS | Khi dùng |
|---|---|---|---|
| **Compute Engine (GCE)** | VM truyền thống | EC2 | Lift-and-shift, custom OS, GPU workload |
| **Cloud Run** | Serverless container (Knative) | Lambda/Fargate hybrid | Container ngắn-trung hạn, scale to zero |
| **Cloud Functions** | Serverless function | Lambda | Event-driven, < 60 phút runtime |
| **GKE** (Kubernetes Engine) | Managed K8s | EKS | Microservices, K8s-native team |
| **App Engine** | PaaS truyền thống (legacy) | Elastic Beanstalk | Project cũ; new project dùng Cloud Run |

### Storage (lưu trữ)

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Cloud Storage (GCS)** | Object storage | S3 |
| **Persistent Disk (PD)** | Block storage cho VM | EBS |
| **Filestore** | Managed NFS | EFS |
| **Local SSD** | NVMe ephemeral cho VM | Instance Store |

### Database

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Cloud SQL** | Managed Postgres/MySQL/SQL Server | RDS |
| **Cloud Spanner** | Globally distributed SQL | Aurora Global (kém hơn nhiều) |
| **Firestore** | Managed NoSQL document | DynamoDB document mode |
| **Bigtable** | Wide-column NoSQL | DynamoDB (key-value) |
| **BigQuery** | Serverless data warehouse | Redshift (nhưng BigQuery superior) |
| **Memorystore** | Managed Redis/Memcached | ElastiCache |

### Network

| Service | Mô tả | Analog AWS |
|---|---|---|
| **VPC** | Virtual private cloud (global, không region-bound như AWS) | VPC |
| **Cloud Load Balancing** | Global L4/L7 LB | ELB |
| **Cloud CDN** | CDN trên Google backbone | CloudFront |
| **Cloud DNS** | Managed DNS | Route 53 |
| **Cloud Armor** | WAF + DDoS protection | AWS WAF + Shield |

### Identity, security, ops

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Cloud IAM** | Permission management | IAM |
| **Secret Manager** | Secret storage | Secrets Manager |
| **Cloud KMS** | Key management | KMS |
| **Cloud Logging** | Log aggregation | CloudWatch Logs |
| **Cloud Monitoring** | Metric + alert | CloudWatch Metrics |
| **Cloud Trace** | Distributed tracing | X-Ray |

### Data & AI

| Service | Mô tả | Analog AWS |
|---|---|---|
| **BigQuery** | Data warehouse | Redshift |
| **Dataflow** | Stream/batch processing (Apache Beam) | Kinesis Data Analytics + EMR |
| **Pub/Sub** | Messaging queue (global) | SNS+SQS combined |
| **Vertex AI** | Managed ML platform | SageMaker |
| **Gemini API** | LLM API | Bedrock |

→ **Học bài 01-04** cluster basic: GCE+PD, GCS+IAM, Cloud SQL+Firestore, Cloud Functions+Cloud Run.

---

## 3️⃣ Resource hierarchy — Org → Folder → Project → Resource

GCP **không có khái niệm "Account" duy nhất** như AWS. Thay vào đó:

```
Organization (gắn với Google Workspace / Cloud Identity domain)
├── Folder: "Engineering"
│   ├── Folder: "Backend"
│   │   ├── Project: "acmeshop-prod"
│   │   │   ├── VM "web-1"
│   │   │   ├── GCS bucket "acmeshop-uploads"
│   │   │   └── Cloud SQL "acmeshop-db"
│   │   └── Project: "acmeshop-staging"
│   └── Folder: "Data"
│       └── Project: "acmeshop-analytics"
└── Folder: "Sandbox"
    └── Project: "thien-le-sandbox"
```

### Các level

| Level | Mô tả | Tương đương AWS |
|---|---|---|
| **Organization** | Top-level — gắn với domain (acmeshop.vn) | AWS Organization |
| **Folder** | Group projects logic (theo team/env) | AWS OU |
| **Project** | Đơn vị **quản lý billing + IAM + resource** | AWS Account |
| **Resource** | VM, bucket, DB cụ thể | (same) |

### Vì sao "Project" là đơn vị chính

- **Billing**: mỗi project gắn 1 billing account (có thể share).
- **IAM**: permission inherit Org → Folder → Project → Resource.
- **Isolation**: resource giữa project tách biệt (giống AWS Account).
- **Quotas**: quota tính per project.

→ **Thực hành**: tạo 1 project riêng cho mỗi `<service>-<env>` (e.g., `acmeshop-prod`, `acmeshop-staging`, `acmeshop-dev`).

---

## 4️⃣ Tạo GCP account + secure baseline

### Bước 1 — Tạo account

1. Truy cập [cloud.google.com](https://cloud.google.com) → "Get started for free".
2. Đăng nhập bằng Google account (hoặc tạo mới).
3. Cung cấp credit card (verify, không charge nếu trong Free Tier).
4. Nhận **$300 trial credit** + 90 ngày sử dụng.

### Bước 2 — Bật MFA cho Google account

**Bắt buộc** trước khi làm gì khác:
1. Settings → Security → 2-Step Verification → Enable.
2. Dùng **Authenticator app** (Google Authenticator, Authy) — **không** dùng SMS.
3. Backup codes lưu offline.

### Bước 3 — Tạo Organization (nếu có domain công ty)

- Nếu dùng Google Workspace → Organization tự tạo.
- Nếu cá nhân (`@gmail.com`) → không có Org, chỉ có **Project**.
- Cá nhân muốn có Org: dùng **Cloud Identity Free** (không cần Workspace).

### Bước 4 — Setup billing alert

```bash
# Trong GCP Console:
# Billing → Budgets & alerts → Create budget
# - Set budget: $20/tháng (sandbox)
# - Alert at: 50%, 90%, 100%, 120%
# - Email: your-email + Slack webhook (optional)
```

**Quan trọng**: GCP **không tự tắt** service khi over budget. Alert chỉ cảnh báo. Phải có **kill switch** (Cloud Function) nếu muốn cap cứng.

### Bước 5 — Bật Cloud Audit Logs

```bash
# Logging → Logs Router → đảm bảo "_Default" sink active
# Audit log Admin Activity = always-on (free)
# Data Access log = optional, tính phí — bật cho service quan trọng
```

### Bước 6 — Không bao giờ dùng tài khoản root cho daily work

- Tài khoản **Org Admin** (Organization Administrator) chỉ dùng để setup ban đầu.
- Tạo **Project IAM Admin** + **Project Editor** cho daily work.
- Service account dùng cho automation, **không** dùng user account.

---

## 5️⃣ gcloud CLI — Cài đặt + auth + config

### Cài đặt

```bash
# macOS
brew install --cask google-cloud-sdk

# Linux (Debian/Ubuntu)
sudo apt install google-cloud-cli

# Windows
# Tải installer từ cloud.google.com/sdk/docs/install-sdk

# Verify
gcloud --version
```

### Auth — User account (interactive)

```bash
# Login (mở browser)
gcloud auth login

# Application Default Credentials (cho SDK)
gcloud auth application-default login

# List accounts active
gcloud auth list

# Switch account
gcloud config set account thien.le@acmeshop.vn
```

### Auth — Service account (CI/CD)

```bash
# Tạo service account
gcloud iam service-accounts create ci-deployer \
    --display-name "CI Deployer" \
    --project acmeshop-prod

# Tạo key (LƯU Ý: key file = secret, không commit Git)
gcloud iam service-accounts keys create ~/secrets/ci-deployer.json \
    --iam-account ci-deployer@acmeshop-prod.iam.gserviceaccount.com

# Auth bằng key
gcloud auth activate-service-account --key-file=~/secrets/ci-deployer.json
```

→ **Best practice 2026**: dùng **Workload Identity Federation** (WIF) cho CI/CD thay vì JSON key — không cần lưu key file, GCP trust GitHub Actions/GitLab OIDC token trực tiếp.

### Config — Multi-project setup

```bash
# Config "default" cho work
gcloud config configurations create work
gcloud config set account thien.le@acmeshop.vn
gcloud config set project acmeshop-prod
gcloud config set compute/region asia-southeast1
gcloud config set compute/zone asia-southeast1-a

# Config "sandbox" cho personal
gcloud config configurations create sandbox
gcloud config set account thien.le@gmail.com
gcloud config set project thien-le-sandbox

# Switch
gcloud config configurations activate work
gcloud config list
```

### Common commands

```bash
# List projects
gcloud projects list

# Set default project
gcloud config set project acmeshop-prod

# List VMs trong project
gcloud compute instances list

# List buckets
gcloud storage buckets list

# Open Console URL trong browser
gcloud cloud-shell scp --help
```

---

## 6️⃣ Free Tier 2026 — Cái gì free

GCP Free Tier có **2 phần**:

### A. $300 trial credit (90 ngày)

- 1 lần duy nhất per billing account.
- Dùng cho mọi service, mọi region.
- Hết 90 ngày hoặc hết $300 → ngừng (không charge nếu chưa upgrade).

### B. Always Free (sau trial)

| Service | Hạn mức always free |
|---|---|
| Compute Engine | 1 `e2-micro` VM tại US (`us-west1`, `us-central1`, `us-east1`) |
| Cloud Storage | 5 GB regional storage tại US, 5000 Class A op/tháng |
| Cloud Run | 2 triệu request/tháng, 360k GB-s memory |
| Cloud Functions | 2 triệu invocation/tháng |
| Cloud Pub/Sub | 10 GB messages/tháng |
| Cloud Build | 120 build-minutes/ngày |
| BigQuery | 1 TB query/tháng, 10 GB storage |
| Firestore | 1 GB storage, 50k read/20k write/20k delete per ngày |
| Logging | 50 GB ingestion/tháng |
| Monitoring | First 150 MB metric ingestion |

→ **Free Tier đủ học + cá nhân project nhỏ**. Đừng nhầm với AWS Free Tier (12-month).

---

## 7️⃣ Cloud IAM cơ bản

🪞 **Ẩn dụ**: *Cloud IAM như **hệ thống vé vào nhà máy** — Identity (ai) cầm vé + Role (vai trò) + Resource (vào khu nào). Permission luôn theo **Principle of Least Privilege** — vé chỉ cho vào đúng khu cần làm.*

### Khái niệm

| Khái niệm | Mô tả |
|---|---|
| **Identity** (Member, Principal) | User, Group, Service Account, Workforce Identity |
| **Role** | Bundle permissions (e.g., `roles/storage.objectViewer`) |
| **Resource** | VM, bucket, project, ... |
| **Binding** | (Identity, Role, Resource) tuple |
| **Policy** | List of bindings cho 1 resource |

### Role types

| Type | Mô tả | Ví dụ |
|---|---|---|
| **Primitive (basic)** | Cũ — Owner/Editor/Viewer toàn project | `roles/owner` |
| **Predefined** | Granular per service | `roles/storage.objectAdmin` |
| **Custom** | Tự tạo permission list | Khi predefined không vừa |

→ **2026 best practice**: **Không dùng** primitive role; luôn predefined hoặc custom.

### Ví dụ — Grant role

```bash
# Grant user quyền view buckets
gcloud projects add-iam-policy-binding acmeshop-prod \
    --member="user:thien.le@acmeshop.vn" \
    --role="roles/storage.objectViewer"

# Grant service account quyền deploy Cloud Run
gcloud projects add-iam-policy-binding acmeshop-prod \
    --member="serviceAccount:ci-deployer@acmeshop-prod.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# View IAM policy của project
gcloud projects get-iam-policy acmeshop-prod
```

---

## 🛠️ Hands-on — Setup GCP account secure + first VM

### Mục tiêu

Bạn tạo account GCP, setup baseline, deploy 1 VM `e2-micro` (free tier), SSH vào.

### Bước 1 — Tạo account + Project

1. Tạo Google account (nếu chưa).
2. Vào [console.cloud.google.com](https://console.cloud.google.com).
3. Nhận $300 trial credit.
4. Tạo project mới: tên `acmeshop-sandbox` (ID phải unique global).

### Bước 2 — Cài gcloud + auth

```bash
brew install --cask google-cloud-sdk
gcloud auth login
gcloud config set project acmeshop-sandbox
gcloud auth application-default login
```

### Bước 3 — Bật billing + budget alert

```bash
# Trong Console:
# Billing → Link a billing account
# Budgets → New budget $10/tháng, alert 50/90/100%
```

### Bước 4 — Tạo VM e2-micro (free tier)

```bash
# Tạo VM
gcloud compute instances create acmeshop-test \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --tags=http-server,https-server

# SSH vào
gcloud compute ssh acmeshop-test --zone=us-central1-a

# Trong VM:
echo "Hello from GCP!" > /tmp/hello.txt
cat /tmp/hello.txt
exit

# Cleanup (tránh charge)
gcloud compute instances delete acmeshop-test --zone=us-central1-a --quiet
```

### Bước 5 — Setup multi-account config

```bash
# Config cho work
gcloud config configurations create work
gcloud config set account work-email@company.com
gcloud config set project work-prod

# Config cho sandbox
gcloud config configurations create sandbox
gcloud config set account thien.le@gmail.com
gcloud config set project acmeshop-sandbox

# Switch
gcloud config configurations activate sandbox
```

→ **Kết quả**: account hoạt động, gcloud setup, VM deploy thử thành công, billing alert active.

---

## ⚠️ Pitfalls — Bẫy phổ biến của người mới

### 1. Để service account key file leak

**Bẫy**: Tạo SA key JSON → commit vào Git repo → push public.

**Hậu quả**: Crypto miner exploit trong 1-2 giờ. $1000-10000 bill.

**Fix**:
- **Không bao giờ commit** key JSON file.
- Dùng `gitleaks` hook check trước khi commit.
- Tốt hơn: **Workload Identity Federation** — không cần key file.

### 2. Quên cleanup VM/bucket trial

**Bẫy**: Tạo VM `n2-highmem-32` để test → quên xóa → cuối tháng $500 bill.

**Fix**:
- Tag mọi resource: `env=sandbox,owner=thien-le`.
- Set **billing budget alert** + Cloud Function tắt VM khi over.
- Daily reminder cron: `gcloud compute instances list` để kiểm tra.

### 3. Project ID nhầm

**Bẫy**: Project có 2 thứ — **Project Name** (display) và **Project ID** (immutable, unique global). Lệnh gcloud dùng **ID**, không phải Name.

**Fix**:
- Đặt ID rõ: `acmeshop-prod-2026`, không `my-project-1234`.
- Luôn `gcloud config set project <ID>` đầu session.

### 4. Region/Zone nhầm

**Bẫy**: VM ở `us-central1-a`, bucket ở `asia-southeast1` → latency cao + egress fee.

**Fix**:
- Set default region/zone trong config.
- Resource liên quan đặt cùng region.

### 5. Primitive role `Editor` cho tất cả

**Bẫy**: Granted `roles/editor` cho dev team → ai cũng có thể delete production DB.

**Fix**:
- Dùng **predefined role** granular: `roles/cloudsql.viewer`, `roles/storage.objectAdmin`.
- Test với `gcloud auth login --impersonate-service-account` xem permission đủ chưa.

### 6. Dùng Org Admin cho daily work

**Bẫy**: Account Org Admin (full power) bị compromise → cả Organization bị wipe.

**Fix**:
- Org Admin chỉ setup ban đầu.
- Daily: tài khoản với role giới hạn.
- Org Admin yêu cầu hardware key (YubiKey).

### 7. Không bật Audit Log Data Access

**Bẫy**: Admin Activity log bật mặc định, nhưng **Data Access log** (ai đọc bucket nào) phải bật thủ công → forensic không truy được.

**Fix**:
- Bật Data Access cho service có data nhạy cảm (GCS bucket chứa PII, BigQuery dataset).
- Lưu ý: Data Access log **tính phí ingest**.

### 8. Mở `0.0.0.0/0` firewall

**Bẫy**: VPC firewall rule allow `0.0.0.0/0` port 22 → ssh brute-force từ Internet.

**Fix**:
- Dùng **IAP (Identity-Aware Proxy) tunnel** cho SSH: `gcloud compute ssh --tunnel-through-iap`.
- Firewall chỉ allow IP range biết.

---

## 🎯 Self-check

- [ ] Mô tả 3 service tier 1 của GCP cho mỗi nhóm (compute/storage/database/network)?
- [ ] Vẽ sơ đồ Org → Folder → Project → Resource cho công ty bạn?
- [ ] Tạo gcloud config riêng cho work vs sandbox?
- [ ] Tạo 1 VM e2-micro free tier, SSH vào, rồi delete?
- [ ] Setup billing budget alert $10/tháng?
- [ ] Giải thích vì sao **không dùng** primitive role `Editor`?
- [ ] Liệt kê 3 cách Workload Identity Federation tốt hơn JSON key?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **GCP** | Google Cloud Platform |
| **Project** | Đơn vị quản lý billing + IAM + resource (analog AWS Account) |
| **Organization** | Top-level container, gắn domain Google Workspace |
| **Folder** | Group projects logic (analog AWS OU) |
| **gcloud CLI** | CLI chính của GCP |
| **Service Account** | Identity cho application/automation (không phải user) |
| **WIF** | Workload Identity Federation — auth không cần key file |
| **IAM** | Identity and Access Management |
| **Role** | Bundle permissions |
| **Predefined Role** | Role granular per service (`roles/storage.objectViewer`) |
| **Primitive Role** | Role cũ rộng (Owner/Editor/Viewer) — **không khuyến nghị** |
| **GCE** | Google Compute Engine — VM service |
| **GCS** | Google Cloud Storage — object storage |
| **GKE** | Google Kubernetes Engine |
| **BigQuery** | Serverless data warehouse, query SQL trên petabyte |
| **Pub/Sub** | Global messaging service |
| **Cloud Run** | Serverless container (Knative) |
| **Free Tier** | Always free + $300 trial 90 ngày |
| **IAP** | Identity-Aware Proxy — SSH/HTTP qua Google identity |
| **CUD** | Committed Use Discount — cam kết 1-3 năm, giảm tới 57% |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- → Tiếp: [01_compute-engine-and-disks.md](01_compute-engine-and-disks.md) *(sắp viết)*
- ↑ Cluster GCP: [GCP README](../../README.md)
- ↶ Cloud Fundamentals: [11_Cloud/cloud-fundamentals](../../../cloud-fundamentals/)

### Cross-reference
- ☁️ [AWS basic](../../../aws/) — so sánh service analog
- ☁️ [Azure basic](../../../azure/) — vendor #2 thứ 3
- 🏗️ [IaC Terraform](../../../../10_DevOps/iac/) — Terraform GCP provider
- 🧭 [Cloud Engineer roadmap](../../../../00_Roadmaps/career/cloud-engineer_career-roadmap.md)

### Tài nguyên ngoài (2026)
- 📖 [GCP docs](https://cloud.google.com/docs)
- 📖 [gcloud CLI reference](https://cloud.google.com/sdk/gcloud/reference)
- 📖 [GCP Free Tier](https://cloud.google.com/free)
- 📖 [Pricing Calculator](https://cloud.google.com/products/calculator)
- 📖 [Cloud Skills Boost](https://www.cloudskillsboost.google/) — official Google courses (Qwiklabs)
- 📖 [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- 📖 [GCP Professional Cloud Architect cert](https://cloud.google.com/certification/cloud-architect)
- 📖 [Workload Identity Federation guide](https://cloud.google.com/iam/docs/workload-identity-federation)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 00 cluster GCP basic. Overview GCP + so sánh AWS/Azure + 20 services tier 1 + Org→Folder→Project hierarchy + gcloud setup + Free Tier 2026 + IAM cơ bản + hands-on tạo VM + 8 pitfalls. Pattern theo AWS lesson 00.
