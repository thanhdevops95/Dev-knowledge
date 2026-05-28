# terraform/eks.tf

# Sử dụng module EKS của cộng đồng để đơn giản hóa việc tạo cụm
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "18.26.6"

  cluster_name    = "final-project-cluster"
  cluster_version = "1.23"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.public_subnets # Đặt các worker node vào public subnet cho đơn giản

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
  }

  eks_managed_node_groups = {
    one = {
      name           = "general-workers"
      instance_types = ["t3.small"]
      min_size     = 1
      max_size     = 3
      desired_size = 2
    }
  }

  tags = {
    Terraform   = "true"
    Environment = "dev"
    Project     = "final-project"
  }
}

# Output ra các thông tin cần thiết để kubectl có thể kết nối
output "cluster_endpoint" {
  description = "Endpoint for EKS cluster."
  value       = module.eks.cluster_endpoint
}

output "cluster_ca_certificate" {
  description = "CA certificate for EKS cluster."
  value       = module.eks.cluster_certificate_authority_data
}
