# 🧪 Lab Exercises - Thực hành K8s

## Lab 1: Kiểm tra Cluster

### Mục tiêu: Hiểu cluster structure

**Tasks:**
1. Xem tất cả nodes:
   ```bash
   kubectl get nodes
   kubectl get nodes -o wide
   ```

2. Xem chi tiết node:
   ```bash
   kubectl describe node minikube
   # Tìm sections: Capacity, Allocatable, Non-terminated Pods
   ```

3. Xem labels của node:
   ```bash
   kubectl get nodes --show-labels
   ```

**Questions:**
- Node có bao nhiêu CPU và Memory?
- Node chạy OS gì?
- Node có những labels gì?

---

## Lab 2: Deploy và Scale Pods

### Mục tiêu: Hiểu Deployment và ReplicaSet

**Tasks:**
1. Deploy application:
   ```bash
   kubectl apply -f yaml-manifests/
   ```

2. Xem replicas:
   ```bash
   kubectl get replicaset
   kubectl get pods
   ```

3. Scale deployment lên 3 replicas:
   ```bash
   kubectl scale deployment curl-app-deployment --replicas=3
   kubectl get pods  # Xem có 3 pods không?
   ```

4. Xem rollout status:
   ```bash
   kubectl rollout status deployment/curl-app-deployment
   ```

5. Scale xuống 1 replica:
   ```bash
   kubectl scale deployment curl-app-deployment --replicas=1
   ```

**Questions:**
- ReplicaSet tên là gì?
- Pods có tên theo format nào?
- Khi scale, pods mới có cùng IP với pods cũ không?

---

## Lab 3: Labels & Selectors

### Mục tiêu: Hiểu cách labels và selectors kết nối resources

**Tasks:**
1. Xem pods với labels:
   ```bash
   kubectl get pods --show-labels
   ```

2. Xem service với selector:
   ```bash
   kubectl get svc curl-app-service -o yaml
   # Xem section spec.selector
   ```

3. Filter pods by label:
   ```bash
   kubectl get pods -l app=curl-app
   kubectl get pods -l tier=frontend
   ```

4. Thêm label mới cho pod:
   ```bash
   POD_NAME=$(kubectl get pods -o jsonpath='{.items[0].metadata.name}')
   kubectl label pod $POD_NAME version=v1
   kubectl get pod $POD_NAME --show-labels
   ```

5. Xem endpoints của service:
   ```bash
   kubectl get endpoints curl-app-service
   # Endpoints là IP của pods có label match
   ```

**Questions:**
- Service selector có labels gì?
- Pods có labels gì?
- Nếu thay đổi label của pod, service có vẫn route được không?

---

## Lab 4: Service và Networking

### Mục tiêu: Hiểu cách service expose pods

**Tasks:**
1. Xem service:
   ```bash
   kubectl get svc
   kubectl describe svc curl-app-service
   ```

2. Xem endpoints:
   ```bash
   kubectl get endpoints curl-app-service -o wide
   ```

3. Port-forward service:
   ```bash
   kubectl port-forward svc/curl-app-service 8080:8080
   # Trong terminal khác: curl http://localhost:8080
   ```

4. Test từ trong cluster:
   ```bash
   # Exec vào pod và curl service name
   kubectl exec -it <pod-name> -- sh
   # Trong pod:
   curl curl-app-service:8080
   ```

5. Test từ host (NodePort):
   ```bash
   NODE_PORT=$(kubectl get svc curl-app-service -o jsonpath='{.spec.ports[0].nodePort}')
   MINIKUBE_IP=$(minikube ip)
   curl http://$MINIKUBE_IP:$NODE_PORT
   ```

**Questions:**
- Service port là gì?
- TargetPort là gì?
- NodePort là bao nhiêu?
- IP của pods là gì? Có ping được giữa các pod không?

---

## Lab 5: Pod Lifecycle

### Mục tiêu: Hiểu cách pod được schedule và quản lý

**Tasks:**
1. Xem pod详细信息:
   ```bash
   kubectl get pod <pod-name> -o wide
   kubectl describe pod <pod-name>
   ```

2. Xem events:
   ```bash
   kubectl get events --sort-by='.lastTimestamp'
   ```

3. Xem logs:
   ```bash
   kubectl logs <pod-name>
   ```

4. Delete pod và xem replicaset tạo lại:
   ```bash
   kubectl delete pod <pod-name>
   kubectl get pods  # Pod mới có tên khác (restart)
   ```

5. Xem pod trên node nào:
   ```bash
   kubectl get pods -o wide
   ```

6. Exec vào pod shell:
   ```bash
   kubectl exec -it <pod-name> -- sh
   # Trong pod:
   env          # Xem environment variables
   ps aux        # Xem processes
   netstat -tlnp # Xem ports
   exit
   ```

**Questions:**
- Pod chạy trên node nào?
- Pod có IP nào?
- Khi delete pod, điều gì xảy ra?
- ReplicaSet có tạo pod mới không?

---

## Lab 6: Experiment với YAML

### Mục tiêu: Hiểu YAML structure và apply changes

**Tasks:**
1. Xem deployment YAML:
   ```bash
   kubectl get deployment curl-app-deployment -o yaml
   ```

