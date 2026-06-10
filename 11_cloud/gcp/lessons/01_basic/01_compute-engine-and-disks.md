# 🖥️ GCP Compute Engine + Persistent Disks

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Đã đọc [GCP — Tổng quan + account setup + gcloud CLI](00_what-is-gcp-overview.md), biết SSH cơ bản.

> [!NOTE]
> **Mục tiêu bài học:**\
> Khi đã hiểu bức tranh tổng quan của GCP, câu hỏi tiếp theo luôn là: *"Vậy chạy app của mình ở đâu?"*. Câu trả lời quen thuộc nhất là **Compute Engine (GCE)** — dịch vụ máy ảo (*Virtual Machine — VM*) của GCP, tương đương AWS EC2 — đi kèm **Persistent Disk (PD)** là ổ đĩa lưu trữ gắn vào VM. Bài này dẫn bạn đi từ việc chọn cấu hình máy, chọn ổ đĩa, dựng image tự động, cho đến cụm máy tự co giãn (*MIG*), tối ưu chi phí và truy cập an toàn không cần *public IP*. Kết bài là một bài hands-on deploy FastAPI lên cụm tự scale hoàn chỉnh.

## 🎯 Sau bài này bạn sẽ

- [ ] Chọn đúng **machine type family** (E2/N2/N2D/C3/T2D) cho từng loại workload.
- [ ] Phân biệt **Persistent Disk** (PD) **Standard / Balanced / SSD / Extreme**.
- [ ] Dùng **custom image** + **startup script** để deploy tự động.
- [ ] Dựng **Managed Instance Group (MIG)** với autoscale + health check.
- [ ] Hiểu **Live Migration** — đặc trưng GCP giúp VM không downtime khi máy chủ bảo trì.
- [ ] Áp dụng **CUD (Committed Use Discount)** + **Spot VM** để tối ưu chi phí.
- [ ] SSH an toàn qua **IAP tunnel** mà không cần public IP trên VM.
- [ ] Deploy một FastAPI app lên VM với HTTPS.

---

## 💡 Sếp giao deploy FastAPI lên GCP và yêu cầu khá "khó nhằn"

Bạn vừa hoàn thành backend FastAPI cho dự án và đã sẵn sàng đưa lên môi trường thật. Sáng thứ Hai, sếp ghé bàn và đặt ra một loạt yêu cầu nghe qua thì rất "đời":

> *"Mình cần deploy FastAPI backend lên GCP. Yêu cầu: 2-10 instance tự co giãn theo CPU, HTTPS qua domain `api.acmeshop.vn`, có healthcheck, VM không được có public IP (ssh qua IAP), và phải tối ưu chi phí khoảng 30% (CUD hoặc Spot). Bạn làm trong tuần này nhé."*

Nghe thì gọn một câu, nhưng mỗi cụm từ trong đó lại là một mảnh ghép kỹ thuật riêng biệt mà bạn phải tự lắp:

- Chọn **machine type** — máy thiên về CPU (*compute-optimized*) hay đa năng (*general-purpose*)?
- Chọn **disk** — Standard, Balanced hay SSD?
- Dựng **MIG (Managed Instance Group)** để cụm máy tự co giãn.
- Đặt **Load Balancer** ở phía trước, kèm Cloud Armor chắn tấn công.
- Cấu hình **IAP** để SSH vào máy không có public IP.
- Gắn **tag + label** cho mọi resource để theo dõi chi phí.

Đây cũng chính là khung của cả bài: mỗi phần dưới đây sẽ lấp đầy đúng một mảnh ghép, và đến phần hands-on tất cả ráp lại thành một hệ thống chạy thật.

---

## 1️⃣ Compute Engine — Machine types

Trước khi tạo VM, câu hỏi đầu tiên luôn là: *"Máy này cần loại CPU nào, mạnh tới đâu?"*. GCP không bắt bạn tự chọn từng con chip — họ đóng gói sẵn thành các **machine family**, mỗi family tối ưu cho một nhóm workload khác nhau. Chọn sai family thì hoặc trả tiền thừa, hoặc máy không đủ sức tải.

🪞 **Ẩn dụ**: *Machine type giống như **chọn xe đi đường** — E2 là **xe máy** (rẻ, gọn, đa năng); N2 là **sedan** (cân bằng); C3 là **xe đua** (CPU mạnh nhất); T2D là **xe tải** (tỉ lệ cost/performance tốt cho throughput cao); N2D là **sedan diesel** (chip AMD EPYC, rẻ hơn N2 khoảng 7-10%).*

### Tổng quan các family (Family overview, 2026)

