# ✅ Solutions: Ansible

---

## Exercise 1: Basic Playbook

```yaml
---
- name: Setup nginx web server
  hosts: webservers
  become: yes
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Copy nginx config
      copy:
        src: files/nginx.conf
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx
    
    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes
  
  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

---

## Exercise 3: Role Structure

```
roles/
├── webserver/
│   ├── tasks/main.yml
│   ├── handlers/main.yml
│   ├── templates/nginx.conf.j2
│   └── defaults/main.yml
├── database/
│   ├── tasks/main.yml
│   └── templates/pg_hba.conf.j2
└── common/
    └── tasks/main.yml
```

```yaml
# site.yml
---
- hosts: all
  roles:
    - common

- hosts: webservers
  roles:
    - webserver

- hosts: databases
  roles:
    - database
```

---

## Exercise 5: Ansible Vault

```bash
# Create vault password file
echo "secret123" > .vault_pass

# Encrypt file
ansible-vault encrypt group_vars/production/secrets.yml

# Encrypt variable
ansible-vault encrypt_string 'MySecretPassword' --name 'db_password'

# Run with vault
ansible-playbook site.yml --vault-password-file .vault_pass
```

---

**[← Back to Exercises](./EXERCISES.md)**
