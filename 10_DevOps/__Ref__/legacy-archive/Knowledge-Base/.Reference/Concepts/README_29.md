# 🎯 GIAI ĐOẠN 8: GITLAB CD - CONTINUOUS DEPLOYMENT

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-8**.
- **Giai đoạn 8: GitLab CD** - Tự động deploy lên server production!

Code mới → CI build → **CD tự động deploy** → Production updated!

## 🏗️ CẬP NHẬT

```
Stage08_Complete/
├── .gitlab-ci.yml        # ← CẬP NHẬT: Thêm stage 'deploy'
└── README.md
```

## 🚀 SETUP

### Bước 1: Tạo SSH Key
```bash
ssh-keygen -t rsa -b 4096 -f gitlab_deploy_key
```

### Bước 2: Add Public Key vào VPS
```bash
# Copy nội dung gitlab_deploy_key.pub
cat gitlab_deploy_key.pub

# SSH vào VPS và thêm vào authorized_keys
ssh user@your-vps
echo "PASTE_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

### Bước 3: Add Variables vào GitLab
Settings → CI/CD → Variables:
1. `SSH_PRIVATE_KEY`: Nội dung file `gitlab_deploy_key`
2. `SSH_HOST`: IP của VPS
3. `SSH_USER`: Username (root hoặc ubuntu)

### Bước 4: Push code
```bash
git add .
git commit -m "Add CD pipeline"
git push
```

## 🧪 PIPELINE FLOW

```
Push code
   ↓
Lint → Build → Push
   ↓
Deploy Stage:
  1. SSH vào VPS
  2. Copy docker-compose.yaml
  3. Pull images mới
  4. Restart containers
   ↓
✅ Production Updated!
```

## ✅ CHECKLIST

- [ ] Tạo SSH key pair
- [ ] Add public key vào VPS
- [ ] Set GitLab Variables
- [ ] Pipeline deploy thành công
- [ ] Truy cập VPS thấy app updated

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **CD Pipeline:** Tự động deploy
2. ✅ **SSH Automation:** Deploy không cần tay
3. ✅ **Zero Downtime:** Docker Compose rolling update
4. ✅ **GitOps Preview:** Git là nguồn chân lý

## 🚧 TIẾP THEO

Giai đoạn 9: **Kubernetes** - Orchestration chuyên nghiệp!
