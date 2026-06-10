# 🚧 Work-In-Progress Tracker

> **Tác giả:** Mr.Rom (+ Claude maintain)\
> **Phiên bản:** v0.65.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 11/06/2026

> 🎯 *Lịch sử các việc đang dở, chưa xong, hoặc đang chờ làm rõ — để khi user/Claude switch task vẫn nhớ quay lại.*

---

## 📌 Cách dùng file này

| Khi nào | Hành động |
|---|---|
| Bắt đầu task mới | Thêm vào `🔥 Đang làm` (hoặc `📋 Backlog` nếu chưa làm ngay) |
| Pause giữa chừng (chuyển task khác) | Cập nhật "next step" + để ở `🔥 Đang làm` |
| Bị block (chờ user quyết) | Move sang `🚨 Blocked` với lý do |
| Xong hoàn toàn | Move sang `✅ Done gần đây`, để lại 3-7 ngày rồi xoá |
| Bỏ luôn | Xoá hẳn + ghi note vào changelog |

**Quy ước item entry:**
```
- [ ] <Title>
  - 📅 Started: YYYY-MM-DD
  - 📍 Last update: YYYY-MM-DD
  - 🎯 Next step: <cụ thể bước tiếp theo>
  - 🚨 Blocker (nếu có): <cần gì để unblock>
  - 📁 Files đang đụng: <list>
```

---

## 🔥 Đang làm (current)

