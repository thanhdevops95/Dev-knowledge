# Bài 8: Giới thiệu về Docker

## 🎯 Mục tiêu bài học

-   Hiểu được vấn đề "It works on my machine" (Nó chạy trên máy tôi) và cách container giải quyết nó.
-   Phân biệt được sự khác nhau giữa Container và Máy ảo (Virtual Machine).
-   Nắm vững các khái niệm cốt lõi của Docker: Image, Container, Dockerfile.
-   Thực hành các lệnh Docker cơ bản: `docker build`, `docker run`, `docker ps`, `docker images`.
-   Viết được một `Dockerfile` đơn giản để "container hóa" một ứng dụng.

## 📖 Nội dung chính

1.  **Vấn đề:** "It works on my machine!"
2.  **Container vs. Máy ảo (VM):** So sánh kiến trúc và hiệu năng.
3.  **Các khái niệm cốt lõi:**
    -   **Docker Image:** Khuôn mẫu chỉ đọc (read-only template).
    -   **Dockerfile:** "Bản thiết kế" để xây dựng một image.
    -   **Container:** Một thực thể (instance) chạy được của một image.
4.  **Thực hành các lệnh Docker:**
    -   `docker build`: Xây dựng image từ Dockerfile.
    -   `docker run`: Chạy một container từ image.
    -   `docker ps`: Liệt kê các container đang chạy.
    -   `docker images`: Liệt kê các image có trên máy.
5.  **Docker Hub:** "GitHub" dành cho Docker image.
6.  **Docker Compose:** Định nghĩa và chạy ứng dụng đa container.

## 🛠️ Công cụ & Lý thuyết

-   **Container Runtime:** <u>Docker</u>, Podman, containerd.
-   **Công cụ build:** <u>Docker</u>, Buildah.
-   **Orchestration (Local):** <u>Docker Compose</u>.
-   **Lý thuyết:** Containerization, OS-level virtualization, Immutable Infrastructure.

---

# Nội dung chi tiết - Bài 8: Giới thiệu về Docker

Một trong những vấn đề kinh điển trong phát triển phần mềm là "It works on my machine!" (Nó chạy trên máy tôi!). Một ứng dụng có thể chạy hoàn hảo trên máy của lập trình viên, nhưng lại lỗi khi triển khai lên môi trường Staging hoặc Production. Nguyên nhân thường là do sự khác biệt về môi trường: phiên bản hệ điều hành, các thư viện hệ thống, biến môi trường, ... Docker ra đời để giải quyết triệt để vấn đề này.

---

### 1. Vấn đề: "It works on my machine!"

Docker giải quyết vấn đề này bằng cách **đóng gói (package) ứng dụng cùng với tất cả các thứ nó cần để chạy (thư viện, file cấu hình, runtime,...) vào một đơn vị duy nhất gọi là Container.**

Container này có thể chạy một cách nhất quán trên mọi máy tính đã cài đặt Docker, từ laptop của lập trình viên cho đến các máy chủ trên cloud. Môi trường đã được "đóng băng" bên trong container.

---

### 2. Container vs. Máy ảo (VM)

| Tiêu chí          | Máy ảo (Virtual Machine - VM)                                  | Container                                                    |
| ----------------- | -------------------------------------------------------------- | ------------------------------------------------------------ |
| **Ảo hóa**        | Ảo hóa **phần cứng**. Mỗi VM có một hệ điều hành (Guest OS) riêng. | Ảo hóa **hệ điều hành**. Các container chia sẻ chung nhân (kernel) của hệ điều hành máy chủ (Host OS). |
| **Kích thước**     | Lớn (vài GB).                                                  | Nhỏ (vài MB đến vài trăm MB).                                 |
| **Thời gian khởi động** | Chậm (vài phút).                                               | Nhanh (vài giây hoặc mili giây).                             |
| **Hiệu năng**     | Tốn nhiều tài nguyên (CPU, RAM).                               | Nhẹ và hiệu năng gần bằng với chạy trực tiếp trên máy chủ.      |
| **Cô lập**        | Rất tốt, cô lập hoàn toàn ở mức phần cứng.                     | Tốt, cô lập ở mức process.                                   |

