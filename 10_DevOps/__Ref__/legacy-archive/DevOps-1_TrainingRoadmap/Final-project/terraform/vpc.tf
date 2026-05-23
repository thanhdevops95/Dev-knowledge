# terraform/vpc.tf

# Sử dụng module có sẵn của cộng đồng để tạo VPC.
# Đây là best practice để tạo ra một VPC đầy đủ và đúng chuẩn một cách nhanh chóng.
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.2"

  name = "final-project-vpc"
  cidr = "10.0.0.0/16" # Dải IP cho toàn bộ VPC

  azs             = ["us-east-1a", "us-east-1b"] # Triển khai trên 2 Availability Zones
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"] # Dải IP cho các private subnets
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"] # Dải IP cho các public subnets

  enable_nat_gateway = true # Cần thiết để các tài nguyên trong private subnet có thể đi ra internet
  enable_dns_hostnames = true

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "final-project"
  }
}
