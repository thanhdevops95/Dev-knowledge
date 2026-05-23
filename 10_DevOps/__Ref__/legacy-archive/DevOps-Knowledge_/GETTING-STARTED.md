# Getting Started - Bắt đầu với Knowledge Base

> Hướng dẫn sử dụng Knowledge Base cho người mới

## 🎯 Knowledge Base này dành cho ai?

- **Người mới bắt đầu DevOps** - Học từ đầu
- **Developer muốn chuyển sang DevOps** - Bổ sung kiến thức
- **DevOps Engineer** - Tra cứu và tham khảo
- **Sinh viên IT** - Học tập và thực hành

## 🚀 Bắt đầu như thế nào?

### Nếu bạn là người hoàn toàn mới

**Lộ trình học tập đề xuất:**

#### Week 1-2: Fundamentals
1. Đọc [THEORY/Fundamentals/linux.md](./THEORY/Fundamentals/linux.md)
2. Thực hành với [CHEATSHEETS/linux-commands.md](./CHEATSHEETS/linux-commands.md)
3. Làm project: [PROJECTS/beginner-projects.md](./PROJECTS/beginner-projects.md) #5 (Linux Server Setup)

#### Week 3-4: Version Control
1. Đọc [THEORY/Fundamentals/version-control.md](./THEORY/Fundamentals/version-control.md)
2. Thực hành với [CHEATSHEETS/git-commands.md](./CHEATSHEETS/git-commands.md)
3. Làm project: [PROJECTS/beginner-projects.md](./PROJECTS/beginner-projects.md) #3 (Git Workflow)

#### Week 5-6: Docker
1. Đọc [THEORY/Containerization/docker.md](./THEORY/Containerization/docker.md)
2. Cài đặt: [SETUP-GUIDES/Tools/docker-installation.md](./SETUP-GUIDES/Tools/docker-installation.md)
3. Thực hành: [CHEATSHEETS/docker-commands.md](./CHEATSHEETS/docker-commands.md)
4. Làm projects: #1, #4 trong [PROJECTS/beginner-projects.md](./PROJECTS/beginner-projects.md)

#### Week 7-8: CI/CD Basics
1. Làm project #6: Simple CI Pipeline
2. Tìm hiểu GitHub Actions
3. Tự động hóa Docker build

#### Week 9-10: Kubernetes (Optional)
1. Đọc [THEORY/Orchestration/kubernetes.md](./THEORY/Orchestration/kubernetes.md)
2. Cài đặt Minikube
3. Thực hành với kubectl

### Nếu bạn đã có kinh nghiệm

**Sử dụng như tài liệu tham khảo:**

```
Cần tra cứu lệnh → CHEATSHEETS/
Gặp lỗi → TROUBLESHOOTING/
Cần code mẫu → CODE-SAMPLES/
Ôn lại lý thuyết → THEORY/
```

## 📚 Cấu trúc Knowledge Base

### [THEORY/](./THEORY) - Kiến thức lý thuyết
**Khi nào dùng:** Khi muốn hiểu sâu về một công nghệ

**Đặc điểm:**
- Mỗi file = 1 chủ đề
- Nội dung đầy đủ, chi tiết
- Có ví dụ thực tế

**Ví dụ:** Muốn học Docker → Đọc `THEORY/Containerization/docker.md`

### [DICTIONARY/](./DICTIONARY) - Từ điển
**Khi nào dùng:** Không hiểu một thuật ngữ

**Files quan trọng:**
- `it-terms.md` - Thuật ngữ IT chung
- `devops-terms.md` - Thuật ngữ DevOps
- `abbreviations.md` - Từ viết tắt (API, CI/CD, K8s...)

### [CHEATSHEETS/](./CHEATSHEETS) - Tra cứu nhanh
**Khi nào dùng:** Cần lệnh nhanh, không nhớ syntax

**Files có sẵn:**
- ✅ `linux-commands.md` - Lệnh Linux
- ✅ `docker-commands.md` - Lệnh Docker
- ✅ `git-commands.md` - Lệnh Git

**Tip:** Bookmark những file này để tra cứu nhanh!

### [TROUBLESHOOTING/](./TROUBLESHOOTING) - Xử lý lỗi
**Khi nào dùng:** Gặp lỗi, không biết fix

**Files có sẵn:**
- ✅ `docker-errors.md` - Lỗi Docker
- ✅ `linux-errors.md` - Lỗi Linux

**Cách dùng:**
1. Copy error message
2. Search trong file tương ứng
3. Follow giải pháp

### [CODE-SAMPLES/](./CODE-SAMPLES) - Code mẫu
**Khi nào dùng:** Cần code để tham khảo hoặc sử dụng

**Có gì:**
- Bash scripts
- Dockerfiles
- docker-compose.yml
- Kubernetes manifests
- Terraform configs

**Cách dùng:**
1. Tìm code mẫu phù hợp
2. Copy và customize
3. Test trước khi dùng production

