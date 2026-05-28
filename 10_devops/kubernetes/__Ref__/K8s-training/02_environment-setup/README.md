# Module 02 — Environment Setup (Cài Đặt Môi Trường)

> **Mục đích:** Setup môi trường K8s **miễn phí trên máy local** + hiểu **versioning** trước khi đi sâu hands-on.

---

## 📋 Metadata Module

- **Số bài:** 2
- **Tổng thời lượng video:** ~22 phút
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Prerequisites:** [Module 01 — Core Concepts](../01-core-concepts/README.md)

---

## 🗺️ Danh Sách Bài Học

| # | Bài Học | Mô Tả | Thời Lượng |
|---|---------|-------|------------|
| 01 | [Cài đặt Minikube, kubectl, Docker](01-cai-dat-minikube-kubectl-docker.md) | Setup môi trường local hoàn chỉnh | ~12 phút |
| 02 | [Kubernetes Versions & Skew Policy](02-kubernetes-version.md) | Format version, lifecycle 14 tháng, skew policy | ~10 phút |

---

## 🎯 Sau Module Này, Bạn Sẽ Có:

- ✅ **Cluster K8s chạy local** (Minikube) — sẵn sàng hands-on
- ✅ **Docker** + **kubectl** đã cài và validate
- ✅ Hiểu **format version** và **lifecycle support** 14 tháng
- ✅ Nắm **Version Skew Policy** giữa các component
- ✅ Biết verify version cluster của mình

---

## ✅ Checklist Trước Khi Vào Module 03

```bash
# Tất cả command này phải chạy thành công:
docker --version       # ✅
kubectl version --client  # ✅
minikube status        # ✅ (host: Running)
kubectl get nodes      # ✅ (minikube Ready)
kubectl get pods -A    # ✅ (thấy các Pod hệ thống)
```

---

## 🔗 Tiếp Theo

➡️ **[Module 03 — Pod & kubectl](../03-pod-and-kubectl/README.md)** (Bắt đầu hands-on với Pod, kubectl logs/exec)
