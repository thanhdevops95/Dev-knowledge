# Bài 45 — Cài ArgoCD & Application đầu tiên

## Phần A — Cài đặt

```bash
# 1. Tạo namespace argocd và cài
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 2. Đợi pod ready (mất 1-3 phút)
kubectl get pods -n argocd -w
# Ctrl+C khi tất cả Running

# 3. Cài ArgoCD CLI
# macOS:
brew install argocd
# Linux:
# curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
# sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd

# 4. Lấy password admin
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
echo

# 5. Mở UI
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Truy cập https://localhost:8080 (chấp nhận certificate self-signed)
# Username: admin  Password: ở bước 4

# 6. Login CLI
argocd login localhost:8080 --username admin --password <password> --insecure
```

## Phần B — Tạo Git repo

Tạo repo trên GitHub: `myapp-gitops` với cấu trúc:
```
myapp-gitops/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── environments/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

Push các manifest từ K8s bài 29-33 vào `base/`.

## Phần C — Tạo Application

```bash
# Sửa argocd-app.yaml: đổi repoURL sang repo của bạn
kubectl apply -f argocd-app.yaml

# Quan sát trên UI - app sync tự động
```

## Câu hỏi

- `prune: true` ? *(xóa resource khỏi cluster khi xóa khỏi Git)*
- `selfHeal: true` ? *(nếu ai đó `kubectl edit` lệch khỏi Git, ArgoCD revert lại)*

## Bài kế tiếp

```bash
cp -r ../45-argocd-setup ../46-gitops-workflow
cd ../46-gitops-workflow
```
