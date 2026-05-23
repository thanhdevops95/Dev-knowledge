# 🔬 Labs: GitOps Platform

> **Hands-on Labs for GitOps with ArgoCD and Flux**
>
> *Bài thực hành GitOps với ArgoCD và Flux.*

---

## 🔬 Lab 1: ArgoCD Installation

### Objective

Install ArgoCD on Kubernetes cluster.

*(Cài đặt ArgoCD trên Kubernetes cluster.)*

### Steps

```bash
# Create namespace (Tạo namespace)
kubectl create namespace argocd

# Install ArgoCD (Cài đặt ArgoCD)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods (Đợi pods khởi động)
kubectl wait --for=condition=Ready pods --all -n argocd --timeout=300s

# Get admin password (Lấy mật khẩu admin)
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Port forward (Port forward)
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

---

## 🔬 Lab 2: First ArgoCD Application

```yaml
# application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

```bash
kubectl apply -f application.yaml
kubectl get applications -n argocd
```

---

## 🔬 Lab 3: Helm Chart Deployment

```yaml
# helm-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: nginx
    targetRevision: 15.0.0
    helm:
      values: |
        replicaCount: 2
        service:
          type: ClusterIP
  destination:
    server: https://kubernetes.default.svc
    namespace: nginx
  syncPolicy:
    automated:
      prune: true
```

---

## 🔬 Lab 4: Flux Installation

```bash
# Install Flux CLI (Cài đặt Flux CLI)
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux (Bootstrap Flux)
flux bootstrap github \
  --owner=<your-username> \
  --repository=<your-repo> \
  --path=clusters/my-cluster \
  --personal

# Check status (Kiểm tra trạng thái)
flux check
kubectl get pods -n flux-system
```

---

## 🔬 Lab 5: Kustomize with Flux

```yaml
# kustomization.yaml (Flux)
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: app
  namespace: flux-system
spec:
  interval: 5m
  path: ./apps
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
```

---

## ✅ Checklist

- [ ] Lab 1: ArgoCD Installation
- [ ] Lab 2: First Application
- [ ] Lab 3: Helm Chart
- [ ] Lab 4: Flux Installation
- [ ] Lab 5: Kustomize

---

## ✅ General Verification (Kiểm chứng tổng quát)

```bash
# Check ArgoCD (Kiểm tra ArgoCD)
kubectl get pods -n argocd
argocd app list

# Check Flux (Kiểm tra Flux)
flux check
flux get all

# Check deployed apps (Kiểm tra apps đã deploy)
kubectl get applications -n argocd
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `ArgoCD: OutOfSync` | Check source repo, sync manually *(Kiểm tra repo, sync thủ công)* |
| `Flux: reconciliation failed` | Check source, run `flux reconcile` *(Kiểm tra source)* |
| `Application not syncing` | Check RBAC, repo access *(Kiểm tra RBAC)* |
| `Helm values not applied` | Check values format, indentation *(Kiểm tra format values)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Delete ArgoCD applications (Xóa applications ArgoCD)
argocd app delete guestbook nginx --cascade

# Uninstall ArgoCD (Gỡ cài đặt ArgoCD)
kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl delete namespace argocd

# Uninstall Flux (Gỡ cài đặt Flux)
flux uninstall
```

---

**[← Back to README](./README.md)**
