# 🎓 Cloud Networking — VPC, Subnets, Peering, VPN

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [01_regions-availability-zones-edge.md](01_regions-availability-zones-edge.md), [Networking basics](../../../../05_networking/)

> 🎯 *Mạng trong cloud không giống mạng vật lý ở văn phòng. Trên cloud, bạn không kéo dây hay cắm switch — bạn vẽ ra một mạng riêng bằng cấu hình, gọi là **VPC** (Virtual Private Cloud). Bài này đi từ chuyện một database bị hack vì phơi ra Internet, rồi dựng lại đúng cách: VPC, *subnet* (public/private/isolated), Internet Gateway, NAT Gateway, route table, security group, *peering*, VPN và Direct Connect. Khái niệm áp dụng cho mọi cloud; ví dụ minh hoạ dùng AWS cho cụ thể.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **VPC** = một mạng ảo cô lập của riêng bạn trong cloud
- [ ] Phân biệt **subnet** *public* vs *private* vs *isolated*
- [ ] **Internet Gateway** (IGW) vs **NAT Gateway** khác nhau ở đâu
- [ ] **Route table** — quyết định gói tin đi về đâu
- [ ] **Security Group** vs **Network ACL** (*stateful* vs *stateless*)
- [ ] **VPC Peering** — nối hai VPC lại với nhau
- [ ] **VPN** + **Direct Connect** — kết nối hybrid cloud với on-prem
- [ ] **Transit Gateway** — mô hình hub-and-spoke cho nhiều VPC
- [ ] Những khoản phí dễ bị "dính chưởng" (NAT Gateway, egress)

---

## Tình huống — App phơi port 5432 ra Internet, 2 ngày sau bị hack

Hãy bắt đầu bằng một lỗi mà rất nhiều người mới mắc phải. Một bạn dev cần Postgres cho app, thấy cách nhanh nhất là dựng luôn Postgres trên một con EC2 rồi mở port cho app kết nối. Cấu hình như sau:

```text
EC2 (Postgres):  Public IP 54.123.45.67, port 5432 open to 0.0.0.0/0
```

Connection string trong app: `postgres://admin:password@54.123.45.67:5432/db`. Nhìn thì gọn — app kết nối được ngay, không phải cấu hình mạng phức tạp. Nhưng `0.0.0.0/0` nghĩa là *cả thế giới* đều gõ tới được port 5432.

2 ngày sau, hậu quả ập đến theo đúng kịch bản:

- Bot quét port 5432 trên toàn dải IP công cộng, phát hiện ra database này.
- Brute force cặp `admin/password` (vốn quá dễ đoán) → đăng nhập thành công.
- Chạy `pg_dump`, hút sạch dữ liệu ra ngoài.
- Drop bảng để xoá dấu vết.

Buổi post-mortem, sếp gói lại bài học bằng ba câu:

- *"Database không bao giờ được nằm trên public IP."*
- *"App ở public subnet, DB ở private subnet, chỉ app mới nói chuyện với DB."*
- *"Security group quy định rõ ai được truy cập cái gì."*

Ba câu đó chính là xương sống của thiết kế mạng cloud đúng chuẩn — và đó là toàn bộ những gì bài này sẽ dựng lại từ đầu.

---

## 1️⃣ VPC — Virtual Private Cloud

### Định nghĩa

Trước khi đặt bất kỳ resource nào lên cloud, bạn cần một "mảnh đất" mạng riêng để đặt chúng vào. Đó là **VPC** (*Virtual Private Cloud*) — một mạng ảo cô lập nằm trong tài khoản cloud của bạn, là không gian riêng tư của bạn.

Ba đặc điểm cần nhớ về một VPC:

- **Dải IP** (*CIDR*): bạn tự chọn (ví dụ `10.0.0.0/16` = 65.536 IP).
- **Cô lập**: khách hàng khác của AWS không nhìn thấy VPC của bạn.
- **Gắn với region**: một VPC nằm trong đúng 1 region (nhưng trải được ra các AZ trong region đó).

### Default VPC

Mỗi tài khoản AWS được tạo sẵn một VPC mặc định ở mỗi region để bạn dùng ngay mà không phải cấu hình gì. Nó có sẵn:

- CIDR `172.31.0.0/16`.
- 1 subnet public cho mỗi AZ.
- Internet Gateway đã gắn sẵn.

→ Tiện cho việc học và thử nghiệm, nhưng **không nên dùng cho production**. Vì nó mở Internet sẵn và bạn không kiểm soát được cách chia mạng. Production luôn dựng VPC riêng để nắm toàn quyền.

### Lập kế hoạch CIDR

*CIDR* là cách chia dải IP private cho VPC. Quy ước: dùng dải RFC 1918 (`10.x.x.x` phổ biến nhất), một VPC `/16` đủ cho hàng chục nghìn IP. Điểm **quan trọng**: nếu sau này định *peer* các VPC lại với nhau (multi-region, multi-account, hay VPN về on-prem), các VPC **không được trùng dải CIDR** — và dải này không sửa được sau khi đã có resource bên trong. Vậy nên chọn đúng ngay từ đầu là việc đáng đầu tư.

Trước hết, làm quen cách đọc một CIDR — con số sau dấu `/` cho biết dải rộng bao nhiêu IP:

```text
10.0.0.0/16    = 10.0.0.0 - 10.0.255.255  (65,536 IPs, /16)
10.0.0.0/24    = 10.0.0.0 - 10.0.0.255    (256 IPs, /24)
10.0.0.0/28    = 10.0.0.0 - 10.0.0.15     (16 IPs, /28)
```

Số `/` càng nhỏ thì dải càng rộng. Có ba dải IP private theo chuẩn RFC 1918 mà mọi mạng nội bộ được phép dùng:

- `10.0.0.0/8` (16 triệu IP) — hay dùng nhất cho VPC.
- `172.16.0.0/12` (1 triệu IP).
- `192.168.0.0/16` (65K IP) — thường gặp ở mạng gia đình.

Khuyến nghị thực tế khi cấp CIDR cho VPC: mỗi VPC lấy một khối `/16` (65K IP), và **tránh chồng lấn** nếu có ý định peer về sau. Một cách chia gọn gàng:

- Dev: `10.0.0.0/16`.
- Staging: `10.1.0.0/16`.
- Prod us-east: `10.2.0.0/16`.
- Prod eu-west: `10.3.0.0/16`.

→ Không trùng dải = sau này peer/VPN thoải mái mà không phải đánh đổi gì.

🪞 **Ẩn dụ**: *VPC giống như một **khu chung cư riêng tư**. Bạn sở hữu cả toà nhà (VPC), tự chia phòng (subnet), kiểm soát ai được vào (security group), và có cổng ra phố (Internet Gateway).*

---

## 2️⃣ Subnet — Chia nhỏ VPC

### Các loại subnet

Có VPC rồi, bước tiếp theo là chia nó thành các *subnet* — những mảnh nhỏ hơn, mỗi mảnh nằm trong đúng 1 AZ. Điều quyết định "tính cách" của một subnet không phải kích thước, mà là **nó có đường ra Internet hay không**. Từ đó sinh ra ba loại:

**Public subnet** — có đường ra phố:

- Có route trỏ tới Internet Gateway (IGW).
- Resource bên trong được gán public IP.
- Truy cập Internet hai chiều (vào lẫn ra).
- Dùng cho: *load balancer*, NAT, *bastion host* (máy trung gian để SSH vào).

**Private subnet** — ra được nhưng không ai vào được:

- Không có route tới IGW.
- Resource chỉ có private IP.
- Đi ra Internet qua NAT Gateway → IGW.
- Dùng cho: app server, database.