Dưới đây là các family đáng nhớ tính đến 2026. Cột "Use case" cho biết nên dùng khi nào, cột "Pricing" để bạn ước lượng chi phí tương đối:

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

Quy tắc thực dụng: phần lớn web service bắt đầu ở **E2** (lúc dev) rồi lên **N2** khi production. Chỉ khi đo đạc thấy CPU là nút thắt thật sự mới nhảy lên C3.

### Sizes (kích cỡ)

Mỗi family có sẵn các kích cỡ định nghĩa theo số vCPU và RAM. Vài size phổ biến hay gặp nhất:

```text
e2-micro    = 2 vCPU shared, 1 GB RAM     (free tier eligible)
e2-small    = 2 vCPU shared, 2 GB RAM
e2-medium   = 2 vCPU shared, 4 GB RAM
n2-standard-2 = 2 vCPU, 8 GB RAM
n2-standard-4 = 4 vCPU, 16 GB RAM
c3-standard-4 = 4 vCPU, 16 GB RAM (Intel SPR)
```

Tên gọi theo pattern `<family>-<purpose>-<vCPU>`, trong đó `purpose` là một trong `standard | highmem | highcpu | custom`. Nhìn tên là đoán được cấu hình mà không cần tra bảng.

### Custom machine type

Khi không size chuẩn nào vừa khít (ví dụ cần đúng 6 vCPU + 12 GB RAM), bạn khai báo **custom machine type** ngay trong tên `--machine-type` theo dạng `<family>-custom-<vCPU>-<RAM tính bằng MB>`:

```bash
# 6 vCPU, 12 GB RAM (12288 MB) — custom machine type họ N2
gcloud compute instances create custom-vm \
    --machine-type=n2-custom-6-12288 \
    --zone=asia-southeast1-a
```

Custom machine type chỉ hỗ trợ một số family (N1/N2/N2D/E2). Cách này hữu ích khi muốn cắt RAM thừa để tiết kiệm thay vì nhảy hẳn lên size lớn hơn.

### Khi nào chọn family nào

Lý thuyết là vậy, nhưng lúc làm thật bạn cần một bảng "tra nhanh" gắn family với workload cụ thể. Đây là các cặp ghép hay dùng nhất:

| Workload | Recommend |
|---|---|
| Web tier (Nginx + FastAPI) | E2 dev, N2 prod, C3 high-RPS |
| Batch processing | T2D (cheap, scale-out) |
| Database self-host | N2 + Local SSD (lưu ý: mất data khi reboot) |
| ML training | A3 (H100) hoặc G2 (L4) |
| ARM workload | T2A (cost giảm 20-30%) |

Với yêu cầu của sếp (web tier FastAPI), lựa chọn hợp lý là **N2** cho production và **E2** cho lúc thử nghiệm — vừa đủ mạnh vừa không lãng phí.

---

## 2️⃣ Persistent Disk (PD)

Máy đã chọn xong, giờ tới chỗ chứa dữ liệu. **Persistent Disk (PD)** là block storage gắn vào VM, và điểm mấu chốt cần nhớ ngay: PD **không** bị xóa khi VM stop hay delete (trừ khi bạn đặt `auto-delete=true`). Đây là khác biệt sống còn so với ổ tạm — chọn nhầm loại đĩa có thể khiến cả database "bốc hơi" sau một lần reboot.

### Disk types 2026

GCP cung cấp nhiều loại đĩa với mức IOPS, throughput và giá khác nhau. Bảng dưới sắp từ rẻ-chậm đến đắt-nhanh; các con số IOPS/throughput là **mức tối đa, tunable** tùy dung lượng và cấu hình:

| Type | IOPS | Throughput | Khi dùng | Cost/GB-month |
|---|---|---|---|---|
| **pd-standard** (HDD) | ~75 read/15 write per GB | 12 MB/s | Cold storage, log archive | $0.040 |
| **pd-balanced** | 3000 base + 6/GB | 140 MB/s | **Default cho VM 2026** | $0.100 |
| **pd-ssd** | 30000 base | 1200 MB/s | Database, high IOPS | $0.170 |
| **pd-extreme** | Up to 120k IOPS | 4000 MB/s | OLTP DB, in-memory cache | $0.125 + provisioned IOPS |
| **Local SSD** | 680k IOPS | 9000 MB/s | Temp / cache (data mất khi stop) | $0.080 |
| **Hyperdisk Balanced/Extreme/Throughput** | Tunable (tối đa) | Up to 4800 MB/s | New 2024+ — thay thế PD lâu dài | $0.125 |

