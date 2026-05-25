# 🎓 Vendor Lock-in & Portability — 4 chiều khoá, abstraction layer, exit cost

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** Đã đọc [00_what-is-multi-cloud-overview](00_what-is-multi-cloud-overview.md) ✅

> 🎯 *Bài 01 cluster Multi-cloud. Bài trước nói "vì sao multi-cloud"; bài này deep dive **vendor lock-in** — 4 dimension lock-in (data, API, skill, contract), tier service theo mức lock (low/medium/high), strategies giảm lock-in (abstraction layer Terraform/Crossplane/Pulumi/OpenTofu), reality của egress fee, framework tính exit cost. Acme Shop tier 100+ service hiện đang dùng để biết "muốn rời AWS thì tốn bao tiền".*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **4 dimension** của vendor lock-in (data, API, skill, contract)
- [ ] **Tier services** thành 3 mức (low/medium/high lock-in) — và quyết định dùng service nào
- [ ] Biết **3 abstraction layer chính** (Terraform, Crossplane, Pulumi) — khi nào nên dùng cái nào
- [ ] Hiểu **egress fee reality** và data gravity
- [ ] Áp dụng **framework tính exit cost** để pitch sếp cụ thể
- [ ] Tránh **over-abstraction** trap (build cloud SDK riêng)

---

## Tình huống — Acme Shop đếm cost rời AWS

Quay lại Acme Shop. Sau khi đọc bài 00, sếp đặt câu hỏi mới:

> Sếp: *"OK mình hiểu vì sao chưa đi multi-cloud ngay. Nhưng giả sử AWS tăng giá 30% năm sau — Acme Shop có rút sang GCP được không, và tốn bao tiền? Bạn cho mình con số cụ thể, không phải 'lock-in cao/thấp' chung chung."*

Bạn ngồi tính:
- Acme Shop có **50TB data** trên S3, **100 microservice** chạy ECS, **5 RDS Postgres**, **3 DynamoDB table**, **20 Lambda function**, **15 SQS queue**, **dùng Cognito auth**, **CloudFront CDN**, **Route 53 DNS**.
- Egress 50TB ra: 50,000 × $0.09 = **$4,500** (1 lần)
- Rewrite Lambda → Cloud Functions: ~3 engineer × 4 tháng = **$60K**
- Rewrite DynamoDB → Firestore (model khác hoàn toàn): ~2 engineer × 6 tháng = **$60K**
- Cognito → Identity Platform GCP migration: **$30K**
- Re-train team GCP: $20K
- Dual-running trong transition 3 tháng: $30K extra cloud bill
- Total: **~$200K + 4-6 tháng**

Sếp: *"OK, vậy AWS phải tăng giá nhiều hơn $200K/năm thì rời mới có lợi. Năm sau invoice là $1M — tăng 30% = $300K thêm. Có khả năng. Vậy chúng ta cần plan giảm lock-in từ giờ."*

→ Bài này dạy: làm sao tier service theo lock-in level, build portability principle để **giảm exit cost** xuống còn $50K thay vì $200K — mà KHÔNG cần multi-cloud ngay.

---

## 1️⃣ 4 dimension của vendor lock-in

🪞 **Ẩn dụ**: *Lock-in giống như **đi thuê nhà** — bị "khoá" theo 4 cách: (1) đồ đạc nặng quá khó chuyển (data lock), (2) hợp đồng dài hạn (contract lock), (3) hệ thống điện riêng không tương thích nhà mới (API lock), (4) cả gia đình quen hàng xóm/trường học khu này (skill lock). Rời nhà chỉ vì giá thuê tăng là phải cân nhắc cả 4.*

### Dimension 1: Data lock-in

**Định nghĩa**: Data đã lưu trên cloud → muốn rời phải transfer ra. Cost phụ thuộc egress fee + data volume + format.

**Thành phần**:

| Yếu tố | Acme Shop ví dụ |
|---|---|
| Volume | 50 TB trên S3 |
| Egress fee | $0.09/GB → **$4,500** chuyển 50TB |
| Format vendor-specific | DynamoDB JSON proprietary → cần ETL |
| Storage tier | Glacier → restore $0.03/GB nữa |

**Sub-type của data lock**:

- **Hot data lock** (live data đang dùng): mất khi rời cloud nếu không sync — RTO cao.
- **Cold data lock** (archive): rẻ lưu nhưng đắt rút (Glacier $0.09/GB restore + $0.02/GB egress).
- **Format lock**: data đang ở format proprietary (Parquet S3 → OK, DynamoDB JSON Stream → khó).
- **Schema lock**: BigQuery schema dùng nested REPEATED struct → re-model khi sang Snowflake.

### Dimension 2: API lock-in

**Định nghĩa**: Code gọi API vendor-specific → không chạy ở cloud khác.

**Spectrum**:

```
Standard ────────────────────── Proprietary
   ↑                                  ↑
  S3 API                          DynamoDB
  Postgres                        BigQuery
  K8s API                         Lambda
                                  Cognito
```

