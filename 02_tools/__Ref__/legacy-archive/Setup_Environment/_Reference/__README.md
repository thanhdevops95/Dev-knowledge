# Module 00: Introduction - Chào mừng đến với DevOps

---

# 📚 Bảng thuật ngữ

Trước khi bắt đầu, hãy làm quen với các thuật ngữ quan trọng:

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **DevOps** | /ˌdevˈɒps/ | Dev + Ops - Văn hóa kết hợp phát triển và vận hành |
| **CI/CD** | - | Continuous Integration / Continuous Delivery - Tích hợp và triển khai liên tục |
| **Automation** | - | Tự động hóa - Máy làm thay công việc lặp lại |
| **Pipeline** | - | Đường ống - Quy trình tự động từ code đến production |
| **Deploy** | - | Triển khai - Đưa ứng dụng lên server |
| **Production** | - | Môi trường thực tế phục vụ người dùng |
| **Container** | - | Đóng gói ứng dụng và dependencies |
| **Orchestration** | - | Điều phối - Quản lý nhiều containers |
| **Infrastructure** | - | Hạ tầng - Servers, networks, storage |
| **Monitoring** | - | Giám sát - Theo dõi trạng thái hệ thống |
| **Scaling** | - | Mở rộng - Tăng tài nguyên khi cần |
| **SLA** | - | Service Level Agreement - Cam kết chất lượng dịch vụ |

---

## 🎬 Tại sao bạn ở đây?

Có thể bạn là:

- **Developer** nghe đồng nghiệp nói về "CI/CD", "Docker", "Kubernetes" và muốn hiểu
- **System Admin** muốn học automation thay vì làm thủ công mỗi ngày
- **Sinh viên IT** chuẩn bị cho sự nghiệp trong thời đại cloud
- **Người tò mò** muốn biết làm sao Netflix serve 200 triệu users mà không sập

Dù bạn là ai, bạn đến đúng nơi rồi.

---

## 📖 DevOps là gì? - Giải thích như đang nói với bạn bè

### Câu chuyện trước khi có DevOps

Hãy tưởng tượng bạn làm việc ở một công ty phần mềm năm 2005:

**Đội Development (Dev):**

- Viết code mới
- Test trên máy của họ: "Chạy tốt!"
- Đóng gói code, gửi cho đội Operations

**Đội Operations (Ops):**

- Nhận code từ Dev
- Deploy lên server production
- **Server sập!** 💥
- Ops: "Code của các anh có bug!"
- Dev: "Máy em chạy tốt mà? Chắc server các anh có vấn đề!"

**Kết quả:** Hai đội đổ lỗi cho nhau. Bug mất weeks để fix. Users không vui.

```
┌─────────────┐         ┌─────────────┐
│     DEV     │   😤    │     OPS     │
│   "Code OK" │◄───────►│ "Server OK" │
│             │   ⚔️    │             │
└─────────────┘         └─────────────┘
        │                      │
        └──────────┬───────────┘
                   ▼
            💥 PRODUCTION DOWN 💥
```

### DevOps ra đời để giải quyết vấn đề này

**DevOps = Dev + Ops làm việc CÙNG NHAU**

Không phải là một công cụ. Không phải là một chức danh. DevOps là **văn hóa làm việc** mà ở đó:

1. **Dev và Ops là một team** - Cùng chịu trách nhiệm từ code đến production
2. **Automation mọi thứ** - Không làm thủ công những việc lặp lại
3. **Feedback nhanh** - Biết lỗi trong minutes, không phải weeks
4. **Cải tiến liên tục** - Luôn tìm cách làm tốt hơn

```
┌─────────────────────────────────────────┐
│              DevOps Team                │
│                                         │
│   👨‍💻 Dev ←───→ 🔧 Ops ←───→ 🔒 Security │
│              │                          │
│              ▼                          │
│         🚀 Automation                   │
│              │                          │
│              ▼                          │
│      ⚡ Deploy 10x/day                  │
│   (thay vì 1x/month)                    │
└─────────────────────────────────────────┘
```

### Ẩn dụ dễ hiểu nhất

**DevOps giống như một nhà hàng hiện đại:**

| Trước DevOps | Với DevOps |
|--------------|------------|
| Bếp nấu xong ném đĩa qua cửa sổ | Bếp và phục vụ làm việc cùng nhau |
| Phục vụ không biết món gồm gì | Phục vụ hiểu món để tư vấn khách |
| Lỗi → Đổ lỗi nhau | Lỗi → Cùng tìm cách fix |
| Khách phải đợi 1 tiếng | Khách có đồ trong 15 phút |

---

## 🔄 Vòng đời DevOps

DevOps không phải là một bước, mà là **vòng lặp liên tục**:

```
        ┌──────────────────────────────────────┐
        │             DEVOPS LOOP               │
        │                                       │
   ┌────▼────┐                           ┌─────┴─────┐
   │  PLAN   │                           │  MONITOR  │
   │ Lên kế  │                           │ Theo dõi  │
   │ hoạch   │                           │ production│
   └────┬────┘                           └─────▲─────┘
        │                                      │
   ┌────▼────┐                           ┌─────┴─────┐
   │  CODE   │                           │  OPERATE  │
   │ Viết    │                           │ Vận hành  │
   │ code    │                           │ hệ thống  │
   └────┬────┘                           └─────▲─────┘
        │                                      │
   ┌────▼────┐                           ┌─────┴─────┐
   │  BUILD  │                           │  DEPLOY   │
   │ Đóng    │                           │ Triển     │
   │ gói     │                           │ khai      │
   └────┬────┘                           └─────▲─────┘
        │                                      │
   ┌────▼────┐                           ┌─────┴─────┐
   │  TEST   │───────────────────────────►  RELEASE  │
   │ Kiểm    │                           │ Phát      │
   │ thử     │                           │ hành      │
   └─────────┘                           └───────────┘
```

**Giải thích từng bước:**

1. **PLAN** - Lên kế hoạch feature mới, fix bug
2. **CODE** - Developer viết code
3. **BUILD** - Compile, đóng gói thành artifact
4. **TEST** - Chạy automated tests
5. **RELEASE** - Chuẩn bị phiên bản mới
6. **DEPLOY** - Đưa lên production
7. **OPERATE** - Vận hành, scale khi cần
8. **MONITOR** - Theo dõi performance, errors
9. **Feedback** - Thông tin từ Monitor quay lại Plan

**Điểm quan trọng:** Vòng này chạy **liên tục**, có thể nhiều lần/ngày.

---

## 🛠️ DevOps Engineer làm gì?

### Công việc hàng ngày

**Buổi sáng:**

```
08:00 - Check alerts đêm qua (nếu có)
08:30 - Review CI/CD pipelines - có build nào fail không?
09:00 - Standup meeting với team
09:30 - Làm task: viết Terraform cho infrastructure mới
```

**Buổi chiều:**

```
13:00 - Debug tại sao deployment bị chậm
14:30 - Code review Dockerfile của đồng nghiệp
15:30 - Update Kubernetes configs
16:30 - Viết documentation
```

**Đột xuất:**

```
🚨 Alert: Production CPU > 90%
→ Điều tra nguyên nhân
→ Scale up hoặc fix code
→ Viết postmortem
```

### Skills cần có

```
┌─────────────────────────────────────────────────────┐
│                  DevOps Skills Tree                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  [Nền tảng - Học trước]                             │
│  ├── Linux/Bash ⭐⭐⭐⭐⭐                            │
│  ├── Networking basics ⭐⭐⭐⭐                       │
│  └── Git ⭐⭐⭐⭐⭐                                   │
│                                                      │
│  [Core DevOps - Học tiếp]                           │
│  ├── Docker ⭐⭐⭐⭐⭐                                │
│  ├── CI/CD (GitHub Actions) ⭐⭐⭐⭐                 │
│  └── Web Servers (Nginx) ⭐⭐⭐                      │
│                                                      │
│  [Advanced - Học sau]                               │
│  ├── Kubernetes ⭐⭐⭐⭐⭐                            │
│  ├── Cloud (AWS/GCP) ⭐⭐⭐⭐                        │
│  ├── Infrastructure as Code (Terraform) ⭐⭐⭐⭐     │
│  └── Monitoring (Prometheus/Grafana) ⭐⭐⭐          │
│                                                      │
│  ⭐ = Độ quan trọng                                 │
└─────────────────────────────────────────────────────┘
```

---

## 📚 Khóa học này dạy gì?

### 16 Modules từ Zero đến Production

| # | Module | Học gì | Tại sao cần |
|---|--------|--------|-------------|
| 00 | Introduction | **Bạn đang ở đây** | Hiểu big picture |
| 01 | Linux | Terminal, commands | 90% servers là Linux |
| 02 | Networking | TCP/IP, DNS, HTTP | Debug network issues |
| 03 | Scripting | Bash, Python | Automation |
| 04 | Git | Version control | Làm việc với code |
| 05 | Web Servers | Nginx | Serve websites |
| 06 | Databases | SQL, Redis | Lưu trữ data |
| 07 | Docker | Containers | Package apps |
| 08 | CI | GitHub Actions | Automate build/test |
| 09 | Kubernetes | Container orchestration | Scale apps |
| 10 | CD | Deployment strategies | Release safely |
| 11 | Cloud | AWS/GCP | Production infrastructure |
| 12 | IaC | Terraform | Infra as code |
| 13 | Security | DevSecOps | Bảo mật |
| 14 | Observability | Monitoring, logging | Biết khi có vấn đề |
| 15 | SRE | Reliability | Keep systems running |

### Dự án xuyên suốt: The Counter App

