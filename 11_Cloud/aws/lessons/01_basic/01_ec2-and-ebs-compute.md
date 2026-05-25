# 🎓 EC2 + EBS — Compute foundation

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [00_what-is-aws-overview.md](00_what-is-aws-overview.md), [Cloud networking basics](../../../cloud-fundamentals/lessons/01_basic/02_cloud-networking.md)

> 🎯 *EC2 = AWS's flagship compute. Hiểu **instance types** (T/M/C/R/X family), **AMI**, **EBS** volumes, **key pairs**, **user data**, **Auto Scaling Groups** basics. Deploy first EC2 with web server.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **EC2 instance types** (T/M/C/R/X family + sizes)
- [ ] Tạo + launch EC2 instance (Console + CLI)
- [ ] **AMI** — pick + create custom
- [ ] **EBS volumes** + types + snapshots
- [ ] **Key pair** SSH access
- [ ] **User data** scripts for bootstrap
- [ ] **Security Group** rules for EC2
- [ ] **Elastic IP** (EIP) static public IP
- [ ] **ASG** (Auto Scaling Group) basics
- [ ] **Spot vs On-demand vs Reserved** pricing

---

## Tình huống — Deploy first FastAPI on EC2

Bạn vừa code FastAPI app local. Cần deploy somewhere:
- Vercel: easy nhưng JS-focused.
- DigitalOcean: $10/month basic.
- AWS EC2: industry standard, more control, more learning.

Sếp: *"Try EC2 first. Standard for production. Học EC2 = học AWS compute foundation."*

→ Bài này dạy deploy FastAPI on EC2 end-to-end.

---

## 1️⃣ EC2 instance types

### Family naming

```
Instance type: t3.medium
                │  │
                │  └─ Size (nano/micro/small/medium/large/xlarge/.../48xlarge)
                └─ Family (T3 = burstable general purpose)
```

### Families 2026

| Family | Optimization | Example | Use case |
|---|---|---|---|
| **T** (T3, T4g) | Burstable, cheap | t3.medium | Dev, small web app, burst workload |
| **M** (M5, M6i, M7i) | General purpose | m6i.large | Balanced web/app servers |
| **C** (C5, C6i, C7i) | Compute-optimized | c6i.xlarge | CPU-heavy: gaming, scientific |
| **R** (R5, R6i, R7i) | Memory-optimized | r6i.xlarge | DB, in-memory cache |
| **X** (X1, X2) | High memory | x1.32xlarge | SAP HANA, in-memory DB |
| **I** (I3, I4i) | High I/O (NVMe SSD) | i4i.xlarge | NoSQL DB, data warehouse |
| **D** (D3, D3en) | Dense storage HDD | d3.xlarge | Big data, distributed file |
| **P** (P4, P5) | GPU (training) | p5.xlarge | ML training |
| **G** (G5, G6) | GPU (inference) | g6.xlarge | ML inference, video |
| **Inf** (Inf1, Inf2) | AWS Trainium/Inferentia | inf2.xlarge | Custom AI chips, cheaper |
| **Mac** | macOS | mac1.metal | iOS build |

### Generation

- Number after family = generation.
- Newer = better price/performance.
- 2026 latest: **7th generation** (Intel Sapphire Rapids, AMD Genoa, Graviton4).

```
m5    → 2018 (Intel Skylake)
m5a   → AMD EPYC
m6i   → 2021 (Intel Ice Lake)
m6g   → 2020 (Graviton2 ARM)
m6a   → 2021 (AMD)
m7i   → 2023 (Intel Sapphire Rapids)
m7g   → 2022 (Graviton3 ARM)
m7a   → 2024 (AMD Genoa)
```

→ **2026 recommend**: m7i for x86, m7g for ARM (cheaper, similar perf).

### Sizes

```
nano   = 1 vCPU, 0.5 GB RAM     (very small)
micro  = 1 vCPU, 1 GB
small  = 1 vCPU, 2 GB
medium = 2 vCPU, 4 GB
large  = 2 vCPU, 8 GB
xlarge = 4 vCPU, 16 GB
2xlarge = 8 vCPU, 32 GB
4xlarge = 16 vCPU, 64 GB
...
48xlarge = 192 vCPU, 768 GB     (huge)
```

→ Each step roughly 2x. Pick smallest that fits + ASG for variability.

### Burstable (T family) — Caveat

**T family** has **CPU credits**:
- Baseline performance (e.g., 20% of vCPU for t3.medium).
- Burst above baseline → consume credits.
- Credits accumulate when idle.

**T3.medium**:
- 24 credits/hour earn.
- Baseline 20% (= ~0.4 vCPU full).
- Can burst to 100% (2 vCPU) for short periods.

**T3 Unlimited mode** (default 2026):
- If credits exhausted, charged $0.05/vCPU-hour over-baseline.
- Predictable performance, variable cost.

**T3 Standard mode**:
- If credits exhausted, **throttled** to baseline.
- Predictable cost, variable performance.

→ Use T for dev/small workload. Use M/C/R for steady production (consistent CPU).

🪞 **Ẩn dụ**: *T instance như **gói data 4G prepaid** — 20% baseline + accumulate khi không dùng. Burst high-speed khi cần. M instance như **fiber dedicated** — consistent.*

### Pricing examples (us-east-1, on-demand, Linux, 2026)