**Isolated subnet** — đóng kín hoàn toàn:

- Không có Internet, cả vào lẫn ra.
- Dùng cho: dữ liệu cực nhạy cảm (PCI, y tế).

### Mô hình subnet trải nhiều AZ

Một thiết kế production tiêu chuẩn thường chia theo công thức **3 tier (public/private/db) × 3 AZ = 9 subnet**. Tier public chứa Load Balancer và NAT, tier private chứa app server, tier db chứa database tách biệt. Trải đều ra 3 AZ để hệ thống vẫn sống khi 1 AZ chết. Subnet `/24` (251 IP dùng được) đủ cho khoảng 100 app instance:

```text
VPC 10.0.0.0/16
  ├── Public Subnet AZ-a   10.0.0.0/24   (256 IPs, for LB)
  ├── Public Subnet AZ-b   10.0.1.0/24
  ├── Public Subnet AZ-c   10.0.2.0/24
  ├── Private Subnet AZ-a  10.0.10.0/24  (apps)
  ├── Private Subnet AZ-b  10.0.11.0/24
  ├── Private Subnet AZ-c  10.0.12.0/24
  ├── DB Subnet AZ-a       10.0.20.0/24  (databases)
  ├── DB Subnet AZ-b       10.0.21.0/24
  └── DB Subnet AZ-c       10.0.22.0/24
```

→ 3 tier (public/private/db) × 3 AZ = 9 subnet. Cách đánh dải `10.0.0.x` cho public, `10.0.1x.x` cho private, `10.0.2x.x` cho db giúp nhìn IP là đoán ngay được tier.

Bỏ qua chuyện trải nhiều AZ, sơ đồ dưới đây cho thấy đường đi của gói tin xuyên qua 3 tier — lưu lượng chỉ chạm tới tầng kế bên, không nhảy cóc:

```mermaid
flowchart TD
    IGW["Internet Gateway"] --> Pub["Public subnet: Load Balancer"]
    Pub --> App["Private subnet: App servers"]
    App --> DB["Private subnet: Database"]
    App -.->|qua NAT| NAT["NAT Gateway"] -.-> IGW
```

Điểm mấu chốt: chỉ Load Balancer ở public subnet quay mặt ra Internet, còn App muốn gọi API ngoài phải đi vòng qua NAT Gateway, và Database thì hoàn toàn không có đường ra Internet trực tiếp.

### Vì sao tách riêng subnet cho DB?

Có thể bạn thắc mắc: app đã ở private subnet rồi, sao phải tách thêm một tier db nữa cho rườm rà? Subnet riêng cho DB có 3 lý do rất thực tế. **Cô lập**: app subnet không truy cập DB trực tiếp được — phải đi qua đúng một security group rule cụ thể. **Tuân thủ**: chuẩn PCI/HIPAA bắt buộc DB phải nằm trong subnet không có route ra Internet. **Tiết kiệm chi phí**: DB không cần NAT (vì không gọi API bên ngoài) → bỏ luôn được phí NAT processing:

- **Cô lập**: DB chỉ truy cập được từ app subnet (qua security group).
- **Tuân thủ**: PCI yêu cầu DB nằm trong subnet isolated.
- **Định tuyến**: DB subnet không cần NAT (tiết kiệm phí).

### Số IP bị AWS giữ lại trong mỗi subnet

Một chi tiết dễ làm người mới bối rối khi tính dung lượng: mỗi subnet không dùng được trọn vẹn số IP. AWS **giữ lại 5 IP trong mỗi subnet** cho mục đích hệ thống:

- `.0`: địa chỉ network.
- `.1`: router của VPC.
- `.2`: DNS server.
- `.3`: dành cho tương lai.
- `.255` (IP cuối): broadcast.

→ Vậy `/24` thực tế = 256 − 5 = 251 IP dùng được. Khi tính sức chứa subnet, nhớ trừ đi 5 IP này.

---

## 3️⃣ Internet Gateway (IGW)

### IGW là gì?

Đến đây bạn đã biết public subnet "có đường ra Internet" — nhưng cái đường đó cụ thể là gì? Chính là **IGW** (*Internet Gateway*), cây cầu nối VPC ↔ Internet. Đặc điểm của nó:

- 1 IGW cho mỗi VPC.
- Gắn ở cấp VPC (không phải cấp subnet).
- Tự scale theo lưu lượng, không có điểm chết đơn lẻ (*no SPOF*).
- Miễn phí (không tính tiền bản thân IGW).

### Gói tin đi ra Internet như thế nào?

IGW vận hành như một **NAT 1:1**. Một con EC2 trong public subnet có cả private IP (10.0.0.5) lẫn public IP (54.123.45.67). Khi gói tin đi ra Internet, IGW thay private IP bằng public IP; khi gói tin trả về, IGW dịch ngược lại. Toàn bộ quá trình diễn ra trong suốt — bản thân EC2 không hề "biết" mình đang có public IP:

```text
EC2 in public subnet (10.0.0.5, ENI has public IP 54.123.45.67)
  ↓
Route table: 0.0.0.0/0 → IGW
  ↓
IGW translates: 10.0.0.5 ↔ 54.123.45.67 (1:1 NAT)
  ↓
Internet
```

→ Để ra được Internet, EC2 cần **cả private IP lẫn public IP**, và việc dịch địa chỉ do IGW lo hết. Đây là điểm phân biệt cốt lõi với NAT Gateway ở phần sau.

### Nếu không có IGW

Ngược lại, một con EC2 nằm trong private subnet sẽ bị "kẹt trong nhà":

- Chỉ có private IP (10.0.10.5).
- Không có route ra Internet.
- Không gọi được `apt-get` để tải gói cài đặt.
- Không gọi được Stripe API hay bất kỳ dịch vụ ngoài nào.

→ Nó vẫn cần đi ra ngoài (để cài thư viện, gọi API), nhưng ta không muốn ai từ ngoài vào được. Lời giải cho bài toán "chỉ ra, không vào" này là **NAT Gateway**.

---

## 4️⃣ NAT Gateway — Đường ra cho private subnet

### Khi nào cần

App nằm trong private subnet thường vẫn cần chủ động đi ra ngoài:

- `apt-get install nginx`.
- `pip install requests`.
- Gọi Stripe API để xử lý thanh toán.

Nhưng tuyệt đối không được phép nhận kết nối từ Internet vào. Đây là mâu thuẫn quen thuộc: cần ra nhưng cấm vào. **NAT Gateway** giải đúng bài này — chỉ cho lưu lượng đi ra, chặn mọi kết nối khởi tạo từ ngoài.

### NAT hoạt động ra sao

NAT Gateway khác IGW ở chỗ nó làm **NAT N:1** (nhiều private IP chia sẻ chung 1 public IP). EC2 private gửi gói tin → route đến NAT (nằm ở public subnet) → NAT thay source IP và port, rồi gửi qua IGW. Khi response trả về, NAT tra bảng connection để trả đúng về con EC2 đã hỏi. Tính chất quan trọng là **bất đối xứng**: ra thì được, vào thì bị chặn:

```text
EC2 private (10.0.10.5)
  ↓
Route table: 0.0.0.0/0 → NAT Gateway
  ↓
NAT Gateway (in public subnet, has public IP 54.123.45.67)
  ↓
Translates: 10.0.10.5:50000 ↔ 54.123.45.67:50000
  ↓
IGW → Internet
```

→ Từ phía Internet nhìn vào, lưu lượng đến từ public IP của NAT chứ không phải private IP của EC2. Vì NAT chỉ ghi nhớ connection do bên trong khởi tạo, nên kết nối từ ngoài vào không có "chỗ neo" để đi vào — đó chính là lý do NAT an toàn theo một chiều.

