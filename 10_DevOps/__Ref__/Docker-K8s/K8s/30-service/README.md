# Bài 30 — Service: expose Deployment

## Lệnh thủ công

```bash
kubectl apply -f service.yaml
kubectl get services -n myapp-dev

# Với Minikube:
minikube service myapp-service -n myapp-dev --url
# Sẽ in URL kiểu http://127.0.0.1:xxxxx

# Hoặc port-forward (cross-platform)
kubectl port-forward -n myapp-dev service/myapp-service 8080:80
curl http://localhost:8080

# Test load balancing — kết hợp xem log từ nhiều pod
for i in {1..10}; do curl -s http://localhost:8080; echo; done
kubectl logs -n myapp-dev -l app=myapp --tail=20
```

## Kết quả mong đợi

- `kubectl get svc` thấy `myapp-service` TYPE `NodePort`, PORT `80:30080/TCP`.
- 10 lần curl, log phân bố ra nhiều pod khác nhau.

## Câu hỏi

- `ClusterIP` (mặc định, chỉ trong cluster) vs `NodePort` (mở port trên mọi node) vs `LoadBalancer` (cloud provider tạo LB)
- `selector` Service hoạt động sao? *(matches `labels` của pod — Service chỉ load balance đến pod khớp label)*

## Bài kế tiếp

```bash
cp -r ../30-service ../31-rolling-update
cd ../31-rolling-update
```
