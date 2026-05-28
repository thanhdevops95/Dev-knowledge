# 🎯 GIAI ĐOẠN 7: GITLAB CI - CONTINUOUS INTEGRATION

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-7**.
- **Giai đoạn 7: GitLab CI** - Tự động test & build khi commit!

Mỗi lần push code lên GitLab → Pipeline tự động chạy → Build image → Push lên Docker Hub.

## 🏗️ FILE MỚI

```
Stage07_Complete/
├── .gitlab-ci.yml        # ← MỚI: CI Pipeline definition
├── (tất cả files cũ)
└── README.md
```

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Setup GitLab Variables
Vào GitLab Project → Settings → CI/CD → Variables:
1. `DOCKER_USER`: Username Docker Hub
2. `DOCKER_PASS`: Password/Token Docker Hub

### Bước 2: Push code lên GitLab
```bash
git init
git add .
git commit -m "Add CI Pipeline"
git remote add origin https://gitlab.com/USERNAME/PROJECT.git
git push -u origin main
```

### Bước 3: Xem Pipeline chạy
Vào GitLab → CI/CD → Pipelines → Click vào pipeline mới nhất

## 🧪 PIPELINE FLOW

```
Commit & Push
   ↓
GitLab Runner nhận job
   ↓
┌─────────────────┐
│  STAGE: LINT    │
├─────────────────┤
│ lint-python     │ → Kiểm tra Python code
│ lint-go         │ → Kiểm tra Go code
└─────────────────┘
   ↓ (Nếu pass)
┌─────────────────┐
│ STAGE: BUILD    │
├─────────────────┤
│ build-push-images│ → Build Docker images
│                 │ → Push lên Docker Hub
└─────────────────┘
   ↓
✅ Pipeline Success
```

## ✅ CHECKLIST

- [ ] Tạo file `.gitlab-ci.yml`
- [ ] Set GitLab Variables
- [ ] Push code lên GitLab
- [ ] Pipeline chạy thành công
- [ ] Images xuất hiện trên Docker Hub

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **CI/CD Pipeline:** Tự động hóa quy trình
2. ✅ **GitLab Runner:** Máy chạy jobs
3. ✅ **Docker-in-Docker:** Build image trong container
4. ✅ **Secrets Management:** Variables cho credentials

## 🚧 TIẾP THEO

Giai đoạn 8: **CD** - Tự động deploy lên server!
