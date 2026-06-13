# 🎓 Dynamic Inventory — Quản lý node cloud co giãn tự động

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 13/06/2026\
> **Cập nhật:** 13/06/2026\
> **Level:** Intermediate\
> **Tags:** ansible, dynamic-inventory, aws, gcp, cloud, configuration-management\
> **Yêu cầu trước:** [Intermediate Overview](00_intermediate-overview.md)

> 🎯 *Ở cụm basic, Acme Shop chỉ có vài con server cố định nên bạn liệt kê IP vào `inventory.ini` là xong. Nhưng giờ Acme chạy auto-scaling trên EC2 — sáng 3 node, trưa 30 node, IP đổi xoành xoạch. Bài này dạy bạn để Ansible **tự hỏi cloud** xem hiện có những máy nào qua **inventory plugin**, gom chúng theo tag, rồi chạy playbook lên đúng nhóm `prod` mà không phải gõ IP bằng tay lần nào nữa.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu vì sao **inventory tĩnh** (`inventory.ini`) chết với hạ tầng auto-scaling
- [ ] Phân biệt **dynamic inventory script** (cũ) và **inventory plugin** (chuẩn 2026)
- [ ] Viết file cấu hình plugin `aws_ec2.yml`: `regions`, `filters`, `keyed_groups`, `compose`, `hostnames`
- [ ] Kiểm tra inventory bằng `ansible-inventory --graph` và `--list`
- [ ] Bật **cache** cho inventory để không gọi API cloud mỗi lần chạy
- [ ] Dùng plugin `constructed` gộp nhiều nguồn (EC2 + GCE) thành group thống nhất
- [ ] Bảo mật credential đúng cách (IAM role / biến môi trường, không hardcode key)
- [ ] Gom EC2 của Acme theo tag `Environment=prod` thành group rồi chạy playbook lên đó

---

## 1️⃣ Vì sao inventory tĩnh "chết" khi gặp auto-scaling

Quay lại Acme Shop. Hồi còn nhỏ, hạ tầng của bạn là 3 con VPS thuê cứng — IP không bao giờ đổi, nên file inventory tĩnh trông rất gọn:

```ini
# inventory.ini — kiểu tĩnh, OK khi server cố định
[webservers]
web-prod1.acmeshop.vn ansible_host=10.0.1.21
web-prod2.acmeshop.vn ansible_host=10.0.1.22

[dbservers]
db-prod1.acmeshop.vn ansible_host=10.0.2.10
```

Mọi thứ ổn cho tới ngày Acme chuyển web tier sang **Auto Scaling Group** trên AWS để chịu tải mùa sale. Từ lúc đó:

- **IP sinh tự động**: mỗi EC2 instance mới có private IP do AWS cấp, bạn không biết trước. Hôm nay là `10.0.1.34`, mai scale-in rồi scale-out lại thành `10.0.1.57`.
- **Node sinh/diệt liên tục**: 8h sáng có 3 node, 12h trưa sale lên 30 node, 2h chiều giảm còn 5. File `inventory.ini` viết tay không thể nào "biết" có bao nhiêu node đang sống.
- **Sửa tay = sai**: mỗi lần scale, bạn phải SSH vào AWS Console copy IP rồi paste vào file. Quên 1 node → node đó không được cấu hình, lệch khỏi các node còn lại (chính là *config drift* mà cả cụm CM sinh ra để diệt).
- **Cấu hình theo vai trò bất khả thi**: bạn muốn chạy playbook chỉ lên các máy `Environment=prod`, nhưng IP thì không nói cho bạn biết máy nào prod, máy nào staging.

> [!WARNING]
> Với hạ tầng động, file inventory tĩnh không chỉ bất tiện — nó **nguy hiểm**. Một IP ghi cứng trong file hôm nay trỏ tới web server, tuần sau AWS tái cấp IP đó cho một database. Chạy playbook web lên nhầm DB là thảm hoạ. Inventory tĩnh và cloud co giãn là hai thứ **về bản chất không tương thích**.

Vấn đề cốt lõi: **"danh sách máy" không còn do bạn nắm, mà do cloud provider (AWS/GCP) nắm**. Vậy thay vì bạn cố chép tay danh sách đó, hãy để Ansible **tự hỏi cloud** mỗi lần chạy. Đó chính là **dynamic inventory** (inventory động).

🪞 **Ẩn dụ**: Inventory tĩnh giống **danh bạ điện thoại in trên giấy** — in xong là cố định, ai đổi số thì danh bạ sai ngay. Dynamic inventory giống **app danh bạ tự đồng bộ với tổng đài** — bạn không nhập số thủ công, mỗi lần mở app nó tự kéo danh sách mới nhất từ nguồn gốc (cloud). Số ai đổi, máy nào mới bật/tắt — app luôn phản ánh đúng hiện tại.

---

## 2️⃣ Dynamic inventory hoạt động ra sao

**Dynamic inventory** là cơ chế Ansible **sinh danh sách host lúc chạy** (runtime) bằng cách gọi một nguồn bên ngoài — thường là API của cloud provider — thay vì đọc một file tĩnh.

Trước khi xem cấu hình cụ thể, hãy hình dung luồng tổng thể. Sơ đồ dưới mô tả điều gì xảy ra giữa lúc bạn gõ `ansible-playbook` và lúc playbook thật sự chạy task:

```mermaid
graph LR
    User["Bạn gõ: ansible-playbook -i aws_ec2.yml"] --> Plugin["Inventory plugin (amazon.aws.aws_ec2)"]
    Plugin -->|"DescribeInstances API"| AWS["AWS EC2 API"]
    AWS -->|"Danh sách instance + tags + IP"| Plugin
    Plugin -->|"Gom group theo tag, sinh host"| Inv["Inventory trong RAM"]
    Inv --> Play["Playbook chạy task lên đúng group"]
```

