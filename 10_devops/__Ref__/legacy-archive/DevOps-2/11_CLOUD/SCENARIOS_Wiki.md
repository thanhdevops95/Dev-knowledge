# 🚨 Tình huống Thực chiến - AWS/Cloud

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi làm việc với Cloud.

---

## Scenario 1: AWS Bill tăng đột biến 10x

### 📋 Bối cảnh

Cuối tháng, AWS bill từ **$500 tăng lên $5000**!

> "CFO đang gọi điện hỏi..."

### 🔍 Triệu chứng

```
AWS Cost Explorer:
- Last month: $500
- This month: $5,000 (+900%)

Top services:
- EC2: $3,000 (up 500%)
- Data Transfer: $1,500 (up 2000%)
```

### 🕵️ Điều tra

**Bước 1: Cost Explorer drill-down**

```
EC2 → By Instance Type:
- m5.4xlarge: $2,800  ← 10 instances running!
  
Filter by tag:
- No tags ← Ai tạo mà không tag?
```

**Bước 2: CloudTrail audit**

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=RunInstances \
  --start-time 2024-01-01
  
# Found: User "intern@company.com" launched 10x m5.4xlarge
# for "testing ML model" and forgot to terminate
```

**Bước 3: Data Transfer**

```
NAT Gateway: $1,500
- 15TB outbound traffic
- Cause: Downloading Docker images from DockerHub mỗi deployment
```

### 💡 Giải pháp

**1. Terminate unused resources:**

```bash
# Find and terminate
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[*].Instances[*].[InstanceId,LaunchTime,Tags]'

aws ec2 terminate-instances --instance-ids i-xxx
```

**2. Mandatory tagging:**

```json
// AWS Service Control Policy
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Action": "ec2:RunInstances",
    "Resource": "*",
    "Condition": {
      "Null": {
        "aws:RequestTag/Owner": "true"
      }
    }
  }]
}
```

**3. Budget alerts:**

```bash
aws budgets create-budget \
  --account-id 123456789 \
  --budget '{
    "BudgetName": "Monthly",
    "BudgetLimit": {"Amount": "600", "Unit": "USD"},
    "TimeUnit": "MONTHLY"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80
    },
    "Subscribers": [{
      "SubscriptionType": "EMAIL",
      "Address": "devops@company.com"
    }]
  }]'
```

**4. ECR for Docker images (save NAT costs):**

```bash
# Push to ECR thay vì pull từ DockerHub
aws ecr get-login-password | docker login --username AWS ...
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp
```

**5. Spot instances for non-critical:**

```hcl
# Terraform
resource "aws_instance" "worker" {
  instance_type = "m5.xlarge"
  
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.10"  # 70% cheaper!
    }
  }
}
```

### 🧠 Bài học

- **Billing alerts là bắt buộc** - Biết trước khi cuối tháng
- **Tagging policy** - Ai tạo, mục đích gì
- **Cleanup automation** - Xóa resources không dùng
- **Data transfer costs** - Thường bị bỏ quên

---

## Scenario 2: S3 bucket bị public - Data breach

### 📋 Bối cảnh

Security scanner phát hiện S3 bucket **public-read**. Chứa database backups.

> CRITICAL: Customer data exposed!

### 🔍 Triệu chứng

```bash
# Anyone can access
curl https://company-backups.s3.amazonaws.com/db/backup.sql
# Returns: 200 OK with database dump!
```

### 🕵️ Điều tra

```bash
# Check bucket ACL
aws s3api get-bucket-acl --bucket company-backups
# "Grantee": {"URI": "http://acs.amazonaws.com/groups/global/AllUsers"}
# "Permission": "READ"  ← PUBLIC!

# CloudTrail: who made it public?
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=company-backups
# User made it public 3 months ago for "sharing with partner"
```

### 💡 Giải pháp

**1. Block public access immediately:**

```bash
aws s3api put-public-access-block \
  --bucket company-backups \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**2. Account-level block:**

```bash
aws s3control put-public-access-block \
  --account-id 123456789 \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**3. Detect public buckets:**

```bash
# AWS Config rule
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "s3-bucket-public-read-prohibited",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
}'
```

**4. Encryption at rest:**

```bash
aws s3api put-bucket-encryption --bucket company-backups \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "aws:kms"
      }
    }]
  }'