Mặc định khôn ngoan cho 2026 là `pd-balanced` — đủ nhanh cho hầu hết web service với chi phí dễ chịu. Database production thì nâng lên `pd-ssd` hoặc `hyperdisk-extreme` khi cần IOPS cao.

### Tạo + attach disk

Lý thuyết đã rõ, giờ tạo VM kèm boot disk và gắn thêm một data disk SSD. Chuỗi lệnh dưới đây tạo VM với đĩa boot `pd-balanced` 50 GB, sau đó tạo và attach một đĩa data `pd-ssd` 100 GB, rồi format + mount nó bên trong VM:

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

Dòng cuối ghi vào `/etc/fstab` để đĩa tự mount lại sau mỗi lần reboot — bỏ bước này thì sau restart đĩa vẫn còn nhưng không tự gắn vào hệ thống.

### Snapshot & resize

Hai thao tác vận hành thường xuyên nhất với PD là **snapshot** (sao lưu) và **resize** (mở rộng). Điểm hay của GCP là cả hai đều làm online, không cần dừng VM hay detach đĩa:

```bash
# Snapshot
gcloud compute disks snapshot web-1-data --zone=asia-southeast1-a

# Resize (online, không cần detach)
gcloud compute disks resize web-1-data --size=200GB --zone=asia-southeast1-a
# Trong VM:
sudo resize2fs /dev/sdb
```

Lưu ý: resize ở tầng GCP chỉ mở rộng "ổ vật lý ảo" — bạn vẫn phải chạy `resize2fs` (hoặc tương đương) bên trong VM để filesystem nhận ra phần dung lượng mới.

---

## 3️⃣ Image + Startup script + Metadata

Tạo từng VM bằng tay thì ổn cho một máy, nhưng khi cần nhân bản hàng chục máy giống nhau thì phải tự động hóa. GCP có ba công cụ ghép lại để làm việc này: **image** (đóng băng một đĩa thành khuôn), **startup script** (chạy lệnh lúc VM khởi động), và **metadata service** (kênh để VM tự lấy config và token). Hiểu ba thứ này là nền móng cho phần MIG ở section sau.

### Public image

VM phải khởi động từ một image hệ điều hành. GCP cung cấp sẵn nhiều **public image**, và mẹo quan trọng là dùng **image family** thay vì pin một version cứng:

```bash
# List images
gcloud compute images list --filter="family:debian-12"
gcloud compute images list --filter="family:ubuntu-2404-lts"

# Image family = symbolic name, auto-update tới latest version
# debian-12, ubuntu-2404-lts, cos-stable, ...
```

`image-family` là một tên tượng trưng luôn trỏ tới bản mới nhất trong dòng đó — nhờ vậy VM mới tạo luôn có bản vá bảo mật cập nhật mà không phải sửa script.

### Custom image (immutable infra)

Khi đã cài sẵn app + dependencies lên một VM, bạn có thể "đóng băng" đĩa của nó thành **custom image** để mọi máy sau đẻ ra từ khuôn này đều giống hệt. Đây là nền tảng của tư duy *immutable infrastructure* — không sửa máy đang chạy mà thay bằng máy mới từ image mới:

```bash
# Setup 1 VM rồi snapshot làm image
gcloud compute images create acmeshop-fastapi-v1.0.0 \
    --source-disk=web-1 \
    --source-disk-zone=asia-southeast1-a \
    --family=acmeshop-fastapi
```

### Startup script

Cách nhẹ nhàng hơn custom image là **startup script** — một đoạn bash chạy mỗi khi VM boot. Hợp cho việc cài đặt linh động hoặc kéo code mới nhất:

```bash
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 \
    --image-family=debian-12 \
    --image-project=debian-cloud \
    --metadata-from-file=startup-script=./startup.sh \
    --tags=http-server \
    --zone=asia-southeast1-a
```

Nội dung `startup.sh` cài Python, kéo code rồi chạy app:

```bash
#!/bin/bash
apt update && apt install -y python3-pip git
pip3 install fastapi uvicorn
git clone https://github.com/acmeshop/api.git /opt/app
cd /opt/app
uvicorn main:app --host 0.0.0.0 --port 8000 &
```

So sánh nhanh: **custom image** nhanh khi boot (mọi thứ đã cài sẵn) nhưng phải rebuild khi đổi dependency; **startup script** linh hoạt nhưng boot lâu hơn vì cài lại mỗi lần. Production thường kết hợp: image chứa phần nặng cố định, script chỉ lo phần config thay đổi.

### Metadata service

Mỗi VM trên GCP có một endpoint nội bộ `metadata.google.internal` (`169.254.169.254`) — nơi VM tự hỏi "mình là ai, config của mình là gì". Đặc biệt, VM có thể lấy *access token* của service account ngay từ đây mà không cần lưu file credential:

```bash
# Trong VM
curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/name
# → web-1

curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
# → access token cho service account
```

Đây chính là lý do trên GCP bạn hiếm khi phải đặt key file vào máy: VM lấy token động qua metadata, vừa an toàn vừa tự xoay vòng.

---

## 4️⃣ Managed Instance Group (MIG) — Autoscale

Yêu cầu "2-10 instance tự co giãn" của sếp chính là việc của **MIG (Managed Instance Group)** — một nhóm VM giống hệt nhau do GCP tự quản lý. Thay vì bạn tự bật/tắt từng máy, MIG lo bốn việc cốt lõi giúp bạn:

- **Autoscale** — tăng/giảm số máy theo CPU, RPS hoặc custom metric.
- **Auto-healing** — tự tạo lại VM nếu health check báo unhealthy.
- **Rolling update** — deploy version mới không downtime.
- **Multi-zone** — rải máy qua nhiều zone để chịu lỗi tốt hơn.

Bốn bước dưới đây dựng trọn pipeline từ khuôn máy đến Load Balancer.

### Bước 1 — Instance Template

MIG không nhận thẳng cấu hình VM mà cần một **Instance Template** — bản đặc tả "mỗi máy trong nhóm trông như thế nào" (machine type, image, script, tag...):

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

Có template rồi thì tạo MIG. Ở đây ta dựng **regional MIG** (rải qua 3 zone của `asia-southeast1`) để có high availability, vì vậy lệnh `create` dùng `--region` kèm `--zones` để chỉ định phân phối — và lệnh `set-autoscaling` sau đó cũng dùng `--region` cho khớp:

```bash
# Tạo regional MIG (rải qua 3 zone)
gcloud compute instance-groups managed create web-mig \
    --template=web-template-v1 \
    --size=2 \
    --region=asia-southeast1 \
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

Cặp `min=2, max=10` đáp ứng đúng yêu cầu "2-10 instance"; `target-cpu-utilization=0.6` nghĩa là MIG cố giữ CPU trung bình quanh 60% — vượt thì thêm máy, thấp thì bớt máy.

### Bước 3 — Health check

Autoscale và auto-healing đều dựa vào một **health check** để biết máy nào còn sống. Ta cấu hình nó gọi vào endpoint `/healthz` của FastAPI:

```bash
gcloud compute health-checks create http web-hc \
    --port=8000 \
    --request-path=/healthz \
    --check-interval=30s \
    --timeout=5s \
    --healthy-threshold=2 \
    --unhealthy-threshold=3
```

Đọc cấu hình này như sau: cứ 30 giây gọi một lần, 2 lần liên tiếp thành công thì coi là khỏe, 3 lần liên tiếp lỗi thì coi là chết (và MIG sẽ tạo lại máy đó).

### Bước 4 — Load Balancer (HTTPS)

Cuối cùng, đặt một **Load Balancer** ở phía trước để gom traffic HTTPS rồi phân về MIG. Cụm lệnh sau dựng backend service, gắn MIG vào, rồi nối URL map → HTTPS proxy → forwarding rule:

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

Sau khi DNS của `api.acmeshop.vn` trỏ về IP của forwarding rule, đường đi của một request là: client → LB (kết thúc TLS) → MIG → một VM khỏe mạnh bất kỳ.

### Rolling update

Khi cần deploy version mới, không cần dựng lại cụm. **Rolling update** thay từng VM dần dần theo template mới, giữ dịch vụ luôn online:

```bash
gcloud compute instance-groups managed rolling-action start-update web-mig \
    --region=asia-southeast1 \
    --version=template=web-template-v2 \
    --max-surge=1 \
    --max-unavailable=0