→ Điểm mấu chốt: **không có file nào liệt kê IP cả**. Plugin gọi API `DescribeInstances`, AWS trả về danh sách instance đang sống kèm tag và IP, plugin biến chúng thành inventory **ngay trong bộ nhớ** rồi đưa cho playbook. Mỗi lần chạy, danh sách được làm tươi — node nào vừa scale-out tự xuất hiện, node nào vừa terminate tự biến mất.

### Hai thời kỳ: script cũ và plugin mới

Ansible có **hai cách** làm dynamic inventory, và đây là chỗ rất nhiều tài liệu cũ trên mạng làm người mới lạc lối:

- **Dynamic inventory script (cũ)**: một file thực thi (thường là `ec2.py`) mà Ansible chạy; script tự gọi API rồi in JSON ra `stdout`. Cách này **đã lỗi thời** — script `ec2.py` huyền thoại giờ không còn được khuyến nghị.
- **Inventory plugin (chuẩn 2026)**: bạn chỉ viết **một file YAML cấu hình** (vd `aws_ec2.yml`), Ansible nạp plugin tương ứng và tự làm phần còn lại. Sạch hơn, có cache, có cấu hình group/biến khai báo gọn gàng.

Bảng dưới so sánh để bạn không bị nhầm khi đọc tài liệu cũ:

| Đặc điểm | Script cũ (`ec2.py`) | Plugin mới (`aws_ec2.yml`) |
|---|---|---|
| Bạn phải viết gì | File Python thực thi (`chmod +x`) | File YAML khai báo |
| Cấu hình group/biến | Sửa code Python | Khai báo trong YAML (`keyed_groups`, `compose`) |
| Cache | Tự code | Có sẵn (bật bằng config) |
| Trạng thái 2026 | ❌ Deprecated / không khuyến nghị | ✅ Chuẩn chính thức |
| Cài qua | — | Collection `amazon.aws` / `google.cloud` |

> [!IMPORTANT]
> Nếu bạn Google "ansible dynamic inventory aws" và thấy hướng dẫn tải file `ec2.py` về rồi `chmod +x` — đó là tài liệu cũ. Năm 2026 dùng **inventory plugin** `amazon.aws.aws_ec2` (cho AWS) và `google.cloud.gcp_compute` (cho GCP). Toàn bộ bài này đi theo cách plugin.

🪞 **Ẩn dụ** (mở rộng từ ẩn dụ danh bạ): script cũ giống bạn tự viết một con **bot cào số điện thoại** rồi tự bảo trì khi tổng đài đổi định dạng. Plugin mới giống dùng **app danh bạ chính hãng** do nhà mạng phát hành — bạn chỉ cấu hình "lọc liên hệ theo nhóm", phần kết nối tổng đài đã có sẵn, ổn định, có cache.

### Cài collection chứa plugin

Plugin không có sẵn trong Ansible lõi mà nằm trong **collection**. Cài bằng `ansible-galaxy` (kiến thức bạn đã học ở bài role):

```bash
# Cài collection AWS (chứa plugin aws_ec2) và GCP (chứa gcp_compute)
ansible-galaxy collection install amazon.aws google.cloud
```

Kết quả mong đợi (rút gọn):

```
Starting collection install process
Installing 'amazon.aws:9.0.0' to '/home/user/.ansible/collections/ansible_collections/amazon/aws'
amazon.aws:9.0.0 was installed successfully
Installing 'google.cloud:1.5.0' to '/home/user/.ansible/collections/ansible_collections/google/cloud'
google.cloud:1.5.0 was installed successfully
```

→ Plugin AWS còn cần thư viện Python `boto3` để gọi API. Cài kèm:

```bash
# boto3 = SDK Python chính thức của AWS, plugin aws_ec2 dùng nó gọi API
python3 -m pip install boto3 botocore
```

> 📖 Đã có plugin, giờ ta viết file cấu hình để nói cho nó biết "hỏi cloud cái gì, gom thế nào".

---

## 3️⃣ File cấu hình plugin `aws_ec2.yml` — mổ xẻ từng phần

File cấu hình của inventory plugin có **quy ước đặt tên**: nó **bắt buộc** kết thúc bằng `aws_ec2.yml` hoặc `aws_ec2.yaml` (vd `inventory.aws_ec2.yml`, `acme.aws_ec2.yml`) để Ansible nhận diện đúng plugin. Đây là điểm người mới hay vấp — đặt tên sai thì Ansible coi nó là file YAML thường và báo "không có host".

Dưới đây là một file đầy đủ cho Acme Shop. Ta sẽ tách từng khối ra giải thích ngay sau:

```yaml
# inventory.aws_ec2.yml — cấu hình inventory plugin cho EC2 của Acme
plugin: amazon.aws.aws_ec2

# 1. Region nào cần quét (chỉ quét region có máy → nhanh hơn)
regions:
  - ap-southeast-1
  - us-east-1

# 2. Chỉ lấy instance đang chạy + thuộc về Acme (lọc phía AWS, đỡ tải về thừa)
filters:
  instance-state-name: running
  tag:Project: acme-shop

# 3. Đặt tên host dễ đọc thay vì IP/instance-id khó nhớ
hostnames:
  - tag:Name
  - private-ip-address

# 4. Tự gom group theo tag (vd Environment=prod → group "env_prod")
keyed_groups:
  - key: tags.Environment
    prefix: env
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: aws_region

# 5. Tạo biến tuỳ ý cho mỗi host từ dữ liệu instance
compose:
  ansible_host: private_ip_address
  instance_type_var: instance_type
```