```

**5. Incident response:**

```markdown
1. Block access immediately
2. Check CloudTrail for who accessed the bucket
3. Notify affected customers (legal requirement)
4. Rotate any credentials in the backup
5. Post-mortem and preventive measures
```

### 🧠 Bài học

- **Block public access at account level** - Default
- **Scan for public buckets** - Tools: S3Scanner, AWS Config
- **Encryption mandatory** - Ngay cả internal data
- **Least privilege** - Không public trừ khi absolutely needed

---

## Scenario 3: EC2 instance unreachable - Cannot SSH

### 📋 Bối cảnh

Production server unreachable. Không SSH được. Website down.

### 🔍 Triệu chứng

```bash
ssh ec2-user@52.1.2.3
# ssh: connect to host 52.1.2.3 port 22: Connection timed out

ping 52.1.2.3
# Request timeout

# AWS Console: Instance status = running
```

### 🕵️ Điều tra

**Checklist debug:**

| Check | Command | Common Issue |
|-------|---------|--------------|
| Security Group | Console/CLI | Port 22 blocked |
| NACL | Console | Stateless rules wrong |
| Route Table | Console | No route to IGW |
| EIP/Public IP | Console | No public IP assigned |
| Instance status | Console | Status check failed |

```bash
# Security group check
aws ec2 describe-security-groups --group-ids sg-xxx
# Không có rule cho port 22 từ IP của bạn!

# Hoặc instance status
aws ec2 describe-instance-status --instance-ids i-xxx
# "Status": "impaired" - Có vấn đề với instance
```

### 💡 Giải pháp

**1. Security group fix:**

```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 22 \
  --cidr 1.2.3.4/32  # Your IP
```

**2. Nếu instance impaired - check System Log:**

```bash
aws ec2 get-console-output --instance-id i-xxx
# Kernel panic?
# File system full?
# Network misconfigured?
```

**3. EC2 Instance Connect (không cần SSH key):**

```bash
aws ec2-instance-connect send-ssh-public-key \
  --instance-id i-xxx \
  --availability-zone us-east-1a \
  --instance-os-user ec2-user \
  --ssh-public-key file://~/.ssh/id_rsa.pub
```

**4. Session Manager (không cần port 22):**

```bash
# Cài SSM Agent trên instance
aws ssm start-session --target i-xxx
# SSH qua AWS Systems Manager - không cần public IP!
```

**5. Recovery via snapshot:**

```bash
# Nếu instance không thể recover
# Stop instance
# Detach EBS
# Attach EBS to healthy instance
# Mount và fix files
# Reattach và start
```

### 🧠 Bài học

- **Session Manager > SSH** - Không cần mở port 22
- **Multiple access methods** - SSH, SSM, Serial Console
- **Bastion host** - Không public IP cho production
- **Backup root volume** - Snapshot định kỳ

---

## Scenario 4: RDS performance degradation

### 📋 Bối cảnh

Database queries từ 50ms tăng lên **5 seconds**. App timeout.

### 🔍 Triệu chứng

```
Application logs:
ERROR: Database query timeout after 30s

CloudWatch RDS metrics:
- CPUUtilization: 95%
- ReadIOPS: 10,000 (baseline: 3,000)
- FreeableMemory: 100MB (16GB instance)
```

### 🕵️ Điều tra

**1. Performance Insights:**

```
Top SQL by Wait:
SELECT * FROM orders WHERE status = 'pending'  ← 60% of load
- Full table scan
- Missing index
```

**2. Check connections:**

```sql
SELECT count(*) FROM pg_stat_activity;
-- 450 connections (max_connections = 500)
```

### 💡 Giải pháp

**1. Add index:**

```sql
CREATE INDEX idx_orders_status ON orders(status);
-- Query time: 5s -> 50ms
```

**2. Connection pooling:**

```yaml
# PgBouncer hoặc RDS Proxy
aws rds create-db-proxy \
  --db-proxy-name myproxy \
  --engine-family POSTGRESQL \
  --auth '{"AuthScheme": "SECRETS", ...}'
