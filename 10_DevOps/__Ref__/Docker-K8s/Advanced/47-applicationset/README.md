# Bài 47 — ApplicationSet (multi-environment)

## Lệnh thủ công

```bash
# Sửa applicationset.yaml: đổi repoURL sang repo của bạn
kubectl apply -f applicationset.yaml

# Sẽ tự tạo 3 Application: myapp-dev, myapp-staging, myapp-prod
kubectl get applications -n argocd
```

## Helm + ArgoCD

Application dùng Helm chart (`application-helm.yaml`):

```bash
kubectl apply -f application-helm.yaml
```

## Bonus — ArgoCD Image Updater

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml
```

Annotate Application để tự update image:
```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: myapp=<YOUR_DOCKERHUB_USERNAME>/myapp
    argocd-image-updater.argoproj.io/myapp.update-strategy: semver
```

Push image mới với tag tăng version → Image Updater tự update Git → ArgoCD sync.

## Bài kế tiếp

```bash
cp -r ../47-applicationset ../48-istio-setup
cd ../48-istio-setup
```
