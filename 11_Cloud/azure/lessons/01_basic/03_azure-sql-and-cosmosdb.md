# 🗄️ Azure SQL + Cosmos DB

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [02_blob-storage-and-rbac](02_blob-storage-and-rbac.md) ✅, hiểu SQL vs NoSQL khác nhau ở đâu, ACID, eventual consistency

> 🎯 *Database trên Azure có 2 dòng chính: **Azure SQL** (relational, ACID) cho transactional workload; **Cosmos DB** (NoSQL multi-API global) cho high-scale low-latency. Bài này dạy: Azure SQL Database (DTU vs vCore, Hyperscale), Managed Instance, geo-replication, PITR; Cosmos DB multi-API (SQL/Mongo/Cassandra/Gremlin/Table) + 5 consistency levels + multi-region writes; decision matrix khi nào dùng cái nào.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Azure SQL Database** vs **Managed Instance** vs **SQL VM**
- [ ] Hiểu **DTU vs vCore** purchasing model + khi nào chọn cái nào
- [ ] **Service tier**: Basic / Standard / Premium / General Purpose / Business Critical / Hyperscale
- [ ] **Geo-replication** + **Auto-failover Group** + **PITR** (Point-in-Time Restore)
- [ ] **Always Encrypted** + **TDE** + **Dynamic Data Masking**
- [ ] **Cosmos DB** — 5 API (SQL/Mongo/Cassandra/Gremlin/Table) + khi nào dùng cái nào
- [ ] **5 consistency level**: Strong / Bounded Staleness / Session / Consistent Prefix / Eventual
- [ ] **Multi-region writes** + **partition key** design
- [ ] **RU/s** (Request Unit) — pricing model Cosmos
- [ ] Decision matrix: Azure SQL vs Cosmos vs Postgres flexible vs MySQL flexible

---

## Tình huống — Acme Shop database stack

Sếp:

> *"Acme Shop đang trên SQL Server on-prem, 500GB orders. Migrate lên Azure SQL Database. Yêu cầu: HA cross-region (Singapore + Tokyo), PITR 35 ngày, encryption at rest + in transit, không downtime > 30 phút. Bên cạnh đó, mobile app user session + cart cần DB low-latency global — multi-region writes. Recommend stack."*

Bạn cần:

- **Azure SQL Database** Business Critical tier cho orders (HA + low latency + read replicas).
- **Auto-failover Group** Singapore ↔ Tokyo.
- **PITR 35 ngày** + long-term retention.
- **TDE** với CMK Key Vault.
- **Cosmos DB SQL API** multi-region writes cho session/cart.
- **Session consistency** cho user experience.

Bài này dạy từng phần + decision matrix.

---

## 1️⃣ Azure SQL — 3 deployment options

🪞 **Ẩn dụ**: *3 lựa chọn như **3 cách thuê căn hộ** — Azure SQL Database = thuê **căn hộ chung cư** (Microsoft quản hết, tiện nhưng giới hạn customize); Managed Instance = thuê **biệt thự gated community** (gần full SQL Server feature, có VNet riêng, quản nhiều hơn); SQL VM = tự **mua đất xây nhà** (toàn quyền OS + SQL, nhưng phải tự lo mọi thứ).*

| Option | Mô tả | Compat | Customize | Cost | Use case |
|---|---|---|---|---|---|
| **Azure SQL Database** | PaaS — 1 database (or elastic pool) | ~99% SQL Server | Hạn chế | Lowest | Default — new app cloud-native |
| **Azure SQL Managed Instance** | PaaS — full SQL Server instance | ~100% (SQL Agent, CLR, cross-DB query) | Trung bình | Mid | Lift-and-shift, legacy app |
| **SQL Server on Azure VM** | IaaS — VM Windows/Linux + SQL Server | 100% (you control) | Full | Highest | Custom CLR, third-party agent, full control |

→ **Default 2026**: SQL Database. Lift-and-shift on-prem SQL Server: Managed Instance. Edge case full control: SQL VM.

