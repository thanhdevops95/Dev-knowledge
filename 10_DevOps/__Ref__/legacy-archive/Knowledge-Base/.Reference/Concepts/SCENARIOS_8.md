# 🚨 Tình huống Thực chiến - Kubernetes

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi vận hành Kubernetes.

---

## Scenario 1: Pod CrashLoopBackOff - Restart vô tận

### 📋 Bối cảnh

Deploy xong, Pods không chạy được. Status hiện **CrashLoopBackOff** và RESTARTS tăng liên tục.

Production đang DOWN!

### 🔍 Triệu chứng

```bash
kubectl get pods
# NAME                   READY   STATUS             RESTARTS      AGE
# myapp-7b9d5f8c-x2k9j   0/1     CrashLoopBackOff   8 (2m ago)    15m
```

### 🕵️ Điều tra

**Bước 1: Xem logs**

```bash
kubectl logs myapp-7b9d5f8c-x2k9j
# Error: Cannot connect to database at db-service:5432
# Connection refused

# Xem logs trước khi crash
kubectl logs myapp-7b9d5f8c-x2k9j --previous
```

**Bước 2: Describe pod**

```bash
kubectl describe pod myapp-7b9d5f8c-x2k9j
# Events:
#   Warning  Unhealthy  Liveness probe failed
#   Normal   Killing    Container failed liveness probe
```

**Bước 3: Check config**

```bash
# Kiểm tra env vars
kubectl get pod myapp-7b9d5f8c-x2k9j -o yaml | grep -A 20 env:
# - name: DATABASE_URL
#   value: postgres://db-service:5432/mydb  ← Có đúng không?
```

### 💡 Giải pháp

**Nguyên nhân thường gặp và cách fix:**

| Nguyên nhân | Cách fix |
|-------------|----------|
| Missing env vars | Kiểm tra ConfigMap/Secret |
| Wrong database host | Fix service name trong config |
| Liveness probe quá aggressive | Tăng `initialDelaySeconds` |
| OOMKilled (hết memory) | Tăng `resources.limits.memory` |
| Image không tồn tại | Fix image tag |

**Fix liveness probe:**

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 60  # Tăng lên nếu app khởi động chậm
  periodSeconds: 10
  failureThreshold: 3
```

**Fix OOMKilled:**

```yaml
resources:
  requests:
    memory: "256Mi"
  limits:
    memory: "512Mi"  # Tăng limit
```

### 🧠 Bài học

- **Logs là friend #1** - Luôn check logs trước
- **Describe cho events** - Thấy lý do K8s kill pod
- **Probe settings quan trọng** - App cần đủ time khởi động
- **Resource limits** - Không set = có thể OOMKilled

---

## Scenario 2: Service không route traffic đến Pods

### 📋 Bối cảnh

Tạo Deployment, Pod chạy OK. Tạo Service để expose. Nhưng gọi Service thì **không có response**.

### 🔍 Triệu chứng

```bash
kubectl get pods
# NAME                   READY   STATUS    RESTARTS   AGE
# myapp-7b9d5f8c-x2k9j   1/1     Running   0          5m  ← Pod OK

kubectl get svc
# NAME        TYPE        CLUSTER-IP     PORT(S)   
# myapp-svc   ClusterIP   10.96.45.123   80/TCP    ← Service OK

# Nhưng curl không response
kubectl run test --image=curlimages/curl --rm -it -- curl myapp-svc
# curl: (7) Failed to connect to myapp-svc port 80
```

### 🕵️ Điều tra

**Bước 1: Check Endpoints**

```bash
kubectl get endpoints myapp-svc
# NAME        ENDPOINTS   AGE
# myapp-svc   <none>      5m  ← KHÔNG CÓ ENDPOINTS!
```

**Bước 2: So sánh selector**

```bash
# Service selector
kubectl get svc myapp-svc -o yaml | grep -A 5 selector
# selector:
#   app: myapp
#   version: v1  ← Yêu cầu cả 2 labels

# Pod labels
kubectl get pods --show-labels
# NAME                   LABELS
# myapp-7b9d5f8c-x2k9j   app=myapp  ← Thiếu version=v1!
```

**Nguyên nhân:** Service selector **không match** Pod labels.

### 💡 Giải pháp

**1. Fix labels trong Deployment:**

```yaml
# deployment.yaml
spec:
  template:
    metadata:
      labels:
        app: myapp
        version: v1  # Thêm label thiếu
```

**2. Hoặc fix selector trong Service:**

```yaml
# service.yaml
spec:
  selector:
    app: myapp  # Chỉ cần label này
```

**Verify:**

```bash
kubectl get endpoints myapp-svc
# NAME        ENDPOINTS         AGE
# myapp-svc   10.244.1.5:8080   1m  ← Có endpoints!
```

### 🧠 Bài học

- **Endpoints = nơi traffic thực sự đến** - Nếu empty = selector sai
- **Labels phải EXACT match** - Không phải partial match
- **Debug: Service → Endpoints → Pod** - Follow the chain

---

## Scenario 3: Deployment stuck - Pods không schedule được

### 📋 Bối cảnh

Apply deployment mới, nhưng Pods stuck ở **Pending** mãi không chạy.

### 🔍 Triệu chứng

```bash
kubectl get pods
# NAME                   READY   STATUS    RESTARTS   AGE
# myapp-7b9d5f8c-x2k9j   0/1     Pending   0          10m  ← Stuck!
```

### 🕵️ Điều tra

```bash
kubectl describe pod myapp-7b9d5f8c-x2k9j
# Events:
#   Warning  FailedScheduling  0/3 nodes are available:
#   - 1 Insufficient cpu
#   - 2 Insufficient memory
#   - 3 node(s) had taints that the pod didn't tolerate
```

**Kiểm tra resources:**

```bash
kubectl top nodes
# NAME    CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# node1   3800m        95%    7168Mi          90%
# node2   3600m        90%    6912Mi          87%
# node3   3900m        97%    7424Mi          93%  ← Tất cả gần full!
```

### 💡 Giải pháp

**1. Giảm resource requests:**

```yaml
resources:
  requests:
    memory: "64Mi"   # Giảm từ 256Mi
    cpu: "100m"      # Giảm từ 500m
