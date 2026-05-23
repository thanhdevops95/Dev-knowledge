# Bài 7: Xây dựng CI/CD Pipeline với GitLab CI

## 🎯 Mục tiêu bài học

-   Hiểu được các khái niệm cốt lõi của GitLab CI: Pipeline, Stage, Job, và Runner.
-   Viết được file cấu hình `.gitlab-ci.yml` để định nghĩa một pipeline.
-   Xây dựng được một pipeline CI đơn giản để tự động build và test một ứng dụng nhỏ.
-   Biết cách xem log và gỡ lỗi khi một pipeline thất bại.

## 📖 Nội dung chính

1.  **Giới thiệu GitLab CI:** Sức mạnh của việc tích hợp CI/CD ngay trong SCM.
2.  **Các thành phần chính:** Pipeline, Stage, Job, Runner.
3.  **File `.gitlab-ci.yml`:** Cú pháp và các từ khóa quan trọng (`image`, `stages`, `script`, `artifacts`).
4.  **Thực hành:** Xây dựng pipeline cho một ứng dụng "Hello World" (ví dụ: Node.js hoặc Python).
    -   Stage `build`: Cài đặt dependencies.
    -   Stage `test`: Chạy unit test.
5.  **Sử dụng Biến (Variables):** Cách định nghĩa và sử dụng biến môi trường.
6.  **Artifacts:** Lưu trữ và truyền kết quả giữa các stage.

## 🛠️ Công cụ & Lý thuyết

-   **Công cụ CI/CD:** <u>GitLab CI/CD</u>, Jenkins, GitHub Actions, CircleCI, Travis CI.
-   **Lý thuyết:** YAML syntax, CI Pipeline as Code.

---

# Nội dung chi tiết - Bài 7: Xây dựng CI/CD Pipeline với GitLab CI

Sau khi đã hiểu lý thuyết về CI/CD, đã đến lúc chúng ta bắt tay vào thực hành với một trong những công cụ phổ biến nhất hiện nay: GitLab CI/CD. Điểm mạnh lớn nhất của GitLab CI là nó được tích hợp sẵn ngay bên trong GitLab, nơi bạn quản lý mã nguồn của mình.

---

### 1. Giới thiệu GitLab CI

GitLab CI/CD là một công cụ cho phép bạn định nghĩa các đường ống (pipeline) CI/CD trực tiếp trong kho chứa code của bạn. Mỗi khi bạn đẩy code mới lên, GitLab sẽ tự động tìm một file đặc biệt tên là `.gitlab-ci.yml` và thực thi các bước được định nghĩa trong đó.

---

### 2. Các thành phần chính

-   **Pipeline:** Là một tập hợp các công việc (jobs) được nhóm lại thành các giai đoạn (stages). Một pipeline định nghĩa toàn bộ quy trình CI/CD của bạn.
-   **Stage:** Đại diện cho một giai đoạn trong pipeline, ví dụ: `build`, `test`, `deploy`. Các jobs trong cùng một stage có thể chạy song song. Các stages sẽ chạy tuần tự (stage sau chỉ chạy khi tất cả các jobs của stage trước thành công).
-   **Job:** Là một tác vụ cụ thể cần thực hiện, ví dụ: `compile-code`, `run-unit-tests`. Mỗi job là một chuỗi các lệnh được thực thi.
-   **Runner:** Là một máy chủ (hoặc một container) được cài đặt phần mềm GitLab Runner. Nó có nhiệm vụ "lắng nghe" và thực thi các jobs mà GitLab CI yêu cầu. Bạn có thể dùng các shared runner do GitLab cung cấp hoặc tự cài đặt runner riêng.

---

### 3. File `.gitlab-ci.yml`

Đây là file bạn sẽ định nghĩa pipeline của mình bằng cú pháp YAML. File này nằm ở thư mục gốc của dự án.

**Các từ khóa quan trọng:**

