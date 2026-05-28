# 📋 AWS Core Services - Cheatsheet

> **Quick Reference for AWS CLI Commands**
>
> *Tra cứu nhanh lệnh AWS CLI*

---

## 🔧 Configuration (Cấu hình)

```bash
aws configure                       # Setup credentials (Cấu hình)
aws sts get-caller-identity         # Check identity (Kiểm tra identity)
aws configure list                  # List config (Xem cấu hình)
```

---

## 💻 EC2

```bash
# Instances
aws ec2 describe-instances          # List instances (Liệt kê)
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx

# Security Groups
aws ec2 describe-security-groups
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx --protocol tcp --port 22 --cidr 0.0.0.0/0
```

---

## 📦 S3

```bash
# Bucket operations (Thao tác bucket)
aws s3 ls                           # List buckets (Liệt kê buckets)
aws s3 mb s3://my-bucket            # Create bucket (Tạo bucket)
aws s3 rb s3://my-bucket            # Remove bucket (Xóa bucket)

# Object operations (Thao tác object)
aws s3 ls s3://bucket/              # List objects (Liệt kê objects)
aws s3 cp file.txt s3://bucket/     # Upload file
aws s3 cp s3://bucket/file.txt .    # Download file
aws s3 sync ./folder s3://bucket/   # Sync folder

# Presigned URL (URL có chữ ký)
aws s3 presign s3://bucket/file.txt --expires-in 3600
```

---

## 🔐 IAM

```bash
aws iam list-users                  # List users (Liệt kê users)
aws iam list-roles                  # List roles (Liệt kê roles)
aws iam get-user                    # Current user info
aws iam create-access-key --user-name username
```

---

## 🗄️ RDS

```bash
aws rds describe-db-instances       # List databases
aws rds start-db-instance --db-instance-identifier mydb
aws rds stop-db-instance --db-instance-identifier mydb
```

---

## 🌐 VPC

```bash
aws ec2 describe-vpcs               # List VPCs
aws ec2 describe-subnets            # List subnets
aws ec2 describe-route-tables       # List route tables
```

---

## 📊 Common Options (Tùy chọn phổ biến)

```bash
--region us-east-1                  # Specify region (Chỉ định region)
--output json|table|text            # Output format (Định dạng output)
--query 'Items[].Name'              # JMESPath query (Truy vấn JMESPath)
--profile production                # Use profile (Dùng profile)
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
