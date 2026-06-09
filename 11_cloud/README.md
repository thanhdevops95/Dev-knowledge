# ☁️ 11_cloud

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.4.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Basic branch hoàn chỉnh — 9/9 sub-cluster có basic content (45 lessons)

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

| # | Bài | Tag |
|---|---|---|
| 00 | [What is cloud computing?](cloud-fundamentals/lessons/01_basic/00_what-is-cloud-computing.md) | MUST-KNOW |
| 01 | [Regions, AZs, Edge](cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md) | MUST-KNOW |
| 02 | [Cloud networking](cloud-fundamentals/lessons/01_basic/02_cloud-networking.md) | MUST-KNOW |
| 03 | [Storage + databases](cloud-fundamentals/lessons/01_basic/03_storage-and-databases.md) | MUST-KNOW |
| 04 | [Security + shared responsibility](cloud-fundamentals/lessons/01_basic/04_cloud-security-and-shared-responsibility.md) | MUST-KNOW |

→ Nền tảng vendor-neutral (không phụ thuộc nhà cung cấp) — học cụm này trước rồi mới chọn vendor cụ thể.

---

## 📖 Active cluster — aws basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is AWS overview](aws/lessons/01_basic/00_what-is-aws-overview.md) | MUST-KNOW |
| 01 | [EC2 + EBS](aws/lessons/01_basic/01_ec2-and-ebs-compute.md) | MUST-KNOW |
| 02 | [S3 deep + IAM](aws/lessons/01_basic/02_s3-deep-and-iam.md) | MUST-KNOW |
| 03 | [RDS + DynamoDB](aws/lessons/01_basic/03_rds-and-dynamodb.md) | MUST-KNOW |
| 04 | [Lambda + API Gateway](aws/lessons/01_basic/04_lambda-and-api-gateway.md) | MUST-KNOW |

---

## 📖 Active cluster — gcp basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is GCP overview](gcp/lessons/01_basic/00_what-is-gcp-overview.md) | MUST-KNOW |
| 01 | [Compute Engine + Disks](gcp/lessons/01_basic/01_compute-engine-and-disks.md) | MUST-KNOW |
| 02 | [Cloud Storage + IAM](gcp/lessons/01_basic/02_cloud-storage-and-iam.md) | MUST-KNOW |
| 03 | [Cloud SQL + Firestore](gcp/lessons/01_basic/03_cloud-sql-and-firestore.md) | MUST-KNOW |
| 04 | [Cloud Functions + Run + API Gateway](gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) | MUST-KNOW |

---

## 📖 Active cluster — azure basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is Azure overview](azure/lessons/01_basic/00_what-is-azure-overview.md) | MUST-KNOW |
| 01 | [VMs + Disks](azure/lessons/01_basic/01_virtual-machines-and-disks.md) | MUST-KNOW |
| 02 | [Blob Storage + RBAC](azure/lessons/01_basic/02_blob-storage-and-rbac.md) | MUST-KNOW |
| 03 | [Azure SQL + Cosmos DB](azure/lessons/01_basic/03_azure-sql-and-cosmosdb.md) | MUST-KNOW |
| 04 | [Functions + App Service](azure/lessons/01_basic/04_functions-and-app-service.md) | MUST-KNOW |

---

## 📖 Active cluster — digitalocean basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is DigitalOcean overview](digitalocean/lessons/01_basic/00_what-is-digitalocean-overview.md) | MUST-KNOW |
| 01 | [Droplets + Volumes](digitalocean/lessons/01_basic/01_droplets-and-volumes.md) | MUST-KNOW |
| 02 | [Spaces Object Storage + CDN](digitalocean/lessons/01_basic/02_spaces-object-storage-and-cdn.md) | MUST-KNOW |
| 03 | [Managed Databases](digitalocean/lessons/01_basic/03_managed-databases.md) | MUST-KNOW |
| 04 | [App Platform + Functions](digitalocean/lessons/01_basic/04_app-platform-and-functions.md) | MUST-KNOW |

---

## 📖 Active cluster — cloudflare basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is Cloudflare overview](cloudflare/lessons/01_basic/00_what-is-cloudflare-overview.md) | MUST-KNOW |
| 01 | [CDN + DNS + SSL](cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md) | MUST-KNOW |
| 02 | [Workers + Pages](cloudflare/lessons/01_basic/02_workers-and-pages.md) | MUST-KNOW |
| 03 | [R2 + D1 + Queues](cloudflare/lessons/01_basic/03_r2-and-d1-and-queues.md) | MUST-KNOW |
| 04 | [Security + Zero Trust + WAF](cloudflare/lessons/01_basic/04_security-zero-trust-and-waf.md) | MUST-KNOW |

---

## 📖 Active cluster — serverless basic (5 bài, vendor-neutral)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is serverless](serverless/lessons/01_basic/00_what-is-serverless-overview.md) | MUST-KNOW |
| 01 | [FaaS deep](serverless/lessons/01_basic/01_function-as-a-service-deep.md) | MUST-KNOW |
| 02 | [Event-driven + triggers](serverless/lessons/01_basic/02_event-driven-and-triggers.md) | MUST-KNOW |
| 03 | [Patterns + anti-patterns](serverless/lessons/01_basic/03_serverless-patterns-and-anti-patterns.md) | MUST-KNOW |
| 04 | [Cost + cold start + observability](serverless/lessons/01_basic/04_serverless-cost-cold-start-and-observability.md) | MUST-KNOW |

