# 🎓 Cloud Networking — VPC, Subnets, Peering, VPN

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [01_regions-availability-zones-edge.md](01_regions-availability-zones-edge.md), [Networking basics](../../../../05_networking/)

> 🎯 *Cloud network ≠ physical network. **VPC** = your private network in cloud. Bài này dạy: VPC + subnet (public/private) + Internet Gateway + NAT + route tables + security groups + peering + VPN + Direct Connect. Vendor-neutral concepts, AWS-flavored examples.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **VPC** = isolated virtual network in cloud
- [ ] **Subnet**: public vs private vs isolated
- [ ] **Internet Gateway** (IGW) vs **NAT Gateway**
- [ ] **Route tables** — how traffic flows
- [ ] **Security Group** vs **Network ACL** (stateful vs stateless)
- [ ] **VPC Peering** — connect VPCs
- [ ] **VPN** + **Direct Connect** — hybrid cloud connectivity
- [ ] **Transit Gateway** — hub-and-spoke for multi-VPC
- [ ] Pricing surprises (NAT Gateway, egress)

---

## Tình huống — App expose port 5432 ra Internet, hack 2 ngày

Dev deploy Postgres trên EC2:
```
EC2 (Postgres):  Public IP 54.123.45.67, port 5432 open to 0.0.0.0/0
```

Connection string in app: `postgres://admin:password@54.123.45.67:5432/db`.

2 ngày sau:
- Bots scan port 5432 worldwide.
- Brute force `admin/password` → succeeded.
- `pg_dump`, exfiltrate data.
- Drop tables.

Sếp post-mortem:
- *"Database should NEVER be on public IP."*
- *"App in public subnet, DB in private subnet, only app talks DB."*
- *"Security group restrict who can access what."*

→ Bài này dạy correct cloud network design.

---

## 1️⃣ VPC — Virtual Private Cloud

### Definition

**VPC** = isolated virtual network trong cloud account. Your private space.

- **IP range** (CIDR): you pick (e.g., 10.0.0.0/16 = 65,536 IPs).
- **Isolated**: other AWS customers can't see your VPC.
- **Region-bound**: VPC exists in 1 region (but spans AZs within region).

### Default VPC

AWS creates default VPC per region per account:
- CIDR `172.31.0.0/16`.
- 1 subnet per AZ (public).
- Internet Gateway attached.

→ Convenient for learning, **not for production**. Build custom VPC for control.

### CIDR planning

CIDR = cách chia private IP range cho VPC. Quy ước: dùng RFC 1918 (`10.x.x.x` phổ biến nhất), VPC /16 đủ cho hàng chục nghìn IP. **Quan trọng**: nếu định peer VPC sau (multi-region, multi-account, on-prem VPN), các VPC **không được trùng CIDR** — không sửa được sau khi đã có resource:

```
10.0.0.0/16    = 10.0.0.0 - 10.0.255.255  (65,536 IPs, /16)
10.0.0.0/24    = 10.0.0.0 - 10.0.0.255    (256 IPs, /24)
10.0.0.0/28    = 10.0.0.0 - 10.0.0.15     (16 IPs, /28)
```

**RFC 1918 private ranges**:
- `10.0.0.0/8` (16M IPs) — most common for VPC.
- `172.16.0.0/12` (1M IPs).
- `192.168.0.0/16` (65K IPs) — home network usually.

**Recommended VPC CIDR**:
- **Per-VPC**: `/16` (65K IPs).
- **Avoid overlap** if planning to peer VPCs.

**Pattern**:
- Dev: `10.0.0.0/16`.
- Staging: `10.1.0.0/16`.
- Prod us-east: `10.2.0.0/16`.
- Prod eu-west: `10.3.0.0/16`.

→ No overlap = can peer/VPN later.

🪞 **Ẩn dụ**: *VPC như **khu chung cư riêng tư**. Bạn có cả tòa nhà (VPC), tự chia phòng (subnets), kiểm soát ai vào (security groups), có cổng ra phố (Internet Gateway).*

---

## 2️⃣ Subnet — Slicing the VPC

### Types

**Public subnet**:
- Has route to Internet Gateway (IGW).
- Resources can have public IPs.
- Direct internet access (bidirectional).
- Use for: load balancers, NAT, bastion hosts.

**Private subnet**:
- No route to IGW.
- Resources only have private IPs.
- Outbound via NAT Gateway → IGW.
- Use for: app servers, databases.

**Isolated subnet**:
- No internet access at all (in or out).
- Use for: ultra-sensitive (PCI, medical).

### Multi-AZ subnet pattern

Pattern production tiêu chuẩn: **3 tier (public/private/db) × 3 AZ = 9 subnet**. Public chứa Load Balancer + NAT, Private chứa app server, DB subnet chứa database isolated. Trải đều 3 AZ để chịu được 1 AZ chết. Subnet `/24` (251 IP usable) đủ cho ~100 app instance:

