# 🔬 Labs: AWS Core Services

---

## 🔬 Lab 1: EC2 Basics

- Launch EC2 instance
- Connect via SSH
- Install web server
- Create AMI

## 🔬 Lab 2: S3 Storage

- Create bucket
- Upload files
- Configure bucket policy
- Enable versioning

## 🔬 Lab 3: IAM Roles

- Create IAM role
- Attach to EC2
- Test permissions

## 🔬 Lab 4: RDS Database

- Launch RDS instance
- Configure security group
- Connect from EC2

## 🔬 Lab 5: Lambda Function

- Create Lambda function
- Add API Gateway trigger
- Test invocation

---

## ✅ Checklist

- [ ] Lab 1: EC2 Basics
- [ ] Lab 2: S3 Storage
- [ ] Lab 3: IAM Roles
- [ ] Lab 4: RDS Database
- [ ] Lab 5: Lambda Function

---

## ✅ General Verification (Kiểm chứng tổng quát)

```bash
# List EC2 instances (Kiểm tra EC2)
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]'

# List S3 buckets (Kiểm tra S3)
aws s3 ls

# List RDS instances (Kiểm tra RDS)
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus]'
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `EC2: Connection refused` | Check security groups, instance state *(Kiểm tra SG và instance)* |
| `S3: Access Denied` | Check bucket policy, IAM permissions *(Kiểm tra policy)* |
| `RDS: Cannot connect` | Check security group, VPC settings *(Kiểm tra SG và VPC)* |
| `Lambda timeout` | Increase timeout, check code *(Tăng timeout)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Terminate EC2 (Xóa EC2)
aws ec2 terminate-instances --instance-ids i-xxx

# Empty and delete S3 bucket (Xóa S3 bucket)
aws s3 rm s3://bucket-name --recursive
aws s3 rb s3://bucket-name

# Delete RDS (Xóa RDS)
aws rds delete-db-instance --db-instance-identifier mydb --skip-final-snapshot
```

---

**[← Back to README](./README.md)**

