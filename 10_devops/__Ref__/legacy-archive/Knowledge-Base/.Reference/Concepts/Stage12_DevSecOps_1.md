# GIAI ĐOẠN 12: DEVSECOPS - BẢO MẬT TỪ GỐC (SHIFT LEFT)

## 📌 MỤC TIÊU GIAI ĐOẠN 12
Bảo mật không phải là bước cuối cùng. Nó phải nằm trong quy trình CI/CD.
"Shift Left Security" nghĩa là đưa bảo mật sang bên trái (đầu) quy trình.

**Nhiệm vụ:**
1. **Trivy**: Quét Image tìm CVE (lỗ hổng đã biết) trước khi Push.
2. **SonarQube**: Quét code tìm "Code Smell" và lỗi bảo mật logic.

---

## 🛡️ PHẦN 1: TÍCH HỢP TRIVY VÀO GITLAB CI

Sửa file `.gitlab-ci.yml`. Thêm stage `security` vào trước `build-push`.

```yaml
stages:
  - lint
  - security  # <--- Mới
  - build-push
  - deploy

# ...

# --- STAGE: SECURITY SCAN ---
trivy-scan:
  stage: security
  image: 
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    # 1. Quét filesystem (code)
    - trivy fs --exit-code 1 --severity CRITICAL ./go-service
    
    # 2. Quét config (Dockerfile, YAML)
    - trivy config ./go-service
    
    # Lưu ý: Ta quét code/config trước. 
    # Nếu muốn quét Image sau khi build, ta phải dùng Docker-in-Docker phức tạp hơn.
    # Ở đây ta chặn ngay từ lúc code.
  allow_failure: true # (Demo: cho phép lỗi vẫn chạy tiếp, thực tế nên là false)
```

---

## 🔎 PHẦN 2: THỰC HÀNH QUÉT THỦ CÔNG

Hãy thử quét image Python của bạn xem có bao nhiêu lỗ hổng.

```bash
trivy image python:3.9-slim
```

**Kết quả:** Bạn sẽ thấy một bảng danh sách dài các lỗ hổng (CVE-xxxx) của hệ điều hành Debian (nền của python-slim).
-> **Bài học:** Không có Image nào an toàn tuyệt đối. Nhiệm vụ của DevSecOps là *biết* và *vá* (update base image thường xuyên).

---

## 🕵️ PHẦN 3: TÍCH HỢP SONARQUBE (MÔ PHỎNG)

Để tích hợp SonarQube vào CI, bạn cần SonarQube Server và Token. Đoạn code mẫu cho `.gitlab-ci.yml`:

```yaml
sonarqube-check:
  stage: security
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"  # Cache location
    GIT_DEPTH: "0"  # Shallow clone disabled
  script: 
    - sonar-scanner -Dsonar.qualitygate.wait=true
  allow_failure: true
  only:
    - main
```
*(Yêu cầu bạn phải đăng ký SonarCloud.io và lấy Token set vào Variable `SONAR_TOKEN` trên GitLab)*.

---

## 📝 TỔNG KẾT
Bảo mật không phải là ma thuật. Nó là kỷ luật.
Bằng cách thêm Trivy vào Pipeline, bạn đảm bảo không ai vô tình "mở cửa" cho hacker bằng những thư viện lỗi thời.

👉 **Bước tiếp theo:** Tự động hóa Deploy ở level cao nhất (Kubernetes-native). Giai đoạn 13: **GitOps với ArgoCD**.
