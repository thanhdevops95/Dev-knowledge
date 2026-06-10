# 📦 Azure Blob Storage + RBAC

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [01_virtual-machines-and-disks](01_virtual-machines-and-disks.md) ✅, hiểu RBAC concept cơ bản

> 🎯 *Nếu bạn từng làm việc với AWS S3 hay Google Cloud Storage (GCS), thì Blob Storage chính là dịch vụ lưu trữ object tương đương trên Azure. Điểm khác biệt là Azure xếp mọi thứ theo 3 tầng: **Storage Account** (cấp cao nhất) chứa nhiều **Container** (tương đương bucket), và mỗi container chứa nhiều **Blob** (object). Bài này đi qua từng phần: các loại storage account, access tier (Hot/Cool/Cold/Archive), lifecycle policy tự động dời tầng, **SAS token** (signed URL có thời hạn), **RBAC + ABAC** cho data plane, firewall cho storage account, **mã hoá CMK với Key Vault**, và cuối cùng là static website + **Azure Front Door** CDN.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Storage Account types** (general v2 / Premium block/file/page)
- [ ] Hiểu **Container** + **Blob** (block/append/page) + **access tier** (Hot/Cool/Cold/Archive)
- [ ] Setup **Lifecycle Management** auto-tier + delete
- [ ] Tạo **SAS token** (User Delegation SAS — best) cho signed URL
- [ ] Phân biệt **Shared Key auth** vs **Entra ID auth** vs **SAS**
- [ ] Setup **RBAC data plane** (`Storage Blob Data Reader/Contributor/Owner`)
- [ ] Storage Account **firewall + private endpoint**
- [ ] **CMK** (Customer-Managed Key) với Key Vault
- [ ] **Static website hosting** + **Azure Front Door** CDN
- [ ] Hands-on: image upload signed URL → resize trigger Functions (preview)

---

## Tình huống — Acme Shop image storage + CDN

Hãy bắt đầu từ một yêu cầu rất quen với bất kỳ ai làm web thương mại điện tử. Acme Shop đang chứa toàn bộ ảnh sản phẩm trên ổ đĩa máy chủ on-prem, web càng nhiều ảnh thì server càng nghẽn. Sếp giao cho bạn nguyên một bài toán di trú lên cloud:

> *"Migrate 500GB ảnh sản phẩm từ on-prem lên Azure Blob. Web upload bằng signed URL (đừng route ảnh qua server). Static site landing ở `shop.acmeshop.vn` qua Blob + Front Door CDN. Ảnh cũ > 90 ngày auto move sang Cold tier (rẻ hơn 50%). Bucket KHÔNG được public. Mã hóa CMK với Key Vault."*

Nghe thì gọn một câu, nhưng để làm đúng và an toàn, bạn cần dựng được từng mảnh ghép sau:

- **Storage Account** General v2 LRS.
- **Container** `product-images` private, RBAC data plane.
- **Lifecycle** auto Hot → Cool sau 30 ngày → Cold sau 90 → Archive sau 365 → Delete sau 7 năm.
- **User Delegation SAS** cho upload từ frontend.
- **Static website** ở container `$web`.
- **Front Door** CDN + WAF + custom domain.
- **CMK** với Key Vault HSM.

Phần còn lại của bài sẽ đi qua từng mảnh ghép này theo thứ tự, rồi gói tất cả lại trong phần hands-on cuối bài.

---

## 1️⃣ Storage Account — cấu trúc

Trước khi đụng tới blob, cần hiểu cái "khung" chứa nó. Storage Account là đơn vị cao nhất trong Azure Storage — bạn không tạo blob trực tiếp được, mà phải tạo account trước rồi mới tạo container và blob bên trong. Account cũng chính là nơi gắn firewall, chìa khoá mã hoá và logging.

🪞 **Ẩn dụ**: *Storage Account như **chung cư 1 tòa nhà** — có 1 địa chỉ duy nhất (`stacmeprodlogs.blob.core.windows.net`); bên trong chia **4 tầng** (Blob/Files/Queue/Table); mỗi tầng có nhiều **căn hộ** (Container/FileShare); mỗi căn hộ chứa nhiều **đồ đạc** (Blob/File). Tòa nhà có firewall, có chìa khóa, có camera (logging).*

### Hierarchy

Sơ đồ dưới cho thấy một storage account thực tế chia ra sao — bạn sẽ thấy 4 dịch vụ (Blob/Files/Queue/Table) cùng sống chung dưới một cái tên, và container đặc biệt `$web` chính là nơi static website nằm (sẽ dùng ở phần 7):

```
Storage Account: stacmeprodsea
├── Blob service (blob.core.windows.net)
│   ├── Container: product-images
│   │   ├── Blob: sku-001.jpg
│   │   └── Blob: sku-002.jpg
│   ├── Container: logs
│   └── Container: $web (special — static website)
├── File service (file.core.windows.net)
│   └── File Share: shared-files
├── Queue service (queue.core.windows.net)
│   └── Queue: orders
└── Table service (table.core.windows.net)
    └── Table: users
```

Bài này tập trung vào nhánh Blob, nhưng nhớ rằng 3 nhánh còn lại cũng nằm chung account.

### Storage Account types

Khi tạo account, câu hỏi đầu tiên Azure hỏi là "kind/type" nào. Đây không phải lựa chọn để cho có — nó quyết định bạn dùng được những access tier nào và mức latency ra sao. Bảng dưới gom các loại đang còn dùng năm 2026:

| Type | Performance | Use case |
|---|---|---|
| **General-purpose v2 (GPv2)** | Standard | **Default** — Blob + Files + Queue + Table, all access tiers |
| **General-purpose v1 (GPv1)** | Standard | Legacy — không dùng nữa |
| **Premium block blob** | Premium SSD | Low latency blob (high TPS, transactional workload) |
| **Premium page blob** | Premium SSD | VM disk (legacy unmanaged) |
| **Premium file shares** | Premium SSD | High-perf SMB/NFS shares |
| **Block blob storage** | Premium | Đã merged vào Premium block blob |

Tóm lại cho thực tế: cứ chọn **GPv2 Standard** cho khoảng 95% workload (đây cũng là default 2026). Chỉ khi cần latency cực thấp và throughput rất cao — real-time analytics, IoT high TPS — mới cân nhắc Premium block blob.