-   `image`: Chỉ định Docker image sẽ được sử dụng để chạy job. Ví dụ `image: node:16` sẽ tạo một container từ image Node.js phiên bản 16 và chạy job của bạn bên trong đó.
-   `stages`: Định nghĩa danh sách và thứ tự các stage trong pipeline.
-   `job_name`: Tên của một job. Bạn có thể đặt tên tùy ý.
    -   `stage`: Chỉ định job này thuộc stage nào.
    -   `script`: Một mảng các lệnh shell sẽ được thực thi bởi Runner. Đây là phần quan trọng nhất của job.
    -   `artifacts`: Cho phép bạn chỉ định các file hoặc thư mục cần được lưu lại sau khi job hoàn thành và có thể được sử dụng ở các job sau.

---

### 4. Thực hành: Pipeline cho ứng dụng Node.js "Hello World"

Hãy tạo một dự án Node.js đơn giản và một pipeline để build và test nó.

**1. Tạo file `package.json`:**
```json
{
  "name": "gitlab-ci-hello",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Tests passed!\""
  },
  "author": "",
  "license": "ISC"
}
```

**2. Tạo file `index.js`:**
```javascript
console.log("Hello, GitLab CI!");
```

**3. Tạo file `.gitlab-ci.yml`:**
```yaml
# Sử dụng Docker image của Node.js phiên bản 16
image: node:16

# Định nghĩa các stage
stages:
  - build
  - test

# Job thuộc stage 'build'
install_dependencies:
  stage: build
  script:
    - echo "Bắt đầu cài đặt dependencies..."
    - npm install
    - echo "Cài đặt hoàn tất."
  artifacts:
    paths:
      - node_modules/ # Lưu lại thư mục node_modules cho stage sau
    expire_in: 1 hour # Xóa artifacts sau 1 giờ

# Job thuộc stage 'test'
run_tests:
  stage: test
  script:
    - echo "Bắt đầu chạy unit tests..."
    - npm test
    - echo "Tests hoàn tất."
```

**Kết quả:**
Khi bạn push 3 file này lên GitLab, một pipeline mới sẽ tự động được tạo ra.
-   Đầu tiên, job `install_dependencies` sẽ chạy. Nó dùng `npm install` để cài các gói cần thiết. Sau khi thành công, nó sẽ lưu thư mục `node_modules` lại.
-   Tiếp theo, job `run_tests` sẽ chạy. Nó sẽ tự động có thư mục `node_modules` từ job trước và thực thi lệnh `npm test`.

---

### 5. Sử dụng Biến (Variables)

Bạn có thể định nghĩa các biến để tái sử dụng trong file `.gitlab-ci.yml` hoặc trong UI của GitLab (Settings > CI/CD > Variables).

```yaml
variables:
  NODE_ENV: "test"

run_tests:
  stage: test
  script:
    - echo "Giá trị biến NODE_ENV là: $NODE_ENV"
    - npm test
```
Các biến được định nghĩa trong UI thường dùng để lưu các thông tin nhạy cảm như API key, mật khẩu...

---

### 6. Artifacts

Artifacts là các file được tạo ra bởi một job. Chúng rất hữu ích để:
-   Truyền kết quả từ một job ở stage này cho một job ở stage khác (như ví dụ `node_modules` ở trên).
-   Lưu lại sản phẩm cuối cùng của pipeline (ví dụ: file binary đã được biên dịch, báo cáo kiểm thử) để bạn có thể tải về.

## ✍️ Bài tập thực hành (Exercises)

Phần thực hành này sẽ hướng dẫn bạn từng bước xây dựng và mở rộng một pipeline CI/CD trên GitLab.

**Yêu cầu:** Bạn cần có một tài khoản GitLab và tạo một dự án mới (private hoặc public) để thực hành.

**Bài 1: Tạo Pipeline CI đầu tiên**
1.  **Trên máy của bạn:**
    -   Tạo một thư mục dự án, `cd` vào đó và `git init`.
    -   Tạo 3 file: `package.json`, `index.js`, và `.gitlab-ci.yml` với nội dung chính xác như trong phần hướng dẫn số 4.
