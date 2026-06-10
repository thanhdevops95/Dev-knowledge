# ☁️ Azure — Tổng quan + account setup + az CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Đã xong [Cloud Fundamentals](../../../cloud-fundamentals/) ✅, hiểu Region/AZ/IaaS-PaaS-SaaS

> 🎯 *Bài đầu tiên của cluster Azure. Azure là vendor #2 (~24% market share Q1 2026), mạnh nhất ở stack doanh nghiệp Microsoft (Windows Server, AD, Office 365, .NET). Bài này dạy: Azure là gì, services tier 1, hierarchy **Management Group → Subscription → Resource Group**, `az` CLI, Free Tier, Entra ID (Azure AD) basics, hands-on deploy first VM. Không deep từng service — 4 bài kế tiếp sẽ làm.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Azure khác AWS/GCP** ở điểm nào, vì sao chọn Azure
- [ ] Biết **20 services tier 1** của Azure và analog với AWS/GCP
- [ ] Tạo **Azure account** an toàn (MFA, billing alert, không leak credential)
- [ ] Hiểu **Management Group → Subscription → Resource Group → Resource** hierarchy
- [ ] Cài đặt **az CLI** + auth + config + multi-subscription
- [ ] Biết **Azure Free Tier 2026** cho gì (12 tháng + always free + $200 credit)
- [ ] Setup **Microsoft Entra ID** (Azure AD) baseline cho 1 user + group
- [ ] Hands-on tạo VM Linux đầu tiên rồi cleanup

---

## Tình huống — Bạn được giao tài khoản Azure của Acme Shop

Sáng thứ Hai, sếp gọi:

> *"Team mình stack chủ yếu trên AWS, nhưng tuần này phải migrate phần kế toán lên Azure vì tích hợp sẵn với Microsoft 365 + Entra ID của công ty. Bạn nhận subscription Azure rồi setup chuẩn nhé. Cuối tuần demo VM + Storage."*

Bạn login `portal.azure.com` lần đầu → bị overwhelm:

- Sidebar có 200+ services.
- "Subscription" là gì? Sao khác "Account"?
- "Resource Group" là cái gì, sao mọi resource bắt buộc nằm trong RG?
- "Azure AD" giờ đổi tên "Entra ID" — hai cái có khác nhau không?
- `az` CLI khác `aws` CLI ở đâu?
- Billing setup chỗ nào? Free Tier có gì?
- Region "Southeast Asia" và "East Asia" — chọn cái nào?

→ Bài này lấp đầy: Azure fundamentals + setup baseline secure + `az` CLI working + hands-on VM đầu tiên.

---

## 1️⃣ Azure là gì, khác AWS/GCP thế nào

🪞 **Ẩn dụ**: *AWS như **siêu thị 300+ kệ hàng** — đa dạng, đôi khi rối; GCP như **cửa hàng kỹ sư Google** — ít sản phẩm hơn nhưng tinh ở data/AI/K8s; Azure như **bộ combo Microsoft Office cho doanh nghiệp** — tích hợp sâu với Windows Server, Active Directory, .NET, Office 365, Dynamics 365, GitHub. Nếu công ty đã chạy stack Microsoft → Azure giảm 50% công migration.*

### Định nghĩa

**Azure** = nhà cung cấp public cloud của Microsoft, ra mắt 2010 (Windows Azure), rebrand 2014 thành Microsoft Azure. Hiện top-2 market share (~24% Q1 2026, sau AWS ~32%, trên GCP ~11%).

### Điểm mạnh Azure 2026

| Điểm mạnh | Vì sao | Ví dụ service |
|---|---|---|
| **Microsoft ecosystem** | Tích hợp sâu Office 365, Dynamics, Windows Server, SQL Server, .NET | Azure AD/Entra ID, Azure SQL, App Service .NET |
| **Hybrid cloud** | Azure Arc + Azure Stack Hub đưa Azure xuống on-prem | Arc-enabled servers, Azure Stack HCI |
| **Identity** | Entra ID = #1 enterprise identity (300M+ users) | Entra ID, Entra Conditional Access, B2C |
| **Enterprise deals** | Microsoft sales team mạnh — EA, MCA discount tới 30-50% | Reserved Instances + Azure Hybrid Benefit |
| **Compliance** | 100+ chứng chỉ — chính phủ Mỹ, EU, ngân hàng tin dùng | Azure Government, Azure China (21Vianet) |
| **AI / OpenAI** | Microsoft đầu tư OpenAI → Azure OpenAI Service độc quyền | Azure OpenAI, Copilot, Azure AI Studio |

### Điểm yếu / Trade-off

| Yếu | Hệ quả |
|---|---|
| Console phức tạp, rename liên tục (Azure AD → Entra ID, ASR → Azure Site Recovery) | Học mất thời gian; doc cũ outdated |
| Pricing model rối (5+ loại discount chồng nhau) | Khó dự đoán bill |
| Linux/open-source experience kém AWS một chút | Stack Linux thuần — AWS thường tốt hơn |
| Outage history nhiều hơn AWS | SLA same nhưng incident frequency cao hơn |
| Documentation chất lượng không đều | Khu vực mới (Container Apps) thiếu docs production-ready |

### Khi nào chọn Azure

| Use case | Chọn Azure nếu |
|---|---|
| Stack Microsoft (Windows, .NET, SQL Server, Office 365) | Azure Hybrid Benefit giảm 40% cost Windows VM |
| Identity-centric (SSO, MFA, Conditional Access) | Entra ID + Microsoft 365 integration |
| Hybrid cloud (on-prem + cloud) | Azure Arc + Stack Hub trưởng thành nhất |
| OpenAI / GPT-4 production | Azure OpenAI Service = exclusive enterprise GPT |
| Compliance ngành (banking, gov, health) | 100+ chứng chỉ, sovereign cloud |
| Migration enterprise lớn | Azure Migrate + EA discount mạnh |

