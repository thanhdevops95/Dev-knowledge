# 📘 MODULE 05: OPERATE - Infrastructure as Code

## 🤔 Tại sao cần IaC?

### Ẩn dụ: Robot xây dựng tự động

**Cách cũ (Manual):**

- Vào AWS Console, click click chuột
- Tạo server: chọn size, region, security group...
- Mất 30 phút, dễ sai sót
- Muốn tạo 10 servers giống nhau → Copy 10 lần

**IaC (Automated):**

- Viết code mô tả infrastructure
- Chạy `terraform apply` → Tạo 100 servers trong 5 phút
- Giống nhau 100%, không sai sót
- Version control bằng Git

---

## 🏗️ Terraform Basics

### Example: main.tf

```hcl
# Provider
provider "aws" {
  region = "us-east-1"
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "Counter-App-Server"
  }
}

# Security Group
resource "aws_security_group" "web_sg" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Workflow

```bash
terraform init      # Download providers
terraform plan      # Preview changes
terraform apply     # Create resources
terraform destroy   # Delete resources
```

---

## 🤖 Ansible Configuration Management

### Example: playbook.yml

```yaml
---
- name: Setup Counter App Server
  hosts: webservers
  become: yes
  tasks:
    - name: Install Docker
      apt:
        name: docker.io
        state: present
    
    - name: Start Docker service
      service:
        name: docker
        state: started
    
    - name: Run Counter App container
      docker_container:
        name: counter-app
        image: counter-app:v1.0
        ports:
          - "80:5000"
```

### Run

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## 💡 Key Takeaways

1. **IaC = Infrastructure عن Code** - Version control cho infrastructure
2. **Terraform = Provisioning** - Tạo/xóa resources
3. **Ansible = Configuration** - Cài đặt software, config
4. **Idempotent** - Chạy 10 lần = chạy 1 lần

⏭️ Next: **LABS.md**
