# 🗄️ Spaces — Object Storage kèm CDN miễn phí

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Droplet và Volume](01_droplets-and-volumes.md), hiểu HTTP/REST cơ bản; nếu từng dùng *S3* hoặc *GCS* thì càng dễ theo.

> 🎯 *Bài 01 cho bạn cái máy chủ và ổ đĩa. Nhưng máy chủ không phải nơi để chứa hàng triệu tấm ảnh, file PDF hay backup — disk của Droplet vừa nhỏ vừa đắt, lại biến mất nếu Droplet chết. Bài này giới thiệu **Spaces** — object storage của DigitalOcean, tương thích API S3 (dùng được mọi tool S3 sẵn có) và kèm sẵn một CDN miễn phí. Bạn sẽ đi từ "object storage là gì" cho tới hands-on host một static site và phát file riêng tư an toàn qua presigned URL.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Spaces** là gì, vì sao "tương thích S3" lại là điểm cộng lớn
- [ ] So sánh chi phí và tính năng giữa **Spaces**, **AWS S3** và **Cloudflare R2**
- [ ] Tạo Space rồi upload/download bằng `s3cmd`, `aws-cli` hoặc SDK
- [ ] Tạo **Spaces Access Key** an toàn (và biết vì sao không được dùng PAT)
- [ ] Sinh **presigned URL** để phát file private
- [ ] Bật **CDN** miễn phí cho Spaces, gắn custom domain
- [ ] Cấu hình **lifecycle policy** để tự dọn file cũ
- [ ] Cấu hình **CORS** cho phép web upload thẳng lên Spaces
- [ ] Tự tay host một static site và phát hóa đơn private an toàn

---

## 💡 Avatar thì ai cũng xem được, hóa đơn thì chỉ chủ nhân

Hãy hình dung bạn đang làm một internal tool, và sếp ghé qua bàn giao đúng hai nhu cầu lưu trữ trông thì giống nhau nhưng bản chất ngược nhau:

> *"Tool của mình có hai chỗ cần chứa file. Một là user upload avatar — ảnh này hiển thị công khai khắp nơi, ai vào trang cũng thấy. Hai là hệ thống xuất hóa đơn PDF — file này riêng tư, chỉ đúng người sở hữu mới được mở. Đừng nhét PDF lên Droplet nhé, vừa chật disk vừa mất sạch nếu Droplet chết. Tìm cái object storage nào rẻ, đơn giản, mà đừng phải đụng tới AWS."*

Nghe thì hai yêu cầu, nhưng nó gói gọn gần hết những gì một lập trình viên cần biết về object storage: file public phải phát nhanh qua *CDN*, file private phải khóa lại nhưng vẫn cho đúng người tải về, và tất cả phải nằm ngoài máy chủ để máy chủ có chết cũng không mất dữ liệu.

DigitalOcean **Spaces** trả lời gọn cả hai. Giá phẳng $5/tháng đã gồm 250GB dung lượng kèm 1TB băng thông; API tương thích *S3* nên `aws-cli`, `boto3` hay bất kỳ tool S3 nào cũng cắm vào chạy được; CDN đi kèm miễn phí để phát avatar nhanh toàn cầu; và presigned URL lo phần phát hóa đơn private. Bài này sẽ dựng đủ cả hai tới mức chạy được production.

---

## 1️⃣ Object Storage là gì, vì sao cần tới nó

Trước khi đụng vào Spaces, cần nắm bản chất "object storage" khác gì cái ổ đĩa quen thuộc. Đây là kiểu lưu trữ mà rất nhiều người mới hiểu nhầm, nên một ẩn dụ sẽ giúp định hình đúng ngay từ đầu.

🪞 **Ẩn dụ**: *Object Storage giống một **nhà kho khổng lồ** nơi mọi món đồ được dán một mã thẻ (gọi là "key") rồi quăng vào kho — không có thư mục thật, không xếp theo thứ tự, muốn lấy món nào thì đọc đúng mã thẻ là nhân viên kho mang ra. Sức chứa coi như vô hạn. Còn Block Storage (Volume ở bài trước) thì như **ổ cứng laptop** — có cây thư mục thật, truy cập ngẫu nhiên cực nhanh, nhưng dung lượng cố định và chỉ một máy cắm vào dùng được.*

Điểm mấu chốt: thư mục trong object storage chỉ là *ảo* — bạn thấy đường dẫn `avatars/user-123.jpg` trông như có folder `avatars/`, nhưng thực ra cả chuỗi đó chỉ là một cái "key" liền mạch. Bảng dưới đặt ba loại storage cloud cạnh nhau để thấy rõ vì sao mỗi loại sinh ra cho một việc khác nhau.

| | Block Storage | File Storage | Object Storage |
|---|---|---|---|
| **Đại diện DO** | Volume | (không có managed) | Spaces |
| **Truy cập** | Cấp block (SSD) | NFS/SMB | HTTP REST |
| **Mount được** | Có (1 Droplet) | Có (multi) | Không (qua API) |
| **Dung lượng** | 1-16 TB | TB → PB | Vô hạn |
| **Latency** | < 1 ms | 1-10 ms | 50-200 ms |
| **Giá/GB/tháng** | $0.10 | (n/a) | $0.02 |
| **Phù hợp** | DB, OS disk | Shared filesystem | Static asset, backup, log, media |

Hai con số đáng chú ý nhất là *latency* và *giá*. Object storage chậm hơn block storage hàng trăm lần (50-200ms so với dưới 1ms) — nghĩa là tuyệt đối đừng đặt database lên nó. Đổi lại, giá chỉ bằng một phần năm ($0.02 so với $0.10/GB), nên nó là lựa chọn hiển nhiên cho thứ gì cần lưu thật nhiều mà không cần truy cập tức thì.

Từ đặc tính đó, ta rút ra được khi nào nên và không nên dùng. Hãy dùng object storage cho:

