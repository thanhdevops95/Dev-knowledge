# 🎓 Namespaces & RBAC — Multi-tenancy + Permission

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [ConfigMaps & Secrets](03_configmaps-and-secrets.md)

> 🎯 *Master **Namespaces** (multi-tenancy), **ResourceQuota** + **LimitRange**, **RBAC** (ClusterRole/Role/Bindings + ServiceAccount), **kubectl auth can-i**, common production patterns (env separation, team isolation). Sau bài này set up multi-environment cluster + control access đúng cách.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Namespace** — isolation + organization
- [ ] Setup **ResourceQuota** + **LimitRange** per namespace
- [ ] **RBAC** — 4 concepts: Role, ClusterRole, RoleBinding, ClusterRoleBinding
- [ ] **ServiceAccount** for pod identity
- [ ] **kubectl auth can-i** check permissions
- [ ] Patterns: env separation (dev/staging/prod), team isolation
- [ ] Hiểu **default ServiceAccount** + token automount
- [ ] Glance **OPA Gatekeeper / Kyverno** policy enforcement

---

## Tình huống — Bạn share cluster cho 3 team

Bạn có K8s cluster. Giờ 3 teams cần share:
- Team A (backend) — deploy FastAPI services.
- Team B (frontend) — deploy React + static sites.
- Team C (data) — deploy ML batch jobs.

Cần:
- 🔒 Mỗi team **chỉ thấy** resource của mình.
- 💰 Mỗi team **CPU/RAM quota** riêng.
- 👤 Dev team không thể `kubectl delete node`.
- 🤖 CI/CD bot chỉ `apply` được, không `exec` pods.

Bạn ngơ:
- **Namespace** là gì? Chia thế nào?
- **RBAC** = Role + Binding... quá nhiều object.
- **ServiceAccount** + **User** khác sao?

Senior:
> *"Namespace = isolation logical. RBAC = ai làm gì ở đâu. Plus quota để team A không hog cả cluster. Lập 1 lần, dùng năm này qua năm khác."*

→ Bài này dạy đầy đủ.

---

## 1️⃣ Namespaces — Logical isolation

**Namespace** giống như "folder ảo" trong cluster — group resource lại để dễ quản lý. Sau khi install, K8s đã có sẵn 4 namespace mặc định: `default` (Pod không khai báo namespace nằm đây), `kube-system` (component K8s), `kube-public` (info public), `kube-node-lease` (heartbeat node):

```bash
# Default 4 namespaces sau install K8s
kubectl get namespaces
# NAME              STATUS
# default            Active     ← Pods không khai báo ns vào đây
# kube-system        Active     ← Core K8s components (kubelet's friends)
# kube-public        Active     ← Public read by all
# kube-node-lease    Active     ← Node heartbeats
```

### Create

Tạo namespace bằng `kubectl create namespace` (nhanh) hoặc YAML manifest (versionable trong Git). Production thường có 3 namespace cơ bản: `production`, `staging`, `dev` — tách rõ môi trường. Khi cần thêm metadata (label team, environment) → dùng YAML:

```bash
kubectl create namespace production
kubectl create namespace staging
kubectl create namespace dev

# YAML
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  labels:
    team: backend
    env: production
```

### Use

Mặc định `kubectl` thao tác trên namespace `default`. Để target namespace khác, thêm flag `-n <namespace>` vào mọi lệnh — hoặc set context default 1 lần để khỏi gõ đi gõ lại. Service cross-namespace gọi nhau qua DNS đầy đủ dạng `<svc>.<ns>.svc.cluster.local`:

```bash
# Specify namespace in commands
kubectl get pods -n production
kubectl apply -f app.yaml -n staging
kubectl logs -n production fastapi-xxx

# Set context default namespace
kubectl config set-context --current --namespace=production

# Cross-namespace ref (DNS)
# In default namespace, fetch postgres in production
http://postgres.production.svc.cluster.local
```

### What's namespaced vs cluster-scoped?

Không phải tất cả object K8s thuộc về 1 namespace — có 2 nhóm. **Namespaced** = object riêng cho từng namespace (Pod, Deployment, Service...). **Cluster-scoped** = object toàn cluster, không thuộc namespace nào (Node, PersistentVolume, ClusterRole...). Phân biệt quan trọng khi viết RBAC và kế hoạch multi-tenant:

