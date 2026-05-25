# 📦 Azure Blob Storage + RBAC

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [01_virtual-machines-and-disks](01_virtual-machines-and-disks.md) ✅, hiểu RBAC concept cơ bản

> 🎯 *Blob Storage = analog AWS S3 / GCS. Trên Azure, blob nằm trong **Storage Account** (cha) → **Container** (tương đương bucket) → **Blob** (object). Bài này dạy: storage account types, access tier (Hot/Cool/Cold/Archive), lifecycle policy, **SAS token** (signed URL), **RBAC + ABAC** cho data plane, Storage Account firewall, **CMK với Key Vault**, static website + **Azure Front Door** CDN.*

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

Sếp:

> *"Migrate 500GB ảnh sản phẩm từ on-prem lên Azure Blob. Web upload bằng signed URL (đừng route ảnh qua server). Static site landing ở `shop.acmeshop.vn` qua Blob + Front Door CDN. Ảnh cũ > 90 ngày auto move sang Cold tier (rẻ hơn 50%). Bucket KHÔNG được public. Mã hóa CMK với Key Vault."*

Bạn cần:

- **Storage Account** General v2 LRS.
- **Container** `product-images` private, RBAC data plane.
- **Lifecycle** auto Hot → Cool sau 30 ngày → Cold sau 90 → Archive sau 365 → Delete sau 7 năm.
- **User Delegation SAS** cho upload từ frontend.
- **Static website** ở container `$web`.
- **Front Door** CDN + WAF + custom domain.
- **CMK** với Key Vault HSM.

Bài này dạy từng phần + hands-on.

---

## 1️⃣ Storage Account — cấu trúc

🪞 **Ẩn dụ**: *Storage Account như **chung cư 1 tòa nhà** — có 1 địa chỉ duy nhất (`stacmeprodlogs.blob.core.windows.net`); bên trong chia **4 tầng** (Blob/Files/Queue/Table); mỗi tầng có nhiều **căn hộ** (Container/FileShare); mỗi căn hộ chứa nhiều **đồ đạc** (Blob/File). Tòa nhà có firewall, có chìa khóa, có camera (logging).*

### Hierarchy

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

### Storage Account types

| Type | Performance | Use case |
|---|---|---|
| **General-purpose v2 (GPv2)** | Standard | **Default** — Blob + Files + Queue + Table, all access tiers |
| **General-purpose v1 (GPv1)** | Standard | Legacy — không dùng nữa |
| **Premium block blob** | Premium SSD | Low latency blob (high TPS, transactional workload) |
| **Premium page blob** | Premium SSD | VM disk (legacy unmanaged) |
| **Premium file shares** | Premium SSD | High-perf SMB/NFS shares |
| **Block blob storage** | Premium | Đã merged vào Premium block blob |

→ **2026 default**: GPv2 Standard cho 95% workload. Premium block blob cho real-time analytics, IoT high TPS.

### Replication (data redundancy)

| Type | Copies | Region | SLA durability |
|---|---|---|---|
| **LRS** (Locally Redundant) | 3 copies | 1 datacenter | 99.999999999% (11 nines) |
| **ZRS** (Zone Redundant) | 3 copies across 3 AZ | 1 region (cross zone) | 99.9999999999% (12 nines) |
| **GRS** (Geo Redundant) | 3 LRS + 3 LRS ở region pair | 2 regions | 99.99999999999999% (16 nines) |
| **GZRS** (Geo Zone Redundant) | 3 ZRS + 3 LRS ở region pair | 2 regions | 99.99999999999999% (16 nines) |
| **RA-GRS** | GRS + read-only secondary endpoint | 2 regions, read both | (same) |
| **RA-GZRS** | GZRS + read-only secondary | (same) | (same) |

→ **Default cho production**: ZRS (in-region HA) hoặc GZRS (cross-region DR). LRS chỉ cho dev/sandbox.

### Naming rule (đặc biệt!)

```
Storage Account name:
  - 3-24 ký tự
  - lowercase + digit ONLY (không gạch, không dấu chấm, không hoa)
  - GLOBALLY UNIQUE (giống S3 bucket)
  - Endpoint: <name>.blob.core.windows.net
```

→ Cách đặt: concat tight `stacmeprodsea001`, `stacmedevimages` — không dùng pattern bình thường `st-acme-prod-sea`.

---

## 2️⃣ Blob types + Access tier

### Blob types

| Type | Mục đích | Max size | Random access |
|---|---|---|---|
| **Block blob** | File thông thường (image, video, doc, log) | 4.75 TiB | Append chỉ |
| **Append blob** | Log file (chỉ append) | 195 GiB | No |
| **Page blob** | VM disk, random read/write | 8 TiB | Yes |

→ Default: **Block blob**. 99% case dùng cái này.

### Access tier (chỉ cho Block blob)

| Tier | Storage cost | Read cost | Min retention | Use case |
|---|---|---|---|---|
| **Hot** | $$$ | $ | None | Active access, daily read/write |
| **Cool** | $$ | $$ | 30 ngày | Infrequent access, monthly read |
| **Cold** | $ | $$$ | 90 ngày | Rare access, backup tier 2 |
| **Archive** | $ (lowest) | $$$$ + rehydrate 1-15h | 180 ngày | Long-term archive, compliance |

