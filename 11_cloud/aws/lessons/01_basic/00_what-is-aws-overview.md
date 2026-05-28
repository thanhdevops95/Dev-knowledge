# 🎓 AWS Overview — Service landscape + Account setup 2026

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Cloud Fundamentals basic](../../../cloud-fundamentals/)

> 🎯 *Bài đầu tiên AWS basic. AWS có 300+ services 2026 — overwhelming. Bài này: 20 services bạn dùng 95% thời gian, naming convention, account setup an toàn, AWS CLI fundamentals, billing alarm. Foundation cho 4 bài deep dive kế tiếp.*

## 🎯 Sau bài này bạn sẽ

- [ ] Biết **20 AWS services** quan trọng nhất (Tier 1)
- [ ] Setup **AWS account** an toàn (root MFA, billing alert)
- [ ] Dùng **AWS CLI** + **profiles**
- [ ] Hiểu **ARN** + naming convention
- [ ] Cài **IAM Identity Center (SSO)** thay vì IAM user
- [ ] Biết **AWS Free Tier** dùng đúng cách
- [ ] **AWS support tiers** + Trusted Advisor

---

## Tình huống — AWS Console 300 services, không biết bắt đầu

Bạn login AWS Console lần đầu:
- Search bar: 300+ services list ra.
- "EC2, S3, Lambda, DynamoDB, EKS, ECS, Fargate, Aurora, RDS, ElastiCache, OpenSearch, Glue, Athena, Redshift, Kinesis, MSK..."
- "Apigee, AppRunner, AppMesh, App Sync, AppStream, AppConfig..."
- Headache.

Sếp: *"Đừng cố biết hết. 20 services chính bạn dùng 95% thời gian. Tab các services kia khi cần. Bài này map landscape."*

→ Bài này tập trung 20 services + setup baseline.

---

## 1️⃣ AWS service landscape — Top 20 (2026)

### Compute

| Service | Mô tả | Use case |
|---|---|---|
| **EC2** | Virtual machines | General-purpose compute |
| **Lambda** | Serverless functions | Event-driven, short tasks |
| **ECS** | Container service (proprietary) | Docker containers, AWS-flavored |
| **EKS** | Managed Kubernetes | Standard K8s |
| **Fargate** | Serverless containers (ECS/EKS backend) | No-ops containers |
| **AppRunner** | Easy container deploy (PaaS) | Quick web app deploy |

### Storage

| Service | Mô tả | Use case |
|---|---|---|
| **S3** | Object storage | Images, videos, backups, data lake |
| **EBS** | Block storage | EC2 disk, DB data |
| **EFS** | Network file system | Shared NFS mount |

### Database

| Service | Mô tả | Use case |
|---|---|---|
| **RDS** | Managed relational (Postgres/MySQL/SQL Server) | OLTP standard |
| **Aurora** | AWS proprietary RDS (faster) | High-scale OLTP |
| **DynamoDB** | NoSQL key-value/document | High-scale low-latency |
| **ElastiCache** | Redis/Memcached | Cache layer |
| **Redshift** | Data warehouse | Analytics, BI |

### Networking

| Service | Mô tả | Use case |
|---|---|---|
| **VPC** | Virtual network | Isolation, subnets |
| **Route 53** | DNS + routing | Domain, latency-routing |
| **CloudFront** | CDN | Static + edge cache |
| **ALB / NLB** | Load balancers | HTTP / TCP traffic |
| **API Gateway** | Managed API entry | REST/WebSocket APIs |

### Security & Identity

| Service | Mô tả | Use case |
|---|---|---|
| **IAM** | Identity + access | Users, roles, policies |
| **IAM Identity Center** | SSO | Federated identity |
| **KMS** | Key management | Encryption keys |
| **Secrets Manager** | Secret store | DB credentials, API keys |
| **Certificate Manager (ACM)** | TLS certs | HTTPS for ALB/CloudFront |
| **WAF** | Web firewall | Block bots, OWASP top 10 |
| **GuardDuty** | Threat detection | ML-based security |

### Observability & Ops

| Service | Mô tả | Use case |
|---|---|---|
| **CloudWatch** | Metrics + logs + alarms | Native monitoring |
| **CloudTrail** | API audit log | Compliance, forensics |
| **AWS Config** | Resource compliance | Detect drift, compliance rules |
| **Systems Manager** | Ops platform | Patching, Session Manager |

