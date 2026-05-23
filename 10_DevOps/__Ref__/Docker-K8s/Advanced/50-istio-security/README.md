# Bài 50 — Security & Observability với Istio (DỰ ÁN CUỐI)

## Phần A — Mutual TLS (mTLS)

```bash
kubectl apply -f peer-auth-strict.yaml

# Verify
istioctl authn tls-check <pod-name>.myapp-dev
# STATUS: OK, mTLS: STRICT
```

## Phần B — Authorization Policy (L7 RBAC)

```bash
kubectl apply -f authz-policy.yaml

# Test: pod ngoài namespace gọi → bị 403
```

## Phần C — Distributed Tracing

```bash
# Tạo traffic
for i in {1..100}; do curl http://myapp.local; done

# Mở Jaeger
istioctl dashboard jaeger
# Xem request flow, latency từng span
```

## Phần D — Metrics

```bash
# Mở Grafana
istioctl dashboard grafana
# Dashboard có sẵn: Istio Mesh / Service / Workload Dashboard
# Quan sát RED metrics: Rate, Errors, Duration (P50/P95/P99)
```

## 🎓 Dự án cuối khóa — Hệ thống hoàn chỉnh

Triển khai `myapp` microservices với:

✅ **Bắt buộc:**

1. **Code & Docker** — 3 microservice (frontend React, backend Python, worker), multi-stage Dockerfile
2. **Kubernetes** — Deployment + Service + Ingress, ConfigMap + Secret, StatefulSet DB, PVC, HPA, probes, resource limits
3. **Helm** — 1 chart, subchart Redis/Postgres, values per env, migration hook
4. **GitOps ArgoCD** — ApplicationSet 3 env, auto-sync, self-heal, Image Updater
5. **Istio** — Sidecar, Gateway, Canary, mTLS strict, AuthZ policy
6. **Observability** — Jaeger + Prometheus + Grafana + Loki/EFK

✅ **Bonus:** CI/CD pipeline, Chaos Mesh, Backup, Cost optimization

**Tiêu chí đánh giá:**

| Tiêu chí | Trọng số |
|----------|----------|
| HA | 20% |
| Bảo mật (mTLS, RBAC, Secret) | 20% |
| Observability (logs/metrics/traces) | 20% |
| Automation (GitOps, CI/CD) | 20% |
| Documentation | 10% |
| Khả năng mở rộng | 10% |

## Hoàn thành chuỗi 50 bài

Bạn đã đi từ:
- `docker pull hello-world` (Bài 01)
- → Flask app + Redis + Postgres (Bài 23)
- → Push lên Docker Hub (Bài 24)
- → K8s Deployment/Service (Bài 29-30)
- → Helm/HPA/Ingress (Bài 37-40)
- → GitOps với ArgoCD (Bài 45-47)
- → Service Mesh với Istio (Bài 48-50)

Chúc bạn tiếp tục hành trình DevOps!
