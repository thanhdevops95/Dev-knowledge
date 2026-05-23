# Bài 33 — Secret

> ⚠️ **CẢNH BÁO QUAN TRỌNG:** Secret trong K8s **CHỈ ĐƯỢC ENCODE bằng base64** (decode 1 phát ra plaintext) — **KHÔNG PHẢI ENCRYPT**. Bất kỳ ai có quyền `get secret` đều đọc được nội dung. Production thật phải dùng **encryption at rest** (etcd encryption), **External Secrets Operator + Vault/AWS Secrets Manager**, hoặc **Sealed Secrets** (Bài 68 Bonus).

## Lệnh thủ công

### Cách 1 — Tạo bằng lệnh (đơn giản)

```bash
kubectl create secret generic myapp-secret \
  --from-literal=DB_PASSWORD=supersecret123 \
  --from-literal=API_KEY=abc-xyz-789 \
  -n myapp-dev
```

### Cách 2 — Tạo bằng YAML với `stringData` (khuyến nghị, không cần base64 thủ công)

File `secret-stringdata.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
  namespace: myapp-dev
type: Opaque
stringData:
  DB_PASSWORD: supersecret123
  API_KEY: abc-xyz-789
```

Apply:
```bash
kubectl apply -f secret-stringdata.yaml
```

> 💡 **`stringData` vs `data`:** Khi apply, K8s tự convert `stringData` → `data` (base64). Khi `kubectl get -o yaml` chỉ thấy `data:`. Dùng `stringData` khi viết tay (dễ đọc), dùng `data` khi nhận output từ tool.

### Cách 3 — Tạo bằng YAML với `data` (phải tự base64)

Trước hết encode giá trị:
```bash
echo -n "supersecret123" | base64
# Output: c3VwZXJzZWNyZXQxMjM=

echo -n "abc-xyz-789" | base64
# Output: YWJjLXh5ei03ODk=
```

Đã có sẵn `secret.yaml` với base64 encoded. Apply:
```bash
kubectl apply -f secret.yaml
```

### Verify

```bash
kubectl get secrets -n myapp-dev
kubectl describe secret myapp-secret -n myapp-dev
kubectl get secret myapp-secret -n myapp-dev -o yaml

# Decode để xem
kubectl get secret myapp-secret -n myapp-dev -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
```

### Dùng trong Deployment

Apply `deployment.yaml` đã được sửa sẵn để inject secret:
```bash
kubectl apply -f deployment.yaml
kubectl rollout restart deployment/myapp-deployment -n myapp-dev
```

## Câu hỏi

- Tại sao `kubectl describe` ẩn value mà `kubectl get -o yaml` lại để lộ?
- Nếu push file Secret YAML lên Git (public), hậu quả ra sao? Cách an toàn?
  - *Hậu quả:* base64 decode 1 dòng `echo ... | base64 -d` → lộ plaintext credential.
  - *Cách an toàn:* SealedSecrets (encrypt trước khi commit), External Secrets + Vault, hoặc gitignore file Secret.

## ⚠️ Lưu ý

- Secret **base64 encode** chỉ là encoding, **KHÔNG mã hóa**. Ai có quyền `get secret` đều xem được giá trị.
- Production: dùng [External Secrets](https://external-secrets.io/) + Vault/AWS SSM/GCP Secret Manager.

## Bài kế tiếp

```bash
cp -r ../33-secret ../34-pv-pvc
cd ../34-pv-pvc
```
