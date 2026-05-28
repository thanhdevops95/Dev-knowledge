# 🗃️ Managed Databases — Postgres / MySQL / Redis / MongoDB / Kafka

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** [02_spaces-object-storage-and-cdn](02_spaces-object-storage-and-cdn.md) ✅, hiểu SQL cơ bản, đã dùng Postgres/Redis

> 🎯 *Bài 03 đi sâu **Managed Databases** của DO. Bạn sẽ học: vì sao nên dùng managed thay self-host, 5 engine (Postgres / MySQL / Redis / MongoDB / Kafka), standby + read replica, connection pooling, automated backup, security baseline, hands-on deploy Postgres production cho Acme Shop.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **vì sao managed DB** > self-host Postgres trên Droplet
- [ ] Phân biệt **5 engine** DO managed (Postgres / MySQL / Redis / MongoDB / Kafka)
- [ ] Chọn đúng **tier** (Basic 1-node dev / Pro HA standby)
- [ ] Cài đặt **Standby node** (HA) và **Read replica** (scale read)
- [ ] Hiểu **PgBouncer connection pooling** built-in
- [ ] Setup **automated backup + PITR** (Point-in-Time Recovery)
- [ ] Bảo mật: **Trusted Sources**, VPC private, SSL bắt buộc, user RBAC
- [ ] Hands-on deploy **Postgres production** cho FastAPI app

---

## Tình huống — DB cho production

Internal tool đã có FastAPI ở Droplet, Spaces lưu file. Giờ tới Postgres:

> *Sếp: "DB là tim ứng dụng. Đừng tự cài Postgres trên Droplet — đêm hôm down ai sửa? Cần managed có: backup tự động, HA, monitor sẵn, scale lên dễ. Budget $30-100/tháng OK."*

DO Managed Postgres giải quyết:
- 1-click deploy, có HA standby option.
- Automated backup daily + 7-day retention.
- PITR (rollback đến giây bất kỳ trong 7 ngày).
- PgBouncer connection pooling sẵn.
- Connection qua VPC private (Droplet → DB không qua internet).
- Monitor + alert built-in.

Bài này dạy đủ deploy production-grade.

---

## 1️⃣ Vì sao Managed DB > Self-host trên Droplet

🪞 **Ẩn dụ**: *Self-host Postgres trên Droplet như **tự nuôi xe ô tô** — bạn vừa làm tài xế, vừa thợ sửa, vừa rửa xe, vừa thay nhớt. Managed DB như **thuê Grab Premium** — bạn chỉ cần đi, mọi thứ khác có người lo.*

### So sánh Self-host vs Managed

| Việc | Self-host Postgres trên Droplet | Managed Postgres DO |
|---|---|---|
| Cài đặt | `apt install postgresql-16`, config, tune | 1-click |
| Backup | Tự cron `pg_dump`, upload Spaces | Daily auto + 7-day retention |
| PITR | Tự setup WAL archive — phức tạp | Built-in |
| HA standby | Patroni / repmgr — khó | 1-click "Add Standby" |
| Read replica | Streaming replication tự setup | 1-click "Add Read-only Node" |
| Major version upgrade | Manual `pg_upgrade` — risky | 1-click maintenance window |
| Monitor | Tự cài Prometheus exporter | Built-in dashboard |
| Security patch | Tự `apt upgrade`, restart | DO tự apply trong maintenance window |
| Connection pooling | Tự cài PgBouncer | Built-in |
| Scale up RAM | Resize Droplet | 1-click resize |

### Khi nào self-host vẫn OK

- Học tập / dev local.
- Budget cực thấp (Droplet $4 < Managed $15).
- Workload trivial (< 100 user, không quan trọng).
- Cần Postgres extension không có trên managed (vd `pg_partman` cũ, `timescaledb` advanced).

### Khi nào BẮT BUỘC managed

- Production, business-critical.
- Compliance: cần audit log, encryption at rest, automated backup.
- Team nhỏ — không có DBA full-time.
- Cần HA (RTO < 1 phút).

