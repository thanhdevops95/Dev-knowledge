# Module 07 — Deployment (10 bài)

> 🎯 **Module quan trọng nhất** — Deployment là tài nguyên dùng nhiều nhất trong K8s production.

---

## 📋 Mục Tiêu Module

Sau module này, bạn sẽ:

- ✅ Tạo Deployment bằng Imperative + Declarative
- ✅ Hiểu mối quan hệ Deployment → ReplicaSet → Pod
- ✅ Thực hiện Rolling Update an toàn (no down-time)
- ✅ Rollback về phiên bản trước chỉ với 1 lệnh
- ✅ Phân biệt Recreate vs RollingUpdate strategy
- ✅ Cấu hình `progressDeadlineSeconds`, `maxSurge`, `maxUnavailable`
- ✅ Quản lý revision: change-cause, history, restart

---

## 📚 Danh Sách Bài

| # | Bài | Cấp độ | Thời lượng |
|---|-----|--------|------------|
| #20 | [Create Deployment (Imperative & Declarative)](01-create-deployment.md) | INTERMEDIATE | ~7' |
| #21 | [Scale & Expose Deployment](02-scale-expose-deployment.md) | INTERMEDIATE | ~6' |
| #22 | [Set Container Image](03-set-image.md) | INTERMEDIATE | ~5' |
| #23 | [Rollout Deployment](04-rollout-deployment.md) | INTERMEDIATE | ~6' |
| #24 | [Rollback Deployment](05-rollback-deployment.md) | INTERMEDIATE | ~5' |
| #25 | [Pause & Resume Deployment](06-pause-resume.md) | INTERMEDIATE | ~5' |
| #26 | [Change Cause (Annotation)](07-change-cause.md) | INTERMEDIATE | ~4' |
| #27 | [Recreate vs RollingUpdate](08-deployment-strategies.md) | INTERMEDIATE | ~10' |
| #28 | [Progress Deadline](09-progress-deadline.md) | INTERMEDIATE | ~6' |
| #29 | [Restart Deployment](10-restart-deployment.md) | INTERMEDIATE | ~3' |

**Tổng thời lượng:** ~57 phút

---

## 🗺️ Sơ Đồ Khái Niệm

```
                  ┌───────── Deployment ─────────┐
                  │                              │
        Bài #20 = │  Tạo Deployment + Pod template │
                  │                              │
                  │  ┌──── ReplicaSet (active) ────┐
                  │  │                             │
                  │  │   ┌── Pod ─┐ ┌── Pod ─┐      │
                  │  │   └────────┘ └────────┘      │
                  │  └─────────────────────────────┘
                  │                              │
                  │  ┌──── ReplicaSet (history)───┐
                  │  │  scale: 0  (giữ rollback)  │
                  │  └─────────────────────────────┘
                  └──────────────────────────────┘

  Bài #21: Scale + Expose
  Bài #22: Update image → tạo RS mới
  Bài #23: Theo dõi rollout
  Bài #24: Rollback ← quay về RS cũ
  Bài #25: Pause/Resume → gom thay đổi
  Bài #26: Change-cause cho mỗi revision
  Bài #27: Strategy = cách tạo Pod mới
  Bài #28: Progress deadline = timeout
  Bài #29: Restart → tạo RS mới (cùng image)
```

---

## 🎯 Bài Quan Trọng Nhất

🔥 **Bài #20** — Cấu trúc Deployment (nền tảng)
🔥 **Bài #24** — Rollback (cứu cánh production)
🔥 **Bài #27** — Strategies (chọn đúng cho production)

---

## 🔗 Navigation

- ⬅️ Module trước: [06-replicaset](../06-replicaset/README.md)
- ➡️ Module tiếp: [08-services](../08-services/README.md)
- 🏠 [Quay về trang chính](../README.md)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
