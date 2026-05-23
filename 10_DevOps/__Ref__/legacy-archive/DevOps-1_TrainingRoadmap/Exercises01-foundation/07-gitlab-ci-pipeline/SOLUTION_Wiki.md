# Lời giải và Hướng dẫn - Bài 7: Xây dựng CI/CD Pipeline với GitLab CI

Chào mừng bạn đến với bài thực hành GitLab CI. Vì tôi không thể tương tác trực tiếp với GitLab, tôi đã chuẩn bị sẵn một dự án hoàn chỉnh cho bạn.

Dưới đây là hướng dẫn để bạn tự mình chạy pipeline và giải thích về các thành phần trong đó.

---

### Tổng quan các file đã tạo

Trong thư mục này, bạn sẽ thấy các file sau:

-   `index.js`: Một file JavaScript đơn giản để mô phỏng code của ứng dụng.
-   `build-script.js`: Một file JavaScript giả lập quá trình build (yêu cầu của Bài 2).
-   `package.json`: File cấu hình của dự án Node.js, chứa các dependencies và các lệnh trong phần `scripts` (như `test` và `build`).
-   `.gitlab-ci.yml`: **File quan trọng nhất**, định nghĩa pipeline CI/CD của chúng ta. Đây là phiên bản hoàn chỉnh, đã bao gồm tất cả các yêu cầu từ Bài 1 đến Bài 4.

---

### Hướng dẫn thực hành từng bước

Hãy làm theo các bước sau để xem pipeline của bạn hoạt động.

**Bước 1: Tạo một dự án mới trên GitLab**

1.  Đăng nhập vào tài khoản GitLab của bạn.
2.  Tạo một dự án mới: Click vào **New project** > **Create blank project**.
3.  Đặt tên cho dự án (ví dụ: `gitlab-ci-practice`) và chọn mức độ hiển thị (Private hoặc Public).
4.  **KHÔNG** khởi tạo dự án với file README.
5.  Sau khi tạo xong, GitLab sẽ cung cấp cho bạn một URL của kho chứa, có dạng `https://gitlab.com/your-username/gitlab-ci-practice.git`. Hãy sao chép URL này.

**Bước 2: Đưa code đã chuẩn bị sẵn lên GitLab**

Mở terminal của bạn và trỏ vào đúng thư mục chứa các file này (`workspare/Exercises02-scm-and-ci/07-gitlab-ci-pipeline/`). Sau đó, chạy các lệnh sau:

```bash
# Khởi tạo một kho chứa Git cục bộ
git init --initial-branch=main

# Kết nối kho chứa cục bộ này với kho chứa từ xa trên GitLab
# Thay <YOUR_GITLAB_PROJECT_URL> bằng URL bạn đã sao chép ở Bước 1
git remote add origin <YOUR_GITLAB_PROJECT_URL>

# Thêm tất cả các file vào Staging Area
git add .

# Tạo commit đầu tiên
git commit -m "Initial project with complete GitLab CI pipeline"

# Đẩy code lên GitLab
git push -u origin main
```

**Bước 3: Thêm biến môi trường trên GitLab (Yêu cầu của Bài 4)**

Đây là bước thủ công **bắt buộc** để pipeline có thể chạy thành công.

1.  Trong dự án GitLab của bạn, đi đến **Settings > CI/CD**.
2.  Tìm và mở rộng phần **Variables**.
3.  Click vào **Add variable**.
4.  Điền các thông tin sau:
    -   **Key:** `DEPLOY_USER`
    -   **Value:** `(Điền tên của bạn vào đây)`
    -   Để các tùy chọn khác ở mặc định và click **Add variable**.

**Bước 4: Quan sát Pipeline**

Ngay sau khi bạn `git push` ở Bước 2, GitLab sẽ tự động phát hiện file `.gitlab-ci.yml` và kích hoạt một pipeline.

1.  Trong dự án GitLab, đi đến **Build > Pipelines** (hoặc **CI/CD > Pipelines** ở menu bên trái).
2.  Bạn sẽ thấy một pipeline đang chạy hoặc đã hoàn thành. Hãy click vào nó.
3.  Bạn sẽ thấy các giai đoạn (stages) và các công việc (jobs) mà chúng ta đã định nghĩa. Click vào từng job để xem log chi tiết và xem các lệnh `echo` đã được thực thi như thế nào.
4.  Sau khi pipeline hoàn tất, ở trang chi tiết pipeline, bạn sẽ thấy một mục **Job artifacts** ở bên phải. Bạn có thể tải file `build-report.txt` (từ Bài 3) về từ đó.

---

### Giải thích chi tiết file `.gitlab-ci.yml`

Đây là trái tim của bài thực hành.

```yaml
image: node:16

stages:
  - build
  - build_app
  - test
  - deploy

install_job:
  stage: build
  script:
    - echo "Bắt đầu cài đặt dependencies..."
    - npm install
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour

build_job:
  stage: build_app
  script:
    - npm run build
    - echo "Build successful at $(date)" > build-report.txt
  artifacts:
    paths:
      - build-report.txt

test_job:
  stage: test
  script:
    - echo "Bắt đầu chạy unit tests..."
    - npm test

deploy_job:
  stage: deploy
  script:
    - echo "Deploying the application as user: $DEPLOY_USER..."
```

-   **`image: node:16`**: Khai báo rằng tất cả các job sẽ chạy bên trong một Docker container sử dụng image `node:16`.
-   **`stages`**: Định nghĩa 4 giai đoạn và thứ tự thực thi của chúng: `build` -> `build_app` -> `test` -> `deploy`.
-   **`install_job`** (`stage: build`):
    -   Chạy `npm install` để cài đặt các dependencies từ `package.json`.
    -   Phần `artifacts` lưu lại thư mục `node_modules/`. Thư mục này sẽ được tự động truyền cho các job ở các stage sau, giúp chúng không cần phải cài đặt lại.
-   **`build_job`** (`stage: build_app`):
    -   Chạy `npm run build`, thực thi script trong `build-script.js`.
    -   Tạo ra một file báo cáo `build-report.txt`.
    -   Phần `artifacts` lưu lại file `build-report.txt` này để người dùng có thể tải về sau khi pipeline hoàn tất.
-   **`test_job`** (`stage: test`):
    -   Job này tự động nhận được `node_modules/` từ `install_job`.
    -   Chạy `npm test` để thực thi các bài test (trong ví dụ này chỉ là một lệnh `echo`).
-   **`deploy_job`** (`stage: deploy`):
    -   Job này mô phỏng việc triển khai.
    -   Nó in ra giá trị của biến `$DEPLOY_USER`. Biến này không được định nghĩa trong file `.yml` mà được lấy từ cấu hình trên UI của GitLab, giúp bảo mật các thông tin nhạy cảm.

Chúc mừng bạn đã hoàn thành bài thực hành về GitLab CI!