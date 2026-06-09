# 🆘 Multi-cloud — Disaster Recovery + Architecture Patterns

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Bài [Kubernetes Multi-cloud — Anthos, Azure Arc, Cluster API, Service Mesh](03_kubernetes-multi-cloud-and-anthos-arc.md) ✅

> 🎯 *Bài 04 (cuối basic). Hai topic kết thúc: **DR patterns** (4 mô hình + RTO/RPO + multi-cloud DR vs single-cloud multi-region) + **architecture patterns** (cloud-agnostic vs cloud-portable vs cloud-native) + case study migration AWS→GCP. Hands-on viết runbook DR + Terraform multi-provider skeleton.*

## 🎯 Sau bài này bạn sẽ

- [ ] Định nghĩa **RTO** (Recovery Time Objective) và **RPO** (Recovery Point Objective)
- [ ] Phân biệt **4 DR patterns**: Backup-Restore / Pilot Light / Warm Standby / Multi-region Active-Active
- [ ] Quyết định khi nào **multi-cloud DR** thay vì single-cloud multi-region
- [ ] Hiểu **3 architecture pattern**: cloud-agnostic / cloud-portable / cloud-native — trade-off
- [ ] Đọc case study **migration AWS → GCP** thực tế: bước, gotcha, cost, timeline
- [ ] Viết **DR runbook** + test schedule (DR drill quarterly)
- [ ] FinOps multi-cloud — tracking + showback cross-cloud
- [ ] Hands-on: Terraform module với multi-provider AWS + GCP

---

## Tình huống — Acme Shop sau incident lớn

Tháng trước AWS `us-east-1` down 4 giờ. Acme Shop deploy 100% trên AWS → mất doanh thu ~$80k.

CEO triệu họp:

> *"Lần sau không được mất nữa. Multi-region đã có, mà toàn AWS hỏng thì cả 2 region đều liên đới. Bạn đề xuất multi-cloud DR — bao lâu, bao nhiêu tiền, complexity ops thế nào. Cuối tuần present."*

Bạn cần:
- Phân tích RTO/RPO target (CEO chấp nhận downtime 30 phút, mất data 5 phút).
- Compare 4 DR pattern × cost × ops complexity.
- Multi-cloud (GCP làm DR site) vs multi-region (AWS thứ 2 region).
- Đề xuất + runbook test plan.

Bài này dạy framework decision + pattern + case study.

---

## 1️⃣ RTO + RPO — Định nghĩa core

🪞 **Ẩn dụ**: *RTO/RPO như **2 chỉ số bác sĩ cấp cứu**: RTO = "bao lâu để hồi sức tỉnh lại" (downtime chấp nhận được), RPO = "bao nhiêu phút trí nhớ bệnh nhân được phép mất" (data loss chấp nhận được). Số càng nhỏ → giường bệnh càng đắt.*

Trước khi chọn pattern DR, bạn phải chốt được 4 con số dưới đây. Hai số đầu (*RTO*, *RPO*) trả lời "chịu được bao lâu, mất bao nhiêu"; hai số sau (*SLA*, *SLO*) là lời hứa với khách hàng và mục tiêu nội bộ. Mọi quyết định kiến trúc DR đều quy về cân bằng giữa 4 con số này với chi phí.

| Chỉ số | Câu hỏi nó trả lời | Đơn vị đo | Ví dụ |
|---|---|---|---|
| **RTO** (*Recovery Time Objective*) | Bao lâu mới online trở lại sau thảm hoạ? | Thời gian | RTO = 1h: có thể chịu 1 giờ downtime |
| **RPO** (*Recovery Point Objective*) | Mất tối đa bao nhiêu dữ liệu? | Thời gian (tính từ điểm backup gần nhất) | RPO = 5p: chấp nhận mất 5 phút giao dịch |
| **SLA** (*Service Level Agreement*) | Cam kết uptime với khách hàng | % uptime | 99.9% = ~8.76h downtime/năm |
| **SLO** (*Service Level Objective*) | Mục tiêu nội bộ (thường khắt khe hơn SLA) | % | 99.95% |

→ Nhìn cột "Đơn vị đo": RTO và RPO đều đo bằng **thời gian** — đó là lý do người ta hay nhầm lẫn. Mẹo phân biệt: RTO nhìn về phía *tương lai* (bao lâu nữa thì khôi phục xong), RPO nhìn về phía *quá khứ* (lùi lại tới điểm dữ liệu nào còn an toàn).

### Phân tier theo mức độ trọng yếu

Không phải dịch vụ nào cũng cần RTO/RPO bằng nhau. Trang admin nội bộ sập 1 ngày không ai chết, nhưng cổng thanh toán sập 1 phút là mất tiền thật. Vì thế ta chia hệ thống thành các *tier* (cấp) theo mức độ trọng yếu, rồi gán cho mỗi tier một mục tiêu RTO/RPO và một DR pattern tương xứng — tránh chi quá tay cho thứ không quan trọng.

| Tier | Mô tả | RTO điển hình | RPO điển hình | DR pattern |
|---|---|---|---|---|
| Tier 0 | Mission-critical (banking, healthcare) | < 1 phút | 0 (zero data loss) | Active-Active multi-region |
| Tier 1 | Critical biz (e-commerce checkout) | < 15 phút | < 5 phút | Warm Standby hoặc Active-Active |
| Tier 2 | Important (catalog, analytics) | < 4 giờ | < 1 giờ | Pilot Light |
| Tier 3 | Internal tools (admin, BI) | < 24 giờ | < 24 giờ | Backup-Restore |

→ Acme Shop checkout = Tier 1 (RTO 15p, RPO 5p) → Warm Standby là phù hợp.

---

