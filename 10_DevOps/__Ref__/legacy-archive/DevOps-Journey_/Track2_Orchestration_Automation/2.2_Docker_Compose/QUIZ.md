# ❓ Quiz: Docker Compose

> **Knowledge Check for Docker Compose (15 Questions)**
>
> *Kiểm tra kiến thức Docker Compose (15 câu hỏi).*

---

### Q1: Compose File Version

Which Compose file version is recommended?

*(Version nào của Compose file được khuyến nghị?)*

- a) 2
- b) 3
- c) 3.8
- d) No version needed *(Không cần version)*

---

### Q2: depends_on Directive

What does `depends_on` do?

*(`depends_on` làm gì?)*

- a) Wait for service healthy *(Đợi service healthy)*
- b) Set startup order *(Thiết lập thứ tự khởi động)*
- c) Link containers *(Liên kết container)*
- d) Share network *(Chia sẻ mạng)*

---

### Q3: Background Services

Command to start services in background?

*(Lệnh start services ở background?)*

- a) `docker compose up`
- b) `docker compose up -d`
- c) `docker compose start`
- d) `docker compose run`

---

### Q4: Named Volumes

Where are named volumes defined?

*(Named volume được define ở đâu?)*

- a) services
- b) networks
- c) volumes (top-level)
- d) configs

---

### Q5: Environment Variables

How to use environment variable from .env?

*(Cách dùng environment variable từ .env?)*

- a) `${VAR_NAME}`
- b) `$VAR_NAME`
- c) `%VAR_NAME%`
- d) a and b *(a và b)*

---

### Q6: Override File

What is the default override file?

*(Override file mặc định?)*

- a) docker-compose.dev.yml
- b) docker-compose.override.yml
- c) docker-compose.local.yml
- d) override.yml

---

### Q7: Restart Policy

What does `restart: unless-stopped` do?

*(`restart: unless-stopped` làm gì?)*

- a) Never restart *(Không bao giờ khởi động lại)*
- b) Always restart *(Luôn khởi động lại)*
- c) Restart unless manually stopped *(Khởi động lại trừ khi dừng thủ công)*
- d) Restart on failure *(Khởi động lại khi lỗi)*

---

### Q8: Internal Network

What is special about internal network?

*(Internal network có đặc điểm gì?)*

- a) Faster *(Nhanh hơn)*
- b) No external access *(Không có truy cập bên ngoài)*
- c) Encrypted *(Được mã hóa)*
- d) Load balanced *(Được cân bằng tải)*

---

### Q9: Real-time Logs

Command to view real-time logs?

*(Lệnh view real-time logs?)*

- a) `docker compose log`
- b) `docker compose logs -f`
- c) `docker compose tail`
- d) `docker compose watch`

---

### Q10: Read-only Mount

How to mount read-only?

*(Cách mount read-only?)*

- a) `./config:/config:readonly`
- b) `./config:/config:ro`
- c) `./config:/config[readonly]`
- d) Not possible *(Không thể)*

---

### Q11: Custom Dockerfile

How to build with custom Dockerfile?

*(Build với custom Dockerfile?)*

- a) `dockerfile: Dockerfile.prod`
- b) `file: Dockerfile.prod`
- c) `build_file: Dockerfile.prod`
- d) `FROM: Dockerfile.prod`

---

### Q12: Exec into Service

How to exec into running service?

*(Exec into running service?)*

- a) `docker compose exec service sh`
- b) `docker compose run service sh`
- c) `docker compose shell service`
- d) `docker compose enter service`

---

### Q13: Scale Service

How to scale a service?

*(Scale service?)*

- a) `docker compose scale api=3`
- b) `docker compose up --scale api=3`
- c) `docker compose replicas api 3`
- d) `docker compose --replicas 3 api`

---

### Q14: Remove Volumes

How to remove volumes when down?

*(Remove volumes khi down?)*

- a) `docker compose down --volumes`
- b) `docker compose down -v`
- c) Both a and b *(Cả a và b)*
- d) `docker compose down --rm-volumes`

---

### Q15: Health Check Condition

What are valid health check conditions?

*(Health check condition?)*

- a) `condition: service_started`
- b) `condition: service_healthy`
- c) `condition: service_ready`
- d) a and b *(a và b)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | c | 3.8 is recommended for most features |
| 2 | b | Sets container startup order only |
| 3 | b | -d flag runs in detached mode |
| 4 | c | Top-level volumes section |
| 5 | d | Both syntaxes work |
| 6 | b | Auto-loaded override file |
| 7 | c | Restarts unless manually stopped |
| 8 | b | No external network access |
| 9 | b | -f follows log output |
| 10 | b | :ro suffix for read-only |
| 11 | a | dockerfile key in build section |
| 12 | a | exec for running containers |
| 13 | b | --scale flag with up command |
| 14 | c | Both flags work |
| 15 | d | started and healthy are valid |

</details>

---

**[← Back to README](./README.md)**
