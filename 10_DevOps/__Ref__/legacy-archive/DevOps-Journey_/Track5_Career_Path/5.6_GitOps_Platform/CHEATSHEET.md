# 📋 Cheatsheet: GitOps Platform

> **Quick Reference for GitOps Tools**
>
> *Tham khảo nhanh công cụ GitOps.*

---

## 🔧 ArgoCD CLI

| Command | Description |
|---------|-------------|
| `argocd login <server>` | Login to ArgoCD *(Đăng nhập ArgoCD)* |
| `argocd app list` | List applications *(Liệt kê applications)* |
| `argocd app sync <app>` | Sync application *(Sync application)* |
| `argocd app get <app>` | Get app details *(Xem chi tiết app)* |
| `argocd app delete <app>` | Delete application *(Xóa application)* |
| `argocd app diff <app>` | Show diff *(Hiển thị diff)* |
| `argocd repo add <url>` | Add repository *(Thêm repository)* |

---

## 🔧 Flux CLI

| Command | Description |
|---------|-------------|
| `flux check` | Check prerequisites *(Kiểm tra điều kiện)* |
| `flux bootstrap github` | Bootstrap Flux *(Khởi tạo Flux)* |
| `flux get all` | List all resources *(Liệt kê resources)* |
| `flux reconcile source git` | Force reconcile *(Force reconcile)* |
| `flux suspend kustomization` | Suspend sync *(Tạm dừng sync)* |
| `flux resume kustomization` | Resume sync *(Tiếp tục sync)* |
| `flux uninstall` | Remove Flux *(Gỡ Flux)* |

---

## 📝 ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/repo.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

---

## 📝 Flux Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  interval: 10m
  path: ./apps
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
```

---

## 🔗 Sync Policies

| Policy | ArgoCD | Flux |
|--------|--------|------|
| Auto sync | `automated: {}` | `interval: 5m` |
| Prune | `prune: true` | `prune: true` |
| Self heal | `selfHeal: true` | N/A |
| Force | `force: true` | `force: true` |

---

**[← Back to README](./README.md)**