→ File này nói: "Hỏi AWS ở 2 region, chỉ lấy instance đang chạy của project acme-shop, đặt tên host theo tag `Name`, tự gom thành group theo `Environment`/`Role`/region, và set `ansible_host` = private IP". Giờ soi từng khối.

### `plugin` — chọn đúng plugin

Dòng đầu `plugin: amazon.aws.aws_ec2` bắt buộc, dùng tên đầy đủ (FQCN). Đây là cách Ansible biết "file YAML này không phải data thường, mà là cấu hình cho plugin EC2".

### `regions` — quét region nào

AWS chia hạ tầng theo **region** (vùng địa lý). Nếu không khai báo, plugin quét region mặc định trong cấu hình AWS của bạn. Khai báo rõ giúp:

- **Nhanh hơn**: chỉ gọi API ở region thật sự có máy, không quét cả 30 region rỗng.
- **An toàn hơn**: tránh vô tình kéo về instance ở region khác không liên quan.

### `filters` — lọc ngay phía AWS

`filters` áp **trước khi tải dữ liệu về** — AWS lọc giúp bạn, nên dữ liệu truyền qua mạng ít hơn. Key của filter dùng đúng cú pháp của AWS `DescribeInstances`:

| Filter | Ý nghĩa |
|---|---|
| `instance-state-name: running` | Chỉ lấy máy đang chạy (bỏ qua máy `stopped`/`terminated`) |
| `tag:Project: acme-shop` | Chỉ lấy máy có tag `Project=acme-shop` |
| `tag:Environment: prod` | Lọc thẳng chỉ máy prod (nếu chỉ cần prod) |

> [!TIP]
> Có hai chỗ để "lọc": `filters` (lọc phía AWS, giảm dữ liệu tải về) và `keyed_groups` (gom group phía Ansible sau khi đã tải về). Quy tắc: **lọc để loại bỏ hẳn máy không cần** → dùng `filters`; **gom máy đã lấy về thành nhóm** → dùng `keyed_groups`. Đừng tải cả ngàn instance về rồi mới lọc bằng Ansible.

### `hostnames` — đặt tên host dễ đọc

Mặc định plugin đặt tên host theo cách khó đọc (thường là `ec2-...` hoặc instance-id). `hostnames` là **danh sách ưu tiên**: plugin thử nguồn đầu, nếu host không có thì rớt xuống nguồn kế:

```yaml
hostnames:
  - tag:Name              # ưu tiên 1: dùng tag Name (vd "acme-web-01")
  - private-ip-address    # ưu tiên 2: máy nào không có tag Name thì dùng private IP
```

→ Nhờ vậy khi chạy playbook, output hiện `acme-web-01` thay vì `i-0a1b2c3d4e5f` — dễ debug hơn nhiều.

### `keyed_groups` — trái tim của việc gom node theo tag

Đây là phần **quan trọng nhất** với hạ tầng động. `keyed_groups` bảo plugin: "với mỗi giá trị của key này, tạo một group tương ứng và bỏ host vào đó". Ví dụ:

```yaml
keyed_groups:
  - key: tags.Environment   # nhìn vào tag Environment của instance
    prefix: env             # tạo group tên "env_<giá trị>"
```

Với tag `Environment=prod` → host vào group `env_prod`. Tag `Environment=staging` → group `env_staging`. Bạn **không khai báo group nào bằng tay** — chúng tự sinh từ tag thực tế trên cloud. Đây chính là cầu nối để bạn chạy playbook "lên đúng nhóm prod".

| Khai báo | Group sinh ra | Khi nào dùng |
|---|---|---|
| `key: tags.Environment`, `prefix: env` | `env_prod`, `env_staging`, `env_dev` | Phân biệt môi trường |
| `key: tags.Role`, `prefix: role` | `role_web`, `role_db` | Phân biệt vai trò máy |
| `key: placement.region`, `prefix: aws_region` | `aws_region_ap_southeast_1` | Gom theo region |
| `key: instance_type`, `prefix: type` | `type_t3_medium` | Gom theo loại máy |

> [!NOTE]
> Plugin "vệ sinh" giá trị tag khi đặt tên group: dấu `-`, `.`, ký tự đặc biệt bị đổi thành `_`. Vì vậy region `ap-southeast-1` thành group `aws_region_ap_southeast_1`. Khi viết `--limit`, dùng tên đã vệ sinh này.

### `compose` — tạo biến cho từng host

`compose` cho phép gán **biến host** từ thuộc tính instance. Phổ biến nhất là set `ansible_host` để Ansible biết SSH vào đâu:

```yaml
compose:
  ansible_host: private_ip_address   # Ansible SSH vào private IP
```

→ Giá trị bên phải là **biểu thức Jinja2** chiếu vào dữ liệu instance (như `private_ip_address`, `public_ip_address`, `instance_type`). Nếu Ansible chạy bên trong VPC (vd từ một bastion/CI runner cùng mạng), dùng `private_ip_address`; nếu chạy từ ngoài Internet thì dùng `public_ip_address`.

> [!WARNING]
> Trong `compose`, vế phải là **tên thuộc tính của plugin**, không phải chuỗi cố định. Viết `ansible_host: private_ip_address` (không dấu nháy) → lấy giá trị IP. Viết `ansible_host: "private_ip_address"` (có nháy) → mọi host nhận đúng chuỗi literal `"private_ip_address"` và Ansible cố SSH vào hostname vô nghĩa đó. Đây là lỗi cấu hình rất hay gặp.

---

## 4️⃣ Kiểm tra inventory — `ansible-inventory`

