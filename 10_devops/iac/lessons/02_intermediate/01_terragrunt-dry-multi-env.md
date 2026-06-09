# 🎓 Terragrunt — DRY Terraform cho multi-env multi-region

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 07/06/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [IaC Intermediate — Tổng quan](00_intermediate-overview.md), đã nắm Terraform *modules* và *workspaces*.

> 🎯 *3 môi trường × 5 region × 5 module = 75 folder, mỗi folder lại copy gần như nguyên xi nhau, cộng dồn thành hàng chục nghìn dòng trùng lặp. Sửa một dòng CIDR cũng phải mò qua chục file và cầu trời không quên cái nào. Bài này chỉ cho bạn dùng **Terragrunt** để giữ DRY: một module Terraform duy nhất, mỗi env chỉ còn một file config chừng mười dòng. Đi qua từ nền tảng, cấu trúc repo, dependency giữa các module, versioning module, `run-all`, cho tới các pattern multi-account nâng cao.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Terragrunt** khác *workspaces* ở đâu và khi nào nên chọn cái nào.
- [ ] Dựng cấu trúc repo theo pattern **`live/` + `modules/`**.
- [ ] Dùng **`include`** + **`generate`** + **`inputs`** trong `terragrunt.hcl`.
- [ ] Quản lý **remote state** với S3 + DynamoDB được sinh tự động.
- [ ] Khai báo **dependency** giữa các module (`dependency` block).
- [ ] Dùng **`run-all`** để apply nhiều module một lượt.
- [ ] Quản lý **version của module** bằng git tag.
- [ ] Thiết lập **multi-account AWS** với *assume role*.

---

## Tình huống — Đổi VPC CIDR = sửa 15 file

Hãy bắt đầu từ một cảnh quen với bất kỳ ai từng quản hạ tầng nhiều môi trường bằng Terraform thuần. Repo của bạn được tổ chức theo kiểu "copy folder cho mỗi env, mỗi region", trông gọn gàng nhưng ẩn chứa quả bom trùng lặp:

```text
infra/
├── dev/
│   ├── us-east-1/vpc/
│   │   ├── main.tf      # 200 dòng
│   │   ├── variables.tf
│   │   └── backend.tf   # config S3 backend — 20 dòng, lặp y hệt trong cả 75 folder
│   ├── us-west-2/vpc/   # bản copy của us-east-1/vpc
│   ├── eu-west-1/vpc/   # copy
│   └── ...
├── staging/  # copy của dev
└── prod/     # copy của dev, chỉ khác CIDR
```

Vấn đề lộ ra ngay khi có một yêu cầu nhỏ: đổi CIDR của VPC cho môi trường prod. Đáng lẽ chỉ là một dòng, nhưng thực tế bạn phải sửa `prod/us-east-1/vpc/variables.tf`, rồi kiểm tra 4 region còn lại, rồi soát lại cả staging cho chắc.

Và đây là hai cái bẫy quen thuộc mọc lên từ kiểu repo này:

- Ai đó quên cập nhật `prod/us-west-2/vpc/` → cấu hình lệch nhau (*drift*), prod mỗi region một kiểu.
- Review code thành cơn ác mộng: một PR đụng tới 5+ file gần như giống hệt nhau, người review chẳng biết nhìn vào đâu.

Sếp đi ngang, liếc qua cái PR rồi gợi ý: *"Refactor sang Terragrunt đi. Một module, N config thôi."* Đó chính là chủ đề của bài này.

---

## 1️⃣ Terragrunt là gì?

Trước khi sửa được bệnh trùng lặp, cần hiểu Terragrunt thực chất là cái gì và nó đứng ở đâu so với Terraform.

**Terragrunt** là một lớp bọc mỏng (*thin wrapper*) quanh Terraform, sinh ra để xoá bỏ trùng lặp. Nó không thay thế Terraform mà chạy *bên ngoài*, gọi Terraform underneath. Bốn việc chính nó làm cho bạn:

- Giữ code module Terraform ở đúng một nơi duy nhất.
- Để config cho từng env (`terragrunt.hcl`) tối giản hết mức.
- Cho phép kế thừa rồi ghi đè (*inherit + override*) cấu hình chung.
- Tự sinh `backend.tf`, `provider.tf` từ config thay vì bắt bạn copy tay.

### So với workspaces

Câu hỏi đầu tiên ai cũng hỏi: "Đã có Terraform *workspaces* rồi, sao còn cần Terragrunt?" Workspaces cũng tách được nhiều môi trường, nhưng nó dừng ở mức khá hẹp. Bảng dưới đặt hai cách cạnh nhau để thấy ranh giới:

| Khía cạnh | Terraform workspaces | **Terragrunt** |
|---|---|---|
| Backend | Cùng một backend, mỗi workspace một state file | Backend riêng cho từng env (state cách ly hẳn) |
| Chuyển môi trường | `terraform workspace select prod` | `cd` vào folder env tương ứng |
| Biến cấu hình | Qua file `terraform.tfvars` | Qua `inputs` kế thừa nhiều tầng |
| Multi-region | Vẫn phải copy folder (workspace gói trong 1 thư mục) | Multi-region, multi-account *native* |
| Dependency | Không có | `dependency` block giữa các module |
| Bố cục phức tạp | Khó mở rộng | Linh hoạt cho layout lớn |

Điểm cốt lõi để nhớ: workspaces giải quyết "nhiều state trên cùng một backend trong cùng một thư mục", còn Terragrunt giải quyết "nhiều env/region/account với state cách ly và có quan hệ phụ thuộc lẫn nhau". Phần còn lại của bài là khai thác đúng điểm khác biệt đó.

