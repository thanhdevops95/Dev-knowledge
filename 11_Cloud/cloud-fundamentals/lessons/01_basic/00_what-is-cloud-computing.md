# 🎓 Cloud computing là gì? — IaaS / PaaS / SaaS + landscape 2026

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** Hiểu cơ bản server/network (xem [Networking basics](../../../../05_Networking/))

> 🎯 *Bài đầu tiên `11_Cloud/`. Hiểu **cloud là gì** (không phải "máy ai đó"), 3 service model **IaaS/PaaS/SaaS**, 3 deployment model **public/private/hybrid**, history 1999-2026, vendor landscape (AWS/GCP/Azure/others), khi nào cloud vs on-prem.*

## 🎯 Sau bài này bạn sẽ

- [ ] Định nghĩa **cloud computing** chuẩn NIST
- [ ] Phân biệt **IaaS / PaaS / SaaS** + ví dụ thực tế
- [ ] Hiểu **public / private / hybrid / multi-cloud**
- [ ] Lịch sử cloud: AWS 2006 → 2026 dominance
- [ ] So sánh **AWS / GCP / Azure / DigitalOcean / Cloudflare / Vercel**
- [ ] Khi nào **cloud** vs **on-prem** vs **hybrid**
- [ ] Cost model: pay-as-you-go vs reserved vs spot

---

## Tình huống — Startup chuyển từ VPS sang AWS lý do gì?

Bạn dev backend FastAPI. Hosting:
- **Year 1**: 1 VPS DigitalOcean $10/month. App chạy ngon.
- **Year 2**: traffic tăng 5x. Add 3 VPS, manual load balance.
- **Year 3**: traffic spike weekend 10x. Add 5 VPS, only Saturday-Sunday — pay 7 days but use 2.
- **Year 4**: DB backup manual. Disaster recovery? Reboot only.
- **Year 5**: customer compliance (SOC2, GDPR). VPS không có audit log + encryption-at-rest documented.

CEO: *"Move to AWS. Pay per usage, scale auto, compliance built-in."*

→ Cloud giải quyết: **elastic capacity + managed services + compliance + pay-as-you-go**.

Nhưng cloud không miễn phí. AWS bill có thể 10x VPS nếu setup sai.

→ Bài này dạy cloud concept để decide đúng.

---

## 1️⃣ Cloud computing là gì? — Định nghĩa NIST

**NIST definition** (2011, still relevant 2026):
> Cloud computing là model cho **on-demand network access** đến **shared pool** của **configurable computing resources** (servers, storage, networks, applications) — provisioned + released **với minimal management effort**.

5 **essential characteristics**:

1. **On-demand self-service**: tạo VM / database không cần human approval.
2. **Broad network access**: access qua Internet/private network từ anywhere.
3. **Resource pooling**: vendor share underlying physical hardware giữa nhiều tenants.
4. **Rapid elasticity**: scale up/down theo demand.
5. **Measured service**: pay per usage (CPU-hour, GB-month, request-count).

🪞 **Ẩn dụ**: *Cloud như **điện lưới quốc gia** — bạn không tự xây nhà máy điện. Plug ổ cắm, dùng bao nhiêu trả bấy nhiêu. Hết dùng = tắt. Cần thêm = scale.*

### "The cloud is just someone else's computer" — đúng hay sai?

Half-truth. Yes, AWS data centers = "computers". NHƯNG cloud ≠ just computers. Khác biệt:
- **Self-service API** (vs ticket-based VPS).
- **Massive scale** (millions of servers, geographic distribution).
- **Managed services** layer (S3, Lambda, RDS — not just VMs).
- **Economies of scale**: AWS buy hardware bulk, pass savings to you.

→ Cloud = **infrastructure as software**.

---

## 2️⃣ 3 Service models — IaaS / PaaS / SaaS

### IaaS — Infrastructure as a Service

**You manage**: OS, runtime, middleware, application, data.
**Vendor manages**: hardware, virtualization, network, datacenter.