```

`max-unavailable=0` đảm bảo không có máy nào bị "rút" trước khi máy mới sẵn sàng — đây là chìa khóa cho zero-downtime deploy.

---

## 5️⃣ Live Migration — Đặc trưng GCP

Một câu hỏi tự nhiên: *"Khi Google bảo trì phần cứng máy chủ vật lý, VM của mình có phải dừng không?"*. Trên nhiều cloud khác thì có. Trên GCP thì không, nhờ một tính năng riêng gọi là **Live Migration**.

🪞 **Ẩn dụ**: *Live Migration như **xe taxi chuyển khách sang xe khác đang chạy** — không cần dừng lại. AWS EC2 không có cơ chế này (instance phải stop khi host vật lý bảo trì).*

### Cách hoạt động

Quá trình diễn ra trong suốt với app của bạn:

- GCP phát hiện host sắp bảo trì (vá kernel, thay phần cứng).
- Khoảng 60 giây trước, VM được **migrate** sang host khác **không downtime**.
- Toàn bộ state của memory, disk và network được giữ nguyên.

### Khi không hỗ trợ

Không phải VM nào cũng được Live Migration. Một số trường hợp GCP buộc phải dừng/khởi động lại thay vì migrate:

- VM có **Local SSD** (data vốn ephemeral).
- VM **preemptible/Spot** (giá rẻ, có thể bị reclaim trong 24h).
- GPU instances.
- Nested virtualization.

### Cấu hình

Hành vi này điều khiển qua `--maintenance-policy`. Mặc định đã là `MIGRATE`, nhưng bạn có thể tắt cho app nhạy cảm với khoảng pause cực ngắn khi migrate:

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

Với web tier thông thường, cứ để mặc định `MIGRATE` — bạn gần như không bao giờ nhận ra việc bảo trì đã diễn ra.

---

## 6️⃣ Tối ưu chi phí (Pricing optimization)

Yêu cầu "tối ưu chi phí 30%" của sếp không phải chuyện may rủi — GCP có sẵn nhiều mô hình giá, mỗi cái đánh đổi giữa mức giảm giá và độ cam kết. Hiểu đúng từng mô hình là cách rẻ nhất để cắt hóa đơn.

### Các mô hình giá (Pricing models)

Bảng dưới xếp từ "không cam kết gì" đến "cam kết nhiều, giảm sâu". Cột Discount cho biết mức tiết kiệm, cột "Khi dùng" cho biết tình huống phù hợp:

| Model | Discount | Khi dùng |
|---|---|---|
| **On-demand** | 0% | Default |
| **Sustained Use Discount (SUD)** | Auto −20% (>25% month) | Auto, không cần làm gì |
| **CUD 1-year** | −20-25% | Cam kết 1 năm, predictable workload |
| **CUD 3-year** | Up to −57% | Cam kết 3 năm |
| **Flexible CUD** | −28% | Cam kết spend, không bind machine type |
| **Spot VM (preemptible)** | −60-91% | Workload chịu được interrupt 24h |
| **Reservation** | 0% (chỉ guarantee capacity) | High-traffic event |

Điểm hay của GCP là **SUD tự động** — chạy một VM quá 25% tháng là đã được giảm ~20% mà không cần làm gì. Muốn giảm sâu hơn nữa thì cam kết qua CUD, hoặc dùng Spot cho phần workload chịu được gián đoạn.

### Spot VM ví dụ

**Spot VM** là quân bài tiết kiệm mạnh nhất — rẻ tới 60-91%, đổi lại có thể bị thu hồi bất cứ lúc nào với cảnh báo chỉ 30 giây:

```bash
gcloud compute instances create batch-worker \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=DELETE \
    --max-run-duration=24h
