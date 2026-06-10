# ☁️ GCP — Tổng quan + account setup + gcloud CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Đã xong [Cloud Fundamentals](../../../cloud-fundamentals/) ✅, hiểu Region/AZ và mô hình IaaS/PaaS/SaaS.

> [!NOTE]
> **Mục tiêu bài học:**\
> Đây là bài mở màn của cụm GCP. Bạn đã nắm cloud nói chung ở cụm Cloud Fundamentals; giờ mình cùng bước vào **Google Cloud Platform** — nhà cung cấp đứng top-3 (sau AWS và Azure). Bài này trả lời: GCP là gì và mạnh ở đâu, đâu là nhóm dịch vụ phải biết ngay, cách tổ chức tài khoản theo mô hình *Org → Folder → Project*, cách cài và cấu hình *gcloud CLI*, Free Tier 2026 cho những gì, và cách dựng một baseline IAM an toàn. Bài này tập trung vào bức tranh tổng thể và setup nền móng; mình sẽ đào sâu từng dịch vụ ở các bài 01–04.

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **GCP khác AWS/Azure** ở điểm nào, và vì sao có lúc nên chọn GCP.
- [ ] Biết **~20 dịch vụ tier 1** của GCP và service tương đương bên AWS.
- [ ] Tạo **GCP account** an toàn (MFA, billing alert, không leak key).
- [ ] Hiểu mô hình phân cấp **Org → Folder → Project**.
- [ ] Cài đặt **gcloud CLI** + auth + config + multi-account.
- [ ] Biết **Free Tier 2026** của GCP cho những gì.
- [ ] Dựng được **Cloud IAM baseline** cho một user.

---

## ☁️ Sáng thứ Hai: bạn được giao tài khoản GCP của công ty

Bạn vừa mở company chat đầu tuần thì nhận được tin nhắn từ sếp:

> *"Team backend mình đang chạy trên AWS, nhưng dự án ML mới sẽ làm trên GCP vì BigQuery và Vertex AI mạnh hơn hẳn. Bạn nhận tài khoản GCP rồi setup chuẩn giúp nhé. Tuần sau là phải deploy model rồi đấy."*

Bạn hồ hởi login vào GCP Console lần đầu, rồi... choáng. Một loạt câu hỏi ập đến mà chưa có lời giải:

- Cái dropdown dịch vụ có hơn 100 mục, biết bắt đầu từ đâu?
- "Project" là gì, sao mọi resource bắt buộc phải nằm trong một project?
- "Organization" của GCP có giống "Account" bên AWS không?
- `gcloud` CLI khác `aws` CLI ra sao?
- Billing setup ở đâu, Free Tier có những gì?
- Service account khác user account chỗ nào?

Cảm giác y hệt lần đầu bạn mở một codebase khổng lồ mà không có bản đồ. Bài này chính là tấm bản đồ đó: nó lấp đầy phần nền tảng GCP, giúp bạn dựng một baseline an toàn và có `gcloud` chạy được trong tay.

---

## 1️⃣ GCP là gì, và khác AWS/Azure thế nào?

Trước khi liệt kê tính năng, hãy định vị GCP trong bức tranh ba ông lớn. Cách dễ hình dung nhất là so ba nhà cung cấp như ba kiểu cửa hàng khác nhau.

> [!NOTE]
> **Ẩn dụ:**\
> AWS giống một **siêu thị 200 mặt hàng** — cái gì cũng có, đa dạng đến mức đôi khi rối. Azure giống **bộ combo đi kèm Microsoft 365** — cực tiện cho doanh nghiệp đã quen hệ sinh thái Windows. Còn GCP giống **cửa hàng của dân kỹ sư Google** — ít sản phẩm hơn nhưng tinh, và ở ba mảng *network*, *data*, *AI* thì gần như vô đối.

Với hình dung đó, ta đi vào định nghĩa chính xác để biết mình đang nói về cái gì.

### Định nghĩa

**GCP** (Google Cloud Platform) là nền tảng public cloud của Google, ra mắt năm 2008 với App Engine và mở rộng sang *IaaS* (hạ tầng cho thuê dạng máy ảo) từ 2012 với Compute Engine. Hiện GCP đứng top-3 thị phần (khoảng 11% trong Q1 2026, sau AWS ~32% và Azure ~24%).

Đã biết GCP là ai, câu hỏi tiếp theo của một kỹ sư luôn là: nó *mạnh* ở đâu để mình chọn nó thay vì hai đối thủ? Bảng dưới gom các thế mạnh thực chiến của GCP năm 2026.

