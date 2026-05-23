# 🐳 Docker — Dockerfile Basics — Checklist Tự Đánh Giá

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)

---

## ✅ Danh Sách Kiểm Tra

### Phần 1: Dockerfile Basics

- [ ] Tôi biết cách viết `FROM <image>:<tag>`
- [ ] Tôi biết cách dùng `WORKDIR` để set working directory
- [ ] Tôi biết cách dùng `COPY` và `ADD` (và khi nào dùng cái nào)
- [ ] Tôi biết cách dùng `RUN` (shell form vs exec form)
- [ ] Tôi biết cách dùng `CMD` (exec form là preferred)
- [ ] Tôi biết cách dùng `ENV` để set environment variables
- [ ] Tôi biết cách dùng `EXPOSE` để document ports
- [ ] Tôi biết cách dùng `USER` để chạy với non-root user
- [ ] Tôi biết cách dùng `LABEL` để thêm metadata

---

### Phần 2: Build Process

- [ ] Tôi biết command `docker build -t name .`
- [ ] Tôi hiểu build context (files được gửi cho daemon)
- [ ] Tôi hiểu mỗi instruction tạo 1 layer
- [ ] Tôi biết layer caching hoạt động thế nào
- [ ] Tôi biết cách order Dockerfile để maximize cache hits
- [ ] Tôi biết cách tag image với `docker tag`

---

### Phần 3: .dockerignore

- [ ] Tôi biết tạo `.dockerignore` file
- [ ] Tôi biết exclude patterns phổ biến (node_modules, .git, .env,...)
- [ ] Tôi hiểu tại sao cần `.dockerignore` (giảm context size, exclude sensitive files)
- [ ] Tôi kiểm tra build context size với `docker build` logs

---

### Phần 4: Multi-Stage Builds

- [ ] Tôi biết syntax: `FROM <image> AS <stage_name>`
- [ ] Tôi biết cách copy artifacts giữa stages: `COPY --from=<stage>`
- [ ] Tôi hiểu mục đích của multi-stage (giảm image size, không có build dependencies)
- [ ] Tôi có thể viết multi-stage Dockerfile cho simple app
- [ ] Tôi biết final stage chỉ chứa runtime + app code

---

### Phần 5: Best Practices

- [ ] Tôi dùng official base images
- [ ] Tôi dùng specific tags (không `latest` trong production)
- [ ] Tôi combine RUN commands để giảm số layers
- [ ] Tôi clean up trong cùng RUN (apt-get clean, rm -rf,...)
- [ ] Tôi run as non-root user (`USER` directive)
- [ ] Tôi dùng exec form cho `CMD` và `ENTRYPOINT`
- [ ] Tôi không dùng `ADD` trừ khi cần unpack

---

### Phần 6: Hands-On Experience

- [ ] Tôi đã viết Dockerfile cho ít nhất 1 app (Node.js, Python, Go,...)
- [ ] Tôi đã build image thành công: `docker build -t myapp .`
- [ ] Tôi đã run container từ image của mình
- [ ] Tôi đã tối ưu Dockerfile với multi-stage build
- [ ] Tôi đã so sánh image size trước/sau tối ưu

---

## 🔍 Tự Đánh Giá

**Nếu >4 chưa check:** Cần làm lại exercises và đọc lại lesson.

**Nếu 2-4 chưa check:** Gần OK, nhưng nên luyện thêm.

**Nếu tất cả đều check:** 🎉 Bạn đã nắm vững Dockerfile basics!

---

**Next Steps:**
1. Hoàn thành [Quiz](quiz.md) (pass ≥70%)
2. Làm [Mini Project](../_projects/simple-webapp-dockerized.md)
3. Chuyển sang [Lesson 04 — Volumes & Networks](<chưa có>) (nếu có)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