Viết file xong, **đừng** chạy playbook ngay. Luôn kiểm tra inventory trước bằng lệnh `ansible-inventory` để chắc Ansible "nhìn thấy" đúng máy và đúng group. Đây là thói quen cứu bạn khỏi việc chạy playbook lên nhầm máy.

### `--graph` — xem cây group trực quan

`--graph` in ra cây group → host, rất dễ đọc để xác nhận việc gom nhóm đúng:

```bash
ansible-inventory -i inventory.aws_ec2.yml --graph
```

Kết quả mong đợi (giả định Acme có 2 web prod, 1 db prod, 1 web staging):

```
@all:
  |--@aws_ec2:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-db-01
  |  |--acme-web-staging-01
  |--@env_prod:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-db-01
  |--@env_staging:
  |  |--acme-web-staging-01
  |--@role_web:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-web-staging-01
  |--@role_db:
  |  |--acme-db-01
  |--@aws_region_ap_southeast_1:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-db-01
  |  |--acme-web-staging-01
  |--@ungrouped:
```

→ Đọc kết quả: dấu `@` đứng trước **tên group**, dòng thụt vào là **host** thuộc group đó. Group `aws_ec2` chứa tất cả máy plugin tìm thấy. Group `env_prod` (tự sinh từ tag `Environment=prod`) gom đúng 3 máy prod — đây chính là group bạn sẽ nhắm tới khi deploy. Nếu thấy `@ungrouped` có host lạ → máy đó thiếu tag, cần kiểm tra lại trên AWS Console.

### `--list` — xem dữ liệu JSON đầy đủ

`--list` in toàn bộ inventory dạng JSON, bao gồm cả biến host (`hostvars`). Dùng khi cần soi giá trị biến cụ thể như `ansible_host`:

```bash
ansible-inventory -i inventory.aws_ec2.yml --list
```

Kết quả (rút gọn — phần `_meta` chứa hostvars):

```json
{
    "env_prod": {
        "hosts": ["acme-web-01", "acme-web-02", "acme-db-01"]
    },
    "_meta": {
        "hostvars": {
            "acme-web-01": {
                "ansible_host": "10.0.1.34",
                "instance_type_var": "t3.medium",
                "tags": {
                    "Environment": "prod",
                    "Role": "web",
                    "Project": "acme-shop"
                }
            }
        }
    }
}
```

→ Để ý `acme-web-01` có `ansible_host: "10.0.1.34"` — đúng là private IP từ `compose`. Biến `tags` cho thấy đầy đủ tag instance, bạn có thể dùng chúng trong playbook (vd `when: tags.Environment == "prod"`). Nếu `ansible_host` ra rỗng hoặc là chuỗi literal → quay lại kiểm tra khối `compose`.

> [!TIP]
> Thêm `--vars` vào `--graph` để vừa thấy cây group vừa thấy biến: `ansible-inventory -i inventory.aws_ec2.yml --graph --vars`. Còn `--host acme-web-01` in biến của đúng 1 host — tiện khi debug một máy cụ thể.

---

## 5️⃣ Caching — đừng gọi API cloud mỗi lần chạy

Mỗi lần `ansible-inventory` hay `ansible-playbook` chạy, plugin gọi lại API AWS. Khi bạn chạy chục lệnh liên tiếp lúc debug, điều này vừa **chậm** vừa có thể chạm **rate limit** của AWS (AWS giới hạn số lần gọi API/giây). Giải pháp: bật **cache** — plugin lưu kết quả lần gọi đầu vào đĩa, các lần sau đọc cache thay vì gọi lại API.

Bật cache ngay trong file plugin:

```yaml
# inventory.aws_ec2.yml — thêm khối cache
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1

# Bật cache: lần đầu gọi API, các lần sau (trong 600s) đọc từ đĩa
cache: true
cache_plugin: jsonfile
cache_timeout: 600
cache_connection: /tmp/ansible_inventory_cache
```

→ Phân tích từng dòng:

- `cache: true` — bật cache cho plugin này.
- `cache_plugin: jsonfile` — lưu cache dạng file JSON (đơn giản, không cần Redis). Có thể đổi sang `redis`/`memcached` cho team lớn.
- `cache_timeout: 600` — cache sống 600 giây; sau đó plugin gọi lại API để làm tươi.
- `cache_connection` — thư mục chứa file cache.

> [!IMPORTANT]
> Cache là con dao hai lưỡi với hạ tầng động. `cache_timeout` quá dài → vừa scale-out 5 node mới nhưng Ansible vẫn dùng danh sách cũ, **bỏ sót** node mới. Quá ngắn → mất tác dụng cache. Với auto-scaling chạy thật, thường để ngắn (vài phút) hoặc xoá cache thủ công trước khi deploy quan trọng. Xoá cache nhanh: `rm -rf /tmp/ansible_inventory_cache` (hoặc thêm `--flush-cache` khi chạy `ansible-playbook`).

Bạn cũng có thể bật cache toàn cục trong `ansible.cfg` thay vì lặp ở từng file plugin:

```ini
# ansible.cfg
[inventory]
cache = true
cache_plugin = jsonfile
cache_timeout = 600
cache_connection = /tmp/ansible_inventory_cache
```

---

## 6️⃣ Gộp nhiều nguồn — plugin `constructed`

Acme Shop không chỉ chạy AWS. Một phần dịch vụ analytics nằm trên **GCP (Google Compute Engine)**. Bạn muốn một số group "xuyên cloud" — vd group `webserver` gồm **cả** web node trên EC2 lẫn web node trên GCE, để chạy chung một playbook.

Cách làm: dùng **nhiều file inventory cùng lúc**, mỗi file một nguồn, đặt chung trong một thư mục. Ansible nạp tất cả file trong thư mục `-i` và **gộp** lại.

