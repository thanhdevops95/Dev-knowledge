# Module 11: Cloud (AWS Fundamentals)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Cloud** | - | Điện toán đám mây - Thuê tài nguyên qua internet |
| **AWS** | - | Amazon Web Services - Cloud provider lớn nhất |
| **EC2** | - | Elastic Compute Cloud - Virtual servers |
| **S3** | - | Simple Storage Service - Object storage |
| **RDS** | - | Relational Database Service - Managed databases |
| **VPC** | - | Virtual Private Cloud - Mạng riêng ảo |
| **IAM** | - | Identity and Access Management - Quản lý quyền |
| **Lambda** | - | Serverless functions |
| **ECS** | - | Elastic Container Service |
| **EKS** | - | Elastic Kubernetes Service |
| **Region** | - | Vùng địa lý của datacenter |
| **Availability Zone** | - | AZ - Datacenter độc lập trong region |
| **Elastic** | - | Co giãn - Tăng/giảm tài nguyên tự động |

---

## 📖 Cloud Computing là gì? (Định nghĩa từ gốc)

### Trước hết: Server là gì?

**Server = Máy tính chạy 24/7 để phục vụ requests.**

Khi bạn mở website, máy tính của bạn (client) gửi request đến một server ở đâu đó. Server xử lý và trả về website.

**Trước khi có Cloud (On-Premises):**

Công ty muốn chạy website phải:

1. **Mua server vật lý** (Dell, HP) - $5,000-50,000
2. **Thuê chỗ đặt** trong datacenter (hoặc phòng server riêng)
3. **Thuê người quản trị** để cài đặt, bảo trì, thay thế phần cứng
4. **Dự đoán capacity** trước 1-3 năm

**Vấn đề:**

| Vấn đề | Ví dụ |
|--------|-------|
| **Chi phí ban đầu cao** | Mua 10 servers = $100,000 |
| **Scale chậm** | Cần thêm server = 2-4 tuần shipping |
| **Lãng phí** | 90% thời gian chỉ dùng 10% capacity |
| **Over-engineering** | Mua dư để phòng traffic spike |

### Cloud Computing giải quyết

> **Cloud = Thuê tài nguyên máy tính qua internet, trả tiền theo dùng**

Thay vì mua server, bạn **thuê** từ các Cloud Provider (AWS, Azure, GCP):

- **Không mua hardware** - Provider lo
- **Scale trong phút** - Click thêm server
- **Trả tiền theo giờ/phút** - Dùng bao nhiêu trả bấy nhiêu
- **Global** - Deploy ở 20+ regions trên thế giới

```
On-Premises:                        Cloud:
┌────────────────────────┐         ┌────────────────────────┐
│   Công ty của bạn      │         │   Cloud Provider       │
│                        │         │   (AWS/Azure/GCP)      │
│  ┌──────────────────┐  │         │  ┌──────────────────┐  │
│  │  Server vật lý   │  │         │  │  Virtual Server  │  │
│  │  (bạn mua)       │  │         │  │  (bạn thuê)      │  │
│  │  (bạn quản lý)   │  │         │  │  (họ quản lý HW) │  │
│  └──────────────────┘  │         │  └──────────────────┘  │
│                        │         │                        │
│  Chi phí: $50,000+     │         │  Chi phí: $50/tháng    │
│  Scale: 2-4 tuần       │         │  Scale: 5 phút         │
└────────────────────────┘         └────────────────────────┘
```

### AWS là gì trong bức tranh này?

> **AWS (Amazon Web Services) = Cloud Provider lớn nhất thế giới**

AWS là công ty của Amazon cung cấp hơn 200 services cho cloud computing:

- **Compute:** EC2 (virtual servers), Lambda (serverless)
- **Storage:** S3 (files), EBS (disks)
- **Database:** RDS (SQL), DynamoDB (NoSQL)
- **Networking:** VPC (private network), Route53 (DNS)
- **Và 200+ services khác...**

**Tại sao học AWS trước?**

- Market share: ~33% (lớn nhất)
- Nhiều job yêu cầu AWS nhất
- Services đầy đủ và mature nhất
- Kiến thức chuyển đổi được sang Azure/GCP

---

## 🎬 Câu chuyện thực tế

Bạn cần deploy website cho startup. Có 2 lựa chọn:

**Lựa chọn 1: On-Premises**