→ **Quy tắc nhanh**: Stack Microsoft → Azure. Stack data/AI → GCP. Còn lại → AWS.

---

## 2️⃣ Azure Services tier 1 (must-know)

Có hơn 200 services. **Tier 1** (cần biết ngay) = ~20 services chiếm 90% workload.

### Compute (chạy code)

| Service | Mô tả | Analog AWS / GCP | Khi dùng |
|---|---|---|---|
| **Virtual Machines (VM)** | VM truyền thống | EC2 / GCE | Lift-and-shift, custom OS, GPU |
| **VM Scale Sets (VMSS)** | Auto-scaling VM group | EC2 ASG / GCE MIG | Stateless web fleet, scale theo CPU/queue |
| **Azure Functions** | Serverless function | Lambda / Cloud Functions | Event-driven, short tasks |
| **App Service** | PaaS web app (Linux/Windows) | Elastic Beanstalk / App Engine | Web app/API, không lo OS |
| **Container Apps** | Serverless container (Knative + Dapr) | Fargate / Cloud Run | Container microservices |
| **AKS** (Azure Kubernetes Service) | Managed Kubernetes | EKS / GKE | K8s-native team |
| **Container Instances (ACI)** | Single container chạy nhanh | Fargate task | Short-lived container, batch |

### Storage (lưu trữ)

| Service | Mô tả | Analog AWS / GCP |
|---|---|---|
| **Blob Storage** | Object storage | S3 / GCS |
| **Managed Disks** | Block storage cho VM | EBS / PD |
| **Azure Files** | Managed SMB/NFS | EFS / Filestore |
| **Disk Snapshots** | Snapshot block storage | EBS Snapshot |
| **Archive Storage** | Cold tier rẻ | S3 Glacier / GCS Archive |

### Database

| Service | Mô tả | Analog AWS / GCP |
|---|---|---|
| **Azure SQL Database** | Managed SQL Server | RDS SQL Server / Cloud SQL |
| **Azure SQL Managed Instance** | Near-100% SQL Server compat | RDS Custom |
| **Azure Database for PostgreSQL** | Managed Postgres | RDS Postgres / Cloud SQL Postgres |
| **Azure Database for MySQL** | Managed MySQL | RDS MySQL / Cloud SQL MySQL |
| **Cosmos DB** | Multi-API NoSQL global (SQL/Mongo/Cassandra/Gremlin/Table) | DynamoDB / Firestore (nhưng đa năng hơn) |
| **Azure Cache for Redis** | Managed Redis | ElastiCache / Memorystore |
| **Synapse Analytics** | Data warehouse + Spark | Redshift / BigQuery |

### Networking

| Service | Mô tả | Analog AWS / GCP |
|---|---|---|
| **Virtual Network (VNet)** | Virtual private cloud (region-bound) | VPC / VPC |
| **Load Balancer** | L4 LB | NLB / Cloud LB L4 |
| **Application Gateway** | L7 LB + WAF | ALB + WAF / Cloud LB L7 |
| **Front Door** | Global L7 + CDN + WAF | CloudFront + Global Accelerator |
| **CDN** | Content delivery network | CloudFront / Cloud CDN |
| **Azure DNS** | Managed DNS | Route 53 / Cloud DNS |
| **ExpressRoute** | Private connection on-prem ↔ Azure | Direct Connect / Cloud Interconnect |

### Identity, security, ops

| Service | Mô tả | Analog AWS / GCP |
|---|---|---|
| **Microsoft Entra ID** (Azure AD) | Identity service | IAM Identity Center / Cloud Identity |
| **Azure RBAC** | Permission management | IAM / Cloud IAM |
| **Key Vault** | Secret + key + cert | Secrets Manager + KMS / Secret Manager + KMS |
| **Microsoft Defender for Cloud** | Security posture + threat detection | Security Hub + GuardDuty / Security Command Center |
| **Azure Monitor** | Metrics + logs + alerts (Log Analytics) | CloudWatch / Cloud Monitoring |
| **Azure Policy** | Compliance enforcement | AWS Config / Organization Policy |

### Data, messaging, AI

| Service | Mô tả | Analog AWS / GCP |
|---|---|---|
| **Service Bus** | Enterprise messaging (queue + topic) | SQS + SNS / Pub/Sub |
| **Event Grid** | Event routing | EventBridge / Eventarc |
| **Event Hubs** | Streaming ingest (Kafka-compatible) | Kinesis / Pub/Sub streaming |
| **Azure OpenAI** | GPT-4o / o-series / DALL-E enterprise (chỉ model OpenAI) | Bedrock (Claude) / Vertex AI (Gemini) |
| **Azure AI Search** | Vector + semantic search | OpenSearch / Vertex AI Search |
| **Azure Data Factory** | ETL/ELT pipeline | Glue / Dataflow |

→ **Học bài 01-04** cluster basic: VM+Disks, Blob+RBAC, SQL+Cosmos DB, Functions+App Service.

---

## 3️⃣ Resource hierarchy — Management Group → Subscription → Resource Group

Azure **không có "Account" làm container** như AWS. Thay vào đó:

```
Tenant (Entra ID directory — 1 tổ chức)
└── Management Group: "Acme Shop"  ← group nhiều subscription
    ├── Management Group: "Production"
    │   ├── Subscription: "acmeshop-prod"          ← billing + quota
    │   │   ├── Resource Group: "rg-prod-web"      ← logical grouping
    │   │   │   ├── VM "vm-prod-web-01"
    │   │   │   ├── Disk "disk-prod-web-01-os"
    │   │   │   └── NIC "nic-prod-web-01"
    │   │   ├── Resource Group: "rg-prod-data"
    │   │   │   ├── Storage Account "stacmeprodlogs"
    │   │   │   └── Azure SQL "sql-prod-orders"
    │   │   └── Resource Group: "rg-prod-network"
    │   └── Subscription: "acmeshop-shared"
    └── Management Group: "Sandbox"
        └── Subscription: "thien-le-sandbox"
```