### Replication (data redundancy)

Tạo xong account, câu hỏi tiếp theo là dữ liệu được nhân bản đi đâu. Đây là yếu tố quyết định bạn chịu được mất mát tới mức nào: mất 1 datacenter, mất 1 availability zone, hay mất cả 1 region. Càng nhiều bản sao thì độ bền (durability) càng cao nhưng giá cũng tăng theo:

| Type | Copies | Region | Durability (năm) |
|---|---|---|---|
| **LRS** (Locally Redundant) | 3 copies | 1 datacenter | 99.999999999% (11 nines) |
| **ZRS** (Zone Redundant) | 3 copies across 3 AZ | 1 region (cross zone) | 99.9999999999% (12 nines) |
| **GRS** (Geo Redundant) | 3 LRS + 3 LRS ở region pair | 2 regions | 99.99999999999999% (16 nines) |
| **GZRS** (Geo Zone Redundant) | 3 ZRS + 3 LRS ở region pair | 2 regions | 99.99999999999999% (16 nines) |
| **RA-GRS** | GRS + read-only secondary endpoint | 2 regions, read both | (same) |
| **RA-GZRS** | GZRS + read-only secondary | (same) | (same) |

Lưu ý cột cuối là **durability theo năm** (xác suất giữ được dữ liệu), không phải SLA availability (xác suất truy cập được) — hai con số khác nhau. Về lựa chọn thực tế: production nên dùng **ZRS** (HA trong cùng region) hoặc **GZRS** (DR cross-region khi cần chịu mất nguyên region). LRS chỉ nên để cho dev/sandbox vì chỉ có 1 datacenter.

### Naming rule (đặc biệt!)

Có một điểm hay làm người mới vấp ngay khi tạo account: tên storage account bị ràng buộc rất chặt, khác hẳn cách đặt tên resource thông thường của Azure. Quy tắc như sau:

```
Storage Account name:
  - 3-24 ký tự
  - lowercase + digit ONLY (không gạch, không dấu chấm, không hoa)
  - GLOBALLY UNIQUE (giống S3 bucket)
  - Endpoint: <name>.blob.core.windows.net
```

Vì không cho phép dấu gạch, bạn buộc phải viết liền: `stacmeprodsea001`, `stacmedevimages` — chứ không thể dùng pattern quen thuộc kiểu `st-acme-prod-sea`. Quy ước phổ biến là prefix `st` + tên project + môi trường + region viết tắt, tất cả dính liền.

---

## 2️⃣ Blob types + Access tier

Có account và container rồi, giờ tới chính bản thân blob. Có hai quyết định bạn phải nắm: **loại blob** (quyết định cách ghi dữ liệu) và **access tier** (quyết định trade-off giữa giá lưu trữ và giá đọc).

### Blob types

Azure không coi mọi object như nhau — tuỳ cách bạn ghi mà chọn loại blob phù hợp. Đa số trường hợp bạn chỉ cần loại đầu tiên, nhưng biết cả ba giúp tránh chọn sai khi gặp log hay VM disk:

| Type | Mục đích | Max size | Random access |
|---|---|---|---|
| **Block blob** | File thông thường (image, video, doc, log) | 4.75 TiB | Append chỉ |
| **Append blob** | Log file (chỉ append) | 195 GiB | No |
| **Page blob** | VM disk, random read/write | 8 TiB | Yes |

Trong bài toán ảnh sản phẩm của Acme, ta dùng **Block blob** — đây cũng là loại mặc định cho khoảng 99% trường hợp.

### Access tier (chỉ cho Block blob)

Đây là cơ chế tiết kiệm tiền cốt lõi của Blob Storage. Ý tưởng đơn giản: ảnh sản phẩm mới đăng được xem mỗi ngày, còn ảnh từ 2 năm trước thì gần như không ai mở. Vậy tại sao phải trả tiền lưu trữ như nhau? Access tier cho phép xếp blob vào các "tầng" với giá lưu trữ khác nhau — đổi lại, tầng càng rẻ thì giá đọc càng đắt và phải giữ tối thiểu một số ngày:

| Tier | Storage cost | Read cost | Min retention | Use case |
|---|---|---|---|---|
| **Hot** | $$$ | $ | None | Active access, daily read/write |
| **Cool** | $$ | $$ | 30 ngày | Infrequent access, monthly read |
| **Cold** | $ | $$$ | 90 ngày | Rare access, backup tier 2 |
| **Archive** | $ (lowest) | $$$$ + rehydrate 1-15h | 180 ngày | Long-term archive, compliance |

Để thấy con số cụ thể, đây là giá lưu trữ thực tế (US East, 2026) — chênh lệch giữa Hot và Archive lên tới gần 20 lần:

```
Cost example (US East, 2026, per GB/month):
  Hot     = $0.0184
  Cool    = $0.0100
  Cold    = $0.0036
  Archive = $0.00099
```

Một điểm tối quan trọng phải nhớ: **Archive không đọc trực tiếp được** — phải rehydrate (kích hoạt lại) 1-15 giờ mới truy cập được. Vì vậy tuyệt đối không dùng Archive cho dữ liệu user còn xem; nó chỉ hợp với log compliance hay backup tier 2.

### Lifecycle Management — auto-tier

Bạn sẽ không ngồi dời tay từng tầng cho 500GB ảnh. Lifecycle Management là policy cho Azure tự động chuyển tier và xoá blob theo tuổi đời. Policy viết dưới dạng JSON, mô tả đúng yêu cầu của sếp (Hot → Cool sau 30 ngày → Cold sau 90 → Archive sau 365 → xoá sau 7 năm):

```json
{
  "rules": [
    {
      "name": "ProductImages",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["product-images/"]
        },
        "actions": {
          "baseBlob": {
            "tierToCool":    { "daysAfterModificationGreaterThan": 30 },
            "tierToCold":    { "daysAfterModificationGreaterThan": 90 },
            "tierToArchive": { "daysAfterModificationGreaterThan": 365 },
            "delete":        { "daysAfterModificationGreaterThan": 2555 }
          }
        }
      }
    }
  ]
}
```

