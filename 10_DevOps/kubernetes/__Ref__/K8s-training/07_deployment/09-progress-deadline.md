# Bài #28 — Progress Deadline Seconds

> 🎯 Đặt **timeout** cho rollout — fail nhanh khi deploy bị lỗi.

---

## 📋 Metadata

- **Bài số:** #28
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~6 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu vấn đề: deployment lỗi nhưng không có timeout
- [ ] Cấu hình `progressDeadlineSeconds`
- [ ] Phát hiện rollout fail qua `kubectl rollout status`

---

## 📚 Nội Dung

### 1. Vấn Đề: Rollout Có Thể Bị "Treo"

Có nhiều lý do rollout không thành công:

- ❌ **ImagePullBackOff** — image không tồn tại
- ❌ **CrashLoopBackOff** — container crash liên tục
- ❌ **Insufficient resources** — cluster hết CPU/RAM
- ❌ **Permission denied** — không có quyền pull image (private registry)

→ Cần một **deadline** để rollout fail rõ ràng.

---

### 2. `progressDeadlineSeconds`

**Mặc định:** `600` giây (10 phút).

```yaml
spec:
  progressDeadlineSeconds: 200   # 200 giây
  replicas: 10
  template:
    # ...
```

**Ý nghĩa:** nếu sau N giây mà rollout không tiến triển → đánh dấu **failed**.

---

### 3. Demo: Tạo Rollout Fail Có Chủ Đích

```bash
# Setup deployment OK
kubectl create deployment app1-deploy \
  --image=hieuvu/simple-app:v1 --replicas=10

# Cấu hình deadline = 200 giây
kubectl patch deployment app1-deploy \
  -p '{"spec":{"progressDeadlineSeconds":200}}'

# Update với image KHÔNG TỒN TẠI
kubectl set image deployment/app1-deploy \
  simple-app=hieuvu/simple-app:v999

# Theo dõi rollout (sẽ block đến khi fail)
kubectl rollout status deployment/app1-deploy
# Waiting for deployment "app1-deploy" rollout to finish: 2 of 10 updated replicas...
# (chờ ~200 giây)
# error: deployment "app1-deploy" exceeded its progress deadline

# Kiểm tra
kubectl describe deployment app1-deploy | grep -A 5 Conditions:
# Type           Status  Reason
# Progressing    False   ProgressDeadlineExceeded   ← FAIL!
# Available      True    MinimumReplicasAvailable
```

> 💡 Deployment **vẫn giữ** Pod cũ chạy → app **không bị down-time**!

---

### 4. Tại Sao Quan Trọng Trong CI/CD?

```bash
# Trong CI pipeline
kubectl set image deployment/app simple-app=app:v2
kubectl rollout status deployment/app --timeout=300s

if [ $? -ne 0 ]; then
  echo "Deploy failed, rolling back..."
  kubectl rollout undo deployment/app
  exit 1
fi
```

→ CI có thể tự **rollback** nếu rollout fail.

---

### 5. Phát Hiện Lỗi Cụ Thể

```bash
# Pod bị lỗi gì?
kubectl get pods | grep -v Running
# app1-deploy-xyz-aaa   0/1   ImagePullBackOff   0   1m

# Chi tiết
kubectl describe pod app1-deploy-xyz-aaa
# Events:
#   Warning  Failed   Failed to pull image "hieuvu/simple-app:v999":
#                    rpc error: not found
```

---

## 💻 Hands-On / Demo

```bash
# Cấu hình qua YAML
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-demo
spec:
  replicas: 3
  progressDeadlineSeconds: 60
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      containers:
        - name: demo
          image: nginx:1.24-alpine
EOF

# Update image lỗi
kubectl set image deployment/app-demo demo=nginx:NOT-EXIST

# Sau 60 giây → fail
kubectl rollout status deployment/app-demo

# Cleanup
kubectl delete deployment app-demo
```

---

## ⚠️ Lưu Ý

- 🔥 Default = **600 giây** — quá dài cho CI/CD nhanh
- 💡 **Recommend:** 120-300 giây cho microservices
- ⚠️ Quá ngắn → false-positive (image lớn pull lâu)
- ✅ Khi rollout fail, Pod cũ **vẫn chạy** → app vẫn available

---

## ✅ Self-Check

1. **`progressDeadlineSeconds` mặc định bao nhiêu?**
   <details>
   <summary>Đáp án</summary>
   `600` giây (10 phút).
   </details>

2. **Rollout fail có làm app down không?**
   <details>
   <summary>Đáp án</summary>
   **Không**. Pod cũ vẫn chạy, chỉ Pod mới không deploy được.
   </details>

3. **Cách kiểm tra lý do rollout fail?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl describe deployment <name>          # Xem Conditions
   kubectl describe pod <pod-name>              # Xem Events
   kubectl get events --sort-by='.lastTimestamp'
   ```

   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #27 — Deployment Strategies](08-deployment-strategies.md)
- ➡️ [Bài #29 — Restart Deployment](10-restart-deployment.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