## 2️⃣ Bốn DR pattern — từ rẻ-chậm tới đắt-nhanh

Có 4 cách dựng "phương án dự phòng" cho hệ thống, xếp theo trục đánh đổi quen thuộc: càng muốn khôi phục nhanh thì càng tốn tiền. Hãy hình dung 4 pattern như 4 mức bảo hiểm xe: từ "chỉ giữ giấy tờ để mua xe mới" (rẻ nhất) đến "luôn có sẵn xe thứ hai chạy song song" (đắt nhất). Phần dưới đi lần lượt từ rẻ nhất lên, mỗi pattern kèm sơ đồ, đặc tính RTO/RPO và tier phù hợp.

### Pattern 1 — Backup-Restore (lạnh)

DR site ở trạng thái "lạnh": chưa có gì chạy, chỉ có bản backup nằm chờ. Đây là phương án rẻ nhất nhưng khôi phục chậm nhất vì khi sự cố xảy ra mới bắt đầu dựng lại hạ tầng từ con số 0.

```text
Production (cloud A)              DR site (cloud B / region B)
  ↓ daily snapshot
  └→ S3 / GCS                     [empty]
```

- DR site **chưa có gì** chạy.
- Khi có thảm hoạ: restore từ backup, provision hạ tầng mới.
- **RTO**: hàng giờ tới hàng ngày. **RPO**: hàng giờ (tính tới bản backup gần nhất).
- **Chi phí**: rẻ nhất (chỉ trả tiền lưu trữ backup).

→ Phù hợp **Tier 3** (analytics, công cụ nội bộ).

### Pattern 2 — Pilot Light (đèn chờ)

Tên gọi *pilot light* lấy từ ngọn lửa nhỏ luôn cháy trong bình nóng lạnh — chỉ cần bật là bùng lên ngay. Ở đây "ngọn lửa chờ" chính là database luôn được đồng bộ sang DR site, còn app server thì để sẵn image nhưng không chạy.

```text
Production (A)                    DR site (B)
  All workload running            Core systems "đèn pilot" — DB replica streaming
                                  App servers: scaled to 0 (image ready)
```

- Database **đang replicate trực tiếp** sang DR site (read replica / streaming).
- App server đã đóng gói sẵn (AMI / container image) nhưng **không chạy**.
- Khi có thảm hoạ: scale up app + chuyển DNS (cutover).
- **RTO**: 10-60 phút. **RPO**: vài giây (độ trễ replica).
- **Chi phí**: trung bình (trả tiền DB chạy liên tục + lưu trữ).

→ Phù hợp **Tier 2**.

### Pattern 3 — Warm Standby (ấm)

Khác Pilot Light, ở đây toàn bộ stack **đã chạy thật** tại DR site nhưng ở quy mô thu nhỏ (ví dụ 1 instance thay vì 10). Khi sự cố chỉ cần "thổi phồng" lên quy mô đầy đủ, nên khôi phục rất nhanh.

```text
Production (A)                    DR site (B)
  Full workload                   Same workload — scaled DOWN (1 instance instead of 10)
```

- DR site **chạy đủ stack** ở quy mô nhỏ (1 instance mỗi service).
- DB streaming replication.
- Khi có thảm hoạ: scale up + chuyển hướng traffic.
- **RTO**: 1-15 phút. **RPO**: < 1 phút.
- **Chi phí**: cao (trả ~30-50% chi phí prod đầy đủ).

→ Phù hợp **Tier 1**. Đúng với cổng checkout của Acme Shop.

### Pattern 4 — Multi-region Active-Active (nóng)

Mức cao nhất: cả 2 region đều đang phục vụ người dùng thật cùng lúc, không có khái niệm "site chính / site dự phòng". Khi một bên sập, traffic tự động dồn sang bên còn lại gần như tức thì.

```text
Production region A ←──────────→ Production region B
  Load balancer global routes traffic to nearest
  Both serve real users; DB multi-master or replicated
```

- Cả 2 region đang phục vụ traffic thật.
- Global LB (Cloudflare, AWS Global Accelerator, GCP Global LB) định tuyến theo độ trễ (latency).
- DB: multi-master (Spanner, CockroachDB, Cassandra) hoặc replicated kèm failover.
- **RTO**: < 1 phút. **RPO**: 0 (nếu strong consistency) hoặc vài giây (eventual).
- **Chi phí**: cao nhất (2x hạ tầng + global LB + chi phí truyền dữ liệu cross-region).

→ Phù hợp **Tier 0** (banking, healthcare, e-commerce lớn).

### Bảng so sánh 4 pattern

Đặt 4 pattern cạnh nhau, bạn thấy ngay quy luật đánh đổi: kéo RTO/RPO xuống thì chi phí và độ phức tạp vận hành kéo lên. Bảng này là công cụ chốt nhanh khi đứng trước bài toán "ngân sách X thì DR được tới đâu".

| Pattern | RTO | RPO | Chi phí (% prod) | Độ phức tạp vận hành |
|---|---|---|---|---|
| Backup-Restore | hàng giờ - hàng ngày | hàng giờ | 5-10% | Thấp |
| Pilot Light | 10-60p | vài giây | 15-25% | Trung bình |
| Warm Standby | 1-15p | < 1p | 30-50% | Trung bình - Cao |
| Active-Active | < 1p | 0 - vài giây | 100-150% | Rất cao |

---

## 3️⃣ Multi-cloud DR vs Single-cloud Multi-region

🪞 **Ẩn dụ**: *Single-cloud multi-region như **2 chi nhánh ngân hàng cùng tập đoàn** — chia sẻ chính sách, hệ thống; nếu tập đoàn hỏng cả 2 cùng hỏng. Multi-cloud DR như **gửi tiền ở 2 ngân hàng khác nhau** — chống cả "tập đoàn hỏng" nhưng quy trình giao dịch khác nhau, mệt hơn.*

