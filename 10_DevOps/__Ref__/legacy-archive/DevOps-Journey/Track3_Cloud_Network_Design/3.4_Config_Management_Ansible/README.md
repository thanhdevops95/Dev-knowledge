# 🔧 Module 3.4: Configuration Management - Ansible

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Infrastructure as Code** - Automate with Ansible.
>
> *Infrastructure as Code - Tự động hóa với Ansible.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand Ansible architecture (Hiểu kiến trúc Ansible)
- ✅ Write Playbooks and roles (Viết Playbooks và roles)
- ✅ Manage inventory (Quản lý inventory)
- ✅ Use variables and templates (Sử dụng biến và templates)
- ✅ Explore Ansible Galaxy (Khám phá Ansible Galaxy)
- ✅ Work with AWX/Tower (Làm việc với AWX/Tower)

---

## 📚 Content (Nội dung)

### 1. What is Ansible? (Ansible là gì?)

**Ansible** is an open-source IT automation tool. It handles configuration management, application deployment, cloud provisioning, and ad-hoc task execution.

*Ansible là công cụ tự động hóa CNTT mã nguồn mở. Nó xử lý quản lý cấu hình, triển khai ứng dụng, cấp phép đám mây và thực thi tác vụ đặc biệt.*

#### Why Ansible? (Tại sao Ansible?)

**Problem:** Managing 100+ servers manually is impossible. SSHing into each server to install/configure takes hours.

*Quản lý 100+ servers bằng tay là không thể. SSH vào từng server để cài đặt/cấu hình tốn hàng giờ.*

**Solution:** Ansible - 1 command configures all servers simultaneously.

*Giải pháp: Ansible - 1 command cấu hình tất cả servers cùng lúc.*

```
┌─────────────────────────────────────────────────────────────┐
│                    ANSIBLE ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Control Node (Your laptop/server)                         │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Playbook.yml  │  Inventory  │  Roles               │   │
│   └────────────────────────┬────────────────────────────┘   │
│                            │                                 │
│                            │ SSH (No agent needed!)         │
│                            │                                 │
│   ┌────────────────────────┼────────────────────────────┐   │
│   │                        │                             │   │
│   ▼                        ▼                             ▼   │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│   │ Server 1 │      │ Server 2 │      │ Server N │          │
│   │ (web)    │      │ (web)    │      │ (db)     │          │
│   └──────────┘      └──────────┘      └──────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Ansible vs Terraform vs Chef

| Feature | Ansible | Terraform | Chef |
|---------|---------|-----------|------|
| **Purpose** | Configuration | Infrastructure | Configuration |
| **Language** | YAML | HCL | Ruby DSL |
| **Agent** | ❌ Agentless (SSH) | ❌ No agent | ✅ Agent required |
| **State** | Push-based | Pull-based (state file) | Pull-based (server) |
| **Best for** | Config servers | Provision infrastructure | Complex configs |

**Conclusion:** Use **Terraform** to create servers → Use **Ansible** to configure servers.

*Kết luận: Dùng **Terraform** để tạo servers → Dùng **Ansible** để cấu hình servers.*

---

### 2. Inventory

**Inventory** is the list of servers Ansible will manage, grouped by function.

*Inventory là danh sách các servers mà Ansible sẽ quản lý, được nhóm theo chức năng.*

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com

[all:vars]
ansible_user=ubuntu
```

**Giải thích:**

- `[webservers]`: Group name (có thể target riêng nhóm này)
- `web1.example.com`: Host (có thể dùng IP)
- `[all:vars]`: Variables áp dụng cho tất cả hosts

### 3. Playbook

Playbooks are YAML files that define what tasks to run on which hosts. This is where automation happens.

*Playbooks là các files YAML định nghĩa tasks chạy trên hosts nào. Đây là nơi automation xảy ra.*

```yaml
# playbook.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx (Cài nginx)
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start nginx (Khởi động nginx)
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Copy config (Sao chép cấu hình)
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx
  
  handlers:
    - name: Restart nginx (Khởi động lại nginx)
      service:
        name: nginx
        state: restarted
```

### 4. Roles (Cấu trúc roles)

```
roles/
└── webserver/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   └── nginx.conf.j2
    ├── vars/
    │   └── main.yml
    └── defaults/
        └── main.yml
```

### 5. Common Commands (Các lệnh phổ biến)

```bash
# Run playbook (Chạy playbook)
ansible-playbook -i inventory.ini playbook.yml

# Check mode - dry run (Chế độ kiểm tra)
ansible-playbook playbook.yml --check

# Limit to specific hosts (Giới hạn hosts)
ansible-playbook playbook.yml --limit webservers

# Pass extra variables (Truyền biến)
ansible-playbook playbook.yml -e "env=production"
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.3 Databases](../3.3_Databases_for_DevOps/) | **3.4 Ansible** | [3.5 Terraform](../3.5_Terraform_IaC/) |

---

**Master configuration management! 🔧**

*Thành thạo quản lý cấu hình!*

</div>
