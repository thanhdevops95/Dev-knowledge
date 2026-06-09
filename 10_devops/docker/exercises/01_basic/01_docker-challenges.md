# 🧪 Thử thách Docker thực chiến — Cấp độ cơ bản

> **Tác giả:** Mr.Rom  
> **Phiên bản:** v1.1.1  
> **Tạo lúc:** 26/05/2026  
> **Cập nhật:** 01/06/2026  
> **Level:** Basic  
> **Tags:** [MUST-KNOW]  
> **Yêu cầu trước:** Đã học hết cụm Docker basic ([bài 00](../../lessons/01_basic/00_what-is-docker.md) → [bài 03](../../lessons/01_basic/03_docker-compose.md)).

> 🎯 *Học mà không hành thì như cầm bản đồ ẩm thực mà chưa từng nếm món ăn. Bạn đã đi qua cài đặt Docker, bản chất container, viết Dockerfile, đến phối hợp đa dịch vụ bằng Compose. Giờ là lúc bước vào "phòng lab thực chiến" — bộ bài tập rèn kỹ năng qua các tình huống doanh nghiệp điển hình.*

---

## 🎯 Mục Tiêu Bộ Thử Thách

- [ ] Củng cố vững chắc lý thuyết cốt lõi về cấu trúc Layer, Caching, và sự khác biệt giữa các cơ chế kết nối.
- [ ] Tự tay thiết kế và tối ưu hóa Dockerfile đạt chuẩn an toàn thông tin và hiệu năng cao (Alpine + Non-root + Multi-stage).
- [ ] Thiết kế kiến trúc tệp `docker-compose.yml` đa dịch vụ hoàn chỉnh kết nối bền vững có kiểm tra sức khỏe (Healthcheck).
- [ ] Viết script tự động hóa (Bash Script) quản lý và dọn dẹp tài nguyên Docker để giải phóng không gian ổ cứng an toàn.

---

## Phần I: Trắc Nghiệm Tư Duy Cốt Lõi (Quiz)

Hãy suy ngẫm kỹ và trả lời các câu hỏi sau trước khi mở đáp án giải mã để đối chiếu tư duy.

### Câu hỏi 1: Sự thật đằng sau cơ chế cô lập của Container và Virtual Machine (VM)
Một lập trình viên kỳ cựu khẳng định: *"Container thực chất chỉ là một process (tiến trình) đặc biệt được chạy cô lập trên hệ điều hành máy host, chứ không hề có nhân kernel hệ điều hành riêng như máy ảo VM."* Khẳng định này là **ĐÚNG** hay **SAI**? Hãy giải thích bản chất.

<details>
<summary><b>💡 Xem đáp án và giải mã chi tiết</b></summary>

Khẳng định trên là hoàn toàn **ĐÚNG**.
- **Virtual Machine (VM):** Cần một tầng giả lập phần cứng (Hypervisor) để chạy một hệ điều hành khách (Guest OS) hoàn chỉnh có nhân kernel riêng. Điều này khiến VM cực kỳ nặng nề (hàng GB), khởi động chậm (vài phút) và tiêu tốn nhiều RAM/CPU cho các tiến trình chạy ngầm của Guest OS.
- **Docker Container:** Chia sẻ chung nhân hệ điều hành (Kernel) của máy host. Docker Daemon sử dụng hai tính năng cốt lõi của nhân Linux là **Namespaces** (để cô lập tài nguyên mạng, tiến trình, ổ đĩa) và **Cgroups** (để giới hạn lượng RAM, CPU tối đa container được dùng). Do đó, container thực chất chỉ là một tiến trình Linux thông thường được bao bọc trong một "bức tường ảo", giúp khởi động siêu nhanh (mili-giây) và cực kỳ tiết kiệm bộ nhớ.

</details>

---

### Câu hỏi 2: Hậu quả của việc đặt sai thứ tự lệnh trong Dockerfile
Nếu bạn đặt câu lệnh `COPY . .` (sao chép toàn bộ mã nguồn) nằm **trước** câu lệnh `RUN npm install` hoặc `RUN pip install`, điều gì sẽ xảy ra với hiệu năng đóng gói (build) của hệ thống khi bạn chỉ sửa đổi một dòng ghi chú comment trong file code?