Nhiều người vội kết luận "muốn an toàn thì cứ multi-cloud", nhưng đó là cái bẫy chi phí. Bảng dưới liệt kê từng lý do thường gặp và trả lời thẳng: lý do đó có *thực sự* đáng để gánh độ phức tạp của multi-cloud DR không.

### Khi nào thực sự cần multi-cloud DR

| Lý do | Có đáng dùng multi-cloud DR? |
|---|---|
| Sự cố toàn vendor (AWS sập toàn cầu) | ✅ Chỉ multi-cloud mới chống được |
| Sự cố 1 region (AWS us-east-1) | ❌ Single-cloud multi-region là đủ |
| Quy định bắt buộc data nằm ở 2 vendor khác nhau (chủ quyền dữ liệu EU) | ✅ Multi-cloud là bắt buộc |
| Chọn dịch vụ tốt nhất từng mảng (*best-of-breed*: BigQuery + S3) | ✅ Nhưng độ phức tạp tăng |
| Lo bị khoá chân vào 1 vendor (*vendor lock-in*) | ✅ Để có đường thoát (*exit plan*) |
| RTO < 5 phút + ngân sách hạn chế | ❌ Multi-cloud quá phức tạp; multi-region rẻ và đủ |

→ Quy luật rút ra: multi-cloud DR chỉ "đáng tiền" khi rủi ro là **toàn vendor** hoặc do **quy định bắt buộc**. Còn rủi ro chỉ ở mức region thì single-cloud multi-region vừa rẻ vừa đủ.

### So sánh đánh đổi hai hướng

Nếu bảng trên trả lời "khi nào", bảng này trả lời "đắt/khó ở đâu". Đặt single-cloud multi-region cạnh multi-cloud DR theo từng khía cạnh vận hành để thấy rõ multi-cloud đổi lấy khả năng chống chịu bằng cái giá nào.

| Khía cạnh | Single-cloud multi-region | Multi-cloud DR |
|---|---|---|
| Chống sự cố vendor | Chỉ ở mức region | Cả vendor ✅ |
| Độ phức tạp thiết lập | Trung bình | Rất cao |
| Chi phí truyền dữ liệu giữa các site | Cross-region trong cùng cloud (rẻ) | Egress cross-cloud (đắt) |
| Tương đương dịch vụ | Y hệt (cùng dịch vụ AWS) | Khác nhau (Lambda vs Cloud Run) |
| Kỹ năng đội ngũ | Thạo 1 cloud | Phải thạo 2 cloud |
| Bộ công cụ vận hành | 1 bộ | 2 bộ (hoặc 1 lớp abstraction) |
| Đồng bộ dữ liệu | Native (replica cross-region) | Thủ công / bên thứ ba (cross-cloud) |
| Kiểm thử failover | Dễ hơn | Khó hơn |

### Thực tế 2026

Lý thuyết là vậy, nhưng thực tế các doanh nghiệp làm gì? Theo khảo sát Gartner 2025, con số hé lộ một khoảng cách lớn giữa "dùng multi-cloud" và "thực sự có multi-cloud DR".

- **89% doanh nghiệp dùng multi-cloud** — nhưng chỉ **12% có multi-cloud DR thật sự**.
- Phần còn lại dùng multi-cloud để **chọn dịch vụ tốt nhất từng mảng** (BigQuery cho analytics, AWS cho compute), chứ không phải để DR.
- **Khuyến nghị**: lấy single-cloud multi-region làm mặc định cho DR. Chỉ chọn multi-cloud DR khi RTO và quy định ép buộc mạnh.

---

## 4️⃣ Ba pattern kiến trúc — Cloud-native / Cloud-portable / Cloud-agnostic

DR pattern quyết định "khi sập thì khôi phục thế nào", còn pattern *kiến trúc* quyết định "ngay từ đầu, app gắn chặt với vendor tới mức nào". Có 3 mức, đi từ ôm trọn vendor để chạy nhanh, tới trung lập hoàn toàn để chạy đa cloud cùng lúc. Mỗi mức là một đánh đổi giữa tốc độ phát triển và khả năng di chuyển — chọn sai sẽ trả giá khi cần migrate hoặc dựng DR cross-vendor.

### Pattern A — Cloud-native (chấp nhận khoá chân)

App dùng trọn bộ dịch vụ managed của một vendor. Đổi lại tốc độ phát triển cao nhất nhưng gắn chặt vào vendor đó.

```text
App dùng:
- AWS Lambda + DynamoDB + S3 + SQS + Cognito
- Hoàn toàn AWS-specific
```

- **Ưu**: tận dụng managed service mạnh, phát triển nhanh.
- **Nhược**: migrate cực khó.
- **Khi chọn**: startup, chiến lược 1 cloud, không có kế hoạch DR multi-cloud.

### Pattern B — Cloud-portable (di chuyển được, mỗi lần 1 cloud)

App xây trên các lớp tiêu chuẩn mở, có thể bê sang cloud khác khi cần — nhưng không chạy đồng thời nhiều cloud. Đây là điểm cân bằng phổ biến nhất.

```text
App dùng:
- Kubernetes (GKE / EKS / AKS) — lớp portable
- Postgres (RDS / Cloud SQL / Azure DB)
- Lưu trữ tương thích S3 (S3 / GCS / R2)
- Chuẩn mở (OAuth, JWT, OpenAPI)
```

- **Ưu**: migrate được, đường thoát rõ ràng.
- **Nhược**: phải bỏ qua một số managed feature đặc thù.
- **Khi chọn**: công ty vừa - lớn, có kế hoạch DR, coi trọng đường thoát (*exit strategy*).

