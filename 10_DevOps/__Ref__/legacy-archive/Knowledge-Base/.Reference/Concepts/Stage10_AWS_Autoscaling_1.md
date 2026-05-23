# GIAI ĐOẠN 10: AWS EKS & AUTOSCALING - CO GIÃN TỰ ĐỘNG

## 📌 MỤC TIÊU GIAI ĐOẠN 10
Triển khai App lên hạ tầng "enterprise" của Amazon (EKS).
Cấu hình **HPA (Horizontal Pod Autoscaler)**: Khi khách đông (CPU tăng), hệ thống tự đẻ thêm Pod. Khi khách vắng, tự giảm Pod để tiết kiệm tiền.

---

## 🏗️ PHẦN 1: TẠO CLUSTER (MẤT 15-20 PHÚT)

Dùng `eksctl` để tạo cluster đơn giản (2 nodes).

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
*Đi pha cà phê chờ nhé. Lệnh này sẽ tạo VPC, Subnet, EC2, EKS Control Plane...*
Sau khi xong, nó tự update `kubectl` context. Check:
```bash
kubectl get nodes
```

---

## ⚙️ PHẦN 2: CÀI ĐẶT METRICS SERVER

Để Autoscaling hoạt động, K8s cần biết CPU/RAM đang dùng bao nhiêu. Metrics Server làm việc này.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
Kiểm tra: `kubectl top nodes` (Nếu ra thông số là OK).

---

## 🚀 PHẦN 3: TRIỂN KHAI APP LÊN EKS

Dùng lại file manifests ở Giai đoạn 9, nhưng cần chút chỉnh sửa: **Service Gateway** nên đổi type thành `LoadBalancer` để AWS cấp cho ta cái Public IP (hoặc Domain) truy cập từ Internet.

Sửa `k8s/gateway.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway
spec:
  type: LoadBalancer # <--- Đổi thành LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: gateway
```

Apply lên EKS:
```bash
kubectl apply -f k8s/
```
Lấy địa chỉ truy cập:
```bash
kubectl get svc gateway
# Cột EXTERNAL-IP sẽ hiện một chuỗi dài (ELB DNS).
# Copy chuỗi đó dán vào trình duyệt -> Bùm! App của bạn đã online toàn cầu.
```

---

## 📈 PHẦN 4: HPA - AUTOSCALING

Giả sử ta muốn: Nếu CPU của `backend` vượt quá 50%, hãy tạo thêm Pod (tối đa 10).

### 1. Giới hạn Resource (Bắt buộc để HPA chạy)
Sửa `k8s/backend.yaml`, thêm phần `resources` vào container:
```yaml
    spec:
      containers:
      - name: backend
        # ...
        resources:
          limits:
            cpu: 200m # Max 0.2 core
          requests:
            cpu: 100m # Cần ít nhất 0.1 core
```
Apply lại: `kubectl apply -f k8s/backend.yaml`

### 2. Tạo HPA
```bash
kubectl autoscale deployment backend --cpu-percent=50 --min=2 --max=10
```
Kiểm tra:
```bash
kubectl get hpa
```

### 3. Stress Test (Load Test)
Tạo file `loadtest.js` (kịch bản cho K6):
```javascript
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 100, // 100 user ảo cùng lúc
  duration: '5m', // Bắn liên tục 5 phút
};

export default function () {
  // Thay URL bằng External IP của Gateway Service
  http.get('http://a1b2c3d4...us-east-1.elb.amazonaws.com/api/todos');
  sleep(1);
}
```

Chạy test:
```bash
k6 run loadtest.js
```

### 4. Quan sát Autoscaling
Mở Terminal khác:
```bash
kubectl get hpa -w
# REPLICAS sẽ tăng dần từ 2 -> 4 -> 8...
```
Khi tắt K6, số lượng Pod sẽ từ từ giảm về 2. Đây chính là sức mạnh của Cloud Native!

---

## 🧹 PHẦN 5: DỌN DẸP CHIẾN TRƯỜNG (QUAN TRỌNG!!!)

Làm xong phải xóa ngay kẻo tốn tiền.

1. **Xóa Service (để xóa Load Balancer - tốn tiền nhất):**
   ```bash
   kubectl delete svc gateway
   ```
2. **Xóa Cluster:**
   ```bash
   eksctl delete cluster --name todo-cluster --region us-east-1
   ```
   *Chờ lệnh này chạy xong hoàn toàn (10-15p).*
3. **Double Check:**
   Vào AWS Console -> EC2 -> Load Balancers / Auto Scaling Groups -> Đảm bảo trống trơn.

---

## 📝 TỔNG KẾT
Bạn đã triển khai thành công hệ thống tự động co giãn.
👉 **Bước tiếp theo:** Hệ thống tự chạy là tốt, nhưng nếu nó lỗi ngầm thì sao? Ta cần "bác sĩ" theo dõi sức khỏe. Giai đoạn 11: **Observability (Prometheus & Grafana)**.
