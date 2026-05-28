# 🔑 Solutions: GitOps Platform

> **Solutions for GitOps Exercises**
>
> *Lời giải cho bài tập GitOps.*

---

## Exercise 1: Repository Structure

```bash
mkdir -p gitops-repo/{apps/{base,overlays/{dev,prod}},infrastructure/{monitoring,ingress},clusters/{dev,prod}}

# apps/base/deployment.yaml
cat <<EOF > gitops-repo/apps/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: nginx:alpine
EOF

# apps/base/kustomization.yaml
cat <<EOF > gitops-repo/apps/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
EOF
```

---

## Exercise 2: Multi-Environment

```yaml
# apps/overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 1
    target:
      kind: Deployment
      name: myapp
configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=debug
```

```yaml
# apps/overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
patches:
  - patch: |-
      - op: replace
        path: /spec/replicas
        value: 3
    target:
      kind: Deployment
      name: myapp
configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=warn
```

---

## Exercise 3: Helm Chart

```yaml
# postgresql-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: postgresql
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://charts.bitnami.com/bitnami
    chart: postgresql
    targetRevision: 12.0.0
    helm:
      values: |
        primary:
          persistence:
            enabled: true
            size: 10Gi
        auth:
          existingSecret: postgresql-secret
  destination:
    server: https://kubernetes.default.svc
    namespace: database
  syncPolicy:
    automated:
      prune: true
```

---

> 💡 **Note:** These are reference solutions. Adapt for your environment.
>
> *Lưu ý: Đây là lời giải tham khảo. Điều chỉnh cho môi trường của bạn.*

---

**[← Back to README](./README.md)**
