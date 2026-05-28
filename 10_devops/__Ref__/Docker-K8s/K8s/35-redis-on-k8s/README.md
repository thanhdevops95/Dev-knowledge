# Bài 35 — Redis trong K8s + app kết nối

> **Tương tự Bài 21 (Docker)** nhưng trên K8s.

## Lệnh thủ công

```bash
# 1. Apply Redis (Deployment + Service)
kubectl apply -f redis.yaml

# 2. Apply myapp (đã sửa env REDIS_HOST)
kubectl apply -f deployment.yaml

# 3. Apply Service nếu chưa có
kubectl apply -f service.yaml 2>/dev/null

# 4. Đợi pod ready
kubectl wait --for=condition=ready pod -l app=redis -n myapp-dev --timeout=60s
kubectl wait --for=condition=ready pod -l app=myapp -n myapp-dev --timeout=60s

# 5. Test
kubectl port-forward -n myapp-dev service/myapp-service 8080:80 &
PF=$!
sleep 2
for i in {1..5}; do curl http://localhost:8080; echo; done
kill $PF 2>/dev/null
```

## ⚠️ Lưu ý quan trọng — bug cần biết

K8s tự inject biến môi trường `<SERVICE>_PORT=tcp://IP:PORT` vào pod. Nếu app dùng `int(os.getenv("REDIS_PORT"))` sẽ lỗi `ValueError: invalid literal for int(): 'tcp://...'`.

**Cách tránh:** đặt tên biến app khác (`APP_REDIS_HOST` thay vì `REDIS_HOST`), hoặc parse `tcp://host:port`.

Repo Compose ở Bài 23 dùng `REDIS_HOST=redis` thì OK với Compose. Nhưng deploy K8s với image cũ thì lỗi 500 ở `/`. → Phải rebuild image với code mới hoặc đổi tên biến trong deployment.

## Câu hỏi

- Tên service Redis là gì trong DNS K8s? *(`redis.myapp-dev.svc.cluster.local`, gọn: `redis`)*

## Bài kế tiếp

```bash
cp -r ../35-redis-on-k8s ../36-probes
cd ../36-probes
```