- Static asset: ảnh, video, CSS, JS, font.
- User-generated content: avatar, file đính kèm, mọi thứ user upload lên.
- Backup: dump database, tarball snapshot server.
- Log lưu trữ lâu dài: gzip log để dành.
- Data lake: file parquet/csv để query sau.
- Host static website.

Và tránh xa object storage trong các trường hợp sau, vì latency cao sẽ giết hiệu năng:

- Database (cần đọc ngẫu nhiên nhanh, cần *ACID*) → dùng Block Storage hoặc Managed DB.
- Hệ thống file cần chuẩn *POSIX* (vd thư mục data của Postgres) → dùng Volume.
- Truy cập đòi latency cực thấp (dưới 10ms) → Volume kèm cache.

Nắm được "object storage hợp với việc gì" rồi, giờ ta xem DigitalOcean hiện thực hóa nó thành sản phẩm Spaces như thế nào.

---

## 2️⃣ Spaces là gì — Object Storage của DigitalOcean

**Spaces** là dịch vụ object storage của DigitalOcean, ra mắt năm 2017 với điểm bán hàng cốt lõi: **API tương thích S3**. Trong thuật ngữ Spaces, mỗi "Space" chính là một "bucket" của S3 — cùng một khái niệm, chỉ khác cái tên.

Vì sao "tương thích S3" lại quan trọng đến vậy? Bởi S3 của Amazon ra đời từ 2006 và đã trở thành chuẩn de-facto của ngành: hầu hết mọi thư viện, SDK, CLI về object storage đều nói được "ngôn ngữ S3". Khi Spaces nói cùng ngôn ngữ đó, bạn không phải học API mới, không phải đổi code — chỉ trỏ endpoint sang DigitalOcean là chạy. Bảng dưới tóm tắt những đặc điểm bạn cần nhớ khi tính toán cho năm 2026 (các con số giá là *tính đến 2026*, DO có thể đổi bảng giá — đối chiếu trang pricing chính thức trước khi quyết).

| Đặc điểm | Mô tả |
|---|---|
| **Pricing flat** | $5/tháng: 250GB storage + 1TB outbound transfer + unlimited upload |
| **Vượt** | $0.02/GB extra storage, $0.01/GB extra transfer |
| **API** | S3-compatible (Signature V4), dùng được AWS SDK |
| **CDN built-in** | Miễn phí, có PoP ở hàng trăm thành phố toàn cầu |
| **Region** | Có ở nhiều region; phổ biến: `nyc3`, `sfo3`, `ams3`, `sgp1`, `fra1`, `syd1` |
| **Max object size** | 5 TB |
| **TLS** | Bắt buộc HTTPS endpoint |
| **Versioning** | Không có (khác S3) |
| **Lifecycle** | Có (Bucket Lifecycle Policy — expire object after N days) |

Hai dòng cuối là chỗ Spaces khác S3 rõ nhất, và là thứ dễ làm bạn vấp nếu quen với AWS: Spaces **không có versioning**, nên ghi đè file là mất bản cũ vĩnh viễn (mục cạm bẫy sẽ nói kỹ). Bù lại nó vẫn có lifecycle để tự dọn file hết hạn.

Mọi object trong Spaces được định danh bằng một URL theo đúng một khuôn mẫu cố định. Hiểu khuôn mẫu này giúp bạn đọc và ghép URL mà không cần tra cứu:

```
https://<space-name>.<region>.digitaloceanspaces.com/<object-key>
```

Áp vào tình huống avatar ở đầu bài, một file cụ thể sẽ có địa chỉ như sau:

```
https://acmeshop-uploads.sgp1.digitaloceanspaces.com/avatars/user-123.jpg
```

Đó là endpoint "gốc" (origin). Nếu muốn file phát nhanh cho người dùng ở khắp thế giới, bạn dùng endpoint CDN — khác đúng một chữ `cdn` chèn vào giữa:

```
https://<space-name>.<region>.cdn.digitaloceanspaces.com/<object-key>
```

Sự khác biệt một chữ này lại là khác biệt về tốc độ: URL origin trỏ thẳng về region gốc, còn URL CDN sẽ được phục vụ từ điểm gần người dùng nhất. Ta sẽ quay lại CDN ở mục 6.

---

## 3️⃣ Spaces, S3 và R2 — chọn cái nào cho ví tiền của bạn

Spaces không phải lựa chọn duy nhất. Trên thị trường còn AWS S3 (ông tổ của thể loại này) và Cloudflare R2 (kẻ thách thức trẻ với chiêu bài "egress miễn phí"). Vì giá object storage có thể chênh nhau cả chục lần tùy workload, chọn sai vendor là đốt tiền oan hàng tháng. Bảng dưới so ba lựa chọn trên những tiêu chí thực sự ảnh hưởng tới hóa đơn (mọi đơn giá ở đây là *tính đến 2026* — cả ba vendor đều chỉnh giá theo thời gian, kiểm tra lại trước khi tính toán thật).

| | DO Spaces | AWS S3 | Cloudflare R2 |
|---|---|---|---|
| **Base price** | $5/tháng (250GB + 1TB) | $0 base + $0.023/GB | $0 base + $0.015/GB |
| **Storage** | $0.02/GB (vượt 250GB) | $0.023/GB Standard | $0.015/GB |
| **Outbound to internet** | $0.01/GB (vượt 1TB) | $0.09/GB | **$0** (free egress!) |
| **PUT/POST** | Included | $0.005/1k | $4.50/1M |
| **GET** | Included | $0.0004/1k | $0.36/1M |
| **CDN built-in** | ✅ Free | ❌ (CloudFront separate) | ✅ Free |
| **Versioning** | ❌ | ✅ | ✅ |
| **Lifecycle** | ✅ | ✅ | ✅ |
| **S3 SDK** | ✅ | ✅ | ✅ |
| **Compliance** | SOC 2 | SOC2, HIPAA, PCI, FedRAMP, ... | SOC 2 |

