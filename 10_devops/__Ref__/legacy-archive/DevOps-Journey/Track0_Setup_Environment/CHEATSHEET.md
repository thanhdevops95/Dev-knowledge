# 📋 Cheatsheet

> **All important commands on one page**
>
> *Tất cả lệnh quan trọng trên một trang*

---

## 🔍 Verify Installation (Kiểm tra cài đặt)

### Quick Check - All Tools (Tất cả tools)

```bash
# Track 1
git --version
docker --version
docker compose version
code --version

# Track 2
kubectl version --client
minikube version
helm version

# Track 3
terraform --version
aws --version
ansible --version

# Track 4
trivy --version
hadolint --version
```

---

## 🐳 Docker Commands

### Images

```bash
docker images                    # List images (Liệt kê images)
docker pull nginx:alpine         # Download image (Tải image)
docker build -t myapp .          # Build image from Dockerfile (Build image từ Dockerfile)
docker rmi image_name            # Remove image (Xóa image)
docker image prune               # Remove unused images (Xóa images không dùng)
```

### Containers

```bash
docker ps                        # Running containers (Containers đang chạy)
docker ps -a                     # All containers (Tất cả containers)
docker run -d -p 80:80 nginx     # Run container (Chạy container)
docker stop container_id         # Stop container (Dừng container)
docker rm container_id           # Remove container (Xóa container)
docker exec -it container bash   # Enter container (Vào container)
docker logs container_id         # View logs (Xem logs)
```

### Docker Compose

```bash
docker compose up -d             # Start services (Khởi động services)
docker compose down              # Stop and remove (Dừng và xóa)
docker compose logs -f           # Follow logs (Theo dõi logs)
docker compose ps                # List services (Liệt kê services)
docker compose build             # Rebuild images (Build lại images)
```

### Cleanup (Dọn dẹp)

```bash
docker system prune              # Remove unused resources (Xóa resources không dùng)
docker system prune -a           # Remove all unused images (Xóa tất cả images không dùng)
docker volume prune              # Remove unused volumes (Xóa volumes không dùng)
```

---

## 📦 Git Commands

### Basic (Cơ bản)

```bash
git init                         # Initialize repo (Khởi tạo repo)
git clone <url>                  # Clone repo
git status                       # Check status (Xem trạng thái)
git add .                        # Stage all (Stage tất cả)
git commit -m "message"          # Commit
git push origin main             # Push to remote (Push lên remote)
git pull origin main             # Pull from remote (Pull từ remote)
```

### Branches

```bash
git branch                       # List branches (Liệt kê branches)
git branch feature-x             # Create branch (Tạo branch)
git checkout feature-x           # Switch branch (Chuyển branch)
git checkout -b feature-x        # Create and switch (Tạo và chuyển)
git merge feature-x              # Merge branch (Hợp nhất branch)
git branch -d feature-x          # Delete branch (Xóa branch)
```

### Undo (Hoàn tác)

```bash
git restore file.txt             # Discard changes (Bỏ thay đổi)
git restore --staged file.txt    # Unstage file (Bỏ stage)
git reset --soft HEAD~1          # Undo commit keep changes (Giữ changes)
git reset --hard HEAD~1          # Undo commit delete changes (Xóa changes)
```

### Remote (GitLab/GitHub)

```bash
# GitLab (Primary - Chính)
git remote add origin git@gitlab.com:user/repo.git
ssh -T git@gitlab.com            # Test connection (Kiểm tra kết nối)

# GitHub (Alternative - Thay thế)
git remote add origin git@github.com:user/repo.git
ssh -T git@github.com            # Test connection (Kiểm tra kết nối)
```

---

## ☸️ Kubernetes Commands

### Cluster

```bash
minikube start                   # Start cluster (Khởi động cluster)
minikube stop                    # Stop cluster (Dừng cluster)
minikube delete                  # Delete cluster (Xóa cluster)
minikube dashboard               # Open dashboard (Mở dashboard)
```

### kubectl Basics

```bash
kubectl get pods                 # List pods (Liệt kê pods)
kubectl get services             # List services (Liệt kê services)
kubectl get deployments          # List deployments (Liệt kê deployments)
kubectl get all                  # List all resources (Liệt kê tất cả)
kubectl get all -A               # All namespaces (Tất cả namespaces)
```

