# 🖥️ Azure VM + Managed Disks — Compute foundation

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [00_what-is-azure-overview.md](00_what-is-azure-overview.md) ✅, hiểu VPC/Region/AZ cơ bản

> 🎯 *Azure VM = flagship compute, analog với AWS EC2 / GCP Compute Engine. Bài này dạy: **VM sizes** (B/D/E/F/L/N series + sub-series), **Managed Disks** (Standard HDD, Standard SSD, Premium SSD, Ultra Disk), **VMSS** (Virtual Machine Scale Sets), **Spot VM** + **Reserved Instances** + **Azure Hybrid Benefit**, **Just-in-Time access**, snapshot + backup. Hands-on deploy FastAPI trên VM Linux + auto-scale với VMSS.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **VM size families** (B/D/E/F/L/N) và khi dùng cái nào
- [ ] Phân biệt **Managed Disk** types: Standard HDD/SSD, Premium SSD v1/v2, Ultra Disk
- [ ] Setup VM với **cloud-init** (analog user data của EC2)
- [ ] Hiểu **Availability Zone vs Availability Set vs VMSS**
- [ ] Deploy **VMSS** auto-scale theo CPU
- [ ] Hiểu **Spot VM** + **Reserved Instance** + **Azure Hybrid Benefit** (giảm cost 30-72%)
- [ ] Setup **Just-in-Time (JIT)** access cho SSH/RDP
- [ ] Snapshot + Azure Backup cơ bản
- [ ] Hands-on: FastAPI trên VM + auto-scale qua VMSS

---

## Tình huống — Acme Shop scale website mùa sale 11.11

Sếp:

> *"Sale 11.11 traffic tăng 10x trong 2 ngày. Hiện chạy 1 VM Linux Standard_D2s_v5 — chắc chắn sập. Bạn deploy auto-scale: 1 VM baseline, scale lên 10 khi CPU > 70%, scale xuống khi < 30%. Tiết kiệm cost — dùng Spot VM cho phần scale, Reserved cho baseline. Backup hằng đêm. JIT SSH thay vì port 22 mở 24/7."*

Bạn cần:

- **VMSS** chạy FastAPI image.
- **Reserved Instance** cho 2 VM baseline (cam kết 1 năm = giảm 40%).
- **Spot VM** cho instance burst (giảm tới 90%).
- **Azure Backup** snapshot hằng đêm, giữ 7 ngày.
- **JIT** mở port 22 chỉ khi cần.

Bài này dạy từng phần + hands-on.

---

## 1️⃣ Azure VM size families

🪞 **Ẩn dụ**: *VM size như **menu nhà hàng** — Mỗi family là loại món (B = burger combo cân bằng giá rẻ; D = pizza general; E = mì Ý nhiều thịt = nhiều RAM; F = steak — CPU mạnh; L = buffet hải sản — nhiều SSD local; N = món GPU đặc biệt). Trong mỗi family, size (s, ms, l) là portion (nhỏ vừa lớn).*

### Naming convention

```
Standard_D4s_v5
         │ │  │
         │ │  └─ Version (v1, v2, ..., v5 mới nhất 2026)
         │ └─── Features: s=Premium SSD, m=high-mem, d=local NVMe, a=AMD, b=block storage
         └───── Family + vCPU count (D family, 4 vCPU)
```

### Families 2026

| Family | Optimization | Example | Use case |
|---|---|---|---|
| **B** (B1ls, B2ms, B4ms) | Burstable, rẻ nhất | B2s | Dev, small web, burst workload |
| **D** (Dv5, Dasv5, Ddsv5) | General purpose | D4s_v5 | Web/app server cân bằng |
| **E** (Ev5, Easv5, Edsv5) | Memory-optimized | E8s_v5 | DB, in-memory cache, SAP |
| **F** (Fsv2, Fxv2) | Compute-optimized | F4s_v2 | Batch, gaming server, scientific |
| **L** (Lsv3, Lasv3) | Storage-optimized (NVMe local) | L8s_v3 | NoSQL DB, data warehouse |
| **M** (Mv2, Mdsv2) | Memory huge (12 TB) | M128ms | SAP HANA |
| **N** (NCv3, NDv5, NVv5) | GPU | NC24s_v3 | ML training/inference, rendering |
| **H** (HBv4, HC) | HPC | HB120rs_v3 | Scientific compute |
| **A** (Av2) | Entry-level legacy | A1_v2 | Tests, không production |
| **G** (Gsv2) | Memory + I/O optimized | G5 | Legacy SAP (deprecated) |

