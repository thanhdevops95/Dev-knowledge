# 🔬 Labs: Ansible

---

## 🔬 Lab 1: Ansible Setup

```bash
# Install Ansible
pip install ansible

# Verify
ansible --version

# Create inventory
cat > inventory.ini << EOF
[webservers]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
EOF

# Test connection
ansible all -i inventory.ini -m ping
```

---

## 🔬 Lab 2: Ad-hoc Commands

```bash
# Ping all hosts
ansible all -m ping

# Run command
ansible webservers -m shell -a "uptime"

# Install package
ansible webservers -m apt -a "name=nginx state=present" -b

# Copy file
ansible webservers -m copy -a "src=file.txt dest=/tmp/"

# Gather facts
ansible webservers -m setup
```

---

## 🔬 Lab 3: First Playbook

```yaml
# playbook.yml
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
    
    - name: Copy index.html
      copy:
        content: "<h1>Hello from {{ inventory_hostname }}</h1>"
        dest: /var/www/html/index.html
```

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## 🔬 Lab 4: Variables & Templates

```yaml
# vars/main.yml
app_name: myapp
app_port: 3000
app_env: production

# templates/app.conf.j2
server {
    listen {{ http_port }};
    server_name {{ inventory_hostname }};
    
    location / {
        proxy_pass http://localhost:{{ app_port }};
    }
}

# playbook.yml
- name: Deploy config
  template:
    src: templates/app.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}
  notify: Reload nginx

handlers:
  - name: Reload nginx
    service:
      name: nginx
      state: reloaded
```

---

## 🔬 Lab 5: Roles

```bash
# Create role structure
ansible-galaxy init roles/webserver

# Structure
roles/webserver/
├── tasks/main.yml
├── handlers/main.yml
├── templates/
├── vars/main.yml
└── defaults/main.yml
```

```yaml
# roles/webserver/tasks/main.yml
---
- name: Install nginx
  apt:
    name: nginx
    state: present

- name: Copy config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx

# playbook.yml
- hosts: webservers
  roles:
    - webserver
```

---

## ✅ Checklist

- [ ] Lab 1: Setup
- [ ] Lab 2: Ad-hoc
- [ ] Lab 3: Playbook
- [ ] Lab 4: Templates
- [ ] Lab 5: Roles

---

**[← Back to README](./README.md)**
