# ☁️ Cloud Computing — Điện toán đám mây

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hạ tầng cho mọi ứng dụng hiện đại

---

## Tại sao cần Cloud?

```
❌ Truyền thống (On-premises):
  Mua server → Đặt phòng máy → Chờ 2-4 tuần → Setup → Bảo trì 24/7
  Giá: $10,000+ upfront + $2,000/tháng điện + cooling + nhân sự

✅ Cloud:
  Đăng ký → Chọn cấu hình → 3 phút → Chạy → Tắt khi không dùng
  Giá: $5-500/tháng tùy dùng
```

---

## 1. Cloud Service Models

```
┌─────────────────────────────────────────────────────┐
│                On-Premises (tự quản lý hết)          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │App   │ │Data  │ │Runtime│ │OS    │ │Server│     │
│  │      │ │      │ │      │ │      │ │      │     │
│  │ BẠN  │ │ BẠN  │ │ BẠN  │ │ BẠN  │ │ BẠN  │     │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘     │
├─────────────────────────────────────────────────────┤
│                    IaaS                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │App   │ │Data  │ │Runtime│ │OS    │ │Server│     │
│  │ BẠN  │ │ BẠN  │ │ BẠN  │ │ BẠN  │ │CLOUD │     │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘     │
│  EC2, GCE, Azure VM                                 │
├─────────────────────────────────────────────────────┤
│                    PaaS                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │App   │ │Data  │ │Runtime│ │OS    │ │Server│     │
│  │ BẠN  │ │ BẠN  │ │CLOUD │ │CLOUD │ │CLOUD │     │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘     │
│  Heroku, App Engine, Azure App Service               │
├─────────────────────────────────────────────────────┤
│                    SaaS                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  │App   │ │Data  │ │Runtime│ │OS    │ │Server│     │
│  │CLOUD │ │CLOUD │ │CLOUD │ │CLOUD │ │CLOUD │     │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘     │
│  Gmail, Slack, Salesforce                            │
├─────────────────────────────────────────────────────┤
│                   Serverless (FaaS)                  │
│  ┌──────┐                                           │
│  │ Code │  ← Bạn CHỈ viết code, cloud lo phần còn lại│
│  │ BẠN  │  AWS Lambda, Cloud Functions              │
│  └──────┘                                           │
└─────────────────────────────────────────────────────┘
```

---

## 2. Core Services — So sánh 3 Cloud lớn

| Dịch vụ | AWS | Azure | GCP |
|---|---|---|---|
| **Compute** | EC2 | Virtual Machines | Compute Engine |
| **Serverless** | Lambda | Functions | Cloud Functions |
| **Containers** | ECS, EKS | AKS | GKE |
| **Object Storage** | S3 | Blob Storage | Cloud Storage |
| **Database (SQL)** | RDS | SQL Database | Cloud SQL |
| **Database (NoSQL)** | DynamoDB | Cosmos DB | Firestore |
| **Cache** | ElastiCache | Cache for Redis | Memorystore |
| **CDN** | CloudFront | Azure CDN | Cloud CDN |
| **DNS** | Route53 | Azure DNS | Cloud DNS |
| **Queue** | SQS | Service Bus | Pub/Sub |
| **AI/ML** | SageMaker | Azure ML | Vertex AI |
| **Monitoring** | CloudWatch | Monitor | Cloud Monitoring |

---

## 3. AWS — Dịch vụ phổ biến nhất

### EC2 — Virtual Server

```bash
# Tạo EC2 instance (AWS CLI)
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.micro \
    --key-name my-key \
    --security-group-ids sg-12345 \
    --count 1

# Instance types:
# t3.micro:  1 vCPU, 1GB RAM    → Free tier, dev
# t3.medium: 2 vCPU, 4GB RAM    → Small app
# m5.large:  2 vCPU, 8GB RAM    → Production
# c5.xlarge: 4 vCPU, 8GB RAM    → CPU-intensive
# r5.large:  2 vCPU, 16GB RAM   → Memory-intensive
```

### S3 — Object Storage

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('image.jpg', 'my-bucket', 'uploads/image.jpg')

# Download
s3.download_file('my-bucket', 'uploads/image.jpg', 'local.jpg')

# Generate presigned URL (temporary access)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'uploads/image.jpg'},
    ExpiresIn=3600  # 1 giờ
)
```

### Lambda — Serverless Function

```python
# handler.py — AWS Lambda function
import json

def handler(event, context):
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }

# Trigger: API Gateway, S3 event, SQS message, cron schedule
# Chi phí: Trả theo số lần gọi + thời gian chạy
# Free tier: 1M requests/tháng + 400,000 GB-giây
```

---

## 4. Infrastructure as Code (IaC)

### Terraform

```hcl
# main.tf — Định nghĩa infrastructure bằng code
provider "aws" {
  region = "ap-southeast-1"  # Singapore
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "production-vpc" }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.micro"
  tags = { Name = "web-server" }
}

# RDS Database
resource "aws_db_instance" "db" {
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  db_name        = "myapp"
  username       = var.db_username
  password       = var.db_password
}
```

```bash
terraform init      # Khởi tạo
terraform plan      # Xem preview thay đổi
terraform apply     # Áp dụng thay đổi
terraform destroy   # Xóa tất cả resources
```

---

## 5. Well-Architected — 6 Trụ cột

| Trụ cột | Ý nghĩa | Ví dụ |
|---|---|---|
| **Security** | Bảo mật dữ liệu & truy cập | IAM, encryption, VPC |
| **Reliability** | Khả năng phục hồi | Multi-AZ, backup, auto-scaling |
| **Performance** | Hiệu năng tối ưu | Right-sizing, caching, CDN |
| **Cost** | Tối ưu chi phí | Reserved instances, spot instances |
| **Operations** | Vận hành tự động | CloudWatch, IaC, CI/CD |
| **Sustainability** | Bền vững | Rightsizing, serverless khi idle |

---

## 6. Cost Optimization

```
Tiết kiệm chi phí cloud:

1. Right-sizing: Chọn instance đúng nhu cầu (không quá lớn)
2. Reserved Instances: Cam kết 1-3 năm → giảm 30-70%
3. Spot Instances: Dùng capacity dư → giảm đến 90% (có thể bị interrupt)
4. Auto-scaling: Scale down khi traffic thấp
5. Serverless: Chỉ trả khi function chạy
6. S3 tiers: Frequently → Infrequent → Glacier (archive)
7. Delete unused: Elastic IPs, old snapshots, idle load balancers
```

---

## Các lỗi thường gặp

```
❌ Sai: Hardcode credentials (AWS keys) trong code
✅ Đúng: Dùng IAM roles, environment variables, secrets manager

❌ Sai: Single AZ deployment → 1 data center down = app down
✅ Đúng: Multi-AZ cho production

❌ Sai: Quên set billing alerts → hóa đơn $10,000 cuối tháng 💸
✅ Đúng: Set AWS Budget alerts ngay lập tức!

❌ Sai: Public S3 bucket → data leak
✅ Đúng: Block public access, use presigned URLs
```

---

## Bài tập thực hành

- [ ] Tạo AWS Free Tier account → launch EC2 → SSH vào → cài Nginx
- [ ] Upload file lên S3 bằng AWS CLI hoặc SDK
- [ ] Deploy Lambda function + API Gateway
- [ ] Viết Terraform config tạo EC2 + Security Group

---

## Tài nguyên thêm

- [AWS Free Tier](https://aws.amazon.com/free/) — 12 tháng miễn phí
- [Cloud Resume Challenge](https://cloudresumechallenge.dev/) — Project thực tế
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) — Best practices
