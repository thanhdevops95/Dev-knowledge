# Module 10: CD Scenarios

---

## 🚨 Scenario 1: "Deployment stuck"

```bash
kubectl rollout status deployment/myapp
# Waiting for deployment to finish...

kubectl describe deployment myapp
# Check events for issues
```

---

## 🚨 Scenario 2: "Rollback needed"

```bash
kubectl rollout undo deployment/myapp
kubectl rollout status deployment/myapp
```

---

## 🚨 Scenario 3: "Canary failing"

```bash
# Check canary pods
kubectl get pods -l version=canary

# If failing, delete canary
kubectl delete deployment myapp-canary
```

---

## 📋 CD Troubleshooting

| Issue | Action |
|-------|--------|
| Stuck rollout | Check pod status |
| Bad release | Rollback |
| Canary failing | Delete canary |

👉 **[Module 11: Cloud](../11_CLOUD/README.md)**
