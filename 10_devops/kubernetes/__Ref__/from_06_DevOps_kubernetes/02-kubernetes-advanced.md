# Kubernetes Advanced

> **Tags:** `kubernetes` `k8s` `helm` `rbac` `hpa` `network-policy` `statefulset` `operators`
> **Level:** Advanced | **Prerequisite:** `kubernetes/01-kubernetes-basics.md`

---

## 1. Workload Types

### StatefulSet — Cho Stateful Applications
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless   # Required: headless service
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:16
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
          name: postgres
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  # Each pod gets its own PVC!
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 20Gi

---
# Headless service (no clusterIP — each pod gets DNS record)
apiVersion: v1
kind: Service
metadata:
  name: postgres-headless
spec:
  clusterIP: None    # Headless!
  selector:
    app: postgres
  ports:
  - port: 5432
# DNS: postgres-0.postgres-headless.default.svc.cluster.local
#      postgres-1.postgres-headless.default.svc.cluster.local
```

### DaemonSet — Run on Every Node
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: log-collector
spec:
  selector:
    matchLabels:
      name: log-collector
  template:
    metadata:
      labels:
        name: log-collector
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule   # Also run on master nodes
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### Job & CronJob
```yaml
# Job: run to completion
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3      # Retry on failure
  activeDeadlineSeconds: 600  # Timeout
  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - name: migrate
        image: myapp:latest
        command: ["./migrate", "up"]

---
# CronJob: scheduled
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup
spec:
  schedule: "0 2 * * *"    # Every day at 2 AM
  concurrencyPolicy: Forbid  # Don't start if previous still running
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: cleanup
            image: myapp:latest
            command: ["./cleanup", "--older-than", "30d"]
```

---

## 2. HPA — Horizontal Pod Autoscaler

```yaml
# Basic HPA (CPU-based)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # Target 70% CPU
  - type: Resource
    resource:
      name: memory
      target:
        type: AverageValue
        averageValue: 400Mi
  # Custom metrics (via Prometheus Adapter)
  - type: External
    external:
      metric:
        name: http_requests_per_second
        selector:
          matchLabels:
            service: api
      target:
        type: Value
        value: 1000    # Scale if > 1000 RPS
  # Scale-in/out behavior
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # Don't scale down for 5 min
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60             # Max 10% scale-down per minute
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Pods
        value: 4
        periodSeconds: 60             # Add max 4 pods per minute
```

### VPA — Vertical Pod Autoscaler
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  updatePolicy:
    updateMode: "Auto"   # Off | Initial | Auto
  resourcePolicy:
    containerPolicies:
    - containerName: api
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 2Gi
```

---

## 3. RBAC — Role-Based Access Control

```yaml
# ServiceAccount
apiVersion: v1
kind: ServiceAccount
metadata:
  name: operator-sa
  namespace: myapp

---
# Role (namespace-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: myapp
rules:
- apiGroups: [""]          # "" = core API group
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]

---
# ClusterRole (cluster-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-monitor
rules:
- apiGroups: [""]
  resources: ["nodes", "nodes/stats", "nodes/metrics"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["metrics.k8s.io"]
  resources: ["nodes", "pods"]
  verbs: ["get", "list"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: bind-pod-reader
  namespace: myapp
subjects:
- kind: ServiceAccount
  name: operator-sa
  namespace: myapp
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
- kind: Group
  name: backend-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role    # or ClusterRole
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

```bash
# Check permissions
kubectl auth can-i list pods                           # Current user
kubectl auth can-i list pods --as alice@example.com   # Specific user
kubectl auth can-i list pods --as system:serviceaccount:myapp:operator-sa

# Debug RBAC
kubectl describe rolebinding bind-pod-reader -n myapp
kubectl get clusterrole pod-reader -o yaml
```

---

## 4. Network Policies

```yaml
# Deny all ingress by default (whitelist approach)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: myapp
spec:
  podSelector: {}   # Select ALL pods
  policyTypes:
  - Ingress

---
# Allow only frontend → backend on port 8080
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: myapp
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    - namespaceSelector:    # AND namespace condition
        matchLabels:
          kubernetes.io/metadata.name: myapp
    ports:
    - protocol: TCP
      port: 8080

---
# Allow backend → database
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-backend-to-db
  namespace: myapp
spec:
  podSelector:
    matchLabels:
      app: postgres
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432
```

---

## 5. Resource Management

```yaml
# Requests & Limits
containers:
- name: api
  image: myapp:latest
  resources:
    requests:             # Guaranteed, used for scheduling
      cpu: "250m"         # 250 millicores = 0.25 CPU
      memory: "256Mi"
    limits:               # Hard cap
      cpu: "1000m"        # 1 full CPU
      memory: "512Mi"     # OOMKill if exceeded!

