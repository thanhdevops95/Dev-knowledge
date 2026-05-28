# 🖥️ GCP Compute Engine + Persistent Disks

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [00_what-is-gcp-overview](00_what-is-gcp-overview.md) ✅, biết SSH cơ bản

> 🎯 *Bài 01. Compute Engine (GCE) = VM service của GCP — analog AWS EC2. Persistent Disk (PD) = block storage gắn VM. Bài này dạy: machine type, image, disk, metadata, startup script, MIG (Managed Instance Group), pricing CUD vs preemptible, live migration, IAP SSH. Hands-on deploy FastAPI lên 1 VM + autoscale với MIG.*

## 🎯 Sau bài này bạn sẽ

- [ ] Chọn đúng **machine type family** (E2/N2/N2D/C3/T2D) cho workload
- [ ] Phân biệt **Persistent Disk** (PD) **Standard / Balanced / SSD / Extreme**
- [ ] Dùng **custom image** + **startup script** để deploy automation
- [ ] Setup **Managed Instance Group (MIG)** với autoscale + health check
- [ ] Hiểu **Live Migration** (đặc trưng GCP) — VM không downtime khi maintenance
- [ ] Áp dụng **CUD (Committed Use Discount)** + **Spot VM** để tối ưu chi phí
- [ ] SSH an toàn qua **IAP tunnel** (không cần public IP)
- [ ] Deploy 1 FastAPI app lên VM với HTTPS

---

## Tình huống — Deploy FastAPI app lên GCP

Sếp giao:

> *"Mình cần deploy FastAPI backend lên GCP. Yêu cầu: 2-10 instance auto-scale theo CPU, HTTPS qua domain `api.acmeshop.vn`, healthcheck, không có public IP trên VM (ssh qua IAP), cost optimization 30% (CUD hoặc Spot). Bạn làm tuần này."*

Bạn cần:
- Chọn **machine type** (compute-optimize vs general-purpose).
- Chọn **disk** (Standard/Balanced/SSD).
- Tạo **MIG** (Managed Instance Group) auto-scale.
- Setup **Load Balancer** front + Cloud Armor.
- IAP cho SSH không public IP.
- Tag + label cho cost tracking.

→ Bài này lấp đầy từng phần.

---

## 1️⃣ Compute Engine — Machine types

🪞 **Ẩn dụ**: *Machine type như **chọn xe đi đường** — E2 là **xe máy** (rẻ, gọn, đa năng); N2 là **sedan** (cân bằng); C3 là **xe đua** (CPU mạnh nhất); T2D là **xe tải** (cost/performance ratio tốt cho throughput); N2D là **sedan diesel** (AMD EPYC, rẻ hơn 7-10%).*

### Family overview (2026)

| Family | CPU | Use case | Pricing |
|---|---|---|---|
| **E2** | Intel/AMD, shared core | Web server, dev, low-cost | Cheapest |
| **N2** | Intel Cascade/Ice Lake | General purpose, web tier | Mid |
| **N2D** | AMD EPYC 2nd gen | Same N2 nhưng rẻ hơn 7-10% | Mid-low |
| **N4** | Intel 5th gen (2024 GA) | New gen general purpose | Mid |
| **C3** | Intel Sapphire Rapids | CPU-bound (web tier high RPS) | High |
| **C3D** | AMD EPYC Genoa | Same C3 AMD version | High-mid |
| **C4** | Intel 5th gen Emerald | Latest compute-optimize | High |
| **T2D / T2A** | AMD EPYC / Ampere Arm | Scale-out workload, batch | Mid-low |
| **M3** | Intel Cascade Lake | Memory-optimize (SAP HANA, in-memory DB) | High |
| **A3 / G2** | Nvidia GPU H100 / L4 | AI training/inference | Premium |

### Sizes

```
e2-micro    = 2 vCPU shared, 1 GB RAM     (free tier eligible)
e2-small    = 2 vCPU shared, 2 GB RAM
e2-medium   = 2 vCPU shared, 4 GB RAM
n2-standard-2 = 2 vCPU, 8 GB RAM
n2-standard-4 = 4 vCPU, 16 GB RAM
c3-standard-4 = 4 vCPU, 16 GB RAM (Intel SPR)
```

→ Pattern: `<family>-<purpose>-<vCPU>` ; `purpose` = `standard|highmem|highcpu|custom`.