Cấu trúc thư mục:

```
inventory/
├── aws.aws_ec2.yml         # nguồn EC2 (plugin amazon.aws.aws_ec2)
├── gcp.gcp_compute.yml     # nguồn GCE (plugin google.cloud.gcp_compute)
└── 99-constructed.yml      # plugin constructed: gom group xuyên cloud
```

File GCP tương tự AWS, đổi plugin và key tag (GCP gọi tag là *label*):

```yaml
# inventory/gcp.gcp_compute.yml
plugin: google.cloud.gcp_compute
projects:
  - acme-analytics-prod
zones:
  - asia-southeast1-a
auth_kind: serviceaccount        # xác thực bằng service account
keyed_groups:
  - key: labels.environment
    prefix: env
  - key: labels.role
    prefix: role
hostnames:
  - name
compose:
  ansible_host: networkInterfaces[0].networkIP
```

Giờ tới ngôi sao của phần này — plugin **`constructed`**. Nó **không** gọi cloud nào cả; nhiệm vụ của nó là **tạo group/biến mới dựa trên dữ liệu các plugin khác đã nạp**. Nhờ nó, EC2 và GCE — vốn dùng cú pháp tag khác nhau — được quy về một group thống nhất:

```yaml
# inventory/99-constructed.yml
plugin: constructed
strict: false

groups:
  # Gom mọi host (bất kể AWS hay GCP) có role=web vào 1 group "webserver"
  webserver: tags.Role | default(labels.role) | default('') == 'web'
  database: tags.Role | default(labels.role) | default('') == 'db'

keyed_groups:
  # Tạo group theo cloud nguồn để vẫn phân biệt được khi cần
  - key: ansible_facts.system_vendor | default('unknown')
    prefix: vendor
```

→ Phân tích: khối `groups` dùng biểu thức Jinja2 trả về true/false để quyết định host có vào group hay không. EC2 lưu vai trò ở `tags.Role`, GCE lưu ở `labels.role` — biểu thức `tags.Role | default(labels.role)` xử lý cả hai. Kết quả: group `webserver` chứa web node từ **cả hai cloud**, và một playbook duy nhất phục vụ được toàn bộ.

> [!NOTE]
> Đặt tên file `99-constructed.yml` với tiền tố số lớn là cố ý: Ansible nạp file inventory theo thứ tự bảng chữ cái/số, nên `constructed` (phụ thuộc dữ liệu nguồn khác) phải nạp **sau** các plugin cloud (`aws.*`, `gcp.*`). Đặt số `99` đảm bảo nó luôn chạy cuối.

Chạy với cả thư mục (truyền thư mục thay vì 1 file):

```bash
ansible-inventory -i inventory/ --graph
```

→ Lúc này cây group có cả host AWS lẫn GCP, cộng thêm group `webserver`/`database` do `constructed` tạo, gom xuyên cloud.

---

## 7️⃣ Bảo mật credential — KHÔNG hardcode key

Đây là phần dễ gây sự cố bảo mật nghiêm trọng nhất. Plugin cần quyền gọi API cloud, nhưng **tuyệt đối không** nhúng `aws_access_key` / `aws_secret_key` vào file `aws_ec2.yml` rồi commit lên Git.

❌ **Anti-pattern** — nhúng key vào file plugin rồi commit:

```yaml
# inventory.aws_ec2.yml — TUYỆT ĐỐI KHÔNG làm thế này
plugin: amazon.aws.aws_ec2
aws_access_key: AKIAIOSFODNN7EXAMPLE
aws_secret_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

→ File này commit lên repo (kể cả private) là rò rỉ key. Bot quét GitHub tìm được trong vài phút, dùng key đào Bitcoin trên tài khoản AWS của bạn → hoá đơn nghìn đô.

✅ **Pattern đúng — thứ tự ưu tiên từ an toàn nhất**:

**1. IAM role (an toàn nhất — khi Ansible chạy trên EC2/CI trong AWS)**: gắn **IAM instance profile** cho con máy chạy Ansible (bastion, CI runner). Máy đó tự có quyền tạm thời, **không có key nào tồn tại trên đĩa**. File plugin để trống phần credential — `boto3` tự lấy quyền từ metadata của instance.

```yaml
# inventory.aws_ec2.yml — KHÔNG có dòng key nào, boto3 tự lấy từ IAM role
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
filters:
  tag:Project: acme-shop
```

**2. Biến môi trường (khi chạy ngoài AWS, vd laptop)**: đặt key vào biến môi trường thay vì file. `boto3` tự đọc:

```bash
# Đặt key vào env, không lưu vào file inventory
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="wJal..."
export AWS_DEFAULT_REGION="ap-southeast-1"