```
VPC 10.0.0.0/16
  ├── Public Subnet AZ-a   10.0.0.0/24   (256 IPs, for LB)
  ├── Public Subnet AZ-b   10.0.1.0/24
  ├── Public Subnet AZ-c   10.0.2.0/24
  ├── Private Subnet AZ-a  10.0.10.0/24  (apps)
  ├── Private Subnet AZ-b  10.0.11.0/24
  ├── Private Subnet AZ-c  10.0.12.0/24
  ├── DB Subnet AZ-a       10.0.20.0/24  (databases)
  ├── DB Subnet AZ-b       10.0.21.0/24
  └── DB Subnet AZ-c       10.0.22.0/24
```

→ 3 tiers (public/private/db) × 3 AZs = 9 subnets.

### Why separate DB subnet?

DB subnet riêng có 3 lý do thực tế. **Isolation**: app subnet không thể truy cập DB trực tiếp — phải qua security group rule cụ thể. **Compliance**: PCI/HIPAA bắt buộc DB phải nằm trong subnet không có route đến Internet. **Cost**: DB không cần NAT (không gọi API ngoài) → tiết kiệm phí NAT processing:

- **Isolation**: DB only accessible from app subnet (security group).
- **Compliance**: PCI requires DB in isolated subnet.
- **Routing**: no NAT for DB subnet (saves cost).

### Reserved IPs per subnet

AWS reserves **5 IPs per subnet**:
- `.0`: Network address.
- `.1`: VPC router.
- `.2`: DNS server.
- `.3`: Future use.
- `.255` (last): Broadcast.

→ `/24` = 256 - 5 = 251 usable IPs.

---

## 3️⃣ Internet Gateway (IGW)

### What is IGW?

**IGW** = bridge VPC ↔ Internet.

- 1 IGW per VPC.
- Attached at VPC level.
- Horizontally scaled, no SPOF.
- Free (no cost).

### How traffic flows

IGW vận hành như một **NAT 1:1**: EC2 có cả private IP (10.0.0.5) và public IP (54.123.45.67). Khi packet ra Internet, IGW thay private IP bằng public IP; khi packet về, IGW translate ngược lại. Quy trình diễn ra trong suốt — EC2 không "biết" mình có public IP:

```
EC2 in public subnet (10.0.0.5, ENI has public IP 54.123.45.67)
  ↓
Route table: 0.0.0.0/0 → IGW
  ↓
IGW translates: 10.0.0.5 ↔ 54.123.45.67 (1:1 NAT)
  ↓
Internet
```

→ EC2 needs **both private IP + public IP** for internet access. IGW does NAT for you.

### Without IGW

EC2 in private subnet:
- Has only private IP (10.0.10.5).
- No route to internet.
- Can't reach `apt-get` repos.
- Can't reach Stripe API.

→ Need **NAT Gateway** for outbound only.

---

## 4️⃣ NAT Gateway — Outbound for private subnet

### Use case

Private subnet apps need:
- `apt-get install nginx`.
- `pip install requests`.
- Call Stripe API.

But shouldn't accept inbound from internet.

→ NAT Gateway: outbound only.

### How NAT works

NAT Gateway khác IGW: làm **N:1 NAT** (nhiều private IP chia sẻ 1 public IP). EC2 private gửi packet → route đến NAT (nằm ở public subnet) → NAT thay source IP + port, gửi qua IGW. Khi response về, NAT lookup connection table để trả đúng EC2. **Asymmetric**: outbound OK, inbound bị block:

```
EC2 private (10.0.10.5)
  ↓
Route table: 0.0.0.0/0 → NAT Gateway
  ↓
NAT Gateway (in public subnet, has public IP 54.123.45.67)
  ↓
Translates: 10.0.10.5:50000 ↔ 54.123.45.67:50000
  ↓
IGW → Internet
```

→ Internet sees traffic from NAT's public IP, not EC2's private IP. **Asymmetric**: outbound OK, inbound blocked (no port-forward configured).

### NAT Gateway cost (⚠️ surprise!)

NAT Gateway charges:
- **$0.045/hour** (~$33/month per NAT Gateway).
- **$0.045 per GB processed** (in + out).

→ App with 1TB/month traffic = $45/month bandwidth + $33/month NAT = ~$78/month.

Multi-AZ: 3 NAT Gateways = $99/month base.

**Cost optimization**:
- Single NAT (vs per-AZ): cheap, but SPOF.
- **VPC Endpoints** for AWS services (S3, DynamoDB free): bypass NAT for AWS calls.
- **Cloudflare R2 / no-egress storage**: avoid NAT for object storage.

### NAT instance vs NAT Gateway

- **NAT Gateway** (managed): scaled, HA. Cost: $33+/month.
- **NAT instance** (DIY EC2): t3.micro $7/month. Manual setup, security updates, SPOF unless HA configured.

→ NAT Gateway default. NAT instance OK for dev/test.

### Egress-only Internet Gateway (IPv6)

For IPv6:
- NAT not needed (IPv6 addresses globally routable).
- **Egress-only IGW**: outbound only, free.

