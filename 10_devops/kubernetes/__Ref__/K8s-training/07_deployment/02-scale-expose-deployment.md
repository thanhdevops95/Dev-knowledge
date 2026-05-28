# Bài #21 — Scale & Expose Deployment (NodePort)

> 🎯 Cách scale Deployment + expose ra ngoài cluster.

---

## 📋 Metadata

- **Bài số:** #21
- **Module:** 07-deployment
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~6 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Scale Deployment lên/xuống bằng `kubectl scale`
- [ ] Expose Deployment thành NodePort Service
- [ ] Hiểu Service tự load-balance cho mọi Pod thuộc Deployment

---

## 📚 Nội Dung

### 1. Scale Deployment

**Cú pháp:**

```bash
kubectl scale deployment <name> --replicas=<n>
```

**Ví dụ:**

```bash
# Hiện tại 3 replicas
kubectl get deploy app1-deploy
# READY: 3/3

# Scale lên 10
kubectl scale deployment app1-deploy --replicas=10

# Scale xuống 5
kubectl scale deployment app1-deploy --replicas=5

# Scale xuống 0 (tạm dừng)
kubectl scale deployment app1-deploy --replicas=0
```

> 💡 Khác với edit YAML — `scale` là cách **nhanh** để thay đổi replicas. Nhưng **production** nên cập nhật vào file YAML rồi `apply`.

---

### 2. Expose Deployment thành Service

```bash
kubectl expose deployment <name> \
  --type=NodePort \
  --port=80 \
  --target-port=80 \
  --name=<service-name>
```

**Ví dụ:**

```bash
kubectl expose deployment app1-deploy \
  --type=NodePort \
  --port=80 \
  --target-port=80 \
  --name=app1-service

kubectl get svc
# NAME           TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
# app1-service   NodePort   10.96.1.50    <none>        80:31234/TCP   5s

minikube service app1-service --url
# http://192.168.49.2:31234
```

**Cơ chế dưới mui:**

```
                Service "app1-service" (Selector: app=app1)
                            │
        ┌───────────────────┼───────────────────────┐
        ▼                   ▼                       ▼
   Pod-A (v1)          Pod-B (v1)              Pod-C (v1)
   IP: 10.244.1.5      IP: 10.244.1.6          IP: 10.244.1.7
```

→ Service **load-balance round-robin** giữa 3 Pod.

---

### 3. Test Load-balancing

```bash
# Truy cập nhiều lần
URL=$(minikube service app1-service --url)
for i in {1..10}; do curl $URL; echo; done
```

→ Mỗi request có thể **rớt vào Pod khác nhau**.

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo deployment
kubectl create deployment app1-deploy \
  --image=nginx:1.24-alpine \
  --replicas=2

# 2. Expose
kubectl expose deployment app1-deploy \
  --type=NodePort \
  --port=80 \
  --name=app1-service

# 3. Test
minikube service app1-service --url
# Mở browser truy cập

# 4. Scale lên 5
kubectl scale deployment app1-deploy --replicas=5

# 5. Scale xuống 2
kubectl scale deployment app1-deploy --replicas=2

# 6. Cleanup
kubectl delete svc app1-service
kubectl delete deploy app1-deploy
```

---

## ⚠️ Lưu Ý

- ⚠️ `kubectl scale` **chỉ thay đổi tạm thời** — lần `apply` lại YAML sẽ bị reset
- ✅ Production: cập nhật `replicas` vào YAML rồi `apply`
- 💡 Dùng **HPA** (Horizontal Pod Autoscaler) để auto-scale theo CPU/RAM

---

## ✅ Self-Check

1. **Scale Deployment xuống 0 có ý nghĩa gì?**
   <details>
   <summary>Đáp án</summary>
   Tạm dừng app (giữ Deployment + Service nhưng không chạy Pod nào). Hữu ích khi debug, tiết kiệm tài nguyên.
   </details>

2. **Tại sao Service expose Deployment có thể load-balance?**
   <details>
   <summary>Đáp án</summary>
   Service dùng **selector match labels** → tất cả Pod thuộc Deployment đều được Service phát hiện và load-balance.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #20 — Create Deployment](01-create-deployment.md)
- ➡️ [Bài #22 — Set Container Image](03-set-image.md)

### Tài Nguyên

- 📺 Video gốc: `Decopy_✅ #21 Scale & Expose Deployment..._captions.txt`

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
