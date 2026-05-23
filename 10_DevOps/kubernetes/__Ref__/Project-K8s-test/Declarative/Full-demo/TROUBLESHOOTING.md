# 🐛 Troubleshooting Guide

## Quick Diagnostic Checklist

```bash
# 1. Check everything
kubectl get all

# 2. Check pods status
kubectl get pods
kubectl get pods -o wide

# 3. Check events
kubectl get events --sort-by='.lastTimestamp'

# 4. Check specific resource
kubectl describe <resource> <name>
```

---

## Common Issues & Solutions

### 1. Pod stuck in Pending

**Symptoms:**
```bash
kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
curl-app-xxxxx-xxxxx    0/1     Pending   0          2m
```

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
# Look for: Events section
# Common messages:
# - Insufficient cpu/memory
# - node(s) didn't match pod's node selector/affinity
# - didn't match pod's node affinity/selector
# - had taints that the pod didn't tolerate
```

**Solutions:**
```bash
# a) Check node resources
kubectl top nodes
kubectl describe node <node-name> | grep -A 10 "Allocated resources"

# b) If insufficient resources:
# - Scale down replicas
kubectl scale deployment <name> --replicas=1

# - Or increase node resources (minikube start --cpus=4 --memory=8192)

# c) Check taints on node
kubectl describe node <node-name> | grep Taint
# If node has taint, pod needs matching toleration

# d) Check pod's nodeSelector
kubectl get pod <pod-name> -o yaml | grep nodeSelector -A 5
```

---

### 2. Pod CrashLoopBackOff

**Symptoms:**
```bash
kubectl get pods
NAME                     READY   STATUS             RESTARTS   AGE
curl-app-xxxxx-xxxxx    0/1     CrashLoopBackOff   5          10m
```

**Diagnosis:**
```bash
# a) Check logs
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Logs từ lần trước

# b) Check container status
kubectl describe pod <pod-name>
# Look for:
# - Last State: Exit Code
# - State: Waiting (Reason)
# - Events
```

**Common Causes:**
- Image không tồn tại (pull error)
- Command/Args sai
- Missing environment variables
- Port đã bị chiếm bởi container khác
- Permission errors
- Health check failing

**Solutions:**
```bash
# a) Check image exists
kubectl get pods <pod-name> -o jsonpath='{.spec.containers[0].image}'

# b) Test image locally (minikube ssh)
minikube ssh
docker pull <image>
docker run -it --rm <image> <command>

# c) Remove livenessProbe/readinessProbe temporarily
# Edit deployment:
kubectl edit deployment <name>
# Comment out probes, apply, check if pod runs

# d) Add environment variables if missing
kubectl set env deployment/<name> KEY=VALUE
```

---

### 3. Service has no endpoints

**Symptoms:**
```bash
kubectl get endpoints <service-name>
NAME               ENDPOINTS   AGE
curl-app-service   <none>      10m
```

**Diagnosis:**
```bash
# a) Check service selector
kubectl get svc <service-name> -o yaml
# spec.selector phải khớp với pod labels

# b) Check pod labels
kubectl get pods --show-labels

# c) Verify selector matches
# Service selector: app=curl-app
# Pod labels: app=curl-app ✅
# Nếu không match → không có endpoints
```

**Solutions:**
```bash
# a) Update pod labels to match service selector
kubectl label pod <pod-name> app=curl-app --overwrite

# b) Or update service selector
kubectl edit svc <service-name>
# Change spec.selector to match pod labels

# c) Verify fix
kubectl get endpoints <service-name>
```

---

### 4. NodePort not accessible from outside

**Symptoms:**
```bash
curl http://$(minikube ip):30007
# Connection refused / timeout
```

**Diagnosis:**
```bash
# a) Check service is NodePort
kubectl get svc <service-name>
# TYPE phải là NodePort

# b) Check nodePort range (default 30000-32767)
kubectl get svc <service-name> -o yaml | grep nodePort

# c) Check service port mappings
kubectl describe svc <service-name>

# d) Test from within cluster
kubectl run curl-test --image=curlimages/curl -it --rm -- \
  curl <service-name>:<port>
```

**Solutions:**
```bash
# a) Minikube specific: check minikube ip
minikube ip
# Use that IP, not localhost

# b) If using Docker driver on Linux, need to expose minikube:
# Minikube Docker driver uses a VM network
# Use `minikube tunnel` for LoadBalancer services
# NodePort should work directly with minikube ip

# c) Check firewall (unlikely on minikube)
# On Linux host:
sudo ufw status

# d) Alternative: use port-forward
kubectl port-forward svc/<service-name> 8080:8080
# Then: curl http://localhost:8080
```

---

### 5. DNS Resolution Issues

**Symptoms:**
```bash
kubectl exec -it <pod-name> -- nslookup kubernetes.default
# Server failure
```

**Diagnosis:**
```bash
# a) Check CoreDNS pods
kubectl get pods -n kube-system
# Look for: coredns-xxxxx

# b) Check CoreDNS logs
kubectl logs -n kube-system <coredns-pod>

# c) Check pod's /etc/resolv.conf
kubectl exec -it <pod-name> -- cat /etc/resolv.conf
```

**Solutions:**
```bash
# a) Minikube: enable DNS addon
minikube addons enable coredns

# b) Restart CoreDNS
kubectl rollout restart deployment/coredns -n kube-system