**Acme Shop ví dụ**:

| API | Mức lock | Khi rời |
|---|---|---|
| `boto3.client('s3').put_object()` | Low (S3 API là standard) | Cloudflare R2, GCS, MinIO đều support |
| `boto3.client('dynamodb').put_item()` | **High** | Phải rewrite cho Firestore / Cosmos DB (model khác hoàn toàn) |
| `boto3.client('cognito-idp')` | **High** | Phải migrate user pool sang Auth0/Identity Platform |
| `aws lambda invoke` | Medium | Move sang Cloud Functions: code Python copy được, runtime + trigger phải re-config |

### Dimension 3: Skill lock-in

**Định nghĩa**: Team chỉ biết 1 cloud → rời cloud = mất team productivity 3-6 tháng.

🪞 *Như hỏi đầu bếp Pháp nấu món Việt — kỹ thuật cơ bản giống, nhưng nguyên liệu + gia vị + cách dùng dao khác, mất 6 tháng học lại.*

**Skill lock components**:
- Cloud-specific tools: AWS CLI, gcloud, az.
- Cloud-specific patterns: IAM role chaining (AWS) vs Service Account impersonation (GCP).
- Cloud-specific monitoring: CloudWatch query syntax vs Cloud Monitoring MQL.
- Cloud-specific certification: AWS SAA mất 1 năm — không transfer được sang GCP.

**Mức lock theo skill**:

| Skill | Transfer rate AWS → GCP |
|---|---|
| Linux / Docker / K8s | 95% (gần như giữ nguyên) |
| Terraform | 80% (DSL giữ, provider khác) |
| Cloud networking concept | 70% (VPC khác hơi nhiều) |
| IAM / Identity | 40% (model khác hẳn) |
| Vendor-specific service (DynamoDB, BigQuery) | 20% |

### Dimension 4: Contract lock-in

**Định nghĩa**: Hợp đồng EDP, Reserved Instance, Committed Use Discount → cam kết multi-year, phá trước thời hạn = penalty.

**Acme Shop ví dụ**:

| Loại commit | Penalty rời sớm |
|---|---|
| AWS Reserved Instance (3 year, all upfront) | Mất tiền đã trả, không refund |
| AWS Savings Plan (3 year) | Phải trả tiếp đến hết term |
| GCP Committed Use Discount | Charge full price từ resource exit |
| AWS EDP (Enterprise Discount Program) | Phải đạt minimum spend, otherwise penalty 10-20% |

**Hidden contract lock**:
- Credit hợp đồng ($300K AWS credit) — chỉ dùng được trên AWS.
- Marketplace SaaS subscription — invoice qua AWS, rời = mất discount.
- AWS Partner program — lợi ích reseller chỉ AWS.

---

## 2️⃣ Tier services theo mức lock-in

Acme Shop ngồi tier hết 100+ service đang dùng. Đây là bảng:

### Tier 1: LOW lock-in (portable)

🟢 *Service có spec/API chuẩn — move được vài tuần.*

| Service | Vì sao low | Alternative |
|---|---|---|
| **EC2** (Compute) | VM với Linux/Docker | GCP CE, Azure VM — same OS |
| **EBS** (Block storage) | Standard volume | GCP PD, Azure Disk |
| **RDS Postgres / MySQL** | Standard SQL | Cloud SQL Postgres, Azure Database for Postgres |
| **S3** (qua API compatible) | S3 API là de facto standard | Cloudflare R2, GCS interop, MinIO |
| **EKS** (Managed K8s) | K8s API là CNCF standard | GKE, AKS — `kubectl` portable |
| **CloudFront** | CDN standard | Cloudflare, Fastly, Akamai |
| **Route 53** | DNS standard | Cloudflare DNS, NS1 |
| **VPC + Subnet** | Networking concept giống nhau | GCP VPC, Azure VNet |
| **Application Load Balancer** | HTTP LB standard | GCP LB, Azure App Gateway |
| **ElastiCache Redis** | Redis OSS protocol | Memorystore, Azure Cache, self-host |

→ **80% workload Acme Shop** ở tier này → exit cost không cao về API.

### Tier 2: MEDIUM lock-in

🟡 *Move được nhưng cần rewrite phần config + integration.*

| Service | Vì sao medium | Migration effort |
|---|---|---|
| **Lambda** | Code Python/Node copy được, nhưng trigger config + cold start behavior khác | 2-4 tuần per ~100 functions |
| **API Gateway** | Định nghĩa OpenAPI portable, nhưng auth + throttling vendor-specific | 1-2 tuần per API |
| **SQS** | Pattern queue giống, library SDK khác | 1 tuần per integration |
| **SNS** | Pub-sub pattern giống Pub/Sub GCP | 1 tuần |
| **CloudWatch Logs** | Log shipping pattern giống — config khác | Vendor log shipper (Vector, Fluent Bit) |
| **IAM Role** | Concept giống GCP Service Account nhưng model khác | Map manually |
| **Aurora** | Postgres-compatible nhưng có Aurora-specific feature (Global DB, Serverless v2) | 2-3 tuần |

