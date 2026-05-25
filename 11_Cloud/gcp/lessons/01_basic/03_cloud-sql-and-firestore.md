# 🗄️ GCP Cloud SQL + Firestore

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** Bài [02_cloud-storage-and-iam](02_cloud-storage-and-iam.md) ✅, cơ bản SQL + NoSQL

> 🎯 *Bài 03. Cloud SQL = managed Postgres/MySQL, analog AWS RDS. Firestore = managed NoSQL document, analog AWS DynamoDB (document mode). Bài này dạy: instance type, HA + read replica, Cloud SQL Auth Proxy, IAM DB auth, backup/PITR; Firestore data model document, security rule, real-time listener, native vs Datastore mode; quyết định khi nào dùng cái nào.*

## 🎯 Sau bài này bạn sẽ

- [ ] Tạo **Cloud SQL Postgres** với HA Multi-zone + read replica
- [ ] Connect Cloud SQL từ GCE/Cloud Run qua **Cloud SQL Auth Proxy** (không public IP)
- [ ] Setup **IAM database authentication** (không cần password)
- [ ] Backup auto + **Point-in-Time Recovery** (PITR)
- [ ] Design **Firestore data model** đúng (subcollection vs flat)
- [ ] Viết **Security Rules** Firestore an toàn
- [ ] Dùng **real-time listener** Firestore cho live update
- [ ] Phân biệt Firestore **Native mode** vs **Datastore mode**
- [ ] Quyết định **Cloud SQL vs Firestore vs Spanner vs Bigtable** per workload

---

## Tình huống — Acme Shop chọn DB

Sếp:

> *"Acme Shop cần: user/order/product table (SQL, ACID), giỏ hàng + session (key-value, fast read/write), chat real-time (document + listener). Bạn design DB stack."*

3 nhu cầu, 3 DB:
- **Users/orders/products** → Cloud SQL Postgres (relational, ACID, complex query).
- **Cart/session** → Firestore (document, fast access by ID).
- **Chat realtime** → Firestore (real-time listener built-in).

Bài này dạy chọn + dùng đúng.

---

## 1️⃣ Cloud SQL — Managed Postgres/MySQL

🪞 **Ẩn dụ**: *Cloud SQL như **chung cư dịch vụ** — Google chăm sóc hạ tầng (backup, patch, HA), bạn chỉ cần "ở" (chạy query). Postgres engine vẫn 100% Postgres OSS — không lock-in syntax. So với DynamoDB-like NoSQL: SQL có "luật nhà" (schema, foreign key) — chặt nhưng predictable.*

### Engines

| Engine | Use case |
|---|---|
| **PostgreSQL** | Default 2026 — feature rich, JSON, full-text search |
| **MySQL** | Legacy ecosystem |
| **SQL Server** | Windows/.NET stack |

### Instance types

| Tier | CPU/RAM | Khi dùng |
|---|---|---|
| `db-f1-micro` | 1/0.6 GB | Dev/test |
| `db-custom-1-3840` | 1/3.75 GB | Small prod |
| `db-custom-2-7680` | 2/7.5 GB | Mid prod |
| `db-custom-8-30720` | 8/30 GB | Large prod |
| `db-perf-optimized-N-*` | New 2024+, NVMe local | High IOPS OLTP |

### Tạo instance HA

```bash
gcloud sql instances create acmeshop-db \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-7680 \
    --region=asia-southeast1 \
    --availability-type=REGIONAL \
    --storage-type=SSD \
    --storage-size=100 \
    --storage-auto-increase \
    --backup \
    --backup-start-time=03:00 \
    --enable-point-in-time-recovery \
    --retained-backups-count=30
```

- `--availability-type=REGIONAL` = HA Multi-zone primary + standby (auto failover 60-120s).
- `--enable-point-in-time-recovery` = PITR, restore tới giây trong 7 ngày.

### Read replica

```bash
gcloud sql instances create acmeshop-db-replica \
    --master-instance-name=acmeshop-db \
    --tier=db-custom-2-7680 \
    --region=asia-southeast1
```

→ Read-only replica, dùng cho analytics + report query.

### Connection — Cloud SQL Auth Proxy

🪞 **Ẩn dụ**: *Auth Proxy như **xe đưa rước có tài xế tin cậy** — bạn không cần biết đường, không cần lo ID — Proxy verify IAM của bạn và tunnel an toàn vào DB.*

```bash
# Cài proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.10.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Chạy proxy local
./cloud-sql-proxy acmeshop-prod:asia-southeast1:acmeshop-db --port=5432 &

# Connect như local
psql "host=127.0.0.1 port=5432 user=postgres dbname=postgres"
```

