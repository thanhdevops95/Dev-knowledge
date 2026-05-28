# Module: Ansible - Configuration Management

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Ansible** | /ˈænsɪbəl/ | Tool Configuration Management, agentless |
| **Playbook** | - | File YAML định nghĩa automation tasks |
| **Inventory** | - | Danh sách servers được quản lý |
| **Task** | - | Một action đơn lẻ trong playbook |
| **Module** | - | Unit code thực thi task (apt, copy, service) |
| **Role** | - | Tập hợp tasks, files, templates có thể reuse |
| **Handler** | - | Task chạy khi được notify (restart service) |
| **Facts** | - | Thông tin về target host (OS, IP, memory) |
| **Idempotent** | /aɪˈdɛmpətənt/ | Chạy nhiều lần, kết quả như nhau |
| **Jinja2** | - | Template engine cho biến và logic |
| **Vault** | - | Encrypt secrets trong Ansible |
| **Galaxy** | - | Repository chia sẻ Ansible roles |

---

## 📖 Ansible là gì? (Định nghĩa từ gốc)

### Trước hết: Configuration Management là gì?

**Vấn đề thực tế:**

Bạn có 100 servers cần:

- Cài đặt cùng packages
- Cấu hình cùng users
- Deploy cùng ứng dụng

**Cách làm thủ công:**

```bash
# SSH vào từng server
ssh server1 "apt install nginx && systemctl start nginx"
ssh server2 "apt install nginx && systemctl start nginx"
... # 98 servers còn lại
# Mất 2 ngày + bug do typo
```

**Configuration Management giải quyết:**

> **Configuration Management = Định nghĩa trạng thái mong muốn của servers bằng code, tool tự động đạt trạng thái đó**

### Ansible cụ thể

> **Ansible = Tool CM agentless, dùng SSH, viết bằng YAML**

**Đặc điểm:**

| Đặc điểm | Giải thích |
|----------|------------|
| **Agentless** | Không cần cài agent trên servers |
| **SSH-based** | Dùng SSH để connect |
| **YAML syntax** | Dễ đọc, dễ viết |
| **Idempotent** | Chạy nhiều lần, an toàn |
| **Declarative** | Mô tả trạng thái muốn đạt |

### Ansible vs Terraform

| | Ansible | Terraform |
|-|---------|-----------|
| **Focus** | Configuration Management | Infrastructure Provisioning |
| **Target** | Servers đã có | Tạo infrastructure mới |
| **Use case** | Install packages, configure | Create VMs, networks, DBs |
| **State** | Không lưu state | State file |

**Thường dùng cùng nhau:**

```
Terraform tạo VMs → Ansible configure VMs
```

---

## 🎬 Câu chuyện thực tế

**Trước Ansible:**

```
1. Deploy lên 50 servers
2. SSH vào từng server
3. Chạy commands
4. Server 37 fail vì typo
5. Mất 3 tiếng fix
6. Không ai dám làm lại
```

**Sau Ansible:**

```
1. Viết playbook một lần
2. ansible-playbook deploy.yml
3. 50 servers configured trong 5 phút
4. Lỗi? Fix playbook, chạy lại
5. Ai cũng có thể run
```

---

## 🏗️ Kiến trúc Ansible

```
┌─────────────────────────────────────────────────────────────┐
│                     CONTROL NODE                             │
│                   (Your laptop/CI server)                    │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Playbook   │    │  Inventory   │    │    Roles     │  │
│   │   (YAML)     │    │  (hosts)     │    │  (reusable)  │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│           │                   │                   │          │
│           └───────────────────┼───────────────────┘          │
│                               │                              │
│                        ┌──────▼──────┐                       │
│                        │   Ansible   │                       │
│                        │   Engine    │                       │
│                        └──────┬──────┘                       │
└────────────────────────────────│─────────────────────────────┘
                                 │ SSH
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    ┌────▼────┐            ┌────▼────┐            ┌────▼────┐
    │ Server1 │            │ Server2 │            │ Server3 │
    │  (web)  │            │  (web)  │            │  (db)   │
    └─────────┘            └─────────┘            └─────────┘
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                           MANAGED NODES
                      (No agent required!)
```