| Điểm mạnh | Vì sao | Ví dụ service |
|---|---|---|
| **Data + Analytics** | BigQuery serverless data warehouse gần như vô địch | BigQuery, Dataflow, Pub/Sub, Looker |
| **AI / ML** | TPU (chip AI tự thiết kế) + Vertex AI all-in-one | Vertex AI, AutoML, Gemini API, TPU |
| **Network** | Google sở hữu global backbone — hạ tầng Tier 1 ISP | Cloud CDN, Network Service Tier Premium |
| **Kubernetes** | K8s sinh ra ở Google → GKE trưởng thành nhất | GKE Autopilot, Anthos |
| **Pricing** | Sustained-use discount + committed-use tự động | CUDs giảm tới 57% |
| **Live migration** | Hot-migrate VM không downtime khi máy chủ bảo trì | Compute Engine |

Đọc bảng trên dễ thấy GCP "lệch" hẳn về data, AI và Kubernetes — đúng với gốc gác kỹ thuật của Google. Nhưng không có nền tảng nào hoàn hảo; phần tiếp theo nói thẳng những điểm yếu để bạn ra quyết định tỉnh táo.

### Điểm yếu / Trade-off

Mọi lựa chọn kỹ thuật đều là sự đánh đổi. Dưới đây là những chỗ GCP còn thua, kèm hệ quả thực tế bạn sẽ gặp:

| Điểm yếu | Hệ quả |
|---|---|
| Ít service hơn AWS (~150 so với 250+) | Workload niche đôi khi thiếu lựa chọn |
| Vendor lock mạnh với BigQuery/Spanner | Di chuyển đi nơi khác (migration) khó |
| Chất lượng tài liệu không đều (so với AWS) | Tự học mất thời gian hơn |
| Hỗ trợ Windows kém Azure | Stack Windows nên cân nhắc Azure |
| Hệ sinh thái Marketplace nhỏ hơn AWS | Ít SaaS bên thứ ba tích hợp sẵn |

Tóm lại: GCP không phải lựa chọn mặc định cho *mọi* bài toán. Nó tỏa sáng ở một số kịch bản cụ thể — và đó chính là lúc nên chọn nó.

### Khi nào chọn GCP

Để biến phân tích trên thành quyết định, đây là các use case mà GCP thực sự là lựa chọn tốt nhất:

| Use case | Chọn GCP nếu |
|---|---|
| Data warehouse + analytics | Cần BigQuery serverless chạy SQL trên dữ liệu cỡ petabyte |
| ML / AI production | Cần Vertex AI managed + TPU |
| Stack Kubernetes-native | GKE Autopilot đang tốt nhất hiện tại |
| App container-first | Cloud Run = serverless container (nền Knative) |
| Chiến lược multi-cloud | Anthos để liên kết AWS + GCP + on-prem |
| Startup nhạy cảm chi phí | Free Tier + $300 trial credit khá rộng rãi |

Đã định vị xong GCP trong bức tranh lớn, giờ ta phóng to vào "kệ hàng" — những dịch vụ cụ thể bạn sẽ chạm tay vào mỗi ngày.

---

## 2️⃣ Các dịch vụ tier 1 (phải biết trước)

GCP có hơn 150 dịch vụ, nhưng bạn không cần học hết. Mình gọi nhóm cần biết ngay là **tier 1** — khoảng 20 dịch vụ gánh tới 90% workload thực tế. Để dễ nhớ, mình nhóm chúng theo chức năng và luôn ghi kèm service tương đương bên AWS (vì rất nhiều người đến GCP từ nền AWS).

### Compute — nơi chạy code

Đây là nhóm trả lời câu hỏi "code của mình chạy ở đâu". Từ VM truyền thống đến serverless, mỗi lựa chọn hợp với một kiểu workload khác nhau:

| Service | Mô tả | Tương đương AWS | Khi dùng |
|---|---|---|---|
| **Compute Engine (GCE)** | VM truyền thống | EC2 | Lift-and-shift, custom OS, workload GPU |
| **Cloud Run** | Serverless container (Knative) | Lambda/Fargate hybrid | Container ngắn–trung hạn, scale về 0 |
| **Cloud Functions** | Serverless function | Lambda | Event-driven, runtime < 60 phút |
| **GKE** (Kubernetes Engine) | Managed K8s | EKS | Microservices, team quen K8s |
| **App Engine** | PaaS đời đầu (legacy) | Elastic Beanstalk | Dự án cũ; dự án mới nên dùng Cloud Run |

### Storage — nơi lưu trữ

Sau khi có chỗ chạy code, dữ liệu phải nằm ở đâu đó. GCP chia storage theo kiểu truy cập — object, block, file:

| Service | Mô tả | Tương đương AWS |
|---|---|---|
| **Cloud Storage (GCS)** | Object storage | S3 |
| **Persistent Disk (PD)** | Block storage gắn vào VM | EBS |
| **Filestore** | Managed NFS | EFS |
| **Local SSD** | NVMe ephemeral cho VM | Instance Store |

### Database