→ **Không cần public IP** trên Cloud SQL; auth qua IAM; encrypt TLS.

### IAM database authentication

```bash
# Bật IAM auth
gcloud sql instances patch acmeshop-db --database-flags=cloudsql.iam_authentication=on

# Tạo user gắn với IAM
gcloud sql users create thien.le@acmeshop.vn \
    --instance=acmeshop-db \
    --type=cloud_iam_user
```

→ User login bằng Google identity, không cần password. Audit log đầy đủ.

### Backup + PITR

- **Automated backup**: daily, retain 7-365 ngày.
- **PITR**: bật → có thể restore tới **mọi giây** trong 7 ngày qua (binlog/WAL based).
- **Export to GCS**: dump SQL → bucket cho archive dài hạn.

```bash
# Manual backup
gcloud sql backups create --instance=acmeshop-db

# PITR restore
gcloud sql instances clone acmeshop-db acmeshop-db-restore \
    --point-in-time='2026-05-23T14:30:00.000Z'

# Export to GCS
gcloud sql export sql acmeshop-db gs://acmeshop-backups/sql/dump-$(date +%Y%m%d).sql \
    --database=app
```

---

## 2️⃣ Firestore — Managed NoSQL document

🪞 **Ẩn dụ**: *Firestore như **tủ hồ sơ** — mỗi document là 1 hồ sơ JSON; collection là ngăn tủ. Truy cập 1 hồ sơ cực nhanh nếu biết ID; tìm theo điều kiện phức tạp thì cần Index (như "mục lục" của tủ).*

### Data model

- **Collection** = thư mục chứa documents (e.g., `users`, `orders`).
- **Document** = JSON object có ID unique trong collection.
- **Subcollection** = collection nằm trong document (`users/<uid>/cart`).

```
firestore
└── users (collection)
    ├── user_001 (document)
    │   ├── name: "Mr.Rom"
    │   ├── email: "thien.le@acmeshop.vn"
    │   └── cart (subcollection)
    │       ├── item_001 (document)
    │       └── item_002 (document)
    └── user_002 (document)
```

### Native vs Datastore mode

| Mode | Khi chọn |
|---|---|
| **Native** (2026 default) | Real-time listener, mobile/web SDK, strong consistency, transactions |
| **Datastore** | Backward-compat với app cũ App Engine; throughput cao hơn |

→ **Project mới luôn Native mode**. Datastore mode deprecated path.

### Quota & limit

| Item | Limit |
|---|---|
| Document size | 1 MB |
| Write rate per doc | 1 write/giây sustained |
| Read/write/delete | 50k read / 20k write / 20k delete free tier/ngày |

### CRUD ví dụ (Python)

```python
from google.cloud import firestore

db = firestore.Client()

# Create
db.collection("users").document("user_001").set({
    "name": "Mr.Rom",
    "email": "thien.le@acmeshop.vn",
    "created_at": firestore.SERVER_TIMESTAMP,
})

# Read
doc = db.collection("users").document("user_001").get()
print(doc.to_dict())

# Update
db.collection("users").document("user_001").update({
    "last_login": firestore.SERVER_TIMESTAMP,
})

# Query
results = db.collection("users").where("email", ">=", "thien").limit(10).stream()

# Delete
db.collection("users").document("user_001").delete()
```

### Real-time listener

```python
def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        print(f"{change.type.name}: {change.document.id}")

db.collection("chat/room1/messages").on_snapshot(on_snapshot)
# → mỗi message mới trigger callback
```

→ Frontend (React, Flutter) dùng SDK tương tự — push update real-time.

### Composite Index

```bash
# Tạo index cho query multi-field
gcloud firestore indexes composite create \
    --collection-group=orders \
    --field-config=field-path=status,order=ascending \
    --field-config=field-path=created_at,order=descending
```

→ Đơn-field index auto-create; **composite cần khai báo**.

---

## 3️⃣ Firestore Security Rules

🪞 **Ẩn dụ**: *Security Rules như **bảo vệ ở quầy lễ tân** — kiểm tra: ai (auth), muốn làm gì (read/write/list), với hồ sơ nào (path), trong trường hợp nào (custom condition).*