### Tier 3: HIGH lock-in (rời = rewrite)

🔴 *Service vendor-specific, không có equivalent 1:1 — rời = re-architect.*

| Service | Vì sao high | Alternative phía cloud khác |
|---|---|---|
| **DynamoDB** | Data model proprietary (partition key + sort key), GSI/LSI khác hẳn Firestore | Firestore, Cosmos DB — re-model |
| **Cognito** | User pool + identity pool tightly coupled | Auth0, Okta, Identity Platform — migrate user |
| **Step Functions** | ASL state machine syntax proprietary | GCP Workflows, Azure Logic Apps — rewrite |
| **Kinesis Data Streams** | Shard model proprietary | Pub/Sub (different model), Kafka self-host |
| **SageMaker** | Training/inference pipeline + endpoint proprietary | Vertex AI, Azure ML — re-engineer |
| **Athena** | SQL on S3 — Presto-based nhưng tooling AWS | BigQuery (different model), Snowflake |
| **AWS Glue** | ETL job + crawler proprietary | Dataflow, Azure Data Factory |
| **CloudFormation** | YAML format AWS only | Terraform là alternative cross-cloud |
| **EventBridge** | Event bus + schema registry proprietary | Pub/Sub + custom schema, EventGrid |
| **WAF** | Rule format proprietary | Cloudflare WAF (much portable), Imperva |

→ **15% workload Acme Shop** ở tier này → cost rời lớn.

### Tier 4: ULTRA lock-in (rời = rebuild)

🔴🔴 *Service không có equivalent — phải design lại business logic.*

| Service | Vì sao ultra | Acme Shop có dùng? |
|---|---|---|
| **AWS Bedrock** | Specific model (Claude Anthropic exclusive via Bedrock) | Có — recommendation |
| **AWS GovCloud / Outposts** | Specific compliance / on-prem | Không |
| **AWS Quantum (Braket)** | Niche tech | Không |
| **Snowflake on AWS** | Snowflake là 3rd party — nhưng setup specific | Không |

### Tier matrix tổng

```
            │  Low (80%)  │  Medium (15%)  │  High (4%)  │ Ultra (1%)  │
────────────┼─────────────┼────────────────┼─────────────┼─────────────┤
Exit cost   │   1 tuần    │    1 tháng     │   3 tháng    │  6 tháng    │
Volume      │   Big       │    Medium      │   Small      │  Tiny       │
Strategy    │   Portable  │  Abstract API  │  Limit usage │   Avoid     │
```

→ Acme Shop tối ưu: minimize tier 3-4 usage, embrace tier 1-2 freely.

---

## 3️⃣ Abstraction layer strategy — 3 cấp độ

🪞 **Ẩn dụ**: *Abstraction layer như **adapter điện** — cắm vào ổ Mỹ hay châu Á đều dùng được. Trade-off: thêm adapter = thêm 1 component để fix khi hỏng.*

### Level 1: Tool-level abstraction (Terraform)

**Cách**: Dùng Terraform với multiple provider. Cùng tool, code khác nhau per cloud.

```hcl
# Terraform AWS
resource "aws_s3_bucket" "data" {
  bucket = "acmeshop-data-${var.env}"
}

# Terraform GCP — vẫn Terraform nhưng resource khác
resource "google_storage_bucket" "data" {
  name     = "acmeshop-data-${var.env}"
  location = "ASIA-SOUTHEAST1"
}
```

**Pros**:
- Tool đồng nhất → 1 team biết Terraform là làm được mọi cloud.
- State management portable.
- Workflow (plan/apply/destroy) giống nhau.

**Cons**:
- Code resource KHÔNG portable — viết riêng cho mỗi cloud.
- Switching cost vẫn là rewrite Terraform code.

**Khi nào dùng**: **Mặc định cho mọi team** — tool abstraction luôn đáng làm.

### Level 2: API-level abstraction (Crossplane)

**Cách**: Define abstraction "Database" — Crossplane translate sang RDS hoặc Cloud SQL tùy config.

```yaml
# Composite Resource Definition (XRD)
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xpostgresdatabases.acmeshop.io
spec:
  group: acmeshop.io
  names:
    kind: XPostgresDatabase
  versions:
    - name: v1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              properties:
                size: {type: string, enum: [small, medium, large]}
                region: {type: string}
                cloud: {type: string, enum: [aws, gcp, azure]}

---
# Composition (mapping per cloud)
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: aws-postgres
spec:
  compositeTypeRef:
    apiVersion: acmeshop.io/v1
    kind: XPostgresDatabase
  resources:
    - name: rds-instance
      base:
        apiVersion: rds.aws.crossplane.io/v1alpha1
        kind: DBInstance
        spec:
          forProvider:
            engine: postgres
            engineVersion: "15.4"

---
# Developer sử dụng
apiVersion: acmeshop.io/v1
kind: XPostgresDatabase
metadata:
  name: orders-db
spec:
  size: medium
  region: ap-southeast-1
  cloud: aws  # Đổi sang gcp → Crossplane tạo Cloud SQL
```

