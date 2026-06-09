# 🎓 Pricing Models — On-demand / Reserved / Spot / Savings Plans

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [FinOps — Văn hóa quản lý chi phí Cloud](00_what-is-finops-overview.md)

> 🎯 *Hiểu FinOps overview rồi, giờ vào **tactic số 1**: chọn đúng pricing model. Bài này dạy 5 model chính (On-demand, RI/CUD/RVI, Savings Plans, Spot/Preemptible, Hybrid Benefit), tính **break-even point**, nhận biết **hidden cost** kinh điển (egress, NAT Gateway, IPv4 charge 2024+). Sau bài này bạn tính được nên mua RI bao lâu, có nên dùng Spot không.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **On-demand** và khi nào dùng
- [ ] Tính được **break-even** cho Reserved Instance (AWS) / CUD (GCP) / RVI (Azure)
- [ ] Hiểu **Savings Plans** AWS — flex hơn RI thế nào
- [ ] Dùng **Spot / Preemptible / Azure Spot** cho fault-tolerant workload
- [ ] Áp dụng **Azure Hybrid Benefit** (mang license Windows/SQL on-prem lên cloud)
- [ ] Tính **commitment math** chính xác (1-year vs 3-year ROI)
- [ ] Phát hiện 3 hidden cost lớn: **data egress**, **NAT Gateway**, **IPv4 public IP charge 2024+**

---

## Tình huống — Acme Shop quyết định mua gì

Sếp tech họp với FinOps practitioner:

> *"Bill $50k/tháng. CFO yêu cầu giảm 25%. Bạn nhìn workload: 60% là web app steady traffic (EC2 24/7), 20% batch processing đêm, 20% dev/test. Mua RI? Spot? Savings Plan? Quyết hôm nay, mai mình ký."*

Bạn — FinOps practitioner — phải trả lời:
1. **Bao nhiêu % capacity** an toàn commit dài hạn?
2. **1-year hay 3-year**?
3. **RI tradition hay Savings Plan**?
4. Batch đêm có bỏ Spot được không?
5. Dev/test có cách nào rẻ hơn?

→ Để trả lời được, bạn phải hiểu **chi tiết từng pricing model** — chứ không thể "vibe-based decision".

---

## 1️⃣ On-demand — Pay-as-you-go

🪞 **Ẩn dụ**: *On-demand giống **đi taxi Grab** — bật là chạy, tắt là dừng, không cam kết. Giá đắt nhất trong các option vì tiện nhất.*

### Đặc điểm

| Khía cạnh | Chi tiết |
|---|---|
| **Cam kết** | Không có |
| **Discount** | 0% — giá list |
| **Billing** | Per-second (Linux EC2/GCE) hoặc per-hour (Windows, một số instance) |
| **Phù hợp** | Dev/test, workload không đoán được, traffic spike đột ngột, POC |

### Ví dụ giá (us-east-1, 2026)

| Cloud | Instance | $/hour | $/tháng (730h) |
|---|---|---|---|
| AWS | t3.medium | $0.0416 | $30 |
| AWS | m6i.large | $0.0960 | $70 |
| AWS | m7i.large | $0.1008 | $74 |
| GCP | e2-medium | $0.0335 | $24 |
| GCP | n2-standard-2 | $0.0971 | $71 |
| Azure | Standard_B2s | $0.0496 | $36 |
| Azure | Standard_D2s_v5 | $0.0960 | $70 |

→ **Quy tắc**: Nếu workload chạy < 25% / tháng (vd: chỉ chạy giờ làm việc) → On-demand đã tối ưu. Mua RI = lỗ.

---

## 2️⃣ Reserved Instances — AWS RI / GCP CUD / Azure RVI

🪞 **Ẩn dụ**: *Reserved giống **đăng ký gói cước hậu mãi 12 tháng / 36 tháng** — cam kết dùng dài, được giảm sâu. Không dùng cũng phải trả.*

### So sánh 3 cloud

