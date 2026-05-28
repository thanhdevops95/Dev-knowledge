# Rà soát tài liệu — Trạng thái chuẩn hóa

> **Cập nhật:** 18/05/2026 · v2.0.0 · Dùng cho giảng viên / học viên theo dõi chất lượng đề.

## 🆕 Đợt cập nhật v2.0.0 (18/05/2026)

**Sửa lỗi kỹ thuật** ở 9 bài:

| Bài | Sửa gì |
|-----|--------|
| Docker 21 | Thêm note DNS FQDN `<svc>.<ns>.svc.cluster.local` (chuẩn bị cho K8s) |
| Docker 23 | Bỏ `version: '3.8'` (deprecated), thêm `healthcheck` + `depends_on.condition: service_healthy`, đổi `docker-compose` → `docker compose` |
| K8s 27 | Thêm `imagePullPolicy: IfNotPresent` + hướng dẫn `minikube image load` / `kind load docker-image` |
| K8s 33 | Cảnh báo `base64 ≠ encryption`, dạy `stringData:` (không cần base64 thủ công), link tới Bonus Bài 68 |
| K8s 34 | Note `hostPath` chỉ single-node, link tới Bonus Bài 63 (StorageClass) |
| K8s 36 | Thêm `startupProbe` (3 probe đầy đủ), bảng so sánh, kiểu probe HTTP/TCP/Exec/gRPC |
| K8s 37 | Chuyển HPA sang `autoscaling/v2` YAML (CPU + memory + `behavior`) |
| Advanced 42 | Cảnh báo `randAlphaNum` trap + pattern `lookup` để giữ password ổn định |
| Advanced 48 | Note RAM requirement của Istio `profile=demo` (4GB) vs `profile=minimal` |

**Thêm Phần D — Bonus Production-grade (Bài 51-69)** — 19 bài:
- Docker (51-55): `.dockerignore`/USER/HEALTHCHECK, Restart & Limits, ENTRYPOINT vs CMD + Signal, Image scanning, Buildx multi-arch
- K8s (56-64): Job/CronJob, DaemonSet, Init/Sidecar, RBAC, NetworkPolicy, Affinity/Taints, Quota/LimitRange/PDB, StorageClass, Kustomize
- Advanced (65-69): cert-manager, Prometheus+Grafana, Velero, Sealed/External Secrets, Operator+CRD

**Tăng chất lượng giảng dạy:**
- Thêm **13 mermaid diagrams** visualize concept khó (lifecycle, RBAC, NetworkPolicy, signal flow, reconcile loop...)
- Bổ sung block chú thích chi tiết cho từng concept (📚 giải thích, ⚠️ cảnh báo, 💡 mẹo)

**Lab-run verification (18/05/2026):** Chạy thật toàn bộ 69 bài trên Docker 29.4.1 + Minikube 1.38.1. Chi tiết: [LAB-RUN-LOG.md](LAB-RUN-LOG.md). Kết quả:
- 44/69 PASS hoàn toàn
- 10 lỗi tài liệu phát hiện và **đã fix tại chỗ** (cp -i alias, BuildKit ID, Flask SIGTERM, IPAddress legacy, pkill missing, uppercase tag, buildx context, Kustomize commonLabels, Helm template snippet warning, ...)
- 15 SKIP-RUNTIME (Advanced 45-50 + 65-68 cần cluster ≥8GB RAM hoặc infra ngoài — YAML đã verify schema đúng)

---

## Audit gốc (v1.0.0)

## Kết luận nhanh

| Tiêu chí | Trạng thái |
|----------|------------|
| Tách 3 phần (Docker / K8s / Advanced) | ✅ Hoàn thành |
| Mỗi bài có prerequisite + checklist + kết quả mong đợi | ✅ (mặc định + một số bài đặc biệt) |
| Bảng **Lưu ý học viên** đầu mỗi file | ✅ |
| Placeholder `<your-username>` thống nhất | ✅ (thay bằng username thật khi làm) |
| Checklist markdown `- [ ]` | ✅ Đã sửa |
| Bản tổng hợp `docker-k8s-practice.md` | ✅ Giữ làm reference; khuyến nghị học từ 3 file tách |

**Đánh giá:** Tài liệu **đủ chuẩn để học** nếu đọc mục **📌 Lưu ý học viên** trước và làm tuần tự từng bài.

---

## Đã sửa trong đợt rà soát này

1. **Checklist** — từ `[ ]` sang `- [ ]` (hiển thị đúng trên GitHub / VS Code).
2. **Lỗi thường gặp** — message riêng từng phần (Docker không còn nhắc `kubectl` chung chung).
3. **Bảng lưu ý học viên** — thêm vào đầu `Docker/docker-practice.md`, `K8s/kubernetes-practice.md`, `Advanced/advanced-practice.md`.
4. **K8s Bài 26** — ghi rõ namespace `myapp-dev` dùng từ Bài 27 (tránh nhầm `dev`).
5. **K8s Bài 28** — bổ sung `-n myapp-dev`, mục **Lệnh thực hiện**, `kubectl cp` đúng cú pháp namespace.
6. **Docker Bài 23** — lưu ý build image trước `compose up`, `depends_on` không đợi DB ready.
7. **Advanced Bài 45** — lưu ý tải ArgoCD CLI bản macOS.
8. **Footer** — bỏ `---` trùng ở cuối file Docker.

---

## Hạn chế còn lại (chấp nhận được)

| # | Vấn đề | Ghi chú cho học viên |
|---|--------|----------------------|
| 1 | Nhiều bài **không có** mục riêng **Lệnh thực hiện** | Lệnh nằm trong **Yêu cầu chi tiết** — vẫn phải chạy đủ; xem lưu ý trong **Lỗi thường gặp** phần Docker. |
| 2 | **Kết quả mong đợi** generic ở bài 02–23, 25–26… | Đủ để tự kiểm; bài 01, 03, 10, 24, 27 có mô tả cụ thể hơn. Có thể bổ sung dần. |
| 3 | `docker-compose` vs `docker compose` | Ghi trong bảng lưu ý — không đổi toàn bộ đề để tránh lệch môi trường cũ. |
| 4 | Chart Helm Bitnami **version** trong đề Advanced | Version trên Hub thay đổi — học viên chọn version gần đúng, không bắt buộc khớp patch. |
| 5 | `hostPath` PV (K8s 34) | Chỉ chắc trên single-node; cluster thật cần StorageClass — đã ghi trong lưu ý. |
| 6 | Bài 41 / 50 — đề dự án lớn | Làm theo checklist trong đề; được phép nộp từng phần nếu GV cho phép (Advanced Bài 50). |

---

## Cách cập nhật tài liệu sau này

```bash
# Tách lại từ file gốc (nếu sửa docker-k8s-practice.md)
python3 scripts/split-practice-series.py

# Chuẩn hóa checklist + lưu ý học viên
python3 scripts/polish-practice-docs.py
```

Sau `split`, chạy `polish` để áp lại lưu ý và sửa checklist. Kiểm tra các bài đã chỉnh tay (Bài 01, 03 Docker; Bài 27 K8s) nếu regenerate.

---

## File tham chiếu

- [README.md](README.md) — lộ trình học
- [Docker/docker-practice.md](Docker/docker-practice.md) — Bài 01–24
- [K8s/kubernetes-practice.md](K8s/kubernetes-practice.md) — Bài 25–41
- [Advanced/advanced-practice.md](Advanced/advanced-practice.md) — Bài 42–50