Thay vì học lý thuyết khô khan, bạn sẽ **xây dựng và deploy một app thực tế** qua từng module.

**Counter App đơn giản:**

- Một nút bấm tăng số
- Số được lưu vào database
- Được deploy lên production

**Nhưng bạn sẽ học:**

- Viết code → Đóng gói Docker → CI/CD → Deploy Kubernetes → Monitoring

```
┌─────────────────────────────────────────────────────┐
│                    COUNTER APP                       │
├─────────────────────────────────────────────────────┤
│                                                      │
│                    [ 42 ]                            │
│                                                      │
│            [+1]    [+10]    [Reset]                 │
│                                                      │
├─────────────────────────────────────────────────────┤
│  Frontend: HTML/CSS                                  │
│  Backend: Python Flask                               │
│  Database: Redis                                     │
│  Infra: Docker → K8s → AWS                          │
└─────────────────────────────────────────────────────┘
```

---

## 💻 Chuẩn bị môi trường học tập

### Yêu cầu máy tính

| Thành phần | Tối thiểu | Khuyến nghị |
|------------|-----------|-------------|
| **OS** | Windows 10, macOS 10.15, Ubuntu 20.04 | Windows 11, macOS 13+, Ubuntu 22.04 |
| **RAM** | 8GB | 16GB |
| **Disk** | 30GB trống | 50GB trống |
| **CPU** | 4 cores | 8 cores |
| **Internet** | Ổn định | Tốc độ tốt |

### Tài khoản cần tạo (Miễn phí)

**Bước 1: GitHub** - Nơi lưu code

1. Vào [github.com](https://github.com)
2. Đăng ký tài khoản
3. Nhớ username và password

**Bước 2: Docker Hub** - Nơi lưu container images

1. Vào [hub.docker.com](https://hub.docker.com)
2. Đăng ký với cùng email

**Bước 3 (Optional): AWS Free Tier** - Cloud platform

1. Vào [aws.amazon.com/free](https://aws.amazon.com/free)
2. Đăng ký (cần credit card nhưng không charge)
3. Sẽ dùng ở modules sau

### Cài đặt tools

**Windows:**

```powershell
# 1. Cài WSL2 (Linux trong Windows)
wsl --install

# 2. Restart máy

# 3. Cài Windows Terminal (từ Microsoft Store)

# 4. Chạy script setup
# Clone repo về và chạy scripts/setup-windows.ps1
```

**macOS:**

```bash
# 1. Cài Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Chạy script setup
bash scripts/setup-mac.sh
```

**Linux (Ubuntu):**

```bash
# Chạy script setup
bash scripts/setup-linux.sh
```

### Kiểm tra cài đặt

Sau khi setup, chạy:

```bash
bash scripts/verify-tools.sh
```

**Output mong đợi:**

```
✅ git: version 2.40.0
✅ docker: version 24.0.0
✅ kubectl: version v1.28.0
✅ terraform: version 1.6.0
...
All tools installed successfully!
```

---

## 🎓 Phương pháp học hiệu quả

### Quy trình 3 bước cho mỗi module

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   1. LÝ     │     │   2. THỰC   │     │   3. THỰC   │
│   THUYẾT    │ ──► │   HÀNH      │ ──► │   CHIẾN    │
│             │     │             │     │             │
│  README.md  │     │  LABS.md    │     │ SCENARIOS   │
│             │     │             │     │    .md      │
│  Hiểu khái  │     │  Làm theo   │     │  Xử lý     │
│  niệm       │     │  từng bước  │     │  tình huống │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Tips học

1. **Đừng skip Labs** - DevOps = practical skill. Đọc không thì không nhớ.

2. **Type, đừng copy-paste** - Gõ commands giúp nhớ lâu hơn.

3. **Break things on purpose** - Học từ lỗi. Tạo bug để học fix.

4. **Hỏi khi không hiểu** - Google, Stack Overflow, hoặc AI chatbots.

5. **Ghi chép** - Viết lại bằng ngôn ngữ của bạn.

### Thời gian dự kiến

| Pace | Thời gian/tuần | Hoàn thành khóa |
|------|----------------|-----------------|
| Casual | 5 giờ | 6-8 tháng |
| Part-time | 10 giờ | 3-4 tháng |
| Intensive | 20+ giờ | 6-8 tuần |

---

## 🗺️ Lộ trình tiếp theo

Bạn đã hiểu DevOps là gì và khóa học này dạy gì.

**Bước tiếp theo:** Bắt đầu với nền tảng quan trọng nhất - Linux!

👉 **[Module 01: Linux Fundamentals](../01_LINUX/README.md)**

---

## 💬 Quote để nhớ

> *"DevOps is not a goal, but a never-ending process of continual improvement."*
> — Jez Humble

> *"The only way to go fast is to go well."*
> — Robert C. Martin

Chúc bạn học vui! 🚀
