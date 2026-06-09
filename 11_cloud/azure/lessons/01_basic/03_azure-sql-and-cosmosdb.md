# 🗄️ Azure SQL + Cosmos DB

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [02_blob-storage-and-rbac](02_blob-storage-and-rbac.md) ✅, hiểu SQL vs NoSQL khác nhau ở đâu, ACID, eventual consistency

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

Hãy bắt đầu từ một yêu cầu rất thực, kiểu mà bất kỳ ai làm cloud cũng sẽ nhận sớm muộn. Sếp dừng lại ở bàn bạn:

> *"Acme Shop đang trên SQL Server on-prem, 500GB orders. Migrate lên Azure SQL Database. Yêu cầu: HA cross-region (Singapore + Tokyo), PITR 35 ngày, encryption at rest + in transit, không downtime > 30 phút. Bên cạnh đó, mobile app user session + cart cần DB low-latency global — multi-region writes. Recommend stack."*

Yêu cầu này chạm vào gần như mọi khái niệm của bài. Đọc kỹ sẽ thấy nó tách làm hai bài toán khác hẳn nhau: phần *orders* là dữ liệu giao dịch quan hệ cần ACID và HA, còn phần *session/cart* là dữ liệu phân tán toàn cầu cần độ trễ thấp. Hai nhu cầu đó dẫn tới hai loại database khác nhau — và đó chính là lý do Azure tách Azure SQL khỏi Cosmos DB. Đáp án mà ta sẽ ráp dần qua cả bài trông như sau:

- **Azure SQL Database** Business Critical tier cho orders (HA + low latency + read replicas).
- **Auto-failover Group** Singapore ↔ Tokyo.
- **PITR 35 ngày** + long-term retention.
- **TDE** với CMK Key Vault.
- **Cosmos DB SQL API** multi-region writes cho session/cart.
- **Session consistency** cho user experience.

Từng mảnh ghép trên sẽ được mổ xẻ ở các phần dưới, kèm decision matrix để bạn tự ráp cho workload của mình.

---

## 1️⃣ Azure SQL — 3 deployment options

Trước khi chọn tier hay model giá, câu hỏi đầu tiên luôn là: *chạy SQL Server trên Azure theo kiểu nào?* Azure cho ba lựa chọn, khác nhau ở mức độ Microsoft lo hộ bạn bao nhiêu.

🪞 **Ẩn dụ**: *3 lựa chọn như **3 cách thuê căn hộ** — Azure SQL Database = thuê **căn hộ chung cư** (Microsoft quản hết, tiện nhưng giới hạn customize); Managed Instance = thuê **biệt thự gated community** (gần full SQL Server feature, có VNet riêng, quản nhiều hơn); SQL VM = tự **mua đất xây nhà** (toàn quyền OS + SQL, nhưng phải tự lo mọi thứ).*

Bảng dưới đặt ba lựa chọn cạnh nhau theo các trục bạn sẽ cân nhắc thật khi quyết định — độ tương thích với SQL Server gốc, khả năng customize, chi phí và tình huống dùng:

| Option | Mô tả | Compat | Customize | Cost | Use case |
|---|---|---|---|---|---|
| **Azure SQL Database** | PaaS — 1 database (or elastic pool) | ~99% SQL Server | Hạn chế | Lowest | Default — new app cloud-native |
| **Azure SQL Managed Instance** | PaaS — full SQL Server instance | ~100% (SQL Agent, CLR, cross-DB query) | Trung bình | Mid | Lift-and-shift, legacy app |
| **SQL Server on Azure VM** | IaaS — VM Windows/Linux + SQL Server | 100% (you control) | Full | Highest | Custom CLR, third-party agent, full control |

Quy tắc chọn rút gọn cho năm 2026: app mới sinh ra trên cloud thì mặc định dùng **SQL Database**; nếu là lift-and-shift một SQL Server on-prem có dùng SQL Agent hay cross-DB query thì chọn **Managed Instance**; còn các edge case cần đụng tới OS hoặc cài agent của bên thứ ba thì mới phải hạ xuống **SQL VM**.

### Azure SQL Database — purchasing model

Đã chọn SQL Database, bạn còn phải quyết một thứ nữa: trả tiền theo model nào. Azure có hai model giá, và việc chọn sai ở đây sẽ khoá luôn các tính năng cao cấp về sau.

#### A. DTU-based (legacy)

Model cũ gói gọn mọi tài nguyên vào một con số duy nhất gọi là DTU. DTU (Database Transaction Unit) là một đơn vị *trộn* CPU + IO + memory lại với nhau — bạn không thấy được từng thành phần, chỉ thấy một con số tổng.