| Type | Specs | $/hour | $/month |
|---|---|---|---|
| t3.micro | 2 vCPU, 1 GB | $0.0104 | $7.50 |
| t3.medium | 2 vCPU, 4 GB | $0.0416 | $30 |
| m7i.large | 2 vCPU, 8 GB | $0.1008 | $73 |
| m7i.xlarge | 4 vCPU, 16 GB | $0.2016 | $146 |
| c7i.xlarge | 4 vCPU, 8 GB | $0.1785 | $129 |
| r7i.xlarge | 4 vCPU, 32 GB | $0.2646 | $192 |

→ **Reserved 1-year** save ~30%, **3-year** save ~60%. **Spot** save 60-90%.

---

## 2️⃣ AMI — Amazon Machine Image

### What is AMI

**AMI** = template for EC2 instance:
- OS + pre-installed software.
- Bootable snapshot.
- Region-bound.

### Standard AMIs

| AMI | Provider | Use |
|---|---|---|
| **Amazon Linux 2023** | AWS | AWS-optimized, free, recommended for AWS-specific |
| **Ubuntu 22.04 / 24.04** | Canonical | Most popular for app deploy |
| **Debian 12** | Debian Project | Stable, conservative |
| **RHEL 9 / 10** | Red Hat | Enterprise, paid |
| **SUSE** | SUSE | Enterprise |
| **macOS** | AWS (special) | iOS dev, expensive |
| **Windows Server 2022/2025** | Microsoft | Windows workloads |

→ **2026 recommend**: Ubuntu 24.04 LTS for general use. Amazon Linux 2023 for tight AWS integration.

### Find AMI

```bash
# Latest Amazon Linux 2023
aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=al2023-ami-*-x86_64" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text

# Latest Ubuntu 24.04
aws ec2 describe-images \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd*ubuntu-noble-24.04-amd64-server-*" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text
```

### Custom AMI

Build your own:
```bash
# After configuring EC2:
aws ec2 create-image \
  --instance-id i-abc \
  --name "myapp-v1.0.0" \
  --description "FastAPI app + dependencies"

# Returns AMI ID, can launch many EC2 from this AMI
```

→ Faster than running user data scripts on each launch. Use for golden images.

### AMI vs container

| Aspect | AMI | Container (Docker) |
|---|---|---|
| Granularity | Full OS + app | App + minimum deps |
| Size | GB | MB |
| Build tool | Packer + AWS | Dockerfile |
| Boot time | 30-90 seconds | 1-10 seconds |
| Portability | AMI region-bound | Docker portable any cloud |

→ **Containers prefer 2026** (faster, portable). AMI for: legacy apps, specialized OS config, regulatory.

### Packer for AMI building

```hcl
# packer.pkr.hcl
source "amazon-ebs" "ubuntu" {
  ami_name      = "myapp-{{timestamp}}"
  instance_type = "t3.medium"
  region        = "ap-southeast-1"
  source_ami    = "ami-..."  # base Ubuntu 24.04
  ssh_username  = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]
  
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y python3-pip nginx",
      "pip3 install fastapi uvicorn",
    ]
  }
}
```

```bash
packer build packer.pkr.hcl
# Builds AMI, registers
```

→ Modern AMI build pipeline.

---

## 3️⃣ EBS volumes

### What is EBS

**EBS** = Elastic Block Store. Network-attached disk for EC2.

