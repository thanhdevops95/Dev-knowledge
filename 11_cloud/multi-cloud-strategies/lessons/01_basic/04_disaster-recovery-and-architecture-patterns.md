# 🆘 Multi-cloud — Disaster Recovery + Architecture Patterns

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [03_kubernetes-multi-cloud-and-anthos-arc](03_kubernetes-multi-cloud-and-anthos-arc.md) ✅

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

🪞 **Ẩn dụ**: *RTO/RPO như **2 chỉ số bác sĩ cấp cứu**: RTO = "bao lâu để hồi sức tỉnh lại" (downtime acceptable), RPO = "bao nhiêu phút trí nhớ bệnh nhân được phép mất" (data loss acceptable). Số càng nhỏ → giường bệnh càng đắt.*

| Term | Câu hỏi | Đo lường | Ví dụ |
|---|---|---|---|
| **RTO** | Bao lâu mới online trở lại sau disaster? | Thời gian | RTO = 1h: có thể chịu 1 giờ downtime |
| **RPO** | Mất tối đa bao nhiêu data? | Thời gian (last backup point) | RPO = 5p: chấp nhận mất 5 phút giao dịch |
| **SLA** | Promise uptime với customer | % uptime | 99.9% = ~8.76h downtime/năm |
| **SLO** | Internal target (thường strict hơn SLA) | % | 99.95% |

### Tier theo critical level

| Tier | Description | Typical RTO | Typical RPO | DR pattern |
|---|---|---|---|---|
| Tier 0 | Mission-critical (banking, healthcare) | < 1 phút | 0 (zero data loss) | Active-Active multi-region |
| Tier 1 | Critical biz (e-commerce checkout) | < 15 phút | < 5 phút | Warm Standby hoặc Active-Active |
| Tier 2 | Important (catalog, analytics) | < 4 giờ | < 1 giờ | Pilot Light |
| Tier 3 | Internal tools (admin, BI) | < 24 giờ | < 24 giờ | Backup-Restore |

→ Acme Shop checkout = Tier 1 (RTO 15p, RPO 5p) → Warm Standby là phù hợp.

---

## 2️⃣ 4 DR Patterns

### Pattern 1 — Backup-Restore (cold)

```
Production (cloud A)              DR site (cloud B / region B)
  ↓ daily snapshot
  └→ S3 / GCS                     [empty]
```

- DR site **chưa có gì** chạy.
- Khi disaster: restore từ backup, provision infra mới.
- **RTO**: hours to days. **RPO**: hours (last backup).
- **Cost**: cheapest (chỉ trả storage backup).

→ Phù hợp **Tier 3** (analytics, internal tool).

### Pattern 2 — Pilot Light

```
Production (A)                    DR site (B)
  All workload running            Core systems "đèn pilot" — DB replica streaming
                                  App servers: scaled to 0 (image ready)
```

- Database **đang replicate live** sang DR site (read replica / streaming).
- App servers chuẩn bị (AMI / container image) nhưng **không chạy**.
- Khi disaster: scale up app + cutover DNS.
- **RTO**: 10-60 phút. **RPO**: vài giây (replica lag).
- **Cost**: medium (trả DB always-on + storage).

→ Phù hợp **Tier 2**.

### Pattern 3 — Warm Standby

```
Production (A)                    DR site (B)
  Full workload                   Same workload — scaled DOWN (1 instance instead of 10)
```

- DR site **chạy full stack** ở quy mô nhỏ (1 instance per service).
- DB streaming replication.
- Khi disaster: scale up + redirect traffic.
- **RTO**: 1-15 phút. **RPO**: < 1 phút.
- **Cost**: high (trả ~30-50% full prod).

→ Phù hợp **Tier 1**. Acme Shop checkout.

### Pattern 4 — Multi-region Active-Active (hot)

```
Production region A ←──────────→ Production region B
  Load balancer global routes traffic to nearest
  Both serve real users; DB multi-master or replicated
```

