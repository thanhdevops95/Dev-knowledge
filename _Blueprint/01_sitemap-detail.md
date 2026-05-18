# 🗺️ Sitemap Detail — Toàn cảnh Repo Tri thức CNTT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.4.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *File này là **bản đồ toàn cảnh** của kho tri thức. Liệt kê tất cả 16 chủ đề L1, các L2 bên trong, và L3 chi tiết cho 3 chủ đề ưu tiên (Roadmaps, DevOps, OS). Khi viết bài mới, tra file này để xác định chủ đề thuộc đâu.*

> 📐 **Nguyên tắc thiết kế quan trọng**: bên trong mỗi chủ đề L2, nội dung được chia theo **7 loại** (xem [§0.2](#02-menu-7-loại-nội-dung)) — *không chỉ* theo cấp độ kiến thức. Lý do: cùng 1 chủ đề có nhiều dạng nội dung khác nhau (lý thuyết, setup, bài tập, project, recipe...). Cấu trúc "chỉ basic/intermediate/advanced" *không đủ*.

---

## 0️⃣ Quy ước đọc sitemap

### 0.1 Các cấp Level

| Ký hiệu | Ý nghĩa |
|---|---|
| **L1** | Chủ đề lớn — thư mục gốc trong kho (`10_DevOps/`, `04_OS/`, ...) |
| **L2** | Chủ đề con — thư mục trong L1 (`10_DevOps/kubernetes/`, `04_OS/linux/`) |
| **L3** | Phân loại nội dung trong L2 — `lessons/`, `setup/`, `exercises/`, `projects/`, `recipes/`, ... (xem §0.2) |
| **L4** | File/folder cụ thể trong L3 (`kubernetes/lessons/01_basic/01_pod.md`) |
| 📦 | Thư mục |
| 📄 | File |
| 🆕 | Chủ đề mới — chưa có content |
| ✅ | Đã có content sẵn ở `_Ref/` — có thể migrate |
| ⭐ | Ưu tiên cao — nên viết sớm |

### 0.2 Menu 7 loại nội dung

→ **Canonical**: [`02_folder-structure.md` §3](./02_folder-structure.md#3️⃣-cấu-trúc-l2--1-chủ-đề-con)

Tóm tắt: Bên trong mỗi L2, content tổ chức theo 7 loại folder: `lessons/`, `setup/`, `exercises/`, `projects/`, `recipes/`, `99_cheatsheet.md`, `_glossary.md`. Chọn loại nào áp dụng cho chủ đề — không bắt buộc đủ 7. Có thể mở rộng (`references/`, `interview-questions/`, ...).

### 0.3 Quy ước nội dung xuyên L2 (cross-cutting)

→ **Canonical**: [`05_linking-strategy.md` §3 (3 case A/B/C)](./05_linking-strategy.md#3️⃣-pattern-cross-l2-reference)

Tóm tắt 3 case:

| Case | Tình huống | Đặt ở |
|---|---|---|
| **A** | Chuỗi tuần tự nhiều stage, mỗi stage gọn 1 L2 | Mỗi stage trong L2 của nó. Điều hướng ở `00_Roadmaps/lab-series/` |
| **B** | Project siêu lớn không tách được (truly cross-L2) | `<L1>/_capstone-projects/` |
| **C** | Ghi chú / khái niệm xuyên L2 | `<L1>/_notes/` hoặc `<L1>/_concepts/` |

### 0.4 L1-level meta content slots

→ **Canonical**: [`02_folder-structure.md` §2 (Cấu trúc L1)](./02_folder-structure.md#2️⃣-cấu-trúc-l1--1-chủ-đề-lớn)

Tóm tắt: L1 có 2 nhóm — **meta slots** (prefix `_`: `_notes/`, `_concepts/`, `_capstone-projects/`, `_glossary.md`) và **L2 con** (không prefix). Meta slots OPTIONAL. README.md + 00_overview.md REQUIRED.

---

## 1️⃣ Sitemap tổng quan — 16 chủ đề + Roadmaps

| # | Chủ đề L1 | Mô tả ngắn | Trạng thái | Nhảy tới L2 |
|---|---|---|---|---|
| 00 | 🗺️ **Roadmaps** | Tập hợp các lộ trình học theo nghề | ⭐ Ưu tiên 1 | [§2.0](#20-00_roadmaps) |
| 01 | 🧠 **Foundations** | CS basics: DSA, OS theory, architecture | 🆕 | [§2.1](#21-01_foundations) |
| 02 | 🛠️ **Tools** | Git, Shell, Editor, productivity | 🆕 | [§2.2](#22-02_tools) |
| 03 | 💻 **Languages** | Python, Go, JS/TS, Rust, ... | 🆕 | [§2.3](#23-03_languages) |
| 04 | 🖥️ **OS** | Linux, MacOS, Windows | ⭐ Ưu tiên 2 | [§2.4](#24-04_os) |
| 05 | 🌐 **Networking** | TCP/IP, HTTP, DNS, ... | 🆕 | [§2.5](#25-05_networking) |
| 06 | 🗄️ **Databases** | SQL, NoSQL, Vector DB | 🆕 | [§2.6](#26-06_databases) |
| 07 | 🕸️ **Web** | Frontend + Backend + API | 🆕 | [§2.7](#27-07_web) |
| 08 | 📱 **Mobile** | iOS, Android, cross-platform | 🆕 | [§2.8](#28-08_mobile) |
| 09 | 🏛️ **Architecture** | Design patterns, System design | 🆕 | [§2.9](#29-09_architecture) |
| 10 | ⚙️ **DevOps** | Docker, K8s, CI/CD, IaC, Observability | ✅ ⭐ Ưu tiên 1 | [§2.10](#210-10_devops) |
| 11 | ☁️ **Cloud** | AWS, GCP, Azure | ✅ Một phần | [§2.11](#211-11_cloud) |
| 12 | 🔒 **Security** | Cybersec, Crypto, Auth | ✅ Một phần | [§2.12](#212-12_security) |
| 13 | 🤖 **AI-ML** | ML, DL, LLM, GenAI | ✅ Roadmaps | [§2.13](#213-13_ai-ml) |
| 14 | 📊 **Data-Engineering** | ETL, Warehouse, Streaming | ✅ Roadmaps | [§2.14](#214-14_data-engineering) |
| 15 | 🎮 **Specialized** | Game, Embedded, Blockchain, IoT | ✅ Một phần | [§2.15](#215-15_specialized) |
| 16 | 💼 **Career-Soft-skills** | Communication, Agile, Career path | ✅ Một phần | [§2.16](#216-16_career-soft-skills) |

---

## 2️⃣ Chi tiết L1 → L2

### 2.0 `00_Roadmaps`

→ **Canonical design**: [`06_roadmap-design.md`](./06_roadmap-design.md)

Tóm tắt cấu trúc:

```
00_Roadmaps/
├── README.md                ← danh mục cả 2 loại
├── career/                  🧭 career roadmap (6-12 tháng/nghề)
│   └── <role>_career-roadmap.md  × ~17 file
└── lab-series/              🧪 lab series (chuỗi bài tập xuyên chủ đề)
    └── <name>_lab-series.md  × ~N file
```

> Chi tiết L3 list các roadmap → [§3.1](#31-00_roadmaps---chi-tiết-l3). Template + spec design → `06_roadmap-design.md`.

---

### 2.1 `01_Foundations`

CS fundamentals — kiến thức gốc rễ cho mọi mảng.

```
01_Foundations/
├── README.md
├── 00_overview.md
├── dsa/                             ← cấu trúc dữ liệu & giải thuật
├── computer-architecture/           ← CPU, memory, bus, ...
├── os-theory/                       ← process, thread, scheduling, memory mgmt
├── compilers-and-interpreters/
├── math-for-cs/                     ← discrete math, logic, linear algebra
├── programming-paradigms/           ← OOP, FP, declarative, ...
└── _glossary.md
```

---

### 2.2 `02_Tools`

Công cụ dùng hằng ngày.

```
02_Tools/
├── README.md
├── 00_overview.md
├── git/                             ← phiên bản kiểm soát code
├── shell/                           ← Bash, Zsh, Fish
├── editor/                          ← VSCode, Vim, JetBrains
├── terminal-tools/                  ← tmux, fzf, ripgrep, bat, lazygit, ...
├── package-managers/                ← brew, apt, yum, npm, pip, ...
├── productivity/                    ← Obsidian, Notion, Raycast, ...
└── _glossary.md
```

---

### 2.3 `03_Languages`

Mỗi ngôn ngữ một thư mục con. Cấu trúc bên trong **giống nhau**: `01_basic/`, `02_intermediate/`, `03_advanced/`, `99_cheatsheet.md`.

```
03_Languages/
├── README.md
├── 00_overview.md
├── python/
├── javascript-typescript/
├── go/
├── rust/
├── java/
├── c-cpp/
├── csharp/
├── php/
├── ruby/
├── kotlin/
├── swift/
├── lua/
├── shell-scripting/                 ← link chéo tới 02_Tools/shell/
├── sql-as-language/                 ← link chéo tới 06_Databases/
└── _glossary.md
```

---

### 2.4 `04_OS`

Hệ điều hành.

```
04_OS/
├── README.md
├── 00_overview.md
├── linux/                           ⭐ — chi tiết L3 ở §3.3
├── macos/
├── windows/
├── cross-platform-concepts/         ← khác biệt khi viết code đa nền tảng
└── _glossary.md
```

> Chi tiết L3 `linux/` → xem [§3.3](#33-04_os--linux---chi-tiết-l3)

---

### 2.5 `05_Networking`

Mạng máy tính.

```
05_Networking/
├── README.md
├── 00_overview.md
├── tcp-ip-fundamentals/             ← OSI, TCP, UDP, IP, ...
├── http-https/                      ← request/response, methods, status, ...
├── dns/                             ← record types, resolution
├── load-balancing/                  ← L4 vs L7, round-robin, sticky session
├── proxy-and-reverse-proxy/         ← Nginx, HAProxy, Caddy
├── vpn/                             ← OpenVPN, WireGuard
├── cdn/                             ← Cloudflare, Akamai
├── network-security/                ← firewall, NAT, port forwarding
└── _glossary.md
```

---

### 2.6 `06_Databases`

Cơ sở dữ liệu.

```
06_Databases/
├── README.md
├── 00_overview.md
├── sql-fundamentals/                ← SQL chung cho mọi RDBMS
├── postgresql/
├── mysql/
├── sqlite/
├── mongodb/                         ← NoSQL document
├── redis/                           ← in-memory, cache
├── elasticsearch/                   ← search
├── vector-databases/                ← Pinecone, Weaviate, Milvus
├── time-series-databases/           ← InfluxDB, TimescaleDB
├── database-design/                 ← ERD, normalization, indexing
└── _glossary.md
```

---

### 2.7 `07_Web`

Web development — chia frontend / backend.

```
07_Web/
├── README.md
├── 00_overview.md
├── frontend/
│   ├── html-css/
│   ├── javascript-dom/
│   ├── react/
│   ├── vue/
│   ├── angular/
│   ├── svelte/
│   └── build-tools/                 ← Webpack, Vite, esbuild
├── backend/
│   ├── rest-api/
│   ├── graphql/
│   ├── websocket/
│   ├── nodejs-express/
│   ├── python-fastapi/
│   ├── python-django/
│   ├── go-gin/
│   └── java-spring/
├── fullstack-concepts/              ← state mgmt, auth flow, SSR/SSG
├── performance-optimization/        ← caching, lazy loading, code split
├── seo/
└── _glossary.md
```

---

### 2.8 `08_Mobile`

Mobile development.

```
08_Mobile/
├── README.md
├── 00_overview.md
├── ios-swift/                       ← native iOS
├── android-kotlin/                  ← native Android
├── react-native/                    ← cross-platform JS
├── flutter/                         ← cross-platform Dart
├── cross-platform-concepts/         ← khi chọn native vs cross-platform
├── mobile-architecture/             ← MVVM, Redux, ViewModel
└── _glossary.md
```

---

### 2.9 `09_Architecture`

Kiến trúc phần mềm & hệ thống.

```
09_Architecture/
├── README.md
├── 00_overview.md
├── design-patterns/                 ← GoF 23 patterns
├── solid-principles/
├── domain-driven-design/
├── microservices/
├── monolith-vs-microservices/
├── event-driven-architecture/       ← pub/sub, event sourcing, CQRS
├── hexagonal-architecture/          ← ports & adapters
├── clean-architecture/
├── system-design/                   ← scalability, caching, queues
├── distributed-systems/             ← CAP, consistency, consensus
└── _glossary.md
```

---

### 2.10 `10_DevOps`

Vận hành & tự động hóa — **chủ đề có nhiều content sẵn nhất**. Có cả L1-level meta (notes, concepts xuyên DevOps) lẫn L2 con (docker, kubernetes, ...) — mỗi L2 dùng menu 7 loại.

```
10_DevOps/
├── README.md                        ← index của DevOps
├── 00_overview.md                   ← DevOps là gì, văn hóa & công cụ
│
├── _notes/                          📝 (OPT) ghi chú xuyên DevOps
│   ├── devops-philosophy.md         ← triết lý: collaboration, automation, ...
│   ├── industry-trends.md           ← xu hướng (Platform Eng, FinOps, ...)
│   └── common-pitfalls.md           ← lỗi phổ biến khi triển khai DevOps
│
├── _concepts/                       💡 (OPT) khái niệm xuyên L2
│   ├── infrastructure-as-code.md    ← áp dụng cho iac/ + cloud/ + k8s/
│   ├── gitops.md                    ← áp dụng cho k8s/ + ci-cd/ + iac/
│   ├── observability-pillars.md     ← metrics + logs + traces (cross-L2)
│   └── shift-left-security.md       ← áp dụng cho ci-cd/ + security/
│
├── _capstone-projects/              🎯 (OPT, RARE) project xuyên L2 không tách được
│   └── master-devops-platform/      ← K8s + Terraform + ArgoCD + Prometheus + Vault đồng thời
│
├── docker/                          L2 ✅ — _Ref/Dev-knowledge/06_DevOps/docker/
├── kubernetes/                      L2 ⭐✅ — chi tiết L3-L4 ở §3.2
├── ci-cd/                           L2 ← Jenkins, GitHub-Actions, GitLab-CI, CircleCI
├── iac/                             L2 ← Terraform, Ansible, Pulumi
├── observability/                   L2 ✅ — Prometheus, Grafana, ELK, Datadog
├── configuration-management/        L2
├── container-registry/              L2 ← Docker-Hub, Harbor, ECR
├── service-mesh/                    L2 ← Istio, Linkerd
├── gitops/                          L2 ← ArgoCD, Flux
│
└── _glossary.md                     ← thuật ngữ DevOps chung (riêng L2 vẫn có glossary)
```

> 📌 **Đọc cấu trúc**: thư mục có prefix `_` (như `_notes/`, `_concepts/`, `_glossary.md`) là **L1-level meta** — áp dụng cho cả L1. Thư mục không có `_` (như `docker/`, `kubernetes/`) là **L2 chủ đề con** — có cấu trúc 7 loại riêng bên trong.

> Chi tiết L3-L4 `kubernetes/` → xem [§3.2](#32-10_devops--kubernetes---chi-tiết-l3-l4)

---

### 2.11 `11_Cloud`

Cloud platforms.

```
11_Cloud/
├── README.md
├── 00_overview.md
├── cloud-fundamentals/              ← region, zone, IAM concepts
├── aws/
├── gcp/
├── azure/
├── digitalocean/
├── cloudflare/
├── multi-cloud-strategies/
├── serverless/                      ← Lambda, Cloud-Functions, Cloud-Run
├── cloud-cost-management/
└── _glossary.md
```

---

### 2.12 `12_Security`

Bảo mật.

```
12_Security/
├── README.md
├── 00_overview.md
├── owasp-top-10/
├── authentication/                  ← OAuth, JWT, OIDC, SAML
├── authorization/                   ← RBAC, ABAC, ACL
├── cryptography/                    ← symmetric, asymmetric, hashing
├── tls-ssl/
├── pentesting-fundamentals/
├── cloud-security/
├── container-security/              ← image scanning, runtime security
├── secrets-management/              ← Vault, sealed-secrets
├── compliance/                      ← GDPR, HIPAA, SOC2
└── _glossary.md
```

---

### 2.13 `13_AI-ML`

Trí tuệ nhân tạo & học máy.

```
13_AI-ML/
├── README.md
├── 00_overview.md
├── math-for-ml/                     ← linear algebra, calculus, probability
├── ml-fundamentals/                 ← regression, classification, clustering
├── deep-learning/                   ← neural networks, CNN, RNN
├── nlp/
├── computer-vision/
├── llm/                             ← transformer, GPT, Claude, ...
├── rag-and-ai-agent/                ← retrieval, agent frameworks
├── fine-tuning-and-training/
├── mlops/                           ← model deployment, monitoring
├── vector-search-and-embeddings/
└── _glossary.md
```

---

### 2.14 `14_Data-Engineering`

Kỹ thuật dữ liệu.

```
14_Data-Engineering/
├── README.md
├── 00_overview.md
├── etl-elt/
├── data-warehouse/                  ← Snowflake, BigQuery, Redshift
├── data-lake/                       ← S3, Delta Lake, Iceberg
├── streaming/                       ← Kafka, Pulsar, Kinesis
├── spark/
├── airflow-and-orchestration/
├── dbt/
├── data-modeling/
├── real-time-analytics/
└── _glossary.md
```

---

### 2.15 `15_Specialized`

Các mảng chuyên biệt.

```
15_Specialized/
├── README.md
├── 00_overview.md
├── game-dev/                        ← Unity, Unreal, Godot
├── embedded-iot/                    ← Arduino, Raspberry Pi, ESP32, IoT protocols
├── blockchain/                      ← Bitcoin, Ethereum, smart contracts
├── quantum-computing/
├── ar-vr/
├── robotics/
└── _glossary.md
```

---

### 2.16 `16_Career-Soft-skills`

Kỹ năng nghề nghiệp & soft skills cho dân CNTT.

```
16_Career-Soft-skills/
├── README.md
├── 00_overview.md
├── communication/                   ← viết email, viết PR, present
├── agile-scrum/                     ← framework, ceremony, role
├── career-path/                     ← Intern → Junior → Senior → Lead → Architect/Manager
├── learning-how-to-learn/           ← học cách học, kỹ thuật ghi nhớ
├── technical-writing/               ← viết doc, README, blog kỹ thuật
├── interview-prep/                  ← coding interview, system design
├── remote-work/                     ← async, time zone, virtual collaboration
├── time-management/
└── _glossary.md
```

---

## 3️⃣ Chi tiết L3 — 3 chủ đề ưu tiên

### 3.1 `00_Roadmaps` — chi tiết L3

#### 🧭 Career roadmap (`career/`)

Lộ trình theo nghề. Mỗi file là kịch bản học **6-12 tháng** cho 1 vai trò. Template ở `06_roadmap-design.md`.

| File | Đối tượng | Đi qua các L1 chính |
|---|---|---|
| `zero-to-coder_career-roadmap.md` | Người chưa biết gì | `02_Tools` → `01_Foundations` → `03_Languages` (chọn 1) |
| `backend-developer_career-roadmap.md` | Backend dev | Tools → Languages → OS → DB → Networking → Web (backend) → DevOps |
| `frontend-developer_career-roadmap.md` | Frontend dev | Tools → Languages (JS/TS) → Web (frontend) → DevOps (CI/CD) |
| `fullstack-developer_career-roadmap.md` | Full-stack | Tools → Languages → DB → Web (full) → DevOps |
| `mobile-developer_career-roadmap.md` | Mobile dev | Tools → Languages (Swift/Kotlin/Dart) → Mobile → Architecture |
| `devops-engineer_career-roadmap.md` | DevOps | Tools → OS (Linux) → Networking → DevOps → Cloud → Security |
| `sre-engineer_career-roadmap.md` | SRE | OS → Networking → DevOps (Observability) → Cloud → Architecture (distributed) |
| `platform-engineer_career-roadmap.md` | Platform | DevOps (K8s + IaC) → Cloud → Architecture → Security |
| `cloud-engineer_career-roadmap.md` | Cloud | Networking → OS → Cloud → DevOps → Security |
| `data-engineer_career-roadmap.md` | Data Eng | Languages (Python/SQL) → DB → Data-Engineering → Cloud |
| `data-scientist_career-roadmap.md` | Data Sci | Foundations (Math) → Languages (Python/R) → AI-ML → Data-Engineering |
| `ml-engineer_career-roadmap.md` | ML Eng | Languages → AI-ML → DevOps → Data-Engineering → Cloud |
| `ai-engineer_career-roadmap.md` | AI/GenAI Eng | Languages → AI-ML (LLM/RAG/Agent) → Web (backend) → Cloud |
| `security-engineer_career-roadmap.md` | Security | OS → Networking → Security → Cloud → DevOps |
| `qa-engineer_career-roadmap.md` | QA/Test | Languages → Web → DevOps (CI/CD) → testing tools |
| `game-developer_career-roadmap.md` | Game dev | Languages (C++/C#) → Foundations (Math) → Specialized (Game) |
| `blockchain-developer_career-roadmap.md` | Blockchain | Languages → Cryptography (Security) → Specialized (Blockchain) |

#### 🧪 Lab series (`lab-series/`)

Chuỗi bài tập thực hành nhiều stage, có thứ tự cố định, xuyên qua nhiều L2. Mỗi file là 1 *playbook* link tới các `lessons/`, `exercises/`, `projects/` cụ thể.

| File | Phạm vi | Stage |
|---|---|---|
| `docker-to-k8s_lab-series.md` | Docker → K8s → Helm → GitOps → Service Mesh | 50 bài, ~3-4 tuần |
| `full-stack-web-app_lab-series.md` | Frontend (React) → Backend (FastAPI) → DB (Postgres) → Deploy (Docker) | ~2-3 tuần |
| `home-lab-self-hosted_lab-series.md` | Linux server → Docker → reverse proxy → monitoring | ~1-2 tuần |
| `python-zero-to-production_lab-series.md` | Python basics → Flask app → Test → Deploy | ~2 tuần |

##### Cấu trúc 1 file lab-series

```markdown
# Lab Series: Docker → K8s

> **Stage 1: Docker basics** (~3 ngày, 8 bài)
> 📍 Vào [`10_DevOps/docker/lessons/01_basic/`](../../10_DevOps/docker/lessons/01_basic/)
> 📍 Hoàn thành: [`docker/projects/01_python-app-docker/`](../../10_DevOps/docker/projects/01_python-app-docker/)

> **Stage 2: Docker runtime & networking** (~4 ngày, 9 bài)
> 📍 Vào [`docker/lessons/02_intermediate/`](../../10_DevOps/docker/lessons/02_intermediate/)
> 📍 Hoàn thành: [`docker/projects/02_flask-web-app/`](../../10_DevOps/docker/projects/02_flask-web-app/)

> **Stage 3: K8s basics** (~5 ngày)
> ⚠️ Prerequisite: source code từ Stage 2 — clone `<repo>` hoặc tự build theo Bài 24
> 📍 Vào [`kubernetes/setup/minikube.md`](../../10_DevOps/kubernetes/setup/minikube.md)
> 📍 Sau đó [`kubernetes/lessons/01_basic/`](../../10_DevOps/kubernetes/lessons/01_basic/)
> 📍 Hoàn thành: [`kubernetes/projects/01_first-pod/`](../../10_DevOps/kubernetes/projects/01_first-pod/)

(tiếp các stage 4-7)
```

> Quy ước chung: **mọi roadmap (cả 2 loại) chỉ link tới chủ đề L1/L2, không lặp nội dung** (DRY).

---

### 3.2 `10_DevOps` → `kubernetes/` — chi tiết L3-L4

Áp dụng menu 7 loại nội dung (xem §0.2). K8s đủ lớn → dùng cả 7 loại.

```
kubernetes/
├── README.md                            ← index toàn chủ đề K8s
├── 00_overview.md                       ← K8s là gì, vì sao K8s, vs Docker Swarm
│
├── lessons/                             📖 BÀI HỌC LÝ THUYẾT
│   ├── README.md                        ← danh mục bài theo level
│   ├── 01_basic/
│   │   ├── 00_architecture.md           ← Control Plane vs Node
│   │   ├── 01_pod.md                    ✅ _Ref/K8s/8_Pod-la-gi-Demo-kubectl.md
│   │   ├── 02_replicaset.md             ✅
│   │   ├── 03_deployment.md             ✅
│   │   ├── 04_service.md                ✅
│   │   ├── 05_namespace.md              ✅
│   │   ├── 06_yaml-manifest.md          ✅
│   │   ├── 07_kubectl-basics.md
│   │   └── 08_imperative-vs-declarative.md  ✅ _Ref/K8s/13_*
│   ├── 02_intermediate/
│   │   ├── 00_configmap-and-secret.md
│   │   ├── 01_volume-and-pvc.md
│   │   ├── 02_ingress.md
│   │   ├── 03_networking.md             ← CNI, Service types, kube-proxy
│   │   ├── 04_statefulset.md
│   │   ├── 05_daemonset.md
│   │   ├── 06_job-and-cronjob.md
│   │   ├── 07_resource-management.md    ✅ _Ref/K8s-training/Module-11
│   │   ├── 08_health-checks.md          ← liveness, readiness, startup
│   │   └── 09_rolling-update-and-rollback.md
│   └── 03_advanced/
│       ├── 00_rbac.md
│       ├── 01_network-policy.md
│       ├── 02_pod-security.md
│       ├── 03_operator-pattern.md
│       ├── 04_custom-resource-definition.md
│       ├── 05_helm-basics.md            ← link tới gitops/ cho ArgoCD
│       ├── 06_kustomize.md
│       ├── 07_admission-controllers.md
│       ├── 08_autoscaling.md            ← HPA, VPA, Cluster Autoscaler
│       └── 09_monitoring-k8s.md         ← link chéo observability/
│
├── setup/                               ⚙️ CÀI ĐẶT MÔI TRƯỜNG K8s
│   ├── README.md                        ← so sánh các option
│   ├── 00_overview.md
│   ├── minikube.md                      ← local dev
│   ├── kind.md                          ← local, container-based
│   ├── docker-desktop.md                ← built-in K8s
│   ├── k3s.md                           ← lightweight
│   ├── kubeadm-cluster.md               ← self-managed cluster
│   └── managed-eks-gke-aks.md           ← cloud-managed
│
├── exercises/                           🧪 BÀI TẬP NHỎ (luyện 1 khái niệm)
│   ├── README.md                        ← danh mục bài tập + độ khó
│   ├── 01_create-first-pod.md           ← luyện Pod
│   ├── 02_scale-deployment.md           ← luyện Deployment scale
│   ├── 03_expose-service.md             ← luyện Service
│   ├── 04_configmap-injection.md        ← luyện ConfigMap
│   ├── 05_pvc-mount.md                  ← luyện Volume
│   ├── 06_ingress-routing.md
│   ├── 07_rolling-update.md
│   └── ...
│
├── projects/                            🎯 TÌNH HUỐNG LỚN nhiều bước
│   ├── README.md                        ← danh mục project + prerequisite
│   ├── 01_first-pod/                    ← Bài 25-30 trong docker-k8s-practice
│   ├── 02_multi-tier-app/               ← Bài 31-38 — ⚠️ nhận source từ docker/projects/03_compose-multi-tier
│   ├── 03_stateful-and-helm/            ← Bài 39-41
│   ├── 04_helm-deep/                    ← Bài 42-44 (Helm template advanced)
│   └── ... (ArgoCD ở gitops/, Istio ở service-mesh/)
│
├── recipes/                             📚 CÔNG THỨC / TÌNH HUỐNG XỬ LÝ
│   ├── README.md
│   ├── troubleshooting/
│   │   ├── pod-crashloopbackoff.md
│   │   ├── image-pull-errors.md
│   │   ├── pending-pod.md
│   │   ├── networking-issues.md
│   │   └── pvc-not-bound.md
│   ├── patterns/
│   │   ├── blue-green-deployment.md
│   │   ├── canary-deployment.md
│   │   ├── sidecar-pattern.md
│   │   └── init-container-pattern.md
│   └── operations/
│       ├── backup-and-restore.md
│       ├── cluster-upgrade.md
│       └── disaster-recovery.md
│
├── 99_cheatsheet.md                     ⚡ kubectl + YAML reference
└── _glossary.md                         📘 Pod, Node, Deployment, CRD, ...
```

**Migration plan từ `_Ref/`:**

| Nguồn `_Ref/` | Đích trong kho mới | Ghi chú |
|---|---|---|
| `_Ref/K8s/8_Pod-la-gi-Demo-kubectl.md` | `lessons/01_basic/01_pod.md` | Refactor theo 8-section template |
| `_Ref/K8s/13_Imperative-vs-Declarative.md` | `lessons/01_basic/08_imperative-vs-declarative.md` | Chỉ cần chuẩn lại header |
| `_Ref/K8s-training/Module-11/*` | `lessons/02_intermediate/07_resource-management.md` | Gộp, refactor |
| `_Ref/Project-K8s-test/` | `projects/01_first-pod/` | Refactor làm project mẫu |
| `_Ref/kubernetes-visual-guide.md` | Tách: phần overview → `00_overview.md`, diagrams → các bài lý thuyết tương ứng | Visual-guide nên phân tán |

**Cross-L2 reference cho project `02_multi-tier-app/`:**

```markdown
# Project 02 — Multi-tier App trên K8s

> **Prerequisite — Lấy source từ Docker:**
> - Bạn cần image `myapp:6.0` đã build ở [`../../docker/projects/03_compose-multi-tier/`](../../docker/projects/03_compose-multi-tier/) (Bài 24, sau khi push lên registry).
> - **Hoặc** clone repo mẫu: `git clone https://github.com/your-username/myapp-source`
> - **Hoặc** build app mới: làm theo `docker/lessons/01_basic/` rồi quay lại đây.

(rồi nội dung project bắt đầu)
```

---

### 3.3 `04_OS` → `linux/` — chi tiết L3-L4

Áp dụng menu 7 loại. Linux dùng đủ 7.

```
linux/
├── README.md
├── 00_overview.md                       ← Linux là gì, lịch sử, distro phổ biến
│
├── lessons/                             📖 BÀI HỌC LÝ THUYẾT
│   ├── README.md
│   ├── 01_basic/
│   │   ├── 00_filesystem.md             ← cấu trúc /etc, /var, /home, ...
│   │   ├── 01_navigation.md             ← cd, ls, pwd, find
│   │   ├── 02_file-operations.md        ← cp, mv, rm, mkdir, touch
│   │   ├── 03_permissions.md            ← chmod, chown, umask, sticky bit
│   │   ├── 04_users-and-groups.md       ← useradd, groupadd, /etc/passwd
│   │   ├── 05_text-tools.md             ← cat, less, grep, sed, awk, cut
│   │   ├── 06_processes.md              ← ps, top, htop, kill, nice
│   │   ├── 07_io-redirection.md         ← stdin, stdout, stderr, pipe, tee
│   │   └── 08_package-management.md     ← apt, yum, dnf, pacman
│   ├── 02_intermediate/
│   │   ├── 00_systemd.md                ← service, unit file, journalctl
│   │   ├── 01_cron-and-timers.md
│   │   ├── 02_networking-linux.md       ← ip, ss, netstat, iptables, nftables
│   │   ├── 03_disk-and-filesystem.md    ← df, du, mount, fdisk
│   │   ├── 04_logs.md                   ← /var/log, journalctl
│   │   ├── 05_ssh.md                    ← ssh, scp, rsync, ssh-keygen
│   │   ├── 06_shell-scripting-intro.md  ← link chéo 02_Tools/shell/
│   │   ├── 07_environment-variables.md  ← PATH, env, export, .bashrc
│   │   └── 08_archive-and-compress.md   ← tar, gzip, zip
│   └── 03_advanced/
│       ├── 00_kernel-modules.md
│       ├── 01_namespaces-and-cgroups.md ← nền tảng container
│       ├── 02_selinux-apparmor.md
│       ├── 03_performance-tuning.md     ← sysctl, /proc, /sys
│       ├── 04_strace-and-debug.md       ← strace, ltrace, gdb
│       ├── 05_lvm.md                    ← logical volume manager
│       ├── 06_raid.md
│       ├── 07_iptables-deep-dive.md
│       └── 08_kernel-tuning.md
│
├── setup/                               ⚙️ CÀI ĐẶT (mỗi distro 1 file)
│   ├── README.md                        ← so sánh các distro
│   ├── 00_overview.md
│   ├── ubuntu.md                        ← cài Ubuntu (desktop/server)
│   ├── debian.md
│   ├── arch-linux.md
│   ├── fedora.md
│   ├── alpine.md                        ← dùng cho container
│   ├── wsl.md                           ← Linux trên Windows
│   └── dual-boot.md                     ← cài kèm với Windows/Mac
│
├── exercises/                           🧪 BÀI TẬP NHỎ
│   ├── README.md
│   ├── 01_find-large-files.md           ← tìm file > 1GB
│   ├── 02_set-up-cronjob.md             ← lập cron backup
│   ├── 03_create-systemd-service.md
│   ├── 04_setup-ssh-key.md
│   ├── 05_grep-awk-log-analysis.md
│   ├── 06_iptables-firewall.md
│   └── ...
│
├── projects/                            🎯 TÌNH HUỐNG LỚN
│   ├── README.md
│   ├── 01_personal-server-setup/        ← cài VPS từ A → Z: SSH, firewall, user, fail2ban
│   ├── 02_backup-system/                ← cron + rsync + remote backup
│   ├── 03_monitoring-stack/             ← Node Exporter + Grafana local
│   └── 04_home-lab-network/             ← static IP + DNS + DHCP setup
│
├── recipes/                             📚 CÔNG THỨC / TROUBLESHOOTING
│   ├── README.md
│   ├── troubleshooting/
│   │   ├── disk-full.md
│   │   ├── high-cpu-load.md
│   │   ├── network-not-working.md
│   │   ├── ssh-connection-refused.md
│   │   └── boot-failure.md
│   ├── patterns/
│   │   ├── rotate-log-files.md
│   │   ├── secure-ssh-server.md
│   │   └── auto-mount-on-boot.md
│   └── one-liners/
│       ├── text-processing.md           ← awk/sed magic
│       ├── system-info.md
│       └── network-debug.md
│
├── 99_cheatsheet.md                     ⚡ lệnh Linux cheatsheet
└── _glossary.md                         📘 inode, daemon, kernel, ...
```

---

## 4️⃣ Hướng dẫn mở rộng sitemap

### Khi nào thêm chủ đề mới

| Tình huống | Hành động |
|---|---|
| Có **subtopic** mới trong L1 đã có | Thêm L2 mới trong L1 đó, không cần đụng sitemap tổng. Áp dụng menu 7 loại (§0.2) |
| Có **chủ đề lớn** không khớp L1 nào | Tạo L1 mới (#17, #18...) — nhớ giữ chỗ #08-#89 vẫn còn nhiều |
| Career roadmap mới (vd: blockchain-engineer) | Thêm file mới trong `00_Roadmaps/career/`, link tới L1 tương ứng |
| Lab series mới (chuỗi thực hành xuyên chủ đề) | Thêm file mới trong `00_Roadmaps/lab-series/`, link tới các project ở L2 tương ứng |
| Có **loại nội dung mới** chưa nằm trong 7 loại | Đề xuất bổ sung menu trong `02_folder-structure.md` trước, rồi mới triển khai |

### Quy tắc đánh số L1 mới

- Số tiếp theo theo thứ tự (`17_`, `18_`, ...) — KHÔNG chèn vào giữa số đã dùng
- Đặt vào group ngữ nghĩa phù hợp (Nền tảng / Ngôn ngữ / Hệ thống / Ứng dụng / Vận hành / Chuyên sâu / Nghề nghiệp)
- Cập nhật mermaid + bảng tổng quan trong file này
- Cập nhật `_idea-overview.md` (bảng L1) + bump version

---

## 📌 Changelog

- **v0.4.0 (15/05/2026)** — **SSOT cleanup**. Slim §0.2 (menu 7 loại), §0.3 (cross-L2), §0.4 (L1 meta slots), §2.0 (Roadmaps) — giữ tóm tắt + link tới canonical owner (`02_folder-structure.md`, `05_linking-strategy.md`, `06_roadmap-design.md`). Mục đích: tránh drift khi sửa.
- **v0.3.0 (15/05/2026)** — Bổ sung sau góp ý: không phải mọi nội dung đều fit vào L2 — có những thứ thật sự cross-L2.
  - Thêm §0.3 case B (project xuyên L2 không tách được) → đặt ở `<L1>/_capstone-projects/`.
  - Thêm §0.3 case C (ghi chú & khái niệm xuyên L2) → đặt ở `<L1>/_notes/` và `<L1>/_concepts/`.
  - Thêm §0.4 **L1-level meta slots** — formalize prefix `_` ở L1 để phân biệt meta-content với L2 con.
  - Thêm §0.5 **L2 menu mở rộng** — 7 loại lõi + 5 loại bổ sung khi cần (`references/`, `interview-questions/`, `case-studies/`, `migration-guides/`, `tools-comparison/`).
  - Update §2.10 (DevOps) thể hiện L1-level slots trong cây thư mục.
- **v0.2.0 (15/05/2026)** — Tinh chỉnh sau khi phát hiện cấu trúc cũ chỉ thể hiện được lý thuyết. Thay đổi lớn:
  - Thêm **menu 7 loại nội dung** (lessons/setup/exercises/projects/recipes/cheatsheet/glossary) — áp dụng cho L2 mọi chủ đề (xem §0.2).
  - Tách `00_Roadmaps/` thành 2 loại: **career roadmap** (`career/`) và **lab series** (`lab-series/`) — phục vụ chuỗi bài tập xuyên chủ đề như `docker-k8s-practice.md` của user.
  - Thêm **quy ước cross-L2** (§0.3): mỗi L2 tự sở hữu projects, trỏ ngược L2 khác bằng link + hướng dẫn sơ bộ. Không tạo cross-L2 `projects/` folder.
  - Viết lại §3.2 (kubernetes) và §3.3 (linux) theo cấu trúc 7 loại.
  - Đổi mô hình level: L3 giờ là *loại nội dung*, L4 là file/folder cụ thể trong loại đó.
- **v0.1.0 (15/05/2026)** — Bản đầu tiên. Sitemap L1 → L2 cho toàn bộ 16 chủ đề + Roadmaps. L3 chi tiết cho 3 chủ đề ưu tiên: `00_Roadmaps`, `10_DevOps/kubernetes/`, `04_OS/linux/`. Kèm migration plan từ `_Ref/`. *(Cấu trúc cũ chỉ có lessons theo level basic/intermediate/advanced — đã được thay thế ở v0.2.0)*