| Cloud | Tên gọi | 1-year | 3-year |
|---|---|---|---|
| **AWS** | Reserved Instances (RI) | −30-40% | −50-72% |
| **GCP** | Committed Use Discount (CUD) | −20-25% | −50-57% |
| **Azure** | Reserved VM Instances (RVI) | −30-40% | −60-65% |

### AWS Reserved Instances — 4 loại

| Loại | Đặc điểm |
|---|---|
| **Standard RI** | Discount cao nhất, lock instance type + region |
| **Convertible RI** | Discount thấp hơn ~10%, đổi được instance type trong cùng family |
| **Scheduled RI** | (Đã deprecated 2026) — chỉ chạy theo schedule |
| **Regional RI** | Apply cho cả region, không lock AZ |
| **Zonal RI** | Lock AZ, có capacity reservation kèm |

Payment options:

| Option | Trả tiền | Discount tăng thêm |
|---|---|---|
| **No Upfront** | Hàng tháng | 0% |
| **Partial Upfront** | 50% upfront, 50% hàng tháng | +5% |
| **All Upfront** | 100% upfront | +10% |

→ Combo `Standard + 3-year + All Upfront` = max discount (~72%).

### GCP Committed Use Discount — 3 loại

| Loại | Cam kết gì | Discount |
|---|---|---|
| **Resource-based CUD** | vCPU + RAM count, bind machine family | 1y: −37%, 3y: −55% |
| **Spend-based CUD** | $ spend per hour, bất kỳ machine type | 1y: −20%, 3y: −46% |
| **Flexible CUD** (2024+) | $ spend, không bind region/family | 1y: −28%, 3y: −46% |

→ Flexible CUD là update lớn của 2024 — giải quyết pain "mua CUD xong muốn đổi region".

### Azure Reserved VM Instances

- 1 hoặc 3 năm.
- Pay upfront hoặc monthly.
- Có thể **cancel** với 12% phí (early termination) — flex hơn AWS RI.
- Apply cross-subscription trong cùng Enrollment Account.

### Khi nào mua RI/CUD/RVI

✅ **Nên mua**:
- Workload chạy **24/7** suốt 1+ năm.
- Instance type **stable** (không migration trong 1-3 năm).
- Đã có **>3 tháng usage history** để forecast.

❌ **Không nên**:
- Workload < 70% utilization.
- Đang migration plan (Lambda, ECS, container).
- Startup chưa ổn định product (instance type còn đổi).

---

## 3️⃣ AWS Savings Plans — flex hơn RI

🪞 **Ẩn dụ**: *Savings Plans giống **gói tiêu thụ điện cam kết** — bạn cam kết tiêu X kWh/giờ trong 1-3 năm, không bind cụ thể bóng đèn nào.*

### 2 loại Savings Plans

| Loại | Bind gì | Apply cho | Discount max |
|---|---|---|---|
| **Compute Savings Plans** | $ spend/hour | EC2 + Fargate + Lambda | −66% |
| **EC2 Instance Savings Plans** | $ spend/hour + family + region | EC2 only, fixed family | −72% |

### Savings Plans vs RI — bảng so sánh

| Khía cạnh | RI | Compute SP | EC2 SP |
|---|---|---|---|
| **Cam kết** | Instance count | $ spend/hour | $ spend/hour |
| **Discount max** | 72% | 66% | 72% |
| **Flex region** | ❌ (Standard) | ✅ | ❌ |
| **Flex family** | Trong cùng (Convertible) | ✅ | ❌ |
| **Apply Fargate/Lambda** | ❌ | ✅ | ❌ |
| **Đổi instance type** | Khó (chỉ Convertible) | Auto-apply | Auto trong family |

→ **2026 recommend**: Compute Savings Plans cho hầu hết workload — flex tốt, discount đủ sâu.

### Ví dụ thực tế

Acme Shop có 10 EC2 m6i.large 24/7:

- On-demand: $70/tháng × 10 × 12 = **$8,400/year**
- RI 3-year Standard All Upfront: $8,400 × 0.28 = **$2,352/year** (save $6,048)
- Compute SP 3-year No Upfront: $8,400 × 0.34 = **$2,856/year** (save $5,544, nhưng flex region/family)

→ Save kém RI ~$500/year nhưng được flex — đáng cho team đang scale.

---

## 4️⃣ Spot / Preemptible — Capacity dư

🪞 **Ẩn dụ**: *Spot giống **vé máy bay phút chót** — cloud có máy bay (server) trống, bán rẻ 60-90%, nhưng có thể đổi ý kéo bạn xuống bất cứ lúc nào.*

### So sánh 3 cloud

| Cloud | Tên | Discount | Cảnh báo trước khi terminate | Max duration |
|---|---|---|---|---|
| **AWS** | Spot Instances | 60-90% | 2 phút | Không giới hạn |
| **GCP** | Spot VM | 60-91% | 30 giây | Không giới hạn (Preemptible legacy: cap 24h) |
| **Azure** | Azure Spot VM | up to 90% | 30 giây | Không giới hạn (có eviction policy) |

### Workload phù hợp ✅

- **Batch processing** (data pipeline, ETL).
- **CI/CD runner** (GitHub Actions self-hosted, Jenkins agent).
- **ML training** với checkpoint save.
- **Stateless web** với load balancer + auto-replace.
- **Render farm** (video, 3D).
- **Big data** (Spark on EMR / Dataproc).

### Workload KHÔNG phù hợp ❌

- **Database primary** (stateful, mất data).
- **Single-instance critical** (no HA fallback).
- **Long-running computation** không có checkpoint.
- **Customer-facing real-time** (vd: video call server).

### AWS Spot Fleet — chiến lược nâng cao

**Spot Fleet** = chạy nhiều instance type/AZ cùng lúc, target capacity tổng:

```bash
aws ec2 create-fleet \
  --type maintain \
  --target-capacity-specification TotalTargetCapacity=10,DefaultTargetCapacityType=spot \
  --launch-template-configs '[{
    "LaunchTemplateSpecification": {"LaunchTemplateId":"lt-abc","Version":"$Latest"},
    "Overrides": [
      {"InstanceType":"m6i.large","AvailabilityZone":"us-east-1a"},
      {"InstanceType":"m6i.large","AvailabilityZone":"us-east-1b"},
      {"InstanceType":"m6a.large","AvailabilityZone":"us-east-1a"},
      {"InstanceType":"m7i.large","AvailabilityZone":"us-east-1b"}
    ]
  }]'
```

→ AWS chọn pool nào rẻ + ít interrupt nhất. Giảm risk single-pool drain.

### GCP Spot VM

```bash
gcloud compute instances create batch-worker \
    --machine-type=n2-standard-4 \
    --provisioning-model=SPOT \
    --instance-termination-action=DELETE \
    --max-run-duration=24h
```

→ 60-91% off, có thể reclaim bất kỳ lúc nào.

### Spot interruption handling

Pattern chuẩn cho stateless worker:

```python
# Worker code
import signal, sys

def handle_term(signum, frame):
    # 2-minute warning from AWS Spot
    print("Spot interruption — saving checkpoint")
    save_state()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_term)

while True:
    process_job()  # idempotent, can resume
```

→ Combine với SQS visibility timeout — job được retry trên instance khác nếu interrupt.

---

## 5️⃣ Azure Hybrid Benefit — mang license on-prem lên cloud

🪞 **Ẩn dụ**: *Hybrid Benefit giống **mang gạo nhà mình lên nhà hàng nhờ nấu** — bạn đã trả tiền cho gạo (Windows/SQL license), nhà hàng (Azure) chỉ tính tiền nấu (compute), không tính tiền gạo nữa.*

### Áp dụng cho

| Resource | Discount |
|---|---|
| **Windows Server VM** | Up to −40% so với pay-as-you-go Windows |
| **SQL Server VM** | Up to −55% |
| **Azure SQL Database** | Up to −55% |
| **Azure SQL Managed Instance** | Up to −55% |