### [SETUP-GUIDES/](./SETUP-GUIDES) - Hướng dẫn cài đặt
**Khi nào dùng:** Cần cài đặt tool hoặc setup môi trường

**Ví dụ:**
- Cài Docker → `Tools/docker-installation.md`
- Setup Ubuntu Server → `Server/ubuntu-server-setup.md`

### [PROJECTS/](./PROJECTS) - Dự án thực hành
**Khi nào dùng:** Muốn thực hành, áp dụng kiến thức

**Levels:**
- **Beginner** ✅ - Đã có 8 projects
- **Intermediate** - Coming soon
- **Advanced** - Coming soon

**Tip:** Làm projects và push lên GitHub để build portfolio!

## 💡 Tips học tập hiệu quả

### 1. Học theo lộ trình
❌ Đừng nhảy lung tung  
✅ Follow lộ trình từ cơ bản → nâng cao

### 2. Thực hành nhiều
❌ Chỉ đọc lý thuyết  
✅ Đọc xong → Thực hành ngay → Làm project

### 3. Document lại
❌ Học xong quên  
✅ Ghi chú, viết blog, tạo cheatsheet riêng

### 4. Build portfolio
❌ Học xong không có gì để show  
✅ Mỗi project push lên GitHub với README đầy đủ

### 5. Join communities
- Reddit: r/devops, r/docker, r/kubernetes
- Discord: DevOps servers
- Stack Overflow: Hỏi đáp

## 🎓 Learning Path đề xuất

### Path 1: DevOps Fundamentals (2-3 tháng)
```
Linux → Git → Docker → CI/CD Basics → Kubernetes Basics
```

### Path 2: Cloud DevOps (3-4 tháng)
```
Fundamentals → AWS/GCP/Azure → Terraform → Kubernetes → Monitoring
```

### Path 3: Full DevOps Engineer (6-12 tháng)
```
All Fundamentals → Cloud Platform → IaC → Orchestration → 
CI/CD Advanced → Monitoring & Logging → Security → 
Real Projects
```

## 📖 Cách đọc hiệu quả

### Đọc THEORY files
1. **Đọc tổng quan** - Xem mục lục, hiểu structure
2. **Đọc chi tiết** - Từng section, không skip
3. **Chạy examples** - Mọi example đều phải chạy thử
4. **Ghi chú** - Note lại những điểm quan trọng
5. **Làm bài tập** - Nếu có

### Dùng CHEATSHEETS
1. **Đọc qua 1 lần** - Để biết có gì
2. **Bookmark** - Để tra cứu nhanh
3. **Practice** - Thử từng lệnh
4. **Customize** - Tạo cheatsheet riêng với những lệnh hay dùng

### Làm PROJECTS
1. **Đọc requirements** - Hiểu rõ cần làm gì
2. **Plan** - Lên kế hoạch từng bước
3. **Research** - Google, đọc docs
4. **Implement** - Làm từng bước nhỏ
5. **Test** - Test kỹ
6. **Document** - Viết README
7. **Push to GitHub** - Build portfolio

## 🔍 Search & Navigate

### Tìm nội dung
```bash
# Tìm trong tất cả files
grep -r "keyword" .

# Tìm file theo tên
find . -name "*docker*"

# Tìm trong một file cụ thể
grep "pattern" CHEATSHEETS/docker-commands.md
```

### Quick Links

**Bắt đầu ngay:**
- [Linux Fundamentals](./THEORY/Fundamentals/linux.md)
- [Docker Installation](./SETUP-GUIDES/Tools/docker-installation.md)
- [Beginner Projects](./PROJECTS/beginner-projects.md)

**Tra cứu nhanh:**
- [Linux Commands](./CHEATSHEETS/linux-commands.md)
- [Docker Commands](./CHEATSHEETS/docker-commands.md)
- [Git Commands](./CHEATSHEETS/git-commands.md)

**Xử lý lỗi:**
- [Docker Errors](./TROUBLESHOOTING/docker-errors.md)
- [Linux Errors](./TROUBLESHOOTING/linux-errors.md)

## 📞 Cần giúp đỡ?

### Khi gặp vấn đề
1. **Check TROUBLESHOOTING/** - Có thể đã có giải pháp
2. **Google error message** - Thường có người gặp rồi
3. **Read documentation** - Official docs luôn là nguồn tốt nhất
4. **Ask in communities** - Reddit, Discord, Stack Overflow

### Resources bổ sung
- [RESOURCES/](./RESOURCES) - Sách, courses, blogs (coming soon)

## 🎯 Goals

**Sau khi hoàn thành Knowledge Base này, bạn sẽ:**
- ✅ Hiểu rõ DevOps fundamentals
- ✅ Sử dụng thành thạo Docker, Git, Linux
- ✅ Biết setup CI/CD pipelines
- ✅ Có portfolio với real projects
- ✅ Sẵn sàng cho DevOps interviews
- ✅ Tự tin apply DevOps positions

---

**Ready to start? Let's go! 🚀**

Bắt đầu với: [Linux Fundamentals](./THEORY/Fundamentals/linux.md)

---

