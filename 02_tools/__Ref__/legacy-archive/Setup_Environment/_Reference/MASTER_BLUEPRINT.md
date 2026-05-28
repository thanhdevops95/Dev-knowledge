# 🏛️ ĐẶC TẢ GIÁO TRÌNH: DEVOPS MASTERY (MASTER BLUEPRINT)

> **Tài liệu này là kim chỉ nam cho toàn bộ nội dung khóa học**

---

## 1. NGUYÊN TẮC CỐT LÕI

Mọi nội dung trong khóa học phải tuân thủ các nguyên tắc sau:

### 1.1. Ngôn ngữ

- **Tiếng Việt** là ngôn ngữ chính
- Phong cách **trực diện, gãy gọn, không văn hoa** ("No fluff")
- Code, commands, tool names giữ nguyên tiếng Anh (vd: `git push`, `docker build`)
- Technical terms khi xuất hiện lần đầu phải giải thích:

```
CI (Continuous Integration - Tích hợp liên tục)
```

### 1.2. Phương pháp Ẩn dụ (Metaphor)

Mỗi khái niệm trừu tượng **BẮT BUỘC** có ví dụ so sánh đời thường:

> **Docker Container** giống như **hộp cơm trưa**. Bạn nấu ở nhà (Dev), đóng hộp lại, mang lên công ty (Server) mở ra ăn thì vị vẫn y hệt.

### 1.3. Dự án xuyên suốt: "The Counter App"

- **Frontend**: HTML/CSS đơn giản
- **Backend**: Python Flask
- **Database**: Redis
- **Tính năng**: Đếm số, reset, lưu persistent

### 1.4. Format chuẩn

Mỗi module có **4 files**:

- `REQUIREMENT.md` - Đề bài, mục tiêu, checklist
- `README.md` - Lý thuyết + Ẩn dụ + Mermaid diagrams
- `LABS.md` - Thực hành step-by-step
- `SCENARIOS.md` - tình huống thực chiến

---

## 2. CẤU TRÚC THƯ MỤC

```
DevOps-Mastery/
├── README.md                      # Landing page
├── MASTER_BLUEPRINT.md            # File này
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
│
├── 00_INTRODUCTION/               # Giới thiệu & Setup
├── 01_LINUX/                      # Linux Fundamentals
├── 02_NETWORKING/                 # Networking Basics
├── 03_SCRIPTING/                  # Shell & Python
├── 04_GIT/                        # Version Control
├── 05_WEB_SERVERS/                # NGINX, Apache
├── 06_DATABASES/                  # SQL, NoSQL, Redis
├── 07_DOCKER/                     # Containerization
├── 08_CI/                         # Continuous Integration
├── 09_KUBERNETES/                 # Container Orchestration
├── 10_CD/                         # Continuous Deployment
├── 11_CLOUD/                      # AWS, GCP, Azure
├── 12_IAC/                        # Terraform, Ansible
├── 13_SECURITY/                   # DevSecOps
├── 14_OBSERVABILITY/              # Monitoring & Logging
├── 15_SRE/                        # Site Reliability Engineering
│
├── CAPSTONE_PROJECT/              # Dự án cuối khóa
├── APPENDIX/                      # Nội dung nâng cao
├── RESOURCES/                     # Tài nguyên bổ sung
├── scripts/                       # Setup scripts
└── source-code/                   # Counter App
```

---

## 3. CHI TIẾT 15 MODULES

| # | Module | Nội dung | Ẩn dụ |
|---|--------|----------|-------|
| 00 | INTRODUCTION | DevOps, Agile, Setup | Đầu bếp + Bồi bàn |
| 01 | LINUX | CLI, Permissions, Services | Nền móng ngôi nhà |
| 02 | NETWORKING | TCP/IP, DNS, HTTP, Firewall | Hệ thống đường giao thông |
| 03 | SCRIPTING | Bash, Python, Automation | Viết công thức nấu ăn |
| 04 | GIT | Version control, Workflow | Google Docs + Version history |
| 05 | WEB_SERVERS | NGINX, Load Balancing, SSL | Lễ tân khách sạn |
| 06 | DATABASES | SQL, NoSQL, Redis | Kho lưu trữ hàng hóa |
| 07 | DOCKER | Containers, Compose | Hộp cơm trưa |
| 08 | CI | GitHub Actions, Testing | Dây chuyền kiểm tra nhà máy |
| 09 | KUBERNETES | Pods, Services, Deployments | Bến cảng container |
| 10 | CD | GitOps, ArgoCD, Strategies | Hệ thống giao hàng tự động |
| 11 | CLOUD | AWS, GCP, Serverless | Thuê nhà vs Mua nhà |
| 12 | IAC | Terraform, Ansible | Robot xây dựng tự động |
| 13 | SECURITY | DevSecOps, Vault, Scanning | Hệ thống an ninh tòa nhà |
| 14 | OBSERVABILITY | Prometheus, Grafana, Logs | Bảng điều khiển máy bay |
| 15 | SRE | Incidents, Post-mortem | Đội cứu hỏa + Họp rút kinh nghiệm |