### Pattern C — Cloud-agnostic (multi-cloud đồng thời)

Mức trung lập tuyệt đối: dùng lớp abstraction để chạy song song trên nhiều cloud cùng lúc. Mạnh nhất về tính di chuyển nhưng cũng phức tạp và tốn người nhất.

```text
App dùng:
- Crossplane / Terraform (lớp abstraction)
- K8s + Istio multi-cluster
- Vault / ESO quản lý secrets cross-cloud
- DB bên thứ ba (Snowflake, MongoDB Atlas)
- Cloudflare cho edge + định tuyến traffic
```

- **Ưu**: trung lập vendor, di chuyển thật sự dễ dàng.
- **Nhược**: độ phức tạp rất cao, cần đội vận hành lớn, tốc độ phát triển chậm hơn 30-50%.
- **Khi chọn**: doanh nghiệp tier-0, quy định ép buộc mạnh, có đội platform > 10 kỹ sư.

### Cây quyết định chọn pattern

Ba pattern nghe đều hấp dẫn, nhưng đa số đội ngũ không nên nhảy thẳng lên cloud-agnostic. Cây quyết định dưới đây lọc theo nhu cầu thực tế: chỉ khi vừa cần DR cross-vendor, vừa có đội đủ lớn, vừa bị quy định ép thì cloud-agnostic mới xứng đáng.

```text
Bạn cần multi-cloud DR? ──Không──→ Cloud-native là đủ
       │ Có
       ▼
Có đội > 10 kỹ sư platform? ──Không──→ Cloud-portable
       │ Có
       ▼
Có quy định bắt buộc cross-vendor? ──Không──→ Cloud-portable
       │ Có
       ▼
       Cloud-agnostic (multi-cloud đầy đủ)
```

---

## 5️⃣ Case study — Acme Shop migrate AWS → GCP

Lý thuyết RTO/RPO và pattern là một chuyện, va vào thực tế lại là chuyện khác. Phần này theo chân Acme Shop dựng DR site trên GCP sau cú outage 4 giờ ở đầu bài: hành trình 6 tháng, những cú vấp ngoài kế hoạch và con số chi phí thật. Mục đích không phải để học thuộc timeline, mà để thấy một dự án DR cross-cloud trông như thế nào khi triển khai.

### Bối cảnh

- 2023: Acme Shop chạy hoàn toàn trên AWS (EC2 + RDS + S3 + Lambda + DynamoDB).
- 2025: BigQuery cho analytics quá tốt → muốn migrate phần analytics sang GCP.
- 2026: Sau cú outage 4 giờ, chốt dựng DR site trên GCP.

### Lộ trình 6 tháng

Migrate cross-cloud không làm một phát "big bang" mà chia thành các giai đoạn có thể kiểm soát và rollback. Sáu tháng dưới đi từ khảo sát hiện trạng, dựng nền tảng, đồng bộ dữ liệu, chuyển app, định tuyến, tới diễn tập — mỗi tháng đặt nền cho tháng sau.

**Tháng 1 — Khảo sát + Kiểm kê**
- Audit tài nguyên AWS (Terraform import).
- Ánh xạ dịch vụ AWS → dịch vụ tương đương bên GCP.
- Ước tính chi phí dựng GCP.
- Chọn phạm vi: làm DR cho **luồng checkout** trước (Tier 1).

**Tháng 2 — Nền tảng**
- Dựng GCP Org + Folder + Project.
- VPN site-to-site AWS ↔ GCP (Cloud VPN HA + Transit Gateway).
- Cloud Identity Federation: AWS IAM ↔ GCP Workforce Identity.
- Đồng bộ secrets cross-cloud bằng Vault.

**Tháng 3 — Đồng bộ dữ liệu**
- Postgres RDS → Cloud SQL Postgres replica (DMS + WAL).
- S3 → GCS (Storage Transfer Service).
- DynamoDB → Firestore (migrate thủ công — không có ánh xạ 1-1).

**Tháng 4 — Chuyển app**
- Container app: ECR → Artifact Registry.
- EKS workload → GKE Autopilot (Helm chart giữ nguyên — chỉ đổi values).
- Lambda → Cloud Run (viết lại handler, pattern khá tương đồng).

**Tháng 5 — DNS + Định tuyến**
- Cloudflare global LB đứng trước cả 2 cloud.
- Health check + tự động failover.
- Bản ghi DNS trỏ endpoint GCP (canary 10%).

**Tháng 6 — Diễn tập DR + Bàn giao**
- DR drill hàng quý: cắt AWS, xác nhận GCP gánh 100%.
- Viết runbook tài liệu hoá.
- Đào tạo đội vận hành cross-cloud.

### Những cú vấp thực tế

Phần khó nhất của migrate cross-cloud không nằm ở compute mà ở những chỗ hai vendor "không nói cùng ngôn ngữ": mô hình dữ liệu, độ chi tiết của IAM, cách đặt biến môi trường. Bảng dưới là các cú vấp đáng nhớ nhất cùng cách Acme Shop xử lý.

| Cú vấp | Ảnh hưởng | Cách khắc phục |
|---|---|---|
| DynamoDB → Firestore mô hình dữ liệu khác | Phải refactor tầng dữ liệu | Thiết kế lại schema + giai đoạn dual-write |
| IAM policy AWS ≠ độ chi tiết IAM role GCP | Lệch quyền (permission gap) | Ánh xạ thủ công + test |
| Egress cross-cloud AWS→GCP $0.09/GB | Tốn thêm $500/tháng | Cache + chỉ đồng bộ chọn lọc |
| Biến môi trường Lambda vs Cloud Run | Script deploy khác nhau | Hợp nhất bằng Terraform |
| Cert Cloudflare vs ACM vs cert Google-managed | Xoay vòng cert cross-vendor | Dùng Cloudflare cho cả hai (tập trung) |
| Hành vi SDK khác nhau (boto3 vs google-cloud) | Bug khó thấy | Lớp wrapper trừu tượng hoá |

