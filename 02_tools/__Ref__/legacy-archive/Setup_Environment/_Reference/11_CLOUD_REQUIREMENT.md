# Module 11: CLOUD PLATFORMS (AWS, GCP, Azure)

> **"Cloud là thuê infrastructure - không cần mua nhà, chỉ thuê đúng cái cần"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu Cloud computing concepts (IaaS, PaaS, SaaS)
- ✅ AWS Core Services (EC2, S3, VPC, IAM, RDS, EKS)
- ✅ GCP và Azure basics
- ✅ Serverless (Lambda, Cloud Functions)
- ✅ Container services (ECS, EKS, GKE)
- ✅ Cloud networking
- ✅ Cost optimization

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| IaaS | Infrastructure as a Service | Thuê infrastructure |
| PaaS | Platform as a Service | Thuê platform |
| SaaS | Software as a Service | Thuê software |
| Region | Region | Vùng địa lý |
| AZ | Availability Zone | Vùng khả dụng |
| EC2 | Elastic Compute Cloud | VMs trên AWS |
| S3 | Simple Storage Service | Object storage |
| VPC | Virtual Private Cloud | Mạng riêng ảo |
| IAM | Identity and Access Management | Quản lý quyền |
| RDS | Relational Database Service | Managed database |
| EKS | Elastic Kubernetes Service | Managed K8s |
| ECS | Elastic Container Service | Container service |
| Lambda | AWS Lambda | Serverless functions |
| API Gateway | API Gateway | Managed API |
| CloudWatch | CloudWatch | Monitoring |
| Route53 | Route 53 | DNS service |
| CloudFront | CloudFront | CDN |
| SNS | Simple Notification Service | Notification |
| SQS | Simple Queue Service | Message queue |
| GKE | Google Kubernetes Engine | GCP managed K8s |
| AKS | Azure Kubernetes Service | Azure managed K8s |

---

## ✅ Checklist Labs

### Labs Cloud Basics

- [ ] Lab 1: Create AWS Free Tier account
- [ ] Lab 2: AWS Console navigation
- [ ] Lab 3: AWS CLI installation
- [ ] Lab 4: AWS CLI configuration (access keys)
- [ ] Lab 5: Regions và AZs

### Labs IAM

- [ ] Lab 6: IAM Users
- [ ] Lab 7: IAM Groups
- [ ] Lab 8: IAM Policies (managed, inline)
- [ ] Lab 9: IAM Roles
- [ ] Lab 10: MFA setup
- [ ] Lab 11: IAM best practices
- [ ] Lab 12: AWS Organizations basics

### Labs VPC & Networking

- [ ] Lab 13: VPC creation
- [ ] Lab 14: Subnets (public, private)
- [ ] Lab 15: Internet Gateway
- [ ] Lab 16: NAT Gateway
- [ ] Lab 17: Route Tables
- [ ] Lab 18: Security Groups
- [ ] Lab 19: Network ACLs
- [ ] Lab 20: VPC Peering

### Labs EC2

- [ ] Lab 21: Launch EC2 instance
- [ ] Lab 22: EC2 instance types
- [ ] Lab 23: Key pairs
- [ ] Lab 24: Security Group rules
- [ ] Lab 25: SSH to EC2
- [ ] Lab 26: EC2 user data
- [ ] Lab 27: AMI creation
- [ ] Lab 28: EC2 pricing models
- [ ] Lab 29: Elastic IP
- [ ] Lab 30: EC2 Auto Scaling

### Labs S3

- [ ] Lab 31: S3 bucket creation
- [ ] Lab 32: S3 objects upload/download
- [ ] Lab 33: S3 bucket policies
- [ ] Lab 34: S3 versioning
- [ ] Lab 35: S3 lifecycle rules
- [ ] Lab 36: S3 static website hosting
- [ ] Lab 37: S3 encryption
- [ ] Lab 38: AWS CLI với S3

### Labs RDS

- [ ] Lab 39: RDS instance creation
- [ ] Lab 40: RDS security groups
- [ ] Lab 41: RDS backups
- [ ] Lab 42: RDS read replicas
- [ ] Lab 43: RDS Multi-AZ

### Labs Container Services

- [ ] Lab 44: ECR repository
- [ ] Lab 45: Push image to ECR
- [ ] Lab 46: ECS cluster creation
- [ ] Lab 47: ECS task definition
- [ ] Lab 48: ECS service
- [ ] Lab 49: EKS cluster creation
- [ ] Lab 50: Deploy to EKS

