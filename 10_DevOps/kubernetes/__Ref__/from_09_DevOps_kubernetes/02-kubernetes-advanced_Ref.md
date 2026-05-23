# ☸️ Kubernetes nâng cao — Orchestration Production

> `[INTERMEDIATE → ADVANCED]` — Scaling, monitoring, security trên K8s

---

## 1. Helm — Package Manager cho K8s

```bash
# Helm = npm cho Kubernetes
helm repo add bitnami https://charts.bitnami.com/bitnami

# Install nginx
helm install my-nginx bitnami/nginx

# Install với custom values
helm install my-app ./my-chart -f values-prod.yaml

# Upgrade
helm upgrade my-app ./my-chart -f values-prod.yaml

# Rollback
helm rollback my-app 1
```

```yaml
# Chart.yaml
apiVersion: v2
name: my-app
version: 1.0.0

# values.yaml
replicaCount: 3
image:
  repository: myapp
  tag: "1.2.3"
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
ingress:
  enabled: true
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
```

---

## 2. Ingress — Routing traffic

```yaml
# Ingress = reverse proxy (Nginx, Traefik)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts: [api.example.com]
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api/users
            pathType: Prefix
            backend:
              service:
                name: user-service
                port: { number: 80 }
          - path: /api/orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port: { number: 80 }
```

```
Internet ──► Ingress Controller ──┬──► user-service
             (Nginx/Traefik)      ├──► order-service
                                  └──► frontend-service
```

---

## 3. ConfigMaps & Secrets

```yaml
# ConfigMap — cấu hình non-sensitive
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres-service"
  REDIS_HOST: "redis-service"
  LOG_LEVEL: "info"
  APP_PORT: "3000"

---
# Secret — cấu hình sensitive (base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQxMjM=    # base64("password123")
  JWT_SECRET: c3VwZXItc2VjcmV0           # base64("super-secret")

---
# Sử dụng trong Deployment
spec:
  containers:
    - name: app
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

---

## 4. Health Checks — Liveness & Readiness

```yaml
spec:
  containers:
    - name: app
      livenessProbe:            # App còn sống không?
        httpGet:                # Nếu fail → RESTART container
          path: /health
          port: 3000
        initialDelaySeconds: 10
        periodSeconds: 10
        failureThreshold: 3

      readinessProbe:           # App sẵn sàng nhận traffic?
        httpGet:                # Nếu fail → BỎ khỏi Service
          path: /ready
          port: 3000
        initialDelaySeconds: 5
        periodSeconds: 5

      startupProbe:             # App đã start xong chưa?
        httpGet:                # Chờ đến khi pass
          path: /health
          port: 3000
        failureThreshold: 30
        periodSeconds: 10
```

```javascript
// Health check endpoints
app.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

app.get('/ready', async (req, res) => {
    try {
        await db.query('SELECT 1');
        await redis.ping();
        res.json({ status: 'ready' });
    } catch (err) {
        res.status(503).json({ status: 'not ready', error: err.message });
    }
});
```

---

## 5. Resource Management

```yaml
spec:
  containers:
    - name: app
      resources:
        requests:              # Minimum resources (scheduling)
          cpu: "250m"          # 0.25 CPU core
          memory: "256Mi"      # 256 MB RAM
        limits:                # Maximum resources (throttling)
          cpu: "1000m"         # 1 CPU core
          memory: "512Mi"      # 512 MB — vượt = OOMKilled!

# HPA — Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # Scale up nếu CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## 6. Rolling Updates & Rollbacks

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1              # Thêm tối đa 1 pod mới
      maxUnavailable: 0        # Không pod nào bị down

# Deploy flow:
# v1 ●●● (3 pods)
# v1 ●●● + v2 ● (tạo 1 pod mới)
# v1 ●● + v2 ●● (v1 giảm, v2 tăng)
# v1 ● + v2 ●●● (tiếp tục...)
# v2 ●●● (hoàn tất, zero downtime!)
```

```bash
# Deploy new version
kubectl set image deployment/my-app app=myapp:v2
kubectl rollout status deployment/my-app

# Rollback nếu lỗi
kubectl rollout undo deployment/my-app
kubectl rollout undo deployment/my-app --to-revision=3

# Xem history
kubectl rollout history deployment/my-app
```

---

## 7. Monitoring — Prometheus + Grafana

```yaml
# ServiceMonitor (Prometheus Operator)
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: app-monitor
spec:
  selector:
    matchLabels:
      app: my-app
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

```javascript
// Express middleware — expose metrics
const promClient = require('prom-client');

const httpRequestCounter = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total HTTP requests',
    labelNames: ['method', 'path', 'status'],
});

const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration',
    labelNames: ['method', 'path'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
});

app.use((req, res, next) => {
    const start = Date.now();
    res.on('finish', () => {
        httpRequestCounter.inc({ method: req.method, path: req.path, status: res.statusCode });
        httpRequestDuration.observe({ method: req.method, path: req.path },
            (Date.now() - start) / 1000);
    });
    next();
});

app.get('/metrics', async (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.end(await promClient.register.metrics());
});
```

---

## 8. Namespace & RBAC

```yaml
# Namespace — chia cluster
apiVersion: v1
kind: Namespace
metadata:
  name: production

---
# RBAC — ai được làm gì
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: developer-role
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "update"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer-binding
  namespace: production
subjects:
  - kind: User
    name: developer@company.com
roleRef:
  kind: Role
  name: developer-role
  apiGroup: rbac.authorization.k8s.io
```

---

## Các lỗi thường gặp

```
❌ Sai: Không set resource limits → 1 pod ăn hết RAM cluster
✅ Đúng: LUÔN set requests + limits

❌ Sai: Không có health checks → K8s không biết app đã crash
✅ Đúng: Liveness + Readiness probes cho mọi deployment

❌ Sai: Image tag :latest → không biết version nào đang chạy
✅ Đúng: Dùng specific tags (:v1.2.3) hoặc SHA digest
```

---

## Bài tập thực hành

- [ ] Tạo Helm chart cho app + database + redis
- [ ] Setup Ingress: routing 2 services qua 1 domain
- [ ] HPA: auto-scale khi CPU > 70% (load test bằng k6)
- [ ] Rolling update → verify → rollback

---

## Tài nguyên thêm

- [Kubernetes Docs](https://kubernetes.io/docs/) — Official
- [Helm Docs](https://helm.sh/docs/) — Package manager
- [Kubernetes Patterns (O'Reilly)](https://k8spatterns.io/) — Advanced patterns