Áp policy này lên account bằng một lệnh CLI, trỏ tới file JSON vừa viết:

```bash
az storage account management-policy create \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --policy @lifecycle.json
```

Cơ chế đếm tuổi dựa trên `daysAfterModificationGreaterThan` (tính từ lần modify cuối, không phải lần tạo — điểm này hay gây nhầm, sẽ nói lại ở phần Cạm bẫy). Với dữ liệu "đuôi dài" ít được truy cập, lifecycle policy giúp tiết kiệm 70-90% chi phí lưu trữ.

---

## 3️⃣ Auth methods — Shared Key vs SAS vs Entra ID

Có dữ liệu rồi thì câu hỏi lớn tiếp theo là: ai được phép đọc/ghi, và chứng minh danh tính bằng cách nào? Azure có 3 cách auth, và chọn sai có thể biến cả account thành lỗ hổng bảo mật. Đây là phần dài nhất của bài, nên hãy đi từng cách một.

🪞 **Ẩn dụ**: *3 cách auth như **3 loại chìa khóa nhà** — Shared Key = chìa khóa master (mở mọi cửa, đưa ai cũng vào được — KHÔNG NÊN dùng); SAS token = vé thăm nhà có thời hạn (chỉ vài giờ, chỉ vào phòng nào); Entra ID = thẻ nhân viên (login Microsoft account, role-based — best practice 2026).*

### A. Shared Key (Account Key)

Đây là cách cũ nhất và cũng nguy hiểm nhất. Mỗi storage account có 2 account key — cầm key là toàn quyền với cả account. Đoạn dưới minh hoạ cách lấy key và dùng nó (lưu ý: không nên làm thế này trong production):

```bash
# Get account key (DON'T do this in production!)
KEY=$(az storage account keys list \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --query "[0].value" -o tsv)

# Use
az storage blob list \
    --account-name stacmeprodsea \
    --container-name product-images \
    --account-key $KEY
```

Vấn đề của Shared Key nằm ở chỗ nó "được ăn cả, ngã về không": dễ dùng và chạy mọi nơi, nhưng đổi lại là toàn quyền read + write + delete trên cả account, không revoke được cho từng người, và nếu key bị lộ thì coi như mất trắng dữ liệu.

Vì vậy best practice 2026 là **tắt hẳn** Shared Key access và buộc mọi truy cập qua Entra ID:

```bash
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --allow-shared-key-access false
```

### B. SAS (Shared Access Signature) — Signed URL

Khi cần cấp quyền tạm thời cho ai đó (ví dụ: frontend cần upload ảnh trực tiếp lên Storage mà không qua server), SAS là công cụ đúng. SAS tạo ra một URL có chữ ký, kèm thời hạn và phạm vi quyền hạn rõ ràng. Nhưng có 3 loại SAS với mức an toàn rất khác nhau:

| Loại | Mô tả | Best practice |
|---|---|---|
| **Account SAS** | Sign bằng account key, cover toàn account | Avoid (giống Shared Key) |
| **Service SAS** | Sign bằng account key, cover 1 service (Blob) | Avoid (vẫn cần account key) |
| **User Delegation SAS** | Sign bằng Entra ID token (no account key) | ✅ Best — revocable, audit |

Điểm mấu chốt: hai loại đầu vẫn ký bằng account key — nghĩa là vẫn dính tới chiếc "chìa khoá master" mà ta vừa khuyên tắt. Chỉ **User Delegation SAS** ký bằng Entra ID token, nên revoke được và để lại audit trail.

#### User Delegation SAS (recommended)

Đây là cách tạo signed URL đúng chuẩn. Bạn login bằng Entra ID, Azure cấp một "user delegation key", rồi SAS được ký bằng key đó (không đụng gì tới account key). Ví dụ dưới tạo SAS read-only cho đúng 1 blob, có hiệu lực 1 giờ:

```bash
# Get user delegation key (cần Entra ID auth)
az login

# Generate SAS cho 1 blob, valid 1 giờ, read-only
SAS=$(az storage blob generate-sas \
    --account-name stacmeprodsea \
    --container-name product-images \
    --name sku-001.jpg \
    --permissions r \
    --expiry "$(date -u -v+1H +%Y-%m-%dT%H:%MZ)" \
    --auth-mode login \
    --as-user \
    --https-only \
    --output tsv)

URL="https://stacmeprodsea.blob.core.windows.net/product-images/sku-001.jpg?$SAS"
curl $URL
```

Lưu ý `--expiry` ở đây dùng giá trị động `$(date -u -v+1H ...)` (cú pháp macOS — Linux dùng `date -u -d "+1 hour" +%Y-%m-%dT%H:%MZ`) để SAS luôn có hiệu lực 1 giờ kể từ lúc chạy, thay vì hard-code một timestamp cứng sẽ hết hạn ngay. Frontend nhận URL này rồi upload/download thẳng lên Storage, không cần proxy qua backend — đúng yêu cầu "đừng route ảnh qua server" của sếp.

#### SAS via SDK (Python)

Ngoài CLI, trong code ứng dụng bạn sẽ sinh SAS bằng SDK. Đoạn Python dưới làm đúng quy trình User Delegation: lấy credential từ Managed Identity hoặc `az login`, xin user delegation key (tối đa 7 ngày), rồi sinh SAS cho blob:

```python
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta

account_url = "https://stacmeprodsea.blob.core.windows.net"
credential = DefaultAzureCredential()  # Managed Identity / az login

client = BlobServiceClient(account_url, credential=credential)

# Get user delegation key (valid 7 days max)
user_delegation_key = client.get_user_delegation_key(
    key_start_time=datetime.utcnow(),
    key_expiry_time=datetime.utcnow() + timedelta(hours=1)
)

# Generate SAS
sas = generate_blob_sas(
    account_name="stacmeprodsea",
    container_name="product-images",
    blob_name="sku-001.jpg",
    user_delegation_key=user_delegation_key,
    permission=BlobSasPermissions(read=True, write=True),
    expiry=datetime.utcnow() + timedelta(hours=1),
    protocol="https"
)

upload_url = f"{account_url}/product-images/sku-001.jpg?{sas}"
```