```
Cost example (US East, 2026, per GB/month):
  Hot     = $0.0184
  Cool    = $0.0100
  Cold    = $0.0036
  Archive = $0.00099
```

→ Archive **CHỈ TRUY CẬP SAU REHYDRATE 1-15 giờ**. Không phù hợp cho user-facing.

### Lifecycle Management — auto-tier

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

```bash
az storage account management-policy create \
    --account-name stacmeprodsea \
    --resource-group rg-prod-data \
    --policy @lifecycle.json
```

→ Auto-tier theo `daysAfterModificationGreaterThan` (đếm từ lần modify cuối). Tiết kiệm 70-90% cost long-tail data.

---

## 3️⃣ Auth methods — Shared Key vs SAS vs Entra ID

🪞 **Ẩn dụ**: *3 cách auth như **3 loại chìa khóa nhà** — Shared Key = chìa khóa master (mở mọi cửa, đưa ai cũng vào được — KHÔNG NÊN dùng); SAS token = vé thăm nhà có thời hạn (chỉ vài giờ, chỉ vào phòng nào); Entra ID = thẻ nhân viên (login Microsoft account, role-based — best practice 2026).*

### A. Shared Key (Account Key)

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

**Pros**: Easy, work everywhere.
**Cons**: Full access (read+write+delete cả account). Không revoke individual. Leak = catastrophe.

→ **2026 best practice**: **DISABLE** Shared Key access:

```bash
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --allow-shared-key-access false
```

### B. SAS (Shared Access Signature) — Signed URL

3 loại SAS:

| Loại | Mô tả | Best practice |
|---|---|---|
| **Account SAS** | Sign bằng account key, cover toàn account | Avoid (giống Shared Key) |
| **Service SAS** | Sign bằng account key, cover 1 service (Blob) | Avoid (vẫn cần account key) |
| **User Delegation SAS** | Sign bằng Entra ID token (no account key) | ✅ Best — revocable, audit |

#### User Delegation SAS (recommended)

```bash
# Get user delegation key (cần Entra ID auth)
az login

# Generate SAS cho 1 blob, valid 1 giờ, read-only
SAS=$(az storage blob generate-sas \
    --account-name stacmeprodsea \
    --container-name product-images \
    --name sku-001.jpg \
    --permissions r \
    --expiry "2026-05-24T15:00:00Z" \
    --auth-mode login \
    --as-user \
    --https-only \
    --output tsv)

URL="https://stacmeprodsea.blob.core.windows.net/product-images/sku-001.jpg?$SAS"
curl $URL
```

→ Frontend nhận URL này, upload/download trực tiếp Storage. Không cần proxy qua backend.

#### SAS via SDK (Python)

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

→ App chạy trên VM/AKS có **Managed Identity** → tự lấy token Entra ID → gọi Blob. Zero credential.

---

## 4️⃣ RBAC + ABAC cho Blob data plane

### Roles built-in (data plane)

| Role | Permission |
|---|---|
| `Storage Blob Data Owner` | Full data plane + POSIX ACL |
| `Storage Blob Data Contributor` | Read + Write + Delete |
| `Storage Blob Data Reader` | Read only |
| `Storage Account Contributor` | Quản lý account (control plane), **không** access data |
| `Reader` | Quản lý metadata only |

→ Chú ý: `Owner`/`Contributor` ở subscription level **KHÔNG** auto cho data plane! Phải gán role data plane riêng.

```bash
# Grant data plane reader
az role assignment create \
    --assignee thien.le@acmeshop.vn \
    --role "Storage Blob Data Reader" \
    --scope "/subscriptions/<sub>/resourceGroups/rg-prod-data/providers/Microsoft.Storage/storageAccounts/stacmeprodsea/blobServices/default/containers/product-images"
```

→ Có thể scope tới **container level** (granular) hoặc **storage account** (broad).

### ABAC (Attribute-Based Access Control) — beyond RBAC

ABAC = condition kèm RBAC role. Ví dụ: chỉ cho user A read blob có tag `Project=AcmeShop`.

```
Condition (in Azure Portal RBAC condition builder):

  (
    !(ActionMatches{'Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read'})
    OR
    @Resource[Microsoft.Storage/storageAccounts/blobServices/containers/blobs/tags:Project<$key_case_sensitive$>] StringEquals 'AcmeShop'
  )
```

→ Powerful, nhưng phức tạp. 2026 still preview cho 1 số scenario. Dùng cho compliance use case (PII filter).

### Anonymous public access (KHÔNG NÊN)

```bash
# Disable anonymous toàn account (best practice)
az storage account update \
    --name stacmeprodsea \
    --resource-group rg-prod-data \
    --allow-blob-public-access false
```

→ Mặc định 2024+ Azure block public. Nếu cần public (static site) → dùng Front Door + private storage.

---

## 5️⃣ Storage Account network — Firewall + Private Endpoint

### Default: public endpoint