Khi cần lưu dữ liệu có cấu trúc, GCP cho bạn dải lựa chọn từ SQL truyền thống tới NoSQL và data warehouse. Lưu ý hai cái tên đắt giá: Spanner (SQL phân tán toàn cầu) và BigQuery (data warehouse serverless):

| Service | Mô tả | Tương đương AWS |
|---|---|---|
| **Cloud SQL** | Managed Postgres/MySQL/SQL Server | RDS |
| **Cloud Spanner** | SQL phân tán toàn cầu | Aurora Global (kém hơn nhiều) |
| **Firestore** | Managed NoSQL dạng document | DynamoDB (document mode) |
| **Bigtable** | NoSQL wide-column | DynamoDB (key-value) |
| **BigQuery** | Serverless data warehouse | Redshift (BigQuery vượt trội hơn) |
| **Memorystore** | Managed Redis/Memcached | ElastiCache |

### Network

Đây là sân nhà của Google: VPC của GCP là *global* (không bị bó trong một region như AWS), còn CDN và load balancer chạy trên chính backbone của Google:

| Service | Mô tả | Tương đương AWS |
|---|---|---|
| **VPC** | Virtual private cloud (global, không bó theo region như AWS) | VPC |
| **Cloud Load Balancing** | Load balancer global L4/L7 | ELB |
| **Cloud CDN** | CDN chạy trên Google backbone | CloudFront |
| **Cloud DNS** | Managed DNS | Route 53 |
| **Cloud Armor** | WAF + chống DDoS | AWS WAF + Shield |

### Identity, security, ops — danh tính, bảo mật, vận hành

Nhóm này lo phần "ai được làm gì" và "khi có sự cố thì nhìn vào đâu" — IAM, quản lý secret/key, log, metric, tracing:

| Service | Mô tả | Tương đương AWS |
|---|---|---|
| **Cloud IAM** | Quản lý quyền (permission) | IAM |
| **Secret Manager** | Lưu trữ secret | Secrets Manager |
| **Cloud KMS** | Quản lý khóa mã hóa | KMS |
| **Cloud Logging** | Tổng hợp log | CloudWatch Logs |
| **Cloud Monitoring** | Metric + alert | CloudWatch Metrics |
| **Cloud Trace** | Distributed tracing (theo dấu request qua nhiều service) | X-Ray |

### Data & AI

Cuối cùng là nhóm làm nên danh tiếng GCP — xử lý dữ liệu lớn và machine learning ở quy mô production:

| Service | Mô tả | Tương đương AWS |
|---|---|---|
| **BigQuery** | Data warehouse | Redshift |
| **Dataflow** | Xử lý stream/batch (Apache Beam) | Kinesis Data Analytics + EMR |
| **Pub/Sub** | Hàng đợi messaging (global) | SNS + SQS gộp lại |
| **Vertex AI** | Nền tảng ML managed | SageMaker |
| **Gemini API** | API mô hình ngôn ngữ lớn (LLM) | Bedrock |

Bạn không cần thuộc lòng cả bảng. Cụm basic này (bài 01–04) sẽ thực hành sâu năm dịch vụ cốt lõi nhất: GCE + PD, GCS + IAM, Cloud SQL + Firestore, rồi Cloud Functions + Cloud Run. Các tên còn lại cứ để mắt tới khi gặp.

Biết được "có những món gì" rồi, câu hỏi tiếp theo là: các món đó được *xếp* vào đâu? Đó là lúc cần hiểu mô hình phân cấp tài nguyên của GCP.

---

## 3️⃣ Mô hình phân cấp — Org → Folder → Project → Resource

Đây là chỗ khiến dân AWS bối rối nhất khi qua GCP. GCP **không có một "Account" duy nhất** như AWS. Thay vào đó, mọi thứ được tổ chức thành một cây phân cấp, và đơn vị trung tâm là *Project*. Hãy nhìn một cây mẫu của công ty `acmeshop` để hình dung:

```text
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

Cây trên có bốn tầng. Để dịch sang ngôn ngữ AWS quen thuộc, bảng này ánh xạ từng tầng:

| Level | Mô tả | Tương đương AWS |
|---|---|---|
| **Organization** | Tầng cao nhất — gắn với domain (acmeshop.vn) | AWS Organization |
| **Folder** | Nhóm các project theo logic (team/env) | AWS OU |
| **Project** | Đơn vị **quản lý billing + IAM + resource** | AWS Account |
| **Resource** | VM, bucket, DB cụ thể | (giống nhau) |

Điểm mấu chốt phải khắc cốt ghi tâm: **Project mới là đơn vị làm việc chính**, chứ không phải Organization. Bốn lý do khiến Project quan trọng đến vậy:

- **Billing**: mỗi project gắn với một billing account (có thể chia sẻ chung).
- **IAM**: quyền được kế thừa theo chiều Org → Folder → Project → Resource.
- **Isolation**: resource giữa các project tách biệt nhau (giống cách AWS Account cô lập).
- **Quotas**: hạn mức (quota) được tính riêng theo từng project.

Từ đó suy ra một thói quen tốt: tạo một project riêng cho mỗi cặp `<service>-<env>`, ví dụ `acmeshop-prod`, `acmeshop-staging`, `acmeshop-dev`. Cách này giữ billing và quyền hạn tách bạch, tránh việc một sai sót ở dev lan sang prod.

Hiểu được cấu trúc, giờ ta bắt tay dựng nó: tạo account và khóa chặt baseline bảo mật ngay từ đầu.

---

## 4️⃣ Tạo GCP account + baseline an toàn

Nguyên tắc của mình: setup bảo mật *trước*, nghịch dịch vụ *sau*. Một tài khoản cloud bị lộ có thể ngốn của bạn hàng nghìn đô chỉ trong vài giờ, nên sáu bước dưới đây làm theo đúng thứ tự.

### Bước 1 — Tạo account

Bắt đầu từ việc đăng ký và nhận khoản credit dùng thử:

1. Truy cập [cloud.google.com](https://cloud.google.com) → "Get started for free".
2. Đăng nhập bằng Google account (hoặc tạo mới).
3. Cung cấp credit card (chỉ để verify, không bị charge nếu còn trong Free Tier).
4. Nhận **$300 trial credit** + 90 ngày sử dụng.

### Bước 2 — Bật MFA cho Google account

Đây là việc **bắt buộc làm trước khi đụng tới bất kỳ thứ gì khác**. Tài khoản Google chính là chìa khóa vào toàn bộ cloud của bạn:

1. Settings → Security → 2-Step Verification → Enable.
2. Dùng **Authenticator app** (Google Authenticator, Authy) — **không** dùng SMS.
3. Lưu backup codes ở chỗ offline.

### Bước 3 — Tạo Organization (nếu có domain công ty)

Việc có Organization hay không phụ thuộc vào loại tài khoản của bạn:

- Nếu dùng Google Workspace → Organization tự động được tạo.
- Nếu là tài khoản cá nhân (`@gmail.com`) → không có Org, chỉ có **Project**.
- Cá nhân muốn có Org: dùng **Cloud Identity Free** (không cần mua Workspace).

### Bước 4 — Setup billing alert

Billing alert là tấm lưới an toàn để không bị "viêm màng túi". Trong GCP Console, vào phần Billing và tạo budget kèm các mốc cảnh báo:

```bash
# Trong GCP Console:
# Billing → Budgets & alerts → Create budget
# - Set budget: $20/tháng (sandbox)
# - Alert at: 50%, 90%, 100%, 120%
# - Email: your-email + Slack webhook (optional)
```

Có một điểm tối quan trọng phải nhớ: GCP **không tự tắt** service khi vượt budget. Alert chỉ *cảnh báo*, không *chặn*. Nếu muốn chặn cứng chi phí, bạn phải tự dựng **kill switch** (thường là một Cloud Function tự tắt resource khi budget vượt ngưỡng).

### Bước 5 — Bật Cloud Audit Logs

Audit log là "camera an ninh" của tài khoản — sau này có sự cố mới có cái mà truy. Cấu hình sink mặc định cho đúng:

```bash
# Logging → Logs Router → đảm bảo "_Default" sink active
# Audit log Admin Activity = always-on (free)
# Data Access log = optional, tính phí — bật cho service quan trọng
```

### Bước 6 — Không bao giờ dùng tài khoản quyền cao nhất cho việc hằng ngày

Nguyên tắc này áp dụng cho mọi nền tảng cloud, không riêng GCP. Tài khoản quyền tối cao chỉ nên xuất hiện đúng một lần — lúc setup ban đầu:

- Tài khoản **Org Admin** (Organization Administrator) chỉ dùng để setup ban đầu.
- Tạo **Project IAM Admin** + **Project Editor** cho công việc hằng ngày.
- Việc automation thì dùng service account, **không** dùng user account.

Setup nền móng xong, giờ ta cần một cái "tay cầm điều khiển" để thao tác nhanh mà không phải click chuột trong Console — đó là gcloud CLI.

---

## 5️⃣ gcloud CLI — Cài đặt + auth + config

Console tiện cho người mới, nhưng dân chuyên nghiệp gần như sống trong terminal. `gcloud` là CLI chính của GCP, làm được mọi thứ Console làm và còn scriptable. Ta đi từ cài đặt, sang xác thực (auth), rồi tới cấu hình nhiều project.

### Cài đặt

Chọn lệnh theo hệ điều hành của bạn. Riêng Linux cần thêm Google Cloud apt repo trước, nếu không sẽ gặp lỗi "package not found" trên máy Debian/Ubuntu sạch:

```bash
# macOS
brew install --cask google-cloud-sdk