| Namespaced | Cluster-scoped |
|---|---|
| Pod, Deployment, ReplicaSet | Node |
| Service, Ingress, ConfigMap, Secret | PersistentVolume |
| Role, RoleBinding, ServiceAccount | ClusterRole, ClusterRoleBinding |
| Job, CronJob | Namespace |
| NetworkPolicy, ResourceQuota | StorageClass, IngressClass |
| Most workload objects | CustomResourceDefinition |

```bash
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```

### Common patterns

**Pattern 1: Per environment**
```
production/
staging/
development/
```

**Pattern 2: Per team**
```
team-frontend/
team-backend/
team-data/
```

**Pattern 3: Per tenant (SaaS)**
```
tenant-customer-1/
tenant-customer-2/
```

**Pattern 4: Per application + env**
```
shop-production/
shop-staging/
analytics-production/
```

→ Choose based on:
- Small team → per env.
- Multi-team → per team.
- SaaS → per tenant.

### Limit Namespaces ≠ Replace Clusters

Đây là **misconception** lớn: nhiều người tin namespace = isolation thật sự như VM riêng. **Sai**. Namespace chỉ là *logical boundary*, không phải security boundary. Pod ở namespace A vẫn share kernel với Pod namespace B, mạng vẫn thông nhau nếu không có NetworkPolicy:

- ✅ Logical isolation, RBAC, quotas.
- ❌ **NOT** security boundary (kernel shared, no isolation Pod → node).
- ❌ **NOT** network isolation by default (need NetworkPolicy).

→ **Hard isolation** (PCI compliance, untrusted code) → separate **clusters**.

---

## 2️⃣ ResourceQuota — Limit total per namespace

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
    services: "10"
    persistentvolumeclaims: "5"
    services.loadbalancers: "2"
    configmaps: "20"
    secrets: "20"
```

```bash
kubectl apply -f quota.yaml
kubectl describe quota -n team-a
# Used / Hard
# 5     / 50      pods
# 3.5   / 10       requests.cpu
# 8Gi   / 20Gi     requests.memory
```

→ Exceed quota → new resources **rejected**.

```bash
kubectl apply -f new-deployment.yaml
# Error: exceeded quota: team-a-quota, requested: requests.cpu=1, used: requests.cpu=10, limited: requests.cpu=10
```

### Use cases

- 💰 **Cost control** — team A only $X/month CPU.
- 🛡️ **Prevent runaway** — bug in app không cạn cluster.
- 🤝 **Fair share** — multi-tenant.

---

## 3️⃣ LimitRange — Default + max per Pod

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    default:                    # Default if not specified
      cpu: 500m
      memory: 512Mi
    defaultRequest:             # Default requests
      cpu: 100m
      memory: 128Mi
    max:                         # Max allowed
      cpu: "2"
      memory: 4Gi
    min:                         # Min required
      cpu: 50m
      memory: 64Mi
```

→ Container without `resources` → auto-inject `default` + `defaultRequest`. Container declaring > `max` → reject.

### Vs ResourceQuota

| | ResourceQuota | LimitRange |
|---|---|---|
| Scope | Per namespace total | Per Pod/Container |
| Purpose | Cap total team usage | Default + bounds individual |
| Example | "Total RAM ≤ 20Gi" | "1 container ≤ 4Gi" |

→ Both together: ResourceQuota = ceiling. LimitRange = per-container guardrail.

---

## 4️⃣ RBAC — 4 building blocks

K8s **RBAC** (Role-Based Access Control) = 4 objects combined:

```
+----------+         +-----------+
|   USER    |◄──bind──┤  Subject   │
+----------+         +-----------+
                            │
                            ▼ binding
                  +-------------------+
                  |  RoleBinding /     │
                  |  ClusterRoleBinding│
                  +-------------------+
                            │
                            ▼ link to
                  +---------+---------+
                  │                   │
                  ▼                   ▼
          +--------------+   +----------------+
          |  Role         │   │  ClusterRole   │
          | (namespaced)  │   │ (cluster-wide) │
          +--------------+   +----------------+
                  │                   │
                  ▼                   ▼
              [Rules: verbs on resources]
```

### Subjects — Ai

```yaml
# 3 loại
subjects:
- kind: User              # human (vd nguyenvana@acmeshop.vn)
  name: alice
- kind: Group             # group
  name: backend-team
- kind: ServiceAccount    # bot/pod
  name: ci-bot
  namespace: ci
```

