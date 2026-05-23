# 📚 Full K8s Demo Project - Tổng quan Files

## 🗂️ Cấu trúc Project

```
FullDemo/
├── README.md              # 🏠 Project overview & mục tiêu
├── QUICKSTART.md          # 🚀 Quick start guide (5 phút)
├── CONCEPTS.md            # 📚 Khái niệm chi tiết (Pods, Nodes, Services, etc.)
├── LAB_EXERCISES.md       # 🧪 Hands-on labs & challenges
├── TROUBLESHOOTING.md     # 🐛 Debugging guide
├── yaml-manifests/        # 📄 Tất cả YAML files
│   ├── 01-pod.yaml
│   ├── 02-deployment.yaml
│   └── 03-service.yaml
└── scripts/               # 🔧 Helper scripts
    ├── deploy-all.sh      # Deploy tất cả resources
    ├── test-app.sh        # Test application
    └── cleanup.sh         # Xóa tất cả resources
```

---

## 🎯 Bắt đầu ở đâu?

**Người mới bắt đầu?** → Đọc [QUICKSTART.md](QUICKSTART.md)

**Muốn hiểu sâu khái niệm?** → Đọc [CONCEPTS.md](CONCEPTS.md)

**Muốn thực hành?** → Làm [LAB_EXERCISES.md](LAB_EXERCISES.md)

**Gặp vấn đề?** → Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📖 Learning Path đề xuất

### Path 1: Người mới (2-3 giờ)
1. Read [QUICKSTART.md](QUICKSTART.md) (10 phút)
2. Deploy project (5 phút)
3. Đọc [CONCEPTS.md](CONCEPTS.md) section by section (1 giờ)
4. Chạy [scripts/test-app.sh](scripts/test-app.sh) (10 phút)
5. Làm Lab 1-3 trong [LAB_EXERCISES.md](LAB_EXERCISES.md) (1 giờ)

### Path 2: Thực hành nhanh (30 phút)
1. Deploy project: `./scripts/deploy-all.sh`
2. Chạy test: `./scripts/test-app.sh`
3. Dùng commands trong CONCEPTS.md để explore
4. Cleanup: `./scripts/cleanup.sh`

### Path 3: Deep dive (1 ngày)
1. Hoàn thành tất cả Lab Exercises trong [LAB_EXERCISES.md](LAB_EXERCISES.md)
2. Thử custom YAML files:
   - Thay đổi replicas count
   - Thay đổi image version
   - Thêm labels mới
   - Thử các loại service khác (ClusterIP)
3. Debug intentionally (break things and fix)
4. Ghi lại findings trong notes

---

## 🔍 Các file quan trọng

### 1. YAML Manifests

**[01-pod.yaml](yaml-manifests/01-pod.yaml)** - Pod đơn giản
- Minimal pod definition
- Labels & container port
- Resource requests/limits

**[02-deployment.yaml](yaml-manifests/02-deployment.yaml)** - Deployment với ReplicaSet
- Replicas management
- Pod template với labels
- Probes (readiness/liveness)
- Resource management

**[03-service.yaml](yaml-manifests/03-service.yaml)** - NodePort Service
- Selector matching
- Port configuration (port/targetPort/nodePort)
- Service types

### 2. Scripts

**[deploy-all.sh](scripts/deploy-all.sh)** - Deploy tất cả
```bash
./scripts/deploy-all.sh
```

**[test-app.sh](scripts/test-app.sh)** - Test application
```bash
./scripts/test-app.sh
```

**[cleanup.sh](scripts/cleanup.sh)** - Cleanup resources
```bash
./scripts/cleanup.sh
```

---

## 🎓 Key Concepts Coverage

| Concept | File | Section |
|---------|------|---------|
| Pod | CONCEPTS.md | 1. POD 🥜 |
| Node | CONCEPTS.md | 2. NODE 🖥️ |
| ReplicaSet | CONCEPTS.md | 3. REPLICASET 🔄 |
| Deployment | CONCEPTS.md | 4. DEPLOYMENT 🚀 |
| Service | CONCEPTS.md | 5. SERVICE 🌐 |
| Labels/Selectors | CONCEPTS.md | 6. LABELS & SELECTORS 🏷️ |
| Ports | CONCEPTS.md | 7. PORTS trong K8s 🔌 |
| Minikube | CONCEPTS.md | 8. MINIKUBE SPECIFIC 🎯 |

---

## 💡 Quick Commands Reference

### View Resources
```bash
kubectl get all                          # Tất cả resources
kubectl get pods -o wide                # Pods với IP & node
kubectl get pods --show-labels          # Pods với labels
kubectl get endpoints <service-name>    # Endpoints
```

### Describe Resources
```bash
kubectl describe pod <pod-name>
kubectl describe svc <service-name>
kubectl describe deployment <name>
kubectl describe node <node-name>
```

### Test & Debug
```bash
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- sh
kubectl port-forward svc/<name> 8080:8080
curl http://$(minikube ip):<nodePort>
```

### Modify
```bash
kubectl scale deployment <name> --replicas=3
kubectl set image deployment/<name> container=image:tag
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>
```