### CPU vendor

- **Default**: Intel (Sapphire Rapids ở v5).
- Suffix **`a`**: AMD EPYC — rẻ hơn ~10%, perf tương đương Intel cho most workload.
- Suffix **`p`**: Ampere ARM (Cobalt 100) — rẻ hơn 30%, cần ARM-compatible binary.

→ **2026 recommend**: `Dasv5` (AMD general) cho web/app; `Edsv5` (Intel local NVMe) cho DB stateful; `Fsv2` cho CPU-bound batch.

### Sizes & vCPU/RAM/Disk

```
B1s     = 1 vCPU,  1 GB RAM,  free tier
B2s     = 2 vCPU,  4 GB RAM
B4ms    = 4 vCPU, 16 GB RAM (m=more RAM)
D2s_v5  = 2 vCPU,  8 GB RAM
D4s_v5  = 4 vCPU, 16 GB RAM
D8s_v5  = 8 vCPU, 32 GB RAM
E4s_v5  = 4 vCPU, 32 GB RAM (more RAM/vCPU ratio)
F4s_v2  = 4 vCPU,  8 GB RAM (less RAM, more CPU)
...
M128ms  = 128 vCPU, 3.8 TB RAM (huge)
```

→ Quy tắc: D có ratio 1 vCPU : 4 GB; E có 1 : 8; F có 1 : 2.

### So sánh AWS / GCP

| Azure | AWS | GCP |
|---|---|---|
| B (burstable) | T3/T4g | e2-burst |
| D (general) | M5/M6i/M7i | n2/n2d |
| E (memory) | R5/R6i/R7i | n2-highmem |
| F (compute) | C5/C6i/C7i | c2/c2d |
| L (storage) | I3/I4i | n2-localssd |
| N (GPU) | P/G/Inf | a2/a3 (TPU/GPU) |

---

## 2️⃣ Managed Disks — Block storage

### Disk types 2026

| Type | Use case | IOPS | Throughput | Cost (relative) |
|---|---|---|---|---|
| **Standard HDD** | Backup, dev, low cost | <500 | <60 MB/s | 1x (cheapest) |
| **Standard SSD** | Web server, dev/test | <6,000 | <750 MB/s | 1.5x |
| **Premium SSD v1** | Production DB, app | <20,000 | <900 MB/s | 3x |
| **Premium SSD v2** | High-perf DB (independent IOPS/throughput) | up to 80,000 | up to 1,200 MB/s | 3x (paying flexibility) |
| **Ultra Disk** | Top-tier DB (SAP HANA, Oracle) | up to 400,000 | up to 10,000 MB/s | 5-7x |

### Disk size + perf

```
Standard SSD:
  E1 (4 GiB)    → 500 IOPS, 60 MB/s
  E10 (128 GiB) → 500 IOPS, 60 MB/s
  E30 (1 TiB)   → 500 IOPS, 60 MB/s
  E80 (32 TiB)  → 2000 IOPS, 750 MB/s

Premium SSD v1:
  P10 (128 GiB) → 500 IOPS, 100 MB/s
  P30 (1 TiB)   → 5000 IOPS, 200 MB/s
  P80 (32 TiB)  → 20000 IOPS, 900 MB/s
```

→ **Quy tắc**: IOPS/throughput **scale theo size disk** (v1). Disk lớn = nhanh hơn. Trade-off cost.

### Premium SSD v2 (mới nhất)