### Role — Namespaced permission

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: team-a
rules:
- apiGroups: [""]                                # "" = core API
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
```

### ClusterRole — Cluster-wide permission

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-read
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]
```

### Built-in ClusterRoles

```bash
kubectl get clusterrole
# cluster-admin       superuser, full access
# admin               admin within namespace
# edit                read+write resources (no RBAC manage)
# view                read-only
```

### RoleBinding — Apply Role to Subject

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: alice-pod-reader
  namespace: team-a
subjects:
- kind: User
  name: alice
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRoleBinding — Cluster-wide bind

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: { name: bob-cluster-view }
subjects:
- kind: User
  name: bob
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

### Verbs

```
get      list      watch
create   update    patch    delete
deletecollection
exec     attach    portforward      (action verbs)
```

→ Common patterns:
- Read-only: `["get", "list", "watch"]`.
- Read-write: `["get", "list", "watch", "create", "update", "patch", "delete"]`.

---

## 5️⃣ ServiceAccount — Pod identity

Default Pod tự có `default` ServiceAccount → mount token at `/var/run/secrets/kubernetes.io/serviceaccount/`.

```bash
kubectl exec -it mypod -- cat /var/run/secrets/kubernetes.io/serviceaccount/token
# eyJhbGciOiJSUzI1NiIs...     ← JWT for K8s API auth
```

### Create dedicated SA

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ci-bot
  namespace: ci
```

### Use in Pod

```yaml
spec:
  serviceAccountName: ci-bot
  automountServiceAccountToken: true        # Default true
  containers: ...
```

### Grant permission to SA

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ci-bot-deploy
  namespace: production
subjects:
- kind: ServiceAccount
  name: ci-bot
  namespace: ci                # SA in 'ci' ns
roleRef:
  kind: Role
  name: deployer               # Role in 'production' ns
  apiGroup: rbac.authorization.k8s.io
```

→ CI bot in `ci` ns can deploy to `production` ns. Cross-namespace via SA reference.

### Disable token automount (security)

```yaml
# Pod or ServiceAccount level
spec:
  automountServiceAccountToken: false
```

→ Disable nếu Pod không cần talk K8s API. Less attack surface.

---

## 6️⃣ `kubectl auth can-i` — Check permission

```bash
# Self check
kubectl auth can-i create pods
# yes

kubectl auth can-i delete nodes
# no

kubectl auth can-i create pods --namespace=production
# yes

kubectl auth can-i '*' '*' --all-namespaces
# no (you're not cluster-admin)

# Check for another user (need impersonate permission)
kubectl auth can-i list pods --as=alice
kubectl auth can-i create deployments --as=alice -n team-a

# Service Account
kubectl auth can-i list pods \
  --as=system:serviceaccount:ci:ci-bot \
  -n production
```

→ Debug RBAC: when user say "I can't deploy", check `kubectl auth can-i create deployments --as=user`.

### Show all permissions

```bash
# Check yourself (modern command)
kubectl auth whoami

# What can I do?
kubectl auth can-i --list
kubectl auth can-i --list -n production
```

---

## 7️⃣ Common production patterns

### Pattern 1 — Read-only dashboard

```yaml
# ClusterRole already exists: view
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: { name: devs-view-all }
subjects:
- kind: Group
  name: developers          # OIDC group
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

→ All devs can see (kubectl get) but not modify.

### Pattern 2 — Team owns namespace

```yaml
# Role: full admin in team-a namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: team-a-admin, namespace: team-a }
subjects:
- kind: Group
  name: team-a
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole         # Reference cluster role from namespace binding!
  name: admin
  apiGroup: rbac.authorization.k8s.io
```

→ Team A members admin **only in team-a namespace**.

### Pattern 3 — CI/CD bot deploy

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: deployer, namespace: ci }

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: deployer, namespace: production }
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: deployer, namespace: production }
subjects:
- kind: ServiceAccount
  name: deployer
  namespace: ci
roleRef:
  kind: Role
  name: deployer
  apiGroup: rbac.authorization.k8s.io
```

→ CI bot can update deployments in production, **không thể exec** pods (no exec verb).

### Pattern 4 — Restrict secret access