```

**3. Read replicas:**

```bash
aws rds create-db-instance-read-replica \
  --db-instance-identifier mydb-replica \
  --source-db-instance-identifier mydb
  
# App reads from replica
```

**4. Scale up (temporary):**

```bash
aws rds modify-db-instance \
  --db-instance-identifier mydb \
  --db-instance-class db.r5.2xlarge \
  --apply-immediately
```

**5. Query optimization:**

```sql
-- Examine query plan
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending';

-- Add pagination
SELECT * FROM orders WHERE status = 'pending' 
LIMIT 100 OFFSET 0;
```

### 🧠 Bài học

- **Performance Insights bật sẵn** - Để debug khi cần
- **Connection pooling** - Giảm connection overhead
- **Indexes** - Missing index = full table scan
- **Read replicas** - Tách read/write traffic

---

## Scenario 5: Region outage - Disaster Recovery

### 📋 Bối cảnh

**AWS us-east-1 outage**. Toàn bộ infrastructure down.

> "Tất cả services ở một region duy nhất"

### 🔍 Triệu chứng

```
AWS Status Page:
🔴 EC2 - us-east-1 - Degraded
🔴 RDS - us-east-1 - Degraded
🔴 S3 - us-east-1 - Degraded

Your monitoring:
- All services: DOWN
- Failover: None configured
```

### 🕵️ Điều tra

```yaml
Current architecture:
- Single region: us-east-1
- No cross-region replication
- No multi-region DNS failover
- RTO: Unknown
- RPO: Unknown
```

### 💡 Giải pháp

**1. Multi-region architecture:**

```
                    Route 53
                       |
           +-----------+-----------+
           |                       |
        us-east-1              us-west-2
           |                       |
     +-----+-----+           +-----+-----+
     |     |     |           |     |     |
    EC2   RDS   S3          EC2   RDS   S3
                            (standby)
```

**2. S3 Cross-Region Replication:**

```bash
aws s3api put-bucket-replication \
  --bucket source-bucket \
  --replication-configuration '{
    "Role": "arn:aws:iam::xxx:role/replication",
    "Rules": [{
      "Status": "Enabled",
      "Destination": {
        "Bucket": "arn:aws:s3:::destination-bucket"
      }
    }]
  }'
```

**3. RDS Cross-Region Read Replica:**

```bash
aws rds create-db-instance-read-replica \
  --db-instance-identifier mydb-dr \
  --source-db-instance-identifier arn:aws:rds:us-east-1:xxx:db:mydb \
  --region us-west-2
```

**4. Route 53 Health Checks & Failover:**

```bash
# Health check
aws route53 create-health-check --caller-reference $(date +%s) \
  --health-check-config '{
    "IPAddress": "52.1.2.3",
    "Port": 443,
    "Type": "HTTPS",
    "ResourcePath": "/health"
  }'

# Failover routing policy
# Primary: us-east-1
# Secondary: us-west-2 (when primary unhealthy)
```

**5. Runbook for DR:**

```markdown
## Disaster Recovery Runbook

### Trigger
- AWS region outage > 30 minutes
- Decision by incident commander

### Steps
1. [ ] Verify outage is region-wide (not just our services)
2. [ ] Notify stakeholders
3. [ ] Promote RDS replica to primary
4. [ ] Update DNS to DR region
5. [ ] Verify services healthy
6. [ ] Monitor for 1 hour
7. [ ] Post-incident: Plan failback
```

### 🧠 Bài học

- **Multi-region không optional** - Cho production critical
- **RTO/RPO defined** - Biết expect gì khi outage
- **DR tested regularly** - Ít nhất quarterly
- **Runbooks ready** - Không improvise khi panic

---

## 📝 AWS Best Practices Checklist

- [ ] Budget alerts configured
- [ ] S3 Block Public Access (account level)
- [ ] Tagging policy enforced
- [ ] Session Manager enabled (no SSH)
- [ ] Multi-AZ for production databases
- [ ] Cross-region backups
- [ ] DR runbook documented
- [ ] Cost optimization review monthly