→ IPv6 deploy can save NAT cost.

---

## 5️⃣ Route Tables

### Concept

**Route table** = rules deciding traffic destination.

```
Public Subnet route table:
  10.0.0.0/16 → local           (intra-VPC)
  0.0.0.0/0  → IGW              (internet)

Private Subnet route table:
  10.0.0.0/16 → local           (intra-VPC)
  0.0.0.0/0  → NAT Gateway      (internet via NAT)
  10.1.0.0/16 → VPC Peer        (peer VPC)
  172.16.0.0/12 → VPN Gateway   (on-prem via VPN)
```

→ Specific (longest match) wins.

### Per-subnet route table

Each subnet attached to 1 route table (default if not specified). Can share route tables across subnets.

**Pattern**:
- 1 route table for all **public subnets** (route to IGW).
- 1 route table per AZ for **private subnets** (route to AZ's NAT, save cross-AZ).

### Diagnose routing

```bash
# AWS CLI
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-abc

# Check which subnet → which route table
aws ec2 describe-route-table-associations
```

---

## 6️⃣ Security Group (SG)

### Concept

**Security Group** = virtual firewall **per resource** (EC2, RDS, Lambda).

- **Stateful**: response traffic auto-allowed (no need to allow return).
- **Allow rules only** (no explicit deny — implicit deny everything).
- Up to ~60 rules per SG.
- Multiple SGs per resource.

### Rules

```
Inbound:
  Allow TCP 443 from 0.0.0.0/0      (HTTPS from internet)
  Allow TCP 80 from 0.0.0.0/0       (HTTP)
  Allow TCP 22 from 1.2.3.4/32      (SSH from office IP only)

Outbound:
  Allow ALL to 0.0.0.0/0            (default — egress anywhere)
```

### SG referencing SG

Powerful pattern: reference another SG instead of IP.

```
App SG (sg-app):
  Inbound: TCP 8000 from sg-lb (Load Balancer SG)

DB SG (sg-db):
  Inbound: TCP 5432 from sg-app (App SG)

LB SG (sg-lb):
  Inbound: TCP 443 from 0.0.0.0/0
  Inbound: TCP 80 from 0.0.0.0/0
```

→ Diagram:
```
Internet → LB SG (443/80 open) → App SG (8000 from LB) → DB SG (5432 from App)
```

**No need to specify IPs**. Resources auto-discover by SG. Even if IPs change, rule holds.

### Default SG

Default VPC SG:
- **Inbound**: allows traffic from same SG (intra-SG).
- **Outbound**: allows all.

→ OK for dev. Production: restrict explicitly.

### SG vs OS firewall (iptables)

Both can exist:
- **SG** = cloud-level (AWS).
- **iptables** = OS-level (inside EC2).

→ Belt + suspenders. SG enforced before traffic reaches EC2. iptables additional defense inside EC2.

---

## 7️⃣ Network ACL (NACL)

### Concept

**NACL** = stateless firewall at **subnet** level.

- Stateless: must allow both inbound + outbound.
- Allow + Deny rules (NACL different from SG).
- Numbered priorities.
- Default: allow all.

### NACL vs SG

| Aspect | Security Group | Network ACL |
|---|---|---|
| Scope | Per resource (EC2, RDS) | Per subnet |
| Stateful | Yes (response auto-allow) | No (must allow both) |
| Rules | Allow only | Allow + Deny |
| Priority | All evaluated | First match wins |
| Default | Deny all inbound | Allow all |
| Use case | Service-level access | Subnet-level coarse |

### When use NACL

- **Block specific IPs** (SG doesn't deny).
- **Subnet-level isolation**.
- **Defense-in-depth** (extra layer).

Example: block bot IPs at NACL.

```
NACL rules:
  100  ALLOW  TCP 443  0.0.0.0/0     Inbound
  110  DENY   ALL      8.8.8.8/32    Inbound (block 8.8.8.8)
  120  ALLOW  ALL      0.0.0.0/0     Inbound
```

→ Most teams skip NACL (SG enough). NACL for compliance / specific scenarios.

---

## 8️⃣ VPC Peering

### Use case

2 VPCs need to communicate:
- Microservices in separate VPCs (per team).
- Shared services VPC (logging, monitoring).
- M&A (acquired company VPC).

### VPC Peering

```
VPC A (10.0.0.0/16) ↔ peering connection ↔ VPC B (10.1.0.0/16)

Route table A:
  10.1.0.0/16 → pcx-abc (peering)

Route table B:
  10.0.0.0/16 → pcx-abc

Security group:
  Allow traffic from peer VPC's SG / CIDR
```

→ Resources in both VPCs communicate via private IPs (no internet hop).

### Limitations

- **No transitive**: VPC A ↔ B ↔ C does NOT mean A ↔ C.
- **No CIDR overlap**: VPC A 10.0.0.0/16 + VPC B 10.0.0.0/16 = can't peer.
- **Cross-region peering**: supported but with cross-region data transfer cost.
- **Limit ~125 peer per VPC** (AWS).

### Transit Gateway

Solution for N+ VPCs:

```
            Transit Gateway (hub)
        ┌───────┼───────┬───────┐
       VPC A  VPC B  VPC C  VPC D ... VPC N
        │       │       │       │
      on-prem (via VPN)
```

→ Single hub, all VPCs attach. Transitive routing.

**Cost**: $0.05/hour ($36/month) + $0.02/GB data processed.

**When**: 5+ VPCs OR multi-account multi-VPC OR hybrid cloud.

---

## 9️⃣ Hybrid: VPN + Direct Connect

### Hybrid cloud use case

Connect on-prem datacenter ↔ cloud VPC:
- App in cloud, DB on-prem (compliance).
- Burst capacity to cloud.
- Migration in progress.

### Site-to-Site VPN

**VPN over internet** (encrypted tunnel).

```
On-prem firewall ←─ encrypted tunnel ─→ AWS VPN Gateway → VPC
```

**Setup**:
- AWS side: VPN Gateway in VPC.
- On-prem side: Customer Gateway (router with VPN capability).
- IPsec tunnel established.

**Pros**:
- Quick setup (hours).
- Encrypted.
- Inexpensive ($36/month + data).

**Cons**:
- Goes over internet (latency variable, ~50-200ms RTT).
- Bandwidth limited (1.25 Gbps per tunnel).
- Not for high-throughput.

### Direct Connect (DX)

**Dedicated fiber** AWS ↔ on-prem (via colocation partner).

```
On-prem ←─ private fiber ─→ Direct Connect location ←→ AWS region
```

**Pros**:
- Consistent latency (1-5ms within metro).
- High bandwidth (1-100 Gbps).
- No internet routing.
- Reduced egress cost (cheaper than internet egress).

**Cons**:
- Expensive: $0.30+/hour ($220+/month) + port + cross-connect.
- Setup weeks (physical fiber).
- Single fiber = SPOF unless redundant.

**When**:
- > 10 Gbps consistent traffic.
- Compliance / regulatory.
- Hybrid cloud with predictable workload.

### Mix: DX + VPN

DX primary + VPN backup. If DX fiber cut, VPN takes over.

---

## 🔟 VPC Endpoints

### Problem

App in private subnet calls S3:
```
EC2 → NAT Gateway → IGW → Internet → S3 (in same region!)
```

→ NAT processes traffic → cost. Routes through internet → latency + security.

### VPC Endpoint solution

**VPC Endpoint** = private connection to AWS service.

**Gateway Endpoint** (free):
- **S3, DynamoDB only**.
- Route table entry: S3 IP range → Gateway Endpoint.
- Traffic stays AWS backbone.

**Interface Endpoint** (PrivateLink, $0.01/hour):
- Other AWS services (Lambda, ECR, Secrets Manager, KMS, etc.).
- ENI in your subnet with private IP.
- DNS for service resolves to endpoint IP.

### Setup Gateway Endpoint S3

```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id          = aws_vpc.main.id
  service_name    = "com.amazonaws.us-east-1.s3"
  route_table_ids = [aws_route_table.private.id]
}
```

→ Route table updated: S3 IP range → endpoint. Traffic bypasses NAT.

**Savings**: 1TB/month S3 traffic via NAT = $45/month. Via endpoint = $0.

---

## 1️⃣1️⃣ Hands-on: Production VPC design

### Goals

- Multi-AZ (3 AZs).
- Public + private + DB tiers.
- NAT for outbound.
- VPC endpoints for AWS services.
- Security groups per tier.

### Terraform

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = { Name = "prod-vpc" }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Public subnets (3 AZs)
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = "ap-southeast-1${["a", "b", "c"][count.index]}"
  map_public_ip_on_launch = true
  
  tags = { Name = "public-${count.index}", Tier = "public" }
}

# Private subnets
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = "ap-southeast-1${["a", "b", "c"][count.index]}"
  
  tags = { Name = "private-${count.index}", Tier = "private" }
}