### Điều kiện

- Có **Software Assurance** hoặc **Subscription license** đang active.
- License Microsoft on-prem có thể "lend" lên Azure trong thời gian đang dùng.

### Ví dụ

Công ty có 50 Windows Server license + Software Assurance trên-prem. Migrate 20 VM lên Azure:
- Pay-as-you-go: $200/VM/tháng × 20 = $4,000/tháng.
- Với Hybrid Benefit: $120/VM/tháng × 20 = $2,400/tháng → **save $1,600/tháng** ($19,200/year).

→ **2026 lưu ý**: AWS có *License Included* (giá đã có Windows license) hoặc *BYOL* (Bring Your Own License). GCP có *Sole-Tenant Nodes* để BYOL. Nhưng feature gọn nhất là Azure.

---

## 6️⃣ Commitment math — Tính break-even

Câu hỏi cốt lõi: **bao giờ thì RI/CUD hoàn vốn so với on-demand?**

### Công thức

```
Break-even (tháng) = Upfront_cost / Monthly_savings

Trong đó:
  Monthly_savings = On_demand_monthly - RI_effective_monthly
  
RI_effective_monthly = (Upfront_cost / commitment_months) + Hourly_RI_rate × 730
```

### Ví dụ — Acme Shop m6i.large 3-year All Upfront

| Mục | Giá |
|---|---|
| On-demand: $0.096/hour × 730h | **$70.08/tháng** |
| RI 3-year All Upfront giá | $1,512 lump-sum |
| RI effective/tháng (chia 36 tháng) | $42/tháng |
| Saving/tháng | $28.08 |
| Break-even | $1,512 / $28.08 ≈ **54 tháng** ❌ |

Khoan — số trên **không đúng**. Lý do: All Upfront có nghĩa toàn bộ 3 năm đã trả, không có hourly rate thêm. Tính lại:

| Mục | Giá |
|---|---|
| On-demand 3-year: $70.08 × 36 | **$2,523** |
| RI 3-year All Upfront | **$1,512** |
| Saving 3 năm | $1,011 |
| Discount thực tế | 40% |

→ **Đúng**: Sau **3 năm** bạn save $1,011. Vì All Upfront trả trọn ngay, "điểm hòa vốn" thực tế là khi chi phí on-demand tích lũy bằng số đã trả: $1,512 / $70.08 ≈ **22 tháng** — từ tháng 22 trở đi mọi tháng là saving thuần. Nếu giữa chừng (vd: 18 tháng) bạn migrate đi: $1,512 đã trả nhưng usage chỉ tương đương $1,261 on-demand → **lỗ $251**.

### Quy tắc commitment math

| Câu hỏi | Trả lời |
|---|---|
| Workload chắc chắn chạy >12 tháng? | Mua 1-year |
| Workload chắc chắn chạy >24 tháng? | Mua 3-year |
| Workload có thể bị thay thế trong < 12 tháng? | Đừng mua, on-demand |
| Không chắc 100% | Mua 1-year + Compute SP (flex), không 3-year |

### Coverage strategy

Đừng cam kết 100% baseline. Standard pattern:

```
Total capacity: 100 EC2

Reserved/SP commit:  70 EC2 (steady baseline, 3-year)
On-demand:           20 EC2 (burst handler)
Spot:                10 EC2 (stateless workers)

Risk: nếu workload drop 30% → RI vẫn dùng hết, không waste
```

→ **70-80% commit là sweet spot**.

---

## 7️⃣ Hidden cost — kẻ giết hóa đơn

Nhiều team mua RI/Spot rồi vẫn ngạc nhiên *"tại sao bill còn cao?"*. Lý do: 3 hidden cost dưới đây.

### Hidden cost 1 — Data egress (out của cloud)

**Egress** = data đi từ cloud ra Internet hoặc sang cloud khác.

