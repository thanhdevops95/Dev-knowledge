# Lời giải và Hướng dẫn - Bài 8: Giới thiệu về Docker

Chào mừng bạn đến với bài thực hành Docker. Tôi đã chuẩn bị sẵn một ứng dụng Node.js đơn giản và một `Dockerfile` để bạn thực hành.

**Yêu cầu:** Máy tính của bạn phải được cài đặt Docker và Docker đang chạy.

Hãy mở terminal, di chuyển vào thư mục của bài tập này (`workspare/.../08-docker-introduction`) và làm theo các bước dưới đây.

---

### Giải thích các file đã tạo

-   `app.js`: Một web server Express cực kỳ đơn giản, lắng nghe trên cổng 8080 và trả về dòng chữ "Hello from Docker Container!".
-   `package.json`: Khai báo thông tin dự án và dependency `express`.
-   `Dockerfile`: "Bản thiết kế" chứa các chỉ dẫn để Docker xây dựng image cho ứng dụng.

---

### Bài 1: Container hóa ứng dụng Node.js

**Mục tiêu:** Xây dựng một Docker image từ mã nguồn đã có.

**1. Cài đặt dependencies trên máy local (chỉ để `package-lock.json` được tạo ra):**

Chạy lệnh sau trong terminal. Thao tác này sẽ tạo ra file `package-lock.json` và thư mục `node_modules`. `Dockerfile` của chúng ta sẽ sử dụng file `package-lock.json` để đảm bảo việc cài đặt dependencies bên trong container là nhất quán.

```bash
npm install
```

**2. Xây dựng Docker image:**

Lệnh này sẽ đọc `Dockerfile` trong thư mục hiện tại, thực thi các bước trong đó, và tạo ra một image có tên là `my-first-app`.

```bash
docker build -t my-first-app .
```
-   **Giải thích:**
    -   `docker build`: Lệnh để xây dựng image.
    -   `-t my-first-app`: `-t` (tag) là để đặt tên và phiên bản cho image. Ở đây ta đặt tên là `my-first-app`.
    -   `.`: Dấu chấm ở cuối chỉ định rằng context (ngữ cảnh) để build là thư mục hiện tại.

**3. Kiểm tra image:**

Liệt kê tất cả các image có trên máy của bạn.

```bash
docker images
```
- **Kết quả mong đợi:** Bạn sẽ thấy `my-first-app` xuất hiện trong danh sách.

---

### Bài 2: Chạy và Tương tác với Container

**Mục tiêu:** Khởi chạy một container từ image đã tạo và tương tác với nó.

**1. Chạy container:**

```bash
docker run --name web-app -p 5000:8080 -d my-first-app
```
-   **Giải thích:**
    -   `docker run`: Lệnh để tạo và chạy một container từ một image.
    -   `--name web-app`: Đặt tên cho container là `web-app` để dễ quản lý.
    -   `-p 5000:8080`: Ánh xạ (map) cổng. Nó chuyển tiếp traffic từ cổng `5000` trên máy của bạn (host) vào cổng `8080` bên trong container (nơi ứng dụng Node.js đang lắng nghe).
    -   `-d`: Chạy container ở chế độ nền (detached).
    -   `my-first-app`: Tên của image mà chúng ta muốn chạy.

**2. Kiểm tra trên trình duyệt:**

Mở trình duyệt và truy cập `http://localhost:5000`. Bạn sẽ thấy dòng chữ "Hello from Docker Container!".

**3. Xem các container đang chạy:**

```bash
docker ps
```
- **Kết quả mong đợi:** Bạn sẽ thấy một container có tên `web-app` đang ở trạng thái `Up`.

**4. Xem log của ứng dụng:**

Để xem output mà `console.log` đã in ra bên trong container.

```bash
docker logs web-app
```
- **Kết quả mong đợi:** `App is running on port 8080`

**5. Thực thi một lệnh bên trong container:**

Lệnh này cho phép bạn "chui vào" container và chạy một lệnh.

```bash
docker exec -it web-app ls -l /app
```
-   **Giải thích:**
    -   `docker exec`: Thực thi một lệnh trong một container đang chạy.
    -   `-it`: Chế độ tương tác.
    -   `web-app`: Tên container.
    -   `ls -l /app`: Lệnh cần chạy bên trong container.
- **Kết quả mong đợi:** Bạn sẽ thấy danh sách các file của dự án (`app.js`, `package.json`,...) nằm trong thư mục `/app` của container.

---

### Bài 3: Quản lý Vòng đời Container

**Mục tiêu:** Học cách dừng, khởi động lại, và xóa container.

1.  **Dừng container:**
    ```bash
    docker stop web-app
    ```
2.  **Kiểm tra lại:** Chạy `docker ps`. Bạn sẽ không thấy container `web-app` nữa.
3.  **Xem tất cả container (kể cả đã dừng):**
    ```bash
    docker ps -a
    ```
    - **Kết quả mong đợi:** Bạn sẽ thấy `web-app` với trạng thái `Exited`.
4.  **Khởi động lại container:**
    ```bash
    docker start web-app
    ```
    - Truy cập lại `http://localhost:5000`, ứng dụng sẽ chạy lại.
5.  **Dọn dẹp:** Khi thực hành xong, hãy dừng và xóa container để giải phóng tài nguyên.
    ```bash
    docker stop web-app
    docker rm web-app
    ```

---

### Bài 4 (Nâng cao): Chia sẻ Image qua Docker Hub

**Mục tiêu:** Đẩy image của bạn lên một registry công khai để có thể chia sẻ hoặc sử dụng ở nơi khác.

**Yêu cầu:** Có tài khoản Docker Hub.

1.  **Đăng nhập:**
    ```bash
    docker login
    ```
    (Nhập username và password Docker Hub của bạn)
2.  **Gắn thẻ (tag) lại image:**
    Image cần được đặt tên theo định dạng `[username]/[repository]:[tag]`.
    ```bash
    # Thay aivn-user bằng tên tài khoản Docker Hub của bạn
    docker tag my-first-app aivn-user/my-first-app:1.0
    ```
3.  **Đẩy image lên Docker Hub:**
    ```bash
    docker push aivn-user/my-first-app:1.0
    ```
4.  **Kiểm tra:**
    Bây giờ bạn có thể vào trang Docker Hub của mình để xem image đã được tải lên. Bạn cũng có thể thử xóa image trên máy (`docker rmi aivn-user/my-first-app:1.0`) và kéo lại nó (`docker pull aivn-user/my-first-app:1.0`).

Chúc mừng bạn đã hoàn thành các bước cơ bản nhất để làm việc với Docker!