| Tier | DTU | Storage | Max DBs | Use case |
|---|---|---|---|---|
| **Basic** | 5 | 2 GB | 1 | Dev/test toy |
| **Standard S0–S12** | 10-3000 | 250 GB | 1 | Small-medium production |
| **Premium P1–P15** | 125-4000 | 1 TB | 1 | High-perf OLTP |

Cái dở của DTU là chính sự "trộn" đó: khi DB chậm, bạn không biết nghẽn ở CPU hay IO để mà tune. Vì vậy năm 2026 model này coi như **deprecated cho project mới** — chỉ còn gặp ở các DB cũ chưa migrate.

#### B. vCore-based (recommended)

Model hiện đại làm ngược lại: tách bạch từng thành phần. vCore cho bạn chỉ định rõ số CPU + RAM + storage, nên chi phí *dự đoán được* và việc tune cũng minh bạch. Đắt hơn DTU một chút nhưng đáng.

| Tier | Compute | Storage | HA |
|---|---|---|---|
| **General Purpose** | 2-128 vCore | Premium SSD remote | 1 replica (standby in same region) |
| **Business Critical** | 2-128 vCore | Local SSD (low latency) | 4-node cluster + 1 read replica free |
| **Hyperscale** | 2-128 vCore | Distributed page server | up to 4 read replicas, 100TB storage |

Trong ba tier vCore, hai tier đầu (General Purpose, Business Critical) là quen thuộc; riêng Hyperscale là một kiến trúc khác hẳn, đáng tách ra nói riêng.

#### Hyperscale — Azure exclusive

Hyperscale tách hẳn lớp lưu trữ ra khỏi lớp compute. Nhờ vậy nó scale tới **100 TB**, snapshot dưới 1 phút, và scale compute lên/xuống chỉ trong vài giây — những thứ kiến trúc SQL Database truyền thống (compute gắn cứng với đĩa local) không làm được. Sơ đồ dưới so sánh hai kiến trúc cạnh nhau:

```text
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

Vì tách được storage khỏi compute, Hyperscale hợp với những DB to phình theo thời gian: OLTP cỡ lớn (e-commerce trên 10TB) hay workload analytics kiểu data warehouse.

#### Cost example (2026, southeastasia)

Lý thuyết tier là vậy, nhưng quyết định cuối cùng thường nằm ở hoá đơn. Đây là vài mức giá tham khảo ở region southeastasia để bạn có cảm giác về khoảng cách giữa các tier:

```text
Standard S2 (50 DTU, 250GB):        ~$75/month
GP 2 vCore Gen5:                     ~$370/month
BC 2 vCore Gen5:                     ~$1000/month
Hyperscale 2 vCore 100GB:            ~$400/month + storage
```

Nhìn bảng giá dễ thấy vCore đắt hơn DTU, nhưng đừng quên một đòn bẩy quan trọng: **Azure Hybrid Benefit** — nếu bạn đã có sẵn license SQL Server, mang nó lên cloud sẽ giảm 30-55% chi phí compute, đủ để bù phần chênh lệch.

---

## 2️⃣ Azure SQL HA + DR

Chọn được tier rồi, câu hỏi tiếp theo là: khi một thành phần chết thì sao? Phần này đi từ HA *trong* một region (built-in, không cần làm gì) ra tới DR *cross-region* (phải tự dựng).

### Service tier HA built-in

Điểm dễ chịu của Azure SQL là HA trong region được gói sẵn theo tier — bạn không cấu hình gì, chỉ cần biết tier mình chọn đang được bảo vệ ra sao:

| Tier | HA option |
|---|---|
| Basic / Standard | Local replica (within DC) |
| Premium / Business Critical | AlwaysOn cluster 4 nodes, free read replica |
| General Purpose | Remote storage, standby compute |
| Hyperscale | Page servers replicated, instant failover |

Nhờ HA built-in này, Azure cam kết SLA **99.99-99.995%** mà bạn không phải dựng cluster thủ công. Nhưng HA built-in chỉ chống chọi sự cố *trong* một region — mất cả region thì cần lớp tiếp theo.

### Geo-replication (cross-region read replica)

Lớp đầu tiên để chống mất region là nhân bản DB sang một region khác. Lệnh dưới tạo một read replica của DB `orders` từ Singapore sang Tokyo:

```bash
# Tạo geo-replica từ Singapore → Tokyo
az sql db replica create \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --name orders \
    --partner-server sql-prod-jpe \
    --partner-resource-group rg-prod-data