<details>
<summary><b>💡 Xem đáp án và giải mã chi tiết</b></summary>

Khi bạn sửa đổi code, mã hash của thư mục nguồn thay đổi. Nếu đặt `COPY . .` lên trước:
1. Docker phát hiện layer `COPY . .` bị thay đổi dữ liệu đầu vào -> **Hủy bỏ cache (Invalidate cache) của layer này**.
2. Theo quy tắc của Docker, một khi một layer bị vỡ cache, toàn bộ các layer tiếp theo phía dưới nó bắt buộc phải rebuild lại từ đầu.
3. Lệnh cài đặt thư viện `RUN npm install` hay `RUN pip install` nằm phía dưới sẽ bị chạy lại hoàn toàn. Quá trình build sẽ mất từ 2-5 phút cực kỳ lãng phí.
- **Quy tắc sống còn:** Luôn luôn copy file khai báo thư viện lên trước (`COPY package*.json .` hoặc `COPY requirements.txt .`), chạy lệnh cài đặt thư viện trước để tạo một layer cache bền vững, sau cùng mới copy mã nguồn thường xuyên thay đổi xuống dưới!

</details>

---

### Câu hỏi 3: Sự phối hợp giữa `ENTRYPOINT` và `CMD` trong Dockerfile
Bạn thiết kế một công cụ quét lỗ hổng bảo mật dạng Command Line (CLI). Bạn muốn khi người dùng gõ lệnh `docker run security-scanner --level=high` thì container sẽ thực hiện chạy binary chính là `security-scanner` kèm tham số `--level=high`. Bạn nên cấu hình `ENTRYPOINT` và `CMD` trong Dockerfile như thế nào?

<details>
<summary><b>💡 Xem đáp án và giải mã chi tiết</b></summary>

Bạn nên sử dụng mô hình kết hợp (**Combo C**) cực kỳ tối ưu sau:
```dockerfile
# Giữ cố định công cụ chạy chính
ENTRYPOINT ["/usr/bin/security-scanner"]

# Đặt tham số mặc định (người dùng có thể dễ dàng ghi đè)
CMD ["--level=low"]
```
- Khi chạy thông thường: `docker run security-scanner` -> Thực thi: `/usr/bin/security-scanner --level=low`
- Khi người dùng muốn đổi mức quét: `docker run security-scanner --level=high` -> Tham số `--level=high` sẽ ghi đè hoàn toàn nội dung của `CMD` nhưng vẫn chạy qua công cụ chính của `ENTRYPOINT`, thực thi: `/usr/bin/security-scanner --level=high`.

</details>

---

### Câu hỏi 4: Bí mật của biến `ARG` và `ENV` liên quan đến bảo mật
Một đồng nghiệp cố tình dùng `ARG DATABASE_PASSWORD=secret_key` trong Dockerfile để truyền mật khẩu lúc build image. Phương pháp này có thực sự an toàn bảo mật không?

<details>
<summary><b>💡 Xem đáp án và giải mã chi tiết</b></summary>

Phương pháp này **CỰC KỲ NGUY HIỂM** và không hề bảo mật.
- Biến `ARG` chỉ tồn tại tạm thời trong quá trình build image và biến mất khi container chạy. Tuy nhiên, toàn bộ các giá trị truyền vào qua `ARG` đều được ghi lại vĩnh viễn trong lịch sử các lớp cấu hình của image.
- Bất kỳ ai có quyền truy cập vào image đều có thể dễ dàng đọc được mật khẩu này bằng lệnh:
  ```bash
  docker history --no-trunc <tên-image>
  ```
- **Cẩm nang bảo mật:** Tuyệt đối không bao giờ hardcode mật khẩu hay API key vào `ARG` hay `ENV` trong Dockerfile. Hãy sử dụng tệp `.env` loại trừ khỏi Git, hoặc sử dụng các công cụ quản lý bí mật chuyên nghiệp như Docker Secrets, HashiCorp Vault.

</details>

---

## Phần II: Các Bài Lab Thực Hành Thực Chiến

---

### 🥼 LAB 1: Tối Ưu Hóa Dockerfile Cho Ứng Dụng Node.js Chuẩn Doanh Nghiệp