### Azure SQL Database — purchasing model

#### A. DTU-based (legacy)

DTU = Database Transaction Unit = blended CPU + IO + memory.

| Tier | DTU | Storage | Max DBs | Use case |
|---|---|---|---|---|
| **Basic** | 5 | 2 GB | 1 | Dev/test toy |
| **Standard S0–S12** | 10-3000 | 250 GB | 1 | Small-medium production |
| **Premium P1–P15** | 125-4000 | 1 TB | 1 | High-perf OLTP |

→ DTU = "tù mù", khó tune. **2026 deprecated cho new project**.

#### B. vCore-based (recommended)

vCore = explicit CPU + RAM + storage. Đắt hơn DTU một chút nhưng predictable.

| Tier | Compute | Storage | HA |
|---|---|---|---|
| **General Purpose** | 2-128 vCore | Premium SSD remote | 1 replica (standby in same region) |
| **Business Critical** | 2-128 vCore | Local SSD (low latency) | 4-node cluster + 1 read replica free |
| **Hyperscale** | 2-128 vCore | Distributed page server | up to 4 read replicas, 100TB storage |

#### Hyperscale — Azure exclusive

= storage layer tách compute, scale to **100 TB**, snapshot < 1 phút, scale compute up/down trong giây.

```
Traditional SQL Database:
  Compute → local disk → 4 TB max

Hyperscale:
  Compute (primary + read replicas)
    ↓
  Page Servers (distributed, scale-out storage)
    ↓
  Long-term log storage (Azure Storage)

Benefit:
  - 100 TB database
  - Instant backup (storage-level snapshot)
  - Add read replica in seconds
  - Compute scale in/out without storage migration
```

→ Use case: large OLTP (e-commerce >10TB), data warehouse-like analytics.

#### Cost example (2026, southeastasia)

```
Standard S2 (50 DTU, 250GB):        ~$75/month
GP 2 vCore Gen5:                     ~$370/month
BC 2 vCore Gen5:                     ~$1000/month
Hyperscale 2 vCore 100GB:            ~$400/month + storage
```

→ vCore đắt hơn nhưng có **Azure Hybrid Benefit** (mang license SQL Server có sẵn = giảm 30-55%).

---

## 2️⃣ Azure SQL HA + DR

### Service tier HA built-in

| Tier | HA option |
|---|---|
| Basic / Standard | Local replica (within DC) |
| Premium / Business Critical | AlwaysOn cluster 4 nodes, free read replica |
| General Purpose | Remote storage, standby compute |
| Hyperscale | Page servers replicated, instant failover |

→ Built-in HA = SLA **99.99-99.995%** không cần config.

### Geo-replication (cross-region read replica)

```bash
# Tạo geo-replica từ Singapore → Tokyo
az sql db replica create \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --name orders \
    --partner-server sql-prod-jpe \
    --partner-resource-group rg-prod-data
```

- Async replication, lag thường <5s.
- Tokyo replica read-only.
- Manual failover trong portal.

### Auto-failover Group (production recommended)

```bash
# Failover group = group nhiều DB + auto failover policy
az sql failover-group create \
    --name fg-acmeshop-prod \
    --partner-server sql-prod-jpe \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --add-db orders inventory users \
    --failover-policy Automatic \
    --grace-period 1
```

- Single connection string (`fg-acmeshop-prod.database.windows.net`) → auto resolve primary.
- Automatic failover khi primary unhealthy ≥ grace period.
- RPO < 5s, RTO < 1 phút (Business Critical).

### PITR (Point-in-Time Restore)

```bash
# Restore tới 1 thời điểm cụ thể
az sql db restore \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --name orders \
    --dest-name orders-restored \
    --time "2026-05-24T03:15:00"
```

- Default retention **7 ngày**, có thể tăng tới **35 ngày**.
- Long-term retention (LTR): weekly/monthly/yearly tới **10 năm** (compliance).
- Cost: backup storage = 100% size DB free, vượt mới tính.

---

## 3️⃣ Azure SQL Security