```

Vài đặc tính cần nhớ về geo-replica: replication chạy bất đồng bộ với độ trễ thường dưới 5 giây, bản ở Tokyo là *read-only*, và muốn chuyển sang dùng nó khi sự cố thì phải failover thủ công trong portal. Chính cái "thủ công" đó là điểm yếu — và Failover Group sinh ra để bịt nó.

### Auto-failover Group (production recommended)

Failover Group đóng gói nhiều DB lại thành một nhóm, gắn vào một chính sách failover tự động, và quan trọng nhất là cho bạn một endpoint duy nhất. Lệnh dưới gom `orders`, `inventory`, `users` vào một group SEA ↔ JPE:

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

Điểm ăn tiền của Failover Group là cái connection string duy nhất (`fg-acmeshop-prod.database.windows.net`): app cứ trỏ vào đó, group tự resolve về primary đang sống. Khi primary "ốm" quá grace period, failover diễn ra tự động — với Business Critical, RPO dưới 5 giây và RTO dưới 1 phút. App không cần đổi config.

### PITR (Point-in-Time Restore)

HA và DR lo phần *hạ tầng* chết. Nhưng còn một loại tai nạn khác: dữ liệu bị xoá nhầm hoặc bị corrupt. Đó là lúc PITR vào cuộc — phục hồi DB về đúng một thời điểm trong quá khứ:

```bash
# Restore tới 1 thời điểm cụ thể
az sql db restore \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --name orders \
    --dest-name orders-restored \
    --time "2026-05-24T03:15:00"
```

Có ba con số đáng nhớ về PITR: retention mặc định là **7 ngày** (tăng được tới **35 ngày**); nếu cần lưu lâu hơn cho compliance thì bật Long-term retention (LTR) theo tuần/tháng/năm tới tận **10 năm**; và về chi phí, backup storage được miễn phí bằng đúng 100% dung lượng DB, chỉ phần vượt mới tính tiền.

---

## 3️⃣ Azure SQL Security

Dữ liệu sống được rồi thì phải kín. Phần này đi từ lớp mã hoá rộng nhất (cả DB) tới hẹp nhất (từng cột), rồi mới tới auth.

### TDE (Transparent Data Encryption) — default

Lớp mã hoá rộng nhất là TDE — mã hoá *at rest* toàn bộ DB bằng AES 256, và mặc định đã bật sẵn. Khác biệt duy nhất bạn cần quyết là ai giữ khoá: Microsoft giữ (service-managed key, mặc định) hay bạn tự giữ (customer-managed key qua Key Vault). Lệnh dưới chỉ để xác nhận/bật trạng thái:

```bash
az sql db tde set \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --database orders \
    --status Enabled
```

### CMK (Customer-Managed Key) for TDE

Khi compliance đòi *bạn* phải kiểm soát khoá (BYOK), bạn chuyển TDE sang dùng khoá nằm trong Key Vault của mình. Quy trình bốn bước: bật Managed Identity cho SQL Server, cấp quyền cho identity đó đọc khoá trong Key Vault, nạp khoá, rồi trỏ TDE vào khoá đó:

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

TDE mã hoá toàn bộ DB nhưng server vẫn thấy plaintext khi xử lý — nghĩa là DBA cũng thấy. Khi có những cột cực nhạy (SSN, số thẻ) mà *kể cả DBA cũng không được thấy*, bạn cần Always Encrypted: khoá nằm ở phía client driver, không bao giờ gửi lên server, nên server chỉ thấy ciphertext. Đây là lựa chọn cho các cột PII phải tuân HIPAA/PCI:

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

Nếu Always Encrypted là "giấu tuyệt đối", thì DDM là "che mắt cho gọn". DDM chỉ mask kết quả query theo role — server vẫn thấy plaintext nên kém an toàn hơn Always Encrypted, đổi lại cấu hình đơn giản hơn nhiều, hợp khi mục tiêu chỉ là tránh lộ dữ liệu cho người không cần thấy đầy đủ:

```sql
ALTER TABLE customers ALTER COLUMN email
ADD MASKED WITH (FUNCTION = 'email()');

-- User without UNMASK permission sees: aXXX@XXXX.com
```

### Microsoft Defender for SQL

Ngoài mã hoá, Azure còn có một lớp giám sát chủ động: Defender for SQL. Dịch vụ này lo vulnerability assessment và Advanced Threat Protection (phát hiện SQL injection, login bất thường...), với chi phí $15/server/tháng — một khoản nhỏ đáng bật cho production.

### Auth methods

Cuối cùng là chuyện *ai* được vào. Azure SQL hỗ trợ hai cách xác thực, và lựa chọn ở đây ảnh hưởng tới cả bảo mật lẫn trải nghiệm vận hành:

1. **SQL auth** — username/password (legacy, dùng cho app cũ).
2. **Entra ID auth** (recommended) — single sign-on, MFA, audit centralized.

Khuyến nghị 2026 là Entra ID auth, vì nó kéo theo SSO, MFA và audit tập trung. Lệnh dưới gán một group Entra ID làm admin cho server:

```bash
# Set Entra ID admin cho server
az sql server ad-admin create \
    --resource-group rg-prod-data \
    --server sql-prod-sea \
    --display-name "DBA Admins" \
    --object-id <group-objectid>