Khác biệt: **decouple** size khỏi IOPS/throughput.

```
Premium SSD v2:
  Size:       1 GiB - 64 TiB
  IOPS:       3000 (free) + extra (charged)
  Throughput: 125 MB/s (free) + extra (charged)

Ví dụ:
  100 GiB + 10,000 IOPS + 500 MB/s = trả phí extra IOPS + throughput
```

→ Tốt cho workload **không cần size lớn nhưng cần IOPS cao**. Hiện chỉ available một số region; chưa support OS disk.

### Disk caching

```
ReadOnly  → cache read on host SSD (default for OS disk + Premium data disk)
ReadWrite → cache read + write (data có thể mất nếu host crash — chỉ dùng SQL Server log)
None      → bypass cache (cho write-heavy workload, log file)
```

```bash
# Set caching khi attach
az vm disk attach \
    --resource-group rg-prod-data \
    --vm-name vm-prod-db-01 \
    --name disk-prod-db-data \
    --caching ReadOnly
```

### Snapshot vs Backup

| Feature | Snapshot | Azure Backup |
|---|---|---|
| Granularity | Single disk | VM-level (all disks + config) |
| Cost | Pay incremental block | Pay per VM + retention |
| Retention | Bạn quản lý thủ công | Policy auto (daily/weekly/monthly/yearly) |
| App-consistent | Không (crash-consistent only) | Có (VSS Windows / pre-post script Linux) |
| Cross-region | Manual copy | Built-in GRS |

→ Production VM → Azure Backup (policy-based). Snapshot cho one-off (trước upgrade quan trọng).

---

## 3️⃣ High availability — AZ vs Availability Set vs VMSS

### Availability Zone (AZ)

- Datacenter vật lý tách biệt trong region (3 zones thông thường).
- VM trải qua nhiều zone → tolerate zone outage.
- SLA: 99.99% với 2+ zones.

```bash
# Deploy VM vào zone 1
az vm create --zone 1 --resource-group rg-prod --name vm-web-01 ...

# Deploy thêm vào zone 2, 3 cho HA
```

### Availability Set (legacy nhưng vẫn dùng)

- Group VM trong **cùng 1 datacenter** nhưng tách:
  - **Fault Domain (FD)**: tách rack (mất power, mất rack).
  - **Update Domain (UD)**: tách update batch (Microsoft maintenance).
- SLA: 99.95% (kém AZ).

```bash
az vm availability-set create \
    --resource-group rg-prod \
    --name avset-web \
    --platform-fault-domain-count 2 \
    --platform-update-domain-count 5
```

→ **2026 best practice**: **dùng AZ thay Availability Set**. Availability Set chỉ cho region không có AZ.

### Virtual Machine Scale Sets (VMSS)

= group VM identical, auto-scale theo metric.

```
VMSS:
  - 1 VM image base
  - Capacity: min=1, max=10
  - Scale rule: CPU > 70% → +1; CPU < 30% → -1
  - Across AZs: tự động spread 3 zone
  - Load Balancer attach: round-robin traffic
```

→ Analog AWS Auto Scaling Group / GCP Managed Instance Group.

### Orchestration mode

- **Uniform** (legacy): mọi VM identical, ít control per-VM.
- **Flexible** (mới, default 2024+): mix VM size, AZ, lifecycle per-VM — recommended.

```bash
az vmss create \
    --resource-group rg-prod-web \
    --name vmss-web-prod \
    --orchestration-mode Flexible \
    --image Ubuntu2204 \
    --vm-sku Standard_D2s_v5 \
    --instance-count 2 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --zones 1 2 3 \
    --upgrade-policy-mode Automatic
```

---

## 4️⃣ Pricing — Spot, Reserved, Hybrid Benefit

🪞 **Ẩn dụ**: *Cost optimization như **đặt vé máy bay** — Pay-as-you-go = mua tại quầy giá full; Reserved = mua sớm 1-3 năm trước (giảm 30-72%); Spot = vé last-minute siêu rẻ (nhưng có thể bị hủy bất cứ lúc nào); Hybrid Benefit = đem voucher Windows/SQL Server license sẵn của công ty (giảm 40% nữa).*

