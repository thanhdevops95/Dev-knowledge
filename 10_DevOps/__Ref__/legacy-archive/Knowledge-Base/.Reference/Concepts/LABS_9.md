# Module 10: CD Labs

---

## 🔧 Lab 1: Rolling Update

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  template:
    spec:
      containers:
        - name: app
          image: nginx:1.24
```

```bash
kubectl apply -f deployment.yaml
kubectl set image deployment/myapp app=nginx:1.25
kubectl rollout status deployment/myapp
```

---

## 🔧 Lab 2: Rollback

```bash
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2
```

---

## 🔧 Lab 3: Blue-Green với Selector

```yaml
# blue-green.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Switch to green when ready
  ports:
    - port: 80
```

```bash
# Switch traffic
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
```

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Rolling updates |
| 2 | Rollbacks |
| 3 | Blue-Green |

👉 **[SCENARIOS.md](SCENARIOS.md)**
