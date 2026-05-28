# 📦 KUBERNETES LEARNING PROJECT - TỔNG QUAN

## ✅ ĐÃ TẠO NHỮNG GÌ

### 📁 Files trong project:
1. **pods/curl-pod.yaml** - Pod đơn lẻ với container curl
2. **deployments/curl-deployment.yaml** - Deployment với 3 replicas
3. **services/curl-service.yaml** - NodePort Service expose ứng dụng
4. **configmaps/curl-config.yaml** - ConfigMap với configuration
5. **deploy.sh** - Script deploy tự động
6. **README.md** - Tài liệu đầy đủ
7. **QUICK-START.md** - Hướng dẫn từng bước chi tiết
8. **KUBERNETES-EXPLAINED.md** - Giải thích sâu từng khái niệm

---

## 🎯 MỤC TIÊU PROJECT

**Học Kubernetes thông qua thực hành với:**
- ✅ Pod (smallest unit)
- ✅ Node (worker machine)
- ✅ Labels & Selectors (grouping & discovery)
- ✅ ReplicaSet (auto-healing, scaling)
- ✅ Deployment (updates, rollback)
- ✅ Service (network abstraction)
- ✅ NodePort (external access)
- ✅ ConfigMap (configuration)
- ✅ YAML syntax
- ✅ Ports (containerPort, port, targetPort, nodePort)

---

## 🚀 CÁCH BẮT ĐẦU (30 GIÂY)

```bash
# 1. Navigate
cd /Users/rom/K8S/Project_K8s_Test/Declarative/k8s-full-project

# 2. Chạy script (nếu có kubectl và cluster)
./deploy.sh

# Hoặc manual:
kubectl apply -f .
```

**Nếu chưa có cluster:**
```bash
# Cài Minikube (recommended)
brew install minikube
minikube start --memory=4096 --cpus=2

# Hoặc Docker Desktop: Enable Kubernetes trong Settings
```

---

## 🧪 TEST NGAY

```bash
# Method 1: Port-forward (không cần NodePort)
kubectl port-forward service/curl-service 8080:80
# Mở http://localhost:8080

# Method 2: Test từ trong cluster
kubectl run curl-test --image=curlimages/curl:latest --rm -i --tty -- \
  curl http://curl-service

# Method 3: Minikube users
minikube service curl-service
```

---

## 📊 KIỂM TRA TRẠNG THÁI

```bash
# Xem tất cả
kubectl get all

# Xem chi tiết
kubectl get pods -o wide
kubectl get nodes
kubectl describe service curl-service
kubectl get endpoints curl-service

# Xem labels
kubectl get pods --show-labels
```

---

## 🎓 CÁC KHÁI NIỆM HỌC ĐƯỢC

| ✅ | Khái niệm | File minh họa |
|----|-----------|---------------|
| 1 | **Pod** | pods/curl-pod.yaml |
| 2 | **Node** | `kubectl get nodes` output |
| 3 | **Label** | Metadata labels trong tất cả YAML |
| 4 | **Selector** | Service và Deployment selector |
| 5 | **ReplicaSet** | Deployment.spec.replicas |
| 6 | **Deployment** | deployments/curl-deployment.yaml |
| 7 | **Port Types** | services/curl-service.yaml |
| 8 | **NodePort** | Service.type: NodePort |
| 9 | **YAML** | Tất cả .yaml files |
| 10 | **ConfigMap** | configmaps/curl-config.yaml |

---

## 📚 TÀI LIỆU ĐỌC

1. **QUICK-START.md** ← **BẮT ĐẦU Ở ĐÂY**
   - Step-by-step hướng dẫn
   - Commands cụ thể
   - Troubleshooting

2. **KUBERNETES-EXPLAINED.md**
   - Giải thích chi tiết từng khái niệm
   - Examples và use cases
   - Best practices

3. **README.md**
   - Tổng quan project
   - Cấu trúc thư mục
   - Commands tổng hợp

---

## 🎯 LEARNING PATH

### Ngay bây giờ:
1. Đọc **QUICK-START.md** (5 phút)
2. Deploy project (5 phút)
3. Test và explore (10 phút)
4. Đọc **KUBERNETES-EXPLAINED.md** (30 phút)

### Sau đó:
1. Thử scale deployment: `kubectl scale deployment curl-deployment --replicas=5`
2. Thử update image: `kubectl set image deployment/curl-deployment curl-container=curlimages/curl:8.5.0`
3. Thử rollback: `kubectl rollout undo deployment/curl-deployment`
4. Thử labels: `kubectl label pod <pod-name> version=v2`
5. Thử namespace mới: `kubectl create namespace dev && kubectl apply -f . -n dev`

---

## 🆘 NẾU GẶP LỖI

### "No cluster found"
→ Cài Minikube: `brew install minikube && minikube start`

### "The connection to the server localhost:8080 was refused"
→ Start cluster: `minikube start` hoặc enable Docker Desktop K8s

### Pods đang Pending
→ `kubectl describe pod <pod-name>` - Check node resources

### Pods CrashLoopBackOff
→ `kubectl logs <pod-name>` - Check logs

### Service không có endpoints
→ Check selector match: `kubectl get pods --show-labels`

---

## 📈 MONITORING

```bash
# Resource usage
kubectl top pods
kubectl top nodes

# Events
kubectl get events --sort-by='.lastTimestamp'

# Logs
kubectl logs -l app=curl-app
```

---

## 🗑️ CLEANUP

```bash
# Xóa project
kubectl delete -f .

# Xóa cluster (Minikube)
minikube stop
minikube delete

# Xóa cluster (Kind)
kind delete cluster

# Xóa cluster (Docker Desktop)
# Turn off Kubernetes in Settings
```

---

## 🎉 KẾT QUẢ SAU KHI HOÀN THÀNH

Sau khi đi qua project này, bạn sẽ hiểu rõ:

✅ **Pod**: Smallest unit, containers, shared network
✅ **Node**: Worker machines, scheduling, resources
✅ **Label**: Key-value tags, metadata
✅ **Selector**: Matching resources với labels
✅ **ReplicaSet**: Ensuring desired state, scaling
✅ **Deployment**: Managing ReplicaSets, rolling updates
✅ **Service**: Network abstraction, load balancing
✅ **NodePort**: External access, port mapping
✅ **ConfigMap**: Configuration management
✅ **YAML**: Declarative configuration

**Và bạn có thể:**
- Deploy ứng dụng lên K8s
- Expose qua Service/NodePort
- Scale up/down replicas
- Update và rollback
- Debug và troubleshooting cơ bản

---

## 🔗 RESOURCES

- **Official Docs**: https://kubernetes.io/docs/home/
- **Interactive Tutorial**: https://kubernetes.io/docs/tutorials/kubernetes-basics/
- **Kubectl Cheatsheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **K8s Concepts**: https://kubernetes.io/docs/concepts/

---

**🎯 BẮT ĐẦU NGAY:**
```bash
cat QUICK-START.md
```

**Happy Learning! 🚀**
