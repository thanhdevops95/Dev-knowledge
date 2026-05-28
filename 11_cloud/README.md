# ☁️ 11_cloud

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.3.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Basic branch hoàn chỉnh — 9/9 sub-cluster có basic content (45 lessons, ~40,625 dòng)

> 🎯 *Cloud knowledge: AWS, GCP, Azure, DigitalOcean, Cloudflare, Serverless, Multi-cloud strategies, FinOps cost management. Vendor-neutral fundamentals trước, sau đó deep dive từng vendor.*

---

## 🎯 Chủ đề này có gì

Cloud computing landscape, vendor-specific (AWS/GCP/Azure/DO/Cloudflare), multi-cloud strategies, serverless, FinOps cost management.

---

## 📂 Sub-clusters

| Cluster | Status | Basic | Intermediate |
|---|---|---|---|
| [cloud-fundamentals](cloud-fundamentals/) | ✅ Active | 5/5 ✅ | ⏳ |
| [aws](aws/) | ✅ Active | 5/5 ✅ | ⏳ |
| [gcp](gcp/) | ✅ Active | 5/5 ✅ | ⏳ |
| [azure](azure/) | ✅ Active | 5/5 ✅ | ⏳ |
| [digitalocean](digitalocean/) | ✅ Active | 5/5 ✅ | ⏳ |
| [cloudflare](cloudflare/) | ✅ Active | 5/5 ✅ | ⏳ |
| [serverless](serverless/) | ✅ Active | 5/5 ✅ | ⏳ |
| [multi-cloud-strategies](multi-cloud-strategies/) | ✅ Active | 5/5 ✅ | ⏳ |
| [cloud-cost-management](cloud-cost-management/) | ✅ Active | 5/5 ✅ | ⏳ |

> Chi tiết sitemap → [`../_blueprint/01_sitemap-detail.md`](../_blueprint/01_sitemap-detail.md).

---

## 🚀 Lộ trình đề xuất

| Bạn là... | Đi theo |
|---|---|
| 🟢 **Beginner zero-base** | [cloud-fundamentals/01_basic/](cloud-fundamentals/lessons/01_basic/) → chọn vendor cụ thể (AWS thường default) |
| 🟡 **Đã dùng cloud, muốn hiểu sâu** | cloud-fundamentals → aws/gcp/azure specific basic |
| 🟠 **Senior — pick best fit** | multi-cloud-strategies + cost-management |
| 🧭 **Cloud Architect / DevOps career path** | cloud-fundamentals → aws basic → IaC + K8s + Observability (10_devops) |

---

## 📖 Active cluster — cloud-fundamentals (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is cloud computing?](cloud-fundamentals/lessons/01_basic/00_what-is-cloud-computing.md) | MUST-KNOW | ~15p |
| 01 | [Regions, AZs, Edge](cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md) | MUST-KNOW | ~17p |
| 02 | [Cloud networking](cloud-fundamentals/lessons/01_basic/02_cloud-networking.md) | MUST-KNOW | ~17p |
| 03 | [Storage + databases](cloud-fundamentals/lessons/01_basic/03_storage-and-databases.md) | MUST-KNOW | ~17p |
| 04 | [Security + shared responsibility](cloud-fundamentals/lessons/01_basic/04_cloud-security-and-shared-responsibility.md) | MUST-KNOW | ~17p |

→ **Tổng ~83 phút đọc**. Foundation vendor-neutral.

---