# Quality of Service classes:
# Guaranteed:  requests == limits for all containers
# Burstable:   requests < limits (some containers)
# BestEffort:  no requests/limits (evicted first under pressure)

---
# LimitRange — default limits for namespace
apiVersion: v1
kind: LimitRange
metadata:
  name: defaults
  namespace: myapp
spec:
  limits:
  - type: Container
    default:          # Default limits
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:   # Default requests
      cpu: "100m"
      memory: "128Mi"
    max:              # Maximum allowed
      cpu: "2"
      memory: "2Gi"
    min:              # Minimum required
      cpu: "50m"
      memory: "64Mi"

---
# ResourceQuota — total limits for namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: myapp
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    pods: "50"
    services: "10"
    count/deployments.apps: "20"
    persistentvolumeclaims: "20"
    requests.storage: "500Gi"
```

---

## 6. Helm — Package Manager

```bash
# Install Helm 3
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Common commands
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/postgresql

helm install my-postgres bitnami/postgresql \
  --namespace myapp --create-namespace \
  --set auth.postgresPassword=secretpassword \
  --set primary.persistence.size=20Gi

helm upgrade my-postgres bitnami/postgresql --set replicaCount=3
helm rollback my-postgres 1   # Rollback to revision 1
helm uninstall my-postgres

helm list -A    # All releases in all namespaces
helm status my-postgres
helm history my-postgres
helm get values my-postgres

# Create custom chart
helm create myapp
```

```yaml
# Chart structure:
myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── _helpers.tpl    # Template helpers
│   └── NOTES.txt       # Post-install message
└── charts/             # Sub-charts (dependencies)
```

```yaml
# templates/deployment.yaml — Helm template
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        ports:
        - containerPort: {{ .Values.service.port }}
        {{- if .Values.env }}
        env:
        {{- range .Values.env }}
        - name: {{ .name }}
          value: {{ .value | quote }}
        {{- end }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
```

---

## 7. Probes

```yaml
containers:
- name: api
  livenessProbe:       # Restart if fails
    httpGet:
      path: /health/live
      port: 8080
    initialDelaySeconds: 30  # Wait 30s before first probe
    periodSeconds: 10
    failureThreshold: 3
    
  readinessProbe:      # Remove from Service if fails
    httpGet:
      path: /health/ready
      port: 8080
    initialDelaySeconds: 5
    periodSeconds: 5
    failureThreshold: 3
    
  startupProbe:        # Disable liveness/readiness until startup completes
    httpGet:
      path: /health/startup
      port: 8080
    failureThreshold: 30   # 30 * 10s = 5 minutes to start
    periodSeconds: 10

# Probe types:
# httpGet: HTTP GET → 200-399 = success
# exec: Run command in container → exit 0 = success
# tcpSocket: TCP connection success

# Exec probe example
livenessProbe:
  exec:
    command:
    - /bin/sh
    - -c
    - redis-cli ping | grep PONG
```

---

## 8. Pod Disruption Budget

```yaml
# Ensure minimum availability during voluntary disruptions (upgrades, drain)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
spec:
  minAvailable: 2       # At least 2 pods always running
  # Or:
  # maxUnavailable: 1   # At most 1 pod down at a time
  selector:
    matchLabels:
      app: api
```

---

## 9. Priority Classes

```yaml
# PriorityClass
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: critical
value: 1000000
globalDefault: false
description: "Critical pods that should not be evicted"

---
# Use in Pod
spec:
  priorityClassName: critical
  containers:
  - name: critical-service
    image: myapp:latest
```

---

## 10. Useful kubectl Commands

```bash
# Debugging
kubectl describe pod <pod-name>          # Full pod status + events
kubectl logs <pod-name> -c <container>   # Specific container logs
kubectl logs <pod-name> --previous       # Previous container instance
kubectl exec -it <pod-name> -- bash      # Shell into container
kubectl port-forward svc/api 8080:80     # Port forward for debugging
kubectl top pods --sort-by=memory        # Resource usage

# Resource inspection
kubectl get all -n myapp                 # All resources in namespace
kubectl get events --sort-by=.lastTimestamp
kubectl get pods -o wide                 # Show node assignment

# Patching
kubectl patch deployment api -p '{"spec":{"replicas":5}}'
kubectl set image deployment/api api=myapp:v2.0

# Context management
kubectl config get-contexts
kubectl config use-context prod-cluster
kubectl config set-context --current --namespace=myapp

# Copy files
kubectl cp pod-name:/app/logs ./logs
kubectl cp ./config.json pod-name:/app/config.json

# Apply with dry-run
kubectl apply -f deployment.yaml --dry-run=client
kubectl diff -f deployment.yaml
```

---

*Tài liệu liên quan: `kubernetes/01-kubernetes-basics.md` | `kubernetes/03-kubernetes-networking.md` | `kubernetes/04-kubernetes-security.md`*