### Developer tools

| Service | Mô tả | Use case |
|---|---|---|
| **CodeCommit** | Git hosting | (legacy, prefer GitHub) |
| **CodeBuild** | CI builds | AWS-native CI |
| **CodePipeline** | CI/CD orchestration | AWS-native delivery |
| **CodeDeploy** | Deployment | Blue-green, canary |

### Messaging

| Service | Mô tả | Use case |
|---|---|---|
| **SQS** | Message queue | Async task processing |
| **SNS** | Pub-sub | Notifications, fan-out |
| **EventBridge** | Event bus | SaaS event routing |
| **MSK** | Managed Kafka | Event streaming |
| **Kinesis** | Streaming data | Real-time analytics |

### Data & AI

| Service | Mô tả | Use case |
|---|---|---|
| **Bedrock** | Foundation model service | LLM apps (Claude, Llama) |
| **SageMaker** | ML platform | Train + deploy models |
| **Glue** | ETL service | Data pipelines |
| **Athena** | Query S3 with SQL | Ad-hoc data analysis |

→ **Top 20 (95% of usage)**: EC2, S3, RDS, Lambda, IAM, VPC, CloudWatch, CloudTrail, KMS, Secrets Manager, ALB, Route 53, CloudFront, DynamoDB, ElastiCache, SQS, EventBridge, EKS, Fargate, ACM.

🪞 **Ẩn dụ**: *AWS như **siêu thị 300+ kệ hàng**. Bạn không mua mỗi kệ. 20 kệ chính (rau củ, thịt cá, đồ khô, đồ uống) chiếm 95% mua sắm. Các kệ khác (chocolate Bỉ, ô-liu Hy Lạp) cho dịp đặc biệt.*

---

## 2️⃣ AWS Account setup (Day 1 baseline)

### Step 1: Create AWS account

- Email + credit card.
- Root password 16+ characters.
- **Immediately** enable MFA on root (hardware key best).

### Step 2: Secure root account

```
☐ Root account password 16+ chars random.
☐ Hardware MFA key (YubiKey).
☐ Backup MFA codes stored offline (encrypted USB).
☐ Bookmark root credentials in offline password manager.
☐ Never use root for daily ops.
☐ Document recovery procedure (in case of loss).
```

### Step 3: Setup IAM Identity Center (SSO)

Default AWS now: **IAM Identity Center** (formerly AWS SSO).

```
Pros:
- Central identity from Google Workspace / Okta / Azure AD
- Temporary credentials (1-12 hours)
- Multi-account access
- Audit log centralized
```

Setup:
```bash
# Via AWS Console:
# 1. Enable IAM Identity Center in management account
# 2. Configure identity source (Identity Center default OK for small)
# 3. Create users + groups
# 4. Assign permission sets
# 5. Devs login via portal URL
```

### Step 4: Create IAM admin user (backup)

Even with SSO, keep IAM admin user as backup:
- Strong password + MFA.
- Permission: AdministratorAccess.
- Don't use daily.
- Recover if SSO breaks.

### Step 5: Billing setup

**Critical**: prevent surprise bills.

```bash
# Enable billing alerts
# AWS Console → Billing → Billing preferences:
# ☐ Receive PDF invoice by email
# ☐ Receive Free Tier Usage Alerts
# ☐ Receive Billing Alerts
```

**Create CloudWatch billing alarm**:
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name "Billing-50USD" \
  --namespace "AWS/Billing" \
  --metric-name "EstimatedCharges" \
  --statistic Maximum \
  --period 21600 \
  --evaluation-periods 1 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=Currency,Value=USD \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT:billing-alarm
```

→ Email at $50, $100, $500. Catch cost spikes early.

### Step 6: Enable CloudTrail (audit log)

```bash
aws cloudtrail create-trail \
  --name acme-trail \
  --s3-bucket-name acme-cloudtrail-logs-$(aws sts get-caller-identity --query Account --output text) \
  --is-multi-region-trail \
  --include-global-service-events \
  --enable-log-file-validation

aws cloudtrail start-logging --name acme-trail
```

→ All API calls logged forever.

### Step 7: Enable GuardDuty

```bash
aws guardduty create-detector --enable
```

→ ML-based threat detection. ~$5-30/month per account.

### Step 8: Block public S3 (account-wide)

```bash
aws s3control put-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

→ Prevent accidental public bucket.

### Day 1 cost estimate

