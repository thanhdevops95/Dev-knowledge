# 🎓 Cloud Security & Shared Responsibility Model

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [03_storage-and-databases.md](03_storage-and-databases.md), khái niệm IAM cơ bản

> 🎯 *Đây là bài cuối của cụm cloud-fundamentals. Cloud có an toàn hơn on-prem không? **Có** — nhưng chỉ khi bạn cấu hình đúng. Chìa khoá nằm ở **Shared Responsibility Model**: vendor lo phần bảo mật **CỦA** cloud (security OF the cloud), còn bạn lo phần bảo mật **TRONG** cloud (security IN the cloud). Bài này đi qua: IAM, mã hoá (encryption), bảo mật mạng (network security), các khung tuân thủ (compliance frameworks), và những lỗi cấu hình phổ biến gây rò rỉ dữ liệu.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Shared Responsibility Model**: đâu là phần của vendor, đâu là phần của bạn
- [ ] Nắm nền tảng **IAM**: users, roles, policies, MFA
- [ ] Áp dụng **least privilege** (đặc quyền tối thiểu) + **temporary credentials** (chứng thực tạm thời)
- [ ] Hiểu **encryption**: at-rest, in-transit, KMS, BYOK
- [ ] Biết **network security**: SG, NACL, WAF, chống DDoS
- [ ] Quản lý **secrets**: không bao giờ nhét vào code
- [ ] Phân biệt các **compliance frameworks**: SOC 2, ISO 27001, HIPAA, PCI, GDPR
- [ ] Nhận diện các **vụ rò rỉ phổ biến** + cách phòng tránh

---

## Tình huống — Startup để S3 bucket public, dữ liệu khách hàng rò rỉ

Sáng thứ Hai, một startup nhận được email lạnh người. Người gửi là một *security researcher* (nhà nghiên cứu bảo mật) bên ngoài, không phải khách hàng, cũng không phải nhân viên:

- *"We discovered your S3 bucket `acme-data` is publicly readable. Customer PII (names, emails, addresses) of 100K users accessible to anyone with URL."*

Dịch ra: bucket `acme-data` của họ ai cũng đọc được, dữ liệu cá nhân (PII — *Personally Identifiable Information*) của 100 nghìn khách hàng phơi ra cho bất kỳ ai có đường link. Đội kỹ thuật kiểm tra lại và xác nhận tệ hơn tưởng tượng: bucket đã public suốt 6 tháng, bất kỳ ai cũng có thể chạy `aws s3 ls s3://acme-data/` rồi tải toàn bộ về.

Truy ngược nguyên nhân, mọi thứ bắt đầu từ một quyết định nhỏ:

- Một dev đặt quyền `Public Read` để test, rồi quên revert.
- Không có hệ thống cảnh báo (alert) nào phát hiện.
- Không có chu kỳ audit bảo mật định kỳ.

Hậu quả thì không hề nhỏ:

- Phạt theo GDPR: có thể lên tới 4% doanh thu hằng năm.
- Phải gửi thông báo cho từng khách hàng (yêu cầu pháp lý bắt buộc).
- Mất niềm tin, khách hàng rời bỏ (churn).
- Đội kỹ thuật phải gác mọi thứ để khắc phục.

Điểm mấu chốt cần nhớ ngay từ đầu: **khoảng 90% vụ rò rỉ trên cloud đến từ lỗi cấu hình (misconfiguration), không phải lỗi của vendor**. Cả bài này tồn tại để bạn không bao giờ rơi vào sáng thứ Hai đó.

---

## 1️⃣ Shared Responsibility Model

### Khái niệm

Bảo mật trên cloud không phải việc của riêng ai — nó là **trách nhiệm chia sẻ** giữa vendor và khách hàng. Vấn đề là đường ranh giới đôi khi mờ, và chính chỗ mờ đó là nơi tai nạn xảy ra. Sơ đồ dưới đây vẽ rõ đường phân chia: phần trên là việc của bạn, phần dưới là việc của vendor.

```text
┌─────────────────────────────────────────┐
│         YOUR responsibility             │
│  (Security IN the cloud)                 │
│                                          │
│  - Data (encryption, classification)     │
│  - IAM users, policies, MFA              │
│  - Network config (SG, NACL)             │
│  - App security (OWASP top 10)           │
│  - OS patching (IaaS only)               │
│  - Encryption keys (BYOK)                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       VENDOR responsibility             │
│  (Security OF the cloud)                 │
│                                          │
│  - Datacenter physical security          │
│  - Network infrastructure                │
│  - Hypervisor                            │
│  - Host OS (PaaS, SaaS)                  │
│  - Hardware                              │
└─────────────────────────────────────────┘
```

Nhìn sơ đồ thì thấy: càng lên cao trong stack, phần việc nghiêng về bạn càng nhiều. Vendor lo những thứ vật lý và hạ tầng bên dưới; còn data, danh tính, cấu hình mạng và bảo mật ứng dụng — những thứ dễ sai nhất — đều nằm trên vai bạn.

### Đường ranh giới dịch theo từng mô hình dịch vụ

Đường phân chia trên không cố định — nó **dịch chuyển** tuỳ theo bạn dùng mô hình dịch vụ nào. Quy luật chung: dịch vụ càng "managed" (được quản lý sẵn) thì vendor gánh càng nhiều, bạn lo càng ít.

- **IaaS — ví dụ EC2** (thuê máy ảo trần):
  - Vendor lo: phần cứng, *hypervisor* (lớp ảo hoá), datacenter, hạ tầng mạng.
  - Bạn lo: vá OS, ứng dụng, dữ liệu, IAM, Security Group.

- **PaaS — ví dụ Elastic Beanstalk, RDS** (nền tảng được quản lý):
  - Vendor lo: tất cả phần IaaS, **cộng thêm** OS, runtime, DB engine.
  - Bạn lo: code ứng dụng, dữ liệu, IAM, quy tắc mạng.

- **SaaS — ví dụ Workspaces, Chime** (phần mềm dùng ngay):
  - Vendor lo: tất cả phần PaaS, **cộng thêm** chính ứng dụng.
  - Bạn lo: dữ liệu bạn upload, danh tính người dùng (IAM users), cấu hình SSO.

### Vì sao điều này quan trọng

Shared Responsibility Model không phải khái niệm trừu tượng — nó **quyết định ai chịu hậu quả** khi có breach. AWS bảo mật datacenter, mã hoá disk vật lý, nhưng nếu bạn để S3 bucket public hoặc IAM key trên GitHub, đó là lỗi của bạn — vendor không bồi thường, audit ghi bạn vi phạm. Có ba điều cần khắc cốt ghi tâm:

- **Đừng mặc định vendor lo hết mọi thứ.**
- **Đừng đổ lỗi cho vendor về lỗi cấu hình của chính mình.**
- Khi audit + compliance: bạn phải tự chứng minh được phần bảo mật IN-cloud của mình.

Mô hình này là chuẩn của toàn ngành — AWS đặt ra, GCP và Azure cũng theo cùng triết lý, chỉ khác chi tiết tên dịch vụ.

🪞 **Ẩn dụ**: *Cloud giống như một **căn hộ chung cư cao cấp**. Chủ toà nhà (cloud vendor) lo: an ninh sảnh, camera lối đi chung, hệ thống cứu hoả, kết cấu toà nhà. Còn bạn lo: khoá cửa căn hộ, két sắt riêng, và ai được phép vào thăm. Toà nhà có an ninh đến đâu mà bạn để cửa căn hộ mở toang thì kẻ gian vẫn vào được — và đó là lỗi của bạn.*

---

## 2️⃣ IAM — Identity and Access Management

### Bốn khái niệm cốt lõi

IAM là hệ thống trả lời câu hỏi "ai được làm gì với tài nguyên nào". Trước khi viết policy, bạn cần phân biệt rạch ròi bốn khái niệm nền tảng, vì chúng hay bị dùng lẫn lộn:

- **User** (người dùng): danh tính của một con người — đăng nhập bằng username + password + MFA.
- **Group** (nhóm): tập hợp nhiều user để gán quyền hàng loạt.
- **Role** (vai trò): danh tính được *dịch vụ* (EC2, Lambda) hoặc *user* (truy cập cross-account) "mượn" tạm thời.
- **Policy** (chính sách): tài liệu JSON định nghĩa cụ thể quyền được phép làm gì.

### Ví dụ một policy

