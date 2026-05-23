# Hướng dẫn AWS Basics

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Amazon Web Services (AWS) là nền tảng cloud computing phổ biến nhất thế giới.

---

## 🔑**CÁC DỊCH VỤ CHÍNH**

| Dịch vụ | Mô tả | Tương đương |
|---------|-------|-------------|
| **EC2** | Virtual servers | VPS |
| **S3** | Object storage | File storage |
| **RDS** | Managed database | MySQL, PostgreSQL |
| **Lambda** | Serverless functions | Cloud Functions |
| **CloudFront** | CDN | Cloudflare |
| **Route 53** | DNS | Cloudflare DNS |
| **IAM** | Identity & Access | User management |
| **VPC** | Virtual network | Private network |

---

## 💻**EC2 (Elastic Compute Cloud)**

### Tạo EC2 Instance

1. Vào **EC2 Dashboard** → **Launch Instance**
2. Chọn **AMI** (Amazon Machine Image): Ubuntu, Amazon Linux
3. Chọn **Instance Type**: t2.micro (Free Tier)
4. Cấu hình **Security Group**
5. Tạo **Key Pair** để SSH

### Kết nối SSH

```bash
# Đổi permission cho key
chmod 400 my-key.pem

# SSH vào instance
ssh -i my-key.pem ubuntu@<public-ip>

# Hoặc với Amazon Linux
ssh -i my-key.pem ec2-user@<public-ip>
```

### Security Group Rules

| Type | Port | Source | Mô tả |
|------|------|--------|-------|
| SSH | 22 | Your IP | Remote access |
| HTTP | 80 | 0.0.0.0/0 | Web traffic |
| HTTPS | 443 | 0.0.0.0/0 | Secure web |
| Custom TCP | 3000 | 0.0.0.0/0 | Node.js app |

---

## 📦**S3 (Simple Storage Service)**

### AWS CLI

```bash
# Cài đặt
pip install awscli

# Cấu hình
aws configure
# Nhập: Access Key, Secret Key, Region
```

### Thao tác với S3

```bash
# Liệt kê buckets
aws s3 ls

# Tạo bucket
aws s3 mb s3://my-bucket-name

# Upload file
aws s3 cp file.txt s3://my-bucket/

# Upload folder
aws s3 sync ./local-folder s3://my-bucket/folder

# Download
aws s3 cp s3://my-bucket/file.txt ./

# Xóa
aws s3 rm s3://my-bucket/file.txt
aws s3 rm s3://my-bucket/ --recursive
```

### Python với S3 (boto3)

```python
import boto3

s3 = boto3.client('s3')

# Upload file
s3.upload_file('local_file.txt', 'bucket-name', 'remote_file.txt')

# Download file
s3.download_file('bucket-name', 'remote_file.txt', 'local_file.txt')

# Upload với public read
s3.upload_file(
    'image.jpg', 
    'bucket-name', 
    'image.jpg',
    ExtraArgs={'ACL': 'public-read'}
)

# Liệt kê files
response = s3.list_objects_v2(Bucket='bucket-name')
for obj in response.get('Contents', []):
    print(obj['Key'])

# Generate presigned URL
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'bucket-name', 'Key': 'file.txt'},
    ExpiresIn=3600  # 1 hour
)
```

---

## 🗄️**RDS (Relational Database Service)**

### Tạo RDS Instance

1. Vào **RDS Dashboard** → **Create database**
2. Chọn engine: MySQL, PostgreSQL, etc.
3. Chọn template: Free tier
4. Cấu hình credentials
5. Cấu hình VPC và Security Group

### Kết nối

```python
import psycopg2

conn = psycopg2.connect(
    host="my-db.xxx.rds.amazonaws.com",
    database="mydb",
    user="admin",
    password="password"
)
```

```bash
# MySQL
mysql -h my-db.xxx.rds.amazonaws.com -u admin -p

# PostgreSQL
psql -h my-db.xxx.rds.amazonaws.com -U admin -d mydb
```

---

## ⚡**LAMBDA**

### Tạo Lambda Function

1. Vào **Lambda** → **Create function**
2. Chọn runtime: Python 3.11
3. Viết code
4. Cấu hình trigger (API Gateway, S3, etc.)

### Lambda Handler (Python)

```python
import json

def lambda_handler(event, context):
    # event: Input data
    # context: Runtime information
    
    name = event.get('name', 'World')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Hello, {name}!'
        })
    }
```

### Deploy với ZIP

```bash
# Tạo ZIP
zip -r function.zip lambda_function.py

# Upload (CLI)
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip
```

### Lambda với Dependencies

```bash
# Tạo folder
mkdir package

# Cài dependencies vào folder
pip install requests -t package/

# Copy code
cp lambda_function.py package/

# Tạo ZIP
cd package
zip -r ../deployment.zip .
```

---

## 🌐**API GATEWAY**

### Tạo REST API

1. Vào **API Gateway** → **Create API**
2. Chọn **REST API**
3. Tạo **Resource** và **Method**
4. Integrate với Lambda
5. **Deploy** API

### Endpoint URL

```
https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/users
```

---

## 👤**IAM (Identity and Access Management)**

### Tạo User

1. Vào **IAM** → **Users** → **Add user**
2. Chọn **Programmatic access**
3. Attach policies
4. Lưu **Access Key** và **Secret Key**

### Policies phổ biến

| Policy | Mô tả |
|--------|-------|
| `AdministratorAccess` | Full access (chỉ admin) |
| `AmazonS3FullAccess` | Full S3 access |
| `AmazonS3ReadOnlyAccess` | Read-only S3 |
| `AmazonEC2FullAccess` | Full EC2 access |
| `AWSLambdaFullAccess` | Full Lambda access |

### Custom Policy (JSON)

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

---

## 🌩️**CLOUDFRONT (CDN)**

### Tạo Distribution

1. Vào **CloudFront** → **Create Distribution**
2. Origin: S3 bucket hoặc EC2
3. Cấu hình cache behavior
4. Chờ deploy (~15 phút)

### URL

```
https://dxxxxxxxxxx.cloudfront.net/image.jpg
```

---

## 📊**CLOUDWATCH**

### Xem Logs

```bash
# CLI
aws logs tail /aws/lambda/my-function --follow
```

### Tạo Alarm

1. Vào **CloudWatch** → **Alarms**
2. Chọn metric (CPU, Memory, etc.)
3. Đặt threshold
4. Cấu hình notification (SNS)

---

## 💰**CHI PHÍ & FREE TIER**

### Free Tier (12 tháng đầu)

| Dịch vụ | Free |
|---------|------|
| EC2 | 750h t2.micro/tháng |
| S3 | 5GB storage |
| RDS | 750h db.t2.micro |
| Lambda | 1M requests/tháng |
| CloudFront | 50GB transfer |

### Tránh phát sinh phí

- [ ] Set billing alerts
- [ ] Tắt EC2 khi không dùng
- [ ] Xóa EBS volumes không dùng
- [ ] Dùng S3 Lifecycle rules
- [ ] Chọn region gần nhất

---

## 📋**AWS CLI CHEATSHEET**

```bash
# Cấu hình
aws configure

# EC2
aws ec2 describe-instances
aws ec2 start-instances --instance-ids i-xxxxx
aws ec2 stop-instances --instance-ids i-xxxxx

# S3
aws s3 ls
aws s3 cp file.txt s3://bucket/
aws s3 sync . s3://bucket/

# Lambda
aws lambda list-functions
aws lambda invoke --function-name my-func output.json

# Logs
aws logs describe-log-groups
aws logs tail /aws/lambda/my-func --follow
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