#### 🚨 Đặt vấn đề:
Một ứng dụng Node.js Express của công ty đang được đóng gói bằng Dockerfile thô sơ dưới đây. Image đầu ra nặng tới **950 MB**, chạy bằng tài khoản quản trị `root` cực kỳ nguy hiểm, và mất tới 3 phút để build lại mỗi khi sửa code.

```dockerfile
# ❌ DOCKERFILE THÔ SƠ - CHƯA TỐI ƯU
FROM node:20

COPY . /app
WORKDIR /app

RUN npm install

EXPOSE 3000
CMD ["node", "server.js"]
```

#### 🎯 Yêu cầu thử thách:
Bạn hãy viết lại một tệp `Dockerfile` hoàn chỉnh áp dụng các tiêu chuẩn Premium sau:
1. Sử dụng Base Image bản rút gọn siêu nhẹ `node:20-alpine` để tối ưu dung lượng đĩa.
2. Tái sắp xếp thứ tự các câu lệnh để bảo toàn Layer Cache tối đa (sửa code build lại dưới 2 giây).
3. Đảm bảo loại bỏ hoàn toàn rác bộ nhớ đệm tạm thời của `npm` khi cài đặt.
4. Chuyển quyền thực thi ứng dụng sang tài khoản người dùng bảo mật có sẵn trong image là `node` (Non-root user).
5. Áp dụng kỹ thuật **Multi-stage Build** để tách biệt giai đoạn cài đặt thư viện công cụ (Build stage) và giai đoạn chạy thật (Production runtime stage).

---

#### 💡 Hướng dẫn tư duy:
- **Stage 1 (Builder):** Sử dụng `node:20-alpine` để copy file cấu hình `package*.json` lên, chạy `npm ci` để cài đặt sạch sẽ toàn bộ thư viện dependencies.
- **Stage 2 (Runtime):** Khởi tạo một môi trường `node:20-alpine` hoàn toàn mới và sạch sẽ. Chỉ sao chép thư mục `node_modules` đã cài ở Stage 1 và file code chính `server.js` sang. Đảm bảo đổi quyền sở hữu thư mục sang user `node` bằng cờ `--chown=node:node`.

---

#### 🏆 Lời giải mẫu (Lab 1)

```dockerfile
# =========================================================
# GIAI ĐOẠN 1: Builder - Cài đặt thư viện dependencies đầy đủ
# =========================================================
FROM node:20-alpine AS builder

# Thiết lập thư mục build tạm thời
WORKDIR /build

# Sao chép các tệp khai báo thư viện lên trước để tận dụng cache
COPY package*.json ./

# Cài đặt sạch toàn bộ thư viện dependencies (bao gồm cả devDependencies phục vụ build nếu có)
RUN npm ci

# Sao chép toàn bộ mã nguồn để chuẩn bị đóng gói
COPY . .

# =========================================================
# GIAI ĐOẠN 2: Runtime - Môi trường chạy thật siêu nhẹ và bảo mật
# =========================================================
FROM node:20-alpine AS runner

# Đặt thư mục chạy ứng dụng chính thức
WORKDIR /usr/src/app

# Sao chép các tệp cấu hình cần thiết từ builder sang
COPY --from=builder /build/package*.json ./
# Chỉ sao chép thư mục node_modules đã cài đặt tối ưu sang
COPY --from=builder /build/node_modules ./node_modules
# Sao chép mã nguồn chạy thực tế
COPY --from=builder /build/server.js ./

# Thiết lập quyền sở hữu thư mục cho người dùng bảo mật 'node' có sẵn trong Alpine
RUN chown -R node:node /usr/src/app

# Chuyển quyền chạy hệ thống sang tài khoản bảo mật non-root
USER node

# Khai báo cổng ứng dụng sử dụng
EXPOSE 3000

# Biến môi trường mặc định chạy thực tế
ENV NODE_ENV=production

# Khởi chạy server sử dụng định dạng Exec Form an toàn
CMD ["node", "server.js"]
```

