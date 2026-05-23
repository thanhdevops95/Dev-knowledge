# 🏗️ System Design nâng cao — High Availability & Scalability

> `[ADVANCED]` — Thiết kế cho hàng triệu người dùng

---

## 1. Caching Strategies (Chiến lược Cache)

Mọi hệ thống lớn đều chết nếu database bị gọi trực tiếp liên tục.

### Cache-Aside (Phổ biến nhất)
App tự quản lý cache. Database và Cache không biết nhau.

```
1. App check Cache (Redis).
2. Nếu HIT: Trả về cho user ngay.
3. Nếu MISS: App SELECT từ DB → Ghi vào Cache → Trả về cho user.
```
✅ **Ưu điểm:** Dễ hiểu. Resilient (cache chết thì query từ DB).

### Write-Through
App ghi vào DB VÀ Cache cùng lúc dưới dạng 1 transaction.
✅ **Ưu điểm:** Data luôn đồng bộ 100% giữa Cache và DB. Đọc nhanh nhất.

### Write-Around
Cache chỉ dùng cho dữ liệu đọc nhiều. App ghi TRỰC TIẾP vào DB, bỏ qua Cache. Chỉ cập nhật Cache qua Cache-Aside khi có request đọc.
✅ **Ưu điểm:** Dành cho data ghi 1 lần rồi ít bao giờ đọc ngay (ví dụ: Log audit).

### Cache Eviction Policies
Khi Redis đầy thì xóa cái gì?
- **LRU (Least Recently Used):** Xóa item N LÂU CHƯA DÙNG nhất (Phổ biến nhất).
- **LFU (Least Frequently Used):** Xóa item ÍT ĐƯỢC DÙNG NHẤT.

---

## 2. Message Queue & Event Broker

Khi request quá nặng (Gửi 10 vạn email, resize 100 video), không thể bắt user chờ. Request API phải xong < 500ms.

```
User (Upload Video) ──► [API Server] ──► Trả về "Đang xử lý!" (200ms)
                             │
                            [Kafka/RabbitMQ] (Xếp hàng)
                             │
                        [Worker Server 1][Worker Server 2]...
```

### RabbitMQ (Message Broker)
- Mô hình **Smart Broker, Dumb Consumer**: Rabbit.
- Tracking chi tiết trạng thái tin nhắn (Nhận thành công không? Xóa khỏi hàng đợi).
- Dành cho **Task Queue**, Job Scheduling (giao hàng rẽ nhánh phức tạp).

### Kafka (Event Streaming)
- Mô hình **Dumb Broker, Smart Consumer**. Logs chỉ append nối đuôi.
- Lưu trữ mọi thứ ở dạng persistent log. Bạn có thể "tua lại" quá khứ.
- Siêu nhanh, hàng triệu tin / giây.
- Dành cho **Analytics, Event Sourcing, Activity Log**.

---

## 3. Database Sharding & Partitioning

Làm sao khi Database phình to lên 10TB? 1 server chạy không nổi nữa.

### Partitioning (Phân mảnh dọc/ngang)
Chia dữ liệu ra thành các bảng nhỏ hơn NẰM TRÊN CÙNG 1 MÁY.
- Ngang: Rows tháng 1 vào bảng `Orders_Jan`, Tháng 2 vào `Orders_Feb`.
- Dọc: Cột `user_Bio_LargeText` tách ra bảng phụ để bảng chính search cho lẹ.

### Sharding (Scaling Database ra N máy)
Chia Data ra NHIỀU SERVER VẬT LÝ khác nhau.

```
Database có 100 Triệu User. Shard Key = id_user
- Máy A: user_id 1 - 33 Triệu (US)
- Máy B: user_id 33T - 66 Triệu (EU)
- Máy C: user_id 66T - 100 Triệu (Asia)
```