🪞 **Ẩn dụ**: *Một module Terraform giống **bản thiết kế nhà mẫu** — 3 phòng ngủ, 2 phòng tắm, một cái sân. Còn config Terragrunt giống **tấm nhãn dán cho từng căn nhà cụ thể**: "Căn số 1: môi trường dev, vùng us-east-1, cỡ nhỏ". Bạn cần một bản thiết kế + 75 tấm nhãn, chứ không phải vẽ lại 75 bản thiết kế giống hệt nhau.*

### Cài đặt

Terragrunt là một Go binary độc lập, cài bằng đúng một câu lệnh. Cài xong, nó tự đứng giữa bạn và Terraform để thêm lớp DRY (versioning module, dependency, config multi-env) mà không động gì tới bản Terraform đang có:

```bash
# macOS
brew install terragrunt

# Linux
wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.55.0/terragrunt_linux_amd64
chmod +x terragrunt_linux_amd64
sudo mv terragrunt_linux_amd64 /usr/local/bin/terragrunt

terragrunt --version
```

---

## 2️⃣ Pattern cấu trúc repo

Hiểu Terragrunt là gì rồi, việc đầu tiên khi bắt tay vào là dựng đúng bộ khung thư mục. Đây là phần quyết định mọi thứ về sau có gọn hay không.

### Bố cục chuẩn

Repo Terragrunt chuẩn tách làm **hai folder** với hai vai trò rạch ròi: `modules/` chứa code Terraform tái sử dụng được (phần DRY), còn `live/` chứa config Terragrunt cho từng env/region/component. Pattern này mở rộng mượt từ một env cho tới hàng trăm:

```text
infrastructure/
├── terragrunt.hcl              # config gốc (root)
├── modules/                    # các module Terraform
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   ├── rds/
│   └── s3/
└── live/                       # config theo từng env
    ├── dev/
    │   ├── account.hcl         # biến cấp account
    │   ├── us-east-1/
    │   │   ├── region.hcl      # biến cấp region
    │   │   ├── vpc/
    │   │   │   └── terragrunt.hcl    # ~10 dòng
    │   │   ├── eks/
    │   │   │   └── terragrunt.hcl
    │   │   ├── rds/
    │   │   │   └── terragrunt.hcl
    │   │   └── s3/
    │   │       └── terragrunt.hcl
    │   ├── us-west-2/...
    │   └── eu-west-1/...
    ├── staging/...
    └── prod/...
```

Cách đọc bố cục này rất đơn giản: `modules/` là nơi giữ code Terraform thật (viết một lần, dùng mọi nơi), còn `live/` chỉ chứa các file config mỏng mô tả "env này, region này muốn dùng module nào với tham số gì".

### Quy trình hằng ngày

Khi đã có bộ khung, công việc thường nhật cực kỳ đơn giản: `cd` vào đúng tổ hợp env + region + component rồi gõ `terragrunt plan`/`apply`. Terragrunt sẽ tự tải module về, sinh `backend.tf` + `provider.tf`, rồi gọi Terraform bên dưới:

```bash
# Plan VPC cho dev us-east-1
cd live/dev/us-east-1/vpc
terragrunt plan

# Apply EKS cho prod us-east-1
cd live/prod/us-east-1/eks
terragrunt apply
```

Toàn bộ phép màu "tải module, sinh backend, sinh provider, chạy init rồi apply" diễn ra ngầm sau một lệnh duy nhất. Phần tiếp theo sẽ mở từng lớp ra xem nó làm điều đó bằng cách nào.

---

## 3️⃣ File gốc `terragrunt.hcl`

Trái tim của cả hệ thống nằm ở file gốc — nơi khai báo những cấu hình chung mà *mọi* file con sẽ kế thừa. Viết tốt phần này thì mỗi file con về sau chỉ còn vài dòng. Hai khối quan trọng nhất là `remote_state` (sinh `backend.tf`) và `generate "provider"` (sinh `provider.tf`):

```hcl
# infrastructure/terragrunt.hcl

# Sinh backend.tf trong từng file con (khỏi lặp tay)
remote_state {
  backend = "s3"

  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }

  config = {
    bucket         = "acme-tfstate-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "acme-tfstate-lock"
  }
}

# Sinh provider.tf trong từng file con
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.env
      ManagedBy   = "Terragrunt"
      Repository  = "acme/infrastructure"
    }
  }

  assume_role {
    role_arn = "arn:aws:iam::$${var.aws_account_id}:role/TerraformExecutionRole"
  }
}
EOF
}

# inputs chung mà mọi file con đều thừa hưởng
inputs = {
  organization = "acme"
}
```

### Các tính năng then chốt

Trong file gốc trên có vài hàm và khối là lý do chính khiến người ta chọn Terragrunt thay vì workspaces. Mỗi cái giải một bài toán mà Terraform thuần không làm gọn được:

- **`generate`** — Terragrunt ghi hẳn một file (ví dụ `backend.tf`) vào folder con *trước khi* chạy Terraform, nên không cần copy tay file backend vào từng nơi.
- **`path_relative_to_include()`** — trả về đường dẫn tương đối từ root tới file con hiện tại, nhờ vậy mỗi env có một *key* state riêng biệt, không đụng nhau.
- **`get_aws_account_id()`** — một trong nhiều hàm dựng sẵn (*built-in functions*) cho phép lấy thông tin runtime mà chèn thẳng vào config.
- **`inputs`** — các biến được truyền xuống module, kế thừa từ tầng này sang tầng kia.

Ý tưởng chung: file gốc khai báo *một lần*, mọi file con thừa hưởng. Hai phần tiếp theo sẽ làm rõ "thừa hưởng từ đâu" — bắt đầu từ các biến cấp account và region.

---

## 4️⃣ Tầng account và region

Cấu hình không chỉ đến từ file gốc. Terragrunt còn cho bạn nhét các biến đặc thù vào từng tầng trung gian — account và region — rồi cho chúng "chảy" xuống các file con bên dưới. Đây là cách tách "cái gì thuộc về cả account" khỏi "cái gì thuộc về riêng một region".