- Cả 2 region đang serve traffic real.
- Global LB (Cloudflare, AWS Global Accelerator, GCP Global LB) route theo latency.
- DB: multi-master (Spanner, CockroachDB, Cassandra) hoặc replicated với failover.
- **RTO**: < 1 phút. **RPO**: 0 (nếu strong consistency) hoặc seconds (eventual).
- **Cost**: highest (2x infra + global LB + cross-region data transfer).

→ Phù hợp **Tier 0** (banking, healthcare, large e-commerce).

### Comparison table

| Pattern | RTO | RPO | Cost (% prod) | Complexity ops |
|---|---|---|---|---|
| Backup-Restore | hours-days | hours | 5-10% | Low |
| Pilot Light | 10-60p | seconds | 15-25% | Medium |
| Warm Standby | 1-15p | < 1p | 30-50% | Medium-High |
| Active-Active | < 1p | 0-seconds | 100-150% | Very High |

---

## 3️⃣ Multi-cloud DR vs Single-cloud Multi-region

🪞 **Ẩn dụ**: *Single-cloud multi-region như **2 chi nhánh ngân hàng cùng tập đoàn** — chia sẻ chính sách, hệ thống; nếu tập đoàn hỏng cả 2 cùng hỏng. Multi-cloud DR như **gửi tiền ở 2 ngân hàng khác nhau** — chống cả "tập đoàn hỏng" nhưng quy trình giao dịch khác nhau, mệt hơn.*

### Khi nào multi-cloud DR

| Lý do | Phù hợp multi-cloud DR? |
|---|---|
| Vendor-wide outage (AWS toàn cầu) | ✅ Multi-cloud chống được |
| Region outage AWS us-east-1 | ❌ Single-cloud multi-region đủ |
| Regulatory: data phải ở 2 vendor khác nhau (EU sovereignty) | ✅ Multi-cloud bắt buộc |
| Best-of-breed (BigQuery + S3) | ✅ But complexity tăng |
| Vendor lock concern | ✅ Có exit plan |
| RTO < 5 phút + budget limited | ❌ Multi-cloud quá phức tạp; multi-region rẻ + đủ |

### Trade-off

| Aspect | Single-cloud multi-region | Multi-cloud DR |
|---|---|---|
| Vendor outage protection | Region-level only | Vendor-wide ✅ |
| Setup complexity | Medium | Very High |
| Cost (network egress between sites) | Cross-region within cloud (cheap) | Cross-cloud egress (expensive) |
| Service parity | Identical (same AWS services) | Different (Lambda vs Cloud Run) |
| Team skill | 1 cloud expertise | 2 cloud expertise |
| Operational tooling | 1 set | 2 set (or abstraction layer) |
| Data sync | Native (cross-region replica) | Manual/3rd-party (cross-cloud) |
| Failover testing | Easier | Harder |

### Reality check 2026

Theo Gartner 2025 survey:
- **89% enterprise multi-cloud** — nhưng chỉ **12% có true multi-cloud DR**.
- Còn lại multi-cloud cho **best-of-breed** (BigQuery for analytics, AWS for compute), không phải DR.
- **Recommendation**: Single-cloud multi-region cho DR là default. Multi-cloud DR chỉ khi RTO + regulatory yêu cầu mạnh.

---

## 4️⃣ Architecture patterns — Cloud-agnostic / Cloud-portable / Cloud-native

### Pattern A — Cloud-native (lock-in chấp nhận)

```
App dùng:
- AWS Lambda + DynamoDB + S3 + SQS + Cognito
- Hoàn toàn AWS-specific
```

**Pros**: Tận dụng managed service mạnh, dev velocity cao.
**Cons**: Migration cực khó.
**Khi chọn**: startup, single-cloud strategy, không có DR plan multi-cloud.

### Pattern B — Cloud-portable (1-cloud-at-a-time)

```
App dùng:
- Kubernetes (GKE / EKS / AKS) — portable layer
- Postgres (RDS / Cloud SQL / Azure DB)
- S3-compatible storage (S3 / GCS / R2)
- Open standards (OAuth, JWT, OpenAPI)
```