```

Sau khi có admin, client kết nối bằng Entra ID chỉ cần thêm cờ `-G`:

```sql
-- Connect via Entra ID
sqlcmd -S sql-prod-sea.database.windows.net -G -d orders
```

---

## 4️⃣ Cosmos DB — multi-API global NoSQL

Xong nửa bài toán quan hệ. Phần *session/cart* toàn cầu trong yêu cầu của sếp lại là một thế giới khác — và đó là sân của Cosmos DB.

🪞 **Ẩn dụ**: *Cosmos DB như **dịch vụ chuyển phát toàn cầu** — dữ liệu của bạn được nhân bản tới 30+ region trên thế giới; user ở Nhật đọc replica Tokyo, user ở Việt Nam đọc Singapore — latency <10ms khắp nơi. Bạn chọn **5 mức "trust" lá thư đến nhanh hay chậm** (consistency level) — strong = thư đến đúng thứ tự khắp nơi nhưng chậm; eventual = thư có thể đến lệch order nhưng nhanh nhất.*

### Cosmos DB là gì

Nói gọn, Cosmos DB là một NoSQL database được Azure quản hoàn toàn, với ba đặc tính định danh: **phân tán toàn cầu**, **đa API**, và **độ trễ một chữ số mili-giây**. Điểm khiến nó khác DynamoDB của AWS là chỗ "đa API": Cosmos cho bạn chọn một trong **5 API** quen thuộc, trong khi DynamoDB chỉ có API riêng của nó.

### 5 API options

Năm API này không phải năm sản phẩm khác nhau, mà là năm "giao diện" tương thích với các hệ NoSQL phổ biến — giúp bạn migrate app cũ sang Cosmos mà gần như không sửa code:

| API | Compatible với | Use case |
|---|---|---|
| **NoSQL API** (formerly SQL API) | JSON document, query SQL-like | Default cho new app, document store |
| **MongoDB API** | MongoDB driver wire protocol | Migrate MongoDB app |
| **Cassandra API** | Apache Cassandra CQL | Migrate Cassandra app |
| **Gremlin API** | Apache TinkerPop graph | Graph queries (social, fraud detect) |
| **Table API** | Azure Table Storage | Migrate from Azure Table |

Một điều khoá tay phải lưu trước khi tạo: mỗi account chỉ chọn **1 API và không đổi được sau đó**. App mới mà không có ràng buộc migrate thì cứ chọn **NoSQL API**.

### Hierarchy

Để biết RU/s và partition key gắn vào đâu, cần hình dung cấu trúc lồng nhau của Cosmos: account chứa nhiều database, database chứa nhiều container, và container mới là nơi document thật sự nằm (mỗi container có một partition key riêng):

```text
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

Trong cả Cosmos, không có quyết định nào ảnh hưởng nhiều bằng việc chọn partition key — đây là field dùng để shard dữ liệu ra các partition vật lý. Chọn đúng thì hệ scale mượt; chọn sai thì dữ liệu dồn cục, đọc/ghi nghẽn. Ba tiêu chí dưới là kim chỉ nam:

```text
Choose partition key:
  ✅ Cardinality cao (nhiều giá trị unique)
  ✅ Phân bố đều (không hot spot)
  ✅ Match query pattern (đa số query filter on this)

Bad: /country → 200 giá trị, "VN" chiếm 80% → hot partition
Good: /userId → triệu giá trị, đều
Good: /tenantId + /userId synthetic key
```

Lý do phải "suy nghĩ kỹ ngay ngày 1": đổi partition key về sau không phải sửa config, mà là *migrate toàn bộ dữ liệu* sang container mới — kèm downtime.

### RU/s — Request Unit per second

Cosmos không tính tiền theo CPU hay storage thuần, mà theo một đơn vị riêng tên RU (Request Unit): mỗi thao tác tiêu một lượng RU nhất định, và bạn trả tiền cho lượng RU/giây cấp cho container. Bảng ước lượng dưới giúp bạn cảm nhận chi phí tương đối của từng loại operation:

```text
Read 1KB doc by ID         = 1 RU
Read 1KB doc by query      = 2-3 RU (with index)
Write 1KB doc              = 5-10 RU
Delete 1KB doc             = 5 RU
Query 100 docs             = 20-50 RU
```

Có ba cách cấp RU, khác nhau ở chỗ bạn cam kết trước bao nhiêu và linh hoạt tới đâu.