Dòng quyết định toàn bộ cuộc chơi là **Outbound to internet** — tức tiền trả khi dữ liệu rời cloud ra Internet (gọi là *egress*). S3 tính $0.09/GB, một con số nhỏ trên giấy nhưng nhân với hàng TB mỗi tháng thì phình ra khủng khiếp. R2 thì miễn phí egress hoàn toàn. Để thấy độ chênh thực tế, hãy lấy một workload giả định cụ thể: 500GB dung lượng và 5TB outbound mỗi tháng.

| Vendor | Cost |
|---|---|
| **DO Spaces** | $5 base + ($250GB × $0.02 = $5) + (4TB × $0.01 = $40) = **$50** |
| **AWS S3** | (500GB × $0.023 = $11.50) + (5TB × $0.09 = $460) = **$471.50** |
| **Cloudflare R2** | (500GB × $0.015 = $7.50) + $0 egress = **$7.50** |

Con số nói thay lời: cùng một workload, S3 đắt gần gấp mười Spaces, mà gần như toàn bộ khoản đắt đó đến từ egress. Từ đây rút ra quy tắc chọn: **DO Spaces** là điểm rơi đẹp cho workload tầm 100-500GB kèm 1-5TB outbound, lại có sẵn CDN khỏi cấu hình; **R2** thắng tuyệt đối nếu egress là khoản chi áp đảo; còn **S3** chỉ nên chọn khi bạn đã ở sẵn trong hệ sinh thái AWS và cần các tính năng compliance nó độc quyền.

> ⚠️ **Xu hướng 2026**: nhiều team đang dịch chuyển từ S3 sang R2 chỉ để cắt khoản egress. DO Spaces vẫn giữ chỗ đứng nhờ sự đơn giản và CDN có sẵn — bạn không phải dựng thêm CloudFront như bên AWS.

---

## 4️⃣ Tạo Space và lần upload đầu tiên

Lý thuyết đủ rồi, giờ bắt tay vào việc. Quy trình từ con số không tới lần upload đầu gồm bốn bước: tạo Space, tạo key, cấu hình tool, rồi upload. Ta đi lần lượt.

### Bước 1 — Tạo Space

Một Space tạo nhanh bằng một dòng `doctl`, chỉ cần đặt tên và chọn region. Region nên gần người dùng của bạn nhất để giảm latency.

```bash
# CLI
doctl spaces create acmeshop-uploads \
    --region sgp1

# Hoặc UI: Spaces → Create Bucket → name + region + ACL
```

> ⚠️ Tên Space phải **unique toàn cầu** (giống quy tắc bucket của S3) — tức trùng với bất kỳ ai trên thế giới là không tạo được. Đặt rõ ràng theo kiểu `<company>-<purpose>` để vừa dễ nhớ vừa khó đụng, ví dụ `acmeshop-uploads`, `acmeshop-static`.

### Bước 2 — Tạo Spaces Access Key

Đây là chỗ rất nhiều người mới vấp. Spaces **không** dùng chung khóa với phần còn lại của DigitalOcean — bạn phải tạo một bộ key riêng dành cho Spaces, tuyệt đối không lấy PAT (Personal Access Token) ra dùng.

```
UI: API → Spaces Keys → Generate New Key
Name: "acmeshop-uploads-app"
Scope:
  - Read & Write: chọn 1 Space cụ thể (least privilege)
  - Hoặc Full Access (cẩn thận)
```

Khi tạo xong, hệ thống hiện cặp `Access Key` và `Secret Key` — hãy copy ngay, vì `Secret Key` chỉ hiện đúng một lần. Mất là phải tạo lại key mới. Theo nguyên tắc *least privilege* (cấp ít quyền nhất có thể), nên giới hạn key vào đúng một Space thay vì Full Access.

### Bước 3 — Cấu hình `s3cmd` (hoặc `aws-cli`)

Có key rồi, bạn cần một tool để nói chuyện với Spaces. Vì Spaces tương thích S3, mọi client S3 đều dùng được — chỉ cần trỏ chúng về endpoint của DigitalOcean thay vì AWS. Dưới đây là ba lựa chọn phổ biến, chọn cái nào hợp thói quen của bạn.

Lựa chọn A là `s3cmd` — gọn nhẹ, hợp cho thao tác thủ công và scripting đơn giản:

```bash
brew install s3cmd

s3cmd --configure
# Access Key: <paste>
# Secret Key: <paste>
# Default Region: US (chấp nhận default, DO không quan tâm)
# S3 Endpoint: sgp1.digitaloceanspaces.com
# DNS-style bucket+hostname: %(bucket)s.sgp1.digitaloceanspaces.com
# Encryption password: (để trống)
# Test access: y
```

Lựa chọn B là `aws-cli` — nếu bạn đã quen công cụ của AWS thì dùng luôn, chỉ cần luôn nhớ kèm cờ `--endpoint-url` để trỏ về Spaces:

```bash
aws configure --profile do-spaces
# AWS Access Key ID: <DO key>
# AWS Secret Access Key: <DO secret>
# Default region: us-east-1  (placeholder)
# Default output: json

# Dùng phải kèm endpoint
aws s3 ls --endpoint-url=https://sgp1.digitaloceanspaces.com --profile do-spaces
```

Lựa chọn C là `boto3` — SDK Python, dùng khi bạn cần thao tác Spaces ngay trong code ứng dụng (chính là cách backend sẽ làm ở phần hands-on). Lưu ý `signature_version='s3v4'` là bắt buộc để Spaces chấp nhận chữ ký:

```python
import boto3
from botocore.client import Config

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='sgp1',
    endpoint_url='https://sgp1.digitaloceanspaces.com',
    aws_access_key_id='DO_ACCESS_KEY',
    aws_secret_access_key='DO_SECRET_KEY',
    config=Config(signature_version='s3v4'),
)

# Upload
client.upload_file('avatar.jpg', 'acmeshop-uploads', 'avatars/user-123.jpg')

# Download
client.download_file('acmeshop-uploads', 'avatars/user-123.jpg', 'local.jpg')

# List
for obj in client.list_objects_v2(Bucket='acmeshop-uploads')['Contents']:
    print(obj['Key'], obj['Size'])
```