# c) Check kubelet config
minikube ssh
cat /var/lib/kubelet/config.yaml | grep -A 5 clusterDNS
```

---

### 6. ImagePullBackOff

**Symptoms:**
```bash
kubectl get pods
NAME                     READY   STATUS                  RESTARTS   AGE
curl-app-xxxxx-xxxxx    0/1     ImagePullBackOff        0          5m
```

**Diagnosis:**
```bash
# a) Check image name
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].image}'

# b) Check events
kubectl describe pod <pod-name> | grep -A 5 "Events"

# c) Common errors:
# - Repository does not exist or no pull access
# - Image tag not found
# - Image digest not found
```

**Solutions:**
```bash
# a) Use valid image
# - curlimages/curl:latest ✅
# - curlimages/curl:8.5.0 ✅
# - myimage/curl:latest ❌ (if not in DockerHub)

# b) For private registry:
# 1. Create secret:
kubectl create secret docker-registry regcred \
  --docker-server=<registry-server> \
  --docker-username=<username> \
  --docker-password=<password>

# 2. Add imagePullSecrets to pod spec:
spec:
  imagePullSecrets:
  - name: regcred

# c) For minikube local images:
# Build image inside minikube's docker daemon:
eval $(minikube docker-env)
docker build -t myapp:latest .
eval $(minikube docker-env -u)
# Now use image: myapp:latest (no pull needed)
```

---

### 7. Resource Quota Exceeded

**Symptoms:**
```bash
kubectl get pods
# pods stuck in Pending
kubectl describe pod <pod-name>
# Events: "exceeded quota: <quota-name>"
```

**Diagnosis:**
```bash
# a) Check resource quota
kubectl get resourcequota -n <namespace>

# b) Check current usage
kubectl describe resourcequota <quota-name> -n <namespace>
```

**Solutions:**
```bash
# a) Delete unused resources
kubectl delete pod --all
kubectl delete svc --all

# b) Request smaller resources in pod spec:
resources:
  requests:
    memory: "64Mi"    # Reduce from 128Mi
    cpu: "100m"       # Reduce from 250m

# c) Increase quota (if cluster admin)
kubectl edit resourcequota <quota-name> -n <namespace>
```

---

### 8. Can't exec into pod

**Symptoms:**
```bash
kubectl exec -it <pod-name> -- sh
# Error: exec: "sh": executable file not found in $PATH
```

**Diagnosis:**
```bash
# a) Check container image
kubectl get pod <pod-name> -o jsonpath='{.spec.containers[0].image}'

# b) Check available shells
# curlimages/curl có /bin/sh ✅
# Alpine images có /bin/sh ✅
# Ubuntu/Debian có /bin/bash ✅
# Some minimal images may not have shell
```

**Solutions:**
```bash
# a) Use correct shell
kubectl exec -it <pod-name> -- /bin/bash  # nếu có bash
kubectl exec -it <pod-name> -- /bin/sh     # nếu có sh

# b) For images without shell (scratch, distroless):
# Can't exec. Need to rebuild image with shell.
# Or use: kubectl logs để xem logs
```

---

### 9. Storage issues (PersistentVolume)

**Symptoms:**
```bash
kubectl get pvc
# STATUS: Pending
```

**Diagnosis:**
```bash
kubectl describe pvc <pvc-name>
# Look for:
# - Mật khẩu
# - Volume binding mode
# - Storage class
```

**Solutions:**
```bash
# For minikube, enable default storage class:
minikube addons enable storage-provisioner

# Or create hostPath PV (for learning):
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: demo-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
  - ReadWriteOnce
  hostPath:
    path: /tmp/data
EOF
```

---

## Debugging Commands Cheatsheet

```bash
# General
kubectl get all --all-namespaces
kubectl get events --sort-by='.lastTimestamp'

# Pods
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <name>
kubectl logs <name> --previous
kubectl logs -f <name>  # Follow logs
kubectl exec -it <name> -- sh

# Deployments
kubectl get deployments
kubectl describe deployment <name>
kubectl rollout status deployment/<name>
kubectl rollout history deployment/<name>

# Services
kubectl get svc
kubectl describe svc <name>
kubectl get endpoints <name>

# Nodes
kubectl get nodes -o wide
kubectl describe node <name>
kubectl top node

# Namespace
kubectl get ns
kubectl get all -n <namespace>

# YAML dump
kubectl get <resource> <name> -o yaml
kubectl get <resource> <name> -o json

# Port forwarding
kubectl port-forward pod/<name> 8080:80
kubectl port-forward svc/<name> 8080:8080

# Delete stuck pod (force)
kubectl delete pod <name> --force --grace-period=0
```

---

## When All Else Fails

1. **Restart pod:**
   ```bash
   kubectl delete pod <pod-name>
   # ReplicaSet sẽ tạo pod mới
   ```

2. **Restart deployment:**
   ```bash
   kubectl rollout restart deployment/<name>
   ```

3. **Stop & start minikube:**
   ```bash
   minikube stop
   minikube start
   ```

4. **Delete & recreate cluster:**
   ```bash
   minikube delete
   minikube start
   ```

5. **Check minikube logs:**
   ```bash
   minikube logs
   ```

---

## Need Help?

- Kubernetes docs: https://kubernetes.io/docs/tasks/debug/
- `kubectl --help`
- `kubectl <command> --help`
- Minikube docs: https://minikube.sigs.k8s.io/docs/troubleshooting/

---

**Remember: `kubectl describe` và `kubectl logs` là your best friends!** 🐛🔧
