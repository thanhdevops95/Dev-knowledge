# ☸️ Kubernetes — Intermediate cluster

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Intermediate cluster hoàn thành (5/5 bài)

> 🎯 *Từ "deploy được" → "production-grade cluster vận hành". Build trên K8s basic (5 bài). Cluster intermediate đầu tiên có operator pattern. Apply insights từ `__Ref__/` (CNI dependency, PDB-HPA conflict, Postgres operator). Output: K8s production tier-1.*

---

## 🚀 Quick start

- **Đã xong basic?** → [00_intermediate-overview](00_intermediate-overview.md).
- **5 service YAML copy-paste khổ?** → [01_helm-package-manager](01_helm-package-manager.md).
- **TLS manual + DNS manual?** → [02_ingress-cert-manager-tls](02_ingress-cert-manager-tls.md).
- **Postgres trong K8s mất data?** → [03_statefulset-and-storage](03_statefulset-and-storage.md).
- **Manual scale không kịp + setup DB 30 YAML?** → [04_autoscaling-and-operators](04_autoscaling-and-operators.md).

---

## 📂 Cấu trúc cluster

```
02_intermediate/
├── README.md                              ← (file này)
├── 00_intermediate-overview.md             ← Intro, không hands-on
├── 01_helm-package-manager.md
├── 02_ingress-cert-manager-tls.md
├── 03_statefulset-and-storage.md
└── 04_autoscaling-and-operators.md
```

---

## 📖 Lessons — Intermediate cluster (5 bài)

| # | Bài | Trọng tâm | Tag | Thời lượng |
|---|---|---|---|---|
| 00 | [Intermediate overview](00_intermediate-overview.md) | Map 4 mảng + tool stack 2026 + CNI dependency war story | MUST-KNOW | ~13p |
| 01 | [Helm](01_helm-package-manager.md) | Chart anatomy + Sprig template + values multi-env + hooks + sub-chart + Helm vs Kustomize | MUST-KNOW | ~25p |
| 02 | [Ingress + cert-manager + TLS](02_ingress-cert-manager-tls.md) | ingress-nginx prod + cert-manager Let's Encrypt + external-dns + Gateway API + NetworkPolicy + Cilium | MUST-KNOW | ~22p |
| 03 | [StatefulSet + Storage](03_statefulset-and-storage.md) | StatefulSet vs Deployment + PV/PVC/StorageClass + Postgres 3-replica + VolumeSnapshot + resize | MUST-KNOW | ~22p |
| 04 | [Autoscaling + Operators](04_autoscaling-and-operators.md) | HPA + VPA + KEDA + Karpenter + PDB war story + Operator pattern + write simple operator + CloudNativePG | MUST-KNOW | ~25p |

→ **Tổng ~107 phút đọc + 6-8h hands-on**. Sau cluster: K8s production-grade.

---

## 🎯 Sau cluster bạn làm được

- [ ] Viết Helm chart cho FastAPI từ đầu + deploy multi-env (dev/staging/prod)
- [ ] Setup ingress-nginx production với cert-manager auto Let's Encrypt + external-dns
- [ ] Enable Cilium CNI để NetworkPolicy thực sự enforce
- [ ] Deploy Postgres 3-replica với StatefulSet + backup VolumeSnapshot
- [ ] Setup HPA + KEDA scale theo CPU + queue + Cron
- [ ] Tránh PDB-HPA conflict (war story)
- [ ] Hiểu Operator pattern + viết simple operator với Kubebuilder
- [ ] Dùng CloudNativePG cho Postgres production-grade (HA, PITR, S3 backup)

---

## 🔗 Liên kết

### Trong workspace
- ↑ [Kubernetes README](../../README.md)
- ↶ [Basic cluster](../01_basic/) — 5 bài foundation
- 🐳 [Docker intermediate](../../../docker/lessons/02_intermediate/) — image production-grade
- 🔁 [CI/CD basic](../../../ci-cd/) — pipeline integration
- 📊 [Observability basic](../../../observability/) — Prometheus custom metric source
- 🏗️ [IaC basic](../../../iac/) — Terraform EKS provision
- 🧭 [DevOps Engineer roadmap](../../../../00_Roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Platform Engineer roadmap](../../../../00_Roadmaps/career/platform-engineer_career-roadmap.md)
- 🧭 [SRE roadmap](../../../../00_Roadmaps/career/sre-engineer_career-roadmap.md)

### Tài nguyên ngoài 2026
- 📖 [Helm docs](https://helm.sh/docs/)
- 📖 [ArgoCD docs](https://argo-cd.readthedocs.io/)
- 📖 [Cilium docs](https://docs.cilium.io/)
- 📖 [cert-manager docs](https://cert-manager.io/docs/)
- 📖 [KEDA docs](https://keda.sh/)
- 📖 [Karpenter docs](https://karpenter.sh/)
- 📖 [CloudNativePG docs](https://cloudnative-pg.io/documentation/)
- 📖 [Kubebuilder book](https://book.kubebuilder.io/)
- 📖 [Operator framework](https://operatorframework.io/)
- 📖 [OperatorHub](https://operatorhub.io/) — operator marketplace
- 📖 [CNCF landscape](https://landscape.cncf.io/) — full ecosystem

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Cluster intermediate đầu tiên của K8s. 5 bài hoàn thành: overview + Helm + Ingress prod + StatefulSet + Autoscaling/Operators. Apply 4 insight từ `__Ref__/`: CNI default Minikube không enforce NetworkPolicy, PDB-HPA war story, CloudNativePG operator, Cilium replace kube-proxy. Apply rule mới Blueprint v0.5.2 (no fictional character).