**⚠️ Đánh đổi của Sharding:**
- Rất phức tạp để phân bổ Shard Key (Nếu shard theo IP VN, VN có đợt event thì máy A tèo, B C rảnh rỗi).
- Transaction xuyên máy gần như không thể (Multi-shard JOIN).
- Thêm node/giảm node (Resharding) là ác mộng.

---

## 4. Rate Limiting (Giới hạn truy cập)

Làm sao để bảo vệ server khỏi bots DDoS hoặc brute force?

### Các thuật toán:
1. **Token Bucket** (Xô Token - Xài nhiều nhất, ví dụ AWS, Stripe):
   Mỗi user có 1 xô đựng N Tokens. Cứ R giây thêm 1 token vào xô. Mỗi lần user gọi hàm thì trừ 1 token. Hết Token = HTTP 429 Too Many Requests.
2. **Leaky Bucket** (Xô rò rỉ): Request đổ vào xô, dưới đáy xô nhỏ giọt (xử lý) với tốc độ cố định. Đầy xô thì tràn (Xóa request mới luôn). Tránh Spike Request tốt.
3. **Fixed Window**: Tính số req từ 1:00 -> 1:01. Dọn dẹp ở 1:01. (Nhược điểm: Spike gấp đôi req ở giây 1:00:59 đến 1:01:01)

```javascript
// Rate Limit với Redis
await redis.incr("limit:user_id:123");
const calls = await redis.get("limit:user_id:123");
if (calls > 100) return res.status(429).send("Thử lại sau 1 phút");
// Set TTL 60 seconds
```

---

## 5. CAP Theorem & PACELC

**CAP Định Lý:** Không 1 hệ thống dữ liệu phân tán nào ĐẠT ĐƯỢC CÙNG LÚC 3 thứ:
- **Consistency** (Nhất quán): Đọc luôn ra bản ghi mới nhất.
- **Availability** (Sẵn sàng): Mọi user luôn nhận phản hồi (không chết).
- **Partition Tolerance** (Chịu chia cắt): Hệ thống chia rẽ vật lý vẫn hoạt động (Vì đứt cáp đại dương, mất router datacenter 1 lúc).

**Do PT là bắt buộc trong Cloud, ta chỉ có thể chọn CP hoặc AP.**

- **CP (Consistency):** Ngân hàng nạp tiền (Bank). Nếu không chắc 100% balance khớp nhau các server, khóa không cho đọc. Thà báo lỗi Hệ thống Bảo trì.
- **AP (Availability):** Mạng Xã Hội like bài (Facebook, Redis Cache). Mạng đứt, User khu vực Á Mỹ mất đồng bộ? Kệ nó, người bên Á thấy người bên Mỹ chưa có like mới cũng không chết người.

---

## Các lỗi thường gặp

```
❌ Sai: Sharding mọi thứ từ ngày ra mắt App
✅ Đúng: Replication → Indexing → Cache → Cuối cùng bế tắc lắm mới Sharding.

❌ Sai: Cache mọi data có thể
✅ Đúng: Chỉ cache "Read Heavy" & "Ít cập nhật". Cache data Realtime (chứng khoán) là tự sát (Thundering Herd pattern).

❌ Sai: Dùng Message Queue thì không bao giờ mất message.
✅ Đúng: Cần setup ACK (Acknowledgement). Nếu Kafka gặp lỗi không Ack, message phải đẩy vào Dead Letter Queue (DLQ).
```

---

## Bài tập thực hành

- [ ] Phân tích thiết kế của 1 Feed Twitter (News Feed) (Cách phân bổ Read/Write cho người nổi tiếng vs người thường).
- [ ] Soạn thảo sơ đồ hệ thống bán vé Concert 1,000,000 người vào tranh 1 phút (Scaling, Queues, Database Locks).

---

## Tài nguyên thêm

- [ByteByteGo (Alex Xu)](https://www.youtube.com/@ByteByteGo) — Minh họa trực quan Design Patterns
- [System Design Interview](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF) — Quyển sách gối đầu giường.
- Kiến trúc Uber, Netflix trên Tech Blogs.