---

## 2️⃣ 5 Engines DO managed

### Đặc điểm chung

| | Postgres | MySQL | Redis | MongoDB | Kafka |
|---|---|---|---|---|---|
| **Phiên bản 2026** | 14, 15, 16, 17 | 8.0, 8.4 | 7.x | 6.0, 7.0 | 3.7, 3.8 |
| **Standby HA** | ✅ | ✅ | ✅ | ✅ | ✅ (multi-broker) |
| **Read replica** | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Connection pool** | PgBouncer | (qua app pool) | (native) | (driver) | (consumer group) |
| **Backup auto** | ✅ daily | ✅ daily | ❌ persistence option | ✅ daily | ❌ (Kafka logs) |
| **PITR** | ✅ 7-day | ✅ 7-day | ❌ | ✅ 7-day | ❌ |
| **VPC private** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **SSL bắt buộc** | ✅ | ✅ | ✅ | ✅ | ✅ |

### Khi nào dùng engine nào

| Use case | Engine |
|---|---|
| OLTP relational (CRUD app) | Postgres (default) |
| Legacy MySQL app | MySQL |
| Cache, session, queue đơn giản | Redis |
| Document store (nested JSON heavy) | MongoDB |
| Event streaming, log pipeline | Kafka |
| Time-series, geo | Postgres + PostGIS |
| Full-text search | Postgres + `pg_trgm` (đủ cho 90% case), nặng → Elasticsearch self-host |

> 💡 **2026 best practice**: chọn **Postgres** mặc định. Nó cover được 90% case (relational, JSON, geo, full-text, vector qua pgvector). Chỉ thêm engine khác khi có lý do cụ thể.

---

## 3️⃣ Pricing — Tier matrix

### Postgres (tương tự MySQL/MongoDB)

| Tier | RAM | vCPU | Storage | Standby | Giá/tháng |
|---|---|---|---|---|---|
| **Basic 1GB (dev)** | 1 GB | 1 | 10 GB | ❌ | $15 |
| **Basic 2GB** | 2 GB | 1 | 25 GB | ❌ | $30 |
| **Basic 4GB** | 4 GB | 2 | 38 GB | ❌ | $60 |
| **Pro 4GB + 1 standby** | 4 GB | 2 | 50 GB | ✅ | $120 |
| **Pro 8GB + 1 standby** | 8 GB | 2 | 115 GB | ✅ | $240 |
| **Pro 32GB + 2 standby** | 32 GB | 8 | 580 GB | ✅✅ | $1370 |

### Add-ons

- **Read replica**: +$15-1000+ tùy size (mỗi replica 1 node riêng).
- **Storage extend**: $0.10/GB/tháng (giống Volume).

### Redis

| Tier | RAM | Giá/tháng |
|---|---|---|
| Basic 1GB | 1 GB | $15 |
| Basic 4GB | 4 GB | $60 |
| Pro 4GB HA | 4 GB | $120 |

---

## 4️⃣ Standby vs Read Replica — Khác nhau

### Standby (HA)

🪞 **Ẩn dụ**: *Standby như **phụ lái xe** — ngồi cùng cabin, luôn sẵn sàng cầm lái khi tài chính ngất. Khách không biết đổi tài.*

- 1 node "thầm lặng" replicate đồng bộ từ primary.
- **Auto-failover**: primary chết → standby promote thành primary trong < 1 phút.
- Connection string **không đổi** — DO redirect tự động.
- Standby **không cho query** (chỉ chờ failover).
- Cost: ~2x Basic tier.

### Read Replica

🪞 **Ẩn dụ**: *Read replica như **bản photocopy của tài liệu** — bạn xem được nhưng không sửa. Sửa phải về bản gốc.*

- Node phụ replicate **async** từ primary.
- **Read-only** — app gửi SELECT query đến đây để giảm tải primary.
- Connection string **riêng** (host khác).
- Lag thường < 1 giây.
- Tự đặt ở **region khác** được (cross-region replication).
- Cost: full price của 1 node thêm.