### Custom machine type (chỉ N1/N2/N2D/E2)

```bash
# 6 vCPU, 12 GB RAM (không có chuẩn) — custom
gcloud compute instances create custom-vm \
    --custom-cpu=6 \
    --custom-memory=12GB \
    --custom-vm-type=n2 \
    --zone=asia-southeast1-a
```

### Khi nào chọn family nào

| Workload | Recommend |
|---|---|
| Web tier (Nginx + FastAPI) | E2 dev, N2 prod, C3 high-RPS |
| Batch processing | T2D (cheap, scale-out) |
| Database self-host | N2 + Local SSD (caveat: data loss khi reboot) |
| ML training | A3 (H100) hoặc G2 (L4) |
| ARM workload | T2A (cost giảm 20-30%) |

---

## 2️⃣ Persistent Disk (PD)

PD = block storage gắn vào VM. **Không** xóa khi VM stop/delete (trừ khi `auto-delete=true`).

### Disk types 2026

| Type | IOPS | Throughput | Khi dùng | Cost/GB-month |
|---|---|---|---|---|
| **pd-standard** (HDD) | ~75 read/15 write per GB | 12 MB/s | Cold storage, log archive | $0.040 |
| **pd-balanced** | 3000 base + 6/GB | 140 MB/s | **Default cho VM 2026** | $0.100 |
| **pd-ssd** | 30000 base | 1200 MB/s | Database, high IOPS | $0.170 |
| **pd-extreme** | Up to 120k IOPS | 4000 MB/s | OLTP DB, in-memory cache | $0.125 + provisioned IOPS |
| **Local SSD** | 680k IOPS | 9000 MB/s | Temp / cache (data mất khi stop) | $0.080 |
| **Hyperdisk Balanced/Extreme/Throughput** | Tunable | Up to 4800 MB/s | New 2024+ — replace PD lâu dài | $0.125 |

→ **2026 default**: `pd-balanced`. Database production: `pd-ssd` hoặc `hyperdisk-extreme`.

### Tạo + attach disk

```bash
# Tạo VM với boot disk balanced 50 GB
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --boot-disk-type=pd-balanced \
    --boot-disk-size=50GB \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --zone=asia-southeast1-a

# Tạo data disk SSD 100 GB
gcloud compute disks create web-1-data \
    --type=pd-ssd \
    --size=100GB \
    --zone=asia-southeast1-a

# Attach disk
gcloud compute instances attach-disk web-1 \
    --disk=web-1-data \
    --zone=asia-southeast1-a

# Format + mount (trong VM)
sudo mkfs.ext4 -F /dev/sdb
sudo mkdir -p /mnt/data
sudo mount /dev/sdb /mnt/data
echo "/dev/sdb /mnt/data ext4 defaults 0 2" | sudo tee -a /etc/fstab
```

### Snapshot & resize

```bash
# Snapshot
gcloud compute disks snapshot web-1-data --zone=asia-southeast1-a

# Resize (online, không cần detach)
gcloud compute disks resize web-1-data --size=200GB --zone=asia-southeast1-a
# Trong VM:
sudo resize2fs /dev/sdb
```

---

## 3️⃣ Image + Startup script + Metadata

### Public image

```bash
# List images
gcloud compute images list --filter="family:debian-12"
gcloud compute images list --filter="family:ubuntu-2404-lts"

# Image family = symbolic name, auto-update tới latest version
# debian-12, ubuntu-2404-lts, cos-stable, ...
```

### Custom image (immutable infra)

```bash
# Setup 1 VM rồi snapshot làm image
gcloud compute images create acmeshop-fastapi-v1.0.0 \
    --source-disk=web-1 \
    --source-disk-zone=asia-southeast1-a \
    --family=acmeshop-fastapi
```

### Startup script

Chạy khi VM boot lần đầu (hoặc mỗi lần restart):

```bash
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --metadata-from-file=startup-script=./startup.sh \
    --tags=http-server \
    --zone=asia-southeast1-a
```

`startup.sh`:
```bash
#!/bin/bash
apt update && apt install -y python3-pip git
pip3 install fastapi uvicorn
git clone https://github.com/acmeshop/api.git /opt/app
cd /opt/app
uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Metadata service

VM có internal endpoint `metadata.google.internal` (`169.254.169.254`):

```bash
# Trong VM
curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/name
# → web-1

curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
# → access token cho service account
```

→ Dùng metadata để get config + SA token mà không cần lưu credential file.

---

## 4️⃣ Managed Instance Group (MIG) — Autoscale

**MIG** = Group of identical VM được manage bởi GCP. Cung cấp:
- **Autoscale** theo CPU/RPS/custom metric.
- **Auto-healing** (recreate VM nếu unhealthy).
- **Rolling update** (zero-downtime deploy).
- **Multi-zone** (high availability).

### Bước 1 — Instance Template

```bash
gcloud compute instance-templates create web-template-v1 \
    --machine-type=n2-standard-2 \
    --image-family=acmeshop-fastapi \
    --image-project=acmeshop-prod \
    --metadata-from-file=startup-script=./startup.sh \
    --tags=http-server \
    --network=default \
    --subnet=default
```

### Bước 2 — MIG với autoscale

```bash
# Tạo MIG
gcloud compute instance-groups managed create web-mig \
    --template=web-template-v1 \
    --size=2 \
    --zones=asia-southeast1-a,asia-southeast1-b,asia-southeast1-c \
    --health-check=web-hc \
    --initial-delay=300

# Autoscale CPU 60%, min=2, max=10
gcloud compute instance-groups managed set-autoscaling web-mig \
    --region=asia-southeast1 \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6 \
    --cool-down-period=120
```

### Bước 3 — Health check

```bash
gcloud compute health-checks create http web-hc \
    --port=8000 \
    --request-path=/healthz \
    --check-interval=30s \
    --timeout=5s \
    --healthy-threshold=2 \
    --unhealthy-threshold=3
```

### Bước 4 — Load Balancer (HTTPS)

```bash
# Backend service
gcloud compute backend-services create web-backend \
    --protocol=HTTP \
    --port-name=http \
    --health-checks=web-hc \
    --global

# Add MIG vào backend
gcloud compute backend-services add-backend web-backend \
    --instance-group=web-mig \
    --instance-group-region=asia-southeast1 \
    --global

# URL map + HTTPS proxy + forwarding rule
gcloud compute url-maps create web-urlmap --default-service=web-backend
gcloud compute target-https-proxies create web-https-proxy \
    --url-map=web-urlmap \
    --ssl-certificates=acmeshop-cert
gcloud compute forwarding-rules create web-https-fr \
    --target-https-proxy=web-https-proxy \
    --global \
    --ports=443
```

→ Sau khi DNS trỏ → traffic vào LB → MIG.

### Rolling update

```bash
gcloud compute instance-groups managed rolling-action start-update web-mig \
    --region=asia-southeast1 \
    --version=template=web-template-v2 \
    --max-surge=1 \
    --max-unavailable=0
```

---

## 5️⃣ Live Migration — Đặc trưng GCP

🪞 **Ẩn dụ**: *Live Migration như **xe taxi chuyển khách sang xe khác đang chạy** — không cần dừng. AWS EC2 không có (instance phải stop khi underlying host maintenance).*

### Cách hoạt động

- GCP detect host maintenance (kernel patch, hardware swap).
- 60 giây trước, VM được **migrate** sang host khác **không downtime**.
- Memory + disk + network state preserve.

### Khi không hỗ trợ

- VM có **Local SSD** (data ephemeral).
- VM **preemptible/Spot** (giá rẻ, bị reclaim 24h).
- GPU instances.
- Nested virtualization.

### Cấu hình

```bash
# Cho phép live migration (default)
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --maintenance-policy=MIGRATE  # default

# Tắt (cho memory-heavy app không chịu pause 100ms)
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --maintenance-policy=TERMINATE  # VM stop khi maintenance
```

---

## 6️⃣ Pricing optimization

### Pricing models

| Model | Discount | Khi dùng |
|---|---|---|
| **On-demand** | 0% | Default |
| **Sustained Use Discount (SUD)** | Auto −20% (>25% month) | Auto, không cần làm gì |
| **CUD 1-year** | −20-25% | Cam kết 1 năm, predictable workload |
| **CUD 3-year** | Up to −57% | Cam kết 3 năm |
| **Flexible CUD** | −28% | Cam kết spend, không bind machine type |
| **Spot VM (preemptible)** | −60-91% | Workload chịu được interrupt 24h |
| **Reservation** | 0% (chỉ guarantee capacity) | High-traffic event |

### Spot VM ví dụ

```bash
gcloud compute instances create batch-worker \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=DELETE \
    --max-run-duration=24h
