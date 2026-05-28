# 🎓 DEVSECOPS ZERO TO HERO - KHÓA HỌC HOÀN CHỈNH

## 📚 GIỚI THIỆU

Chào mừng bạn đến với khóa học **DevSecOps Zero to Hero**! 

Đây là một lộ trình học tập hoàn chỉnh từ cơ bản đến nâng cao, giúp bạn xây dựng và vận hành một hệ thống Microservices chuyên nghiệp.

### � Bạn sẽ học được gì?

- ✅ Xây dựng ứng dụng Microservices từ đầu (Go + Python)
- ✅ Containerization với Docker
- ✅ Orchestration với Kubernetes
- ✅ CI/CD Pipeline tự động (GitLab)
- ✅ Cloud Deployment (AWS EKS)
- ✅ Monitoring & Logging (Prometheus, Grafana, Loki)
- ✅ Security Scanning (Trivy, SonarQube)
- ✅ GitOps với ArgoCD

### 🎓 Đối tượng học viên

- Sinh viên IT muốn học DevOps thực chiến
- Developer muốn chuyển sang DevOps/SRE
- Sysadmin muốn hiện đại hóa kỹ năng
- Bất kỳ ai muốn hiểu cách vận hành hệ thống quy mô lớn

### ⏱️ Thời gian học

- **Tổng thời gian:** 40-60 giờ (tùy tốc độ)
- **Khuyến nghị:** 2-3 giờ/ngày, hoàn thành trong 3-4 tuần

---

## 🗺️ LỘ TRÌNH HỌC TẬP (13 GIAI ĐOẠN)

### 🟢 PHẦN 1: NỀN TẢNG & CONTAINERIZATION (Giai đoạn 1-4)

| Giai đoạn | Nội dung | Thời gian | Công nghệ |
|-----------|----------|-----------|-----------|
| **1. Bare-metal** | Giao tiếp liên dịch vụ | 3-4h | Python, Go, cURL |
| **2. Docker** | Containerization | 4-5h | Docker, Dockerfile |
| **3. Volume** | Persistent Storage | 2-3h | Docker Volume |
| **4. Compose** | Orchestration cơ bản | 2-3h | Docker Compose |

**Kết quả:** Hiểu cách services giao tiếp, đóng gói ứng dụng, lưu trữ dữ liệu.

---

### 🟡 PHẦN 2: WEB & DATABASE (Giai đoạn 5-6)

| Giai đoạn | Nội dung | Thời gian | Công nghệ |
|-----------|----------|-----------|-----------|
| **5. NGINX & Web** | Frontend + Reverse Proxy | 4-5h | NGINX, HTML/CSS/JS |
| **6. MySQL** | Database thực thụ | 3-4h | MySQL 8.0 |

**Kết quả:** Ứng dụng hoàn chỉnh với giao diện Web và Database chuyên nghiệp.

---

### 🔴 PHẦN 3: CI/CD & AUTOMATION (Giai đoạn 7-8)

| Giai đoạn | Nội dung | Thời gian | Công nghệ |
|-----------|----------|-----------|-----------|
| **7. GitLab CI** | Continuous Integration | 3-4h | GitLab CI, Docker Hub |
| **8. GitLab CD** | Continuous Deployment | 3-4h | SSH, Automation |

**Kết quả:** Tự động test, build, deploy khi commit code.

---

### 🟣 PHẦN 4: CLOUD & SCALE (Giai đoạn 9-10)

| Giai đoạn | Nội dung | Thời gian | Công nghệ |
|-----------|----------|-----------|-----------|
| **9. Kubernetes** | Container Orchestration | 5-6h | K8s, Minikube |
| **10. AWS EKS** | Cloud + Autoscaling | 4-5h | AWS EKS, HPA |

**Kết quả:** Hệ thống tự phục hồi, tự scale trên Cloud.

⚠️ **Lưu ý:** Giai đoạn 10 tốn phí AWS (~$5-10 nếu làm nhanh).

---

### ⚫ PHẦN 5: OBSERVABILITY & SECURITY (Giai đoạn 11-13)

| Giai đoạn | Nội dung | Thời gian | Công nghệ |
|-----------|----------|-----------|-----------|
| **11. Monitoring** | Metrics & Logs | 3-4h | Prometheus, Grafana, Loki |
| **12. DevSecOps** | Security Scanning | 2-3h | Trivy, SonarQube |
| **13. GitOps** | Vận hành hiện đại | 3-4h | ArgoCD |

**Kết quả:** Giám sát toàn diện, bảo mật tích hợp, vận hành tự động.

---

## � CẤU TRÚC DỰ ÁN