```

Vì có thể bị reclaim đột ngột, Spot chỉ hợp với workload **stateless hoặc có checkpoint**: batch job, CI runner, ML training lưu checkpoint định kỳ. Tuyệt đối không đặt database lên Spot.

### Best practice cost 2026

Gom lại thành công thức theo từng loại môi trường, bạn có thể áp dụng ngay:

1. **Sandbox**: E2 + Spot + auto-shutdown bằng CronJob.
2. **Production stable**: CUD 1-3 năm cho phần baseline + on-demand cho phần peak.
3. **Variable**: MIG autoscale + trộn thêm Spot cho phần co giãn.
4. **Tag mọi resource**: gắn `env`, `team`, `cost-center` để Billing tách được chi phí theo nhóm.

Với bài toán của sếp, kết hợp **CUD cho 2 máy baseline + Spot/on-demand cho phần autoscale** là cách đạt mục tiêu giảm 30% mà vẫn an toàn.

---

## 7️⃣ IAP SSH — SSH không cần public IP

Yêu cầu cuối của sếp là "VM không được có public IP nhưng vẫn SSH được". Nghe mâu thuẫn, nhưng đây chính là việc của **IAP (Identity-Aware Proxy)** — cho phép bạn chui vào VM qua một đường hầm xác thực bằng danh tính Google, không cần mở cửa ra Internet.

🪞 **Ẩn dụ**: *IAP như **cổng tòa nhà có bảo vệ check thẻ nhân viên** — bạn vào qua IAP tunnel (thẻ ở đây là Google identity), không cần để cửa sau (public IP) mở toang cho cả Internet.*

### Cách hoạt động

Cơ chế gồm ba lớp:

- VM **không** có public IP.
- IAP proxy xác minh Google identity + quyền IAM `roles/iap.tunnelResourceAccessor`.
- Tunnel TCP đi qua HTTPS để chạm tới internal IP của VM.

### Setup

Bốn bước dưới đây dựng trọn luồng: tạo VM không IP ngoài, mở firewall cho dải IAP, cấp quyền IAM, rồi SSH qua tunnel:

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

Lợi ích kép: không public IP nghĩa là *attack surface* giảm hẳn, đồng thời mọi phiên SSH đều đi qua IAP nên audit log ghi đầy đủ ai vào máy nào, lúc nào.

---

## 🛠️ Hands-on — Deploy FastAPI lên MIG với LB + IAP SSH

Đến đây mọi mảnh ghép đã sẵn sàng. Bài hands-on này ráp tất cả lại thành một hệ thống production-grade đúng yêu cầu của sếp: cụm 2-10 instance autoscale, Load Balancer HTTPS, không public IP, SSH qua IAP, và tối ưu chi phí bằng Spot. Mỗi bước dưới đây tự đủ — bạn chạy tuần tự từ trên xuống là ra hệ thống hoàn chỉnh.

### Mục tiêu

Dựng một backend FastAPI chạy thật: tự co giãn theo tải, có HTTPS, truy cập an toàn không lộ ra Internet, và chi phí được tối ưu.

### Bước 1 — Custom image

Đầu tiên dựng một VM "builder" để cài sẵn môi trường, tạo systemd unit cho FastAPI, rồi đóng băng đĩa thành custom image. Có image rồi thì xóa builder để khỏi tốn tiền:

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

# Tạo systemd unit để FastAPI tự chạy khi VM boot
sudo tee /etc/systemd/system/fastapi.service > /dev/null <<'EOF'
[Unit]
Description=FastAPI service
After=network.target

[Service]
WorkingDirectory=/opt/app
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fastapi   # đã có unit file ở trên nên lệnh này hợp lệ
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

Từ custom image vừa tạo, dựng template rồi lần lượt health check → MIG regional → backend service → LB HTTPS. Đây là toàn bộ lệnh inline để bạn không phải cuộn ngược lên section 4:

```bash
# Instance template từ custom image
gcloud compute instance-templates create web-template-v1 \
    --machine-type=n2-standard-2 \
    --image-family=acmeshop-fastapi \
    --image-project=acmeshop-prod \
    --tags=http-server \
    --network=default --subnet=default

# Health check vào /healthz
gcloud compute health-checks create http web-hc \
    --port=8000 --request-path=/healthz \
    --check-interval=30s --timeout=5s \
    --healthy-threshold=2 --unhealthy-threshold=3

# Regional MIG + autoscale 2..10 theo CPU 60%
gcloud compute instance-groups managed create web-mig \
    --template=web-template-v1 --size=2 \
    --region=asia-southeast1 \
    --zones=asia-southeast1-a,asia-southeast1-b,asia-southeast1-c \
    --health-check=web-hc --initial-delay=300
gcloud compute instance-groups managed set-autoscaling web-mig \
    --region=asia-southeast1 \
    --min-num-replicas=2 --max-num-replicas=10 \
    --target-cpu-utilization=0.6 --cool-down-period=120

# Backend service + gắn MIG + LB HTTPS
gcloud compute backend-services create web-backend \
    --protocol=HTTP --port-name=http \
    --health-checks=web-hc --global
gcloud compute backend-services add-backend web-backend \
    --instance-group=web-mig \
    --instance-group-region=asia-southeast1 --global
gcloud compute url-maps create web-urlmap --default-service=web-backend
gcloud compute target-https-proxies create web-https-proxy \
    --url-map=web-urlmap --ssl-certificates=acmeshop-cert
gcloud compute forwarding-rules create web-https-fr \
    --target-https-proxy=web-https-proxy --global --ports=443
```

### Bước 3 — IAP SSH

Để vào một máy bất kỳ trong MIG mà không cần public IP, dùng IAP tunnel (nhớ đã cấp `roles/iap.tunnelResourceAccessor` như section 7):

```bash
gcloud compute ssh web-mig-instance-abc \
    --tunnel-through-iap \
    --zone=asia-southeast1-a
```

### Bước 4 — Verify

Cuối cùng kiểm tra hệ thống có sống và có tự scale không. Gọi `/healthz` qua LB để xác nhận luồng HTTPS, rồi bắn tải để xem MIG nhân máy:

```bash
# Curl LB
curl https://api.acmeshop.vn/healthz
# → 200 OK