- Bound to AZ (can't attach to EC2 in different AZ).
- Persistent (survives instance stop/start, restart).
- Snapshot to S3 (cross-region copy possible).
- One EBS = one EC2 typically (Multi-Attach limited).

### Volume types

| Type | Use | Cost | IOPS |
|---|---|---|---|
| **gp3** (general purpose SSD) | Default 2026, predictable | $0.08/GB/mo | 3K-16K |
| **gp2** (older gp) | Older deploys | $0.10/GB/mo | 3 IOPS/GB up to 16K |
| **io2 Block Express** | High-perf DB | $0.125/GB/mo + $0.065/IOPS | 256K |
| **st1** (HDD throughput) | Big sequential read | $0.045/GB/mo | — |
| **sc1** (HDD cold) | Infrequent | $0.025/GB/mo | — |

→ **gp3 default 2026**. io2 cho production DB. st1/sc1 cho cold data.

### gp3 sizing

Default 100 GB gp3:
- 3,000 IOPS included.
- 125 MB/s throughput included.
- Cost: $8/month.

Need more IOPS? Pay extra:
- IOPS above 3,000: $0.005/IOPS-month.
- Throughput above 125: $0.04/MB/s-month.

Example: 100GB + 10K IOPS:
- Storage: $8.
- IOPS: 7000 × $0.005 = $35.
- Total: $43/month.

### Boot volume + data volume

```
EC2 instance has:
  - 1 boot volume (root, OS)  — typically 8-20 GB
  - 0+ data volumes (app data, logs)  — variable
```

### EBS snapshots

```bash
aws ec2 create-snapshot \
  --volume-id vol-abc \
  --description "Daily backup"

# Restore:
aws ec2 create-volume \
  --snapshot-id snap-xyz \
  --volume-type gp3 \
  --availability-zone us-east-1a
```

→ Incremental (only changed blocks). Stored in S3 (managed).

**Cost**: $0.05/GB/month for snapshot storage.

### Backup strategy

```bash
# Daily, retain 7 days
aws backup create-backup-plan \
  --backup-plan '{
    "BackupPlanName": "daily-ebs",
    "Rules": [{
      "RuleName": "DailyBackups",
      "TargetBackupVaultName": "Default",
      "ScheduleExpression": "cron(0 2 * * ? *)",
      "Lifecycle": {
        "DeleteAfterDays": 7
      }
    }]
  }'
```

→ **AWS Backup** service automate. Cross-region copy for DR.

---

## 4️⃣ Key pairs + SSH access

### Create key pair

```bash
# Create key pair
aws ec2 create-key-pair \
  --key-name my-key \
  --query 'KeyMaterial' \
  --output text > my-key.pem

chmod 400 my-key.pem
```

→ Public key stored in AWS. Private key (`.pem`) keep secret.

### Launch EC2 with key

```bash
aws ec2 run-instances \
  --image-id ami-abc \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-xyz \
  --subnet-id subnet-pqr
```

### SSH into EC2

```bash
ssh -i my-key.pem ubuntu@<public-ip>
# Or for Amazon Linux:
ssh -i my-key.pem ec2-user@<public-ip>
```

### Issue: SSH key management at scale

Problems:
- Share `.pem` file? Insecure.
- 50 engineers, 1 key? When someone leaves, rotate for everyone.
- Lose key = lose EC2 access forever.

### Solution: AWS Systems Manager Session Manager

**No SSH** at all:

```bash
# Install SSM Agent (default Amazon Linux 2023, Ubuntu 24.04)
# Attach IAM role with SSM permissions to EC2

# Then:
aws ssm start-session --target i-abc123
```

→ Direct shell, IAM-authenticated, audit logged, no SSH port open, no key management.

### Best practice 2026

- **Don't open port 22** to internet.
- **Use SSM Session Manager** for shell access.
- **Or AWS Client VPN** + bastion for SSH.
- **Or Tailscale / WireGuard** mesh VPN.

→ Eliminate SSH attack surface.

---

## 5️⃣ User data — Bootstrap scripts

### What's user data

Shell script that runs on **first boot** of EC2.

```bash
#!/bin/bash
# user-data.sh
apt-get update
apt-get install -y nginx python3-pip
pip3 install fastapi uvicorn

cat > /home/ubuntu/app.py <<EOF
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from EC2!"}
EOF

cat > /etc/systemd/system/myapp.service <<EOF
[Unit]
Description=FastAPI app
After=network.target

[Service]
ExecStart=/usr/bin/uvicorn app:app --host 0.0.0.0 --port 8000
WorkingDirectory=/home/ubuntu
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

systemctl enable myapp
systemctl start myapp
```

### Launch with user data

```bash
aws ec2 run-instances \
  --image-id ami-abc \
  --instance-type t3.medium \
  --key-name my-key \
  --user-data file://user-data.sh \
  --security-group-ids sg-xyz \
  --subnet-id subnet-pqr
```

→ User data executed once. Logs in `/var/log/cloud-init-output.log` for debug.

### Use cases

- **Install software**: Docker, app, dependencies.
- **Configure**: SSH keys, sysctl, hostname.
- **Start service**: systemd.
- **Pull code**: clone repo + `make install`.

### Cloud-init

User data uses **cloud-init** (default Linux EC2).

`#cloud-config` format alternative:
```yaml
#cloud-config
packages:
  - nginx
  - python3-pip
runcmd:
  - pip3 install fastapi
  - systemctl start nginx
write_files:
  - path: /etc/myapp.conf
    content: |
      foo=bar
```

→ Declarative alternative to shell.

### Caveats

- **Runs once** (first boot). Re-run = re-launch instance.
- **No secrets in user data** — visible to anyone with EC2 read.
- **Logs visible**: don't echo passwords.
- **Time-limited**: 16 KB max user data size.

### Modern alternative

**Use AMI with pre-baked software** (Packer) + minimal user data for config-only.

→ Faster boot (no install delay), reproducible.

---

## 6️⃣ Security Group for EC2

### Default SG for web server

```hcl
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id
  
  # HTTP from internet
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # HTTPS from internet
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # SSH from office IP only
  # (Better: no SSH, use Session Manager)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["1.2.3.4/32"]
  }
  
  # All outbound (default)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Multi-tier SG pattern

(Recall cloud-networking bài 02)

```
Internet → ALB SG (443/80 open) → App SG (8000 from ALB) → DB SG (5432 from App)
```

```hcl
resource "aws_security_group" "alb" {
  ingress { from_port = 443 to_port = 443 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
}

resource "aws_security_group" "app" {
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]   # reference SG
  }
}

resource "aws_security_group" "db" {
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}
```

---

## 7️⃣ Elastic IP (EIP)

### Use case

EC2 by default has dynamic public IP — changes on stop/start.

**EIP** = static public IP assigned to account.

```bash
# Allocate EIP
aws ec2 allocate-address --domain vpc

# Associate with EC2
aws ec2 associate-address \
  --instance-id i-abc \
  --allocation-id eipalloc-xyz