### Labs Serverless

- [ ] Lab 51: Lambda function basics
- [ ] Lab 52: Lambda với Python
- [ ] Lab 53: Lambda triggers (S3, API Gateway)
- [ ] Lab 54: API Gateway setup
- [ ] Lab 55: Lambda environment variables
- [ ] Lab 56: Lambda layers

### Labs Monitoring & Logging

- [ ] Lab 57: CloudWatch metrics
- [ ] Lab 58: CloudWatch logs
- [ ] Lab 59: CloudWatch alarms
- [ ] Lab 60: CloudWatch dashboards
- [ ] Lab 61: CloudTrail basics

### Labs DNS & CDN

- [ ] Lab 62: Route53 hosted zone
- [ ] Lab 63: Route53 record types
- [ ] Lab 64: CloudFront distribution
- [ ] Lab 65: CloudFront với S3

### Labs Cost Optimization

- [ ] Lab 66: AWS Cost Explorer
- [ ] Lab 67: AWS Budgets
- [ ] Lab 68: Reserved instances concept
- [ ] Lab 69: Spot instances concept
- [ ] Lab 70: Resource tagging

### Labs GCP Basics

- [ ] Lab 71: GCP Console
- [ ] Lab 72: gcloud CLI
- [ ] Lab 73: GCE instances
- [ ] Lab 74: GCS buckets
- [ ] Lab 75: GKE cluster

### Labs Azure Basics

- [ ] Lab 76: Azure Portal
- [ ] Lab 77: Azure CLI
- [ ] Lab 78: Azure VMs
- [ ] Lab 79: Azure Blob Storage
- [ ] Lab 80: AKS cluster

---

## 🚨 Checklist Scenarios

### Scenarios về IAM

- [ ] Scenario 1: User không có quyền access resource
- [ ] Scenario 2: Access key bị expose
- [ ] Scenario 3: Role assumption failed
- [ ] Scenario 4: Cross-account access issues

### Scenarios về VPC

- [ ] Scenario 5: EC2 không connect được internet
- [ ] Scenario 6: Private subnet không reach internet
- [ ] Scenario 7: Security group blocking traffic
- [ ] Scenario 8: VPC peering không work

### Scenarios về EC2

- [ ] Scenario 9: Instance không SSH được
- [ ] Scenario 10: Instance stopped unexpectedly
- [ ] Scenario 11: EBS volume full
- [ ] Scenario 12: Key pair lost

### Scenarios về S3

- [ ] Scenario 13: Access denied to S3 object
- [ ] Scenario 14: Bucket policy conflict
- [ ] Scenario 15: Object deleted accidentally
- [ ] Scenario 16: Cross-account S3 access

### Scenarios về RDS

- [ ] Scenario 17: RDS connection timeout
- [ ] Scenario 18: RDS storage full
- [ ] Scenario 19: Backup restore needed
- [ ] Scenario 20: Master password forgot

### Scenarios về Containers

- [ ] Scenario 21: ECS task failed to start
- [ ] Scenario 22: ECR pull failed
- [ ] Scenario 23: EKS kubectl access denied
- [ ] Scenario 24: Container crash trong ECS

### Scenarios về Serverless

- [ ] Scenario 25: Lambda timeout
- [ ] Scenario 26: Lambda cold start slow
- [ ] Scenario 27: API Gateway 5xx errors
- [ ] Scenario 28: Lambda out of memory

### Scenarios về Cost

- [ ] Scenario 29: Unexpected AWS bill
- [ ] Scenario 30: Forgotten resources running
- [ ] Scenario 31: Data transfer costs high
- [ ] Scenario 32: Reserved capacity không optimize

---

## ⏱️ Thời lượng

**Ước tính:** 8-10 giờ

| Phần | Thời gian |
|------|-----------|
| Cloud basics & IAM (Labs 1-12) | 1.5 giờ |
| VPC & Networking (Labs 13-20) | 1.5 giờ |
| EC2 (Labs 21-30) | 1.5 giờ |
| S3 & RDS (Labs 31-43) | 1.5 giờ |
| Containers (Labs 44-50) | 1 giờ |
| Serverless (Labs 51-56) | 1 giờ |
| Monitoring, DNS, Cost | 1 giờ |
| GCP & Azure basics | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [GCP Documentation](https://cloud.google.com/docs)
- [Azure Documentation](https://docs.microsoft.com/azure/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
