# Terraform Advanced

> **Tags:** `terraform` `iac` `modules` `workspaces` `state` `remote-backend` `providers`
> **Level:** Intermediate | **Prerequisite:** `iac/01-terraform.md`

---

## 1. Modules — Reusable Infrastructure

```hcl
# modules/rds/main.tf
variable "identifier" {
  description = "DB instance identifier"
  type        = string
}

variable "instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "database_name"     { type = string }
variable "username"          { type = string }
variable "password"          { 
  type      = string 
  sensitive = true
}

variable "subnet_ids"  { type = list(string) }
variable "vpc_id"      { type = string }
variable "allowed_cidr_blocks" {
  type    = list(string)
  default = []
}

resource "aws_db_subnet_group" "this" {
  name       = "${var.identifier}-subnet-group"
  subnet_ids = var.subnet_ids
  tags       = local.common_tags
}

resource "aws_security_group" "rds" {
  name   = "${var.identifier}-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }
}

resource "aws_db_instance" "this" {
  identifier             = var.identifier
  engine                 = "postgres"
  engine_version         = "16.1"
  instance_class         = var.instance_class
  db_name                = var.database_name
  username               = var.username
  password               = var.password
  
  db_subnet_group_name   = aws_db_subnet_group.this.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  backup_retention_period  = 7
  delete_automated_backups = false
  skip_final_snapshot      = false
  final_snapshot_identifier = "${var.identifier}-final"
  
  storage_encrypted       = true
  performance_insights_enabled = true
  
  tags = local.common_tags
}

# modules/rds/outputs.tf
output "endpoint"           { value = aws_db_instance.this.endpoint }
output "port"               { value = aws_db_instance.this.port }
output "security_group_id"  { value = aws_security_group.rds.id }
output "db_name"            { value = aws_db_instance.this.db_name }

# modules/rds/locals.tf  
locals {
  common_tags = {
    Module = "rds"
    Name   = var.identifier
  }
}
```

### Using Modules
```hcl
# environments/prod/main.tf
module "production_db" {
  source = "../../modules/rds"   # Local module
  # Or: source = "git::https://github.com/org/terraform-modules.git//rds?ref=v2.1.0"
  # Or: source = "registry.terraform.io/hashicorp/consul/aws"  # Terraform Registry

  identifier    = "prod-postgres"
  instance_class = "db.r6g.large"
  database_name = "myapp"
  username      = "dbadmin"
  password      = var.db_password   # Passed from tfvars/env
  
  subnet_ids   = module.vpc.private_subnet_ids
  vpc_id       = module.vpc.vpc_id
  allowed_cidr_blocks = module.vpc.private_subnet_cidr_blocks
}

output "db_endpoint" {
  value     = module.production_db.endpoint
  sensitive = true
}
```

---

## 2. Remote State & State Locking

```hcl
# backend.tf — Store state in S3 with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/us-east-1/app/terraform.tfstate"
    region         = "us-east-1"
    
    # State locking (prevents concurrent writes)
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
    
    # Optional: workspace-based paths
    # key = "prod/{workspace}/terraform.tfstate"
  }
}

# Terragrunt (DRY remote backend configuration)
# terragrunt.hcl
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite"
  }
  config = {
    bucket         = "my-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

### Cross-stack References (data source for remote state)
```hcl
# Read outputs from another Terraform state
data "terraform_remote_state" "networking" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "prod/networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use outputs from networking stack
resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.networking.outputs.private_subnet_id
  vpc_security_group_ids = [data.terraform_remote_state.networking.outputs.app_sg_id]
}
```

---

## 3. Workspaces — Multiple Environments

```bash
# Workspace commands
terraform workspace new staging
terraform workspace new production
terraform workspace list         # * marks current
terraform workspace select staging
terraform workspace show         # Current workspace name

# Use workspace name in configuration
```

```hcl
# Use workspace to drive configuration
locals {
  workspace = terraform.workspace
  
  instance_types = {
    default    = "t3.micro"
    staging    = "t3.small"
    production = "c5.xlarge"
  }
  
  replica_counts = {
    default    = 1
    staging    = 1
    production = 3
  }
}

resource "aws_instance" "app" {
  count         = local.replica_counts[local.workspace]
  instance_type = local.instance_types[local.workspace]
  
  tags = {
    Environment = terraform.workspace
  }
}
```

> **Note**: For complex multi-env, Terragrunt or separate state per env is better than workspaces.

---

## 4. Data Sources

```hcl
# data sources = read existing resources (not managed by this Terraform)

# Existing VPC
data "aws_vpc" "existing" {
  tags = {
    Name = "production-vpc"
  }
}

# Latest AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Current AWS account ID and region
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
}

# Route53 zone
data "aws_route53_zone" "main" {
  name = "example.com"
}

# SSM Parameter (secrets)
data "aws_ssm_parameter" "db_password" {
  name            = "/app/prod/db_password"
  with_decryption = true
}

# Usage
resource "aws_db_instance" "this" {
  password = data.aws_ssm_parameter.db_password.value
}
```

---

## 5. Lifecycle Rules

```hcl
resource "aws_s3_bucket" "uploads" {
  bucket = "my-app-uploads"

  lifecycle {
    # Prevent accidental deletion
    prevent_destroy = true
    
    # Create new resource BEFORE destroying old one (no downtime)
    create_before_destroy = true
    
    # Ignore these attributes (e.g., set by external process)
    ignore_changes = [
      tags["LastModifiedBy"],
      tags["ManagedBy"],
    ]
    
    # Replace only when condition is true (Terraform 1.2+)
    replace_triggered_by = [
      aws_security_group.app.id
    ]
  }
}