### Các level

| Level | Mô tả | Tương đương AWS / GCP |
|---|---|---|
| **Tenant** | Entra ID directory — gắn domain (acmeshop.onmicrosoft.com) | AWS Organization / GCP Organization |
| **Management Group** | Group subscription để apply policy + RBAC kế thừa | AWS OU / GCP Folder |
| **Subscription** | Đơn vị **billing** + quota + isolation; mỗi resource thuộc 1 subscription | AWS Account / GCP Project |
| **Resource Group** | Container logical để group resource cùng vòng đời | (không có exact analog — gần nhất AWS Tag/CloudFormation Stack) |
| **Resource** | VM, Disk, Storage Account, ... | (same) |

### Vì sao "Resource Group" là khái niệm độc đáo của Azure

- **Group theo vòng đời**: tất cả resource trong RG nên có lifecycle giống nhau — deploy cùng, xóa cùng.
- **RBAC + Policy** apply trên RG → kế thừa xuống mọi resource bên trong.
- **Cost tracking** dễ dàng: filter cost theo RG.
- **Region của RG** chỉ là metadata; resource bên trong có thể ở region khác (nhưng best practice = cùng region).

### Vì sao "Subscription" là đơn vị chính

- **Billing**: mỗi subscription có 1 billing account (có thể share trong EA).
- **Quota**: vCPU limit, public IP limit tính per subscription.
- **Isolation**: resource giữa subscription tách biệt.
- **RBAC**: role assignment thường ở subscription/RG level.

→ **Thực hành**: 1 subscription cho 1 environment (`prod`, `staging`, `dev`); RG nhóm theo workload (`rg-prod-web`, `rg-prod-data`).

---

## 4️⃣ Tạo Azure account + secure baseline

### Bước 1 — Tạo account

