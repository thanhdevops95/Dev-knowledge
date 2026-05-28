# GIAI ĐOẠN 8: GITLAB CD - TRIỂN KHAI TỰ ĐỘNG

## 📌 MỤC TIÊU GIAI ĐOẠN 8
Sau khi CI đã build và push image mới lên Docker Hub, bước tiếp theo là CD (Continuous Deployment):
1. SSH vào Server Production.
2. Pull Image mới nhất về.
3. Restart lại các container (dùng Docker Compose).

---

## 🛠️ PHẦN 1: TẠO FILE DEPLOY SCIPT

Trong thực tế, ta cần file `docker-compose.yaml` nằm trên Server.
Bạn có thể copy thủ công, hoặc để CD tự copy. Ở đây ta dùng cách đơn giản: **SCP** (Secure Copy) file yaml lên trước rồi mới chạy lệnh.

### Cập nhật `.gitlab-ci.yml`
Thêm stage `deploy` và job mới vào cuối file:

```yaml
stages:
  - lint
  - build-push
  - deploy # <--- Thêm stage này

# ... (Các phần trước giữ nguyên)

# --- STAGE 3: DEPLOY (CD) ---
deploy-to-server:
  stage: deploy
  image: alpine:latest
  before_script:
    # 1. Cài ssh-agent và client
    - apk add --no-cache openssh-client
    
    # 2. Chạy ssh-agent
    - eval $(ssh-agent -s)
    
    # 3. Thêm Private Key vào agent (Set permission 600 cho key trước)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' > id_rsa
    - chmod 600 id_rsa
    - ssh-add id_rsa
    
    # 4. Tắt check Host Key (để đỡ hỏi Yes/No lần đầu)
    - mkdir -p ~/.ssh
    - echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

  script:
    - echo "Deploying to $SSH_HOST..."
    
    # Copy file docker-compose lên server
    - scp docker-compose.yaml $SSH_USER@$SSH_HOST:/root/todo-app/
    
    # SSH vào và chạy commands
    - |
      ssh $SSH_USER@$SSH_HOST "
        cd /root/todo-app
        
        # Cập nhật biến môi trường cho Compose biết dùng Image Tag nào
        export GO_IMAGE=$DOCKER_USER/todo-go
        export PYTHON_IMAGE=$DOCKER_USER/todo-python
        export IMAGE_TAG=$CI_COMMIT_SHORT_SHA
        
        # Login Docker Hub trên Server (để pull image private nếu cần)
        # echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
        
        # Pull và Up lại
        docker compose pull
        docker compose up -d --remove-orphans
      "
```

⚠️ **Lưu ý quan trọng**:
File `docker-compose.yaml` gốc của chúng ta đang fix cứng version (ví dụ `image: todo-go:v3`).
Để CD hoạt động mượt mà với Image Tag động (`$CI_COMMIT_SHORT_SHA`), bạn cần sửa file `docker-compose.yaml` để dùng biến môi trường:

**Sửa `docker-compose.yaml`:**
```yaml
services:
  backend:
    image: ${GO_IMAGE}:${IMAGE_TAG:-latest} # Dùng biến môi trường
    # ...
  gateway:
    image: ${PYTHON_IMAGE}:${IMAGE_TAG:-latest}
    # ...
```

---

## 🚀 PHẦN 2: KÍCH HOẠT CD

1. Sửa code (ví dụ đổi màu nút bấm trên Web hoặc đổi dòng text "Hello").
2. Commit & Push.
3. Quan sát Pipeline:
   - Lint ✅
   - Build-Push ✅
   - Deploy ✅

Sau khi Job Deploy xanh, hãy F5 trang web thật (IP VPS). Bạn sẽ thấy thay đổi được cập nhật ngay lập tức mà không cần SSH vào server gõ lệnh!

---

## 📝 TỔNG KẾT
Chúc mừng! Bạn đã hoàn thành chu trình **DevOps Loop**:
Code -> Git -> CI (Test/Build) -> CD (Deploy) -> Production.

👉 **Bước tiếp theo:** Khi hệ thống lớn lên hàng trăm service, Docker Compose không quản nổi nữa. Chúng ta cần **Kubernetes (Giai đoạn 9)**.