### Pricing options

| Option | Discount | Commitment | Use case |
|---|---|---|---|
| **Pay-As-You-Go (PAYG)** | 0% | Không | Dev, unpredictable workload |
| **Reserved Instance (RI) 1 năm** | up to 41% | 1 năm | Baseline production |
| **Reserved Instance 3 năm** | up to 62% | 3 năm | Long-term baseline |
| **Savings Plan 1 năm** | up to 28% | $/h flexible | Mix VM size flexible |
| **Savings Plan 3 năm** | up to 65% | $/h flexible | Long-term flexible |
| **Spot VM** | up to 90% | None (có thể bị evict) | Stateless batch, dev |
| **Azure Hybrid Benefit (AHB)** | up to 40% (Windows) + 55% (SQL) | License đã có | Customer có Windows/SQL Server license |

### Spot VM

```bash
# Tạo Spot VM với eviction policy + max price
az vm create \
    --resource-group rg-batch \
    --name vm-spot-worker \
    --image Ubuntu2204 \
    --size Standard_D4s_v5 \
    --priority Spot \
    --eviction-policy Deallocate \
    --max-price 0.05 \
    --admin-username azureuser \
    --generate-ssh-keys
```

- **eviction-policy**: `Deallocate` (giữ disk, stop VM) hoặc `Delete` (xóa hẳn).
- **max-price**: $/h cap. `-1` = chấp nhận giá hiện tại Azure. Nếu giá Spot vượt → evict.
- Notice trước evict: **30 giây**. Workload phải graceful shutdown.

### Reserved Instance (RI)

- Mua qua portal: "Reservations" → chọn VM family + region + term + payment (upfront/monthly).
- Apply tự động cho VM matching size + region.
- **Exchange/cancel** linh hoạt (chính sách 2026).

### Azure Hybrid Benefit (AHB)

- Customer có **Windows Server license** với Software Assurance hoặc subscription → đem lên Azure VM Windows → không phải trả license Windows trong VM cost (giảm ~40%).
- Tương tự cho **SQL Server license** → giảm tới 55% trên SQL VM/SQL Database.

```bash
# Bật AHB cho VM Windows
az vm update --resource-group rg-prod --name vm-win-01 --license-type Windows_Server

# Bật AHB cho SQL VM
az sql vm update --resource-group rg-prod --name sqlvm-prod --sql-license-type AHUB
```

→ **Kết hợp**: RI 3 năm + AHB + Spot cho phần burst = giảm tới **80% total cost** so PAYG.

---

## 5️⃣ Cloud-init — Bootstrap VM (analog EC2 user data)

```bash
# cloud-init.yaml
#cloud-config
package_update: true
packages:
  - nginx
  - python3-pip

write_files:
  - path: /etc/nginx/sites-available/default
    content: |
      server {
        listen 80;
        location / { proxy_pass http://localhost:8000; }
      }

runcmd:
  - pip3 install fastapi uvicorn
  - systemctl enable nginx && systemctl start nginx
  - useradd -m apiuser
  - su - apiuser -c "uvicorn main:app --host 127.0.0.1 --port 8000 &"
```

```bash
az vm create \
    --resource-group rg-prod-web \
    --name vm-prod-web-01 \
    --image Ubuntu2204 \
    --size Standard_B2s \
    --admin-username azureuser \
    --generate-ssh-keys \
    --custom-data ./cloud-init.yaml
```

→ VM tự cài nginx + Python + FastAPI khi boot.

---

## 6️⃣ Just-in-Time (JIT) access

🪞 **Ẩn dụ**: *JIT như **thẻ key khách sạn** — bạn yêu cầu mở phòng 22 chỉ trong 3 giờ → security mở NSG cho IP của bạn 3 giờ rồi tự đóng lại. Không có thẻ = không vào.*

### Tại sao cần JIT

