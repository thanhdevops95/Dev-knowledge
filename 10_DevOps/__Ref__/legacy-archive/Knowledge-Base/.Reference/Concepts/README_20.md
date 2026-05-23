# 📘 DEVSECOPS ZERO TO HERO - LỘ TRÌNH HỌC TẬP

## 🎯 GIỚI THIỆU KHÓA HỌC

Chào mừng bạn đến với khóa học **DevSecOps Zero to Hero**! Đây là một hành trình thực hành từ con số 0, giúp bạn xây dựng và vận hành một hệ thống Microservices hoàn chỉnh.

### 🌟 Bạn sẽ học được gì?
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

### 🟢 PHẦN 1: NỀN TẢNG & CONTAINERIZATION

#### **Giai đoạn 1: Bare-metal - Giao tiếp liên dịch vụ**
📁 Files: `Stage01_Setup.md` + `Stage01_BareMetal.md`

**Mục tiêu:** Hiểu cách các service giao tiếp qua HTTP, nhận biết vấn đề lưu trữ RAM.

**Thời gian:** 3-4 giờ

**Công nghệ:** Python (Flask), Go (Gin), cURL

**Kết quả:** Hệ thống 2 service chạy trên máy cá nhân, gọi nhau qua localhost.

---

#### **Giai đoạn 2: Docker hóa - Sự cô lập**
📁 Files: `Stage02_Setup.md` + `Stage02_Dockerization.md`

**Mục tiêu:** Đóng gói ứng dụng vào Container, hiểu Docker Network.

**Thời gian:** 4-5 giờ

**Công nghệ:** Docker, Dockerfile, Docker Network

**Kết quả:** 2 container giao tiếp qua DNS, chạy đâu cũng được.

---

#### **Giai đoạn 3: Docker Volume - Cứu dữ liệu**
📁 Files: `Stage03_Setup.md` + `Stage03_Persistence.md`

**Mục tiêu:** Lưu trữ dữ liệu bền vững bằng Volume.

**Thời gian:** 2-3 giờ

**Công nghệ:** Docker Volume (Bind Mount)

**Kết quả:** Dữ liệu không mất khi restart container.

---

#### **Giai đoạn 4: Docker Compose - Nhạc trưởng**
📁 Files: `Stage04_Setup.md` + `Stage04_DockerCompose.md`

**Mục tiêu:** Quản lý nhiều container bằng 1 file YAML.

**Thời gian:** 2-3 giờ

**Công nghệ:** Docker Compose

**Kết quả:** Chỉ cần `docker compose up` để chạy toàn bộ hệ thống.

---

#### **Giai đoạn 5: NGINX & Web Interface**
📁 Files: `Stage05_Setup.md` + `Stage05_Nginx.md`

**Mục tiêu:** Thêm giao diện Web và Reverse Proxy.

**Thời gian:** 4-5 giờ

**Công nghệ:** NGINX, HTML/CSS/JS

**Kết quả:** Ứng dụng hoàn chỉnh với UI đẹp mắt.

---

### 🟡 PHẦN 2: CHUYÊN NGHIỆP HÓA & AUTOMATION

#### **Giai đoạn 6: MySQL Database - Chuẩn hóa lưu trữ**
📁 Files: `Stage06_Setup.md` + `Stage06_Database.md`

**Mục tiêu:** Thay file JSON bằng Database thực thụ.

**Thời gian:** 3-4 giờ

**Công nghệ:** MySQL 8.0, SQL Driver

**Kết quả:** Hệ thống 3-tier hoàn chỉnh (Frontend - Backend - Database).

---

#### **Giai đoạn 7: GitLab CI - Tích hợp liên tục**
📁 Files: `Stage07_Setup.md` + `Stage07_CI.md`

**Mục tiêu:** Tự động test và build khi commit code.

**Thời gian:** 3-4 giờ

**Công nghệ:** GitLab CI/CD, Docker Hub

**Kết quả:** Pipeline tự động: Lint → Build → Push Image.

---

#### **Giai đoạn 8: GitLab CD - Triển khai liên tục**
📁 Files: `Stage08_Setup.md` + `Stage08_CD.md`

**Mục tiêu:** Tự động deploy lên server production.

**Thời gian:** 3-4 giờ

**Công nghệ:** SSH, GitLab Runner

**Kết quả:** Code mới tự động lên production sau khi CI pass.

---

### 🔴 PHẦN 3: SCALE, CLOUD & SECURITY

#### **Giai đoạn 9: Kubernetes - Orchestration**
📁 Files: `Stage09_Setup.md` + `Stage09_Kubernetes.md`

**Mục tiêu:** Quản lý hàng trăm container, tự phục hồi.

**Thời gian:** 5-6 giờ

**Công nghệ:** Kubernetes (Minikube), kubectl

