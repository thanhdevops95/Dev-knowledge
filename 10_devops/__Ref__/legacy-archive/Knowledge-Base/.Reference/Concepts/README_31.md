# 🎯 GIAI ĐOẠN 10: AWS EKS & AUTOSCALING

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-10**.
- **Giai đoạn 10: AWS EKS & HPA** - Deploy lên Cloud, tự động scale!

Minikube là local. EKS là production-ready Kubernetes trên AWS.

## 🚀 CÁCH CHẠY

### Bước 1: Tạo EKS Cluster
```bash
eksctl create cluster \
  --name todo-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```
⏱️ Mất 15-20 phút

### Bước 2: Cài Metrics Server
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

### Bước 3: Deploy App
```bash
kubectl apply -f k8s/
```

### Bước 4: Lấy URL
```bash
kubectl get svc gateway
# Copy EXTERNAL-IP (ELB DNS)
```

### Bước 5: Setup HPA
```bash
kubectl autoscale deployment backend --cpu-percent=50 --min=2 --max=10
```

## 🧪 TESTING

### Test 1: Load Test
Tạo file `loadtest.js`:
```javascript
import http from 'k6/http';
export const options = { vus: 100, duration: '5m' };
export default function () {
  http.get('http://YOUR_ELB_DNS/api/todos');
}
```

Chạy:
```bash
k6 run loadtest.js
```

### Test 2: Xem Autoscaling
```bash
kubectl get hpa -w
# REPLICAS sẽ tăng từ 2 → 10
```

## ⚠️ DỌN DẸP (QUAN TRỌNG!)

```bash
# Xóa Service (xóa Load Balancer trước)
kubectl delete svc gateway

# Xóa Cluster
eksctl delete cluster --name todo-cluster --region us-east-1
```

## ✅ CHECKLIST

- [ ] Tạo được EKS cluster
- [ ] Deploy app thành công
- [ ] Truy cập được qua ELB
- [ ] HPA hoạt động
- [ ] **ĐÃ XÓA CLUSTER** (tránh tốn tiền!)

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **EKS:** Managed Kubernetes trên AWS
2. ✅ **HPA:** Horizontal Pod Autoscaler
3. ✅ **Load Balancer:** AWS ELB tự động tạo
4. ✅ **Cloud Cost:** Hiểu chi phí Cloud

## 🚧 TIẾP THEO

Giai đoạn 11: **Monitoring** - Prometheus & Grafana!