### Bước 4 — Upload, download và các thao tác cơ bản

Với `s3cmd` đã cấu hình xong, các thao tác hằng ngày chỉ còn là những lệnh ngắn. Đáng chú ý nhất là cờ `--acl-public`: mặc định mọi file upload lên đều *private*, nên muốn file hiển thị công khai (như avatar) bạn phải nói rõ.

```bash
# Upload file
s3cmd put avatar.jpg s3://acmeshop-uploads/avatars/user-123.jpg

# Upload với public ACL
s3cmd put avatar.jpg s3://acmeshop-uploads/avatars/user-123.jpg --acl-public

# Download
s3cmd get s3://acmeshop-uploads/avatars/user-123.jpg ./local.jpg

# List
s3cmd ls s3://acmeshop-uploads/
s3cmd ls s3://acmeshop-uploads/avatars/

# Sync folder
s3cmd sync ./public/ s3://acmeshop-uploads/public/ --acl-public --delete-removed

# Delete
s3cmd del s3://acmeshop-uploads/avatars/user-123.jpg

# Set bucket public read (để serve static)
s3cmd setacl s3://acmeshop-uploads --acl-public
```

Lệnh `sync` là con dao Thụy Sĩ ở đây — nó so sánh folder local với Space rồi chỉ upload phần thay đổi, kèm `--delete-removed` để xóa luôn file đã bị bỏ ở local. Đây chính là cơ chế ta dùng để deploy static site ở phần hands-on. Nhưng trước khi serve file public, hãy giải quyết nửa khó hơn của bài toán: file private.

---

## 5️⃣ Presigned URL — phát file private đúng người

Quay lại yêu cầu hóa đơn PDF ở đầu bài: file của user A tuyệt đối không được để user B xem. Cách thô là đặt cả Space về private, nhưng làm vậy thì chính user A cũng không tải được — vì người dùng cuối làm gì có Spaces key. Đây là bài toán kinh điển: *làm sao cho đúng một người, đúng một lúc, được tải đúng một file private mà không cần phát key cho họ?*

🪞 **Ẩn dụ**: *Presigned URL giống một **vé gửi xe có dập giờ**. Bạn — người giữ kho — dập lên vé "vé này vào lấy đúng chiếc xe số 42, có hiệu lực trong 1 giờ" rồi đưa cho khách. Khách cầm vé vào lấy xe bình thường, không cần biết mật khẩu kho. Quá 1 giờ, vé thành tờ giấy lộn.*

Cơ chế đúng như vậy: backend (vốn có Spaces key) sẽ sinh ra một URL đã ký sẵn chữ ký số, kèm thời hạn ngắn, rồi gửi URL đó cho user. User dùng URL như một link tải bình thường (HTTP GET), và khi hết giờ thì link tự vô hiệu. Toàn bộ "uy quyền" nằm trong chữ ký, nên không cần lộ key cho client.

Sinh một presigned URL để **tải** (GET) file private bằng `boto3` chỉ là một lời gọi hàm. Tham số `ExpiresIn` là thời hạn tính bằng giây:

```python
url = client.generate_presigned_url(
    'get_object',
    Params={
        'Bucket': 'acmeshop-uploads',
        'Key': f'invoices/{user_id}/2026-05-invoice.pdf'
    },
    ExpiresIn=3600,  # 1 giờ
)
print(url)
# https://acmeshop-uploads.sgp1.digitaloceanspaces.com/invoices/u123/2026-05-invoice.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...&X-Amz-Expires=3600&X-Amz-Signature=abc123
```

Nhìn vào URL kết quả, phần đuôi `?X-Amz-Signature=...` chính là "con dấu" — đó là chữ ký mà Spaces sẽ kiểm để biết URL hợp lệ và chưa hết hạn. Nếu thích dùng CLI thay vì code, `aws s3 presign` cho ra cùng kết quả:

```bash
aws s3 presign s3://acmeshop-uploads/invoices/u123/2026-05-invoice.pdf \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --expires-in 3600 \
    --profile do-spaces
```

Hay hơn nữa, presigned URL không chỉ dùng để tải mà còn để **upload** (PUT). Thay vì user gửi file qua backend rồi backend mới đẩy lên Spaces (tốn băng thông hai chặng), backend chỉ cấp một URL upload và user bắn file thẳng lên Spaces:

```python
# Backend tạo URL upload
url = client.generate_presigned_url(
    'put_object',
    Params={
        'Bucket': 'acmeshop-uploads',
        'Key': f'avatars/{user_id}.jpg',
        'ContentType': 'image/jpeg',
    },
    ExpiresIn=600,  # 10 phút
)
# Trả URL cho frontend
```

Phía frontend chỉ việc PUT file vào URL nhận được:

```javascript
// User chọn file, upload trực tiếp lên Spaces
const file = document.querySelector('input[type=file]').files[0];
await fetch(presignedUrl, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': 'image/jpeg' }
});
```

Lợi ích rất rõ: backend không còn phải làm trạm trung chuyển cho từng byte của mọi file — giảm tải CPU, giảm băng thông Droplet, và file đi đường ngắn nhất tới Spaces. Đổi lại, vì client cầm "vé" trong tay nên bạn phải siết quy tắc cấp vé cho chặt. Bảng dưới là những best practice nên áp ngay từ đầu.

| Best practice | Lý do |
|---|---|
| Expire ngắn (5-60 phút) | Hạn chế replay attack (URL bị tóm và dùng lại) |
| Include `Content-Type` khi upload | Tránh user upload file lạ kiểu khác |
| Validate size sau upload | User có thể bypass giới hạn ở UI |
| Re-generate URL cho mỗi request | Không cache, không chia sẻ lại |
| Log lần generate (audit) | Truy vết khi có sự cố rò rỉ |

---

## 6️⃣ CDN miễn phí — phát nội dung từ rìa mạng

