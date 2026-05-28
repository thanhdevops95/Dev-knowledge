# Bài 65 — cert-manager + Let's Encrypt

> **Mục tiêu:** TLS tự động cho Ingress (cấp + renew miễn phí).

## Tiên quyết

- Cluster có Ingress controller (nginx) chạy được — Bài 38.
- Domain công khai trỏ về Ingress IP (hoặc `nip.io` cho lab: `myapp.<INGRESS_IP>.nip.io`).
- Sửa email trong `cluster-issuer-staging.yaml` / `cluster-issuer-prod.yaml` thành email thật.

## File trong thư mục

- `cluster-issuer-staging.yaml` — ClusterIssuer dùng endpoint Let's Encrypt **staging** (test, không lo rate limit).
- `cluster-issuer-prod.yaml` — ClusterIssuer dùng endpoint **production** (chỉ apply sau khi staging OK).
- `ingress-tls.yaml` — Ingress của `myapp` đã annotate cert-manager.

## Lệnh thủ công

```bash
# 1. Cài cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl rollout status deployment/cert-manager -n cert-manager
kubectl get pods -n cert-manager     # 3 pod Running

# 2. Apply ClusterIssuer staging trước (tránh rate limit)
kubectl apply -f cluster-issuer-staging.yaml
kubectl get clusterissuer            # Ready=True

# 3. Apply Ingress có annotation
kubectl apply -f ingress-tls.yaml

# 4. Quan sát Certificate sinh ra
kubectl get certificate -w
kubectl describe certificate myapp-tls
kubectl get secret myapp-tls -o yaml | grep -E 'tls\.(crt|key)'

# 5. Khi đã OK với staging → đổi sang production
kubectl apply -f cluster-issuer-prod.yaml
# Sửa annotation Ingress: letsencrypt-staging -> letsencrypt-prod
kubectl apply -f ingress-tls.yaml
```

## Kết quả mong đợi

- `kubectl get certificate myapp-tls` → `READY=True`.
- `curl -kvI https://myapp.example.com` (hoặc nip.io tương ứng) → cert hợp lệ, không còn warning self-signed.
- Secret `myapp-tls` chứa `tls.crt` + `tls.key`.

## Câu hỏi

- Vì sao test bằng staging trước? → Let's Encrypt **prod** giới hạn 50 cert/domain/tuần.
- Cert tự renew khi nào? → mặc định khi còn < **30 ngày**.

## Bài kế tiếp

```bash
cd ../66-prometheus-stack
```
