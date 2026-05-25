# 🔁 CI/CD — Intermediate cluster

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Intermediate cluster hoàn thành (5/5 bài)

> 🎯 *Từ "deploy được" → "supply chain secure + GitOps + progressive". Build trên CI/CD basic (5 bài). Cluster intermediate thứ 3 của `10_DevOps/`. Apply 4 insight từ `__Ref__/` (GitOps anti-pattern, 12-factor, SLSA, progressive). Output: pipeline SOC2-compliant + auto-rollback.*

---

## 🚀 Quick start

- **Đã xong basic?** → [00_intermediate-overview](00_intermediate-overview.md).
- **Push deploy CI khổ?** → [01_gitops-with-argocd](01_gitops-with-argocd.md).
- **SOC2 audit fail?** → [02_supply-chain-security](02_supply-chain-security.md).
- **Secret leak vào Git?** → [03_secret-management](03_secret-management.md).
- **Deploy v2 lỗi all-or-nothing $80K loss?** → [04_progressive-delivery](04_progressive-delivery.md).

---

## 📂 Cấu trúc cluster

```
02_intermediate/
├── README.md                              ← (file này)
├── 00_intermediate-overview.md             ← Intro, không hands-on
├── 01_gitops-with-argocd.md
├── 02_supply-chain-security.md
├── 03_secret-management.md
└── 04_progressive-delivery.md
```

---

## 📖 Lessons — Intermediate cluster (5 bài)

| # | Bài | Trọng tâm | Tag | Thời lượng |
|---|---|---|---|---|
| 00 | [Intermediate overview](00_intermediate-overview.md) | Map 4 mảng + tool stack 2026 + 4 production incident scenarios | MUST-KNOW | ~13p |
| 01 | [GitOps với ArgoCD](01_gitops-with-argocd.md) | ArgoCD architecture + Application + ApplicationSet (4 generators) + multi-cluster + sync waves + RBAC + ArgoCD vs Flux | MUST-KNOW | ~25p |
| 02 | [Supply chain security](02_supply-chain-security.md) | SLSA Level 3 + provenance attestation + cosign full chain + Kyverno admission verify + vulnerability lifecycle | MUST-KNOW | ~22p |
| 03 | [Secret management](03_secret-management.md) | 12-factor + Vault + ESO + Sealed Secrets + SOPS + dynamic credentials + gitleaks + IRSA | MUST-KNOW | ~22p |
| 04 | [Progressive delivery](04_progressive-delivery.md) | Argo Rollouts canary + AnalysisTemplate auto-rollback + traffic shifting (nginx/Istio) + Feature flags (OpenFeature/Unleash) | MUST-KNOW | ~25p |

→ **Tổng ~107 phút đọc + 6-8h hands-on**. Sau cluster: CI/CD production-grade tier-1, SOC2-ready.

---

## 🎯 Sau cluster bạn làm được

- [ ] Manage 10+ apps × 3 envs qua 1 ArgoCD ApplicationSet
- [ ] Build SLSA Level 3 pipeline với reusable workflow + provenance + cosign keyless
- [ ] Kyverno admission policy reject image không signed/provenance
- [ ] Deploy Vault + ESO; rotate Postgres credentials 1h tự động
- [ ] Pre-commit gitleaks + CI scan blockmọi secret leak
- [ ] Canary deploy với metric-driven auto-rollback (Prometheus)
- [ ] Feature flag với OpenFeature SDK + Unleash backend
- [ ] A/B test 2 variants với analytics validation

---

## 🔗 Liên kết

### Trong workspace
- ↑ [CI/CD README](../../README.md)
- ↶ [Basic cluster](../01_basic/) — 5 bài foundation
- 🐳 [Docker intermediate](../../../docker/lessons/02_intermediate/) — image production-grade
- ☸️ [Kubernetes intermediate](../../../kubernetes/lessons/02_intermediate/) — K8s production
- 📊 [Observability basic](../../../observability/) — Prometheus cho canary analysis
- 🏗️ [IaC basic](../../../iac/) — Terraform infra
- 🧭 [DevOps Engineer roadmap](../../../../00_Roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Platform Engineer roadmap](../../../../00_Roadmaps/career/platform-engineer_career-roadmap.md)
- 🧭 [SRE roadmap](../../../../00_Roadmaps/career/sre-engineer_career-roadmap.md)

### Tài nguyên ngoài 2026
- 📖 [ArgoCD docs](https://argo-cd.readthedocs.io/)
- 📖 [SLSA framework](https://slsa.dev/)
- 📖 [Sigstore docs](https://docs.sigstore.dev/)
- 📖 [Vault docs](https://www.vaultproject.io/docs)
- 📖 [External Secrets Operator](https://external-secrets.io/)
- 📖 [Argo Rollouts](https://argo-rollouts.readthedocs.io/)
- 📖 [OpenFeature](https://openfeature.dev/)
- 📖 [Unleash](https://docs.getunleash.io/)
- 📖 [12-Factor App](https://12factor.net/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Cluster intermediate thứ 3 của `10_DevOps/`. 5 bài hoàn thành: overview + ArgoCD + supply chain SLSA + secret Vault + progressive delivery. Apply 4 insight từ `__Ref__/` (GitOps anti-pattern, 12-factor violations, SLSA Level 3, progressive delivery patterns). Apply rule Blueprint v0.5.2 (no fictional character).