ansible-inventory -i inventory.aws_ec2.yml --graph
```

**3. AWS profile (`~/.aws/credentials`)**: dùng `aws configure` lưu key vào file profile chuẩn của AWS CLI (nằm ngoài repo), rồi trỏ plugin tới profile:

```yaml
# inventory.aws_ec2.yml — dùng profile, key nằm trong ~/.aws/credentials (ngoài repo)
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
aws_profile: acme-prod
```

> [!CAUTION]
> Quy tắc sống còn: **key bí mật KHÔNG bao giờ nằm trong file được commit**. Thứ tự ưu tiên 2026: IAM role > biến môi trường > AWS profile > (cuối cùng, nếu buộc phải) Ansible Vault mã hoá. Bonus: cấp IAM cho Ansible **quyền tối thiểu** — chỉ cần `ec2:DescribeInstances` để liệt kê inventory, không cần quyền tạo/xoá máy.

Với GCP, nguyên tắc y hệt: ưu tiên service account gắn sẵn cho máy (workload identity), hoặc trỏ tới file service-account JSON qua biến môi trường `GOOGLE_APPLICATION_CREDENTIALS` thay vì nhúng nội dung JSON vào file inventory.

---

## 8️⃣ Hands-on — gom EC2 prod của Acme rồi chạy playbook

Mục tiêu cuối: từ con số 0, dựng dynamic inventory gom các EC2 có tag `Environment=prod` thành group `env_prod`, kiểm tra, rồi chạy một playbook lên đúng group đó.

### 🛠️ Bước 1: Cài collection và boto3

```bash
ansible-galaxy collection install amazon.aws
python3 -m pip install boto3 botocore
```

### 🛠️ Bước 2: Cấp credential qua biến môi trường

Giả sử bạn chạy từ laptop (chưa có IAM role). Đặt key vào env, **không** viết vào file:

```bash
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="wJal..."
export AWS_DEFAULT_REGION="ap-southeast-1"
```

### 🛠️ Bước 3: Viết file `inventory.aws_ec2.yml`

Lưu ý tên file kết thúc bằng `aws_ec2.yml`. Ở đây ta gom theo `Environment` và set `ansible_host` = public IP (vì chạy từ laptop ngoài VPC):

```yaml
# inventory.aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
filters:
  instance-state-name: running
  tag:Project: acme-shop
hostnames:
  - tag:Name
keyed_groups:
  - key: tags.Environment
    prefix: env
  - key: tags.Role
    prefix: role
compose:
  ansible_host: public_ip_address
```

### 🛠️ Bước 4: Kiểm tra inventory thấy đúng group `env_prod`

```bash
ansible-inventory -i inventory.aws_ec2.yml --graph
```

Kết quả mong đợi:

```
@all:
  |--@aws_ec2:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-web-staging-01
  |--@env_prod:
  |  |--acme-web-01
  |  |--acme-web-02
  |--@env_staging:
  |  |--acme-web-staging-01
  |--@role_web:
  |  |--acme-web-01
  |  |--acme-web-02
  |  |--acme-web-staging-01
  |--@ungrouped:
```

→ Group `env_prod` đã gom đúng 2 máy prod (`acme-web-01`, `acme-web-02`); `acme-web-staging-01` nằm ở `env_staging`. Đây là bằng chứng tag đã được gom thành group đúng như mong muốn.

### 🛠️ Bước 5: Ping thử group `env_prod`

Trước khi chạy playbook thật, ping (`-m ping`) để chắc Ansible SSH vào được các máy trong group:

```bash
ansible -i inventory.aws_ec2.yml env_prod -m ansible.builtin.ping
```

Kết quả mong đợi:

```
acme-web-01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
acme-web-02 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

→ `pong` trên cả 2 máy nghĩa là Ansible kết nối SSH thành công và Python sẵn sàng. Nếu một máy báo `UNREACHABLE` → kiểm tra Security Group (port 22), SSH key, hoặc giá trị `ansible_host` trong `compose`.

### 🛠️ Bước 6: Viết playbook và chạy lên `env_prod`

Tận dụng role `webserver` bạn đã build ở cụm basic. Playbook chỉ nhắm vào group động `env_prod`:

```yaml
# deploy-prod.yml
- name: Cấu hình web tier prod của Acme (dynamic inventory)
  hosts: env_prod          # group này do plugin tự sinh từ tag Environment=prod
  become: true
  roles:
    - webserver
```

Chạy playbook với file dynamic inventory thay cho `inventory.ini` tĩnh:

```bash
ansible-playbook -i inventory.aws_ec2.yml deploy-prod.yml
```

Kết quả mong đợi (rút gọn):

```
PLAY [Cấu hình web tier prod của Acme (dynamic inventory)] ********

TASK [Gathering Facts] *******************************************
ok: [acme-web-01]
ok: [acme-web-02]

TASK [webserver : Cài gói nginx] *********************************
changed: [acme-web-01]
changed: [acme-web-02]

TASK [webserver : Sinh và đẩy config site] **********************
changed: [acme-web-01]
changed: [acme-web-02]

RUNNING HANDLER [webserver : Reload nginx] **********************
changed: [acme-web-01]
changed: [acme-web-02]

PLAY RECAP *******************************************************
acme-web-01 : ok=5    changed=3    unreachable=0    failed=0
acme-web-02 : ok=5    changed=3    unreachable=0    failed=0
```

→ Playbook chạy **chính xác lên 2 máy prod** mà bạn **không gõ một IP nào**. Tuần sau Acme scale-out thêm node prod thứ 3 — bạn chạy lại đúng lệnh này, node mới tự xuất hiện trong `env_prod` và được cấu hình ngay. Đó là sức mạnh của dynamic inventory: hạ tầng co giãn bao nhiêu, lệnh deploy của bạn vẫn y nguyên.

> [!TIP]
> Vẫn dùng được `--limit` để thu hẹp thêm. Vd chỉ deploy 1 máy để canary test: `ansible-playbook -i inventory.aws_ec2.yml deploy-prod.yml --limit acme-web-01`. Hoặc giao nhau group: `--limit 'env_prod:&role_web'` = máy vừa prod vừa web.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: đặt sai tên file plugin → Ansible báo "no hosts"