### C. Entra ID auth (RBAC data plane) — best for app

Với app chạy bền (không phải cấp quyền tạm cho client bên ngoài), cách tốt nhất là để app tự xác thực bằng Entra ID thông qua RBAC. App không cầm key hay SAS gì cả — nó dùng identity của chính nó. Đoạn dưới cho thấy `DefaultAzureCredential` tự dò ra identity từ môi trường:

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()  # Auto-detect: env vars, Managed Identity, az login
client = BlobServiceClient(
    account_url="https://stacmeprodsea.blob.core.windows.net",
    credential=credential
)

container = client.get_container_client("product-images")
blob = container.get_blob_client("sku-001.jpg")
blob.upload_blob(b"image bytes", overwrite=True)
```

Khi app chạy trên VM hoặc AKS có gắn **Managed Identity**, nó tự lấy token Entra ID rồi gọi Blob — zero credential lưu trong code hay config. Đây là mô hình an toàn nhất và là đích đến nên hướng tới cho mọi app production.

---

## 4️⃣ RBAC + ABAC cho Blob data plane

Phần trên nói "RBAC" nhiều lần, giờ là lúc làm rõ nó hoạt động ra sao với Blob. Điều dễ gây bất ngờ nhất ở đây: Azure tách quyền quản lý account (control plane) khỏi quyền truy cập dữ liệu (data plane) — và hai cái này dùng role hoàn toàn khác nhau.

### Roles built-in (data plane)

Để đọc/ghi blob content, bạn cần đúng các role có chữ "Data" trong tên. Bảng dưới liệt kê các role data plane built-in cùng vài role control plane để đối chiếu:

| Role | Permission |
|---|---|
| `Storage Blob Data Owner` | Full data plane + POSIX ACL |
| `Storage Blob Data Contributor` | Read + Write + Delete |
| `Storage Blob Data Reader` | Read only |
| `Storage Account Contributor` | Quản lý account (control plane), **không** access data |
| `Reader` | Quản lý metadata only |

Đây là cái bẫy lớn nhất: có `Owner` hay `Contributor` ở cấp subscription **không** tự động cho bạn đọc blob — bạn vẫn nhận lỗi 403 cho tới khi được gán riêng một role data plane. Lệnh dưới gán quyền read cho một user, scope tới đúng container `product-images`:

```bash
# Grant data plane reader
az role assignment create \
    --assignee thien.le@acmeshop.vn \
    --role "Storage Blob Data Reader" \
    --scope "/subscriptions/<sub>/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodsea/blobServices/default/containers/product-images"
```

Scope có thể đặt ở cấp **container** (chặt, chỉ 1 container) hoặc cấp **storage account** (rộng, mọi container). Nguyên tắc least-privilege: scope càng hẹp càng an toàn.

### ABAC (Attribute-Based Access Control) — beyond RBAC

RBAC trả lời "ai được làm gì", nhưng đôi khi bạn cần thêm điều kiện "trong hoàn cảnh nào". ABAC chính là việc gắn thêm condition vào một RBAC role — ví dụ: chỉ cho user A read những blob có tag `Project=AcmeShop`. Condition được viết bằng cú pháp riêng trong RBAC condition builder của Portal:

```
Condition (in Azure Portal RBAC condition builder):

  (
    !(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'})
    OR
    @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs/tags:Project<$key_case_sensitive$>] StringEquals 'AcmeShop'
  )
```

ABAC rất mạnh nhưng cũng phức tạp, và năm 2026 vẫn còn ở mức preview cho một số scenario. Cứ để dành nó cho các use case compliance thật sự cần (ví dụ lọc dữ liệu PII), còn nhu cầu thường ngày thì RBAC là đủ.

### Anonymous public access (KHÔNG NÊN)

Có một "công tắc" cho phép bất kỳ ai trên Internet đọc blob ẩn danh — nghe tiện nhưng là lỗ hổng kinh điển. Best practice là tắt hẳn nó ở cấp account:

```bash
# Disable anonymous toàn account (best practice)
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --allow-blob-public-access false
```

Từ 2024 trở đi Azure mặc định block public access. Khi thực sự cần phục vụ nội dung công khai (như static site), cách đúng không phải mở public storage, mà là đặt Front Door phía trước và giữ storage private — sẽ làm ở phần 7.

---

## 5️⃣ Storage Account network — Firewall + Private Endpoint

Auth giải quyết "ai được phép", nhưng còn một lớp nữa: "truy cập từ đâu". Mặc định storage account mở ra Internet, ai cũng resolve được endpoint — auth vẫn bảo vệ, nhưng bề mặt tấn công (attack surface) là cả thế giới. Với dữ liệu nhạy cảm, ta muốn thu hẹp lại.

### Default: public endpoint

Mặc định, endpoint của account là một địa chỉ public mà bất kỳ ai cũng phân giải được:

```
https://stacmeprodsea.blob.core.windows.net  ← bất kỳ ai trên Internet đều resolve được
```

Auth (Entra ID/SAS) vẫn chặn truy cập trái phép, nhưng việc endpoint lộ ra public đồng nghĩa attack surface rộng — đó là lý do ta muốn thêm tường lửa.

### Storage Account firewall

Cách thu hẹp đầu tiên là firewall: mặc định từ chối tất cả, rồi chỉ cho phép đúng những VNet subnet hoặc IP mà bạn tin. Ba lệnh dưới lần lượt bật chế độ "deny all", cho phép một subnet, và cho phép một IP cụ thể:

```bash
# Default deny all
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --default-action Deny

# Allow VNet subnet
az storage account network-rule add \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --vnet-name vnet-prod \
    --subnet snet-web

# Allow specific IP
az storage account network-rule add \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --ip-address 203.0.113.5
```

### Private Endpoint (best practice production)

Firewall vẫn để traffic đi qua Internet (chỉ lọc nguồn). Để traffic hoàn toàn không ra Internet, ta dùng Private Endpoint — bản chất là tạo một NIC trong VNet, gán cho nó private IP, và mọi truy cập đi qua mạng nội bộ Azure. Chuỗi lệnh dưới tạo private endpoint cho blob service, kèm Private DNS Zone để phân giải tên về IP private:

```bash
# Tạo Private Endpoint cho blob service
az network private-endpoint create \
    --name pe-stacmeprodsea-blob \
    --resource-group rg-prod-data \
    --vnet-name vnet-prod \
    --subnet snet-pe \
    --private-connection-resource-id "/subscriptions/<sub>/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodsea" \
    --group-id blob \
    --connection-name pe-conn