### Sự thật về chi phí

Câu hỏi sống còn của mọi dự án DR: có đáng tiền không? Bảng dưới đối chiếu hoá đơn trước/sau. Điểm mấu chốt nằm ở dòng cuối — chi phí phát sinh phải đặt cạnh thiệt hại mà DR giúp tránh được.

| Khoản | Trước | Sau |
|---|---|---|
| Hoá đơn AWS | $50k/tháng | $35k/tháng (giảm vì đẩy DR checkout sang GCP) |
| Hoá đơn GCP | $0 | $18k/tháng (warm standby) |
| Egress cross-cloud | $0 | $500/tháng |
| **Tổng** | **$50k** | **$53.5k** (+7%) |
| Giá trị chống thiệt hại downtime (ước tính) | $80k/sự cố | Tránh 1 sự cố/năm = tiết kiệm $80k |

→ **Điểm hoà vốn**: chỉ cần tránh được 1 sự cố mỗi năm là đã bù lại phần chi phí tăng thêm.

---

## 6️⃣ Mẫu DR Runbook

Có DR site mà không có *runbook* (kịch bản xử lý) thì lúc sự cố thật mọi người sẽ luống cuống, mỗi người làm một kiểu. Runbook tốt chia thành 4 pha rạch ròi: **Detect** (phát hiện) → **Decide** (quyết định) → **Execute** (thực thi) → **Recover** (khôi phục) — ai cũng biết khi nào bấm nút và bấm nút gì.

### Detect — Tiêu chí kích hoạt

Bước đầu là định nghĩa rõ "thế nào là thảm hoạ" để không failover nhầm vì một trục trặc nhỏ. Ba ngưỡng dưới phải cùng xét để tránh báo động giả.

- AWS `us-east-1` health dashboard: 2+ dịch vụ bị ảnh hưởng > 15 phút.
- Giám sát nội bộ: tỷ lệ lỗi > 5% kéo dài > 5 phút.
- Báo cáo từ khách hàng > 10 trong 5 phút.

### Decide — Ma trận leo thang

Phát hiện rồi thì ai có quyền quyết định failover? Ma trận dưới gán mức độ nghiêm trọng với người ra quyết định và hành động tương ứng, tránh tình trạng "chờ nhau" giữa lúc cháy nhà.

| Mức độ | Người ra quyết định | Hành động |
|---|---|---|
| Sev 1 (sập toàn bộ) | On-call SRE + Engineering manager | Tự động failover |
| Sev 2 (suy giảm) | On-call SRE | Chờ 15p; failover nếu còn kéo dài |
| Sev 3 (1 dịch vụ lẻ) | On-call SRE | Khắc phục tại chỗ; không failover |

### Execute — Các bước failover

Khi đã quyết định failover, đây là chuỗi lệnh thực thi theo đúng thứ tự: xác nhận sự cố → đẩy DB replica lên primary → scale app → chuyển traffic → kiểm chứng → thông báo. Mỗi lệnh phải chạy được sao chép trực tiếp lúc khẩn cấp.

```bash
# 1. Confirm AWS region status
aws health describe-events --region us-east-1

# 2. Promote Cloud SQL replica to primary
gcloud sql instances promote-replica acmeshop-db-replica --quiet

# 3. Scale Cloud Run from min=1 to min=10
gcloud run services update acmeshop-api \
    --min-instances=10 --max-instances=50 \
    --region=asia-southeast1

# 4. Switch Cloudflare LB to GCP origin
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE}/load_balancers/${LB_ID}" \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -d '{"default_pools":["gcp-asia-pool"]}'

# 5. Verify DNS propagation
dig api.acmeshop.io

# 6. Notify customer support + Slack #incidents
```

### Recover — Failback (khôi phục về primary)

Failover chỉ là một nửa câu chuyện. Khi AWS đã hồi phục, phải đưa hệ thống về trạng thái bình thường một cách *từ từ và có kiểm soát* — vội vàng cutover ngược lại dễ gây sự cố lần hai.

Sau khi AWS phục hồi:

1. Đồng bộ dữ liệu GCP → AWS (chiều ngược lại).
2. Test AWS ở chế độ chỉ-đọc.
3. Cutover Cloudflare LB về AWS theo từng nấc (10% → 50% → 100%).
4. Đẩy DB AWS trở lại làm primary.
5. Viết postmortem trong vòng 5 ngày.

### Test — Lịch diễn tập DR

Runbook chỉ có giá trị nếu được tập dượt định kỳ — bằng không, nó là tờ giấy chết. Ba nhịp dưới phủ từ diễn tập đầy đủ tới mô phỏng trên giấy và inject lỗi tự động.

- **Hàng quý**: diễn tập failover đầy đủ, làm ngoài giờ cao điểm.
- **Hàng tháng**: tabletop exercise (diễn tập trên giấy, không động vào hạ tầng).
- **Hàng tuần**: chaos engineering tự động (Gremlin/Litmus).

---

## 7️⃣ FinOps multi-cloud

Chạy 2 cloud nghĩa là 2 hoá đơn, 2 dashboard, 2 cách tính giá — rất dễ "vung tay quá trán" mà không hay. *FinOps* (quản trị chi phí cloud) cho multi-cloud xoay quanh việc nhìn được tổng thể và quy trách nhiệm chi phí về từng đội. Sáu thực hành dưới là bộ khung tối thiểu.