```

→ 60-91% rẻ. Có thể bị reclaim bất cứ lúc nào (warning 30s). Phù hợp batch, CI runner, ML training checkpoint.

### Best practice cost 2026

1. **Sandbox**: E2 + Spot + auto-shutdown CronJob.
2. **Production stable**: CUD 1-3 năm cho baseline + on-demand cho peak.
3. **Variable**: MIG autoscale + Spot mix.
4. **Tag mọi resource**: `env`, `team`, `cost-center` → Billing breakdown.

---

## 7️⃣ IAP SSH — SSH không cần public IP

🪞 **Ẩn dụ**: *IAP như **cổng vào tòa nhà có bảo vệ check thẻ nhân viên** — bạn vào qua IAP tunnel (thẻ là Google identity), không cần để cửa sau (public IP) mở cho Internet.*

### Cách hoạt động

- VM **không** có public IP.
- IAP proxy verify Google identity + IAM permission `roles/iap.tunnelResourceAccessor`.
- Tunnel TCP qua HTTPS đến VM internal IP.

### Setup

```bash
# 1. VM không có external IP
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --no-address \
    --zone=asia-southeast1-a

# 2. Firewall allow IAP range (35.235.240.0/20)
gcloud compute firewall-rules create allow-iap-ssh \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:22 \
    --source-ranges=35.235.240.0/20

# 3. Grant IAM
gcloud projects add-iam-policy-binding acmeshop-prod \
    --member="user:thien.le@acmeshop.vn" \
    --role="roles/iap.tunnelResourceAccessor"

# 4. SSH qua IAP
gcloud compute ssh web-1 --tunnel-through-iap --zone=asia-southeast1-a
```

→ Lợi: không public IP = attack surface giảm; audit log đầy đủ (ai SSH, khi nào).

---

## 🛠️ Hands-on — Deploy FastAPI lên MIG với LB + IAP SSH

### Mục tiêu

Production-grade: 2-10 instance autoscale, LB HTTPS, không public IP, IAP SSH, cost-optimize Spot.

### Bước 1 — Custom image

```bash
# VM tạm để cài đặt
gcloud compute instances create builder \
    --machine-type=n2-standard-2 \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --zone=asia-southeast1-a

# SSH vào, cài đặt
gcloud compute ssh builder --zone=asia-southeast1-a
sudo apt update && sudo apt install -y python3-pip nginx
pip3 install fastapi uvicorn gunicorn
# (copy code FastAPI vào /opt/app)
sudo systemctl enable fastapi  # systemd unit
exit

# Tạo image
gcloud compute images create acmeshop-fastapi-v1 \
    --source-disk=builder \
    --source-disk-zone=asia-southeast1-a \
    --family=acmeshop-fastapi

# Delete builder
gcloud compute instances delete builder --zone=asia-southeast1-a --quiet
```

### Bước 2 — Template + MIG + Health Check + LB

(Xem code section 4.)

### Bước 3 — IAP SSH

```bash
gcloud compute ssh web-mig-instance-abc \
    --tunnel-through-iap \
    --zone=asia-southeast1-a
```

### Bước 4 — Verify

```bash
# Curl LB
curl https://api.acmeshop.vn/healthz
# → 200 OK