### Khi nào dùng gì

| Mục tiêu | Giải pháp |
|---|---|
| HA (uptime cao) | Pro tier với standby |
| Read-heavy workload | Add read replica |
| Cross-region disaster recovery | Read replica ở region khác |
| Analytics query nặng không ảnh hưởng prod | Read replica dedicated cho BI |

---

## 5️⃣ Connection pooling — PgBouncer built-in

### Vấn đề

Postgres mỗi connection ~10MB RAM. 200 web request → 200 connection → 2GB RAM Postgres chỉ để giữ connection.

→ Cần **connection pool**: app mở 200 "logical" connection, pool maintain 20 "physical" tới Postgres, multiplex.

### DO Postgres có PgBouncer built-in

```
Endpoint 1: postgres-1234.b.db.ondigitalocean.com:25060
            → connect trực tiếp Postgres (1 conn = 1 backend)

Endpoint 2: postgres-1234.b.db.ondigitalocean.com:25061
            → qua PgBouncer (pool, multiplex)
```

### 3 pool modes

| Mode | Mô tả | Khi dùng |
|---|---|---|
| **Session** | 1 client conn = 1 backend conn cho cả session | Tương đương no-pool, ít lợi |
| **Transaction** | 1 client conn → backend chỉ trong 1 transaction | Mặc định khuyến nghị |
| **Statement** | 1 client → 1 query, return về pool | Aggressive, không hỗ trợ prepared statement |

### Setup ở DO

```
UI: Database → Connection Pools → New Pool
- Name: "app-pool"
- Database: acmeshop
- User: doadmin
- Mode: Transaction
- Pool size: 20  (= ~20% max connection của tier)
```

App connect:
```python
DATABASE_URL = "postgresql://doadmin:PASSWORD@postgres-1234.b.db.ondigitalocean.com:25061/app-pool?sslmode=require"
```

### Best practices

| BP | Lý do |
|---|---|
| Mode = Transaction | Cân bằng performance + compatibility |
| Pool size = 20-30% max_connections | Tránh overflow |
| App tự pool nhỏ (5-10) + PgBouncer | 2 layers, layer DB-side là chính |
| Không dùng SESSION-level feature (LISTEN/NOTIFY, prepared statement session) qua pool transaction-mode | Sẽ fail |

---

## 6️⃣ Backup + PITR

### Automated backup

DO Postgres tự backup **daily**, retention **7 days** (Basic), **35 days** (Pro upgrade).

```
UI: Database → Backups → List
- Daily snapshot
- WAL stream continuous → PITR
```

### Point-in-Time Recovery (PITR)

🪞 **Ẩn dụ**: *PITR như **tua time-machine** — bạn có thể về đúng giây 14:23:45 hôm thứ Ba, không phải chỉ về điểm snapshot cuối ngày.*

```
UI: Database → Backups → "Restore from backup"
- Select date/time: 2026-05-24 14:23:45 UTC
- New cluster name: acmeshop-restored
- Create
```

DO tạo cluster mới từ WAL replay → bạn switch app connection string sang cluster mới khi sẵn sàng. **Original cluster KHÔNG bị thay đổi** — safe.

### Manual snapshot (logical dump)

```bash
# Trên local máy hoặc Droplet trong cùng VPC
pg_dump --no-owner --no-acl \
    "postgresql://doadmin:PWD@postgres-1234.b.db.ondigitalocean.com:25060/acmeshop?sslmode=require" \
    > acmeshop-backup-$(date +%F).sql

# Upload lên Spaces backup
s3cmd put acmeshop-backup-*.sql s3://acmeshop-backups/postgres/

# Restore
psql "postgresql://..." < acmeshop-backup-2026-05-24.sql
```

### Backup strategy 3-2-1

