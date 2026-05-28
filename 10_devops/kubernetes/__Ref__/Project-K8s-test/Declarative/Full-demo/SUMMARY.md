# 🎯 K8s Full Demo - Summary

## 📦 Project hoàn tất!

Bạn vừa tạo một project K8s demo đầy đủ với các YAML files và scripts để học:

✅ **Pods** - Đơn vị cơ bản nhất
✅ **Nodes** - Worker machines
✅ **ReplicaSet** - Maintain desired pod count
✅ **Deployment** - Declarative updates với rolling updates
✅ **Service (NodePort)** - Expose pods ra outside
✅ **Labels & Selectors** - Connection giữa resources
✅ **Ports** - containerPort, port, targetPort, nodePort
✅ **Minikube** - Local K8s cluster

---

## 🚀 Cách chạy nhanh (3 commands)

```bash
# 1. Start Minikube
minikube start --driver=docker

# 2. Deploy
cd /Users/rom/K8S/Project_K8s_Test/FullDemo
./scripts/deploy-all.sh

# 3. Test
./scripts/test-app.sh

# 4. Truy cập từ browser:
# http://$(minikube ip):30007
```

---

## 📚 Files trong project

| File | Mô tả | Dành cho |
|------|-------|----------|
| `README.md` | Project overview & goals | Đọc đầu tiên |
| `INDEX.md` | Tổng quan tất cả files | Reference |
| `QUICKSTART.md` | Quick start trong 5 phút | Người mới |
| `CONCEPTS.md` | Giải thích chi tiết từng khái niệm | Học sâu |
| `LAB_EXERCISES.md` | Hands-on labs & challenges | Thực hành |
| `TROUBLESHOOTING.md` | Debugging guide | Khi gặp lỗi |
| `yaml-manifests/*.yaml` | Các YAML files | Reference code |
| `scripts/*.sh` | Helper scripts | Chạy demo |

---

## 🎓 Learning Path đề xuất

### 1. Khởi động (30 phút)
```
Read: QUICKSTART.md
Deploy: ./scripts/deploy-all.sh
Test: ./scripts/test-app.sh
Explore: kubectl get all, kubectl describe <resource>
```

### 2. Hiểu khái niệm (1-2 giờ)
```
Đọc: CONCEPTS.md section by section
Thực hành: Chạy commands trong CONCEPTS.md
Ghi chú: Vào pod shell với kubectl exec
```

### 3. Lab Exercises (1-2 giờ)
```
Làm: LAB_EXERCISES.md Lab 1-5
Scale: kubectl scale deployment --replicas=3
Observe: Xem pods mới được tạo
Debug: Dùng troubleshooting commands
```

### 4. Deep Dive (tự experiment)
```
- Thay đổi YAML files
- Thử break và fix
- Rolling update
- Rollback
- Labels experiments
- NodePort vs ClusterIP
```

---

## 🔑 Key Takeaways

### 1. Declarative vs Imperative
- **Declarative** (YAML): "Đây là state tôi muốn"
- **Imperative** (kubectl run): "Làm cái này ngay"
- **Demo dùng Declarative** - best practice

### 2. Resource Hierarchy
```
Deployment
  └── ReplicaSet
        └── Pods (2 replicas)
              └── Container (curl-app)
```

### 3. Labels & Selectors là cốt lõi
- Labels: metadata (key-value)
- Selectors: filter resources by labels
- Service dùng selector để tìm pods
- **Selector phải match EXACTLY với pod labels**

### 4. Service Discovery
- Service có stable DNS name: `<service-name>.<namespace>.svc.cluster.local`
- Within cluster: curl `<service-name>:<port>`
- Outside cluster: curl `<node-ip>:<nodePort>`
- Service load balance giữa các pods

### 5. Port Types
- **containerPort**: Port container lắng nghe (80)
- **port**: Service port trong cluster (8080)
- **targetPort**: Forward đến container port (80)
- **nodePort**: Port trên node để access từ outside (30007)

---

## 🎯 Commands phải biết

```bash
# View
kubectl get all
kubectl get pods -o wide
kubectl describe <resource> <name>
kubectl logs <pod-name>

# Exec
kubectl exec -it <pod-name> -- sh

# Modify
kubectl scale deployment <name> --replicas=3
kubectl set image deployment/<name> container=image:tag

# Rollout
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>
kubectl rollout undo deployment/<name>

# Delete
kubectl delete -f yaml-manifests/
kubectl delete all --all
```

---

## 🐛 Nếu gặp vấn đề