# DNS: tự động resolve stacmeprodsea.blob.core.windows.net → IP private 10.0.x.x
# Cần Private DNS Zone privatelink.blob.core.windows.net
az network private-dns zone create \
    --resource-group rg-prod-data \
    --name privatelink.blob.core.windows.net

# Link zone vào VNet
az network private-dns link vnet create \
    --resource-group rg-prod-data \
    --zone-name privatelink.blob.core.windows.net \
    --name link-prod \
    --virtual-network vnet-prod \
    --registration-enabled false
```

Kết quả: app trong VNet gọi blob → DNS phân giải ra IP private → traffic chạy nội bộ Azure, không bao giờ ra Internet. Đây là lựa chọn bắt buộc cho dữ liệu PII hoặc dữ liệu chịu quy định (regulated data). Một lưu ý quan trọng: nếu quên bước Private DNS Zone, app vẫn resolve ra IP public — sẽ nói kỹ ở phần Cạm bẫy.

---

## 6️⃣ Encryption — CMK với Key Vault

Yêu cầu cuối về bảo mật của sếp là "mã hoá CMK với Key Vault". Trước hết cần biết: mọi blob trên Azure **luôn được mã hoá sẵn** — câu hỏi chỉ là ai giữ chìa khoá mã hoá.

### Encryption tại Rest (default)

Mặc định, Azure tự mã hoá mọi blob bằng PMK (Platform-Managed Key) — chuẩn AES-256, key do Microsoft tạo và quản lý. Bạn không phải làm gì cả, miễn phí và trong suốt. Nhược điểm duy nhất: bạn không kiểm soát được chìa khoá.

### CMK (Customer-Managed Key)

Khi cần tự nắm quyền rotate (xoay vòng) và revoke (thu hồi) chìa khoá — thường vì lý do compliance — bạn dùng CMK: tự cung cấp key qua Key Vault và bảo Storage dùng key đó để mã hoá. Quy trình 5 bước dưới đi từ tạo Key Vault → tạo key → bật identity cho Storage → cấp quyền → bật CMK:

```bash
# 1. Tạo Key Vault với purge protection (bắt buộc cho CMK)
az keyvault create \
    --name kv-acmeshop-prod \
    --resource-group rg-prod-data \
    --location southeastasia \
    --enable-purge-protection true \
    --enable-rbac-authorization true

# 2. Tạo Key
az keyvault key create \
    --vault-name kv-acmeshop-prod \
    --name storage-cmk \
    --kty RSA --size 2048

# 3. Bật Managed Identity cho Storage Account
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --identity-type SystemAssigned

# 4. Grant Storage Identity quyền key
STORAGE_PRINCIPAL=$(az storage account show -n stacmeprodsea -g rg-prod-data --query identity.principalId -o tsv)
az role assignment create \
    --assignee $STORAGE_PRINCIPAL \
    --role "Key Vault Crypto Service Encryption User" \
    --scope "/subscriptions/<sub>/resourceGroups/rg-prod-data/providers/Microsoft.KeyVault/vaults/kv-acmeshop-prod"

# 5. Bật CMK trên Storage
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --encryption-key-source Microsoft.Keyvault \
    --encryption-key-vault https://kv-acmeshop-prod.vault.azure.net \
    --encryption-key-name storage-cmk \
    --encryption-key-version ""
```

Sức mạnh của CMK nằm ở chỗ bạn cầm "công tắc": rotate key thì Storage tự mã hoá lại (không downtime), còn revoke key thì toàn bộ blob lập tức không đọc được nữa — đây chính là cơ chế kill-switch khi có sự cố bảo mật.

### HSM-backed key (top security)

Với những ngành đòi hỏi cao nhất, key có thể được sinh và giữ bên trong phần cứng HSM thật sự — chìa khoá không bao giờ rời khỏi hộp phần cứng:

- **Key Vault Premium** + **Managed HSM** → key sinh trong HSM hardware FIPS 140-2 Level 3.
- Cost: ~$5,000/tháng cho Managed HSM cluster (expensive).
- Use case: banking, healthcare, government.

Vì giá khá cao, HSM-backed key chỉ đáng dùng cho banking, healthcare hay government — phần lớn workload thường chỉ cần CMK với Key Vault chuẩn là đủ.

---

## 7️⃣ Static website + Front Door CDN

Mảnh ghép cuối là phục vụ trang landing `shop.acmeshop.vn` từ Blob, nhưng vẫn giữ storage private. Lời giải gồm hai phần: bật static website trên storage, rồi đặt Front Door phía trước làm CDN + cổng vào.

### Static website hosting

Blob Storage có thể serve HTML trực tiếp qua một container đặc biệt tên `$web`. Lệnh dưới bật tính năng này (chỉ định trang index và trang 404) rồi upload thư mục `dist` lên:

```bash
# Bật static website (tạo container $web)
az storage blob service-properties update \
    --account-name stacmeprodsea \
    --static-website \
    --404-document 404.html \
    --index-document index.html

# Upload site
az storage blob upload-batch \
    --account-name stacmeprodsea \
    --source ./dist \
    --destination '$web' \
    --auth-mode login

# Endpoint default
# https://stacmeprodsea.z23.web.core.windows.net  ← chậm, không CDN
```

Endpoint mặc định (`...web.core.windows.net`) chạy được nhưng chậm và không có CDN — không phù hợp cho production. Đó là lý do cần Front Door.

### Azure Front Door (Global CDN + WAF)

Front Door là L7 global accelerator: nó vừa là CDN (cache nội dung ở edge gần user), vừa là WAF (tường lửa ứng dụng), vừa lo HTTPS tự động cho custom domain. Chuỗi lệnh dưới dựng đủ một profile Front Door từ A đến Z — tạo profile, endpoint, origin group trỏ về static site, route, và cuối cùng gắn custom domain `shop.acmeshop.vn`:

```bash
# Tạo Front Door Standard
az afd profile create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --sku Standard_AzureFrontDoor