1. Vào [azure.microsoft.com/free](https://azure.microsoft.com/free) → "Start free".
2. Đăng nhập bằng Microsoft account (hotmail/outlook/work email).
3. Cung cấp credit card (verify, không charge nếu trong Free Tier).
4. Nhận **$200 trial credit** + 30 ngày + **12 tháng free** một số service + **always free** một số service.

### Bước 2 — Bật MFA cho Microsoft account

**Bắt buộc** trước khi làm gì khác:

1. [account.microsoft.com/security](https://account.microsoft.com/security) → Two-step verification → Turn on.
2. Dùng **Microsoft Authenticator** app — không dùng SMS.
3. Backup codes lưu offline (encrypted USB hoặc password manager offline).

### Bước 3 — Setup Entra ID baseline (tenant)

Azure tự động tạo 1 **Entra ID tenant** khi đăng ký. Tenant default domain: `<your-name>.onmicrosoft.com`.

```
☐ Bật Security Defaults (free, 1 click) — bắt buộc MFA toàn tenant.
☐ Tạo Break-glass account (emergency admin, không MFA, password 30+ chars, lưu offline).
☐ Bật Conditional Access (cần Entra ID P1 — tính phí — cho enterprise).
☐ Audit log: Entra ID → Monitoring → Sign-in logs (90 ngày miễn phí).
```

### Bước 4 — Setup billing alert (Cost Management)

```
Portal:
  Cost Management + Billing
    → Budgets
      → Add budget: "acme-monthly-cap"
      → Amount: $20/tháng
      → Alert: 50%, 80%, 100%, 110%
      → Email + Action Group (Slack webhook optional)
```

**Quan trọng**: Azure **không tự tắt** service khi over budget. Alert chỉ cảnh báo. Muốn cap cứng → dùng **Spending limit** (chỉ available với Free Trial / MSDN subscription) hoặc Logic App auto-shutdown VM.

### Bước 5 — Bật Microsoft Defender for Cloud (Free tier)

```bash
# Free tier: Cloud Security Posture Management (CSPM) miễn phí.
# Bật trong Portal:
# Defender for Cloud → Environment settings → chọn subscription → Enable Defender CSPM (free).

# Hoặc CLI:
az security pricing create --name "CloudPosture" --tier "Free"
```

→ Free tier check security baseline (RBAC issues, public storage, weak password policy). Không protect runtime — bản Standard tính ~$15/server/tháng.

### Bước 6 — Enable Activity Log + diagnostic settings

```bash
# Activity Log = tất cả API call (control plane), free 90 ngày.
# Để giữ lâu hơn → export sang Log Analytics workspace.

# Tạo workspace
az monitor log-analytics workspace create \
    --resource-group rg-shared \
    --workspace-name law-acmeshop-prod \
    --location southeastasia

# Forward Activity Log
az monitor diagnostic-settings subscription create \
    --name "ActivityLog-to-LAW" \
    --location southeastasia \
    --workspace law-acmeshop-prod \
    --logs '[{"category":"Administrative","enabled":true},{"category":"Security","enabled":true}]'
```

### Bước 7 — Không dùng Global Admin cho daily work

- Tài khoản **Global Administrator** (Entra ID) chỉ dùng emergency setup.
- Tạo user thường + role granular: `Owner`, `Contributor`, `Reader`, hoặc role custom.
- Bật **Privileged Identity Management (PIM)** nếu có Entra ID P2 — admin role chỉ active khi cần (just-in-time).

### Day 1 cost estimate

| Service | Cost/tháng |
|---|---|
| Azure subscription | $0 |
| Entra ID Free tier | $0 |
| Defender for Cloud (CSPM free) | $0 |
| Activity Log → Log Analytics (~1 GB) | ~$3 |
| Storage Account (logs) | <$1 |
| **Total baseline** | **~$5/tháng** |

→ Cheaper baseline than AWS (~$10-30) vì Defender CSPM free.

---

## 5️⃣ Naming conventions Azure

### Resource ID format

Mỗi resource Azure có 1 **Resource ID** unique:

```
/subscriptions/<sub-id>/resourceGroups/<rg-name>/providers/<namespace>/<type>/<name>
```

Examples:

```
/subscriptions/abc-123/resourceGroups/rg-prod-web/providers/Microsoft.Compute/virtualMachines/vm-prod-web-01
/subscriptions/abc-123/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodlogs
/subscriptions/abc-123/resourceGroups/rg-prod-data/providers/Microsoft.Sql/servers/sql-prod-orders/databases/orders
```

→ Phức tạp hơn AWS ARN, nhưng predictable: subscription → RG → provider → type → name.

### Region naming

| Region code | Location | Tier |
|---|---|---|
| `eastus` | Virginia | Tier 1 |
| `eastus2` | Virginia (paired) | Tier 1 |
| `westus2` | Washington | Tier 1 |
| `westus3` | Arizona | Tier 1 |
| `centralus` | Iowa | Tier 1 |
| `northeurope` | Ireland | Tier 1 |
| `westeurope` | Netherlands | Tier 1 |
| `uksouth` | London | Tier 1 |
| `francecentral` | Paris | Tier 1 |
| `germanywestcentral` | Frankfurt | Tier 1 |
| `southeastasia` | Singapore | Tier 1 |
| `eastasia` | Hong Kong | Tier 1 |
| `japaneast` | Tokyo | Tier 1 |
| `koreacentral` | Seoul | Tier 1 |
| `australiaeast` | Sydney | Tier 1 |

→ Convention: `<geo><direction><number>`. Một số region là **pair** (eastus + eastus2 = disaster recovery cặp).

### Resource naming pattern (CAF — Cloud Adoption Framework)

```
Convention:
  <resource-type-abbrev>-<workload>-<env>-<region>-<instance>

Examples:
  vm-web-prod-sea-01           (VM)
  rg-orders-prod-sea           (Resource Group)
  st-acmeshop-prod-sea         (Storage Account — KHÔNG có gạch nối, max 24 char, lowercase)
  sql-orders-prod-sea          (SQL Server)
  kv-acmeshop-prod-sea         (Key Vault)
  func-resize-prod-sea         (Function App)
  app-api-prod-sea             (App Service)
```

→ Một số resource có **constraint đặc biệt** (Storage Account: lowercase + numbers + max 24 char, không dấu gạch). Xem bảng [Azure resource abbreviations](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations).

### Tags

Mọi resource taggable:

```bash
az resource tag --tags Environment=prod Workload=orders Team=payments \
    Owner=thien.le@acmeshop.vn CostCenter=eng \
    --resource-group rg-prod-data --name sql-prod-orders \
    --resource-type "Microsoft.Sql/servers"
```

→ Cost Management filter by tag. Azure Policy enforce required tags.

---

## 6️⃣ az CLI — Cài đặt + auth + config

### Cài đặt

```bash
# macOS
brew install azure-cli

# Linux (Debian/Ubuntu)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Windows
# Tải MSI từ aka.ms/installazurecliwindows

# Verify
az --version
# azure-cli  2.66.0 ...
```

### Auth — User account (interactive)

```bash
# Login (mở browser device-code flow)
az login

# Login không browser (device code)
az login --use-device-code

# List subscriptions accessible
az account list --output table

# Set default subscription
az account set --subscription "acmeshop-prod"

# Verify current context
az account show --output table
```

### Auth — Service Principal (CI/CD)

```bash
# Tạo Service Principal (analog Service Account GCP / IAM Role AWS)
az ad sp create-for-rbac \
    --name "sp-ci-deployer" \
    --role "Contributor" \
    --scopes "/subscriptions/<sub-id>/resourceGroups/rg-prod-web" \
    --years 1

# Output:
# {
#   "appId": "...",        ← client_id
#   "displayName": "sp-ci-deployer",
#   "password": "...",     ← client_secret (chỉ hiện 1 lần!)
#   "tenant": "..."
# }

# Auth bằng SP
az login --service-principal \
    --username <appId> \
    --password <password> \
    --tenant <tenantId>
```

→ **Best practice 2026**: dùng **Workload Identity Federation** với GitHub Actions / GitLab OIDC — không cần lưu password, Azure trust OIDC token trực tiếp. (Tương tự GCP WIF / AWS OIDC trust.)

### Managed Identity (cho resource trên Azure)

```bash
# Bật System-assigned Managed Identity cho VM
az vm identity assign --resource-group rg-prod-web --name vm-prod-web-01

# VM gọi az/SDK không cần credential — Azure tự inject token
# Trong VM:
curl -H "Metadata: true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
```

→ Equivalent AWS instance role / GCP service account on VM. **Zero credential management** — best practice cho workload chạy trên Azure.

### Config — Multi-subscription

```bash
# List
az account list --output table

# Set default
az account set --subscription "acmeshop-prod"

# Set output format
az configure --defaults location=southeastasia group=rg-prod-web
az configure --defaults output=table

# Multiple contexts (workaround vì az không có "profile" như aws)
# Cách 1: export AZURE_SUBSCRIPTION_ID=<id>
# Cách 2: alias trong shell:
alias az-prod='az account set --subscription acmeshop-prod && az'
alias az-dev='az account set --subscription acmeshop-dev && az'
```

### Common commands

```bash
# Identity
az account show

# Region list
az account list-locations --output table

# Resource Group
az group create --name rg-test --location southeastasia
az group list --output table
az group delete --name rg-test --yes

# VM
az vm list --output table
az vm show --resource-group rg-prod-web --name vm-prod-web-01

# Storage
az storage account list --output table
az storage blob list --account-name stacmeprodlogs --container-name logs

# Functions
az functionapp list --output table

# Cost
az consumption usage list --start-date 2026-05-01 --end-date 2026-05-24
```

### Output formats + query (JMESPath)

```bash
# Default: json
az vm list

# Table
az vm list --output table

# TSV (parseable)
az vm list --output tsv

# JMESPath query
az vm list --query "[?powerState=='VM running'].[name,location,hardwareProfile.vmSize]" --output table

# Combine với --filter (server-side)
az resource list --resource-type Microsoft.Compute/virtualMachines \
    --query "[?tags.Environment=='prod'].[name,resourceGroup]" --output table
```

---

## 7️⃣ Azure Free Tier 2026

Azure Free Tier có **3 phần** (rộng hơn AWS, GCP):

### A. $200 credit trong 30 ngày đầu

- Dùng cho mọi service, mọi region.
- Hết 30 ngày hoặc hết $200 → ngừng (không charge nếu chưa upgrade Pay-As-You-Go).

### B. 12 tháng free (sau khi upgrade Pay-As-You-Go)

| Service | Hạn mức 12 tháng |
|---|---|
| Linux VM | 750h B1S VM/tháng |
| Windows VM | 750h B1S VM/tháng |
| Managed Disk | 64 GB × 2 SSD |
| Blob Storage | 5 GB LRS hot |
| Files | 5 GB LRS |
| Bandwidth (out) | 100 GB/tháng |
| Azure SQL Database | 250 GB S0 |

### C. Always Free (không hết hạn)

| Service | Hạn mức always free |
|---|---|
| Azure Functions | 1 triệu request/tháng + 400k GB-s |
| App Service | 10 web app F1 tier |
| Cosmos DB | 1000 RU/s + 25 GB |
| Cognitive Search | 50 MB index, 3 index |
| Azure DevOps | 5 users, unlimited private repo |
| Entra ID Free | 50k MAU object directory |
| Notification Hubs | 1 triệu push/tháng |
| Container Registry | 100 GB-s/tháng (Basic) |
| Azure AI translator | 2M ký tự/tháng |

→ **Azure Free Tier rộng nhất** trong 3 vendor (AWS chỉ 12 tháng, GCP chỉ always free + $300/90d). Tận dụng tối đa cho học và sandbox.

---

## 8️⃣ Entra ID (Azure AD) basics

🪞 **Ẩn dụ**: *Entra ID như **phòng nhân sự + bảo vệ tòa nhà** — Identity (ai bạn là) + Group (phòng ban) + Role (chức vụ) + Conditional Access (giờ vào, vị trí, thiết bị nào). Permission luôn theo **Principle of Least Privilege** — chỉ cho vào phòng cần làm việc, theo lịch.*

### Khái niệm

| Khái niệm | Mô tả |
|---|---|
| **Tenant** | 1 Entra ID directory (1 organization) |
| **User** | Account cá nhân (member/guest) |
| **Group** | Tập hợp user (Security/Microsoft 365) |
| **Application** | App đăng ký để gọi Microsoft Graph / Azure |
| **Service Principal** | Identity của app trong tenant (instance của Application) |
| **Managed Identity** | SP tự động cấp cho resource Azure (System/User-assigned) |
| **Role assignment** | Gán role cho identity tại scope (MG/Sub/RG/Resource) |

### Azure RBAC roles (≠ Entra roles)

| Loại | Phạm vi | Ví dụ |
|---|---|---|
| **Azure RBAC role** | Resource Azure (subscription, RG, ...) | `Owner`, `Contributor`, `Reader`, `Storage Blob Data Reader` |
| **Entra ID role** | Tenant directory (users, groups, apps) | `Global Administrator`, `User Administrator` |

→ 2 hệ thống tách biệt! Đừng nhầm. Azure RBAC quản resource Azure; Entra role quản directory.

### Built-in role thường dùng

| Role | Mô tả |
|---|---|
| `Owner` | Full control + assign role |
| `Contributor` | Full control trừ assign role |
| `Reader` | Read-only |
| `User Access Administrator` | Chỉ assign role, không touch resource |
| `Storage Blob Data Contributor` | Read+Write blob data |
| `Key Vault Secrets User` | Get/list secret (data plane) |
| `Virtual Machine Contributor` | Manage VM (control plane), không SSH |
| `Network Contributor` | Manage VNet/NSG |

→ **2026 best practice**: **không dùng** `Owner`/`Contributor` cho service principal; luôn role granular.

### Ví dụ — Grant role

```bash
# Grant user quyền read Blob trong 1 Storage Account
az role assignment create \
    --assignee thien.le@acmeshop.vn \
    --role "Storage Blob Data Reader" \
    --scope "/subscriptions/<sub-id>/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodlogs"

# Grant SP quyền deploy ARM trong RG
az role assignment create \
    --assignee <sp-app-id> \
    --role "Contributor" \
    --scope "/subscriptions/<sub-id>/resourceGroups/rg-prod-web"

# List assignment
az role assignment list --assignee thien.le@acmeshop.vn --output table
```

---

## 🛠️ Hands-on — Setup Azure baseline + first VM

### Mục tiêu

Bạn tạo subscription Azure, setup secure baseline, deploy 1 VM B1S Linux (free tier), SSH vào, cleanup.

### Bước 1 — Tạo account + subscription

1. Vào [azure.microsoft.com/free](https://azure.microsoft.com/free).
2. Đăng ký với Microsoft account.
3. Verify credit card (không charge).
4. Nhận $200 credit + 12 tháng free + always free.

### Bước 2 — Cài `az` + login

```bash
brew install azure-cli
az login
az account show --output table
az account set --subscription "Azure subscription 1"  # hoặc tên thực tế
```

### Bước 3 — Tạo Resource Group

```bash
az group create \
    --name rg-sandbox-sea \
    --location southeastasia \
    --tags Environment=sandbox Owner=thien.le@acmeshop.vn
```

### Bước 4 — Tạo VM B1S (free tier)

```bash
# Tạo VM với SSH key (key tự gen)
az vm create \
    --resource-group rg-sandbox-sea \
    --name vm-sandbox-test \
    --image Ubuntu2204 \
    --size Standard_B1s \
    --admin-username azureuser \
    --generate-ssh-keys \
    --public-ip-sku Standard

# Output có publicIpAddress
```

### Bước 5 — Mở port 22 + SSH

```bash
# B1s default NSG đã mở 22 nếu --generate-ssh-keys.
# Nếu chưa:
az vm open-port --port 22 --resource-group rg-sandbox-sea --name vm-sandbox-test

# Lấy public IP
PUBLIC_IP=$(az vm show -d --resource-group rg-sandbox-sea --name vm-sandbox-test --query publicIps -o tsv)
echo $PUBLIC_IP

# SSH
ssh azureuser@$PUBLIC_IP

# Trong VM:
echo "Hello from Azure!" > /tmp/hello.txt
cat /tmp/hello.txt
exit
```

### Bước 6 — Setup budget alert

```bash
# Tạo budget $10/tháng
az consumption budget create \
    --budget-name "sandbox-cap" \
    --amount 10 \
    --time-grain Monthly \
    --start-date 2026-05-01 \
    --end-date 2027-04-30 \
    --resource-group rg-sandbox-sea
```

### Bước 7 — Cleanup (tránh charge)

```bash
# Xóa toàn bộ RG = xóa mọi resource bên trong (VM, disk, NIC, NSG, public IP)
az group delete --name rg-sandbox-sea --yes --no-wait
```

→ **Kết quả**: Subscription hoạt động, `az` CLI configured, VM Ubuntu deploy + SSH thành công, budget alert active, cleanup gọn.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Để Service Principal password leak

**Bẫy**: Tạo SP, password hiện đúng 1 lần → copy vào script → commit vào Git public.

**Hậu quả**: Bot scan Git → exploit trong 1-2 giờ → crypto miner → $1000+ bill.

**Fix**:
- **Không bao giờ commit** SP password.
- Pre-commit hook `gitleaks` check.
- Tốt hơn: **Federated credential** (OIDC) cho CI/CD — không cần password.
- Tốt nhất: **Managed Identity** cho workload chạy trên Azure.

### 2. Quên xóa Resource Group sandbox

**Bẫy**: Tạo VM `Standard_D8s_v5` để test → quên xóa → cuối tháng $500 bill (B1s free tier chỉ áp dụng B1S).

**Fix**:
- Tag mọi RG: `Environment=sandbox`.
- Cron Logic App / Azure Automation tắt VM ngoài giờ làm việc.
- Daily reminder: `az resource list --output table`.
- Đặt budget hard alert + auto-shutdown.

### 3. Storage Account naming nhầm

**Bẫy**: `st-acme-prod-sea` → invalid! Storage Account chỉ cho phép **lowercase + digit, max 24 char, không dấu gạch**.

**Fix**:
- Đặt: `stacmeprodsea001` (concat tight).
- Validate trước khi deploy: regex `^[a-z0-9]{3,24}$`.

### 4. Region nhầm giữa "East Asia" vs "Southeast Asia"

**Bẫy**: VM ở `eastasia` (Hong Kong), Storage ở `southeastasia` (Singapore) → latency 30-50ms + egress fee.

**Fix**:
- Set default: `az configure --defaults location=southeastasia`.
- Vietnam → `southeastasia` (Singapore, ~30ms từ HCM/HN). `eastasia` chỉ tốt cho Hong Kong/South China.

### 5. Dùng `Owner` cho mọi user

**Bẫy**: Grant `Owner` subscription cho dev team → ai cũng delete production DB được.

**Fix**:
- Default role: `Reader` + `Contributor` cho RG cụ thể.
- Sensitive resource (Key Vault, SQL): role data-plane riêng (`Key Vault Secrets User`).
- Bật **Privileged Identity Management (PIM)** cho admin role just-in-time.

### 6. Global Admin cho daily work

**Bẫy**: Tài khoản Global Admin (Entra) bị compromise → cả tenant bị wipe.

**Fix**:
- Global Admin chỉ setup ban đầu + emergency.
- Tạo break-glass account riêng (password 30+ chars, lưu offline).
- Daily: tài khoản role giới hạn.
- Global Admin yêu cầu hardware key (FIDO2) + Conditional Access.

### 7. Không tắt Public IP mặc định trên VM

**Bẫy**: `az vm create` default tạo Public IP + mở port 22 cho `0.0.0.0/0` → SSH brute-force.

**Fix**:
- Dùng **Azure Bastion** (managed jump host) thay vì Public IP + SSH.
- Hoặc **Just-in-Time access** (Defender for Cloud) — port chỉ mở khi cần.
- Hoặc NSG rule chỉ allow IP nhà/VPN.

### 8. Không hiểu Soft Delete làm tăng cost

**Bẫy**: Xóa Storage Account → tưởng hết phí → nhưng Soft Delete giữ 7-30 ngày → vẫn tính storage cost.

**Fix**:
- Hiểu Soft Delete: Storage, Blob, Key Vault, VM disk đều có Soft Delete.
- Sandbox tắt Soft Delete để xóa hẳn ngay.
- Production bật để recovery — accept cost extra.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] Mô tả 3 service tier 1 của Azure cho mỗi nhóm (compute/storage/database/network)?
- [ ] Vẽ sơ đồ Tenant → Management Group → Subscription → Resource Group → Resource cho công ty bạn?
- [ ] Phân biệt **Azure RBAC role** vs **Entra ID role** — 2 hệ thống khác nhau ở đâu?
- [ ] Tạo 1 VM B1s free tier, SSH vào, rồi `az group delete` cleanup?
- [ ] Setup budget alert $10/tháng + activity log → Log Analytics?
- [ ] Giải thích vì sao **Managed Identity** tốt hơn Service Principal password?
- [ ] Vì sao Storage Account name không cho phép dấu gạch và viết hoa?
- [ ] Region Vietnam-friendly: `southeastasia` hay `eastasia`?

---

## 💡 Câu hỏi beginner hay hỏi

**Q1.** "Học Azure bắt đầu từ đâu?"

→ **20 services tier 1** ở trên. Đừng cố học hết 200 service. Pick 1 project (web app với SQL, hoặc serverless với Functions) → dùng 5-7 services là đủ.

**Q2.** "Cần Azure certification?"

→ **Helpful cho career, không bắt buộc**. 2026 recommend:
- **AZ-104 Azure Administrator Associate**: foundation cho ops.
- **AZ-204 Azure Developer Associate**: cho dev focus.
- **AZ-305 Azure Solutions Architect Expert**: sau khi có 1-2 năm hands-on.
- Skip AZ-900 nếu đã có kinh nghiệm cloud.

→ Cost: $165/exam. Học 1-2 tháng part-time. Microsoft Learn có free training path.

**Q3.** "Portal vs `az` CLI vs Terraform vs Bicep — học cái nào?"

→ **All four, theo thứ tự**:
- **Portal**: explore, debug, one-off task.
- **`az` CLI**: scripting, automation, ad-hoc.
- **Bicep**: IaC native Microsoft (DSL trên ARM JSON). Đơn giản, syntax đẹp.
- **Terraform**: IaC multi-cloud. Industry standard.

→ Daily: `az` CLI + Bicep/Terraform. Portal cho troubleshoot.

**Q4.** "Azure portal có quá nhiều menu, làm sao navigate nhanh?"

→ Mẹo:
- Pin 5-10 service hay dùng lên sidebar.
- Dùng search bar (`/`) — gõ tên service, resource, doc.
- Cloud Shell trong portal (`>_` icon) — chạy `az`/PowerShell ngay trong browser.
- Bookmark URL trực tiếp: `portal.azure.com/#@<tenant>/resource/subscriptions/<id>/resourceGroups/<rg>/overview`.

**Q5.** "Azure đắt hơn AWS/GCP cho startup?"

→ **Không, ngược lại**:
- Free Tier rộng hơn (12 tháng + always free + $200 credit).
- F1 App Service free 10 apps.
- Cosmos DB free 1000 RU/s + 25 GB always.
- Functions always free 1M req.

→ Azure phù hợp startup MVP free, AWS phù hợp scale production.

---

## 🗺️ Beyond basic — Career paths

Sau Azure basic:

| Path | Next Azure services |
|---|---|
| **DevOps Engineer** | AKS, Azure DevOps, Bicep, Container Apps, Azure Pipelines |
| **Backend Engineer** | Azure SQL, Cosmos DB, Functions, App Service, Service Bus, API Management |
| **Data Engineer** | Synapse, Data Factory, Databricks, Event Hubs, Stream Analytics |
| **ML Engineer** | Azure Machine Learning, Azure OpenAI, AI Search, Cognitive Services |
| **Cloud Architect** | Azure Well-Architected, Landing Zones, ExpressRoute, Front Door |
| **Security Engineer** | Defender for Cloud, Sentinel, Entra ID P2, Key Vault HSM, Confidential Compute |

→ Pick path. Deep dive 5-10 services per path.

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Gom các lệnh `az` nền tảng hay dùng nhất ngay từ bài đầu (login, chọn subscription, resource group, config) cùng bảng quy đổi nhanh tên service Azure sang AWS/GCP.

| Mục đích | Lệnh |
|---|---|
| Login (browser/device code) | `az login` · `az login --use-device-code` |
| Liệt kê subscription | `az account list --output table` |
| Chọn subscription mặc định | `az account set --subscription "acmeshop-prod"` |
| Xem context hiện tại | `az account show --output table` |
| Liệt kê region | `az account list-locations --output table` |
| Tạo / xoá Resource Group | `az group create --name rg-test --location southeastasia` · `az group delete --name rg-test --yes` |
| Đặt default location + group + output | `az configure --defaults location=southeastasia group=rg-prod-web output=table` |
| Tạo Service Principal cho CI/CD | `az ad sp create-for-rbac --name sp-ci-deployer --role Contributor --scopes <scope>` |
| Bật Managed Identity cho VM | `az vm identity assign --resource-group <rg> --name <vm>` |
| Gán RBAC role granular | `az role assignment create --assignee <user> --role "Storage Blob Data Reader" --scope <scope>` |
| Query JMESPath + output table | `az vm list --query "[?powerState=='VM running'].[name,location]" --output table` |

Bảng quy đổi nhanh tên service tier 1 sang AWS/GCP (dùng để chuyển kiến thức cũ sang Azure):

| Azure | AWS | GCP |
|---|---|---|
| Virtual Machines (VM) | EC2 | Compute Engine |
| Blob Storage | S3 | Cloud Storage |
| Azure SQL Database | RDS SQL Server | Cloud SQL |
| Cosmos DB | DynamoDB | Firestore |
| Azure Functions | Lambda | Cloud Functions |
| App Service | Elastic Beanstalk | App Engine |
| Container Apps | Fargate / App Runner | Cloud Run |
| AKS | EKS | GKE |
| Virtual Network (VNet) | VPC | VPC |
| Entra ID | IAM Identity Center | Cloud Identity |
| Key Vault | Secrets Manager + KMS | Secret Manager + KMS |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Azure** | Đám mây Microsoft | Nền tảng *public cloud* của Microsoft |
| **Subscription** | Gói đăng ký | Đơn vị billing + quota + isolation (tương đương AWS Account / GCP Project) |
| **Tenant** | Thư mục tổ chức | 1 Entra ID directory đại diện cho 1 tổ chức |
| **Management Group** | Nhóm quản trị | Group nhiều subscription để áp policy + RBAC kế thừa |
| **Resource Group (RG)** | Nhóm tài nguyên | Container logical gom resource cùng vòng đời |
| **Resource ID** | Định danh tài nguyên | Path unique định danh một resource trên Azure |
| **`az` CLI** | Dòng lệnh Azure | CLI chính thức của Azure |
| **Entra ID** | Dịch vụ định danh | Tên mới của Azure AD (từ 2023) — identity service |
| **Service Principal (SP)** | Danh tính ứng dụng | Identity cho app/automation, có credential (password/cert) |
| **Managed Identity** | Danh tính tự quản | SP tự động cấp cho resource Azure, không cần credential |
| **Workload Identity Federation** | Liên kết danh tính | OIDC trust GitHub/GitLab → không cần lưu password |
| **RBAC** | Phân quyền theo vai trò | Role-Based Access Control trên resource Azure |
| **Built-in role** | Vai trò dựng sẵn | Role pre-defined của Microsoft (Owner, Contributor, ...) |
| **Custom role** | Vai trò tùy biến | Tự định nghĩa danh sách permission |
| **PIM** | Quyền admin tạm thời | Privileged Identity Management — admin role just-in-time |
| **VM** | Máy ảo | Virtual Machine (nhóm Compute) |
| **VMSS** | Nhóm VM co giãn | Virtual Machine Scale Set — auto-scale group |
| **VNet** | Mạng riêng ảo | Virtual Network |
| **NSG** | Tường lửa L4 | Network Security Group — firewall tầng L4 |
| **Blob Storage** | Lưu trữ đối tượng | Object storage |
| **Storage Account** | Tài khoản lưu trữ | Container chứa Blob/Files/Queue/Table |
| **Key Vault** | Két bí mật | Nơi lưu secret + key + certificate |
| **App Service** | Web app PaaS | Dịch vụ chạy web app dạng PaaS |
| **Functions** | Hàm serverless | Serverless function |
| **AKS** | Kubernetes quản lý | Azure Kubernetes Service |
| **Bicep** | Ngôn ngữ IaC Azure | DSL IaC native của Azure (compile sang ARM JSON) |
| **ARM** | Lớp quản lý tài nguyên | Azure Resource Manager — API control plane |
| **Free Tier** | Hạn mức miễn phí | 12 tháng + always free + $200 credit (30 ngày) |
| **CAF** | Khung áp dụng cloud | Cloud Adoption Framework — best practice của Microsoft |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../../../cloud-fundamentals/)
- ➡️ **Bài tiếp theo:** [Azure VM + Managed Disks — Compute foundation](01_virtual-machines-and-disks.md)
- ↑ **Về cụm:** [Azure](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **So sánh vendor:** [AWS](../../../aws/) — đối chiếu service analog
- ☁️ **So sánh vendor:** [GCP (Google Cloud Platform)](../../../gcp/) — vendor #3
- 🏗️ **Triển khai tự động:** [IaC — Infrastructure as Code](../../../../10_devops/iac/) — Terraform có Azure provider
- 🧭 **Tấm bản đồ sự nghiệp:** [Cloud Engineer Career Roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác

- 📖 [Azure docs](https://learn.microsoft.com/azure/)
- 📖 [`az` CLI reference](https://learn.microsoft.com/cli/azure/)
- 📖 [Azure Free Tier](https://azure.microsoft.com/free)
- 📖 [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- 📖 [Microsoft Learn free training](https://learn.microsoft.com/training/azure/)
- 📖 [Cloud Adoption Framework](https://learn.microsoft.com/azure/cloud-adoption-framework/)
- 📖 [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
- 📖 [Resource abbreviations (CAF)](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations)
- 📖 [AZ-104 Administrator cert](https://learn.microsoft.com/certifications/azure-administrator/)
- 📖 [AZ-204 Developer cert](https://learn.microsoft.com/certifications/azure-developer/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 00 cụm Azure basic. Overview Azure + so sánh AWS/GCP + 20 services tier 1 + Management Group → Subscription → Resource Group hierarchy + `az` CLI + Service Principal/Managed Identity + Free Tier 2026 + Entra ID & RBAC cơ bản + hands-on tạo VM B1s + 8 pitfalls.
- **v1.1.0 (01/06/2026)** — Sửa lỗi QA: bỏ Claude khỏi mô tả Azure OpenAI (Azure OpenAI chỉ phục vụ model OpenAI; Claude qua Bedrock/Vertex AI); đổi field metadata "Prerequisites" → "Yêu cầu trước"; chuẩn hoá bảng Glossary sang 3 cột "Thuật ngữ | Tiếng Việt | Giải thích"; chuẩn hoá khối Liên kết & Tài nguyên (marker ⬅️/➡️/↑, 3 sub-heading canonical, link-text = tiêu đề thực của bài đích).
- **v1.1.1 (10/06/2026)** — Bổ sung mục Tra cứu nhanh (Cheatsheet) cho đồng bộ với cụm Azure.