### TDE (Transparent Data Encryption) — default

- AES 256, encrypt at rest.
- Default: **Service-managed key** (Microsoft quản).
- BYOK: **Customer-managed key** với Key Vault.

```bash
az sql db tde set \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --database orders \
    --status Enabled
```

### CMK (Customer-Managed Key) for TDE

```bash
# Bật Managed Identity cho SQL Server
az sql server update --name sql-prod-sea --resource-group rg-prod-data --identity-type SystemAssigned

# Grant SQL Server access Key Vault
SQL_PRINCIPAL=$(az sql server show -n sql-prod-sea -g rg-prod-data --query identity.principalId -o tsv)
az role assignment create \
    --assignee $SQL_PRINCIPAL \
    --role "Key Vault Crypto Service Encryption User" \
    --scope "/subscriptions/<sub>/resourceGroups/rg-prod-data/providers/Microsoft.KeyVault/vaults/kv-acmeshop-prod"

# Set key
az sql server key create \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --kid https://kv-acmeshop-prod.vault.azure.net/keys/sql-cmk/<version>

az sql server tde-key set \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --server-key-type AzureKeyVault \
    --kid https://kv-acmeshop-prod.vault.azure.net/keys/sql-cmk/<version>
```

### Always Encrypted (column-level, even DBA không thấy plaintext)

- Encrypt key sit at **client driver**, không gửi server.
- Server thấy ciphertext.
- Use case: cột PII (SSN, card number), compliance HIPAA/PCI.

```sql
-- Trong SQL Server / SSMS
CREATE COLUMN MASTER KEY CMK_Auto1
WITH (KEY_STORE_PROVIDER_NAME = N'AZURE_KEY_VAULT',
      KEY_PATH = N'https://kv-acmeshop-prod.vault.azure.net/keys/aealways/...');

CREATE COLUMN ENCRYPTION KEY CEK_Auto1
WITH VALUES (...);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    email VARCHAR(100),
    ssn VARCHAR(11) ENCRYPTED WITH (
        COLUMN_ENCRYPTION_KEY = CEK_Auto1,
        ENCRYPTION_TYPE = DETERMINISTIC,
        ALGORITHM = 'AEAD_AES_256_CBC_HMAC_SHA_256'
    )
);
```

### Dynamic Data Masking (DDM)

= mask data trong query result theo role. Đơn giản hơn Always Encrypted nhưng kém secure (server vẫn thấy plaintext).

```sql
ALTER TABLE customers ALTER COLUMN email
ADD MASKED WITH (FUNCTION = 'email()');

-- User without UNMASK permission sees: aXXX@XXXX.com
```

### Microsoft Defender for SQL

- Vulnerability assessment.
- Advanced Threat Protection (SQL injection detect, anomalous login, ...).
- Cost: $15/server/tháng.

### Auth methods

1. **SQL auth** — username/password (legacy, dùng cho app cũ).
2. **Entra ID auth** (recommended) — single sign-on, MFA, audit centralized.

```bash
# Set Entra ID admin cho server
az sql server ad-admin create \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --display-name "DBA Admins" \
    --object-id <group-objectid>
```

```sql
-- Connect via Entra ID
sqlcmd -S sql-prod-sea.database.windows.net -G -d orders
```

---

## 4️⃣ Cosmos DB — multi-API global NoSQL

🪞 **Ẩn dụ**: *Cosmos DB như **dịch vụ chuyển phát toàn cầu** — dữ liệu của bạn được nhân bản tới 30+ region trên thế giới; user ở Nhật đọc replica Tokyo, user ở Việt Nam đọc Singapore — latency <10ms khắp nơi. Bạn chọn **5 mức "trust" lá thư đến nhanh hay chậm** (consistency level) — strong = thư đến đúng thứ tự khắp nơi nhưng chậm; eventual = thư có thể đến lệch order nhưng nhanh nhất.*

### Cosmos DB là gì

= managed NoSQL database, **globally distributed**, **multi-API**, **single-digit ms latency**.