**Không cần cài gì trên Managed Nodes** - chỉ cần SSH access và Python.

---

## 📝 Inventory - Danh sách Servers

### Format cơ bản

```ini
# inventory.ini

# Ungrouped hosts
server1.example.com

# Grouped hosts
[webservers]
web1.example.com
web2.example.com
10.0.0.51

[dbservers]
db1.example.com
db2.example.com

# Nested groups
[production:children]
webservers
dbservers

# Variables cho group
[webservers:vars]
http_port=80
```

### YAML format

```yaml
# inventory.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
          ansible_host: 10.0.0.51
        web2.example.com:
      vars:
        http_port: 80
    
    dbservers:
      hosts:
        db1.example.com:
          ansible_host: 10.0.0.61
```

### Dynamic Inventory

```bash
# Lấy inventory từ AWS
ansible-inventory -i aws_ec2.yml --list

# Plugin inventory cho cloud
# aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
```

---

## 📕 Playbook - File Automation

### Cấu trúc cơ bản

```yaml
# deploy.yml
---
- name: Deploy web application  # Play name
  hosts: webservers             # Target hosts
  become: yes                   # Run as sudo
  vars:
    app_port: 8080
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
```

### Chạy playbook

```bash
# Basic run
ansible-playbook -i inventory.ini deploy.yml

# Check mode (dry run)
ansible-playbook deploy.yml --check

# Limit to specific hosts
ansible-playbook deploy.yml --limit web1

# Extra variables
ansible-playbook deploy.yml -e "app_port=9000"

# Verbose output
ansible-playbook deploy.yml -vvv
```

---

## 🧩 Modules - Các "động từ" của Ansible

### Modules phổ biến

```yaml
tasks:
  # Package management
  - name: Install package (Debian/Ubuntu)
    apt:
      name: nginx
      state: present
      update_cache: yes
  
  - name: Install package (RedHat/CentOS)
    yum:
      name: httpd
      state: latest
  
  # File operations
  - name: Copy file
    copy:
      src: files/app.conf
      dest: /etc/app/app.conf
      owner: root
      mode: '0644'
  
  - name: Template file
    template:
      src: templates/nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx
  
  - name: Create directory
    file:
      path: /var/log/myapp
      state: directory
      owner: www-data
      mode: '0755'
  
  # Service management
  - name: Start and enable service
    service:
      name: nginx
      state: started
      enabled: yes
  
  # User management
  - name: Create user
    user:
      name: deploy
      groups: sudo
      shell: /bin/bash
      create_home: yes
  
  # Commands
  - name: Run command
    command: /opt/app/setup.sh
    args:
      creates: /opt/app/.setup_done  # Skip if file exists
  
  - name: Run shell command with pipes
    shell: cat /etc/passwd | grep deploy
    register: result
  
  # Git
  - name: Clone repository
    git:
      repo: https://github.com/company/app.git
      dest: /opt/app
      version: main
  
  # Docker
  - name: Pull Docker image
    docker_image:
      name: nginx
      tag: latest
      source: pull
  
  - name: Run container
    docker_container:
      name: web
      image: nginx
      ports:
        - "80:80"
```

---

## 🔄 Handlers - Triggered Actions

```yaml
# handlers/main.yml
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
  
  - name: Reload nginx
    service:
      name: nginx
      state: reloaded

# Trong tasks
tasks:
  - name: Update nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx  # Trigger handler

  - name: Update site config
    template:
      src: site.conf.j2
      dest: /etc/nginx/sites-available/default
    notify: Reload nginx
```

**Handler chỉ chạy một lần** sau khi tất cả tasks hoàn thành, dù được notify nhiều lần.

---

## 📦 Roles - Reusable Automation

### Cấu trúc Role

```
roles/
└── nginx/
    ├── tasks/
    │   └── main.yml      # Main tasks
    ├── handlers/
    │   └── main.yml      # Handlers
    ├── templates/
    │   └── nginx.conf.j2 # Jinja2 templates
    ├── files/
    │   └── index.html    # Static files
    ├── vars/
    │   └── main.yml      # Variables
    ├── defaults/
    │   └── main.yml      # Default values
    └── meta/
        └── main.yml      # Dependencies
```

