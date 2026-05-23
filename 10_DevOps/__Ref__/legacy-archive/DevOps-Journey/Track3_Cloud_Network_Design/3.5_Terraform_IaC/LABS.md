# 🔬 Labs: Terraform

---

## 🔬 Lab 1: Terraform Setup

```bash
# Install Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify
terraform version

# Configure AWS credentials
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
```

---

## 🔬 Lab 2: First Configuration

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "HelloWorld"
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

## 🔬 Lab 3: Variables & Outputs

```hcl
# variables.tf
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

# main.tf
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Environment = var.environment
  }
}

# outputs.tf
output "instance_ip" {
  value = aws_instance.web.public_ip
}

# terraform.tfvars
environment = "production"
instance_type = "t3.micro"
```

---

## 🔬 Lab 4: State Management

```hcl
# backend.tf - Remote state
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

```bash
# State commands
terraform state list
terraform state show aws_instance.web
terraform state mv aws_instance.web aws_instance.app
terraform state rm aws_instance.web
```

---

## 🔬 Lab 5: Modules

```hcl
# modules/vpc/main.tf
variable "cidr_block" {}
variable "name" {}

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  
  tags = {
    Name = var.name
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
}

# main.tf - Using module
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  name       = "production-vpc"
}

# Using registry module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

---

## ✅ Checklist

- [ ] Lab 1: Setup
- [ ] Lab 2: First Config
- [ ] Lab 3: Variables
- [ ] Lab 4: State
- [ ] Lab 5: Modules

---

**[← Back to README](./README.md)**
