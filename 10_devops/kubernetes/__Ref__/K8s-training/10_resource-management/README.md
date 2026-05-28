# Module 10 — Resource Management (6 bài)

> 🎯 Module **CUỐI** — quản lý CPU/Memory hiệu quả + multi-tenant.

---

## 📋 Mục Tiêu Module

- ✅ Cấu hình `requests` / `limits` cho container
- ✅ Hiểu best practices CPU/Memory (3 rule vàng)
- ✅ Override `command` / `args`
- ✅ Enable Metrics Server để monitor
- ✅ ResourceQuota để giới hạn namespace
- ✅ LimitRange để default + min/max

---

## 📚 Danh Sách Bài

| # | Bài | Cấp độ | Thời lượng |
|---|-----|--------|------------|
| #35 | [Requests & Limits](01-requests-limits.md) | INTERMEDIATE | ~12' |
| #36 | [Best Practices Requests/Limits](02-best-practices-requests-limits.md) | ADVANCED | ~10' |
| #37 | [Command & Args](03-command-args.md) | INTERMEDIATE | ~7' |
| #38 | [Metrics Server](04-metrics-server.md) | INTERMEDIATE | ~7' |
| #39 | [Resource Quotas](05-resource-quotas.md) | ADVANCED | ~10' |
| #40 | [Limit Ranges](06-limit-ranges.md) | ADVANCED | ~9' |

**Tổng:** ~55 phút

---

## 🗺️ Sơ Đồ Khái Niệm

```
                    Resource Management
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   Per-Container        Per-Namespace      Monitoring
                                                │
   Bài #35: req/lim      Bài #39: Quota    Bài #38:
   Bài #36: best pract.  Bài #40: LimitRng Metrics Srv
   Bài #37: cmd/args
```

---

## 🎯 3 Rule Vàng (Bài #36)

1. 🔥 **KHÔNG set CPU Limit** (CPU compressible)
2. 🔥 **LUÔN set CPU Request**
3. 🔥 **Memory: Request = Limit**

---

## 🔗 Navigation

- ⬅️ Module trước: [09-namespace](../09-namespace/README.md)
- 🏠 [Quay về trang chính](../README.md)

---

## 🎉 Hoàn Tất Series 40 Bài!

```
✅ Module 00: Introduction        ✅ Module 06: ReplicaSet
✅ Module 01: Core Concepts       ✅ Module 07: Deployment
✅ Module 02: Environment Setup   ✅ Module 08: Services
✅ Module 03: Pod & kubectl       ✅ Module 09: Namespace
✅ Module 04: Expose Pod          ✅ Module 10: Resource Mgmt
✅ Module 05: Imperative vs Decl.
```

🎓 **Chúc mừng!** Bạn đã hoàn thành kiến thức nền tảng Kubernetes.

---

**Tác giả:** Mr.Rom
**Ngày tạo:** 09/05/2026