### kubectl Operations

```bash
kubectl apply -f file.yaml       # Apply manifest (Áp dụng manifest)
kubectl delete -f file.yaml      # Delete resources (Xóa resources)
kubectl describe pod pod-name    # Pod details (Chi tiết pod)
kubectl logs pod-name            # View logs (Xem logs)
kubectl exec -it pod-name -- sh  # Enter pod shell (Vào shell pod)
kubectl port-forward pod 8080:80 # Forward port
```

### Helm

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update                 # Update repos (Cập nhật repos)
helm search repo nginx           # Search charts (Tìm charts)
helm install my-app bitnami/nginx  # Install chart (Cài đặt chart)
helm list                        # List releases (Liệt kê releases)
helm uninstall my-app            # Uninstall (Gỡ cài đặt)
```

---

## 🏗️ Terraform Commands

```bash
terraform init                   # Initialize (Khởi tạo)
terraform fmt                    # Format code (Định dạng code)
terraform validate               # Validate syntax (Xác thực)
terraform plan                   # Preview changes (Xem trước)
terraform apply                  # Apply changes (Áp dụng)
terraform apply -auto-approve    # Apply without prompt (Không hỏi)
terraform destroy                # Destroy resources (Xóa resources)
terraform state list             # List state (Liệt kê state)
terraform output                 # Show outputs (Xem outputs)
```

---

## ☁️ AWS CLI Commands

### Configuration (Cấu hình)

```bash
aws configure                    # Configure credentials (Cấu hình)
aws sts get-caller-identity      # Check identity (Kiểm tra identity)
```

### EC2

```bash
aws ec2 describe-instances       # List instances (Liệt kê instances)
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
```

### S3

```bash
aws s3 ls                        # List buckets (Liệt kê buckets)
aws s3 ls s3://bucket-name       # List objects (Liệt kê objects)
aws s3 cp file.txt s3://bucket/  # Upload file
aws s3 sync ./folder s3://bucket/ # Sync folder
```

---

## 🔒 Security Tools (Công cụ bảo mật)

### Trivy

```bash
trivy image nginx:latest         # Scan image (Quét image)
trivy image --severity HIGH,CRITICAL nginx
trivy fs .                       # Scan filesystem (Quét filesystem)
trivy config .                   # Scan IaC files (Quét IaC)
```

### Hadolint

```bash
hadolint Dockerfile              # Lint Dockerfile
hadolint --ignore DL3008 Dockerfile  # Ignore rule (Bỏ qua rule)
```

---

## 🔄 GitLab CI Commands (Lệnh GitLab CI)

```bash
# View pipeline status (Xem trạng thái pipeline)
# GitLab UI > CI/CD > Pipelines

# GitLab Runner (Local)
gitlab-runner exec docker job_name  # Run job locally

# Validate .gitlab-ci.yml
# GitLab UI > CI/CD > Editor > Validate
```

---

## 🔧 Useful Shortcuts (Phím tắt hữu ích)

### VS Code Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command Palette |
| `Ctrl+`` ` | Toggle Terminal |
| `Ctrl+B` | Toggle Sidebar |
| `Ctrl+Shift+E` | Explorer |
| `Ctrl+Shift+G` | Git |
| `Ctrl+Shift+F` | Search in files |

### Terminal Shortcuts (Bash)

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel command |
| `Ctrl+L` | Clear screen |
| `Ctrl+R` | Search history |
| `Tab` | Auto-complete |
| `!!` | Run last command |
| `!$` | Last argument |

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| **GitLab** | <https://gitlab.com> |
| **GitHub** | <https://github.com> |
| Docker Hub | <https://hub.docker.com/> |
| Kubernetes Docs | <https://kubernetes.io/docs/> |
| Terraform Registry | <https://registry.terraform.io/> |
| AWS Console | <https://console.aws.amazon.com/> |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [Troubleshooting](./TROUBLESHOOTING.md) | **Cheatsheet** | [README](./README.md) |

---

*Last Updated: 2025-12-30*

*Cập nhật lần cuối: 2025-12-30*