Port 22 (SSH) / 3389 (RDP) mở 24/7 = bị brute-force liên tục. JIT mở **chỉ khi cần** cho **IP của bạn**.

### Setup

```bash
# Cần Defender for Cloud Standard ($15/server/tháng)
# Hoặc dùng manual NSG + Logic App như free workaround.

# Bật JIT cho VM (qua portal hoặc API)
# Portal:
#   Defender for Cloud → Workload protections → Just-in-time VM access
#   → Add VM → Set rule: port 22, max 3h, source "Per request"
```

### Request access

```bash
# CLI request 1 giờ SSH từ IP nhà
MY_IP=$(curl -s ifconfig.me)
az security jit-policy initiate \
    --resource-group rg-prod-web \
    --name vm-prod-web-01 \
    --resource '[{"id":"/subscriptions/<sub>/resourceGroups/rg-prod-web/providers/Microsoft.Compute/virtualMachines/vm-prod-web-01","ports":[{"number":22,"allowedSourceAddressPrefix":"'$MY_IP'","duration":"PT1H"}]}]'

# NSG rule tạo tự động cho IP của bạn, 1 giờ, rồi tự xóa.
ssh azureuser@<vm-public-ip>
```

### Free workaround — Azure Bastion

```bash
# Bastion = managed jump host, không cần public IP trên VM
az network bastion create \
    --resource-group rg-prod-shared \
    --name bastion-prod \
    --public-ip-address pip-bastion \
    --vnet-name vnet-prod \
    --sku Basic
# SSH qua portal hoặc native client → no public IP, no port 22
```

→ **Best practice**: Bastion + Conditional Access. JIT bổ sung nếu vẫn cần direct.

---

## 7️⃣ Backup + Snapshot

### Snapshot (one-off)

```bash
# Snapshot OS disk
az snapshot create \
    --resource-group rg-prod-web \
    --name snap-vm-prod-web-01-os-20260524 \
    --source disk-vm-prod-web-01-os \
    --incremental true

# Restore: tạo disk từ snapshot rồi attach VM mới
az disk create \
    --resource-group rg-prod-web \
    --name disk-restored \
    --source snap-vm-prod-web-01-os-20260524
```

### Azure Backup (policy-based)

```bash
# Tạo Recovery Services Vault
az backup vault create \
    --resource-group rg-prod-backup \
    --name rsv-acmeshop-prod \
    --location southeastasia

# Tạo backup policy (daily 02:00, retain 30 days)
# (Portal nhanh hơn CLI vì policy syntax phức tạp)

# Enable backup cho VM
az backup protection enable-for-vm \
    --resource-group rg-prod-backup \
    --vault-name rsv-acmeshop-prod \
    --vm vm-prod-web-01 \
    --policy-name DailyPolicy
```

→ Daily snapshot all disks + VM config. Restore: VM mới hoặc disk replace.

---

## 🛠️ Hands-on — FastAPI trên VMSS auto-scale

### Mục tiêu

Deploy FastAPI app trên VMSS 2 instance baseline, scale-out tới 10 khi CPU > 70%, Spot VM cho instance burst, Load Balancer front, JIT cho SSH debug.

### Bước 1 — VNet + NSG + LB

```bash
# Resource Group
az group create --name rg-prod-web --location southeastasia

# VNet + Subnet
az network vnet create \
    --resource-group rg-prod-web \
    --name vnet-prod-web \
    --address-prefix 10.0.0.0/16 \
    --subnet-name snet-web \
    --subnet-prefix 10.0.1.0/24

# Public IP + LB
az network public-ip create \
    --resource-group rg-prod-web \
    --name pip-lb-web-prod \
    --sku Standard \
    --allocation-method Static \
    --zone 1 2 3

az network lb create \
    --resource-group rg-prod-web \
    --name lb-web-prod \
    --sku Standard \
    --public-ip-address pip-lb-web-prod \
    --frontend-ip-name fe-web \
    --backend-pool-name bp-web

# Health probe + rule port 80
az network lb probe create \
    --resource-group rg-prod-web \
    --lb-name lb-web-prod \
    --name probe-http \
    --protocol Http --port 80 --path /health

az network lb rule create \
    --resource-group rg-prod-web \
    --lb-name lb-web-prod \
    --name rule-http \
    --protocol Tcp --frontend-port 80 --backend-port 8000 \
    --frontend-ip-name fe-web --backend-pool-name bp-web \
    --probe-name probe-http
```