```

### Cost

- Allocated + attached to running EC2: **free**.
- Allocated but NOT attached: **$0.005/hour ($3.60/month)** — penalty for hoarding.
- 5 EIP per account limit (default).

### When use EIP

- Need static IP for whitelist (3rd party firewall).
- DNS pointing to fixed IP.

### Don't need EIP when

- App behind ALB (LB has DNS, not IP).
- Auto Scaling Group (instances ephemeral).

→ Most apps don't need EIP. Use LB + DNS.

---

## 8️⃣ Auto Scaling Group (ASG) — Basics

### Why ASG

Single EC2:
- Crashes → downtime.
- Traffic spike → overload.

ASG:
- **Multi-AZ**: instances across AZs.
- **Auto-replace**: dead instance replaced automatically.
- **Auto-scale**: more instances on high load.

### Components

1. **Launch Template**: blueprint for EC2 (AMI, type, SG, user data).
2. **Auto Scaling Group**: min/max/desired count.
3. **Scaling policies**: trigger rules (CPU > 70% → +2 instances).

### Terraform example

```hcl
resource "aws_launch_template" "web" {
  name_prefix   = "web-"
  image_id      = "ami-abc"
  instance_type = "t3.medium"
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = base64encode(file("user-data.sh"))
  
  tag_specifications {
    resource_type = "instance"
    tags = { Name = "web-asg" }
  }
}

resource "aws_autoscaling_group" "web" {
  name                = "web-asg"
  min_size            = 2
  max_size            = 10
  desired_capacity    = 2
  
  vpc_zone_identifier = [
    aws_subnet.private[0].id,
    aws_subnet.private[1].id,
    aws_subnet.private[2].id,
  ]
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  
  health_check_type         = "ELB"
  health_check_grace_period = 60
  
  target_group_arns = [aws_lb_target_group.web.arn]
  
  tag {
    key                 = "Name"
    value               = "web-asg"
    propagate_at_launch = true
  }
}

# Scale up on high CPU
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 300
  autoscaling_group_name = aws_autoscaling_group.web.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 120
  statistic           = "Average"
  threshold           = 70
  
  alarm_actions = [aws_autoscaling_policy.scale_up.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.web.name
  }
}
```

### ASG features

- **Target tracking**: maintain target metric (e.g., CPU at 50%).
- **Step scaling**: tiered (CPU > 70% +2, > 90% +5).
- **Scheduled scaling**: scale based on time (business hours).
- **Predictive scaling**: ML-based (AWS predicts demand).

→ Bài K8s intermediate cluster has similar patterns (HPA + Cluster Autoscaler).

---

## 9️⃣ EC2 pricing — On-demand vs Reserved vs Spot

### On-demand

- Pay per second (Linux) or hour (Windows).
- Highest cost.
- No commitment.

**Use**: dev, unpredictable workload, testing.

### Reserved Instances (RI) / Savings Plans

**Commit 1 or 3 years for discount**:
- 1-year: 30-40% off.
- 3-year: 50-72% off.

**Savings Plans** (more flexible than RI):
- Compute Savings Plans: any region, any family.
- EC2 Instance Savings Plans: specific family + region.

**Use**: predictable baseline workload (steady production).

```bash
# View Reserved Instance recommendations
aws ce get-reservation-purchase-recommendation \
  --service "AmazonEC2"
```

### Spot Instances

**Use unused AWS capacity**:
- 60-90% off on-demand price.
- AWS can interrupt with **2-minute warning**.

**Use cases**:
- Stateless workers.
- Batch jobs.
- CI/CD runners.
- Fault-tolerant apps.

**Avoid for**:
- Stateful (DB).
- Long-running single instance.
- Real-time customer-facing.

```bash
aws ec2 request-spot-instances \
  --spot-price "0.05" \
  --instance-count 5 \
  --launch-specification file://spec.json
```

→ Cheap but risky. Combine with on-demand for HA.

### Pricing strategy

```
Production:
  Baseline: Reserved Instances (40% off) — 70% of capacity
  Burst: On-demand — 20% of capacity
  Spot-tolerant workers: Spot — 10% of capacity
  
Result: ~50% savings vs all on-demand
```

→ Mix strategies for optimal cost/reliability.

---

## 🔟 Hands-on: Deploy FastAPI on EC2 end-to-end

### Step 1: Pre-requisites

- AWS account.
- AWS CLI configured.
- VPC with public subnet (from cloud-fundamentals bài 02).

### Step 2: Security group

```bash
aws ec2 create-security-group \
  --group-name fastapi-sg \
  --description "FastAPI web" \
  --vpc-id vpc-abc

# Allow HTTP + HTTPS (replace sg-id)
SG_ID=sg-xyz
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp --port 443 --cidr 0.0.0.0/0
```

### Step 3: Key pair

```bash
aws ec2 create-key-pair \
  --key-name fastapi-key \
  --query 'KeyMaterial' \
  --output text > fastapi-key.pem
chmod 400 fastapi-key.pem
```

### Step 4: User data script

`user-data.sh`:
```bash
#!/bin/bash
set -e

apt-get update
apt-get install -y python3-pip nginx

pip3 install fastapi uvicorn[standard]

mkdir -p /opt/myapp
cat > /opt/myapp/app.py <<'EOF'
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hello from EC2 via FastAPI!",
        "time": datetime.utcnow().isoformat()
    }

@app.get("/health")
def health():
    return {"status": "ok"}
EOF

cat > /etc/systemd/system/myapp.service <<'EOF'
[Unit]
Description=FastAPI app
After=network.target

[Service]
ExecStart=/usr/local/bin/uvicorn app:app --host 127.0.0.1 --port 8000
WorkingDirectory=/opt/myapp
User=www-data
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Nginx config (proxy)
cat > /etc/nginx/sites-available/myapp <<'EOF'
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

