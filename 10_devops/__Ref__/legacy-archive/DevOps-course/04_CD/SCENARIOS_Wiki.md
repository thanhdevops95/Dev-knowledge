# 🚨 MODULE 04: SCENARIOS - Kubernetes Issues

## Scenario 1: CrashLoopBackOff

### 🚨 Bối cảnh

```bash
kubectl get pods
# NAME                      READY   STATUS             RESTARTS
# counter-7d9f8-abc12       0/1     CrashLoopBackOff   5
```

### 🕵️ Điều tra

```bash
kubectl logs counter-7d9f8-abc12
# Error: Redis connection failed

kubectl describe pod counter-7d9f8-abc12
# Events: Back-off restarting failed container
```

### 💡 Giải pháp

**Nguyên nhân:** Redis service chưa deploy

```yaml
# Deploy Redis
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
```

### 🧠 Bài học

- Check logs first: `kubectl logs`
- Use `describe` for events
- Deploy dependencies before app

---

## Scenario 2: Service Không Accessible

### 🚨 Bối cảnh

Service deployed nhưng không access được từ browser.

### 🕵️ Điều tra

```bash
kubectl get svc
# TYPE: ClusterIP  ← Internal only!
```

### 💡 Giải pháp

**Change to LoadBalancer:**

```yaml
spec:
  type: LoadBalancer  # hoặc NodePort
```

**For minikube:**

```bash
minikube service counter-service --url
```

### 🧠 Bài học

- ClusterIP = internal only
- LoadBalancer = external access
- Use `minikube service` for local

---

## Scenario 3: Rolling Update Failed

### 🚨 Bối cảnh

Deployment update → Pods không start, stuck ở "Pending".

### 🕵️ Điều tra

```bash
kubectl describe pod counter-abc
# Events: 0/1 nodes available: insufficient memory
```

### 💡 Giải pháp

**1. Rollback immediately:**

```bash
kubectl rollout undo deployment/counter
```

**2. Fix resource limits:**

```yaml
spec:
  containers:
  - name: web
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 🧠 Bài học

- Always set resource limits
- Monitor rollout status
- Rollback quickly if failed

---

## Scenario 4: OOM (Out of Memory) Kills

### 🚨 Bối cảnh

Pods restart frequently:

```bash
kubectl get pods
# RESTARTS: 12 (mỗi lần OOM killed)
```

### 🕵️ Điều tra

```bash
kubectl describe pod counter-abc
# Reason: OOMKilled
```

### 💡 Giải pháp

**Increase memory limit:**

```yaml
resources:
  limits:
    memory: "256Mi"  # Tăng từ 128Mi
```

**Or optimize app** (fix memory leaks)

### 🧠 Bài học

- Monitor resource usage
- Set appropriate limits
- Optimize app if OOM persists

---

## Scenario 5: ArgoCD Sync Stuck "Progressing"

### 🚨 Bối cảnh

ArgoCD UI shows "Progressing" forever.

### 🕵️ Điều tra

```bash
kubectl get app -n argocd
# SYNC STATUS: Progressing (5 minutes)

argocd app get counter --refresh
# Shows: Deployment waiting for replicas
```

### 💡 Giải pháp

**Check underlying issue:**

```bash
kubectl get pods -n counter-namespace
# → Pods in ImagePullBackOff (wrong image)
```

**Fix deployment YAML:**

```yaml
image: correct-registry/counter-app:v2.0
```

**Force sync:**

```bash
argocd app sync counter --force
```

### 🧠 Bài học

- ArgoCD shows K8s state
- Fix K8s issue, not ArgoCD
- Use `--force` for stuck syncs

---

## 🎯 Tổng kết Module 04

| Scenario | Vấn đề | Giải pháp |
|----------|--------|-----------|
| 1 | CrashLoopBackOff | Check logs + Fix dependencies |
| 2 | Service inaccessible | Use LoadBalancer/NodePort |
| 3 | Rolling update failed | Rollback + Fix resources |
| 4 | OOM kills | Increase memory limits |
| 5 | ArgoCD stuck | Fix underlying K8s issue |

✅ **Next:** Module 05 - OPERATE!
