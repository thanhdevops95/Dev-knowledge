# Bài 25 — Cài đặt cluster K8s

> **Tiên quyết:** đã có image `<your-username>/myapp:6.0` trên Docker Hub (Bài 24).
> **Lưu ý:** trong tất cả manifest từ Bài 27 trở đi, thay `<your-username>` bằng username Docker Hub thật.

## Lệnh thủ công

### Cách 1 — Minikube (khuyến nghị)

```bash
minikube start --driver=docker
minikube status
```

### Cách 2 — Kind

```bash
kind create cluster --name myapp-cluster
```

### Cách 3 — Docker Desktop

Settings → Kubernetes → tick **Enable Kubernetes** → Apply & Restart.

### Verify (cách nào cũng được)

```bash
kubectl version
kubectl cluster-info
kubectl get nodes              # STATUS: Ready
kubectl get pods -A            # tất cả system pod Running
```

### Cài autocomplete (tùy chọn)

```bash
# bash
source <(kubectl completion bash)
echo 'alias k=kubectl' >> ~/.bashrc

# zsh
source <(kubectl completion zsh)
echo 'alias k=kubectl' >> ~/.zshrc
```

## Kết quả mong đợi

```
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   2m     v1.xx.x
```

## Bài kế tiếp

```bash
cp -r ../25-cluster-setup ../26-namespace
cd ../26-namespace
```