systemctl enable myapp
systemctl start myapp
systemctl restart nginx
```

### Step 5: Find Ubuntu AMI

```bash
AMI_ID=$(aws ec2 describe-images \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd*ubuntu-noble-24.04-amd64-server-*" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text)

echo $AMI_ID
```

### Step 6: Launch EC2

```bash
aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.medium \
  --key-name fastapi-key \
  --security-group-ids $SG_ID \
  --subnet-id subnet-public-abc \
  --user-data file://user-data.sh \
  --associate-public-ip-address \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=fastapi-demo}]' \
  --query 'Instances[0].InstanceId' \
  --output text
```

### Step 7: Verify

```bash
INSTANCE_ID=i-abc...   # from previous output

# Wait for instance to be ready (~30 seconds boot + ~2 min user data)
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Visit: http://$PUBLIC_IP"

# Test
curl http://$PUBLIC_IP
# {"message":"Hello from EC2 via FastAPI!","time":"..."}

curl http://$PUBLIC_IP/health
# {"status":"ok"}
```

### Step 8: SSH (for debug)

```bash
ssh -i fastapi-key.pem ubuntu@$PUBLIC_IP

# Check service
sudo systemctl status myapp

# Check logs
sudo journalctl -u myapp -f

# Logout
exit
```

### Step 9: Cleanup (avoid charges!)

```bash
aws ec2 terminate-instances --instance-ids $INSTANCE_ID
aws ec2 delete-security-group --group-id $SG_ID
aws ec2 delete-key-pair --key-name fastapi-key
rm fastapi-key.pem
```

→ Always cleanup test resources!

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Forget to cleanup → bills

→ Test EC2 running forever. $30+/month silently.

→ **Fix**:
- Tag test resources clearly.
- Daily/weekly cleanup audit.
- Use AWS Budget alerts.

### ❌ Pitfall: Open SSH to 0.0.0.0/0

→ Bots brute force.

→ **Fix**:
- SSM Session Manager (no SSH port).
- Or SSH from specific IP only.
- Or VPN/Tailscale.

### ❌ Pitfall: T-class instance for production

→ Burstable, CPU credits exhausted → throttle → app slow.

→ **Fix**: M/C/R for production. T only for dev/burst-tolerant.

### ❌ Pitfall: EBS too small, fill up

→ Volume full → app crash.

→ **Fix**:
- Monitor EBS usage (CloudWatch).
- Alert at 80%.
- Resize live (`modify-volume` for gp3) — no downtime.

### ❌ Pitfall: No backups

→ EBS volume gone (instance terminated, snapshot deleted) → data lost.

→ **Fix**:
- AWS Backup automated.
- Snapshot policy.
- Test restore quarterly.

### ❌ Pitfall: Hardcode IP in app config

→ EC2 IP changes on restart (unless EIP). App breaks.

→ **Fix**: 
- Use ALB DNS (changes don't propagate).
- Or Route 53 record.
- Or EIP if must have IP.

### ✅ Best practice: Tag everything

```hcl
tags = {
  Name        = "fastapi-prod-1"
  Environment = "prod"
  Service     = "api"
  Team        = "backend"
  CostCenter  = "engineering"
}
```

→ Cost allocation, automation, compliance.

### ✅ Best practice: Use IAM role, not access keys

EC2 needs S3 access:
- ❌ Hardcode access key in env.
- ✅ Attach IAM role to EC2. SDK auto-gets credentials.

### ✅ Best practice: Spot for stateless workers

CI runners, batch jobs:
- Use spot instances.
- Save 60-90%.
- Acceptable interruption.

### ✅ Best practice: Right-size + RI

After 1 month production:
- Review CPU/memory usage.
- Right-size (often smaller).
- Buy RI for steady baseline.

→ Save 30-60% via discipline.

---

## 🧠 Self-check

**Q1.** When use T-class vs M-class instances?

<details>
<summary>💡 Đáp án</summary>

**T-class** (T3, T4g) — burstable:
- Baseline CPU performance (e.g., 20% of vCPU).
- Burst above baseline with CPU credits.
- Cheap (50-70% less than M).

**Use T-class**:
- **Dev/staging**: low utilization, OK with variability.
- **Low-traffic apps**: small websites, internal tools.
- **Bursty workloads**: spike then idle.
- **Cost-sensitive**: budget tight.

**M-class** — general purpose, consistent:
- Steady CPU all-time.
- Higher cost, predictable performance.

**Use M-class**:
- **Production web/app servers**: consistent traffic.
- **CPU-bound**: API servers, app logic.
- **DB**: medium-scale RDS.

**Avoid T-class when**:
- Consistent high CPU (credits exhausted → throttled or extra charge).
- Customer-facing prod (predictable performance critical).
- High-frequency batch processing.

**T3 Unlimited mode**:
- Default 2026.
- Burst as much as needed.
- Charged $0.05/vCPU-hour above baseline.
- If burst average < baseline, no extra cost.
- If burst average exceeds baseline, M-class often cheaper.

**Decision**:
- Predictable workload at ≤ 20% CPU → T3.
- Variable, low-average CPU → T3 (cheap baseline).
- Consistent high CPU → M class.

**Real example**:
- Internal dashboard, 10% CPU: t3.medium = $30/month. m6i.large = $73/month. T wins.
- Production API, 50% CPU: t3.medium charged extra credits ~$50/month. m6i.large = $73, predictable. M better.

→ Check actual CPU usage via CloudWatch metrics. Right-size monthly.
</details>

**Q2.** AMI vs container — when each for AWS?

<details>
<summary>💡 Đáp án</summary>

**Container (Docker on ECS/EKS/Fargate)**:
- **Lightweight**: MB, not GB.
- **Fast boot**: 1-10 seconds.
- **Portable**: same image any cloud.
- **Layered**: efficient builds + caching.
- **Modern**: 2026 standard for new apps.

**Use containers when**:
- Modern app development.
- Microservices.
- CI/CD pipeline.
- K8s ecosystem.
- Multi-cloud strategy.

**AMI**:
- **Full OS snapshot**.
- **Slow boot**: 30-90 seconds.
- **AWS-bound**: AMI per region.
- **Includes runtime**: Java, Python, etc. pre-installed.

**Use AMI when**:
- **Legacy app**: hardcoded to OS-level dependencies.
- **Specific kernel/OS config**: not containerizable.
- **Compliance**: gov/regulated where container = new risk.
- **Long-running stateful**: VMs are fine, container overhead unnecessary.
- **EC2-only deployments**: not using ECS/EKS.

**Hybrid**:
- **AMI** = pre-installed runtime + agent.
- **Container** = app code.
- E.g., AMI has Docker pre-installed, EC2 pulls container at boot.

**Reality 2026**:
- **New apps**: containers (95% of cases).
- **Legacy**: AMI or lift-and-shift.
- **Specialized**: AMI for HPC, ML training (large VMs with GPUs).

**Choosing**:
- **Greenfield**: containers.
- **Lift-and-shift from on-prem**: AMI initially, refactor to containers later.
- **Stateless web app**: containers.
- **Database**: managed service (RDS), not AMI or container.

**Build pipelines**:
- AMI: Packer.
- Container: Docker + ECR.

→ Default 2026: containers. AMI for specific cases.
</details>

**Q3.** EBS gp3 vs gp2 — should I migrate?

<details>
<summary>💡 Đáp án</summary>

**gp2** (older general purpose SSD, 2014+):
- IOPS tied to size: 3 IOPS/GB.
- 100GB = 300 IOPS, 1TB = 3000 IOPS.
- $0.10/GB/month.
- Burst: 3000 IOPS for short bursts.

**gp3** (newer, 2020+):
- **Independent IOPS + throughput**: not tied to size.
- Baseline: 3000 IOPS + 125 MB/s **for any size**.
- $0.08/GB/month (**20% cheaper**).
- Extra IOPS: $0.005/IOPS-month above 3000.
- Extra throughput: $0.04/MB/s-month above 125.

**Migration benefits**:

For 100GB volume:
- gp2: $10/month + 300 IOPS.
- gp3: $8/month + 3000 IOPS.
- **gp3 cheaper AND 10x more IOPS**.

For 1TB volume:
- gp2: $100/month + 3000 IOPS.
- gp3: $80/month + 3000 IOPS.
- gp3 **20% cheaper**.

For 4TB volume (high IOPS need):
- gp2: $400/month + 12000 IOPS (burst).
- gp3: $320/month + 12000 IOPS (provisioned).
- gp3 **20% cheaper, consistent performance**.

**Migration steps**:

```bash
# In-place migration (no downtime, no data loss)
aws ec2 modify-volume \
  --volume-id vol-abc \
  --volume-type gp3
