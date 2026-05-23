# ✅ Solutions: Network Advanced

---

## Exercise 1: VPC Design

```
VPC: 10.0.0.0/16

AZ-a Subnets:
  - Public:   10.0.1.0/24   (256 IPs)
  - Private:  10.0.10.0/24  (256 IPs)
  - Database: 10.0.100.0/24 (256 IPs)

AZ-b Subnets:
  - Public:   10.0.2.0/24
  - Private:  10.0.20.0/24
  - Database: 10.0.200.0/24

Route Tables:
  - Public: 0.0.0.0/0 → Internet Gateway
  - Private: 0.0.0.0/0 → NAT Gateway
  - Database: Local only (no internet)
```

---

## Exercise 2: Security Rules

```bash
# Web Security Group
aws ec2 create-security-group --group-name web-sg --vpc-id vpc-xxx

# Inbound: HTTP, HTTPS from anywhere
aws ec2 authorize-security-group-ingress --group-id sg-web \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id sg-web \
  --protocol tcp --port 443 --cidr 0.0.0.0/0

# App Security Group
# Inbound: Only from web-sg
aws ec2 authorize-security-group-ingress --group-id sg-app \
  --protocol tcp --port 3000 --source-group sg-web

# DB Security Group
# Inbound: Only from app-sg
aws ec2 authorize-security-group-ingress --group-id sg-db \
  --protocol tcp --port 5432 --source-group sg-app
```

---

**[← Back to Exercises](./EXERCISES.md)**