2. Edit deployment:
   ```bash
   kubectl edit deployment curl-app-deployment
   # Thay đổi replicas từ 1 → 3
   # Save và exit
   ```

3. Xem rollout history:
   ```bash
   kubectl rollout history deployment/curl-app-deployment
   ```

4. Update image:
   ```bash
   kubectl set image deployment/curl-app-deployment \
     curl-app=curlimages/curl:8.5.0
   kubectl rollout status deployment/curl-app-deployment
   ```

5. Rollback nếu cần:
   ```bash
   kubectl rollout undo deployment/curl-app-deployment
   ```

**Questions:**
- Deployment tạo ReplicaSet tên gì?
- YAML deployment có những phần quan trọng nào?
- Rolling update có tạo downtime không?

---

## Lab 7: Multi-tier Application (Optional)

### Mục tiêu: Tạo app với frontend + backend

**Tasks:**
1. Tạo backend deployment (port 3000):
   ```yaml
   # backend-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: backend-app
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: backend
     template:
       metadata:
         labels:
           app: backend
       spec:
         containers:
         - name: backend
           image: curlimages/curl:latest
           command: ["sleep", "3600"]
   ```

2. Tạo backend service:
   ```yaml
   # backend-service.yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: backend-service
   spec:
     selector:
       app: backend
     ports:
     - port: 3000
       targetPort: 3000
   ```

3. Tạo frontend deployment với label tier=frontend

4. Tạo frontend service NodePort

5. Frontend pods có thể access backend qua service name:
   ```bash
   kubectl exec -it <frontend-pod> -- curl backend-service:3000
   ```

---

## Lab 8: Troubleshooting

### Mục tiêu: Biết cách debug khi có vấn đề

**Scenarios:**

**Scenario 1: Pod stuck trong Pending**
```bash
kubectl describe pod <pod-name>
# Check: events, conditions
# Common causes:
# - Insufficient resources (CPU/Memory)
# - No node match (nodeSelector, affinity)
# - Taints/Tolerations
```

**Scenario 2: Pod CrashLoopBackOff**
```bash
kubectl logs <pod-name> --previous  # Logs của lần trước
kubectl describe pod <pod-name>
# Check: container status, exit code
```

**Scenario 3: Service không có endpoints**
```bash
kubectl get endpoints <service-name>
# Nếu empty:
kubectl get pods --show-labels
kubectl describe svc <service-name>
# Check: selector labels match với pod labels?
```

**Scenario 4: NodePort không accessible**
```bash
# Check service:
kubectl get svc <service-name>
# Check firewall (nếu có)
# Test từ node:
kubectl run curl-test --image=curlimages/curl -it --rm -- \
  curl <node-ip>:<nodePort>
```

---

## 🎯 Challenge Exercises

### Challenge 1: Rolling Update
1. Tạo deployment với replicas=3, image: curlimages/curl:latest
2. Update image version sang curlimages/curl:8.5.0
3. Xem rollout status
4. Rollback về version cũ
5. Xem rollout history

### Challenge 2: Scale and Autoscale (cần metrics-server)
```bash
# Install metrics-server
minikube addons enable metrics-server

# Autoscale deployment
kubectl autoscale deployment curl-app-deployment --cpu-percent=10 --min=1 --max=5

# Generate load (trong pod):
kubectl exec -it <pod-name> -- sh -c "while true; do echo load; done"

# Watch hpa
kubectl get hpa -w
```

### Challenge 3: Labels Filtering
1. Thêm labels: `team=devops`, `project=demo`, `env=dev` vào pods
2. Filter pods: `kubectl get pods -l team=devops`
3. Filter pods: `kubectl get pods -l 'env=dev,project=demo'`
4. Filter pods NOT in label: `kubectl get pods -l 'env!=prod'`

### Challenge 4: Node Affinity
1. Label node: `kubectl label node minikube disktype=ssd`
2. Chỉnh pod spec với nodeSelector:
   ```yaml
   spec:
     nodeSelector:
       disktype: ssd
   ```
3. Delete pod và xem pod mới schedule lên node nào

---

## 📝 Lab Report Template

Sau mỗi lab, ghi lại:

```
Lab 1: Cluster Inspection
=========================
1. Node name: ___________
2. Node OS: ___________
3. Node CPU: ___________
4. Node Memory: ___________
5. Node labels: ___________

Lab 2: Deployment & ReplicaSet
=============================
1. Deployment name: ___________
2. ReplicaSet name: ___________
3. Number of replicas: ___________
4. Pods names: ___________
5. Pod IPs: ___________

Lab 3: Labels & Selectors
=========================
1. Pod labels: ___________
2. Service selector: ___________
3. Endpoints IPs: ___________
4. When label mismatch: ___________

[... Continue for other labs ...]
```

---

**🎓 Tips:**
- Luôn dùng `kubectl get <resource> -o wide` để xem thêm info
- Dùng `kubectl describe <resource> <name>` khi gặp vấn đề
- Dùng `kubectl get events` để xem recent events
- Labels/Selectors là core concept - nắm vững!

Happy Lab! 🧪
