# GIAI ĐOẠN 7: GITLAB CI - TÍCH HỢP LIÊN TỤC

## 📌 MỤC TIÊU GIAI ĐOẠN 7
"Code -> Commit -> Tự động Test -> Tự động Build -> Tự động Push".
Bạn sẽ thiết lập một Pipeline tự động hóa quá trình này. Nếu code lỗi, Pipeline sẽ báo đỏ và chặn không cho build.

**Flow:**
1. **Lint**: Kiểm tra cú pháp (Python/Go).
2. **Build**: Build Docker Image.
3. **Push**: Đẩy Image lên Docker Hub.

---

## 🛠️ PHẦN 1: VIẾT FILE .GITLAB-CI.YML

Tạo file `.gitlab-ci.yml` tại thư mục gốc dự án. Đây là "linh hồn" của CI/CD.

```yaml
stages:
  - lint
  - build-push

variables:
  # Tên Image sẽ lưu trên Docker Hub
  IMAGE_TAG: $CI_COMMIT_SHORT_SHA # Tag theo mã commit (VD: a1b2c3d)
  GO_IMAGE: $DOCKER_USER/todo-go
  PYTHON_IMAGE: $DOCKER_USER/todo-python

# --- STAGE 1: LINT (KIỂM TRA CÚ PHÁP) ---
lint-python:
  stage: lint
  image: python:3.9-slim
  script:
    - pip install flake8
    # Kiểm tra code trong folder python-service
    # Bỏ qua lỗi E501 (line too long) cho đỡ khó tính
    - flake8 python-service/ --ignore=E501 

lint-go:
  stage: lint
  image: golang:1.21-alpine
  script:
    - cd go-service
    - go vet ./... # Kiểm tra lỗi logic tiềm ẩn

# --- STAGE 2: BUILD & PUSH DOCKER HUB ---
build-push-images:
  stage: build-push
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind # Docker-in-Docker
  before_script:
    # Đăng nhập Docker Hub bằng biến đã lưu ở Setup
    - echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
  script:
    # 1. Build & Push Go Service
    - docker build -t $GO_IMAGE:$IMAGE_TAG -t $GO_IMAGE:latest ./go-service
    - docker push $GO_IMAGE:$IMAGE_TAG
    - docker push $GO_IMAGE:latest
    
    # 2. Build & Push Python Service
    - docker build -t $PYTHON_IMAGE:$IMAGE_TAG -t $PYTHON_IMAGE:latest ./python-service
    - docker push $PYTHON_IMAGE:$IMAGE_TAG
    - docker push $PYTHON_IMAGE:latest
    
    # In ra thông báo thành công
    - echo "Build and Push complete! Tag: $IMAGE_TAG"
```

---

## 🚀 PHẦN 2: KÍCH HOẠT PIPELINE

Sau khi tạo file xong, bạn chỉ cần commit và push lên GitLab.

```bash
git add .gitlab-ci.yml
git commit -m "Add CI Pipeline"
git push origin main
```

### Quan sát kết quả
1. Vào GitLab -> Build -> Pipelines.
2. Bạn sẽ thấy một Pipeline đang chạy (Status: Running).
3. Bấm vào chi tiết để xem từng Job (`lint-python`, `build-push-images`).

Nếu tất cả đều **Passed** (Màu xanh lá) ✅:
- Kiểm tra trên Docker Hub.
- Bạn sẽ thấy 2 repo `todo-go` và `todo-python` vừa được cập nhật image mới nhất.

---

## 🧪 PHẦN 3: THỬ LÀM SAI (BREAK THE BUILD)

CI sinh ra để bắt lỗi. Hãy thử viết Code sai.

1. Sửa file `python-service/app.py`.
2. Gõ bậy bạ gì đó vào (ví dụ xóa dấu hai chấm `:`).
3. Commit & Push.
4. Xem Pipeline: Job `lint-python` sẽ **Failed** ❌.
5. Job `build-push-images` sẽ **Skipped** (không chạy).
-> **Thành công:** Code lỗi không bao giờ được đóng gói!

---

## 📝 TỔNG KẾT
Bạn đã thiết lập xong CI (Continuous Integration).
- Code sạch -> Build -> Push.
- Code bẩn -> Báo lỗi -> Dừng.

👉 **Bước tiếp theo:** Image đã có trên Docker Hub rồi. Làm sao để tự động lôi nó về Server để chạy? Giai đoạn 8: **GitLab CD**.
