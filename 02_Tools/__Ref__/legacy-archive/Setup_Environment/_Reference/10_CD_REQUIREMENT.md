# Module 10: CONTINUOUS DEPLOYMENT (CD)

> **"CD là hệ thống giao hàng tự động - code merge xong, production có ngay"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu CD vs Continuous Delivery
- ✅ GitOps principles
- ✅ ArgoCD setup và usage
- ✅ Deployment strategies (Rolling, Blue-Green, Canary)
- ✅ Feature flags
- ✅ Rollback strategies
- ✅ Progressive delivery

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| CD | Continuous Deployment/Delivery | Triển khai liên tục |
| GitOps | GitOps | Git là nguồn sự thật |
| ArgoCD | ArgoCD | GitOps tool cho K8s |
| Flux | FluxCD | GitOps tool khác |
| Rolling Update | Rolling Update | Update từng pod một |
| Blue-Green | Blue-Green Deployment | Switch traffic giữa 2 envs |
| Canary | Canary Deployment | Release cho % nhỏ users |
| A/B Testing | A/B Testing | Test 2 versions |
| Feature Flag | Feature Flag | Toggle tính năng on/off |
| Rollback | Rollback | Quay về version cũ |
| Promotion | Environment Promotion | Đẩy từ staging → production |
| Sync | Sync | Đồng bộ desired state |
| Drift | Configuration Drift | Sự khác biệt actual vs desired |
| Health Check | Health Check | Kiểm tra app health |
| Progressive Delivery | Progressive Delivery | Release từ từ, có kiểm soát |

---

## ✅ Checklist Labs

### Labs GitOps Concepts

- [ ] Lab 1: GitOps workflow overview
- [ ] Lab 2: Push vs Pull model
- [ ] Lab 3: Single source of truth
- [ ] Lab 4: Declarative configuration
- [ ] Lab 5: Git repository structure cho GitOps

### Labs ArgoCD Setup

- [ ] Lab 6: Install ArgoCD on K8s
- [ ] Lab 7: ArgoCD CLI setup
- [ ] Lab 8: ArgoCD UI access
- [ ] Lab 9: ArgoCD architecture
- [ ] Lab 10: ArgoCD projects

### Labs ArgoCD Applications

- [ ] Lab 11: Create Application từ UI
- [ ] Lab 12: Create Application từ CLI
- [ ] Lab 13: Create Application từ YAML
- [ ] Lab 14: Application sync policies
- [ ] Lab 15: Auto-sync và self-heal
- [ ] Lab 16: Sync options (prune, apply-out-of-order)
- [ ] Lab 17: Application health status
- [ ] Lab 18: Sync hooks (PreSync, PostSync)

### Labs ArgoCD với Helm

- [ ] Lab 19: Deploy Helm chart với ArgoCD
- [ ] Lab 20: Helm values file
- [ ] Lab 21: Multiple values files
- [ ] Lab 22: Helm hooks trong ArgoCD

### Labs ArgoCD với Kustomize

- [ ] Lab 23: Kustomize basics
- [ ] Lab 24: Deploy Kustomize với ArgoCD
- [ ] Lab 25: Overlays cho environments

### Labs Deployment Strategies

- [ ] Lab 26: Rolling update trong K8s
- [ ] Lab 27: Blue-Green với K8s Services
- [ ] Lab 28: Blue-Green với ArgoCD Rollouts
- [ ] Lab 29: Canary với ArgoCD Rollouts
- [ ] Lab 30: Canary analysis
- [ ] Lab 31: Automated rollback

### Labs Argo Rollouts

- [ ] Lab 32: Install Argo Rollouts
- [ ] Lab 33: Create Rollout resource
- [ ] Lab 34: Rollout với Canary strategy
- [ ] Lab 35: Rollout với Blue-Green strategy
- [ ] Lab 36: Rollout với traffic management
- [ ] Lab 37: Analysis templates
- [ ] Lab 38: AnalysisRun

### Labs Feature Flags

- [ ] Lab 39: Feature flag concepts
- [ ] Lab 40: LaunchDarkly/Unleash basics
- [ ] Lab 41: Feature flags trong code
- [ ] Lab 42: Feature flags với Argo Rollouts

### Labs Multi-Environment

- [ ] Lab 43: Repository structure cho multi-env
- [ ] Lab 44: ApplicationSet
- [ ] Lab 45: Environment promotion workflow
- [ ] Lab 46: ArgoCD notifications

### Labs Counter App CD

- [ ] Lab 47: Setup GitOps repo cho Counter App
- [ ] Lab 48: Deploy Counter App với ArgoCD
- [ ] Lab 49: Automated image updates
- [ ] Lab 50: Canary release Counter App

### Labs Security

- [ ] Lab 51: RBAC trong ArgoCD
- [ ] Lab 52: SSO integration
- [ ] Lab 53: Sealed Secrets
- [ ] Lab 54: External Secrets Operator

---

## 🚨 Checklist Scenarios

### Scenarios về Sync

- [ ] Scenario 1: Application out of sync
- [ ] Scenario 2: Sync failed
- [ ] Scenario 3: Self-heal không work
- [ ] Scenario 4: Prune delete nhầm resources

### Scenarios về Deployments

- [ ] Scenario 5: Rolling update stuck
- [ ] Scenario 6: Blue-green cutover failed
- [ ] Scenario 7: Canary analysis failed
- [ ] Scenario 8: Rollback không complete

### Scenarios về GitOps

- [ ] Scenario 9: Git repo không accessible
- [ ] Scenario 10: Branch protection blocking sync
- [ ] Scenario 11: Configuration drift detected
- [ ] Scenario 12: Conflicting changes

### Scenarios về ArgoCD

- [ ] Scenario 13: ArgoCD UI không accessible
- [ ] Scenario 14: Application health degraded
- [ ] Scenario 15: Sync waves order incorrect
- [ ] Scenario 16: Hooks failed

### Scenarios về Multi-Environment

- [ ] Scenario 17: Wrong environment deployed
- [ ] Scenario 18: Promotion pipeline broken
- [ ] Scenario 19: Environment config mismatch
- [ ] Scenario 20: Secret không sync across envs

### Scenarios về Production

- [ ] Scenario 21: Production deployment failed
- [ ] Scenario 22: Cần emergency rollback
- [ ] Scenario 23: Feature flag stuck
- [ ] Scenario 24: Canary causing issues
- [ ] Scenario 25: Auto-sync during incident

---

## ⏱️ Thời lượng

**Ước tính:** 6-8 giờ

| Phần | Thời gian |
|------|-----------|
| GitOps concepts (Labs 1-5) | 0.5 giờ |
| ArgoCD setup & apps (Labs 6-18) | 2 giờ |
| Helm & Kustomize (Labs 19-25) | 1 giờ |
| Deployment strategies (Labs 26-38) | 2 giờ |
| Feature flags & Multi-env (Labs 39-46) | 1 giờ |
| Counter App + Security | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [GitOps Principles](https://www.gitops.tech/)
- [Flagger](https://flagger.app/) (Alternative)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