Khác DynamoDB: Cosmos hỗ trợ **5 API** (DynamoDB chỉ proprietary API).

### 5 API options

| API | Compatible với | Use case |
|---|---|---|
| **NoSQL API** (formerly SQL API) | JSON document, query SQL-like | Default cho new app, document store |
| **MongoDB API** | MongoDB driver wire protocol | Migrate MongoDB app |
| **Cassandra API** | Apache Cassandra CQL | Migrate Cassandra app |
| **Gremlin API** | Apache TinkerPop graph | Graph queries (social, fraud detect) |
| **Table API** | Azure Table Storage | Migrate from Azure Table |

→ **Pick 1 API per account** (không đổi sau khi tạo). Default: **NoSQL API**.

### Hierarchy

```
Cosmos DB Account: cosmos-acmeshop-prod
├── Database: shopdb
│   ├── Container: sessions      ← partition by /userId
│   │   ├── Document {userId: "u-001", cart: [...]}
│   │   └── Document {userId: "u-002", cart: [...]}
│   ├── Container: products      ← partition by /category
│   └── Container: orders        ← partition by /orderId
└── Database: analyticsdb
```

### Partition key — quan trọng nhất

= field dùng để shard data across physical partitions.

```
Choose partition key:
  ✅ Cardinality cao (nhiều giá trị unique)
  ✅ Phân bố đều (không hot spot)
  ✅ Match query pattern (đa số query filter on this)

Bad: /country → 200 giá trị, "VN" chiếm 80% → hot partition
Good: /userId → triệu giá trị, đều
Good: /tenantId + /userId synthetic key
```

→ Chọn sai partition key = phải migrate (downtime). Suy nghĩ kỹ ngày 1.

### RU/s — Request Unit per second

= unit pricing Cosmos, mỗi operation tiêu RU:

```
Read 1KB doc by ID         = 1 RU
Read 1KB doc by query      = 2-3 RU (with index)
Write 1KB doc              = 5-10 RU
Delete 1KB doc             = 5 RU
Query 100 docs             = 20-50 RU
```

#### Provisioned throughput

```bash
# Tạo container với 1000 RU/s
az cosmosdb sql container create \
    --account-name cosmos-acmeshop-prod \
    --database-name shopdb \
    --name sessions \
    --partition-key-path /userId \
    --throughput 1000
```

→ Pay $0.008/100 RU/h ≈ $58/month per 1000 RU/s.

#### Autoscale

```bash
az cosmosdb sql container create \
    --account-name cosmos-acmeshop-prod \
    --database-name shopdb \
    --name sessions \
    --partition-key-path /userId \
    --max-throughput 4000
```

→ Scale 400-4000 RU/s. Pay theo max consumption hourly. Cost ~1.5x provisioned nhưng linh hoạt.

#### Serverless

```bash
# Cosmos DB account serverless (set on account create)
az cosmosdb create \
    --name cosmos-acmeshop-dev \
    --resource-group rg-dev-data \
    --capabilities EnableServerless
```

- Pay per request (5 RU = $0.000026).
- Free Tier always: 1000 RU/s + 25 GB.
- Use case: dev/sandbox, traffic spike unpredictable.

---

## 5️⃣ Consistency levels — 5 mức

🪞 **Ẩn dụ tiếp**: *Strong = thư bảo đảm — ai cũng đọc cùng nội dung mới nhất, chậm; Eventual = bưu thiếp — nhanh nhưng có thể lệch order; 3 mức giữa là trade-off.*

| Level | Mô tả | Latency | Use case |
|---|---|---|---|
| **Strong** | Linearizable — đọc luôn thấy write mới nhất | Cao nhất | Banking, leaderboard real-time |
| **Bounded Staleness** | Lag bound theo K version hoặc T thời gian | Trung bình | Status feed, "đã đọc" cuối cùng < 5 phút |
| **Session** (default) | Within session: strong; cross-session: eventual | Thấp | Default — user-centric app |
| **Consistent Prefix** | Đọc thấy đúng thứ tự, nhưng có thể lag | Thấp | Chat order, comment |
| **Eventual** | Cuối cùng converge, không guarantee order | Thấp nhất | Counter, like, view count |