**Pros**: Migration possible, không chạy đồng thời.
**Cons**: Bỏ qua một số managed feature.
**Khi chọn**: medium-large company, có DR plan, exit strategy quan trọng.

### Pattern C — Cloud-agnostic (multi-cloud đồng thời)

```
App dùng:
- Crossplane / Terraform (abstraction layer)
- K8s + Istio multi-cluster
- Vault / ESO secrets cross-cloud
- 3rd-party DB (Snowflake, MongoDB Atlas)
- Cloudflare for edge + traffic routing
```

**Pros**: Vendor-neutral, true portability.
**Cons**: Complexity rất cao, ops team lớn, dev velocity chậm hơn 30-50%.
**Khi chọn**: enterprise tier-0, regulatory mạnh, có team platform > 10 engineer.

### Decision framework

```
Bạn cần multi-cloud DR? ──No──→ Cloud-native OK
       │ Yes
       ▼
Bạn có team > 10 platform engineer? ──No──→ Cloud-portable
       │ Yes
       ▼
Bạn có regulatory mandate cross-vendor? ──No──→ Cloud-portable
       │ Yes
       ▼
       Cloud-agnostic (full multi-cloud)
```

---

## 5️⃣ Case study — Acme Shop migrate AWS → GCP

### Background

- 2023: Acme Shop full AWS (EC2 + RDS + S3 + Lambda + DynamoDB).
- 2025: BigQuery cho analytics quá tốt → muốn migrate analytics sang GCP.
- 2026: Sau outage 4h, decide DR site trên GCP.

### Timeline 6 tháng

**Month 1 — Discovery + Inventory**
- Audit AWS resources (Terraform import).
- Map AWS services → GCP equivalent.
- Cost estimate GCP setup.
- Pick scope: DR cho **checkout flow** trước (Tier 1).

**Month 2 — Foundation**
- GCP Org + Folder + Project setup.
- VPN site-to-site AWS ↔ GCP (Cloud VPN HA + Transit Gateway).
- Cloud Identity Federation: AWS IAM ↔ GCP Workforce Identity.
- Vault cross-cloud secrets.

**Month 3 — Data sync**
- Postgres RDS → Cloud SQL Postgres replica (DMS + WAL).
- S3 → GCS sync (Storage Transfer Service).
- DynamoDB → Firestore (custom migration — không có 1-1 mapping).

**Month 4 — App migration**
- Container app: ECR → Artifact Registry.
- EKS workload → GKE Autopilot (Helm chart same — chỉ change values).
- Lambda → Cloud Run (rewrite handler, OK pattern khá tương đồng).

**Month 5 — DNS + Routing**
- Cloudflare global LB front cả 2 cloud.
- Health check + automatic failover.
- DNS record GCP endpoint (weight 10% canary).

**Month 6 — DR drill + handover**
- Quarterly DR drill: cut AWS, verify GCP serves 100%.
- Documentation runbook.
- Team train cross-cloud ops.

### Gotcha thực tế

| Gotcha | Impact | Mitigation |
|---|---|---|
| DynamoDB → Firestore data model khác | Refactor data layer | Schema redesign + dual-write period |
| AWS IAM policy ≠ GCP IAM role granularity | Permission gap | Manual mapping + test |
| Cross-cloud egress AWS→GCP $0.09/GB | $500/tháng extra | Cache + selective sync |
| Lambda env vars vs Cloud Run env vars | Deploy script khác | Terraform unified |
| Cloudflare cert vs ACM vs Google-managed cert | Cert rotation cross-vendor | Use Cloudflare for both (centralized) |
| Different SDK behavior (boto3 vs google-cloud) | Bug subtle | Wrapper abstraction layer |

### Cost reality