# DB subnets
resource "aws_subnet" "db" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = "ap-southeast-1${["a", "b", "c"][count.index]}"
  
  tags = { Name = "db-${count.index}", Tier = "db" }
}

# NAT Gateways (1 per AZ for HA)
resource "aws_eip" "nat" {
  count  = 3
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}

# Public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  count          = 3
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private route tables (1 per AZ for AZ-local NAT)
resource "aws_route_table" "private" {
  count  = 3
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
}

resource "aws_route_table_association" "private" {
  count          = 3
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# DB subnets: no internet route (isolated)
resource "aws_route_table" "db" {
  vpc_id = aws_vpc.main.id
  # Only local route, no NAT
}

# VPC Endpoint S3 (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.ap-southeast-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [
    aws_route_table.private[0].id,
    aws_route_table.private[1].id,
    aws_route_table.private[2].id,
  ]
}

# Security groups (LB → App → DB pattern)
resource "aws_security_group" "lb" {
  name   = "lb-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name   = "db-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
  
  # No egress needed (DB doesn't initiate)
}
```

### Result diagram

```
                Internet
                   │
                   ↓
            ┌──────────────┐
            │     IGW      │
            └──────────────┘
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
   Public AZ-a Public AZ-b Public AZ-c
   (LB nodes, NAT)
        │          │          │
   ┌────┴────┐┌────┴────┐┌────┴────┐
   │ NAT-A   ││ NAT-B   ││ NAT-C   │ (1 per AZ)
   └────┬────┘└────┬────┘└────┬────┘
        ↓          ↓          ↓
   Private AZ-a Private AZ-b Private AZ-c
   (App servers)
        │          │          │
        ↓          ↓          ↓
   DB AZ-a    DB AZ-b    DB AZ-c
   (RDS, isolated)

