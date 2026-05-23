# ❓ Quiz: Docker Compose

> **Knowledge Check for Docker Compose (15 Questions)**
>
> *Kiểm tra kiến thức Docker Compose (15 câu hỏi).*

---

### Q1

Version nào của Compose file được khuyến nghị?

- a) 2
- b) 3
- c) 3.8
- d) Không cần version  

---

### Q2

`depends_on` làm gì?

- a) Đợi service healthy (Đợi service khỏe mạnh)
- b) Set startup order (Thiết lập thứ tự khởi động)
- c) Link containers (Liên kết container)
- d) Share network (Chia sẻ mạng)  

---

### Q3

Lệnh start services ở background?

- a) `docker compose up`
- b) `docker compose up -d`
- c) `docker compose start`
- d) `docker compose run`  

---

### Q4

Named volume được define ở đâu?

- a) services
- b) networks
- c) volumes (top-level)
- d) configs  

---

### Q5

Cách dùng environment variable từ .env?

- a) `${VAR_NAME}`
- b) `$VAR_NAME`
- c) `%VAR_NAME%`
- d) a và b  

---

### Q6

Override file mặc định?

- a) docker-compose.dev.yml
- b) docker-compose.override.yml
- c) docker-compose.local.yml
- d) override.yml  

---

### Q7

`restart: unless-stopped` làm gì?

- a) Never restart (Không bao giờ khởi động lại)
- b) Always restart (Luôn khởi động lại)
- c) Restart unless manually stopped (Khởi động lại trừ khi dừng thủ công)
- d) Restart on failure (Khởi động lại khi lỗi)  

---

### Q8

Internal network có đặc điểm gì?

- a) Faster (Nhanh hơn)
- b) No external access (Không có truy cập bên ngoài)
- c) Encrypted (Được mã hóa)
- d) Load balanced (Được cân bằng tải)  

---

### Q9

Lệnh view real-time logs?

- a) `docker compose log`
- b) `docker compose logs -f`
- c) `docker compose tail`
- d) `docker compose watch`  

---

### Q10

Cách mount read-only?

- a) `./config:/config:readonly`
- b) `./config:/config:ro`
- c) `./config:/config[readonly]`
- d) Không thể  

---

### Q11

Build với custom Dockerfile?

- a) `dockerfile: Dockerfile.prod`
- b) `file: Dockerfile.prod`
- c) `build_file: Dockerfile.prod`
- d) `FROM: Dockerfile.prod`  

---

### Q12

Exec into running service?

- a) `docker compose exec service sh`
- b) `docker compose run service sh`
- c) `docker compose shell service`
- d) `docker compose enter service`  

---

### Q13

Scale service?

- a) `docker compose scale api=3`
- b) `docker compose up --scale api=3`
- c) `docker compose replicas api 3`
- d) `docker compose --replicas 3 api`  

---

### Q14

Remove volumes khi down?

- a) `docker compose down --volumes`
- b) `docker compose down -v`
- c) Cả a và b
- d) `docker compose down --rm-volumes`  

---

### Q15

Health check condition?

- a) `condition: service_started`
- b) `condition: service_healthy`
- c) `condition: service_ready`
- d) a và b  

---

## 📝 Answers

<details>
<summary>Click để xem đáp án</summary>

| Q | A |
|---|---|
| 1 | c |
| 2 | b |
| 3 | b |
| 4 | c |
| 5 | d |
| 6 | b |
| 7 | c |
| 8 | b |
| 9 | b |
| 10 | b |
| 11 | a |
| 12 | a |
| 13 | b |
| 14 | c |
| 15 | d |

</details>

---

**[← Back to README](./README.md)**