**Examples**:
- **AWS EC2** — virtual machines.
- **AWS EBS** — block storage.
- **AWS VPC** — virtual network.
- **GCP Compute Engine**.
- **Azure VMs**.

**You'd say**: *"Give me a Linux VM with 4 CPU, 16GB RAM."*

```bash
# AWS EC2 launch
aws ec2 run-instances --image-id ami-... --instance-type t3.xlarge
# → You get SSH access to a fresh Ubuntu VM. You install everything.
```

**Pros**: max control, similar to on-prem mental model.
**Cons**: still ops work (patch OS, configure DB, etc.).

### PaaS — Platform as a Service

**You manage**: application, data.
**Vendor manages**: runtime, middleware, OS, hardware, etc.

**Examples**:
- **AWS Elastic Beanstalk** — deploy app, vendor runs servers.
- **GCP App Engine** — serverless app platform.
- **Azure App Service**.
- **Heroku** (classic PaaS).
- **Vercel**, **Netlify** — frontend PaaS.
- **Render** — modern PaaS.

**You'd say**: *"Here's my Node.js app, deploy it."*

```bash
# Heroku deploy
git push heroku main
# → Vendor builds, runs Node.js app, manages scaling, load balancer, DB.
```

**Pros**: focus on code, no ops.
**Cons**: less control (vendor's runtime version, limited customization), can lock-in.

### SaaS — Software as a Service

**You manage**: data (config, content).
**Vendor manages**: everything else — application + infra.

**Examples**:
- **Gmail**, **Google Workspace**.
- **Salesforce**.
- **Slack**, **Notion**, **Linear**.
- **GitHub** (the website, not the binary).
- **Zoom**, **Figma**.

**You'd say**: *"I just want email. I don't want to manage mail server."*

```bash
# Use Gmail
# → Login at gmail.com. That's it.
```

**Pros**: zero ops, fast value.
**Cons**: vendor lock-in, customization limited, data sovereignty concerns.

### Bonus models 2026

3 model gốc IaaS/PaaS/SaaS được mở rộng thành nhiều subcategory 2026 — mỗi cái phục vụ use case riêng. **CaaS** cho team đã đóng gói container (giữa IaaS-PaaS), **FaaS** cho event-driven workload, **DBaaS** cho team chỉ cần DB không muốn vận hành. Hiểu rõ giúp chọn đúng layer thay vì over-provision:

- **CaaS — Containers as a Service**: AWS ECS/Fargate, GCP Cloud Run, Azure Container Apps. Between IaaS + PaaS.
- **FaaS — Functions as a Service** (serverless): AWS Lambda, GCP Cloud Functions, Azure Functions. PaaS but event-driven.
- **DBaaS — Database as a Service**: AWS RDS, Aurora, GCP Cloud SQL. PaaS for databases.
- **iPaaS — Integration PaaS**: Zapier, Make, n8n. Connect SaaS apps.
- **BaaS — Backend as a Service**: Firebase, Supabase. Mobile + frontend get backend without code.

### Stack diagram

Cloud stack có 9 lớp xếp chồng từ datacenter dưới cùng lên Data trên cùng. Tuỳ model (IaaS/PaaS/SaaS) mà ranh giới "ai quản gì" dịch lên hay xuống. Diagram dưới đây minh hoạ trực quan: layer càng cao bạn quản càng ít — đổi lại càng phụ thuộc vendor:

```
                  ┌──────────────────┐
                  │     Data         │ ← you manage
                  ├──────────────────┤
                  │  Application     │
                  ├──────────────────┤
                  │   Runtime        │
SaaS              ├──────────────────┤   ─┐
                  │   Middleware     │    │
PaaS              ├──────────────────┤    │
                  │   OS             │    │ vendor manages
                  ├──────────────────┤    │
IaaS              │   Virtualization │    │
                  ├──────────────────┤    │
                  │   Hardware       │   ─┘
                  ├──────────────────┤
                  │   Network        │
                  ├──────────────────┤
                  │   Datacenter     │
                  └──────────────────┘
```

→ Layer càng cao bạn manage càng ít, vendor lock-in càng cao.

🪞 **Ẩn dụ**: *Cloud service models như **mức độ "ăn ngoài"**:
- **On-prem** = nấu nhà (tự lo mọi thứ).
- **IaaS** = thuê bếp + nguyên liệu, tự nấu.
- **PaaS** = nhà hàng có menu, đầu bếp họ nấu.
- **SaaS** = mua đồ ăn sẵn, vào microwave.*

---

## 3️⃣ 4 Deployment models — Public / Private / Hybrid / Multi-cloud

### Public cloud

Vendor-owned datacenter, shared with thousands customers (multi-tenant).

**Examples**: AWS, GCP, Azure, DigitalOcean, Cloudflare.

**Pros**: 
- Lowest cost (vendor economy of scale).
- Fastest setup.
- Latest services.

**Cons**:
- Less control.
- Data sovereignty (where data stored).
- Vendor lock-in risks.

**Best for**: most workloads 2026 (startup → enterprise).

### Private cloud

Single-tenant cloud — for **one organization** only.

**Variants**:
- **On-prem private cloud**: company runs own datacenter with cloud-like API (VMware, OpenStack).
- **Hosted private cloud**: vendor dedicates hardware to you (AWS Outposts, Azure Stack, GCP Anthos on-prem).

**Pros**: max control, data sovereignty, compliance strict.
**Cons**: high upfront cost, slower innovation, harder to scale.

**Best for**: government, defense, healthcare (HIPAA strict), financial (PCI).

### Hybrid cloud

**Mix**: on-prem datacenter + public cloud, connected via private network (VPN / Direct Connect).

**Examples**:
- Database on-prem (sensitive data) + web app on AWS.
- Burst to cloud (steady-state on-prem, spike to AWS for Black Friday).
- Tier: dev cloud, prod on-prem.

**Pros**: 
- Migrate gradually.
- Keep sensitive workloads on-prem.
- Cost optimization (long-running on-prem, elastic cloud).

**Cons**: 
- Complexity (2 environments).
- Latency between on-prem ↔ cloud.
- Need orchestration (K8s, Anthos, Azure Arc).

### Multi-cloud

Use **multiple public clouds** for different workloads.

**Examples**:
- AWS for compute, GCP for ML (BigQuery, Vertex AI), Cloudflare for CDN.
- Disaster recovery: primary AWS, DR Azure.
- Avoid vendor lock-in.

**Pros**:
- Best-of-breed (pick best service per cloud).
- Negotiation leverage with vendors.
- Geographic / political risk mitigation.

**Cons**:
- **Complexity**: 3x ops surface area.
- **Skills**: team must know multiple clouds.
- **Data transfer cost**: cross-cloud egress expensive.
- **Lowest common denominator**: abstraction limit features.

**Reality 2026**: most companies have **incidental multi-cloud** (AWS primary + Cloudflare CDN + GitHub) rather than **strategic multi-cloud** (50/50 AWS+GCP).

→ Don't pursue multi-cloud for its own sake. Pick reasons.

---

## 4️⃣ History 1999 → 2026

### Timeline

Cloud không "đột nhiên" có — nó nảy mầm từ 1999 với Salesforce SaaS, bùng nổ 2006 khi AWS public S3+EC2. Timeline dưới đây show 26 năm — chú ý 3 cột mốc: 2006 (AWS — modern cloud), 2014 (Kubernetes — orchestration), 2023 (AI cloud — current era):

| Year | Event |
|---|---|
| 1999 | Salesforce — first major SaaS (CRM in cloud) |
| 2002 | Amazon launches AWS infrastructure (internal) |
| 2006 | **AWS S3 + EC2 public launch** — start modern cloud era |
| 2008 | Google App Engine (PaaS) |
| 2010 | Microsoft Azure launches |
| 2010 | OpenStack founded (open source private cloud) |
| 2011 | NIST defines "cloud computing" |
| 2012 | Google Compute Engine (GCP IaaS) |
| 2014 | **Kubernetes** released (Google open source) — orchestration layer |
| 2014 | AWS Lambda (FaaS) — serverless mainstream |
| 2015 | CNCF founded |
| 2018 | Cloudflare Workers (edge computing) |
| 2019 | Multi-cloud strategic for enterprise |
| 2020 | COVID accelerate cloud migration |
| 2022 | Vercel, Netlify mainstream (frontend cloud) |
| 2023 | AI cloud services (OpenAI API, AWS Bedrock) |
| 2024 | OpenTofu (Terraform OSS fork after Hashicorp license change) |
| 2025 | Edge computing + AI inference combined |
| **2026** | **AI-first cloud services** + sustainability focus + post-quantum encryption |

### Market share 2026 (estimates)

Thị phần *Infrastructure-as-a-Service* (IaaS) năm 2026 vẫn đậm chất "Big 3": AWS, Azure, GCP chiếm ~70%. Số liệu dưới đây ước lượng từ Synergy Research + Canalys — không exact nhưng cho cái nhìn cân đối khi học. Quan trọng: chọn cloud nên dựa **use case + team skill**, không theo top:

| Vendor | Market share | Strength |
|---|---|---|
| **AWS** | ~33% | Most services, mature ops |
| **Azure** | ~25% | Enterprise + Microsoft ecosystem |
| **GCP** | ~12% | AI/ML + BigQuery |
| **Alibaba** | ~6% | China + Asia |
| **Oracle** | ~3% | Database + ERP customers |
| **IBM** | ~2% | Hybrid + RedHat |
| **DigitalOcean** | ~1% | Developers, simplicity |
| **Cloudflare** | ~1% | Edge + CDN |
| Others | ~17% | Various niches |

→ AWS leader, Azure growing fast (Microsoft enterprise sales).

---

## 5️⃣ Top vendor comparison

### AWS — The leader

**Strengths**:
- Most services (300+ services 2026).
- Mature ops, longest track record.
- Largest community + docs + 3rd party tools.
- Government Cloud (FedRAMP, GovCloud).

**Weaknesses**:
- Complex pricing, easy to overspend.
- UI not best.
- AWS-specific concepts (e.g., IAM policies arcane).

**Best for**: most workloads, default choice for serious production.

### GCP — The data + AI cloud

**Strengths**:
- **BigQuery**: best data warehouse 2026.
- **Vertex AI**: integrated ML platform.
- **Kubernetes**: GCP invented K8s, best GKE.
- Network: Google's global network = fast cross-region.

**Weaknesses**:
- Fewer services than AWS.
- Less enterprise sales support (vs Azure).
- Customer support not always great.

**Best for**: data-heavy companies, ML workloads, K8s-first orgs.

### Azure — The enterprise cloud

**Strengths**:
- **Microsoft ecosystem**: Windows Server, AD, Office 365 integration.
- **Enterprise sales**: account managers, contracts.
- **Hybrid**: Azure Stack, Arc — best hybrid story.

**Weaknesses**:
- Documentation quality varies.
- Newer (less mature than AWS in some areas).
- Pricing complex.

**Best for**: enterprises already on Microsoft stack.

### DigitalOcean — The developer cloud

**Strengths**:
- **Simple pricing**: predictable VM cost.
- **Developer-friendly**: clean UI, good docs.
- **Managed DBs**: simple managed Postgres/MySQL/Redis.

**Weaknesses**:
- Fewer services (no Lambda equivalent).
- Smaller global presence.
- Less enterprise features.

**Best for**: startup, indie devs, small-mid teams.

### Cloudflare — The edge cloud

**Strengths**:
- **Edge compute** (Workers): closest to user, low latency.
- **CDN**: industry-leading.
- **DDoS protection**: massive scale.
- **R2**: S3-compatible no egress fees.

**Weaknesses**:
- Not full IaaS (no traditional VMs).
- Edge limits (Workers V8 isolates, not containers).

**Best for**: frontend + CDN + edge functions, supplementary to AWS/GCP.

### Vercel / Netlify — Frontend cloud

**Strengths**:
- **Git push to deploy**: simplest possible.
- **Edge functions**: low-latency JS.
- **Preview deployments**: PR = preview URL.

**Weaknesses**:
- Frontend-focused, not for arbitrary backend.
- Cost can spike at scale.

**Best for**: Next.js, frontend SPAs.

### Decision matrix 2026

Không có "cloud tốt nhất" — chỉ có "cloud phù hợp use case". Ma trận dưới đây tổng hợp 8 tình huống điển hình + cloud khuyến nghị tương ứng. Dùng làm gợi ý xuất phát; quyết định cuối phụ thuộc thêm team skill, budget, compliance:

| Use case | Recommended |
|---|---|
| General startup | AWS (default) or DigitalOcean (simpler) |
| Frontend + edge | Vercel + Cloudflare |
| Data-heavy / ML | GCP |
| Enterprise Microsoft shop | Azure |
| Government / heavy compliance | AWS GovCloud or Azure Gov |
| Asia/China presence | Alibaba + AWS regional |
| Cost-sensitive devs | DigitalOcean / Hetzner |
| Multi-cloud hedge | AWS primary + GCP DR |

---

## 6️⃣ Cost model

### Pricing models

1. **On-demand**: pay per use, no commitment. Highest unit price.
   - Best for: dev, unpredictable workload.

2. **Reserved instances** (RI) / **Savings Plans**: commit 1 or 3 years for 30-70% discount.
   - Best for: steady-state production workload.

3. **Spot instances**: AWS/GCP/Azure sell unused capacity at 50-90% discount, but **can interrupt** with 2-min warning.
   - Best for: fault-tolerant batch jobs, stateless workers.

4. **Commit + flexible** (Savings Plans, sustained use discount): commit $/hour without locking instance type.
   - Best for: production with some flexibility.

### Hidden costs

⚠️ Common cost surprises:
- **Egress** (data out): $0.09/GB AWS, $0.12/GB GCP. 1TB out = $90.
- **NAT Gateway**: $0.045/hour + $0.045/GB processed.
- **Idle resources**: forgot to stop EC2 = pay 24/7.
- **Log volume**: CloudWatch logs $0.50/GB ingested.
- **Cross-AZ traffic**: $0.01/GB even internal.
- **Snapshots**: EBS snapshots accumulate.

→ Watch bill weekly. Cost monitoring (FinOps) = essential.

### Cost optimization basics

| Tactic | Saving |
|---|---|
| Right-size instances (smaller fits) | 20-40% |
| Reserved Instances (1-year) | 30-50% |
| Spot for stateless workloads | 50-80% |
| Turn off dev nights/weekends | 70% on dev |
| Use S3 lifecycle (move to Glacier) | 80% on cold data |
| Avoid cross-AZ where possible | 10-20% |
| CDN cache (reduce origin egress) | 50% on egress |

→ Apply systematically = 50% cost reduction common.

---

## 7️⃣ Cloud vs On-prem vs Hybrid

### Cost over time

```
Cost
 │
 │      ╱─────  Cloud (scale flexible)
 │    ╱
 │  ╱
 │ ╱
 │╱     ┌──────── On-prem (high upfront, low ongoing)
 │      │
 └──────────────────────────► Time
        ↑
   Break-even ~3 years
```

→ **Cloud** OPEX-heavy (pay forever), **On-prem** CAPEX-heavy (upfront, then cheap).

### When cloud wins

- Unpredictable workload (spike for Black Friday).
- Geographic distribution (regions/edge worldwide).
- Need latest managed services (Lambda, BigQuery, Bedrock).
- Small team without sysadmin.
- Compliance (cloud have certifications ready).
- Disaster recovery (multi-region).

### When on-prem wins

- **Steady workload** with predictable cost (cloud OPEX > on-prem CAPEX after 3-5 years).
- **Data sovereignty**: government, healthcare, financial.
- **Low latency** requirement to local users (factory, hospital).
- **Specialized hardware**: HPC, GPU clusters, custom ASICs.
- **Air-gapped**: defense, secure facilities.

### When hybrid wins

- Migration in progress (years-long).
- Burst capacity (steady on-prem, spike to cloud).
- Tier by sensitivity (dev cloud, prod on-prem).
- Compliance with hybrid acceptable.

→ **Reality 2026**: vast majority of new workloads → public cloud. On-prem retained for legacy + compliance reasons.

---

## 8️⃣ Khi nào cloud KHÔNG đúng

Anti-patterns:

1. **Just to look modern**:
   - "We moved to cloud" without business reason → costs spike, complexity.

2. **Lift-and-shift everything**:
   - Move VMs as-is to cloud = pay cloud price for VM workload. No re-architect = no savings.

3. **Single VM in cloud**:
   - 1 EC2 = same as 1 VPS but 3x more expensive. Use cloud-native (managed services) or stick VPS.

4. **Storing massive data without lifecycle**:
   - 100TB on S3 Standard forever = $2,000/month. Move to Glacier = $40/month.

5. **Underestimate egress cost**:
   - Streaming app pulling 1PB/month from S3 = $90,000 egress. Use CDN or Cloudflare R2 (no egress).

6. **Multi-cloud "because we should"**:
   - 2x ops cost, 0x benefit for most teams.

7. **Forgotten test resources**:
   - Engineer spin up GPU cluster for ML experiment, forget to stop. Friday → Monday = $5,000 burnt.

→ Cloud is **tool**, not strategy. Use intentionally.

---

## 💡 Câu hỏi beginner hay hỏi

**Q1.** "Free tier có dùng được thực sự không?"

→ **Yes for learning**, no for production:
- **AWS free tier**: 12 months — 750 hours/month t2.micro EC2, 5GB S3, 750 hours RDS micro.
- **GCP free tier**: $300 credit + always-free tier (e2-micro VM, 5GB S3).
- **Azure**: $200 credit + 30-day + always-free.

→ Build learning project. Watch billing alert. Stop everything when done.

**Q2.** "Cloud có an toàn không, data của tôi?"

→ **More secure than on-prem in most cases**. Cloud vendors invest billions in security:
- 24/7 SOC, vulnerability scanning.
- Compliance certifications (SOC2, ISO 27001, HIPAA, PCI).
- Physical security beats most companies' datacenters.

**Caveats**:
- **You** must configure securely (IAM, encryption, network).
- Most breaches = misconfig (S3 public, IAM keys leaked), not cloud vendor fault.
- Shared responsibility (bài 04).

**Q3.** "Khi nào move to cloud?"

→ Triggers:
- Hardware refresh due — cost compare cloud vs new hardware.
- Geographic expansion (new market).
- Compliance gap.
- Team can't keep up (small ops team, growing service).
- Investor pressure (cloud-native looks modern).

**Don't move when**:
- No clear cost/business benefit.
- Team has no cloud skills (train first).
- Current infra works fine.

**Q4.** "AWS vs GCP vs Azure cho startup?"

→ Default **AWS** (largest community, most services, hire engineers easier). **GCP** if data/ML heavy. **Azure** if enterprise sale + Microsoft stack.

→ Avoid switching mid-project. Pick + commit + learn deeply.

**Q5.** "Cloud cost spike — fix sao?"

→ Process:
1. **Cost Explorer** (AWS) / Billing dashboard.
2. Filter by service: EC2? S3? Data transfer?
3. Identify top spenders: tag-based allocation.
4. Optimize: right-size, RI, spot, lifecycle.
5. **FinOps team** if > $50K/month.

Tools: **Infracost** (CI estimate), **Vantage**, **CloudHealth**.

---

## 🗺️ Lộ trình học tiếp theo

| Bài | Nội dung | Output |
|---|---|---|
| **01** Regions, AZs, Edge | Geographic distribution + latency + CDN + reliability tiers | Pick right region + setup CDN |
| **02** Cloud networking | VPC, subnets, peering, VPN, Direct Connect | Design VPC for production app |
| **03** Storage + Databases | Block/object/file + managed DBs + cache + queue + search | Choose right storage per use case |
| **04** Cloud security | IAM + encryption + network sec + shared responsibility + compliance | Secure-by-default cloud setup |

→ **Tổng ~75 phút đọc**. Sau cluster: vendor-neutral cloud foundations. Specific clouds (AWS/GCP/Azure) → separate sub-clusters.

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Cloud computing** | On-demand network access to shared compute pool (NIST definition) |
| **IaaS** | Infrastructure as a Service — VMs, storage, network |
| **PaaS** | Platform as a Service — runtime + middleware managed |
| **SaaS** | Software as a Service — full application managed |
| **CaaS** | Containers as a Service (Fargate, Cloud Run) |
| **FaaS** | Functions as a Service / serverless (Lambda) |
| **DBaaS** | Database as a Service (RDS, Cloud SQL) |
| **BaaS** | Backend as a Service (Firebase, Supabase) |
| **Public cloud** | Multi-tenant vendor cloud (AWS, GCP, Azure) |
| **Private cloud** | Single-tenant cloud (on-prem or hosted) |
| **Hybrid cloud** | Mix on-prem + public cloud |
| **Multi-cloud** | Use multiple public clouds |
| **On-demand pricing** | Pay per use, no commitment |
| **Reserved instances (RI)** | 1-3 year commitment for discount |
| **Spot instances** | Discounted unused capacity (interruptible) |
| **Egress** | Data leaving cloud (charged) |
| **Lift-and-shift** | Move existing workload to cloud without re-architecting |
| **Cloud-native** | Architecture leveraging managed services |
| **Shared responsibility** | Vendor secures cloud, you secure in cloud (bài 04) |
| **Tenant** | Customer of multi-tenant cloud |
| **Region** | Geographic cluster of datacenters (bài 01) |
| **Availability Zone (AZ)** | Datacenter within region (bài 01) |
| **FinOps** | Financial Operations — cloud cost management discipline |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- → Tiếp: [01_regions-availability-zones-edge.md](01_regions-availability-zones-edge.md) *(sắp viết)*
- ↑ Cluster: [Cloud Fundamentals README](../../README.md)

### Cross-reference
- 🏗️ [IaC basic](../../../../10_DevOps/iac/lessons/01_basic/) — Terraform manage cloud
- 🐳 [Docker basic](../../../../10_DevOps/docker/lessons/01_basic/) — containers in cloud
- ☸️ [K8s basic](../../../../10_DevOps/kubernetes/lessons/01_basic/) — K8s on cloud

### Tài nguyên ngoài (2026)
- 📖 [NIST cloud computing definition](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf)
- 📖 [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) — best practices
- 📖 [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- 📖 [Azure Cloud Adoption Framework](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/)
- 📖 [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- 📖 [The Cloud Native Computing Foundation (CNCF) Landscape](https://landscape.cncf.io/)
- 📖 [State of the Cloud Report (Flexera)](https://www.flexera.com/about-us/press-center/flexera-releases-2024-state-of-the-cloud-report) — annual
- 📖 [Cloud Excellence Pillars (Gartner)](https://www.gartner.com/en/insights)
- 📖 [Wardley Mapping](https://learnwardleymapping.com/) — strategic cloud decisions

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Bonus models 2026 + Stack diagram + Timeline + Market share 2026 + Decision matrix 2026.
- **v1.0.0 (24/05/2026)** — Bài đầu tiên của `11_Cloud/`. Cloud definition NIST + IaaS/PaaS/SaaS + 4 deployment models (public/private/hybrid/multi-cloud) + history 1999-2026 + vendor comparison (AWS/GCP/Azure/DO/Cloudflare/Vercel) + cost models + cloud vs on-prem + anti-patterns. Foundation cho 4 bài kế tiếp.
