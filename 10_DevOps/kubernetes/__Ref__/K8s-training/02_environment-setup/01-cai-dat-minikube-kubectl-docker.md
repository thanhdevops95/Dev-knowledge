# Bài #6 — Cài Đặt Minikube, kubectl, Docker (Môi Trường Học K8s Miễn Phí)

> 🎯 **Hands-On bắt đầu từ đây!** Sau bài này bạn sẽ có 1 cluster K8s chạy trên máy mình, hoàn toàn miễn phí.

---

## 📋 Metadata

- **Bài số:** #6
- **Module:** 02-environment-setup
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~12 phút
- **Prerequisites:** [Module 01 — Core Concepts](../01-core-concepts/README.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ có:

- [ ] **Docker** chạy trên máy local (chạy container)
- [ ] **kubectl** (CLI tương tác với cluster K8s)
- [ ] **Minikube** (cluster K8s mini chạy local) — đã start thành công
- [ ] **Docker Hub account** (tùy chọn nhưng nên có)
- [ ] Hiểu sự khác nhau **Minikube vs Kind**

---

## 📚 Nội Dung

### 1. Cần Cài Gì? Tại Sao?

```
┌─────────────────────────────────────────────────────────────┐
│                       MÁY LOCAL CỦA BẠN                       │
│                                                              │
│   ┌─────────────────────┐    ┌─────────────────────┐         │
│   │   Docker Engine     │    │      kubectl         │         │
│   │   (chạy container)  │    │  (CLI gọi cluster)   │         │
│   └─────────────────────┘    └────────┬────────────┘         │
│             ▲                          │                      │
│             │ chạy bên dưới            │ HTTPS                │
│             │                          ▼                      │
│   ┌─────────────────────────────────────────────────┐         │
│   │             Minikube Cluster                     │         │
│   │  (mini K8s — Control Plane + 1 Node)             │         │
│   └─────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

| Tool                   | Vai trò                             | Bắt buộc?     |
| ---------------------- | ----------------------------------- | ------------- |
| **Docker**             | Container runtime để chạy container | ✅             |
| **kubectl**            | CLI tương tác với mọi cluster K8s   | ✅             |
| **Minikube**           | Cluster K8s local                   | ✅ (hoặc Kind) |
| **Kind**               | Alternative cho Minikube            | Tùy chọn      |
| **Docker Hub account** | Lưu image của bạn                   | Khuyến nghị   |

---

### 2. Bước 1: Cài Docker Engine

Hỗ trợ cả **macOS, Linux, Windows** (kể cả Apple Silicon M1/M2/M3).

#### macOS

```bash
# Cách 1: Tải Docker Desktop từ web
open https://www.docker.com/products/docker-desktop/

# Cách 2: Homebrew
brew install --cask docker
```

#### Linux (Ubuntu/Debian)

```bash
curl -fsSL https://get.docker.com | bash
sudo usermod -aG docker $USER  # Thêm user vào docker group
# Logout/login lại để áp dụng
```

#### Windows

Tải **Docker Desktop for Windows** từ [docker.com](https://www.docker.com/products/docker-desktop/).

#### Yêu cầu hệ thống

- Tối thiểu **4 GB RAM**
- Apple Silicon (M1/M2/M3) đã được hỗ trợ ổn định

#### Validate

```bash
docker --version
# Output: Docker version 25.0.3, build XXX

docker images
# Output: hiện danh sách image (có thể trống)

docker ps
# Output: hiện container đang chạy
```

---

### 3. Bước 2: Tạo Docker Hub Account (khuyến nghị)

[https://hub.docker.com](https://hub.docker.com) — đăng ký tài khoản miễn phí.

**Lợi ích:**
- Lưu image của bạn để pull từ bất kỳ máy nào
- Đặt **alias name** sớm để dùng dài lâu (vd: `mrrom/myapp`)

> 💡 Alternative: AWS ECR, GitHub Container Registry, Quay.io…

#### Test chạy 1 container

```bash
docker run -p 8081:8080 -d mrrom/web-app:v1
docker ps
docker logs <container_id>

# Truy cập: http://localhost:8081
```

> 📝 Bài #6 gốc có nhắc tới image `mrrom/web-app` của giảng viên — bạn có thể dùng image bất kỳ để test, vd: `nginx`.

---

### 4. Bước 3: Cài kubectl

`kubectl` (đọc là **"kube-control"** hoặc **"kube-c-t-l"**) — CLI để gọi K8s cluster.

#### macOS

```bash
# Cách 1: Homebrew (đơn giản)
brew install kubectl

# Cách 2: Native binary (recommended bởi docs chính thức)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
```

#### Linux

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

#### Windows

```powershell
# Chocolatey
choco install kubernetes-cli

# Hoặc tải binary từ: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

#### Validate

```bash
kubectl version --client
# Output: Client Version: v1.29.x
```

---

### 5. Bước 4: Cài Minikube

Có 2 lựa chọn local cluster: **Minikube** và **Kind**. Series này dùng **Minikube** (đẹp, document trực quan hơn).

#### macOS

```bash
# Homebrew
brew install minikube

# Native binary (Apple Silicon)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
```

#### Linux

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

#### Yêu cầu hệ thống

- 2 CPU cores
- 2 GB RAM (recommend 4GB+)
- 20 GB disk
- Internet connection

---

### 6. Bước 5: Start Cluster Đầu Tiên

```bash
# Khởi động Minikube với version K8s mặc định
minikube start

# Hoặc chỉ định version cụ thể
minikube start --kubernetes-version=v1.32.0

# Lần đầu chạy: pull base image của Minikube — sẽ chậm (~1-2 phút)
# Lần sau: rất nhanh
```

**Output kỳ vọng:**

```
😄  minikube v1.32.0 on Darwin
🆕  Kubernetes 1.29.0 is now available...
✨  Automatically selected the docker driver
📌  Using Docker Desktop driver with root privileges
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass
🏄  Done! kubectl is now configured to use "minikube"
```

#### Verify cluster

```bash
# Status của cluster
minikube status
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

# Lấy danh sách Node
kubectl get nodes
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   1m    v1.28.3

# Liệt kê tất cả Pod (kể cả trong namespace hệ thống)
kubectl get pods -A
# Sẽ thấy: coredns, etcd, kube-apiserver, kube-controller-manager,
# kube-proxy, kube-scheduler, storage-provisioner...
```

> 🎉 **Cluster K8s đầu tiên của bạn đã chạy!** Đó là 7 component bạn vừa học ở Bài #4.

---

### 7. Minikube Dashboard (UI trực quan)

```bash
minikube dashboard
```

Một browser sẽ tự động mở với UI dashboard của Minikube — xem Pod, Deployment, Service…

> 💡 **Lưu ý:** Trong thực tế bạn sẽ dùng `kubectl` (CLI) **nhiều hơn** dashboard. Dashboard chỉ giúp lúc mới bắt đầu cho dễ nhìn.

---

### 8. Useful Minikube Commands

```bash
minikube start                      # Start cluster
minikube stop                       # Stop (giữ data)
minikube delete                     # Xóa hoàn toàn
minikube status                     # Trạng thái
minikube dashboard                  # UI
minikube ssh                        # SSH vào VM của Minikube
minikube ip                         # IP của Minikube
minikube addons list                # Xem addon có sẵn
minikube addons enable metrics-server  # Bật addon
```

---

## 💻 Hands-On Đầy Đủ

```bash
# 1. Verify Docker
docker --version
docker ps

# 2. Verify kubectl
kubectl version --client

# 3. Start Minikube
minikube start

# 4. Verify cluster
kubectl get nodes
kubectl get pods -A

# 5. Tạo Pod test đầu tiên (chuẩn bị cho Bài #8)
kubectl run hello-pod --image=nginx --port=80
kubectl get pods
# NAME        READY   STATUS    RESTARTS   AGE
# hello-pod   1/1     Running   0          15s

# 6. Cleanup
kubectl delete pod hello-pod
```

---

## ⚠️ Lưu Ý

- 🐢 **Lần đầu start Minikube** sẽ chậm vì pull base image. Lần sau nhanh hơn nhiều.
- 💾 **Đảm bảo có ít nhất 4GB RAM** trống. Docker Desktop chạy nặng.
- 🔄 **Nếu start fail**, thử `minikube delete` rồi `minikube start` lại.
- 🌐 Nếu network bị block, có thể dùng option `--driver=docker` hoặc `--driver=virtualbox`.
- ✅ **Trên macOS với Apple Silicon (M1/M2/M3):** chọn binary `arm64`, KHÔNG chọn `amd64`.
- ⚡ **Khuyến nghị Minikube hơn Kind** cho người mới bắt đầu (tài liệu trực quan hơn).

---

## ✅ Self-Check

1. **Vì sao cần `kubectl` và `minikube` trên cùng 1 máy?**
   <details>
   <summary>Đáp án</summary>
   - **Minikube** tạo cluster K8s
   - **kubectl** là CLI để bạn ra lệnh cho cluster đó
   Hai cái khác nhau nhưng dùng chung.
   </details>

2. **Câu lệnh nào hiển thị tất cả Pod kể cả Pod hệ thống?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl get pods -A
   # hoặc
   kubectl get pods --all-namespaces
   ```

   </details>

3. **Sau khi `minikube start`, Pod nào của Control Plane bạn sẽ thấy?**
   <details>
   <summary>Đáp án</summary>
   - `kube-apiserver`
   - `etcd`
   - `kube-controller-manager`
   - `kube-scheduler`
   - `kube-proxy`
   - `coredns`
   - `storage-provisioner`
   </details>

4. **Apple Silicon (M1) thì dùng binary nào?**
   <details>
   <summary>Đáp án</summary>
   `arm64` (không phải `amd64`/`x86_64`).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #4 — Cluster Architecture](../01-core-concepts/03-cluster-architecture.md)
- ➡️ [Bài #7 — Kubernetes Versions](02-kubernetes-version.md)

### Tài Nguyên

- 📖 [Minikube Official Install](https://minikube.sigs.k8s.io/docs/start/)
- 📖 [Install kubectl](https://kubernetes.io/docs/tasks/tools/)
- 📖 [Docker Install](https://docs.docker.com/get-docker/)
- 📖 [Kind (Alternative)](https://kind.sigs.k8s.io/)
- 📺 Video gốc: `Decopy_✅ #6 _ Hướng Dẫn Cài Đặt Minikube..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Trên Tutorial người ta làm rất nhanh, multi rất lẹ — vì người ta làm chuyện này rất nhiều lần rồi. Các bạn lần đầu có thể chậm là chuyện bình thường."*

> 💬 *"Mình recommend các bạn cài thông qua **binary** thay vì Homebrew — vì sau này khi cài thêm `eksctl`, `awscli` của AWS thì cũng dùng binary."*

> 💬 *"Dashboard của Minikube cũng dành cho thời gian các bạn tò mò ngó nghít thôi. Sau này các bạn sẽ chủ yếu làm trên terminal nhiều hơn — vì gõ command nhanh hơn rất nhiều."*

> 💬 *"Trong bài tiếp theo mình sẽ tìm hiểu để dựng 1 cluster có thêm 2 Worker Node — để các bạn thấy môi trường nó thực tế hơn."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