#### Provisioned throughput

Cách cổ điển: bạn cấp cứng một mức RU/s và trả tiền cho mức đó dù dùng hay không. Lệnh dưới tạo container `sessions` với 1000 RU/s:

```bash
# Tạo container với 1000 RU/s
az cosmosdb sql container create \
    --account-name cosmos-acmeshop-prod \
    --database-name shopdb \
    --name sessions \
    --partition-key-path /userId \
    --throughput 1000
```

Giá tham khảo: khoảng $0.008 cho mỗi 100 RU mỗi giờ, tức ~$58/tháng cho mỗi 1000 RU/s cấp cứng.

#### Autoscale

Nếu traffic lên xuống thất thường, cấp cứng dễ bị thiếu lúc cao điểm và thừa lúc vắng. Autoscale giải bài này: bạn chỉ đặt mức *trần*, hệ tự co giãn từ 10% tới 100% của trần đó theo tải. Lệnh dưới đặt trần 4000 RU/s (tức dải tự co giãn 400-4000 RU/s):

```bash
az cosmosdb sql container create \
    --account-name cosmos-acmeshop-prod \
    --database-name shopdb \
    --name sessions \
    --partition-key-path /userId \
    --max-throughput 4000
```

Chi phí của autoscale tính theo mức tiêu thụ cao nhất trong từng giờ, đắt hơn provisioned khoảng 1.5 lần, nhưng đổi lại sự linh hoạt và khỏi lo throttle lúc spike.

#### Serverless

Cực kia của phổ là serverless: không cấp trước gì cả, chỉ trả tiền theo từng request thực tế. Đặt chế độ này lúc tạo account:

```bash
# Cosmos DB account serverless (set on account create)
az cosmosdb create \
    --name cosmos-acmeshop-dev \
    --resource-group rg-dev-data \
    --capabilities EnableServerless
```

Serverless tính rất rẻ ở mức request thấp (5 RU ≈ $0.000026), lại có Free Tier vĩnh viễn 1000 RU/s + 25 GB, nên hợp nhất cho dev/sandbox hoặc workload có lưu lượng khó đoán.

---

## 5️⃣ Consistency levels — 5 mức

Phân tán toàn cầu kéo theo một câu hỏi nan giải: khi ghi ở Singapore, user ở Tokyo có đọc thấy ngay không? Cosmos không ép bạn chọn cực đoan "luôn thấy ngay" hay "kệ trễ bao lâu cũng được", mà cho cả một dải 5 mức để đánh đổi giữa độ nhất quán và độ trễ.

🪞 **Ẩn dụ tiếp**: *Strong = thư bảo đảm — ai cũng đọc cùng nội dung mới nhất, chậm; Eventual = bưu thiếp — nhanh nhưng có thể lệch order; 3 mức giữa là trade-off.*

Bảng dưới xếp 5 mức từ nhất quán nhất (chậm nhất) xuống lỏng nhất (nhanh nhất), kèm tình huống điển hình cho từng mức:

| Level | Mô tả | Latency | Use case |
|---|---|---|---|
| **Strong** | Linearizable — đọc luôn thấy write mới nhất | Cao nhất | Banking, leaderboard real-time |
| **Bounded Staleness** | Lag bound theo K version hoặc T thời gian | Trung bình | Status feed, "đã đọc" cuối cùng < 5 phút |
| **Session** (default) | Within session: strong; cross-session: eventual | Thấp | Default — user-centric app |
| **Consistent Prefix** | Đọc thấy đúng thứ tự, nhưng có thể lag | Thấp | Chat order, comment |
| **Eventual** | Cuối cùng converge, không guarantee order | Thấp nhất | Counter, like, view count |

Mức mặc định là **Session**, và đó cũng là lựa chọn hợp lý cho đa số app web/mobile: trong cùng một phiên người dùng thì nhất quán tuyệt đối (đọc thấy ngay thứ mình vừa ghi), còn giữa các phiên khác nhau thì chấp nhận eventual.

### Set level

Mức consistency mặc định được đặt ở cấp account lúc tạo:

```bash
az cosmosdb create \
    --name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --default-consistency-level Session
```

Khi một operation cụ thể cần chặt hơn mặc định, bạn override ngay tại request đó — ví dụ đọc một item với Strong:

```python
from azure.cosmos import CosmosClient, ConsistencyLevel

client.read_item(item="u-001", partition_key="u-001",
                 consistency_level=ConsistencyLevel.Strong)
```

---

## 6️⃣ Multi-region writes (active-active)

Mặc định, Cosmos cho đọc ở nhiều region nhưng chỉ ghi ở một. Phần này giải thích vì sao mặc định như vậy, và khi nào nên mở khoá ghi đa region.