1. Check status: `kubectl get all`
2. Check events: `kubectl get events --sort-by='.lastTimestamp'`
3. Describe resource: `kubectl describe pod <name>`
4. Check logs: `kubectl logs <pod-name>`
5. Check endpoints: `kubectl get endpoints <service-name>`
6. Check labels: `kubectl get pods --show-labels`
7. Tham khảo: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📊 Expected Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MINIKUBE CLUSTER                     │
│  ┌─────────────────────────────────────────────────────┐│
│  │                   Node: minikube                   ││
│  │  IP: 192.168.49.2                                 ││
│  │                                                   ││
│  │  ┌─────────────────────────────────────────────┐  ││
│  │  │  Service: curl-app-service (NodePort)      │  ││
│  │  │  Port: 8080 → targetPort: 80               │  ││
│  │  │  NodePort: 30007                           │  ││
│  │  │  Selector: app=curl-app                    │  ││
│  │  └───────┬───────────────────────────┬───────┘  ││
│  │          │                           │          ││
│  │          ▼                           ▼          ││
│  │  ┌─────────────────┐   ┌─────────────────┐     ││
│  │  │  Pod: curl-app  │   │  Pod: curl-app  │     ││
│  │  │  - app=curl-app│   │  - app=curl-app│     ││
│  │  │  IP: 10.244.1.5│   │  IP: 10.244.1.6│     ││
│  │  │  Port: 80      │   │  Port: 80      │     ││
│  │  │  Container:    │   │  Container:    │     ││
│  │  │  curlimages/   │   │  curlimages/   │     ││
│  │  │  curl:latest   │   │  curl:latest   │     ││
│  │  └─────────────────┘   └─────────────────┘     ││
│  │           │ Load Balance                        ││
│  └───────────┼───────────────────────────────────────┘│
│              │                                       ││
│   Outside:   │ curl http://192.168.49.2:30007       ││
└──────────────┴───────────────────────────────────────┘│
```

---

## 🧪 Experiment Ideas

1. **Scale và observe:**
   ```bash
   kubectl scale deployment curl-app-deployment --replicas=5
   kubectl get pods -o wide
   ```

2. **Pod failure:**
   ```bash
   kubectl delete pod <pod-name>
   # ReplicaSet tạo pod mới ✅
   ```

3. **Update image:**
   ```bash
   kubectl set image deployment/curl-app-deployment \
     curl-app=curlimages/curl:8.5.0
   kubectl rollout status deployment/curl-app-deployment
   ```

4. **Label experiments:**
   ```bash
   kubectl get pods --show-labels
   kubectl label pod <pod-name> version=v2
   kubectl get pods -l version=v2
   ```

5. **Service discovery:**
   ```bash
   kubectl exec -it <pod-name> -- nslookup curl-app-service
   kubectl exec -it <pod-name> -- curl curl-app-service:8080
   ```

---

## 🎓 Check your understanding

Sau khi hoàn thành demo, trả lời:

1. **Pod** là gì? Một pod có thể chứa bao nhiêu container?
2. **Node** là gì? Pods chạy trên node nào?
3. **ReplicaSet** làm gì? Ai tạo và quản lý ReplicaSet?
4. **Deployment** có tính năng gì? Làm sao để update?
5. **Service** dùng để làm gì? Có mấy loại?
6. **NodePort** là gì? Port range?
7. **Labels** là gì? Dùng để làm gì?
8. **Selectors** là gì? Nó kết nối thế nào?
9. **containerPort vs targetPort vs port vs nodePort**?
10. **Kubectl commands** quan trọng nhất là gì?

---

## 📚 Further Learning

Sau project này, bạn có thể:

1. **Persistent Storage**: PVC, PV, StorageClass
2. **Config & Secrets**: ConfigMap, Secret
3. **Networking**: Ingress, NetworkPolicy
4. **Security**: RBAC, ServiceAccount, PodSecurityPolicy
5. **Advanced**: StatefulSet, DaemonSet, Job, CronJob
6. **Monitoring**: Metrics Server, HPA, Prometheus
7. **CI/CD**: GitOps với ArgoCD/Flux

---

## 🎉 Chúc mừng!

Bạn vừa tạo một project K8s demo đầy đủ với:
- ✅ YAML manifests đúng best practices
- ✅ Các scripts để deploy, test, cleanup
- ✅ Tài liệu chi tiết về từng khái niệm
- ✅ Lab exercises để thực hành
- ✅ Troubleshooting guide

**Time to learn K8s!** 🚀

---

**Start Learning:** [QUICKSTART.md](QUICKSTART.md) | [INDEX.md](INDEX.md)