## 📖 Active cluster — aws basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is AWS overview](aws/lessons/01_basic/00_what-is-aws-overview.md) | MUST-KNOW | ~17p |
| 01 | [EC2 + EBS](aws/lessons/01_basic/01_ec2-and-ebs-compute.md) | MUST-KNOW | ~22p |
| 02 | [S3 deep + IAM](aws/lessons/01_basic/02_s3-deep-and-iam.md) | MUST-KNOW | ~22p |
| 03 | [RDS + DynamoDB](aws/lessons/01_basic/03_rds-and-dynamodb.md) | MUST-KNOW | ~20p |
| 04 | [Lambda + API Gateway](aws/lessons/01_basic/04_lambda-and-api-gateway.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — gcp basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is GCP overview](gcp/lessons/01_basic/00_what-is-gcp-overview.md) | MUST-KNOW | ~17p |
| 01 | [Compute Engine + Disks](gcp/lessons/01_basic/01_compute-engine-and-disks.md) | MUST-KNOW | ~22p |
| 02 | [Cloud Storage + IAM](gcp/lessons/01_basic/02_cloud-storage-and-iam.md) | MUST-KNOW | ~22p |
| 03 | [Cloud SQL + Firestore](gcp/lessons/01_basic/03_cloud-sql-and-firestore.md) | MUST-KNOW | ~20p |
| 04 | [Cloud Functions + Run + API Gateway](gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — azure basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is Azure overview](azure/lessons/01_basic/00_what-is-azure-overview.md) | MUST-KNOW | ~17p |
| 01 | [VMs + Disks](azure/lessons/01_basic/01_virtual-machines-and-disks.md) | MUST-KNOW | ~22p |
| 02 | [Blob Storage + RBAC](azure/lessons/01_basic/02_blob-storage-and-rbac.md) | MUST-KNOW | ~22p |
| 03 | [Azure SQL + Cosmos DB](azure/lessons/01_basic/03_azure-sql-and-cosmosdb.md) | MUST-KNOW | ~20p |
| 04 | [Functions + App Service](azure/lessons/01_basic/04_functions-and-app-service.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — digitalocean basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is DigitalOcean overview](digitalocean/lessons/01_basic/00_what-is-digitalocean-overview.md) | MUST-KNOW | ~15p |
| 01 | [Droplets + Volumes](digitalocean/lessons/01_basic/01_droplets-and-volumes.md) | MUST-KNOW | ~22p |
| 02 | [Spaces Object Storage + CDN](digitalocean/lessons/01_basic/02_spaces-object-storage-and-cdn.md) | MUST-KNOW | ~20p |
| 03 | [Managed Databases](digitalocean/lessons/01_basic/03_managed-databases.md) | MUST-KNOW | ~22p |
| 04 | [App Platform + Functions](digitalocean/lessons/01_basic/04_app-platform-and-functions.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — cloudflare basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is Cloudflare overview](cloudflare/lessons/01_basic/00_what-is-cloudflare-overview.md) | MUST-KNOW | ~17p |
| 01 | [CDN + DNS + SSL](cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md) | MUST-KNOW | ~20p |
| 02 | [Workers + Pages](cloudflare/lessons/01_basic/02_workers-and-pages.md) | MUST-KNOW | ~22p |
| 03 | [R2 + D1 + Queues](cloudflare/lessons/01_basic/03_r2-and-d1-and-queues.md) | MUST-KNOW | ~22p |
| 04 | [Security + Zero Trust + WAF](cloudflare/lessons/01_basic/04_security-zero-trust-and-waf.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — serverless basic (5 bài, vendor-neutral)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is serverless](serverless/lessons/01_basic/00_what-is-serverless-overview.md) | MUST-KNOW | ~17p |
| 01 | [FaaS deep](serverless/lessons/01_basic/01_function-as-a-service-deep.md) | MUST-KNOW | ~20p |
| 02 | [Event-driven + triggers](serverless/lessons/01_basic/02_event-driven-and-triggers.md) | MUST-KNOW | ~22p |
| 03 | [Patterns + anti-patterns](serverless/lessons/01_basic/03_serverless-patterns-and-anti-patterns.md) | MUST-KNOW | ~22p |
| 04 | [Cost + cold start + observability](serverless/lessons/01_basic/04_serverless-cost-cold-start-and-observability.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — multi-cloud-strategies basic (5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is multi-cloud](multi-cloud-strategies/lessons/01_basic/00_what-is-multi-cloud-overview.md) | MUST-KNOW | ~17p |
| 01 | [Lock-in + Portability](multi-cloud-strategies/lessons/01_basic/01_vendor-lock-in-and-portability.md) | MUST-KNOW | ~20p |
| 02 | [Network + Identity](multi-cloud-strategies/lessons/01_basic/02_multi-cloud-network-and-identity.md) | MUST-KNOW | ~22p |
| 03 | [K8s multi-cloud + Anthos/Arc](multi-cloud-strategies/lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md) | MUST-KNOW | ~22p |
| 04 | [DR + Architecture patterns](multi-cloud-strategies/lessons/01_basic/04_disaster-recovery-and-architecture-patterns.md) | MUST-KNOW | ~22p |

---

## 📖 Active cluster — cloud-cost-management basic (FinOps, 5 bài)

| # | Bài | Tag | Thời lượng |
|---|---|---|---|
| 00 | [What is FinOps](cloud-cost-management/lessons/01_basic/00_what-is-finops-overview.md) | MUST-KNOW | ~17p |
| 01 | [Pricing models deep](cloud-cost-management/lessons/01_basic/01_pricing-models-deep.md) | MUST-KNOW | ~20p |
| 02 | [Tagging + Showback](cloud-cost-management/lessons/01_basic/02_tagging-allocation-and-showback.md) | MUST-KNOW | ~22p |
| 03 | [Optimization tactics](cloud-cost-management/lessons/01_basic/03_optimization-tactics-compute-storage-network.md) | MUST-KNOW | ~22p |
| 04 | [FinOps tools + automation](cloud-cost-management/lessons/01_basic/04_finops-tools-and-automation.md) | MUST-KNOW | ~22p |

---

## 🔗 Liên kết

### Trong workspace
- 🐳 [Docker](../10_devops/docker/) — containers in cloud
- ☸️ [Kubernetes](../10_devops/kubernetes/) — K8s on cloud
- 🏗️ [IaC Terraform](../10_devops/iac/) — manage cloud via code
- 🔁 [CI/CD](../10_devops/ci-cd/) — deploy to cloud
- 📊 [Observability](../10_devops/observability/) — monitor cloud
- 🌐 [Networking](../05_networking/) — TCP/IP foundation
- 🧭 [DevOps roadmap](../00_roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Cloud Architect roadmap](../00_roadmaps/career/cloud-engineer_career-roadmap.md)

---

## 📌 Changelog

- **v1.3.0 (24/05/2026)** — 🎉 **11_cloud basic branch ĐÓNG 9/9 sub-cluster** (45 lessons, ~40,625 dòng). Buildout 6 cluster còn lại trong cùng session: Azure, DigitalOcean, Cloudflare, Serverless, Multi-cloud-strategies, Cloud-cost-management. Foundation coverage hoàn chỉnh.
- **v1.2.0 (24/05/2026)** — Cluster **GCP basic 5/5 hoàn chỉnh**. 3/9 sub-clusters active (cloud-fundamentals + aws + gcp).
- **v1.1.0 (24/05/2026)** — Cluster **AWS basic 5/5 hoàn chỉnh**.
- **v1.0.0 (24/05/2026)** — Cluster **cloud-fundamentals basic 5/5 hoàn chỉnh**. Foundation vendor-neutral cho 11_cloud.
- **v0.1.0 (16/05/2026)** — Skeleton ban đầu.
