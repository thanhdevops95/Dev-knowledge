# Module 12: IaC Labs

---

## 🔧 Lab 1: First Terraform Config

```bash
mkdir terraform-lab && cd terraform-lab
```

```hcl
# main.tf
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
    }
  }
}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello from Terraform!"
}
```

```bash
terraform init
terraform plan
terraform apply
cat hello.txt
```

---

## 🔧 Lab 2: AWS Resources

```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = "my-terraform-test-bucket-unique-12345"
  
  tags = {
    Environment = "Dev"
    ManagedBy   = "Terraform"
  }
}
```

```bash
terraform init
terraform plan
terraform apply
terraform destroy
```

---

## 🔧 Lab 3: Variables

```hcl
# variables.tf
variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
}

variable "environment" {
  default = "dev"
}

# main.tf
resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  tags = {
    Environment = var.environment
  }
}

# terraform.tfvars
bucket_name = "my-cool-bucket"
environment = "staging"
```

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Basic Terraform |
| 2 | AWS resources |
| 3 | Variables |

👉 **[SCENARIOS.md](SCENARIOS.md)**