### `account.hcl` — biến cấp account (cho từng env)

File này khai báo những thứ gắn liền với cả một tài khoản AWS: tên env, account ID. Mỗi env một file:

```hcl
# live/dev/account.hcl
locals {
  account_name = "dev"
  account_id   = "111111111111"
  env          = "dev"
}
```

```hcl
# live/prod/account.hcl
locals {
  account_name = "prod"
  account_id   = "222222222222"
  env          = "prod"
}
```

### `region.hcl` — biến cấp region

Tương tự, file này giữ những thứ đặc thù theo vùng: tên region và dải CIDR riêng của vùng đó. Mỗi region một file:

```hcl
# live/dev/us-east-1/region.hcl
locals {
  aws_region = "us-east-1"
  vpc_cidr   = "10.0.0.0/16"
}
```

```hcl
# live/dev/us-west-2/region.hcl
locals {
  aws_region = "us-west-2"
  vpc_cidr   = "10.1.0.0/16"
}
```

Mấu chốt là các biến account + region này sẽ *chảy xuống* (*cascade*) các file con thông qua khối `include` — đúng phần ta xem ngay sau đây.

---

## 5️⃣ File con `terragrunt.hcl`

Đây là nơi mọi mảnh ghép gặp nhau: file con thừa hưởng config gốc, đọc các biến account + region, rồi trỏ tới module thật và truyền tham số xuống. Vẻ đẹp của Terragrunt nằm cả ở chỗ file này ngắn đến bất ngờ.

### Module VPC đơn giản

```hcl
# live/dev/us-east-1/vpc/terragrunt.hcl

# Kế thừa config gốc (backend, provider, inputs chung)
include "root" {
  path = find_in_parent_folders()
}

# Đọc các file hcl cục bộ
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

# Nguồn của module Terraform
terraform {
  source = "../../../../modules/vpc"
  # HOẶC remote: source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.2.3"
}

# inputs ghi đè / mở rộng
inputs = {
  env             = local.account_vars.locals.env
  aws_account_id  = local.account_vars.locals.account_id
  region          = local.region_vars.locals.aws_region
  cidr_block      = local.region_vars.locals.vpc_cidr

  availability_zones = [
    "${local.region_vars.locals.aws_region}a",
    "${local.region_vars.locals.aws_region}b",
    "${local.region_vars.locals.aws_region}c",
  ]

  enable_nat_gateway = true
  single_nat_gateway = local.account_vars.locals.env == "dev"   # dev rẻ, prod chạy HA
}
```

Đếm lại sẽ thấy: cả file con cho một VPC chỉ khoảng **10 dòng** thực chất. Tất cả phần nặng nề — backend, provider, code module — đều được kế thừa từ root + account + region.

### Chuyện gì xảy ra khi chạy

Để hiểu file ngắn vậy mà vẫn đủ, hãy xem từng bước Terragrunt làm khi bạn gõ lệnh:

```bash
cd live/dev/us-east-1/vpc
terragrunt plan
```

Terragrunt sẽ lần lượt:

1. Đọc file `terragrunt.hcl` hiện tại.
2. Tìm file `terragrunt.hcl` gốc (qua `find_in_parent_folders`).
3. Kế thừa `remote_state`, `generate "provider"`, `inputs`.
4. Đọc các `locals` trong `account.hcl` + `region.hcl`.
5. Sinh `backend.tf` + `provider.tf` ngay tại folder hiện tại.
6. Chạy `terraform init` + `terraform plan`.

Kết quả là một lần apply sạch sẽ, với state file nằm đúng chỗ riêng của nó: `s3://acme-tfstate-..../live/dev/us-east-1/vpc/terraform.tfstate`. Mỗi env-region một key, không đụng nhau — chính nhờ `path_relative_to_include()` ở phần trước.

---

## 6️⃣ Dependency giữa các module

Tới đây bạn build được từng module độc lập. Nhưng hạ tầng thật không độc lập: EKS cần VPC tồn tại trước, RDS lại cần network sẵn sàng. Đây là lúc khối `dependency` toả sáng.

### Vấn đề

Trật tự bắt buộc: VPC phải có trước EKS, EKS phải có trước RDS. Không có Terragrunt, bạn phải tự nhớ thứ tự này và gõ apply đúng tuần tự bằng tay — quên thứ tự là apply chết ngay vì thiếu đầu vào.

### Khối `dependency`

Terragrunt cho phép một module *đọc output* của module khác và tự sắp xếp thứ tự apply. EKS chỉ cần khai báo nó phụ thuộc VPC, rồi lấy `vpc_id` và `subnet_ids` từ output của VPC:

```hcl
# live/dev/us-east-1/eks/terragrunt.hcl

include "root" {
  path = find_in_parent_folders()
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id     = "vpc-12345"
    subnet_ids = ["subnet-1", "subnet-2"]
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

terraform {
  source = "../../../../modules/eks"
}

inputs = {
  cluster_name = "acme-dev-us-east-1"
  vpc_id       = dependency.vpc.outputs.vpc_id
  subnet_ids   = dependency.vpc.outputs.private_subnet_ids
}
```

Khi chạy, Terragrunt sẽ kiểm tra state của VPC đã tồn tại chưa, đọc output (`vpc_id`, `private_subnet_ids`), tiêm chúng làm input cho EKS, rồi mới apply EKS với thông tin VPC thật.

Còn `mock_outputs` để làm gì? Đó là các giá trị giả dùng cho lệnh `plan` *khi VPC chưa được apply* — tình huống "con gà và quả trứng": muốn plan EKS nhưng VPC chưa tồn tại nên chưa có output thật. Mock cho phép plan chạy qua; còn apply thật thì bắt buộc VPC phải có trước.

