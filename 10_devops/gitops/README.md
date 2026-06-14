# ⚓ GitOps — Declarative Continuous Delivery

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 14/06/2026

> 🎯 *GitOps dùng Git làm nguồn chân lý duy nhất (Single Source of Truth) cho cả cấu hình app + hạ tầng: mọi thay đổi đi qua commit/PR, và một agent trong cluster **liên tục đồng bộ** trạng thái thật về đúng những gì khai trong Git. Kết quả: triển khai có audit, rollback bằng `git revert`, tự phát hiện + sửa drift, và CI không cần quyền vào cluster. Chủ đề này dạy từ nguyên tắc + ArgoCD/Flux, cấu trúc repo, quản lý secret, reconciliation, cho tới vận hành đa cluster/đa team ở production.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu GitOps là gì + **4 nguyên tắc OpenGitOps**, phân biệt **push-based vs pull-based** deploy
- [x] So sánh + chọn giữa **ArgoCD** và **Flux**
- [x] Thiết kế **cấu trúc repo GitOps** (tách config repo, env promotion với Kustomize overlays, app-of-apps)
- [x] Quản lý **secret an toàn** trong Git: Sealed Secrets / SOPS / External Secrets Operator
- [x] Hiểu **reconciliation loop**: sync auto/manual, self-heal, prune, drift, sync waves, rollback
- [x] (Intermediate) Quản nhiều app/cluster (**ApplicationSet**), **progressive delivery**, multi-tenancy, security + observability + DR

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng GitOps (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`GitOps là gì`](./lessons/01_basic/00_what-is-gitops.md) | 🌱 Intro | ✅ | 4 nguyên tắc OpenGitOps, Git = single source of truth, push vs pull deploy, lợi ích (audit/rollback/drift), GitOps vs CI/CD. |
| **01** | [`ArgoCD vs Flux`](./lessons/01_basic/01_flux-vs-argocd.md) | 🌳 Lesson | ✅ | Hai GitOps engine CNCF Graduated: kiến trúc, Application CRD vs GitOps Toolkit, bảng so sánh, chọn cái nào. |
| **02** | [`Cấu trúc Repo GitOps`](./lessons/01_basic/02_repository-structure-and-patterns.md) | 🌳 Lesson | ✅ | Tách config repo, monorepo vs polyrepo, env promotion (Kustomize base+overlays), app-of-apps, promotion qua PR. |
| **03** | [`Secrets trong GitOps`](./lessons/01_basic/03_secrets-in-gitops.md) | 🌳 Lesson | ✅ | Không commit secret plaintext; Sealed Secrets, SOPS (age/KMS), External Secrets Operator — so sánh + chọn. |
| **04** | [`Sync, Drift & Reconciliation`](./lessons/01_basic/04_sync-drift-and-reconciliation.md) | 🌳 Lesson | ✅ | Reconciliation loop, sync auto/manual, self-heal + prune, drift, sync waves/hooks, rollback = git revert. |

### 📖 Lộ trình Intermediate — Quy mô Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | 🚧 | GitOps quy mô lớn: nhiều app/team/cluster, progressive delivery, security/observability/DR. |
| **01** | [`App-of-Apps & ApplicationSet`](./lessons/02_intermediate/01_app-of-apps-and-applicationset.md) | 🌳 Lesson | 🚧 | Quản nhiều app/cluster: ArgoCD app-of-apps + ApplicationSet generators, Flux multi-tenancy, scaling. |
| **02** | [`Progressive Delivery với Argo Rollouts`](./lessons/02_intermediate/02_progressive-delivery-with-argo-rollouts.md) | 🌳 Lesson | 🚧 | Canary/blue-green GitOps-native: Argo Rollouts / Flagger, analysis metric-based, tích hợp mesh/ingress. |
| **03** | [`Multi-Cluster & Multi-Tenancy`](./lessons/02_intermediate/03_multi-cluster-and-multi-tenancy.md) | 🌳 Lesson | 🚧 | Quản nhiều cluster (ApplicationSet cluster generator), AppProject + RBAC, hub-spoke, namespace isolation. |
| **04** | [`Security, Observability & DR`](./lessons/02_intermediate/04_security-observability-and-dr.md) | 🌳 Lesson | 🚧 | RBAC + AppProject restriction + signed commit, metrics/notification/alert sync, disaster recovery cho ArgoCD/Flux. |

> 🚧 = đang biên soạn trong đợt hoàn thiện nhánh DevOps (06/2026).

> 💡 **Lưu ý:** Hands-on chuyên sâu **ArgoCD** (cài đặt, Application, sync) đã có ở **CI/CD Intermediate** — [`../ci-cd/lessons/02_intermediate/01_gitops-with-argocd.md`](../ci-cd/lessons/02_intermediate/01_gitops-with-argocd.md). Cụm này bổ sung góc nhìn phương pháp luận + Flux + repo patterns + secrets + reconciliation + vận hành production.

---

## 🚀 Lộ trình đề xuất

- **Beginner:** Đọc [Bài 00](./lessons/01_basic/00_what-is-gitops.md) nắm 4 nguyên tắc + pull-based, rồi [ArgoCD vs Flux](./lessons/01_basic/01_flux-vs-argocd.md) để chọn công cụ. Thực hành [cấu trúc repo](./lessons/01_basic/02_repository-structure-and-patterns.md) + [secrets](./lessons/01_basic/03_secrets-in-gitops.md), và hiểu [reconciliation](./lessons/01_basic/04_sync-drift-and-reconciliation.md) — trái tim của GitOps.
- **Intermediate:** Quản nhiều app/cluster với [ApplicationSet](./lessons/02_intermediate/01_app-of-apps-and-applicationset.md); deploy an toàn với [Progressive Delivery](./lessons/02_intermediate/02_progressive-delivery-with-argo-rollouts.md); siết bảo mật + giám sát + DR ở [bài 04](./lessons/02_intermediate/04_security-observability-and-dr.md).

## 🔗 Liên kết cụm liên quan

- [CI/CD](../ci-cd/) — CI build/test, CD = GitOps; ArgoCD hands-on ở ci-cd intermediate.
- [Kubernetes](../kubernetes/) — GitOps đồng bộ manifest K8s; ConfigMaps/Secrets.
- [IaC](../iac/) — GitOps cho app/config; IaC (Terraform) cho hạ tầng — bổ trợ nhau.
- [Service Mesh](../service-mesh/) — progressive delivery thường phối hợp mesh routing.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
- **v0.2.0 (26/05/2026)** — Cập nhật trạng thái có 1 bài lesson Basic placeholder.
- **v1.0.0 (14/06/2026)** — Hoàn thiện cụm **Basic 5/5** (4 nguyên tắc + ArgoCD/Flux + repo structure + secrets + reconciliation). Bổ sung lộ trình Intermediate (đang biên soạn).