```

→ Live migration over a few hours. App keeps running.

**When NOT to migrate**:

- **Very small volumes** (< 50GB): cost diff trivial.
- **Constrained AWS old account**: edge cases with old configurations.

**When YES (almost always)**:

- 50GB+: cheaper.
- High IOPS needs: gp3 customizable.
- New deployments: gp3 default.

**Verify after migration**:
- Performance same or better.
- Cost reduced next bill.

**Real example** (medium production):
- 5 EC2, each 200GB EBS = 1TB total.
- gp2: $100/month.
- gp3: $80/month + free 3000 IOPS each.
- Savings: $240/year. Easy win.

**At scale**:
- Large fleet 100TB EBS: $1000+ savings/month.
- ROI: 1 hour migration script.

→ **Migrate to gp3 default 2026**. No reason to stay gp2.
</details>

**Q4.** Spot instances trade-offs — what workloads?

<details>
<summary>💡 Đáp án</summary>

**Spot instances**:
- 60-90% discount vs on-demand.
- Can be **interrupted with 2-minute warning**.
- Price varies hourly (market).

**Good workloads** (fault-tolerant):

1. **Stateless workers**:
   - Image processing.
   - Video encoding.
   - Batch ETL jobs.
   - CI/CD runners.

2. **Distributed systems**:
   - Kafka consumers (re-process from offset).
   - K8s spot nodes (pods rescheduled).
   - Hadoop/Spark batch (retry tasks).

3. **Test/dev environments**:
   - Acceptable interruption.
   - Save 80% on non-critical.

4. **Burst capacity**:
   - Spike workloads with spot, baseline with on-demand.

**Bad workloads** (avoid spot):

1. **Stateful**:
   - Databases (data loss risk).
   - Long-running build with no checkpoint.

2. **Real-time**:
   - Customer-facing APIs (sudden interruption = downtime).
   - WebSocket connections.

3. **Single-instance critical**:
   - One key service, no redundancy.

**Spot strategies**:

**Capacity-Optimized**:
- AWS recommends instance type with lowest interruption probability.
- Best for: long-running tasks, sensitive to interruption.

**Lowest-Price**:
- Cheapest instance type.
- Best for: maximum savings, very fault-tolerant.

**Diversified**:
- Spread across multiple instance types/AZs.
- Best for: high resilience, less chance of total interruption.

**Spot fleet vs Spot instances**:
- **Spot fleet**: multi-type, multi-AZ, mix on-demand + spot, target capacity.
- **Spot instances**: simpler, less flexible.

**Handling interruption**:

```bash
# Inside EC2: check metadata
curl http://169.254.169.254/latest/meta-data/spot/instance-action
# If 2-min warning, gracefully shut down
```

```python
# Application-level
import requests
def check_spot_termination():
    r = requests.get('http://169.254.169.254/latest/meta-data/spot/instance-action', timeout=2)
    if r.status_code == 200:
        # 2-min warning, drain + save state + exit
        cleanup_and_exit()
