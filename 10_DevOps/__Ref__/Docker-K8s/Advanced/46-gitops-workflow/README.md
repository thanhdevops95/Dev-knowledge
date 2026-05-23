# Bài 46 — GitOps Workflow

> **Tiên quyết:** ArgoCD đã cài (Bài 45), Application `myapp-dev` đang sync.

## Kịch bản 1 — Update image version

```bash
# Trên máy local (clone repo gitops):
cd ~/myapp-gitops

# Sửa environments/dev/kustomization.yaml
# Đổi newTag: "6.0" → "8.0"

git add .
git commit -m "Update myapp to v8.0 in dev"
git push origin main

# ArgoCD tự sync trong ~3 phút (polling)
# Force sync ngay:
argocd app sync myapp-dev
```

`environments/dev/kustomization.yaml`:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
images:
  - name: <YOUR_DOCKERHUB_USERNAME>/myapp
    newTag: "8.0"
```

## Kịch bản 2 — Self-heal

Cố ý drift (sửa thủ công ngoài Git):
```bash
kubectl scale deployment myapp-deployment --replicas=10 -n myapp-dev
```

Sau vài giây quan sát trên ArgoCD UI: phát hiện "OutOfSync" và **tự revert** về `replicas=3`.

## Kịch bản 3 — Rollback

```bash
# Xem history
argocd app history myapp-dev

# Rollback
argocd app rollback myapp-dev <REVISION_ID>
```

> **GitOps thuần:** rollback đúng cách là `git revert` commit rồi để ArgoCD sync. Cách trên dùng cho khẩn cấp.

## Bài kế tiếp

```bash
cp -r ../46-gitops-workflow ../47-applicationset
cd ../47-applicationset
```