### Single-region write (default)

Ở chế độ mặc định, một region làm "region ghi", các region còn lại chỉ là read replica:

```text
1 region = write region (Singapore)
N region = read replica (Tokyo, London, ...)
```

Hệ quả: user ở Tokyo đọc thì nhanh (lấy từ replica local), nhưng mỗi lần *ghi* lại phải gửi ngược về Singapore — chậm. Với app ghi nhiều và phân tán toàn cầu, độ trễ ghi này là điểm đau.

### Multi-region writes

Bật multi-region writes cho phép user ghi vào region gần nhất, không phải vòng về một region trung tâm:

```bash
az cosmosdb update \
    --name cosmos-acmeshop-prod \
    --resource-group rg-prod-data \
    --locations regionName=southeastasia failoverPriority=0 isZoneRedundant=False \
    --locations regionName=japaneast failoverPriority=1 isZoneRedundant=False \
    --enable-multiple-write-locations true
```

Đổi lại tốc độ ghi local là chi phí: chế độ này tốn gấp khoảng 2 lần, vì hệ phải có cơ chế hợp nhất (CRDT-like merge) khi hai region ghi cùng một bản ghi gần như đồng thời. Và cái "ghi cùng lúc" đó dẫn thẳng tới bài toán conflict.

### Conflict resolution

Khi hai region cùng sửa một document, Cosmos cần một luật để quyết ai thắng. Có hai cách:

- **Last Write Wins** (LWW, default) — based on `_ts` (timestamp).
- **Custom merge function** — stored procedure on conflict.

Tóm lại, multi-region writes đáng dùng cho workload ghi dày và toàn cầu (chat, IoT, gaming), nhưng phải cẩn thận với tính toàn vẹn dữ liệu — vì conflict là chuyện xảy ra thật, không phải lý thuyết.

---

## 7️⃣ Decision matrix — DB nào cho workload nào

Đã đi qua cả Azure SQL lẫn Cosmos, giờ là lúc lùi lại nhìn toàn cảnh. Azure còn nhiều database khác ngoài hai cái chính của bài, và bảng dưới gom lại để bạn biết khi gặp một workload thì nên trỏ tay vào đâu:

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

Rút thành một câu để nhớ: mặc định **SQL** cho dữ liệu quan hệ, **Cosmos** cho NoSQL toàn cầu, **Synapse** cho OLAP, và **Redis** cho cache.

---

## 🛠️ Hands-on — Stack Azure SQL + Cosmos cho Acme Shop

### Mục tiêu

Giờ ráp toàn bộ lý thuyết thành một stack chạy thật theo đúng yêu cầu của sếp ở đầu bài: deploy Azure SQL Database (orders) + Cosmos DB (user sessions), test failover SQL, và test multi-region read trên Cosmos. Tám bước, đi từ tạo hạ tầng SQL tới Cosmos rồi kiểm chứng failover.

### Bước 1 — Azure SQL Database

Bắt đầu bằng resource group và một SQL Server *logical* (lưu ý: đây là server quản lý logic, không phải VM). Ta tắt luôn public network ngay từ đầu để buộc dùng Private Endpoint về sau:

```bash
az group create --name rg-prod-data --location southeastasia

# SQL Server (logical, không phải VM) — tắt public network ngay từ đầu
az sql server create \
    --name sql-acmeshop-prod-sea \
    --resource-group rg-prod-data \
    --location southeastasia \
    --admin-user sqladmin \
    --admin-password 'Strong-Password-123!' \
    --enable-public-network Disabled

# (Public đã tắt; sẽ dùng Private Endpoint trong VNet — xem pitfall #10)

# Firewall: allow Azure services + my IP
MY_IP=$(curl -s ifconfig.me)
az sql server firewall-rule create \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --name AllowMyIP \
    --start-ip-address $MY_IP --end-ip-address $MY_IP

# Database — General Purpose 2 vCore, backup Geo ngay từ đầu
az sql db create \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --name orders \
    --edition GeneralPurpose \
    --family Gen5 \
    --capacity 2 \
    --backup-storage-redundancy Geo \
    --zone-redundant false
```

> ⚠️ `--enable-public-network` nhận giá trị `Enabled`/`Disabled` (không phải `true`/`false`). Và `--backup-storage-redundancy` nên đặt đúng từ lúc `create` — đổi redundancy sau khi DB đã tạo bị Azure hạn chế, nên ở đây ta set thẳng `Geo` (backup cross-region) ngay bước này thay vì update về sau.

### Bước 2 — Bật PITR 35 ngày + kiểm tra TDE

Bước 1 đã chốt backup redundancy ở mức `Geo`. Việc còn lại của bước này là kéo dài retention PITR lên 35 ngày và xác nhận TDE đang bật (TDE mặc định đã on, ta chỉ kiểm tra):

