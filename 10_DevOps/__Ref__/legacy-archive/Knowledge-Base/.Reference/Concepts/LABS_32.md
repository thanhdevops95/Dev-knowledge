# 🧪 MODULE 05: LABS - Terraform & Ansible

## LAB 1: Thiết lập Công cụ

```bash
# Install Terraform
brew install terraform  # macOS
# Windows: choco install terraform

# Verify
terraform version

# Install Ansible
pip install ansible

# Verify
ansible --version
```

---

## LAB 2: Provision EC2 với Terraform

### main.tf

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "counter" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "Counter-App"
  }
}

output "instance_ip" {
  value = aws_instance.counter.public_ip
}
```

### Run

```bash
terraform init
terraform plan
terraform apply -auto-approve

# Get IP
terraform output instance_ip
```

---

## LAB 3: Ansible Playbook

### inventory.ini

```ini
[webservers]
<instance_ip> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/aws-key.pem
```

### playbook.yml

```yaml
---
- hosts: webservers
  become: yes
  tasks:
    - name: Update apt
      apt: update_cache=yes
    
    - name: Install Docker
      apt: name=docker.io state=present
```

### Run

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## LAB 4: Tự động Mở rộng

### autoscaling.tf

```hcl
resource "aws_autoscaling_group" "counter" {
  min_size         = 1
  max_size         = 5
  desired_capacity = 2
  
  launch_template {
    id      = aws_launch_template.counter.id
    version = "$Latest"
  }
}
```

✅ **Checklist**

- [ ] Terraform installed
- [ ] EC2 provisioned
- [ ] Ansible playbook working
- [ ] Auto-scaling configured