---

## 📖 Active cluster — multi-cloud-strategies basic (5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is multi-cloud](multi-cloud-strategies/lessons/01_basic/00_what-is-multi-cloud-overview.md) | MUST-KNOW |
| 01 | [Lock-in + Portability](multi-cloud-strategies/lessons/01_basic/01_vendor-lock-in-and-portability.md) | MUST-KNOW |
| 02 | [Network + Identity](multi-cloud-strategies/lessons/01_basic/02_multi-cloud-network-and-identity.md) | MUST-KNOW |
| 03 | [K8s multi-cloud + Anthos/Arc](multi-cloud-strategies/lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md) | MUST-KNOW |
| 04 | [DR + Architecture patterns](multi-cloud-strategies/lessons/01_basic/04_disaster-recovery-and-architecture-patterns.md) | MUST-KNOW |

---

## 📖 Active cluster — cloud-cost-management basic (FinOps, 5 bài)

| # | Bài | Tag |
|---|---|---|
| 00 | [What is FinOps](cloud-cost-management/lessons/01_basic/00_what-is-finops-overview.md) | MUST-KNOW |
| 01 | [Pricing models deep](cloud-cost-management/lessons/01_basic/01_pricing-models-deep.md) | MUST-KNOW |
| 02 | [Tagging + Showback](cloud-cost-management/lessons/01_basic/02_tagging-allocation-and-showback.md) | MUST-KNOW |
| 03 | [Optimization tactics](cloud-cost-management/lessons/01_basic/03_optimization-tactics-compute-storage-network.md) | MUST-KNOW |
| 04 | [FinOps tools + automation](cloud-cost-management/lessons/01_basic/04_finops-tools-and-automation.md) | MUST-KNOW |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

Cloud không đứng một mình — nó là một mắt xích trong lộ trình DevOps/Cloud Engineer. Hai roadmap dưới đây cho bạn thấy cụm này nằm ở đâu trong bức tranh nghề nghiệp tổng thể:

- 🧭 [DevOps Engineer — Career roadmap](../00_roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Cloud Engineer / Architect — Career roadmap](../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🧩 Các chủ đề có thể bạn quan tâm

Các cụm dưới đây bổ trợ trực tiếp cho cloud: container hoá ứng dụng, điều phối ở quy mô lớn, quản lý hạ tầng bằng code, tự động hoá triển khai, giám sát và nền tảng mạng:

- 🐳 [Docker](../10_devops/docker/) — đóng gói ứng dụng thành container để chạy trên cloud
- ☸️ [Kubernetes](../10_devops/kubernetes/) — điều phối container ở quy mô lớn trên cloud
- 🏗️ [IaC / Terraform](../10_devops/iac/) — khai báo và quản lý hạ tầng cloud bằng code
- 🔁 [CI/CD](../10_devops/ci-cd/) — tự động build và deploy lên cloud
- 📊 [Observability](../10_devops/observability/) — giám sát hệ thống đang chạy trên cloud
- 🌐 [Networking](../05_networking/) — nền tảng TCP/IP, điều kiện hiểu networking trên cloud

### 🌐 Tài nguyên tham khảo khác

Bảng giá và dịch vụ trên cloud thay đổi liên tục, nên khi cần số liệu chính xác hãy đối chiếu trực tiếp với trang chính thức của từng nhà cung cấp:

- 🟧 [AWS Documentation](https://docs.aws.amazon.com/) — tài liệu chính thức của Amazon Web Services
- 🔵 [Google Cloud Documentation](https://cloud.google.com/docs) — tài liệu chính thức của GCP
- 🟦 [Azure Documentation](https://learn.microsoft.com/azure/) — tài liệu chính thức của Microsoft Azure
- 🌊 [DigitalOcean Docs](https://docs.digitalocean.com/) · 🟠 [Cloudflare Docs](https://developers.cloudflare.com/)
- 💰 [FinOps Foundation](https://www.finops.org/) — khung chuẩn về quản lý chi phí cloud

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (16/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Cluster **cloud-fundamentals basic 5/5 hoàn chỉnh**. Foundation vendor-neutral cho 11_cloud.
- **v1.1.0 (24/05/2026)** — Cluster **AWS basic 5/5 hoàn chỉnh**.
- **v1.2.0 (24/05/2026)** — Cluster **GCP basic 5/5 hoàn chỉnh**. 3/9 sub-clusters active (cloud-fundamentals + aws + gcp).
- **v1.3.0 (24/05/2026)** — 🎉 **11_cloud basic branch ĐÓNG 9/9 sub-cluster** (45 lessons). Buildout 6 cluster còn lại trong cùng session: Azure, DigitalOcean, Cloudflare, Serverless, Multi-cloud-strategies, Cloud-cost-management. Foundation coverage hoàn chỉnh.
- **v1.4.0 (01/06/2026)** — Bỏ cột "Thời lượng" + các dòng "~XX phút đọc" trong 9 bảng lessons (field thời lượng đã loại toàn kho); đổi field "Status" → "Trạng thái"; đổi heading "🔗 Liên kết" → "🔗 Liên kết & Tài nguyên" và tách thành 3 mục chuẩn (🧭 Định hướng lộ trình học / 🧩 Các chủ đề có thể bạn quan tâm / 🌐 Tài nguyên tham khảo khác).
