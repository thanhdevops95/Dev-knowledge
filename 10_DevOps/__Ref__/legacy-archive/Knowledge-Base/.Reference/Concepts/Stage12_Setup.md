# 🛠️ GIAI ĐOẠN 12: CHUẨN BỊ DEVSECOPS

## 📌 MỤC TIÊU
Cài đặt công cụ quét bảo mật **Trivy**. Trivy là máy quét lỗ hổng cực nhanh cho Container.

---

## 1. CÀI ĐẶT TRIVY (LOCAL)
Để thử nghiệm quét trên máy cá nhân trước khi đưa vào CI.

### macOS
```bash
brew install aquasecurity/trivy/trivy
```

### Windows/Linux
Làm theo hướng dẫn tại: [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy/v0.18.3/installation/)

## 2. CHUẨN BỊ SONARQUBE (OPTIONAL)
SonarQube cần server riêng khá nặng (Java). Trong khuôn khổ bài lab nhanh, ta sẽ dùng **SonarCloud** (kết nối với GitLab) hoặc chủ yếu tập trung vào Trivy (Container Security).
Nếu muốn chạy SonarQube local:
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube
```

## ✅ CHECKLIST
```bash
trivy --version
```
Sẵn sàng săn tìm lỗ hổng!