**Kết quả:** Hệ thống self-healing, tự tạo Pod mới khi crash.

---

#### **Giai đoạn 10: AWS EKS & Autoscaling**
📁 Files: `Stage10_Setup.md` + `Stage10_AWS_Autoscaling.md`

**Mục tiêu:** Deploy lên Cloud, tự động scale theo tải.

**Thời gian:** 4-5 giờ

**Công nghệ:** AWS EKS, HPA, K6 Load Test

**Kết quả:** Hệ thống tự tăng/giảm số Pod theo CPU.

⚠️ **Lưu ý:** Giai đoạn này tốn phí AWS (~$5-10 nếu làm nhanh).

---

#### **Giai đoạn 11: Observability - Giám sát toàn diện**
📁 Files: `Stage11_Setup.md` + `Stage11_Observability.md`

**Mục tiêu:** Dashboard giám sát metrics và logs.

**Thời gian:** 3-4 giờ

**Công nghệ:** Prometheus, Grafana, Loki, Helm

**Kết quả:** Biết ngay khi hệ thống có vấn đề, xem log tập trung.

---

#### **Giai đoạn 12: DevSecOps - Bảo mật tích hợp**
📁 Files: `Stage12_Setup.md` + `Stage12_DevSecOps.md`

**Mục tiêu:** Quét lỗ hổng bảo mật tự động.

**Thời gian:** 2-3 giờ

**Công nghệ:** Trivy, SonarQube

**Kết quả:** Pipeline chặn code/image có lỗ hổng bảo mật.

---

#### **Giai đoạn 13: GitOps với ArgoCD**
📁 Files: `Stage13_Setup.md` + `Stage13_GitOps.md`

**Mục tiêu:** Vận hành hiện đại nhất - Git là nguồn chân lý.

**Thời gian:** 3-4 giờ

**Công nghệ:** ArgoCD

**Kết quả:** Sửa file YAML trên Git → K8s tự động đồng bộ.

---

## 🚀 CÁCH SỬ DỤNG KHÓA HỌC

### Bước 1: Chuẩn bị môi trường
Mỗi giai đoạn có file **`StageXX_Setup.md`** hướng dẫn cài đặt công cụ cần thiết.

### Bước 2: Thực hành
Đọc file **`StageXX_TênGiaiĐoạn.md`** và làm theo từng bước.

### Bước 3: Kiểm tra
Mỗi giai đoạn có phần **Testing** để bạn tự kiểm tra kết quả.

### Bước 4: Ghi chú
Nên tạo file note riêng ghi lại những gì học được, lỗi gặp phải.

---

## 📚 TÀI LIỆU THAM KHẢO

### Tài liệu chính thức
- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Prometheus](https://prometheus.io/docs/)

### Video tiếng Việt (Khuyến nghị)
- Tìm kiếm "Docker tutorial tiếng Việt" trên YouTube
- Tìm kiếm "Kubernetes cơ bản" trên YouTube

### Community
- [DevOps Vietnam Facebook Group](https://www.facebook.com/groups/vietnam.devops/)
- [Kubernetes Vietnam](https://www.facebook.com/groups/k8s.vn/)

---

## ❓ TROUBLESHOOTING

Nếu gặp lỗi, hãy xem file **`Troubleshooting_Guide.md`** (sẽ được tạo riêng).

Các lỗi phổ biến:
- Port already in use → Đổi port hoặc kill process
- Permission denied → Chạy với sudo (Linux) hoặc Admin (Windows)
- Cannot connect to Docker daemon → Khởi động Docker Desktop

---

## 🎯 MỤC TIÊU SAU KHÓA HỌC

Sau khi hoàn thành, bạn có thể:
- ✅ Tự tin ứng tuyển vị trí **Junior DevOps Engineer**
- ✅ Xây dựng CI/CD pipeline cho dự án công ty
- ✅ Vận hành ứng dụng trên Kubernetes
- ✅ Giám sát và troubleshoot hệ thống production

---

## 📞 HỖ TRỢ

Nếu có thắc mắc, hãy:
1. Đọc kỹ lại phần hướng dẫn
2. Google lỗi cụ thể
3. Hỏi trên các group DevOps Vietnam

---

## 🏆 LỜI KHUYÊN

1. **Đừng vội:** Mỗi giai đoạn hãy làm kỹ, hiểu sâu.
2. **Thực hành nhiều lần:** Làm lại từ đầu 2-3 lần để nhớ lâu.
3. **Ghi chú:** Viết lại bằng lời của bạn.
4. **Thử phá:** Cố tình làm sai để hiểu cách xử lý lỗi.
5. **Chia sẻ:** Viết blog hoặc làm video chia sẻ những gì học được.

---

**Chúc bạn học tập hiệu quả! 🚀**

*Hãy bắt đầu từ `Stage01_Setup.md` ngay bây giờ!*
