# Bài 56 — Job & CronJob 🔴

> **Tiên quyết:** Hoàn thành Bài 41; namespace `myapp-dev` đã tồn tại.
> **File:** `job-migrate.yaml`, `cronjob-backup.yaml`.

## Trước khi apply

Mở `job-migrate.yaml`, thay `<YOUR_DOCKERHUB_USERNAME>` bằng username Docker Hub thật.

## Lệnh thủ công

```bash
# 1. Apply Job 1 lần (migration)
kubectl apply -f job-migrate.yaml
kubectl get jobs -n myapp-dev
kubectl logs -f job/myapp-migrate -n myapp-dev

# 2. Quan sát: Job xong → COMPLETIONS 1/1
kubectl get pods -n myapp-dev -l job-name=myapp-migrate
# Pod ở STATUS Completed

# 3. Apply CronJob (backup mỗi giờ)
kubectl apply -f cronjob-backup.yaml
kubectl get cronjobs -n myapp-dev

# 4. Trigger thủ công để test (không chờ schedule)
kubectl create job --from=cronjob/myapp-backup manual-backup-$(date +%s) -n myapp-dev
kubectl get jobs -n myapp-dev

# 5. Sau 10 phút Job tự xóa nhờ ttlSecondsAfterFinished
```

## Kết quả mong đợi

- `myapp-migrate` chạy 10s rồi `Completed`, COMPLETIONS `1/1`.
- `myapp-backup` CronJob có `SCHEDULE 0 * * * *`, `ACTIVE 0` lúc bình thường.
- Trigger thủ công tạo job mới và chạy ngay.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Job retry mãi không dừng | `backoffLimit` chưa đặt hoặc quá cao; xem log pod fix root cause |
| Pod Job `CrashLoopBackOff` | Job phải `restartPolicy: OnFailure` hoặc `Never` — KHÔNG được `Always` |
| CronJob không trigger | `schedule` sai cron syntax; timezone control-plane lệch — kiểm tra `kubectl describe cronjob` |

## Câu hỏi

- Job khác Deployment thế nào về `restartPolicy`?
  *(Deployment: bắt buộc `Always`. Job: phải `OnFailure` hoặc `Never`.)*
- `concurrencyPolicy: Allow / Forbid / Replace` — chọn cái nào cho backup? cho metric report?
  *(Backup: `Forbid` để tránh ghi đè. Metric report: `Replace` để luôn lấy số mới nhất.)*

## Bài kế tiếp

```bash
cd ../57-daemonset
```
