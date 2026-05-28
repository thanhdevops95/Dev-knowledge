# Bài 68 — Sealed Secrets / External Secrets

> **Mục tiêu:** quản lý secret an toàn — KHÔNG commit plaintext lên Git.

## Tiên quyết

- Hoàn thành Bài 33 (Secret) — hiểu base64 ≠ encryption.
- Helm 3 đã cài.
- (Tùy chọn) Có AWS account hoặc Vault để test External Secrets thật. Nếu không, có thể thay bằng provider `kubernetes` để demo workflow.

## File trong thư mục

- `sealedsecret-example.yaml` — Placeholder SealedSecret (file output của `kubeseal`, đã encrypt).
- `clustersecretstore.yaml` — `ClusterSecretStore` của External Secrets (provider AWS Secrets Manager).
- `externalsecret.yaml` — `ExternalSecret` kéo `DB_PASSWORD` từ AWS về thành K8s Secret.

## Lệnh thủ công

### Phần A — Sealed Secrets

```bash
# 1. Cài controller + kubeseal CLI
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets sealed-secrets/sealed-secrets -n kube-system
brew install kubeseal

# 2. Tạo Secret thường (chưa apply)
kubectl create secret generic myapp-secret \
  --from-literal=DB_PASSWORD=supersecret \
  --dry-run=client -o yaml > secret-plain.yaml

# 3. Encrypt thành SealedSecret (file SẢN PHẨM tương đương sealedsecret-example.yaml)
kubeseal --format yaml < secret-plain.yaml > sealedsecret-example.yaml

# 4. Apply — file SealedSecret CÓ THỂ commit lên Git
kubectl apply -f sealedsecret-example.yaml
kubectl get secret myapp-secret -o yaml   # đã có Secret thật
```

### Phần B — External Secrets Operator

```bash
# 1. Cài ESO
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets-system --create-namespace

# 2. Tạo credentials AWS trong cluster (cần access key có quyền secretsmanager:GetSecretValue)
kubectl -n external-secrets-system create secret generic aws-creds \
  --from-literal=access-key=AKIA... \
  --from-literal=secret-key=...

# 3. Apply ClusterSecretStore + ExternalSecret
kubectl apply -f clustersecretstore.yaml
kubectl apply -f externalsecret.yaml

# 4. Verify
kubectl get clustersecretstore aws-store
kubectl get externalsecret myapp-db -n myapp-dev
kubectl get secret myapp-secret -n myapp-dev -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
```

## Kết quả mong đợi

- **Sealed Secrets:** file `sealedsecret-example.yaml` có thể public mà vẫn an toàn; controller tự decrypt thành Secret thật.
- **External Secrets:** `ExternalSecret` ở trạng thái `SecretSynced`, K8s Secret `myapp-secret` trong `myapp-dev` chứa giá trị lấy từ AWS Secrets Manager (key `/prod/myapp/db`).

## Câu hỏi

- Sealed Secrets vs External Secrets — khi nào dùng cái nào?
- Cả hai cùng giải quyết "base64 không phải encryption" (Bài 33) — đúng không?

## Bài kế tiếp

```bash
cd ../69-operator-crd
```
