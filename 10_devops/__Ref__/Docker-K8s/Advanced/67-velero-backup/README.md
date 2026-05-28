# Bài 67 — Velero — Backup & Restore

> **Mục tiêu:** backup toàn bộ cluster (manifest + PV data) ra Object Storage và restore khi gặp sự cố.

## Tiên quyết

- Hoàn thành Bài 34 (PV/PVC) và Bài 41.
- Velero CLI cài máy local (`brew install velero`).
- Object Storage: dùng MinIO local cho lab, hoặc S3/GCS thật.

## File trong thư mục

- `backup-schedule.yaml` — `Schedule` CR backup namespace `myapp-dev` lúc 02:00 mỗi ngày.
- `restore-example.md` — Kịch bản khôi phục sau khi xóa namespace.

## Lệnh thủ công

```bash
# 1. (Lab) cài MinIO làm object storage
helm install minio bitnami/minio -n velero --create-namespace \
  --set auth.rootUser=minio --set auth.rootPassword=minio123

# 2. Credentials file cho Velero
cat > credentials-velero <<EOF
[default]
aws_access_key_id=minio
aws_secret_access_key=minio123
EOF

# 3. Install Velero server (qua CLI)
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.9.0 \
  --bucket velero-backups \
  --secret-file ./credentials-velero \
  --use-volume-snapshots=false \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.velero.svc:9000

kubectl get pods -n velero

# 4. Backup on-demand
velero backup create myapp-backup --include-namespaces myapp-dev
velero backup describe myapp-backup     # Phase: Completed

# 5. Backup theo schedule (apply file đi kèm)
kubectl apply -f backup-schedule.yaml
velero schedule get
```

## Kết quả mong đợi

- `velero backup describe myapp-backup` → `Phase: Completed`.
- File backup xuất hiện trong bucket MinIO (`mc ls minio/velero-backups/`).
- Restore từ backup phục hồi đầy đủ workload — chi tiết xem `restore-example.md`.

## Câu hỏi

- Velero backup gồm những gì? PV data có được backup mặc định không?
- Khác `etcdctl snapshot` thế nào? (etcd: toàn cluster; Velero: per-namespace).

## Bài kế tiếp

```bash
cd ../68-secrets-mgmt
```