### Bước 2 — cloud-init cho FastAPI

```bash
cat > cloud-init.yaml <<'EOF'
#cloud-config
package_update: true
packages:
  - python3-pip
write_files:
  - path: /home/azureuser/app/main.py
    owner: azureuser:azureuser
    content: |
      from fastapi import FastAPI
      import socket
      app = FastAPI()
      @app.get("/")
      def root(): return {"host": socket.gethostname()}
      @app.get("/health")
      def health(): return {"status": "ok"}
  - path: /etc/systemd/system/fastapi.service
    content: |
      [Unit]
      Description=FastAPI
      After=network.target
      [Service]
      User=azureuser
      WorkingDirectory=/home/azureuser/app
      ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
      Restart=always
      [Install]
      WantedBy=multi-user.target
runcmd:
  - pip3 install fastapi uvicorn
  - systemctl daemon-reload
  - systemctl enable fastapi && systemctl start fastapi
EOF
```

### Bước 3 — Tạo VMSS Flexible

```bash
az vmss create \
    --resource-group rg-prod-web \
    --name vmss-web-prod \
    --orchestration-mode Flexible \
    --image Ubuntu2204 \
    --vm-sku Standard_D2s_v5 \
    --instance-count 2 \
    --admin-username azureuser \
    --generate-ssh-keys \
    --vnet-name vnet-prod-web \
    --subnet snet-web \
    --lb lb-web-prod \
    --backend-pool-name bp-web \
    --zones 1 2 3 \
    --custom-data cloud-init.yaml \
    --upgrade-policy-mode Automatic
```

### Bước 4 — Autoscale rule

```bash
# Scale up: CPU > 70% trong 5 phút → +2
az monitor autoscale create \
    --resource-group rg-prod-web \
    --resource vmss-web-prod \
    --resource-type Microsoft.Compute/virtualMachineScaleSets \
    --name autoscale-web-prod \
    --min-count 2 --max-count 10 --count 2

az monitor autoscale rule create \
    --resource-group rg-prod-web \
    --autoscale-name autoscale-web-prod \
    --condition "Percentage CPU > 70 avg 5m" \
    --scale out 2

az monitor autoscale rule create \
    --resource-group rg-prod-web \
    --autoscale-name autoscale-web-prod \
    --condition "Percentage CPU < 30 avg 10m" \
    --scale in 1
```

### Bước 5 — Spot VM extra (manual add)

```bash
# Thêm 5 Spot instance vào VMSS Flexible
az vmss scale --resource-group rg-prod-web --name vmss-web-prod --new-capacity 7

# Update profile để Spot tier cho instance mới (advanced — qua ARM template)
```

### Bước 6 — Test

```bash
# Lấy public IP của LB
LB_IP=$(az network public-ip show -g rg-prod-web -n pip-lb-web-prod --query ipAddress -o tsv)

# Curl nhiều lần → thấy hostname khác nhau (round-robin)
for i in {1..10}; do curl http://$LB_IP/; echo; done

# Load test
ab -n 10000 -c 100 http://$LB_IP/
# Xem VMSS scale lên khi CPU > 70%
az vmss list-instances -g rg-prod-web -n vmss-web-prod --output table
```

### Bước 7 — Cleanup

```bash
az group delete --name rg-prod-web --yes --no-wait
```

→ **Kết quả**: VMSS auto-scale theo CPU, LB phân phối traffic, cost optimize với mix Reserved + Spot.

---

## ⚠️ Pitfalls — Bẫy phổ biến

### 1. Chọn region không có AZ

