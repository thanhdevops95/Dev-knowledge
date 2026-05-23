# ☁️ Module 3.2: AWS Core Services

[![Duration](https://img.shields.io/badge/Duration-1--2%20weeks-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **AWS Fundamentals** - Core services for DevOps on AWS.
>
> *Nền tảng AWS - Các dịch vụ cốt lõi cho DevOps trên AWS.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Launch EC2 instances and Auto Scaling (Khởi chạy EC2 và Auto Scaling)
- ✅ Configure S3 storage and policies (Cấu hình S3 và policies)
- ✅ Manage IAM roles and policies (Quản lý IAM roles và policies)
- ✅ Deploy RDS databases (Deploy databases RDS)
- ✅ Create Lambda serverless functions (Tạo hàm Lambda serverless)
- ✅ Setup CloudWatch monitoring (Thiết lập giám sát CloudWatch)
- ✅ Master AWS CLI (Thành thạo AWS CLI)

---

## 📚 Content (Nội dung)

### 1. AWS Introduction (Giới thiệu AWS)

#### What is AWS? (AWS là gì?)

**Amazon Web Services (AWS)** is the world's largest cloud computing platform, offering over 200 services from data centers around the globe. Instead of buying physical servers, you "rent" computing resources on demand.

*AWS là nền tảng điện toán đám mây lớn nhất thế giới, cung cấp hơn 200 dịch vụ từ các trung tâm dữ liệu toàn cầu. Thay vì mua server vật lý, bạn "thuê" tài nguyên tính toán theo nhu cầu.*

#### Why DevOps needs AWS? (Tại sao DevOps cần học AWS?)

| Reason (Lý do) | Explanation (Giải thích) |
|----------------|--------------------------|
| **Job market** | AWS holds ~33% cloud market share, most companies use AWS *(AWS chiếm ~33% thị phần cloud)* |
| **Automation** | Everything on AWS can be automated via CLI/API *(Mọi thứ đều có thể tự động hóa)* |
| **Infrastructure as Code** | Terraform, CloudFormation help manage infrastructure as code *(Quản lý hạ tầng bằng code)* |
| **Scalability** | Auto scale up/down based on demand *(Tự động mở rộng/thu hẹp theo nhu cầu)* |

---

### 2. EC2 - Elastic Compute Cloud

#### What is EC2? (EC2 là gì?)

**EC2** allows you to create virtual servers on the cloud. You choose the CPU, RAM, storage configuration and only pay for the time you use.

*EC2 là dịch vụ cho phép bạn tạo máy chủ ảo (virtual server) trên cloud. Bạn có thể chọn cấu hình CPU, RAM, storage và chỉ trả tiền cho thời gian sử dụng.*

#### When to use EC2? (Khi nào dùng EC2?)

- Run web server, API server *(Chạy web server, API server)*
- Host applications needing custom configuration *(Host ứng dụng cần cấu hình tùy chỉnh)*
- Development/staging environments *(Môi trường development/staging)*

#### How to create EC2 instance (Cách tạo EC2 instance)

The command below creates an EC2 instance with basic configuration:

*Lệnh dưới đây tạo một EC2 instance với cấu hình cơ bản:*

```bash
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name mykey \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0
```

**Parameter explanation:** *(Giải thích từng tham số:)*

- `--image-id`: AMI (Amazon Machine Image) - base OS (Ubuntu, Amazon Linux...) *(hệ điều hành base)*
- `--instance-type`: Machine config (t3.micro = 2 vCPU, 1GB RAM - free in Free Tier) *(Cấu hình máy - miễn phí trong Free Tier)*
- `--key-name`: SSH key to access server *(SSH key để truy cập server)*
- `--security-group-ids`: Firewall rules (open ports, allowed IPs) *(mở port nào, cho IP nào truy cập)*
- `--subnet-id`: Subnet in VPC to place instance *(Mạng con trong VPC để đặt instance)*

---

### 3. S3 - Simple Storage Service

#### What is S3? (S3 là gì?)

**S3** is an object storage service with 99.999999999% durability. You can store unlimited data and access it from anywhere via HTTP.

*S3 là dịch vụ lưu trữ object (file) với độ bền 99.999999999% (11 số 9). Bạn có thể lưu trữ không giới hạn dung lượng, truy cập từ bất kỳ đâu qua HTTP.*

#### Common Use Cases (Các trường hợp sử dụng phổ biến)

- **Static website hosting** - Host static website (HTML, CSS, JS) *(Host website tĩnh)*
- **Backup and archive** - Store backups, log files *(Lưu trữ backup, log files)*
- **Data lake** - Data warehouse for analytics *(Kho dữ liệu cho analytics)*
- **CI/CD artifacts** - Store build outputs, Docker images *(Lưu build outputs, Docker images)*

#### Working with S3 (Thao tác với S3)

```bash
# 1. Create bucket - bucket name must be globally unique
# (Tạo bucket - tên bucket phải unique toàn cầu)
aws s3 mb s3://my-company-devops-bucket-2026

# 2. Upload a file (Upload một file)
aws s3 cp myfile.txt s3://my-company-devops-bucket-2026/

# 3. Sync entire directory (like rsync)
# (Đồng bộ toàn bộ thư mục)
aws s3 sync ./build s3://my-company-devops-bucket-2026/website

# 4. Download file
aws s3 cp s3://my-company-devops-bucket-2026/myfile.txt ./downloaded.txt
```

---

### 4. IAM - Identity and Access Management

#### What is IAM? (IAM là gì?)

**IAM** controls who is allowed to do what on AWS. It's the "security guard" of your entire AWS account, critical for security.

*IAM kiểm soát ai được phép làm gì trên AWS. Đây là "bảo vệ" của toàn bộ tài khoản AWS, cực kỳ quan trọng cho bảo mật.*

#### IAM Components (Các thành phần IAM)

| Component (Thành phần) | Description (Mô tả) | Example (Ví dụ) |
|------------------------|---------------------|-----------------|
| **User** | A person or application *(Một người hoặc ứng dụng)* | developer-john, ci-cd-bot |
| **Group** | Users with same permissions *(Nhóm users có cùng quyền)* | developers, admins |
| **Role** | Temporary permissions for services *(Quyền tạm thời cho services)* | EC2 needs to read S3 |
| **Policy** | JSON document defining permissions *(Document JSON định nghĩa quyền)* | Allow read/write to S3 |

#### IAM Policy Example (Ví dụ IAM Policy)

The policy below allows reading and writing to a specific S3 bucket:

*Policy dưới đây cho phép đọc và ghi vào một S3 bucket cụ thể:*

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

**Explanation:** *(Giải thích:)*

- `Effect`: Allow or Deny *(Allow hoặc Deny)*
- `Action`: Allowed actions (s3:GetObject = download, s3:PutObject = upload) *(Hành động được phép)*
- `Resource`: Resource to apply (ARN of bucket) *(Tài nguyên áp dụng - ARN của bucket)*

---

### 5. Lambda - Serverless Functions

#### What is Lambda? (Lambda là gì?)

**Lambda** lets you run code without managing servers. You only pay when your code actually runs (billed per millisecond).

*Lambda cho phép bạn chạy code mà không cần quản lý server. Bạn chỉ trả tiền khi code thực sự chạy (tính theo millisecond).*

#### When to Use Lambda? (Khi nào dùng Lambda?)

- **API endpoints** - Handle HTTP requests *(Xử lý HTTP requests)*
- **Event processing** - Process when new file is uploaded to S3 *(Xử lý khi có file mới upload lên S3)*
- **Scheduled tasks** - Run cron jobs (cleanup, reports) *(Chạy cron jobs - dọn dẹp, báo cáo)*
- **Webhooks** - Receive notifications from external services *(Nhận notifications từ external services)*

#### Lambda Function Example (Ví dụ Lambda function)

```python
# lambda_function.py
import json

def lambda_handler(event, context):
    """
    Handler called every time Lambda is triggered.
    - event: Input data (HTTP request, S3 event...)
    - context: Metadata about the execution (memory, timeout...)
    """
    name = event.get('name', 'World')
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Hello, {name}!')
    }
```

**How to deploy Lambda:** *(Cách deploy Lambda:)*

```bash
# Package code (Đóng gói code)
zip function.zip lambda_function.py

# Create function on AWS (Tạo function trên AWS)
aws lambda create-function \
  --function-name hello-world \
  --runtime python3.9 \
  --role arn:aws:iam::123456789:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.1 Network Advanced](../3.1_Network_Advanced/) | **3.2 AWS Core** | [3.3 Databases](../3.3_Databases_for_DevOps/) |

---

**Master AWS cloud services! ☁️**

*Thành thạo dịch vụ đám mây AWS!*

</div>