- **Triệu chứng**: `ansible-inventory --graph` chỉ hiện `@all:` và `@ungrouped:` rỗng, dù AWS có hàng chục instance đang chạy.
- **Nguyên nhân**: file không kết thúc bằng `aws_ec2.yml`/`aws_ec2.yaml` (vd đặt là `inventory.yml`), nên Ansible coi nó là YAML thường chứ không kích hoạt plugin. Hoặc plugin chưa được bật trong `ansible.cfg`.
- **Cách tránh**: đặt tên đúng đuôi `*.aws_ec2.yml`. Nếu vẫn lỗi, bật plugin trong `ansible.cfg`: thêm `enable_plugins = amazon.aws.aws_ec2, constructed` vào mục `[inventory]`. Chạy `ansible-inventory -i ... --list -vvv` để xem log nạp plugin.

### ❌ Cạm bẫy: cache cũ làm bỏ sót node vừa scale-out

- **Triệu chứng**: vừa scale ASG lên 5 node, nhưng playbook chỉ chạy lên 3 node cũ; node mới như "tàng hình".
- **Nguyên nhân**: cache inventory còn hạn (`cache_timeout` chưa hết), Ansible đọc danh sách cũ thay vì gọi API tươi.
- **Cách tránh**: trước deploy quan trọng, chạy kèm `--flush-cache`, hoặc đặt `cache_timeout` ngắn cho môi trường co giãn mạnh. Xoá tay: `rm -rf <cache_connection>`.

### ❌ Cạm bẫy: hardcode credential vào file plugin

- **Triệu chứng**: key AWS bị lộ, hoá đơn AWS tăng đột biến, AWS gửi cảnh báo bảo mật.
- **Nguyên nhân**: nhúng `aws_access_key`/`aws_secret_key` thẳng vào `aws_ec2.yml` rồi commit lên Git — bot quét repo tìm thấy.
- **Cách tránh**: dùng IAM role (tốt nhất) hoặc biến môi trường. Không bao giờ commit key. Thêm pattern key vào `.gitignore` và bật secret scanning trên repo.

### ✅ Best practice: luôn `ansible-inventory --graph` trước khi `ansible-playbook`

- **Vì sao**: với inventory động, bạn không "nhìn thấy" danh sách host trong file như inventory tĩnh. Một filter sai có thể khiến playbook chạy lên nhầm hoặc thiếu máy. Kiểm tra graph là cách rẻ nhất để bắt lỗi trước khi thay đổi máy thật.
- **Cách áp dụng**: biến `ansible-inventory -i ... --graph` thành bước bắt buộc trong quy trình. Ghép với `ping` để xác nhận kết nối, rồi mới `--check` (dry-run), cuối cùng mới apply thật.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Vì sao inventory tĩnh (`inventory.ini`) không dùng được với Auto Scaling Group?

<details>
<summary>💡 Xem giải thích</summary>

ASG sinh/diệt instance liên tục và IP do AWS cấp động, không biết trước. File tĩnh viết tay không thể cập nhật kịp số lượng node và IP thay đổi → bỏ sót node mới (không được cấu hình → config drift), hoặc trỏ tới IP đã bị tái cấp cho máy khác (chạy nhầm máy). Dynamic inventory hỏi cloud lúc chạy nên luôn phản ánh đúng hiện trạng.

</details>

**Q2.** Phân biệt dynamic inventory script (`ec2.py`) và inventory plugin (`aws_ec2.yml`). Cái nào nên dùng năm 2026?

<details>
<summary>💡 Xem giải thích</summary>

Script cũ là file Python thực thi, tự gọi API và in JSON — đã deprecated, cấu hình group/biến phải sửa code. Plugin mới chỉ là file YAML khai báo (`plugin:`, `keyed_groups`, `compose`...), nằm trong collection `amazon.aws`, có cache sẵn, là **chuẩn chính thức 2026**. Nên dùng plugin `amazon.aws.aws_ec2`.

</details>

**Q3.** `filters` và `keyed_groups` khác nhau ở đâu? Khi nào dùng cái nào?

<details>
<summary>💡 Xem giải thích</summary>

`filters` lọc **phía AWS trước khi tải về** — loại bỏ hẳn instance không cần (vd chỉ lấy `running`, chỉ lấy project acme-shop), giảm dữ liệu truyền. `keyed_groups` chạy **phía Ansible sau khi đã tải về** — gom các máy đã lấy thành group theo giá trị tag (vd `Environment=prod` → group `env_prod`). Loại bỏ máy → `filters`; gom nhóm → `keyed_groups`.

</details>

**Q4.** Tại sao không nên đặt `cache_timeout` quá dài cho hạ tầng auto-scaling?

<details>
<summary>💡 Xem giải thích</summary>

Cache lưu danh sách host của lần gọi API trước. Nếu timeout dài, sau khi ASG scale-out node mới, Ansible vẫn đọc danh sách cũ trong cache và **bỏ sót** node mới (không cấu hình node đó). Với hạ tầng co giãn mạnh nên để timeout ngắn hoặc chạy `--flush-cache` trước deploy quan trọng.

</details>

**Q5.** Cách an toàn nhất để cấp quyền cho Ansible gọi API EC2 khi nó chạy trên một máy trong AWS là gì?

<details>
<summary>💡 Xem giải thích</summary>