# Endpoint
az afd endpoint create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --endpoint-name shop-acmeshop \
    --enabled-state Enabled
# → shop-acmeshop-<hash>.z01.azurefd.net

# Origin group (backend)
az afd origin-group create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --origin-group-name og-static-web \
    --probe-request-type GET --probe-protocol Https --probe-interval-in-seconds 100 --probe-path /

az afd origin create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --origin-group-name og-static-web \
    --origin-name origin-static \
    --host-name stacmeprodsea.z23.web.core.windows.net \
    --origin-host-header stacmeprodsea.z23.web.core.windows.net \
    --priority 1 --weight 1000 --enabled-state Enabled --https-port 443

# Route
az afd route create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --endpoint-name shop-acmeshop \
    --route-name route-default \
    --origin-group og-static-web \
    --supported-protocols Https \
    --patterns-to-match "/*" \
    --forwarding-protocol HttpsOnly \
    --link-to-default-domain Enabled \
    --enable-caching true

# Custom domain shop.acmeshop.vn
az afd custom-domain create \
    --resource-group rg-prod-cdn \
    --profile-name afd-acmeshop \
    --custom-domain-name shop-acmeshop-vn \
    --host-name shop.acmeshop.vn \
    --certificate-type ManagedCertificate
```

Sau khi hoàn tất, Front Door tự cấp HTTPS cert, cache nội dung ở edge toàn cầu, và áp WAF rule built-in (chặn OWASP top 10, bot, geo-block). User truy cập `shop.acmeshop.vn` chạm vào edge gần nhất — nhanh và an toàn — trong khi storage phía sau vẫn private.

---

## 🛠️ Hands-on — Image upload pipeline

### Mục tiêu

Đến đây ta gom mọi mảnh ghép thành một pipeline chạy được. Mục tiêu: web upload ảnh qua **User Delegation SAS** trực tiếp lên Storage (không qua server), container giữ private, lifecycle tự động dời tier, và static site landing phục vụ qua Front Door.

### Bước 1 — Tạo Storage Account

Bắt đầu bằng resource group và một account dựng đúng best practice ngay từ đầu — tắt public access, tắt shared key, ép TLS 1.2, và mặc định deny network:

```bash
az group create --name rg-prod-data --location southeastasia

az storage account create \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --location southeastasia \
    --sku Standard_ZRS \
    --kind StorageV2 \
    --access-tier Hot \
    --allow-blob-public-access false \
    --allow-shared-key-access false \
    --min-tls-version TLS1_2 \
    --default-action Deny
```

### Bước 2 — Container + RBAC

Vì account đã `default-action Deny`, ta tạm mở IP của chính mình để thao tác được, rồi tạo container và gán role data plane cho user (nhớ phần 4: thiếu role này là 403):

```bash
# Tạm allow IP để tạo container
MY_IP=$(curl -s ifconfig.me)
az storage account network-rule add \
    --account-name stacmeprodsea --resource-group rg-prod-data --ip-address $MY_IP

# Tạo container
az storage container create \
    --account-name stacmeprodsea \
    --name product-images \
    --auth-mode login

# Gán quyền data plane cho user
USER_OBJID=$(az ad signed-in-user show --query id -o tsv)
az role assignment create \
    --assignee $USER_OBJID \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodsea"
```

### Bước 3 — Generate User Delegation SAS

Giờ viết một script Python nhỏ sinh SAS cho frontend upload. Script nhận tên blob từ tham số, xin user delegation key, rồi trả về URL upload có hiệu lực 10 phút với quyền write + create:

```python
# generate_sas.py
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import sys

account_url = "https://stacmeprodsea.blob.core.windows.net"
container = "product-images"
blob_name = sys.argv[1]

cred = DefaultAzureCredential()
client = BlobServiceClient(account_url, credential=cred)

udk = client.get_user_delegation_key(
    datetime.utcnow(), datetime.utcnow() + timedelta(hours=1)
)

sas = generate_blob_sas(
    account_name="stacmeprodsea",
    container_name=container,
    blob_name=blob_name,
    user_delegation_key=udk,
    permission=BlobSasPermissions(write=True, create=True),
    expiry=datetime.utcnow() + timedelta(minutes=10),
    protocol="https",
)
print(f"{account_url}/{container}/{blob_name}?{sas}")
```

Chạy script rồi dùng `curl` mô phỏng frontend upload thẳng lên Storage bằng URL vừa sinh:

```bash
pip install azure-identity azure-storage-blob
URL=$(python generate_sas.py sku-001.jpg)

# Upload từ frontend (curl mô phỏng)
curl -X PUT -H "x-ms-blob-type: BlockBlob" \
     --data-binary @local-image.jpg \
     "$URL"
```

### Bước 4 — Lifecycle policy

Áp policy auto-tier đã thiết kế ở phần 2 — ghi file JSON rồi tạo management policy:

```bash
cat > lifecycle.json <<'EOF'
{
  "rules": [{
    "name": "TierAndExpire",
    "enabled": true,
    "type": "Lifecycle",
    "definition": {
      "filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["product-images/"] },
      "actions": {
        "baseBlob": {
          "tierToCool":    { "daysAfterModificationGreaterThan": 30 },
          "tierToCold":    { "daysAfterModificationGreaterThan": 90 },
          "tierToArchive": { "daysAfterModificationGreaterThan": 365 },
          "delete":        { "daysAfterModificationGreaterThan": 2555 }
        }
      }
    }
  }]
}
EOF

az storage account management-policy create \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --policy @lifecycle.json
```

### Bước 5 — Static website + Front Door

Bật static website, upload trang index, rồi test endpoint mặc định trước (phần Front Door đầy đủ đã ở section 7, ở đây ta kiểm tra storage serve HTML đã):

```bash
# Bật static website
az storage blob service-properties update \
    --account-name stacmeprodsea \
    --static-website \
    --404-document 404.html \
    --index-document index.html

# Upload landing
echo "<h1>Acme Shop</h1>" > index.html
az storage blob upload \
    --account-name stacmeprodsea \
    --container-name '$web' \
    --name index.html \
    --file index.html \
    --auth-mode login