```bash
# Set short-term retention 35 days (PITR)
az sql db short-term-retention-policy set \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --database orders \
    --retention-days 35

# TDE default already on — chỉ verify
az sql db tde show \
    --resource-group rg-prod-data \
    --server sql-acmeshop-prod-sea \
    --database orders
```

### Bước 3 — Geo-replica + Failover Group

Có DB primary ở Singapore rồi, giờ dựng lớp DR cross-region: tạo một SQL Server thứ hai ở Tokyo, rồi gom DB `orders` vào một Failover Group để có endpoint duy nhất và failover tự động:

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

Hạ tầng SQL đã xong; giờ kết nối qua endpoint của Failover Group và tạo bảng `orders` để có dữ liệu thật mà test:

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

Xong nửa SQL, chuyển sang nửa Cosmos. Tạo một account trải hai region với multi-region writes bật sẵn (cho session/cart ghi local), rồi thêm database và container `sessions` partition theo `/userId`:

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

Có container rồi, ta dùng SDK Python để ghi một session và đọc lại. Lưu ý cách query *có* filter theo partition key (`/userId`) — đây là điểm tối quan trọng để query rẻ, sẽ nói kỹ ở pitfall #5:

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

Trước khi chạy script, identity của bạn cần quyền *data plane* trên Cosmos (RBAC quản lý khác hẳn với quyền đọc/ghi dữ liệu). Cấp role rồi cài SDK và chạy:

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

Đây là phần kiểm chứng cái đắt giá nhất ta vừa dựng: HA cross-region. Ép failover thủ công sang Tokyo, rồi xác nhận chính connection string cũ vẫn hoạt động — vì Failover Group tự resolve sang primary mới:

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

Lab xong thì dọn sạch để khỏi tốn tiền — xoá nguyên resource group là gọn nhất:

```bash
az group delete --name rg-prod-data --yes --no-wait
```

Kết quả của cả hands-on: SQL geo-replicated SEA ↔ JPE, Cosmos multi-region write trên 2 region, PITR 35 ngày — một stack đúng yêu cầu của sếp, chạy end-to-end.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Chọn DTU thay vì vCore cho new project

**Bẫy**: Pick DTU vì rẻ → khó tune, không có Hyperscale option, không Hybrid Benefit.

**Fix**: 2026 luôn vCore. Hybrid Benefit nếu có license SQL Server.

### 2. Backup storage = LRS mặc định

**Bẫy**: SQL Database backup default LRS → mất cả region → mất backup.

**Fix**: `--backup-storage-redundancy Geo` hoặc `Zone` (production). Đặt **ngay lúc create** — đổi redundancy sau khi DB đã tạo bị hạn chế.

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
- `--enable-public-network Disabled`.
- Private Endpoint trong VNet.
- Hoặc deny all + allow specific IP.

---

## 🧠 Tự kiểm tra (Self-check)

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

## ⚡ Tra cứu nhanh (Cheatsheet)

Phần tra nhanh cho lúc làm việc thật — gom theo nhóm: tạo SQL Database, HA/DR, security, rồi tới Cosmos (account/container/throughput).