Gắn **IAM role (instance profile)** cho con máy chạy Ansible. Khi đó `boto3` tự lấy quyền tạm thời từ metadata của instance — **không có key bí mật nào nằm trên đĩa hay trong file**, không có gì để lộ qua Git. Nên cấp quyền tối thiểu (`ec2:DescribeInstances`) thay vì full access.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh / Cú pháp |
|---|---|
| Cài collection AWS + GCP | `ansible-galaxy collection install amazon.aws google.cloud` |
| Cài SDK AWS cho plugin | `python3 -m pip install boto3 botocore` |
| Xem cây group | `ansible-inventory -i inventory.aws_ec2.yml --graph` |
| Xem JSON đầy đủ + hostvars | `ansible-inventory -i inventory.aws_ec2.yml --list` |
| Xem biến 1 host | `ansible-inventory -i inventory.aws_ec2.yml --host acme-web-01` |
| Ping group động | `ansible -i inventory.aws_ec2.yml env_prod -m ansible.builtin.ping` |
| Chạy playbook lên group động | `ansible-playbook -i inventory.aws_ec2.yml deploy-prod.yml` |
| Bỏ qua cache khi chạy | `ansible-playbook -i inventory.aws_ec2.yml site.yml --flush-cache` |
| Giới hạn 1 host (canary) | `ansible-playbook -i inventory.aws_ec2.yml site.yml --limit acme-web-01` |
| Giao nhau 2 group | `--limit 'env_prod:&role_web'` |
| Nạp cả thư mục nhiều nguồn | `ansible-inventory -i inventory/ --graph` |

```yaml
# Mẫu file inventory.aws_ec2.yml tối thiểu
plugin: amazon.aws.aws_ec2
regions:
  - ap-southeast-1
filters:
  instance-state-name: running
keyed_groups:
  - key: tags.Environment
    prefix: env
compose:
  ansible_host: private_ip_address
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| Static inventory | Inventory tĩnh | File liệt kê host cố định bằng tay (`inventory.ini`) |
| Dynamic inventory | Inventory động | Danh sách host sinh lúc chạy bằng cách hỏi nguồn ngoài (cloud API) |
| Inventory plugin | Plugin inventory | Cơ chế chuẩn 2026 lấy host từ nguồn ngoài qua file YAML khai báo |
| Inventory script | Script inventory | Cách cũ (file thực thi in JSON), nay đã deprecated |
| Auto Scaling Group (ASG) | Nhóm tự co giãn | Dịch vụ AWS tự tăng/giảm số EC2 theo tải |
| `aws_ec2` plugin | (giữ nguyên) | Plugin của collection `amazon.aws` lấy host từ EC2 |
| `gcp_compute` plugin | (giữ nguyên) | Plugin của `google.cloud` lấy host từ GCE |
| `keyed_groups` | Group theo khoá | Tự sinh group từ giá trị tag/thuộc tính instance |
| `filters` | Bộ lọc | Lọc instance ngay phía cloud trước khi tải về |
| `compose` | Tạo biến | Gán biến host từ thuộc tính instance (vd `ansible_host`) |
| `hostnames` | Nguồn đặt tên | Danh sách ưu tiên chọn tên hiển thị cho host |
| `constructed` plugin | (giữ nguyên) | Plugin gộp/tạo group dựa trên dữ liệu plugin khác |
| Cache (inventory) | Bộ nhớ đệm | Lưu kết quả gọi API để lần sau khỏi gọi lại |
| IAM role | Vai trò IAM | Quyền tạm thời gắn cho máy AWS, không cần key trên đĩa |
| Instance profile | Hồ sơ instance | Cách gắn IAM role vào một EC2 instance |
| boto3 | (giữ nguyên) | SDK Python chính thức của AWS, plugin EC2 dùng để gọi API |
| Tag (AWS) / Label (GCP) | Nhãn | Cặp key-value gắn lên resource để phân loại |
| Config drift | Lệch cấu hình | Trạng thái thực tế các máy lệch khỏi cấu hình mong muốn |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Configuration Management Intermediate — Khi Ansible gặp quy mô Production](00_intermediate-overview.md)
- ➡️ **Bài tiếp theo:** [Advanced Playbooks — Hiệu năng, error handling & rolling update zero-downtime](02_advanced-playbooks-and-strategies.md)
- ↑ **Về cụm:** [Configuration Management — README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- [Playbooks & Roles — Cấu trúc, biến, Jinja2 template, tái sử dụng](../01_basic/02_playbooks-and-roles.md) — role `webserver` dùng lại trong hands-on bài này
- [Testing Ansible — ansible-lint & Molecule cho role đáng tin cậy](03_testing-with-molecule.md) — test role trước khi chạy lên cloud thật
- [AWX / Ansible Automation Platform & vận hành CM quy mô lớn](04_awx-aap-and-at-scale.md) — vận hành inventory động tập trung
- [EC2 & EBS — Compute trên AWS](../../../../11_cloud/aws/lessons/01_basic/01_ec2-and-ebs-compute.md) — hiểu EC2/tag mà plugin truy vấn

### 🌐 Tài nguyên tham khảo khác

- [amazon.aws.aws_ec2 inventory plugin](https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html) — spec đầy đủ option của plugin EC2
- [google.cloud.gcp_compute inventory plugin](https://docs.ansible.com/ansible/latest/collections/google/cloud/gcp_compute_inventory.html) — plugin cho GCE
- [Ansible — Working with dynamic inventory](https://docs.ansible.com/ansible/latest/inventory_guide/intro_dynamic_inventory.html) — hướng dẫn chính thức
- [ansible.builtin.constructed inventory plugin](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/constructed_inventory.html) — gộp nhiều nguồn

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (13/06/2026)** — Bản đầu tiên. Cover: vì sao inventory tĩnh chết với auto-scaling, dynamic inventory script (cũ) vs inventory plugin (chuẩn 2026), cài collection `amazon.aws`/`google.cloud` + boto3, mổ xẻ file `aws_ec2.yml` (regions/filters/hostnames/keyed_groups/compose), kiểm tra bằng `ansible-inventory --graph`/`--list`, caching inventory, plugin `constructed` gộp EC2+GCE, bảo mật credential (IAM role/env/profile), hands-on gom EC2 `Environment=prod` thành group `env_prod` rồi chạy playbook role `webserver` lên đó.