```yaml
# Default Roles include "get secrets" — restrict it
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: developer, namespace: prod }
rules:
- apiGroups: ["", "apps", "networking.k8s.io"]
  resources: ["*"]
  verbs: ["*"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]      # No create/update/delete
  resourceNames: ["app-config", "app-tls"]  # Only specific secrets
```

→ Devs can view list of secrets in prod, but cannot read sensitive ones unless name match.

---

## 8️⃣ OPA Gatekeeper / Kyverno — Policy enforcement

RBAC = "ai có quyền". **Policy** = "what's allowed at all" (regardless of RBAC).

### Example policies

- ❌ Disallow `:latest` image tag.
- ❌ Require `resources.limits` on every container.
- ❌ Block privileged containers.
- ❌ Block hostNetwork.
- ✅ Require `app=name` label on every Pod.

### Kyverno (recommended 2026)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata: { name: require-resource-limits }
spec:
  validationFailureAction: enforce
  rules:
  - name: check-limits
    match:
      resources: { kinds: [Pod] }
    validate:
      message: "All containers must have resource limits"
      pattern:
        spec:
          containers:
          - resources:
              limits:
                memory: "?*"
                cpu: "?*"
```

→ Apply policy → Pods missing limits get rejected at admission.

### Vs OPA Gatekeeper

| Kyverno | OPA Gatekeeper |
|---|---|
| YAML policies | Rego (DSL) |
| K8s native | General-purpose |
| Easier learning | More powerful |
| 2026 preferred | Established |

---

## 9️⃣ multi-team setup của bạn

### Namespace setup

```bash
kubectl create namespace team-backend
kubectl create namespace team-frontend
kubectl create namespace team-data
kubectl create namespace production
kubectl create namespace ci
```

### Quotas per namespace

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: { name: team-backend-quota, namespace: team-backend }
spec:
  hard:
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "100"
    services.loadbalancers: "5"
```

(Repeat for team-frontend, team-data with different limits)

### RBAC mapping

```
Group         Namespace        Role
backend-team   team-backend    admin
frontend-team  team-frontend   admin
data-team      team-data       admin
all-devs        production     view (read-only prod)
ci-bot (SA)     production     deployer (deployments + RO services)
ops-team        *              cluster-admin
```

### Sample binding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: backend-admin, namespace: team-backend }
subjects:
- kind: Group
  name: backend-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata: { name: all-devs-prod-view }
subjects:
- kind: Group
  name: all-devs
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

### Audit

```bash
# Daily: review who has cluster-admin
kubectl get clusterrolebinding -o json | jq -r '.items[] | select(.roleRef.name == "cluster-admin") | .metadata.name'

# Monthly: review namespaces + quota
kubectl describe quota -A | grep "Used\|Hard"
```

---

## ⚠️ 5 pitfall hay vướng

1. **Forget `-n namespace`** → resources land in `default`. Set context default ns + always specify.
2. **Granting `cluster-admin` casually** → nuclear option. Use built-in `admin` (namespace-scoped) or custom Role.
3. **ResourceQuota nhưng không LimitRange** → Pod without resources.requests reject. Always add LimitRange with defaults.
4. **Namespace ≠ security boundary** → untrusted code share kernel. Real isolation = separate clusters.
5. **Token automount cho mọi Pod** → Pod compromise = K8s API access. `automountServiceAccountToken: false` cho pods không cần.

---

## ✅ Self-check

1. Khác **Role** vs **ClusterRole**?
2. **ResourceQuota** vs **LimitRange** — vai trò mỗi cái?
3. Lệnh **check ai có thể delete pods** ở namespace `prod`?
4. **ServiceAccount** vs **User** — khác sao?
5. **Namespace** đủ cho **untrusted workload** không?

<details>
<summary>Gợi ý đáp án</summary>

1. **Role**: permissions trong **1 namespace** (Pod, Deployment, Secret in ns). **ClusterRole**: cluster-wide (Nodes, PersistentVolumes, CRDs) hoặc namespaced resources across all namespaces. ClusterRole có thể bind qua RoleBinding (limit to 1 ns) hoặc ClusterRoleBinding (cluster-wide).

2. **ResourceQuota**: cap **total** per namespace (e.g., "namespace team-a max 20 CPU total"). **LimitRange**: per-Pod/Container default + max (e.g., "container max 4GB RAM, default 256Mi if not specified"). Together: quota = ceiling, limitrange = per-resource guardrail.