**Tóm lại:** Container nhẹ hơn, nhanh hơn, và hiệu quả hơn VM rất nhiều.

---

### 3. Các khái niệm cốt lõi

-   **Image (Khuôn mẫu):** Là một gói chỉ-đọc (read-only) chứa mã nguồn ứng dụng, một runtime, các thư viện, biến môi trường và file cấu hình.
    > Nếu ví von, Image giống như một **khuôn làm bánh**.

-   **Container (Thực thể):** Là một thực thể (instance) đang chạy của một Image. Bạn có thể tạo, khởi động, dừng, di chuyển và xóa container.
    > Container chính là **cái bánh** được tạo ra từ khuôn đó. Bạn có thể tạo ra nhiều cái bánh từ cùng một khuôn.

-   **Dockerfile (Bản thiết kế):** Là một file văn bản chứa các chỉ dẫn để Docker tự động xây dựng (build) một Image.
    > Dockerfile là **công thức** để tạo ra cái khuôn làm bánh.

---

### 4. Thực hành các lệnh Docker

Hãy container hóa một ứng dụng Node.js đơn giản.

**1. Tạo file `app.js`:**
```javascript
const express = require('express');
const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
  res.send('Hello from Docker Container!');
});

app.listen(PORT, () => {
  console.log(`App is running on port ${PORT}`);
});
```
**2. Tạo file `package.json`:**
Chạy `npm init -y` và `npm install express`.

**3. Tạo file `Dockerfile`:**
```dockerfile
# 1. Chọn một image gốc
FROM node:16-alpine

# 2. Tạo một thư mục làm việc bên trong image
WORKDIR /app

# 3. Sao chép file package.json và package-lock.json
COPY package*.json ./

# 4. Cài đặt dependencies
RUN npm install

# 5. Sao chép toàn bộ mã nguồn còn lại
COPY . .

# 6. Mở cổng 8080 để bên ngoài có thể truy cập vào
EXPOSE 8080

# 7. Lệnh để chạy ứng dụng khi container khởi động
CMD [ "node", "app.js" ]
```

**Các lệnh Docker:**

-   **`docker build -t my-nodejs-app .`**: Xây dựng một image từ Dockerfile trong thư mục hiện tại và đặt tên (`-t`) cho nó là `my-nodejs-app`.
-   **`docker images`**: Liệt kê các image, bạn sẽ thấy `my-nodejs-app` vừa được tạo.
-   **`docker run -p 4000:8080 -d my-nodejs-app`**: Chạy một container từ image `my-nodejs-app`.
    -   `-p 4000:8080`: Ánh xạ (map) cổng 4000 trên máy chủ vào cổng 8080 bên trong container.
    -   `-d`: Chạy ở chế độ nền (detached).
-   Mở trình duyệt và truy cập `http://localhost:4000`, bạn sẽ thấy "Hello from Docker Container!".
-   **`docker ps`**: Liệt kê các container đang chạy.
-   **`docker stop <container_id>`**: Dừng container.
-   **`docker rm <container_id>`**: Xóa container.

---

### 5. Docker Hub

Docker Hub là một kho lưu trữ registry cho các Docker image. Nó giống như GitHub cho code vậy. Bạn có thể:
-   `docker pull ubuntu`: Tải image `ubuntu` chính thức về máy.
-   `docker push your-username/my-nodejs-app`: Đẩy image của bạn lên Docker Hub để chia sẻ với người khác hoặc sử dụng trong pipeline CI/CD.

---

### 6. Docker Compose

Khi ứng dụng của bạn phức tạp hơn, ví dụ gồm một web server, một database, và một Redis cache, việc chạy 3 lệnh `docker run` riêng lẻ rất bất tiện. `docker-compose` cho phép bạn định nghĩa và chạy toàn bộ ứng dụng đa container bằng một file YAML duy nhất (`docker-compose.yml`).

```yaml
version: '3.8'
services:
  web:
    build: . # Build image từ Dockerfile trong thư mục hiện tại
    ports:
      - "4000:8080"
  database:
    image: "postgres:13"
    environment:
      - POSTGRES_PASSWORD=mysecretpassword
```
Chỉ cần chạy `docker-compose up`, toàn bộ ứng dụng của bạn sẽ được khởi chạy.

