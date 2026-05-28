# 🛠️ GIAI ĐOẠN 13: CHUẨN BỊ ARGOCD

## 📌 MỤC TIÊU
Cài đặt ArgoCD vào cụm Kubernetes.

---

## 1. CÀI ĐẶT ARGOCD
```bash
# Tạo namespace
kubectl create namespace argocd

# Apply manifest chính chủ từ ArgoCD Project
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## 2. CÀI ĐẶT ARGOCD CLI (OPTIONAL)
Để quản lý bằng dòng lệnh (mặc dù dùng Web UI là đủ).
- **macOS**: `brew install argocd`
- **Windows**: [Tải binary](https://github.com/argoproj/argo-cd/releases/latest).

## ✅ CHECKLIST
```bash
kubectl get pods -n argocd
# Đợi tất cả status là Running
```
Sẵn sàng cho mô hình vận hành hiện đại nhất thế giới!