- **Showback**: bóc tách chi phí theo từng đội/dịch vụ, gộp cả hai cloud.
- **Chiến lược gắn tag**: dùng chung một schema cross-cloud (`env`, `team`, `service`, `cost-center`).
- **Công cụ**: CloudHealth, Apptio Cloudability, hoặc bộ native (Cost Explorer + Cloud Billing + Azure Cost Management).
- **Tối ưu egress**: tìm điểm nóng egress cross-cloud rồi giảm hoặc chấp nhận có chủ đích.
- **Cam kết dung lượng (Reserved Capacity)**: AWS RI + GCP CUD + Azure Reserved Instance — cam kết riêng cho từng vendor.
- **Phát hiện bất thường**: cảnh báo dựa trên ML khi chi phí tăng vọt.

---

## 🛠️ Hands-on — Khung Terraform multi-provider

Đến đây ta ráp mọi mảnh lại bằng code. Đoạn Terraform dưới khai báo cùng lúc 3 provider (AWS primary, GCP làm warm standby, Cloudflare làm global LB) trong một stack duy nhất — đúng kiến trúc mà case study đã mô tả. Đây là khung sườn (*skeleton*) để bạn điền module thật vào, không phải bản chạy production ngay.

```hcl
# main.tf
terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
    google = { source = "hashicorp/google", version = "~> 5.0" }
    cloudflare = { source = "cloudflare/cloudflare", version = "~> 4.0" }
  }
  backend "gcs" {
    bucket = "acmeshop-tfstate"
    prefix = "multi-cloud"
  }
}

provider "aws" {
  region = "us-east-1"
}

provider "google" {
  project = "acmeshop-prod"
  region  = "asia-southeast1"
}

provider "cloudflare" {
  api_token = var.cloudflare_token
}

# Module AWS primary
module "aws_primary" {
  source = "./modules/app-aws"
  env    = "prod"
  region = "us-east-1"
}

# Module GCP warm standby
module "gcp_dr" {
  source = "./modules/app-gcp"
  env    = "prod-dr"
  region = "asia-southeast1"
  scale_factor = 0.3  # 30% of prod
}

# Cloudflare LB
resource "cloudflare_load_balancer" "global" {
  zone_id = var.zone_id
  name    = "api.acmeshop.io"

  default_pool_ids = [cloudflare_load_balancer_pool.aws.id]
  fallback_pool_id = cloudflare_load_balancer_pool.gcp.id

  region_pools {
    region   = "WNAM"
    pool_ids = [cloudflare_load_balancer_pool.aws.id]
  }
  region_pools {
    region   = "SEAS"
    pool_ids = [cloudflare_load_balancer_pool.gcp.id]
  }
}
```

### Kiểm thử failover

Khung đã dựng xong thì phải tự tay kéo cầu dao để chắc chắn failover hoạt động — đừng đợi tới sự cố thật mới biết. Đoạn dưới mô phỏng "AWS sập" bằng cách tắt pool AWS trên Cloudflare, rồi kiểm chứng traffic có nhảy sang origin GCP không.

```bash
# Disable AWS pool (simulate region down)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE}/load_balancers/pools/${AWS_POOL_ID}" \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -d '{"enabled": false}'

# Verify traffic shift to GCP
curl -v https://api.acmeshop.io/healthz  # Should hit GCP origin
```

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy 1: DR site dựng xong rồi không bao giờ test

- **Triệu chứng**: Dựng warm standby xong để đó, cả năm không đụng tới; khi thảm hoạ thật ập đến thì DR site đã hỏng từ lúc nào không biết.
- **Nguyên nhân**: Coi DR là việc "dựng một lần xong thôi", không xem nó như hệ thống sống cần bảo trì.
- **Cách tránh**: DR drill hàng quý bắt buộc, ghi lại tỷ lệ thất bại từng lần để cải thiện.

### ❌ Cạm bẫy 2: Không giám sát độ trễ đồng bộ dữ liệu

- **Triệu chứng**: Postgres replication lag tới 30 phút mà không có cảnh báo → RPO thực tế thành 30 phút thay vì 1 phút như cam kết.
- **Nguyên nhân**: Chỉ giám sát "replica còn sống không", không giám sát "replica trễ bao nhiêu".
- **Cách tránh**: Cảnh báo khi replication lag vượt ngưỡng RPO mục tiêu.

### ❌ Cạm bẫy 3: DNS TTL đặt quá cao

- **Triệu chứng**: TTL 24h → khi failover, DNS mất tới 24h để lan truyền → người dùng vẫn bị trỏ vào site đã chết.
- **Nguyên nhân**: Để TTL mặc định cao, không tính tới kịch bản phải đổi endpoint gấp.
- **Cách tránh**: Đặt TTL 60s cho các bản ghi trọng yếu. (Đánh đổi: số lượng truy vấn DNS nhiều hơn, chi phí nhích lên.)

### ❌ Cạm bẫy 4: Lệch quyền cross-cloud

- **Triệu chứng**: Đội quen vận hành AWS, không có quyền truy cập GCP → đúng lúc failover lại không thao tác được trên GCP.
- **Nguyên nhân**: Quyền truy cập hai cloud cấp rời rạc, không liên thông.
- **Cách tránh**: IAM federation cross-cloud; người on-call phải có quyền trên cả hai cloud.

### ❌ Cạm bẫy 5: Theo dõi chi phí trên 2 dashboard tách rời

- **Triệu chứng**: Mỗi cloud xem một nơi → không ai nắm được con số tổng.
- **Nguyên nhân**: Thiếu một lớp gộp chi phí chung cho cả hai vendor.
- **Cách tránh**: Dùng công cụ quản trị chi phí hợp nhất (Vantage, Cloudability) hoặc một dashboard Looker kéo dữ liệu cả hai cloud.

