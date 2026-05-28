# GIAI ĐOẠN 13: GITOPS VỚI ARGOCD - VẬN HÀNH HIỆN ĐẠI

## 📌 MỤC TIÊU GIAI ĐOẠN 13
Truyền thống (Giai đoạn 8): GitLab Runner SSH vào server -> Gõ lệnh `docker compose up`.
Hiện đại (GitOps): **ArgoCD** nằm trong Cluster, canh chừng Git.
- Git thay đổi -> ArgoCD tự động đồng bộ (Sync) trạng thái Cluster cho khớp với Git.
- Không cần lộ SSH Key. Không cần mở port SSH. Git là "Single Source of Truth".

---

## 🚢 PHẦN 1: TRUY CẬP ARGOCD UI

### 1. Port Forward
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### 2. Lấy Password
User mặc định: `admin`.
Password lấy bằng lệnh:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### 3. Đăng nhập
Mở `https://localhost:8080` (chấp nhận cảnh báo SSL). Đăng nhập.

---

## 🔗 PHẦN 2: KẾT NỐI GIT REPO

### 1. Chuẩn bị Manifests trên Git
Tạo thư mục `k8s/` trên GitLab repo của bạn (đã làm ở Giai đoạn 9). Đảm bảo folder này chứa các file deployment.yaml hoàn chỉnh.

### 2. Tạo App trên ArgoCD
- Vào UI -> **New App**.
- **Application Name**: `todo-app`
- **Project Name**: `default`
- **Sync Policy**: `Automatic` (Tự động sync khi git đổi), tích thêm `Prune Resources` (Xóa trong K8s nếu xóa trên Git) và `Self Heal` (Ai sửa tay K8s sẽ bị ArgoCD sửa lại cho đúng Git).
- **Source**:
  - Repo URL: `https://gitlab.com/USERNAME/todo-devsecops.git`
  - Path: `k8s`
- **Destination**:
  - Cluster URL: `https://kubernetes.default.svc`
  - Namespace: `default`
  
- Bấm **CREATE**.

---

## 🔮 PHẦN 3: MA THUẬT GITOPS

Ngay sau khi Create, ArgoCD sẽ quét Git và báo trạng thái **Synced** (Xanh lá).
Các Pods sẽ được tạo ra trên Cluster.

### Thử nghiệm GitOps Flow:
1. Sửa file `k8s/backend.yaml` trên GitLab (trực tiếp trên Web IDE).
   - Tăng `replicas: 2` lên `replicas: 5`.
   - Commit changes.
   
2. Qua tab ArgoCD:
   - Bạn sẽ thấy ArgoCD phát hiện "Out of Sync" (hoặc tự động Sync ngay lập tức).
   - Biểu đồ sẽ đẻ thêm 3 pod backend nữa.
   - Bạn KHÔNG HỀ gõ lệnh `kubectl apply`.

### Thử nghiệm Self-Healing:
1. Xóa trộm 1 service: `kubectl delete svc backend`.
2. ArgoCD phát hiện ngay lập tức: "Ê, trên Git bảo có Service mà thực tế không có!".
3. ArgoCD tự động tạo lại Service đó ngay lập tức.

---

## 🎊 TỔNG KẾT KHÓA HỌC
Chúc mừng bạn đã hoàn thành hành trình **DevSecOps Zero to Hero**! 🏆

Bạn đã đi từ:
- Code tay Ping-Pong
- Docker hóa
- Orchestrate với Compose
- Triển khai K8s
- Scale trên Cloud
- Giám sát 24/7
- Và vận hành tự động bằng GitOps

Đây là nền tảng vững chắc để bạn ứng tuyển vào vị trí DevOps/SRE Engineer. Hãy tiếp tục thực hành!