→ Default Cosmos: **Session**. App phổ biến (web, mobile) chọn Session.

### Set level

```bash
az cosmosdb create \
    --name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --default-consistency-level Session
```

Override per-request:

```python
from azure.cosmos import CosmosClient, ConsistencyLevel

client.read_item(item="u-001", partition_key="u-001",
                 consistency_level=ConsistencyLevel.Strong)
```

---

## 6️⃣ Multi-region writes (active-active)

### Single-region write (default)

```
1 region = write region (Singapore)
N region = read replica (Tokyo, London, ...)
```

→ User Tokyo read local (fast), nhưng write phải gửi Singapore (slow).

### Multi-region writes

```bash
az cosmosdb update \
    --name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --locations regionName=southeastasia failoverPriority=0 isZoneRedundant=False \
    --locations regionName=japaneast failoverPriority=1 isZoneRedundant=False \
    --enable-multiple-write-locations true
```

→ User write local region → faster. Cost gấp ~2x (cần CRDT-like merge logic).

### Conflict resolution

- **Last Write Wins** (LWW, default) — based on `_ts` (timestamp).
- **Custom merge function** — stored procedure on conflict.

→ Use case multi-region writes: high-velocity write toàn cầu (chat, IoT, gaming). Cẩn thận với data integrity.

---

## 7️⃣ Decision matrix — DB nào cho workload nào

| Workload | Recommend | Lý do |
|---|---|---|
| OLTP relational, ACID, transactions | **Azure SQL Database** GP/BC | SQL, relational, mature |
| Legacy on-prem SQL Server migrate | **Azure SQL Managed Instance** | Near-100% compat |
| Need OS-level access SQL | **SQL Server on VM** | Full control |
| Postgres / MySQL workload | **Azure Database for PostgreSQL/MySQL Flexible Server** | OSS compat |
| Document/JSON store, single-region | **Cosmos DB Serverless** hoặc **Azure SQL JSON columns** | Cost-effective |
| Global multi-region low-latency | **Cosmos DB** any API | Built-in geo + 5 consistency |
| Mongo migrate | **Cosmos DB Mongo API** hoặc **Mongo Atlas on Azure** | Wire protocol compat |
| Cassandra migrate | **Cosmos DB Cassandra API** | CQL compat |
| Graph (social, fraud) | **Cosmos DB Gremlin API** | Native graph traversal |
| Analytics OLAP | **Synapse Analytics** | Columnar, petabyte |
| Time series | **Azure Data Explorer (ADX)** | Optimized for telemetry |
| Cache | **Azure Cache for Redis** | Sub-ms latency |

→ Quy tắc: **default SQL** cho relational, **Cosmos** cho NoSQL global, **Synapse** cho OLAP, **Redis** cho cache.

---

## 🛠️ Hands-on — Stack Azure SQL + Cosmos cho Acme Shop

### Mục tiêu

Deploy Azure SQL Database (orders) + Cosmos DB (user sessions), test failover SQL, test multi-region read Cosmos.

### Bước 1 — Azure SQL Database

```bash
az group create --name rg-prod-data --location southeastasia

# SQL Server (logical, không phải VM)
az sql server create \
    --name sql-acmeshop-prod-sea \
    --resource-group rg-prod-data \
    --location southeastasia \
    --admin-user sqladmin \
    --admin-password 'Strong-Password-123!' \
    --enable-public-network false  # Public disable, dùng Private Endpoint sau

# Firewall: allow Azure services + my IP
MY_IP=$(curl -s ifconfig.me)
az sql server firewall-rule create \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --name AllowMyIP \
    --start-ip-address $MY_IP --end-ip-address $MY_IP

# Database — General Purpose 2 vCore
az sql db create \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --name orders \
    --edition GeneralPurpose \
    --family Gen5 \
    --capacity 2 \
    --backup-storage-redundancy Zone \
    --zone-redundant false
```