VPC Endpoint S3 → bypass NAT for S3 traffic
```

→ Production-grade. Multi-AZ HA. NAT per AZ (no cross-AZ NAT cost). SG layered defense.

### Cost estimate

- 3x NAT Gateway: $99/month base + traffic.
- 3x EIP: free (when attached).
- IGW: free.
- VPC + subnets + SG: free.
- S3 endpoint: free.
- Interface endpoints: $7-15/month each.

**Total network**: ~$100-130/month base.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Database in public subnet

→ Internet exposed, brute force, hack.

→ **Fix**: DB in private subnet. App in private. LB in public. Only LB faces internet.

### ❌ Pitfall: 1 NAT Gateway = SPOF + cross-AZ cost

```
Single NAT in AZ-a:
  - AZ-a outage = all NAT down.
  - Apps in AZ-b, AZ-c → cross-AZ → NAT in AZ-a = $0.01/GB cross-AZ + NAT cost.
```

→ **Fix**: NAT per AZ (3 NAT). Multi-AZ HA. No cross-AZ traffic for NAT.

**Cost trade-off**: 3 NAT vs 1 NAT = $66/month extra. Worth it.

### ❌ Pitfall: Hardcoded IPs in security group

```
ingress: cidr_blocks = ["10.0.1.5/32"]    # specific EC2 IP
```

→ EC2 replace = IP changes = SG rule broken.

→ **Fix**: Reference SG instead:
```
ingress: security_groups = [aws_security_group.app.id]
```

→ Auto-resolves to whatever EC2 has that SG.

### ❌ Pitfall: Open SSH to 0.0.0.0/0

```
ingress: TCP 22 from 0.0.0.0/0
```

→ Bot brute force.

→ **Fix**:
- SSH from office IP only: `cidr_blocks = ["1.2.3.4/32"]`.
- **Better**: AWS Systems Manager Session Manager — no SSH port needed, AWS IAM auth.
- **Best**: AWS Client VPN or Tailscale for team access.

### ❌ Pitfall: VPC CIDR too small

```
VPC: 10.0.0.0/24    # 256 IPs total
```

→ Can't grow. K8s alone needs 100+ IPs per node.

→ **Fix**: Default `/16` (65K IPs). Plenty for future.

### ❌ Pitfall: VPC CIDR overlap with on-prem

```
VPC: 10.0.0.0/16
On-prem: 10.0.0.0/16    # conflict!
```

→ Can't VPN/peering.

→ **Fix**: Coordinate CIDR allocation across cloud + on-prem. Document IPAM.

### ❌ Pitfall: NAT Gateway data transfer surprise

→ Apps download 10GB Docker images via NAT = $0.45/image. 100 deploys = $45.

→ **Fix**:
- Use VPC Endpoint for ECR (free for S3-backed ECR layers).
- Cache Docker images locally (registry mirror).
- Pull-through cache.

### ❌ Pitfall: SG too permissive "allow all"

```
ingress: protocol = "-1"; cidr_blocks = ["0.0.0.0/0"]
```

→ Everything open. SG useless.

→ **Fix**: Explicit ports + sources. Audit SG quarterly.

### ✅ Best practice: VPC per environment

```
- Dev VPC: 10.0.0.0/16
- Staging VPC: 10.1.0.0/16
- Prod VPC: 10.2.0.0/16
```

→ Strong isolation. Different SG, different IAM.

### ✅ Best practice: Flow logs enabled

VPC Flow Logs: log all network connections.

```hcl
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  log_destination = aws_s3_bucket.flow_logs.arn
}
```

→ Audit traffic. Detect anomalies. Forensics.

### ✅ Best practice: NACL default-deny + explicit allow

```
NACL: deny all → allow specific
```

→ Belt + suspenders with SG.

→ Most teams skip (SG enough). For compliance-strict, use NACL.

### ✅ Best practice: Bastion via Session Manager (no SSH key)

```
AWS Systems Manager Session Manager:
- No SSH port open.
- IAM-based access (not SSH key).
- Audit log per session.
- Multi-factor auth via IAM.
```

→ Replace `ssh -i key.pem ec2@public-ip` with `aws ssm start-session --target i-abc123`.

---

## 🧠 Self-check

**Q1.** Public subnet vs private subnet — main difference is route table, gì khác?

<details>
<summary>💡 Đáp án</summary>

**Defining difference**: route table.
- Public subnet: route 0.0.0.0/0 → IGW.
- Private subnet: route 0.0.0.0/0 → NAT (or no route at all = isolated).

**Other differences**:

1. **Public IP assignment**:
   - Public subnet typically `map_public_ip_on_launch = true`.
   - Private subnet: false (only private IP).

2. **Internet accessibility**:
   - Public: 2-way (inbound + outbound).
   - Private: outbound via NAT, no inbound from internet.

3. **Use cases**:
   - Public: load balancer, NAT, bastion, public API.
   - Private: app servers, internal services.
   - Isolated (no route): databases (compliance).

4. **Security implications**:
   - Public: must have strict SG (limit inbound).
   - Private: SG can be more permissive (limited reachability).

5. **Cost**:
   - Public: free (just IGW).
   - Private with internet: NAT Gateway cost.

**Convention**:
- Tier-1: only LB in public.
- Tier-2: app in private.
- Tier-3: DB in isolated.

**Anti-pattern**: putting database in public subnet. Common mistake → security breach.

→ Route table = technical answer. Architecture intent = security/cost driven.
</details>

**Q2.** Security Group stateful vs Network ACL stateless — implication?

<details>
<summary>💡 Đáp án</summary>

**Security Group (Stateful)**:
- Allow inbound TCP 443.
- Response traffic auto-allowed (no need explicit outbound rule).
- Connection tracking remembers initiator.

```
Inbound SG:
  TCP 443 from 0.0.0.0/0    ← only need this
