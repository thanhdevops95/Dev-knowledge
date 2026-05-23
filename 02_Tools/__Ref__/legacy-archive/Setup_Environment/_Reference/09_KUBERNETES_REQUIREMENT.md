# Module 09: KUBERNETES

> **"Kubernetes là bến cảng container - quản lý hàng nghìn containers như một"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu Kubernetes architecture
- ✅ Deploy applications lên K8s
- ✅ Quản lý Pods, Deployments, Services
- ✅ ConfigMaps và Secrets
- ✅ Persistent storage
- ✅ K8s Networking (Ingress, NetworkPolicy)
- ✅ Helm charts
- ✅ K8s RBAC
- ✅ Troubleshooting K8s

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| K8s | Kubernetes | K-8 chữ-s, viết tắt Kubernetes |
| Cluster | Cluster | Cụm servers chạy K8s |
| Node | Node | Server trong cluster |
| Master | Control Plane | Thành phần điều khiển |
| Worker | Worker Node | Node chạy workloads |
| Pod | Pod | Đơn vị nhỏ nhất, 1+ containers |
| Deployment | Deployment | Quản lý Pod replicas |
| Service | Service | Expose Pods ra network |
| Ingress | Ingress | HTTP load balancer |
| ConfigMap | ConfigMap | Lưu config không nhạy cảm |
| Secret | Secret | Lưu data nhạy cảm |
| PV | Persistent Volume | Storage resource |
| PVC | Persistent Volume Claim | Yêu cầu storage |
| Namespace | Namespace | Phân vùng logic cluster |
| Label | Label | Tag để filter resources |
| Selector | Selector | Chọn resources theo label |
| ReplicaSet | ReplicaSet | Duy trì số lượng Pods |
| StatefulSet | StatefulSet | Cho stateful apps |
| DaemonSet | DaemonSet | Chạy Pod trên mọi Node |
| Job | Job | Chạy task một lần |
| CronJob | CronJob | Chạy task định kỳ |
| Helm | Helm | Package manager cho K8s |
| Chart | Helm Chart | Package K8s manifests |
| kubectl | kubectl | CLI tool cho K8s |

---

## ✅ Checklist Labs

### Labs Setup & Basics

- [ ] Lab 1: Install kubectl
- [ ] Lab 2: Setup local cluster (minikube/kind/k3d)
- [ ] Lab 3: kubectl config và contexts
- [ ] Lab 4: kubectl get, describe, logs
- [ ] Lab 5: kubectl explain
- [ ] Lab 6: kubectl apply vs create

### Labs Pods

- [ ] Lab 7: Create Pod từ CLI
- [ ] Lab 8: Create Pod từ YAML
- [ ] Lab 9: Multi-container Pod
- [ ] Lab 10: Init containers
- [ ] Lab 11: Pod lifecycle
- [ ] Lab 12: Pod resource requests và limits
- [ ] Lab 13: Liveness và Readiness probes
- [ ] Lab 14: Pod logs và exec

### Labs Deployments

- [ ] Lab 15: Create Deployment
- [ ] Lab 16: Scale Deployment
- [ ] Lab 17: Rolling update
- [ ] Lab 18: Rollback deployment
- [ ] Lab 19: Deployment strategies
- [ ] Lab 20: Revision history

### Labs Services

- [ ] Lab 21: ClusterIP Service
- [ ] Lab 22: NodePort Service
- [ ] Lab 23: LoadBalancer Service
- [ ] Lab 24: ExternalName Service
- [ ] Lab 25: Headless Service
- [ ] Lab 26: Service endpoints

### Labs ConfigMaps & Secrets

- [ ] Lab 27: Create ConfigMap từ literal
- [ ] Lab 28: Create ConfigMap từ file
- [ ] Lab 29: Use ConfigMap as env vars
- [ ] Lab 30: Use ConfigMap as volume
- [ ] Lab 31: Create Secret
- [ ] Lab 32: Use Secret as env vars
- [ ] Lab 33: Use Secret as volume
- [ ] Lab 34: Image pull secrets

### Labs Storage

- [ ] Lab 35: EmptyDir volume
- [ ] Lab 36: HostPath volume
- [ ] Lab 37: PersistentVolume creation
- [ ] Lab 38: PersistentVolumeClaim
- [ ] Lab 39: Storage classes
- [ ] Lab 40: Dynamic provisioning

### Labs Networking

- [ ] Lab 41: Pod-to-Pod networking
- [ ] Lab 42: Service DNS
- [ ] Lab 43: Ingress controller setup
- [ ] Lab 44: Ingress rules
- [ ] Lab 45: TLS termination
- [ ] Lab 46: NetworkPolicy basics
- [ ] Lab 47: Ingress annotations

