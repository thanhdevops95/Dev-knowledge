# 📋 MODULE 02: BUILD - YÊU CẦU & TIÊU CHÍ NGHIỆM THU

## 🎯 Mục tiêu Module

Sau khi hoàn thành module này, bạn sẽ:

1. ✅ Hiểu **tại sao** cần containerization và lợi ích của Docker
2. ✅ Viết được **Dockerfile** tối ưu cho Python app
3. ✅ Sử dụng thành thạo **Docker CLI** commands
4. ✅ Orchestrate multi-container với **Docker Compose**
5. ✅ Hiểu **Git branching strategies** và áp dụng vào dự án
6. ✅ Giải quyết được 5 tình huống thực chiến về Docker và Git

---

## 📖 Danh sách thuật ngữ (Terminology)

| Từ viết tắt | Tiếng Anh đầy đủ | Nghĩa tiếng Việt |
|-------------|------------------|------------------|
| **Docker** | Docker | Nền tảng containerization |
| **Image** | Docker Image | Bản thiết kế container (blueprint) |
| **Container** | Docker Container | Instance đang chạy từ image |
| **Dockerfile** | Dockerfile | File hướng dẫn build image |
| **Layer** | Image Layer | Lớp trong Docker image |
| **Volume** | Docker Volume | Lưu trữ persistent data |
| **Network** | Docker Network | Mạng kết nối giữa containers |
| **Compose** | Docker Compose | Tool orchestrate multi-container |
| **Registry** | Container Registry | Kho lưu trữ images (Docker Hub) |
| **Tag** | Image Tag | Phiên bản của image (v1.0, latest) |

---

## ✅ Checklist bài tập (LABS)

### Phần 1: Docker Basics

- [ ] **LAB 1.1**: Cài đặt Docker Desktop và verify
- [ ] **LAB 1.2**: Pull image từ Docker Hub
- [ ] **LAB 1.3**: Run container đầu tiên
- [ ] **LAB 1.4**: Inspect container (logs, exec, stats)

### Phần 2: Dockerfile

- [ ] **LAB 2.1**: Viết Dockerfile cho Counter App
- [ ] **LAB 2.2**: Build Docker image
- [ ] **LAB 2.3**: Optimize Dockerfile (multi-stage build)
- [ ] **LAB 2.4**: Push image lên Docker Hub

### Phần 3: Docker Compose

- [ ] **LAB 3.1**: Viết docker-compose.yml
- [ ] **LAB 3.2**: Start multi-container app
- [ ] **LAB 3.3**: Configure networks và volumes
- [ ] **LAB 3.4**: Health checks và restart policies

### Phần 4: Git Advanced

- [ ] **LAB 4.1**: Git branching strategies (Gitflow)
- [ ] **LAB 4.2**: Rebase vs Merge
- [ ] **LAB 4.3**: Cherry-pick commits
- [ ] **LAB 4.4**: Git tags và releases

---

## 🚨 Checklist tình huống (SCENARIOS)

- [ ] **Scenario 1**: Image quá lớn (2GB) - Tối ưu xuống còn 200MB
- [ ] **Scenario 2**: Container exit ngay khi start
- [ ] **Scenario 3**: Data mất khi restart container
- [ ] **Scenario 4**: Containers không communicate được với nhau
- [ ] **Scenario 5**: Git commit nhầm sensitive data (passwords, API keys)

---

## 💯 Tiêu chí nghiệm thu

### Kiến thức lý thuyết

- ✅ Giải thích Docker bằng ẩn dụ "hộp cơm trưa"
- ✅ Phân biệt Image vs Container
- ✅ So sánh Docker vs Virtual Machine

### Kỹ năng thực hành

- ✅ Build được Docker image từ Dockerfile
- ✅ Run multi-container app với docker-compose
- ✅ Sử dụng volumes để persist data
- ✅ Áp dụng Gitflow cho dự án

### Deliverables

- ✅ Dockerfile tối ưu (<500MB)
- ✅ docker-compose.yml hoàn chỉnh
- ✅ Image đã push lên Docker Hub
- ✅ Git repository với branch strategy rõ ràng

---

## ⏱️ Thời lượng ước tính

- **Lý thuyết**: 2-3 giờ
- **LAB**: 4-5 giờ
- **SCENARIOS**: 2-3 giờ
- **Tổng**: 8-10 giờ

---

## ⏭️ Next Module

👉 **Module 03: CI - Continuous Integration**