**Pros**:
- Developer KHÔNG cần biết cloud — chỉ cần biết schema XPostgresDatabase.
- Switching cloud = change 1 field.
- Self-service platform engineering.

**Cons**:
- Heavy upfront cost: 3-6 tháng setup Crossplane + define XRD.
- Yêu cầu team Platform engineering chuyên trách (3-5 engineer).
- Abstraction leak: feature đặc biệt của 1 cloud không expose ra được.

**Khi nào dùng**: Enterprise 200+ engineer, đã thật sự multi-cloud, có Platform team.

### Level 3: SDK-level abstraction (Pulumi / SDK riêng)

**Cách**: Code TypeScript/Python dùng SDK đa cloud (Pulumi) hoặc tự build wrapper.

```typescript
// Pulumi - same code AWS or GCP via abstraction
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as gcp from "@pulumi/gcp";

const cloud = pulumi.getStack().includes("gcp") ? "gcp" : "aws";

let bucket;
if (cloud === "aws") {
  bucket = new aws.s3.Bucket("data", { acl: "private" });
} else {
  bucket = new gcp.storage.Bucket("data", { location: "ASIA-SOUTHEAST1" });
}

export const bucketName = bucket.name;
```

**Pros**:
- Code thật bằng Python/TS, không phải HCL.
- Abstraction custom theo nhu cầu.
- Test được như application code.

**Cons**:
- Vẫn phải viết logic if/else per cloud.
- Bugs hiding behind abstraction.
- Maintenance burden tăng theo cloud count.

**⚠️ Anti-pattern**: Build "MyCompany Cloud SDK" từ đầu để abstract hết — chôn 1 năm engineering vào rồi không bao giờ dùng cloud thứ 2.

### Decision matrix

| Tình huống Acme Shop | Abstraction nên |
|---|---|
| Team <50, single-cloud nhưng muốn option | Level 1 (Terraform) |
| Team 50-200, hybrid, có ML team trên GCP | Level 1 + selective Level 2 |
| Enterprise 200+, đã multi-cloud thật | Level 2 (Crossplane) + Platform team |
| Startup 5 người | KHÔNG abstraction layer — chọn 1 cloud chạy thật |

→ Mặc định **Level 1**. Đừng over-engineer.

---

## 4️⃣ Egress fee reality — chiến lược thật

🪞 **Ẩn dụ**: *Data có **"trọng lực"** (gravity). Càng nhiều data, càng khó di chuyển. Cloud lớn dụ vào dễ (ingress free) nhưng đi ra đắt — như hotel có wifi free nhưng minibar đắt.*

### Egress fee 2026 (cập nhật mới)

| Source → Destination | Cost (per GB) |
|---|---|
| AWS → Internet (first 100 GB) | $0 (free) |
| AWS → Internet (100GB-10TB) | $0.09 |
| AWS → Internet (>10TB tier giảm) | $0.085-0.05 |
| AWS region → AWS region (same continent) | $0.02 |
| AWS region → AWS region (cross continent) | $0.02-0.05 |
| AWS → GCP (counted as internet egress) | $0.09 |
| GCP → Internet | $0.085-0.12 (varies by region) |
| GCP → AWS | $0.085-0.12 |
| Azure → Internet | $0.087 |
| **Cloudflare R2 → Internet** | **$0** (no egress!) |
| **Cloudflare R2 → anywhere** | **$0** |
| Backblaze B2 → Internet | $0.01 |

### Cách giảm egress fee

**Strategy 1: Same-region across cloud**
- Đặt workload AWS Singapore + GCP Singapore → latency low + có thể dùng dedicated interconnect (xem bài 02).

**Strategy 2: Use Cloudflare R2 cho cold storage / served data**
- Acme Shop: 50TB images user upload → lưu R2, served qua Cloudflare CDN.
- Saving so với S3: $4,500/tháng egress + $1,150 storage = **save ~$4,500/tháng** (chỉ trả storage).

**Strategy 3: Compress / dedupe before egress**
- Parquet thay vì JSON: 70% size reduction.
- Snappy compression for streaming.
- Acme Shop: log data 10TB/tháng compressed → 3TB. Save $630/tháng.

**Strategy 4: AWS Direct Connect / GCP Cloud Interconnect**
- Dedicated line: $0.02/GB egress (vs $0.09).
- Setup cost: $1K-3K/tháng port + $0.30/Mbps cross-connect.
- Worth it nếu >5TB/tháng egress.

**Strategy 5: AWS Savings Plan / EDP egress discount**
- EDP commitment 3 năm có thể negotiate 50% egress discount.
- Spot egress credit từ AWS partner program.

### Data gravity analysis

Acme Shop chốt: data nằm đâu lâu nhất → cloud đó là "home".
- **50TB user uploads** trên S3 đã 3 năm → migrate cost > value, stay AWS.
- **5TB ML training data** mới upload tháng này → có thể đặt GCP từ đầu.