File public như avatar thì không cần chữ ký, nhưng cần **nhanh** — và nhanh với người dùng toàn cầu nghĩa là phải phát từ điểm gần họ chứ không bắt họ kéo dữ liệu vòng nửa vòng trái đất về region gốc. Đó là việc của *CDN* (Content Delivery Network — mạng phân phối nội dung): cache file ở hàng loạt điểm rìa (*edge*) trên khắp thế giới. Điểm cộng lớn của Spaces là CDN này có sẵn và miễn phí, bật chỉ một thao tác.

Bật CDN qua UI hoặc một lệnh `doctl`. Tham số `TTL` (Time to Live) quyết định bao lâu edge giữ bản cache trước khi hỏi lại file gốc:

```
UI: Spaces → <space-name> → Settings → CDN → Enable
TTL: 3600 (default) — tùy nhu cầu
Custom domain: cdn.acmeshop.vn (optional)
```

```bash
doctl spaces cdn create acmeshop-uploads \
    --ttl 3600
```

Mặc định URL CDN sẽ có dạng `...cdn.digitaloceanspaces.com`, hơi dài và lộ tên nhà cung cấp. Production thường muốn một domain đẹp của riêng mình như `cdn.acmeshop.vn`. Quy trình gắn custom domain gồm các bước sau, trong đó DigitalOcean tự lo luôn chứng chỉ SSL:

```
1. UI bật CDN → "Add Custom Subdomain"
2. Nhập: cdn.acmeshop.vn
3. DO tạo SSL cert auto (Let's Encrypt)
4. Bạn add CNAME ở DNS:
   cdn.acmeshop.vn → acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com
5. Wait 5-30 phút, SSL active
```

Sau khi cấu hình xong, cùng một file sẽ có ba địa chỉ truy cập, mỗi cái cho một mục đích khác nhau. Đừng nhầm lẫn giữa chúng — đặc biệt là đừng để URL origin lọt ra trang public vì nó bỏ qua CDN.

| Loại | URL | Khi dùng |
|---|---|---|
| Origin | `https://acmeshop-uploads.sgp1.digitaloceanspaces.com/avatar.jpg` | Internal, debug |
| CDN | `https://acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com/avatar.jpg` | Public, faster global |
| Custom | `https://cdn.acmeshop.vn/avatar.jpg` | Production, branded |

Cache là con dao hai lưỡi: nó làm mọi thứ nhanh, nhưng khi bạn cập nhật file thì người dùng vẫn thấy bản cũ cho tới khi cache hết hạn. Khi cần ép edge bỏ bản cũ ngay, dùng lệnh purge:

```bash
# Purge 1 file
doctl spaces cdn flush <CDN_ID> --files /avatars/user-123.jpg

# Purge all
doctl spaces cdn flush <CDN_ID> --files "*"
```

> ⚠️ Purge mất 1-2 phút mới lan hết các edge. Với file hay đổi trong production, đặt version vào key (`avatar-v2.jpg`) thường gọn hơn là purge liên tục — vì URL mới thì không có gì để cache cũ cả.

---

## 7️⃣ Lifecycle policy — tự dọn file cũ

File rác tích lại theo thời gian: thư mục `temp/` đầy file tạm, `logs/` phình ra mỗi ngày. Dọn tay thì quên, mà để đó thì tốn tiền lưu trữ. Lifecycle policy giải quyết bằng cách đặt sẵn quy tắc "file trong thư mục X quá N ngày thì tự xóa", để DigitalOcean lo phần dọn dẹp.

Quy tắc viết dưới dạng JSON, mỗi rule gắn với một tiền tố (*prefix*) đường dẫn và một số ngày hết hạn. Ví dụ dưới đặt hai rule: dọn file tạm sau 7 ngày, dọn log sau 90 ngày:

```bash
# Tạo lifecycle JSON
cat > lifecycle.json <<EOF
{
  "Rules": [
    {
      "ID": "delete-temp-after-7days",
      "Status": "Enabled",
      "Filter": { "Prefix": "temp/" },
      "Expiration": { "Days": 7 }
    },
    {
      "ID": "delete-logs-after-90days",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Expiration": { "Days": 90 }
    }
  ]
}
EOF

# Apply
aws s3api put-bucket-lifecycle-configuration \
    --bucket acmeshop-uploads \
    --lifecycle-configuration file://lifecycle.json \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces

# Verify
aws s3api get-bucket-lifecycle-configuration \
    --bucket acmeshop-uploads \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces
```

Luôn chạy lệnh `get-bucket-lifecycle-configuration` ngay sau khi apply để xác nhận rule đã vào đúng — vì lifecycle là thao tác *xóa tự động*, một prefix gõ sai có thể quét nhầm dữ liệu thật. Cũng lưu ý lifecycle chạy bất đồng bộ: DigitalOcean quét mỗi ngày một lần, nên chấp nhận việc file hết hạn còn nằm lại thêm vài giờ trước khi bị dọn.

---

## 8️⃣ CORS — cho phép web upload thẳng lên Spaces

Còn một rào chắn cuối khi muốn frontend upload thẳng lên Spaces (như cách presigned PUT ở mục 5). Trình duyệt có một cơ chế bảo vệ tên là *same-origin policy*: theo mặc định, trang `https://acmeshop.vn` không được phép gửi request tới một domain khác như `https://acmeshop-uploads.sgp1...`. Browser sẽ chặn thẳng tay và báo lỗi CORS. Để mở đường, Space phải khai báo rõ "tôi cho phép những origin nào gọi tới".

Khai báo này cũng là một file JSON, liệt kê các origin được phép, các HTTP method và header cho phép:

```bash
cat > cors.json <<EOF
{
  "CORSRules": [
    {
      "AllowedOrigins": ["https://acmeshop.vn", "http://localhost:3000"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
EOF

aws s3api put-bucket-cors \
    --bucket acmeshop-uploads \
    --cors-configuration file://cors.json \
    --endpoint-url=https://sgp1.digitaloceanspaces.com \
    --profile do-spaces
```

Để ý `AllowedOrigins` liệt kê đích danh `https://acmeshop.vn` cho production và `http://localhost:3000` cho lúc dev. Đây là chi tiết an ninh quan trọng, không phải tiện tay.