---

## 4. QUY ĐỊNH NỘI DUNG TỪNG FILE

### A. REQUIREMENT.md (Đề bài)

```markdown
# Module XX: TÊN MODULE

## 🎯 Mục tiêu
Sau khi hoàn thành module này, bạn sẽ:
- [Danh sách mục tiêu]

## 📚 Thuật ngữ
| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| ... | ... | ... |

## ✅ Checklist bài tập
- [ ] Lab 1: ...
- [ ] Lab 2: ...

## 🚨 Checklist tình huống
- [ ] Scenario 1: ...
- [ ] Scenario 2: ...

## ⏱️ Thời lượng
Ước tính: X-Y giờ
```

### B. README.md (Lý thuyết)

```markdown
# Module XX: TÊN MODULE

## 🎯 Tổng quan
[Giải thích + Ẩn dụ]

## 📖 Nội dung

### 1. Khái niệm A
[Giải thích + Ẩn dụ + Diagram]

### 2. Khái niệm B
...

## 🔗 Tài liệu tham khảo
```

### C. LABS.md (Thực hành)

```markdown
# Labs: Module XX

## Lab 1: Tên Lab

### Mục tiêu
[Mục tiêu cụ thể]

### Bước 1: ...
[Hướng dẫn chi tiết + Code có comment]

### Expected Output
[Kết quả mong đợi]
```

### D. SCENARIOS.md (Tình huống thực chiến)

```markdown
# Scenarios: Module XX

## Scenario 1: Tên tình huống

### 🚨 Bối cảnh
[Mô tả triệu chứng lỗi]

### 🕵️ Điều tra
[Dùng công cụ gì để tìm nguyên nhân?]

### 💡 Giải pháp
[Cách sửa lỗi]

### 🧠 Bài học
[Rút kinh nghiệm]
```

---

## 5. QUY TẮC ĐẶT TÊN

| Loại | Quy tắc | Ví dụ |
|------|---------|-------|
| Thư mục Module | `XX_TÊN` | `01_LINUX`, `02_NETWORKING` |
| Files trong Module | `TÊN.md` (CAPS) | `README.md`, `LABS.md` |
| Scripts | `tên-action.sh` | `setup-linux.sh` |
| Thư mục khác | `lowercase` hoặc `CAPS` | `scripts/`, `RESOURCES/` |

---

## 6. THỜI LƯỢNG ƯỚC TÍNH

| Module | Thời lượng |
|--------|------------|
| 00. INTRODUCTION | 2-3 giờ |
| 01. LINUX | 6-8 giờ |
| 02. NETWORKING | 4-6 giờ |
| 03. SCRIPTING | 6-8 giờ |
| 04. GIT | 4-6 giờ |
| 05. WEB_SERVERS | 4-6 giờ |
| 06. DATABASES | 4-6 giờ |
| 07. DOCKER | 8-10 giờ |
| 08. CI | 6-8 giờ |
| 09. KUBERNETES | 10-12 giờ |
| 10. CD | 6-8 giờ |
| 11. CLOUD | 8-10 giờ |
| 12. IAC | 8-10 giờ |
| 13. SECURITY | 4-6 giờ |
| 14. OBSERVABILITY | 6-8 giờ |
| 15. SRE | 4-6 giờ |
| CAPSTONE | 20-30 giờ |
| **TỔNG** | **~110-150 giờ** |

---

## 7. ICONS & EMOJI CHUẨN

| Emoji | Ý nghĩa |
|-------|---------|
| 🎯 | Mục tiêu |
| 📖 | Lý thuyết |
| 💡 | Gợi ý / Giải pháp |
| ⚠️ | Cảnh báo |
| 🚨 | Lỗi / Sự cố |
| ✅ | Hoàn thành / Đúng |
| ❌ | Sai / Không nên |
| 🔧 | Thực hành / Tools |
| 🧠 | Bài học rút ra |
| 📝 | Ghi chú |
| 🕵️ | Điều tra |
| ⏱️ | Thời gian |
| 🔗 | Link tham khảo |

---

## 8. NGUYÊN TẮC VIẾT CODE

```python
# ✅ TỐT: Code có comment giải thích
def get_counter():
    """Lấy giá trị counter từ Redis"""
    redis_client = redis.Redis(host='redis', port=6379)  # Kết nối Redis
    count = redis_client.get('counter')  # Lấy giá trị
    return int(count) if count else 0    # Trả về 0 nếu chưa có

# ❌ XẤU: Code không comment
def get_counter():
    r = redis.Redis(host='redis', port=6379)
    c = r.get('counter')
    return int(c) if c else 0
```

---

**Tài liệu này sẽ được cập nhật khi cần thiết.**

*Phiên bản: 1.0*
*Cập nhật: 2024-12-22*