### Labs Namespaces & RBAC

- [ ] Lab 48: Create Namespaces
- [ ] Lab 49: Resource quotas
- [ ] Lab 50: Limit ranges
- [ ] Lab 51: ServiceAccount
- [ ] Lab 52: Role và RoleBinding
- [ ] Lab 53: ClusterRole và ClusterRoleBinding

### Labs Helm

- [ ] Lab 54: Helm install
- [ ] Lab 55: helm search, repo add
- [ ] Lab 56: helm install, upgrade, rollback
- [ ] Lab 57: helm values
- [ ] Lab 58: Create Helm chart
- [ ] Lab 59: Chart templates
- [ ] Lab 60: Chart dependencies

### Labs Advanced

- [ ] Lab 61: StatefulSet
- [ ] Lab 62: DaemonSet
- [ ] Lab 63: Job
- [ ] Lab 64: CronJob
- [ ] Lab 65: Horizontal Pod Autoscaler

### Labs Counter App on K8s

- [ ] Lab 66: Deploy Counter App
- [ ] Lab 67: Counter App with ConfigMap
- [ ] Lab 68: Counter App with Secrets
- [ ] Lab 69: Counter App with Ingress
- [ ] Lab 70: Counter App Helm chart

### Labs Troubleshooting

- [ ] Lab 71: Debug pending pods
- [ ] Lab 72: Debug crashloopbackoff
- [ ] Lab 73: Debug service không accessible
- [ ] Lab 74: kubectl debug
- [ ] Lab 75: Resource monitoring

---

## 🚨 Checklist Scenarios

### Scenarios về Pods

- [ ] Scenario 1: Pod stuck in Pending
- [ ] Scenario 2: Pod CrashLoopBackOff
- [ ] Scenario 3: Pod ImagePullBackOff
- [ ] Scenario 4: Pod OOMKilled
- [ ] Scenario 5: Pod evicted
- [ ] Scenario 6: Init container fails

### Scenarios về Deployments

- [ ] Scenario 7: Rolling update stuck
- [ ] Scenario 8: Rollback cần thiết
- [ ] Scenario 9: Replicas không đủ
- [ ] Scenario 10: Deployment not progressing

### Scenarios về Services

- [ ] Scenario 11: Service không route traffic
- [ ] Scenario 12: Endpoints empty
- [ ] Scenario 13: NodePort không accessible
- [ ] Scenario 14: Load balancer pending

### Scenarios về Storage

- [ ] Scenario 15: PVC pending
- [ ] Scenario 16: Storage class not found
- [ ] Scenario 17: Volume mount fails
- [ ] Scenario 18: Data persistence issue

### Scenarios về Networking

- [ ] Scenario 19: DNS resolution fails
- [ ] Scenario 20: Ingress không route
- [ ] Scenario 21: NetworkPolicy block traffic
- [ ] Scenario 22: External traffic không vào được

### Scenarios về Config

- [ ] Scenario 23: ConfigMap update không reflect
- [ ] Scenario 24: Secret không decode được
- [ ] Scenario 25: Environment variable missing

### Scenarios về Resources

- [ ] Scenario 26: Resource quota exceeded
- [ ] Scenario 27: CPU throttling
- [ ] Scenario 28: Node not ready
- [ ] Scenario 29: Cluster autoscaler issues

### Scenarios về Security

- [ ] Scenario 30: RBAC permission denied
- [ ] Scenario 31: ServiceAccount không có quyền
- [ ] Scenario 32: Pod security policy violation
- [ ] Scenario 33: Secret exposure

### Scenarios về Helm

- [ ] Scenario 34: Helm release stuck
- [ ] Scenario 35: Chart values override không work
- [ ] Scenario 36: Helm rollback issues

---

## ⏱️ Thời lượng

**Ước tính:** 10-12 giờ

| Phần | Thời gian |
|------|-----------|
| Setup & Pods (Labs 1-14) | 2 giờ |
| Deployments & Services (Labs 15-26) | 2 giờ |
| ConfigMaps, Secrets, Storage (Labs 27-40) | 2 giờ |
| Networking & RBAC (Labs 41-53) | 2 giờ |
| Helm (Labs 54-60) | 1.5 giờ |
| Advanced & Counter App (Labs 61-75) | 2 giờ |
| Scenarios | 1.5 giờ |

---

## 🔗 Tài liệu tham khảo

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)
- [Helm Documentation](https://helm.sh/docs/)
- [Learn Kubernetes Basics (Interactive)](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
