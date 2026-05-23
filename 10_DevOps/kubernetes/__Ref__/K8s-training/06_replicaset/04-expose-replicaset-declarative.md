# Bài #18 — Expose ReplicaSet Bằng Declarative (NodePort YAML)

> 🎯 Tạo NodePort Service bằng YAML — kiểm soát được **fixed nodePort** thay vì random.

---

## 📋 Metadata

- **Bài số:** #18
- **Module:** 06-replicaset
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~3 phút
- **Prerequisites:** [Bài #17 — Expose RS Imperative](03-expose-replicaset-imperative.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Viết được **NodePort Service manifest** đầy đủ
- [ ] Chỉ định **cố định** `nodePort` (vd: `31988`)
- [ ] Hiểu sự khác nhau `port` / `targetPort` / `nodePort` qua YAML
- [ ] Apply Service và verify

---

## 📚 Nội Dung

### 1. Cấu Trúc NodePort Service Manifest

```yaml
apiVersion: v1                  # ← Service là v1 (NOT apps/v1!)
kind: Service
metadata:
  name: service-3-declarative
spec:
  type: NodePort                # ← Bắt buộc nếu muốn NodePort
  selector:                     # ← Match Pod backend
    app: app3
  ports:
    - port: 8080                # ← Service port (cluster-internal)
      targetPort: 80            # ← Container port bên trong Pod
      nodePort: 31988           # ← Port public (CỐ ĐỊNH, 30000-32767)
```

### 2. So Sánh 3 Cấp Port Trong YAML

```
            Service (NodePort)
            ├─ port: 8080        ← Pod khác trong cluster gọi qua port này
            ├─ targetPort: 80    ← Forward đến container :80
            └─ nodePort: 31988   ← User ngoài gọi vào http://<node-ip>:31988
```

> 💡 **Lưu ý:** Trên Imperative, `--port=80` = `port`. Còn `nodePort` không thể chỉ định bằng Imperative.

---

## 💻 Hands-On / Demo

### Bước 1: Tạo File `nodeport-svc.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-3-declarative
spec:
  type: NodePort
  selector:
    app: app3
  ports:
    - port: 8080
      targetPort: 80
      nodePort: 31988
```

### Bước 2: Apply

```bash
# Đảm bảo RS rs3 đang chạy (3 Pod label app=app3)
kubectl get pods -l app=app3
# rs3-abc12   1/1   Running
# rs3-def34   1/1   Running
# rs3-ghi56   1/1   Running

# Apply Service
kubectl apply -f nodeport-svc.yaml
# service/service-3-declarative created
```

### Bước 3: Verify

```bash
kubectl get svc service-3-declarative
# NAME                       TYPE        CLUSTER-IP    PORT(S)          AGE
# service-3-declarative      NodePort    10.97.x.y     8080:31988/TCP   5s
#                                                            │
#                                                            └─ Đúng nodePort!
```

### Bước 4: Test

```bash
# Trên Minikube
minikube service service-3-declarative --url
# Thấy URL với port 31988

curl http://<node-ip>:31988
# Nhận response từ 1 trong 3 Pod
```

### Bước 5: Lỗi Thường Gặp

#### ❌ Lỗi: `nodePort out of range`

```yaml
ports:
  - port: 80
    nodePort: 3000     # ❌ < 30000
```

```bash
kubectl apply -f bad.yaml
# error: provided port is not in the valid range. The range of valid ports is 30000-32767
```

#### ❌ Lỗi: `nodePort already in use`

Nếu nodePort đã được Service khác dùng → lỗi conflict. Phải đổi port khác.

### Cleanup

```bash
kubectl delete -f nodeport-svc.yaml
```

---

## ⚠️ Lưu Ý

- 🔥 `apiVersion: v1` cho Service (KHÔNG `apps/v1`)
- 🔥 `nodePort` PHẢI trong **30000-32767**
- 🔥 `nodePort` không thể trùng giữa các Service
- ✅ Production: **không cố định nodePort** trừ khi thật sự cần (vì ít khi user gõ NodePort trực tiếp)
- ✅ Trong Imperative, không thể chỉ định `nodePort` — bắt buộc YAML

---

## ✅ Self-Check

1. **`apiVersion` của Service là gì?**
   <details>
   <summary>Đáp án</summary>
   `v1` (không phải `apps/v1`)
   </details>

2. **3 trường port trong NodePort Service?**
   <details>
   <summary>Đáp án</summary>
   - `port` — Service port (internal)
   - `targetPort` — Container port
   - `nodePort` — Public port trên Node
   </details>

3. **Range hợp lệ của `nodePort`?**
   <details>
   <summary>Đáp án</summary>
   **30000-32767**
   </details>

4. **Lệnh nào tạo Service từ YAML?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl apply -f service.yaml
   ```

   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #17 — Expose RS Imperative](03-expose-replicaset-imperative.md)
- ➡️ [Bài #19 — Edit RS & Giới thiệu Deployment](05-edit-replicaset-va-deployment.md)

### Tài Nguyên

- 📖 [Service NodePort](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)
- 📺 Video gốc: `Decopy_✅ #18 _ Expose NodePort ReplicaSet Declarative..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Khi dùng Imperative, nodePort sinh ra ngẫu nhiên. Khi dùng Declarative, các bạn có thể CHỌN bất kỳ port nào (trong range)."*

> 💬 *"Đây là cái bạn sau này sẽ làm nhiều hơn so với gõ những dòng lệnh Imperative."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
