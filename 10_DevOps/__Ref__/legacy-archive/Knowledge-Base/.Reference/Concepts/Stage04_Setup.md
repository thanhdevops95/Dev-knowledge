# 🛠️ GIAI ĐOẠN 4: CHUẨN BỊ DOCKER COMPOSE

## 📌 MỤC TIÊU
Giai đoạn này chúng ta chuyển từ "thủ công" sang "tự động hóa". Docker Compose giúp bạn định nghĩa toàn bộ hạ tầng (nhiều container, mạng, volume) chỉ trong 1 file văn bản.

---

## 1. KIỂM TRA DOCKER COMPOSE

Docker Compose hiện nay đã được tích hợp sẵn vào Docker CLI (Version 2).

### Kiểm tra version
```bash
docker compose version
# Output: Docker Compose version v2.x.x
```
*Lưu ý: Lệnh là `docker compose` (có dấu cách, bản V2) thay vì `docker-compose` (có gạch nối, bản V1 cũ). Tuy nhiên cả 2 thường đều chạy được.*

Nếu bạn không thấy lệnh này:
- Hãy update Docker Desktop lên bản mới nhất.
- Hoặc cài plugin `docker-compose-plugin` (trên Linux).

---

## 2. CHUẨN BỊ MÔI TRƯỜNG
Hãy chắc chắn:
1. Bạn đã xóa các container chạy thủ công ở bài trước để tránh xung đột port hoặc tên:
   ```bash
   docker rm -f go-app python-app
   ```
2. Thư mục `data/` vẫn còn đó (để test việc Compose tái sử dụng volume cũ).

Sẵn sàng? Hãy tạo file `docker-compose.yaml` ở bài tiếp theo.