2.  **Trên GitLab:**
    -   Tạo một dự án mới.
    -   Làm theo hướng dẫn của GitLab để kết nối dự án trên máy bạn với kho chứa từ xa này (`git remote add origin ...`).
3.  **Thực thi:**
    -   `git add .`, `git commit -m "Initial CI pipeline"`, và `git push origin main`.
4.  **Kiểm tra:**
    -   Vào dự án của bạn trên GitLab, đi đến mục `Build > Pipelines` (hoặc `CI/CD > Pipelines`).
    -   Quan sát pipeline được thực thi. Click vào nó để xem các stage và job.
    -   Click vào từng job (`install_dependencies`, `run_tests`) để xem log chi tiết.

**Bài 2: Thêm một Stage mới**
1.  Trên máy của bạn, tạo một file `build-script.js` với nội dung: `console.log("Đây là quá trình build giả lập...");`.
2.  Mở file `package.json`, thêm một script mới vào phần `"scripts"`: `"build": "node build-script.js"`.
3.  Sửa file `.gitlab-ci.yml`:
    -   Thêm `build_app` vào danh sách `stages`, đặt nó ở giữa `build` và `test`.
    -   Tạo một job mới có tên `build_job` (hoặc tên tùy ý).
    -   Khai báo `stage: build_app` cho job này.
    -   Trong phần `script`, thêm lệnh `npm run build`.
4.  Commit và push file `.gitlab-ci.yml` đã thay đổi. Quan sát pipeline mới có thêm stage `build_app`.

**Bài 3: Sử dụng Artifacts để tạo "Báo cáo"**
1.  Trong job `build_job` bạn vừa tạo ở Bài 2, hãy tạo ra một "báo cáo build" giả. Sửa lại phần `script` của job này như sau:
    ```yaml
    script:
      - npm run build
      - echo "Build successful at $(date)" > build-report.txt
    ```
2.  Vẫn trong job `build_job`, thêm khối `artifacts` để lưu lại file báo cáo:
    ```yaml
    artifacts:
      paths:
        - build-report.txt
    ```
3.  Commit và push thay đổi. Sau khi pipeline chạy xong, vào trang chi tiết của pipeline, bạn sẽ thấy một mục "Job artifacts" ở phía bên phải. Hãy thử tải file `build-report.txt` về.

**Bài 4: Sử dụng Biến môi trường (Variables)**
1.  Vào dự án của bạn trên GitLab, đi đến `Settings > CI/CD`.
2.  Mở rộng phần `Variables` và click `Add variable`.
3.  Tạo một biến mới:
    -   **Key:** `DEPLOY_USER`
    -   **Value:** (Tên của bạn)
4.  Quay lại file `.gitlab-ci.yml`, thêm một stage cuối cùng tên là `deploy`.
5.  Tạo một job mới tên `deploy_job` thuộc stage `deploy`.
6.  Trong script của job này, hãy in ra giá trị của biến bạn vừa tạo:
    ```yaml
    script:
      - echo "Deploying the application as user: $DEPLOY_USER..."
    ```
7.  Commit và push. Xem log của job `deploy_job` để thấy rằng nó đã in ra đúng tên của bạn. Đây là cách cơ bản để truyền các thông tin nhạy cảm (như API key, password) vào pipeline một cách an toàn.

---

Trong bài học tiếp theo, chúng ta sẽ tìm hiểu về Docker, một công nghệ sẽ giúp pipeline của chúng ta trở nên mạnh mẽ và nhất quán hơn rất nhiều.

[Bài trước: Lý thuyết về CI/CD](../06-ci-cd-theory/) | [Quay lại Mục lục chính](../../README.md) | [Bài tiếp theo: Giới thiệu về Docker](../../Lesson03-containerization-and-orchestration/08-docker-introduction/)