# Generate load → autoscale
ab -n 100000 -c 100 https://api.acmeshop.vn/healthz
# Theo dõi: gcloud compute instance-groups managed describe web-mig --region=asia-southeast1
```

---

## ⚠️ Pitfalls

### 1. Boot disk delete khi VM delete

**Bẫy**: Default `--boot-disk-auto-delete=true` → delete VM = mất disk.

**Fix**: Production VM set `--no-boot-disk-auto-delete` + snapshot trước khi delete.

### 2. Local SSD data loss khi reboot

**Bẫy**: Local SSD nhanh nhưng **data mất khi stop/restart**.

**Fix**: Local SSD chỉ cho cache/temp; database luôn PD.

### 3. MIG initial-delay quá ngắn

**Bẫy**: Initial delay 60s → VM chưa start FastAPI xong → health check fail → MIG delete VM → loop.

**Fix**: Initial delay = startup time + 60s buffer (thường 300s cho heavy app).

### 4. Quên grant `iap.tunnelResourceAccessor` cho IAP SSH

**Bẫy**: `gcloud ssh --tunnel-through-iap` → permission denied.

**Fix**: Grant role trên project hoặc instance.

### 5. Spot VM cho stateful app

**Bẫy**: Postgres trên Spot → reclaim → mất data.

**Fix**: Spot chỉ stateless + có checkpoint.

### 6. Region/Zone latency

**Bẫy**: VM `us-central1`, user VN → latency 200ms.

**Fix**: Asia user → `asia-southeast1` (Singapore) hoặc `asia-east1` (Taiwan).

### 7. Không tag → cost không biết của ai

**Fix**: Mọi VM phải có label `env`, `team`, `service`. Billing breakdown qua label.

### 8. Public IP mặc định

**Bẫy**: Default VM có external IP → trả $2.92/tháng/IP + attack surface.

**Fix**: `--no-address` + IAP SSH; LB chỉ ở front.

---

## 🎯 Self-check

- [ ] Chọn machine family cho 3 workload: web tier, batch, ML training?
- [ ] Khi nào `pd-ssd` vs `pd-balanced`?
- [ ] Tạo MIG với autoscale CPU 60%, min=2 max=10?
- [ ] Setup IAP SSH cho VM không public IP?
- [ ] Tính CUD vs Spot savings cho web tier 24/7?
- [ ] Custom image vs startup script — khi dùng cái nào?
- [ ] Live Migration không hỗ trợ workload nào?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **GCE** | Google Compute Engine — VM service |
| **PD** | Persistent Disk — block storage |
| **MIG** | Managed Instance Group — VM autoscale group |
| **Instance Template** | Spec để MIG tạo VM (machine type, image, ...) |
| **IAP** | Identity-Aware Proxy — SSH/HTTPS qua Google identity |
| **CUD** | Committed Use Discount |
| **SUD** | Sustained Use Discount (auto) |
| **Spot VM** | Preemptible — rẻ 60-91%, có thể bị reclaim |
| **Live Migration** | Hot-migrate VM không downtime |
| **Metadata service** | Internal endpoint cho VM lấy config + token |
| **Startup script** | Bash chạy khi VM boot |
| **Custom image** | Image build từ disk snapshot |
| **Image family** | Symbolic name auto-track latest image |
| **Local SSD** | NVMe ephemeral (mất data khi stop) |
| **Hyperdisk** | Disk gen mới 2024+, tunable IOPS/throughput |
| **Rolling update** | Deploy zero-downtime cho MIG |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_what-is-gcp-overview](00_what-is-gcp-overview.md)
- → Tiếp: [02_cloud-storage-and-iam](02_cloud-storage-and-iam.md) *(sắp viết)*
- ↑ Cluster GCP: [GCP README](../../README.md)

### Cross-reference
- ☁️ [AWS EC2](../../../aws/lessons/01_basic/01_ec2-and-ebs-compute.md) — analog
- ☸️ [Kubernetes basic](../../../../10_devops/kubernetes/) — GKE context
- 🏗️ [Terraform GCP provider](../../../../10_devops/iac/) — Terraform manage

### Tài nguyên ngoài (2026)
- 📖 [Compute Engine docs](https://cloud.google.com/compute/docs)
- 📖 [Machine families](https://cloud.google.com/compute/docs/machine-resource)
- 📖 [Persistent Disk types](https://cloud.google.com/compute/docs/disks)
- 📖 [Hyperdisk](https://cloud.google.com/compute/docs/disks/hyperdisks)
- 📖 [MIG autoscaling](https://cloud.google.com/compute/docs/autoscaler)
- 📖 [IAP TCP forwarding](https://cloud.google.com/iap/docs/using-tcp-forwarding)
- 📖 [CUD calculator](https://cloud.google.com/products/calculator)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 01 GCP basic. Machine type 10 family + PD 6 type + custom image + startup script + MIG + autoscale + Live Migration + CUD/SUD/Spot pricing + IAP SSH + hands-on FastAPI MIG + 8 pitfalls. Pattern theo AWS lesson 01 EC2.