### `terragrunt run-all`

Khi muốn apply *cả cây* module theo đúng thứ tự phụ thuộc mà không phải `cd` qua từng folder, dùng `run-all`:

```bash
cd live/dev/us-east-1
terragrunt run-all apply
```

Terragrunt sẽ quét toàn bộ `terragrunt.hcl` trong cây thư mục, dựng đồ thị phụ thuộc, apply theo thứ tự topo (VPC → EKS → RDS), và chạy song song những module độc lập với nhau (ví dụ S3 + DynamoDB không phụ thuộc VPC).

> ⚠️ `run-all` mạnh nhưng nguy hiểm, phải dùng cẩn thận. `run-all destroy` sẽ xoá sạch mọi thứ trong cây; lock có thể đụng nhau khi chạy song song. Dùng `--terragrunt-include-dir` / `--terragrunt-exclude-dir` để giới hạn phạm vi.

---

## 7️⃣ Versioning cho module

Module dùng chung cho nhiều env mở ra một bài toán mới: làm sao nâng cấp module cho dev mà không vô tình làm vỡ prod? Câu trả lời là gán *version* cho module.

### Vấn đề

Khi module `modules/vpc/` nằm chung *monorepo* với code live, mọi env đều trỏ tới cùng một bản code. Bạn vừa sửa module để thử trên dev là prod cũng "ăn" thay đổi đó luôn — cực kỳ rủi ro. Cách chữa là tách module ra và đánh version cho nó.

### Pattern: tách module sang repo riêng

Đưa toàn bộ module sang một repo độc lập, ví dụ `infrastructure-modules`:

```text
infrastructure-modules/   (repo riêng)
├── vpc/
├── eks/
├── rds/
└── ...
```

Mỗi lần module ổn định, gắn một git tag để đóng băng phiên bản: `v1.2.0`, `v1.3.0`, v.v.

### Tham chiếu trong Terragrunt

Lúc này mỗi env có thể *ghim* vào một version khác nhau. Dev có thể chạy bản mới nhất trong khi prod vẫn ở bản cũ đã được kiểm chứng:

```hcl
# live/dev/us-east-1/vpc/terragrunt.hcl
terraform {
  source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.2.0"
}

# live/prod/us-east-1/vpc/terragrunt.hcl
terraform {
  source = "git::git@github.com:acme/infrastructure-modules.git//vpc?ref=v1.0.0"
  # prod ghim bản cũ hơn
}
```

Nhờ vậy bạn có một quy trình promote an toàn: nâng dev lên `v1.3.0` trước → kiểm thử → rồi mới promote prod lên `v1.3.0` sau.

### Quy trình tag

Vòng đời một bản release gọn trong vài lệnh — tag ở repo module, đổi `ref` ở repo live rồi apply:

```bash
# Trong repo module
git tag v1.3.0
git push origin v1.3.0

# Trong repo live
# Sửa terragrunt.hcl thành ref=v1.3.0
terragrunt plan   # tải v1.3.0 về
terragrunt apply
```

---

## 8️⃣ Pattern multi-account

Một bước trưởng thành nữa của hạ tầng là tách mỗi môi trường vào một *tài khoản AWS riêng*. Terragrunt hỗ trợ chuyện này gần như miễn phí nhờ cơ chế *assume role*.

### Thiết lập AssumeRole

Mô hình điển hình gồm ba tài khoản AWS:

- Tài khoản gốc (*root account*) — không chứa resource nào.
- Tài khoản dev (`111111111111`).
- Tài khoản prod (`222222222222`).

Mỗi tài khoản con có sẵn một role tên `TerraformExecutionRole` tin tưởng (*trust*) tài khoản gốc. Config provider trong Terragrunt chỉ cần khai báo assume role tới đúng account ID của env:

```hcl
generate "provider" {
  path = "provider.tf"
  contents = <<EOF
provider "aws" {
  region = var.region

  assume_role {
    role_arn = "arn:aws:iam::$${var.aws_account_id}:role/TerraformExecutionRole"
  }
}
EOF
}
```

Giá trị `aws_account_id` lấy từ `account.hcl` của từng env, nên Terragrunt tự assume role vào đúng tài khoản đích.

### Lợi ích

Tách account không chỉ cho gọn — nó mang lại vài lợi ích an toàn rất đáng giá:

- **Cô lập bán kính ảnh hưởng** (*blast radius*): lỡ tay trên dev không thể chạm tới prod.
- **Tách quyền IAM**: muốn vào dev chỉ có thể qua assume role, không có đường tắt.
- **Theo dõi chi phí**: hoá đơn tách theo từng account.
- **Tuân thủ** (*compliance*): tài khoản prod có thể siết SCP chặt hơn hẳn.

### Dependency xuyên account

Đôi khi prod EKS lại cần VPC peering tới dev VPC. Khối `dependency` của Terragrunt vẫn làm việc xuyên account, miễn là state nằm trong một bucket chia sẻ được:

```hcl
dependency "dev_vpc" {
  config_path = "../../../dev/us-east-1/vpc"
  # Bucket state có thể khác — config gốc lo phần này
}
```

---

## 9️⃣ Hands-on: refactor repo 75 folder sang Terragrunt

Giờ ráp mọi mảnh ghép lại thành một việc thật: biến đống repo trùng lặp ở đầu bài thành một cấu trúc Terragrunt gọn gàng. Phần này đi từ ảnh "trước/sau", qua các bước migrate, rồi tới quy trình promote.

### Trước

Đây là điểm xuất phát quen thuộc — mỗi tổ hợp env-region-component là một bản copy của `main.tf`:

```text
infra/dev/us-east-1/vpc/main.tf        (200 dòng)
infra/dev/us-west-2/vpc/main.tf        (copy)
infra/dev/eu-west-1/vpc/main.tf        (copy)
infra/staging/us-east-1/vpc/main.tf    (copy)
infra/prod/us-east-1/vpc/main.tf       (copy)
...  (75 folder, ~15K dòng)
```

### Sau: cấu trúc Terragrunt

Sau khi refactor, code module gom về một chỗ, còn mỗi env-region chỉ còn vài dòng config:

```text
infrastructure/
├── terragrunt.hcl                       (50 dòng, config gốc)
├── modules/
│   └── vpc/main.tf                       (200 dòng, MỘT bản duy nhất)
└── live/
    ├── dev/
    │   ├── account.hcl                   (5 dòng)
    │   ├── us-east-1/
    │   │   ├── region.hcl                (4 dòng)
    │   │   └── vpc/terragrunt.hcl        (15 dòng)
    │   ├── us-west-2/
    │   │   ├── region.hcl
    │   │   └── vpc/terragrunt.hcl
    │   └── eu-west-1/...
    ├── staging/...
    └── prod/...
```

Con số nói lên tất cả: từ ~15K dòng rút còn 200 dòng module + khoảng 15 × 15 = 225 dòng config, tổng cộng tầm **400 dòng** — giảm khoảng **97%**. Quan trọng hơn cả con số: từ nay sửa CIDR chỉ còn đúng một chỗ.

### Quy trình migrate

Refactor không làm một phát mà đi từng bước, luôn giữ nguyên hiện trạng hạ tầng để không gây gián đoạn:

1. **Khảo sát hiện trạng**: liệt kê toàn bộ config Terraform đang có, tìm phần code chung.
2. **Tách module**: copy `dev/us-east-1/vpc/main.tf` sang `modules/vpc/main.tf`, tham số hoá bằng các `variable`.
3. **Dựng cấu trúc live**: tạo `live/dev/us-east-1/vpc/terragrunt.hcl` trỏ tới module + biến dev/us-east-1.
4. **Thử một env**: chạy `terragrunt plan`, kết quả phải là *no changes* (state không đổi) — đó là dấu hiệu refactor đúng.
5. **Di trú state nếu cần**: nếu đường dẫn state thay đổi, dùng `terragrunt state mv`.
6. **Lặp lại cho từng env**.
7. **Xoá các folder cũ**.

### Quy trình promote

Khi muốn nâng module lên version mới, nguyên tắc là luôn chạy dev trước, prod sau. Dev nâng module lên `v1.3.0`:

```bash
cd live/dev/us-east-1/vpc
# Sửa ref=v1.3.0 trong terragrunt.hcl
terragrunt plan
terragrunt apply
```

Nếu ổn, promote tiếp sang staging:

```bash
cd live/staging/us-east-1/vpc
# Sửa ref=v1.3.0
terragrunt plan
terragrunt apply
```

Cứ thế lặp lại cho các region và env còn lại. Khi cần xử lý hàng loạt trong một env, dùng `run-all`:

```bash
cd live/dev   # chỉ riêng dev
terragrunt run-all plan
```

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: lỡ tay `run-all destroy`

```bash
cd live/prod
terragrunt run-all destroy   # xoá SẠCH mọi resource của prod!
```

→ Cả cluster biến mất chỉ trong vài phút.

→ **Fix**:
- **Luôn yêu cầu xác nhận** — đừng để dính `--terragrunt-non-interactive` trên prod.
- **RBAC**: quyền `terraform destroy` chỉ cấp cho role cụ thể.
- **Backup state**: bật versioning cho S3 + DynamoDB.
- **Không `run-all` trên prod** — chỉ apply từng module một.

### ❌ Cạm bẫy: mock outputs lệch với thực tế

```hcl
mock_outputs = {
  vpc_id = "vpc-12345"
  subnet_ids = []                    # ← rỗng!
}
```

→ `terragrunt plan` chạy qua ngon lành, nhưng `apply` chết vì EKS cần ít nhất 2 subnet.

→ **Fix**: cho mock outputs sát thực tế (đúng kiểu, đủ phần tử). Thỉnh thoảng chạy apply thật để chắc mock không trôi xa hiện thực.

### ❌ Cạm bẫy: phụ thuộc vòng (circular dependency)

```text
A phụ thuộc B
B phụ thuộc C
C phụ thuộc A    ← vòng lặp!
```

→ `run-all apply` lặp vô hạn hoặc báo lỗi.

→ **Fix**: refactor để cắt vòng. Thường tách C thành C1 (không phụ thuộc A) + C2 (dùng A).

### ❌ Cạm bẫy: để `backend.tf` thủ công trong folder module

```text
modules/vpc/
├── main.tf
└── backend.tf      ← ĐỪNG! Terragrunt tự sinh file này
```

→ Xung đột với `generate "backend"` của Terragrunt.

→ **Fix**: folder module KHÔNG được có `backend.tf` hay `provider.tf`. Terragrunt sinh chúng riêng cho từng env.

### ❌ Cạm bẫy: hardcode account_id / giá trị env trong module

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"   # ← thứ đặc thù env phải là biến!
}
```

→ Module không còn dùng lại được cho env khác.

→ **Fix**: tham số hoá module: `variable "cidr_block" {}`.

### ❌ Cạm bẫy: đặt thời gian giữ lock quá lâu

```hcl
remote_state {
  config = {
    dynamodb_table = "tflocks"
    # Không có lock TTL!
  }
}
```

→ Một lần apply bị crash sẽ để lại lock vĩnh viễn, phải mở khoá tay.

→ **Fix**:
- Đặt timeout cho Terragrunt: `--terragrunt-fetch-dependency-output-from-state` với timeout ngắn hơn.
- Mở khoá tay: `terragrunt force-unlock <lock-id>`.
- Atlantis (xem bài kế) xử lý chuyện này tự động.

### ❌ Cạm bẫy: ghim module vào branch thay vì tag

```hcl
source = "git::...//vpc?ref=main"   # ← main luôn dịch chuyển!
```

→ Cùng một `terragrunt.hcl` nhưng apply ở hai thời điểm cho kết quả khác nhau. Mất khả năng tái lập (*reproducibility*).

→ **Fix**: luôn ghim vào **tag** hoặc **commit SHA**:

```hcl
source = "git::...//vpc?ref=v1.2.0"          # tag
source = "git::...//vpc?ref=abc123def4567890" # SHA
```

### ✅ Best practice: dùng `dependency` thay vì `data` source

```hcl
# ❌ Dùng data source để đọc state
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = { bucket = "...", key = "..." }
}

