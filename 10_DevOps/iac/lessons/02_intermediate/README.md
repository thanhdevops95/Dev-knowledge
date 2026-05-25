# 🏗️ IaC — Intermediate cluster

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Intermediate cluster hoàn thành (5/5 bài)

> 🎯 *Từ "terraform apply local" → "GitOps infra production". Cluster intermediate cuối của DevOps sprint. Build trên IaC basic. Apply 4+ insight từ `__Ref__/` (GitOps as enforcement gate, drift detection workflow, Sealed Secrets pattern, state migration). 🎉 **Bài 04 = DevOps intermediate sprint complete (25 lessons)**.*

---

## 🚀 Quick start

- **Đã xong basic?** → [00_intermediate-overview](00_intermediate-overview.md).
- **15 file VPC sửa CIDR đau đầu?** → [01_terragrunt-dry-multi-env](01_terragrunt-dry-multi-env.md).
- **3 dev concurrent apply state conflict?** → [02_atlantis-gitops-for-iac](02_atlantis-gitops-for-iac.md).
- **`plan` show 200 destroy resources?** → [03_state-advanced-and-drift](03_state-advanced-and-drift.md).
- **HCL frustrate dev team?** → [04_pulumi-cdk-crossplane](04_pulumi-cdk-crossplane.md).

---

## 📂 Cấu trúc cluster

```
02_intermediate/
├── README.md                              ← (file này)
├── 00_intermediate-overview.md             ← Intro, không hands-on
├── 01_terragrunt-dry-multi-env.md
├── 02_atlantis-gitops-for-iac.md
├── 03_state-advanced-and-drift.md
└── 04_pulumi-cdk-crossplane.md
```

---

## 📖 Lessons — Intermediate cluster (5 bài)

| # | Bài | Trọng tâm | Tag | Thời lượng |
|---|---|---|---|---|
| 00 | [Intermediate overview](00_intermediate-overview.md) | Map 4 mảng + IaC at scale + tool stack 2026 | MUST-KNOW | ~13p |
| 01 | [Terragrunt DRY multi-env](01_terragrunt-dry-multi-env.md) | DRY pattern + `live/`+`modules/` + dependency + run-all + module versioning + multi-account | MUST-KNOW | ~22p |
| 02 | [Atlantis GitOps for IaC](02_atlantis-gitops-for-iac.md) | Architecture + Helm install + atlantis.yaml + RBAC + state lock + Terragrunt integration | MUST-KNOW | ~25p |
| 03 | [State advanced + Drift detection](03_state-advanced-and-drift.md) | State commands deep + import + moved block + driftctl + backup/recovery + state surgery | MUST-KNOW | ~22p |
| 04 | [Pulumi/CDK/Crossplane](04_pulumi-cdk-crossplane.md) | Pulumi real langs + AWS CDK + CDKTF + Crossplane CRDs + decision matrix + multi-cloud abstraction | MUST-KNOW | ~25p |

→ **Tổng ~107 phút đọc + 8-10h hands-on**. Sau cluster: IaC production-grade + know when to use each tool.

---

## 🎯 Sau cluster bạn làm được

- [ ] Refactor 75-folder repo → DRY Terragrunt structure
- [ ] Setup Atlantis PR-based workflow (no more local apply)
- [ ] `moved` block + `import` block for safe refactoring
- [ ] driftctl daily cron + alert + remediation workflow
- [ ] State backup + recovery procedure
- [ ] Write Pulumi (TypeScript/Python) for new project
- [ ] Setup Crossplane + Compositions for IDP
- [ ] Decision: when Terraform vs Pulumi vs CDK vs Crossplane

---

## 🔗 Liên kết

### Trong workspace
- ↑ [IaC README](../../README.md)
- ↶ [Basic cluster](../01_basic/) — 5 bài foundation
- 🐳 [Docker intermediate](../../../docker/lessons/02_intermediate/)
- ☸️ [Kubernetes intermediate](../../../kubernetes/lessons/02_intermediate/)
- 🔁 [CI/CD intermediate](../../../ci-cd/lessons/02_intermediate/)
- 📊 [Observability intermediate](../../../observability/lessons/02_intermediate/)
- 🧭 [DevOps Engineer roadmap](../../../../00_Roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Platform Engineer roadmap](../../../../00_Roadmaps/career/platform-engineer_career-roadmap.md)

### Tài nguyên ngoài 2026
- 📖 [Terragrunt docs](https://terragrunt.gruntwork.io/)
- 📖 [Atlantis docs](https://www.runatlantis.io/)
- 📖 [driftctl](https://github.com/snyk/driftctl)
- 📖 [Pulumi docs](https://www.pulumi.com/docs/)
- 📖 [AWS CDK docs](https://docs.aws.amazon.com/cdk/)
- 📖 [CDKTF docs](https://developer.hashicorp.com/terraform/cdktf)
- 📖 [Crossplane docs](https://docs.crossplane.io/)
- 📖 [OpenTofu](https://opentofu.org/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Cluster intermediate thứ 5 (cuối) của `10_DevOps/`. 5 bài hoàn thành: overview + Terragrunt + Atlantis + State advanced + Pulumi/CDK/Crossplane. Apply 4+ insight từ `__Ref__/` (GitOps Git as enforcement gate, drift detection workflow, state migration patterns, multi-cloud abstraction). 🎉 **DEVOPS INTERMEDIATE SPRINT 100% COMPLETE (5/5 clusters, 25 lessons)**.