# Linux (Debian/Ubuntu) — cần thêm Google Cloud apt repo trước
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
sudo apt update && sudo apt install google-cloud-cli

# Windows
# Tải installer từ cloud.google.com/sdk/docs/install-sdk

# Verify
gcloud --version
```

### Auth — User account (interactive)

Cách xác thực đầu tiên là đăng nhập tương tác bằng chính tài khoản người dùng của bạn — hợp khi làm việc thủ công trên máy cá nhân:

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

Pipeline CI/CD không thể click browser để login, nên nó cần một danh tính riêng: service account. Lưu ý dòng tạo key — file JSON đó là *secret*, tuyệt đối không commit lên Git:

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

Thật ra năm 2026 có cách an toàn hơn hẳn JSON key: **Workload Identity Federation** (WIF). Với WIF, bạn không cần lưu key file nào cả — GCP tin tưởng trực tiếp token OIDC từ GitHub Actions/GitLab, nên không có file secret nào để lỡ tay làm rò rỉ. Mình sẽ quay lại WIF ở phần cạm bẫy.

### Config — Multi-project setup

Trong thực tế bạn sẽ nhảy qua lại giữa tài khoản công ty và sandbox cá nhân. `gcloud` cho phép lưu nhiều "configuration", mỗi cái nhớ sẵn account + project + region, đổi qua lại bằng một lệnh:

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

### Lệnh dùng thường ngày

Cuối cùng là một nhúm lệnh bạn sẽ gõ đi gõ lại — liệt kê project, đặt project mặc định, xem VM và bucket:

```bash
# List projects
gcloud projects list

# Set default project
gcloud config set project acmeshop-prod

# List VMs trong project
gcloud compute instances list

# List buckets
gcloud storage buckets list

# Xem chi tiết 1 VM (vd lấy external IP)
gcloud compute instances describe web-1 \
    --zone=asia-southeast1-a \
    --format='value(networkInterfaces[0].accessConfigs[0].natIP)'