# ✅ Dùng dependency của Terragrunt
dependency "vpc" {
  config_path = "../vpc"
}
```

→ Khối `dependency` để Terragrunt tự lo thứ tự apply, và báo lỗi sạch hơn nếu VPC chưa được apply.

### ✅ Best practice: ghim version Terragrunt

```text
# .terragrunt-version
0.55.0
```

→ Các công cụ như `tgenv` (trình quản lý version Terragrunt) sẽ cài đúng phiên bản cho từng repo, giúp cả team đồng nhất.

### ✅ Best practice: pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.86.0
    hooks:
      - id: terragrunt_validate
      - id: terragrunt_fmt
      - id: terraform_tflint
      - id: terraform_tfsec
```

→ Tự format + validate + quét bảo mật trước mỗi lần commit.

---

## 🧠 Tự kiểm tra (Self-check)

Năm câu dưới chạm đúng những chỗ dễ nhầm nhất của Terragrunt. Bạn thử tự trả lời trước khi mở đáp án — đó là cách nhanh nhất để biết mình thật sự hiểu hay chỉ mới thấy quen.

**Q1.** Terragrunt và Terraform workspaces — chọn cái nào, khi nào?

<details>
<summary>💡 Đáp án</summary>

**Workspaces** (Terraform cơ bản):
- Cùng backend, mỗi workspace một state.
- Cùng thư mục, chuyển bằng `terraform workspace`.
- Biến qua file `<workspace>.tfvars`.
- Một config provider duy nhất.

**Hợp với**:
- Multi-env đơn giản (dev/staging/prod) trong cùng một tài khoản AWS.
- Cùng region (hoặc region để làm biến).
- Team nhỏ, dưới 5 module.

**Terragrunt**:
- Backend riêng cho từng env (cách ly state).
- Folder riêng cho từng env-region.
- Config account/region khác nhau.
- Quản lý dependency giữa các module.

**Hợp với**:
- Multi-account (mỗi env một tài khoản AWS riêng).
- Multi-region với config khác nhau.
- Trên 10 module có phụ thuộc lẫn nhau.
- Versioning module khác nhau giữa các env (dev v1.3, prod v1.0).

**Cách quyết**:
- **1 account, 1 region, dưới 5 module**: dùng workspaces.
- **Multi-account HOẶC multi-region HOẶC trên 10 module**: dùng Terragrunt.

Lưu ý lai: Terraform Cloud workspaces (khác hẳn `terraform workspace`) có một số tính năng giẫm lên Terragrunt.

Việc chuyển từ workspaces sang Terragrunt khá thẳng băng: copy state + refactor lại cấu trúc thư mục.
</details>

**Q2.** Vì sao nên sinh `backend.tf` thay vì đặt nó trong module?

<details>
<summary>💡 Đáp án</summary>

**Không Terragrunt** (backend nằm trong module):
```text
modules/vpc/
├── main.tf
└── backend.tf      # bucket = "...", key = "vpc/terraform.tfstate"
```

→ Cùng một backend cho MỌI env! Tất cả env dùng chung state — xung đột và cực kỳ nguy hiểm.

**Thử tham số hoá backend?** Không được — backend của Terraform không dùng được biến:

```hcl
# KHÔNG CHẠY
backend "s3" {
  bucket = "${var.env}-tfstate"   # LỖI
}
```

→ Config backend không cho dùng biến (con gà–quả trứng: cần backend trước khi init, mà biến lại có sau).

**Lách bằng** partial config + cờ `-backend-config`:
```bash
terraform init -backend-config="bucket=acme-dev-tfstate"
```

→ Chạy được nhưng thủ công và dài dòng.

**Cách của Terragrunt**:
- `generate "backend"` ghi `backend.tf` ngay tại **folder con hiện tại** trước khi `terraform init`.
- Nội dung lấy từ `terragrunt.hcl` gốc với các giá trị nội suy (path, env).
- Mỗi env một state riêng, hoàn toàn tự động.

```hcl
remote_state {
  backend = "s3"
  generate = {
    path = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = "acme-tfstate-${get_aws_account_id()}"
    key = "${path_relative_to_include()}/terraform.tfstate"
    # ...
  }
}
```

→ Mỗi folder con được đúng backend của nó, không phải config tay.

**Ý chốt**: Terragrunt đứng NGOÀI Terraform, sinh ra các file mà Terraform sẽ đọc — nhờ vậy né được giới hạn "backend không dùng biến" của Terraform.
</details>

**Q3.** `mock_outputs` trong `dependency` — vì sao cần?

<details>
<summary>💡 Đáp án</summary>

**Bối cảnh**: một env hoàn toàn mới (dev), chưa có resource nào. Bạn muốn plan EKS.

EKS Terragrunt có `dependency "vpc"`. VPC chưa apply → state rỗng → `dependency.vpc.outputs.vpc_id` không xác định → plan chết.

**Mock outputs** giải bài này:
```hcl
dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id = "vpc-mock"
    private_subnet_ids = ["subnet-mock-1", "subnet-mock-2"]
  }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}
```