> ⚠️ **Đừng** dùng `AllowedOrigins: ["*"]` — đó là mời mọi website trên đời gọi tới Space của bạn, mở đường cho tấn công CSRF và scrape dữ liệu. Luôn liệt kê origin cụ thể.

---

## 🛠️ Hands-on — Static site và hóa đơn private

Đã đủ nguyên liệu để dựng trọn vẹn cả hai yêu cầu sếp giao ở đầu bài. Phần thực hành này gồm ba mảnh: host một static site công khai, phát hóa đơn private qua presigned URL, và cho user upload avatar thẳng lên Spaces.

### Mục tiêu

1. Host static site `https://www.acmeshop.vn` từ một Space.
2. Backend sinh presigned URL cho user tải hóa đơn private.
3. Backend cấp presigned PUT cho user upload avatar không qua trung chuyển.

### Phần A — Static site

Trước hết tạo một Space riêng cho nội dung tĩnh (tách khỏi Space chứa upload của user để dễ phân quyền), đẩy thư mục build lên kèm `Cache-Control` để trình duyệt cache hợp lý, rồi bật CDN:

```bash
# Tạo Space riêng cho static
doctl spaces create acmeshop-static --region sgp1

# Upload site (assume folder ./dist)
s3cmd sync ./dist/ s3://acmeshop-static/ \
    --acl-public \
    --delete-removed \
    --add-header="Cache-Control:public, max-age=3600"

# Bật CDN
doctl spaces cdn create acmeshop-static --ttl 3600

# Custom domain → cdn.acmeshop.vn → CNAME
```

Sau bước này, site đã sống tại `https://acmeshop-static.sgp1.cdn.digitaloceanspaces.com/index.html`. Có một giới hạn cần biết trước để khỏi bất ngờ:

> Note: DO Spaces chưa có "static website hosting mode" với index.html mặc định ở root như S3. Nếu cần, đặt Cloudflare đứng trước Spaces và dùng Page Rules để rewrite đường dẫn.

### Phần B — Hóa đơn private (FastAPI)

Phần lõi của yêu cầu hóa đơn: backend kiểm tra quyền sở hữu trước, rồi mới cấp presigned URL có thời hạn ngắn. Endpoint dưới làm đúng trình tự đó — chặn ngay nếu invoice không thuộc về user đang đăng nhập, sau đó sinh URL hết hạn sau 10 phút:

```python
# app.py
from fastapi import FastAPI, HTTPException, Depends
import boto3
from botocore.client import Config
import os

app = FastAPI()

s3 = boto3.client(
    's3',
    region_name='sgp1',
    endpoint_url='https://sgp1.digitaloceanspaces.com',
    aws_access_key_id=os.environ['DO_SPACES_KEY'],
    aws_secret_access_key=os.environ['DO_SPACES_SECRET'],
    config=Config(signature_version='s3v4'),
)

@app.get("/invoice/{invoice_id}/download")
def download_invoice(invoice_id: str, user_id: str = Depends(get_current_user)):
    # Kiểm tra invoice thuộc user
    invoice = db.get_invoice(invoice_id)
    if invoice.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    # Generate presigned URL
    key = f"invoices/{user_id}/{invoice_id}.pdf"
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'acmeshop-uploads', 'Key': key},
        ExpiresIn=600,  # 10 phút
    )
    return {"download_url": url, "expires_in": 600}
```

Thử gọi endpoint bằng `curl`, ta nhận về URL tải kèm thời hạn:

```bash
# Test
curl -H "Authorization: Bearer TOKEN" \
    https://api.acmeshop.vn/invoice/INV-2026-001/download
# > {"download_url":"https://acmeshop-uploads.sgp1...?X-Amz-...","expires_in":600}
```

Browser của user chỉ việc GET cái `download_url` đó để tải PDF, và URL tự hết hiệu lực sau 10 phút. Kiểm tra quyền nằm ở backend, còn việc truyền file nặng thì để Spaces lo — đúng tinh thần "backend không làm trạm trung chuyển".

### Phần C — Upload avatar (presigned PUT)

Mảnh cuối: cho user upload avatar thẳng lên Spaces. Vì avatar là file public, ta cấp luôn `ACL: public-read` ngay trong URL upload và trả về sẵn `public_url` qua CDN để frontend dùng hiển thị:

```python
@app.post("/avatar/upload-url")
def get_avatar_upload_url(user_id: str = Depends(get_current_user)):
    key = f"avatars/{user_id}.jpg"
    url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'acmeshop-uploads',
            'Key': key,
            'ContentType': 'image/jpeg',
            'ACL': 'public-read',  # avatar public
        },
        ExpiresIn=600,
    )
    public_url = f"https://acmeshop-uploads.sgp1.cdn.digitaloceanspaces.com/{key}"
    return {"upload_url": url, "public_url": public_url}
```

Frontend lấy `upload_url`, PUT file lên, rồi dùng `public_url` để hiển thị avatar:

```javascript
const { upload_url, public_url } = await fetch('/avatar/upload-url').then(r => r.json());
await fetch(upload_url, {
    method: 'PUT',
    body: file,
    headers: { 'Content-Type': 'image/jpeg', 'x-amz-acl': 'public-read' }
});
console.log("Avatar at:", public_url);
```

Kết quả là cả vòng đời avatar không có byte nào đi qua backend: user bắn file thẳng lên Spaces, rồi đọc lại qua edge CDN gần nhất. Cùng với phần B, bạn đã có một hệ thống xử lý trọn vẹn cả file public lẫn private đúng như yêu cầu ban đầu — giờ chỉ còn né những cái bẫy hay gặp khi đưa lên production.

---

## 💡 Cạm bẫy thường gặp & Best practice

Phần này gom những lỗi mà gần như ai mới dùng Spaces cũng vấp ít nhất một lần. Mỗi mục nêu cái bẫy và cách thoát.

### ❌ Cạm bẫy 1 — Dùng PAT thay vì Spaces Access Key

