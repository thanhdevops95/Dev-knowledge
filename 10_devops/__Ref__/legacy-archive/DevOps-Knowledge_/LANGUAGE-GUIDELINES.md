# LANGUAGE GUIDELINES -- Hướng dẫn Ngôn ngữ

> Bilingual language rules for the Knowledge Base -- Quy tắc ngôn ngữ song ngữ cho Knowledge Base

## 📋 General Principles -- Nguyên tắc Chung

### ✅ Standard Format -- Format Chuẩn

**Two main patterns -- Hai pattern chính:**

1. **For terms that need translation -- Cho thuật ngữ cần dịch:**
   - Format: `English -- Tiếng Việt`
   - Example: `Installation -- Cài đặt`

2. **For terms with English explanation -- Cho thuật ngữ có bổ nghĩa tiếng Anh:**
   - Format: `Term (English explanation -- Dịch tiếng Việt)`
   - Example: `Docker (Container Platform -- Nền tảng Container)`

### Key Rules -- Quy tắc Chính

- **`--`** = Vietnamese translation -- Dịch tiếng Việt
- **`()`** = English explanation with Vietnamese translation -- Bổ nghĩa tiếng Anh kèm dịch tiếng Việt
- Always English first, Vietnamese after `--` -- Luôn tiếng Anh trước, tiếng Việt sau `--`

## 📝 Specific Cases -- Các Trường hợp Cụ thể

### 1. Headings -- Tiêu đề

#### Case 1: Term doesn't need translation -- Thuật ngữ không cần dịch

**✅ CORRECT -- ĐÚNG:**
```markdown
# Docker (Container Platform -- Nền tảng Container)
# Kubernetes (Container Orchestration -- Điều phối Container)
# API (Application Programming Interface -- Giao diện Lập trình Ứng dụng)
```

**Explanation -- Giải thích:**
- `Docker` không cần dịch (proper noun)
- `(Container Platform -- Nền tảng Container)` bổ nghĩa cho Docker

#### Case 2: Term needs translation -- Thuật ngữ cần dịch

**✅ CORRECT -- ĐÚNG:**
```markdown
# Installation -- Cài đặt
# Configuration -- Cấu hình
# Troubleshooting -- Xử lý Sự cố
# Best Practices -- Thực hành Tốt nhất
```

#### Case 3: Term with additional context -- Thuật ngữ với ngữ cảnh bổ sung

**✅ CORRECT -- ĐÚNG:**
```markdown
# CI/CD (Continuous Integration/Continuous Deployment -- Tích hợp & Triển khai Liên tục)
# IaC (Infrastructure as Code -- Hạ tầng dưới dạng Mã)
```

**❌ INCORRECT -- SAI:**
```markdown
# Nền tảng Container - Docker
# Docker (Nền tảng Container)
# Cài đặt
```

### 2. Content Sentences -- Câu trong Nội dung

**✅ CORRECT -- ĐÚNG:**
```markdown
Linux is the operating system that powers most servers worldwide. -- Linux là hệ điều hành cung cấp sức mạnh cho hầu hết các servers trên toàn thế giới.

Docker is a container platform that enables developers to package applications. -- Docker là nền tảng container cho phép developers đóng gói ứng dụng.

A container is a lightweight, standalone package. -- Container là một gói nhẹ, độc lập.

Kubernetes orchestrates containerized applications across clusters. -- Kubernetes điều phối các ứng dụng được container hóa trên các clusters.
```

**For shorter content -- Cho nội dung ngắn:**
```markdown
Fast deployment. -- Triển khai nhanh.
Portable containers. -- Containers di động.
Isolated environments. -- Môi trường cô lập.
```

**❌ INCORRECT -- SAI:**
```markdown
Container (container) là một đơn vị đóng gói ứng dụng...
Linux là hệ điều hành...
Docker cung cấp nền tảng container...
```

### 3. Lists and Table of Contents -- Danh sách và Mục lục

