# ☁️ Cloud Computing — AWS, Azure, GCP

> `[INTERMEDIATE]` — Hạ tầng trên đám mây cho mọi quy mô

---

## Cloud là gì?

**Cloud Computing** = Thuê tài nguyên máy tính (server, storage, database, networking...) qua Internet thay vì tự mua phần cứng.

**3 mô hình dịch vụ:**

| Model | Bạn quản lý | Cloud quản lý | Ví dụ |
|---|---|---|---|
| **IaaS** (Infrastructure) | OS, Runtime, App | Hardware, Network | EC2, Azure VM |
| **PaaS** (Platform) | App, Data | OS, Runtime, Hardware | Heroku, App Engine |
| **SaaS** (Software) | Không gì cả | Tất cả | Gmail, Slack |

**3 nhà cung cấp lớn:**

| | AWS | Azure | GCP |
|---|---|---|---|
| **Thị phần** | ~33% | ~22% | ~11% |
| **Mạnh về** | Tổng thể, nhất mature | Enterprise, Microsoft | Data, ML, Kubernetes |
| **Khuyên học** | Nếu không biết chọn gì | Nếu dùng Microsoft stack | Nếu focus Data/ML |

---

## AWS — Amazon Web Services

### Các dịch vụ cốt lõi

#### Compute
```
EC2 (Elastic Compute Cloud)
  → Virtual machines (VMs)
  → Chọn instance type: t3.micro (test), c5.large (CPU), r5.large (RAM)

Lambda
  → Serverless functions
  → Trả tiền theo số lần gọi, không phải theo giờ
  → Tốt cho: API endpoints, event processing, scheduled tasks

ECS / EKS
  → Container orchestration
  → ECS: AWS-native Docker
  → EKS: Managed Kubernetes
```

#### Storage
```
S3 (Simple Storage Service)
  → Object storage, unlimited
  → Dùng cho: ảnh, video, backup, static website
  → Pricing: ~$0.023/GB/tháng

EBS (Elastic Block Store)
  → Block storage gắn vào EC2 (như ổ cứng)

EFS (Elastic File System)
  → Shared file system, nhiều EC2 cùng dùng

RDS (Relational Database Service)
  → Managed: PostgreSQL, MySQL, MariaDB, Oracle
  → Auto backup, multi-AZ failover

DynamoDB
  → NoSQL serverless, cực scale
  → Single-digit millisecond latency
```

#### Networking
```
VPC (Virtual Private Cloud)
  → Mạng riêng ảo của bạn trên AWS

Subnet
  → Public: có Internet Gateway
  → Private: không ra internet trực tiếp

Internet Gateway → Kết nối VPC ra internet

NAT Gateway → Private subnet ra internet (1 chiều)

Route 53 → DNS service

CloudFront → CDN

ALB/NLB → Load Balancer
  → ALB: Layer 7 (HTTP/HTTPS)
  → NLB: Layer 4 (TCP/UDP)
```

#### Identity & Security
```
IAM (Identity and Access Management)
  → Users, Groups, Roles, Policies
  → Nguyên tắc: Least Privilege

Security Groups → Firewall cho EC2/RDS
NACL → Firewall cho Subnet level
KMS → Encryption key management
Secrets Manager → Lưu secrets an toàn
```

---

### Kiến trúc 3-tier điển hình trên AWS

```
Internet
    │
    ▼
Route 53 (DNS)
    │
    ▼
CloudFront (CDN)
    │
    ▼
ALB (Application Load Balancer)
    │
    ├──► EC2 / ECS (App tier) — Private subnet
    │         │
    │         ▼
    │    RDS PostgreSQL (DB tier) — Private subnet
    │         │
    │    ElastiCache Redis — Private subnet
    │
    └──► S3 (Static assets)
```

---

### AWS CLI & SDK

```bash
# Cài và cấu hình
brew install awscli
aws configure
# AWS Access Key ID: ...
# AWS Secret Access Key: ...
# Default region: ap-southeast-1

# S3
aws s3 ls                              # List buckets
aws s3 ls s3://my-bucket              # List files
aws s3 cp file.txt s3://my-bucket/    # Upload
aws s3 sync ./dist s3://my-bucket     # Sync thư mục

# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0

# Logs
aws logs get-log-events --log-group-name /app/api --log-stream-name ...
```