> [!TIP]
> **Thành quả đột phá:** Image đầu ra sau khi áp dụng Multi-stage build và Alpine chỉ còn vỏn vẹn **~110 MB** (giảm gần 9 lần so với nguyên bản), đồng thời tuyệt đối an toàn vì không chạy bằng quyền root!

---

### 🥼 LAB 2: Thiết Kế Kiến Trúc Compose Hệ Thống Live Chat Đa Container

#### 🚨 Đặt vấn đề:
Công ty chuẩn bị chạy thử nghiệm một dịch vụ Live Chat thời gian thực. Hệ thống yêu cầu tích hợp 3 thành phần liên kết chặt chẽ:
1. Ứng dụng Web NodeJS (`chat-app`) tự build từ thư mục hiện tại.
2. Bộ lưu trữ cache tin nhắn nhanh sử dụng Redis (`chat-cache`).
3. Cơ sở dữ liệu chính lưu thông tin tài khoản và phòng chat sử dụng MongoDB (`chat-db`).

#### 🎯 Yêu cầu thử thách:
Bạn hãy thiết kế một tệp `docker-compose.yml` đạt chuẩn vận hành cao cấp đáp ứng các tiêu chí sau:
1. Đọc mật khẩu admin và cổng kết nối từ tệp cấu hình môi trường `.env`.
2. Toàn bộ cơ sở dữ liệu MongoDB và Redis bắt buộc phải được gắn Named Volume bền vững để bảo toàn dữ liệu khi khởi động lại.
3. Thiết lập cơ chế kiểm tra sức khỏe **Healthcheck** an toàn cho MongoDB: Yêu cầu container `chat-app` chỉ được phép khởi động khi dịch vụ MongoDB đã hoàn toàn sẵn sàng kết nối.

---

#### 🏆 Lời giải mẫu (Lab 2)

Trước tiên, tạo file cấu hình môi trường `.env` tại thư mục dự án:
```text
# .env - Tệp cấu hình bảo mật cục bộ
MONGO_ADMIN_USER=dbchatadmin
MONGO_ADMIN_PASS=supersecuritypassword2026
CHAT_SERVER_PORT=3000
```

Viết tệp `docker-compose.yml` hoàn chỉnh:
```yaml
# docker-compose.yml
services:
  # -------------------------------------------------------------
  # Dịch vụ 1: Ứng dụng chính Live Chat Node.js
  # -------------------------------------------------------------
  chat-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${CHAT_SERVER_PORT}:3000"     # Đọc cổng public từ tệp cấu hình .env
    environment:
      # Chuỗi kết nối bảo mật tới MongoDB sử dụng biến từ file .env
      MONGO_URI: mongodb://${MONGO_ADMIN_USER}:${MONGO_ADMIN_PASS}@chat-db:27017/chatdb?authSource=admin
      REDIS_HOST: chat-cache
      NODE_ENV: production
    # Cơ chế kiểm soát khởi động: Đợi cho tới khi MongoDB vượt qua Healthcheck thành công
    depends_on:
      chat-db:
        condition: service_healthy

  # -------------------------------------------------------------
  # Dịch vụ 2: Cơ sở dữ liệu chính MongoDB
  # -------------------------------------------------------------
  chat-db:
    image: mongo:7.0-jammy
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ADMIN_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ADMIN_PASS}
    volumes:
      - mongo-volume:/data/db         # Gắn named volume lưu trữ dữ liệu an toàn
    ports:
      - "27017:27017"                 # Chỉ mở cổng nếu cần truy cập từ bên ngoài dev
    # Thiết lập Healthcheck kiểm tra thực tế xem MongoDB đã sẵn sàng nhận query chưa
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 5s                    # Tần suất kiểm tra
      timeout: 3s                     # Thời gian chờ phản hồi tối đa
      retries: 5                      # Số lần thử lại tối đa trước khi báo lỗi

  # -------------------------------------------------------------
  # Dịch vụ 3: Lưu trữ dữ liệu đệm Redis Cache
  # -------------------------------------------------------------
  chat-cache:
    image: redis:7-alpine
    volumes:
      - redis-volume:/data            # Bảo toàn dữ liệu cache
    ports:
      - "6379:6379"

# Khai báo các Named Volume độc lập ở cấp độ dự án
volumes:
  mongo-volume:
  redis-volume:
```