→ Plan render được template với giá trị mock. Apply thì cần giá trị thật (mock không dùng cho apply).

**Quy trình**:
1. `terragrunt plan` EKS → dùng mock_outputs → cho thấy EKS SẼ tạo gì.
2. Nhận ra cần VPC trước.
3. `terragrunt apply` VPC → có output thật.
4. `terragrunt apply` EKS → dùng output VPC thật.

**`mock_outputs_allowed_terraform_commands`** giới hạn mock chỉ cho các lệnh an toàn (plan, validate). Apply/destroy buộc phải dùng output thật.

**Best practice**:
- Mock outputs **sát thực tế** (ID trông thật, CIDR hợp lệ...).
- Mock outputs đúng kiểu (list vs scalar).
- Định kỳ chạy apply đầy đủ để mock không trôi xa thực tế.

→ Mock outputs = tiện ích để lập trình viên plan được qua các module chưa apply.
</details>

**Q4.** Giới hạn chạy song song của `run-all` — cần biết gì?

<details>
<summary>💡 Đáp án</summary>

**Hành vi của `terragrunt run-all apply`**:
- Quét đệ quy mọi `terragrunt.hcl`.
- Dựng đồ thị phụ thuộc.
- Apply theo **thứ tự topo** (dependency trước).
- **Chạy song song** các module độc lập ở cùng một tầng.

**Mặc định**: mọi module độc lập chạy cùng lúc.

**Các vấn đề**:

1. **Rate limit của AWS API**: 100+ module apply song song → bị throttle.

```bash
# Giới hạn song song
terragrunt run-all apply --terragrunt-parallelism 5
```

2. **Đụng lock**: 2 module cùng một lock DynamoDB → phải chờ.

3. **Giới hạn tài nguyên**: mỗi process Terraform ngốn ~100MB RAM. 50 module = 5GB → CI runner OOM.

4. **Mạng**: 50 lệnh `terraform init` song song tải provider cùng lúc.

**Giải pháp**:
- `--terragrunt-parallelism N` — chặn mức song song.
- Gom apply theo từng giai đoạn (prod-vpc → cả cụm → prod-eks → cả cụm → prod-apps).
- Atlantis (bài kế) xếp hàng apply một cách thông minh.

**Pattern cho production**: Atlantis chạy `terragrunt plan/apply` cho từng module, không dùng `run-all`, để tránh rủi ro đổ dây chuyền.

**`run-all` hợp cho**:
- Phát triển cục bộ (apply nhanh cả env dev).
- Khôi phục thảm hoạ (dựng lại từ đầu ở region DR).
- Bootstrap env mới.

**`run-all` không hợp cho**:
- Apply production (dùng Atlantis với PR tường minh).
- Thao tác destroy (làm từng module một).

→ `run-all` là công cụ mạnh. Dùng có chủ đích.
</details>

**Q5.** Versioning module bằng git tag — rollback ra sao?

<details>
<summary>💡 Đáp án</summary>

**Bối cảnh**: dev đã apply module v1.3.0, vỡ một thứ gì đó. Cần rollback về v1.2.0.

**Bước 1**: sửa terragrunt.hcl:
```hcl
source = "git::...//vpc?ref=v1.2.0"
```

**Bước 2**:
```bash
cd live/dev/us-east-1/vpc
terragrunt plan
```

Terragrunt sẽ:
- Tải v1.2.0 của module.
- Đọc state hiện tại (đang ở v1.3.0).
- Diff: cho thấy các thay đổi để revert từ v1.3.0 → v1.2.0.

**Bước 3**:
```bash
terragrunt apply
```

Áp dụng các thay đổi ngược lại.

**Lưu ý**:

1. **Có thể dính thao tác phá huỷ**: v1.3.0 thêm cột vào RDS, v1.2.0 không có → `terraform plan` báo drop cột. **Mất dữ liệu**.

   Cách phòng: thêm `lifecycle { prevent_destroy = true }` cho resource trọng yếu.

2. **Tái tạo resource**: vài thay đổi (ví dụ đổi CIDR subnet) buộc phải destroy + recreate → gián đoạn.

   Cách phòng: dùng `lifecycle { create_before_destroy = true }` ở nơi có thể.

3. **Di trú state**: v1.3.0 thêm output mới, v1.2.0 không có. `terragrunt apply` xoá output đó → các module phụ thuộc vỡ theo.

   Cách phòng: rollback theo từng giai đoạn. Cập nhật các module phụ thuộc trước.

**Best practice**:
- **Thử ở dev trước** khi promote tag lên prod.
- **Tag mọi release** để rollback dễ.
- **Ghi breaking change** vào CHANGELOG của module.
- **Bump major version** cho breaking change (theo SemVer).

**Khôi phục thảm hoạ**:
- Versioning S3 trên bucket state = khôi phục lại state file cũ khi cần.
- Kết hợp với git revert của terragrunt.hcl = đường rollback đầy đủ.

→ Versioning module + versioning state = lưới an toàn cho mọi thay đổi IaC trên prod.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

Phần tra nhanh cho lúc làm việc thật — gom theo nhóm: lệnh Terragrunt cơ bản, `run-all`, thao tác state, mẫu `terragrunt.hcl`, và các hàm dựng sẵn hay dùng.

```bash
# === Terragrunt cơ bản ===
terragrunt --version
terragrunt init
terragrunt plan
terragrunt apply
terragrunt destroy
terragrunt show
terragrunt output

# === Run-all ===
terragrunt run-all plan
terragrunt run-all apply
terragrunt run-all apply --terragrunt-parallelism 5
terragrunt run-all apply --terragrunt-include-dir live/dev
terragrunt run-all apply --terragrunt-exclude-dir live/prod

# === Lệnh state ===
terragrunt state list
terragrunt state show <resource>
terragrunt state mv <source> <dest>
terragrunt state rm <resource>
terragrunt force-unlock <lock-id>

# === Xem đồ thị phụ thuộc ===
terragrunt graph-dependencies
# Output: DAG của mọi module
```