```bash
# === Azure SQL Database ===
# Tạo server + DB (vCore General Purpose)
az sql server create -n <server> -g <rg> -l <region> \
    --admin-user <user> --admin-password '<pass>' --enable-public-network Disabled
az sql db create -g <rg> -s <server> -n <db> \
    --edition GeneralPurpose --family Gen5 --capacity 2 --backup-storage-redundancy Geo

# === HA / DR ===
az sql db replica create -g <rg> -s <server> -n <db> --partner-server <server2>
az sql failover-group create -n <fg> -g <rg> -s <server> \
    --partner-server <server2> --add-db <db> --failover-policy Automatic --grace-period 1
az sql db short-term-retention-policy set -g <rg> -s <server> -d <db> --retention-days 35
az sql db restore -g <rg> -s <server> -n <db> --dest-name <db>-restored --time "<ISO8601>"

# === Security ===
az sql db tde set -g <rg> -s <server> --database <db> --status Enabled
az sql server ad-admin create -g <rg> -s <server> --display-name "<group>" --object-id <oid>

# === Cosmos DB ===
az cosmosdb create -n <acct> -g <rg> --default-consistency-level Session \
    --locations regionName=southeastasia failoverPriority=0 isZoneRedundant=False
az cosmosdb sql database create --account-name <acct> -g <rg> --name <db>
# Provisioned vs Autoscale
az cosmosdb sql container create --account-name <acct> --database-name <db> -g <rg> \
    --name <container> --partition-key-path /userId --throughput 1000
az cosmosdb sql container create --account-name <acct> --database-name <db> -g <rg> \
    --name <container> --partition-key-path /userId --max-throughput 4000
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Azure SQL Database** | CSDL SQL dạng PaaS | PaaS SQL Server đơn database hoặc elastic pool |
| **Managed Instance** | Instance được quản lý | PaaS SQL Server full instance, gần 100% compat |
| **DTU** | Đơn vị giao dịch DB | Database Transaction Unit — purchasing model cũ |
| **vCore** | Lõi ảo | Virtual core — purchasing model hiện đại |
| **GP / BC / Hyperscale** | Các service tier vCore | General Purpose / Business Critical / Hyperscale |
| **Hyperscale** | Tier scale-out | 100 TB storage, instant scale, snapshot < 1 phút |
| **PITR** | Khôi phục theo thời điểm | Point-in-Time Restore |
| **LTR** | Lưu trữ dài hạn | Long-Term Retention (tới 10 năm) |
| **TDE** | Mã hoá dữ liệu trong suốt | Transparent Data Encryption (at-rest) |
| **CMK** | Khoá do khách quản | Customer-Managed Key |
| **Always Encrypted** | Mã hoá cấp cột | Encrypt từng cột, khoá nằm tại client |
| **DDM** | Che dữ liệu động | Dynamic Data Masking |
| **Failover Group** | Nhóm chuyển đổi dự phòng | Group DB + chính sách auto-failover |
| **Cosmos DB** | CSDL NoSQL toàn cầu | NoSQL global, multi-API |
| **NoSQL API** | API NoSQL (tên mới) | Tên mới của SQL API (JSON document) |
| **RU/s** | Đơn vị request mỗi giây | Request Unit per second — pricing model |
| **Partition key** | Khoá phân vùng | Field dùng để shard dữ liệu |
| **Consistency level** | Mức nhất quán | 5 mức trade-off latency vs consistency |
| **Session consistency** | Nhất quán theo phiên | Default — trong phiên strong, ngoài phiên eventual |
| **Multi-region writes** | Ghi đa region | Write ở bất kỳ region, replicate toàn cầu |
| **LWW** | Ghi sau thắng | Last Write Wins — conflict resolution mặc định |
| **Autoscale** | Tự co giãn throughput | RU/s tự scale trong dải 10%–100% của max (vd max 4000 → 400-4000 RU/s) |
| **Serverless** | Trả theo request | Pay-per-request, không có min throughput |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Azure Blob Storage + RBAC](02_blob-storage-and-rbac.md)
- ➡️ **Bài tiếp theo:** [Azure Functions + App Service + Container Apps](04_functions-and-app-service.md)
- ↑ **Về cụm:** [Azure — Microsoft Cloud Platform](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS RDS + DynamoDB](../../../aws/lessons/01_basic/03_rds-and-dynamodb.md) — bản tương đương trên AWS
- ☁️ [GCP Cloud SQL + Firestore](../../../gcp/lessons/01_basic/03_cloud-sql-and-firestore.md) — bản tương đương trên GCP
- 📚 [Nền tảng Databases](../../../../06_databases/) — SQL vs NoSQL từ gốc
- 🏗️ [Terraform cho hạ tầng](../../../../10_devops/iac/) — quản lý SQL/Cosmos bằng IaC

### 🌐 Tài nguyên tham khảo khác

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

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bài 03 cluster Azure basic. Azure SQL Database/Managed Instance/SQL VM + DTU vs vCore + GP/BC/Hyperscale + geo-replication + Failover Group + PITR/LTR + TDE/Always Encrypted/DDM + Cosmos DB 5 API + 5 consistency level + multi-region writes + RU/s + decision matrix + hands-on stack SQL+Cosmos + 10 pitfalls. Mirror AWS RDS+DynamoDB lesson.
- **v2.0.0 (01/06/2026)** — Viết lại prose từ kiểu "điện tín" sang narrative tiếng Việt: thêm lời dẫn trước mỗi bảng/code/list + câu phân tích sau + câu bắc cầu giữa các section, giữ nguyên 100% code/số liệu/diagram. Chuẩn hoá heading framework + Glossary 3 cột + nav (marker ⬅️/➡️/↑, link-text = tiêu đề thực, thêm Cheatsheet). Việt hoá field metadata "Yêu cầu trước". Sửa lỗi kỹ thuật: `--enable-public-network` nhận `Disabled` (không phải `false`); set `--backup-storage-redundancy Geo` ngay lúc create thay vì update Zone→Geo về sau (đổi redundancy sau create bị hạn chế); làm rõ Glossary Autoscale "dải 10%–100% của max". Thêm fence ngôn ngữ `text` cho block ASCII/output.
