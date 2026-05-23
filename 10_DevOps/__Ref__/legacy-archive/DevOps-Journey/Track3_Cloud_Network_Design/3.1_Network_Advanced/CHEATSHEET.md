# 📋 Network Advanced - Cheatsheet

> **Quick Reference for Advanced Networking**
>
> *Tra cứu nhanh mạng nâng cao*

---

## 🌐 VPC Concepts (Khái niệm VPC)

| Component | Description (Mô tả) |
|-----------|---------------------|
| VPC | Virtual Private Cloud - Mạng ảo riêng |
| Subnet | Phân đoạn mạng con |
| Internet Gateway | Kết nối internet |
| NAT Gateway | NAT cho private subnets |
| Route Table | Bảng định tuyến |
| Security Group | Tường lửa stateful |
| NACL | Tường lửa stateless |

---

## 🔢 CIDR Quick Reference

| CIDR | Hosts | Use Case |
|------|-------|----------|
| /16 | 65,534 | VPC |
| /20 | 4,094 | Large subnet |
| /24 | 254 | Standard subnet |
| /28 | 14 | Small subnet |

---

## 🔒 Security Groups vs NACLs (So sánh)

| Feature | Security Group | NACL |
|---------|---------------|------|
| Level | Instance | Subnet |
| Stateful | Yes | No |
| Rules | Allow only | Allow & Deny |
| Order | All evaluated | Order matters |

---

## 📡 Load Balancing Types

| Type | Layer | Use Case |
|------|-------|----------|
| ALB | 7 (HTTP) | Web apps, microservices |
| NLB | 4 (TCP) | High performance, gaming |
| CLB | 4/7 | Legacy |

---

## 🔧 Common Commands (Lệnh thường dùng)

```bash
# DNS troubleshooting (Xử lý DNS)
dig +trace example.com
nslookup example.com

# Connectivity (Kết nối)
traceroute -n example.com
mtr example.com

# Port scanning
nc -zv host 22-443
nmap -p 22,80,443 host
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