```hcl
# === Mẫu terragrunt.hcl ===
include "root" {
  path = find_in_parent_folders()
}

locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
}

dependency "vpc" {
  config_path = "../vpc"
  mock_outputs = { vpc_id = "vpc-mock" }
  mock_outputs_allowed_terraform_commands = ["plan", "validate"]
}

terraform {
  source = "git::git@github.com:acme/infra-modules.git//eks?ref=v1.3.0"
}

inputs = {
  cluster_name = "${local.account_vars.locals.env}-eks"
  vpc_id       = dependency.vpc.outputs.vpc_id
  subnet_ids   = dependency.vpc.outputs.private_subnet_ids
}
```

```bash
# === Hàm dựng sẵn ===
get_aws_account_id()
get_terraform_command()
get_terraform_commands_that_need_locking()
get_env("ENV_VAR", "default")
path_relative_to_include()
path_relative_from_include()
find_in_parent_folders("filename.hcl")
read_terragrunt_config("file.hcl")
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **Terragrunt** | Lớp bọc Terraform | Wrapper quanh Terraform để giữ config DRY |
| **Terraform module** | Module Terraform | Code Terraform tái sử dụng (variables + resources + outputs) |
| **`live/` folder** | Thư mục `live/` | Config Terragrunt theo từng env |
| **`modules/` folder** | Thư mục `modules/` | Code module Terraform tái sử dụng |
| **`terragrunt.hcl`** | File config Terragrunt | File config Terragrunt cho từng folder |
| **`include` block** | Khối `include` | Kế thừa config từ `terragrunt.hcl` cha |
| **`generate` block** | Khối `generate` | Tự sinh file (backend.tf/provider.tf) trước khi chạy Terraform |
| **`dependency` block** | Khối `dependency` | Tham chiếu output của module khác |
| **`mock_outputs`** | Giá trị giả | Giá trị giả cho `plan` khi dependency chưa apply |
| **`run-all`** | Chạy toàn cụm | Apply nhiều module theo thứ tự phụ thuộc |
| **Topological order** | Thứ tự topo | Thứ tự tôn trọng dependency (theo DAG) |
| **`source`** | Nguồn module | Vị trí module Terraform (local/git/registry) |
| **Module versioning** | Đánh version module | Ghim module vào tag/SHA cụ thể |
| **Cross-account** | Xuyên tài khoản | Thiết lập nhiều tài khoản AWS với assume role |
| **DRY** | Đừng lặp lại | Don't Repeat Yourself — nguyên tắc tránh trùng lặp |
| **`find_in_parent_folders()`** | Hàm tìm file cha | Built-in: đi ngược lên cây thư mục tìm file |
| **`path_relative_to_include()`** | Đường dẫn tương đối | Path từ config gốc tới folder hiện tại |
| **driftctl** | Công cụ dò drift | Công cụ OSS phát hiện drift (xem bài kế) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [IaC Intermediate — Từ "terraform apply local" đến "GitOps infra"](00_intermediate-overview.md)
- ➡️ **Bài tiếp theo:** [Atlantis — GitOps cho Terraform/Terragrunt](02_atlantis-gitops-for-iac.md)
- ↑ **Về cụm:** [IaC — Infrastructure as Code](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ⬅️ **Bài trước:** [Modules & Multi-env — DRY + Reusability](../01_basic/03_modules-and-workspaces.md) — nền tảng module trước khi lên Terragrunt
- ☸️ [Helm — Package manager cho K8s](../../../kubernetes/lessons/02_intermediate/01_helm-package-manager.md) — cùng tư tưởng DRY cho hạ tầng

### 🌐 Tài nguyên tham khảo khác

- 📖 [Terragrunt docs](https://terragrunt.gruntwork.io/)
- 📖 [Gruntwork Terragrunt Examples](https://github.com/gruntwork-io/terragrunt-infrastructure-live-example)
- 📖 [Terragrunt Best Practices](https://terragrunt.gruntwork.io/docs/getting-started/best-practices/)
- 📖 [terragrunt-atlantis-config](https://github.com/transcend-io/terragrunt-atlantis-config) — công cụ cầu nối
- 📖 [pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 01 intermediate. Terragrunt vs workspaces + cấu trúc `live/` + `modules/` + root + account + region + child terragrunt.hcl + generate backend/provider + dependency block + run-all + module versioning + multi-account assume role + migration workflow. 7 pitfall + 3 best practice + 5 self-check + cheatsheet.
- **v1.1.0 (25/05/2026)** — Thêm lead-in trước Install + Standard layout + Workflow + Key features.
- **v2.0.0 (07/06/2026)** — Viết lại toàn bộ prose sang tiếng Việt narrative theo gold-standard: thay các đoạn "điện tín" tiếng Anh (concept, vs workspaces, key features, result, benefits, toàn bộ 5 self-check) bằng câu văn mạch WHY→WHAT→HOW có lời dẫn trước và phân tích sau mỗi code/bảng; Việt hoá metadata "Yêu cầu trước" và mục tiêu; chuyển khối So-sánh workspaces từ bullet sang bảng; Việt hoá heading nav (⬅️/➡️/↑ + link-text = tiêu đề H1 thực) và 3 sub-heading chuẩn; xoá nhãn "(sắp viết)" cho bài Atlantis đã tồn tại; Glossary chuyển sang 3 cột (Thuật ngữ | Tiếng Việt | Giải thích); Việt hoá comment trong code/output. Giữ nguyên 100% code/lệnh/config/số liệu/flag và cấu trúc 8 phần.