---

### 🥼 LAB 3: Tự Động Hóa Quản Lý Tài Nguyên Bằng Script Dọn Dẹp Docker

#### 🚨 Đặt vấn đề:
Trong quá trình học tập và làm việc hàng ngày với Docker, mỗi lần bạn build image lỗi hoặc dừng container không đúng cách, hệ thống sẽ sinh ra hàng loạt rác thải công nghệ bao gồm: các container đã tắt (stopped containers), các image không có nhãn bị mồ côi (dangling/untagged images), và các volume không dùng đến (unused volumes). 

Những rác thải này có thể âm thầm chiếm dụng hàng chục GB dung lượng ổ đĩa SSD đắt đỏ trên máy Mac của bạn. Bạn quyết định viết một công cụ tự động hóa dọn dẹp an toàn.

#### 🎯 Yêu cầu thử thách:
Bạn hãy viết một đoạn Script Bash mang tên `docker-clean.sh` thực hiện các yêu cầu tự động sau:
1. Sử dụng cú pháp Zsh/Bash an toàn, bắt buộc bật cờ kiểm tra lỗi nghiêm ngặt (`set -euo pipefail`).
2. Tự động tính toán và hiển thị dung lượng đĩa còn trống của hệ điều hành **trước** khi tiến hành dọn dẹp.
3. Tiến hành dọn dẹp tự động theo thứ tự an toàn:
   - Xóa bỏ toàn bộ các container đã dừng hoạt động (`stopped containers`).
   - Xóa bỏ các mạng ảo Docker không sử dụng (`unused networks`).
   - Xóa bỏ các image mồ côi không có nhãn (`dangling images` - các image dạng `<none>`).
4. Tự động tính toán lại dung lượng đĩa còn trống **sau** khi dọn dẹp và in ra màn hình thông báo tổng lượng dung lượng (tính bằng MB/GB) đã giải phóng thành công cho hệ thống.
5. Thiết lập cơ chế an toàn: Bắt buộc hiển thị câu hỏi xác nhận đồng ý từ người dùng (`y/n`) trước khi thực hiện xóa. Nếu người dùng chạy kèm tham số `--force` (hoặc `-f`), bỏ qua câu hỏi xác nhận và thực thi ngay lập tức (tiêu chuẩn viết CLI script chuyên nghiệp).

---

#### 🏆 Lời giải mẫu (Lab 3)

Hãy tạo một tệp tin mang tên `docker-clean.sh` và viết nội dung script cực kỳ tường minh dưới đây:

```bash
#!/usr/bin/env bash

# ==============================================================================
# Tên công cụ: docker-clean.sh
# Script dọn dẹp tài nguyên Docker an toàn
# Vai trò: Tự động dọn dẹp rác tài nguyên Docker để giải phóng ổ cứng an toàn
# ==============================================================================

# Kích hoạt các cờ kiểm tra lỗi nghiêm ngặt trong Shell Script
set -euo pipefail

# Khai báo màu sắc hiển thị cho terminal sinh động
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (Bỏ màu)

# Biến cờ đánh dấu có bỏ qua xác nhận hay không
FORCE_MODE=false

# Phân tích tham số đầu vào của script
for arg in "$@"; do
    if [[ "$arg" == "--force" || "$arg" == "-f" ]]; then
        FORCE_MODE=true
    fi
done

echo -e "${BLUE}=== CÔNG CỤ DỌN DẸP TỰ ĐỘNG DOCKER ===${NC}\n"

# Hàm lấy dung lượng đĩa còn trống (đơn vị KB) trên MacOS
get_free_disk_space() {
    # Sử dụng lệnh df để quét ổ đĩa root và trả về số block trống
    df -k / | awk 'NR==2 {print $4}'
}

# Lấy dung lượng đĩa trước khi dọn dẹp
INITIAL_FREE=$(get_free_disk_space)
INITIAL_FREE_GB=$(echo "scale=2; $INITIAL_FREE / 1024 / 1024" | bc)
echo -e "Dung lượng ổ cứng trống ban đầu: ${YELLOW}${INITIAL_FREE_GB} GB${NC}"

# Kiểm tra cơ chế xác nhận của người dùng
if [ "$FORCE_MODE" = false ]; then
    echo -e "${YELLOW}CẢNH BÁO: Lệnh này sẽ xóa toàn bộ stopped containers, unused networks và dangling images!${NC}"
    read -p "Bạn có chắc chắn muốn tiếp tục thực hiện dọn dẹp không? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[yY](es)?$ ]]; then
        echo -e "${RED}Đã hủy bỏ quá trình dọn dẹp theo yêu cầu người dùng.${NC}"
        exit 0
    fi
fi

echo -e "\n${BLUE}Bắt đầu quá trình dọn dẹp an toàn...${NC}"

# 1. Dọn dẹp các container đã dừng hoạt động
echo -e "\n1. Đang dọn dẹp các stopped containers..."
docker container prune -f

# 2. Dọn dẹp các mạng ảo không sử dụng
echo -e "\n2. Đang dọn dẹp các unused networks..."
docker network prune -f

# 3. Dọn dẹp các dangling images (các lớp image mồ côi không nhãn)
echo -e "\n3. Đang dọn dẹp các dangling images..."
docker image prune -f

echo -e "\n${GREEN}Quá trình dọn dẹp hoàn tất thành công!${NC}"

# Lấy dung lượng đĩa sau khi dọn dẹp
FINAL_FREE=$(get_free_disk_space)
FINAL_FREE_GB=$(echo "scale=2; $FINAL_FREE / 1024 / 1024" | bc)

# Tính toán lượng ổ cứng đã được giải phóng
SAVED_KB=$((FINAL_FREE - INITIAL_FREE))

if [ "$SAVED_KB" -le 0 ]; then
    echo -e "\nHệ thống của bạn đã cực kỳ sạch sẽ! Không giải phóng thêm dung lượng nào."
    echo -e "Dung lượng ổ cứng trống hiện tại: ${GREEN}${FINAL_FREE_GB} GB${NC}"
else
    # Quy đổi dung lượng đã giải phóng sang Megabytes (MB)
    SAVED_MB=$(echo "scale=2; $SAVED_KB / 1024" | bc)
    echo -e "\nKết quả giải phóng ổ đĩa:"
    echo -e "- Dung lượng trống hiện tại: ${GREEN}${FINAL_FREE_GB} GB${NC}"
    echo -e "- Tổng dung lượng đã được cứu về: ${GREEN}${SAVED_MB} MB${NC} 🎉"
fi
```

Để khởi chạy script này trên máy Mac của bạn, hãy thực hiện phân quyền chạy cho file:

```bash
# Cấp quyền thực thi cho file script
chmod +x docker-clean.sh

# Chạy thử nghiệm công cụ ở chế độ thông thường (Có hỏi xác nhận)
./docker-clean.sh

# Hoặc chạy ở chế độ tự động ép buộc (Không hỏi xác nhận phục vụ tự động hóa cronjob)
./docker-clean.sh --force
```

Đoạn script chuẩn chỉ này chính là một người trợ thủ đắc lực giúp giữ cho ổ cứng máy tính phát triển của bạn luôn trong trạng thái thông thoáng và tối ưu nhất!

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (26/05/2026)** — Bản đầu tiên: 4 câu hỏi trắc nghiệm có đáp án ẩn + 3 bài Lab (Lab 1: multi-stage build Node.js; Lab 2: Docker Compose multi-service có Healthcheck; Lab 3: Bash script dọn dẹp tài nguyên Docker an toàn).
- **v1.1.0 (01/06/2026)** — Đổi metadata YAML sang khối block-quote tiêu chuẩn; bỏ các cụm cá nhân hoá; bỏ dấu hai chấm cuối tiêu đề lời giải.
- **v1.1.1 (01/06/2026)** — Sửa lỗi QA: sửa typo tiêu đề "Phân I" → "Phần I"; gỡ chuỗi "AUTHOR: MR.ROM" còn sót trong output script (banner echo); đánh số 3 tiêu đề "Lời giải mẫu" thành (Lab 1/2/3) để hết trùng heading (MD024). Đã verify lại Dockerfile (build + run non-root OK), compose YAML (safe_load OK), bash script (bash -n OK).