| Service | Cost/month |
|---|---|
| AWS Account | $0 |
| IAM Identity Center | $0 (built-in) |
| CloudTrail | $0 (1 trail free) |
| GuardDuty | $5-30 |
| S3 (logs) | <$1 |
| **Total baseline** | **~$10-30/month** |

→ Affordable secure baseline.

---

## 3️⃣ AWS naming conventions

### ARN — Amazon Resource Name

Every AWS resource has ARN:
```
arn:aws:<service>:<region>:<account-id>:<resource-type>/<resource-id>
```

Examples:
```
arn:aws:s3:::my-bucket                          (S3 bucket — global, no region/account)
arn:aws:s3:::my-bucket/path/to/file.txt          (S3 object)
arn:aws:ec2:us-east-1:123456789012:instance/i-abc  (EC2 instance)
arn:aws:lambda:us-east-1:123456789012:function:myFn (Lambda function)
arn:aws:iam::123456789012:user/alice              (IAM user — global, no region)
```

**Usage in policies**:
```json
{
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

### Region naming

| Region code | Location |
|---|---|
| `us-east-1` | N. Virginia |
| `us-east-2` | Ohio |
| `us-west-1` | N. California |
| `us-west-2` | Oregon |
| `eu-west-1` | Ireland |
| `eu-west-2` | London |
| `eu-central-1` | Frankfurt |
| `eu-north-1` | Stockholm |
| `ap-southeast-1` | Singapore |
| `ap-southeast-2` | Sydney |
| `ap-northeast-1` | Tokyo |
| `ap-northeast-2` | Seoul |
| `ap-south-1` | Mumbai |
| `sa-east-1` | São Paulo |
| `ca-central-1` | Canada |

→ Convention: `<geo>-<direction>-<number>`. Old regions = lower numbers.

### Resource naming patterns

```
Convention:
  <project>-<env>-<service>-<role>

Examples:
  acme-prod-eks-cluster
  acme-prod-rds-postgres
  acme-staging-s3-uploads
  acme-prod-lambda-api
```

→ Sortable in console. Searchable. Cost-allocatable.

### Tags

Every resource taggable:
```hcl
tags = {
  Environment = "prod"
  Service     = "checkout"
  Team        = "payments"
  CostCenter  = "engineering"
  Owner       = "nguyenvana@acme.com"
}
```

→ Cost Explorer can filter by tag. Compliance audit by tag.

---

## 4️⃣ AWS CLI fundamentals

### Install

```bash
# macOS
brew install awscli

# Or pip
pip install awscli --upgrade --user

# Verify
aws --version
# aws-cli/2.15.40 Python/3.12.0 Darwin/...
```

### Configure

```bash
# Interactive setup
aws configure
# AWS Access Key ID: <key>
# AWS Secret Access Key: <secret>
# Default region: ap-southeast-1
# Default output: json

# Stored in ~/.aws/credentials and ~/.aws/config
```

### Profiles (multiple accounts)

```bash
# Multiple profiles
aws configure --profile dev
aws configure --profile prod

# Use profile
aws s3 ls --profile prod

# Or set env
export AWS_PROFILE=prod
aws s3 ls
```

`~/.aws/credentials`:
```ini
[default]
aws_access_key_id = ...
aws_secret_access_key = ...

[dev]
aws_access_key_id = ...
aws_secret_access_key = ...

[prod]
aws_access_key_id = ...
aws_secret_access_key = ...
```

### IAM Identity Center SSO with CLI

Better than static keys:

```bash
# Configure SSO
aws configure sso
# SSO start URL: https://acme.awsapps.com/start
# Region: ap-southeast-1
# Pick account + role

# Login
aws sso login --profile prod

# Use
aws s3 ls --profile prod
```

→ Temporary credentials, auto-rotated.

### Common CLI commands

```bash
# Identity
aws sts get-caller-identity

# Region setup
aws configure set region ap-southeast-1

# S3
aws s3 ls
aws s3 cp file.txt s3://bucket/
aws s3 sync ./local s3://bucket/

# EC2
aws ec2 describe-instances
aws ec2 describe-regions

# IAM
aws iam list-users
aws iam list-roles

# Lambda
aws lambda list-functions
aws lambda invoke --function-name myFn output.json
```

### Output formats

```bash
# JSON (default)
aws ec2 describe-instances

# Table (readable)
aws ec2 describe-instances --output table

