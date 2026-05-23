# Kubernetes Advanced — RBAC, HPA, Network, Production

> **Tags:** `kubernetes` `k8s` `helm` `rbac` `networking` `hpa` `production`
> **Level:** Advanced | **Prerequisite:** `kubernetes/01-kubernetes-basics.md`

---

## 1. RBAC (Role-Based Access Control)

```yaml
# Service Account for application
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-service
  namespace: production
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/api-pod-role  # AWS IRSA

---
# Role — namespace-scoped permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: config-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
    resourceNames: ["app-config", "api-secrets"]  # Restrict to specific names

---
# Bind role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-config-reader
  namespace: production
subjects:
  - kind: ServiceAccount
    name: api-service
    namespace: production
roleRef:
  kind: Role
  name: config-reader
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole — cluster-wide (all namespaces)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-reader
rules:
  - apiGroups: [""]
    resources: ["nodes", "pods", "services", "endpoints"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "statefulsets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["metrics.k8s.io"]
    resources: ["nodes", "pods"]
    verbs: ["get", "list"]
```

```bash
# Audit permissions
kubectl auth can-i list pods --as=system:serviceaccount:production:api-service
kubectl auth can-i create deployments -n production --as=dev@example.com

# View all permissions for a user
kubectl auth can-i --list -n production --as=dev@example.com
```

---

## 2. Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-api
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70        # Scale out when avg CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    # Custom metric from Prometheus (via KEDA or custom metrics adapter)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"           # Scale when avg RPS/pod > 100
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30    # Wait 30s before scaling up again
      policies:
        - type: Percent
          value: 100                    # Max double pods per period
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300   # 5 min cool-down before scale down
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60
```

---

## 3. Resource Management & QoS

```yaml
# Always set both requests AND limits
containers:
  - name: api
    resources:
      requests:
        cpu: "100m"      # 100 millicores = 0.1 CPU core
        memory: "128Mi"  # Minimum guaranteed memory
      limits:
        cpu: "1000m"     # Max 1 CPU — throttled if exceeded
        memory: "512Mi"  # Max memory — OOMKilled if exceeded

# QoS Classes (eviction priority):
# Guaranteed: requests == limits for both CPU and memory → evicted LAST
# Burstable:  requests < limits, or only one set → middle
# BestEffort: no requests/limits → evicted FIRST
```

```yaml
# LimitRange — enforce defaults for namespace
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: staging
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "256Mi"
      defaultRequest:
        cpu: "100m"
        memory: "64Mi"
      max:
        cpu: "4"
        memory: "4Gi"

---
# ResourceQuota — cap total namespace usage
apiVersion: v1
kind: ResourceQuota
metadata:
  name: staging-quota
  namespace: staging
spec:
  hard:
    requests.cpu: "20"
    requests.memory: "40Gi"
    limits.cpu: "40"
    limits.memory: "80Gi"
    pods: "100"
    services.loadbalancers: "2"
    persistentvolumeclaims: "20"
```

---

## 4. Network Policies (Zero Trust)

```yaml
# Start: deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}     # All pods
  policyTypes:
    - Ingress
    - Egress

---
# Allow: ingress-controller → API pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: my-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080

---
# Allow: API pods → Database (egress)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-to-db
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: my-api
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgresql
      ports:
        - protocol: TCP
          port: 5432
    # Allow DNS resolution
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
```

---

## 5. Pod Disruption Budget

```yaml
# Ensure minimum availability during node drain/upgrades
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-pdb
  namespace: production
spec:
  minAvailable: 2          # At least 2 pods must always be running
  # OR: maxUnavailable: 1  # At most 1 pod can be unavailable
  selector:
    matchLabels:
      app: my-api
# kubectl drain node/worker-1 → K8s will respect PDB, wait for replacement
```

---

## 6. Pod Scheduling — Affinity & Anti-Affinity

```yaml
spec:
  affinity:
    # Require specific node type (hard requirement)
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: node.kubernetes.io/instance-type
                operator: In
                values: ["m5.xlarge", "m5.2xlarge"]
    
    # Spread pods across availability zones (soft preference)
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                app: my-api
            topologyKey: topology.kubernetes.io/zone
  
  # Even spread constraint (fine-grained)
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app: my-api
  
  # Allow running on tainted nodes
  tolerations:
    - key: "dedicated"
      operator: "Equal"
      value: "high-mem"
      effect: "NoSchedule"
```

---

## 7. External Secrets Operator

```yaml
# Better than storing secrets directly in K8s (stored encrypted in cloud)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-secrets
  namespace: production
spec:
  refreshInterval: 1h           # Re-sync every hour
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  target:
    name: api-secrets            # K8s Secret to create
    creationPolicy: Owner
  data:
    - secretKey: database-url
      remoteRef:
        key: production/api      # AWS SM path
        property: database_url   # Key within the secret JSON
    - secretKey: jwt-secret
      remoteRef:
        key: production/api
        property: jwt_secret
```

---

## 8. Production Pod Spec (Best Practices)

```yaml
spec:
  serviceAccountName: api-service     # Dedicated SA (not default!)
  automountServiceAccountToken: false  # Disable if not needed
  
  securityContext:                    # Pod-level
    runAsNonRoot: true
    runAsUser: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault            # Restrict syscalls
  
  containers:
    - name: api
      securityContext:                # Container-level
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true  # Can't write to filesystem
        capabilities:
          drop: ["ALL"]               # No Linux capabilities
      
      # Probes
      startupProbe:                   # Allow slow start (30 * 10s = 5 min)
        httpGet: { path: /health, port: 8080 }
        failureThreshold: 30
        periodSeconds: 10
      
      livenessProbe:                  # Kill & restart if unhealthy
        httpGet: { path: /health/live, port: 8080 }
        initialDelaySeconds: 0        # startupProbe covers initial wait
        periodSeconds: 10
        failureThreshold: 3
      
      readinessProbe:                 # Remove from LB if not ready
        httpGet: { path: /health/ready, port: 8080 }
        periodSeconds: 5
        failureThreshold: 3
      
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 15"]   # Drain connections
      
      # Writable directories via emptyDir (rest is read-only)
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  
  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir:
        sizeLimit: 256Mi
  
  # Graceful shutdown
  terminationGracePeriodSeconds: 60   # Default 30 — increase if drain takes longer
```

---

## 9. Helm Chart Management Tips

```bash
# Chart creation
helm create my-chart

# Lint chart
helm lint ./my-chart

# Dry run
helm install --dry-run --debug my-api ./my-chart -f values-prod.yaml

# Template rendering (view generated YAML)
helm template my-api ./my-chart -f values-prod.yaml > debug.yaml

# Diff plugin (see what will change)
helm plugin install https://github.com/databus23/helm-diff
helm diff upgrade my-api ./my-chart -f values-prod.yaml

# Releases in all namespaces
helm list --all-namespaces

# Chart structure for multiple environments
my-chart/
├── values.yaml           # Defaults
├── values-staging.yaml   # Staging overrides (fewer replicas, dev resources)
└── values-production.yaml # Production overrides

# Deploy to staging
helm upgrade --install my-api . -f values.yaml -f values-staging.yaml --set image.tag="$SHA"

# Deploy to production
helm upgrade --install my-api . -f values.yaml -f values-production.yaml --set image.tag="$SHA" \
  --atomic             # Rollback automatically if deploy fails
  --cleanup-on-fail    # Remove resources created during failed upgrade
```

---

*Tài liệu liên quan: `kubernetes/01-kubernetes-basics.md` | `iac/02-terraform-advanced.md` | `observability/02-observability-advanced.md` | `cicd/02-github-actions-advanced.md`*