| Cloud | Free tier egress | Giá vượt |
|---|---|---|
| **AWS** | 100 GB/tháng (2024+) | $0.09/GB (us → Internet), $0.02/GB (cross-region) |
| **GCP** | 200 GB/tháng (2024+) | $0.12/GB → Internet |
| **Azure** | 100 GB/tháng | $0.087/GB → Internet |

**Trap thật**: Acme Shop bật S3 cross-region replication US-east-1 → US-west-2 cho DR. 5 TB/tháng × $0.02 = **$100/tháng** silent extra.

**Cách giảm**:
- **CDN** (CloudFront/Cloud CDN/Azure CDN) — giảm origin egress 60-80%, lại có free tier riêng.
- **Cross-region replication** chỉ làm cho bucket critical, không phải mọi thứ.
- **VPC endpoints** (AWS): traffic đến S3 trong cùng region không tính egress.
- **Direct Connect / Interconnect**: pricing đặc biệt cho > 1 Gbps traffic.

### Hidden cost 2 — NAT Gateway (AWS)

**NAT Gateway** cho phép private subnet ra Internet (download package, gọi API).

| Mục | Giá AWS |
|---|---|
| Per NAT Gateway-hour | $0.045/h = **$33/tháng** |
| Data processed | $0.045/GB |

**Trap thật**: 1 VPC 3 AZ → 3 NAT Gateway (HA pattern) = **$99/tháng base** + traffic.

Acme Shop: 10 VPC × 3 AZ = 30 NAT Gateway = **$990/tháng** chỉ để private subnet ra Internet. Mỗi GB process còn $0.045 nữa.

**Cách giảm**:
- **NAT Instance** (EC2 nhỏ tự setup) — rẻ hơn nhiều nhưng cần maintain.
- **VPC Endpoint** cho service AWS (S3, DynamoDB, ECR) — không qua NAT.
- **Cẩn thận pattern multi-AZ NAT** — chỉ 1 NAT cho dev/test (chấp nhận downtime nhỏ khi AZ chết).
- GCP **Cloud NAT** có pricing khác, generous hơn (1 NAT/region, không charge per-GB nhỏ).

### Hidden cost 3 — IPv4 public IP charge (2024+)

**2024-02-01**: AWS bắt đầu charge **$0.005/h** ($3.65/tháng) cho mọi **public IPv4** — kể cả IP gắn vào EC2 đang chạy, kể cả Elastic IP (EIP) đang attach.

**Trước 2024**: chỉ charge khi EIP không attach (idle).\
**Sau 2024**: charge mọi public IPv4, regardless of attach.

| Resource | Charge |
|---|---|
| EC2 instance có public IP | $3.65/tháng |
| EIP attach | $3.65/tháng |
| EIP idle (không attach) | $3.65/tháng |
| Load Balancer public IP | $3.65/tháng/IP |
| NAT Gateway public IP | $3.65/tháng |

**Trap thật**: Acme Shop 200 EC2 đều có public IP (không setup VPC private subnet) → 200 × $3.65 = **$730/tháng** extra từ 2024.

**Cách giảm**:
- **Private subnet + ALB**: chỉ ALB cần public IP, EC2 đều private.
- **IPv6 dual-stack**: AWS chưa charge IPv6.
- Audit: `aws ec2 describe-addresses --filters Name=domain,Values=vpc` — xem có EIP idle nào không.

### Hidden cost 4 — Bonus: Log + Monitoring runaway

- **CloudWatch Logs ingestion**: $0.50/GB. App verbose log → 100 GB/tháng = $50.
- **DataDog / NewRelic**: per-host, scale theo traffic — startup hay bất ngờ.
- **GuardDuty / Defender**: ai cũng nghĩ rẻ, nhưng scan tất S3 + VPC flow log → có thể $500+/tháng.

→ Bài 02 sẽ dạy tag để allocate những cost này về team gây ra.

---

## 8️⃣ Đáp lại tình huống Acme Shop

Quay lại câu hỏi đầu bài. Khuyến nghị:

| Workload | % capacity | Pricing model | Lý do |
|---|---|---|---|
| Web app steady 24/7 | 60% | **Compute SP 3-year No Upfront** | Flex, save ~50%, cover baseline |
| Web app burst | thêm 10% baseline | **On-demand** | Handle spike chưa lock |
| Batch processing đêm | 20% | **Spot** | Fault-tolerant, save 70% |
| Dev/test | 10% | **On-demand + auto-shutdown 18h-8h sáng** | Save 65% effective (chỉ chạy 9h/ngày) |

**Projected saving**:
- Web 60%: $30k → $15k (−50%).
- Batch 20%: $10k → $3k (−70%).
- Dev 10%: $5k → $1.75k (−65%).
- Web burst 10%: $5k → $5k (no change).

→ Total: $50k → **$24.75k**, giảm **−50%**. Vượt mục tiêu 25%.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Mua RI 3-year cho instance type sẽ thay đổi

- **Triệu chứng**: Mua m5.xlarge 3-year, 6 tháng sau team chuyển sang m7g (Graviton ARM cheaper).
- **Nguyên nhân**: Lock instance type quá sớm.
- **Cách tránh**: Convertible RI hoặc Compute SP — đổi family không mất tiền.

### ❌ Cạm bẫy: Bật cross-region replication mọi S3 bucket

- **Triệu chứng**: S3 cost ổn nhưng egress tăng mạnh.
- **Nguyên nhân**: Apply replication blanket cho cả bucket non-critical.
- **Cách tránh**: Chỉ replicate bucket có RPO < 1h. Phần còn lại dùng versioning + cross-region backup hàng đêm (cheaper).

### ❌ Cạm bẫy: 1 NAT Gateway/AZ mọi VPC

- **Triệu chứng**: 30 NAT Gateway, $1k/tháng chỉ base.
- **Nguyên nhân**: Copy-paste pattern HA từ doc AWS không cân nhắc cost.
- **Cách tránh**: Dev/test 1 NAT, accept downtime nhỏ. Prod 2 NAT (không cần 3 cho mọi VPC).

### ✅ Best practice: Coverage 70-80%, không 100%

- **Vì sao**: Chừa room cho fluctuation, migration, downsize.
- **Cách áp dụng**: Quarterly review RI utilization. Nếu < 95% sau 3 tháng → bán RI Marketplace.

### ✅ Best practice: Bắt đầu Compute SP 1-year trước

- **Vì sao**: Flex tốt nhất, học cost behavior team trước khi commit 3-year.
- **Cách áp dụng**: Year 1 buy 1-year SP cover 60% baseline. Year 2 audit → mua 3-year cho phần stable.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Workload chạy 24/7, instance type m6i.large, dự kiến chạy 2 năm. Mua gì?

<details>
<summary>💡 Đáp án</summary>

**Compute Savings Plans 1-year No Upfront** — không phải 3-year RI.

Lý do:
- 2 năm chạy, nhưng business có thể đổi → flex.
- 1-year SP save 30-35%, đỡ rủi ro.
- Sau 1 năm review: nếu workload vẫn ổn → renew + cân nhắc thêm 3-year cho phần stable.

3-year quá sớm vì chỉ chắc 2 năm.

</details>

**Q2.** Batch processing chạy 8h/ngày, có thể chịu interrupt. Mua gì?

<details>
<summary>💡 Đáp án</summary>

**Spot Instances** (AWS) hoặc **Spot VM** (GCP) hoặc **Azure Spot**.

Save 60-90% so với on-demand. Setup checkpoint trong job code để resume khi bị interrupt. Combine với SQS/Pub-Sub queue + visibility timeout — message redelivery tự xử lý.

Đừng mua RI vì chạy 33% thời gian → RI sẽ idle 67%.

</details>

**Q3.** Tính break-even: m6i.large 3-year All Upfront $1,512. On-demand $70.08/tháng. Sau bao nhiêu tháng bạn save?

<details>
<summary>💡 Đáp án</summary>

Tháng 22 (với All Upfront).

