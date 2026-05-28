# 🛠️ Minikube — User Guide

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 19/05/2026\
> **Cập nhật:** 19/05/2026\
> **Loại:** Tool individual — focused on Minikube\
> **Đọc trước:** [So sánh K8s local options](./00_local-k8s-options.md) (nếu chưa chọn xong)

> 🎯 *Bài này CHỈ về Minikube — cài, dùng UI/CLI, addon, cấu hình khuyến nghị, troubleshoot. KHÔNG so sánh với Kind/k3d (đã có ở file category).*

---

## Vậy Minikube là gì?

Minikube là **K8s cluster 1-node chạy trong VM hoặc container trên máy bạn**. Open source từ 2016 dưới CNCF, hiện thuộc Kubernetes SIG.

🪞 **Ẩn dụ**: nếu K8s production là *cả 1 chung cư*, Minikube là *căn hộ 1 phòng* — đủ giường, bếp, toa-lét, nhưng nhỏ gọn, mở khoá 30 giây là dùng được.

---

## Khi nào pick Minikube?

✅ Pick khi:
- Mới học K8s, muốn UI Dashboard built-in
- Cần nhiều addon (Ingress, Registry, GPU, metrics-server) bật bằng 1 lệnh
- Beginner-friendly nhất, cộng đồng support nhiều

❌ Không pick khi:
- Chạy CI test (Kind nhanh hơn)
- Hardware yếu < 2GB RAM (k3d nhẹ hơn)

→ So sánh chi tiết với Kind/k3d → [00_local-k8s-options.md](./00_local-k8s-options.md).

---

## Cài đặt

### macOS (M1/M2/M3 + Intel)

```bash
brew install minikube
```

### Linux (Ubuntu/Debian)

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Windows

```powershell
choco install minikube
# hoặc qua winget
winget install minikube
```

### Verify

```bash
minikube version
```

Kết quả mong đợi: `minikube version: v1.32.0` (hoặc mới hơn).

---

## Khởi cluster đầu tiên

```bash
minikube start
```

Lệnh này tự:
1. Tải image K8s phù hợp
2. Tạo VM (default driver tuỳ OS)
3. Cài kubelet, kube-proxy, etcd, scheduler, controller
4. Setup kubectl context

Verify:

```bash
kubectl get nodes
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   60s   v1.28.3
```

### Driver — chọn engine chạy cluster

Minikube có thể chạy trên nhiều backend:

| Driver | OS | Đặc điểm |
|---|---|---|
| `docker` ⭐ | Đa nền tảng | Nhanh, không cần VM, **default mới** |
| `hyperkit` | macOS Intel | Native Mac VM (deprecated) |
| `qemu` | macOS M-series | Default cho M1/M2/M3 nếu không có Docker |
| `virtualbox` | Đa nền tảng | Universal, chậm hơn |
| `kvm2` | Linux | Native KVM |
| `hyperv` | Windows | Built-in Windows Pro |

Chọn driver:

```bash
minikube start --driver=docker
```

> 💡 Lần đầu chạy chưa rõ → cứ `minikube start` không cờ. Minikube tự pick driver tối ưu cho OS bạn.

---

## UI Tour — `minikube dashboard`

Lệnh:

```bash
minikube dashboard
```

→ Tự mở browser ở `http://127.0.0.1:port`. Dashboard có:

| Panel | Hiển thị |
|---|---|
| **Workloads** | Deployments, Pods, ReplicaSets, Jobs, CronJobs |
| **Services & Networking** | Services, Ingresses, Endpoints |
| **Config & Storage** | ConfigMaps, Secrets, PVC, StorageClasses |
| **Cluster** | Nodes, Namespaces, Events, Roles |
| **Custom Resources** | CRDs đã cài |

Mỗi resource click vào sẽ thấy:
- YAML manifest (có thể edit inline)
- Logs (cho Pod)
- Events
- Exec shell (cho Pod)

> 📌 Dashboard chỉ là UI cho `kubectl` — không có gì kubectl không làm được. Nhưng visual hơn nhiều cho beginner.

---

## Addon — siêu năng lực của Minikube

Addon là feature có thể bật/tắt bằng 1 lệnh. Đây là chỗ Minikube vượt trội Kind/k3d.

### List addon

```bash
minikube addons list
```

Kết quả (rút gọn):

```
|-----------------------------|----------|--------------|
|         ADDON NAME          | PROFILE  |    STATUS    |
|-----------------------------|----------|--------------|
| dashboard                   | minikube | enabled ✅    |
| ingress                     | minikube | disabled     |
| ingress-dns                 | minikube | disabled     |
| metrics-server              | minikube | disabled     |
| registry                    | minikube | disabled     |
| storage-provisioner         | minikube | enabled ✅    |
| ...                         |          |              |
```

### Addon nên bật cho học K8s

```bash
minikube addons enable ingress         # NGINX Ingress Controller
minikube addons enable metrics-server  # cho HPA + kubectl top
minikube addons enable registry        # local image registry
minikube addons enable dashboard       # web UI (đã default)
```