```

Có `gcloud` chạy được rồi, một câu hỏi rất thực tế: nghịch nhiêu đây có tốn tiền không? Phần Free Tier trả lời.

---

## 6️⃣ Free Tier 2026 — Cái gì miễn phí

Tin tốt cho người học: GCP cho dùng miễn phí khá rộng tay. Free Tier gồm **hai phần** tách biệt — credit dùng thử có hạn, và một nhóm "always free" dùng mãi mãi.

### A. $300 trial credit (90 ngày)

Phần đầu là khoản credit hào phóng dành cho người mới, nhưng chỉ một lần:

- Một lần duy nhất cho mỗi billing account.
- Dùng được cho mọi service, mọi region.
- Hết 90 ngày hoặc hết $300 → dừng lại (không bị charge nếu bạn chưa chủ động upgrade).

### B. Always Free (dùng mãi, sau khi hết trial)

Phần thứ hai mới là thứ giữ chân bạn lâu dài: một loạt hạn mức miễn phí vĩnh viễn, đủ để học và chạy vài project nhỏ:

| Service | Hạn mức always free |
|---|---|
| Compute Engine | 1 VM `e2-micro` tại US (`us-west1`, `us-central1`, `us-east1`) |
| Cloud Storage | 5 GB regional storage tại US, 5000 Class A op/tháng |
| Cloud Run | 2 triệu request/tháng, 360k GB-s memory |
| Cloud Functions | 2 triệu invocation/tháng |
| Cloud Pub/Sub | 10 GB messages/tháng |
| Cloud Build | 120 build-minutes/ngày |
| BigQuery | 1 TB query/tháng, 10 GB storage |
| Firestore | 1 GB storage, 50k read/20k write/20k delete mỗi ngày |
| Logging | 50 GB ingestion/tháng |
| Monitoring | 150 MB metric ingestion đầu tiên |

Hạn mức này đủ thoải mái cho việc học và các project cá nhân nhỏ. Một lưu ý nhỏ để khỏi nhầm: đừng lẫn Free Tier của GCP với AWS Free Tier — AWS cho miễn phí theo kiểu 12 tháng đầu, còn "always free" của GCP là vĩnh viễn nhưng theo hạn mức.

Còn một mảnh ghép cuối của baseline mà ta đã nhắc tới nhiều lần nhưng chưa đào sâu: hệ thống phân quyền IAM.

---

## 7️⃣ Cloud IAM cơ bản

IAM (Identity and Access Management) là bộ não phân quyền của GCP: nó quyết định *ai* được làm *gì* trên *resource nào*. Hiểu sai IAM là nguồn gốc của phần lớn sự cố bảo mật cloud, nên ta dành hẳn một phần cho nó.

> [!NOTE]
> **Ẩn dụ:**\
> Cloud IAM giống **hệ thống vé ra vào một nhà máy**. Mỗi người (*Identity*) cầm một tấm vé ghi rõ vai trò (*Role*) và được vào khu nào (*Resource*). Vé luôn theo nguyên tắc **least privilege** — chỉ cho vào đúng khu cần làm việc, không hơn. Cấp vé "đi đâu cũng được" cho tất cả mọi người chính là cách nhanh nhất để mất kiểm soát.

Với ẩn dụ đó, các khái niệm IAM trở nên dễ ráp lại với nhau:

| Khái niệm | Mô tả |
|---|---|
| **Identity** (Member, Principal) | User, Group, Service Account, Workforce Identity |
| **Role** | Một bó permission (vd `roles/storage.objectViewer`) |
| **Resource** | VM, bucket, project, ... |
| **Binding** | Bộ ba (Identity, Role, Resource) |
| **Policy** | Danh sách các binding cho một resource |

Trong các khái niệm trên, *Role* là thứ bạn chọn nhiều nhất, nên cần phân biệt rõ ba loại role:

| Loại | Mô tả | Ví dụ |
|---|---|---|
| **Primitive (basic)** | Đời cũ — Owner/Editor/Viewer cho toàn project | `roles/owner` |
| **Predefined** | Chi tiết (granular) theo từng service | `roles/storage.objectAdmin` |
| **Custom** | Tự tạo danh sách permission riêng | Khi predefined không vừa |

Kim chỉ nam năm 2026: **không dùng** primitive role nữa, hãy luôn ưu tiên predefined; chỉ tự tạo custom khi predefined không khớp nhu cầu. Lý do nằm ở phần cạm bẫy bên dưới.

Để thấy IAM hoạt động cụ thể, đây là ba lệnh cấp và xem quyền hay dùng nhất:

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

Lý thuyết đã đủ. Giờ ráp tất cả lại thành một bài thực hành đầu-cuối, để bạn tự tay chạm vào account, gcloud và một VM thật.

---

## 🛠️ Hands-on — Setup GCP account an toàn + VM đầu tiên

### Mục tiêu

Bạn sẽ tạo account GCP, dựng baseline an toàn, deploy một VM `e2-micro` (free tier), SSH vào, rồi dọn dẹp sạch để không phát sinh chi phí.

### Bước 1 — Tạo account + Project

Khởi đầu bằng việc có một project sạch để nghịch:

1. Tạo Google account (nếu chưa có).
2. Vào [console.cloud.google.com](https://console.cloud.google.com).
3. Nhận $300 trial credit.
4. Tạo project mới: tên `acmeshop-sandbox` (Project ID phải unique trên toàn cầu).

### Bước 2 — Cài gcloud + auth

Cài CLI và đăng nhập, đồng thời trỏ về đúng project vừa tạo:

```bash
brew install --cask google-cloud-sdk
gcloud auth login
gcloud config set project acmeshop-sandbox
gcloud auth application-default login
```

### Bước 3 — Bật billing + budget alert

Trước khi tạo bất cứ resource nào tốn tiền, dựng sẵn lưới an toàn budget:

```bash
# Trong Console:
# Billing → Link a billing account
# Budgets → New budget $10/tháng, alert 50/90/100%
```

### Bước 4 — Tạo VM e2-micro (free tier)

Đây là phần thú vị nhất — dựng một máy ảo thật trong vài giây, SSH vào chạy thử, rồi xóa ngay để khỏi tốn:

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

Bước cleanup không phải tùy chọn — đó là thói quen sống còn. Một VM quên xóa cuối tháng có thể là một hóa đơn bất ngờ.

### Bước 5 — Setup multi-account config

Cuối cùng, dựng hai configuration để sau này nhảy qua lại work/sandbox chỉ bằng một lệnh:

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

Hoàn thành năm bước trên nghĩa là bạn đã có: account hoạt động, gcloud được cấu hình, một VM deploy thử thành công, và billing alert đang canh chừng. Đó chính là baseline mà sếp giao đầu bài.

---

## 💡 Cạm bẫy thường gặp & Best practice

Dưới đây là tám cái bẫy mình thấy người mới (và cả người có kinh nghiệm) dính nhiều nhất trên GCP, kèm cách phòng. Đọc kỹ phần này có khi tiết kiệm cho bạn cả nghìn đô và vài đêm mất ngủ.

### ❌ Cạm bẫy: Để service account key file rò rỉ

Bạn tạo một SA key JSON, lỡ tay commit vào Git repo rồi push lên public.

**Hậu quả:** crypto miner quét GitHub liên tục và sẽ khai thác key của bạn trong vòng 1–2 giờ, để lại hóa đơn $1000–10000.

### ✅ Best practice

- **Không bao giờ commit** file key JSON.
- Cài `gitleaks` làm git hook để chặn trước khi commit.
- Tốt nhất: dùng **Workload Identity Federation** — không cần key file nào cả.

### ❌ Cạm bẫy: Quên cleanup VM/bucket khi thử nghiệm

Bạn tạo một VM `n2-highmem-32` để test cho nhanh, rồi quên xóa — cuối tháng nhận hóa đơn $500.

### ✅ Best practice

- Gắn tag cho mọi resource: `env=sandbox,owner=thien-le`.
- Đặt **billing budget alert** + một Cloud Function tự tắt VM khi vượt ngưỡng.
- Lập cron nhắc hằng ngày: chạy `gcloud compute instances list` để rà soát.

### ❌ Cạm bẫy: Nhầm giữa Project Name và Project ID

Project có hai thứ dễ lẫn — **Project Name** (tên hiển thị, đổi được) và **Project ID** (immutable, unique toàn cầu). Lệnh `gcloud` luôn dùng **ID**, không dùng Name.

### ✅ Best practice

- Đặt ID rõ ràng: `acmeshop-prod-2026`, đừng để mặc định kiểu `my-project-1234`.
- Luôn `gcloud config set project <ID>` ở đầu mỗi session.

### ❌ Cạm bẫy: Nhầm Region/Zone

VM nằm ở `us-central1-a` nhưng bucket lại ở `asia-southeast1` → latency cao và phát sinh phí egress (truyền dữ liệu ra ngoài region).

### ✅ Best practice

- Đặt sẵn default region/zone trong config.
- Các resource liên quan nhau nên cùng một region.

### ❌ Cạm bẫy: Cấp primitive role `Editor` cho tất cả

Cả dev team được cấp `roles/editor` → ai cũng có thể xóa luôn database production.

### ✅ Best practice

- Dùng **predefined role** chi tiết: `roles/cloudsql.viewer`, `roles/storage.objectAdmin`.
- Kiểm thử quyền bằng `gcloud auth login --impersonate-service-account` xem đã đủ chưa.

### ❌ Cạm bẫy: Dùng Org Admin cho việc hằng ngày

Tài khoản Org Admin (toàn quyền) nếu bị chiếm → cả Organization có thể bị xóa sạch.

### ✅ Best practice

- Org Admin chỉ dùng lúc setup ban đầu.
- Hằng ngày làm việc bằng tài khoản có role giới hạn.
- Bắt buộc Org Admin dùng hardware key (YubiKey).

### ❌ Cạm bẫy: Không bật Audit Log Data Access

Admin Activity log bật sẵn mặc định, nhưng **Data Access log** (ghi nhận ai đã đọc bucket nào) phải bật thủ công → khi cần điều tra (forensic) thì không có dấu vết để lần.

### ✅ Best practice

- Bật Data Access cho các service chứa dữ liệu nhạy cảm (GCS bucket chứa PII, BigQuery dataset).
- Lưu ý: Data Access log **tính phí ingest**, nên bật có chọn lọc.

### ❌ Cạm bẫy: Mở firewall `0.0.0.0/0`

VPC firewall rule cho phép `0.0.0.0/0` ở port 22 → mở cửa cho SSH brute-force từ khắp Internet.

### ✅ Best practice

- Dùng **IAP (Identity-Aware Proxy) tunnel** cho SSH: `gcloud compute ssh --tunnel-through-iap`.
- Firewall chỉ mở cho dải IP mà bạn biết rõ.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] Kể tên 3 service tier 1 của GCP cho mỗi nhóm (compute / storage / database / network)?
- [ ] Vẽ sơ đồ Org → Folder → Project → Resource cho công ty của bạn?
- [ ] Tạo được gcloud config riêng cho work và cho sandbox?
- [ ] Tạo một VM `e2-micro` free tier, SSH vào, rồi xóa?
- [ ] Setup billing budget alert $10/tháng?
- [ ] Giải thích vì sao **không nên dùng** primitive role `Editor`?
- [ ] Nêu lý do Workload Identity Federation an toàn hơn JSON key?

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Nhóm lệnh `gcloud` hay dùng nhất, gom lại để tra cho nhanh:

```bash
# Auth & account
gcloud auth login                          # đăng nhập user account (mở browser)
gcloud auth list                           # liệt kê account đang active
gcloud auth application-default login      # cấp credential cho SDK