```

**Cost-savings examples**:

- 100 CI runners running 8h/day workdays:
  - On-demand m5.large: 100 × 8h × 20 days × $0.10 = $1600/month.
  - Spot m5.large (60% off): $640/month.
  - **Savings: $960/month**.

**Tools**:
- **Karpenter** (K8s): mixes spot + on-demand intelligently.
- **AWS Spot Advisor**: analyze interruption rates.

→ Spot for any fault-tolerant workload = huge savings.

**Anti-patterns**:
- DB on spot.
- Critical single-instance service on spot.
- "Just spot everything" without graceful handling.
</details>

**Q5.** ASG vs manual EC2 scaling — when needed?

<details>
<summary>💡 Đáp án</summary>

**Manual scaling**: provision N EC2 statically. Resize manually when needed.

**ASG (Auto Scaling Group)**: dynamic, automated.

**Use ASG when**:

1. **Traffic varies significantly**:
   - Day vs night.
   - Weekday vs weekend.
   - Black Friday spike.

2. **High availability required**:
   - Multi-AZ instances.
   - Auto-replace failed instances.

3. **Cost optimization**:
   - Scale down at low traffic.
   - Save 30-70% vs over-provisioned static.

4. **Stateless workload**:
   - Web servers, API.
   - Workers.

**Manual scaling OK when**:

1. **Predictable workload**:
   - Internal tool, 9-5 weekday only.

2. **Very small scale**:
   - 1-2 instances.
   - Manual restart acceptable.

3. **Stateful single-instance**:
   - Specific DB instance.
   - Cache server with state.

**ASG features**:

- **Min/Max/Desired count**.
- **Multi-AZ distribution**.
- **Auto-replace** failed instances (Health check).
- **Scaling policies**:
  - Target tracking (e.g., CPU 50%).
  - Step scaling (tiered).
  - Scheduled (cron-based).
  - Predictive (ML-based).

**Trade-offs**:

- **Stateless required**: EC2 may terminate/launch. App must handle.
- **Boot time**: instances need bootstrap (user data) before serving traffic. Often 1-5 min.
- **Cost spike during scale-up**: temporary over-capacity.

**Patterns**:

1. **Web tier**: ASG behind ALB. Multi-AZ. Scale on CPU/RPS.
2. **Worker tier**: ASG processing queue. Scale on queue depth.
3. **Cache tier**: NOT ASG. Use ElastiCache (managed).
4. **DB tier**: NOT ASG. Use RDS or DynamoDB.

**Modern alternative**:
- **K8s + HPA + Cluster Autoscaler**: more flexible than ASG, but more complex.
- **Fargate**: serverless containers, no instance management.
- **Lambda**: serverless functions, scales to zero.

**Decision**:
- 1-2 static instances: manual.
- Variable workload, stateless: ASG.
- K8s shop: K8s autoscaling.
- Serverless candidate: Lambda/Fargate.

→ ASG is **standard for stateless tier with variable load**. Default for production web/app.

**Anti-pattern**:
- Try to ASG a database or stateful service.
- Forget to terminate orphan instances.
- No metric to trigger scale → no actual scaling.
- Scale up but never scale down (cost spike).
</details>

---

## ⚡ Cheatsheet

```bash
# === EC2 ===
aws ec2 describe-instances
aws ec2 run-instances --image-id ami-xxx --instance-type t3.medium --key-name key
aws ec2 start-instances --instance-ids i-abc
aws ec2 stop-instances --instance-ids i-abc
aws ec2 terminate-instances --instance-ids i-abc
aws ec2 describe-instance-types --instance-types t3.medium

# === AMI ===
aws ec2 describe-images --owners amazon --filters Name=name,Values="al2023-ami-*"
aws ec2 create-image --instance-id i-abc --name "myapp-v1"

# === EBS ===
aws ec2 describe-volumes
aws ec2 create-volume --size 100 --volume-type gp3 --availability-zone us-east-1a
aws ec2 attach-volume --volume-id vol-abc --instance-id i-xyz --device /dev/sdf
aws ec2 modify-volume --volume-id vol-abc --volume-type gp3 --iops 10000
aws ec2 create-snapshot --volume-id vol-abc --description "Backup"

# === Key pairs ===
aws ec2 create-key-pair --key-name my-key --query 'KeyMaterial' --output text > my-key.pem
chmod 400 my-key.pem
aws ec2 describe-key-pairs