# Text (parseable)
aws ec2 describe-instances --output text

# YAML
aws ec2 describe-instances --output yaml
```

### Filter + query (JMESPath)

```bash
# Filter
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running"

# Query specific field
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].InstanceId'

# Combine
aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=prod" \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,State.Name]' \
  --output table
```

---

## 5️⃣ AWS Free Tier (2026)

### What's free

**12-month free** (counted from account creation):
- **EC2**: 750 hours/month t2.micro or t3.micro Linux.
- **S3**: 5 GB storage + 20K GET + 2K PUT.
- **RDS**: 750 hours db.t2.micro / db.t3.micro Multi-AZ + 20 GB storage.
- **EBS**: 30 GB SSD storage.
- **CloudFront**: 1 TB egress.
- **API Gateway**: 1M API calls.
- **Lambda**: 1M requests + 400K GB-seconds compute (always free).

**Always free**:
- **Lambda**: 1M req + 400K GB-s/month always.
- **DynamoDB**: 25 GB + 25 WCU + 25 RCU.
- **CloudWatch**: 10 metrics + 10 alarms.

**Trials** (specific duration):
- **SageMaker**: 2 months trial.
- **Aurora**: 30 days.

### Anti-patterns

**Pitfall**: Spin up t2.large by mistake (not in free tier) → $50/month surprise.

**Pitfall**: Free tier covers 1 instance. Run 5 t3.micro → 4 charged.

**Pitfall**: Forget to delete after testing → next month still billed.

### Safe learning setup

1. **Billing alert**: $1, $5, $10 thresholds.
2. **AWS Free Tier Usage Alert**: enabled.
3. **Stop everything weekly**: review running resources.
4. **Use AWS Budgets**: predict spending.

→ Learn AWS for free if disciplined.

---

## 6️⃣ AWS support tiers

| Tier | Cost | Includes |
|---|---|---|
| **Basic** | Free | Forums, docs, AWS Trusted Advisor 7 checks |
| **Developer** | $29/month or 3% of usage | Email support (business hours), 12h response |
| **Business** | $100/month or 10% of usage | 24/7 phone, 1h response for production down |
| **Enterprise On-Ramp** | $5,500/month | TAM (Technical Account Manager) light |
| **Enterprise** | $15,000+/month or 5-10% | Dedicated TAM, 15-min response |

**Trusted Advisor** (in higher tiers):
- Cost optimization recommendations.
- Performance.
- Security findings.
- Fault tolerance.

→ Basic OK for learning. Business for production. Enterprise for $1M+ AWS spend.

---

## 7️⃣ Lộ trình AWS basic 5 bài

| Bài | Nội dung | Output |
|---|---|---|
| **01** EC2 + EBS | Instance types + AMI + EBS + key pairs + user data + ASG basics | Deploy first EC2 with web server |
| **02** S3 + IAM basics | Buckets + policies + lifecycle + presigned URLs + IAM users/roles for S3 | Static website on S3 + IAM secure access |
| **03** RDS + DynamoDB | Managed Postgres + DynamoDB design + Multi-AZ + snapshots | First DB deployed with backup strategy |
| **04** Lambda + API Gateway | First serverless function + HTTP API + event triggers | Serverless API live |

→ After 5 bài: deploy production small app on AWS.

---

## 💡 Câu hỏi beginner hay hỏi

**Q1.** "Học AWS bắt đầu từ đâu?"

→ **20 services tier 1** (above). Don't try to learn everything. Pick 1 project (web app, data pipeline) → use 5-7 services.

**Q2.** "Cần AWS certification?"

→ **Helpful for career, not required for engineering**. 2026 recommend:
- **AWS Certified Solutions Architect Associate** (SAA-C03): broad knowledge.
- **AWS Certified Developer Associate**: for dev focus.
- Skip Cloud Practitioner if you have hands-on.

→ Cost: $150 exam. Study 1-2 months part-time.

**Q3.** "AWS Console vs CLI vs Terraform — học cái nào?"

→ **All three**:
- **Console**: explore, debug, one-off.
- **CLI**: scripting, automation.
- **Terraform**: infrastructure as code (production).

→ Daily: CLI + Terraform. Console for troubleshoot.

**Q4.** "How to learn AWS fast?"

→ Build projects:
- Deploy WordPress on EC2.
- Static site on S3 + CloudFront.
- Lambda function triggered by S3 upload.
- RDS Postgres + Python app.

→ 4 projects = touch 80% of AWS basics. Better than 100 hours tutorial.

**Q5.** "AWS expensive for personal projects?"

→ **Free tier** covers learning. Beyond that:
- Static site: $1-5/month (S3 + CloudFront).
- Small app: $20-50/month (small EC2 + small RDS).
- For real personal projects: **DigitalOcean / Hetzner** often cheaper.

→ Use AWS for **professional** work. Personal projects on cheaper hosts.

---

## 🗺️ Beyond basic — Career paths

After AWS basic:

| Path | Next AWS services |
|---|---|
| **DevOps Engineer** | EKS, ECS, Fargate, ECR, CodeBuild, Systems Manager |
| **Backend Engineer** | Aurora, ElastiCache, Lambda, API Gateway, SQS |
| **Data Engineer** | Glue, Athena, Redshift, Kinesis, EMR |
| **ML Engineer** | SageMaker, Bedrock, EC2 GPU instances |
| **Cloud Architect** | Well-Architected, Multi-account Organizations, Control Tower |
| **Security Engineer** | GuardDuty, Macie, Security Hub, Inspector, Detective |

→ Pick path. Deep dive 5-10 services per path.

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **AWS** | Amazon Web Services |
| **EC2** | Elastic Compute Cloud (VMs) |
| **S3** | Simple Storage Service |
| **RDS** | Relational Database Service |
| **VPC** | Virtual Private Cloud |
| **IAM** | Identity and Access Management |
| **ARN** | Amazon Resource Name (unique identifier) |
| **Region** | Geographic cluster of datacenters |
| **AZ** | Availability Zone (within region) |
| **AMI** | Amazon Machine Image (EC2 template) |
| **ASG** | Auto Scaling Group (EC2 group with scaling rules) |
| **ALB / NLB** | Application/Network Load Balancer |
| **CloudFront** | CDN service |
| **Route 53** | DNS service |
| **Lambda** | Serverless function service |
| **EKS / ECS** | Kubernetes / Container service |
| **Fargate** | Serverless containers |
| **DynamoDB** | NoSQL DB |
| **ElastiCache** | Managed Redis/Memcached |
| **SQS / SNS** | Queue / Pub-sub |
| **EventBridge** | Event bus |
| **KMS** | Key Management Service |
| **ACM** | Certificate Manager |
| **Secrets Manager** | Secret storage |
| **CloudWatch** | Monitoring + logs + alarms |
| **CloudTrail** | API audit log |
| **AWS Config** | Resource compliance |
| **GuardDuty** | ML threat detection |
| **WAF** | Web Application Firewall |
| **IAM Identity Center** | SSO (formerly AWS SSO) |
| **Trusted Advisor** | AWS recommendations engine |
| **Free Tier** | Free usage limits for new accounts |
| **AWS CLI** | Command-line interface |
| **Profile** | CLI named credential set |
| **SSO** | Single Sign-On |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- → Tiếp: [01_ec2-and-ebs-compute.md](01_ec2-and-ebs-compute.md) *(sắp viết)*
- ↑ Cluster: [AWS README](../../README.md)

### Cross-reference
- ☁️ [Cloud Fundamentals](../../../cloud-fundamentals/) — vendor-neutral foundation
- 🏗️ [IaC Terraform](../../../../10_devops/iac/) — manage AWS via code

### Tài nguyên ngoài (2026)
- 📖 [AWS docs](https://docs.aws.amazon.com/)
- 📖 [AWS CLI docs](https://docs.aws.amazon.com/cli/)
- 📖 [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 📖 [AWS Free Tier](https://aws.amazon.com/free/)
- 📖 [AWS Pricing Calculator](https://calculator.aws/)
- 📖 [AWS Certified Solutions Architect Associate](https://aws.amazon.com/certification/certified-solutions-architect-associate/)
- 📖 [A Cloud Guru](https://acloudguru.com/) — courses
- 📖 [AWS Skill Builder](https://skillbuilder.aws/) — free official
- 📖 [Cloud Practitioner Practice Exams](https://aws.amazon.com/certification/certified-cloud-practitioner/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 00 cluster AWS basic. 20 services tier 1 + Account setup baseline (root MFA, billing alert, CloudTrail, GuardDuty) + ARN naming + AWS CLI + profiles + IAM Identity Center SSO + Free Tier + Support tiers. Foundation cho 4 bài kế tiếp.
