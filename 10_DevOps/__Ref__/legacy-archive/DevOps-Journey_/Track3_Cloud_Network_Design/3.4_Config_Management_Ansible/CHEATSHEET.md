# 📋 Ansible - Cheatsheet

> **Quick Reference for Ansible**
>
> *Tra cứu nhanh Ansible*

---

## 🔧 Basic Commands (Lệnh cơ bản)

```bash
# Ad-hoc commands (Lệnh ad-hoc)
ansible all -m ping                          # Ping all hosts
ansible webservers -m shell -a "uptime"      # Run command
ansible all -m copy -a "src=file dest=/tmp/" # Copy file

# Playbook execution (Chạy playbook)
ansible-playbook playbook.yml
ansible-playbook playbook.yml -i inventory.ini
ansible-playbook playbook.yml --check        # Dry run (Thử)
ansible-playbook playbook.yml -v             # Verbose

# Inventory (Kho host)
ansible-inventory --list                     # List inventory
ansible-inventory --graph                    # Graph view
```

---

## 📝 Inventory File

```ini
# inventory.ini
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[dbservers]
db1 ansible_host=192.168.1.20

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

---

## 📋 Basic Playbook

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  
  vars:
    http_port: 80
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: Copy config file
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx
  
  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

---

## 🧩 Common Modules (Modules phổ biến)

| Module | Purpose (Mục đích) |
|--------|---------------------|
| `apt/yum` | Package management |
| `copy` | Copy files |
| `template` | Jinja2 templates |
| `file` | File/directory management |
| `service` | Service management |
| `user` | User management |
| `git` | Git operations |
| `docker_container` | Docker management |

---

## 🔄 Variables & Facts

```yaml
# playbook.yml
vars:
  app_name: myapp
  
tasks:
  - name: Debug facts
    debug:
      var: ansible_facts['os_family']
  
  - name: Use variable
    debug:
      msg: "App is {{ app_name }}"
```

---

## 📁 Roles Structure (Cấu trúc Roles)

```
roles/
└── webserver/
    ├── tasks/main.yml
    ├── handlers/main.yml
    ├── templates/
    ├── files/
    ├── vars/main.yml
    └── defaults/main.yml
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
