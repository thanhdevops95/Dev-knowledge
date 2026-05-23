# 📋 Infrastructure Security - Cheatsheet

> **Quick Reference for Infrastructure Security**
>
> *Tra cứu nhanh bảo mật hạ tầng*

---

## 🔐 HashiCorp Vault

### Basic Commands (Lệnh cơ bản)

```bash
# Start server (Khởi động server)
vault server -dev

# Login (Đăng nhập)
vault login token

# Secrets (Quản lý secrets)
vault kv put secret/myapp password=secret123
vault kv get secret/myapp
vault kv delete secret/myapp
vault kv list secret/
```

### Docker

```bash
docker run -d --name vault \
  -p 8200:8200 \
  -e VAULT_DEV_ROOT_TOKEN_ID=mytoken \
  vault
```

---

## 🔑 SSH Security (Bảo mật SSH)

```bash
# Generate key (Tạo key)
ssh-keygen -t ed25519 -C "email@example.com"

# Secure sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers user1 user2

# Test config (Kiểm tra cấu hình)
sshd -t
```

---

## 🔥 Firewall (Tường lửa)

### UFW (Ubuntu)

```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny from 192.168.1.100
sudo ufw status verbose
```

### iptables

```bash
# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Block IP
iptables -A INPUT -s 192.168.1.100 -j DROP

# Save rules (Lưu rules)
iptables-save > /etc/iptables.rules
```

---

## 🛡️ Kubernetes Security

### RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
subjects:
  - kind: User
    name: developer
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

### Security Context

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
  containers:
    - name: app
      securityContext:
        readOnlyRootFilesystem: true
        allowPrivilegeEscalation: false
```

---

## 📊 Compliance Tools (Công cụ tuân thủ)

| Tool | Purpose (Mục đích) |
|------|---------------------|
| **OPA** | Policy as Code |
| **Falco** | Runtime security |
| **kube-bench** | CIS benchmark |
| **kube-hunter** | Security testing |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