- [ ] **PHASE: Review sâu từng bài (per-cluster QA) + góp ý blueprint**
  - 📅 Started: 01/06/2026
  - 📍 Last update: 01/06/2026
  - ✅ Đã xong (chuẩn bị): blueprint review + áp 3 quyết định (changelog tăng dần / heading Việt-hoá canonical / bỏ ước tính thời gian) lên 34 file blueprint + **sweep cơ học toàn kho** (257 heading Changelog/Glossary + 111 changelog đảo tăng dần + **521 H2 framework + 410 H3 Pitfall → canonical**, 0 trùng, 0 mất nội dung) + **docker re-align xong** (bản tham chiếu sạch).
  - ✅ **11_cloud DONE 56/56 (01/06)** — audit 145 findings → rewrite Việt-hoá (cụm agent-written bị "điện tín EN") + fix code/factual + heading/nav/Glossary canonical. **0 telegraphic-EN, 0 artifact, 0 cụt, 56/56 changelog 01/06.** Bài học: workflow rewrite có schema phức tạp → agent kiệt budget không trả StructuredOutput; dùng **workflow schema-free + verify cơ học (grep)** ổn định hơn. Artifact tool-call lọt file → phải grep dọn sau mỗi batch (verify-agent bỏ sót).
  - ✅ **PHIÊN 07/06 — "1 lược" review toàn kho DONE phần agent-written + convention-sync:**
    - **Convention-sync toàn kho** (mechanical, verified, 0 file hỏng): de-meta gỡ 342 link `_blueprint`/101 file; nav canonical (🧭/🧩/🌐 + ⬅️/➡️/↑ + link-text=H1) ~170 file, 0 nav cũ; bỏ ước-tính-thời-gian lessons + 18 roadmap; broken-link 70→~0 thật (11 false-positive checker đọc code trong fence — **checker cần fix fence-blind**).
    - **iac + observability**: rewrite "điện tín EN"→tiếng Việt (8 file).
    - **README** html-css + javascript-dom (cụm đã xong nhưng còn skeleton) → v1.0.0.
    - **12_security + 13_ai-ml audit+fix** (46 findings): **owasp-top-10 restructure sang OWASP Top 10:2025** (verified web, final release — A02 lên #2, A03 Supply Chain mới, A10 Mishandling mới, SSRF gộp A01) + fix code/factual (JWT PUBLIC_KEYS→jwks_client, argon2 verify try/except, IBM $4.88M, PBKDF2 OWASP-not-NIST, SLSA L4, qdrant query_points, json imports) + dọn artifact "là gì? là gì" ở stub.
  - 🎯 Next step: **content-audit cụm VIẾT TAY** (foundations/languages/os/networking/06_db/rest-10_devops/mobile/arch/14_data/15/16) — đã review nội dung trước + conventions synced + telegraphic=0, nhưng chưa audit code/factual phiên này. Tuỳ user: audit kỹ hay chấp nhận prior-review.
  - 📁 Scripts tái dùng: `_workspace/_rewrite-generic.js`, `_fix-secai.js`, `/tmp/nav_canonical.py`, `/tmp/strip_time.py`, `/tmp/strip_roadmap_time.py`
  - ⚠️ Quyết định chốt: heading **canonical nghiêm ngặt 1:1**; **bỏ HẾT ước tính thời gian kể cả roadmap stage-duration**; rewrite dùng **schema-free workflow + grep verify cơ học** (schema phức tạp → agent kiệt budget, lỗi StructuredOutput). Verify-agent KHÔNG đáng tin bắt artifact → luôn grep cơ học sau batch.

---

## 📋 Backlog (planned, chưa làm)



### Lesson series tiếp theo (sau PostgreSQL basic)
- 📅 Added: 20/05/2026 — updated: 23/05/2026
- 💡 Candidates (priority cao):
  - HTTP intermediate (`05_networking/http-https/02_intermediate/`) — CORS deep, JWT advanced, caching, HTTP/3
  - SQL intermediate (`06_databases/sql-fundamentals/02_intermediate/`) — subquery, CTE, window functions
  - Redis (`06_databases/redis/`) — cache + pub/sub, có __Ref__ content sẵn
  - MongoDB (`06_databases/mongodb/`) — document NoSQL, có __Ref__ content sẵn
  - FastAPI intermediate (`07_web/backend/python-fastapi/02_intermediate/`) — testing, WebSocket, deploy
  - K8s basic (`10_devops/kubernetes/`) — devops/sre/platform roadmap
  - Build tools (`07_web/frontend/build-tools/`) — Vite deep, esbuild
  - Load balancing (`05_networking/load-balancing/`) — Nginx + HAProxy
  - HTTP intermediate (`05_networking/http-https/02_intermediate/`) — CORS deep, JWT advanced, caching, HTTP/3
  - Load balancing (`05_networking/load-balancing/`) — Nginx + HAProxy + cloud LB
  - SQL intermediate (`06_databases/sql-fundamentals/02_intermediate/`) — subquery, CTE, window functions
  - PostgreSQL specific (`06_databases/postgresql/`) — backend-dev Stage 3
  - FastAPI intermediate (`07_web/backend/python-fastapi/02_intermediate/`) — testing, WebSocket, deploy
  - K8s basic lessons (`10_devops/kubernetes/`) — devops/sre/platform roadmap
- 🎯 Cần user pick priority cho cluster kế tiếp

### Phase 3: Lab Series
- 📅 Added: 20/05/2026
- 🎯 Khi làm: viết 4 lab series ở `00_roadmaps/lab-series/`:
  - `docker-to-k8s_lab-series.md` (50 bài)
  - `full-stack-web-app_lab-series.md`
  - `home-lab-self-hosted_lab-series.md`
  - `python-zero-to-production_lab-series.md`
- ⏳ Dependency: cần Phase 2 lessons xong trước (đặc biệt Docker + K8s + FastAPI + React)

### 💎 Insights cho DevOps Intermediate clusters (captured 24/05/2026)
- 📅 Added: 24/05/2026 (sau audit toàn bộ DevOps basic + mining `__Ref__/`)
- 🎯 Khi mở intermediate cluster, áp dụng các nuggets sau:

**Docker intermediate**:
- Image layer optimization: `--squash`, multi-stage advanced, distroless base image
- BuildKit features: cache mounts, secret mounts, bake
- Image security: Trivy/Snyk scan, SBOM, signed images (cosign)

**Kubernetes intermediate**:
- **NetworkPolicy CNI dependency** — chỉ work với Calico/Cilium, không Minikube default. War story team enforce policy → break tất cả deployment vì Istio webhook bị block (`__Ref__/legacy-archive/MINIKUBE-LOCAL-TIPS.md §12,17`)
- **Resource limits trên Minikube** — node capacity hết nhanh trên local; show calculation (3 replicas × 512Mi = 1.5GB)
- **Cross-namespace ServiceMonitor** — Prometheus không auto-scrape across namespace nếu thiếu `namespaceSelector`
- **PDB conflict HPA** — autoscale evict pod, PDB block, cascade timeout
- **TTL on Jobs/CronJobs** — completed pods sweep tránh bloat etcd

**CI/CD intermediate**:
- **GitOps anti-pattern**: team dùng ArgoCD nhưng SRE còn `kubectl apply` thủ công → drift, ArgoCD revert 3 phút sau, không audit trail (`__Ref__/legacy-archive/GitOps-practices_Ref.md`)
- **Docker Compose v1 vs v2 hell**: `docker compose` vs `docker-compose` khác biệt trong CI script
- **12-factor violations**: hardcode DB credential trong Dockerfile (factor 3), session data trong container (factor 6), write log to disk (factor 11)
- **Environment parity check** pattern — CI ensure staging match prod (cùng secret structure, log target, resource limit)

**Observability intermediate**:
- **Postmortem blameless template**: Summary → Timeline UTC → Root Cause → Contributing Factors → Action Items với owner/date. Ví dụ: "DB connection leak in error path" (code bug) + "no connection pool alert" (process gap)
- **On-call rotation pattern**: max 1 tuần, min 2 tuần off; runbook common alerts; reduce toil (≥1 task automate/quarter); escalate nếu không resolve trong 30p
- **Alert on saturation (connection pool %) — không chỉ utilization**: với war story cụ thể
- **Multi-window burn rate alerts**: short (5m, fast burn) + long (1h, slow burn) → giảm alert fatigue

**IaC intermediate**:
- **GitOps "Git as enforcement gate"**: merge = deploy signal. Cấm `kubectl apply` trực tiếp
- **Drift detection workflow**: CI cron schedule chạy `terraform plan` định kỳ, alert nếu diff
- **Sealed Secrets vs Vault**: rule "không commit plaintext secret"
- **State migration pattern**: `terraform state mv` khi refactor module

**Cross-cutting metaphors** (chưa apply):
- "Container as shipping container" (logistics angle) — bổ sung Lego metaphor ở Docker 00
- "Git = single source of truth" — bổ sung GitOps intro
- "Production system as patient" cho observability (vital signs = metrics, EKG = traces)

→ **Sources**: `10_devops/__Ref__/legacy-archive/{MINIKUBE-LOCAL-TIPS.md, SRE-practices_Ref.md, GitOps-practices_Ref.md, docker-k8s-practice.md, 12-factor-app_Ref.md}`

### __Ref__ improvements candidates (cherry-pick khi rảnh)
- 📅 Added: 21/05/2026
- 💡 Content có sẵn trong `__Ref__/` có thể nâng:
  - **Python** (`03_languages/python/__Ref__/python_from_05Languages/`): có `01-python-basics`, `02-python-advanced`, `03-packaging-setup`, `04-testing-practices`, `05-performance-practices`, `06-cheatsheet`
    - → Cherry-pick cho lessons mới: `04_io-and-files`, `05_modules-and-packages`, `06_error-handling` + tạo `_cheatsheet.md`
  - **Linux** (`04_os/linux/__Ref__/linux/`): có `01-essentials-basics`, `02-administration-advanced`, `03-networking-advanced`
    - → Cherry-pick cho `lessons/02_intermediate/` (systemd, ssh, networking)
  - **Docker** (`10_devops/docker/__Ref__/`): có `_Draft_Syntax.md`, `from_06_DevOps_docker/_quizzes/`, `_projects/simple-webapp-dockerized`
    - → Cherry-pick cho `exercises/` (quiz), `projects/` (webapp), `_cheatsheet.md`
  - **Shell/terminal** (`02_tools/terminal-emulators/__Ref__/`): có `02-bash-scripting-basics`, `04-vim-neovim-basics`, `03-shell-tools-cheatsheet`
    - → Cherry-pick cho `02_tools/shell/lessons/01_basic/` lessons mới (bash scripting, vim intro)
  - **Git** (`01_foundations/version-control/__Ref__/git_*`): đã có nội dung tham khảo — git bộ đã viết v2.0.0, có thể bổ sung lesson `05_rebase-cherrypick` nếu cần
- 🎯 KHÔNG ưu tiên — Phase 2 chính trước. Note để khỏi quên.

---

## ✅ Done gần đây (3-7 ngày)

### 11/06/2026 (Việt hoá heading nội dung cụm agent-written + dọn nốt)

> User chọn "Việt hoá heading nội dung" sau khi mechanical polish xong. Nguyên tắc: **dịch heading MÔ TẢ sang tiếng Việt, GIỮ thuật ngữ/brand/param tiếng Anh** (conservative — phân vân thì giữ EN). Theo §3.7 Vietnamese-first. Làm cụm LLM trước làm mẫu → user duyệt calibration → nhân ra 6 cụm còn lại (mỗi cụm 1 agent + 1 commit riêng).

- ✅ **Việt hoá ~880 heading mô tả qua 7 cụm** (heading EN ~1,430 → 218 còn lại, đều là thuật ngữ/brand giữ chủ ý). Commit riêng từng cụm:
  - `13_ai-ml/llm` (5 bài, ~150) — commit 21e9ab7 — mẫu calibration.
  - `12_security/owasp-top-10` (77) — b090b8d.
  - `12_security/authentication` (99) — 860d217.
  - `10_devops/iac` (~100, 4 bài basic; intermediate đã VN sẵn) — c8ff648.
  - `10_devops/kubernetes` (101, 4 bài intermediate; basic đã VN sẵn) — ac21190.
  - `10_devops/observability` (~166, 7 bài) — 06d1171.
  - `10_devops/ci-cd` (~240, 9 bài) — 419e063.
  - GIỮ: brand (OpenAI/Anthropic/ArgoCD/Prometheus/Grafana/Keycloak/Terraform...), thuật ngữ (Zero-shot/Few-shot/JWT/OAuth/PKCE/SLSA/cosign/PromQL/SLO/error budget/Pod/Helm/CRD/state/drift...), param/identifier (Top-k/Max tokens/reclaimPolicy/values-*.yaml...). Verify: fence cân bằng toàn bộ, edit chỉ chạm heading (+ vài bold-label/code-comment lẻ, hợp §3.7).
- ✅ **Cheatsheet heading canonical** — `## ⚡ Cheatsheet` / `📋 Bảng Tra Cứu Nhanh (Cheatsheet)` → `## ⚡ Tra cứu nhanh (Cheatsheet)` (27 file, commit b68273e). Đợt sweep trước key theo `📚 Glossary` nên bỏ sót biến thể Cheatsheet.
- ℹ️ **Broken-link checker**: 12 hit đều là **false-positive** (code/regex trong fence + link ví dụ trong block ```markdown ở `_idea-overview.md`) — checker chưa fence-aware. 0 link gãy thật.

### 10/06/2026 (phiên "đánh bóng #2" — sót cơ học + audit nội dung + SƠ ĐỒ)

> Mục tiêu: hoàn tất phần đợt văn phong vừa rồi CHƯA làm (audit nội dung + sơ đồ). Phạm vi user chốt: đánh bóng toàn diện, KHÔNG viết bài mới cho module trống.

- ✅ **Mr.Rom lọt thân bài — sửa TOÀN KHO (audit cũ chỉ bắt 2 file Git, thực tế ~13 file):** 2 lesson + 3 exercise Git (quiz/lab), 4 Python basic (callout/code/summary), **5 K8s basic** (+ chuyển YAML frontmatter → block-quote chuẩn), foundations/computer-architecture, 2 LLM (prompt persona + code comment), helm intermediate (`- name`). Verify repo-wide: thân bài = 0 (chỉ còn ở `Tác giả`/changelog). Bullet `*`→`-` fence-aware cho file đụng.
- ✅ **Sweep canonical còn sót từ đợt trước:** Glossary `📘 Glossary`/`📚 Thuật Ngữ Cần Nhớ`/`📘 …Chuyên Ngành` → `📚 Từ Điển Thuật Ngữ (Glossary)` **70 file**; `**Prerequisites:**` → `**Yêu cầu trước:**` **112 file**; field EN khác (Author/Version/Created/Difficulty) → VN; heading `## 📌 Changelog` cũ → canonical **15 file**.
- ✅ **Sót cơ học khác:** Python 01/02/03 thêm Changelog (thiếu hẳn); 4 LLM gỡ nhãn "(sắp viết)" sai; MASTER-CATALOG Docker "6 bài"→"4 bài + setup + bài tập"; README 14_data-engineering + 15_specialized đổi marker skeleton→🚧 (đã có bài intro); 4 lab Git bỏ field "Thời gian ước tính" (theo template) + thêm Changelog; Azure 00/02/04 thêm Cheatsheet (đồng bộ cụm).
- ✅ **Audit nội dung/factual (phần đợt trước CHƯA làm):** `what-is-shell` sh 1971→**1979** (Bourne shell; 1971 là Thompson); **bảng LIKE trong `01_select-and-filter` viết lại toàn bộ** (pattern + tên placeholder lệch nhau sau đợt bulk-rename Alice→Nguyen Van A — `'D____'` chú "Pham Van D" v.v.) + reorder changelog tăng dần; claim "Opus 4.7+ gỡ temperature/top_p/top_k → effort" **verify bằng skill claude-api = ĐÚNG** (giữ nguyên); time-marker "tính đến 2026" cho giá DigitalOcean/Spaces/Workers/R2 + TLS%; sửa count DigitalOcean ("12 services" vs liệt kê 22); platform note `grep -P` (GNU/macOS `ggrep`) + `scp` deprecated (→ sftp/rsync).
- ✅ **SƠ ĐỒ — bổ sung 18 mermaid (user nhấn mạnh "trực quan"):**
  - 13_ai-ml/llm (trước = 0 sơ đồ): function-calling sequence + agent loop ReAct + RAG 2-pha + tokenization pipeline.
  - 07_web: CSS specificity + flexbox axis + JS event loop + React Virtual DOM diffing.
  - SQL/Git/PG: SELECT logical execution-order + Git merge gitGraph + undo decision-tree + B-tree.
  - K8s/CI-CD/Sec/Cloud: 4 Service types + rolling-update + deploy strategies (Blue-Green/Canary) + STRIDE map + Region/AZ/Edge + VPC 3-tier.
  - Mỗi sơ đồ kèm lead-in + câu phân tích (§3.6). Verify fence cân bằng.
- ✅ **Follow-up (11/06, commit `8554562`):** (1) atlantis nested-fence **ĐÃ FIX** — bọc 2 ví dụ comment GitHub bằng fence 4-backtick (trước đó "Apply complete!" rớt ra ngoài block + 1 block rỗng); 0 file lessons còn fence lẻ. (2) Changelog **giảm dần ĐÃ sweep toàn kho** — đảo 19 bài (git/web/sql/networking) về tăng dần; detector `cl_order.py` = 0 descending / 184 bài có changelog đa-entry.
- ⏳ **Còn defer (theo quyết định user — đánh bóng, KHÔNG viết bài mới):** Coverage gap — 09_architecture 0%, 16_career 0%, nhiều ngôn ngữ (Go/Rust/Java...) + DB (Mongo/Redis/MySQL...) còn trống. Đây là roadmap dài hạn, cần user chốt scope trước khi mở.

### 01/06/2026 (phiên review — blueprint + sweep cơ học + docker re-align)

- ✅ **Blueprint review + áp 3 quyết định** (changelog tăng dần / heading Việt-hoá canonical / bỏ mọi ước tính thời gian) lên 34 file `_blueprint/` + templates + examples. Sync README §5 version table. `_CONCEPT-MAP.md` v1.1.0 (+ concept #31–34). Move `_DOGFOOD-FINDINGS.md` → `_blueprint/_internal/`.
- ✅ **Sweep cơ học toàn kho (in-scope lessons)** — an toàn, verified:
  - 257 file: heading `## 📌 Changelog` → `## 📌 Nhật ký thay đổi (Changelog)`; `## 📚 Glossary` → `## 📚 Từ Điển Thuật Ngữ (Glossary)`.
  - 111 file: changelog đảo **tăng dần** (guard chỉ xử lý changelog thuần entry/note, skip multi-line — an toàn).
  - **521 H2 framework heading** (Self-check/Cheatsheet/Pitfall, mọi biến thể emoji + EN) → **canonical nghiêm ngặt 1:1**. **410 H3 `Pitfall` → `Cạm bẫy`**. Fence-aware. **0 heading trùng, 0 mất nội dung.**
  - KHÔNG đụng heading content đánh số (`## 10. Concurrency Bugs Cheatsheet`, `## 5. Pitfall: Label Design`) — đó là section nội dung, không phải framework.
- ✅ **Docker re-align xong** — 9 heading creative ở basic 01/02/03 + 12 bare EN ở intermediate → canonical. Docker = bản tham chiếu sạch cho phần review còn lại. (00_what-is-docker + 00_intermediate-overview giữ nguyên: intro, dùng FAQ/Tool-stack section, không bắt buộc đủ 8 phần.)
- ⚠️ **Còn lại cho review sâu**: ~10 heading creative free-text (python/k8s) + 78 broken link + content/code/factual QA per-cluster.

### 25/05/2026 (phiên đêm — 11_cloud start)

- ✅ **🎉 Phase 4 11_cloud/cloud-fundamentals COMPLETE 5/5** (5 file 1 turn, **mốc 100 lessons ✨**):
  - File 97: `00_what-is-cloud-computing.md` v1.0.0 → v1.1.0 — 5 lead-in (Bonus models + Stack diagram + Timeline + Market share + Decision matrix)
  - File 98: `01_regions-availability-zones-edge.md` v1.0.0 → v1.1.0 — 5 lead-in (Region structure + Multi-AZ + How CDN + TCP/TLS handshake + Latency tactics)
  - File 99: `02_cloud-networking.md` v1.0.0 → v1.1.0 — 5 lead-in (CIDR planning + Multi-AZ subnet + Why separate DB + How IGW + How NAT)
  - File 100: `03_storage-and-databases.md` v1.0.0 → v1.1.0 — 5 lead-in (Decision matrix + Storage classes + Encryption + S3 features + S3 vs alternatives) ✨ **mốc 100**
  - File 101: `04_cloud-security-and-shared-responsibility.md` v1.0.0 → v1.1.0 — 5 lead-in (Why this matters + Policy example + Encryption everywhere + Compliance frameworks + Compliance as differentiator)
- **11_cloud progress 5/45**: cloud-fundamentals 5/5 ✅. Còn aws/azure/gcp/cloudflare/digitalocean/serverless/multi-cloud/cost-management = 40 file.
- **Phase 4 total: 101/156 (64.7%)**

### 25/05/2026 (phiên tối)

- ✅ **🎉 Phase 4 10_devops/kubernetes/ COMPLETE 10/10** (phiên tối 25/05, 5 file 1 turn + 1 file turn này = 6 file/turn):
  - File 87: `01_basic/00_what-is-kubernetes.md` v1.0.0 → v1.1.0 — 5 lead-in (K8s không phải + K8s là + Docker Compose + Khi nào chọn + Architecture)
  - File 88: `01_basic/01_pods-and-deployments.md` v1.0.0 → v1.1.0 — 5 lead-in (Why Pod + YAML đơn giản + Pod lifecycle + Pitfall + Khi nào dùng raw Pod) + add changelog
  - File 89: `01_basic/04_namespaces-and-rbac.md` v1.0.0 → v1.1.0 — 5 lead-in (§1 Namespaces + Create + Use + namespaced vs cluster + Limit Namespaces) + add changelog
  - File 90: `02_intermediate/02_ingress-cert-manager-tls.md` v1.0.0 → v1.1.0 — 5 lead-in (Install qua Helm + Verify + ingress-nginx vs Traefik vs HAProxy + cert-manager Install + Add annotation)
  - File 91: `02_intermediate/03_statefulset-and-storage.md` v1.0.0 → v1.1.0 — 5 lead-in (Deployment design + StatefulSet design + Bảng so sánh + Headless Service + Concepts PV/PVC)
  - File 92: `02_intermediate/04_autoscaling-and-operators.md` v1.0.0 → v1.1.0 — 5 lead-in (Install metrics-server + HPA basic CPU + VPA Install + Modes + Example)
- ✅ **🎉 observability 10/10** (4 file thêm trong turn):
  - File 93: `01_basic/01_metrics-prometheus.md` v1.0.0 → v1.1.0 — 5 lead-in (Architecture + Data model + Time-series + Labels + Cardinality control)
  - File 94: `01_basic/03_traces-opentelemetry.md` v1.0.0 → v1.1.0 — 5 lead-in (Trace Tree of Spans + Span anatomy + Components + Why OTel + W3C TraceContext)
  - File 95: `01_basic/04_grafana-and-alerting.md` v1.0.0 → v1.1.0 — 5 lead-in (Install K8s + Anatomy + Panel Latency + Variables template + Useful variables)
  - File 96: `02_intermediate/03_opentelemetry-instrumentation.md` v1.0.0 → v1.1.0 — 5 lead-in (Why OTel vs Vendor SDK + Python Auto+manual + Manual span business logic + Node.js + Go)
- **🎉🎉🎉 10_devops COMPLETE 49/49 ✅**: docker 9/9 + ci-cd 10/10 + iac 10/10 + kubernetes 10/10 + **observability 10/10**. Toàn bộ DevOps stack production-grade tier-1 + tier-2 đã apply Blueprint v0.5.4+ §3.6.
- **Phase 4 total: 93/156 (59.6%)**. Tiếp theo: 11_cloud 45 files (0% done) → 12_security 10 → 13_ai-ml 5.

### 25/05/2026

- ✅ **🧹 Tier 2 residue cleanup**: 36 subs across 8 files (`long@example.com` → `nguyenvana@`, `long@vps`/`long@laptop` → `user@*`, `/Users/long` → `/Users/user`, `longshop`/`pg-longshop` → `acmeshop`/`pg-acmeshop`, `psql -U longshop` → `-U acmeshop`). Files: http-methods, what-is-http, ports-sockets, dns-records, psql-meta, what-is-postgresql, ssh-deep-dive, systemd-services + manual fix ssh-deep L269 `long@bastion` → `user@bastion`.
- ✅ **🎉 Phase 4 06_databases sql-fundamentals/ COMPLETE 6/6 files** (cùng phiên với 05_networking dns + sql-fundamentals batch):
  - 05_schema-design-basics → v1.1.0 (data types numeric/text/boolean/date/JSON)
  - 01_select-and-filter → v1.1.0 (SELECT syntax + cột cụ thể + alias + biểu thức)
  - 03_joins → v1.1.0 (Setup 2 bảng + 5 loại JOIN + INNER JOIN)
  - 04_insert-update-delete → v1.1.0 (INSERT cú pháp + multi + SELECT + DEFAULT + RETURNING) + fix `'Lê bạn'` → `'Nguyen Van A (updated)'`
  - 00_what-is-sql → v1.1.0 (Excel vs SQL + Anatomy table + Relational diagram + Khi nào chọn gì + Flow đầy đủ) + fix residue `bạn` → `Nguyen Van A` 2 places
  - 02_aggregations → v1.1.0 (Ví dụ toàn bộ + COUNT variations + GROUP BY + multi-col + Quy tắc vàng) + fix residue `bạn` → `Nguyen Van A` output table
  - **🎉 PostgreSQL/ COMPLETE 5/5** (cùng phiên): 00_what-is-postgresql v1.0.0 → v1.1.0 (đổi "History" → "Lịch sử" + "Adoption" → "Mức độ phổ biến" theo §3.7), 01_psql-and-meta-commands v1.0.0 → v1.1.0 (Kết nối 5 cách + .pgpass + .psqlrc + meta-commands), 02_indexes-and-performance v1.0.0 → v1.1.0 (đổi "5 loại index" → "6 loại" cho đúng count + CONCURRENTLY), 03_jsonb-and-arrays v1.0.0 → v1.1.0 (JSON vs JSONB + Create+insert + operators + path access) + fix `'bạn'` → `'Nguyen Van A'`, 04_backup-and-replication v1.0.0 → v1.1.0 (2 loại backup + Logical/Physical pros/cons Việt hoá + format + options).
  - **06_databases COMPLETE 11/11 ✅** (sql-fundamentals 6 + postgresql 5).
  - **🔄 10_devops progress 37/49**: docker 9/10 ✅ + ci-cd 10/10 ✅ + kubernetes 4/10 + observability 6/10 + iac 8/10 (basic 4/5 + intermediate 4/5 — còn iac basic 04 + iac intermediate 03).
  - **🎉 07_web COMPLETE 20/20 ✅** (4 phiên dồn):
    - html-css 5/5: 00+01+02+03+04 → v1.1.0 (fix `bạn Shop` 3 files)
    - js-dom 5/5: 00+01+02+03+04 → v1.1.0 (đổi "History" → "Lịch sử")
    - react 5/5: 00+01+02+03+04 → v1.1.0 (fix `name="bạn"` 2 files)
    - fastapi 5/5: 00+01+02+03+04 → v1.1.0 (fix `"bạn"` user data 2 files)

- ✅ **🎉 Phase 4 05_networking COMPLETE 16/16 files** (manual thorough — pace ~5 files/turn):
  - `http-methods.md` v1.0.0 → v1.1.0 — 5 lead-in + name placeholder
  - `http-status-codes.md` v1.0.0 → v1.1.0 — 5 lead-in (5 nhóm + 2xx + 200/201/204 + 202 + 3xx)
  - `http-headers.md` v1.0.0 → v1.1.0 — 5 lead-in (CORS tình huống + 4 nhóm + Content-Type + Multipart) + name fix
  - `rest-api-concepts.md` v1.0.0 → v1.1.0 — 5 lead-in (REST vs RPC + RESTful distinction + 3 quy tắc) + thêm Changelog section
  - `what-is-http.md` v1.0.0 → v1.1.0 — 5 lead-in (Bản chất + Versions + Use cases + Luôn theo cặp + Anatomy)
  - `https-tls.md` v1.1.0 → v1.2.0 — 5 lead-in (Port + Vì sao HTTPS + TLS versions + Handshake mermaid + 4 bước)
  - `what-is-tcp-ip.md` v1.0.0 → v1.1.0 — 5 lead-in (4-layer + Nhiệm vụ + Layer X mapping + TCP/IP vs OSI + Header per layer)
  - **http-https/ 6/6 ✅** + **tcp-ip-fundamentals/ 5/5 ✅** + **dns/ 5/5 ✅** — TOÀN BỘ 05_networking đóng.
  - Batch cuối: 01_dns-records → v1.1.0; 02_dns-resolution → v1.1.0; 03_dns-tools → v1.1.0; 04_dns-setup-and-security → v1.2.0.
  - **Next**: Phase 4 06_databases (11 files) — sql-fundamentals 6 + postgresql 5.

- ✅ **🔄 Blueprint v0.5.8 — Soften §3.5: "hạn chế" không "cấm"**: User clarify *"các ví dụ bạn muốn đưa data sao cũng được, miễn sao hạn chế tên riêng là được. Hạn chế, chứ không ép không dùng nhé."* — mình hôm 24/05 quá cứng nhắc bulk-fix Alice→Nguyen Van A. Update Blueprint:
  - Title §3.5: "Nhân vật và tên riêng — **Hạn chế, không ép**"
  - Bảng `✅ Default` / `⚠️ Hạn chế` thay vì `✅ Dùng` / `❌ Tránh`
  - Vẫn giữ Nguyen Van A/Le Van B/... là **default ưu tiên** cho code multi-row
  - Cho phép: ví dụ ngắn 1-2 lần `name = "Alice"` OK, cryptography "Alice ↔ Bob" giữ convention, tài liệu chuẩn ngoài quote nguyên
  - Vẫn tránh: fictional character recurring xuyên cluster (Long/Mai story arc)
  - KHÔNG bulk-revert Alice→Nguyen Van A đã chạy hôm 24/05 (placeholder VN vẫn là default).
  - Memory `feedback_no_self_invented_characters.md` updated với section "KHÔNG ÉP — linh hoạt khi đáng ra cần".

### 24/05/2026

- ✅ **🧹 SWEEP v2 — Alice/Bob/Charlie → Nguyen Van A/Le Van B/Tran Van C** (cuối phiên 24/05, sau user clarification): User feedback: *"không nên dùng tên riêng bất cứ tiếng gì... bạn A bạn B Nguyen Van A Le Van B Tran Van C kiểu vậy"*. Alice/Bob/Charlie/David/Eve/Frank/Grace mình vừa đưa vào VẪN LÀ tên riêng (tiếng Anh) → vi phạm.
  - Blueprint v0.5.6 → **v0.5.7**: thêm rule chính thức "placeholder Việt convention" (Nguyen Van A / Le Van B / Tran Van C / Pham Van D / Hoang Van E / Vu Van F / Bui Van G — không dấu code-safe, hoặc dạng ngắn `bạn A`/`bạn B` cho narrative).
  - **2 scripts run**:
    - `fix-international-names.py`: 27 files, 279 subs (Alice/Bob/Charlie/David/Eve/Frank/Grace → VN placeholder + email lowercase versions)
    - `fix-residue-after-vn-placeholder.py`: 16 files, 49 subs (residue emails `long@ex.com` → `nguyenvana@ex.com`, UPPER output `LONG` → `NGUYEN VAN A`, LIKE patterns `'%alice%'`/`'%long%'` → `'%nguyen%'`, orphan "bạn" user-1 SQL cells → "Nguyen Van A")
  - **Total v2: 328 replacements across 43 files**. Verify: grep `\b(Alice|Bob|Charlie|David|Eve|Frank|Grace)\b` returns 0 in non-changelog content.
  - Memory `feedback_no_self_invented_characters.md` updated với convention mới.
  - **Cosmetic note**: 1 số SQL output table có column alignment lệch nhẹ do "Alice" (5 ký tự) → "Nguyen Van A" (12 ký tự). Acceptable trade-off (đây là lesson MD, không phải SQL output thực).

- ✅ **🧹 SWEEP v1 — Fictional names 0 residue** (cuối phiên 24/05): User feedback "không cần long hay ròm, không dùng tên riêng". Update Blueprint v0.5.5 → v0.5.6 + 7 pass bulk-fix script (~367 replacements across 47+ files):
  - Pass 1-3: username/path patterns (`/Users/rom/`, `rom@laptop`, `chown rom`, `"Hello Rom!"` Python) → generic user/dev + Alice/Bob/Charlie
  - SQL fix (6 files, 144 subs): Mai/Hùng/Lan/Bình/Châu/Đức → Alice/Bob/Charlie/David/Eve/Frank/Grace (with LIKE pattern table rewrite for new names)
  - Mai tools fix (5 files, 21 subs): git-clients/github.md, github-desktop.md story arc, text-processing sample data
  - Final cleanup (5 files, 22 subs): Python tuples/dicts, React JSX `<Greeting name="Mai" />`, HTML form a11y "Mai bị mù bẩm sinh"
  - Python Rom aggressive (4 files, 29 subs): whole-word Rom in code samples
  - Manual rewrites: git/03_remote-and-github.md (Mai story arc → "đồng nghiệp"), docker/00_what-is-docker.md + 02_dockerfile-basics.md (Mai story), OAuth JWT `"name": "Mr. Rom"` → `"name": "Alice Nguyen"`, github.md username examples `long123`/`nguyen-van-long` → `dev123`/`nguyen-van-a`
  - **Verify**: `grep -E '\b(Mai|Hùng|Lan|Hoa|Bình|Hung|Rom|Long)\b'` returns 0 hits in non-changelog content (excluding Mr.Rom author + Châu Á/Âu/Mỹ geographic + Bình thường idiom + Long-running/Long-lived technical terms)
  - Blueprint v0.5.6 changelog logged with full pass summary

- ✅ **🔧 Phase 4 progress: 19/186 lessons fixed Blueprint v0.5.4** (phiên cuối):
  - **7 Foundations**: terminal (00), shell (01), filesystem (02), process (03), env-vars (04), io-redirection (05), industry-landscape (00) — thêm lead-in trước bảng/code, mở rộng ẩn dụ.
  - **4 Python basic**: what-is-python (00), variables-and-types (01), control-flow (02), functions (03) — lead-in + ẩn dụ liên tục (người phiên dịch xuyên section, lề lùi đoạn văn cho indentation).
  - **8 Linux**: 3 basic (navigation, file-ops, view-content) + 5 intermediate (users-permissions, systemd, ssh, package-mgmt, text-processing) — lead-in + ẩn dụ mới (biên lai cho `ls -l`, mật mã 3 số cho octal, quản gia cho systemd, bộ chìa khoá cho SSH, app store + thợ sửa cho package, kính lúp cho grep). Fix residue `long` lowercase username → `rom`.
  - Tổng phiên: 19 files manual rewrite. Còn ~155 files. Next: 05_networking (16 files).
- ✅ **🔍 Blueprint v0.5.4 + Audit + Long character fix** (cuối phiên 24/05, sau khi user yêu cầu kiểm tra toàn bộ):
  - **Blueprint v0.5.3** thêm §3.6 (Anti-pattern Header→Code) + §3.7 (Vietnamese-first principle).
  - **Blueprint v0.5.4** thêm §3.8-3.12: Comments code đánh số bước, Mở bài relatable problem, Ẩn dụ liên tục, ✅❌ format, Bảng trade-off + lead-in. Học từ mining 10 pattern hay trong __Ref__ folders.
  - **Auth 01 (password-and-mfa) v2.0.0** rewrite làm demo theo Blueprint mới (1149 dòng, đậm tiếng Việt + lead-in đầy đủ).
  - **Audit 186 files** với script `_workspace/audit-blueprint-v0.5.4.py` — kết quả: 181/186 files vi phạm (97%), 6 loại vi phạm phổ biến.
  - **Phase 4 manual fix 7 files 01_foundations**: 00_terminal, 01_shell, 02_filesystem, 03_process, 04_env-vars, 05_io-redirect, industry-landscape/00 — thêm lead-in trước bảng/code, mở rộng ẩn dụ.
  - **Phát hiện 12 files vi phạm §3.5 (Long character)** — audit cũ miss vì chỉ check Mai/longshop. Fix tất cả via targeted script: 5 file git/, 3 file git-clients tool guide, 4 file Docker basic. Bump version v1.0→v1.1 hoặc v2.0→v2.1.
  - **Sự cố revert** giữa quá trình: bulk-fix Long script tạo inconsistency capitalization. User chọn revert. `git checkout HEAD --` reset quá tay → MẤT 14 README files (3 parent + 11 cluster). Restore lại tay tất cả 14 READMEs (v1.0.0+).
  - **Blueprint v0.5.4** + Auth 01 v2.0.0 + 8 file Foundations đã fix + 12 file Long fixed + 14 file README restored.
- ✅ **🔍 Audit pass — Blueprint v0.5.2 compliance** (cuối phiên 24/05): User yêu cầu dừng + kiểm tra rule. Tìm + fix:
  - **5 vi phạm Blueprint §3.5** (fictional character "Mai") trong `13_ai-ml/llm/01` + `04` — replace bằng "trợ lý support Acme Shop" generic
  - **2 vi phạm** "Mai 2h" + "em" trong `11_cloud/serverless/01` + `03` — replace bằng "bạn" + "Deadline mai"
  - **1 PII leak** trong `12_security/authentication/00` ("Nguyễn Thiện Lê, sinh 1990") — replace bằng generic "tên + ngày sinh + số CMND"
  - **1 title missing emoji** `11_cloud/azure/00` ("# Azure" → "# ☁️ Azure")
  - **3 broken filenames** trong cross-reference (04_authentication-jwt → 04_auth-and-middleware; 04_sre-practices-and-postmortem → 04_sre-practices; 00_what-is-cloud-overview → 00_what-is-cloud-computing) ở 5 files
  - **5 wrong-depth paths** (`../../../<L1>` → `../../../../<L1>`) trong OWASP 00
  - Verified: zero smart quotes, zero broken links sau fix, all 8-part Blueprint structure trong files Mr.Rom viết, all metadata headers complete.
  - Lesson learned: trước khi launch agent → brief rõ ràng hơn về Blueprint §3.5, cross-reference depth, không tự bịa nhân vật.
- ✅ **🆕 `12_security/authentication/` BASIC cluster COMPLETE 5/5** — Cluster thứ hai của 12_security branch (2/10 sub-clusters active). 5 bài (~3443 dòng): Auth foundation + AuthN/AuthZ + factors + session vs token (00), Password Argon2id + breach check + TOTP + WebAuthn/Passkey + backup codes (01), OAuth 2.1 + OIDC + 5 flows + JWKS + Google/Apple login (02), JWT/JWS/JWE + signing algorithms + key rotation + refresh family + revocation strategies + session lifecycle (03), SAML vs OIDC + Keycloak self-host + SCIM + JIT + break-glass + audit + compliance (04). Auth cluster README v1.0.0. 12_security parent README v1.0.0 → v1.1.0. MASTER-CATALOG v1.39.0 → v1.40.0. Tổng bài 205 → **210**. Deep dive OWASP A07.
- ✅ **🆕 `13_ai-ml/llm/` BASIC cluster COMPLETE 5/5** — Cluster đầu tiên của 13_ai-ml branch (1/10 sub-clusters active). 5 bài (~3683 dòng): LLM intro + tokenization + models 2026 (00), prompt engineering + structured output + injection (01), function calling + agent loop + MCP standard (02), RAG fundamentals + embedding + vector DB + reranker (03), production LLM app cost + eval + guardrails + 30-item checklist (04). LLM cluster README v1.0.0. 13_ai-ml parent README v0.1.0 → v1.0.0. MASTER-CATALOG v1.38.0 → v1.39.0. Tổng bài 200 → **205**. Foundation cho dev build AI app — không cần math/classical ML trước.
- ✅ **🆕 `12_security/owasp-top-10/` BASIC cluster COMPLETE 5/5** — Cluster đầu tiên của 12_security branch (1/10 sub-clusters active). 5 bài (~3353 dòng): OWASP intro + threat modeling STRIDE/DREAD (00), A01 Access Control + A03 Injection + XSS/CSRF/CSP (01), A02 Crypto + A04 Insecure Design + Argon2/TLS/JWT (02), A05 Misconfig + A06 Vulnerable Components + A08 Supply Chain + cosign/SLSA (03), A07 Auth + A09 Logging + A10 SSRF + MFA WebAuthn/TOTP + audit log (04). OWASP cluster README v1.0.0. 12_security parent README v0.1.0 → v1.0.0. MASTER-CATALOG v1.37.0 → v1.38.0. Tổng bài 195 → **200**. Foundation cross-stack security cho mọi role backend/devops/cloud.
- ✅ **🎉🎉🎉 11_cloud BASIC BRANCH HOÀN CHỈNH 9/9 SUB-CLUSTER** (45 lessons, ~40,625 dòng) — Trong cùng session 24/05:
  - cloud-fundamentals (5/5) + aws (5/5) + gcp (5/5) — đầu phiên
  - **Azure (5/5 — ~4400 dòng)**: overview/VM/Blob/SQL+Cosmos/Functions — agent (1067s) + Mr.Rom finalize README
  - **DigitalOcean (5/5 — ~3974 dòng)**: overview/Droplet/Spaces/MgdDB/AppPlatform — agent complete (full + README)
  - **Cloudflare (5/5 — ~4273 dòng)**: overview/CDN-DNS-SSL/Workers-Pages/R2-D1-Queues/Security-ZeroTrust — agent (1102s) + Mr.Rom README
  - **Serverless (5/5 — ~4663 dòng)**: overview/FaaS/Events/Patterns/Cost-ColdStart-Obs — agent (1378s, 3/4 lessons + bài 04 Mr.Rom write) + Mr.Rom README
  - **Multi-cloud-strategies (5/5 — ~4000 dòng)**: overview/LockIn/Network-Identity/K8s-Anthos/DR-Patterns — agent (1026s, 3/4 lessons + bài 04 Mr.Rom write) + Mr.Rom README
  - **Cloud-cost-management (5/5 — ~3530 dòng)**: FinOps/Pricing/Tagging/Optimization/Tools — agent (1326s, full lessons) + Mr.Rom README
  - MASTER-CATALOG v1.36.0 → v1.37.0. Tổng bài 165 → **195** (+30 lessons).
  - 11_cloud parent README v1.2.0 → v1.3.0.
  - 4/6 agent hit session limit "2:40pm Asia/Saigon" giữa task → Mr.Rom finalize 2 lesson 04 thiếu (serverless + multi-cloud) + 5 README skeleton (azure/cloudflare/serverless/multi-cloud/cost).
- ✅ **🆕 `11_cloud/gcp/` BASIC cluster COMPLETE 5/5** — Cluster vendor-specific thứ hai (sau AWS) của `11_cloud/`. 5 bài (GCP overview + Compute Engine/PD + Cloud Storage/IAM + Cloud SQL/Firestore + Cloud Functions/Run/API Gateway) ~6000 dòng. Pattern mirror AWS 00-04 + GCP-specific topics: Live Migration, IAP SSH, Workload Identity Federation, Firestore Security Rules, Cloud Run scale-to-zero, Spanner/Bigtable mention. README cluster v1.0.0. 3/9 sub-clusters active.
- ✅ **2 sơ sài overview expanded** — docker/02_intermediate/00 (311→401 dòng) + k8s/02_intermediate/00 (337→437 dòng). Bổ sung: real-world incidents table, ROI metric table, learning timeline Day 1-90, anti-patterns 8-10 mục, +3 Q&A. Lý do: user feedback yêu cầu chiều sâu cho intro overview lessons.
- ✅ **13 🪞 metaphor added** — Lessons DevOps intermediate (CI/CD supply chain, Docker security/optimization/registry, IaC state/Pulumi, K8s ingress/autoscaling, Observability PromQL/OTel) + AWS basic (S3/RDS/Lambda) bổ sung 🪞 Ẩn dụ theo Blueprint v0.5.2 §2.3.
- ✅ **🆕 `11_cloud/aws/` BASIC cluster COMPLETE 5/5** — Cluster vendor-specific đầu tiên của `11_cloud/`. 5 bài (AWS overview + EC2/EBS + S3/IAM + RDS/DynamoDB + Lambda/API Gateway) ~5890 dòng. Build on cloud-fundamentals. Production-grade AWS skill foundation. MASTER-CATALOG v1.35.0. Tổng 155 → **160** (134 lesson). 2/9 sub-clusters của 11_cloud active.
- ✅ **🆕 `11_cloud/cloud-fundamentals/` BASIC cluster COMPLETE 5/5** — Cluster đầu tiên của `11_cloud/` (was skeleton). 5 bài (cloud computing + regions/AZs + networking + storage/DBs + security/shared responsibility) ~5200 dòng. Vendor-neutral foundation. MASTER-CATALOG v1.34.0. Tổng 150 → **155** (129 lesson). Cluster README + 11_cloud parent README updated (v0.1.0 → v1.0.0). Next: AWS / GCP / Azure specific clusters hoặc continue career roadmaps.
- ✅ **🎉🎉🎉 DEVOPS INTERMEDIATE SPRINT 100% COMPLETE 🎉🎉🎉** — IaC intermediate cluster 5/5 hoàn thành ~5870 dòng (overview + Terragrunt + Atlantis + State+Drift + Pulumi/CDK/Crossplane). Apply 4+ insight từ `__Ref__/` (GitOps as enforcement gate, drift detection workflow, state migration, multi-cloud abstraction). MASTER-CATALOG v1.33.0. Tổng 145 → **150** (124 lesson). **DevOps tier-1 production-grade toàn bộ stack** (Docker + K8s + CI/CD + Obs + IaC = 49 lessons).
- ✅ **🎉 Observability INTERMEDIATE cluster HOÀN CHỈNH 5/5** — Cluster intermediate thứ 4 của `10_devops/`. 5 bài (overview + PromQL deep + LogQL deep + OTel instrumentation + SRE practices) ~5560 dòng. Apply 4+ insight từ `__Ref__/` (SRE practices, blameless postmortem, burn rate alerts, on-call patterns). MASTER-CATALOG v1.32.0. Tổng 140 → **145** (119 lesson). 4/5 DevOps cluster intermediate complete.
- ✅ **🎉 CI/CD INTERMEDIATE cluster HOÀN CHỈNH 5/5** — Cluster intermediate thứ 3 của `10_devops/`. 5 bài (overview + ArgoCD + Supply chain SLSA + Secret Vault/ESO + Progressive delivery Argo Rollouts) ~4830 dòng. Apply 4 insight từ `__Ref__/` (GitOps anti-pattern, 12-factor, SLSA L3, progressive delivery). MASTER-CATALOG v1.31.0. Tổng 135 → **140** (114 lesson). SOC2-ready CI/CD pipeline.
- ✅ **🎉 Kubernetes INTERMEDIATE cluster HOÀN CHỈNH 5/5** — Cluster intermediate thứ 2 của `10_devops/`. 5 bài (overview + Helm + Ingress+cert-manager + StatefulSet + Autoscaling+Operators) ~4220 dòng. Apply 4 insight từ `__Ref__/` (CNI dependency, PDB-HPA, CloudNativePG, Cilium). MASTER-CATALOG v1.30.0. Tổng 130 → **135** (109 lesson). Foundation cho Platform/SRE/DevOps role production.
- ✅ **🎉 Docker INTERMEDIATE cluster HOÀN CHỈNH 5/5** — Cluster intermediate đầu tiên của `10_devops/`. 5 bài (overview + BuildKit + security + optimization + registry) ~3540 dòng. Apply Blueprint v0.5.2 rule mới (no fictional character). MASTER-CATALOG v1.29.0. Tổng 125 → **130** (104 lesson). Foundation cho K8s intermediate + CI/CD intermediate sau.
- ✅ **Audit toàn bộ DevOps basic 24 lessons** — 4 Explore agent song song + mining `__Ref__/`. Fix 5 critical bug + 3 polish + apply 2 nugget (SIGTERM pitfall docker/02, SLO error-budget obs/00). Verified bằng grep toàn bộ (zero "Long"/"Mai"/"longshop" residual).
- ✅ **Blueprint governance update**: writing-style v0.5.2 (§3.5 cấm tự bịa nhân vật) + quality-checklist v0.3.1 (2 checkpoint mới). Save 2 memory: governance-changelog-discipline + no-self-invented-characters. Capture 20+ insight cho DevOps Intermediate vào backlog.
- ✅ **Bulk fix Long/Mai/longshop character** qua 3 pass Python script (95+ files). Verified clean toàn bộ DevOps lesson + meta files.

### 23/05/2026

- ✅ **🎉 DEVOPS SPRINT COMPLETE — 4 CLUSTERS + 20 LESSONS** 🎊
- ✅ **🎉 iac BASIC CLUSTER HOÀN CHỈNH 5/5** — Cuối DevOps sprint. story arc: click-ops vs IaC (00) → Terraform basics + AWS VPC (01) → S3+DynamoDB state production (02) → modules DRY multi-env (03) → security + cost + policy + alternatives (04). 5 bài ~2790 dòng. README v1.0.0. MASTER-CATALOG v1.28.0. Tổng 120 → **125**.
- ✅ **🎉 observability BASIC CLUSTER HOÀN CHỈNH 5/5** — DevOps sprint #3. story arc tiếp CI/CD: deploy crash unknown → Prometheus metrics → centralize logs → distributed tracing OTel → Grafana + alerting on-call. 5 bài ~2660 dòng. README v1.0.0. MASTER-CATALOG v1.27.0. Tổng 115 → **120**.
- ✅ **🎉 ci-cd BASIC CLUSTER HOÀN CHỈNH 5/5** — DevOps sprint #2. story arc tiếp K8s: deploy thủ công khổ → GitHub Actions master → GitLab CI → patterns production → 5 deploy strategies. 5 bài ~2680 dòng. README v1.0.0. MASTER-CATALOG v1.26.0. Tổng 110 → **115**.
- ✅ **🎉 kubernetes BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster thứ 2 của `10_devops/` (sau Docker). DevOps sprint #1. story arc: scale 1000 user (00) → first Pod (01) → expose ra Internet (02) → hardcode DATABASE_URL (03) → share cluster 3 team (04). 5 bài ~2980 dòng. README v1.0.0. MASTER-CATALOG v1.25.0. Tổng 105 → **110**.
- ✅ **🎉 postgresql BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster thứ 2 của `06_databases/`. story arc tiếp React: chọn DB production (00) → debug Postgres lần đầu (01) → 5s query slow (02) → lưu config động (03) → rm-rf DB (04). 5 bài ~2920 dòng. README v1.0.0. MASTER-CATALOG v1.24.0. Tổng 100 → **105**. `__Ref__/06_databases/` chỉ có NoSQL content (Mongo/Redis/Neo4j) → save cho Redis/Mongo cluster sau.
- ✅ **🎉 react BASIC CLUSTER HOÀN CHỈNH 5/5 — MỐC 100 BÀI ✨** — Cluster thứ 3 của frontend. story arc tiếp javascript-dom: vanilla JS scale kém (00) → copy-paste card 10 lần (01) → mutate cart vô tận (02) → fetch infinite loop (03) → SPA nhiều trang + cart count khắp nơi (04). 5 bài ~2910 dòng. README v1.0.0. MASTER-CATALOG v1.23.0. Tổng 95 → **100**. Fullstack complete (React + FastAPI). `__Ref__/07_web/` rỗng → skip.
- ✅ **🎉 javascript-dom BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster thứ 2 của frontend. story arc tiếp html-css: thêm interactivity (00) → copy SO 3 bug (01) → thay jQuery cũ (02) → 1000 listener performance (03) → fetch FastAPI lỗi không hiện (04). 5 bài ~2850 dòng. README v1.0.0. MASTER-CATALOG v1.22.0. Tổng 90 → **95**. `__Ref__/07_web/` rỗng → skip.
- ✅ **🎉 html-css BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster đầu tiên của `07_web/frontend/`. story arc tiếp Linux: build frontend cho FastAPI (00) → viết about.html div lung tung (01) → form login đồng nghiệp không dùng được (02) → "sao style không apply" (03) → viết homepage responsive (04). 5 bài ~2730 dòng. README v1.0.0. MASTER-CATALOG v1.21.0. Tổng 85 → **90**. `__Ref__/07_web/` rỗng → skip cherry-pick.
- ✅ **🎉 linux INTERMEDIATE CLUSTER HOÀN CHỈNH 5/5** — Cluster intermediate đầu tiên đóng. story arc tiếp FastAPI: deploy bind port 80 (00) → đóng SSH app chết (01) → 5 server gõ pass mệt (02) → cài Python 3.12 (03) → log nginx 10GB (04). 5 bài ~2840 dòng. README v0.2.0 (Linux). MASTER-CATALOG v1.20.0. Tổng 80 → **85**.
- ✅ **Cherry-pick 2 gem từ `__Ref__/04_os/linux/__Ref__/`** → improve:
  - 🔧 `02_ssh-deep-dive.md` v1.0.0 → v1.1.0 — mở rộng **fail2ban** (jail.local config + 6 commands + whitelist + bantime.increment)
  - 🔧 `03_package-management.md` v1.0.0 → v1.1.0 — mở rộng **unattended-upgrades** (auto-reboot scheduling, production strategy table, disable cho critical service)
- ✅ **🎉 python-fastapi BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster đầu tiên của `07_web/backend/`. Synthesis của Python + SQL + HTTP + REST. story arc: build API đầu tiên (00) → CRUD chuẩn REST (01) → lộ password response (02) → cần DB persistent (03) → ai cũng vào được, cần auth (04). 5 bài ~2570 dòng. README cluster v1.0.0. MASTER-CATALOG v1.19.0. Tổng bài 75 → **80**. `__Ref__/07_web/` rỗng — skip cherry-pick lần này.
- ✅ **Cherry-pick 3 gem từ `__Ref__/05_networking/04_Networking_old/`** → apply 3 cluster networking:
  - 🔧 `tcp-vs-udp.md` v1.0.0 → v1.1.0 — thêm **Nagle's Algorithm + TCP_NODELAY** (interactive app latency)
  - 🔧 `https-tls.md` v1.0.0 → v1.1.0 — thêm **Perfect Forward Secrecy + ECDHE** (RSA vs ECDHE key exchange, TLS 1.3 enforce PFS)
  - 🔧 `dns-setup-and-security.md` v1.0.0 → v1.1.0 — thêm **DNSSEC 4 records** (DNSKEY/RRSIG/DS/NSEC) + **chain of trust flow** + adoption stats
  - Workflow `__Ref__` cherry-pick mới được verify — apply mỗi cluster sau khi đóng.
- ✅ **🎉 tcp-ip-fundamentals BASIC CLUSTER HOÀN CHỈNH 5/5** — 3-trụ-cột networking đủ (HTTP + DNS + TCP/IP). story arc tiếp SQL: bạn debug "Connection refused" (00) → config VPS network engineer hỏi đầy lạ (01) → video stream lag (02) → port 5432 timeout (03) → on-call 2 giờ sáng (04). 5 bài ~2560 dòng. README cluster v1.0.0. MASTER-CATALOG v1.18.0. Tổng bài 70 → **75**.
- ✅ **🎉 sql-fundamentals BASIC CLUSTER HOÀN CHỈNH 6/6** — Cluster đầu tiên của `06_databases/`. story arc tiếp DNS: bạn quản lý 100 user trong Excel (00) → query 5s với SELECT* (01) → sếp hỏi "user mỗi city" (02) → list user+order (03) → DELETE quên WHERE (04) → schema sai sau 3 tháng (05). 6 bài ~3150 dòng. README cluster v1.0.0. MASTER-CATALOG v1.17.0. Tổng bài 64 → **70**.
- ✅ **🎉 dns BASIC CLUSTER HOÀN CHỈNH 5/5** — Cluster thứ 2 của `05_networking/`. story arc tiếp HTTP: bạn đổi máy chủ user kêu site die (00) → mua domain ngơ trước Cloudflare panel (01) → đợi 24h vẫn 5% IP cũ (02) → debug DNS không biết lỗi đâu (03) → mua domain `.vn` đầu tiên muốn setup từ A-Z (04). 5 bài ~2300 dòng. README cluster v1.0.0. MASTER-CATALOG v1.16.0. Tổng bài 59 → **64**.
- ✅ **🎉 http-https BASIC CLUSTER HOÀN CHỈNH 6/6** — Cluster đầu tiên của `05_networking/`. story arc tiếp git/docker: bạn debug 401 DevTools (00) → design POST /getUsers bị chê (01) → debug 5 status (02) → 5 lỗi CORS 1 ngày (03) → deploy self-signed cert (04) → sếp bảo "phải RESTful" (05). 6 bài ~3000 dòng + mermaid TLS handshake + framework code samples. README cluster v1.0.0. MASTER-CATALOG v1.15.0. Tổng bài 53 → **59**.
- ✅ **🎉 git-clients CLUSTER HOÀN CHỈNH 7/7** — Thêm 5 file: github-desktop (~400), gitlab (~600), bitbucket (~500), codeberg (~450), gitea (~500). Tool category đầu tiên của `02_tools/` đóng đủ pattern (category + 6 individual). README v1.0.0 + MASTER-CATALOG v1.14.0. Tổng bài 48 → 53.
- ✅ **GitHub user guide** — `github.md` (~720 dòng): account+2FA, SSH/PAT/gh auth, repo+UI tour, PR workflow, Actions, Pages, gh CLI, security. Unblock 3 "(chưa có)" link → ✅. README v0.3.0 + MASTER-CATALOG v1.13.0. Tổng bài 47 → 48.
- ✅ **Tool category git-clients mở** — `00_what-is-git-hosting.md` (~520 dòng): so sánh 7 platform, 7 case khuyến nghị, vendor lock-in, AI 2026. README v0.2.0 + MASTER-CATALOG v1.12.0.
- ✅ **🎉 Computing-environment CLUSTER BASIC HOÀN CHỈNH 6/6** — Thêm `05_io-redirection.md` (~520 dòng): 3 streams + redirect + pipe + /dev/null + tee + 3 ví dụ kết hợp. README v1.0.0 + MASTER-CATALOG v1.11.0. Cluster đầu tiên của Foundations đóng hoàn chỉnh.
- ✅ **Computing-environment 04_env-variables** (~470 dòng): env var + $PATH + 3 scope + inheritance + `.env`/`.env.example` + secrets vs config + vault tools + Docker env. README v0.6.0 + MASTER-CATALOG v1.10.0. Cluster basic 5/6.
- ✅ **Computing-environment 03_process-and-pid** (~470 dòng): Program vs Process, PID tree, PID 1 (systemd/launchd/Docker), 4 trạng thái + Zombie, signal SIGTERM/SIGKILL, fg/bg/nohup/disown, Docker context. README v0.5.0 + MASTER-CATALOG v1.9.0. Cluster basic 4/6.
- ✅ **Computing-environment 02_filesystem-concept** (~420 dòng): filesystem 3 OS, absolute/relative path, 5 ký hiệu, CWD, hidden files, permissions, symlink. README v0.4.0 + MASTER-CATALOG v1.8.0. Cluster basic 3/6.
- ✅ **Computing-environment buildout** — viết `01_what-is-shell.md` (~350 dòng): phân biệt 3 lớp Terminal/Shell/Command + so sánh bash/zsh/fish (10 tiêu chí) + cách check shell + đổi shell + intro `.bashrc`/`.zshrc`. Mở bằng tình huống tutorial nói "thêm vào ~/.bashrc". Update README v0.3.0 + MASTER-CATALOG v1.7.0. Cluster basic computing-environment giờ 2/6 bài.

### 21/05/2026

- ✅ **Move terminal intro** `02_tools/shell/lessons/01_basic/00_what-is-terminal.md` → `01_foundations/computing-environment/lessons/01_basic/00_what-is-terminal.md` (v2.0.0 → v2.1.0). Sweep 6 external + 2 internal refs. Update shell README (v0.4.0) + computing-environment README (v0.2.0) + MASTER-CATALOG (v1.6.0).
- ✅ **Python 4 lessons refactor v2.0.0** — `00_what-is-python` (tình huống cài Python, mở terminal không biết gõ gì), `01_variables-and-types` (viết script tính lương, TypeError vì chưa biết types), `02_control-flow` (tax theo bậc + lặp 30 nhân viên), `03_functions` (lặp 180 chỗ vì chưa biết function). Headers câu hỏi tự nhiên. Content kỹ thuật KHÔNG đổi.
- ✅ **Linux 3 lessons refactor v2.0.0** — `01_navigation` (terminal mở lần đầu, 3 câu hỏi), `02_file-operations` (tạo cấu trúc project + cảnh báo rm), `03_view-file-content` (debug log production 50,000 dòng). Style v0.5.1.
- ✅ **Shell intro refactor v2.0.0** — Tutorial bảo "mở terminal" mà beginner không biết. Style v0.5.1.
- ✅ **Fix 3 stale § refs** trong Docker `02_dockerfile-basics.md` (§6 → §5, §5 → §4 sau renumber).

### 20/05/2026

- ✅ **Docker bộ refactor v2.0.0** — 4 lesson files (intro + 01 images + 02 dockerfile + 03 compose) áp story arc tiếp git: bạn ship project → đồng nghiệp pull về máy gặp "works on my machine" → discover Docker → 8 lệnh CRUD → Dockerfile build myapp → Compose ghép 4 service. Headers đổi sang câu hỏi tự nhiên (writing-style v0.5.1). KHÔNG đổi content kỹ thuật.
- ✅ **WIP-TRACKER + memory** — tạo `_workspace/WIP-TRACKER.md` + 3 memory (expert collab, __Ref__ intentional, WIP tracker auto-load)
- ✅ **Folder skeleton đầy đủ** — 146 L2 + 15 L3 web + 264 README placeholder + 608 .gitkeep theo Blueprint sitemap
- ✅ **Fix broken anchor** — `#stage-1--tools-cơ-bản` → `#stage-1--tools-tối-thiểu` ở 8 file
- ✅ **Tool category đầu tiên** — `02_tools/ide/` với `00_what-is-ide.md` + `vs-code.md` v2.0.0 (move từ `editor/setup/`)
- ✅ **MASTER-CATALOG** v1.1.0 → v1.2.0 → v1.3.0

### 19/05/2026

- ✅ **Move git folder** từ `02_tools/git/` → `01_foundations/version-control/git/`
- ✅ **Git lessons refactor v2.0.0** — 5 bài (intro + 01-04) với story arc narrative
- ✅ **zero-to-coder v2.0.0** — thêm Stage 0 (bản đồ ngành) + Stage 2 đổi sang "Chọn 1 ngôn ngữ"
- ✅ **industry-landscape lesson** — NEW (~470 dòng) cho Stage 0
- ✅ **Writing style v0.5.1** — WHY/WHAT/HOW từ "tiêu đề bắt buộc" → "tiêu chí đánh giá"
- ✅ **Blueprint cleanup** — sync MASTER-CATALOG, 01_foundations README, version-control git README

---

## 🚨 Blocked / Cần user quyết định

### Tool category priority sau ide/
- ⚠️ Đã đề xuất 4 candidate (`git-clients/`, `terminal-emulators/`, `k8s-local/`, `docker-tools/`) — chưa pick
- 🎯 Decision needed: làm cái nào trước theo nhu cầu thực tế

### Lesson series tiếp theo (sau PostgreSQL basic)
- ⚠️ Đã list 8 candidate (HTTP intermediate, SQL intermediate, Redis, MongoDB, FastAPI intermediate, K8s, build-tools, load-balancing) trong Backlog — chưa pick priority cho cluster kế tiếp
- 🎯 Decision needed: chọn 1 để làm tiếp Phase 2

---

## 📌 Changelog

- **v0.62.0 (25/05/2026)** — Phase 4 11_cloud/cloud-fundamentals COMPLETE 5/5 ✅ (5 file 1 turn, files 97-101). Mốc **100 lessons** Phase 4 đạt ở file 100. Total 101/156 (64.7%). Còn aws/azure/gcp/cloudflare/digitalocean/serverless/multi-cloud/cost-management = 40 file 11_cloud + 15 file 12_security/13_ai-ml.
- **v0.61.0 (25/05/2026)** — 🎉🎉🎉 **10_devops COMPLETE 49/49 ✅** (9 file 1 turn). observability 10/10 đóng (files 93-96). Toàn bộ DevOps tier-1 + tier-2 apply Blueprint v0.5.4+. Phase 4 total 93/156 (59.6%). Tiếp 11_cloud 45 → 12_security 10 → 13_ai-ml 5.
- **v0.60.0 (25/05/2026)** — Phase 4 progress: 10_devops/kubernetes 10/10 ✅ COMPLETE (6 files in 1 turn). observability 7/10 (file 93 metrics-prometheus done). Total 90/156 (57.7%). Còn 3 file observability + 11_cloud 45 + 12_security 10 + 13_ai-ml 5.
- **v0.27.0 (24/05/2026)** — 🆕 `11_cloud/aws/` basic cluster complete 5/5 (~5890 dòng). Cluster vendor-specific đầu tiên. AWS production foundation (EC2/S3/IAM/RDS/DynamoDB/Lambda). Tổng 155 → **160**. 2/9 sub-clusters của 11_cloud active.
- **v0.26.0 (24/05/2026)** — 🆕 `11_cloud/cloud-fundamentals/` basic cluster complete 5/5 (~5200 dòng). Cluster đầu tiên `11_cloud/`. Vendor-neutral foundation (cloud computing concepts + regions + networking + storage/DBs + security). Tổng 150 → **155**. Sub-clusters AWS/GCP/Azure/etc. còn skeleton.
- **v0.25.0 (24/05/2026)** — 🎉 IaC INTERMEDIATE cluster hoàn thành 5/5 bài (~5870 dòng). **DEVOPS INTERMEDIATE SPRINT 100% COMPLETE** — 5/5 clusters intermediate (Docker + K8s + CI/CD + Obs + IaC = 25 intermediate lessons total). Apply 4+ insight từ `__Ref__/` đã capture (GitOps enforcement, drift detection, state migration, multi-cloud abstraction). Tổng bài 145 → **150**. Production-grade DevOps stack tier-1 hoàn chỉnh.
- **v0.24.0 (24/05/2026)** — Observability INTERMEDIATE cluster hoàn thành 5/5 bài (~5560 dòng). Cluster intermediate thứ 4 của `10_devops/`. Apply 4+ insight từ `__Ref__/` đã capture (SRE practices, blameless postmortem template, on-call patterns, burn rate alerts, alert on saturation). Tổng bài 140 → **145**. 4/5 DevOps cluster intermediate complete. Còn IaC intermediate cuối.
- **v0.23.0 (24/05/2026)** — CI/CD INTERMEDIATE cluster hoàn thành 5/5 bài (~4830 dòng). Cluster intermediate thứ 3 của `10_devops/`. Apply 4 insight từ `__Ref__/` đã capture (GitOps anti-pattern, 12-factor violations, SLSA L3, progressive delivery patterns). Tổng bài 135 → **140**. 3 cluster DevOps đã intermediate (Docker + K8s + CI/CD).
- **v0.22.0 (24/05/2026)** — K8s INTERMEDIATE cluster hoàn thành 5/5 bài (~4220 dòng). Cluster intermediate thứ 2 của `10_devops/`. Apply 4 insight từ `__Ref__/` đã capture (NetworkPolicy CNI dependency, PDB-HPA war story, Postgres Operator CloudNativePG, Cilium kube-proxy replacement). Tổng bài 130 → **135**.
- **v0.21.0 (24/05/2026)** — Docker INTERMEDIATE cluster hoàn thành 5/5 bài (~3540 dòng). Cluster intermediate đầu tiên của `10_devops/`. Apply rule mới Blueprint v0.5.2 (no fictional character). Tổng bài 125 → **130**. Foundation cho K8s/CI-CD intermediate.
- **v0.20.0 (24/05/2026)** — Bulk fix "Long"/"Mai" character + "longshop" brand qua 95+ files (24 DevOps lessons + meta files) qua 3 pass Python script. Audit toàn bộ 24 DevOps lessons + mining `__Ref__/` qua 5 Explore agent → fix 5 critical bug (broken HTML `<ated>`, residual `long-staging/long-prod` cluster name, `substr "long"` output bug, "backend Long" README leak) + 3 polish + 2 nugget (SIGTERM pitfall vào docker/02, SLO/error-budget table vào obs/00). **Capture 20+ insight cho DevOps Intermediate** vào backlog. Blueprint writing-style v0.5.2 + quality-checklist v0.3.1 thêm rule "KHÔNG tự bịa nhân vật fictional".
- **v0.19.0 (23/05/2026)** — IaC basic cluster 5/5 done. **DEVOPS SPRINT COMPLETE** 4 clusters (K8s+CICD+Obs+IaC) = 20 lessons.
- **v0.18.0 (23/05/2026)** — Observability basic cluster 5/5 done. DevOps sprint #3.
- **v0.17.0 (23/05/2026)** — CI/CD basic cluster 5/5 done. DevOps sprint #2.
- **v0.16.0 (23/05/2026)** — Kubernetes basic cluster 5/5 done. DevOps sprint #1.
- **v0.15.0 (23/05/2026)** — PostgreSQL basic cluster 5/5 done. Cluster thứ 2 của 06_databases.
- **v0.14.0 (23/05/2026)** — React basic cluster 5/5 done. **MỐC 100 BÀI ✨**. Fullstack React + FastAPI complete.
- **v0.13.0 (23/05/2026)** — javascript-dom basic cluster 5/5 done. Cluster thứ 2 của frontend.
- **v0.12.0 (23/05/2026)** — html-css basic cluster 5/5 done. Cluster đầu tiên của `07_web/frontend/`.
- **v0.11.0 (23/05/2026)** — Linux intermediate cluster 5/5 done + cherry-pick 2 gem (fail2ban, unattended-upgrades). Cluster intermediate đầu tiên.
- **v0.10.0 (23/05/2026)** — FastAPI basic cluster 5/5 done. Synthesis Python+SQL+HTTP+REST. Cluster đầu tiên của `07_web/backend/`.
- **v0.9.0 (23/05/2026)** — TCP/IP fundamentals basic cluster 5/5 done. 3-trụ-cột networking đủ. **Workflow mới**: sau khi đóng cluster → cherry-pick `__Ref__/` improve.
- **v0.8.0 (23/05/2026)** — SQL fundamentals basic cluster 6/6 done. Cluster đầu tiên của `06_databases/` đóng.
- **v0.7.0 (23/05/2026)** — DNS basic cluster 5/5 done. Cluster thứ 2 của `05_networking/` đóng.
- **v0.6.0 (23/05/2026)** — HTTP basic cluster 6/6 done. Backlog "Lesson series" → updated với HTTP intermediate/DNS làm candidate kế tiếp.
- **v0.5.0 (23/05/2026)** — git-clients cluster 7/7 done + computing-environment cluster 6/6 done.
- **v0.4.0 (23/05/2026)** — Computing-environment buildout: thêm `01_what-is-shell.md` (cluster basic 2/6 bài).
- **v0.3.0 (21/05/2026)** — Move terminal intro xong (02_tools/shell → 01_foundations/computing-environment), Backlog "Move terminal" → Done.
- **v0.2.0 (21/05/2026)** — Audit + refactor cycle:
  - ✅ Done 8 lesson refactor v2.0.0 (Python 4 + Linux 3 + Shell intro 1)
  - ✅ Fix 3 stale § refs trong Docker file 02
  - ➕ Add **__Ref__ improvements** backlog (Python/Linux/Docker/Shell content có sẵn để cherry-pick)
- **v0.1.0 (20/05/2026)** — Bản đầu tiên. Pre-seed với 1 đang làm + 4 backlog + 11 done (3 ngày 18-20/05) + 2 blocked.
