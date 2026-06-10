# 🔍 Audit Văn Phong — Báo cáo tồn đọng (2026-06-10)

> Tác giả: Claude (audit) · Nguồn: workflow vanphong-audit (24 cụm, 49 agent, adversarial-verified)

> **307 vi phạm xác thực / 147 file** — high 100, medium 141, low 66


## 🚨 Ưu tiên 1 — Hư hại nội dung do script bulk-replace (sửa ngay)

- `00_roadmaps/career/ai-engineer_career-roadmap.md:184` [high] **TELEGRAPHIC_EN** — Hãy dừng lại ở đây và dànhhọc qua Stage 2 của lộ trình [Zero to Coder]
- `00_roadmaps/career/cloud-engineer_career-roadmap.md:163` [high] **TELEGRAPHIC_EN** — Khi đã giỏi AWS, bạn chỉ mấtđể làm quen với GCP hay Azure.
- `00_roadmaps/career/data-scientist_career-roadmap.md:144` [high] **TELEGRAPHIC_EN** — để dự báo doanh số bán hàng của chuỗi siêu thị trongtới, giúp tối ưu hóa chi phí lưu kho.
- `00_roadmaps/career/frontend-developer_career-roadmap.md:184` [high] **TELEGRAPHIC_EN** — đều tương đồng 90% với React, bạn chỉ mất khoảngđể làm quen với cú pháp mới.
- `00_roadmaps/career/fullstack-developer_career-roadmap.md:190` [high] **TELEGRAPHIC_EN** — Tập trungđầu hoàn thiện Frontend (Stage 1 & 2), sau đó chuyển hẳn sang Backend ởtiếp theo (Stage 3).
- `10_devops/ci-cd/lessons/02_intermediate/03_secret-management.md:1026` [high] **NAME_RESIDUE** — Dòng 1026: "**bạn TTL** (e.g., 24 hours):" — đối xứng với "**Short TTL** (e.g., 15 minutes):" ở dòng 1020.
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:197` [high] **NAME_RESIDUE** — Dòng 197: "Severity   Short window  bạn window   Budget in 1 hour" — "Long" bị bulk-replace nhầm thành "bạn".
- `11_cloud/cloud-cost-management/lessons/01_basic/02_tagging-allocation-and-showback.md:54` [high] **NAME_RESIDUE** — Dòng 54: "| `owner` | Người chịu trách nhiệm cuối | `thien.le`, `team-backend` (email/Slack handle) |". `thien.le` trùng email tác
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:68` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:98` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:118` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:143` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 5**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:66` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:87` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:113` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:134` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 5**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:68` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:89` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:110` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:132` [medium] **H_BRIDGE** — >  puente **Cầu nối sang Stage 5**:
- `02_tools/git-clients/github.md:739` [medium] **TELEGRAPHIC_EN** — **Q4.** Strangerd có thể đọc public repo bạn. Vậy sao đỡ leak?
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:574` [medium] **NAME_RESIDUE** — <Link to="/">🛒 bạn Shop</Link>
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:587` [medium] **NAME_RESIDUE** — <footer>© 2026 bạn Shop</footer>
- `00_roadmaps/career/game-developer_career-roadmap.md:197` [low] **TELEGRAPHIC_EN** — Thiết lập các câu bắc cầu logic kết nối mượt mượt giữa các Stage.
- `10_devops/ci-cd/lessons/02_intermediate/README.md:56` [low] **NAME_RESIDUE** — README.md dòng 56: "- [ ] Pre-commit gitleaks + CI scan blockmọi secret leak" — dính chữ "blockmọi".

## 📋 Toàn bộ theo rule


### TELEGRAPHIC_EN (83)

- `00_roadmaps/career/ai-engineer_career-roadmap.md:184` [high] Hãy dừng lại ở đây và dànhhọc qua Stage 2 của lộ trình [Zero to Coder]
- `00_roadmaps/career/cloud-engineer_career-roadmap.md:163` [high] Khi đã giỏi AWS, bạn chỉ mấtđể làm quen với GCP hay Azure.
- `00_roadmaps/career/data-engineer_career-roadmap.md:77` [high] Để làm được điều này, SRE phải thiết kế dữ liệu theo dạng sơ đồ hình sao (Star Schema)
- `00_roadmaps/career/data-scientist_career-roadmap.md:144` [high] để dự báo doanh số bán hàng của chuỗi siêu thị trongtới, giúp tối ưu hóa chi phí lưu kho.
- `00_roadmaps/career/frontend-developer_career-roadmap.md:184` [high] đều tương đồng 90% với React, bạn chỉ mất khoảngđể làm quen với cú pháp mới.
- `00_roadmaps/career/fullstack-developer_career-roadmap.md:190` [high] Tập trungđầu hoàn thiện Frontend (Stage 1 & 2), sau đó chuyển hẳn sang Backend ởtiếp theo (Stage 3).
- `00_roadmaps/career/ml-engineer_career-roadmap.md:53` [high] Một file code Jupyter Notebook hỗn loạn dài 1000 dòng không bao giờ được phép đưa lên production. SRE sẽ từ chối deploy 
- `02_tools/git-clients/github.md:23` [high] 5 câu hỏi đầu tiên. Bài này dẫn bạn (và bạn) qua **mọi setup cần thiết** trong 30 phút
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:40` [high] Dòng 40: "→ 30 phút SSH + clicking. Bug giờ deploy không nhớ steps. **Manual** = **error-prone + slow**."
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:42` [high] Dòng 42-44: "Bạn ngơ:\n- **CI/CD** giúp gì cụ thể?\n- Tools nào — GitHub Actions, Jenkins, GitLab CI?"
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:69` [high] Dòng 69: "**CD** (Delivery) = mọi commit pass CI → **ready to deploy** at any time. Deployment **manual trigger**."
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:339` [high] Dòng 343-344: "- ✅ **Fast feedback** — fail in first 1-5 minutes.\n- ✅ **Cache aggressive** — `npm`, `pip`, Docker layer
- `10_devops/ci-cd/lessons/01_basic/03_pipeline-patterns.md:27` [high] Dòng 27-29: "## 1️⃣ PR validation pattern\n\n**Goal**: every PR validated before merge." — mở section bằng telegraphic E
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:27` [high] Dòng 27: "**Infrastructure as Code** = quản lý infra (servers, networks, DBs, K8s, ...) qua **code/config files**, versi
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:74` [high] Dòng 74-77: "Day 1: Nguyen Van A click-ops staging env / Day 30: Le Van B click-ops prod env / Day 60: Tran Van C debug 
- `10_devops/iac/lessons/01_basic/01_terraform-basics.md:11` [high] Dòng 11: "*Master Terraform/OpenTofu core: ... Sau bài này provision real cloud infra.*"; dòng 111 "→ **First infra prov
- `10_devops/iac/lessons/01_basic/02_state-and-backend.md:59` [high] Dòng 59: "→ JSON snapshot of all managed resources. Updated on every apply."; dòng 69 "→ **Implication**: state file is 
- `10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md:28` [high] Dòng 28: "Tools scan `.tf` files for security issues."; dòng 107 "→ Catch before production."; dòng 113 "Estimate AWS/GC
- `10_devops/iac/lessons/02_intermediate/04_pulumi-cdk-crossplane.md:1141` [high] Thân bài tiếng Việt (dòng 1126-1128, intro Self-check dòng 1134 đều VN), nhưng đáp án Q1 (dòng 1141-1179) và Q2 (1187-12
- `10_devops/kubernetes/lessons/02_intermediate/00_intermediate-overview.md:11` [high] > 🎯 *Bài INTRO. Bạn deploy được first Pod, expose Service, hardcode ConfigMap, share cluster RBAC ở basic. Production th
- `10_devops/observability/lessons/01_basic/00_what-is-observability.md:84` [high] Dòng 92-95: "- **Aggregated** — pre-computed counters/gauges.\n- **Time-series** database...\n- Low storage cost.\n- Fas
- `10_devops/observability/lessons/01_basic/01_metrics-prometheus.md:60` [high] Dòng 60-71: mục Pull vs Push toàn câu cụt tiếng Anh ("Server controls scrape interval", "Works behind NAT/firewall", "Lo
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:50` [high] Dòng 50-62: định nghĩa SLI/SLO/SLA toàn tiếng Anh điện-tín ("quantitative measure of aspect of service", "target value o
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:35` [high] Dòng 35-40: danh sách "Problems" tiếng Anh điện-tín ("No SLO → no consensus on reliability target", "No error budget → p
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:785` [high] Dòng 785-804 (đáp án Self-check Q1) nguyên văn EN điện tín: '**2 AZs**: 1 AZ fails → 1 left. Can survive 1 failure, but:
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:812` [high] Dòng 812-860 (đáp án Q2) nguyên văn EN: '**Main complexity**: **database consistency**.' ... 'Writes can conflict (same 
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:868` [high] Dòng 868-930 (đáp án Q3) nguyên văn EN: '**Cache-Control header** controls CDN + browser caching. **By asset type**:' ..
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:938` [high] Dòng 938-998 (đáp án Q4) nguyên văn EN: '**Schrems II** (2020 EU court ruling): US-based cloud vendors ... subject to **
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:1006` [high] Dòng 1006-1076 (đáp án Q5) nguyên văn EN: '**99.9% (3 nines)** = 43 min downtime/month allowed. **Architecture**: - Mult
- `12_security/authentication/lessons/01_basic/00_what-is-authentication.md:29` [high] Câu thoại sếp dòng 29: "Acme Shop launch 6 tháng tới. Cần auth từ đầu: register email + password + MFA, social login (Go
- `12_security/authentication/lessons/01_basic/00_what-is-authentication.md:111` [high] Dòng 111-113 mục Ưu điểm Session: "- Revocation: delete entry in Redis = logout instantly. - Update permissions live (re
- `12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md:11` [high] Lời dẫn dòng 11: "OAuth 2.0/2.1 = framework delegated authorization (Login with Google). OIDC = OAuth + identity layer (
- `12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md:32` [high] Dòng 32-39 danh sách yêu cầu điện tín EN + câu cụt: "Cần: - Web Google login (Auth Code + PKCE). - Mobile Apple Sign In.
- `12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md:581` [high] Section Cạm bẫy (## dòng 579): "### 1. Skip state validation — Bẫy: Library auto-handles, you skip check. Fix: Always ve
- `12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md:11` [high] Lời dẫn dòng 11: "JWT thực thi đúng + Session management — 2 paradigm core. Bài này dạy: JWT anatomy + JWS/JWE/JWT khác 
- `12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md:31` [high] Dòng 31-38: "Bạn cần: - JWT format đúng (RS256, kid, jti). - Refresh token rotation + family detection. - Logout = inval
- `12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md:675` [high] Section Cạm bẫy (## dòng 673) chỉ có tiêu đề + 1 dòng Fix EN: "### 3. JWT in URL — Fix: Always Authorization header or h
- `12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md:33` [high] Dòng 33-40: "Bạn cần: - 1 nơi quản identity (IdP). - Đăng nhập 1 lần, dùng mọi tool (SSO). - Auto-create account khi onb
- `12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md:496` [high] Section Cạm bẫy (## dòng 494) chỉ có tiêu đề + dòng Fix EN: "### 1. SAML signature wrapping — Fix: Use library (python-s
- `02_tools/git-clients/github-desktop.md:16` [medium] Tiếp story. 1 đồng nghiệp junior FE đã follow git lessons + setup GitHub account.
- `02_tools/git-clients/github.md:262` [medium] Workflow chuẩn khi 2+ người làm chung. Tiếp bạn story:
- `02_tools/git-clients/github.md:739` [medium] **Q4.** Strangerd có thể đọc public repo bạn. Vậy sao đỡ leak?
- `02_tools/git-clients/gitlab.md:16` [medium] Tiếp bạn story. Bạn đổi việc sang **fintech startup**.
- `02_tools/ide/00_what-is-ide.md:172` [medium] Không có lựa chọn — submit App Store yêu cầu Xcode. Cài chỉ làm bạn miss-out gì cả vì Apple toolchain lock-in.
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:499` [medium] Dòng 502-504: "...ready to deploy (deploy manual trigger)... Both \"CD\" — confusing." và "DORA = bible đo DevOps perfor
- `10_devops/ci-cd/lessons/01_basic/03_pipeline-patterns.md:510` [medium] Dòng 510: "**Flaky test** = same code, sometimes pass sometimes fail. Bad signal!"
- `10_devops/ci-cd/lessons/01_basic/04_deploy-strategies.md:478` [medium] Dòng 478: "After deploy, **automated checks** verify basic functionality:" — lead-in §8 Smoke tests bằng EN.
- `10_devops/docker/lessons/02_intermediate/01_buildkit-and-multistage-advanced.md:94` [medium] Dòng 94: "Docker 23+ (2023) đã enable BuildKit mặc định — nhưng đáng check trước khi dùng feature mới. 2 lệnh dưới confi
- `10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md:331` [medium] Dòng 331: "**Attack scenario**: attacker compromise registry → push image với same tag nhưng malicious. Bạn pull, deploy
- `10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md:337` [medium] Dòng 337-348: "**Sigstore** (Linux Foundation, 2021) = ecosystem keyless signing cho artifacts." và các bước "1. Cosign 
- `10_devops/docker/lessons/02_intermediate/03_optimization-and-distroless.md:146` [medium] Dòng 146-150: "**Distroless** = image chứa **chỉ** application + runtime dependencies, **không**: ❌ Shell (no bash, sh) 
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:490` [medium] Dòng 501-509: đáp án Self-check toàn EN điện tín — "easy single resource, no learning curve. But: irreproducible, no aud
- `10_devops/iac/lessons/01_basic/01_terraform-basics.md:923` [medium] Dòng 926-934: đáp án Self-check toàn EN điện tín — "terraform init: (a) Download providers per required_providers. (b) S
- `10_devops/iac/lessons/01_basic/02_state-and-backend.md:603` [medium] Dòng 606-614: đáp án Self-check toàn EN điện tín — "(a) Laptop = single point of failure. (b) No collaboration...".
- `10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md:745` [medium] Dòng 748-754: đáp án Self-check toàn EN điện tín — "Both. **tfsec**: focused Terraform, fast, 100+ rules. **Checkov**: b
- `10_devops/kubernetes/lessons/02_intermediate/01_helm-package-manager.md:38` [medium] → **40 file YAML** trong repo. Mỗi file 50-80 dòng, similar nhau. (dòng thực 38, finding ghi 26)
- `10_devops/kubernetes/lessons/02_intermediate/02_ingress-cert-manager-tls.md:46` [medium] Customer email bão. Bạn lại renew manual, repeat 5 lần. (dòng thực 46, finding ghi 42)
- `10_devops/kubernetes/lessons/02_intermediate/03_statefulset-and-storage.md:49` [medium] emptyDir: {}     # ← AI! ephemeral
- `10_devops/kubernetes/lessons/02_intermediate/04_autoscaling-and-operators.md:1030` [medium] **Q2.** Why **scale-to-zero** powerful but tricky?
- `10_devops/kubernetes/lessons/02_intermediate/04_autoscaling-and-operators.md:11` [medium] > 🎯 *...Manual `kubectl scale` không kịp với load spike. **HPA** scale pod, **VPA** adjust limits, **Cluster Autoscaler*
- `10_devops/observability/lessons/01_basic/02_logs-loki-elk.md:452` [medium] Dòng 452-459: bảng log levels cột "When" toàn tiếng Anh điện-tín ("Function entry/exit, very verbose (rare in prod)", "U
- `10_devops/observability/lessons/02_intermediate/01_promql-deep-and-alerting.md:1089` [medium] Dòng 1089-1109: đáp án self-check Q1 trong <details> toàn tiếng Anh điện-tín ("False positive at high traffic", "No time
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:855` [medium] Dòng 859-874: đáp án self-check Q1 trong <details> toàn tiếng Anh điện-tín ("Cost vs benefit", "~10x infrastructure cost
- `11_cloud/cloudflare/README.md:9` [medium] > 🎯 *Cloudflare — vendor edge-first 320+ POPs toàn cầu. 3 trụ cột: Network (CDN/DNS/SSL), Security (WAF/Bot/DDoS/Zero Tr
- `11_cloud/digitalocean/README.md:9` [medium] > 🎯 *DigitalOcean — vendor developer-first, pricing predictable. Phù hợp startup, small/medium team. Alternative cho Her
- `11_cloud/digitalocean/lessons/01_basic/00_what-is-digitalocean-overview.md:11` [medium] Bài này dạy: DO là gì, niche, Team/Project hierarchy, doctl CLI, pricing flat, hands-on Droplet đầu tiên.
- `12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md:406` [medium] ### Strategy 1 — Short TTL only (dòng 406-411): "JWT TTL 5-15 min. No denylist. Revoke = wait for expire." và "Nhược điể
- `12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md:250` [medium] Dòng 250: "Now: admin click login → redirect to Keycloak → Keycloak redirect to Google → Google login → back to Keycloak
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:111` [low] [Web3 Architecture & Frontend Integration](../../15_specialized/blockchain/) 🚧 —RPC Nodes, Providers và Signers.
- `00_roadmaps/career/game-developer_career-roadmap.md:197` [low] Thiết lập các câu bắc cầu logic kết nối mượt mượt giữa các Stage.
- `02_tools/git-clients/github-desktop.md:269` [low] - **bạn (BE dev quen CLI)**: dùng `git` CLI + VS Code Source Control khi cần visual diff.
- `02_tools/git/lessons/03_advanced/00_undo-and-recovery.md:47` [low] **bạn tê người**. 6 tiếng code — biến mất.
- `03_languages/python/exercises/01_basic/01_basic-challenges.md:123` [low] """Calculates BMI and returns it as float."""
- `04_os/linux/lessons/01_basic/02_file-operations.md:177` [low] → Sometimes dùng để "force" Make/build system rebuild file đó.
- `04_os/linux/lessons/02_intermediate/01_systemd-services.md:422` [low] ### Vault rotation + size limit
- `04_os/linux/lessons/02_intermediate/02_ssh-deep-dive.md:131` [low] ### Behind scene
- `10_devops/docker/lessons/02_intermediate/01_buildkit-and-multistage-advanced.md:843` [low] Dòng 843: "→ Layer cache = all-or-nothing per layer. Cache mount = persistent storage shared across layer rebuilds." — c
- `10_devops/docker/lessons/02_intermediate/02_image-security-supply-chain.md:757` [low] Dòng 757-760: "1. Bạn (qua GitHub Actions) authenticate với Fulcio CA bằng OIDC token. 2. Fulcio issue cert ngắn hạn gắn
- `10_devops/docker/lessons/02_intermediate/03_optimization-and-distroless.md:162` [low] Dòng 162-167: "**Chainguard** (cgr.dev) image: - Built on Wolfi (minimal Linux distro, glibc). - **0 CVE policy** — auto
- `11_cloud/cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md:27` [low] Acme Shop dùng AWS S3 + CloudFront để serve static asset. ... Khách Việt Nam, Indonesia complain ảnh sản phẩm load chậm
- `11_cloud/cloudflare/lessons/01_basic/02_workers-and-pages.md:895` [low] - ➡️ **Bài tiếp theo:** [Cloudflare R2 + D1 + Queues — Storage & data layer ở edge](03_r2-and-d1-and-queues.md) — Storag
- `13_ai-ml/vector-search-and-embeddings/lessons/01_basic/00_what-is-vector-search-and-embeddings.md:25` [low] > Bài học này đang trong giai đoạn phát triển. Nội dung chi tiết sẽ được bổ sung theo chuẩn
- `16_career-soft-skills/README.md:12` [low] Line 12 under heading '## 🎯 Chủ đề này có gì': "Communication, Agile/Scrum, Career path, learning, technical writing, in

### EN_ONLY_TABLE (39)

- `10_devops/kubernetes/lessons/02_intermediate/00_intermediate-overview.md:384` [high] | Term | Vietnamese / Explanation | | **Helm** | Package manager cho K8s — `chart` template hóa YAML | | **Chart** | Hel
- `10_devops/kubernetes/lessons/02_intermediate/01_helm-package-manager.md:1414` [high] | Term | Vietnamese / Explanation | | **Helm** | Package manager cho K8s — install/upgrade/rollback chart | | **Release*
- `10_devops/kubernetes/lessons/02_intermediate/02_ingress-cert-manager-tls.md:1158` [high] | Term | Vietnamese / Explanation | | **Ingress** | K8s resource định nghĩa routing rules HTTP/HTTPS từ external → servi
- `10_devops/kubernetes/lessons/02_intermediate/03_statefulset-and-storage.md:1107` [high] | Term | Vietnamese / Explanation | | **StatefulSet** | Workload type cho stateful app: stable identity + per-pod PVC + 
- `10_devops/kubernetes/lessons/02_intermediate/04_autoscaling-and-operators.md:1209` [high] | Term | Vietnamese / Explanation | | **HPA** | Horizontal Pod Autoscaler — scale replica count theo metric | | **VPA** 
- `10_devops/observability/lessons/01_basic/00_what-is-observability.md:56` [high] Dòng 60-66: bảng Monitoring vs Observability, header (Aspect/Focus/Type/Data/Era) + value ("Is it broken?", Reactive, Pr
- `12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md:55` [high] Bảng OAuth vs OIDC dòng 55-62 toàn EN: "Purpose | Authorization (access resources) | Authentication (identify user)", "W
- `12_security/authentication/lessons/01_basic/03_jwt-and-sessions-deep.md:48` [high] Bảng Term clarification dòng 48-56 toàn EN: "Term | Description", "JWT | JSON Web Token — generic term cho JSON token (u
- `12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md:70` [high] Bảng Components dòng 70-77 cột Role toàn EN: "IdP (Identity Provider) | Authenticate user + issue assertion/token to app
- `12_security/authentication/lessons/01_basic/04_federation-sso-and-idp.md:85` [high] Bảng SAML vs OIDC dòng 85-94 cả header lẫn value EN: "Complexity | High (XML signature, encryption, canonicalization) | 
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:75` [medium] Dòng 75-79: header "| Practice | Auto deploy prod? | Common at |" với value "Everyone", "Enterprise, banking", "Tech sta
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:188` [medium] Dòng 188-197: "| Component | Role |" với cột Role toàn EN ("Event start pipeline (push, PR, schedule, manual)", "Group o
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:561` [medium] Dòng 563-569: cột "Ý nghĩa" toàn EN ("Continuous Integration — auto build + test on push", "Ready to deploy, manual trig
- `10_devops/ci-cd/lessons/01_basic/01_github-actions.md:231` [medium] Dòng 231-235: "| Type | Description |" với dữ liệu 3 cột lệch khỏi header 2 cột; value EN ("Node.js code, fast", "Contai
- `10_devops/ci-cd/lessons/01_basic/01_github-actions.md:861` [medium] Dòng 864-867: "| **Job** | Group of steps on a runner |", "| **Step** | Single command or action |", "| **Runner** | Mac
- `10_devops/ci-cd/lessons/01_basic/02_gitlab-ci.md:727` [medium] Dòng 730-731: "| **Stage** | Sequential phase (build/test/deploy) |", "| **Job** | Unit run inside stage |".
- `10_devops/ci-cd/lessons/01_basic/04_deploy-strategies.md:701` [medium] Dòng 703-704: "| **Recreate** | Stop all → start all (downtime) |", "| **Rolling update** | Gradual replace, default K8s
- `10_devops/docker/lessons/02_intermediate/04_registry-production-patterns.md:909` [medium] Dòng 909-918: bảng so sánh trong self-check Q3 toàn tiếng Anh cả header (Aspect / Harbor self-host / ECR managed) lẫn va
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:58` [medium] Dòng 58-67: bảng "| Benefit | Example |" với value toàn EN (Reproducibility | Recreate prod env in 30 min; Version contr
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:133` [medium] Dòng 135-150: bảng "| Tool | Year | Type | Notes |" + bảng Compare "| Tool | Pros | Cons | 2026 status |" toàn EN (De-fa
- `10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md:524` [medium] Dòng 524-532: bảng "| Aspect | Pulumi | Terraform |" toàn EN cả header lẫn value (Language | TS/Python/Go/C# real progra
- `10_devops/iac/lessons/02_intermediate/04_pulumi-cdk-crossplane.md:1214` [medium] Dòng 1214-1222: bảng "| Question | Lean to |" trong đáp án Q2 toàn EN (AWS only forever? | CDK; Multi-cloud possible? | 
- `10_devops/observability/lessons/01_basic/00_what-is-observability.md:553` [medium] Dòng 553-568: cột "Ý nghĩa" Glossary toàn tiếng Anh ("Ability to understand system from outputs", "Numeric time-series",
- `10_devops/observability/lessons/01_basic/00_what-is-observability.md:216` [medium] Dòng 220-228: bảng OSS stack header (Tool/Pillar/Notes) + cột Notes toàn EN ("Pull-based, time-series DB", "Prometheus f
- `10_devops/observability/lessons/01_basic/01_metrics-prometheus.md:440` [medium] Dòng 440-451: bảng Exporters header (Exporter/Source) + mô tả toàn EN ("Linux node metrics (CPU/RAM/disk/network)", "Con
- `10_devops/observability/lessons/01_basic/01_metrics-prometheus.md:751` [medium] Dòng 751-769: cột "Ý nghĩa" Glossary toàn tiếng Anh ("Time-series database", "Pull metrics from target", "Unique metric 
- `10_devops/observability/lessons/01_basic/02_logs-loki-elk.md:234` [medium] Dòng 234-241: bảng so sánh agents header (Agent/Language/Notes) + cột Notes toàn EN ("Loki default, K8s friendly", "Fast
- `10_devops/observability/lessons/01_basic/02_logs-loki-elk.md:666` [medium] Dòng 666-681: cột "Ý nghĩa" Glossary toàn EN ("JSON format", "Full-text index (Elasticsearch)", "Grafana logs, label-bas
- `10_devops/observability/lessons/01_basic/03_traces-opentelemetry.md:80` [medium] Dòng 80-88: bảng Span anatomy header (Field/Purpose) + cột Purpose toàn EN ("Unique per request (correlate cross-service
- `10_devops/observability/lessons/01_basic/03_traces-opentelemetry.md:679` [medium] Dòng 679-697: cột "Ý nghĩa" Glossary toàn tiếng Anh ("Track request across services", "Single operation in trace").
- `10_devops/observability/lessons/01_basic/04_grafana-and-alerting.md:684` [medium] Dòng 684-704: cột "Ý nghĩa" Glossary toàn tiếng Anh ("OSS dashboard tool", "Culture focus system fixes", "Routing + grou
- `10_devops/observability/lessons/02_intermediate/00_intermediate-overview.md:352` [medium] Dòng 352-374: Glossary header canonical đúng nhưng header bảng ghi "Vietnamese / Explanation" mà cột giá trị không có ti
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:1146` [medium] Dòng 1146-1164: Glossary header ghi "Vietnamese / Explanation" nhưng toàn bộ giải thích bằng tiếng Anh ("Service Level I
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:338` [medium] Dòng 338-347: bảng có header '| Tactic | Saving |' và value toàn EN: '**Pick close region** | 80% latency reduction', '*
- `12_security/authentication/lessons/01_basic/00_what-is-authentication.md:143` [medium] Bảng Decision dòng 143-150 toàn EN cả header lẫn value: "Use case | Pick", "Traditional web app same domain | Session + 
- `10_devops/ci-cd/lessons/02_intermediate/00_intermediate-overview.md:346` [low] Dòng 346-350: header "| Term | Vietnamese / Explanation |" nhưng value phần lớn EN ("Pattern: Git = single source of tru
- `10_devops/observability/lessons/01_basic/04_grafana-and-alerting.md:249` [low] Dòng 249-257: bảng contact points header (Type/Use) + cột Use toàn EN ("Webhook to Slack channel", "Incident escalation"
- `11_cloud/cloud-fundamentals/lessons/01_basic/01_regions-availability-zones-edge.md:300` [low] Dòng 300-306: header '| Distance | Min latency (one-way) |' EN; value 'Hanoi → Ho Chi Minh City (1100 km) | ~5.5ms' dùng
- `11_cloud/gcp/lessons/01_basic/01_compute-engine-and-disks.md:57` [low] Dòng 57-68: bảng 'Family overview' header '| Family | CPU | Use case | Pricing |' và value EN ở chỗ Việt-hoá được: 'Web 

### H_GLOSSARY (66)

- `01_foundations/computer-architecture-theory/lessons/01_basic/00_how-computer-works.md:153` [high] ## 📚 Glossary (Từ điển thuật ngữ)
- `07_web/frontend/html-css/lessons/01_basic/00_what-is-html-and-css.md:491` [high] ## 📘 Glossary
- `07_web/frontend/html-css/lessons/01_basic/01_html-essentials.md:625` [high] ## 📘 Glossary
- `07_web/frontend/html-css/lessons/01_basic/02_forms-and-accessibility.md:658` [high] ## 📘 Glossary
- `07_web/frontend/html-css/lessons/01_basic/03_css-fundamentals.md:740` [high] ## 📘 Glossary
- `07_web/frontend/html-css/lessons/01_basic/04_layout-flexbox-grid-responsive.md:738` [high] ## 📘 Glossary
- `07_web/frontend/javascript-dom/lessons/01_basic/00_what-is-javascript.md:539` [high] ## 📘 Glossary
- `07_web/frontend/javascript-dom/lessons/01_basic/01_variables-functions-types.md:791` [high] ## 📘 Glossary
- `07_web/frontend/javascript-dom/lessons/01_basic/02_dom-manipulation.md:630` [high] ## 📘 Glossary
- `07_web/frontend/javascript-dom/lessons/01_basic/03_events-and-async.md:773` [high] ## 📘 Glossary
- `07_web/frontend/javascript-dom/lessons/01_basic/04_fetch-and-modules.md:789` [high] ## 📘 Glossary
- `07_web/frontend/react/lessons/01_basic/00_what-is-react.md:595` [high] ## 📘 Glossary
- `07_web/frontend/react/lessons/01_basic/01_components-and-props.md:737` [high] ## 📘 Glossary
- `07_web/frontend/react/lessons/01_basic/02_state-and-events.md:764` [high] ## 📘 Glossary
- `07_web/frontend/react/lessons/01_basic/03_useeffect-and-fetch.md:646` [high] ## 📘 Glossary
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:714` [high] ## 📘 Glossary
- `10_devops/ci-cd/lessons/01_basic/00_what-is-cicd.md:559` [high] Dòng 559: "## 📘 Glossary" — bare English, dùng emoji 📘 và không có tiêu đề tiếng Việt canonical.
- `10_devops/ci-cd/lessons/01_basic/01_github-actions.md:859` [high] Dòng 859: "## 📘 Glossary" — bare English.
- `10_devops/ci-cd/lessons/01_basic/02_gitlab-ci.md:725` [high] Dòng 725: "## 📘 Glossary" — bare English.
- `10_devops/ci-cd/lessons/01_basic/03_pipeline-patterns.md:798` [high] Dòng 798: "## 📘 Glossary" — bare English.
- `10_devops/ci-cd/lessons/01_basic/04_deploy-strategies.md:699` [high] Dòng 699: "## 📘 Glossary" — bare English.
- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:558` [high] Dòng 558: "## 📘 Glossary" — heading trần dùng emoji sai (📘) và thiếu phần tiếng Việt.
- `10_devops/iac/lessons/01_basic/01_terraform-basics.md:1010` [high] Dòng 1010: "## 📘 Glossary" — heading trần, emoji 📘, không khớp canonical.
- `10_devops/iac/lessons/01_basic/02_state-and-backend.md:671` [high] Dòng 671: "## 📘 Glossary" — heading trần, emoji 📘.
- `10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md:805` [high] Dòng 805: "## 📘 Glossary" — heading trần, emoji 📘.
- `10_devops/observability/lessons/01_basic/00_what-is-observability.md:549` [high] Dòng 549: "## 📘 Glossary" — heading trần, sai emoji (📘 thay vì 📚) và thiếu phần tiếng Việt.
- `10_devops/observability/lessons/01_basic/01_metrics-prometheus.md:749` [high] Dòng 749: "## 📘 Glossary" — heading trần, sai emoji + thiếu tiếng Việt.
- `10_devops/observability/lessons/01_basic/02_logs-loki-elk.md:664` [high] Dòng 664: "## 📘 Glossary" — heading trần, sai emoji + thiếu tiếng Việt.
- `10_devops/observability/lessons/01_basic/03_traces-opentelemetry.md:677` [high] Dòng 677: "## 📘 Glossary" — heading trần, sai emoji + thiếu tiếng Việt.
- `10_devops/observability/lessons/01_basic/04_grafana-and-alerting.md:682` [high] Dòng 682: "## 📘 Glossary" — heading trần, sai emoji + thiếu tiếng Việt.
- `03_languages/python/lessons/01_basic/00_what-is-python.md:288` [medium] ## 📚 Thuật Ngữ Cần Nhớ (Glossary)
- `03_languages/python/lessons/01_basic/01_variables-and-types.md:571` [medium] ## 📚 Thuật Ngữ Cần Nhớ (Glossary)
- `03_languages/python/lessons/01_basic/02_control-flow.md:534` [medium] ## 📚 Thuật Ngữ Cần Nhớ (Glossary)
- `03_languages/python/lessons/01_basic/03_functions.md:486` [medium] ## 📚 Thuật Ngữ Cần Nhớ (Glossary)
- `04_os/linux/lessons/02_intermediate/00_users-and-permissions.md:516` [medium] ## 📘 Glossary
- `04_os/linux/lessons/02_intermediate/01_systemd-services.md:620` [medium] ## 📘 Glossary
- `04_os/linux/lessons/02_intermediate/02_ssh-deep-dive.md:640` [medium] ## 📘 Glossary
- `04_os/linux/lessons/02_intermediate/03_package-management.md:581` [medium] ## 📘 Glossary
- `04_os/linux/lessons/02_intermediate/04_text-processing-advanced.md:608` [medium] ## 📘 Glossary
- `05_networking/dns/lessons/01_basic/00_what-is-dns.md:343` [medium] Dòng 343: "## 📘 Glossary" — heading trần, sai emoji (📘 thay vì 📚) và thiếu tiêu đề tiếng Việt.
- `05_networking/dns/lessons/01_basic/01_dns-records.md:469` [medium] Dòng 469: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/dns/lessons/01_basic/02_dns-resolution.md:413` [medium] Dòng 413: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/dns/lessons/01_basic/03_dns-tools.md:536` [medium] Dòng 536: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/dns/lessons/01_basic/04_dns-setup-and-security.md:444` [medium] Dòng 444: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md:420` [medium] Dòng 420: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/00_what-is-tcp-ip.md:360` [medium] Dòng 360: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/01_ip-addressing.md:496` [medium] Dòng 496: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/02_tcp-vs-udp.md:435` [medium] Dòng 435: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/03_ports-sockets-firewall.md:475` [medium] Dòng 475: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/04_network-tools.md:594` [medium] Dòng 594: "## 📘 Glossary" — heading trần, sai emoji, thiếu tiêu đề tiếng Việt.
- `06_databases/postgresql/lessons/01_basic/00_what-is-postgresql.md:542` [medium] ## 📘 Glossary
- `06_databases/postgresql/lessons/01_basic/01_psql-and-meta-commands.md:655` [medium] ## 📘 Glossary
- `06_databases/postgresql/lessons/01_basic/02_indexes-and-performance.md:574` [medium] ## 📘 Glossary
- `06_databases/postgresql/lessons/01_basic/03_jsonb-and-arrays.md:661` [medium] ## 📘 Glossary
- `06_databases/postgresql/lessons/01_basic/04_backup-and-replication.md:677` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/00_what-is-sql.md:434` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/01_select-and-filter.md:610` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/02_aggregations.md:493` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/03_joins.md:633` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/04_insert-update-delete.md:650` [medium] ## 📘 Glossary
- `06_databases/sql-fundamentals/lessons/01_basic/05_schema-design-basics.md:751` [medium] ## 📘 Glossary
- `07_web/backend/python-fastapi/lessons/01_basic/00_what-is-fastapi.md:503` [medium] ## 📘 Glossary
- `07_web/backend/python-fastapi/lessons/01_basic/01_routes-and-parameters.md:577` [medium] ## 📘 Glossary
- `07_web/backend/python-fastapi/lessons/01_basic/02_pydantic-models.md:580` [medium] ## 📘 Glossary
- `07_web/backend/python-fastapi/lessons/01_basic/03_database-with-sqlmodel.md:585` [medium] ## 📘 Glossary
- `07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md:580` [medium] ## 📘 Glossary

### H_CHEATSHEET (22)

- `01_foundations/computing-environment/lessons/01_basic/02_filesystem-concept.md:439` [high] ## ⚡ Cheatsheet — Path symbols
- `07_web/frontend/html-css/lessons/01_basic/01_html-essentials.md:567` [high] ## ⚡ Cheatsheet
- `07_web/frontend/javascript-dom/lessons/01_basic/01_variables-functions-types.md:728` [high] ## ⚡ Cheatsheet
- `07_web/frontend/javascript-dom/lessons/01_basic/02_dom-manipulation.md:575` [high] ## ⚡ Cheatsheet
- `07_web/frontend/react/lessons/01_basic/00_what-is-react.md:544` [high] ## ⚡ Cheatsheet
- `07_web/frontend/react/lessons/01_basic/02_state-and-events.md:712` [high] ## ⚡ Cheatsheet
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:644` [high] ## ⚡ Cheatsheet
- `03_languages/python/lessons/01_basic/01_variables-and-types.md:547` [medium] ## 📋 Bảng Tra Cứu Nhanh (Cheatsheet) Dành Cho Dev
- `03_languages/python/lessons/01_basic/02_control-flow.md:507` [medium] ## 📋 Bảng Tra Cứu Nhanh (Cheatsheet) Về Vòng Lặp
- `03_languages/python/lessons/01_basic/03_functions.md:465` [medium] ## 📋 Bảng Tra Cứu Nhanh (Cheatsheet) Về Thiết Kế Hàm
- `04_os/linux/lessons/02_intermediate/03_package-management.md:531` [medium] ## ⚡ Cheatsheet
- `05_networking/dns/lessons/01_basic/01_dns-records.md:442` [medium] Dòng 442: "## ⚡ Cheatsheet" — heading trần, thiếu cụm canonical "Tra cứu nhanh".
- `05_networking/http-https/lessons/01_basic/02_http-status-codes.md:567` [medium] Dòng 567: "## ⚡ Cheatsheet — 11 mã MUST-KNOW" — thiếu cụm canonical "Tra cứu nhanh".
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/03_ports-sockets-firewall.md:417` [medium] Dòng 417: "## ⚡ Cheatsheet" — heading trần, thiếu cụm canonical "Tra cứu nhanh".
- `06_databases/postgresql/lessons/01_basic/00_what-is-postgresql.md:482` [medium] ## ⚡ Cheatsheet
- `06_databases/sql-fundamentals/lessons/01_basic/01_select-and-filter.md:542` [medium] ## ⚡ Cheatsheet
- `06_databases/sql-fundamentals/lessons/01_basic/02_aggregations.md:436` [medium] ## ⚡ Cheatsheet
- `06_databases/sql-fundamentals/lessons/01_basic/03_joins.md:578` [medium] ## ⚡ Cheatsheet
- `06_databases/sql-fundamentals/lessons/01_basic/04_insert-update-delete.md:575` [medium] ## ⚡ Cheatsheet
- `07_web/backend/python-fastapi/lessons/01_basic/01_routes-and-parameters.md:525` [medium] ## ⚡ Cheatsheet
- `07_web/backend/python-fastapi/lessons/01_basic/02_pydantic-models.md:521` [medium] ## ⚡ Cheatsheet
- `10_devops/kubernetes/00_kubernetes-complete-guide.md:3088` [low] ## 28. Cheatsheet — lệnh phải thuộc

### H_CHANGELOG (19)

- `07_web/frontend/html-css/lessons/01_basic/01_html-essentials.md:666` [high] ## 📌 Changelog
- `07_web/frontend/javascript-dom/lessons/01_basic/01_variables-functions-types.md:833` [high] ## 📌 Changelog
- `07_web/frontend/javascript-dom/lessons/01_basic/02_dom-manipulation.md:673` [high] ## 📌 Changelog
- `07_web/frontend/react/lessons/01_basic/00_what-is-react.md:642` [high] ## 📌 Changelog
- `07_web/frontend/react/lessons/01_basic/02_state-and-events.md:803` [high] ## 📌 Changelog
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:759` [high] ## 📌 Changelog
- `10_devops/observability/lessons/01_basic/01_metrics-prometheus.md:797` [high] Dòng 797: "## 📜 Changelog" — heading trần, sai emoji (📜 thay vì 📌) + thiếu tiếng Việt.
- `10_devops/observability/lessons/01_basic/03_traces-opentelemetry.md:722` [high] Dòng 722: "## 📜 Changelog" — heading trần, sai emoji + thiếu tiếng Việt.
- `10_devops/observability/lessons/01_basic/04_grafana-and-alerting.md:731` [high] Dòng 731: "## 📜 Changelog" — heading trần, sai emoji + thiếu tiếng Việt.
- `04_os/linux/lessons/02_intermediate/03_package-management.md:622` [medium] ## 📌 Changelog
- `05_networking/dns/lessons/01_basic/01_dns-records.md:511` [medium] Dòng 511: "## 📌 Changelog" — heading trần, thiếu cụm "Nhật ký thay đổi".
- `05_networking/tcp-ip-fundamentals/lessons/01_basic/03_ports-sockets-firewall.md:518` [medium] Dòng 518: "## 📌 Changelog" — heading trần, thiếu cụm "Nhật ký thay đổi".
- `06_databases/postgresql/lessons/01_basic/00_what-is-postgresql.md:588` [medium] ## 📌 Changelog
- `06_databases/sql-fundamentals/lessons/01_basic/01_select-and-filter.md:647` [medium] ## 📌 Changelog
- `06_databases/sql-fundamentals/lessons/01_basic/02_aggregations.md:526` [medium] ## 📌 Changelog
- `06_databases/sql-fundamentals/lessons/01_basic/03_joins.md:670` [medium] ## 📌 Changelog
- `06_databases/sql-fundamentals/lessons/01_basic/04_insert-update-delete.md:687` [medium] ## 📌 Changelog
- `07_web/backend/python-fastapi/lessons/01_basic/01_routes-and-parameters.md:614` [medium] ## 📌 Changelog
- `07_web/backend/python-fastapi/lessons/01_basic/02_pydantic-models.md:617` [medium] ## 📌 Changelog

### H_PITFALL (1)

- `04_os/linux/lessons/01_basic/03_view-file-content.md:147` [medium] #### ⚠️ Pitfall: `cat` file dài → spam terminal

### H_SELFCHECK (1)

- `10_devops/kubernetes/lessons/01_basic/04_namespaces-and-rbac.md:848` [low] ## ✅ Bài Tập Tự Đánh Giá Tư Duy Cốt Lõi (trong khi 4 bài cùng cụm 00-03 đều dùng '## 🧠 Tự kiểm tra (Self-check)')

### H_LINKS (2)

- `11_cloud/cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md:727` [medium] - ➡️ **Bài tiếp theo:** [Page Rules → Rules engine migration](https://developers.cloudflare.com/rules/page-rules/migrati
- `11_cloud/cloudflare/lessons/01_basic/02_workers-and-pages.md:904` [low] ### Tài nguyên ngoài (2026)

### H_BRIDGE (12)

- `00_roadmaps/career/blockchain-developer_career-roadmap.md:68` [medium] >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:98` [medium] >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:118` [medium] >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/blockchain-developer_career-roadmap.md:143` [medium] >  puente **Cầu nối sang Stage 5**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:66` [medium] >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:87` [medium] >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:113` [medium] >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/data-scientist_career-roadmap.md:134` [medium] >  puente **Cầu nối sang Stage 5**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:68` [medium] >  puente **Cầu nối sang Stage 2**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:89` [medium] >  puente **Cầu nối sang Stage 3**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:110` [medium] >  puente **Cầu nối sang Stage 4**:
- `00_roadmaps/career/mobile-developer_career-roadmap.md:132` [medium] >  puente **Cầu nối sang Stage 5**:

### NAV_PATHTEXT (22)

- `11_cloud/cloud-cost-management/README.md:57` [medium] Dòng 57: "- ⬅️ **Bài trước:** [Infracost](https://www.infracost.io/) — xem trước chi phí ngay trong Pull Request" — nằm 
- `11_cloud/cloudflare/README.md:15` [medium] - [00_what-is-cloudflare-overview](lessons/01_basic/00_what-is-cloudflare-overview.md)
- `01_foundations/computing-environment/lessons/01_basic/01_what-is-shell.md:339` [low] | ➡️ Bài tiếp | [02_filesystem-concept.md](./02_filesystem-concept.md) — chưa có |
- `01_foundations/computing-environment/lessons/01_basic/02_filesystem-concept.md:491` [low] | ⬅️ Bài trước | [01_what-is-shell.md](./01_what-is-shell.md) — Shell concept |
- `01_foundations/computing-environment/lessons/01_basic/02_filesystem-concept.md:492` [low] | ➡️ Bài tiếp | [03_process-and-pid.md](./03_process-and-pid.md) — chưa có |
- `01_foundations/computing-environment/lessons/01_basic/03_process-and-pid.md:475` [low] | ⬅️ Bài trước | [02_filesystem-concept.md](./02_filesystem-concept.md) — Filesystem concept |
- `01_foundations/computing-environment/lessons/01_basic/03_process-and-pid.md:476` [low] | ➡️ Bài tiếp | [04_env-variables.md](./04_env-variables.md) — chưa có |
- `01_foundations/computing-environment/lessons/01_basic/04_env-variables.md:619` [low] | ⬅️ Bài trước | [03_process-and-pid.md](./03_process-and-pid.md) — Process concept (env theo process) |
- `01_foundations/computing-environment/lessons/01_basic/04_env-variables.md:620` [low] | ➡️ Bài tiếp | [05_io-redirection.md](./05_io-redirection.md) — chưa có |
- `01_foundations/computing-environment/lessons/01_basic/05_io-redirection.md:616` [low] | ⬅️ Bài trước | [04_env-variables.md](./04_env-variables.md) — Env vars |
- `04_os/linux/lessons/01_basic/01_navigation.md:421` [low] | ➡️ Bài tiếp | [02_file-operations.md](./02_file-operations.md) — mkdir, touch, cp, mv, rm |
- `04_os/linux/lessons/01_basic/02_file-operations.md:503` [low] | ⬅️ Bài trước | [01_navigation.md](./01_navigation.md) |
- `04_os/linux/lessons/01_basic/02_file-operations.md:504` [low] | ➡️ Bài tiếp | [03_view-file-content.md](./03_view-file-content.md) — cat, less, head, tail |
- `04_os/linux/lessons/01_basic/02_file-operations.md:9` [low] **Prerequisites:** [01_navigation.md](./01_navigation.md)
- `04_os/linux/lessons/01_basic/03_view-file-content.md:9` [low] **Prerequisites:** [01_navigation.md](./01_navigation.md), [02_file-operations.md](./02_file-operations.md)
- `04_os/linux/lessons/01_basic/03_view-file-content.md:409` [low] | ⬅️ Bài trước | [02_file-operations.md](./02_file-operations.md) |
- `10_devops/docker/README.md:29` [low] Dòng 29: "- ✅ 🌟 [`setup/install-docker.md`](./setup/install-docker.md) — Cài đặt Docker Desktop & Engine trên macOS, Win
- `10_devops/docker/lessons/02_intermediate/README.md:15` [low] Dòng 15: "- **Bạn xong basic 4 bài?** → vào [00_intermediate-overview](00_intermediate-overview.md) để map lộ trình." — 
- `11_cloud/cloud-cost-management/lessons/01_basic/02_tagging-allocation-and-showback.md:9` [low] Dòng 9: "> **Yêu cầu trước:** [01_pricing-models-deep.md](01_pricing-models-deep.md)" — dùng đường dẫn file làm link-tex
- `11_cloud/cloud-cost-management/lessons/01_basic/04_finops-tools-and-automation.md:9` [low] Dòng 9: "> **Yêu cầu trước:** [03_optimization-tactics-compute-storage-network.md](03_optimization-tactics-compute-stora
- `11_cloud/multi-cloud-strategies/lessons/01_basic/03_kubernetes-multi-cloud-and-anthos-arc.md:900` [low] Dòng 900: "- ↑ **Về cụm:** [IaC Terraform](../../../../10_devops/iac/) — provisioning cho Cluster API". Marker '↑ Về cụm
- `15_specialized/README.md:32` [low] Line 32: '| 🧭 Theo roadmap | Xem [`../00_roadmaps/career/`](../00_roadmaps/career/) chọn career path đi qua chủ đề này |

### NAME_RESIDUE (11)

- `01_foundations/computing-environment/lessons/01_basic/02_filesystem-concept.md:72` [high] │   └── rom/               ← = ~  (Linux user)
- `01_foundations/computing-environment/lessons/01_basic/02_filesystem-concept.md:79` [high] │   └── rom/               ← = ~  (Mac user)
- `10_devops/ci-cd/lessons/02_intermediate/03_secret-management.md:1026` [high] Dòng 1026: "**bạn TTL** (e.g., 24 hours):" — đối xứng với "**Short TTL** (e.g., 15 minutes):" ở dòng 1020.
- `10_devops/observability/lessons/02_intermediate/04_sre-practices.md:197` [high] Dòng 197: "Severity   Short window  bạn window   Budget in 1 hour" — "Long" bị bulk-replace nhầm thành "bạn".
- `11_cloud/cloud-cost-management/lessons/01_basic/02_tagging-allocation-and-showback.md:54` [high] Dòng 54: "| `owner` | Người chịu trách nhiệm cuối | `thien.le`, `team-backend` (email/Slack handle) |". `thien.le` trùng
- `02_tools/git/lessons/01_basic/02_remote-and-github-basic.md:87` [medium] git push https://github.com/romdev/my-first-git-project.git main
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:574` [medium] <Link to="/">🛒 bạn Shop</Link>
- `07_web/frontend/react/lessons/01_basic/04_routing-and-context.md:587` [medium] <footer>© 2026 bạn Shop</footer>
- `MASTER-CATALOG.md:1056` [medium] `01_dns-records.md` (~480 dòng) — ... ALIAS/CNAME flattening, zone đầy đủ cho longshop.vn
- `03_languages/python/lessons/01_basic/01_variables-and-types.md:330` [low] "email": "rom@example.com",
- `10_devops/ci-cd/lessons/02_intermediate/README.md:56` [low] README.md dòng 56: "- [ ] Pre-commit gitleaks + CI scan blockmọi secret leak" — dính chữ "blockmọi".

### HEADER_THEN_CODE (10)

- `10_devops/iac/lessons/01_basic/01_terraform-basics.md:209` [medium] Dòng 209-216: "## 4️⃣ Providers" → ngay dưới "**Provider** = plugin for specific cloud/service." → "### Major providers"
- `10_devops/iac/lessons/01_basic/02_state-and-backend.md:240` [medium] Dòng 240-251: "## 4️⃣ `terraform state` subcommands" → "### List" → ngay code block `terraform state list`, không có lea
- `10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md:111` [medium] Dòng 111-118: "## 2️⃣ Cost estimation — Infracost" → "Estimate AWS/GCP/Azure cost from Terraform plan." → "### Install" 
- `12_security/authentication/lessons/01_basic/02_oauth-and-oidc.md:210` [medium] Dòng 210 heading "## 3️⃣ Other flows" nhảy ngay vào "### Device Authorization Flow" với lead-in nửa Anh nửa Việt cụt dòn
- `10_devops/ci-cd/lessons/01_basic/01_github-actions.md:227` [low] Dòng 225-235: ngay sau "## 4️⃣ Actions — Building blocks" chỉ có 1 dòng định nghĩa cụt "**Action** = pre-built reusable 
- `10_devops/kubernetes/lessons/02_intermediate/00_intermediate-overview.md:62` [low] ## 1️⃣ Vì sao 4 mảng này quan trọng?  ### Helm — Package manager của K8s  **Vấn đề**: Production cluster có 50+ Deployme
- `11_cloud/cloudflare/lessons/01_basic/01_cdn-dns-and-ssl.md:60` [low] ### Records cơ bản  | Type | Mục đích | Ví dụ |
- `11_cloud/cloudflare/lessons/01_basic/03_r2-and-d1-and-queues.md:250` [low] ### Use case D1 phù hợp  - ✅ Catalog (read-heavy, write hiếm)
- `11_cloud/digitalocean/lessons/01_basic/00_what-is-digitalocean-overview.md:99` [low] ### Compute  | Service | Mô tả | Analog AWS | Khi dùng |
- `11_cloud/digitalocean/lessons/01_basic/01_droplets-and-volumes.md:366` [low] ## 5️⃣ Snapshot vs Image — Backup & Clone  ### Khác nhau  | | Snapshot | Custom Image |

### META_INCOMPLETE (8)

- `11_cloud/cloudflare/README.md:7` [low] > **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)
- `11_cloud/digitalocean/README.md:7` [low] > **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)
- `15_specialized/ar-vr/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*
- `15_specialized/blockchain/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*
- `15_specialized/embedded-iot/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*
- `15_specialized/game-dev/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*
- `15_specialized/quantum-computing/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*
- `15_specialized/robotics/README.md:4` [low] Lines 3-6: '> **Tác giả:** Mr.Rom' / '> **Phiên bản:** v0.1.0 (skeleton)' / '> **Cập nhật:** 20/05/2026' / '> **Status:*

### EN_TERM_UNDEFINED (5)

- `08_mobile/react-native/lessons/01_basic/00_what-is-react-native.md:10` [low] > 🎯 *React Native là framework cross-platform cho phép bạn xây dựng ứng dụng iOS và Android bằng JavaScript/TypeScript v
- `14_data-engineering/airflow-and-orchestration/lessons/01_basic/00_what-is-airflow-and-orchestration.md:10` [low] Dòng 10 (TL;DR): "> 🎯 *Apache Airflow là nền tảng quản lý và lập lịch data pipeline. Data Orchestration điều phối các bư
- `14_data-engineering/data-lake/lessons/01_basic/00_what-is-data-lake.md:10` [low] Dòng 10 (TL;DR): "> 🎯 *Data Lake là hệ thống lưu trữ dữ liệu thô ở mọi định dạng (structured, semi-structured, unstructu
- `14_data-engineering/dbt/lessons/01_basic/00_what-is-dbt.md:10` [low] Dòng 10 (TL;DR): "> 🎯 *dbt (data build tool) là công cụ transform dữ liệu trong warehouse bằng SQL. Hỗ trợ version contr
- `14_data-engineering/streaming/lessons/01_basic/00_what-is-streaming.md:10` [low] Dòng 10 (TL;DR): "> 🎯 *Data Streaming xử lý dữ liệu real-time khi nó phát sinh (Kafka, Pulsar, Kinesis), thay vì batch p

### TIME_ESTIMATE (3)

- `11_cloud/multi-cloud-strategies/README.md:36` [medium] Dòng 36: "→ Phần thực hành (*hands-on*) trải dài khoảng **6–8 giờ** nếu bạn làm trọn vẹn các bài lab." — ước tính thời l
- `02_tools/git/lessons/01_basic/00_what-is-git.md:242` [low] | # | Bài | Học gì | Thời gian | ... | 01 | ... | 20 phút | ... | 03 | ... | 25 phút |
- `13_ai-ml/llm/lessons/01_basic/04_llm-app-cost-eval-and-production.md:662` [low] → **5 bài, ~110p đọc, ~10-15h hands-on**. Output: production-ready LLM app skill.

### MISSING_METAPHOR (2)

- `10_devops/iac/lessons/01_basic/00_what-is-iac.md:256` [medium] Toàn file grep "🪞" = 0 kết quả; §5 State và §6 Mutable vs Immutable (dòng 256-287) không có ẩn dụ đời thường. Đối chiếu 
- `10_devops/iac/lessons/01_basic/01_terraform-basics.md:115` [low] Toàn file grep "🪞"/"ẩn dụ" = 0; §3 HCL, resource vs data source, count vs for_each không có ẩn dụ đời thường.

### MISSING_GLOSSARY (1)

- `10_devops/kubernetes/00_kubernetes-complete-guide.md:1` [medium] File 3325 dòng dày đặc thuật ngữ EN (Pod, ReplicaSet, StatefulSet, reconciliation, headless, provisioner...) nhưng grep 