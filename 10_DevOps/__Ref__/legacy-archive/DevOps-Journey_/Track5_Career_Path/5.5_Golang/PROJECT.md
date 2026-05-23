# 🚀 Project: Go DevOps Tool

> **Build a DevOps CLI Tool in Go**
>
> *Xây dựng công cụ CLI DevOps bằng Go.*

---

## 🎯 Objective

Create a CLI tool called `devops-cli` that automates common DevOps tasks.

*(Tạo công cụ CLI gọi là `devops-cli` tự động hóa các tác vụ DevOps phổ biến.)*

---

## 📋 Requirements

### Core Features

1. **System Check** - Display system information *(Hiển thị thông tin hệ thống)*
2. **Docker Status** - Check Docker containers *(Kiểm tra Docker containers)*
3. **Port Scanner** - Scan ports on host *(Quét ports trên host)*
4. **Health Check** - Check URL health *(Kiểm tra health URL)*

### Commands

```bash
devops-cli system info        # System information
devops-cli docker ps          # List containers
devops-cli port scan <host>   # Scan ports
devops-cli health <url>       # Check URL health
```

---

## 🛠️ Tech Stack

- Go 1.21+
- Cobra CLI framework
- Viper for config
- Docker SDK for Go

---

## 📂 Project Structure

```
devops-cli/
├── cmd/
│   ├── root.go
│   ├── system.go
│   ├── docker.go
│   ├── port.go
│   └── health.go
├── pkg/
│   ├── system/
│   ├── docker/
│   └── network/
├── Dockerfile
├── go.mod
├── go.sum
└── README.md
```

---

## ✅ Deliverables

- [ ] Working CLI tool *(Công cụ CLI hoạt động)*
- [ ] Unit tests *(Unit tests)*
- [ ] Dockerfile *(Dockerfile)*
- [ ] README documentation *(Tài liệu README)*
- [ ] GitHub release *(Release GitHub)*

---

## 📊 Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Functionality | 40% |
| Code quality | 25% |
| Tests | 20% |
| Documentation | 15% |

---

**[← Back to README](./README.md)**