1. **3** copies: primary + DO auto-backup + manual `pg_dump` Spaces.
2. **2** storage type: DB cluster + Object storage.
3. **1** off-site: Spaces ở region khác hoặc S3.

---

## 7️⃣ Security baseline

### A. Trusted Sources — restrict IP

Mặc định DB cluster expose ra internet (port 25060). Phải khoá:

```bash
# Add trusted source = chỉ Droplet ABC + IP văn phòng
doctl databases firewalls append CLUSTER_ID \
    --rule "droplet:DROPLET_ID" \
    --rule "ip_addr:1.2.3.4" \
    --rule "tag:env:prod"

# List
doctl databases firewalls list CLUSTER_ID
```

→ Sau đó, DB chỉ accept connection từ những source whitelist.

### B. VPC Private Network

DO tạo VPC mặc định mỗi region. Database + Droplet cùng VPC → connection qua **private IP**, không qua internet.

```
Connection string mặc định (public):
postgres-1234.b.db.ondigitalocean.com

Connection string private:
private-postgres-1234.b.db.ondigitalocean.com
```

→ App trên Droplet dùng `private-...` host:
- Không traffic ra internet.
- Bypass Trusted Sources (private network tự trust).
- Bandwidth không tính.

### C. SSL bắt buộc

DO Postgres **bắt buộc** TLS connection. Connection string phải có `?sslmode=require`:

```python
DATABASE_URL = "postgresql://...?sslmode=require"

# Strict (verify CA cert):
DATABASE_URL = "postgresql://...?sslmode=verify-full&sslrootcert=ca-certificate.crt"
```

Download CA cert:
```
UI: Database → Overview → "Download CA certificate"
```

### D. User RBAC

```bash
# Tạo user app-only (không superuser)
doctl databases user create CLUSTER_ID app-user
# Output password copy ngay

# Hoặc qua psql:
psql ... -c "CREATE USER app_user WITH PASSWORD 'xxxx';"
psql ... -c "GRANT CONNECT ON DATABASE acmeshop TO app_user;"
psql ... -c "GRANT USAGE ON SCHEMA public TO app_user;"
psql ... -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;"
```

→ App dùng `app_user`, không phải `doadmin` (superuser). Limit blast radius nếu compromise.

### E. Rotate password định kỳ

```bash
doctl databases user reset CLUSTER_ID app-user
# New password output
```

Cập nhật app secret (env var) sau.

---

## 🛠️ Hands-on — Deploy Postgres production

### Mục tiêu

Tạo Postgres Pro 4GB + standby cho Acme Shop FastAPI:
- HA với standby.
- VPC private connection từ Droplet.
- App user RBAC.
- PgBouncer pool.
- Backup auto + manual weekly to Spaces.

### Bước 1 — Tạo cluster

```bash
doctl databases create acmeshop-postgres \
    --engine pg \
    --version 17 \
    --size db-s-2vcpu-4gb \
    --num-nodes 2 \
    --region sgp1 \
    --private-network-uuid $(doctl vpcs list --format ID --no-header | head -1) \
    --wait

# 2 nodes = 1 primary + 1 standby
# Mất ~5-10 phút
```

### Bước 2 — Tạo database + user

```bash
CLUSTER_ID=$(doctl databases list --format ID,Name --no-header | grep acmeshop-postgres | awk '{print $1}')

# Tạo database
doctl databases db create $CLUSTER_ID acmeshop

# Tạo app user
doctl databases user create $CLUSTER_ID app_user
# Copy password
```

### Bước 3 — Trusted Sources

```bash
# Get Droplet ID của app server
DROP_ID=$(doctl compute droplet list acmeshop-web --format ID --no-header)

doctl databases firewalls append $CLUSTER_ID \
    --rule "droplet:$DROP_ID"

# Hoặc dùng tag
doctl databases firewalls append $CLUSTER_ID \
    --rule "tag:env:prod"
```

### Bước 4 — Tạo connection pool

```bash
doctl databases pool create $CLUSTER_ID \
    --name app-pool \
    --db acmeshop \
    --mode transaction \
    --size 20 \
    --user app_user
```

