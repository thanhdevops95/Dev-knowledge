# 🧠 Giao thoa Cấu trúc Dữ liệu & System Design

> `[ADVANCED]` — Thuật toán phía sau các Service khổng lồ

---

## Mở đầu: DSA không chỉ để phỏng vấn

Khi bạn thoát khỏi LeetCode và bước vào thiết kế hệ thống có 100 triệu User (Twitter, Tinder, DynamoDB), những Array, Hash Map hay Binary Tree cơ bản không còn đủ dùng nữa. Bạn cần những **Cấu trúc Dữ liệu chuyên biệt cho Distributed Systems**. 

---

## 1. Bloom Filter (Lọc Bloom) 

**Bài toán:** Bạn có 1 tỷ URL độc hại. Khi user nhập 1 URL, làm sao để check xem URL này có nằm trong danh sách không TỐC ĐỘ NHẤT có thể và tốn RẤT ÍT RAM? (Google Chrome Safe Browsing). Nếu dùng Hash Map, 1 tỷ URL có thể tốn hàng chục GB RAM.

**Giải pháp: Bloom Filter**
Cho một mảng N bit bằng 0. Khi nạp 1 chuỗi vào, ta dùng K hàm Băm (Hash functions) để băm chuỗi đó ra K vị trí. Set các vị trí đó bằng 1.

Đọc: Băm chuỗi cần tìm bằng K hàm tương tự. Nếu check K vị trí đó có bất kỳ vị trí nào bằng 0 -> **CHẮC CHẮN 100% KHÔNG TỒN TẠI**.
Nếu tất cả bằng 1 -> **CÓ THỂ TỒN TẠI** (Xác suất nhỏ nảy sinh dương tính giả - False Positive).

```python
# Giả lập Mảng 10 bits và 2 Hàm Hash
# H1("abc") -> 2. H2("abc") -> 5
# Mảng: [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]

# Check "xyz". Giả sử H1("xyz") -> 2. H2("xyz") -> 7.
# Bit 7 là 0 -> Chắc chắn "xyz" chưa bao giờ được thêm vào.
```

**Ứng dụng thực tế:**
- Medium / Quora: Lọc bài viết "Người này đã đọc bài này chưa?" (Tránh gợi ý lại).
- Database: Tránh Cache Penetration (Tấn công chọc thủng Cache bằng các ID không bao giờ tồn tại). Bloom check nếu không tồn tại thì chặn đứng không gọi gọi xuống DB luôn.

---

## 2. Consistent Hashing (Băm Nhất Quán)

**Bài toán:** Bạn có 4 Server Cache (Redis). Hàm Load Balancer là `hash(user_id) % 4`. Đột nhiên Server số 3 chết. Load balancer chỉnh lại thành `hash(user_id) % 3`.
KẾT QUẢ: Mọi modulo bị thay đổi. Gần như 100% người dùng bị văng ra Cache Miss hất xuống DB. Lũ lụt làm sập DB (Cache Avalanche). 

**Giải pháp: Consistent Hashing (Vòng tròn Băm)**
Tạo ra một vòng tròn chứa từ 0 đến Số rất lớn (Vd: Hash Max). Băm 4 Server đặt nó ở 4 điểm trên vòng.
Khi User Request tới, Băm ID của User đưa lên vòng tròn. Gặp điểm nào thì **đi theo chiều kim đồng hồ** gặp Server nào gần nhất thì chui vào.

```
Khi Server số 3 CHẾT. Những dữ liệu thuộc về Server số 3 đi tiếp chiều kim đồng hồ nhét vào Server số 4.
Data ở Server 1, 2, 4 VẪN NGUYÊN VỊ TRÍ, KHÔNG BỊ Cache Miss!
```

**Nhược điểm:** Mất 1 Server thì gánh nặng dồn hết cho thằng kế tiếp. (Khắc phục bằng **Virtual Nodes** - 1 Server có nhiều bóng ma rải rác vòng tròn).

**Ứng dụng thực tế:**
- Amazon DynamoDB partitioning.
- Memcached / Redis Cluster.

---

## 3. QuadTree và Geohash (Hệ thống Định vị LBS)

**Bài toán:** Tìm tài xế Uber gần nhất hoặc tìm Bạn trên Tinder. `SELECT * FROM Drivers WHERE lat = X AND lng = Y`. Nếu có hàng triệu tài xế, query này chạy O(N) tìm kiếm phẳng là tự sát, kể cả có Index (Vì đây là bài toán 2 chiều).

**Giải pháp 1: Geohash**
Chia bản đồ thế giới thành các lưới vuông nhỏ dần.
VD: `9` -> Lưới Trái Đất lớn. `9q` -> Lưới Mỹ. `9q8` -> San Francisco. `9q8y` -> Nhà của bạn.
Hai người ở gần nhau sẽ có Prefix (tiền tố giống nhau). 
Truy vấn SQL chỉ cần: `SELECT * FROM Drivers WHERE geohash LIKE '9q8%'`. Biến bài toán 2D thành so sánh chuỗi 1D siêu nhanh có Index.