### Addon advanced

| Addon | Khi dùng |
|---|---|
| `gpu` | Test workload GPU (NVIDIA) |
| `istio-provisioner` | Học service mesh Istio |
| `volumesnapshots` | Test snapshot PVC |
| `csi-hostpath-driver` | Test CSI driver |
| `ambassador` | Học Ambassador gateway |

---

## Cấu hình khuyến nghị

### Profile cho beginner

```bash
minikube start \
  --cpus=2 \
  --memory=4096 \
  --disk-size=20g \
  --kubernetes-version=v1.28.3 \
  --addons=ingress,metrics-server,dashboard
```

### Profile cho dev mạnh (M2/M3 16GB+)

```bash
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --nodes=3 \
  --kubernetes-version=v1.29.0 \
  --addons=ingress,metrics-server,dashboard,registry
```

→ `--nodes=3` tạo cluster 3 node (1 control plane + 2 worker) — giả lập production.

### Lưu profile vào config

```bash
minikube config set memory 4096
minikube config set cpus 2
minikube config set driver docker
```

Sau đó `minikube start` không cần cờ nữa.

---

## Workflows phổ biến

### 1. Load image local vào cluster

Build image trên Mac, muốn dùng trong cluster:

```bash
# Cách 1: dùng Docker daemon của Minikube
eval $(minikube docker-env)
docker build -t myapp:dev .

# Cách 2: load image qua minikube
minikube image load myapp:dev
```

### 2. Expose Service ra host

```bash
kubectl expose deployment myapp --type=NodePort --port=8080
minikube service myapp
```

→ Tự mở browser ở URL tunnel.

### 3. Tunnel LoadBalancer

```bash
minikube tunnel
```

(chạy ở terminal khác — cần sudo)

→ Service type `LoadBalancer` có EXTERNAL-IP truy cập được.

### 4. SSH vào Minikube node

```bash
minikube ssh
```

### 5. Multi-cluster (profile)

```bash
minikube start -p cluster-2
kubectl config get-contexts
kubectl config use-context cluster-2
```

---

## Shortcut + lệnh hay dùng

| Lệnh | Mục đích |
|---|---|
| `minikube start` | Khởi cluster |
| `minikube stop` | Tạm dừng (giữ state) |
| `minikube delete` | Xoá hẳn |
| `minikube status` | Trạng thái |
| `minikube ip` | IP cluster |
| `minikube dashboard` | Mở web UI |
| `minikube tunnel` | Expose LoadBalancer |
| `minikube ssh` | SSH vào node |
| `minikube addons list` | List addon |
| `minikube logs` | Xem log Minikube |
| `minikube image load <img>` | Load image local |
| `minikube pause` | Pause workload |
| `minikube unpause` | Tiếp tục |

---

## Troubleshooting

### ❌ `Exiting due to DRV_AS_ROOT: ...`

→ Đừng chạy `sudo minikube start`. Chạy với user thường.

### ❌ Cluster lên rồi nhưng `kubectl get nodes` timeout

```bash
minikube status
# Nếu Stopped → minikube start lại
# Nếu Running nhưng kube-apiserver Unreachable → minikube delete && start
```

### ❌ Ingress addon enable nhưng URL không access được

```bash
# Đảm bảo đã chạy:
minikube tunnel
# Hoặc dùng NodePort thay vì Ingress khi học
```

### ❌ Image không pull được trong cluster

→ Có thể trong company VPN/firewall. Dùng `--image-mirror-country=cn` (mirror) hoặc cấu hình proxy.

### ❌ Mac M-series chậm

→ Pick driver `qemu` thay `docker` nếu Docker Desktop tốn RAM. Hoặc dùng [OrbStack](https://orbstack.dev) thay Docker Desktop.

---

## 📦 Repo + tài nguyên hữu ích

| Repo / Link | Khi dùng |
|---|---|
| [kubernetes/minikube](https://github.com/kubernetes/minikube) | Source + issue tracker |
| [Minikube docs](https://minikube.sigs.k8s.io/docs/) | Official |
| [Minikube tutorials](https://minikube.sigs.k8s.io/docs/tutorials/) | Hands-on từ team chính |
| [Awesome Minikube](https://github.com/topics/minikube) | Bộ sưu tập tool kèm |

---

## 🔗 Liên kết

- 🛠️ So sánh với Kind/k3d → [00_local-k8s-options.md](./00_local-k8s-options.md)
- 📚 Bài lesson K8s → [10_devops/kubernetes/lessons/01_basic/00_what-is-k8s.md](../../10_devops/kubernetes/lessons/01_basic/00_what-is-k8s.md)
- 🛠️ GUI quản lý cluster → [Lens](../k8s-gui/lens.md) (chưa có)
- 🛠️ TUI quản lý → [k9s](../k8s-cli/k9s.md) (chưa có)

---

## 📌 Changelog

- **v1.0.0 (19/05/2026)** — Bản đầu tiên. Cài + start + UI + addon + workflow + troubleshoot. Mac/Linux/Win.