## ✍️ Bài tập thực hành (Exercises)

Phần thực hành này sẽ giúp bạn nắm vững vòng đời làm việc cơ bản với Docker, từ lúc viết code đến lúc chia sẻ image.

**Yêu cầu:** Đã cài đặt Docker Desktop (trên Windows/Mac) hoặc Docker Engine (trên Linux).

**Bài 1: Container hóa ứng dụng Node.js**
1.  Tạo một thư mục mới cho dự án, ví dụ `docker-practice`.
2.  Bên trong thư mục đó, tạo các file `app.js` và `package.json` như hướng dẫn trong bài. Đừng quên chạy `npm init -y` và `npm install express`.
3.  Tạo file `Dockerfile` với nội dung chính xác như trong phần hướng dẫn số 4.
4.  Mở terminal trong thư mục dự án và chạy lệnh sau để xây dựng image:
    ```bash
    docker build -t my-first-app .
    ```
5.  Kiểm tra xem image đã được tạo thành công chưa bằng lệnh `docker images`. Bạn sẽ thấy image `my-first-app` trong danh sách.

**Bài 2: Chạy và Tương tác với Container**
1.  Chạy container từ image bạn vừa tạo:
    ```bash
    docker run --name web-app -p 5000:8080 -d my-first-app
    ```
    *Ghi chú: `--name web-app` đặt tên cho container để dễ quản lý.*
2.  Mở trình duyệt và truy cập `http://localhost:5000`. Bạn có thấy thông điệp "Hello from Docker Container!" không?
3.  Sử dụng `docker ps` để xem container `web-app` đang ở trạng thái "Up".
4.  Xem log mà ứng dụng Node.js đã in ra bên trong container: `docker logs web-app`.
5.  Thực thi một lệnh **bên trong** container đang chạy để xem các file trong thư mục `/app`:
    ```bash
    docker exec -it web-app ls -l /app
    ```

**Bài 3: Quản lý Vòng đời Container**
1.  Dừng container đang chạy: `docker stop web-app`.
2.  Kiểm tra lại với `docker ps` (sẽ không thấy container nữa).
3.  Sử dụng `docker ps -a` để xem tất cả các container, kể cả những container đã dừng. Bạn sẽ thấy `web-app` với trạng thái "Exited".
4.  Khởi động lại container đã dừng: `docker start web-app`.
5.  Cuối cùng, khi đã thực hành xong, hãy dọn dẹp bằng cách dừng và xóa container: `docker stop web-app` sau đó `docker rm web-app`.

**Bài 4 (Nâng cao): Chia sẻ Image qua Docker Hub**
1.  Tạo một tài khoản trên [Docker Hub](https://hub.docker.com/).
2.  Trên máy của bạn, đăng nhập vào Docker Hub bằng lệnh `docker login`.
3.  "Tag" (gắn thẻ) lại image của bạn để chuẩn bị push, với định dạng `[Tên tài khoản Docker Hub]/[Tên image]:[Phiên bản]`:
    ```bash
    # Thay aivn-user bằng tên tài khoản Docker Hub của bạn
    docker tag my-first-app aivn-user/my-first-app:1.0
    ```
4.  Đẩy image của bạn lên Docker Hub:
    ```bash
    docker push aivn-user/my-first-app:1.0
    ```
5.  Để kiểm tra, bạn có thể xóa image này khỏi máy mình (`docker rmi aivn-user/my-first-app:1.0`), sau đó kéo lại nó từ Docker Hub (`docker pull aivn-user/my-first-app:1.0`).

---

Trong bài học tiếp theo, chúng ta sẽ giải quyết vấn đề: "Làm thế nào để quản lý hàng trăm, hàng ngàn container chạy trên nhiều máy chủ?". Câu trả lời chính là Kubernetes.

[Bài trước: Xây dựng CI/CD Pipeline với GitLab CI](../../Lesson02-scm-and-ci/07-gitlab-ci-pipeline/) | [Quay lại Mục lục chính](../../../training-roadmap/README.md) | [Bài tiếp theo: Kubernetes (K8s) - Điều phối Container](../09-kubernetes-basics/)