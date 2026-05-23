# ❓ Quiz: Docker Fundamentals

> **Knowledge Check for Docker (20 Questions)**
>
> *Kiểm tra kiến thức Docker (20 câu hỏi).*

---

### Q1: Container vs VM

How is a container different from a VM?

*(Container khác VM như thế nào?)*

- a) Container has its own OS *(Container có OS riêng)*
- b) Container shares host kernel *(Container chia sẻ kernel của host)*
- c) VM is lighter than container *(VM nhẹ hơn container)*
- d) No difference *(Không khác nhau)*

---

### Q2: Docker Image

What is a Docker image?

*(Docker image là gì?)*

- a) Running container (Container đang chạy)
- b) Read-only template (Mẫu chỉ đọc)
- c) Docker configuration (Cấu hình Docker)
- d) Virtual machine (Máy ảo)  

---

### Q3: Dockerfile CMD

What is the `CMD` instruction in Dockerfile used for?

*(Lệnh `CMD` trong Dockerfile dùng để?)*

- a) Run command during build (Chạy lệnh trong quá trình build)
- b) Set default command khi container start (Thiết lập lệnh mặc định khi container chạy)
- c) Copy files (Sao chép tệp)
- d) Set environment (Thiết lập môi trường)  

---

### Q4: EXPOSE

What does `EXPOSE 80` do in Dockerfile?

*(`EXPOSE 80` trong Dockerfile làm gì?)*

- a) Publish port 80 (Công khai port 80)
- b) Document port 80 (Khai báo port 80)
- c) Block port 80 (Chặn port 80)
- d) Forward port 80 (Chuyển tiếp port 80)  

---

### Q5: Volume

What is Docker volume used for?

*(Docker volume dùng để?)*

- a) Increase container size (Tăng kích thước container)
- b) Persist data (Lưu trữ dữ liệu bền vững)
- c) Network containers (Kết nối mạng container)
- d) Build images (Xây dựng image)  

---

### Q6: Port Mapping

What does `docker run -p 8080:80` mean?

*(`docker run -p 8080:80` có nghĩa gì?)*

- a) Container 8080 maps to host 80
- b) Host 8080 maps to container 80
- c) Both ports 8080 (Cả hai port 8080)
- d) No mapping (Không map)  

---

### Q7: Detached Mode

What does the `-d` flag in `docker run -d` mean?

*(Flag `-d` trong `docker run -d` có nghĩa gì?)*

- a) Debug mode (Chế độ gỡ lỗi)
- b) Detached (background) (Chạy ngầm)
- c) Delete after run (Xóa sau khi chạy)
- d) Disk mode (Chế độ đĩa)  

---

### Q8: Docker Network

What is the default Docker network type?

*(Network type default của Docker là gì?)*

- a) host
- b) bridge
- c) none
- d) overlay  

---

### Q9: RUN vs CMD

`RUN` khác `CMD` như thế nào?

- a) RUN execute at runtime, CMD at build
- b) RUN execute at build, CMD at runtime (RUN chạy khi build, CMD chạy khi runtime)
- c) Same thing (Giống nhau)
- d) RUN for files, CMD for commands (RUN cho file, CMD cho lệnh)  

---

### Q10: COPY vs ADD

`COPY` khác `ADD` như thế nào?

- a) Không khác
- b) ADD can extract archives and URL (ADD có thể giải nén và tải URL)
- c) COPY can extract archives (COPY có thể giải nén)
- d) ADD không copy được  

---

### Q11: Layer

Mỗi instruction trong Dockerfile tạo gì?

- a) Container
- b) Image layer
- c) Volume
- d) Network  

---

### Q12: Prune

`docker system prune` làm gì?

- a) Delete all containers and images (Xóa tất cả container và images)
- b) Remove unused data (Xóa dữ liệu không sử dụng)
- c) Restart Docker (Khởi động lại Docker)
- d) Update Docker (Cập nhật Docker)  

---

### Q13: Entrypoint

`ENTRYPOINT` khác `CMD` như thế nào?

- a) ENTRYPOINT can be overridden easily (ENTRYPOINT dễ bị ghi đè)
- b) CMD appends to ENTRYPOINT (CMD nối vào ENTRYPOINT)
- c) Same thing (Giống nhau)
- d) ENTRYPOINT for files only (ENTRYPOINT chỉ cho file)  

---

### Q14: Multi-stage

Multi-stage build dùng để?

- a) Build multiple apps (Build nhiều app)
- b) Reduce final image size (Giảm kích thước image cuối cùng)
- c) Run multiple containers (Chạy nhiều container)
- d) Create multiple networks (Tạo nhiều mạng)  

---

### Q15: Tag

Nếu không specify tag, default tag là gì?

- a) v1
- b) default
- c) latest
- d) none  

---

### Q16: Logs

Lệnh xem logs của container running?

- a) `docker logs container_name`
- b) `docker show logs`
- c) `docker container logs`
- d) a và c đều đúng  

---

### Q17: Health Check

`HEALTHCHECK` instruction dùng để?

- a) Check Docker health (Kiểm tra sức khỏe Docker)
- b) Define container health check (Định nghĩa kiểm tra sức khỏe container)
- c) Check host health (Kiểm tra sức khỏe host)
- d) Monitor resources (Giám sát tài nguyên)  

---

### Q18: Resource Limits

Flag nào giới hạn memory?

- a) `--memory-limit`
- b) `--mem`
- c) `-m` or `--memory`
- d) `--ram`  

---

### Q19: Registry

Docker Hub là gì?

- a) Docker documentation (Tài liệu Docker)
- b) Public container registry (Kho lưu trữ container công cộng)
- c) Docker CLI
- d) Docker desktop  

---

### Q20: Context

Build context là gì?

- a) Docker daemon
- b) Files sent to daemon for build (Các file được gửi tới daemon để build)
- c) Dockerfile location (Vị trí Dockerfile)
- d) Environment variables (Biến môi trường)  

---

## 📝 Answers

<details>
<summary>Click để xem đáp án</summary>

| Q | A | Q | A |
|---|---|---|---|
| 1 | b | 11 | b |
| 2 | b | 12 | b |
| 3 | b | 13 | b |
| 4 | b | 14 | b |
| 5 | b | 15 | c |
| 6 | b | 16 | d |
| 7 | b | 17 | b |
| 8 | b | 18 | c |
| 9 | b | 19 | b |
| 10 | b | 20 | b |

</details>

---

**[← Back to README](./README.md)**