| | Trước | Sau |
|---|---|---|
| AWS bill | $50k/tháng | $35k/tháng (giảm vì offload checkout DR sang GCP) |
| GCP bill | $0 | $18k/tháng (warm standby) |
| Cross-cloud egress | $0 | $500/tháng |
| **Total** | **$50k** | **$53.5k** (+7%) |
| Downtime cost protection (estimate) | $80k/incident | Eliminate 1 incident/năm = save $80k |

→ **Break-even**: 1 incident avoided/năm covers extra cost.

---

## 6️⃣ DR Runbook template

### Detect — Trigger criteria

- AWS `us-east-1` health dashboard: 2+ services impacted > 15 phút.
- Internal monitoring: error rate > 5% sustained > 5 phút.
- Customer report > 10 in 5 phút.

### Decide — Escalation matrix

| Severity | Decision authority | Action |
|---|---|---|
| Sev 1 (full outage) | On-call SRE + Engineering manager | Auto-failover |
| Sev 2 (degraded) | On-call SRE | Wait 15p; failover if persists |
| Sev 3 (single service) | On-call SRE | Local mitigation; no failover |

### Execute — Failover steps

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
dig api.acmeshop.vn

# 6. Notify customer support + Slack #incidents
```

### Recover — Failback

After AWS recovers:
1. Sync data GCP → AWS (reverse direction).
2. Test AWS read-only.
3. Cutover Cloudflare LB back (gradual: 10% → 50% → 100%).
4. Promote AWS DB back to primary.
5. Postmortem within 5 ngày.

### Test — DR drill schedule

- **Quarterly**: full failover drill, ngoài giờ.
- **Monthly**: tabletop exercise (paper walkthrough).
- **Weekly**: automated chaos engineering (Gremlin/Litmus).

---

## 7️⃣ FinOps multi-cloud

- **Showback**: cost per team/service breakdown, both clouds.
- **Tagging strategy**: cùng schema cross-cloud (`env`, `team`, `service`, `cost-center`).
- **Tool**: CloudHealth, Apptio Cloudability, native Cost Explorer + Cloud Billing + Azure Cost Management.
- **Egress optimization**: identify cross-cloud egress hot spot; reduce or accept.
- **Reserved Capacity**: AWS RI + GCP CUD + Azure Reserved Instance — commit separately per vendor.
- **Anomaly detection**: ML-based alert khi cost spike.

---

## 🛠️ Hands-on — Terraform multi-provider skeleton

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
  name    = "api.acmeshop.vn"

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

### Test failover

```bash
# Disable AWS pool (simulate region down)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE}/load_balancers/pools/${AWS_POOL_ID}" \
    -H "Authorization: Bearer ${CF_TOKEN}" \
    -d '{"enabled": false}'