### Bước 2 — Bật PITR 35 ngày + TDE

```bash
# PITR retention
az sql db update \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --name orders \
    --backup-storage-redundancy Geo  # cross-region backup

# Set short-term retention 35 days
az sql db short-term-retention-policy set \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --database orders \
    --retention-days 35

# TDE default already on
az sql db tde show \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --database orders
```

### Bước 3 — Geo-replica + Failover Group

```bash
# SQL server thứ 2 ở Tokyo
az sql server create \
    --name sql-acmeshop-prod-jpe \
    --resource-group rg-prod-data \
    --location japaneast \
    --admin-user sqladmin \
    --admin-password 'Strong-Password-123!'

# Failover group
az sql failover-group create \
    --name fg-acmeshop-prod \
    --partner-server sql-acmeshop-prod-jpe \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --add-db orders \
    --failover-policy Automatic \
    --grace-period 1

# Connection string (single endpoint)
echo "Server=fg-acmeshop-prod.database.windows.net;Database=orders;..."
```

### Bước 4 — Connect + create table

```bash
# Cài sqlcmd
brew install sqlcmd  # macOS

sqlcmd -S fg-acmeshop-prod.database.windows.net -U sqladmin -P 'Strong-Password-123!' -d orders -Q "
CREATE TABLE orders (
    id INT IDENTITY PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2),
    created_at DATETIME2 DEFAULT SYSUTCDATETIME()
);

INSERT INTO orders (user_id, amount) VALUES ('u-001', 100.00), ('u-002', 250.50);

SELECT * FROM orders;
"
```

### Bước 5 — Cosmos DB account multi-region

```bash
az cosmosdb create \
    --name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --locations regionName=southeastasia failoverPriority=0 isZoneRedundant=False \
    --locations regionName=japaneast failoverPriority=1 isZoneRedundant=False \
    --kind GlobalDocumentDB \
    --default-consistency-level Session \
    --enable-multiple-write-locations true \
    --enable-automatic-failover true

# Database + Container
az cosmosdb sql database create \
    --account-name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --name shopdb

az cosmosdb sql container create \
    --account-name cosmos-acmeshop-prod \
    --database-name shopdb \
    --resource-group rg-prod-data \
    --name sessions \
    --partition-key-path /userId \
    --throughput 400  # min provisioned
```

### Bước 6 — Insert + query Cosmos

```python
# cosmos_test.py
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

url = "https://cosmos-acmeshop-prod.documents.azure.com"
cred = DefaultAzureCredential()
client = CosmosClient(url, credential=cred)

db = client.get_database_client("shopdb")
container = db.get_container_client("sessions")

# Insert
container.upsert_item({
    "id": "session-001",
    "userId": "u-001",
    "cart": [{"sku": "prod-A", "qty": 2}],
    "createdAt": "2026-05-24T10:00:00Z"
})

# Query (partition key in filter = cheaper)
for item in container.query_items(
    query="SELECT * FROM c WHERE c.userId = @userId",
    parameters=[{"name": "@userId", "value": "u-001"}],
    enable_cross_partition_query=False
):
    print(item)
```

```bash
# Cần grant data plane role
USER_ID=$(az ad signed-in-user show --query id -o tsv)
az cosmosdb sql role assignment create \
    --account-name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --scope "/" \
    --principal-id $USER_ID \
    --role-definition-id "00000000-0000-0000-0000-000000000002"  # Cosmos DB Built-in Data Contributor

pip install azure-cosmos azure-identity
python cosmos_test.py
```

### Bước 7 — Test failover

```bash
# Manual failover SQL
az sql failover-group set-primary \
    --name fg-acmeshop-prod \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-jpe

# Verify connection string vẫn work — auto resolve sang Tokyo
sqlcmd -S fg-acmeshop-prod.database.windows.net ... -Q "SELECT @@SERVERNAME"
```

### Bước 8 — Cleanup

