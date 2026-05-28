# Module 00: SETUP - Chuẩn bị môi trường DevOps

> **Thời gian học:** Linh hoạt (1-3 ngày tùy background)
>
> **Prerequisite:** Không có - Module này dành cho beginners
>
> **Difficulty:** ⭐☆☆☆☆

---

## 📋 Mục lục

1. [Giới thiệu DevOps](#1-giới-thiệu-devops)
2. [Tại sao cần môi trường Linux?](#2-tại-sao-cần-môi-trường-linux)
3. [Công cụ cần thiết](#3-công-cụ-cần-thiết)
4. [Hướng dẫn Setup Windows](#4-hướng-dẫn-setup-windows)
5. [Hướng dẫn Setup macOS](#5-hướng-dẫn-setup-macos)
6. [Hướng dẫn Setup Linux Native](#6-hướng-dẫn-setup-linux-native)
7. [Tài khoản cần tạo](#7-tài-khoản-cần-tạo)
8. [Verification & Testing](#8-verification--testing)
9. [Troubleshooting](#9-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **DevOps là gì** và tại sao nó quan trọng
- ✅ Thiết lập được **môi trường Linux** trên Windows/macOS/Linux
- ✅ Cài đặt và cấu hình **Terminal, VS Code, Git**
- ✅ Tạo các **tài khoản cần thiết** (GitHub, Docker Hub)
- ✅ Verify môi trường với **automation scripts**
- ✅ Tự tin **troubleshoot** các vấn đề setup phổ biến

---

## 1. Giới thiệu DevOps

### 1.1. DevOps là gì?

#### Định nghĩa

**DevOps** = **Dev**elopment (Phát triển) + **Op**eration**s** (Vận hành)

DevOps là một **triết lý, văn hóa và tập hợp practices** nhằm:

- Phá bỏ "bức tường" giữa team Dev và Ops
- Tự động hóa toàn bộ software delivery lifecycle
- Giao phần mềm nhanh hơn, tin cậy hơn, an toàn hơn

**Không phải:**

- ❌ Một công cụ cụ thể (Docker, Kubernetes...)
- ❌ Một job title (dù có "DevOps Engineer")
- ❌ "Làm cả Dev lẫn Ops"

**Mà là:**

- ✅ Culture: Collaboration thay vì siloed teams
- ✅ Automation: CI/CD pipelines thay vì manual deployment
- ✅ Measurement: Metrics, monitoring, feedback loops

#### Lịch sử ra đời

**2000s - Vấn đề "Dev vs Ops":**

```
Developer team:                Operations team:
"Em code xong rồi!"           "Sao deploy lên server nó lỗi?"
"Trên máy em chạy ngon mà!"   "Bạn cài dependency gì vậy?"
"Tính năng mới, ship luôn!"   "Chưa test stability, đợi!"
```

**Hệ quả:**

- Release cycle **chậm** (hàng tháng, thậm chí hàng quý)
- Deploy **thường xuyên fail**
- Blame culture: "Lỗi của team kia!"

**2007-2009 - Phong trào DevOps:**

- Patrick Debois (2009): Tổ chức "DevOpsDays" đầu tiên tại Bỉ
- John Allspaw & Paul Hammond (Flickr): "10+ Deploys Per Day: Dev and Ops Cooperation"
- Idea: **Automation + Collaboration = Faster & Safer releases**

**2010s - Bùng nổ:**

- Docker (2013): Containerization mainstream
- Kubernetes (2014): Container orchestration
- Cloud providers (AWS, GCP, Azure): Infra as code
- CI/CD tools: Jenkins, GitLab CI, GitHub Actions

**2020s - Hiện tại:**

- DevSecOps: Tích hợp security từ đầu
- GitOps: Git as single source of truth
- Platform Engineering: Internal developer platforms

#### Vấn đề DevOps giải quyết

**Trước DevOps:**

| Vấn đề | Mô tả | Hệ quả |
|--------|-------|--------|
| **Slow releases** | Deploy 1 tháng/lần hoặc chậm hơn | Tính năng đến tay users quá chậm |
| **Manual processes** | Deploy bằng tay: SSH vào server, copy files, restart... | Lỗi human error, không reproducible |
| **"Works on my machine"** | Dev: "Trên máy tôi chạy được!" <br> Ops: "Lên server lỗi!" | Mất thời gian debug env differences |
| **Siloed teams** | Dev và Ops không nói chuyện với nhau | Lack of ownership, blame game |
| **No visibility** | Không biết app đang chạy thế nào production | Discover issues quá muộn |

**Sau DevOps:**

| Giải pháp | Cách thức | Kết quả |
|-----------|-----------|---------|
| **Continuous Delivery** | CI/CD pipelines tự động build, test, deploy | Deploy multiple times/ngày |
| **Automation** | Infrastructure as Code, automated testing | Reproducible, reliable |
| **Containerization** | Docker: đóng gói app + dependencies | "Works on my machine" = "Works everywhere" |
| **Collaboration** | Shared ownership, ChatOps | Faster problem-solving |
| **Observability** | Monitoring, logging, alerting | Catch issues early |

#### So sánh: Traditional vs DevOps

```
TRADITIONAL WATERFALL:
┌─────────────────────────────────────────────┐
│  Plan → Design → Develop → Test → Deploy   │
│  (6-12 tháng)                      ↓        │
│                                Operations   │
│                             (maintain, fix) │
└─────────────────────────────────────────────┘

DEVOPS CONTINUOUS:
    ┌──────────────────────────────────────┐
    │  Plan → Code → Build → Test          │
    │    ↑                         ↓        │
    │  Monitor ← Operate ← Deploy ← Release│
    └──────────────────────────────────────┘
         (Infinite loop, hàng ngày)
```

### 1.2. Tại sao học DevOps?

#### Market Demand

**Thống kê việc làm (2024):**

- **Remote DevOps jobs:** Tăng 300% so với 2019
- **Median salary:**
  - Junior DevOps (VN): 15-25 triệu/tháng
  - Mid-level (VN): 25-45 triệu/tháng
  - Senior (VN): 45-80+ triệu/tháng
  - US/EU: $80,000 - $180,000/năm

**Top companies tuyển:**

- Tech giants: Google, Amazon, Microsoft, Meta
- Startups: Hầu hết startups tech cần DevOps
- Enterprise: Banks, telcos chuyển đổi số
- Remote-first companies

#### Xu hướng Cloud-Native

**Doanh nghiệp đang shift:**

```
On-premise servers → Cloud (AWS/GCP/Azure)
Manual deploys → CI/CD pipelines
Monolith → Microservices
VMs → Containers → Kubernetes
```

**Impact:**

- Demand for DevOps skills **tăng vọt**
- DevOps Engineer = One of most in-demand roles
- Skill gap: Nhiều jobs, ít người đủ skill

#### Career Path

**DevOps là hub kết nối nhiều roles:**

```
         ┌─────────────────┐
         │   DevOps Eng    │
         └────────┬────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
┌────▼───┐   ┌───▼────┐  ┌───▼──────┐
│  SRE   │   │Platform│  │ Security │
│(Google)│   │Engineer│  │ Engineer │
└────────┘   └────────┘  └──────────┘
```

**Roadmap:**

1. **Junior DevOps:** CI/CD, Docker, cloud basics
2. **Mid-level:** Kubernetes, Terraform, monitoring
3. **Senior:** Architecture, multi-cloud, mentoring
4. **Staff/Principal:** Strategy, tooling decisions
5. **Manager/Lead:** Team leadership

**Hoặc specialize:**

- **SRE** (Site Reliability Engineering): Focus reliability, monitoring
- **Platform Engineer:** Build internal developer platforms
- **DevSecOps:** Security + DevOps

#### Skills transferable

**DevOps skills apply everywhere:**

- Startup: Build infra from scratch
- Enterprise: Modernize legacy systems
- Freelance/Consulting: Help companies adopt DevOps
- Open source: Contribute to tools (Kubernetes, Terraform...)
- Teaching: Tạo courses, write blogs

### 1.3. Roadmap tổng quan

#### Foundation Track (Module này)

**Mục tiêu:** Zero → Junior DevOps

```
00. SETUP ← BẠN ĐANG Ở ĐÂY
    ↓
01. LINUX_BASICS
    ↓
02. GIT_GITHUB
    ↓
03. NETWORKING
    ↓
04. HTML/CSS/JS (để test app)
    ↓
05. DOCKER
    ↓
06. CI/CD (GitHub Actions)
    ↓
07. WEB_SERVERS (NGINX)
    ↓
08. DEPLOYMENT
    ↓
09. MONITORING
    ↓
FINAL PROJECT: Portfolio với full CI/CD
```

**Kết quả:** Deploy & monitor web app lên production

#### Advanced Track (Sau Foundation)

```
10. KUBERNETES
11. TERRAFORM
12. ANSIBLE
13. CLOUD (AWS/GCP)
14. OBSERVABILITY (Prometheus, Grafana)
15. SECURITY
... và nhiều hơn
```

#### Thời gian dự kiến

**Foundation Track:**

- Full-time (8h/ngày): 4-6 tuần
- Part-time (2h/ngày): 3-4 tháng
- Casual (5h/tuần): 6-8 tháng

**Nhớ:** Quan trọng là **consistency**, không phải speed!

### 1.4. Mindset của DevOps Engineer

#### 1. Automation-first thinking

**Philosophy:** "Nếu làm 2 lần → Nên tự động hóa"

**Examples:**

- ❌ Manual: SSH vào server, git pull, restart service
- ✅ Automated: Git push → CI/CD auto deploy

- ❌ Manual: Copy-paste config files giữa servers
- ✅ Automated: Infrastructure as Code (Terraform)

**Quote:**
> "The best DevOps engineer is a lazy engineer" - Tự động hóa mọi thứ để không phải làm lại

#### 2. Failure is normal

**Mindset shift:**

```
Traditional:          DevOps:
❌ "Error = Bad"      ✅ "Error = Learning opportunity"
❌ "Hide failures"    ✅ "Surface failures early"
❌ "Blame culture"    ✅ "Blameless post-mortems"
```

**Practice:**

- Deploy fails? → Fix, learn, improve pipeline
- Server crashes? → Add monitoring, alerts
- Security breach? → Post-mortem, prevent future

**Chaos Engineering:**

- Netflix: Chaos Monkey randomly kills servers
- Purpose: Ensure system resilient to failures
- Mindset: "Break it in testing, not in production"

#### 3. Iterative improvement

**Không cần perfect từ đầu:**

```
Version 1: "Works" ← Start here
    ↓
Version 2: "Works well"
    ↓
Version 3: "Works beautifully"
```

**Example - Deployment evolution:**

1. **V1:** Manual SSH deploy (works, but manual)
2. **V2:** Bash script deploy (better, but still manual trigger)
3. **V3:** CI/CD pipeline (automated on git push)
4. **V4:** Blue-green deployment (zero-downtime)
5. **V5:** Canary deployments (gradual rollout)

**Key:** Ship V1, then iterate!

#### 4. Measure everything

**"You can't improve what you don't measure"**

**DevOps metrics:**

- **Deployment Frequency:** Bao nhiêu lần deploy/ngày?
- **Lead Time:** Từ code → production mất bao lâu?
- **MTTR** (Mean Time To Recovery): Fix incident mất bao lâu?
- **Change Failure Rate:** % deploys gây lỗi?

**Tools:**

- Application: Response time, error rate
- Infrastructure: CPU, memory, disk usage
- Business: User engagement, revenue impact

#### 5. You build it, you run it

**Ownership principle:**

```
Traditional:
Dev: "Tôi viết code, Ops lo deploy"
Ops: "Code lỗi, không phải lỗi infra!"

DevOps:
Team: "Chúng tôi build feature,
       chúng tôi deploy,
       chúng tôi monitor,
       chúng tôi on-call khi có incident"
```

**Benefits:**

- Developers care about prod stability
- Faster feedback loops
- Better monitoring/logging

#### 6. Documentation as code

**Treat docs like code:**

- Version controlled (Git)
- Reviewed (Pull Requests)
- Tested (ensure commands work)
- Automated (generate from code)

**Examples:**

- README.md for every repo
- Architecture diagrams (as code: Mermaid, PlantUML)
- Runbooks for incidents
- API docs (auto-generated: Swagger)

---

## 2. Tại sao cần môi trường Linux?

### 2.1. Windows vs Linux trong DevOps

#### Thực tế production servers

**Thống kê:**

- **~95%** production servers chạy Linux (hoặc Unix-based)
- **~5%** Windows Server (chủ yếu legacy enterprise)

**Major cloud providers:**

```
AWS EC2 instances:
├── 92% Linux (Amazon Linux, Ubuntu, RHEL...)
└── 8% Windows Server

Google Cloud VMs:
├── 94% Linux
└── 6% Windows

Azure VMs:
├── 70% Linux (Microsoft công bố 2019)
└── 30% Windows
```

**Why Linux dominates:**

1. **Free & Open Source:** Không license fees
2. **Stability:** Uptime hàng năm không reboot
3. **Performance:** Lightweight, fast
4. **Security:** Ít malware hơn Windows
5. **Customization:** Control mọi aspect của OS
6. **Tooling:** DevOps tools built for Linux first

#### DevOps tools ecosystem

**Tools được design cho Linux:**

| Category | Tools | Linux Support |
|----------|-------|---------------|
| **Container** | Docker, Kubernetes | Native Linux |
| **Config Mgmt** | Ansible, Chef, Puppet | Linux-first |
| **CI/CD** | Jenkins, GitLab CI | Runs on Linux |
| **Monitoring** | Prometheus, Grafana | Linux-native |
| **Cloud** | AWS CLI, gcloud, az | Best on Linux |

**Windows support:**

- Có, nhưng often **secondary**
- Performance thường **kém hơn** Linux
- Community support **nhỏ hơn**

**Kết luận:** Learn Linux = Learn ngôn ngữ của DevOps

#### Performance comparison

**Container performance:**

```
Windows Containers:
- Chỉ chạy trên Windows Server
- Image size: 1-5 GB (base image lớn)
- Startup time: 5-15 giây

Linux Containers:
- Chạy mọi nơi (Linux, macOS, Windows+WSL)
- Image size: 5-100 MB (Alpine base)
- Startup time: < 1 giây
```

**Why difference?**

- Linux containers share kernel với host
- Windows containers cần Windows kernel → overhead lớn

**Example:**

```bash
# Alpine Linux image
docker pull alpine
# Size: ~5 MB

# Windows Server Core image  
docker pull mcr.microsoft.com/windows/servercore
# Size: ~3.5 GB

# Gấp 700 lần!
```

### 2.2. WSL2 là gì?

#### Windows Subsystem for Linux (WSL)

**Định nghĩa:**
WSL = Tính năng của Windows cho phép chạy **Linux environment** trực tiếp trên Windows, không cần dual boot hay VM nặng nề.

**WSL1 vs WSL2:**

| Feature | WSL1 | WSL2 |
|---------|------|------|
| **Architecture** | Translation layer | Real Linux kernel |
| **Performance** | Chậm với file I/O | Nhanh (gần native Linux) |
| **Compatibility** | 60-70% Linux tools | 95%+ compatibility |
| **Docker** | Không support tốt | Full support |
| **Released** | 2017 | 2019 |

**WSL2 = Recommended!**

#### Architecture WSL2

**Cách nó hoạt động:**

```
┌───────────────────────────────────────┐
│         Windows 10/11                 │
│  ┌─────────────────────────────────┐  │
│  │         Hyper-V                 │  │
│  │  ┌───────────────────────────┐  │  │
│  │  │   Real Linux Kernel       │  │  │
│  │  │  ┌─────────────────────┐  │  │  │
│  │  │  │  Ubuntu 22.04       │  │  │  │
│  │  │  │  (Your distro)      │  │  │  │
│  │  │  └─────────────────────┘  │  │  │
│  │  └───────────────────────────┘  │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

**Key components:**

1. **Hyper-V:** Windows virtualization technology
2. **Linux Kernel:** Microsoft-maintained, open source
3. **Distro:** Ubuntu, Debian, Fedora... (bạn chọn)

**Benefits:**

- ✅ Real Linux kernel → 100% compatibility
- ✅ Fast: Near-native performance
- ✅ Integrated: Access Windows files from Linux & ngược lại
- ✅ Lightweight: Dùng ít RAM hơn VirtualBox

#### File system integration

**Cross-OS file access:**

```bash
# Từ Linux (WSL), access Windows files:
cd /mnt/c/Users/YourName/Desktop
ls

# Từ Windows, access Linux files:
\\wsl$\Ubuntu\home\username\
```

**Best practices:**

- ✅ Code projects trong Linux filesystem (`~/projects/`)
- ✅ Performance tốt hơn **rất nhiều**
- ❌ Tránh code trong `/mnt/c/` (Windows filesystem from Linux)
- ❌ Chậm do cross-filesystem operations

#### Benchmark: WSL2 vs VirtualBox vs Dual Boot

**File I/O (sequential read/write):**

```
Dual Boot Linux:       ████████████████████ 100%
WSL2:                  ██████████████████░░  90%
VirtualBox:            ████████░░░░░░░░░░░░  40%
WSL1:                  ████░░░░░░░░░░░░░░░░  20%
```

**Docker build time (NextJS app):**

```
Dual Boot:    56 seconds
WSL2:         62 seconds  (+10%)
VirtualBox:   145 seconds (+158%)
Windows native: <varies, slower>
```

**RAM usage (Ubuntu running):**

```
Dual Boot:    0 GB (native OS)
WSL2:         1-2 GB overhead
VirtualBox:   2-4 GB overhead
```

**Verdict:** WSL2 = Best balance cho Windows users!

### 2.3. Alternatives to WSL2

#### Option 1: Dual Boot

**Cách thức:**

- Cài thêm Linux lên 1 partition riêng
- Boot vào Windows hoặc Linux

**Pros:**

- ✅ Native Linux performance (100%)
- ✅ Full control OS
- ✅ Best cho hardcore Linux users

**Cons:**

- ❌ Phải restart để switch OS
- ❌ Cần partition ổ cứng
- ❌ Risk: Newbies có thể xóa nhầm partition Windows

**When to use:**

- Bạn muốn dùng Linux làm daily driver
- Performance tối ưu là must-have
- OK với không dùng Windows apps

#### Option 2: VirtualBox / VMware

**Cách thức:**

- Chạy Linux trong virtual machine trên Windows/macOS

**Pros:**

- ✅ Isolated environment
- ✅ Snapshots: Backup state, rollback khi lỗi
- ✅ Run multiple OS cùng lúc

**Cons:**

- ❌ Performance kém (40-60% native)
- ❌ Nặng: Cần 2-4 GB RAM cho VM
- ❌ Setup phức tạp hơn WSL2
- ❌ Docker performance rất tệ

**When to use:**

- Cần test app trên nhiều OS
- Learn system administration
- Company requires VMs for isolation

#### Option 3: Cloud VM (AWS EC2, GCP, Azure)

**Cách thức:**

- Thuê Linux server trên cloud
- SSH vào để làm việc

**Pros:**

- ✅ Real production-like environment
- ✅ Access từ mọi nơi (có internet)
- ✅ Scalable: Upgrade CPU/RAM dễ dàng

**Cons:**

- ❌ Cost: ~ $5-50/tháng
- ❌ Cần internet connection stable
- ❌ Latency khi SSH (nếu server xa)

**When to use:**

- Máy local yếu (< 4GB RAM)
- Deploy learning: Muốn môi trường giống prod
- Team collaboration: Share server

#### Option 4: macOS Terminal (Native Unix)

**Cách thức:**

- macOS built on Unix (Darwin kernel)
- Terminal = Unix environment native

**Pros:**

- ✅ Native Unix, không cần setup gì thêm
- ✅ Performance tuyệt vời
- ✅ Homebrew = package manager tốt

**Cons:**

- ❌ Không phải Linux (còn differences)
- ❌ Some Linux-specific tools không chạy
- ❌ Đắt: Macbook giá cao

**When to use:**

- Bạn đã có Mac
- OK với ~95% compatibility

#### So sánh tổng hợp

| Factor | WSL2 | Dual Boot | VirtualBox | Cloud VM | macOS |
|--------|------|-----------|------------|----------|-------|
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease of setup** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | Free | Free | Free | $$$ | $$$$$ |
| **Docker support** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Compatibility** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Sugg­estion:**

- **Windows users:** WSL2 (best balance)
- **Want 100% Linux:** Dual Boot
- **Mac users:** Native Terminal (đủ tốt)
- **Learning cloud:** AWS/GCP free tier

---

## 3. Công cụ cần thiết

### 3.1. Terminal / Shell

#### Windows Terminal

**Tại sao cần:**

- Default Windows CMD/PowerShell = cũ, xấu, thiếu features
- Windows Terminal = modern, đẹp, powerful

**Features:**

- ✅ Tabs: Nhiều terminal trong 1 window
- ✅ Themes: Customize colors
- ✅ Unicode/Emoji support: 🚀 💻 ✅
- ✅ GPU acceleration: Render nhanh
- ✅ Multiple profiles: CMD, PowerShell, WSL, Git Bash...

**Install:**

```
Microsoft Store → Search "Windows Terminal" → Get
```

Hoặc:

```powershell
winget install Microsoft.WindowsTerminal
```

#### Oh My Zsh (Linux/macOS)

**Tại sao cần:**

- Default Bash shell = basic
- Zsh + Oh My Zsh = supercharged shell

**Features:**

- ✅ Auto-completion: Tab → suggest commands
- ✅ Syntax highlighting: Lệnh đúng = màu xanh, sai = đỏ
- ✅ Themes: 100+ themes đẹp (powerlevel10k recommended)
- ✅ Plugins: git, docker, kubectl shortcuts
- ✅ History search: Ctrl+R tìm lệnh cũ

**Install script:**

```bash
# Install Zsh
sudo apt install zsh -y  # Ubuntu/Debian
# Or: brew install zsh   # macOS

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Set Zsh as default shell
chsh -s $(which zsh)
```

**Recommended theme:**

```bash
# Powerlevel10k - Most popular
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Edit ~/.zshrc
ZSH_THEME="powerlevel10k/powerlevel10k"

# Reload
source ~/.zshrc
```

#### Customization tips

**Windows Terminal settings.json:**

```json
{
  "defaultProfile": "{Ubuntu-22.04-GUID}",
  "profiles": {
    "defaults": {
      "fontFace": "Cascadia Code PL",
      "fontSize": 11,
      "colorScheme": "One Half Dark"
    }
  },
  "schemes": [
    {
      "name": "One Half Dark",
      "background": "#282C34",
      "foreground": "#DCDFE4"
    }
  ]
}
```

**Useful keyboard shortcuts:**

```
Ctrl + Shift + T    : New tab
Ctrl + Shift + W    : Close tab
Ctrl + Shift + D    : Duplicate pane
Alt + Shift + +/-   : Split pane
Ctrl + Shift + F    : Search
```

### 3.2. Code Editor - VS Code

#### Tại sao VS Code?

**Market share (2024):**

- VS Code: ~74% developers
- IntelliJ: ~10%
- Vim/Neovim: ~7%
- Others: ~9%

**Why so popular:**

- ✅ **Free & Open Source**
- ✅ **Fast:** Electron-based nhưng optimized tốt
- ✅ **Extensions:** 40,000+ extensions
- ✅ **Git integration:** Built-in
- ✅ **Remote development:** SSH, WSL, Containers
- ✅ **IntelliSense:** Auto-complete thông minh
- ✅ **Debugging:** Powerful debugger built-in

#### Must-have Extensions for DevOps

**Core:**

1. **Remote - WSL** (ms-vscode-remote.remote-wsl)
   - Mở VS Code trong WSL environment
   - Essential cho Windows users

2. **GitLens** (eamodio.gitlens)
   - Supercharge Git: Blame, history, comparison

3. **Docker** (ms-azuretools.vscode-docker)
   - Manage containers, images, compose files

4. **YAML** (redhat.vscode-yaml)
   - Syntax highlighting, validation cho Kubernetes/CI files

5. **Markdown All in One** (yzhang.markdown-all-in-one)
   - Preview, shortcuts, TOC generation

**Productivity:**
6. **Path Intellisense** - Auto-complete file paths
7. **Better Comments** - Highlight TODO, FIXME, ! comments
8. **Error Lens** - Inline error messages
9. **Prettier** - Code formatter
10. **Live Share** - Collaborative editing (Google Docs for code)

**Theme & UI:**
11. **One Dark Pro** - Popular theme
12. **Material Icon Theme** - Better file icons
13. **Bracket Pair Colorizer** - Match brackets với colors

#### Settings.json configuration

**Essential settings:**

```json
{
  // Editor
  "editor.fontSize": 14,
  "editor.fontFamily": "'Cascadia Code', 'Courier New', monospace",
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.formatOnSave": true,
  "editor.minimap.enabled": false,
  
  // Files
  "files.autoSave": "onFocusChange",
  "files.trimTrailingWhitespace": true,
  
  // Terminal
  "terminal.integrated.fontSize": 13,
  "terminal.integrated.defaultProfile.windows": "Ubuntu (WSL)",
  
  // Git
  "git.autofetch": true,
  "git.confirmSync": false,
  
  // Extensions
  "gitlens.currentLine.enabled": false,
  "docker.showStartPage": false
}
```

#### Keyboard shortcuts essentials

**Navigation:**

```
Ctrl + P          : Quick open file
Ctrl + Shift + P  : Command Palette
Ctrl + B          : Toggle sidebar
Ctrl + `          : Toggle terminal
Ctrl + Shift + E  : Open Explorer
Ctrl + Shift + F  : Search across files
```

**Editing:**

```
Alt + Up/Down     : Move line up/down
Shift + Alt + Down: Duplicate line
Ctrl + /          : Comment/uncomment
Ctrl + D          : Select next occurrence
Ctrl + Shift + L  : Select all occurrences
```

**Advanced:**

```
Ctrl + K Ctrl + S : Keyboard shortcuts
Ctrl + K V        : Markdown preview side-by-side
F2                : Rename symbol
Ctrl + .          : Quick fix
```

### 3.3. Package Managers

#### APT (Ubuntu/Debian)

**Là gì:**

- **APT** = Advanced Package Tool
- Package manager của Debian/Ubuntu
- Install/update/remove software via command line

**Basic commands:**

```bash
# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install package
sudo apt install packagename -y

# Remove package
sudo apt remove packagename

# Search package
apt search keyword

# Show package info
apt show packagename
```

**Example workflow:**

```bash
# 1. Refresh repos
sudo apt update

# 2. Install Docker
sudo apt install docker.io -y

# 3. Verify
docker --version
```

#### Homebrew (macOS)

**Là gì:**

- "The Missing Package Manager for macOS"
- Install Unix tools on Mac

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Basic commands:**

```bash
# Install package
brew install packagename

# Update Homebrew
brew update

# Upgrade packages
brew upgrade

# Search
brew search keyword

# List installed
brew list
```

**Example:**

```bash
# Install common tools
brew install git
brew install wget
brew install htop
brew install node
```

#### Chocolatey (Windows - Optional)

**Là gì:**

- Package manager cho Windows (như apt cho Ubuntu)

**Install:**

```powershell
# Run PowerShell as Admin
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

**Usage:**

```powershell
# Install Git
choco install git -y

# Install VS Code
choco install vscode -y

# Install multiple
choco install git vscode nodejs -y
```

---

## 4. Hướng dẫn Setup Windows

### 4.1. Kiểm tra yêu cầu hệ thống

#### Check Windows version

**Requirements:**

- Windows 10 version **1903** trở lên (Build 18362+)
- Hoặc Windows 11 (mọi version)

**Check version:**

```
1. Press Win + R
2. Type: winver
3. Enter
```

**Should see:**

```
Windows 10:
Phiên bản 21H2 (Build 19044) ← OK nếu >= 18362

Windows 11:
Phiên bản 22H2 (Build 22621) ← Always OK
```

**Nếu version cũ:**

```
Settings → Update & Security → Windows Update → Check for updates
```

#### Check RAM

**Minimum:** 8 GB
**Recommended:** 16 GB

**Check:**

```
Task Manager (Ctrl+Shift+Esc) → Performance → Memory
```

**Example output:**

```
Memory: 16.0 GB
Speed: 3200 MHz
Slots used: 2 of 2
```

#### Check Disk Space

**Minimum:** 50 GB free
**Recommended:** 100 GB free (cho Docker images, projects)

**Check:**

```
File Explorer → This PC → C: drive

Should see:
Local Disk (C:)
Free space: 150 GB of 500 GB  ← OK
```

#### Check Virtualization Enabled

**WSL2 cần Virtualization trong BIOS.**

**Check trong Windows:**

```
1. Task Manager (Ctrl+Shift+Esc)
2. Performance tab
3. CPU
4. Look for "Virtualization: Enabled"
```

**Nếu Disabled:**

```
1. Restart PC
2. Enter BIOS (thường là phím F2, F10, hoặc Delete khi boot)
3. Tìm setting: "Intel VT-x" hoặc "AMD-V" hoặc "Virtualization"
4. Enable
5. Save & Exit
```

**Note:** Mỗi motherboard khác nhau, Google "enable virtualization [your laptop model]"

### 4.2. Cài đặt WSL2

#### Enable WSL Feature

**Method 1: PowerShell (Recommended)**

Mở PowerShell **as Administrator**:

```powershell
# Enable WSL và Virtual Machine Platform
wsl --install

# Hoặc manual:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**Method 2: GUI**

```
Settings → Apps → Optional Features → More Windows Features
☑ Windows Subsystem for Linux
☑ Virtual Machine Platform
→ OK → Restart
```

**Restart required!**

#### Set WSL2 as Default

**After restart:**

```powershell
# Set default version to 2
wsl --set-default-version 2
```

#### Install Ubuntu 22.04

**Method 1: Microsoft Store (Recommended)**

```
1. Microsoft Store app
2. Search "Ubuntu 22.04"
3. Get/Install
4. Launch
```

**Method 2: Command Line**

```powershell
# List available distros
wsl --list --online

# Install Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

**First launch:**

```
Installing, this may take a few minutes...
Enter new UNIX username: yourname
New password: ********
Retype password: ********

Installation successful!
```

**Tips cho password:**

- Không thấy gì khi gõ (normal cho Unix passwords)
- Chọn password đơn giản cho local learning (vd: "1234")
- Production thì mới cần complex password

#### Verify Installation

```bash
# Check WSL version
wsl --list --verbose

# Output:
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2

# Check Linux distro
cat /etc/os-release

# Output:
NAME="Ubuntu"
VERSION="22.04.1 LTS (Jammy Jellyfish)"
```

### 4.3. Cấu hình Ubuntu

#### Update Packages

**Sau khi install Ubuntu, update ngay:**

```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Expected output:
Reading package lists... Done
Building dependency tree... Done
...
Fetched 85.2 MB in 15s (5,680 kB/s)
```

**Time:** ~2-5 phút tùy internet

#### Create User

**Username đã tạo lúc install. Để change:**

```bash
# Create new user (nếu muốn)
sudo adduser newusername

# Add to sudo group
sudo usermod -aG sudo newusername

# Switch user
su - newusername
```

**Tip:** Hầu hết không cần làm, dùng user đã tạo lúc install.

#### Generate SSH Keys

**SSH keys để authenticate với GitHub, servers...**

```bash
# Generate key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter to accept default location (~/.ssh/id_ed25519)
# Enter passphrase (hoặc Enter để skip cho simplicity)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

#View public key
cat ~/.ssh/id_ed25519.pub

# Copy đoạn text bắt đầu với "ssh-ed25519 AAA..."
```

**Sẽ dùng key này khi add vào GitHub (phần sau).**

#### Set Git Config

```bash
# Set name
git config --global user.name "Your Name"

# Set email
git config --global user.email "your.email@example.com"

# Verify
git config --list

# Output:
user.name=Your Name
user.email=your.email@example.com
```

### 4.4. Cài đặt VS Code

#### Download & Install

**Download:**

```
https://code.visualstudio.com/
→ Download for Windows
→ Run installer
```

**Install options:**

- ☑ Add "Open with Code" to context menu
- ☑ Add to PATH
- ☑ Register Code as an editor for supported file types

#### Install Remote - WSL Extension

**Method 1: Extension Marketplace**

```
1. Open VS Code
2. Extensions (Ctrl+Shift+X)
3. Search "Remote - WSL"
4. Install (by Microsoft)
```

**Method 2: Command Line**

```powershell
code --install-extension ms-vscode-remote.remote-wsl
```

#### Connect to WSL

**Method 1: From VS Code**

```
1. Open VS Code
2. Press F1
3. Type: "WSL: Connect to WSL"
4. Enter
```

**Method 2: From Terminal**

```bash
# From Ubuntu terminal in WSL:
code .

# VS Code will open connected to WSL
```

**Verify connection:**

- Bottom-left corner should show: `WSL: Ubuntu-22.04`

#### Open Project in WSL

```bash
# In WSL terminal:
cd ~
mkdir projects
cd projects
mkdir my-first-project
cd my-first-project

# Open in VS Code
code .
```

**VS Code opens → Connected to WSL → Ready to code!**

---

## 5. Hướng dẫn Setup macOS

### 5.1. Install Homebrew

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow on-screen instructions to add to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Verify
brew --version
```

### 5.2. Install iTerm2 (Optional but recommended)

```bash
brew install --cask iterm2
```

**iTerm2 features:**

- Split panes
- Search
- Autocomplete
- Better than default Terminal.app

### 5.3. Install Oh My Zsh

```bash
# Zsh is default on macOS Catalina+, but install Oh My Zsh:
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install Powerlevel10k theme
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Set theme in ~/.zshrc
sed -i '' 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc

# Reload
source ~/.zshrc

# Configure (follow prompts)
```

### 5.4. Install Essential Tools

```bash
# Git (nếu chưa có)
brew install git

# VS Code
brew install --cask visual-studio-code

# Common tools
brew install wget
brew install htop
brew install tree
```

### 5.5. Generate SSH Keys

```bash
# Same as Linux
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# View public key
cat ~/.ssh/id_ed25519.pub
```

### 5.6. Configure Git

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 6. Hướng dẫn Setup Linux Native

### 6.1. Ubuntu Desktop (Dual Boot hoặc Primary OS)

**Nếu bạn đã có Ubuntu desktop, skip install steps.**

**Update & Upgrade:**

```bash
sudo apt update && sudo apt upgrade -y
```

### 6.2. Install Essential Tools

```bash
# Build essentials
sudo apt install build-essential curl wget git -y

# VS Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

sudo apt update
sudo apt install code -y

# Oh My Zsh
sudo apt install zsh -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### 6.3. SSH Keys & Git Config

```bash
# SSH keys
ssh-keygen -t ed25519 -C "your.email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Git config
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 7. Tài khoản cần tạo

### 7.1. GitHub Account

#### Tạo account

```
1. Truy cập: https://github.com/signup
2. Email: your.email@example.com
3. Password: (strong password)
4. Username: choose-unique-username
5. Verify email
```

#### Enable 2FA (Two-Factor Authentication)

**Highly recommended:**

```
Settings → Password and authentication → Enable two-factor authentication
→ Use Authenticator App (Google Authenticator, Authy)
```

#### Add SSH Key

```
Settings → SSH and GPG keys → New SSH key

Title: "My WSL Ubuntu"
Key: [Paste public key từ ~/.ssh/id_ed25519.pub]

→ Add SSH key
```

**Verify:**

```bash
ssh -T git@github.com

# Output:
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

### 7.2. Docker Hub Account

#### Tạo account

```
1. https://hub.docker.com/signup
2. Docker ID: choose-username
3. Email: your.email@example.com
4. Password: (strong password)
5. Verify email
```

**Docker Hub = Registry để store Docker images (sẽ học ở Module 05)**

### 7.3. Cloud Accounts (Optional - Có thể làm sau)

**AWS Free Tier:**

- <https://aws.amazon.com/free/>
- 12 tháng free tier
- Credit card required (nhưng không charge nếu trong limits)

**Google Cloud Platform:**

- <https://cloud.google.com/free>
- $300 credits (90 ngày)
- Credit card required

**Tip:** Làm khi học đến Module Cloud (Advanced Track)

---

## 8. Verification & Testing

### 8.1. Run Verification Script

**Script này check:**

- OS version
- WSL version (nếu Windows)
- Git installed?
- SSH keys generated?
- VS Code installed?

**Download script:**

```bash
# Linux/macOS/WSL:
curl -o verify-setup.sh https://raw.githubusercontent.com/[your-repo]/DevOpsTraining/main/scripts/verify-linux.sh

# Make executable
chmod +x verify-setup.sh

# Run
./verify-setup.sh
```

**Expected output:**

```
===========================================
  DevOps Training - Environment Check
===========================================

✅ OS: Ubuntu 22.04 LTS
✅ WSL Version: WSL2
✅ Git: version 2.34.1
✅ SSH Keys: Found (~/.ssh/id_ed25519)
✅ VS Code: Version 1.85.1
✅ Zsh: /usr/bin/zsh
✅ Oh My Zsh: Installed

===========================================
  ALL CHECKS PASSED! 🎉
===========================================

You're ready to start Module 01!
```

### 8.2. Interpret Output

**Nếu thấy ❌ (failed check):**

| Error | Meaning | Fix |
|-------|---------|-----|
| `❌ Git: Not found` | Git chưa cài | `sudo apt install git -y` |
| `❌ SSH Keys: Not found` | SSH key chưa tạo | `ssh-keygen -t ed25519 -C "email"` |
| `❌ VS Code: Not found` | VS Code chưa cài | Install VS Code (xem phần trên) |
| `❌ WSL Version: WSL1` | Chưa upgrade WSL2 | `wsl --set-version Ubuntu-22.04 2` |

### 8.3. Manual Verification

**Nếu không dùng script, check manual:**

```bash
# Check OS
cat /etc/os-release

# Check Git
git --version

# Check SSH keys
ls -la ~/.ssh/

# Check VS Code (from terminal)
code --version

# Check Zsh
echo $SHELL
```

---

## 9. Troubleshooting

### 9.1. WSL Issues

#### Issue: "WslRegisterDistribution failed with error: 0x80370102"

**Cause:** Virtualization chưa enable trong BIOS

**Fix:**

```
1. Restart PC
2. Enter BIOS (F2/F10/Delete khi boot)
3. Find "Intel VT-x" or "AMD-V" or "Virtualization"
4. Enable
5. Save & Exit
6. Retry wsl --install
```

#### Issue: "WSL2 requires an update to its kernel component"

**Fix:**

```
1. Download WSL2 kernel update:
   https://aka.ms/wsl2kernel
2. Run the .msi installer
3. Restart WSL: wsl --shutdown
4. wsl
```

#### Issue: Ubuntu boot rất chậm

**Possible cause:** WSL2 file system nằm trên HDD thay vì SSD

**Check:**

```powershell
# Find .vhdx file location
Get-ChildItem -Path $env:LOCALAPPDATA\Packages -Recurse -Filter "ext4.vhdx"

# Should be on SSD (C:) not HDD (D:)
```

**Fix:** Di chuyển .vhdx lên SSD (advanced, Google "move WSL2 to another drive")

### 9.2. Network Issues

#### Issue: Cannot reach internet from WSL

**Check:**

```bash
ping google.com

# Nếu fail:
# ping: google.com: Temporary failure in name resolution
```

**Fix:**

```bash
# Edit /etc/resolv.conf
sudo nano /etc/resolv.conf

# Replace content với:
nameserver 8.8.8.8
nameserver 8.8.4.4

# Save (Ctrl+O, Enter, Ctrl+X)

# Test
ping google.com
```

**Permanent fix:**

```bash
# Create /etc/wsl.conf
sudo nano /etc/wsl.conf

# Add:
[network]
generateResolvConf = false

# Save, then restart WSL:
# From PowerShell:
wsl --shutdown
wsl
```

#### Issue: SSH connection timeout

**Check:**

```bash
ssh -T git@github.com

# Timeout...
```

**Fix:**

```bash
# Edit SSH config
nano ~/.ssh/config

# Add:
Host github.com
  Hostname ssh.github.com
  Port 443
  User git

# Save, test:
ssh -T git@github.com
```

### 9.3. Permission Issues

#### Issue: "Permission denied" khi chạy script

**Fix:**

```bash
# Make executable
chmod +x script.sh

# Run
./script.sh
```

#### Issue: "sudo: command not found"

**Rare, nhưng nếu gặp (minimal distro):**

```bash
# Install sudo
apt install sudo

# Add user to sudo group
usermod -aG sudo username
```

### 9.4. VS Code Issues

#### Issue: VS Code cannot connect to WSL

**Fix:**

```
1. Uninstall "Remote - WSL" extension
2. Reinstall
3. Reload VS Code
4. Try again: "WSL: Connect to WSL"
```

#### Issue: Extensions not working in WSL

**Cause:** Extensions installed in Windows, not WSL

**Fix:**

```
1. Open VS Code in WSL
2. Click Extensions
3. Notice "Install in WSL: Ubuntu-22.04" button
4. Click to install
```

### 9.5. Common Errors

#### Error: "command not found"

**Meaning:** Command chưa cài hoặc không trong PATH

**Fix:**

```bash
# Check if installed
which commandname

# If not found:
sudo apt install commandname

# Or update PATH:
echo 'export PATH=$PATH:/path/to/bin' >> ~/.zshrc
source ~/.zshrc
```

#### Error: "Package not found" (apt)

**Fix:**

```bash
# Update package lists
sudo apt update

# Retry install
sudo apt install packagename
```

---

## 📚 Tổng kết

### Key Takeaways

1. **DevOps** = Culture + Automation + Measurement
2. **Linux** là ngôn ngữ của DevOps (95% production servers)
3. **WSL2** = Best balance cho Windows users (near-native performance)
4. **Tools:** Windows Terminal, VS Code, Oh My Zsh
5. **Accounts:** GitHub, Docker Hub là must-have

### Checklist hoàn thành

- [ ] Hiểu DevOps là gì, tại sao học
- [ ] Setup môi trường Linux (WSL2/macOS/Native)
- [ ] Cài đặt Terminal, VS Code, Git
- [ ] Tạo GitHub account + add SSH key
- [ ] Tạo Docker Hub account
- [ ] Run verification script → All green ✅
- [ ] Troubleshoot bất kỳ issues nào gặp

### Next Steps

👉 **Module 01: LINUX_BASICS**

Bây giờ môi trường đã ready, chúng ta sẽ học:

- Linux file system
- Command line mastery
- Permissions, processes
- Shell scripting basics

---

## 📖 Further Reading

### Recommended Resources

**DevOps:**

- [The Phoenix Project](https://itrevolution.com/product/the-phoenix-project/) - Novel về DevOps transformation
- [DevOps Handbook](https://itrevolution.com/product/the-devops-handbook/) - Theory & practices
- [r/devops](https://reddit.com/r/devops) - Community

**WSL2:**

- [Official WSL docs](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL tips & tricks](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)

**Linux:**

- [Linux Journey](https://linuxjourney.com/) - Interactive learning
- [The Linux Command Line](http://linuxcommand.org/tlcl.php) - Free book

### Communities

- [DevOps Discord servers](https://discord.gg/devops)
- [Stack Overflow - DevOps tag](https://stackoverflow.com/questions/tagged/devops)
- [Dev.to - DevOps](https://dev.to/t/devops)

---

> **Chúc mừng! Bạn đã hoàn thành Module 00! 🎉**
>
> **Môi trường đã sẵn sàng. Let's start the DevOps journey! 🚀**
>
> **Next: Module 01 - LINUX_BASICS**