**Giải pháp 2: QuadTree**
Cấu trúc cây. 1 Node chia bản đồ làm 4 góc (Tây Bắc, Đông Bắc, Tây Nam, Đông Nam).
Nếu ở 1 khu vực (như NY) có QUÁ NHIỀU tài xế, Node đó tiếp tục đẻ ra 4 Node con. (Lưới động - nơi đông người ô sẽ nhỏ lại).
Tốc độ tìm kiếm: O(log N).

---

## 4. LSM-Tree & B-Tree (Trái tim của Database)

Tại sao lại có MySQL và Cassandra? Khác biệt nằm ở Trái Tim lưu trữ của chúng.

### 4.1 B-Tree / B+ Tree (Read Heavy - MySQL, PostgreSQL)
Cây nhiều nhánh (Balanced Tree). Dữ liệu nằm phẳng ở lá (Leaf Nodes).
- Điểm mạnh: Tìm đọc rất nhanh (O(log N)).
- Điểm yếu: Nhét dữ liệu mới vào (Write) ở khoảng giữa làm cây phải chạy thuật toán Bẻ Nhánh (Rebalance / Page Split) cực tốn chi phí Disk I/O quay đĩa.

### 4.2 LSM-Tree (Log-Structured Merge-Tree) (Write Heavy - Cassandra, RocksDB)
- Mọi thao tác Ghi (Write) đều chỉ NỐI VÀO ĐUÔI (Append-only log) trong RAM (MemTable). Nhanh như chớp! Khi RAM đầy mới đẩy xuống Ổ cứng (SSTable).
- Điểm mạnh: Ghi dồn dập (Chat systems, Sensor IoT) lên tới triệu requests/s mà vẫn chịu được vì không cần Rebalance nhọc nhằn.
- Điểm yếu: Tìm kiếm (Đọc) đôi khi phải chạy lệnh duyệt nhiều file SSTable (Read Amplification). Bù lại nó dùng... **Bloom Filter** để tìm nhanh xem chép ở file nào.

---

## 5. Merkle Tree & CRDTs 

### 5.1 Merkle Tree (Cây Băm - Blockchain & Git)
- Cây nhị phân ở đó các "Lá" là Hash của Data. Đi dần lên con là Hash của Gộp 2 Lá. Root cuối cùng chỉ là 1 Dải Mã Hash đại diện toàn cây.
**Bài Toán:** Tải file Torrent 10GB bị lỗi 1 bit ở đâu đó. Chả lẽ tải lại từ đầu?
**Giải pháp:** Chỉ cần lấy Root Hash đi so, sai rẽ trái phải tìm sẽ moi ra đúng block hư 1MB tải lại. Tốc độ Sync siêu thanh. (Dùng trong Blockchain, tải Git file).

### 5.2 CRDTs (Conflict-free Replicated Data Types)
**Bài Toán:** 10 người cùng gõ 1 file Google Docs. Anh A ở VN chèn số 1, cô B ở US chèn chữ "K" ở cùng 1 giây. Không dùng Lock Database (bởi Lock là chờ tới chết). Làm sao gom lại thành chuỗi đúng?
**Giải pháp:** Dùng CRDTs (Dữ liệu quy tụ phi xung đột). Mỗi ký tự được gắn 1 nhãn Fractional Index (Giống số thập phân). 
A gõ vào 1.5, B gõ vào 1.6. Ghép file lại mọi mạng phân tán không cần nói chuyện cũng auto ra đúng thứ tự chữ là A(1.5)B(1.6). Dùng ở Figma, Google Docs, Notion.

---

## Các lỗi thường gặp khi đi Phỏng vấn SD

```
❌ Hở chút Database quá tải thì lôi Kafka / Redis Cache ra đỡ.
✅ Nếu User Search FullText thì phải lôi ElasticSearch / Inverted Index. Lọc ID thì Bloom Filter. Phải nói rõ Tên Thuật Toán mới đậu mức Senior.

❌ Cho rằng Consistent Hashing chỉ dùng chia Backend Server.
✅ Nó áp dụng rộng rãi chia Database, Database Partition.
```

---

## Bài tập thực hành

- [ ] Lên mạng xem minh họa **Consistent Hashing** Visualization trên Youtube. 
- [ ] Code một Bloom Filter đơn giản bằng Python dùng 3 hàm Hash MD5, SHA-1 nhỏ nhỏ trên mảng Bit array.
- [ ] Tham khảo thuật toán CRDT (Yjs) thử xem làm sao Build 1 realtime Todo App phi máy chủ (Offline First).

---

## Tài nguyên thêm
- [Designing Data-Intensive Applications (Martin Kleppmann)](https://dataintensive.net/) - Kinh Thánh cuốn 1 của Software Engineer.
- [Geohash visualization](http://geohash.gofreerange.com/)