### Rules ví dụ

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // User chỉ đọc/sửa hồ sơ chính mình
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }

    // Order: user đọc của mình; admin đọc tất
    match /orders/{orderId} {
      allow read: if request.auth.uid == resource.data.user_id
                  || request.auth.token.admin == true;
      allow create: if request.auth != null
                    && request.resource.data.user_id == request.auth.uid;
      allow update, delete: if request.auth.token.admin == true;
    }

    // Public products
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth.token.admin == true;
    }
  }
}
```

### Deploy rules

```bash
firebase deploy --only firestore:rules
```

### Test rules

```bash
# Firestore emulator + unit test
firebase emulators:start --only firestore
# Test trong code với @firebase/rules-unit-testing
```

---

## 4️⃣ Quyết định DB nào

🪞 **Ẩn dụ**: *Chọn DB như **chọn phương tiện đi lại** — Cloud SQL như **ô tô** (đa năng, biết đường rành); Firestore như **xe đạp điện** (linh hoạt, nhanh cho đoạn ngắn); Spanner như **máy bay** (mạnh, đắt, đa châu lục); Bigtable như **tàu hàng** (chở khối lượng khổng lồ, không cần SQL).*

### Decision matrix

| Workload | Recommend | Vì sao |
|---|---|---|
| Relational, ACID, complex JOIN | **Cloud SQL Postgres** | Engine standard, ecosystem rộng |
| Document storage, mobile/web app | **Firestore Native** | Real-time listener, SDK đầy đủ |
| Global SQL multi-region strong consistency | **Cloud Spanner** | Globally distributed, hiếm cần |
| Wide-column high throughput (IoT, telemetry) | **Bigtable** | Petabyte-scale, < 10ms latency |
| Session/cache | **Memorystore (Redis)** | In-memory |
| Analytics, OLAP | **BigQuery** | Serverless data warehouse |
| Time-series (metric, log) | **Bigtable** hoặc **BigQuery** | High write throughput |

### So sánh Cloud SQL vs Firestore

| Khía cạnh | Cloud SQL | Firestore |
|---|---|---|
| Schema | Strict (CREATE TABLE) | Schemaless (JSON) |
| Transactions | Multi-row ACID | Limited (10 docs in tx) |
| Query | SQL full power (JOIN, GROUP BY, window) | Limited (no JOIN, no full-text) |
| Real-time | Polling/CDC | Built-in listener |
| Scalability | Vertical (instance size) | Horizontal auto |
| Latency | 5-20ms typical | 50-200ms (network + serverless) |
| Cost | Instance flat | Pay per op (read/write/delete) |

---

## 🛠️ Hands-on — Acme Shop DB stack

### Mục tiêu

Setup Cloud SQL Postgres cho user/order + Firestore cho cart/session.

### Bước 1 — Cloud SQL Postgres

```bash
# Tạo instance
gcloud sql instances create acmeshop-db \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-7680 \
    --region=asia-southeast1 \
    --availability-type=REGIONAL \
    --backup --backup-start-time=03:00 \
    --enable-point-in-time-recovery

# Tạo DB + user
gcloud sql databases create app --instance=acmeshop-db
gcloud sql users create app_user --instance=acmeshop-db --password=secure-pw

# IAM auth user
gcloud sql instances patch acmeshop-db --database-flags=cloudsql.iam_authentication=on
gcloud sql users create thien.le@acmeshop.vn \
    --instance=acmeshop-db --type=cloud_iam_user

# Connect qua proxy
./cloud-sql-proxy acmeshop-prod:asia-southeast1:acmeshop-db --port=5432 &
psql "host=127.0.0.1 port=5432 user=app_user dbname=app"
```

### Bước 2 — Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_cents BIGINT NOT NULL,
    status VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_orders_user ON orders(user_id);
```

### Bước 3 — Firestore Native

```bash
# Enable Firestore Native (mode chỉ chọn 1 lần)
gcloud firestore databases create --location=asia-southeast1
```

```python
# Backend ghi cart
db.collection("carts").document(user_id).set({
    "items": [{"product_id": "p1", "qty": 2}],
    "updated_at": firestore.SERVER_TIMESTAMP,
})
```

### Bước 4 — Security Rules

```javascript
match /carts/{userId} {
  allow read, write: if request.auth.uid == userId;
}
```

### Bước 5 — Verify

```bash
# Cloud SQL: insert + query
psql -h 127.0.0.1 -U app_user -d app -c "INSERT INTO users (email, name) VALUES ('test@x.com', 'Test')"
psql -h 127.0.0.1 -U app_user -d app -c "SELECT * FROM users"

# Firestore: backend ghi, frontend listen
firebase emulators:start --only firestore  # test rules
```

---

## ⚠️ Pitfalls

### 1. Cloud SQL public IP

**Bẫy**: Default Cloud SQL public IP → ai cũng connect được (nếu biết user/pw).

**Fix**: Disable public IP, dùng **Cloud SQL Auth Proxy** + private IP.