```
https://stacmeprodsea.blob.core.windows.net  ← bất kỳ ai trên Internet đều resolve được
```

→ Auth bảo vệ, nhưng surface attack lớn.

### Storage Account firewall

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

= Tạo NIC trong VNet, gắn private IP, traffic không qua Internet.

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

→ App trong VNet gọi blob → resolve private IP → traffic intra-Azure, không Internet. **Best for PII/regulated data**.

---

## 6️⃣ Encryption — CMK với Key Vault

### Encryption tại Rest (default)

- Azure tự encrypt mọi blob bằng **PMK** (Platform-Managed Key) — AES 256, key Microsoft quản lý.
- Free, transparent.

### CMK (Customer-Managed Key)

Customer tự cung cấp encryption key qua Key Vault → giữ quyền **rotate/revoke**.

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

→ Rotate key → Storage tự encrypt lại; revoke key → blob không đọc được nữa (kill switch).

### HSM-backed key (top security)

- **Key Vault Premium** + **Managed HSM** → key sinh trong HSM hardware FIPS 140-2 Level 3.
- Cost: ~$5,000/tháng cho Managed HSM cluster (expensive).
- Use case: banking, healthcare, government.

---

## 7️⃣ Static website + Front Door CDN

### Static website hosting

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

### Azure Front Door (Global CDN + WAF)

= L7 global accelerator + CDN + WAF + custom domain HTTPS auto.

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

→ HTTPS auto cert, global edge cache, WAF rule built-in (block OWASP top 10, bot, geo-block).

---

## 🛠️ Hands-on — Image upload pipeline

### Mục tiêu

Web upload ảnh qua **User Delegation SAS** trực tiếp lên Storage (không qua server). Container private. Lifecycle auto-tier. Static site landing qua Front Door.

### Bước 1 — Tạo Storage Account

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

```bash
pip install azure-identity azure-storage-blob
URL=$(python generate_sas.py sku-001.jpg)

# Upload từ frontend (curl mô phỏng)
curl -X PUT -H "x-ms-blob-type: BlockBlob" \
     --data-binary @local-image.jpg \
     "$URL"
```

### Bước 4 — Lifecycle policy

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

```bash
az group delete --name rg-prod-data --yes --no-wait
```

→ **Kết quả**: Upload qua SAS thành công, container private, lifecycle policy active, static site live.

---

## ⚠️ Pitfalls

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

## 🎯 Self-check

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

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Storage Account** | Container chứa Blob/Files/Queue/Table (1 endpoint global unique) |
| **Container** | Tương đương S3 bucket — group blob |
| **Blob** | Object lưu trữ (Block/Append/Page) |
| **Block blob** | File thông thường — default |
| **Page blob** | Random access — VM disk legacy |
| **Append blob** | Append-only — log |
| **Access tier** | Hot / Cool / Cold / Archive — trade-off storage vs access cost |
| **LRS / ZRS / GRS / GZRS** | Replication options |
| **GPv2** | General-purpose v2 — default account kind |
| **SAS** | Shared Access Signature — signed URL temporary |
| **User Delegation SAS** | SAS sign bằng Entra ID — revocable, audit |
| **Shared Key** | Account key — full access, KHÔNG NÊN dùng |
| **Managed Identity** | Identity tự động cho Azure resource — best for auth |
| **Storage Blob Data Reader/Contributor/Owner** | RBAC role data plane |
| **ABAC** | Attribute-Based Access Control — condition + RBAC |
| **Private Endpoint** | NIC trong VNet, traffic không Internet |
| **Private DNS Zone** | `privatelink.blob.core.windows.net` resolve private IP |
| **CMK** | Customer-Managed Key — encryption key Key Vault |
| **PMK** | Platform-Managed Key — default Microsoft key |
| **Lifecycle Management** | Policy auto-tier + delete blob theo age |
| **Static website** | Container `$web` serve HTML qua HTTPS |
| **Front Door** | Global L7 CDN + WAF + custom domain HTTPS |
| **Purge protection** | Key Vault không delete được trong retention period |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [01_virtual-machines-and-disks](01_virtual-machines-and-disks.md)
- → Tiếp: [03_azure-sql-and-cosmosdb](03_azure-sql-and-cosmosdb.md)
- ↑ Cluster Azure: [Azure README](../../README.md)

### Cross-reference
- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — analog
- ☁️ [GCP Cloud Storage + IAM](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md) — analog
- 🔐 [Cloud security basic](../../../cloud-fundamentals/) — RBAC, encryption concept
- 🏗️ [Terraform azurerm_storage_account](../../../../10_DevOps/iac/)

### Tài nguyên ngoài (2026)
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

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài 02 cluster Azure basic. Storage Account types + replication + Blob types + access tier (Hot/Cool/Cold/Archive) + Lifecycle + 3 auth methods (Shared Key/SAS/Entra ID) + User Delegation SAS + RBAC data plane + ABAC preview + firewall + Private Endpoint + CMK Key Vault + static website + Front Door CDN + hands-on image upload pipeline + 9 pitfalls. Mirror AWS S3+IAM lesson.