# Config & project
gcloud config configurations list          # liệt kê các configuration
gcloud config configurations activate work # đổi sang config "work"
gcloud config set project <PROJECT_ID>     # đặt project mặc định
gcloud config list                         # xem config hiện tại
gcloud projects list                       # liệt kê toàn bộ project

# Compute & storage
gcloud compute instances list              # liệt kê VM
gcloud compute ssh <vm> --zone=<zone>      # SSH vào VM
gcloud storage buckets list                # liệt kê bucket GCS

# IAM
gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="user:<email>" --role="<role>"   # cấp role
gcloud projects get-iam-policy <PROJECT_ID>   # xem policy của project
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **GCP** | Google Cloud Platform | Nền tảng public cloud của Google |
| **Project** | Dự án | Đơn vị quản lý billing + IAM + resource (tương đương AWS Account) |
| **Organization** | Tổ chức | Container cấp cao nhất, gắn với domain Google Workspace |
| **Folder** | Thư mục | Nhóm các project theo logic (tương đương AWS OU) |
| **gcloud CLI** | CLI của GCP | Công cụ dòng lệnh chính của GCP |
| **Service Account** | Tài khoản dịch vụ | Identity cho ứng dụng/automation (không phải user) |
| **WIF** | Workload Identity Federation | Cơ chế auth không cần lưu key file |
| **IAM** | Quản lý danh tính & quyền | Identity and Access Management |
| **Role** | Vai trò | Một bó permission gộp lại |
| **Predefined Role** | Vai trò định sẵn | Role chi tiết theo từng service (`roles/storage.objectViewer`) |
| **Primitive Role** | Vai trò cơ bản | Role đời cũ rộng (Owner/Editor/Viewer) — không khuyến nghị |
| **GCE** | Google Compute Engine | Dịch vụ máy ảo (VM) |
| **GCS** | Google Cloud Storage | Object storage |
| **GKE** | Google Kubernetes Engine | Managed Kubernetes |
| **BigQuery** | (giữ nguyên) | Data warehouse serverless, query SQL trên dữ liệu petabyte |
| **Pub/Sub** | (giữ nguyên) | Dịch vụ messaging global |
| **Cloud Run** | (giữ nguyên) | Serverless container (nền Knative) |
| **Free Tier** | Gói miễn phí | Always free + $300 trial trong 90 ngày |
| **IAP** | Identity-Aware Proxy | SSH/HTTP đi qua xác thực Google identity |
| **CUD** | Committed Use Discount | Cam kết 1–3 năm, giảm tới 57% chi phí |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloud Fundamentals — nền tảng cloud chung](../../../cloud-fundamentals/)
- ➡️ **Bài tiếp theo:** [GCP Compute Engine + Persistent Disks](01_compute-engine-and-disks.md)
- ↑ **Về cụm:** [GCP (Google Cloud Platform)](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **So sánh vendor:** [AWS basic](../../../aws/) — đối chiếu các service tương đương
- ☁️ **Vendor #2:** [Azure basic](../../../azure/) — nhà cung cấp đứng thứ hai
- 🏗️ **Hạ tầng dạng code:** [IaC Terraform](../../../../10_devops/iac/) — dùng Terraform GCP provider
- 🧭 **Tấm bản đồ sự nghiệp:** [Cloud Engineer Career Roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác

- [GCP docs](https://cloud.google.com/docs) — tài liệu chính thức đầy đủ nhất.
- [gcloud CLI reference](https://cloud.google.com/sdk/gcloud/reference) — tra cứu mọi lệnh gcloud.
- [GCP Free Tier](https://cloud.google.com/free) — kiểm tra hạn mức miễn phí mới nhất.
- ⬅️ **Bài trước:** [Pricing Calculator](https://cloud.google.com/products/calculator) — ước tính chi phí trước khi dựng.
- [Cloud Skills Boost](https://www.cloudskillsboost.google/) — khóa học chính thức của Google (Qwiklabs).
- [GCP Architecture Framework](https://cloud.google.com/architecture/framework) — best practice thiết kế hệ thống.
- [GCP Professional Cloud Architect cert](https://cloud.google.com/certification/cloud-architect) — chứng chỉ kiến trúc sư cloud.
- [Workload Identity Federation guide](https://cloud.google.com/iam/docs/workload-identity-federation) — auth không cần key file.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 00 cụm GCP basic. Overview GCP + so sánh AWS/Azure + 20 services tier 1 + Org→Folder→Project hierarchy + gcloud setup + Free Tier 2026 + IAM cơ bản + hands-on tạo VM + 8 pitfalls.
- **v2.0.0 (01/06/2026)** — Viết lại sang văn phong narrative theo gold-standard (lời dẫn trước mỗi bảng/code/list + câu phân tích sau, mạch WHY→WHAT→HOW, ẩn dụ đời thường). Chuẩn hoá heading framework + Glossary 3 cột + nav (⬅️/➡️/↑ Về cụm, link-text = tiêu đề thực, xoá nhãn "sắp viết"). Đổi "Prerequisites" → "Yêu cầu trước". Sửa lỗi code: thêm bước add Google Cloud apt repo khi cài gcloud trên Linux; thay lệnh vô nghĩa `gcloud cloud-shell scp --help` bằng `gcloud compute instances describe`. Thêm phần Cheatsheet. Bảo toàn toàn bộ số liệu và code kỹ thuật.
- **v2.0.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
