# 🐳 Docker — Intermediate cluster

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Status:** ✅ Intermediate cluster hoàn thành (5/5 bài)

> 🎯 *Từ "chạy được" → "production-grade". Cluster intermediate đầu tiên của `10_devops/`. Build trên Docker basic (4 bài) — đi sâu BuildKit advanced + Image security supply chain + Optimization & distroless + Registry production. Output: deploy Docker stack tier-1 sẵn sàng SOC2/compliance.*

---

## 🚀 Quick start

- **Bạn xong basic 4 bài?** → vào [00_intermediate-overview](00_intermediate-overview.md) để map lộ trình.
- **Build chậm/cache kém?** → [01_buildkit-and-multistage-advanced](01_buildkit-and-multistage-advanced.md).
- **Image có CVE, chưa scan, chưa sign?** → [02_image-security-supply-chain](02_image-security-supply-chain.md).
- **Image 1GB+ muốn giảm?** → [03_optimization-and-distroless](03_optimization-and-distroless.md).
- **Setup private registry production?** → [04_registry-production-patterns](04_registry-production-patterns.md).

---

## 📂 Cấu trúc cluster

```
02_intermediate/
├── README.md                          ← (file này)
├── 00_intermediate-overview.md         ← Intro, không hands-on
├── 01_buildkit-and-multistage-advanced.md
├── 02_image-security-supply-chain.md
├── 03_optimization-and-distroless.md
└── 04_registry-production-patterns.md
```

---

## 📖 Lessons — Intermediate cluster (5 bài)

| # | Bài | Trọng tâm | Tag |
|---|---|---|---|
| 00 | [Intermediate overview](00_intermediate-overview.md) | 4 mảng intermediate + tool stack 2026 + roadmap | MUST-KNOW |
| 01 | [BuildKit & Multi-stage advanced](01_buildkit-and-multistage-advanced.md) | Cache/secret mount + buildx multi-platform + bake monorepo + CI cache strategies | MUST-KNOW |
| 02 | [Image Security & Supply chain](02_image-security-supply-chain.md) | Trivy + SBOM (Syft) + cosign keyless signing + Kyverno admission + SLSA | MUST-KNOW |
| 03 | [Optimization & Distroless](03_optimization-and-distroless.md) | dive analyze + alpine/slim/distroless/scratch + layer order + 1.2GB→85MB | MUST-KNOW |
| 04 | [Registry & Production patterns](04_registry-production-patterns.md) | Harbor + ECR + pull-through cache + immutable tag + GC + replication + IRSA | MUST-KNOW |

→ Sau cluster: Docker production-grade tier-1 (dự kiến 4-6h hands-on).

---

## 🎯 Sau cluster bạn làm được

- [ ] Build image multi-platform (amd64+arm64) trong < 1 phút (cache mount + buildx)
- [ ] Pipeline build → Trivy scan → cosign sign → push registry full automated
- [ ] Image production < 100 MB (distroless) + 0 CRITICAL CVE
- [ ] Setup Harbor self-host hoặc dùng ECR production-grade
- [ ] Pull-through cache cho Docker Hub upstream → tránh rate limit + DR
- [ ] K8s deploy với image digest immutable + signature verify (Kyverno)
- [ ] Triển khai cross-region/cross-cloud replication
- [ ] Token rotation tự động (External Secrets / IRSA)

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ↑ **Về cụm:** [Docker README](../../README.md)
- ⬅️ **Bài trước:** [Basic cluster](../01_basic/) — 4 bài foundation
- ☸️ [Kubernetes basic](../../../kubernetes/) — apply image vào K8s
- 🔁 [CI/CD basic](../../../ci-cd/) — pipeline integration
- 📊 [Observability basic](../../../observability/) — monitor container
- 🏗️ [IaC basic](../../../iac/) — provision registry infra
- 🧭 [DevOps Engineer roadmap](../../../../00_roadmaps/career/devops-engineer_career-roadmap.md)
- 🧭 [Platform Engineer roadmap](../../../../00_roadmaps/career/platform-engineer_career-roadmap.md)

### Tài nguyên ngoài 2026
- 📖 [BuildKit docs](https://docs.docker.com/build/buildkit/)
- 📖 [Trivy](https://aquasecurity.github.io/trivy/) — vulnerability scanner
- 📖 [Sigstore](https://docs.sigstore.dev/) — keyless signing
- 📖 [SLSA framework](https://slsa.dev/)
- 📖 [Distroless](https://github.com/GoogleContainerTools/distroless)
- 📖 [Chainguard Images](https://www.chainguard.dev/chainguard-images)
- 📖 [Harbor](https://goharbor.io/) — CNCF registry
- 📖 [dive](https://github.com/wagoodman/dive) — layer inspector

---

## 📌 Nhật ký thay đổi (Changelog)
- **v1.0.0 (24/05/2026)** — Cluster intermediate đầu tiên. 5 bài hoàn thành: overview + BuildKit + security + optimization + registry. Cherry-pick từ `__Ref__/legacy-archive/04_Advanced/` + insights từ DevOps audit. Apply rule mới Blueprint v0.5.2 (no fictional character, brand `Acme Shop` thống nhất).