**Bẫy**: Deploy `southeastasia` (Singapore) — có AZ ✅. Nhưng `southindia` chưa có AZ → không thể `--zone 1 2 3` → fallback Availability Set, SLA thấp.

**Fix**: Check region có AZ chưa: `az vm list-skus --location <region> --zone`. Vietnam-friendly + AZ: `southeastasia` ✅, `japaneast` ✅, `koreacentral` ✅.

### 2. Premium SSD chỉ support VM với suffix `s`

**Bẫy**: Attach Premium SSD vào `D4_v5` (không có `s`) → fail.

**Fix**: Luôn dùng VM có `s` (D4**s**_v5, B2**s**, E4**s**_v5) để support Premium Storage.

### 3. Spot VM evict không có warning đủ

**Bẫy**: Workload stateful trên Spot → evict giữa chừng → mất data.

**Fix**:
- Spot **chỉ cho stateless** workload (web, batch).
- Listen `eviction notice` event (30s) → graceful shutdown.
- Quan trọng → dùng PAYG hoặc RI.
- Mix: baseline RI + burst Spot.

### 4. Disk size = perf nhầm

**Bẫy**: Premium SSD P10 (128 GiB) → tưởng đủ. Nhưng chỉ 500 IOPS. DB cần 5000 IOPS → bottleneck.

**Fix**:
- Hiểu IOPS scale theo size disk (v1).
- DB cần P30+ (1 TiB → 5000 IOPS).
- Hoặc dùng Premium SSD v2 — decouple IOPS khỏi size.

### 5. Không bật disk caching cho OS

**Bẫy**: OS disk caching = None → boot chậm, app load chậm.

**Fix**: OS disk **luôn** ReadWrite caching (default). Data disk: ReadOnly cho read-heavy, None cho write-heavy log.

### 6. Public IP mặc định trên mọi VM

**Bẫy**: `az vm create` tạo Public IP mặc định → mọi VM expose Internet → attack surface lớn.

**Fix**:
- `--public-ip-address ""` để skip.
- SSH/RDP qua **Azure Bastion** (managed jump host).
- Outbound qua NAT Gateway / Azure Firewall.

### 7. Backup retention nhầm

**Bẫy**: Setup Backup retention 7 ngày → sau 1 năm phát hiện ransomware → đã quá 7 ngày, không restore được.

**Fix**:
- Production: GFS pattern (7 daily + 4 weekly + 12 monthly + 7 yearly).
- Test restore quarterly — backup mà không restore được = vô dụng.

### 8. Reserved Instance mua nhầm size

**Bẫy**: Mua RI cho `D4s_v5` 3 năm — sau 6 tháng workload đổi sang `E4s_v5` → RI không apply.

**Fix**:
- Bắt đầu RI 1 năm (linh hoạt hơn 3 năm).
- Hoặc dùng **Savings Plan** — $/h flexible cross family/region.
- Exchange RI miễn phí (chính sách 2026).

### 9. Update Domain Linux gặp reboot bất ngờ

**Bẫy**: Microsoft maintenance reboot VM khi update host → app chưa graceful shutdown → request fail.

**Fix**:
- VMSS / AZ → spread across UD/FD/zones, Microsoft update từng nhóm.
- Subscribe **Scheduled Events** API (metadata service) — VM nhận notice 15 phút trước reboot.
- App graceful shutdown: drain connection từ LB rồi terminate.

---

## 🎯 Self-check