3. ```bash
   kubectl auth can-i delete pods -n prod --as=alice
   ```
   Returns "yes" / "no". Need impersonate permission (or self-check).

4. **User**: human, auth via cert/OIDC/LDAP/static token. K8s không quản — comes from outside (kubeconfig). **ServiceAccount**: K8s native object, for **Pods/bots**. Has auto-mounted JWT token at `/var/run/secrets/...`. SA for in-cluster identity. Human user outside cluster.

5. **KHÔNG**. Namespace = **logical isolation** (RBAC, quota, network policy). Pods share **kernel + node**. Untrusted code (multi-tenant SaaS untrusted code) → kernel exploit = compromise host. Real isolation: **separate clusters** (or **virtual clusters** like vcluster, gVisor sandbox).
</details>

---

## ⚡ Cheatsheet

### Namespace

```bash
kubectl create namespace team-a
kubectl get pods -n team-a
kubectl config set-context --current --namespace=team-a
```

### ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata: { name: q, namespace: ns }
spec:
  hard:
    limits.cpu: "10"
    limits.memory: "20Gi"
    pods: "50"
```

### Role + RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: x, namespace: ns }
rules:
- apiGroups: [""]
  resources: [pods]
  verbs: [get, list, watch]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: x, namespace: ns }
subjects: [{ kind: User, name: alice, apiGroup: rbac.authorization.k8s.io }]
roleRef:
  kind: Role
  name: x
  apiGroup: rbac.authorization.k8s.io
```

### Built-in ClusterRoles

```
cluster-admin   full access
admin           admin in namespace
edit            read+write (no RBAC)
view            read-only
```

### Check auth

```bash
kubectl auth can-i create pods -n prod
kubectl auth can-i --list -n prod
kubectl auth whoami
```

### ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: bot, namespace: ci }

# Use in pod
spec:
  serviceAccountName: bot
  automountServiceAccountToken: false   # for non-K8s pods
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Namespace** | Logical isolation for resources |
| **ResourceQuota** | Cap total resources per namespace |
| **LimitRange** | Default + max per Pod/Container |
| **RBAC** | Role-Based Access Control |
| **Role** | Namespaced permissions |
| **ClusterRole** | Cluster-wide permissions |
| **RoleBinding** | Apply Role to subjects in namespace |
| **ClusterRoleBinding** | Apply ClusterRole cluster-wide |
| **Subject** | User, Group, or ServiceAccount |
| **ServiceAccount** | Pod identity (JWT auto-mount) |
| **Verbs** | get/list/watch/create/update/patch/delete/exec |
| **`kubectl auth can-i`** | Check permission |
| **OPA Gatekeeper / Kyverno** | Policy enforcement (admission webhook) |
| **CRB** | ClusterRoleBinding (shorthand) |

---

## 🔗 Links

### Trong cluster
- ← Trước: [ConfigMaps & Secrets](03_configmaps-and-secrets.md)
- ↑ Cluster: [kubernetes README](../../README.md)

### Cross-reference
- [Linux users & permissions](../../../../04_OS/linux/lessons/02_intermediate/00_users-and-permissions.md) — Unix permission concept
- [FastAPI auth](../../../../07_Web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md) — app-level auth

### External
- 📖 [K8s docs — Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- 📖 [K8s docs — RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- 📖 [K8s docs — ServiceAccount](https://kubernetes.io/docs/concepts/security/service-accounts/)
- 📖 [Kyverno](https://kyverno.io/)
- 📖 [OPA Gatekeeper](https://open-policy-agent.github.io/gatekeeper/)
- 📖 [RBAC Lookup tool](https://github.com/FairwindsOps/rbac-lookup) — debug
- 📖 [vcluster](https://www.vcluster.com/) — virtual K8s cluster

---

> 🎯 *Cluster K8s basic 5/5 đóng. Bạn vận hành multi-team K8s. Bài kế tiếp ngoài cluster: K8s storage (PV/PVC/StatefulSet), GitOps (ArgoCD), service mesh, helm.*

---

## 📜 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §1 Namespaces + Create + Use + namespaced vs cluster-scoped + Limit Namespaces.
- **v1.0.0 (23/05/2026)** — Bản đầu tiên. K8s sprint #5.