**✅ CORRECT -- ĐÚNG:**
```markdown
## Table of Contents -- Mục lục

- [Introduction](#introduction) -- Giới thiệu
- [Docker Basics](#docker-basics) -- Kiến thức Cơ bản về Docker
- [Container Images](#container-images) -- Làm việc với Images
- [Networking](#networking) -- Mạng
- [Best Practices](#best-practices) -- Thực hành Tốt nhất

**Key Features -- Tính năng Chính:**
- Fast deployment -- Triển khai nhanh
- Portable containers -- Containers di động
- Isolated environments -- Môi trường cô lập
- Easy scaling -- Mở rộng dễ dàng
```

### 4. Term Definitions -- Định nghĩa Thuật ngữ

**✅ CORRECT -- ĐÚNG:**
```markdown
### API (Application Programming Interface -- Giao diện Lập trình Ứng dụng)

**Definition -- Định nghĩa:** A set of rules and protocols that allows different software applications to communicate with each other. -- Một tập hợp các quy tắc và giao thức cho phép các ứng dụng phần mềm khác nhau giao tiếp với nhau.

**Purpose -- Mục đích:** Enable integration between systems. -- Cho phép tích hợp giữa các hệ thống.

**Examples -- Ví dụ:** REST API, GraphQL API, SOAP API
```

### 5. Code Comments -- Chú thích Code

**✅ CORRECT -- ĐÚNG:**
```bash
#!/bin/bash

###############################################################################
# Backup Script -- Script Sao lưu
# Description: Automated backup for files and databases
#              -- Mô tả: Tự động sao lưu files và databases
###############################################################################

# Configuration -- Cấu hình
BACKUP_DIR="/backup"
SOURCE_DIR="/var/www"

# Start backup process -- Bắt đầu quá trình backup
log_info "Starting file backup..."

# Check if directory exists -- Kiểm tra thư mục có tồn tại không
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR" # Create backup directory -- Tạo thư mục backup
fi
```

### 6. File and Directory Names -- Tên File và Thư mục

**✅ CORRECT -- ĐÚNG:**
```
THEORY/
CHEATSHEETS/
TROUBLESHOOTING/
CODE-SAMPLES/
docker-commands.md
kubernetes-errors.md
linux-fundamentals.md
```

**❌ INCORRECT -- SAI:**
```
LY-THUYET/
BANG-TRA-CUU/
lenh-docker.md
```

### 7. Short Descriptions -- Mô tả Ngắn

**✅ CORRECT -- ĐÚNG:**
```markdown
> Container platform for packaging and running applications -- Nền tảng container để đóng gói và chạy ứng dụng

> Monitoring and alerting system for infrastructure -- Hệ thống giám sát và cảnh báo cho infrastructure

> Infrastructure as Code tool -- Công cụ Infrastructure as Code
```

## 🎯 Complete Example -- Ví dụ Hoàn chỉnh