### Bước 5 — Config app connection

```python
# Trên Droplet, /opt/acmeshop/.env
DATABASE_URL=postgresql://app_user:PASSWORD@private-postgres-1234.b.db.ondigitalocean.com:25061/app-pool?sslmode=require
```

```python
# app.py — SQLAlchemy
from sqlalchemy import create_engine
import os

engine = create_engine(
    os.environ['DATABASE_URL'],
    pool_size=5,      # app-side small pool
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={'sslmode': 'require'},
)
```

### Bước 6 — Init schema

```bash
# SSH vào Droplet (đã ở VPC)
ssh deploy@acmeshop-web

# Connect psql
psql "$DATABASE_URL"

# Run migration
\i schema.sql

# Verify
\dt
SELECT count(*) FROM users;
\q
```

### Bước 7 — Test failover (Pro tier)

```bash
# Force failover (test only — production thì DO tự handle)
doctl databases failover $CLUSTER_ID --wait

# Connection string vẫn thế, primary đã swap
# App reconnect tự động (pool_pre_ping=True giúp)
```

### Bước 8 — Weekly backup to Spaces

```bash
# Cron weekly trên Droplet
sudo tee /etc/cron.weekly/postgres-backup <<'EOF'
#!/bin/bash
set -e
DATE=$(date +%F)
pg_dump --no-owner --no-acl \
    "postgresql://app_user:$DB_PWD@private-postgres-1234.b.db.ondigitalocean.com:25060/acmeshop?sslmode=require" \
    | gzip > /tmp/acmeshop-$DATE.sql.gz

s3cmd put /tmp/acmeshop-$DATE.sql.gz s3://acmeshop-backups/postgres/

rm /tmp/acmeshop-$DATE.sql.gz

# Send notification (optional)
curl -X POST https://hooks.slack.com/... \
    -d "{\"text\":\"Postgres backup $DATE OK\"}"
EOF
sudo chmod +x /etc/cron.weekly/postgres-backup
```

→ **Kết quả**: Postgres production HA, app secure, backup 3-2-1. Bill ~$120/tháng + Spaces.

---

## ⚠️ Pitfalls

### 1. Quên `?sslmode=require`

**Bẫy**: Connect không SSL → DO reject với "no pg_hba.conf entry".

**Fix**: Luôn `?sslmode=require` trong connection string. Production: `?sslmode=verify-full&sslrootcert=...`.

### 2. Dùng `doadmin` cho app

**Bẫy**: App connect bằng `doadmin` (superuser) → SQL injection thành disaster.

**Fix**: Tạo app user RBAC limited. `doadmin` chỉ cho migration/admin.

### 3. Connection qua public endpoint

**Bẫy**: Droplet cùng region nhưng dùng `postgres-xxx.b.db...` public endpoint → traffic qua internet, tính bandwidth, latency cao.

**Fix**: Dùng `private-postgres-xxx.b.db...` cho Droplet cùng VPC.

### 4. Pool mode SESSION với prepared statement

**Bẫy**: Pool mode `transaction` không hỗ trợ prepared statement persistence → app báo lỗi `prepared statement "..." does not exist`.

**Fix**:
- Mode SESSION (mất lợi multiplex), HOẶC
- Tắt server-side prepared statement trong driver: `prepareThreshold=0` (Java JDBC), `prepare_threshold=None` (psycopg).

### 5. Standby fail nhưng cluster vẫn 1 node sống — không thay thế tự động

**Bẫy**: Standby chết → bạn không thấy thông báo → cluster về single point of failure.

**Fix**:
- Bật notification (Settings → Notifications).
- Add Slack webhook for DB alerts.
- DO sẽ rebuild standby tự động sau vài giờ — nhưng chủ động monitor vẫn cần.

### 6. PITR chỉ trong retention window

**Bẫy**: Drop table accidental 10 ngày trước → muốn restore qua PITR → không được vì retention 7 ngày.

