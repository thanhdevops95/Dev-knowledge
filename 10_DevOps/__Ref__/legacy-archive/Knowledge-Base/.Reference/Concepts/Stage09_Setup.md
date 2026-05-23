# 🛠️ GIAI ĐOẠN 9: CHUẨN BỊ KUBERNETES LOCAL

## 📌 MỤC TIÊU
Trước khi lên Cloud trả tiền, chúng ta cần một môi trường Kubernetes (K8s) miễn phí ngay trên máy để thực hành.

---

## 1. CÀI ĐẶT KUBECTL (CMD TOOL)
`kubectl` là "cây đũa thần" để ra lệnh cho K8s Cluster.

### macOS (Homebrew)
```bash
brew install kubectl
```
### Windows (Chocolatey hoặc tải trực tiếp)
```powershell
choco install kubernetes-cli
```

### Kiểm tra
```bash
kubectl version --client
```

---

## 2. CÀI ĐẶT MINIKUBE (LOCAL CLUSTER)
Minikube tạo một máy ảo chứa K8s Cluster 1 node.

### Cài đặt
- **macOS**: `brew install minikube`
- **Windows**: [Tải installer](https://minikube.sigs.k8s.io/docs/start/)

### Khởi động Cluster
```bash
minikube start --driver=docker
```
*(Nếu dùng Docker Desktop, driver=docker là ổn nhất. Windows có thể dùng Hyper-V).*

### Kiểm tra Cluster
```bash
kubectl get nodes
# Output: minikube   Ready   control-plane ...
```

---

## 3. TẠO THƯ MỤC K8S
```bash
mkdir k8s
```

## ✅ CHECKLIST
- `kubectl` đã cài.
- `minikube` đã chạy (Ready).

Sẵn sàng bước vào thế giới Container Orchestration!