### ❌ Cạm bẫy 6: Config app khác nhau giữa các cloud

- **Triệu chứng**: Biến môi trường trên Lambda khác trên Cloud Run → sinh bug khó thấy khi failover.
- **Nguyên nhân**: Cấu hình được quản lý riêng từng cloud, không có nguồn chân lý chung.
- **Cách tránh**: Quản lý config qua Vault/External Secrets — một nguồn chân lý duy nhất (*single source of truth*).

### ❌ Cạm bẫy 7: Hứa RTO cao hơn năng lực thực tế

- **Triệu chứng**: Cam kết RTO 5 phút nhưng thực tế chỉ dựng pilot light (RTO ~30 phút).
- **Nguyên nhân**: Đặt cam kết theo mong muốn, không đo bằng diễn tập thật.
- **Cách tránh**: Đo RTO thật qua DR drill; rồi hoặc điều chỉnh cam kết, hoặc nâng cấp pattern cho khớp.

### ❌ Cạm bẫy 8: Có backup nhưng chưa từng thử restore

- **Triệu chứng**: Backup chạy đều đặn nhưng chưa bao giờ restore thử; tới lúc cần thật mới phát hiện backup đã hỏng.
- **Nguyên nhân**: Nhầm "đã backup" với "đã có khả năng khôi phục".
- **Cách tránh**: Test restore hàng tháng vào môi trường sandbox.

### ✅ Best practice 1: Coi DR là hệ thống sống, tập dượt định kỳ

- Lên lịch drill cố định (quý/tháng/tuần như mục 6) và đối xử với nó như một SLA nội bộ.
- Sau mỗi drill ghi lại RTO/RPO đo được thực tế, so với mục tiêu rồi điều chỉnh.

### ✅ Best practice 2: Một nguồn chân lý cho config và secrets

- Mọi biến môi trường, credential, cấu hình đi qua Vault/External Secrets — không hardcode riêng từng cloud.
- Nhờ vậy app trên AWS và GCP hành xử giống nhau, giảm hẳn bug "chạy ở đây nhưng không chạy ở kia".

### ✅ Best practice 3: Nhìn chi phí và độ trễ trên một bảng duy nhất

- Gộp hoá đơn hai cloud về một dashboard, gắn tag chung schema để bóc tách theo đội/dịch vụ.
- Cảnh báo sớm trên cả chi phí (cost spike) lẫn replication lag — hai con số quyết định DR có "thật" hay không.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Cổng checkout của Acme Shop chấp nhận downtime 30 phút và mất tối đa 5 phút dữ liệu. RTO và RPO là bao nhiêu, và nó thuộc tier nào?

<details>
<summary>💡 Đáp án</summary>

- **RTO = 30 phút** (thời gian tối đa được phép offline) và **RPO = 5 phút** (lượng dữ liệu tối đa được phép mất).
- Với RTO 15-30 phút và RPO < 5 phút, checkout rơi vào **Tier 1** (dịch vụ kinh doanh trọng yếu).
- Pattern phù hợp: **Warm Standby** (RTO 1-15 phút, RPO < 1 phút) — dư sức đáp ứng và vẫn rẻ hơn Active-Active.

</details>

**Q2.** So sánh nhanh 4 DR pattern theo RTO / RPO / chi phí. Pattern nào "rẻ nhất" và pattern nào "nhanh nhất"?

<details>
<summary>💡 Đáp án</summary>

| Pattern | RTO | RPO | Chi phí (% prod) |
|---|---|---|---|
| Backup-Restore | hàng giờ - hàng ngày | hàng giờ | 5-10% |
| Pilot Light | 10-60p | vài giây | 15-25% |
| Warm Standby | 1-15p | < 1p | 30-50% |
| Active-Active | < 1p | 0 - vài giây | 100-150% |

- **Rẻ nhất**: Backup-Restore (chỉ trả tiền lưu trữ).
- **Nhanh nhất**: Active-Active (< 1 phút, gần như không gián đoạn) — nhưng đắt nhất.
- Quy luật: kéo RTO/RPO xuống thì chi phí và độ phức tạp kéo lên.

</details>

**Q3.** Khi nào nên dùng multi-cloud DR thay vì single-cloud multi-region?

<details>
<summary>💡 Đáp án</summary>

Chỉ khi:
1. Cần chống **sự cố toàn vendor** (cả AWS sập toàn cầu), không chỉ 1 region.
2. **Quy định bắt buộc** data nằm ở 2 vendor khác nhau (chủ quyền dữ liệu).

Còn lại, single-cloud multi-region là mặc định vì rẻ hơn, đồng bộ native và dễ test hơn. Theo Gartner 2025: 89% doanh nghiệp dùng multi-cloud nhưng chỉ 12% thực sự có multi-cloud DR — phần lớn dùng multi-cloud để chọn dịch vụ tốt nhất từng mảng, không phải để DR.

</details>

**Q4.** Một đội 5 dev, single-cloud, chưa có kế hoạch DR multi-cloud. Nên chọn pattern kiến trúc nào trong 3 pattern (cloud-native / cloud-portable / cloud-agnostic)?

<details>
<summary>💡 Đáp án</summary>

- Chọn **Cloud-native**. Theo cây quyết định: không cần multi-cloud DR → cloud-native là đủ.
- Đội 5 người không kham nổi độ phức tạp của cloud-agnostic (cần đội platform > 10 kỹ sư) và cũng chưa cần cloud-portable nếu chưa có exit strategy.
- Đổi lại sự gắn chặt vendor, họ được tốc độ phát triển cao nhất — đúng thứ một đội nhỏ cần.

</details>