- Mua server: $10,000
- Thuê chỗ datacenter: $500/tháng
- Thuê admin: $2,000/tháng
- Thời gian setup: 2-4 tuần
- **Tổng năm đầu: ~$40,000**

**Lựa chọn 2: AWS**

- EC2 instance (t3.medium): ~$30/tháng
- Không cần thuê chỗ, không cần admin chuyên trách
- Thời gian setup: 10 phút
- **Tổng năm đầu: ~$360**

Đây là lý do **phần lớn startups và enterprise đều dùng Cloud**.

---

## 📖 AWS Core Services

AWS có hàng trăm services, nhưng DevOps Engineer chỉ cần master khoảng 10-15 services chính. Dưới đây là những services quan trọng nhất theo từng category:

### Compute - "Máy chủ"

Đây là nơi code của bạn chạy. Tùy theo nhu cầu mà chọn service phù hợp:

| Service | Description | Khi nào dùng |
|---------|-------------|--------------|
| **EC2** | Virtual servers | Cần full control, traditional apps |
| **ECS** | Container service | Docker containers, không cần K8s |
| **EKS** | Managed Kubernetes | K8s workloads, enterprise |
| **Lambda** | Serverless functions | Short tasks, event-driven |

> 💡 **Tip:** Bắt đầu với EC2 để hiểu cơ bản, sau đó học ECS/Lambda để tối ưu cost.

### Storage - "Lưu trữ"

Mỗi loại storage phù hợp với use case khác nhau:

| Service | Description | Khi nào dùng |
|---------|-------------|--------------|
| **S3** | Object storage | Files, backups, static websites |
| **EBS** | Block storage for EC2 | Database files, OS volumes |
| **EFS** | File system | Shared storage giữa nhiều EC2 |

> 💡 **Tip:** S3 là service bạn sẽ dùng nhiều nhất - lưu logs, backups, artifacts, static content.

### Database - "Cơ sở dữ liệu"

AWS quản lý database cho bạn - không cần lo backup, patching, scaling:

| Service | Description | Khi nào dùng |
|---------|-------------|--------------|
| **RDS** | Managed databases | PostgreSQL, MySQL, SQL Server |
| **DynamoDB** | NoSQL | High throughput, simple queries |
| **ElastiCache** | Redis/Memcached | Caching, sessions |

### Networking - "Mạng"

Để các services nói chuyện với nhau và với internet:

| Service | Description | Khi nào dùng |
|---------|-------------|--------------|
| **VPC** | Virtual network | Luôn cần - mạng riêng ảo |
| **Route53** | DNS | Domain management |
| **ALB/ELB** | Load balancers | Phân tải traffic |

---

## 🔧 AWS CLI

**Tại sao cần CLI?** Console (UI) tiện để học và explore, nhưng:

- Không thể automate
- Không thể version control
- Dễ sai sót khi click nhiều

**AWS CLI** cho phép bạn thực hiện mọi thứ qua command line, dễ dàng tích hợp vào scripts và CI/CD.

### Setup

```bash
# Cài đặt và cấu hình lần đầu
aws configure
# Nhập: Access Key, Secret Key, Region (vd: ap-southeast-1), Output format (json)
```

> ⚠️ **Bảo mật:** Không bao giờ commit Access Key lên Git. Dùng IAM roles cho EC2, environment variables cho local.

### EC2 Commands

```bash
# Xem tất cả EC2 instances
aws ec2 describe-instances

# Tạo EC2 instance mới
aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro

# Dừng/Khởi động instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

### S3 Commands (dùng nhiều nhất)

```bash
# Liệt kê tất cả buckets
aws s3 ls

# Upload file lên S3
aws s3 cp file.txt s3://mybucket/

# Sync folder (chỉ upload files thay đổi - rất hiệu quả)
aws s3 sync ./folder s3://mybucket/folder

# Download file
aws s3 cp s3://mybucket/file.txt ./
```

### ECS Commands

```bash
# Xem tất cả ECS clusters
aws ecs list-clusters

# Xem chi tiết service
aws ecs describe-services --cluster mycluster --services myservice

# Force new deployment (dùng khi cần re-pull image)
aws ecs update-service --cluster mycluster --service myservice --force-new-deployment
```

---

## 📝 Tổng kết

✅ AWS core services  
✅ CLI basics  
✅ IAM and security  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
