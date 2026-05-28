# Ansible Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Ansible commands and playbook syntax for quick reference -- Lệnh và cú pháp playbook Ansible để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Ad-hoc Commands](#ad-hoc-commands) -- Lệnh Ad-hoc
- [Inventory](#inventory) -- Inventory
- [Playbook Basics](#playbook-basics) -- Playbook Cơ bản
- [Variables](#variables) -- Biến
- [Conditionals & Loops](#conditionals--loops) -- Điều kiện và Vòng lặp
- [Handlers](#handlers) -- Handlers
- [Templates](#templates) -- Templates
- [Roles](#roles) -- Roles
- [Vault](#vault) -- Vault
- [Common Modules](#common-modules) -- Modules Thường dùng

## <a id="ad-hoc-commands"></a> Ad-hoc Commands -- Lệnh Ad-hoc

```bash
# Basic syntax -- Cú pháp cơ bản
ansible <hosts> -m <module> -a "<arguments>"

# Ping hosts -- Ping hosts
ansible all -m ping                    # Ping all hosts -- Ping tất cả hosts
ansible webservers -m ping             # Ping group -- Ping nhóm

# Run commands -- Chạy lệnh
ansible all -m command -a "uptime"     # Run command -- Chạy lệnh
ansible all -m shell -a "cat /etc/passwd | head"  # Run shell command -- Chạy lệnh shell
ansible all -a "uptime"                # Default module is command -- Module mặc định là command

# File operations -- Thao tác file
ansible all -m copy -a "src=file.txt dest=/tmp/"  # Copy file -- Sao chép file
ansible all -m file -a "path=/tmp/test state=directory"  # Create directory -- Tạo thư mục
ansible all -m file -a "path=/tmp/test state=absent"  # Delete -- Xóa

# Package management -- Quản lý gói
ansible all -m apt -a "name=nginx state=present" -b  # Install (Debian) -- Cài đặt
ansible all -m yum -a "name=httpd state=present" -b  # Install (RHEL) -- Cài đặt
ansible all -m apt -a "name=nginx state=absent" -b   # Remove -- Gỡ bỏ

# Service management -- Quản lý service
ansible all -m service -a "name=nginx state=started" -b   # Start -- Khởi động
ansible all -m service -a "name=nginx state=stopped" -b   # Stop -- Dừng
ansible all -m service -a "name=nginx enabled=yes" -b     # Enable -- Bật khởi động cùng hệ thống

# User management -- Quản lý người dùng
ansible all -m user -a "name=deploy state=present" -b     # Create user -- Tạo người dùng

# Gather facts -- Thu thập facts
ansible all -m setup                   # All facts -- Tất cả facts
ansible all -m setup -a "filter=ansible_os_family"  # Filter facts -- Lọc facts

# Options -- Các tùy chọn
-i inventory.ini                       # Custom inventory -- Inventory tùy chỉnh
-b, --become                          # Run as root (sudo) -- Chạy với quyền root
-K, --ask-become-pass                 # Prompt for sudo password -- Nhắc mật khẩu sudo
-u username                           # Remote user -- Người dùng remote
-k, --ask-pass                        # Prompt for SSH password -- Nhắc mật khẩu SSH
--limit hosts                         # Limit to specific hosts -- Giới hạn hosts cụ thể
-v, -vv, -vvv                        # Verbosity levels -- Mức độ chi tiết
```

## <a id="inventory"></a> Inventory

```ini
# INI format (inventory.ini) -- Định dạng INI
[webservers]
web1.example.com
web2.example.com ansible_host=192.168.1.22

[dbservers]
db1.example.com ansible_port=2222
db2.example.com

[production:children]
webservers
dbservers

[webservers:vars]
http_port=80
ansible_user=deploy

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

```yaml
# YAML format (inventory.yml) -- Định dạng YAML
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_host: 192.168.1.22
      vars:
        http_port: 80
    dbservers:
      hosts:
        db1.example.com:
          ansible_port: 2222
        db2.example.com:
    production:
      children:
        webservers:
        dbservers:
  vars:
    ansible_python_interpreter: /usr/bin/python3
```

```bash
# Inventory commands -- Lệnh inventory
ansible-inventory --list              # Show inventory -- Hiển thị inventory
ansible-inventory --graph             # Show inventory graph -- Hiển thị đồ thị inventory
ansible all --list-hosts              # List all hosts -- Liệt kê tất cả hosts
```

## <a id="playbook-basics"></a> Playbook Basics -- Playbook Cơ bản

```yaml
# Basic playbook (site.yml) -- Playbook cơ bản
---
- name: Configure web servers # -- Cấu hình web servers
  hosts: webservers
  become: yes                 # Run as root -- Chạy với quyền root
  gather_facts: yes           # Collect system info -- Thu thập thông tin hệ thống

  tasks:
    - name: Install nginx     # -- Cài đặt nginx
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Start nginx       # -- Khởi động nginx
      service:
        name: nginx
        state: started
        enabled: yes

    - name: Copy config file  # -- Sao chép file cấu hình
      copy:
        src: nginx.conf
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: '0644'
      notify: Reload nginx    # Trigger handler -- Kích hoạt handler

  handlers:
    - name: Reload nginx      # -- Reload nginx
      service:
        name: nginx
        state: reloaded
```

```bash
# Playbook commands -- Lệnh playbook
ansible-playbook site.yml              # Run playbook -- Chạy playbook
ansible-playbook site.yml -i inventory.ini  # With inventory -- Với inventory
ansible-playbook site.yml --check      # Dry run -- Chạy thử
ansible-playbook site.yml --diff       # Show changes -- Hiển thị thay đổi
ansible-playbook site.yml --tags "nginx"  # Run specific tags -- Chạy tags cụ thể
ansible-playbook site.yml --skip-tags "debug"  # Skip tags -- Bỏ qua tags
ansible-playbook site.yml --limit webservers  # Limit hosts -- Giới hạn hosts
ansible-playbook site.yml --start-at-task "Install nginx"  # Start at task -- Bắt đầu từ task
```

## <a id="variables"></a> Variables -- Biến

```yaml
# Variables in playbook -- Biến trong playbook
---
- name: Example playbook
  hosts: all
  vars:
    app_name: myapp
    app_port: 8080
    users:
      - name: alice
        role: admin
      - name: bob
        role: user

  vars_files:
    - vars/common.yml
    - vars/{{ environment }}.yml

  tasks:
    - name: Use variables
      debug:
        msg: "App {{ app_name }} on port {{ app_port }}"

    - name: Loop with list variable
      user:
        name: "{{ item.name }}"
        state: present
      loop: "{{ users }}"
```

```yaml
# Host/Group variables -- Biến host/group
# group_vars/webservers.yml
---
http_port: 80
max_connections: 100

# host_vars/web1.example.com.yml
---
server_id: 1
```

```yaml
# Register variables -- Đăng ký biến
- name: Get command output
  command: hostname
  register: hostname_result

- name: Display result
  debug:
    msg: "Hostname: {{ hostname_result.stdout }}"
```

```yaml
# Facts and magic variables -- Facts và magic variables
{{ ansible_hostname }}                 # Hostname
{{ ansible_os_family }}               # OS family (Debian, RedHat)
{{ ansible_distribution }}            # OS name (Ubuntu, CentOS)
{{ ansible_memory_mb.real.total }}    # Total RAM in MB
{{ inventory_hostname }}              # Current host name
{{ hostvars['web1']['http_port'] }}   # Variable from another host
{{ groups['webservers'] }}            # List of hosts in group
```

```bash
# Variable precedence (lowest to highest) -- Thứ tự ưu tiên biến (thấp đến cao)
# 1. Role defaults
# 2. Inventory vars
# 3. Playbook vars
# 4. Role vars
# 5. Task vars
# 6. Extra vars (-e)
```

## <a id="conditionals--loops"></a> Conditionals & Loops -- Điều kiện và Vòng lặp

```yaml
# Conditionals -- Điều kiện
- name: Install on Debian only
  apt:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"

- name: Multiple conditions
  service:
    name: nginx
    state: started
  when:
    - ansible_os_family == "Debian"
    - nginx_installed.changed

- name: OR condition
  debug:
    msg: "This is a web or db server"
  when: inventory_hostname in groups['webservers'] or inventory_hostname in groups['dbservers']

# Loops -- Vòng lặp
- name: Install multiple packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - vim
    - curl

- name: Loop with dict
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
  loop:
    - { name: alice, groups: admins }
    - { name: bob, groups: users }

- name: Loop with index
  debug:
    msg: "{{ index }}: {{ item }}"
  loop:
    - apple
    - banana
  loop_control:
    index_var: index

- name: Loop with register
  command: echo "{{ item }}"
  loop:
    - one
    - two
  register: echo_results

- name: Display registered loop results
  debug:
    msg: "{{ item.stdout }}"
  loop: "{{ echo_results.results }}"
```

## <a id="handlers"></a> Handlers

```yaml
# Handlers -- Handlers
- name: Configure app
  hosts: all
  tasks:
    - name: Update config
      template:
        src: app.conf.j2
        dest: /etc/app/app.conf
      notify:
        - Restart app
        - Clear cache

    - name: Force handler execution
      meta: flush_handlers

  handlers:
    - name: Restart app
      service:
        name: app
        state: restarted

    - name: Clear cache
      command: /usr/bin/clear-cache.sh
```

## <a id="templates"></a> Templates

```jinja2
{# templates/nginx.conf.j2 #}
{# This is a Jinja2 comment -- Đây là comment Jinja2 #}

server {
    listen {{ http_port }};
    server_name {{ server_name }};

    {% if ssl_enabled %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert }};
    {% endif %}

    {% for location in locations %}
    location {{ location.path }} {
        proxy_pass {{ location.backend }};
    }
    {% endfor %}
}

# Variables and filters -- Biến và filters
{{ variable | default('default_value') }}
{{ my_list | join(', ') }}
{{ my_string | upper }}
{{ my_string | lower }}
{{ my_string | replace('old', 'new') }}
{{ my_number | int }}
{{ my_path | basename }}
{{ my_path | dirname }}
```

```yaml
# Use template -- Sử dụng template
- name: Deploy nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
```

## <a id="roles"></a> Roles

```
# Role directory structure -- Cấu trúc thư mục role
roles/
└── nginx/
    ├── defaults/
    │   └── main.yml      # Default variables -- Biến mặc định
    ├── files/
    │   └── index.html    # Static files -- Files tĩnh
    ├── handlers/
    │   └── main.yml      # Handlers
    ├── meta/
    │   └── main.yml      # Role metadata -- Metadata của role
    ├── tasks/
    │   └── main.yml      # Main tasks -- Tasks chính
    ├── templates/
    │   └── nginx.conf.j2 # Jinja2 templates
    └── vars/
        └── main.yml      # Role variables -- Biến của role
```

```yaml
# roles/nginx/tasks/main.yml
---
- name: Install nginx
  apt:
    name: nginx
    state: present

- name: Deploy config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: Restart nginx

- name: Ensure started
  service:
    name: nginx
    state: started
    enabled: yes
```

```yaml
# Use role in playbook -- Sử dụng role trong playbook
---
- name: Configure servers
  hosts: webservers
  roles:
    - nginx
    - { role: app, app_port: 8080 }
    - role: database
      vars:
        db_name: mydb
      when: inventory_hostname in groups['dbservers']
      tags: database
```

```bash
# Role commands -- Lệnh role
ansible-galaxy init role_name          # Create role structure -- Tạo cấu trúc role
ansible-galaxy install geerlingguy.nginx  # Install from Galaxy -- Cài đặt từ Galaxy
ansible-galaxy install -r requirements.yml  # Install from file -- Cài đặt từ file
ansible-galaxy list                     # List installed roles -- Liệt kê roles đã cài
```

## <a id="vault"></a> Vault

```bash
# Create encrypted file -- Tạo file mã hóa
ansible-vault create secrets.yml

# Edit encrypted file -- Chỉnh sửa file mã hóa
ansible-vault edit secrets.yml

# Encrypt existing file -- Mã hóa file hiện có
ansible-vault encrypt vars.yml

# Decrypt file -- Giải mã file
ansible-vault decrypt vars.yml

# View encrypted file -- Xem file mã hóa
ansible-vault view secrets.yml

# Change password -- Đổi mật khẩu
ansible-vault rekey secrets.yml

# Encrypt string -- Mã hóa chuỗi
ansible-vault encrypt_string 'supersecret' --name 'db_password'

# Run playbook with vault -- Chạy playbook với vault
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```

```yaml
# Using encrypted variable -- Sử dụng biến mã hóa
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  61626364656667686970...
```

## <a id="common-modules"></a> Common Modules -- Modules Thường dùng

```yaml
# File modules -- Modules file
- name: Copy file
  copy:
    src: local.txt
    dest: /remote/path/file.txt
    owner: root
    mode: '0644'

- name: Create directory
  file:
    path: /path/to/dir
    state: directory
    mode: '0755'

- name: Create symlink
  file:
    src: /path/to/source
    dest: /path/to/link
    state: link

- name: Download file
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz

# Package modules -- Modules gói
- name: Install package (apt)
  apt:
    name: nginx
    state: present
    update_cache: yes

- name: Install package (yum)
  yum:
    name: httpd
    state: present

# Service module -- Module service
- name: Manage service
  service:
    name: nginx
    state: started
    enabled: yes

- name: Systemd service
  systemd:
    name: nginx
    state: restarted
    daemon_reload: yes

# User module -- Module user
- name: Create user
  user:
    name: deploy
    groups: sudo
    shell: /bin/bash
    generate_ssh_key: yes

# Command modules -- Modules lệnh
- name: Run command
  command: /path/to/script.sh
  args:
    chdir: /working/directory
    creates: /path/to/marker  # Skip if exists -- Bỏ qua nếu tồn tại

- name: Run shell command
  shell: cat /etc/passwd | grep deploy
  register: result
  changed_when: false

# Debug module -- Module debug
- name: Print variable
  debug:
    var: my_variable

- name: Print message
  debug:
    msg: "Value is {{ my_variable }}"
```

---