→ **Quy tắc data gravity**: data lớn + cũ → khó move. Tránh let-it-grow ở cloud bạn không muốn lock.

---

## 5️⃣ Framework tính exit cost cụ thể

Acme Shop dùng framework này pitch sếp:

### Step 1: Inventory service đang dùng

```
Service          | Tier | Volume       | Critical?
-----------------|------|--------------|----------
S3               | 1    | 50TB        | Y
EC2              | 1    | 200 inst    | Y
EKS              | 1    | 3 cluster   | Y
RDS Postgres     | 1    | 5 db        | Y
DynamoDB         | 3    | 3 tables    | Y
Lambda           | 2    | 20 fn       | Y
Cognito          | 3    | 500K user   | Y
CloudFront       | 1    | -            | Y
SQS              | 2    | 15 queue    | N
SES              | 3    | 100K/d email | N
Bedrock          | 4    | -            | N
```

### Step 2: Estimate per-tier cost

| Tier | Cost formula | Acme Shop |
|---|---|---|
| 1 | Egress + Terraform rewrite | $4,500 + 1 eng × 2 mo = **$24K** |
| 2 | Rewrite glue code + retesting | 2 eng × 3 mo = **$60K** |
| 3 | Re-model + migrate data | 4 eng × 6 mo = **$240K** |
| 4 | Re-architect business logic | 2 eng × 3 mo = **$60K** |
| Dual-running | 3 month overlapping | $50K cloud bill extra |
| Training | New cloud certs + courses | $30K |
| **Total** | | **~$464K + 6 months** |

### Step 3: Identify quick wins to reduce exit cost

| Action | Saving |
|---|---|
| Migrate DynamoDB usage → Postgres JSONB (where possible) | -$120K (drop tier 3) |
| Stop using Bedrock (use OpenAI direct) | -$60K (drop tier 4) |
| Re-architect Lambda → containerized (Cloud Run portable) | -$30K (tier 2 → tier 1) |
| Adopt S3 API everywhere (no AWS SDK-specific feature) | -$10K |
| **Reduced exit cost** | **~$244K** |

→ Spending $50K trong 12 tháng để giảm exit cost xuống $244K (giảm 47%) — ROI rõ ràng.

### Step 4: Decision

| Scenario | Acme Shop làm |
|---|---|
| AWS giá tăng <20% | Stay AWS, exit cost không xứng |
| AWS giá tăng 20-40% | Pilot 1 workload sang GCP, đo savings |
| AWS giá tăng >40% | Plan full migration trong 12 tháng |
| Regulatory force | Buộc phải, dù exit cost cao |

→ Đây là **leverage** Acme Shop dùng đàm phán AWS — show them exit plan đã sẵn.

---

## 6️⃣ Hands-on — Terraform module portable cho S3 / GCS

Mục tiêu: viết 1 module Terraform tạo object storage, dùng được trên AWS hoặc GCP.

### Setup

```bash
mkdir terraform-portable-bucket && cd terraform-portable-bucket
mkdir modules/object-storage
```

### File: `modules/object-storage/variables.tf`

```hcl
variable "cloud" {
  type    = string
  default = "aws"
  validation {
    condition     = contains(["aws", "gcp"], var.cloud)
    error_message = "Cloud must be 'aws' or 'gcp'."
  }
}

variable "bucket_name" {
  type = string
}

variable "region" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}
```

### File: `modules/object-storage/aws.tf`

```hcl
resource "aws_s3_bucket" "this" {
  count  = var.cloud == "aws" ? 1 : 0
  bucket = var.bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "this" {
  count  = var.cloud == "aws" ? 1 : 0
  bucket = aws_s3_bucket.this[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  count  = var.cloud == "aws" ? 1 : 0
  bucket = aws_s3_bucket.this[0].id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

### File: `modules/object-storage/gcp.tf`

```hcl
resource "google_storage_bucket" "this" {
  count    = var.cloud == "gcp" ? 1 : 0
  name     = var.bucket_name
  location = var.region
  labels   = var.tags

  versioning {
    enabled = true
  }

  uniform_bucket_level_access = true
}
```

### File: `modules/object-storage/outputs.tf`

```hcl
output "bucket_name" {
  value = var.cloud == "aws" ? (
    length(aws_s3_bucket.this) > 0 ? aws_s3_bucket.this[0].id : null
  ) : (
    length(google_storage_bucket.this) > 0 ? google_storage_bucket.this[0].name : null
  )
}