### Sử dụng Role

```yaml
# playbook.yml
---
- hosts: webservers
  become: yes
  roles:
    - nginx
    - { role: app, app_port: 8080 }
```

### Tạo Role

```bash
# Tạo role skeleton
ansible-galaxy init roles/nginx
```

### Ansible Galaxy

```bash
# Install role từ Galaxy
ansible-galaxy install geerlingguy.nginx

# requirements.yml
roles:
  - name: geerlingguy.nginx
    version: 3.1.0
  - name: geerlingguy.docker

# Install từ requirements
ansible-galaxy install -r requirements.yml
```

---

## 🔐 Ansible Vault - Secrets Management

### Encrypt file

```bash
# Encrypt file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt vars/secrets.yml

# View encrypted file
ansible-vault view secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Decrypt
ansible-vault decrypt secrets.yml
```

### Encrypt string

```bash
# Encrypt single value
ansible-vault encrypt_string 'supersecret' --name 'db_password'

# Output:
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  61626364...
```

### Sử dụng trong playbook

```yaml
# vars/main.yml (không encrypt)
db_user: myapp

# vars/secrets.yml (encrypted)
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  61626364...

# Chạy với vault password
ansible-playbook deploy.yml --ask-vault-pass
# Hoặc
ansible-playbook deploy.yml --vault-password-file ~/.vault_pass
```

---

## 📋 Best Practices

### 1. Cấu trúc Project

```
ansible-project/
├── ansible.cfg           # Ansible config
├── inventory/
│   ├── production/
│   │   └── hosts
│   └── staging/
│       └── hosts
├── group_vars/
│   ├── all.yml           # Variables cho all hosts
│   ├── webservers.yml    # Variables cho webservers
│   └── vault.yml         # Encrypted secrets
├── host_vars/
│   └── web1.yml          # Variables cho specific host
├── roles/
│   ├── common/
│   ├── nginx/
│   └── app/
├── playbooks/
│   ├── site.yml          # Main playbook
│   ├── webservers.yml
│   └── dbservers.yml
└── requirements.yml      # Galaxy roles
```

### 2. Variables hierarchy

```
# Precedence (thấp → cao):
1. Role defaults
2. Inventory group_vars
3. Inventory host_vars
4. Playbook vars
5. Extra vars (-e)
```

### 3. Idempotency

```yaml
# ❌ Không idempotent
- name: Add line to file
  shell: echo "line" >> /etc/config

# ✅ Idempotent
- name: Add line to file
  lineinfile:
    path: /etc/config
    line: "line"
```

### 4. Error handling

```yaml
tasks:
  - name: Try to start service
    service:
      name: myapp
      state: started
    ignore_errors: yes
    register: result
  
  - name: Fallback if failed
    debug:
      msg: "Service failed, running fallback"
    when: result is failed
```

---

## 🚨 Lỗi thường gặp

### 1. SSH Connection refused

```bash
# Error
UNREACHABLE! => SSH Error: Permission denied

# Fix
ansible-playbook deploy.yml --private-key ~/.ssh/mykey.pem -u ubuntu
```

### 2. Sudo password required

```bash
# Error
Missing sudo password

# Fix
ansible-playbook deploy.yml --ask-become-pass
# Hoặc trong inventory:
[webservers:vars]
ansible_become_pass=mysudopass  # Không recommend cho production
```

### 3. Python not found

```bash
# Error
module_stdout: /usr/bin/python: not found

# Fix trong inventory
[webservers:vars]
ansible_python_interpreter=/usr/bin/python3
```

---

## 📝 Tổng kết

Trong module này bạn đã học:

✅ Configuration Management và tại sao cần Ansible  
✅ Kiến trúc agentless của Ansible  
✅ Inventory, Playbooks, Modules  
✅ Roles và code reuse  
✅ Ansible Vault cho secrets  
✅ Best practices và troubleshooting  

---

## ⏭️ Tiếp theo

Để thực hành, hãy xem:

- [LABS.md](LABS.md) - Hands-on exercises
- [SCENARIOS.md](SCENARIOS.md) - Tình huống thực tế
- [QUIZ.md](QUIZ.md) - Tự kiểm tra kiến thức
