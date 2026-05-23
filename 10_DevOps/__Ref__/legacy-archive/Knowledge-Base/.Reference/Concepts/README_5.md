# 💻 IMPLEMENTATIONS - BÀI LÀM THỰC HÀNH

## 📌 GIỚI THIỆU

Thư mục này chứa **13 thư mục code hoàn chỉnh** tương ứng với 13 giai đoạn của khóa học.

Mỗi thư mục là một "snapshot" hoàn chỉnh của hệ thống tại giai đoạn đó, bao gồm:
- ✅ Code nguồn (Go, Python, Frontend)
- ✅ Cấu hình (Docker, Kubernetes, CI/CD)
- ✅ README hướng dẫn chạy
- ✅ NOTES ghi chú kết quả test

---

## 📂 CẤU TRÚC

```
Implementations/
├── Stage01_Complete/    # Giai đoạn 1: Bare-metal
├── Stage02_Complete/    # Giai đoạn 2: Docker
├── Stage03_Complete/    # Giai đoạn 3: Volume & Persistence
├── Stage04_Complete/    # Giai đoạn 4: Docker Compose
├── Stage05_Complete/    # Giai đoạn 5: NGINX & Frontend
├── Stage06_Complete/    # Giai đoạn 6: MySQL Database
├── Stage07_Complete/    # Giai đoạn 7: GitLab CI
├── Stage08_Complete/    # Giai đoạn 8: GitLab CD
├── Stage09_Complete/    # Giai đoạn 9: Kubernetes
├── Stage10_Complete/    # Giai đoạn 10: AWS EKS & Autoscaling
├── Stage11_Complete/    # Giai đoạn 11: Monitoring
├── Stage12_Complete/    # Giai đoạn 12: DevSecOps
└── Stage13_Complete/    # Giai đoạn 13: GitOps
```

---

## 🚀 CÁCH SỬ DỤNG

### Phương án 1: Học tuần tự (Khuyến nghị)
1. Bắt đầu từ `Stage01_Complete/`
2. Đọc `README.md` để biết cách chạy
3. Đọc `NOTES.md` để biết điểm lưu ý
4. Chạy code và thực hành
5. Chuyển sang `Stage02_Complete/` và lặp lại

### Phương án 2: Nhảy vào giai đoạn cụ thể
Nếu bạn đã hiểu các giai đoạn trước, có thể nhảy thẳng vào giai đoạn muốn học:
- Ví dụ: Muốn học Kubernetes → Vào `Stage09_Complete/`
- Mỗi thư mục đã chứa đầy đủ code từ đầu đến giai đoạn đó

### Phương án 3: Tham khảo code mẫu
Khi làm dự án riêng, có thể tham khảo code trong các thư mục này.

---

## 📝 MỖI THƯ MỤC CHỨA GÌ?

Ví dụ `Stage05_Complete/`:

```
Stage05_Complete/
├── README.md              # Hướng dẫn chạy chi tiết
├── NOTES.md               # Ghi chú kết quả test, điểm thiếu
├── docker-compose.yaml    # Cấu hình Docker Compose
├── go-service/            # Backend Go
│   ├── main.go
│   ├── go.mod
│   └── Dockerfile
├── python-service/        # Gateway Python
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # Web UI
│   ├── index.html
│   ├── css/
│   └── js/
└── nginx/                 # Web server config
    └── conf.d/
```

---

## 🎯 CHECKLIST HỌC TẬP

- [ ] Stage 01: Bare-metal - Hiểu giao tiếp HTTP
- [ ] Stage 02: Docker - Containerization
- [ ] Stage 03: Volume - Persistent storage
- [ ] Stage 04: Compose - Orchestration
- [ ] Stage 05: NGINX - Web interface
- [ ] Stage 06: MySQL - Database thực thụ
- [ ] Stage 07: CI - Tự động test & build
- [ ] Stage 08: CD - Tự động deploy
- [ ] Stage 09: Kubernetes - Self-healing
- [ ] Stage 10: AWS EKS - Cloud & Autoscaling
- [ ] Stage 11: Monitoring - Observability
- [ ] Stage 12: Security - DevSecOps
- [ ] Stage 13: GitOps - ArgoCD

---

## 💡 TIPS

1. **Đọc README trước khi chạy code**
2. **Đọc NOTES để biết điểm lưu ý**
3. **Thử phá code để hiểu cách xử lý lỗi**
4. **So sánh code giữa các stage để thấy sự tiến hóa**

---

## 🔗 QUAY LẠI

- **Tài liệu hướng dẫn:** [`../Course_Content/`](../Course_Content/)
- **README chính:** [`../README.md`](../README.md)

---

**Chúc bạn thực hành hiệu quả! 🚀**