---

## 🎯 Demo Scenarios

### Scenario 1: First Deployment
```bash
cd Project_K8s_Test/FullDemo
./scripts/deploy-all.sh
./scripts/test-app.sh
```

**Expected output:**
- 2 pods running
- 1 deployment
- 1 replicaset
- 1 service với NodePort

### Scenario 2: Scale and Observe
```bash
kubectl scale deployment curl-app-deployment --replicas=4
kubectl get pods -o wide  # Xem 4 pods
```

**Observe:**
- ReplicaSet tạo thêm 2 pods
- Pods có names: curl-app-deployment-xxxxx-xxxxx
- Pods có IPs khác nhau
- Pods có thể trên cùng node (single-node cluster)

### Scenario 3: Service Discovery
```bash
kubectl get endpoints curl-app-service
# Endpoints là IP của tất cả pods có label app=curl-app

kubectl exec -it <pod-name> -- curl curl-app-service:8080
# Works! Service DNS name resolves to service IP
```

### Scenario 4: Pod Failure & Recovery
```bash
kubectl delete pod <pod-name>
kubectl get pods
# ReplicaSet tự động tạo pod mới ✅
# Pod mới có tên khác (suffix mới)
```

---

## 📊 Expected Outputs

### kubectl get all
```
NAME                               READY   STATUS    RESTARTS   AGE
pod/curl-app-deployment-xxxxx      1/1     Running   0          5m

NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/curl-app-service     NodePort    10.96.123.456   <none>        8080:30007/TCP   5m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/curl-app-deployment   1/1     1            1           5m

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/curl-app-deployment-xxxxx   1         1         1       5m
```

### Minikube IP & NodePort
```bash
$ minikube ip
192.168.49.2

$ kubectl get svc curl-app-service
NAME                TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
curl-app-service    NodePort   10.96.123.456   <none>        8080:30007/TCP   5m

Access URL: http://192.168.49.2:30007
```

---

## 🧠 Connection Flow

```
┌─────────────────┐
│   User Request  │ curl http://192.168.49.2:30007
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Node: minikube (IP: 192.168.49.2)     │
│  Port: 30007 (NodePort)                │
│  Forward to service port: 8080         │
└────────┬──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Service: curl-app-service             │
│  ClusterIP: 10.96.123.456:8080        │
│  Selector: app=curl-app                │
└────────┬──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Pods (with label app=curl-app)       │
│  - curl-app-deployment-xxxxx-aaaaa    │
│    IP: 10.244.1.5:80                  │
│  - curl-app-deployment-xxxxx-bbbb     │
│    IP: 10.244.2.7:80                  │
│  Load balancing giữa các pods         │
└────────┬──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Container: curl-app                   │
│  Image: curlimages/curl:latest        │
│  Command: sleep 3600                  │
└─────────────────────────────────────────┘
```

---

## 🎓 After Demo Checklist

Sau khi hoàn thành demo, bạn có thể:

- [ ] Hiểu Pod là gì và cách tạo pod
- [ ] Hiểu Node là gì và xem pods trên node nào
- [ ] Hiểu ReplicaSet đảm bảo số lượng pods
- [ ] Hiểu Deployment quản lý ReplicaSet
- [ ] Hiểu Service expose pods
- [ ] Hiểu Labels & Selectors kết nối resources
- [ ] Hiểu Ports: containerPort, port, targetPort, nodePort
- [ ] Có thể kubectl get/describe/logs/exec
- [ ] Có thể scale deployment
- [ ] Có thể rollout status/history
- [ ] Biết cách debug với kubectl describe
- [ ] Biết cách test service từ trong cluster và outside

---

## 🚀 Next Steps

Sau khi hoàn thành project này:

1. **Thử Horizontal Pod Autoscaler**:
   ```bash
   minikube addons enable metrics-server
   kubectl autoscale deployment curl-app-deployment --cpu-percent=10 --min=1 --max=5
   ```

2. **Thử ConfigMap & Secret**:
   - Tạo ConfigMap với config
   - Mount vào pod

3. **Thử PersistentVolume**:
   - Tạo PVC
   - Mount vào pod

4. **Thử Ingress** (minikube addons enable ingress):
   - Tạo Ingress resource
   - Configure host rules

5. **Multi-namespace**:
   - Tạo namespace riêng
   - Deploy resources vào namespace đó

6. **Real Application**:
   - Deploy Nginx hoặc Apache
   - Config volume mount cho static files
   - Test rolling update

---

## 📚 Additional Resources

- **Kubernetes Basics Tutorial**: https://kubernetes.io/docs/tutorials/kubernetes-basics/
- **kubectl Cheat Sheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **Minikube Start Guide**: https://minikube.sigs.k8s.io/docs/start/
- **K8s Concepts Deep Dive**: https://kubernetes.io/docs/concepts/

---

**Ready to start?** → [QUICKSTART.md](QUICKSTART.md)

**Questions?** → Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Practice?** → Do [LAB_EXERCISES.md](LAB_EXERCISES.md)

**Want details?** → Read [CONCEPTS.md](CONCEPTS.md)