Outbound SG:
  Default allow all          ← anyway permissive
```

→ User → LB:443 inbound allowed. LB response back to user → auto-allowed by stateful tracking.

**Network ACL (Stateless)**:
- Allow inbound TCP 443 — only handles inbound.
- Response goes outbound on **ephemeral port** (e.g., 50000-65535).
- Must explicitly allow outbound on ephemeral ports.

```
Inbound NACL:
  Rule 100: ALLOW TCP 443 from 0.0.0.0/0
  Rule 110: ALLOW TCP 1024-65535 from 0.0.0.0/0    ← response inbound (e.g., for outbound API call)
  
Outbound NACL:
  Rule 100: ALLOW TCP 1024-65535 to 0.0.0.0/0      ← response to client
  Rule 110: ALLOW TCP 443 to 0.0.0.0/0             ← outgoing HTTPS
```

→ Easy to misconfigure. Forget ephemeral port range = response blocked.

**Why ephemeral ports**:
- Connection: server:443 ↔ client:ephemeral (e.g., 54321).
- Response from server goes back on client's ephemeral port.
- OS allocates ephemeral 32768-60999 (Linux default).

**Practical**:
- **SG always stateful**: simpler, default for resource-level.
- **NACL stateless**: only when need DENY rules or subnet-wide blocks.

**Mistakes**:
- Apply NACL like SG → forget ephemeral range → mysterious connection issues.
- Default NACL allows all → seems to work → break when you add rules.

**Recommend**:
- Use SG for everything by default.
- NACL only for specific: block bot IPs, compliance, defense-in-depth.
- Document NACL rules carefully.

→ Stateful (SG) = easy. Stateless (NACL) = power but careful.
</details>

**Q3.** NAT Gateway cost optimization — top tactics?

<details>
<summary>💡 Đáp án</summary>

**NAT Gateway costs**:
- $0.045/hour × 720 hours = **$32.40/month per NAT** (base).
- $0.045/GB processed (in + out).

For 3-AZ HA setup: 3 NATs = $97/month base + traffic.

**Top optimization tactics**:

1. **VPC Endpoints for AWS services** (free for Gateway type):
   - S3, DynamoDB: Gateway endpoint, no cost.
   - Other (Lambda, ECR, KMS, etc.): Interface endpoint $7/month each.
   - **Savings**: AWS traffic bypasses NAT. Often 70%+ of NAT traffic.

2. **ECR pull-through cache + immutable tags**:
   - Cache base images locally.
   - Reduce ECR pull traffic.

3. **Cloudflare R2 or no-egress S3 alternative**:
   - R2 has 0 egress cost. Move large download workloads.

4. **HTTP/2 keep-alive + compression**:
   - Reduce data volume via compression (Brotli).
   - Connection pooling reduce overhead.

5. **CDN for outbound** (downloads from your app):
   - Static content via CloudFront / Cloudflare.
   - Origin pull from S3 (via Gateway endpoint, no NAT).

6. **Single NAT for non-prod**:
   - Dev/staging: 1 NAT (acceptable SPOF risk).
   - Saves $65/month (2 fewer NATs).

7. **IPv6 + egress-only IGW** (advanced):
   - Egress-only IGW free.
   - Modern infra: IPv6 outbound from private subnet, no NAT.

8. **Audit traffic to identify wasteful**:
   - VPC Flow Logs analyze.
   - Common waste: ECR over NAT, telemetry over NAT, package installs over NAT.

**Real example**:
- Before: 3 NATs + 5TB/month NAT traffic = $97 + $225 = $322/month.
- After VPC Endpoint S3 + ECR + pull-through cache: 5TB → 500GB = $97 + $22.5 = **$120/month**.
- **Savings**: 60% on NAT.

**At scale**:
- Large companies (Netflix, Stripe) often eliminate NAT entirely.
- Move to IPv6 + egress IGW.
- VPC Endpoints for everything AWS.
- Custom proxies for non-AWS outbound.

→ Audit NAT traffic. Most have 50%+ unnecessary.
</details>

**Q4.** When VPC Peering vs Transit Gateway?

<details>
<summary>💡 Đáp án</summary>

**VPC Peering**:
- Direct 1:1 connection between 2 VPCs.
- Non-transitive (A↔B + B↔C doesn't make A↔C).
- Free (no hourly charge).
- $0.01/GB cross-region transfer.

**Best for**:
- 2-3 VPCs total.
- Specific pairings only.
- Simple architecture.

**Transit Gateway** (hub):
- Hub-and-spoke: all VPCs connect to TGW.
- Transitive: A↔TGW↔B↔TGW↔C works.
- $0.05/hour ($36/month) + $0.02/GB.
- Can also connect VPN + Direct Connect.

**Best for**:
- 5+ VPCs.
- Multi-account architecture.
- Hybrid cloud (cloud + on-prem via VPN).
- Network segmentation (route policies).

**Decision matrix**:

| Scenario | Use |
|---|---|
| 2 VPCs need to talk | VPC Peering |
| Shared services VPC (1 → many) | VPC Peering (per spoke) or TGW |
| 5+ VPCs mesh | Transit Gateway |
| Multi-account (Organization) | Transit Gateway |
| Hybrid (cloud + on-prem VPN) | Transit Gateway |
| Cost-sensitive < $36/month justification | VPC Peering |

**N-to-N peering issue**:
- 5 VPCs need full mesh: 5*4/2 = **10 peering connections**.
- Each must be configured separately.
- Routes manual in each.
- N=10 = 45 connections.

**TGW solution**:
- 5 VPCs attach to 1 TGW.
- 5 attachments.
- Centralized routing.

**Cost compare** for 5 VPCs:
- Peering: 0 base + traffic.
- TGW: $36 base + $0.02/GB + attachment cost.

**Recommended**:
- < 4 VPCs: VPC Peering.
- 4+ VPCs OR hybrid: Transit Gateway.
- Multi-account always: TGW (RAM share).

**Alternative**: VPC Lattice (newer, application-layer):
- Service-to-service across VPCs.
- HTTP/gRPC, not raw network.
- Higher abstraction.
- Use when service mesh-like needs.
</details>

**Q5.** SG referencing SG vs CIDR block — pros/cons?

<details>
<summary>💡 Đáp án</summary>

**SG referencing SG**:
```
db_sg ingress:
  Allow TCP 5432 from sg-app