# (Front Door setup section 7 — phức tạp, hands-on test endpoint default trước)
WEB_URL=$(az storage account show -n stacmeprodsea -g rg-prod-data --query primaryEndpoints.web -o tsv)
echo $WEB_URL
curl $WEB_URL
```

### Bước 6 — Cleanup

Xoá nguyên resource group để không phát sinh chi phí sau khi thực hành xong:

```bash
az group delete --name rg-prod-data --yes --no-wait
```

Kết quả mong đợi: upload qua SAS thành công, container vẫn private, lifecycle policy đang active, và static site đã live.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Storage Account name conflict

**Bẫy**: Đặt `acme-prod-storage` → fail (dấu gạch không cho phép).

**Fix**: Lowercase + digit, max 24 ký tự, không gạch: `stacmeprodsea001`. Test trước: `az storage account check-name --name <name>`.

### 2. Account key leak trong app

**Bẫy**: Hardcode account key vào app code → push Git public → bot scan → DoS / data exfil.

**Fix**:
- **Disable Shared Key**: `allow-shared-key-access false`.
- Dùng **Managed Identity** + RBAC.
- Quét pre-commit: `gitleaks`.
- Rotate key nếu nghi ngờ leak.

### 3. SAS token expiry quá dài

**Bẫy**: SAS valid 30 ngày → leak → 30 ngày bị abuse.

**Fix**:
- User Delegation SAS expiry **max 7 ngày**, nên set 1-2 giờ.
- Rotate user delegation key nếu nghi ngờ.
- SAS audit qua Storage Analytics log.

### 4. RBAC inheritance nhầm

**Bẫy**: User có `Contributor` subscription → tưởng read được blob → 403.

**Fix**:
- Data plane (Blob/File data) **cần role riêng**: `Storage Blob Data Reader/Contributor/Owner`.
- Control plane (account, container metadata) khác data plane (blob content).

### 5. Public access vẫn bật mặc định một số old storage

**Bẫy**: Storage Account tạo 2022 → `allow-blob-public-access=true` → ai cũng anonymously list được nếu container set Public.

**Fix**:
- Audit: `az storage account list --query "[?allowBlobPublicAccess].name"`.
- Disable: `--allow-blob-public-access false`.
- Use Defender for Cloud policy auto-enforce.

### 6. Archive tier rehydrate không phải instant

**Bẫy**: Move 1TB ảnh vào Archive → user xem → 404 / timeout. Archive cần rehydrate 1-15 giờ.

**Fix**:
- Archive **CHỈ** cho rare/compliance data (log 7 năm, backup tier 2).
- User-facing tối thiểu **Cool** tier.
- Rehydrate priority: Standard (1-15h) hoặc High ($$$, <1h).

### 7. Lifecycle policy đo từ modification time

**Bẫy**: Tưởng `daysAfterModificationGreaterThan` đo từ create. Thực tế đo từ **last modify**. Touch file = reset đếm.

**Fix**:
- Dùng `daysAfterCreationGreaterThan` nếu muốn đếm từ create.
- Hoặc `daysAfterLastAccessTimeGreaterThan` (cần bật Last Access Time Tracking — extra cost).

### 8. Private Endpoint không tự setup DNS

**Bẫy**: Tạo Private Endpoint xong → app vẫn resolve public IP → traffic Internet thay vì private.

**Fix**:
- Phải tạo **Private DNS Zone** `privatelink.blob.core.windows.net` + link vào VNet.
- Hoặc dùng Azure Private DNS Resolver / on-prem DNS forward.
- Test: `nslookup stacmeprodsea.blob.core.windows.net` từ VM trong VNet → IP private 10.x.

### 9. Storage Account region nhầm với resource khác

**Bẫy**: Storage `eastasia`, VM `southeastasia` → cross-region traffic + egress fee + latency.

**Fix**: Same region as compute. Vietnam → `southeastasia`.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] Phân biệt GPv2 / Premium block blob / Premium file shares?
- [ ] LRS vs ZRS vs GZRS — chọn cái nào cho prod / dev / DR?
- [ ] Hot / Cool / Cold / Archive — khi nào dùng cái nào, min retention bao nhiêu ngày?
- [ ] Vì sao User Delegation SAS tốt hơn Account/Service SAS?
- [ ] Disable Shared Key access + dùng Entra ID Managed Identity — tại sao?
- [ ] Phân biệt RBAC control plane vs data plane cho Blob?
- [ ] Setup Private Endpoint + Private DNS Zone — 3 bước?
- [ ] CMK Key Vault — rotate key có downtime không?
- [ ] Static website + Front Door — flow truy cập?
- [ ] Lifecycle policy `daysAfterModification` vs `daysAfterCreation` — khác nhau?

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Gom các lệnh `az storage ...` và `az role assignment ...` hay dùng nhất trong bài — từ tạo account/container, sinh SAS, gán RBAC data plane, tới firewall, CMK và static website.

| Mục đích | Lệnh |
|---|---|
| Tạo Storage Account an toàn | `az storage account create --name <st> -g <rg> --sku Standard_ZRS --kind StorageV2 --allow-blob-public-access false --allow-shared-key-access false --min-tls-version TLS1_2 --default-action Deny` |
| Tắt Shared Key access | `az storage account update --name <st> -g <rg> --allow-shared-key-access false` |
| Tắt anonymous public access | `az storage account update --name <st> -g <rg> --allow-blob-public-access false` |
| Tạo container | `az storage container create --account-name <st> --name <container> --auth-mode login` |
| Sinh User Delegation SAS (read 1h) | `az storage blob generate-sas --account-name <st> --container-name <c> --name <blob> --permissions r --expiry <ISO8601> --auth-mode login --as-user --https-only -o tsv` |
| Áp lifecycle policy | `az storage account management-policy create --account-name <st> -g <rg> --policy @lifecycle.json` |
| Gán RBAC data plane reader | `az role assignment create --assignee <user> --role "Storage Blob Data Reader" --scope <container-scope>` |
| Gán RBAC data plane contributor | `az role assignment create --assignee <user> --role "Storage Blob Data Contributor" --scope <account-scope>` |
| Firewall: deny all + allow IP | `az storage account update --name <st> -g <rg> --default-action Deny` · `az storage account network-rule add --account-name <st> -g <rg> --ip-address <ip>` |
| Tạo Private Endpoint cho blob | `az network private-endpoint create --name <pe> -g <rg> --vnet-name <vnet> --subnet <snet> --private-connection-resource-id <st-id> --group-id blob --connection-name <conn>` |
| Bật CMK (Key Vault) | `az storage account update --name <st> -g <rg> --encryption-key-source Microsoft.Keyvault --encryption-key-vault <kv-uri> --encryption-key-name <key>` |
| Bật static website | `az storage blob service-properties update --account-name <st> --static-website --index-document index.html --404-document 404.html` |
| Kiểm tra tên account hợp lệ | `az storage account check-name --name <name>` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Storage Account** | Tài khoản lưu trữ | Container chứa Blob/Files/Queue/Table (1 endpoint global unique) |
| **Container** | Thùng chứa | Tương đương S3 bucket — group blob |
| **Blob** | Đối tượng lưu trữ | Object lưu trữ (Block/Append/Page) |
| **Block blob** | Blob khối | File thông thường — default |
| **Page blob** | Blob trang | Random access — VM disk legacy |
| **Append blob** | Blob nối thêm | Append-only — log |
| **Access tier** | Tầng truy cập | Hot / Cool / Cold / Archive — trade-off storage vs access cost |
| **LRS / ZRS / GRS / GZRS** | Tùy chọn nhân bản | Replication options |
| **GPv2** | General-purpose v2 | Loại account mặc định |
| **SAS** | Chữ ký truy cập chia sẻ | Shared Access Signature — signed URL temporary |
| **User Delegation SAS** | SAS ủy quyền người dùng | SAS sign bằng Entra ID — revocable, audit |
| **Shared Key** | Khóa chia sẻ | Account key — full access, KHÔNG NÊN dùng |
| **Managed Identity** | Danh tính quản lý | Identity tự động cho Azure resource — best for auth |
| **Storage Blob Data Reader/Contributor/Owner** | Vai trò data plane | RBAC role data plane |
| **ABAC** | Kiểm soát theo thuộc tính | Attribute-Based Access Control — condition + RBAC |
| **Private Endpoint** | Điểm cuối riêng | NIC trong VNet, traffic không Internet |
| **Private DNS Zone** | Vùng DNS riêng | `privatelink.blob.core.windows.net` resolve private IP |
| **CMK** | Khóa khách quản lý | Customer-Managed Key — encryption key Key Vault |
| **PMK** | Khóa nền tảng quản lý | Platform-Managed Key — default Microsoft key |
| **Lifecycle Management** | Quản lý vòng đời | Policy auto-tier + delete blob theo age |
| **Static website** | Trang web tĩnh | Container `$web` serve HTML qua HTTPS |
| **Front Door** | Cổng vào toàn cầu | Global L7 CDN + WAF + custom domain HTTPS |
| **Purge protection** | Chống xóa vĩnh viễn | Key Vault không delete được trong retention period |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Azure VM + Managed Disks — Compute foundation](01_virtual-machines-and-disks.md)
- ➡️ **Bài tiếp theo:** [Azure SQL + Cosmos DB](03_azure-sql-and-cosmosdb.md)
- ↑ **Về cụm:** [Azure README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — dịch vụ tương đương trên AWS
- ☁️ [GCP Cloud Storage + IAM](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md) — dịch vụ tương đương trên GCP
- 🔐 [Cloud security basic](../../../cloud-fundamentals/) — khái niệm RBAC, encryption nền tảng
- 🏗️ [Terraform azurerm_storage_account](../../../../10_devops/iac/) — quản lý storage account bằng IaC

### 🌐 Tài nguyên tham khảo khác

- 📖 [Azure Blob Storage docs](https://learn.microsoft.com/azure/storage/blobs/)
- 📖 [Storage Account types](https://learn.microsoft.com/azure/storage/common/storage-account-overview)
- 📖 [Access tier overview](https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview)
- 📖 [Lifecycle Management](https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview)
- 📖 [SAS overview](https://learn.microsoft.com/azure/storage/common/storage-sas-overview)
- 📖 [User Delegation SAS](https://learn.microsoft.com/rest/api/storageservices/create-user-delegation-sas)
- 📖 [RBAC for Blob data](https://learn.microsoft.com/azure/storage/blobs/assign-azure-role-data-access)
- 📖 [Private Endpoint for Storage](https://learn.microsoft.com/azure/storage/common/storage-private-endpoints)
- 📖 [CMK with Key Vault](https://learn.microsoft.com/azure/storage/common/customer-managed-keys-overview)
- 📖 [Azure Front Door docs](https://learn.microsoft.com/azure/frontdoor/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bài 02 cluster Azure basic. Storage Account types + replication + Blob types + access tier (Hot/Cool/Cold/Archive) + Lifecycle + 3 auth methods (Shared Key/SAS/Entra ID) + User Delegation SAS + RBAC data plane + ABAC preview + firewall + Private Endpoint + CMK Key Vault + static website + Front Door CDN + hands-on image upload pipeline + 9 pitfalls. Mirror AWS S3+IAM lesson.
- **v2.0.0 (01/06/2026)** — Viết lại toàn bộ prose sang tiếng Việt narrative (lời dẫn 2-3 câu trước mỗi bảng/code/list, câu phân tích sau, câu bắc cầu giữa section); thay khối Pros/Cons điện tín bằng văn xuôi. Đổi cột "SLA durability" → "Durability (năm)" cho đúng nghĩa (durability theo năm, không phải SLA availability). Đổi `--expiry` SAS từ timestamp cứng (đã quá hạn) sang giá trị động `$(date ...)`. Chuẩn hoá metadata field "Yêu cầu trước", Glossary 3 cột (Thuật ngữ/Tiếng Việt/Giải thích), và nav (⬅️/➡️/↑ + link-text = tiêu đề H1 thực + 3 sub chuẩn).
- **v2.0.1 (10/06/2026)** — Bổ sung mục Tra cứu nhanh (Cheatsheet) cho đồng bộ với cụm Azure.