Lấy PAT (Personal Access Token) ra làm key cho `s3cmd` rồi ngồi gãi đầu vì không kết nối được. PAT chỉ dành cho `doctl` và DigitalOcean API, hoàn toàn không phải credential của S3 API.

### ✅ Best practice 1

Spaces có hệ key riêng tại UI → API → Spaces Keys. Luôn tạo và dùng đúng loại key này cho mọi tool S3.

### ❌ Cạm bẫy 2 — Endpoint sai region

Space đặt ở `sgp1` nhưng lại trỏ tool về endpoint `nyc3.digitaloceanspaces.com`, kết quả là 404 dù file rõ ràng tồn tại.

### ✅ Best practice 2

Endpoint phải khớp region của Space theo đúng mẫu `<region>.digitaloceanspaces.com`.

### ❌ Cạm bẫy 3 — Quên bật public-read khi serve asset

Upload mặc định là private, nên user vào xem ảnh thì nhận 403 thay vì thấy ảnh.

### ✅ Best practice 3

Dùng `s3cmd put --acl-public` cho từng file, hoặc đặt bucket policy public-read cho cả Space khi nó chỉ chứa nội dung công khai.

### ❌ Cạm bẫy 4 — CORS để `AllowedOrigins: ["*"]`

Wildcard origin nghĩa là bất kỳ website nào cũng upload/đọc được — mở cửa cho CSRF (lừa user click để upload file rác dưới danh nghĩa họ) và scrape dữ liệu.

### ✅ Best practice 4

Liệt kê domain đích danh. Dev thì cho `http://localhost:3000`, production thì chỉ `https://acmeshop.vn`.

### ❌ Cạm bẫy 5 — Presigned URL expire quá dài

Đặt expire 7 ngày cho tiện, rồi user vô tình chia sẻ URL — thế là cả tuần ai có link cũng tải được.

### ✅ Best practice 5

Đặt expire ngắn (5-60 phút). Nếu cần chia sẻ lâu dài, sinh URL mới mỗi khi cần thay vì kéo dài hạn một URL.

### ❌ Cạm bẫy 6 — Không versioning rồi ghi đè production

Spaces **không có versioning**. Upload `index.html` mới đè lên bản cũ là bản cũ bay luôn, không có nút rollback.

### ✅ Best practice 6

Có vài cách phòng:

- Đặt version vào key: `index-v2.html`.
- Deploy hai stage: `dist/v1/`, `dist/v2/`, rồi chuyển CDN trỏ qua bản mới.
- Backup dữ liệu quan trọng: sync định kỳ sang S3 hoặc B2 độc lập.

### ❌ Cạm bẫy 7 — Lifecycle xóa nhầm dữ liệu quan trọng

Rule "xóa sau 7 ngày" đáng lẽ chỉ áp cho prefix `temp/` nhưng gõ nhầm path, quét luôn cả dữ liệu thật.

### ✅ Best practice 7

Test lifecycle trên một Space dev trước, và luôn verify bằng `aws s3api get-bucket-lifecycle-configuration` sau khi apply.

### ❌ Cạm bẫy 8 — CDN cache bản cũ

Cập nhật `style.css` nhưng user vẫn thấy giao diện cũ vì edge còn cache cả tiếng.

### ✅ Best practice 8

Chọn một trong các cách:

- Đặt version vào tên file: `style-v123.css`.
- Purge CDN: `doctl spaces cdn flush ID --files "/style.css"`.
- Đặt `Cache-Control` lúc upload: `--add-header "Cache-Control:no-cache"`.

### ❌ Cạm bẫy 9 — Multipart upload dở dang không dọn

Upload file lớn fail giữa chừng, các part đã lên vẫn nằm lại và vẫn bị tính tiền lưu trữ.

### ✅ Best practice 9

Thêm rule lifecycle để tự hủy multipart chưa hoàn tất:

```json
{ "ID": "abort-incomplete", "Status": "Enabled",
  "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 } }
```

### ❌ Cạm bẫy 10 — Tải ngược về Droplet vẫn tính băng thông

App trên Droplet GET ảnh từ Spaces về để resize, và mỗi lần kéo về như vậy đều tính vào băng thông outbound của Spaces.

### ✅ Best practice 10

Hai hướng tối ưu:

- Cùng region thì dùng internal network `https://<space>.<region>.digitaloceanspaces.com` — DigitalOcean không tính transfer nội vùng kể từ 2024.
- Hoặc serve thẳng cho user qua CDN, đừng để Droplet đứng giữa làm proxy.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Spaces khác Volume thế nào?

<details>
<summary>💡 Đáp án</summary>

- Volume = block storage, mount vào 1 Droplet, latency thấp, dung lượng cố định.
- Spaces = object storage, truy cập qua HTTP API, không mount, dung lượng vô hạn, latency cao hơn (50-200ms).
- Volume cho DB/OS disk; Spaces cho asset/backup.

</details>

**Q2.** Khi nào dùng Presigned URL?

<details>
<summary>💡 Đáp án</summary>

Khi file cần private (chỉ user có quyền xem) nhưng vẫn muốn user tải/upload trực tiếp từ Spaces (bypass backend proxy):
- Download: hóa đơn, file riêng tư của user.
- Upload: user upload avatar trực tiếp lên Spaces, backend chỉ tạo URL.

</details>

**Q3.** CDN của Spaces khác với CloudFront?

<details>
<summary>💡 Đáp án</summary>

- DO CDN: **miễn phí**, đi kèm Space, có PoP ở hàng trăm thành phố, ít tùy chọn cấu hình.
- CloudFront: tính phí $0.085/GB outbound, mạng edge lớn hơn, nhiều option (geo block, signed cookies, edge functions Lambda@Edge).

Spaces CDN đủ dùng cho web/asset cơ bản. Cần advanced (geo block, A/B test edge) → CloudFront hoặc Cloudflare đứng trước Spaces.

</details>

**Q4.** Lifecycle policy DO Spaces có gì khác S3?