```

**Pros**:

1. **Dynamic**: app SG members change (new EC2, replace) — rule auto-applies.
2. **Readable**: intent clear ("DB accepts from app").
3. **Resilient to IP changes**: ASG scaling, instance replacement, no rule update needed.
4. **Cleaner**: no IP list to maintain.

**Cons**:

1. **Only within same VPC** (and peered VPCs in same region as of 2024).
2. **Cross-account / region**: need to use CIDR (until newer features).
3. **Audit harder**: "what IPs can reach DB?" requires querying SG membership.

**CIDR block reference**:
```
db_sg ingress:
  Allow TCP 5432 from 10.0.10.0/24
```

**Pros**:

1. **Cross-VPC / region / account**: works anywhere.
2. **Explicit**: IPs documented.
3. **Static**: known IP range.

**Cons**:

1. **Stale**: if subnet changes CIDR (rare), rule needs update.
2. **Overpermissive**: allowing entire `/24` includes non-app instances in subnet.
3. **Manual**: must update when topology changes.

**Recommended pattern**:

**Within same VPC**: prefer SG reference.
```
db_sg ingress: from sg-app
```

**Cross-VPC / on-prem**: CIDR.
```
db_sg ingress: from 192.168.10.0/24 (on-prem range)
```

**Cross-account (via Organizations)**: SG reference works via VPC sharing (newer AWS feature).

**Hybrid pattern**:
```
db_sg ingress:
  Allow TCP 5432 from sg-app             # intra-VPC dynamic
  Allow TCP 5432 from 10.1.0.0/16        # peered VPC range
  Allow TCP 5432 from 192.168.0.0/16     # on-prem VPN range