- [ ] So sánh B vs D vs E vs F vs L family — pick cho web server, DB, batch CPU-heavy?
- [ ] Premium SSD v1 vs v2 — khi nào v2 tốt hơn?
- [ ] Vẽ sơ đồ Availability Zone vs Availability Set vs VMSS?
- [ ] Tính cost: 2 D4s_v5 PAYG vs 2 D4s_v5 RI 3 năm + AHB Windows. Giảm bao nhiêu %?
- [ ] Spot VM khi nào dùng đúng? 3 trường hợp KHÔNG nên dùng?
- [ ] Cloud-init cài nginx + start systemd service?
- [ ] JIT access vs Azure Bastion — khác nhau ra sao?
- [ ] Snapshot vs Azure Backup — khi nào dùng cái nào?
- [ ] VMSS Flexible vs Uniform orchestration — chọn cái nào 2026?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **VM** | Virtual Machine — máy ảo |
| **VMSS** | Virtual Machine Scale Set — group auto-scale VM identical |
| **VM family** | B/D/E/F/L/N — phân loại theo workload optimization |
| **vCPU** | Virtual CPU — luồng CPU ảo |
| **Managed Disk** | Block storage do Azure quản lý lifecycle (vs unmanaged trên Storage Account) |
| **Standard HDD/SSD** | Disk type rẻ, IOPS thấp |
| **Premium SSD** | Disk type production, IOPS cao |
| **Ultra Disk** | Disk top-tier, IOPS up to 400k |
| **AZ** | Availability Zone — datacenter tách biệt trong region |
| **Availability Set** | Group VM cùng datacenter, tách FD/UD |
| **Fault Domain (FD)** | Tách rack/power |
| **Update Domain (UD)** | Tách batch maintenance |
| **Spot VM** | VM giá rẻ 90%, có thể bị evict |
| **Reserved Instance (RI)** | Cam kết 1-3 năm, giảm 30-72% |
| **Savings Plan** | $/h commitment flexible cross family |
| **Azure Hybrid Benefit (AHB)** | Dùng Windows/SQL license sẵn → giảm 40-55% |
| **Cloud-init** | Script bootstrap VM khi boot lần đầu |
| **JIT access** | Just-in-Time mở port chỉ khi cần |
| **Azure Bastion** | Managed jump host SSH/RDP qua browser |
| **NSG** | Network Security Group — firewall L4 |
| **Recovery Services Vault** | Container của Azure Backup |
| **Scheduled Events** | API metadata báo trước maintenance |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_what-is-azure-overview](00_what-is-azure-overview.md)
- → Tiếp: [02_blob-storage-and-rbac](02_blob-storage-and-rbac.md)
- ↑ Cluster Azure: [Azure README](../../README.md)

### Cross-reference
- ☁️ [AWS EC2 + EBS](../../../aws/lessons/01_basic/01_ec2-and-ebs-compute.md) — analog
- ☁️ [GCP Compute Engine + Disks](../../../gcp/lessons/01_basic/01_compute-engine-and-disks.md) — analog
- 🌐 [Cloud networking basics](../../../cloud-fundamentals/lessons/01_basic/02_cloud-networking.md)
- 🏗️ [IaC Terraform Azure provider](../../../../10_devops/iac/)

### Tài nguyên ngoài (2026)
- 📖 [Azure VM sizes](https://learn.microsoft.com/azure/virtual-machines/sizes)
- 📖 [Azure Managed Disks](https://learn.microsoft.com/azure/virtual-machines/managed-disks-overview)
- 📖 [VMSS Flexible orchestration](https://learn.microsoft.com/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-orchestration-modes)
- 📖 [Spot VM pricing](https://azure.microsoft.com/pricing/spot-advisor/)
- 📖 [Azure Hybrid Benefit](https://azure.microsoft.com/pricing/hybrid-benefit/)
- 📖 [Azure Bastion](https://learn.microsoft.com/azure/bastion/)
- 📖 [Azure Backup VM](https://learn.microsoft.com/azure/backup/backup-azure-vms-introduction)
- 📖 [cloud-init on Azure](https://learn.microsoft.com/azure/virtual-machines/linux/using-cloud-init)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 01 cluster Azure basic. VM size families (B/D/E/F/L/N) + Managed Disks (Standard/Premium/Ultra) + AZ/Availability Set/VMSS + Spot/RI/Hybrid Benefit pricing + cloud-init + JIT/Bastion + Snapshot/Backup + hands-on VMSS FastAPI auto-scale + 9 pitfalls. Mirror AWS EC2+EBS lesson.
