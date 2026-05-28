# ☁️ AWS

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *Amazon Web Services — vendor #1 (~32% Q1 2026). 5 services tier 1 (EC2/S3/IAM/RDS/Lambda) cho 95% workloads. Sau cluster: deploy small production app on AWS.*

---

## 🚀 Quick start

- **AWS là gì, account setup?** → [00_what-is-aws-overview](lessons/01_basic/00_what-is-aws-overview.md).
- **Deploy first EC2 + auto-scale?** → [01_ec2-and-ebs-compute](lessons/01_basic/01_ec2-and-ebs-compute.md).
- **S3 + IAM + presigned URL?** → [02_s3-deep-and-iam](lessons/01_basic/02_s3-deep-and-iam.md).
- **Managed DB RDS + DynamoDB?** → [03_rds-and-dynamodb](lessons/01_basic/03_rds-and-dynamodb.md).
- **Serverless Lambda + API Gateway?** → [04_lambda-and-api-gateway](lessons/01_basic/04_lambda-and-api-gateway.md).

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Trọng tâm | Tag | Thời lượng |
|---|---|---|---|---|
| 00 | [What is AWS overview](lessons/01_basic/00_what-is-aws-overview.md) | 20 services tier 1 + account setup + ARN + IAM Identity Center + Free Tier | MUST-KNOW | ~17p |
| 01 | [EC2 + EBS](lessons/01_basic/01_ec2-and-ebs-compute.md) | Instance types + AMI + EBS + ASG + spot/RI pricing | MUST-KNOW | ~22p |
| 02 | [S3 deep + IAM](lessons/01_basic/02_s3-deep-and-iam.md) | Bucket policy + IAM policy + presigned URL + lifecycle + versioning | MUST-KNOW | ~22p |
| 03 | [RDS + DynamoDB](lessons/01_basic/03_rds-and-dynamodb.md) | RDS Postgres Multi-AZ + Aurora + DynamoDB design + decision matrix | MUST-KNOW | ~20p |
| 04 | [Lambda + API Gateway](lessons/01_basic/04_lambda-and-api-gateway.md) | Lambda triggers + cold start + API Gateway HTTP vs REST | MUST-KNOW | ~22p |

→ **Tổng ~103 phút đọc + 6-8h hands-on**.

---

## 🔗 Liên kết

- ↑ [11_cloud README](../README.md)
- ☁️ [Cloud Fundamentals](../cloud-fundamentals/)
- 🏗️ [IaC Terraform](../../10_devops/iac/)
- ☸️ [Kubernetes](../../10_devops/kubernetes/) — EKS context

### Tài nguyên ngoài 2026
- 📖 [AWS docs](https://docs.aws.amazon.com/)
- 📖 [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- 📖 [AWS Skill Builder](https://skillbuilder.aws/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. AWS vendor-specific deep cluster đầu tiên của 11_cloud.
- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