```bash
az group delete --name rg-prod-data --yes --no-wait
```

→ **Kết quả**: SQL geo-replicated SEA↔JPE, Cosmos multi-region write 2 region, PITR 35 ngày, end-to-end working.

---

## ⚠️ Pitfalls

### 1. Chọn DTU thay vì vCore cho new project

**Bẫy**: Pick DTU vì rẻ → khó tune, không có Hyperscale option, không Hybrid Benefit.

**Fix**: 2026 luôn vCore. Hybrid Benefit nếu có license SQL Server.

### 2. Backup storage = LRS mặc định

**Bẫy**: SQL Database backup default LRS → mất cả region → mất backup.

**Fix**: `--backup-storage-redundancy Geo` hoặc `Zone` (production).

### 3. PITR chỉ 7 ngày mặc định

**Bẫy**: Phát hiện corruption sau 10 ngày → quá retention → không restore.

**Fix**: Set `--retention-days 35` (max short-term). Compliance → LTR weekly/monthly/yearly.

### 4. Cosmos partition key nhầm = hot partition

**Bẫy**: Partition by `/country` → "VN" chiếm 80% → throttle.

**Fix**:
- Cardinality cao + phân bố đều.
- Synthetic key: `/tenantId_userId`.
- Test với production-like data trước launch.
- Re-partition = migrate full data (downtime).

### 5. Cross-partition query rất đắt

**Bẫy**: Query không filter partition key → fan-out tới mọi partition → RU cost x100.

**Fix**:
- Luôn filter partition key trong WHERE.
- `enable_cross_partition_query=False` để fail-fast.
- Nếu cần cross-partition: pre-aggregate vào container thứ 2.

### 6. Cosmos Strong consistency single-region

**Bẫy**: Strong consistency + multi-region writes → KHÔNG support đồng thời (chỉ Bounded Staleness max).

**Fix**:
- Multi-region writes → max Bounded Staleness.
- Need Strong → single-region write, multi-region read.

### 7. Always Encrypted query limit

**Bẫy**: Encrypt column với Randomized algorithm → không LIKE / range query được.

**Fix**:
- Deterministic encryption: equality query OK, không range.
- Randomized: max security nhưng chỉ INSERT/SELECT plain.
- Trade-off: security vs query capability.

### 8. Cosmos RU/s estimation sai

**Bẫy**: Set 400 RU/s (min) → traffic spike → 429 throttle → user-facing fail.

**Fix**:
- Bật **autoscale** thay vì provisioned cố định.
- Monitor `Total Request Units` metric.
- Set max-throughput đủ cho peak.

### 9. SQL connection pool exhaustion

**Bẫy**: App tạo new connection mỗi request → 1800 connection limit Standard tier → hit ceiling.

**Fix**:
- Connection pooling (HikariCP / SQLAlchemy pool).
- Pool size = 2 * CPU + 1 (Microsoft khuyến nghị).
- Idle timeout đủ ngắn để recycle.

### 10. Public network bật mặc định

**Bẫy**: SQL Server tạo qua portal default public + "allow Azure services" → ai có Azure account login được.

**Fix**:
- `--enable-public-network false`.
- Private Endpoint trong VNet.
- Hoặc deny all + allow specific IP.

---

## 🎯 Self-check