```
Todo-App-DevOps/
│
├── README.md                    # ← File này (Đề bài tổng quan)
│
├── Course_Content/              # 📚 Tài liệu hướng dẫn (30 files)
│   ├── README.md                # Lộ trình chi tiết
│   ├── 00_Foundation_Knowledge.md
│   ├── Troubleshooting_Guide.md
│   ├── Quick_Reference.md
│   ├── Stage01_Setup.md         # Cài đặt công cụ
│   ├── Stage01_BareMetal.md     # Hướng dẫn thực hành
│   ├── Stage02_Setup.md
│   ├── Stage02_Dockerization.md
│   └── ... (26 files khác)
│
└── Implementations/             # 💻 Bài làm thực hành (13 thư mục)
    ├── Stage01_Complete/        # Bare-metal
    ├── Stage02_Complete/        # Docker
    ├── Stage03_Complete/        # Volume
    ├── Stage04_Complete/        # Compose
    ├── Stage05_Complete/        # NGINX & Web
    ├── Stage06_Complete/        # MySQL
    ├── Stage07_Complete/        # CI
    ├── Stage08_Complete/        # CD
    ├── Stage09_Complete/        # Kubernetes
    ├── Stage10_Complete/        # AWS EKS
    ├── Stage11_Complete/        # Monitoring
    ├── Stage12_Complete/        # Security
    └── Stage13_Complete/        # GitOps
```

---

## 🚀 CÁCH SỬ DỤNG

### Bước 1: Đọc tài liệu hướng dẫn

Bắt đầu từ thư mục **`Course_Content/`**:

1. **Đọc tổng quan:** [`Course_Content/README.md`](./Course_Content/README.md)
2. **Nắm kiến thức nền:** [`Course_Content/00_Foundation_Knowledge.md`](./Course_Content/00_Foundation_Knowledge.md)
3. **Làm từng giai đoạn:**
   - Setup: `Course_Content/Stage01_Setup.md`
   - Tutorial: `Course_Content/Stage01_BareMetal.md`
   - Lặp lại cho Stage 02-13

### Bước 2: Thực hành với code mẫu

Vào thư mục **`Implementations/`**:

1. **Chọn giai đoạn:** Ví dụ `Implementations/Stage01_Complete/`
2. **Đọc README:** Hướng dẫn chạy code
3. **Đọc NOTES:** Ghi chú kết quả test, điểm lưu ý
4. **Chạy code:** Làm theo từng bước

### Bước 3: Tham khảo khi cần

- **Gặp lỗi?** → [`Course_Content/Troubleshooting_Guide.md`](./Course_Content/Troubleshooting_Guide.md)
- **Quên lệnh?** → [`Course_Content/Quick_Reference.md`](./Course_Content/Quick_Reference.md)

---

## 🎯 MỤC TIÊU SAU KHÓA HỌC

Sau khi hoàn thành, bạn có thể:

- ✅ Tự tin ứng tuyển vị trí **Junior DevOps Engineer**
- ✅ Xây dựng CI/CD pipeline cho dự án công ty
- ✅ Vận hành ứng dụng trên Kubernetes
- ✅ Giám sát và troubleshoot hệ thống production

---

## � THỐNG KÊ DỰ ÁN

- **Tổng số files:** ~150+ files
- **Lines of Code:** ~5000+ lines
- **Công nghệ:** 20+ công nghệ khác nhau
- **Tài liệu:** 30 files markdown
- **Code mẫu:** 13 thư mục hoàn chỉnh

---

## 💡 LỜI KHUYÊN

1. **Đừng vội:** Mỗi giai đoạn hãy làm kỹ, hiểu sâu
2. **Thực hành nhiều lần:** Làm lại 2-3 lần để nhớ lâu
3. **Ghi chú:** Viết lại bằng lời của bạn
4. **Thử phá:** Cố tình làm sai để hiểu cách xử lý lỗi
5. **Chia sẻ:** Viết blog hoặc làm video chia sẻ những gì học được

---

## � HỖ TRỢ

Nếu có thắc mắc:

1. Đọc kỹ lại phần hướng dẫn
2. Xem `Troubleshooting_Guide.md`
3. Google lỗi cụ thể
4. Hỏi trên các group DevOps Vietnam

---

## 🔗 LINKS QUAN TRỌNG

- **Tài liệu hướng dẫn:** [`Course_Content/`](./Course_Content/)
- **Code thực hành:** [`Implementations/`](./Implementations/)
- **Troubleshooting:** [`Course_Content/Troubleshooting_Guide.md`](./Course_Content/Troubleshooting_Guide.md)
- **Quick Reference:** [`Course_Content/Quick_Reference.md`](./Course_Content/Quick_Reference.md)

---

## 🏆 BẮT ĐẦU NGAY!

👉 **Bước đầu tiên:** Vào [`Course_Content/README.md`](./Course_Content/README.md) để bắt đầu hành trình!

Chúc bạn học tập hiệu quả! 🚀