Vì đã trả trọn $1,512 ngay từ đầu, "điểm hòa" là khi chi phí on-demand tích lũy bằng số đã trả:
$1,512 / $70.08/tháng = 21.6 tháng → từ tháng 22 trở đi, mọi tháng tiếp tục là **saving thuần** so với on-demand.

Xét trọn 36 tháng để thấy tổng lợi:
- 3 năm on-demand: $70.08 × 36 = $2,523.
- 3 năm RI: $1,512.
- Total saving: $1,011 (≈ 40% discount thực tế).

Nếu cancel sau 18 tháng → on-demand cùng kỳ chỉ $1,261, mà đã trả $1,512 → lỗ $251.

→ Chỉ mua 3-year khi chắc chắn chạy đủ 36 tháng.

</details>

**Q4.** Acme Shop 5 VPC × 3 AZ NAT Gateway. Có cách nào giảm?

<details>
<summary>💡 Đáp án</summary>

Có 3 cách:

1. **VPC Endpoints** cho S3, DynamoDB, ECR — traffic đến service AWS này không qua NAT (free). Riêng S3/DynamoDB là Gateway Endpoint hoàn toàn free.
2. **Dev/test VPC**: 1 NAT/VPC thay vì 3/VPC. Chấp nhận downtime nhỏ khi AZ chết.
3. **NAT Instance** (EC2 nhỏ tự host) — $5-10/tháng thay vì $33/tháng/NAT, nhưng phải maintain.

Save tiềm năng: 15 NAT → 5 NAT = $1k/tháng → $330/tháng.

</details>

**Q5.** Azure Hybrid Benefit có dùng được cho công ty không có Software Assurance không?

<details>
<summary>💡 Đáp án</summary>

**Không**. Hybrid Benefit yêu cầu:
- Windows Server license với **Software Assurance**, hoặc
- **Subscription license** (Office 365 / M365 với Windows License rights).

Không có SA → vẫn dùng Pay-as-you-go Windows ($200/VM/tháng) hoặc AWS Windows On-Demand.

Workaround: chuyển sang **Linux** nếu app cho phép, miễn license Windows hoàn toàn.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Pricing model | Best for | Saving |
|---|---|---|
| **On-demand** | Dev, burst, < 25% utilization | 0% |
| **Reserved (Standard 3y AUR)** | 24/7 stable workload, 3+ years | 50-72% |
| **Convertible RI** | 24/7 stable, có thể đổi instance type | 40-60% |
| **Compute Savings Plans** | Flex region/family, cover Lambda/Fargate | 50-66% |
| **EC2 Instance SP** | Lock family, flex size | 60-72% |
| **Spot Instances** | Stateless, fault-tolerant | 60-90% |
| **GCP Spot VM** | Tương tự AWS Spot, max 24h | 60-91% |
| **Azure Spot** | Tương tự AWS Spot | up to 90% |
| **Azure Hybrid Benefit** | Có Windows/SQL license + SA | 40-55% |
| **GCP Flexible CUD** | Cam kết $ spend, không bind region | 28-46% |