# Prevent destroy with condition
resource "aws_instance" "critical" {
  lifecycle {
    prevent_destroy = true   # terraform destroy will fail!
  }
}
```

---

## 6. Dynamic Blocks

```hcl
variable "ingress_rules" {
  description = "List of ingress rules"
  type = list(object({
    port        = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    { port = 80,   protocol = "tcp", cidr_blocks = ["0.0.0.0/0"], description = "HTTP" },
    { port = 443,  protocol = "tcp", cidr_blocks = ["0.0.0.0/0"], description = "HTTPS" },
    { port = 22,   protocol = "tcp", cidr_blocks = ["10.0.0.0/8"], description = "SSH internal" },
  ]
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = var.vpc_id

  # Generate multiple blocks dynamically
  dynamic "ingress" {
    for_each = var.ingress_rules
    iterator = rule   # Optional: rename the iterator (default: ingress)
    content {
      from_port   = rule.value.port
      to_port     = rule.value.port
      protocol    = rule.value.protocol
      cidr_blocks = rule.value.cidr_blocks
      description = rule.value.description
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## 7. For Expressions & Complex Types

```hcl
# locals.tf — complex transformations
locals {
  # List of strings to set
  azs = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  # for expression: list transformation
  az_suffixes = [for az in local.azs : substr(az, -1, 1)]  # ["a", "b", "c"]
  
  # for expression: map transformation
  subnet_map = {
    for i, az in local.azs :
    az => "10.0.${i}.0/24"
  }
  # { "us-east-1a" = "10.0.0.0/24", "us-east-1b" = "10.0.1.0/24", ... }
  
  # Conditional in for expression  
  public_subnets = [
    for subnet in aws_subnet.all : subnet.id
    if subnet.map_public_ip_on_launch
  ]
  
  # Flatten nested lists
  all_tags = flatten([
    for env, tags in var.environment_tags : [
      for key, value in tags : {
        environment = env
        key         = key
        value       = value
      }
    ]
  ])
}

# Merge maps
locals {
  common_tags = {
    Project     = "myapp"
    Terraform   = "true"
    Region      = var.region
  }
  
  resource_tags = merge(local.common_tags, {
    Environment = var.environment
    Owner       = var.team
  })
}
```

---

## 8. Provisioners (Use Sparingly!)

```hcl
# Provisioners are a last resort — prefer cloud-init, Ansible, Packer
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deploy.key_name

  # Run script on first boot
  user_data = templatefile("user_data.sh.tpl", {
    db_host = module.database.endpoint
    app_env = var.environment
  })
  
  # Local exec: run command on YOUR machine
  provisioner "local-exec" {
    command = "echo 'Instance ID: ${self.id}' > instance_id.txt"
  }
  
  # Remote exec: run command inside instance (requires SSH)
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx",
    ]
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
  
  # Run on destroy
  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Destroying ${self.id}'"
  }
}
```

---

## 9. Testing Terraform

```bash
# terraform validate — syntax and provider schema validation
terraform validate

# terraform fmt — format code
terraform fmt -recursive -diff -check   # -check: exit 1 if not formatted

# tflint — additional linting rules (AWS-specific, etc.)
tflint --format=compact

# checkov — security scanning
checkov -d . --framework terraform

# Terratest (Go) — integration testing
# terratest/main_test.go
func TestRDSModule(t *testing.T) {
    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../modules/rds",
        Vars: map[string]interface{}{
            "identifier":     "test-db",
            "database_name":  "testdb",
            "username":       "testuser",
            "password":       "testpassword",
            // ...
        },
    })
    
    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)
    
    endpoint := terraform.Output(t, terraformOptions, "endpoint")
    assert.NotEmpty(t, endpoint)
    
    // Test actual connectivity
    host, port, _ := net.SplitHostPort(endpoint)
    db, err := sql.Open("postgres", fmt.Sprintf("host=%s port=%s user=testuser password=testpassword dbname=testdb", host, port))
    assert.NoError(t, err)
    assert.NoError(t, db.Ping())
}
```

---

## 10. Terraform Workflow Commands

```bash
# Initialize (download providers, init backend)
terraform init
terraform init -upgrade    # Upgrade providers to latest
terraform init -backend-config=backend.conf   # External backend config

# Plan & Apply
terraform plan -var-file=prod.tfvars -out=tfplan
terraform apply tfplan    # Apply pre-generated plan (recommended for CI/CD)
terraform apply -auto-approve   # Skip confirmation (CI/CD only)

# Target specific resources
terraform plan -target=module.database
terraform apply -target=aws_instance.web

# Destroy
terraform destroy -target=module.staging
terraform plan -destroy   # Preview destroy

# State management
terraform state list
terraform state show aws_instance.web
terraform state rm aws_instance.web   # Remove from state (doesn't destroy resource)
terraform import aws_instance.web i-1234567890    # Import existing resource

# Force unlock state (if lock is stuck)
terraform force-unlock LOCK_ID

# Graph
terraform graph | dot -Tsvg > graph.svg
```

---

*Tài liệu liên quan: `iac/01-terraform.md` | `iac/03-pulumi.md` | `cloud/01-aws-core.md`*
