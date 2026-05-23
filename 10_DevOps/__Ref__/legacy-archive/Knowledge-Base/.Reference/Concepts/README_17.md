# 🎯 GIAI ĐOẠN 12: DEVSECOPS - SECURITY SCANNING

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-12**.
- **Giai đoạn 12: Trivy Security Scanning** - Bảo mật từ đầu!

"Shift Left Security" - Bắt lỗi bảo mật ngay từ lúc code, không đợi đến production.

## 🚀 CÁCH CHẠY

### Bước 1: Cài Trivy
```bash
# macOS
brew install aquasecurity/trivy/trivy

# Linux
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

### Bước 2: Scan Image
```bash
# Scan Go image
trivy image YOUR_USER/todo-go:latest

# Scan Python image
trivy image YOUR_USER/todo-python:latest
```

### Bước 3: Scan Filesystem
```bash
trivy fs ./go-service
trivy fs ./python-service
```

## 🧪 TESTING

### Test 1: Scan Base Image
```bash
trivy image python:3.9-slim
# Thấy danh sách CVE vulnerabilities
```

### Test 2: Scan với Severity Filter
```bash
trivy image --severity CRITICAL,HIGH YOUR_USER/todo-go:latest
# Chỉ hiện lỗi nghiêm trọng
```

### Test 3: Tích hợp vào CI
Thêm vào `.gitlab-ci.yml`:
```yaml
trivy-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy fs --exit-code 1 --severity CRITICAL ./go-service
    - trivy config ./k8s
```

## ✅ CHECKLIST

- [ ] Cài được Trivy
- [ ] Scan được images
- [ ] Hiểu được CVE reports
- [ ] Tích hợp vào CI pipeline
- [ ] Biết cách fix vulnerabilities

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **CVE:** Common Vulnerabilities and Exposures
2. ✅ **Image Scanning:** Tìm lỗ hổng trong dependencies
3. ✅ **Config Scanning:** Kiểm tra K8s manifests
4. ✅ **Shift Left:** Bắt lỗi sớm

## 🚧 TIẾP THEO

Giai đoạn 13: **GitOps với ArgoCD** - Tự động hóa cuối cùng!