# Generate load → autoscale
ab -n 100000 -c 100 https://api.acmeshop.vn/healthz
# Theo dõi: gcloud compute instance-groups managed describe web-mig --region=asia-southeast1
```

Nếu cấu hình đúng, khi tải tăng bạn sẽ thấy số replica trong output của lệnh `describe` nhích dần lên (tới tối đa 10), rồi tự co lại sau khi tải giảm.

---

## 💡 Cạm bẫy thường gặp & Best practice

Dưới đây là những "vết xe đổ" hay gặp nhất khi mới làm Compute Engine — kèm cách phòng tránh. Đọc trước để khỏi mất buổi tối debug.

### 1. Boot disk delete khi VM delete

**Bẫy**: Mặc định `--boot-disk-auto-delete=true` → xóa VM là mất luôn boot disk.

**Fix**: Production VM đặt `--no-boot-disk-auto-delete` và snapshot trước khi xóa.

### 2. Local SSD data loss khi reboot

**Bẫy**: Local SSD rất nhanh nhưng **mất sạch data khi stop/restart**.

**Fix**: Local SSD chỉ dùng cho cache/temp; database luôn để trên PD.

### 3. MIG initial-delay quá ngắn

**Bẫy**: Initial delay 60s → VM chưa kịp start FastAPI → health check fail → MIG xóa VM → lặp vô tận.

**Fix**: Initial delay = thời gian startup + 60s buffer (thường 300s cho app nặng).

### 4. Quên grant `iap.tunnelResourceAccessor` cho IAP SSH

**Bẫy**: Chạy `gcloud ssh --tunnel-through-iap` → permission denied.

**Fix**: Grant role này ở cấp project hoặc cấp instance.

### 5. Spot VM cho stateful app

**Bẫy**: Đặt Postgres lên Spot → bị reclaim → mất data.

**Fix**: Spot chỉ cho workload stateless hoặc có checkpoint.

### 6. Region/Zone latency

**Bẫy**: VM ở `us-central1`, user ở VN → latency ~200ms.

**Fix**: User châu Á → chọn `asia-southeast1` (Singapore) hoặc `asia-east1` (Taiwan).

### 7. Không tag → không biết chi phí của ai

**Fix**: Mọi VM phải có label `env`, `team`, `service`; Billing tách chi phí theo label.

### 8. Public IP mặc định

**Bẫy**: VM mặc định có external IP → trả $2.92/tháng/IP + tăng attack surface.

**Fix**: Dùng `--no-address` + IAP SSH; chỉ để public ở tầng LB phía trước.

---

## 🧠 Tự kiểm tra (Self-check)

Nếu trả lời trôi chảy các câu dưới đây, bạn đã nắm chắc bài này:

- [ ] Chọn machine family cho 3 workload: web tier, batch, ML training?
- [ ] Khi nào dùng `pd-ssd` thay vì `pd-balanced`?
- [ ] Tạo MIG với autoscale CPU 60%, min=2 max=10 như thế nào?
- [ ] Setup IAP SSH cho VM không có public IP gồm những bước gì?
- [ ] So sánh tiết kiệm CUD vs Spot cho web tier chạy 24/7?
- [ ] Custom image vs startup script — khi nào dùng cái nào?
- [ ] Live Migration không hỗ trợ những workload nào?

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Các lệnh hay dùng nhất, gom lại để copy nhanh khi làm thật:

```bash
# Tạo VM cơ bản (balanced disk, IAP-ready)
gcloud compute instances create web-1 \
    --machine-type=n2-standard-2 --no-address \
    --boot-disk-type=pd-balanced --boot-disk-size=50GB \
    --image-family=debian-12 --image-project=debian-cloud \
    --zone=asia-southeast1-a

# Custom machine type (6 vCPU, 12 GB)
--machine-type=n2-custom-6-12288

# SSH qua IAP (không cần public IP)
gcloud compute ssh web-1 --tunnel-through-iap --zone=asia-southeast1-a

# Snapshot + resize disk (online)
gcloud compute disks snapshot web-1-data --zone=asia-southeast1-a
gcloud compute disks resize web-1-data --size=200GB --zone=asia-southeast1-a

# Autoscale MIG
gcloud compute instance-groups managed set-autoscaling web-mig \
    --region=asia-southeast1 --min-num-replicas=2 --max-num-replicas=10 \
    --target-cpu-utilization=0.6

# Rolling update zero-downtime
gcloud compute instance-groups managed rolling-action start-update web-mig \
    --region=asia-southeast1 --version=template=web-template-v2 \
    --max-surge=1 --max-unavailable=0