**Q5.** DR site cấu hình RPO mục tiêu 1 phút, nhưng Postgres replication lag thực tế đang là 30 phút và không ai biết. RPO thực tế là bao nhiêu, và sửa thế nào?

<details>
<summary>💡 Đáp án</summary>

- **RPO thực tế = 30 phút**, không phải 1 phút. RPO bị quyết định bởi độ trễ replica thực tế chứ không phải con số cấu hình trên giấy.
- Sửa: bật **cảnh báo khi replication lag vượt ngưỡng RPO mục tiêu**. Đây là cạm bẫy "không giám sát độ trễ đồng bộ" — replica còn sống không có nghĩa là dữ liệu còn kịp.

</details>

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| RTO | Mục tiêu thời gian khôi phục | Bao lâu mới online lại sau thảm hoạ (Recovery Time Objective) |
| RPO | Mục tiêu điểm khôi phục | Mất tối đa bao nhiêu dữ liệu (Recovery Point Objective) |
| SLA | Cam kết mức dịch vụ | Lời hứa uptime với khách hàng (Service Level Agreement) |
| SLO | Mục tiêu mức dịch vụ | Mục tiêu nội bộ, thường khắt khe hơn SLA |
| DR drill | Diễn tập khôi phục thảm hoạ | Tập failover định kỳ để kiểm chứng DR site |
| Backup-Restore | Sao lưu - khôi phục | DR pattern lạnh, dựng lại từ backup khi sự cố |
| Pilot Light | Đèn chờ | DB luôn đồng bộ, app server để sẵn image nhưng scale về 0 |
| Warm Standby | Dự phòng ấm | Chạy đủ stack ở quy mô thu nhỏ, sự cố thì scale up |
| Active-Active | Song song chủ động | Cả 2 region cùng phục vụ traffic thật |
| Failover | Chuyển dự phòng | Cutover từ site primary sang site DR |
| Failback | Chuyển về primary | Cutover ngược về sau khi primary phục hồi |
| Cloud-native | Bám sát vendor | Tận dụng tối đa dịch vụ đặc thù của một vendor |
| Cloud-portable | Di chuyển được | Dựa trên chuẩn mở, migrate được khi cần |
| Cloud-agnostic | Trung lập vendor | Chạy multi-cloud đồng thời qua lớp abstraction |
| Tabletop exercise | Diễn tập trên giấy | Đi qua kịch bản DR chỉ trên giấy, không động vào hạ tầng |
| Chaos engineering | Kỹ thuật hỗn loạn | Chủ động inject lỗi để kiểm tra khả năng chống chịu |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Kubernetes Multi-cloud — Anthos, Azure Arc, Cluster API, Service Mesh](03_kubernetes-multi-cloud-and-anthos-arc.md)
- ↑ **Về cụm:** [Multi-cloud Strategies](../../README.md)
- 🧭 **Tấm bản đồ sự nghiệp:** [Cloud Engineer Career Roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS](../../../aws/) — cloud primary trong case study
- ☁️ [GCP](../../../gcp/) — DR site trong case study
- 💰 [Cloud Cost Management](../../../cloud-cost-management/) — đào sâu FinOps cross-cloud
- 🏗️ [IaC với Terraform](../../../../10_devops/iac/) — quản lý hạ tầng multi-provider
- ↑ **Về cụm:** [Kubernetes intermediate](../../../../10_devops/kubernetes/lessons/02_intermediate/) — multi-cluster
- 📊 [SRE practices](../../../../10_devops/observability/lessons/02_intermediate/04_sre-practices.md) — RTO/RPO, error budget

### 🌐 Tài nguyên tham khảo khác

- [AWS Disaster Recovery Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html) — 4 DR pattern từ chính AWS.
- [GCP DR Planning Guide](https://cloud.google.com/architecture/dr-scenarios-planning-guide) — khung lập kế hoạch DR của Google.
- [Azure DR Architecture](https://learn.microsoft.com/azure/architecture/resiliency/disaster-recovery-azure-applications) — góc nhìn DR phía Azure.
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — nền tảng về SLA/SLO/RTO/RPO.
- [Crossplane](https://www.crossplane.io/) — control plane multi-cloud.
- [Cloudflare Load Balancing](https://www.cloudflare.com/load-balancing/) — global LB + failover.
- [Gremlin](https://www.gremlin.com/) — nền tảng chaos engineering.
- [Litmus Chaos](https://litmuschaos.io/) — chaos engineering cho Kubernetes.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) Multi-cloud. RTO/RPO + 4 DR pattern + multi-cloud DR vs multi-region + 3 architecture pattern (native/portable/agnostic) + case study AWS→GCP migration 6 tháng + DR runbook template + FinOps multi-cloud + hands-on Terraform multi-provider + 8 pitfalls. Hoàn thành Multi-cloud-strategies basic cluster.
- **v1.1.0 (01/06/2026)** — Việt hoá narrative các bảng/section còn ở dạng điện tín (RTO/RPO, 4 DR pattern, multi-cloud vs multi-region, 3 architecture pattern, case study, runbook, FinOps); thêm lời dẫn trước và câu phân tích sau mỗi bảng/diagram; thêm ngôn ngữ `text` cho các fence ASCII diagram. Chuẩn hoá khung framework: đổi field `Prerequisites` → `Yêu cầu trước` (link text = tiêu đề thực), Glossary sang 3 cột `EN | VN | Giải thích`, Pitfall sang định dạng `❌ Cạm bẫy N` (Triệu chứng/Nguyên nhân/Cách tránh) + 3 `✅ Best practice`, Self-check sang 5 câu Q&A có `<details>` đáp án, nav sang marker `⬅️/↑` + 3 sub-heading chuẩn. Sửa domain `acmeshop.vn` → `acmeshop.io` (3 chỗ) cho nhất quán toàn cụm.