**Fix**:
- Upgrade Pro để có 35-day retention.
- Manual `pg_dump` weekly to Spaces (giữ lâu hơn).

### 7. Resize storage không shrink

**Bẫy**: Mở rộng storage 100GB → muốn về 50GB → không cho.

**Fix**: Resize **up only**. Cần shrink → tạo cluster mới size nhỏ, `pg_dump`/`pg_restore`.

### 8. Major version upgrade gẫy extension

**Bẫy**: Upgrade Postgres 15 → 17, extension `pg_partman` không tương thích → app fail.

**Fix**:
- Test upgrade trên fork/replica trước.
- Read [DO release notes](https://docs.digitalocean.com/products/databases/postgresql/details/release-notes/).
- Schedule maintenance window low-traffic.

### 9. Maintenance window giờ peak

**Bẫy**: DO maintenance default Sunday 04:00 UTC — VN giờ trưa.

**Fix**: Set maintenance window phù hợp (Settings → Maintenance Window). Chọn giờ low-traffic local.

### 10. Connection limit hit

**Bẫy**: App spawn 1000 connection (no pool) → Postgres max_connections=22 (Basic 1GB) → fail.

**Fix**:
- Dùng pool endpoint (port 25061) thay vì direct (25060).
- App-side pool nhỏ + DB-side PgBouncer.
- Upgrade tier để max_connections cao hơn.

---

## 🧠 Self-check

**Q1.** Standby và Read Replica khác nhau thế nào?

<details>
<summary>💡 Đáp án</summary>

- **Standby**: passive, sync replicate, không cho query, auto-failover khi primary chết. Mục tiêu: HA.
- **Read Replica**: active, async replicate, read-only query được, có endpoint riêng. Mục tiêu: scale read.

Cùng cluster Pro có thể có **1 standby + N read replica**.

</details>

**Q2.** Khi nào dùng pool TRANSACTION mode, khi nào SESSION mode?

<details>
<summary>💡 Đáp án</summary>

- **TRANSACTION** (mặc định): hiệu quả nhất, app không cần feature SESSION-level. Phù hợp 90% case.
- **SESSION**: cần `LISTEN/NOTIFY`, prepared statement persist, advisory lock — feature giữ trạng thái cross-transaction.

Production app web: TRANSACTION. Worker dùng LISTEN/NOTIFY: SESSION.

</details>

**Q3.** Vì sao app phải dùng `app_user`, không phải `doadmin`?

<details>
<summary>💡 Đáp án</summary>

- `doadmin` = superuser, có thể DROP DATABASE, CREATE EXTENSION, modify schema.
- App compromise (SQL injection, leak) → attacker dùng doadmin → wipe DB.
- `app_user` chỉ SELECT/INSERT/UPDATE/DELETE → blast radius giới hạn.

Principle of Least Privilege.

</details>

**Q4.** PITR (Point-in-Time Recovery) hoạt động thế nào?

<details>
<summary>💡 Đáp án</summary>

DO stream **WAL (Write-Ahead Log)** liên tục → object storage. Khi restore:
1. Bắt đầu từ snapshot daily gần nhất trước thời điểm muốn restore.
2. Replay WAL từ snapshot tới đúng giây bạn chọn.
3. Stop replay → cluster mới ở trạng thái đó.

→ Restore đến **đúng giây** trong retention window (7-35 ngày).

</details>

**Q5.** Vì sao Trusted Sources + VPC private quan trọng?

<details>
<summary>💡 Đáp án</summary>

- Default DB cluster expose port 25060 ra internet → bot brute-force password.
- Trusted Sources whitelist IP/Droplet → drop mọi connection khác ở firewall layer.
- VPC private → traffic Droplet ↔ DB qua mạng riêng, không qua internet, không bandwidth phí, latency thấp.

Combined: zero attack surface từ internet.

</details>

---

## ⚡ Cheatsheet

| Mục đích | Lệnh |
|---|---|
| Tạo cluster | `doctl databases create NAME --engine pg --version 17 --size SIZE --num-nodes 2 --region sgp1` |
| List cluster | `doctl databases list` |
| Get connection | `doctl databases connection CLUSTER_ID` |
| Tạo DB | `doctl databases db create CLUSTER_ID DBNAME` |
| Tạo user | `doctl databases user create CLUSTER_ID USERNAME` |
| Reset password | `doctl databases user reset CLUSTER_ID USERNAME` |
| Add firewall rule | `doctl databases firewalls append CLUSTER_ID --rule droplet:ID` |
| Tạo pool | `doctl databases pool create CLUSTER_ID --name POOL --db DB --mode transaction --size 20 --user USER` |
| Failover (test) | `doctl databases failover CLUSTER_ID` |
| Backup list | `doctl databases backups CLUSTER_ID` |
| Restore PITR | UI: Backups → Restore from backup → select time |
| `pg_dump` | `pg_dump "URL" > backup.sql` |
| `psql` connect | `psql "postgresql://USER:PWD@HOST:25060/DB?sslmode=require"` |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| **Managed DB** | DB có quản | DB DO lo deploy/backup/HA/patch |
| **Standby** | Dự phòng đồng bộ | Node passive sync replicate, auto-failover |
| **Read replica** | Bản sao đọc | Node async replicate, read-only |
| **PgBouncer** | (giữ nguyên) | Connection pool proxy cho Postgres |
| **Session mode** | Chế độ phiên | 1 client = 1 backend cả session |
| **Transaction mode** | Chế độ giao dịch | 1 client = 1 backend trong 1 transaction |
| **PITR** | Khôi phục theo thời điểm | Point-in-Time Recovery — restore đến đúng giây |
| **WAL** | Nhật ký ghi-trước | Write-Ahead Log — Postgres streaming changes |
| **Trusted Sources** | Nguồn tin cậy | Firewall whitelist IP/Droplet |
| **VPC private** | Mạng riêng VPC | Network nội bộ region, không qua internet |
| **doadmin** | (giữ nguyên) | Tài khoản superuser DO tạo mặc định |
| **RBAC** | Quản lý truy cập theo vai | Role-Based Access Control |
| **Failover** | Chuyển đổi dự phòng | Primary chết → standby promote |
| **Maintenance window** | Cửa sổ bảo trì | Khung giờ DO apply patch |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [02_spaces-object-storage-and-cdn](02_spaces-object-storage-and-cdn.md)
- → Tiếp: [04_app-platform-and-functions](04_app-platform-and-functions.md)
- ↑ Cluster DigitalOcean: [DigitalOcean README](../../README.md)

### Cross-reference
- ☁️ [AWS RDS + DynamoDB](../../../aws/lessons/01_basic/03_rds-and-dynamodb.md) — so sánh
- 🐘 [Postgres](../../../../03_Programming/databases/postgres/) — engine deep dive
- 🐍 [SQLAlchemy + asyncpg](../../../../07_web/backend/python-fastapi/) — driver

### Tài nguyên ngoài (2026)
- 📖 [DO Managed Databases docs](https://docs.digitalocean.com/products/databases/)
- 📖 [DO Postgres docs](https://docs.digitalocean.com/products/databases/postgresql/)
- 📖 [DO Connection pools](https://docs.digitalocean.com/products/databases/postgresql/how-to/manage-connection-pools/)
- 📖 [PgBouncer docs](https://www.pgbouncer.org/)
- 📖 [Postgres official docs](https://www.postgresql.org/docs/17/)
- 📖 [DO Database pricing](https://www.digitalocean.com/pricing/managed-databases)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu. Managed DB rationale + 5 engine (Postgres/MySQL/Redis/MongoDB/Kafka) + tier matrix + standby vs read replica + PgBouncer pool mode + backup PITR + Trusted Sources + VPC private + user RBAC + hands-on Postgres production + 10 pitfalls.