| Hidden cost | Mức độ | Cách giảm |
|---|---|---|
| **Egress** ($0.09/GB AWS) | 🔴 Lớn | CDN, VPC Endpoint, ít cross-region |
| **NAT Gateway** ($33/tháng/NAT) | 🟡 Vừa | VPC Endpoint, NAT Instance dev |
| **IPv4 charge** ($3.65/tháng/IP) | 🟡 Vừa | Private subnet + ALB, IPv6 |
| **CloudWatch Logs** ($0.50/GB) | 🟡 Vừa | Retention policy, log filter |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **On-demand** | Trả theo dùng | Pay-as-you-go, không cam kết |
| **Reserved Instance (RI)** | Instance đặt trước | AWS — cam kết 1-3y đổi discount |
| **Standard RI** | RI tiêu chuẩn | Lock instance + region, discount cao |
| **Convertible RI** | RI đổi được | Đổi instance type trong family, discount thấp hơn |
| **Savings Plans** | Gói tiết kiệm | AWS — cam kết $ spend, flex hơn RI |
| **Compute SP** | Compute Savings Plan | SP áp dụng EC2 + Fargate + Lambda |
| **CUD** | Committed Use Discount | GCP — tương đương RI |
| **Flexible CUD** | CUD linh hoạt | GCP 2024+ — cam kết spend, không bind region |
| **RVI** | Reserved VM Instance | Azure — tương đương RI |
| **Spot / Preemptible** | Spot / Có thể bị thu hồi | Capacity dư, rẻ 60-90%, có thể bị terminate |
| **Spot Fleet** | Hạm đội Spot | AWS — multi-type/AZ strategy |
| **Hybrid Benefit** | Lợi ích lai | Azure — mang Windows/SQL license on-prem lên cloud |
| **Software Assurance (SA)** | Đảm bảo phần mềm | Microsoft license program cho Hybrid Benefit |
| **Egress** | Lưu lượng đi ra | Data ra Internet hoặc cross-region/cross-cloud |
| **NAT Gateway** | Cổng NAT | AWS managed NAT cho private subnet |
| **VPC Endpoint** | Điểm cuối VPC | Truy cập service AWS không qua NAT |
| **Break-even** | Điểm hòa vốn | Khi commitment hoàn vốn so với on-demand |
| **Coverage** | Tỷ lệ bao phủ | % capacity được cover bởi RI/SP |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [FinOps — Văn hóa quản lý chi phí Cloud](00_what-is-finops-overview.md)
- ➡️ **Bài tiếp theo:** [Tagging, Allocation & Showback Reports](02_tagging-allocation-and-showback.md)
- ↑ **Về cụm:** [Cloud Cost Management](../../README.md)

### 🧩 Các chủ đề liên quan

- ☁️ [AWS EC2 pricing](../../../aws/lessons/01_basic/01_ec2-and-ebs-compute.md) — pricing context EC2
- ☁️ [GCP CUD trong Compute Engine](../../../gcp/lessons/01_basic/01_compute-engine-and-disks.md) — CUD/SUD detail

### 🌐 Tài nguyên tham khảo khác

- 📖 [AWS Savings Plans docs](https://docs.aws.amazon.com/savingsplans/) — official
- 📖 [AWS Reserved Instances](https://aws.amazon.com/ec2/pricing/reserved-instances/)
- 📖 [Spot Instance Advisor](https://aws.amazon.com/ec2/spot/instance-advisor/) — interrupt rate per instance type
- 📖 [GCP Committed Use Discounts](https://cloud.google.com/docs/cuds-introduction)
- 📖 [GCP Flexible CUD](https://cloud.google.com/billing/docs/how-to/cud-flexible) — 2024+
- 📖 [Azure Reservations docs](https://learn.microsoft.com/azure/cost-management-billing/reservations/)
- 📖 [Azure Hybrid Benefit](https://azure.microsoft.com/pricing/hybrid-benefit/)
- 📖 [AWS Data Transfer pricing](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer) — egress detail
- 📖 [AWS public IPv4 charge announcement](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 01 cluster cloud-cost-management. 5 pricing model deep dive (On-demand + RI/CUD/RVI + Savings Plans + Spot + Hybrid Benefit) + commitment math + break-even tính cụ thể + 4 hidden cost (egress, NAT Gateway, IPv4 charge 2024+, log runaway) + Acme Shop $50k → $24.75k worked example + 5 pitfalls + 5 self-check.
- **v1.1.0 (01/06/2026)** — Chuẩn hóa nav (marker ⬅️/➡️/↑ + link text = tiêu đề H1 thật, 3 sub 🧭/🧩/🌐), metadata "Yêu cầu trước", Glossary header "Thuật ngữ | Tiếng Việt | Giải thích". Sửa factual: GCP Spot VM max duration "Không giới hạn" (cap 24h chỉ áp Preemptible legacy). Thống nhất định nghĩa break-even (~22 tháng) giữa §6 và Self-check Q3.
