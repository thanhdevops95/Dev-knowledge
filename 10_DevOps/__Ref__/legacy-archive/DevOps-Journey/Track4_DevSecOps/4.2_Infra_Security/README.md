# 🛡️ Module 4.2: Infrastructure Security

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Secure Infrastructure** - Hardening, compliance, and security monitoring.
>
> *Hạ tầng bảo mật - Hardening, tuân thủ, và giám sát bảo mật.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Apply cloud security best practices (Áp dụng bảo mật cloud)
- ✅ Implement network security (Triển khai bảo mật mạng)
- ✅ Manage secrets (Quản lý secrets)
- ✅ Understand compliance frameworks (Hiểu các framework tuân thủ)
- ✅ Setup security monitoring (Thiết lập giám sát bảo mật)
- ✅ Perform incident response (Xử lý sự cố)

---

## 📚 Content (Nội dung)

### 1. Why Secrets Management Matters? (Tại sao Secrets Management quan trọng?)

**Problem:** Secrets (passwords, API keys, tokens) leakage is the #1 cause of data breaches.

*Secrets (passwords, API keys, tokens) bị lộ là nguyên nhân #1 của các vụ data breach.*

| Common Mistake | Consequence |
|----------------|-------------|
| Hardcode in source code | Exposed when pushed to public Git |
| Store in `.env` file | Anyone with file access can see |
| Share passwords | No audit trail of who used it |
| No key rotation | Attacker has permanent access if leaked |

**Solution:** Use **Secrets Manager** - centralized storage, encryption, access control.

*Giải pháp: Sử dụng **Secrets Manager** - lưu trữ tập trung, mã hóa, kiểm soát truy cập.*

---

### 2. HashiCorp Vault

**Vault** is the most popular secrets management tool. It provides **dynamic secrets** (temporary credentials for each request).

*Vault là công cụ quản lý secrets phổ biến nhất. Nó cung cấp **dynamic secrets** (tạo credentials tạm thời cho mỗi request).*

```bash
# Store secret in Vault (Lưu secret vào Vault)
vault kv put secret/myapp db_password=secret123 api_key=abc123

# Read secret from Vault (Đọc secret từ Vault)
vault kv get secret/myapp

# Read only 1 field (Đọc chỉ 1 field)
vault kv get -field=db_password secret/myapp
```

**Explanation:** *(Giải thích:)*

- `secret/myapp`: Storage path (can set permissions per path) *(Path lưu trữ - có thể phân quyền theo path)*
- `db_password=secret123`: Key-value pair
- Secrets are encrypted at-rest and in-transit *(Secrets được mã hóa at-rest và in-transit)*

---

### 3. AWS Secrets Manager

If you use AWS, **Secrets Manager** integrates with RDS, Lambda, ECS out of the box.

*Nếu bạn dùng AWS, **Secrets Manager** tích hợp sẵn với RDS, Lambda, ECS.*

```bash
# Create new secret (Tạo secret mới)
aws secretsmanager create-secret \
  --name prod/myapp/db \
  --secret-string '{"username":"admin","password":"secret123"}'

# Read secret (Đọc secret)
aws secretsmanager get-secret-value --secret-id prod/myapp/db

# Rotate secret automatically for RDS (Rotate secret tự động cho RDS)
aws secretsmanager rotate-secret --secret-id prod/myapp/db
```

**Benefits compared to Vault:** *(Lợi ích so với Vault:)*

- No server management needed *(Không cần quản lý server)*
- Built-in integration with AWS services *(Tích hợp sẵn với AWS services)*
- Automatic rotation for RDS *(Automatic rotation cho RDS)*

---

### 4. AWS Security Best Practices (Bảo mật AWS)

### 5. CIS Benchmarks

- OS hardening *(Hardening hệ điều hành)*
- SSH configuration *(Cấu hình SSH)*
- Firewall rules *(Quy tắc tường lửa)*
- Audit logging *(Ghi nhật ký kiểm toán)*

### 6. Compliance (Tuân thủ)

```yaml
# InSpec
control 'ssh-config' do
  impact 1.0
  title 'SSH configuration'
  
  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
    its('PasswordAuthentication') { should eq 'no' }
  end
end
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
| [4.1 Security Pipeline](../4.1_Security_in_Pipeline/) | **4.2 Infra Security** | [4.3 Capstone](../4.3_Capstone_Project/) |

---

**Secure your infrastructure! 🛡️**

*Bảo mật hạ tầng của bạn!*

</div>