### Chi phí NAT Gateway (⚠️ dễ "dính chưởng"!)

Đây là chỗ nhiều người bị bất ngờ trên hoá đơn. NAT Gateway tính tiền hai phần:

- **$0.045/giờ** (~$33/tháng cho mỗi NAT Gateway).
- **$0.045 mỗi GB xử lý** (cả chiều vào lẫn ra).

→ Một app chạy 1TB/tháng lưu lượng = $45/tháng phí băng thông + $33/tháng phí NAT = ~$78/tháng. Và nếu làm multi-AZ thì nhân lên: 3 NAT Gateway = $99/tháng chỉ riêng phí cố định, chưa tính lưu lượng.

Vì vậy có vài cách tối ưu đáng nhớ:

- Dùng **1 NAT chung** (thay vì mỗi AZ một cái): rẻ hơn, nhưng thành điểm chết đơn lẻ (SPOF).
- Dùng **VPC Endpoint** cho các dịch vụ AWS (S3, DynamoDB miễn phí): các lệnh gọi AWS không cần đi qua NAT nữa.
- Dùng kho object không tính phí egress (kiểu **Cloudflare R2**): tránh NAT cho lưu trữ object.

### NAT instance vs NAT Gateway

Ngoài NAT Gateway (do AWS quản lý), bạn còn có thể tự dựng NAT bằng một con EC2 — gọi là *NAT instance*. So sánh nhanh để biết khi nào dùng cái nào:

- **NAT Gateway** (managed): tự scale, sẵn HA. Chi phí: từ $33/tháng.
- **NAT instance** (tự dựng trên EC2): t3.micro chỉ ~$7/tháng. Nhưng phải tự cài đặt, tự vá bảo mật, và là SPOF trừ khi tự cấu hình HA.

→ Mặc định nên chọn NAT Gateway cho production. NAT instance chỉ hợp cho môi trường dev/test khi muốn tiết kiệm.

### Egress-only Internet Gateway (cho IPv6)

Một điểm thú vị: với IPv6, câu chuyện NAT khác hẳn. Vì địa chỉ IPv6 đều route được toàn cầu nên không cần NAT để "che" địa chỉ private nữa. Thay vào đó AWS có **Egress-only IGW** — chỉ cho đi ra, và miễn phí.

→ Triển khai theo IPv6 có thể tiết kiệm được khoản phí NAT đáng kể.

---

## 5️⃣ Route Table

### Khái niệm

Cho đến giờ ta cứ nói "có route tới IGW", "route tới NAT" — vậy cái "route" đó nằm ở đâu? Nằm trong **route table** — bảng các quy tắc quyết định gói tin đi tới đâu, gắn vào từng subnet:

```text
Public Subnet route table:
  10.0.0.0/16 → local           (intra-VPC)
  0.0.0.0/0  → IGW              (internet)

Private Subnet route table:
  10.0.0.0/16 → local           (intra-VPC)
  0.0.0.0/0  → NAT Gateway      (internet via NAT)
  10.1.0.0/16 → VPC Peer        (peer VPC)
  172.16.0.0/12 → VPN Gateway   (on-prem via VPN)
```

→ Khi một gói tin có nhiều route khớp, route **cụ thể nhất (dải hẹp nhất) thắng** — đây là quy tắc *longest prefix match*. Chính dòng `0.0.0.0/0 → IGW` (hay `→ NAT`) là thứ phân định một subnet là public hay private.

### Mỗi subnet một route table

Mỗi subnet gắn với đúng 1 route table (dùng route table mặc định nếu không chỉ định). Nhiều subnet có thể dùng chung một route table. Một mô hình hay gặp trong production:

- 1 route table dùng chung cho mọi **public subnet** (đều route ra IGW).
- 1 route table riêng cho mỗi AZ ở **private subnet** (route tới NAT của chính AZ đó, để tránh lưu lượng chạy chéo AZ vốn tốn tiền).

### Soi route khi gặp sự cố

Khi gói tin đi không đúng nơi, hai lệnh sau giúp soi xem route table đang cấu hình gì và subnet nào gắn với bảng nào:

```bash
# AWS CLI
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-abc

# Check which subnet → which route table
aws ec2 describe-route-table-associations
```

---

## 6️⃣ Security Group (SG)

### Khái niệm

Route table lo gói tin đi đâu; còn ai được phép kết nối tới resource thì do **Security Group** quyết định. Đây là *firewall* ảo gắn theo **từng resource** (EC2, RDS, Lambda). Bốn tính chất cần nắm:

- **Stateful**: lưu lượng trả về được tự động cho phép (không cần khai báo chiều về).
- **Chỉ có rule "allow"** (không có "deny" tường minh — mặc định mọi thứ đều bị chặn cho tới khi bạn cho phép).
- Tối đa khoảng 60 rule mỗi SG.
- Một resource gắn được nhiều SG cùng lúc.

### Cấu hình rule

Một SG điển hình cho web server gồm các rule vào (inbound) và ra (outbound):

```text
Inbound:
  Allow TCP 443 from 0.0.0.0/0      (HTTPS from internet)
  Allow TCP 80 from 0.0.0.0/0       (HTTP)
  Allow TCP 22 from 1.2.3.4/32      (SSH from office IP only)

Outbound:
  Allow ALL to 0.0.0.0/0            (default — egress anywhere)
```

→ Để ý rule SSH chỉ mở cho đúng IP văn phòng (`1.2.3.4/32`), không mở cho cả thế giới — đây là khác biệt sống còn so với cái EC2 bị hack ở đầu bài.

### SG tham chiếu SG

Đây là mẫu rất mạnh và đáng học: thay vì cho phép theo dải IP, một SG có thể tham chiếu thẳng tới một SG khác. Ý là "cho phép bất kỳ resource nào đang mang SG kia":

```text
App SG (sg-app):
  Inbound: TCP 8000 from sg-lb (Load Balancer SG)

DB SG (sg-db):
  Inbound: TCP 5432 from sg-app (App SG)

LB SG (sg-lb):
  Inbound: TCP 443 from 0.0.0.0/0
  Inbound: TCP 80 from 0.0.0.0/0
```

Kết quả là một chuỗi truy cập rõ ràng theo tầng:

```text
Internet → LB SG (443/80 open) → App SG (8000 from LB) → DB SG (5432 from App)
```

→ **Không cần khai báo IP cụ thể**. Resource tự nhận diện nhau qua SG. Kể cả khi IP đổi (EC2 bị thay, ASG scale), rule vẫn đúng — đây là lợi thế lớn so với hardcode IP.

### Default SG

Mỗi VPC có sẵn một SG mặc định. Hành vi của nó:

- **Inbound**: cho phép lưu lượng từ chính các resource cùng SG (intra-SG).
- **Outbound**: cho phép tất cả.

→ Ổn cho dev. Production thì nên định nghĩa rule tường minh thay vì dựa vào default.

### SG vs firewall ở OS (iptables)

Một câu hỏi hay gặp: đã có SG rồi thì còn cần `iptables` trong máy không? Cả hai có thể tồn tại song song:

- **SG** = firewall ở tầng cloud (AWS).
- **iptables** = firewall ở tầng hệ điều hành (bên trong EC2).

→ Đây là chiến lược "thắt lưng + dây đeo quần" (phòng thủ nhiều lớp). SG chặn trước khi gói tin chạm tới EC2; iptables là lớp phòng thủ bổ sung bên trong EC2.

---

## 7️⃣ Network ACL (NACL)

### Khái niệm