# Verify traffic shift to GCP
curl -v https://api.acmeshop.vn/healthz  # Should hit GCP origin
```

---

## ⚠️ Pitfalls

### 1. DR site không bao giờ test

**Bẫy**: Setup warm standby xong, không test 1 năm → khi disaster thật → DR site broken.

**Fix**: Quarterly DR drill bắt buộc. Document failure rate.

### 2. Data sync lag không monitor

**Bẫy**: Postgres replication lag 30 phút mà không alert → RPO thực tế 30 phút thay vì 1 phút.

**Fix**: Alert on replication lag > target RPO.

### 3. DNS TTL quá cao

**Bẫy**: TTL 24h → failover DNS mất 24h propagate → user vẫn vào dead site.

**Fix**: TTL 60s cho critical record. (Trade-off: nhiều DNS query cost ↑.)

### 4. Permission gap cross-cloud

**Bẫy**: Team operate AWS, không có access GCP → khi failover không operate được.

**Fix**: Cross-cloud IAM federation; on-call có quyền cả 2.

### 5. Cost tracking 2 dashboard riêng

**Bẫy**: Mỗi cloud xem riêng → không biết tổng.

**Fix**: Cost mgmt tool unified (Vantage, Cloudability) hoặc Looker dashboard pull cả 2.

### 6. App config khác giữa cloud

**Bẫy**: Lambda env var khác Cloud Run env var → bug subtle.

**Fix**: Config qua Vault/External Secrets — same source of truth.

### 7. RTO promise > thực tế

**Bẫy**: Hứa RTO 5 phút mà setup chỉ pilot light (RTO 30p).

**Fix**: Đo thực tế DR drill; điều chỉnh promise hoặc upgrade pattern.

### 8. Forget backup test restore

**Bẫy**: Có backup, không bao giờ thử restore → khi cần thật → backup corrupted.

**Fix**: Monthly restore test vào sandbox env.

---

## 🎯 Self-check

- [ ] Định nghĩa RTO + RPO cho Acme Shop checkout?
- [ ] 4 DR patterns + RTO/RPO/Cost compare?
- [ ] Khi nào multi-cloud DR vs multi-region cùng cloud?
- [ ] Cloud-native vs portable vs agnostic — chọn cho team 5 dev?
- [ ] Viết runbook failover step-by-step?
- [ ] Test plan DR drill quarterly?
- [ ] Terraform multi-provider AWS + GCP + Cloudflare?
- [ ] FinOps multi-cloud — 3 tactic giảm cost?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **RTO** | Recovery Time Objective — bao lâu mới online lại |
| **RPO** | Recovery Point Objective — mất tối đa bao nhiêu data |
| **SLA** | Service Level Agreement — promise external |
| **SLO** | Service Level Objective — target internal |
| **DR drill** | Test failover periodic |
| **Backup-Restore** | DR pattern cold, restore from backup |
| **Pilot Light** | Core systems on, app scaled to 0 |
| **Warm Standby** | Full stack at smaller scale |
| **Active-Active** | Both regions serve real traffic |
| **Failover** | Cutover từ primary → DR |
| **Failback** | Cutover lại sau primary recovered |
| **Cloud-native** | Tận dụng tối đa vendor-specific service |
| **Cloud-portable** | Standards-based, có thể migrate khi cần |
| **Cloud-agnostic** | Multi-cloud đồng thời, abstraction layer |
| **Tabletop exercise** | DR walkthrough paper-only, không touch infra |
| **Chaos engineering** | Tự inject failure để test resilience |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [03_kubernetes-multi-cloud-and-anthos-arc](03_kubernetes-multi-cloud-and-anthos-arc.md)
- ↑ Cluster Multi-cloud: [Multi-cloud README](../../README.md)

### Cross-reference
- ☁️ [AWS basic](../../../aws/) — primary cloud
- ☁️ [GCP basic](../../../gcp/) — DR site
- 💰 [Cloud Cost Management](../../../cloud-cost-management/)
- 🏗️ [IaC Terraform](../../../../10_devops/iac/)
- ☸️ [Kubernetes intermediate](../../../../10_devops/kubernetes/lessons/02_intermediate/) — multi-cluster
- 📊 [Observability SRE practices](../../../../10_devops/observability/lessons/02_intermediate/04_sre-practices.md)

### Tài nguyên ngoài (2026)
- 📖 [AWS Disaster Recovery Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
- 📖 [GCP DR Planning Guide](https://cloud.google.com/architecture/dr-scenarios-planning-guide)
- 📖 [Azure DR Architecture](https://learn.microsoft.com/azure/architecture/resiliency/disaster-recovery-azure-applications)
- 📖 [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- 📖 [Crossplane](https://www.crossplane.io/) — control plane multi-cloud
- 📖 [Cloudflare Load Balancing](https://www.cloudflare.com/load-balancing/)
- 📖 [Gremlin chaos engineering](https://www.gremlin.com/)
- 📖 [Litmus Chaos](https://litmuschaos.io/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) Multi-cloud. RTO/RPO + 4 DR pattern + multi-cloud DR vs multi-region + 3 architecture pattern (native/portable/agnostic) + case study AWS→GCP migration 6 tháng + DR runbook template + FinOps multi-cloud + hands-on Terraform multi-provider + 8 pitfalls. Hoàn thành Multi-cloud-strategies basic cluster.
