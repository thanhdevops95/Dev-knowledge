# Bài 44 — Subchart, Dependencies & Hooks

> ⚠️ **File trong `examples/` là Helm template snippet** + 2 file `values-{dev,prod}.yaml` (Helm values, không phải K8s Resource). **KHÔNG** `kubectl apply -f` trực tiếp. Dùng với `helm install ... -f values-prod.yaml` hoặc copy templates vào `<chart>/templates/`.

## Phần A — Dependencies

Trong `myapp-fullstack/Chart.yaml`:
```yaml
apiVersion: v2
name: myapp-fullstack
version: 1.0.0
dependencies:
  - name: redis
    version: "18.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
  - name: postgresql
    version: "13.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

Lệnh:
```bash
helm dependency update
helm dependency list
```

Override values cho subchart trong `values.yaml`:
```yaml
redis:
  enabled: true
  auth:
    password: "myredispass"

postgresql:
  enabled: true
  auth:
    username: myapp
    password: mypass
    database: myappdb
```

## Phần B — Hooks

`templates/migration-job.yaml` chạy migration trước install/upgrade:
```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
```

Hook test sau install (`templates/tests/test-connection.yaml`):
```yaml
metadata:
  annotations:
    "helm.sh/hook": test
```

Chạy:
```bash
helm install myapp ./myapp-fullstack
helm test myapp
```

## Phần C — Multi-environment

Tạo `values-dev.yaml`, `values-staging.yaml`, `values-prod.yaml`. Deploy:
```bash
helm install myapp-dev   ./myapp-fullstack -f values-dev.yaml   -n dev
helm install myapp-stag  ./myapp-fullstack -f values-staging.yaml -n staging
helm install myapp-prod  ./myapp-fullstack -f values-prod.yaml  -n prod
```

## Bài kế tiếp

```bash
cp -r ../44-helm-hooks ../45-argocd-setup
cd ../45-argocd-setup
```