```

**2. Scale down pods khác:**

```bash
kubectl scale deployment other-app --replicas=2  # Giảm từ 5
```

**3. Thêm nodes:**

```bash
# Trên cloud provider
kubectl get nodes  # Check số nodes hiện tại
# Scale up node pool
```

**4. Nếu do taints:**

```bash
# Xem taints
kubectl describe nodes | grep Taints
# Taints: dedicated=production:NoSchedule

# Thêm tolerations vào Pod
spec:
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "production"
    effect: "NoSchedule"
```

### 🧠 Bài học

- **Pending = scheduler không tìm được node** - Check resources/taints
- **Resource requests ảnh hưởng scheduling** - Đặt đúng thực tế
- **Node capacity planning** - Monitor trước khi full

---

## Scenario 4: Rolling Update stuck - Deployment không complete

### 📋 Bối cảnh

Update deployment với image mới. Rollout bắt đầu nhưng **stuck** ở giữa. Cả old và new pods đang chạy.

### 🔍 Triệu chứng

```bash
kubectl rollout status deployment/myapp
# Waiting for deployment "myapp" rollout to finish: 
# 2 out of 3 new replicas have been updated...  ← Stuck!

kubectl get pods
# NAME                    READY   STATUS             RESTARTS   AGE
# myapp-old-abc123        1/1     Running            0          1h
# myapp-new-def456        1/1     Running            0          5m
# myapp-new-ghi789        0/1     CrashLoopBackOff   5          5m  ← New pod failing!
```

### 🕵️ Điều tra

```bash
# New pods failing
kubectl logs myapp-new-ghi789
# Error: Missing required environment variable API_KEY

# So sánh env giữa old và new
kubectl get deployment myapp -o yaml | grep -A 30 env
# Phát hiện: New image cần env var mới mà chưa có
```

### 💡 Giải pháp

**1. Rollback ngay (nếu urgent):**

```bash
kubectl rollout undo deployment/myapp
# deployment.apps/myapp rolled back
```

**2. Fix config và redeploy:**

```bash
# Thêm env var còn thiếu
kubectl set env deployment/myapp API_KEY=xxx

# Hoặc edit ConfigMap
kubectl edit configmap myapp-config
```

**3. Kiểm tra rollout hoàn tất:**

```bash
kubectl rollout status deployment/myapp
# deployment "myapp" successfully rolled out
```

### 🧠 Bài học

- **Rollout stuck = new pods không healthy** - Check new pod logs
- **progressDeadlineSeconds** - Đặt timeout cho rollout
- **Rollback là OK** - Đừng ngại undo nếu có vấn đề
- **Test image mới ở staging trước** - Đừng deploy thẳng production

---

## Scenario 5: Secrets bị xóa - Pods crash hàng loạt

### 📋 Bối cảnh

Ai đó chạy `kubectl delete secret db-credentials`. Ngay lập tức, tất cả pods restart và fail.

CRITICAL INCIDENT!

### 🔍 Triệu chứng

```bash
kubectl get pods
# NAME                   READY   STATUS                       RESTARTS
# myapp-abc123           0/1     CreateContainerConfigError   0
# myapp-def456           0/1     CreateContainerConfigError   0
# myapp-ghi789           0/1     CreateContainerConfigError   0

kubectl describe pod myapp-abc123
# Warning  Failed  Error: secret "db-credentials" not found
```

### 🕵️ Điều tra

```bash
# Kiểm tra secret
kubectl get secrets
# db-credentials không còn!

# Ai xóa? Check audit logs (nếu có)
# Hoặc hỏi team
```

### 💡 Giải pháp

**1. Restore secret ngay (nếu biết values):**

```bash
kubectl create secret generic db-credentials \
  --from-literal=username=myuser \
  --from-literal=password=mypassword
```

**2. Restart pods:**

```bash
kubectl rollout restart deployment/myapp
```

**3. Ngăn chặn trong tương lai:**

```yaml
# Đánh dấu secret quan trọng
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  annotations:
    "helm.sh/resource-policy": keep  # Helm không xóa
  finalizers:
  - kubernetes.io/protect  # Cần xóa finalizer trước khi delete
```

**4. RBAC - Giới hạn quyền delete:**

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]  # Không có "delete"!
```

**5. Backup secrets:**

```bash
# Script backup định kỳ
kubectl get secrets -o yaml > secrets-backup.yaml
# Encrypt và lưu an toàn
```

### 🧠 Bài học

- **Secrets là critical** - Một delete có thể down toàn bộ app
- **RBAC cho secrets** - Không phải ai cũng cần quyền delete
- **Backup secrets** - Không chỉ code, cả config quan trọng
- **GitOps** - Secrets nên được quản lý qua code, không manual

---

## 📝 Checklist Khi Có Incident K8s

1. [ ] **Xác định scope** - Pods nào affected?
2. [ ] **Check pod status** - kubectl get pods
3. [ ] **Check logs** - kubectl logs <pod>
4. [ ] **Describe pod** - kubectl describe pod <pod>
5. [ ] **Check events** - kubectl get events --sort-by=.metadata.creationTimestamp
6. [ ] **Check resources** - kubectl top pods/nodes
7. [ ] **Rollback nếu cần** - kubectl rollout undo
8. [ ] **Document incident** - Ghi lại timeline và root cause