IAM policy là một **tài liệu JSON** gồm các *statement* — mỗi statement có Effect (Allow/Deny), Action (`s3:GetObject`...), Resource (ARN cụ thể), và optional Condition (chỉ áp dụng khi điều kiện đúng). Ví dụ dưới đây cho phép read + write đúng một bucket, đồng thời **chặn mọi request S3 không đi qua HTTPS** (đây là *defence-in-depth* — phòng thủ nhiều lớp):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-bucket/*"
    },
    {
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "*",
      "Condition": {
        "Bool": { "aws:SecureTransport": "false" }
      }
    }
  ]
}
```

Đọc policy này theo lối nói thường: cho phép get/put trên `my-bucket`, nhưng chặn thẳng mọi truy cập S3 đi qua HTTP — bắt buộc phải HTTPS. Statement Deny luôn thắng Allow, nên đây là một lớp khoá an toàn dù bạn lỡ cấp quyền rộng ở chỗ khác.

### Nguyên tắc: Least privilege (đặc quyền tối thiểu)

Nguyên tắc vàng của IAM: chỉ cấp đúng quyền cần thiết, không hơn một ly. So sánh hai cực dưới đây sẽ thấy rõ vì sao.

Đây là **anti-pattern** (kiểu làm sai) kinh điển — cấp toàn quyền:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

Policy này chính là `AdministratorAccess`. ⚠️ Đừng bao giờ dùng cho công việc hằng ngày — chỉ cần một key rò rỉ là toàn bộ tài khoản sụp đổ.

Còn đây là **cách đúng** — chỉ mở đúng quyền cần, đúng tài nguyên cụ thể:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::my-app/data/*"
}
```

Khác biệt là cả một trời vực: cái sau chỉ cho đọc đúng một đường dẫn trong một bucket, không hơn.

### MFA — Multi-Factor Authentication (xác thực đa yếu tố)

Mật khẩu rò rỉ là chuyện thường ngày. MFA thêm một lớp thứ hai (thứ bạn *có*, ngoài thứ bạn *biết*), khiến kẻ trộm mật khẩu vẫn không vào được. Những đối tượng **bắt buộc** phải bật MFA:

- Root account (luôn luôn, không có ngoại lệ).
- IAM user có quyền truy cập console.
- IAM user có quyền cao (high-privilege).

Các phương thức MFA, xếp theo độ an toàn:

- TOTP — mã một lần theo thời gian (Google Authenticator, Authy).
- Hardware key — khoá vật lý (YubiKey, AWS U2F): an toàn nhất.
- SMS — kém an toàn nhất, tránh dùng nếu được (dễ bị SIM-swap).

Bạn còn có thể **ép buộc MFA bằng policy**, chặn mọi hành động nếu phiên đăng nhập chưa qua MFA:

```json
{
  "Condition": {
    "Bool": { "aws:MultiFactorAuthPresent": "false" }
  },
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*"
}
```

Policy này nói thẳng: nếu MFA không hiện diện trong phiên, từ chối làm mọi thứ. Đây là cách biến MFA từ "khuyến khích" thành "bắt buộc về mặt kỹ thuật".

### Service roles — không dùng static credentials

Một sai lầm phổ biến là nhét access key cứng vào máy chủ. Hãy xem **anti-pattern** này:

```text
EC2 instance has AWS access key in environment variable.
Key leaked → AWS account compromised.
```

Vấn đề: key tĩnh nằm trong biến môi trường, rò một lần là kẻ gian dùng được mãi mãi. Cách đúng là dùng **IAM role cho EC2** (hoặc IRSA nếu chạy trên K8s) — máy chủ "mượn" quyền tạm thời thay vì giữ key:

```text
EC2 assumes IAM role.
AWS provides temporary credentials (1-hour TTL).
Auto-rotated.
Never in environment.
```

Triển khai bằng Terraform, ta tạo role + gắn vào instance qua *instance profile*, hoàn toàn không cần access key:

```hcl
resource "aws_iam_role" "app" {
  name = "app-role"
  assume_role_policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "app" {
  name = "app-profile"
  role = aws_iam_role.app.name
}

resource "aws_instance" "app" {
  ami = "ami-xxx"
  iam_instance_profile = aws_iam_instance_profile.app.name
  # No access keys needed!
}
```

Bên trong EC2, AWS SDK tự lấy chứng thực tạm thời từ *instance metadata* (dịch vụ metadata nội bộ của máy ảo). Không một dòng key nào nằm trong code — và chứng thực tự hết hạn, tự xoay vòng.

### IRSA — IAM Roles for Service Accounts (cho EKS)

Trên Kubernetes, ta cũng muốn pod "mượn" IAM role thay vì cắm key. IRSA làm chính việc đó bằng cách map một *ServiceAccount* của K8s sang một IAM role:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/app-role
```

Pod nào dùng ServiceAccount này thì AWS SDK trong pod sẽ tự assume IAM role tương ứng — vẫn theo đúng tinh thần "không có key tĩnh" như service role của EC2.

### Permission boundaries (giới hạn quyền tối đa)

Có một tình huống khó: bạn muốn cho dev tự tạo role, nhưng không muốn họ tạo role quyền lực hơn cả mình. *Permission boundary* là trần quyền — dù policy có ghi `*` đi nữa, principal cũng không vượt được trần này:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "StringNotEquals": {
        "aws:RequestedRegion": ["us-east-1", "us-west-2"]
      }
    }
  }]
}
```

Với boundary này, kể cả một admin cũng chỉ thao tác được trong `us-east-1` và `us-west-2`. Rất hữu ích cho môi trường sandbox hoặc khi giao quyền tạo role cho team.

### Vài pattern IAM thường dùng

Trong thực tế, các tổ chức trưởng thành thường gom IAM về vài mẫu thiết kế quen thuộc. Ba mẫu phổ biến nhất:

1. **Tách tài khoản người và máy:**
   - Người: IAM user, ép MFA.
   - Máy: IAM role, không có quyền truy cập console.

2. **Dùng AWS SSO (IAM Identity Center):**
   - Danh tính tập trung (Google Workspace, Okta, AD).
   - Single sign-on xuyên nhiều tài khoản AWS.
   - Chứng thực tạm thời, tự hết hạn.

3. **Cross-account access (truy cập liên tài khoản):**
   - Tài khoản A có role.
   - User của tài khoản B assume role đó.
   - Cho phép quản lý tập trung thay vì phân tán.

---

## 3️⃣ Encryption — Mã hoá at-rest + in-transit

### Mã hoá at-rest (dữ liệu khi nằm yên)

Mã hoá at-rest nghĩa là dữ liệu được mã hoá ngay trên đĩa. Lý do cần nó nghe hơi xa nhưng rất thực: kẻ gian đánh cắp ổ cứng vật lý, đĩa bị tái sử dụng mà chưa xoá sạch, hay một bản snapshot bị lộ — trong mọi trường hợp, nếu dữ liệu đã mã hoá thì kẻ lấy được cũng chỉ thấy một mớ bit vô nghĩa.

Trên AWS, hầu hết dịch vụ lưu trữ đều hỗ trợ sẵn:

- **S3**: SSE-S3 (mặc định từ 2026), SSE-KMS, SSE-C.
- **EBS**: mã hoá at-rest bằng KMS.
- **RDS**: mã hoá at-rest (snapshot cũng được mã hoá theo).
- **DynamoDB**: mã hoá mặc định, không cần bật.

Câu hỏi tiếp theo luôn là "ai giữ chìa khoá?". Đây là các lựa chọn quản lý khoá, từ tiện đến kiểm soát chặt:

- **AWS managed**: AWS sở hữu khoá, miễn phí, bạn không kiểm soát.
- **Customer managed (KMS)**: bạn kiểm soát, có audit log, giá khoảng $1/khoá/tháng.
- **BYOK** (Bring Your Own Key): bạn tự import key material vào.
- **External (CloudHSM)**: khoá nằm trong phần cứng chuyên dụng (HSM).

### Mã hoá in-transit (dữ liệu khi di chuyển)

Mã hoá in-transit là mã hoá dữ liệu trên đường truyền mạng. Nó chống lại *man-in-the-middle* (kẻ chen giữa) và nghe lén — những kẻ ngồi giữa hai đầu kết nối để đọc trộm gói tin.

Chuẩn nên dùng cho năm 2026:

- **TLS 1.3** (tối thiểu phải là 1.2).
- **HTTPS** cho web traffic.
- **mTLS** (TLS hai chiều) cho giao tiếp service-to-service trong microservices.
- **VPN** cho kết nối site-to-site.

Và quan trọng là phải **ép buộc**, đừng chỉ "khuyến khích":

- ALB / CloudFront: chỉ cho HTTPS, redirect HTTP → HTTPS.
- S3 bucket policy: chặn truy cập không phải HTTPS (như ví dụ JSON ở phần IAM).
- RDS: yêu cầu SSL.

### KMS — Key Management Service

**KMS** là dịch vụ quản lý khoá mã hoá được AWS quản lý sẵn. Thay vì tự xây hệ thống giữ khoá (vừa khó vừa nguy hiểm), bạn để KMS giữ và phục vụ khoá. Vài lệnh cơ bản:

```bash
# Create CMK (Customer Master Key)
aws kms create-key --description "App encryption key"

# Encrypt data
aws kms encrypt --key-id alias/app-key --plaintext "secret data"

# Decrypt
aws kms decrypt --ciphertext-blob ...
```

KMS được dùng ở khắp nơi: làm khoá cho S3 SSE-KMS, mã hoá EBS, đứng sau Secrets Manager, hoặc mã hoá trực tiếp những mẩu dữ liệu nhỏ.

Nhưng KMS có một giới hạn: nó không nhận dữ liệu lớn. Với dữ liệu lớn, ta dùng kỹ thuật **envelope encryption** (mã hoá phong bì) — mã hoá dữ liệu bằng một khoá cục bộ, rồi chỉ gửi *khoá đó* cho KMS mã hoá:

1. KMS sinh ra một *data key*.
2. Mã hoá dữ liệu bằng data key (làm tại chỗ, không gửi data đi đâu).
3. Mã hoá chính data key đó bằng KMS.
4. Lưu lại: dữ liệu đã mã hoá + data key đã mã hoá.

Cách này hiệu quả vì dữ liệu lớn không bao giờ phải đi qua KMS — chỉ có khoá nhỏ mới đi.

### Mã hoá ở mọi điểm

Production năm 2026 đòi hỏi mã hoá **end-to-end** — không có chỗ nào dữ liệu đi qua dưới dạng plaintext. Sơ đồ dưới minh hoạ ý đó: TLS từ browser tới CloudFront, rồi TLS tới ALB, rồi TLS tới EC2, rồi TLS tới RDS, và đĩa EBS được KMS mã hoá at-rest. Mỗi chặng là một lớp khoá:

```text
User browser ──TLS──→ CloudFront ──TLS──→ ALB ──TLS──→ EC2
                                                       ↓
                                                  TLS to RDS
                                                       ↓
                                                  KMS-encrypted EBS
```

Toàn tuyến không có một mắt xích hở. Đây là tư duy "mã hoá ở mọi điểm" mà các khung compliance như SOC 2 hay HIPAA đều yêu cầu.

---

## 4️⃣ Network security

### Defense in depth (phòng thủ nhiều lớp)

Không có một lớp phòng thủ nào là hoàn hảo, nên triết lý ở đây là xếp nhiều lớp — lớp này thủng thì lớp kia vẫn đỡ. Đi từ ngoài vào trong:

1. **Edge** (CloudFront + WAF): chặn bot, chặn theo địa lý.
2. **Network** (SG, NACL): giới hạn cổng + IP.
3. **Host** (firewall OS): thêm quy tắc ở cấp máy.
4. **App** (auth + kiểm tra input): tầng logic ứng dụng.
5. **Data** (encryption): lớp cuối cùng.

Ý nghĩa của cách xếp này: một lớp thủng thì các lớp còn lại vẫn bảo vệ. Kẻ tấn công phải vượt qua tất cả mới chạm được dữ liệu.

### Security Group + NACL

Hai lớp network ở trên dựa vào hai công cụ chính (đã đào sâu ở bài 02), khác nhau ở chỗ:

- **SG** (Security Group): *stateful* (nhớ trạng thái), chỉ cho phép (allow-only), gắn theo từng tài nguyên.
- **NACL**: *stateless* (không nhớ trạng thái), cho phép cả allow lẫn deny, gắn theo subnet.

### Web Application Firewall (WAF)

**WAF** lọc HTTP traffic theo luật, đứng chắn trước ứng dụng để loại bỏ request độc hại trước khi chúng tới được app. Những thứ WAF thường chặn:

- SQL injection.
- XSS (cross-site scripting).
- Command injection.
- Các mẫu hành vi của bot.
- Chặn theo địa lý (block cả một quốc gia).

Với **AWS WAF**, cách dùng điển hình:

- Gắn vào CloudFront, ALB, hoặc API Gateway.
- Luật có thể là *managed* (do AWS hoặc OWASP cung cấp sẵn) hoặc *custom*.
- Hỗ trợ rate limiting theo từng IP.

Ngoài AWS WAF còn vài lựa chọn thay thế:

- **Cloudflare WAF**: đi kèm trong gói dịch vụ.
- **AWS Shield**: chuyên chống DDoS (bản Advanced giá $3000/tháng).

### Chống DDoS

DDoS có hai loại, và cách phòng cũng khác nhau, nên cần phân biệt rõ:

- **Layer 3/4 DDoS** (flood ở tầng mạng): cloud vendor tự động giảm thiểu ở cấp hạ tầng, bạn gần như không phải làm gì.
- **Layer 7 DDoS** (flood ở tầng ứng dụng): cần WAF + rate limiting, vì đây là request "trông giống thật".

Công cụ thường dùng:

- AWS Shield Standard (miễn phí, cơ bản).
- AWS Shield Advanced ($3000/tháng, cao cấp).
- Cloudflare Pro trở lên (chống DDoS không giới hạn dung lượng).

### Bastion / Jump host

Để vào shell của máy chủ trong private subnet, ngày xưa người ta dựng một *bastion host* (máy bắc cầu). Đây là **pattern cũ**: một EC2 bastion đặt ở public subnet, từ đó SSH vào EC2 private.

**Cách hiện đại 2026** là **AWS Systems Manager Session Manager** — không cần bastion, không cần mở cổng SSH:

```bash
aws ssm start-session --target i-abc123
# Direct shell, IAM auth, no SSH key, audit log
```

Bạn vào thẳng shell, xác thực bằng IAM, không có SSH key để mất, mọi phiên đều được ghi log. Lợi ích lớn nhất: xoá bỏ hoàn toàn bề mặt tấn công của cổng SSH.

---

## 5️⃣ Secrets management

### Các anti-pattern (đừng bao giờ làm)

Secret (mật khẩu, API key, token) bị lộ là một trong những nguyên nhân rò rỉ phổ biến nhất — và phần lớn đến từ ba thói quen sai dưới đây.

Thứ nhất, ❌ nhét secret thẳng vào code:

```python
DATABASE_PASSWORD = "supersecret123"   # Will leak in Git
```

Dòng này sẽ đi thẳng vào lịch sử Git và nằm đó mãi mãi.

Thứ hai, ❌ nhét secret vào biến môi trường ngay trong Dockerfile:

```dockerfile
ENV DATABASE_PASSWORD=secret    # in image layer history
```

Secret này bị "đóng băng" vào layer history của image, ai pull image về cũng moi ra được.

Thứ ba, ❌ in secret ra log CI:

```yaml
- run: echo $DATABASE_PASSWORD    # leaked to logs
```

Một dòng `echo` vô tình là secret nằm trong log CI cho cả team xem.

### Các giải pháp đúng

Thay vì ba cách trên, hãy đẩy secret ra ngoài và gọi vào lúc runtime. Lựa chọn phổ biến nhất là **AWS Secrets Manager**:

- Lưu secret được mã hoá bằng KMS.
- Tự động xoay vòng (auto-rotation) sẵn cho RDS, Redshift.
- Ghi audit log qua CloudTrail.

```python
import boto3
secrets = boto3.client('secretsmanager')
db_password = secrets.get_secret_value(SecretId='prod/db/password')['SecretString']
```

Code chỉ giữ *tên* của secret, còn giá trị thật lấy về lúc chạy — không có gì để lộ trong source. Vài lựa chọn khác tuỳ ngữ cảnh:

- **AWS Parameter Store**: rẻ hơn (bản Standard miễn phí), hỗ trợ đường dẫn phân cấp.
- **Vault** (HashiCorp): đa cloud, cấp chứng thực động — sẽ đào sâu ở CI/CD intermediate bài 03.
- **External Secrets Operator** (cho K8s): đồng bộ từ kho ngoài vào K8s Secrets.

### Quét secret trước khi commit (pre-commit)

Phòng bệnh hơn chữa bệnh: chặn secret ngay tại bước commit, trước khi nó kịp vào lịch sử Git. Công cụ phổ biến là *gitleaks*:

```yaml
# .pre-commit-config.yaml
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.20.0
  hooks:
    - id: gitleaks
```

Hook này phát hiện AWS key, GitHub token, Stripe key... ngay khi bạn định commit, và chặn lại trước khi quá muộn.

### GitHub secret scanning

GitHub tự động quét các public repo để tìm các mẫu secret đã biết. Nếu phát hiện, nó sẽ:

- Báo cho chủ repo.
- Với một số đối tác (AWS, Stripe), tự động vô hiệu hoá key bị lộ.

Đây là lưới an toàn miễn phí cho các dự án open source — nhưng đừng coi nó là tuyến phòng thủ chính.

---

## 6️⃣ Compliance frameworks

### Các khung phổ biến

Compliance không phải "một chuẩn cho mọi loại". Mỗi framework phục vụ một domain riêng — SaaS B2B cần SOC 2, healthcare cần HIPAA, payment cần PCI DSS, có user EU thì cần GDPR. Đa số startup khi scale lên sẽ gặp đồng thời 3-4 framework. Bảng dưới giúp bạn scope đúng audit nào cần làm:

| Framework | Domain | Áp dụng cho |
|---|---|---|
| **SOC 2** | Tiêu chí dịch vụ tin cậy (Trust services criteria) | SaaS B2B (yêu cầu khi bán hàng) |
| **ISO 27001** | Quản lý an toàn thông tin | Doanh nghiệp quốc tế |
| **HIPAA** | Quyền riêng tư dữ liệu y tế (Mỹ) | Ứng dụng healthcare |
| **PCI DSS** | Dữ liệu thẻ tín dụng | Xử lý thanh toán |
| **GDPR** | Quy định bảo mật của EU | Có user ở EU |
| **CCPA** | Bảo mật người tiêu dùng California | Có user California |
| **FedRAMP** | Dữ liệu chính phủ liên bang Mỹ | Bán cho chính phủ Mỹ |
| **HITRUST** | Khung tổng hợp cho healthcare | Healthcare cần nhiều framework |
| **PIPEDA** | Bảo mật của Canada | Có user Canada |

Nhìn bảng thấy ngay nguyên tắc: bạn phục vụ thị trường nào, ngành nào, thì framework tương ứng "tự tìm đến". Không ai làm hết một lúc — bạn làm theo nhu cầu thực tế của khách hàng và pháp lý.

### Compliance là lợi thế cạnh tranh

Compliance không chỉ là "tránh phạt" — nó là một **chiến lược kinh doanh**. Enterprise B2B sẽ yêu cầu SOC 2 trước khi ký hợp đồng; healthcare cần HIPAA BAA mới được đụng vào dữ liệu PHI; thanh toán thẻ phải qua PCI DSS. Đầu tư vào audit chính là mở khoá thị trường — không có compliance đồng nghĩa mất deal:

- **B2B SaaS** khi bán hàng: SOC 2 gần như bắt buộc (audit từ $5K+/năm).
- **Healthcare**: HIPAA BAA (Business Associate Agreement — thoả thuận đối tác xử lý dữ liệu).
- **Payment**: cấp độ PCI tuỳ theo khối lượng giao dịch.
- **Có user EU**: tuân thủ GDPR.

Nói cách khác, compliance là tấm vé vào cửa thị trường, không phải gánh nặng thuần tuý.

### Cloud vendor và compliance

Một tin tốt: AWS/GCP/Azure đều đã được chứng nhận sẵn cho phần lớn framework ở cấp hạ tầng:

- SOC 2 ✓
- ISO 27001 ✓
- HIPAA (kèm BAA) ✓
- PCI DSS Level 1 ✓
- FedRAMP High (GovCloud) ✓

Nhưng đừng hiểu lầm: cloud chỉ cung cấp **hạ tầng tuân thủ**. Phần tuân thủ cho *ứng dụng của bạn* thì **bạn** phải tự làm — vendor không gánh thay.

### Checklist SOC 2 mẫu (mức tổng quan)

Để hình dung một audit thực tế trông thế nào, đây là các nhóm kiểm soát điển hình mà một kỳ SOC 2 sẽ soi:

- **Access control**: IAM kèm MFA, least privilege.
- **Encryption**: at-rest + in-transit.
- **Logging**: mọi hành động admin đều được ghi (CloudTrail).
- **Monitoring**: cảnh báo cho các sự kiện bảo mật.
- **Incident response**: quy trình xử lý sự cố có tài liệu.
- **Background checks**: kiểm tra lý lịch nhân viên có quyền truy cập prod.
- **Vendor management**: rà soát bảo mật bên thứ ba.
- **Change management**: deploy theo quy trình PR.
- **Backup + DR**: kiểm tra khôi phục định kỳ hằng quý.
- **Code review**: bắt buộc cho mọi thay đổi.

Việc tự tay làm tất cả những bằng chứng này rất tốn công, nên có các công cụ như **Vanta**, **Drata**, **SecureFrame** tự động thu thập bằng chứng giúp bạn.

### GDPR cơ bản

GDPR (sẽ chi tiết hơn ở bài 01) đặt ra một loạt nghĩa vụ với dữ liệu của người dùng EU mà bạn cần nắm:

- *Data residency*: dữ liệu EU phải ở region EU.
- Quyền được xem + xoá dữ liệu cá nhân của user.
- *Data Processing Agreement* (thoả thuận xử lý dữ liệu).
- *DPO* (Data Protection Officer) nếu xử lý một số loại dữ liệu nhất định.
- Thông báo breach trong vòng 72 giờ.

---

## 7️⃣ Các vụ rò rỉ phổ biến + cách phòng

Lý thuyết là vậy, nhưng cách học nhanh nhất là nhìn vào những vụ rò rỉ có thật và đảo ngược chúng thành bài học phòng thủ. Dưới đây là sáu kịch bản gặp nhiều nhất.

### Vụ 1: S3 bucket public

**Kịch bản**: một dev đặt bucket public để test rồi quên đi (chính là tình huống mở bài).

**Cách phòng**:

1. Bật **Block Public Access** ở cấp tài khoản:
   ```bash
   aws s3control put-public-access-block --account-id <ID> \
     --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
   ```
2. Dùng luật **AWS Config** để phát hiện bucket public.
3. **Audit hằng tháng** với Macie hoặc AWS Trusted Advisor.

### Vụ 2: AWS access key bị lộ trên Git

**Kịch bản**: dev commit `aws_access_key_id` lên public GitHub. Bot quét được, lấy key, đào bitcoin trên tài khoản của bạn.

**Cách phòng**:

1. **Pre-commit hook**: gitleaks.
2. **GitHub secret scanning**: cảnh báo.
3. **Không dùng key tĩnh**: chuyển sang IAM role + SSO.
4. **MFA + Conditional access**: chặn nếu không có MFA.
5. **Billing alert**: phát hiện chi phí bất thường sớm.

### Vụ 3: Mật khẩu DB yếu

**Kịch bản**: Postgres để `admin/password`. Bot brute force trong vài phút.

**Cách phòng**:

1. **Mật khẩu mạnh**: ngẫu nhiên, 24+ ký tự.
2. **Secrets Manager**: tự động xoay vòng.
3. **DB trong private subnet**: không phơi ra internet.
4. **IAM database auth** (RDS Postgres): không mật khẩu, dùng IAM token.

### Vụ 4: SSRF trong app → đánh cắp cloud credentials

**Kịch bản**: app có lỗ hổng SSRF (*Server-Side Request Forgery*). Kẻ tấn công ép app gọi `http://169.254.169.254/` (endpoint metadata của EC2) → lấy được AWS credentials.

**Cách phòng**:

1. **IMDSv2**: yêu cầu session token (giảm thiểu SSRF).
2. **Kiểm tra input của app**: chặn SSRF từ gốc.
3. **WAF rules**: chặn IP metadata trong các request đi ra.

### Vụ 5: CI/CD pipeline bị xâm nhập

**Kịch bản**: deploy key của GitHub Actions bị lộ. Kẻ tấn công đẩy code độc vào.

**Cách phòng**:

1. **OIDC thay cho key sống lâu**: GitHub Actions → AWS qua OIDC token tạm thời.
2. **Branch protection**: bắt buộc review.
3. **Signed commits**: GPG/Sigstore.
4. **Code signing**: cosign cho image.

### Vụ 6: Insider threat (mối đe doạ nội bộ)

**Kịch bản**: nhân viên bất mãn xoá dữ liệu trước khi nghỉ việc.

**Cách phòng**:

1. **Audit logging**: mọi hành động vào CloudTrail.
2. **Least privilege**: thu hồi quyền không cần thiết.
3. **Break-glass procedures**: chỉ dùng trong khẩn cấp.
4. **Backup**: lưu trữ bất biến (immutable).
5. **Offboarding checklist**: thu hồi quyền ngay khi nghỉ việc.

---

## 8️⃣ Công cụ 2026 — Cloud security ops

Khi hệ thống lớn lên, bạn không thể kiểm tra bảo mật bằng tay. Phần này điểm qua các công cụ vận hành bảo mật cloud, chia làm hai nhóm: native của AWS và bên thứ ba.

### AWS native

Đây là bộ công cụ "cây nhà lá vườn" của AWS, tích hợp sẵn, thường là điểm khởi đầu rẻ và nhanh nhất:

| Công cụ | Dùng để |
|---|---|
| **IAM Access Analyzer** | Phát hiện policy cấp quyền quá rộng |
| **AWS Config** | Luật compliance, phát hiện cấu hình lệch (drift) |
| **CloudTrail** | Audit log các API call |
| **GuardDuty** | Phát hiện mối đe doạ (dựa trên ML) |
| **Security Hub** | Tổng hợp các phát hiện |
| **Macie** | Phát hiện PII trong S3 |
| **Inspector** | Quét lỗ hổng EC2/Lambda |
| **Detective** | Điều tra pháp y (forensic) |
| **CloudFormation Guard** | Kiểm tra compliance của IaC |

### Bên thứ ba

Khi nhu cầu vượt khỏi phạm vi native (đa cloud, posture toàn diện, tự động hoá compliance), các công cụ bên thứ ba bù vào khoảng trống:

| Công cụ | Dùng để |
|---|---|
| **Wiz** | Quản lý tư thế bảo mật cloud (CSPM) |
| **Lacework** | Workload + posture |
| **Snyk** | Quét code + IaC |
| **Checkov** | Quét IaC (Terraform) |
| **tfsec** | Quét bảo mật Terraform |
| **Prowler** | Audit AWS |
| **ScoutSuite** | Audit đa cloud |
| **Vanta / Drata / SecureFrame** | Tự động hoá compliance |

### Bộ công cụ nền tảng khuyến nghị 2026

Không cần dùng hết mọi thứ ngay — quy mô đến đâu chọn đến đó.

Với **startup**, bộ tối thiểu mà hiệu quả:

- IAM Access Analyzer (miễn phí).
- GuardDuty (khoảng $30/tháng cho tài khoản nhỏ).
- Config (tính phí theo luật).
- Macie (audit S3 hằng quý).
- tfsec trong CI.
- gitleaks pre-commit.

Với **enterprise**, bổ sung thêm:

- Security Hub (bộ tổng hợp).
- Wiz / Lacework (CSPM).
- Vanta (tự động hoá compliance).

---

## 9️⃣ Hands-on: Thiết lập baseline an toàn cho tài khoản AWS mới

Lý thuyết đã đủ — giờ ta dựng một "ngày đầu tiên" an toàn cho một tài khoản AWS trắng. Mười bước dưới đây là baseline tối thiểu mà mọi tài khoản production nên có ngay từ đầu.

### Bước 1: Khoá root account

1. Bật MFA hardware key cho root account.
2. Không bao giờ dùng root cho công việc hằng ngày.
3. Cất chứng thực root vào két offline.

### Bước 2: Chặn truy cập public S3

```bash
aws s3control put-public-access-block --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

### Bước 3: Bật CloudTrail

```bash
aws cloudtrail create-trail \
  --name acme-trail \
  --s3-bucket-name acme-cloudtrail-logs \
  --is-multi-region-trail \
  --include-global-service-events
```

Từ đây trở đi, mọi API call đều được ghi log — nền tảng cho mọi cuộc điều tra sau này.

### Bước 4: Bật GuardDuty

```bash
aws guardduty create-detector --enable
```

GuardDuty bắt đầu phát hiện mối đe doạ dựa trên ML.

### Bước 5: IAM Access Analyzer

```bash
aws accessanalyzer create-analyzer \
  --analyzer-name acme-analyzer \
  --type ACCOUNT
```

Công cụ này tìm các đường truy cập cross-account ngoài ý muốn.

### Bước 6: Baseline luật Config

```bash
# Enable Config recorder
aws configservice put-configuration-recorder --configuration-recorder name=default,roleARN=arn:aws:iam::ROLE

# Subscribe to AWS managed rules
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "s3-bucket-public-read-prohibited",
  "Source": { "Owner": "AWS", "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED" }
}'
```

Config sẽ tự động phát hiện tài nguyên không tuân thủ.

### Bước 7: Thiết lập cảnh báo

```yaml
# CloudWatch alarms
- Billing alert if > $500/month
- GuardDuty critical findings → SNS → Slack
- CloudTrail root user activity → alert
- Failed login spike → alert
```

### Bước 8: Chính sách backup

- **AWS Backup**: tự động, cross-region.
- Snapshot hằng ngày, giữ 30 ngày.
- Kiểm tra khôi phục hằng quý.

### Bước 9: Mặc định mạng

- VPC mặc định: xoá (không dùng tới).
- VPC tự tạo: subnet theo từng AZ, NAT, SG phân lớp.
- Chặn cổng 22, 3389 tới `0.0.0.0/0`.
- Dùng Session Manager để vào shell.

### Bước 10: Baseline compliance

- Bật mã hoá at-rest mặc định (S3, EBS, RDS).
- Ép HTTPS qua bucket policy.
- Lập tài liệu cho các kiểm soát bảo mật.
- Lên lịch audit nội bộ hằng quý.

Đây mới là baseline **ngày đầu tiên** — hãy xây tiếp lên trên nền này.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Dùng root account hằng ngày

Root account là chìa khoá vạn năng — bất kỳ sự xâm nhập nào cũng đồng nghĩa mất trắng cả tài khoản.

→ **Fix**:
- Bật MFA hardware cho root.
- Không dùng root hằng ngày.
- Tạo IAM admin user riêng cho việc vận hành.

### ❌ Cạm bẫy: Access key sống lâu

Key nằm trong laptop → laptop bị mất → key vẫn dùng được mãi mãi.

→ **Fix**:
- IAM roles + IAM Identity Center (SSO).
- Chứng thực tạm thời (1-12 giờ).
- Tự xoay vòng ở nơi có thể.

### ❌ Cạm bẫy: SG mở `0.0.0.0/0` tới dịch vụ nội bộ

DB phơi thẳng ra internet.

→ **Fix**:
- SG của DB: chỉ cho phép từ SG của app.
- Audit SG hằng quý.
- Dùng Inspector / Prowler.

### ❌ Cạm bẫy: Không bật CloudTrail

Không có audit trail thì không thể điều tra khi sự cố xảy ra.

→ **Fix**: CloudTrail multi-region, bật ngay từ ngày đầu.

### ❌ Cạm bẫy: S3 bucket public "để serve ảnh"

Thường bị cấu hình rộng hơn ý định ban đầu.

→ **Fix**: đặt CloudFront ở phía trước, bucket để private, dùng signed URL hoặc OAI.

### ❌ Cạm bẫy: Compliance "để năm sau"

Khách hàng yêu cầu SOC 2 → cuống cuồng chạy nước rút.

→ **Fix**: xây với compliance ngay từ ngày đầu; dùng Vanta / Drata để tự động hoá.

### ❌ Cạm bẫy: Không có kế hoạch ứng phó sự cố

Breach xảy ra → lúng túng, phản ứng chậm, thiệt hại lan rộng.

→ **Fix**:
- Có kế hoạch IR (incident response) bằng văn bản.
- Runbook cho các kịch bản thường gặp.
- Diễn tập tabletop hằng quý.

### ✅ Best practice: IAM Identity Center cho SSO

Danh tính tập trung qua Okta / Google Workspace / AD:
- Một tài khoản, truy cập nhiều nơi.
- Phân quyền theo nhóm.
- Tự thu hồi khi offboarding.

### ✅ Best practice: Defense in depth

```text
WAF (edge) → ALB SG (network) → EC2 SG (instance) → app auth (logic) → DB SG + encrypt (data)
```

Một lớp thủng, các lớp còn lại vẫn bảo vệ.

### ✅ Best practice: Mã hoá ở mọi điểm

- S3: SSE-KMS mặc định.
- EBS: mã hoá at-rest.
- RDS: mã hoá at-rest.
- TLS in-transit ở khắp nơi.
- Secret để trong Secrets Manager.

### ✅ Best practice: Audit + alert

- Hằng ngày: bất thường chi phí, các phát hiện bảo mật.
- Hằng tuần: audit SG, rà soát IAM.
- Hằng tháng: kiểm tra compliance, lỗ hổng dependency.
- Hằng quý: pentest, diễn tập DR, rà soát postmortem.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Shared responsibility model — với EC2 thì vendor cụ thể lo những gì?

<details>
<summary>💡 Đáp án</summary>

Đầu tiên là phần **của AWS (Security OF the cloud)**:

1. **Bảo mật vật lý**:
   - Kiểm soát ra vào datacenter.
   - Giám sát (surveillance).
   - Hệ thống chữa cháy.

2. **Hạ tầng**:
   - Phần cứng mạng (switch, router).
   - Phần cứng lưu trữ.
   - Điện, làm mát.

3. **Hypervisor**:
   - Lớp ảo hoá phần cứng.
   - Cách ly giữa các tenant.
   - Vá bảo mật cho hypervisor.

4. **Host OS** (cho các managed service):
   - Quản lý bare metal.
   - Không phải việc của bạn.

5. **Bảo mật dịch vụ AWS**:
   - Tính sẵn sàng của dịch vụ EC2.
   - Định tuyến VPC.
   - Độ bền (durability) của S3.

Còn phần **của bạn (Security IN the cloud)** với EC2:

1. **Guest OS**:
   - Vá Ubuntu/RHEL/Windows.
   - Cấu hình firewall, antivirus.

2. **Danh tính + Truy cập**:
   - IAM users, roles, policies.
   - MFA.
   - Quản lý khoá (SSH key, certificate).

3. **Cấu hình mạng**:
   - Luật Security Group.
   - NACL.
   - Quyết định định tuyến VPC.

4. **Bảo mật ứng dụng**:
   - Lỗ hổng code (OWASP top 10).
   - Quản lý dependency.
   - Kiểm tra input.

5. **Dữ liệu**:
   - Mã hoá at-rest (KMS).
   - Mã hoá in-transit (TLS).
   - Backup + retention.
   - Phân loại dữ liệu (PII, PHI, PCI).

6. **Compliance**:
   - Các kiểm soát SOC 2 trong app của bạn.
   - HIPAA ở cấp ứng dụng.

Có vài **vùng xám** đáng lưu ý:

- **Vá cho managed service** (RDS, ElastiCache): AWS vá, nhưng bạn đặt maintenance window.
- **Lambda runtime**: AWS vá, nhưng bạn chọn phiên bản runtime.

Quy luật chung dễ nhớ: **càng lên cao trong stack, càng nhiều việc về phía bạn**. Cụ thể theo mô hình:
- IaaS (EC2): nhiều việc về bạn.
- PaaS (RDS): nhiều việc về AWS.
- SaaS (Workspaces): gần như toàn bộ về AWS.

Hai hiểu lầm phổ biến cần tránh:
- "AWS bảo mật dữ liệu của tôi" — SAI. AWS cung cấp công cụ (mã hoá), bạn phải cấu hình.
- "App của tôi an toàn vì nó chạy trên AWS" — SAI. Code app là trách nhiệm của bạn.

Tóm lại: shared responsibility là một **quan hệ đối tác**, không phải sự uỷ thác toàn bộ.
</details>

**Q2.** IAM least privilege — quy trình thực tế làm thế nào?

<details>
<summary>💡 Đáp án</summary>

**Khái niệm**: cấp đúng lượng quyền tối thiểu cần thiết, không hơn.

**Anti-pattern**: gắn `AdministratorAccess` cho mọi role. Dễ nhưng cực kỳ nguy hiểm.

Quy trình thực tế đi theo các bước:

**Bước 1: Bắt đầu chặt, mở dần theo nhu cầu**:
- Dịch vụ mới: mặc định deny all.
- Policy ban đầu để trống.
- Thêm quyền khi app báo lỗi `AccessDenied`.

**Bước 2: Dùng AWS managed policy làm điểm khởi đầu**:
- `AmazonS3ReadOnlyAccess`.
- `AmazonEC2ContainerRegistryReadOnly`.
- Tuỳ chỉnh dần → policy riêng.

**Bước 3: Chỉ định ARN tài nguyên cụ thể**:
```json
"Resource": "arn:aws:s3:::my-bucket/*"
```
Không dùng:
```json
"Resource": "*"
```

**Bước 4: Quyền có điều kiện**:
```json
"Condition": {
  "StringEquals": { "aws:RequestedRegion": "us-east-1" },
  "DateGreaterThan": { "aws:CurrentTime": "2026-01-01T00:00:00Z" }
}
```

**Bước 5: Rà soát bằng IAM Access Analyzer**:
- Phát hiện: "role này có quyền không dùng tới suốt 30 ngày".
- Cắt về đúng mức thực tế dùng.

**Bước 6: Permission boundary để uỷ quyền**:
- Dev được tạo role, nhưng tối đa chỉ tới mức boundary cho phép.

Một số công cụ hỗ trợ:

- **IAM Access Advisor**: cho thấy dịch vụ truy cập gần nhất theo từng role. Cắt phần không dùng.
- **iamlive**: log API call AWS lúc test, sinh ra policy tối thiểu.
- **policy_sentry**: sinh policy least-privilege từ mẫu CRUD.
- **AWS IAM Access Analyzer**: phân tích liên tục.

Các policy cần **tránh**:
- `AdministratorAccess` cho việc hằng ngày.
- `PowerUserAccess` (gần như tệ ngang).
- `*` cho action hoặc resource mà không kèm điều kiện.

Nhịp audit nên có:
- Hằng quý: rà soát mọi role, gỡ phần không dùng.
- Hằng tháng: kiểm tra các phát hiện của IAM Access Analyzer.
- Hằng ngày: cảnh báo khi có role mới với quyền rộng.

Thực tế phát triển theo thời gian: ngày đầu dễ bắt đầu rộng rồi thu hẹp dần; về sau policy chặt là điều bắt buộc; trưởng thành hơn nữa thì có boundary tự động + truy cập just-in-time.

Điểm mấu chốt: least privilege là **văn hoá + công cụ**, không phải một config duy nhất.
</details>

**Q3.** KMS Customer Managed Key vs AWS Managed Key — đánh đổi ra sao?

<details>
<summary>💡 Đáp án</summary>

**AWS Managed Key** (mặc định):
- AWS sở hữu.
- Miễn phí.
- Không kiểm soát được rotation, deletion.
- AWS tự xoay vòng.
- Bạn không xoá được.

**Customer Managed Key (CMK)** ($1/tháng + phí API call):
- Bạn sở hữu.
- Tự định nghĩa key policy (ai được dùng).
- Xoay vòng thủ công hoặc tự động hằng năm.
- Có thể xoá (kèm cửa sổ chờ 7-30 ngày).
- Có audit log mọi lần dùng (CloudTrail).

**Dùng Customer Managed Key khi**:

1. **Compliance yêu cầu kiểm soát**:
   - HIPAA, FedRAMP, PCI: thường yêu cầu khoá do khách hàng quản lý.
   - SOC 2 Trust Services Criteria: kiểm soát khoá ở phía khách hàng.

2. **Truy cập cross-account**:
   - Chia sẻ khoá với tài khoản AWS khác.
   - Cho KMS của tài khoản A giải mã dữ liệu của tài khoản B.

3. **Kiểm soát truy cập chi tiết**:
   - Khoá khác nhau theo dịch vụ / theo phân loại dữ liệu.
   - Thu hồi quyền dùng khoá một cách chính xác.

4. **Audit lượt dùng khoá cụ thể**:
   - CloudTrail log mọi encrypt/decrypt kèm key ID.
   - Phát hiện lượt dùng bất thường.

5. **Chính sách xoay vòng khoá**:
   - Xoay vòng thủ công khi có sự kiện (compliance, nghi ngờ breach).
   - Khác với AWS managed = tự động hằng năm.

6. **BYOK** (Bring Your Own Key):
   - Import key material từ HSM on-prem.
   - Giữ quyền kiểm soát việc sinh khoá.

**Dùng AWS Managed Key khi**:

1. **Mã hoá mặc định, độ phức tạp thấp**:
   - SSE-S3, mã hoá EBS mặc định.
   - Không có yêu cầu compliance cụ thể.

2. **Nhạy cảm với chi phí ở quy mô lớn**:
   - 1000+ khoá × $1 = $1000/tháng.
   - AWS managed = miễn phí.

3. **Không cần kiểm soát chi tiết**:
   - Mọi app đều được encrypt/decrypt.
   - Không cần phân vùng.

**Khuyến nghị thực tế**:

- **Startup nhỏ ngày đầu**: AWS managed (rẻ, đơn giản).
- **Ngày đầu nhưng có PII / dữ liệu nhạy cảm**: Customer managed cho riêng phần tài nguyên nhạy cảm.
- **SOC 2 / HIPAA**: Customer managed cho mọi thứ trong phạm vi compliance.

**Cách lai (hybrid)**:
- Customer managed cho: PII, PHI, secret, khoá mã hoá backup.
- AWS managed cho: log, dữ liệu tạm không nhạy cảm.

**Ví dụ chi phí** (app cỡ trung):
- 10 customer managed key = $10/tháng.
- 100K API call (encrypt/decrypt) = $0.03/10K = $0.30.
- **Tổng**: khoảng $11/tháng cho quản lý khoá đạt chuẩn compliance.

Đây là khoản bảo hiểm rẻ cho cả compliance lẫn kiểm soát. Dùng Customer Managed cho bất cứ thứ gì từ PII trở lên.

**Anti-pattern**: dùng 1 khoá cho tất cả. Mất quyền truy cập khoá = dữ liệu không cứu được. Hãy phân vùng (compartmentalize).
</details>

**Q4.** Ba lỗi cấu hình cloud gây breach nhiều nhất là gì?

<details>
<summary>💡 Đáp án</summary>

Dựa trên các báo cáo ngành (Verizon DBIR, Trend Micro, Wiz), ba lỗi đứng đầu là:

**1. Lưu trữ truy cập public** (S3, GCS, Azure Blob):

- Bucket policy đặt `"Principal": "*"`.
- Bật public ACL.
- Phân quyền cấp object sai.
- **Ví dụ thực tế**: Capital One (S3 + SSRF), Uber, Verizon, Pentagon.

**Phòng**:
- AWS Block Public Access (cấp account + bucket).
- Luật AWS Config.
- Công cụ CSPM (Wiz, Lacework).
- Tagging bắt buộc + cảnh báo.

**2. Lộ chứng thực trong code/config**:

- AWS key commit lên GitHub.
- Mật khẩu DB trong file môi trường nằm trong Docker image.
- Secret trong log CI.
- **Ví dụ thực tế**: Uber 2022 (AWS key trong Slack), nhiều startup nhỏ.

**Phòng**:
- Pre-commit hook (gitleaks).
- GitHub secret scanning.
- Secrets Manager / Vault.
- IAM role thay cho key tĩnh.
- Xoay vòng + cảnh báo.

**3. IAM cấp quyền quá rộng**:

- `*:*` trên resource `*`.
- Access key sống lâu.
- Role cho phép quá nhiều principal assume.
- Cross-account trust không kèm điều kiện.
- **Ví dụ thực tế**: SolarWinds, Capital One.

**Phòng**:
- Least privilege ngay từ đầu.
- IAM Access Analyzer.
- Permission boundary.
- IAM Identity Center / SSO.
- Truy cập just-in-time.
- Audit IAM hằng quý.

Vài lỗi đáng nhắc thêm:

**4. Dữ liệu at-rest không mã hoá**:
- EBS không mã hoá.
- RDS snapshot không mã hoá.
- Backup để dạng rõ.

**5. Root không bật MFA**:
- Root account = truy cập tối cao.
- Không MFA = chỉ một mật khẩu = mất trắng nếu lộ.

**6. Security group mở toang**:
- SSH 22 / RDP 3389 tới `0.0.0.0/0`.
- Cổng DB phơi ra ngoài.
- Default SG của VPC mặc định.

**7. Phần mềm lỗi thời**:
- EC2 chưa vá.
- Container image chứa CVE.
- Lambda runtime hết hỗ trợ (EOL).

**8. Không logging / monitoring**:
- CloudTrail chưa bật.
- Không có CloudWatch alarm.
- Sự cố chỉ được phát hiện bởi researcher bên ngoài.

**9. Insider threat / offboarding kém**:
- Cựu nhân viên còn giữ quyền.
- Không rà soát truy cập khi nghỉ việc.

**10. CI/CD không an toàn**:
- GitHub Actions giữ admin key.
- Không code review.
- Container không ký.

**Khung giảm thiểu**:

1. **Baseline ngày đầu**: bật các mặc định (chặn public, mã hoá, log, MFA).
2. **Giám sát liên tục**: GuardDuty, Security Hub, CSPM.
3. **IaC + scanning**: Checkov, tfsec bắt lỗi ngay trong PR.
4. **Tự động hoá compliance**: Vanta / Drata.
5. **Audit hằng quý**: pentest bên ngoài hằng năm.

Điểm cốt lõi: **khoảng 80% breach có thể phòng được** bằng cấu hình baseline + giám sát. Làm tốt ba lỗi đầu tiên là đã chặn được phần lớn nguy cơ.
</details>

**Q5.** Chuẩn bị audit SOC 2 — lộ trình thực tế gồm những gì?

<details>
<summary>💡 Đáp án</summary>

**SOC 2 = Service Organization Control 2**, do một hãng CPA audit. Có hai loại:
- **Type I**: tại một thời điểm. "Các kiểm soát có tồn tại."
- **Type II**: quan sát qua 6-12 tháng. "Các kiểm soát hoạt động ổn định."

Type II là chuẩn vàng mà enterprise thường yêu cầu.

Lộ trình điển hình đi qua các mốc:

**Mốc khởi đầu**: Quyết định theo đuổi SOC 2 (thường do yêu cầu khi bán cho enterprise).

**Chọn phạm vi**:
- Trust Services Criteria: Security (bắt buộc), Availability, Confidentiality, Privacy, Processing Integrity.
- Phần lớn bắt đầu với: chỉ Security.

**Gap assessment (đánh giá khoảng cách)**:
- Thuê tư vấn hoặc dùng nền tảng tự động (Vanta, Drata, SecureFrame).
- Map các kiểm soát hiện có với yêu cầu SOC 2.
- Xác định các gap.

**Triển khai kiểm soát**:
- IAM kèm MFA + IAM Identity Center.
- Mã hoá (KMS).
- Logging (CloudTrail, audit log).
- Monitoring + alerting (CloudWatch, GuardDuty).
- Rà soát truy cập (hằng quý).
- Quản lý vendor.
- Background check (cho ai có quyền prod).
- Kế hoạch IR + diễn tập tabletop.
- Change management (theo PR).
- Backup + kiểm tra DR.

**Audit ban đầu (Type I)**:
- Auditor xem tài liệu + bằng chứng.
- Báo cáo Type I: "tại ngày 1/6/2026, các kiểm soát tồn tại."

**Giai đoạn quan sát (Type II)**:
- Tiếp tục thu thập bằng chứng.
- Auditor lấy mẫu định kỳ.
- Duy trì các kiểm soát vận hành thật.

**Báo cáo Type II**:
- "Từ 1/6/2026 đến 1/6/2027, các kiểm soát hoạt động hiệu quả."
- Gia hạn hằng năm.

**Chi phí**:
- **Audit**: $15K-$60K tuỳ quy mô + hãng.
- **Vanta/Drata**: $7K-$30K/năm tiền thuê bao.
- **Engineering**: 2-3 person-month ban đầu, 0.5/tháng duy trì.
- **Tổng năm 1**: $30K-$100K.
- **Từ năm 2**: $20K-$70K/năm.

**Tăng tốc bằng các nền tảng**:
- Vanta/Drata có tích hợp sẵn:
  - AWS: tự thu IAM, CloudTrail, Config.
  - GitHub: bằng chứng code review.
  - Slack: incident response.
  - Notion: tài liệu chính sách.
- Tự động thu thập bằng chứng, rút ngắn đáng kể giai đoạn chuẩn bị.

**Các bẫy thường gặp**:

1. **Đánh giá thiếu phạm vi**: bắt đầu quá rộng.
2. **Chỉ dựa vào công cụ**: có tooling mà thiếu quy trình.
3. **Nước rút phút chót**: sát ngày audit mới cuống.
4. **Không ai sở hữu**: không có người chịu trách nhiệm chương trình compliance.
5. **Coi là việc một lần**: SOC 2 là việc liên tục, không phải dự án một lần.

**Trình tự khuyến nghị**:

1. **Baseline kỹ thuật trước**: IAM, mã hoá, logging, monitoring.
2. **Tài liệu sau**: chính sách, quy trình.
3. **Onboard Vanta/Drata**: kết nối công cụ, tự thu bằng chứng.
4. **Khắc phục gap**: xử lý các phát hiện.
5. **Audit Type I**.
6. **Giai đoạn quan sát Type II**.

**ROI**:
- Không có SOC 2: enterprise từ chối, mất deal.
- Có SOC 2: mở cửa thị trường enterprise. Hợp đồng enterprise trung bình $50K-$500K/năm.
- **Hoàn vốn**: thường ngay trong 1-2 deal đầu tiên.

Hãy coi SOC 2 vừa là công cụ bán hàng vừa là sản phẩm phụ của thói quen bảo mật tốt.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

```bash
# === IAM ===
aws iam list-users
aws iam create-policy --policy-name MyPolicy --policy-document file://policy.json
aws iam attach-user-policy --user-name alice --policy-arn arn:aws:iam::...:policy/MyPolicy
aws iam create-access-key --user-name alice    # avoid! Use SSO

# === KMS ===
aws kms create-key --description "App key"
aws kms encrypt --key-id alias/my-key --plaintext "secret"
aws kms decrypt --ciphertext-blob fileb://encrypted.bin

# === S3 security ===
aws s3api put-public-access-block --bucket mybucket --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket mybucket --server-side-encryption-configuration ...

# === CloudTrail ===
aws cloudtrail create-trail --name myTrail --s3-bucket-name myBucket --is-multi-region-trail
aws cloudtrail start-logging --name myTrail

# === GuardDuty ===
aws guardduty create-detector --enable
aws guardduty list-findings --detector-id $DETECTOR_ID

# === Config ===
aws configservice describe-config-rules
aws configservice get-compliance-summary-by-config-rule

# === Secrets Manager ===
aws secretsmanager create-secret --name prod/db --secret-string '{"username":"admin","password":"..."}'
aws secretsmanager get-secret-value --secret-id prod/db
```

```json
// === IAM policy templates ===

// Least privilege S3 access:
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/users/${aws:userid}/*"
}

// Deny without MFA:
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "Bool": { "aws:MultiFactorAuthPresent": "false" }
  }
}

// Region restriction:
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": { "aws:RequestedRegion": ["us-east-1", "us-west-2"] }
  }
}
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Shared Responsibility Model** | Mô hình trách nhiệm chia sẻ | Phân chia trách nhiệm bảo mật giữa vendor và khách hàng |
| **IAM** | Quản lý danh tính & truy cập | Identity and Access Management |
| **User** | Người dùng | Danh tính con người trong IAM |
| **Role** | Vai trò | Danh tính được dịch vụ/user mượn tạm thời |
| **Policy** | Chính sách | Tài liệu JSON định nghĩa quyền |
| **Least privilege** | Đặc quyền tối thiểu | Cấp đúng lượng quyền cần thiết, không hơn |
| **MFA** | Xác thực đa yếu tố | Multi-Factor Authentication |
| **TOTP** | Mật khẩu một lần theo thời gian | Time-based One-Time Password (Google Authenticator) |
| **Hardware key** | Khoá vật lý | Thiết bị 2FA vật lý (YubiKey) |
| **Service role** | Vai trò dịch vụ | IAM role do dịch vụ AWS assume (EC2, Lambda) |
| **IRSA** | IAM role cho ServiceAccount | IAM Roles for Service Accounts (K8s) |
| **IAM Identity Center** | Trung tâm danh tính | AWS SSO với danh tính tập trung |
| **Permission boundary** | Trần quyền | Giới hạn quyền tối đa của một principal |
| **KMS** | Dịch vụ quản lý khoá | Key Management Service |
| **CMK** | Khoá chủ của khách hàng | Customer Master Key |
| **Envelope encryption** | Mã hoá phong bì | Mã hoá data key bằng KMS, mã hoá data bằng data key |
| **BYOK** | Tự mang khoá | Bring Your Own Key |
| **CloudHSM** | HSM chuyên dụng | Phần cứng HSM riêng để giữ khoá |
| **WAF** | Tường lửa ứng dụng web | Web Application Firewall |
| **DDoS** | Tấn công từ chối dịch vụ phân tán | Distributed Denial of Service |
| **SOC 2** | Kiểm soát tổ chức dịch vụ 2 | Service Organization Control 2 audit |
| **ISO 27001** | Chuẩn bảo mật quốc tế | International security standard |
| **HIPAA** | Luật riêng tư y tế (Mỹ) | US healthcare data privacy |
| **PCI DSS** | Chuẩn bảo mật thẻ thanh toán | Payment card data security |
| **GDPR** | Quy định bảo mật EU | EU privacy regulation |
| **CloudTrail** | Nhật ký audit API | AWS API audit log |
| **GuardDuty** | Phát hiện mối đe doạ | AWS ML threat detection |
| **Config** | Audit cấu hình | AWS resource configuration audit |
| **Macie** | Phát hiện PII trong S3 | AWS S3 PII detection |
| **Security Hub** | Bộ tổng hợp phát hiện | Aggregator for findings |
| **CSPM** | Quản lý tư thế bảo mật cloud | Cloud Security Posture Management (Wiz, Lacework) |
| **Session Manager** | Truy cập không cần SSH | Vào shell qua AWS IAM, không mở cổng SSH |
| **SSO** | Đăng nhập một lần | Single Sign-On |
| **OIDC** | Danh tính liên kết | OpenID Connect (federated identity) |
| **Vanta/Drata/SecureFrame** | Nền tảng tự động hoá compliance | Compliance automation platforms |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloud Storage + Databases — Chọn đúng nơi cất dữ liệu](03_storage-and-databases.md)
- ↑ **Về cụm:** [Cloud Fundamentals](../../README.md)
- 🎯 Hoàn thành cụm cloud-fundamentals basic 5/5!

### 🧩 Các chủ đề có thể bạn quan tâm

- 🔁 **Supply chain security:** [Supply chain security — SLSA Level 3 pipeline + admission verify](../../../../10_devops/ci-cd/lessons/02_intermediate/02_supply-chain-security.md) — ký + verify image
- 🔁 **Quản lý secret:** [Secret management — Vault + External Secrets Operator + 12-factor](../../../../10_devops/ci-cd/lessons/02_intermediate/03_secret-management.md) — Vault + ESO
- ☸️ **RBAC trên K8s:** [Namespaces và RBAC: Thiết lập biên giới an ninh và phân quyền hạn chế](../../../../10_devops/kubernetes/lessons/01_basic/04_namespaces-and-rbac.md) — IAM của K8s
- 🏗️ **Bảo mật IaC:** [IaC Best Practices & Alternatives](../../../../10_devops/iac/lessons/01_basic/04_best-practices-and-alternatives.md) — quét IaC

### 🌐 Tài nguyên tham khảo khác

- 📖 [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- 📖 [AWS IAM docs](https://docs.aws.amazon.com/IAM/)
- 📖 [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- 📖 [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- 📖 [GCP Security best practices](https://cloud.google.com/security/best-practices)
- 📖 [Azure Security baseline](https://learn.microsoft.com/en-us/security/benchmark/azure/)
- 📖 [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- 📖 [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- 📖 [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- 📖 [Verizon Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/dbir/)
- 📖 [Vanta](https://www.vanta.com/) / [Drata](https://drata.com/) / [SecureFrame](https://secureframe.com/) — tự động hoá compliance

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bài 04 — cuối cụm cloud-fundamentals basic. Shared Responsibility Model + IAM deep (users/roles/policies/MFA/SSO/IRSA) + encryption (KMS, BYOK, at-rest, in-transit) + network security (WAF, DDoS, defense in depth) + secrets management + compliance frameworks (SOC2/ISO27001/HIPAA/PCI/GDPR) + top 6 cloud breaches + tools 2026 + hands-on secure baseline. 7 pitfall + 4 best practice + 5 self-check + cheatsheet.
- **v1.1.0 (25/05/2026)** — Thêm lời dẫn trước các bảng/diagram chính (Why this matters, Policy example, Encryption everywhere, Common frameworks, Compliance as differentiator).
- **v2.0.0 (01/06/2026)** — Việt hoá toàn bộ prose sang văn phong narrative (giữ nguyên code/JSON/lệnh AWS, tên dịch vụ): tình huống mở bài, 9 phần nội dung và toàn bộ đáp án self-check Q1-Q5. Chuẩn hoá metadata (Yêu cầu trước), Glossary 3 cột (Thuật ngữ/Tiếng Việt/Giải thích), nav (⬅️/↑ + tiêu đề thực) và 3 sub-heading liên kết. Bỏ mọi ước tính thời gian theo mốc tháng trong self-check SOC 2 (chuyển sang mô tả theo trình tự).