```python
# Python SDK (boto3)
import boto3

# S3
s3 = boto3.client("s3", region_name="ap-southeast-1")
s3.upload_file("local.txt", "my-bucket", "remote.txt")
s3.download_file("my-bucket", "remote.txt", "local.txt")

# Generate presigned URL (cho phép upload từ browser)
url = s3.generate_presigned_url(
    "put_object",
    Params={"Bucket": "my-bucket", "Key": "image.jpg"},
    ExpiresIn=3600
)

# DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("users")
table.put_item(Item={"id": "123", "name": "Jesse"})
response = table.get_item(Key={"id": "123"})

# SES (Email)
ses = boto3.client("ses", region_name="ap-southeast-1")
ses.send_email(
    Source="noreply@example.com",
    Destination={"ToAddresses": ["user@example.com"]},
    Message={
        "Subject": {"Data": "Xác nhận đăng ký"},
        "Body": {"Text": {"Data": "Cảm ơn bạn đã đăng ký!"}}
    }
)
```

---

## Azure — Microsoft Cloud

### Dịch vụ tương đương AWS

| AWS | Azure | GCP |
|---|---|---|
| EC2 | Virtual Machines | Compute Engine |
| Lambda | Azure Functions | Cloud Functions |
| ECS/EKS | AKS (Kubernetes) | GKE |
| S3 | Blob Storage | Cloud Storage |
| RDS | Azure Database | Cloud SQL |
| DynamoDB | Cosmos DB | Firestore |
| IAM | Azure AD / Entra ID | IAM |
| CloudFront | Azure CDN | Cloud CDN |
| Route 53 | Azure DNS | Cloud DNS |
| CloudWatch | Azure Monitor | Cloud Monitoring |

### Azure Resource Groups

```
Subscription
  └── Resource Group (my-app-prod)
        ├── Virtual Network (VNet)
        │     └── Subnets
        ├── App Service (Web App)
        ├── Azure Database for PostgreSQL
        ├── Azure Cache for Redis
        ├── Storage Account
        └── Key Vault (Secrets)
```

---

## GCP — Google Cloud Platform

### Dịch vụ nổi bật

```
BigQuery
  → Data warehouse serverless, cực nhanh
  → Tốt nhất cho analytics queries

Vertex AI
  → Managed ML platform
  → Training, deployment, monitoring

GKE (Google Kubernetes Engine)
  → Kubernetes đẳng cấp nhất (Google tạo ra K8s)

Cloud Run
  → Serverless containers
  → Deploy Docker image, tự scale về 0

Cloud Pub/Sub
  → Message queue như Kafka

Firebase
  → Real-time database, Authentication, Hosting
  → Tốt cho mobile apps và startups nhanh
```

---

## Serverless — Pay per execution

```python
# AWS Lambda function
import json
import boto3

def handler(event, context):
    """
    event: Dict với data từ trigger
    context: Lambda execution context
    """
    body = json.loads(event.get("body", "{}"))
    name = body.get("name", "World")
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"message": f"Hello, {name}!"})
    }
```

```yaml
# serverless.yml (Serverless Framework)
service: my-api

provider:
  name: aws
  runtime: python3.12
  region: ap-southeast-1
  environment:
    DATABASE_URL: ${ssm:/my-app/database-url}

functions:
  hello:
    handler: handler.handler
    events:
      - http:
          path: /hello
          method: post
          cors: true
    timeout: 30
    memorySize: 256
```

---

## Cloud Cost Optimization

```
✅ Right-sizing — Chọn đúng instance type
✅ Reserved Instances / Savings Plans — Cam kết 1-3 năm để giảm ~30-60%
✅ Spot Instances (AWS) / Preemptible VMs (GCP) — Giảm ~60-90%
   → Dùng cho: batch jobs, CI/CD runners (stateless)
✅ Auto Scaling — Scale down khi ít tải
✅ S3 Lifecycle policies — Chuyển data cũ sang Glacier (rẻ hơn)
✅ CloudWatch billing alerts — Cảnh báo khi vượt ngưỡng
✅ Delete unused resources — Elastic IPs, Snapshots, Old AMIs
```

---

## Bài tập thực hành

- [ ] Tạo S3 bucket, upload file, tạo presigned URL
- [ ] Deploy một app đơn giản lên EC2 bằng tay
- [ ] Setup VPC với public/private subnets
- [ ] Dùng Terraform để provision toàn bộ hạ tầng trên → [../06-DevOps/iac/01-terraform.md](../06-DevOps/iac/01-terraform.md)

---

## Tài nguyên thêm

- [AWS Free Tier](https://aws.amazon.com/free/) — 12 tháng miễn phí nhiều dịch vụ
- [AWS Skill Builder](https://skillbuilder.aws/) — Khóa học chính thức
- [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) — Free credits cho labs
- [Azure Learn](https://learn.microsoft.com/en-us/azure/) — Microsoft Learn
- [Cloud Computing Concepts (Coursera)](https://www.coursera.org/learn/cloud-computing) — Nền tảng lý thuyết