```markdown
# Docker (Container Platform -- Nền tảng Container)

> Container platform for packaging and running applications -- Nền tảng container để đóng gói và chạy ứng dụng

## Table of Contents -- Mục lục

- [Introduction](#introduction) -- Giới thiệu
- [Installation](#installation) -- Cài đặt
- [Docker Architecture](#docker-architecture) -- Kiến trúc Docker
- [Images & Containers](#images--containers) -- Images và Containers
- [Best Practices](#best-practices) -- Thực hành Tốt nhất

## Introduction -- Giới thiệu

### What is Docker? -- Docker là gì?

Docker is an open-source platform that automates the deployment of applications inside lightweight, portable containers. -- Docker là một nền tảng mã nguồn mở tự động hóa việc triển khai ứng dụng bên trong các containers nhẹ, di động.

The platform was created to solve the "it works on my machine" problem. -- Nền tảng này được tạo ra để giải quyết vấn đề "nó chạy trên máy tôi".

**Key Benefits -- Lợi ích Chính:**
- Consistent environments -- Môi trường nhất quán
- Faster deployment -- Triển khai nhanh hơn
- Better resource utilization -- Sử dụng tài nguyên tốt hơn
- Simplified dependency management -- Quản lý dependencies đơn giản hơn

### Core Concepts -- Khái niệm Cốt lõi

#### Image -- Image

An image is a read-only template that contains instructions for creating a container. -- Image là một template chỉ-đọc chứa các hướng dẫn để tạo container.

Images are built from a Dockerfile and stored in a registry. -- Images được build từ Dockerfile và lưu trữ trong registry.

**Properties -- Thuộc tính:**
- Immutable and versioned -- Bất biến và có phiên bản
- Layered file system -- Hệ thống file nhiều lớp
- Shareable across teams -- Có thể chia sẻ giữa các teams

#### Container -- Container

A container is a runnable instance of an image. -- Container là một instance có thể chạy của image.

Containers are isolated from each other but share the OS kernel. -- Containers được cô lập với nhau nhưng chia sẻ OS kernel.

**Lifecycle -- Vòng đời:**
1. Create -- Tạo
2. Start -- Khởi động
3. Stop -- Dừng
4. Remove -- Xóa

## Installation -- Cài đặt

### Prerequisites -- Yêu cầu Tiên quyết

Before installing Docker, ensure your system meets these requirements. -- Trước khi cài đặt Docker, đảm bảo hệ thống đáp ứng các yêu cầu sau.

**System Requirements -- Yêu cầu Hệ thống:**
- 64-bit operating system -- Hệ điều hành 64-bit
- Minimum 4GB RAM -- Tối thiểu 4GB RAM
- Virtualization support enabled -- Hỗ trợ ảo hóa được bật

### Ubuntu Installation -- Cài đặt trên Ubuntu

```bash
# Update package index -- Cập nhật package index
sudo apt update

# Install dependencies -- Cài đặt dependencies
sudo apt install apt-transport-https ca-certificates curl

# Add Docker GPG key -- Thêm Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Install Docker -- Cài đặt Docker
sudo apt install docker-ce docker-ce-cli containerd.io
```

## Best Practices -- Thực hành Tốt nhất

### Image Optimization -- Tối ưu hóa Image

Use multi-stage builds to reduce image size. -- Sử dụng multi-stage builds để giảm kích thước image.

```dockerfile
# Build stage -- Giai đoạn Build
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage -- Giai đoạn Production
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["node", "server.js"]
```
```

## 📊 Quick Reference -- Tham khảo Nhanh

### Format Patterns -- Các Pattern Format

| Case | Format | Example |
|------|--------|---------|
| Term không cần dịch | `Term (English explanation -- Dịch Việt)` | `Docker (Container Platform -- Nền tảng Container)` |
| Term cần dịch | `English -- Tiếng Việt` | `Installation -- Cài đặt` |
| Câu nội dung | `English sentence. -- Câu tiếng Việt.` | `Linux is... -- Linux là...` |
| List item | `English -- Tiếng Việt` | `Fast deployment -- Triển khai nhanh` |
| Code comment | `# English -- Tiếng Việt` | `# Configuration -- Cấu hình` |
| File name | `english-name.md` | `docker-commands.md` |

### Decision Tree -- Cây Quyết định

```
Heading?
├─ Proper noun (Docker, Kubernetes)?
│  └─ YES → Term (English explanation -- Dịch Việt)
│           Example: Docker (Container Platform -- Nền tảng Container)
│
└─ Common term (Installation, Configuration)?
   └─ YES → English -- Tiếng Việt
            Example: Installation -- Cài đặt
```

## ✅ Remember -- Nhớ

1. **`--`** is for Vietnamese translation -- `--` dùng cho dịch tiếng Việt
2. **`()`** is for English explanation -- `()` dùng cho bổ nghĩa tiếng Anh
3. **Always English first** -- Luôn tiếng Anh trước
4. **Be consistent** -- Nhất quán

---

**Apply consistently across the entire Knowledge Base! -- Áp dụng nhất quán trong toàn bộ Knowledge Base!**