<details>
<summary>💡 Đáp án</summary>

DO Spaces lifecycle hỗ trợ:
- Expire after N days.
- Abort incomplete multipart.

KHÔNG hỗ trợ (khác S3):
- Transition storage class (DO chỉ 1 class, không có Glacier).
- Noncurrent version expiration (DO không có versioning).

</details>

**Q5.** Vì sao **không** dùng `AllowedOrigins: ["*"]` trong CORS?

<details>
<summary>💡 Đáp án</summary>

Cho phép mọi origin upload/read → attacker site có thể CSRF (lừa user click → upload junk file dưới tên user) hoặc scrape data. Always list origin production cụ thể.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh |
|---|---|
| Tạo Space | `doctl spaces create NAME --region sgp1` |
| Config s3cmd | `s3cmd --configure` (endpoint: `sgp1.digitaloceanspaces.com`) |
| Upload | `s3cmd put file s3://SPACE/key` |
| Upload public | `s3cmd put file s3://SPACE/key --acl-public` |
| Sync folder | `s3cmd sync ./dist/ s3://SPACE/ --acl-public` |
| Download | `s3cmd get s3://SPACE/key file` |
| List | `s3cmd ls s3://SPACE/` |
| Delete | `s3cmd del s3://SPACE/key` |
| Set ACL bucket | `s3cmd setacl s3://SPACE --acl-public` |
| Bật CDN | `doctl spaces cdn create NAME --ttl 3600` |
| Purge CDN | `doctl spaces cdn flush ID --files "/path"` |
| Presigned URL (Python) | `client.generate_presigned_url('get_object', Params=..., ExpiresIn=600)` |
| Set lifecycle | `aws s3api put-bucket-lifecycle-configuration --bucket ... --endpoint-url=...` |
| Set CORS | `aws s3api put-bucket-cors --bucket ... --endpoint-url=...` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Object Storage** | Lưu trữ đối tượng | Storage theo key-value qua HTTP, không POSIX |
| **Space** | (giữ nguyên) | "Bucket" trong DO terminology |
| **Object** | Đối tượng | 1 file trong Space, có key + data + metadata |
| **Key** | Khoá | Đường dẫn đầy đủ identify object (`avatars/user-123.jpg`) |
| **Bucket** | (giữ nguyên) | Term chung S3 = Space trong DO |
| **S3-compatible** | Tương thích S3 API | Dùng được AWS SDK/CLI để gọi |
| **Presigned URL** | URL ký sẵn | URL có signature + expire, cho phép GET/PUT bypass auth |
| **CDN** | Mạng phân phối nội dung | Edge cache giảm latency global |
| **Origin** | Nguồn gốc | Server gốc lưu file (Space) |
| **PoP** | Point of Presence | Edge location của CDN |
| **TTL** | Time to Live | Thời gian cache trước khi refresh |
| **ACL** | Access Control List | Quyền truy cập (public-read, private) |
| **CORS** | Cross-Origin Resource Sharing | Header cho phép browser request cross-domain |
| **Lifecycle policy** | Chính sách vòng đời | Quy tắc auto-action (expire, transition) |
| **Multipart upload** | Upload nhiều phần | Chia file lớn thành chunks, upload song song |
| **Egress** | Băng thông ra | Lưu lượng dữ liệu rời cloud ra Internet, thường tính tiền |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Droplet + Block Storage Volumes — Compute cơ bản DO](01_droplets-and-volumes.md)
- ➡️ **Bài tiếp theo:** [Managed Databases — Postgres / MySQL / Redis / MongoDB / Kafka](03_managed-databases.md)
- ↑ **Về cụm:** [DigitalOcean](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — đối chiếu với object storage của AWS.
- ☁️ [GCP Cloud Storage](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md) — đối chiếu với object storage của Google Cloud.
- 🐍 [boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — SDK Python cho S3 và Spaces.

### 🌐 Tài nguyên tham khảo khác

- 📖 [DO Spaces docs](https://docs.digitalocean.com/products/spaces/) — tài liệu chính thức về Spaces.
- 📖 [Spaces API reference](https://docs.digitalocean.com/reference/api/spaces-api/) — tham chiếu API đầy đủ.
- 📖 [s3cmd usage](https://s3tools.org/usage) — hướng dẫn dùng s3cmd.
- 📖 [Spaces vs S3 comparison](https://www.digitalocean.com/blog/spaces-vs-s3) — so sánh chính thức từ DigitalOcean.
- 📖 [Cloudflare R2 docs](https://developers.cloudflare.com/r2/) — tài liệu của lựa chọn thay thế R2.
- 📖 [DO CDN docs](https://docs.digitalocean.com/products/spaces/how-to/enable-cdn/) — hướng dẫn bật CDN.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu. Object storage concept + Spaces S3-compatible + comparison S3/R2 + Access Key + s3cmd/boto3 + presigned URL + CDN built-in + Lifecycle + CORS + hands-on static site + private invoice + 10 pitfalls.
- **v2.0.0 (01/06/2026)** — Viết lại toàn bộ prose sang văn phong narrative tiếng Việt theo gold-standard (lời dẫn trước mỗi bảng/code, câu phân tích sau, ẩn dụ, câu bắc cầu giữa các phần); chuẩn hoá heading framework, field "Yêu cầu trước", Glossary 3 cột, nav (⬅️/➡️/↑ + link-text = tiêu đề thực); pitfall chuyển sang dạng ❌ Cạm bẫy / ✅ Best practice; sửa lỗi số đếm region (bỏ "4 region" mâu thuẫn với danh sách) và diễn đạt mềm số PoP CDN cho khớp tài liệu hiện hành; bổ sung thuật ngữ Egress vào Glossary. Giữ nguyên toàn bộ code/lệnh/config và số liệu kỹ thuật.
- **v2.0.1 (10/06/2026)** — Gắn mốc *tính đến 2026* cho bảng giá Spaces (§2) và bảng so giá Spaces/S3/R2 (§3) vì đơn giá biến động theo thời gian. Không đổi con số.
