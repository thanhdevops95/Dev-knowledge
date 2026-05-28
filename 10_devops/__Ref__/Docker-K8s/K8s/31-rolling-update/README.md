# Bài 31 — Rolling Update & Rollback

## Bước chuẩn bị

Cần image `myapp:7.0` trên Docker Hub. Cách nhanh: tag lại từ 6.0.

```bash
# Trong terminal khác, ngoài cluster
docker tag <your-username>/myapp:6.0 <your-username>/myapp:7.0
docker push <your-username>/myapp:7.0
```

Hoặc rebuild với code thay đổi rồi push.

## Lệnh thủ công

```bash
# 1. Update image deployment
kubectl set image deployment/myapp-deployment \
  myapp=<your-username>/myapp:7.0 \
  -n myapp-dev

# 2. Xem rolling update
kubectl rollout status deployment/myapp-deployment -n myapp-dev
kubectl get pods -n myapp-dev -w   # Ctrl+C khi xong

# 3. Lịch sử
kubectl rollout history deployment/myapp-deployment -n myapp-dev

# 4. Rollback về revision trước
kubectl rollout undo deployment/myapp-deployment -n myapp-dev

# Hoặc về revision cụ thể
kubectl rollout undo deployment/myapp-deployment -n myapp-dev --to-revision=1
```

## Kết quả mong đợi

- Trong khi rolling update, có pod cũ và pod mới chạy đồng thời (mặc định maxSurge=25%, maxUnavailable=25%).
- KHÔNG downtime — Service tiếp tục route đến pod healthy.

## Bài kế tiếp

```bash
cp -r ../31-rolling-update ../32-configmap
cd ../32-configmap
```