output "bucket_url" {
  value = var.cloud == "aws" ? (
    length(aws_s3_bucket.this) > 0 ? "s3://${aws_s3_bucket.this[0].id}" : null
  ) : (
    length(google_storage_bucket.this) > 0 ? "gs://${google_storage_bucket.this[0].name}" : null
  )
}
```

### File: `main.tf` (caller)

```hcl
terraform {
  required_providers {
    aws    = { source = "hashicorp/aws",    version = "~> 5.0" }
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

provider "google" {
  project = "acmeshop-prod"
  region  = "asia-southeast1"
}

# Bucket A: AWS
module "uploads_bucket_aws" {
  source      = "./modules/object-storage"
  cloud       = "aws"
  bucket_name = "acmeshop-uploads-aws"
  region      = "ap-southeast-1"
  tags        = { Env = "prod", App = "uploads" }
}

# Bucket B: GCP — same module, same interface
module "uploads_bucket_gcp" {
  source      = "./modules/object-storage"
  cloud       = "gcp"
  bucket_name = "acmeshop-uploads-gcp"
  region      = "asia-southeast1"
  tags        = { env = "prod", app = "uploads" }
}

output "aws_bucket_url" {
  value = module.uploads_bucket_aws.bucket_url
}

output "gcp_bucket_url" {
  value = module.uploads_bucket_gcp.bucket_url
}
```

### Run

```bash
terraform init
terraform plan
terraform apply
```

Kết quả mong đợi:

```
aws_bucket_url = "s3://acmeshop-uploads-aws"
gcp_bucket_url = "gs://acmeshop-uploads-gcp"
```

→ Cùng 1 module interface, 2 cloud khác nhau. Khi cần đổi cloud, change `cloud = "aws"` → `cloud = "gcp"`.

**⚠️ Lưu ý**:
- Module này là **Level 1 abstraction** (Terraform tool-level). Resource code vẫn riêng per cloud.
- KHÔNG abstract data plane — app code dùng `boto3` (AWS) hay `google-cloud-storage` (GCP) riêng. Để portable hơn, dùng S3-compatible library (`minio-py`, `boto3` trỏ về GCS interop endpoint).

---

## 7️⃣ Strategy giảm lock-in từ ngày 0

🪞 **Ẩn dụ**: *Như **đi thuê nhà mà giữ option mua** — không bám rễ quá sâu nếu chưa chắc ở lâu.*

### Principle 1: Prefer open standard

| Choice | Vì sao |
|---|---|
| PostgreSQL / MySQL > DynamoDB | SQL chuẩn, portable |
| K8s > ECS | CNCF standard |
| S3 API (boto3 with custom endpoint) > AWS SDK exclusive | Cloudflare R2, MinIO, GCS đều support |
| Open Telemetry > CloudWatch SDK | Vendor-neutral telemetry |
| Redis (open protocol) > vendor-managed only | Self-host fallback |

### Principle 2: Keep stateful at edges

- Stateless compute (Lambda, container) dễ move.
- Stateful (DB, object storage) khó move.
- → Centralize state ở 1-2 service, keep rest stateless.

### Principle 3: Use S3 SDK with endpoint flag

```python
# Code này chạy được cả S3, R2, GCS interop, MinIO
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='https://storage.googleapis.com',  # GCS interop
    # endpoint_url='https://<account>.r2.cloudflarestorage.com',  # R2
    # endpoint_url=None,  # AWS S3 default
)

s3.put_object(Bucket='acmeshop-data', Key='file.txt', Body=b'hello')
```

→ Switching object storage = change 1 environment variable.

### Principle 4: Avoid "magic glue" services

- Step Functions: high lock (ASL specific) → prefer Airflow / Temporal (portable).
- AWS Glue ETL: high lock → prefer dbt + Airflow.
- EventBridge: medium → consider Kafka self-host nếu cross-cloud.

### Principle 5: Don't abstract until you have 2 clouds

🪞 *Đừng xây cây cầu trước khi có 2 bờ sông.*

- Build clean code with dependency injection (DB driver, storage client).
- Khi ngày đó đến — abstract dễ vì code đã clean.
- Build abstraction premature = chôn engineering trong cái chưa cần.

---

## 💡 Pitfall thường gặp & Best practice

### ❌ Pitfall 1: Đếm chỉ cost compute khi exit, bỏ qua opportunity cost

- **Triệu chứng**: Pitch "rời AWS save $200K/năm cloud bill".
- **Nguyên nhân**: Quên đếm 6 tháng team chậm tiến → mất $500K opportunity (feature ship trễ).
- **Cách tránh**: Exit cost = (engineering time × opportunity cost) + (extra cloud bill during transition) + training + tooling.

### ❌ Pitfall 2: "Standard SQL" không thật sự portable

- **Triệu chứng**: Code Postgres với JSONB query advanced → move sang Cloud SQL Postgres "tương thích" nhưng version 13 thay vì 15 → khác behavior.
- **Nguyên nhân**: Cloud cung cấp Postgres nhưng giới hạn version + extension list.
- **Cách tránh**: Stick to standard SQL features; document version + extension dependencies; test với target cloud version.

### ❌ Pitfall 3: Build "MyCompany Cloud SDK"

- **Triệu chứng**: 3 engineer ngồi xây "internal cloud abstraction" 9 tháng.
- **Nguyên nhân**: NIH syndrome (Not Invented Here).
- **Cách tránh**: Dùng Crossplane / Pulumi đã có. Nếu thật sự cần custom, build incrementally khi có nhu cầu cụ thể.

### ❌ Pitfall 4: Lock-in giả vì lười tận dụng

- **Triệu chứng**: "Đã trên AWS rồi nên dùng SES luôn" → 6 tháng sau khó switch.
- **Nguyên nhân**: Lười evaluate alternative.
- **Cách tránh**: Set policy — service vendor-specific phải approve qua Cloud Architect.

### ✅ Best practice 1: Tag service theo tier

- Resource tag: `lock-in-tier: 1|2|3|4`.
- Cost Explorer breakdown by tier → biết % spend trên service high-lock.

### ✅ Best practice 2: Yearly lock-in review

- Q4 mỗi năm: re-evaluate exit cost.
- Identify quick wins giảm tier 3-4 service.
- Track metric: % budget on tier 1-2 vs tier 3-4 (target >80% tier 1-2).

### ✅ Best practice 3: Negotiate annually with vendor

- AWS rep know your exit cost? Show them.
- Demand discount or features.
- Don't be afraid to threaten leaving — but only if your portability plan is real.

---

## 🧠 Self-check

**Q1.** Cloud-portable và cloud-native có mâu thuẫn không?

<details>
<summary>💡 Đáp án</summary>

**Có ở mức service-specific, nhưng KHÔNG ở mức kiến trúc**.

- Service-specific: AWS Lambda (cloud-native AWS) thì không portable.
- Kiến trúc: K8s + container (cloud-native pattern) thì rất portable.

→ Pick "cloud-native pattern" thay vì "cloud-native service" để giữ cả 2 lợi ích.

</details>

**Q2.** Acme Shop có 5 RDS Postgres. Move sang Cloud SQL có dễ không?

<details>
<summary>💡 Đáp án</summary>

**Trung bình dễ** (Tier 1-2), với caveats:

1. **Schema portable** nếu dùng standard SQL.
2. **Logical replication** Postgres native → setup AWS RDS → Cloud SQL logical replication, sync, cutover.
3. **Caveats**:
   - Extension: vài extension AWS-specific (`rds_*`) không có ở Cloud SQL → check list.
   - Version: ensure version match (Cloud SQL có thể chậm hơn 1 minor version).
   - Performance: instance sizing model khác.
   - IAM: AWS IAM authentication không transfer → re-configure.

→ Ước tính: ~4 tuần per database cho production migration.

</details>

**Q3.** Egress cost AWS → GCP 50TB/lần. Strategy nào giảm?

<details>
<summary>💡 Đáp án</summary>

**Top 3 strategy**:

1. **AWS Direct Connect + GCP Cloud Interconnect** (cross-cloud private circuit): giảm egress từ $0.09 xuống $0.02-0.03/GB. Setup cost $2K/tháng port nhưng tiết kiệm lớn ở volume cao.
2. **Compress data trước khi egress**: Parquet + Snappy giảm 70% volume.
3. **Snowball / Transfer Appliance offline**: với 50TB+, AWS Snowball gửi physical disk có thể rẻ hơn (~$300/TB) + xử lý 1 tuần.

→ Combine: Snowball cho one-time migration + Direct Connect cho ongoing sync.

</details>

**Q4.** Acme Shop dùng DynamoDB cho session store. Có nên migrate ra Redis (open) không?

<details>
<summary>💡 Đáp án</summary>

**Có, hợp lý**:

- Session store = simple key-value, TTL — không cần DynamoDB advanced features (GSI, Streams).
- Redis (ElastiCache hoặc Memorystore hoặc self-host) portable across cloud.
- Cost: Redis thường rẻ hơn DynamoDB cho high-traffic session workload (DynamoDB charge per WCU/RCU).
- Migration effort: 2-3 tuần (rewrite client code, dual-write transition, cutover).

→ Drop tier 3 service → tier 1. Quick win cho portability.

</details>

**Q5.** Pulumi vs Terraform để abstract multi-cloud — pick which?

<details>
<summary>💡 Đáp án</summary>

**Mặc định Terraform** unless có nhu cầu cụ thể cho Pulumi:

| Tiêu chí | Terraform | Pulumi |
|---|---|---|
| Ecosystem | Lớn nhất (mọi provider) | Đang grow |
| Language | HCL (DSL) | TypeScript/Python/Go (real code) |
| Test | Limited | Full unit test (real code) |
| Team skill VN 2026 | Phổ biến | Hiếm |
| State management | Mature | Mature |
| Multi-cloud | Tốt (provider riêng per cloud) | Tốt (SDK abstraction nếu code custom) |

→ Pick Terraform nếu team standard. Pick Pulumi nếu team strong TS/Python + cần programmatic logic phức tạp.

</details>

---

## ⚡ Cheatsheet

### Tier nhanh

| Tier | Sample service | Exit cost |
|---|---|---|
| 1 (Low) | S3, EC2, RDS, EKS, K8s | 1-2 tuần |
| 2 (Medium) | Lambda, SQS, API Gateway, IAM | 1 tháng |
| 3 (High) | DynamoDB, Cognito, Step Functions, Kinesis | 3-6 tháng |
| 4 (Ultra) | Bedrock, GovCloud, Outposts | Re-design |

### Abstraction layer

| Level | Tool | Effort | Khi dùng |
|---|---|---|---|
| 1 | Terraform multi-provider | Low | Default cho mọi team |
| 2 | Crossplane | High | Enterprise multi-cloud thật sự |
| 3 | Pulumi / SDK riêng | Medium | Team strong dev lang |

### Egress fee tóm tắt

| Path | Cost/GB |
|---|---|
| AWS internet | $0.09 |
| AWS cross-region | $0.02 |
| AWS → GCP | $0.09 |
| Cloudflare R2 → anywhere | **$0** |
| Direct Connect / Interconnect | $0.02 |

### Quick principles

```
1. Default to open standard (Postgres, K8s, S3 API, OpenTelemetry)
2. Stateless compute > stateful service
3. Tag every resource with lock-in tier
4. Don't abstract until you have 2 clouds
5. Yearly review exit cost
```

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Vendor lock-in | Khóa nhà cung cấp | Khó rời vendor vì phụ thuộc |
| Data lock-in | Khóa data | Data lưu vendor format/volume khó move |
| API lock-in | Khóa API | Code gọi API riêng vendor |
| Skill lock-in | Khóa kỹ năng | Team chỉ biết 1 cloud |
| Contract lock-in | Khóa hợp đồng | Cam kết multi-year, penalty rời sớm |
| Egress fee | Phí xuất | Tiền khi data ra khỏi cloud |
| Data gravity | Trọng lực dữ liệu | Data lớn + cũ → khó move |
| EDP | Enterprise Discount Program | Hợp đồng discount AWS enterprise (3 năm) |
| RI / Reserved Instance | (AWS) | Cam kết VM 1-3 năm, giảm 30-70% |
| CUD | Committed Use Discount | Cam kết GCP 1-3 năm |
| Crossplane | (CNCF) | Multi-cloud control plane qua K8s CRD |
| Pulumi | (vendor) | IaC viết bằng TypeScript/Python/Go |
| OpenTofu | (open-source) | Fork Terraform sau license change 2023 |
| Abstraction layer | Lớp trừu tượng | Code/tool che giấu khác biệt vendor |
| Cloud-portable | Có thể chuyển | Move giữa cloud trong vài tuần |
| Cloud-agnostic | Trung lập | Chạy được trên mọi cloud |
| Tier service | Phân tầng dịch vụ | Phân loại theo mức lock-in (1-4) |
| S3 API compatible | Tương thích API S3 | Cloud khác (R2, GCS, MinIO) implement S3 protocol |
| Logical replication | Sao chép logic | Postgres native cross-version replication |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ← Trước: [00_what-is-multi-cloud-overview.md](00_what-is-multi-cloud-overview.md)
- → Tiếp: [02_multi-cloud-network-and-identity.md](02_multi-cloud-network-and-identity.md)
- ↑ Cluster: [Multi-cloud-strategies README](../../README.md)

### Cross-reference
- 🏗️ [IaC Terraform](../../../../10_DevOps/iac/) — Terraform multi-provider
- ☸️ [Kubernetes](../../../../10_DevOps/kubernetes/) — portable runtime
- ☁️ [Cloud Cost Management](../../../cloud-cost-management/) — exit cost trong FinOps
- 🗄️ [PostgreSQL](../../../../05_Database/postgres/) — portable SQL
- 📦 [S3 deep + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — S3 specifics

### Tài nguyên ngoài (2026)
- 📖 [HashiCorp Terraform Multi-cloud guide](https://www.terraform.io/use-cases/multi-cloud-deployment)
- 📖 [Crossplane.io docs](https://docs.crossplane.io/)
- 📖 [Pulumi multi-cloud](https://www.pulumi.com/docs/concepts/cloud/)
- 📖 [OpenTofu (Terraform fork)](https://opentofu.org/)
- 📖 [Cloudflare R2 — Zero egress fee](https://developers.cloudflare.com/r2/)
- 📖 [AWS Egress pricing](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer)
- 📖 [GCP Network pricing](https://cloud.google.com/vpc/network-pricing)
- 📖 [The Hidden Costs of Cloud Lock-in — A16Z](https://a16z.com/the-cost-of-cloud-a-trillion-dollar-paradox/)
- 📖 [Data Gravity concept — McCrory](https://datagravity.org/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 01 cluster Multi-cloud basic. 4 dimension lock-in (data/API/skill/contract) + tier service (low/medium/high/ultra) + 3 level abstraction (Terraform/Crossplane/Pulumi) + egress fee reality 2026 + framework tính exit cost + hands-on Terraform module portable S3/GCS + 5 principles giảm lock-in từ ngày 0. Acme Shop $464K exit cost analysis làm trục chính.