# === Security groups (recap) ===
aws ec2 create-security-group --group-name app-sg --vpc-id vpc-abc
aws ec2 authorize-security-group-ingress --group-id sg-abc --protocol tcp --port 443 --cidr 0.0.0.0/0

# === EIP ===
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-abc --allocation-id eipalloc-xyz
aws ec2 release-address --allocation-id eipalloc-xyz

# === ASG ===
aws autoscaling describe-auto-scaling-groups
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg --min-size 2 --max-size 10
aws autoscaling set-desired-capacity --auto-scaling-group-name web-asg --desired-capacity 5

# === Session Manager (no SSH) ===
aws ssm start-session --target i-abc

# === User data ===
# In run-instances: --user-data file://user-data.sh
# Or base64: --user-data $(base64 user-data.sh)

# Verify user data executed
ssh ubuntu@ec2-ip "cat /var/log/cloud-init-output.log"
```

```hcl
# === Terraform EC2 + ASG + ALB ===
resource "aws_launch_template" "web" {
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  
  user_data = base64encode(file("user-data.sh"))
  
  iam_instance_profile { name = aws_iam_instance_profile.app.name }
  
  network_interfaces {
    security_groups = [aws_security_group.web.id]
  }
}

resource "aws_autoscaling_group" "web" {
  min_size            = 2
  max_size            = 10
  desired_capacity    = 3
  vpc_zone_identifier = aws_subnet.private[*].id
  
  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }
  
  target_group_arns = [aws_lb_target_group.web.arn]
}

resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "cpu-target"
  autoscaling_group_name = aws_autoscaling_group.web.name
  policy_type            = "TargetTrackingScaling"
  
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 50.0
  }
}
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **EC2** | Elastic Compute Cloud (virtual machines) |
| **Instance type** | EC2 size + family (t3.medium, m6i.large) |
| **Instance family** | T/M/C/R/X/I/D/P/G (use case-optimized) |
| **Instance size** | nano/micro/small/medium/large/xlarge/... |
| **Generation** | Number after family (m5, m6i, m7i) |
| **Burstable (T)** | Burst above baseline using CPU credits |
| **CPU credits** | Earned when idle, spent when bursting (T-class) |
| **AMI** | Amazon Machine Image (EC2 template) |
| **Region** | Geographic cluster of datacenters |
| **AZ** | Availability Zone (datacenter within region) |
| **EBS** | Elastic Block Store (network disk) |
| **Volume type** | gp3/io2/st1/sc1 (EBS performance tier) |
| **Snapshot** | EBS backup to S3 (incremental) |
| **Key pair** | SSH public/private key |
| **User data** | Shell script run on first boot |
| **cloud-init** | Linux EC2 boot script processor |
| **Security Group** | Stateful firewall per resource |
| **Elastic IP (EIP)** | Static public IP |
| **Launch Template** | EC2 blueprint (newer than Launch Config) |
| **Auto Scaling Group (ASG)** | Group of EC2 with scaling policies |
| **Target tracking** | ASG scale to maintain metric target |
| **Step scaling** | ASG tiered scaling rules |
| **On-demand** | Pay per use, no commitment |
| **Reserved Instance (RI)** | 1-3 year commit, 30-70% discount |
| **Savings Plan** | Flexible commit (Compute, EC2 Instance) |
| **Spot Instance** | 60-90% off, interruptible |
| **Spot fleet** | Multi-type, multi-AZ spot strategy |
| **Session Manager** | SSH-less access via AWS IAM |
| **IAM instance profile** | Attach IAM role to EC2 |
| **Packer** | HashiCorp tool building AMI |
| **EC2 metadata** | http://169.254.169.254/ — instance info |
| **IMDSv2** | Secure metadata version (2026 default) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_what-is-aws-overview.md](00_what-is-aws-overview.md)
- → Tiếp: [02_s3-deep-and-iam.md](02_s3-deep-and-iam.md) *(sắp viết)*
- ↑ Cluster: [AWS README](../../README.md)

### Cross-reference
- ☁️ [Cloud Fundamentals networking](../../../cloud-fundamentals/lessons/01_basic/02_cloud-networking.md) — VPC + SG context
- ☁️ [Cloud Fundamentals storage](../../../cloud-fundamentals/lessons/01_basic/03_storage-and-databases.md) — block storage overview
- 🐳 [Docker basic](../../../../10_DevOps/docker/lessons/01_basic/) — containers vs AMI

### Tài nguyên ngoài
- 📖 [EC2 docs](https://docs.aws.amazon.com/ec2/)
- 📖 [EC2 instance types](https://aws.amazon.com/ec2/instance-types/)
- 📖 [EBS docs](https://docs.aws.amazon.com/ebs/)
- 📖 [EC2 pricing](https://aws.amazon.com/ec2/pricing/)
- 📖 [Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/)
- 📖 [Packer docs](https://www.packer.io/docs)
- 📖 [Auto Scaling docs](https://docs.aws.amazon.com/autoscaling/)
- 📖 [SSM Session Manager docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 01 AWS basic cluster. EC2 instance families + sizes + generations + burstable T-class + AMI (standard + custom + Packer) + EBS volume types + snapshots + key pairs + user data scripts + Security Group patterns + Elastic IP + Auto Scaling Group basics + pricing (on-demand/RI/spot) + hands-on FastAPI on EC2 end-to-end. 6 pitfall + 4 best practice + 5 self-check + cheatsheet.