```

**Anti-pattern**:
- CIDR `0.0.0.0/0` to internal DB.
- Listing 50 specific IPs (use SG ref or subnet CIDR).
- Mixing both without clear pattern.

**Audit tool**:
- `aws ec2 describe-security-group-rules` → list all.
- Tools like Steampipe, Pacu for security audit.

→ SG reference = best within VPC. CIDR for cross-boundary.
</details>

---

## ⚡ Cheatsheet

```bash
# === VPC commands ===
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-abc

# === Security groups ===
aws ec2 describe-security-groups --group-ids sg-abc
aws ec2 authorize-security-group-ingress \
  --group-id sg-abc \
  --protocol tcp --port 443 --cidr 0.0.0.0/0

# === Route tables ===
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-abc

# === Flow logs ===
aws ec2 describe-flow-logs --filter Name=resource-id,Values=vpc-abc

# === VPC peering ===
aws ec2 create-vpc-peering-connection --vpc-id vpc-abc --peer-vpc-id vpc-def

# === Transit gateway ===
aws ec2 describe-transit-gateways
aws ec2 create-transit-gateway-vpc-attachment --transit-gateway-id tgw-abc --vpc-id vpc-abc

# === VPN ===
aws ec2 describe-vpn-connections
aws ec2 describe-customer-gateways

# === Endpoint ===
aws ec2 describe-vpc-endpoints
```

```hcl
# === VPC essentials ===
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

# Public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Route table → IGW
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id
}

# Security group SG-to-SG
resource "aws_security_group_rule" "db_from_app" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.app.id
  security_group_id        = aws_security_group.db.id
}

# VPC Endpoint S3 (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **VPC** | Virtual Private Cloud — isolated network in cloud |
| **CIDR** | Classless Inter-Domain Routing notation (e.g., 10.0.0.0/16) |
| **Subnet** | Slice of VPC, bound to 1 AZ |
| **Public subnet** | Has route to IGW |
| **Private subnet** | No direct internet, outbound via NAT |
| **Isolated subnet** | No internet, totally private |
| **IGW (Internet Gateway)** | VPC ↔ Internet bridge |
| **NAT Gateway** | Outbound-only internet for private subnet |
| **NAT instance** | DIY NAT on EC2 (older pattern) |
| **Route table** | Rules for traffic destination |
| **Security Group (SG)** | Stateful firewall at resource level |
| **Network ACL (NACL)** | Stateless firewall at subnet level |
| **VPC Peering** | Direct connection between 2 VPCs |
| **Transit Gateway (TGW)** | Hub for connecting many VPCs + on-prem |
| **VPC Endpoint (Gateway)** | Free, S3/DynamoDB only |
| **VPC Endpoint (Interface)** | PrivateLink, other AWS services |
| **VPN Gateway** | AWS side of site-to-site VPN |
| **Customer Gateway** | On-prem side of VPN |
| **Direct Connect (DX)** | Dedicated fiber AWS ↔ on-prem |
| **Egress** | Outbound traffic |
| **Ingress** | Inbound traffic |
| **Bastion host** | Jump server for SSH access |
| **Session Manager** | AWS shell access without SSH |
| **Flow Logs** | VPC network connection logs |
| **ENI** | Elastic Network Interface (virtual NIC) |
| **EIP** | Elastic IP (static public IP) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [01_regions-availability-zones-edge.md](01_regions-availability-zones-edge.md)
- → Tiếp: [03_storage-and-databases.md](03_storage-and-databases.md) *(sắp viết)*
- ↑ Cluster: [Cloud Fundamentals README](../../README.md)

### Cross-reference
- 🌐 [TCP/IP fundamentals](../../../../05_networking/tcp-ip-fundamentals/) — networking foundation
- 🏗️ [IaC Terraform basics](../../../../10_devops/iac/lessons/01_basic/01_terraform-basics.md) — VPC IaC
- ☸️ [K8s Services](../../../../10_devops/kubernetes/lessons/01_basic/02_services-and-networking.md) — VPC + K8s

### Tài nguyên ngoài
- 📖 [AWS VPC docs](https://docs.aws.amazon.com/vpc/)
- 📖 [GCP VPC docs](https://cloud.google.com/vpc/docs)
- 📖 [Azure Virtual Network docs](https://learn.microsoft.com/en-us/azure/virtual-network/)
- 📖 [AWS Networking Workshop](https://catalog.workshops.aws/networking/)
- 📖 [VPC sizing calculator](https://aws.amazon.com/blogs/networking-and-content-delivery/best-practices-vpc-sizing/)
- 📖 [Cloud Network Pricing](https://aws.amazon.com/vpc/pricing/)

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước CIDR planning + Multi-AZ subnet pattern + Why separate DB subnet + How traffic flows (IGW) + How NAT works.
- **v1.0.0 (24/05/2026)** — Bài 02 cluster cloud-fundamentals. VPC + subnet types + IGW + NAT Gateway + route tables + SG vs NACL + VPC Peering + Transit Gateway + VPN + Direct Connect + VPC Endpoints. Hands-on Terraform production VPC design. Apply security: DB in isolated subnet, SG-to-SG references, defense-in-depth.