- [ ] SQL Database vs Managed Instance vs SQL VM — pick cho 3 scenario?
- [ ] DTU vs vCore — vì sao vCore tốt hơn 2026?
- [ ] General Purpose vs Business Critical vs Hyperscale — khác nhau ở đâu?
- [ ] Geo-replica vs Auto-failover Group — group có gì hơn?
- [ ] TDE vs Always Encrypted — khi nào dùng cái nào?
- [ ] Cosmos 5 API — pick cho document store, graph, Cassandra migrate?
- [ ] Partition key design tốt — 3 nguyên tắc?
- [ ] 5 consistency level — pick cho banking, social feed, counter?
- [ ] Multi-region writes — khi nào worth it, khi nào không?
- [ ] Provisioned vs Autoscale vs Serverless Cosmos — chọn cái nào?

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Azure SQL Database** | PaaS SQL Server đơn database/pool |
| **Managed Instance** | PaaS SQL Server full instance, gần 100% compat |
| **DTU** | Database Transaction Unit (legacy purchasing) |
| **vCore** | Virtual core (modern purchasing) |
| **GP / BC / Hyperscale** | Service tier vCore |
| **Hyperscale** | 100 TB storage, instant scale, snapshot < 1 phút |
| **PITR** | Point-in-Time Restore |
| **LTR** | Long-Term Retention (10 năm) |
| **TDE** | Transparent Data Encryption (at-rest) |
| **CMK** | Customer-Managed Key |
| **Always Encrypted** | Column-level encrypt, key tại client |
| **DDM** | Dynamic Data Masking |
| **Failover Group** | Group DB + auto-failover policy |
| **Cosmos DB** | NoSQL global multi-API |
| **NoSQL API** | Tên mới của SQL API (JSON document) |
| **RU/s** | Request Unit per second — pricing |
| **Partition key** | Field dùng shard data |
| **Consistency level** | 5 mức trade-off latency vs consistency |
| **Session consistency** | Default — within session strong, cross eventual |
| **Multi-region writes** | Write any region, replicate global |
| **LWW** | Last Write Wins — conflict resolution default |
| **Autoscale** | RU/s scale 0.1x-1x max theo load |
| **Serverless** | Pay per request, no min throughput |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [02_blob-storage-and-rbac](02_blob-storage-and-rbac.md)
- → Tiếp: [04_functions-and-app-service](04_functions-and-app-service.md)
- ↑ Cluster Azure: [Azure README](../../README.md)

### Cross-reference
- ☁️ [AWS RDS + DynamoDB](../../../aws/lessons/01_basic/03_rds-and-dynamodb.md) — analog
- ☁️ [GCP Cloud SQL + Firestore](../../../gcp/lessons/01_basic/03_cloud-sql-and-firestore.md) — analog
- 📚 [Databases foundation](../../../../06_Data/databases/) — SQL vs NoSQL fundamentals
- 🏗️ [Terraform azurerm_mssql](../../../../10_DevOps/iac/)

### Tài nguyên ngoài (2026)
- 📖 [Azure SQL Database docs](https://learn.microsoft.com/azure/azure-sql/database/)
- 📖 [vCore purchasing model](https://learn.microsoft.com/azure/azure-sql/database/service-tiers-vcore)
- 📖 [Hyperscale service tier](https://learn.microsoft.com/azure/azure-sql/database/service-tier-hyperscale)
- 📖 [Auto-failover Group](https://learn.microsoft.com/azure/azure-sql/database/auto-failover-group-sql-db)
- 📖 [PITR + LTR](https://learn.microsoft.com/azure/azure-sql/database/long-term-retention-overview)
- 📖 [Always Encrypted](https://learn.microsoft.com/azure/azure-sql/database/always-encrypted-azure-key-vault-configure)
- 📖 [Cosmos DB docs](https://learn.microsoft.com/azure/cosmos-db/)
- 📖 [Partition key design](https://learn.microsoft.com/azure/cosmos-db/partitioning-overview)
- 📖 [Consistency levels](https://learn.microsoft.com/azure/cosmos-db/consistency-levels)
- 📖 [Multi-region writes](https://learn.microsoft.com/azure/cosmos-db/how-to-multi-master)
- 📖 [RU/s calculator](https://cosmos.azure.com/capacitycalculator/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 03 cluster Azure basic. Azure SQL Database/Managed Instance/SQL VM + DTU vs vCore + GP/BC/Hyperscale + geo-replication + Failover Group + PITR/LTR + TDE/Always Encrypted/DDM + Cosmos DB 5 API + 5 consistency level + multi-region writes + RU/s + decision matrix + hands-on stack SQL+Cosmos + 10 pitfalls. Mirror AWS RDS+DynamoDB lesson.