### 2. Không bật PITR

**Bẫy**: Backup daily → mất 24h data nếu accident.

**Fix**: `--enable-point-in-time-recovery` — restore tới giây.

### 3. Single-zone instance cho production

**Bẫy**: `--availability-type=ZONAL` → zone down = DB down.

**Fix**: Production luôn `REGIONAL` (HA Multi-zone).

### 4. Firestore "hot document"

**Bẫy**: Counter ghi 1 document → 1 write/giây sustained limit → throttle.

**Fix**: **Distributed counter** pattern — split thành N shards.

### 5. Firestore Security Rules quá lỏng

**Bẫy**: `allow read, write: if true` để dev → quên thay → public DB.

**Fix**: Default deny + chỉ allow khi auth + path đúng.

### 6. Composite index quên tạo

**Bẫy**: Query `where("status", "==", "active").orderBy("created_at")` → fail "needs composite index".

**Fix**: Khai báo composite index trong `firestore.indexes.json` + deploy.

### 7. Firestore mode lock

**Bẫy**: Tạo project bằng Datastore mode → muốn dùng Native không được (mode immutable per project).

**Fix**: Project mới luôn Native; nếu nhầm, tạo project mới.

### 8. Backup không test restore

**Bẫy**: Backup chạy đều nhưng chưa bao giờ test restore → khi cần thật → backup corrupted.

**Fix**: Test restore quarterly (DR drill).

---

## 🎯 Self-check

- [ ] Tạo Cloud SQL HA + read replica + PITR enable?
- [ ] Connect qua Cloud SQL Auth Proxy không cần public IP?
- [ ] IAM database authentication setup cho user?
- [ ] Design Firestore subcollection cho user/cart?
- [ ] Viết Security Rules ngăn user đọc cart của user khác?
- [ ] Real-time listener trong Python cho collection `chat/room1/messages`?
- [ ] Quyết định Cloud SQL vs Firestore vs Spanner vs Bigtable cho 5 workload khác nhau?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Cloud SQL** | Managed Postgres/MySQL/SQL Server |
| **HA (Regional)** | Multi-zone primary + standby, auto failover |
| **Read replica** | Read-only DB sync từ primary |
| **PITR** | Point-in-Time Recovery — restore tới giây bất kỳ |
| **Cloud SQL Auth Proxy** | Local proxy connect Cloud SQL qua IAM |
| **IAM Database Authentication** | Auth DB bằng Google identity, không password |
| **Firestore** | Managed NoSQL document DB |
| **Native mode** | Default 2026 — real-time listener, SDK đầy đủ |
| **Datastore mode** | Legacy compat với App Engine |
| **Collection** | Container of documents |
| **Document** | JSON object + ID unique trong collection |
| **Subcollection** | Collection trong document |
| **Composite Index** | Index multi-field, phải khai báo |
| **Security Rules** | Logic auth/authz trên Firestore (Firebase syntax) |
| **Distributed counter** | Pattern split counter tránh hot document |
| **Spanner** | Globally distributed SQL DB |
| **Bigtable** | Wide-column NoSQL, petabyte-scale |
| **Memorystore** | Managed Redis/Memcached |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [02_cloud-storage-and-iam](02_cloud-storage-and-iam.md)
- → Tiếp: [04_cloud-functions-cloud-run-and-api-gateway](04_cloud-functions-cloud-run-and-api-gateway.md) *(sắp viết)*
- ↑ Cluster GCP: [GCP README](../../README.md)

### Cross-reference
- ☁️ [AWS RDS + DynamoDB](../../../aws/lessons/01_basic/03_rds-and-dynamodb.md) — analog
- 🗄️ [PostgreSQL basic](../../../../05_Database/sql/postgresql/) — engine details

### Tài nguyên ngoài (2026)
- 📖 [Cloud SQL docs](https://cloud.google.com/sql/docs)
- 📖 [Cloud SQL Auth Proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy)
- 📖 [Firestore docs](https://cloud.google.com/firestore/docs)
- 📖 [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- 📖 [Spanner docs](https://cloud.google.com/spanner/docs)
- 📖 [Bigtable docs](https://cloud.google.com/bigtable/docs)
- 📖 [Distributed counter pattern](https://firebase.google.com/docs/firestore/solutions/counters)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 03 GCP basic. Cloud SQL Postgres HA + read replica + PITR + Auth Proxy + IAM DB auth + Firestore Native data model + Security Rules + real-time listener + composite index + decision matrix 7 DB GCP + hands-on Acme Shop stack + 8 pitfalls.
