# 🎯 GIAI ĐOẠN 13: GITOPS VỚI ARGOCD - VẬN HÀNH HIỆN ĐẠI NHẤT

## 📌 MÔ TẢ
Thư mục này chứa code từ **TOÀN BỘ 13 GIAI ĐOẠN**.
- **Giai đoạn 13: ArgoCD** - Git là nguồn chân lý duy nhất!

Không cần SSH, không cần kubectl thủ công. Chỉ cần sửa file YAML trên Git → ArgoCD tự đồng bộ!

## 🚀 CÁCH CHẠY

### Bước 1: Cài ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Bước 2: Truy cập UI
```bash
# Lấy password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo

# Port forward
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Mở: https://localhost:8080
- User: `admin`
- Pass: (từ lệnh trên)

### Bước 3: Tạo App
1. Vào UI → New App
2. **Application Name:** `todo-app`
3. **Project:** `default`
4. **Sync Policy:** `Automatic` + `Prune` + `Self Heal`
5. **Source:**
   - Repo URL: `https://gitlab.com/YOUR_USER/todo-app`
   - Path: `k8s`
6. **Destination:**
   - Cluster URL: `https://kubernetes.default.svc`
   - Namespace: `default`
7. Create

## 🧪 TESTING

### Test 1: GitOps Flow
1. Sửa file `k8s/backend.yaml` trên GitLab
2. Tăng `replicas: 2` → `replicas: 5`
3. Commit & Push
4. Vào ArgoCD UI → Thấy "Out of Sync"
5. ArgoCD tự động Sync (nếu bật Auto)
6. Kiểm tra: `kubectl get pods` → Thấy 5 pods!

### Test 2: Self-Healing
1. Xóa trộm 1 service: `kubectl delete svc backend`
2. ArgoCD phát hiện ngay lập tức
3. ArgoCD tự tạo lại service

### Test 3: Rollback
1. Vào ArgoCD UI → History
2. Chọn version cũ
3. Bấm Rollback
4. Hệ thống quay về trạng thái cũ

## ✅ CHECKLIST

- [ ] Cài được ArgoCD
- [ ] Truy cập được UI
- [ ] Tạo được Application
- [ ] Test GitOps flow thành công
- [ ] Test self-healing
- [ ] Hiểu được GitOps philosophy

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **GitOps:** Git là Single Source of Truth
2. ✅ **Declarative:** Khai báo "muốn gì", không phải "làm thế nào"
3. ✅ **Self-Healing:** Tự sửa khi ai đó sửa tay
4. ✅ **Audit Trail:** Mọi thay đổi đều có Git history

## 🎊 HOÀN THÀNH KHÓA HỌC!

Chúc mừng! Bạn đã đi hết hành trình **DevSecOps Zero to Hero**! 🏆

**Bạn đã học:**
- ✅ Bare-metal → Docker → Compose
- ✅ NGINX → MySQL → CI/CD
- ✅ Kubernetes → AWS → Monitoring
- ✅ Security → GitOps

**Bước tiếp theo:**
1. Làm lại toàn bộ từ đầu (để nhớ lâu)
2. Áp dụng vào dự án thực tế
3. Viết blog chia sẻ kinh nghiệm
4. Ứng tuyển vị trí DevOps Engineer!

**Good luck! 🚀**
