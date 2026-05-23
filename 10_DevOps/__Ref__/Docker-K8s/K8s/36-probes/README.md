# Bài 36 — Liveness, Readiness & Startup Probes

**3 loại probe — phân biệt rõ:**

| Probe | Thất bại → K8s làm gì? | Khi nào dùng |
|-------|-----------------------|--------------|
| **Liveness** | **Restart container** | App treo/deadlock, cần đá ra để cứu |
| **Readiness** | **Tạm gỡ pod khỏi Service endpoints** (không restart) | App tạm thời busy/loading config, không nhận traffic |
| **Startup** | **Restart container** (như liveness, nhưng chỉ áp dụng ở giai đoạn khởi động) | App khởi động chậm (Java/JVM warmup, load model AI...) — tránh liveness kill pod trước khi app kịp ready |

> 💡 **Thứ tự kích hoạt:** `startupProbe` chạy trước. Khi nó **pass lần đầu**, K8s mới bắt đầu chạy `livenessProbe` và `readinessProbe`. Đây là cách an toàn để app khởi động chậm không bị kill oan.

## Lệnh thủ công

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp-deployment -n myapp-dev

# Xem cả 3 probe đã được set
kubectl describe deployment myapp-deployment -n myapp-dev | grep -A 3 -E "Startup|Liveness|Readiness"

# Quan sát events khi probe fail (bài tập): tạm thời đổi path probe sang /khong-ton-tai
# kubectl get pods -w -n myapp-dev   # sẽ thấy pod restart
```

## Kết quả mong đợi

- Pod `Ready 1/1` sau khi cả 3 probe pass.
- `kubectl describe pod` → thấy phần `Startup`, `Liveness`, `Readiness` đều có cấu hình.

## Câu hỏi

- Liveness fail → K8s **restart container** (`kubectl describe` thấy `Last State: Terminated`).
- Readiness fail → K8s **không gửi traffic** vào pod đó (loại khỏi Service endpoints) **nhưng KHÔNG restart**.
- Startup fail → K8s restart container (giống liveness), nhưng chỉ ở giai đoạn boot.
- Tại sao readiness fail KHÔNG restart pod? *(Vì có thể app tạm thời busy, không phải lỗi nghiêm trọng.)*
- Đặt `livenessProbe` mà KHÔNG có `readinessProbe` → rolling update có thể gửi traffic vào pod chưa ready, fail request.

## Probe có nhiều kiểu (chọn đúng theo app)

```yaml
# HTTP (web app)
httpGet:
  path: /health
  port: 5000

# TCP socket (DB, queue)
tcpSocket:
  port: 6379

# Exec command (script tự kiểm tra)
exec:
  command: ["sh", "-c", "pg_isready -U admin"]

# gRPC (K8s 1.24+)
grpc:
  port: 9000
```

## Bài kế tiếp

```bash
cp -r ../36-probes ../37-hpa
cd ../37-hpa
```