SG gắn theo resource; còn **NACL** (*Network ACL*) là firewall ở cấp **subnet**, và quan trọng là *stateless*:

- Stateless: phải khai báo cho phép cả chiều vào lẫn chiều ra (không tự nhớ chiều về như SG).
- Có cả rule Allow lẫn Deny (khác SG — SG chỉ có Allow).
- Đánh số ưu tiên (số nhỏ xét trước).
- Mặc định: cho phép tất cả.

### NACL vs SG

Để thấy rõ khi nào dùng cái nào, đặt hai loại firewall cạnh nhau:

| Khía cạnh | Security Group | Network ACL |
|---|---|---|
| Phạm vi | Theo resource (EC2, RDS) | Theo subnet |
| Stateful | Có (chiều về tự cho phép) | Không (phải khai cả hai chiều) |
| Loại rule | Chỉ Allow | Allow + Deny |
| Xét rule | Xét tất cả | Khớp đầu tiên thắng |
| Mặc định | Chặn mọi inbound | Cho phép tất cả |
| Hợp dùng cho | Cấp phép theo dịch vụ | Chặn thô ở cấp subnet |

### Khi nào dùng NACL

Nhìn bảng trên, NACL chỉ thực sự hữu ích trong vài trường hợp đặc thù mà SG không làm được:

- **Chặn IP cụ thể** (SG không có "deny", nên không chặn nổi 1 IP).
- **Cô lập ở cấp subnet**.
- **Phòng thủ nhiều lớp** (thêm một tầng nữa).

Ví dụ chặn một dải IP bot ngay tại NACL:

```text
NACL rules:
  100  ALLOW  TCP 443  0.0.0.0/0     Inbound
  110  DENY   ALL      8.8.8.8/32    Inbound (block 8.8.8.8)
  120  ALLOW  ALL      0.0.0.0/0     Inbound
```

→ Thực tế đa số team bỏ qua NACL (SG là đủ). NACL chỉ dùng cho yêu cầu tuân thủ hoặc các kịch bản chặn đặc thù.

---

## 8️⃣ VPC Peering

### Khi nào cần

Đôi khi hai VPC cần nói chuyện với nhau:

- Microservices nằm ở các VPC riêng (mỗi team một VPC).
- VPC dịch vụ dùng chung (logging, monitoring).
- Sáp nhập công ty (VPC của bên được mua lại).

### VPC Peering

**VPC Peering** dựng một kết nối trực tiếp giữa hai VPC, để resource hai bên nói chuyện qua private IP mà không phải đi vòng ra Internet. Cần khai báo ở cả hai phía — route table mỗi bên trỏ về peering connection, và security group cho phép lưu lượng từ phía kia:

```text
VPC A (10.0.0.0/16) ↔ peering connection ↔ VPC B (10.1.0.0/16)

Route table A:
  10.1.0.0/16 → pcx-abc (peering)

Route table B:
  10.0.0.0/16 → pcx-abc

Security group:
  Allow traffic from peer VPC's SG / CIDR
```

→ Resource hai VPC giao tiếp qua private IP, không bước nào đi qua Internet — vừa nhanh vừa an toàn.

### Giới hạn

Peering nghe đơn giản nhưng có vài giới hạn dễ làm bạn đụng tường khi mở rộng:

- **Không bắc cầu** (*non-transitive*): A ↔ B ↔ C **không** đồng nghĩa A ↔ C. Muốn A nói với C phải peer riêng A ↔ C.
- **Không được trùng CIDR**: VPC A `10.0.0.0/16` + VPC B `10.0.0.0/16` = không peer được.
- **Peering xuyên region**: có hỗ trợ, nhưng phát sinh phí truyền dữ liệu liên region.
- **Giới hạn ~125 peer mỗi VPC** (AWS).

### Transit Gateway

Chính vì peering không bắc cầu, khi số VPC tăng lên, số kết nối phải tạo bùng nổ theo. Lời giải là **Transit Gateway** — một hub trung tâm, mọi VPC chỉ cần cắm vào đó:

```text
            Transit Gateway (hub)
        ┌───────┼───────┬───────┐
       VPC A  VPC B  VPC C  VPC D ... VPC N
        │       │       │       │
      on-prem (via VPN)
```

→ Một hub duy nhất, tất cả VPC gắn vào, định tuyến có tính bắc cầu (transitive). Thêm VPC mới chỉ là gắn thêm một attachment.

Về chi phí: $0.05/giờ (~$36/tháng) + $0.02/GB dữ liệu xử lý. Đáng dùng khi: từ 5 VPC trở lên, HOẶC multi-account nhiều VPC, HOẶC làm hybrid cloud.

---

## 9️⃣ Hybrid: VPN + Direct Connect

### Khi nào cần hybrid cloud

Nhiều tổ chức không chuyển hết lên cloud cùng lúc, mà cần nối datacenter on-prem ↔ VPC trên cloud:

- App ở cloud, DB vẫn ở on-prem (vì yêu cầu tuân thủ).
- Mượn cloud để gánh tải lúc cao điểm (*burst*).
- Đang trong quá trình di trú dần lên cloud.

Có hai cách nối: VPN (qua Internet, rẻ và nhanh) và Direct Connect (đường riêng, đắt và ổn định). Lần lượt qua từng cái.

### Site-to-Site VPN

VPN dựng một **đường hầm mã hoá đi qua chính Internet** giữa firewall on-prem và VPN Gateway phía AWS:

```text
On-prem firewall ←─ encrypted tunnel ─→ AWS VPN Gateway → VPC
```

Cách dựng gồm ba phần: phía AWS đặt VPN Gateway trong VPC; phía on-prem là Customer Gateway (router có khả năng VPN); và một đường hầm IPsec được thiết lập giữa hai bên.

Cân nhắc nhanh ưu/nhược của VPN:

- ✅ **Ưu**: dựng nhanh (vài giờ), có mã hoá, rẻ ($36/tháng + phí dữ liệu).
- ❌ **Nhược**: đi qua Internet nên độ trễ thất thường (~50-200ms RTT), băng thông giới hạn (1.25 Gbps mỗi tunnel), không hợp cho lưu lượng lớn.

### Direct Connect (DX)

Khi VPN qua Internet không đủ ổn định, **Direct Connect** kéo hẳn một **đường cáp quang riêng** từ on-prem tới AWS (thông qua đối tác colocation):

```text
On-prem ←─ private fiber ─→ Direct Connect location ←→ AWS region
```

So với VPN, DX đổi chiều ưu/nhược:

- ✅ **Ưu**: độ trễ ổn định (1-5ms trong cùng vùng đô thị), băng thông cao (1-100 Gbps), không đi qua Internet, phí egress rẻ hơn (rẻ hơn đi Internet thường).
- ❌ **Nhược**: đắt ($0.30+/giờ ~ $220+/tháng + phí port + cross-connect), dựng lâu (vì phải kéo cáp vật lý), một sợi cáp = SPOF trừ khi làm dự phòng.

Khi nào chọn DX: lưu lượng ổn định >10 Gbps, HOẶC yêu cầu tuân thủ/pháp lý, HOẶC hybrid cloud với khối lượng công việc đoán trước được.

### Kết hợp: DX + VPN

Mẫu phổ biến trong thực tế là dùng cả hai: DX làm đường chính, VPN làm dự phòng. Nếu sợi cáp DX bị đứt, VPN tự gánh thay — vừa được độ ổn định của DX, vừa có lưới an toàn của VPN.

---

## 🔟 VPC Endpoints

### Vấn đề

Hãy nhìn một nghịch lý hay gặp: app ở private subnet gọi S3 (vốn cùng region), nhưng gói tin lại đi một vòng tốn kém:

```text
EC2 → NAT Gateway → IGW → Internet → S3 (in same region!)
```

→ Đi qua NAT thì tốn phí processing, lại vòng qua Internet nên thêm độ trễ và rủi ro bảo mật — dù S3 nằm ngay trong cùng region với bạn.

### Lời giải VPC Endpoint

**VPC Endpoint** mở một đường kết nối *riêng tư* thẳng tới dịch vụ AWS, không phải vòng ra Internet. Có hai kiểu:

**Gateway Endpoint** (miễn phí):

- Chỉ dùng cho **S3 và DynamoDB**.
- Thêm một dòng trong route table: dải IP của S3 → Gateway Endpoint.
- Lưu lượng đi trong backbone của AWS.

**Interface Endpoint** (PrivateLink, $0.01/giờ):

- Dùng cho các dịch vụ AWS khác (Lambda, ECR, Secrets Manager, KMS, v.v.).
- Tạo một ENI (card mạng ảo) trong subnet của bạn, mang private IP.
- DNS của dịch vụ phân giải về IP của endpoint.

### Dựng Gateway Endpoint cho S3

Chỉ vài dòng Terraform là gắn được S3 endpoint vào route table private:

```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id          = aws_vpc.main.id
  service_name    = "com.amazonaws.us-east-1.s3"
  route_table_ids = [aws_route_table.private.id]
}
```

→ Route table được cập nhật: dải IP của S3 → endpoint. Lưu lượng S3 không còn đi qua NAT nữa. Khoản tiết kiệm rất thực: 1TB/tháng lưu lượng S3 qua NAT = $45/tháng; qua endpoint = $0.

---

## 1️⃣1️⃣ Hands-on: Thiết kế VPC production

### Mục tiêu

Giờ gom tất cả mảnh ghép trên thành một VPC production hoàn chỉnh. Bản thiết kế cần đạt:

- Multi-AZ (3 AZ).
- Đủ ba tier: public + private + db.
- NAT cho lưu lượng đi ra.
- VPC endpoint cho dịch vụ AWS.
- Security group riêng cho từng tier.

### Terraform

Đoạn Terraform dưới dựng nguyên bản thiết kế đó. Đọc theo thứ tự: VPC → IGW → 3 nhóm subnet → NAT → route table → S3 endpoint → 3 security group theo chuỗi LB → App → DB:

```hcl
# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = { Name = "prod-vpc" }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Public subnets (3 AZs)
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index}.0/24"
  availability_zone       = "ap-southeast-1${["a", "b", "c"][count.index]}"
  map_public_ip_on_launch = true
  
  tags = { Name = "public-${count.index}", Tier = "public" }
}

# Private subnets
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = "ap-southeast-1${["a", "b", "c"][count.index]}"
  
  tags = { Name = "private-${count.index}", Tier = "private" }
}

# DB subnets
resource "aws_subnet" "db" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 20}.0/24"
  availability_zone = "ap-southeast-1${["a", "b", "c"][count.index]}"
  
  tags = { Name = "db-${count.index}", Tier = "db" }
}

# NAT Gateways (1 per AZ for HA)
resource "aws_eip" "nat" {
  count  = 3
  domain = "vpc"
}

resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
}

# Public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  count          = 3
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Private route tables (1 per AZ for AZ-local NAT)
resource "aws_route_table" "private" {
  count  = 3
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
}

resource "aws_route_table_association" "private" {
  count          = 3
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# DB subnets: no internet route (isolated)
resource "aws_route_table" "db" {
  vpc_id = aws_vpc.main.id
  # Only local route, no NAT
}

# VPC Endpoint S3 (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.ap-southeast-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [
    aws_route_table.private[0].id,
    aws_route_table.private[1].id,
    aws_route_table.private[2].id,
  ]
}

# Security groups (LB → App → DB pattern)
resource "aws_security_group" "lb" {
  name   = "lb-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name   = "db-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
  
  # No egress needed (DB doesn't initiate)
}
```

### Sơ đồ kết quả

Khi `terraform apply` xong, kiến trúc dựng lên đúng theo sơ đồ sau — lưu lượng từ Internet chỉ chạm tới LB ở public, rồi xuống dần app ở private và DB ở tầng isolated:

```text
                Internet
                   │
                   ↓
            ┌──────────────┐
            │     IGW      │
            └──────────────┘
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
   Public AZ-a Public AZ-b Public AZ-c
   (LB nodes, NAT)
        │          │          │
   ┌────┴────┐┌────┴────┐┌────┴────┐
   │ NAT-A   ││ NAT-B   ││ NAT-C   │ (1 per AZ)
   └────┬────┘└────┬────┘└────┬────┘
        ↓          ↓          ↓
   Private AZ-a Private AZ-b Private AZ-c
   (App servers)
        │          │          │
        ↓          ↓          ↓
   DB AZ-a    DB AZ-b    DB AZ-c
   (RDS, isolated)

VPC Endpoint S3 → bypass NAT for S3 traffic
```

→ Đây là cấu hình production-grade: HA nhờ multi-AZ, NAT đặt theo từng AZ (tránh phí chạy chéo AZ), security group phòng thủ theo tầng.

### Ước tính chi phí

Để có cảm giác về hoá đơn, đây là các khoản phí mạng cố định của thiết kế này:

- 3× NAT Gateway: $99/tháng phí cố định + lưu lượng.
- 3× EIP: miễn phí (khi đang gắn vào NAT).
- IGW: miễn phí.
- VPC + subnet + SG: miễn phí.
- S3 endpoint: miễn phí.
- Interface endpoint: $7-15/tháng mỗi cái.

→ **Tổng phí mạng**: khoảng $100-130/tháng (chưa tính lưu lượng). Phần lớn là NAT — nên đây cũng là chỗ đáng tối ưu nhất.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Database nằm trong public subnet

Đây chính là lỗi đã thổi bay database ở đầu bài: DB phơi ra Internet → bị quét port, brute force, rồi hack.

→ **Fix**: DB ở private subnet, app ở private, LB ở public. Chỉ LB mới quay mặt ra Internet.

### ❌ Cạm bẫy: 1 NAT Gateway = SPOF + phí chạy chéo AZ

Đặt đúng một NAT ở AZ-a tưởng tiết kiệm, nhưng đổi lại hai rủi ro:

```text
Single NAT in AZ-a:
  - AZ-a outage = all NAT down.
  - Apps in AZ-b, AZ-c → cross-AZ → NAT in AZ-a = $0.01/GB cross-AZ + NAT cost.
```

→ **Fix**: mỗi AZ một NAT (3 NAT). HA multi-AZ, và không còn lưu lượng chạy chéo AZ.

**Đánh đổi chi phí**: 3 NAT so với 1 NAT = thêm khoảng $66/tháng — đáng để đổi lấy HA.

### ❌ Cạm bẫy: Hardcode IP trong security group

Khai IP cứng vào SG là tự gài bom hẹn giờ:

```text
ingress: cidr_blocks = ["10.0.1.5/32"]    # specific EC2 IP
```

→ EC2 bị thay = IP đổi = rule SG hỏng.

→ **Fix**: tham chiếu SG thay vì IP:

```text
ingress: security_groups = [aws_security_group.app.id]
```

→ Rule tự khớp với bất kỳ EC2 nào đang mang SG đó.

### ❌ Cạm bẫy: Mở SSH cho 0.0.0.0/0

```text
ingress: TCP 22 from 0.0.0.0/0
```

→ Bot lập tức brute force.

→ **Fix**, theo mức độ an toàn tăng dần:

- Chỉ mở SSH cho IP văn phòng: `cidr_blocks = ["1.2.3.4/32"]`.
- **Tốt hơn**: AWS Systems Manager Session Manager — không cần mở port SSH, xác thực bằng IAM.
- **Tốt nhất**: AWS Client VPN hoặc Tailscale cho truy cập của cả team.

### ❌ Cạm bẫy: VPC CIDR quá nhỏ

```text
VPC: 10.0.0.0/24    # 256 IPs total
```

→ Không có chỗ lớn lên. Riêng K8s đã ngốn 100+ IP mỗi node.

→ **Fix**: mặc định lấy `/16` (65K IP). Thừa sức cho tương lai.

### ❌ Cạm bẫy: VPC CIDR trùng với on-prem

```text
VPC: 10.0.0.0/16
On-prem: 10.0.0.0/16    # conflict!
```

→ Không VPN/peering được.

→ **Fix**: phối hợp cấp CIDR thống nhất giữa cloud + on-prem. Ghi lại trong tài liệu IPAM (quản lý dải IP).

### ❌ Cạm bẫy: Phí truyền dữ liệu NAT bất ngờ

Một nguồn tốn tiền âm thầm: kéo image lớn qua NAT. App tải 10GB Docker image qua NAT = $0.45/image. 100 lần deploy = $45.

→ **Fix**:

- Dùng VPC Endpoint cho ECR (miễn phí cho layer ECR lưu trên S3).
- Cache Docker image tại chỗ (registry mirror).
- Bật pull-through cache.

### ❌ Cạm bẫy: SG quá thoáng kiểu "allow all"

```text
ingress: protocol = "-1"; cidr_blocks = ["0.0.0.0/0"]
```

→ Mở toang tất cả. SG thành vô dụng.

→ **Fix**: chỉ định rõ port + nguồn. Rà soát SG định kỳ hằng quý.

### ✅ Best practice: Mỗi môi trường một VPC

```text
- Dev VPC: 10.0.0.0/16
- Staging VPC: 10.1.0.0/16
- Prod VPC: 10.2.0.0/16
```

→ Cô lập mạnh. SG khác nhau, IAM khác nhau, và các dải không trùng để peer được sau này.

### ✅ Best practice: Bật Flow Logs

VPC Flow Logs ghi lại mọi kết nối mạng — vô giá khi điều tra sự cố:

```hcl
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  log_destination = aws_s3_bucket.flow_logs.arn
}
```

→ Soi lưu lượng, phát hiện bất thường, phục vụ forensics.

### ✅ Best practice: NACL mặc định-từ-chối + cho phép tường minh

```text
NACL: deny all → allow specific
```

→ Lớp phòng thủ bổ sung cùng SG. Đa số team bỏ qua (SG là đủ); chỉ dùng khi yêu cầu tuân thủ ngặt nghèo.

### ✅ Best practice: Vào server qua Session Manager (không SSH key)

```text
AWS Systems Manager Session Manager:
- No SSH port open.
- IAM-based access (not SSH key).
- Audit log per session.
- Multi-factor auth via IAM.
```

→ Thay `ssh -i key.pem ec2@public-ip` bằng `aws ssm start-session --target i-abc123` — không mở port SSH, xác thực qua IAM, có log từng phiên.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Public subnet vs private subnet — khác biệt cốt lõi là route table, còn gì nữa?

<details>
<summary>💡 Đáp án</summary>

**Khác biệt định nghĩa** nằm ở route table:

- Public subnet: route `0.0.0.0/0` → IGW.
- Private subnet: route `0.0.0.0/0` → NAT (hoặc không có route ra ngoài luôn = isolated).

Ngoài route table, còn vài khác biệt kéo theo:

1. **Gán public IP**:
   - Public subnet thường để `map_public_ip_on_launch = true`.
   - Private subnet: false (chỉ có private IP).

2. **Khả năng ra Internet**:
   - Public: hai chiều (vào + ra).
   - Private: chỉ ra qua NAT, không ai từ Internet vào được.

3. **Tình huống dùng**:
   - Public: load balancer, NAT, bastion, public API.
   - Private: app server, dịch vụ nội bộ.
   - Isolated (không route): database (tuân thủ).

4. **Hệ quả bảo mật**:
   - Public: phải có SG chặt (giới hạn inbound).
   - Private: SG có thể thoáng hơn (vì khả năng tiếp cận đã hẹp).

5. **Chi phí**:
   - Public: miễn phí (chỉ cần IGW).
   - Private mà cần Internet: phát sinh phí NAT Gateway.

**Quy ước phân tầng**:

- Tier 1: chỉ LB ở public.
- Tier 2: app ở private.
- Tier 3: DB ở isolated.

**Anti-pattern**: đặt database vào public subnet — lỗi kinh điển dẫn tới bị hack.

→ Route table là câu trả lời kỹ thuật. Còn ý đồ kiến trúc thì do bảo mật + chi phí dẫn dắt.
</details>

**Q2.** Security Group stateful vs Network ACL stateless — kéo theo hệ quả gì?

<details>
<summary>💡 Đáp án</summary>

**Security Group (Stateful)**:

- Cho phép inbound TCP 443.
- Lưu lượng trả về tự động được cho phép (không cần khai rule outbound).
- Connection tracking nhớ ai là bên khởi tạo.

```text
Inbound SG:
  TCP 443 from 0.0.0.0/0    ← only need this
Outbound SG:
  Default allow all          ← anyway permissive
```

→ User → LB:443 inbound được phép. LB trả về cho user → tự được phép nhờ stateful tracking.

**Network ACL (Stateless)**:

- Cho phép inbound TCP 443 — chỉ lo chiều vào.
- Phản hồi đi ra trên **ephemeral port** (ví dụ 50000-65535).
- Phải khai báo cho phép outbound trên dải ephemeral một cách tường minh.

```text
Inbound NACL:
  Rule 100: ALLOW TCP 443 from 0.0.0.0/0
  Rule 110: ALLOW TCP 1024-65535 from 0.0.0.0/0    ← response inbound (e.g., for outbound API call)
  
Outbound NACL:
  Rule 100: ALLOW TCP 1024-65535 to 0.0.0.0/0      ← response to client
  Rule 110: ALLOW TCP 443 to 0.0.0.0/0             ← outgoing HTTPS
```

→ Rất dễ cấu hình sai. Quên dải ephemeral port = phản hồi bị chặn.

**Vì sao có ephemeral port**:

- Kết nối: server:443 ↔ client:ephemeral (ví dụ 54321).
- Phản hồi từ server quay về trên ephemeral port của client.
- OS cấp ephemeral 32768-60999 (mặc định trên Linux).

**Thực tế**:

- **SG luôn stateful**: đơn giản, mặc định cho cấp resource.
- **NACL stateless**: chỉ dùng khi cần rule DENY hoặc chặn cả subnet.

**Lỗi hay mắc**:

- Áp NACL như SG → quên dải ephemeral → lỗi kết nối khó hiểu.
- NACL mặc định cho phép tất cả → tưởng chạy ổn → vỡ khi bắt đầu thêm rule.

**Khuyến nghị**:

- Mặc định dùng SG cho mọi thứ.
- NACL chỉ cho việc đặc thù: chặn IP bot, tuân thủ, phòng thủ nhiều lớp.
- Ghi chú rule NACL thật cẩn thận.

→ Stateful (SG) = dễ. Stateless (NACL) = mạnh nhưng phải cẩn thận.
</details>

**Q3.** Tối ưu chi phí NAT Gateway — những chiêu mạnh nhất?

<details>
<summary>💡 Đáp án</summary>

**Chi phí NAT Gateway**:

- $0.045/giờ × 720 giờ = **$32.40/tháng mỗi NAT** (phí cố định).
- $0.045/GB xử lý (vào + ra).

Với setup HA 3-AZ: 3 NAT = $97/tháng cố định + lưu lượng.

**Các chiêu tối ưu mạnh nhất**:

1. **VPC Endpoint cho dịch vụ AWS** (miễn phí với loại Gateway):
   - S3, DynamoDB: Gateway endpoint, không tốn phí.
   - Dịch vụ khác (Lambda, ECR, KMS, v.v.): Interface endpoint $7/tháng mỗi cái.
   - **Tiết kiệm**: lưu lượng AWS không qua NAT. Thường chiếm 70%+ lưu lượng NAT.

2. **ECR pull-through cache + immutable tag**:
   - Cache base image tại chỗ.
   - Giảm lưu lượng pull ECR.

3. **Cloudflare R2 hoặc giải pháp object storage không tính egress**:
   - R2 không tính phí egress. Dời các workload tải nặng sang đó.

4. **HTTP/2 keep-alive + nén**:
   - Giảm khối lượng dữ liệu nhờ nén (Brotli).
   - Connection pooling giảm overhead.

5. **CDN cho lưu lượng ra** (download từ app của bạn):
   - Nội dung tĩnh qua CloudFront / Cloudflare.
   - Origin kéo từ S3 (qua Gateway endpoint, không qua NAT).

6. **Một NAT duy nhất cho non-prod**:
   - Dev/staging: 1 NAT (chấp nhận rủi ro SPOF).
   - Tiết kiệm $65/tháng (bớt 2 NAT).

7. **IPv6 + egress-only IGW** (nâng cao):
   - Egress-only IGW miễn phí.
   - Hạ tầng hiện đại: IPv6 đi ra từ private subnet, không cần NAT.

8. **Soi lưu lượng để tìm chỗ lãng phí**:
   - Phân tích VPC Flow Logs.
   - Lãng phí hay gặp: ECR qua NAT, telemetry qua NAT, cài gói qua NAT.

**Ví dụ thực tế**:

- Trước: 3 NAT + 5TB/tháng lưu lượng NAT = $97 + $225 = $322/tháng.
- Sau khi thêm VPC Endpoint S3 + ECR + pull-through cache: 5TB → 500GB = $97 + $22.5 = **$120/tháng**.
- **Tiết kiệm**: 60% phí NAT.

**Ở quy mô lớn**:

- Các công ty lớn (Netflix, Stripe) thường loại bỏ NAT hoàn toàn.
- Chuyển sang IPv6 + egress IGW.
- VPC Endpoint cho mọi thứ thuộc AWS.
- Proxy tự xây cho lưu lượng ra ngoài AWS.

→ Hãy soi lưu lượng NAT. Đa số có 50%+ là không cần thiết.
</details>

**Q4.** Khi nào dùng VPC Peering, khi nào dùng Transit Gateway?

<details>
<summary>💡 Đáp án</summary>

**VPC Peering**:

- Kết nối trực tiếp 1:1 giữa 2 VPC.
- Không bắc cầu (A↔B + B↔C không tạo ra A↔C).
- Miễn phí (không tính phí theo giờ).
- $0.01/GB cho truyền liên region.

**Hợp nhất khi**:

- Tổng cộng 2-3 VPC.
- Chỉ cần vài cặp nối cụ thể.
- Kiến trúc đơn giản.

**Transit Gateway** (hub):

- Hub-and-spoke: mọi VPC nối vào TGW.
- Có bắc cầu: A↔TGW↔B↔TGW↔C đều thông.
- $0.05/giờ ($36/tháng) + $0.02/GB.
- Còn nối được cả VPN + Direct Connect.

**Hợp nhất khi**:

- Từ 5 VPC trở lên.
- Kiến trúc multi-account.
- Hybrid cloud (cloud + on-prem qua VPN).
- Cần phân vùng mạng (route policy).

**Bảng quyết định**:

| Tình huống | Dùng |
|---|---|
| 2 VPC cần nói chuyện | VPC Peering |
| VPC dịch vụ dùng chung (1 → nhiều) | VPC Peering (mỗi spoke) hoặc TGW |
| 5+ VPC nối lưới đầy đủ | Transit Gateway |
| Multi-account (Organization) | Transit Gateway |
| Hybrid (cloud + on-prem VPN) | Transit Gateway |
| Nhạy chi phí, chưa đáng < $36/tháng | VPC Peering |

**Vấn đề peering N-to-N**:

- 5 VPC nối lưới đầy đủ: 5*4/2 = **10 kết nối peering**.
- Mỗi cái phải cấu hình riêng.
- Route khai tay ở mỗi VPC.
- N=10 = 45 kết nối.

**Lời giải TGW**:

- 5 VPC gắn vào 1 TGW.
- 5 attachment.
- Định tuyến tập trung.

**So chi phí** cho 5 VPC:

- Peering: 0 phí cố định + lưu lượng.
- TGW: $36 cố định + $0.02/GB + phí attachment.

**Khuyến nghị**:

- < 4 VPC: VPC Peering.
- 4+ VPC HOẶC hybrid: Transit Gateway.
- Multi-account thì luôn TGW (chia sẻ qua RAM).

**Giải pháp thay thế**: VPC Lattice (mới hơn, ở tầng ứng dụng):

- Service-to-service xuyên các VPC.
- HTTP/gRPC, không phải mạng thô.
- Trừu tượng cao hơn.
- Dùng khi cần kiểu service mesh.
</details>

**Q5.** SG tham chiếu SG vs CIDR block — ưu/nhược?

<details>
<summary>💡 Đáp án</summary>

**SG tham chiếu SG**:

```text
db_sg ingress:
  Allow TCP 5432 from sg-app
```

**Ưu**:

1. **Động**: thành viên của app SG thay đổi (EC2 mới, bị thay) — rule tự áp.
2. **Dễ đọc**: ý đồ rõ ("DB nhận từ app").
3. **Bền với việc đổi IP**: ASG scale, instance bị thay, không cần sửa rule.
4. **Gọn**: không phải bảo trì danh sách IP.

**Nhược**:

1. **Chỉ trong cùng VPC** (và VPC đã peer cùng region, tính tới 2024).
2. **Cross-account / region**: phải dùng CIDR (cho tới khi có tính năng mới hơn).
3. **Audit khó hơn**: "IP nào tới được DB?" phải truy vấn thành viên của SG.

**Tham chiếu bằng CIDR block**:

```text
db_sg ingress:
  Allow TCP 5432 from 10.0.10.0/24
```

**Ưu**:

1. **Cross-VPC / region / account**: chạy được ở mọi nơi.
2. **Tường minh**: IP được ghi rõ.
3. **Tĩnh**: dải IP biết trước.

**Nhược**:

1. **Lỗi thời**: nếu subnet đổi CIDR (hiếm), rule phải sửa.
2. **Quá rộng**: cho cả `/24` nghĩa là gồm luôn các instance không phải app trong subnet.
3. **Thủ công**: phải sửa khi topology thay đổi.

**Mẫu khuyến nghị**:

**Trong cùng VPC**: ưu tiên tham chiếu SG.

```text
db_sg ingress: from sg-app
```

**Cross-VPC / on-prem**: dùng CIDR.

```text
db_sg ingress: from 192.168.10.0/24 (on-prem range)
```

**Cross-account (qua Organizations)**: tham chiếu SG dùng được qua VPC sharing (tính năng AWS mới hơn).

**Mẫu kết hợp**:

```text
db_sg ingress:
  Allow TCP 5432 from sg-app             # intra-VPC dynamic
  Allow TCP 5432 from 10.1.0.0/16        # peered VPC range
  Allow TCP 5432 from 192.168.0.0/16     # on-prem VPN range
```

**Anti-pattern**:

- CIDR `0.0.0.0/0` cho DB nội bộ.
- Liệt kê 50 IP cụ thể (nên dùng SG ref hoặc subnet CIDR).
- Trộn cả hai mà không theo mẫu rõ ràng.

**Công cụ audit**:

- `aws ec2 describe-security-group-rules` → liệt kê tất cả.
- Công cụ như Steampipe, Pacu để audit bảo mật.

→ SG reference = tốt nhất trong cùng VPC. CIDR cho việc vượt ranh giới.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

```bash
# === VPC commands ===
aws ec2 describe-vpcs
aws ec2 create-vpc --cidr-block 10.0.0.0/16
aws ec2 describe-subnets --filters Name=vpc-id,Values=vpc-abc

# === Security groups ===
aws ec2 describe-security-groups --group-ids sg-abc
aws ec2 authorize-security-group-ingress \
  --group-id sg-abc \
  --protocol tcp --port 443 --cidr 0.0.0.0/0

# === Route tables ===
aws ec2 describe-route-tables --filters Name=vpc-id,Values=vpc-abc

# === Flow logs ===
aws ec2 describe-flow-logs --filter Name=resource-id,Values=vpc-abc

# === VPC peering ===
aws ec2 create-vpc-peering-connection --vpc-id vpc-abc --peer-vpc-id vpc-def

# === Transit gateway ===
aws ec2 describe-transit-gateways
aws ec2 create-transit-gateway-vpc-attachment --transit-gateway-id tgw-abc --vpc-id vpc-abc

# === VPN ===
aws ec2 describe-vpn-connections
aws ec2 describe-customer-gateways

# === Endpoint ===
aws ec2 describe-vpc-endpoints
```

```hcl
# === VPC essentials ===
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

# Public subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

# Route table → IGW
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id
}

# Security group SG-to-SG
resource "aws_security_group_rule" "db_from_app" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.app.id
  security_group_id        = aws_security_group.db.id
}

# VPC Endpoint S3 (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **VPC** | Mạng riêng ảo | Virtual Private Cloud — mạng cô lập của riêng bạn trong cloud |
| **CIDR** | Ký hiệu chia dải IP | Classless Inter-Domain Routing (ví dụ 10.0.0.0/16) |
| **Subnet** | Mạng con | Một mảnh của VPC, gắn với 1 AZ |
| **Public subnet** | Subnet công khai | Có route tới IGW |
| **Private subnet** | Subnet riêng | Không ra Internet trực tiếp, đi ra qua NAT |
| **Isolated subnet** | Subnet cô lập | Không Internet, hoàn toàn kín |
| **IGW (Internet Gateway)** | Cổng Internet | Cầu nối VPC ↔ Internet |
| **NAT Gateway** | Cổng NAT | Chỉ cho private subnet đi ra Internet |
| **NAT instance** | NAT tự dựng | NAT tự xây trên EC2 (mẫu cũ) |
| **Route table** | Bảng định tuyến | Quy tắc quyết định gói tin đi đâu |
| **Security Group (SG)** | Nhóm bảo mật | Firewall stateful ở cấp resource |
| **Network ACL (NACL)** | Danh sách kiểm soát mạng | Firewall stateless ở cấp subnet |
| **VPC Peering** | Ghép nối VPC | Kết nối trực tiếp giữa 2 VPC |
| **Transit Gateway (TGW)** | Cổng trung chuyển | Hub nối nhiều VPC + on-prem |
| **VPC Endpoint (Gateway)** | Điểm cuối VPC (Gateway) | Miễn phí, chỉ S3/DynamoDB |
| **VPC Endpoint (Interface)** | Điểm cuối VPC (Interface) | PrivateLink, các dịch vụ AWS khác |
| **VPN Gateway** | Cổng VPN | Phía AWS của site-to-site VPN |
| **Customer Gateway** | Cổng phía khách | Phía on-prem của VPN |
| **Direct Connect (DX)** | Kết nối trực tiếp | Cáp quang riêng AWS ↔ on-prem |
| **Egress** | Lưu lượng ra | Traffic đi ra ngoài |
| **Ingress** | Lưu lượng vào | Traffic đi vào trong |
| **Bastion host** | Máy nhảy | Jump server để SSH vào mạng riêng |
| **Session Manager** | Quản lý phiên | Truy cập shell của AWS không cần SSH |
| **Flow Logs** | Nhật ký lưu lượng | Log các kết nối mạng trong VPC |
| **ENI** | Card mạng ảo | Elastic Network Interface (NIC ảo) |
| **EIP** | IP tĩnh đàn hồi | Elastic IP (public IP cố định) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Regions, Availability Zones, Edge — Phân bố địa lý của Cloud](01_regions-availability-zones-edge.md)
- ➡️ **Bài tiếp theo:** [Cloud Storage + Databases — Chọn đúng nơi cất dữ liệu](03_storage-and-databases.md)
- ↑ **Về cụm:** [Cloud Fundamentals — Tổng quan cụm](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- 🌐 [TCP/IP fundamentals](../../../../05_networking/tcp-ip-fundamentals/) — nền tảng networking
- 🏗️ [IaC Terraform basics](../../../../10_devops/iac/lessons/01_basic/01_terraform-basics.md) — dựng VPC bằng IaC
- ☸️ [K8s Services](../../../../10_devops/kubernetes/lessons/01_basic/02_services-and-networking.md) — VPC + K8s

### 🌐 Tài nguyên tham khảo khác

- 📖 [AWS VPC docs](https://docs.aws.amazon.com/vpc/)
- 📖 [GCP VPC docs](https://cloud.google.com/vpc/docs)
- 📖 [Azure Virtual Network docs](https://learn.microsoft.com/en-us/azure/virtual-network/)
- 📖 [AWS Networking Workshop](https://catalog.workshops.aws/networking/)
- 📖 [VPC sizing calculator](https://aws.amazon.com/blogs/networking-and-content-delivery/best-practices-vpc-sizing/)
- 📖 [Cloud Network Pricing](https://aws.amazon.com/vpc/pricing/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bài 02 cụm cloud-fundamentals. VPC + subnet types + IGW + NAT Gateway + route tables + SG vs NACL + VPC Peering + Transit Gateway + VPN + Direct Connect + VPC Endpoints. Hands-on Terraform thiết kế VPC production. Áp dụng bảo mật: DB ở isolated subnet, SG-to-SG references, phòng thủ nhiều lớp.
- **v1.1.0 (25/05/2026)** — Thêm lời dẫn trước phần CIDR planning, Multi-AZ subnet pattern, Why separate DB subnet, How traffic flows (IGW), How NAT works.
- **v2.0.0 (01/06/2026)** — Việt hoá toàn bộ prose từ văn phong "điện tín" EN sang narrative tiếng Việt theo nhịp WHY→WHAT→HOW (lời dẫn trước + câu phân tích sau mỗi bảng/code/diagram, câu bắc cầu giữa các section, Việt hoá toàn bộ self-check). Chuẩn hoá metadata (Yêu cầu trước), Glossary 3 cột, nav (⬅️/➡️/↑ + tiêu đề H1 thực), bỏ nhãn "(sắp viết)" cho bài 03 đã tồn tại. Giữ nguyên mọi code/lệnh/config, số liệu và ví dụ kỹ thuật.
- **v2.0.1 (10/06/2026)** — Bổ sung sơ đồ bố cục VPC 3 tier cho trực quan.