# Spot VM tiết kiệm 60-91%
gcloud compute instances create batch-worker \
    --provisioning-model=SPOT --instance-termination-action=DELETE
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **GCE** | Google Compute Engine | Dịch vụ máy ảo (VM) của GCP |
| **PD** | Persistent Disk | Block storage gắn vào VM, bền qua stop/delete |
| **MIG** | Managed Instance Group | Nhóm VM tự co giãn do GCP quản lý |
| **Instance Template** | Khuôn máy | Đặc tả để MIG đẻ ra VM (machine type, image...) |
| **IAP** | Identity-Aware Proxy | Cho SSH/HTTPS qua xác thực Google identity |
| **CUD** | Committed Use Discount | Giảm giá khi cam kết dùng dài hạn |
| **SUD** | Sustained Use Discount | Giảm giá tự động khi dùng nhiều trong tháng |
| **Spot VM** | Máy ưu tiên thấp | Rẻ 60-91%, có thể bị reclaim bất cứ lúc nào |
| **Live Migration** | Di chuyển nóng | Chuyển VM sang host khác không downtime |
| **Metadata service** | Dịch vụ metadata | Endpoint nội bộ để VM lấy config + token |
| **Startup script** | Kịch bản khởi động | Đoạn bash chạy khi VM boot |
| **Custom image** | Ảnh tùy biến | Image dựng từ snapshot của một disk |
| **Image family** | Dòng image | Tên tượng trưng luôn trỏ tới image mới nhất |
| **Local SSD** | Ổ SSD nội | NVMe ephemeral, mất data khi stop |
| **Hyperdisk** | Đĩa thế hệ mới | Disk gen 2024+, tunable IOPS/throughput |
| **Rolling update** | Cập nhật cuốn chiếu | Deploy zero-downtime cho MIG |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [GCP — Tổng quan + account setup + gcloud CLI](00_what-is-gcp-overview.md)
- ➡️ **Bài tiếp theo:** [GCP Cloud Storage + IAM](02_cloud-storage-and-iam.md)
- ↑ **Về cụm:** [GCP (Google Cloud Platform)](../../README.md)
- 🗺️ **Tấm bản đồ sự nghiệp:** [Cloud Engineer Career Roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **Đối chiếu AWS:** [EC2 + EBS — Compute foundation](../../../aws/lessons/01_basic/01_ec2-and-ebs-compute.md) — dịch vụ tương đương bên AWS.
- ☸️ **Bối cảnh GKE:** [Kubernetes](../../../../10_devops/kubernetes/) — khi muốn chạy container thay vì quản VM thủ công.
- 🏗️ **Quản hạ tầng bằng code:** [Infrastructure as Code (Terraform)](../../../../10_devops/iac/) — dựng lại toàn bộ resource trong bài này bằng Terraform.

### 🌐 Tài nguyên tham khảo khác

- [Compute Engine docs](https://cloud.google.com/compute/docs) — tài liệu gốc đầy đủ nhất.
- [Machine families](https://cloud.google.com/compute/docs/machine-resource) — chi tiết từng family.
- [Persistent Disk types](https://cloud.google.com/compute/docs/disks) — bảng IOPS/throughput cập nhật.
- [Hyperdisk](https://cloud.google.com/compute/docs/disks/hyperdisks) — đĩa thế hệ mới.
- [MIG autoscaling](https://cloud.google.com/compute/docs/autoscaler) — cấu hình autoscale.
- [IAP TCP forwarding](https://cloud.google.com/iap/docs/using-tcp-forwarding) — SSH/RDP qua IAP.
- [CUD calculator](https://cloud.google.com/products/calculator) — ước tính tiết kiệm CUD.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 01 GCP basic. Machine type 10 family + PD 6 type + custom image + startup script + MIG + autoscale + Live Migration + CUD/SUD/Spot pricing + IAP SSH + hands-on FastAPI MIG + 8 pitfalls. Pattern theo AWS lesson 01 EC2.
- **v2.0.0 (01/06/2026)** — Viết lại toàn bộ prose sang tiếng Việt narrative theo gold-standard (lời dẫn trước mỗi bảng/code/list, mạch WHY→WHAT→HOW, câu phân tích sau); chuẩn hoá metadata sang "Yêu cầu trước" + Alert Box mục tiêu; Glossary chuyển sang 3 cột; thêm mục Cheatsheet; nav chuẩn ⬅️/➡️/↑ với link-text = tiêu đề thật + xoá nhãn "(sắp viết)" cho bài 02 đã tồn tại; sửa code-error: `--custom-vm-type` → `--machine-type=n2-custom-6-12288`, regional MIG dùng `--region` nhất quán, thêm systemd unit file cho FastAPI trước `systemctl enable`; inline lại lệnh template/MIG/LB ở hands-on thay cho "(Xem section 4)"; làm rõ IOPS/throughput đĩa là "tối đa, tunable".
- **v2.0.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
