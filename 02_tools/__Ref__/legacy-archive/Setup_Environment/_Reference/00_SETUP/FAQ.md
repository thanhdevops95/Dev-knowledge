# FAQ - Module 00: SETUP

> **Câu hỏi thường gặp về setup môi trường**

---

## 📑 Mục lục

- [General Questions](#general-questions)
- [Windows / WSL2 Questions](#windows--wsl2-questions)
- [macOS Questions](#macos-questions)
- [Linux Questions](#linux-questions)
- [VS Code Questions](#vs-code-questions)
- [Download & Course Materials](#download--course-materials)
- [Accounts Questions](#accounts-questions)
- [Next Steps](#next-steps)

---

## General Questions

### Q1: Tôi hoàn toàn mới với lập trình/CNTT. Có nên học DevOps không?

**A:** CÓ! DevOps là con đường tốt để bắt đầu vì:

**Lý do:**

1. **Không cần background lập trình sâu** - DevOps focus vào automation và tools, không phải viết app phức tạp
2. **Học được nhiều thứ** - Linux, Networking, Cloud, Containers... → Kiến thức nền tảng cho mọi vai trò IT
3. **Nhu cầu cao** - Mọi công ty đều cần DevOps, dễ tìm việc
4. **Lương tốt** - Junior DevOps lương ~15-20M VND/tháng tại VN

**Nhưng bạn CẦN:**

- Kiên nhẫn và chịu học
- Practice hands-on NHIỀU
- Không bỏ cuộc khi gặp khó khăn

**Foundation track này được thiết kế cho người mới 100%!**

---

### Q2: Mất bao lâu để học xong Foundation track?

**A:** Tùy vào thời gian bạn có:

| Thời gian/tuần | Hoàn thành sau |
|----------------|----------------|
| 6-8 giờ/tuần | 8 tuần (2 tháng) |
| 10-12 giờ/tuần | 5-6 tuần |
| 15-20 giờ/tuần | 3-4 tuần |
| Full-time (40h/tuần) | 2 tuần |

**Khuyến nghị:** 6-8 giờ/tuần để có thời gian absorb kiến thức.

Học quá nhanh → không hiểu sâu → quên nhanh.

---

### Q3: Tôi có cần biết tiếng Anh không?

**A:** Cần **đọc** tiếng Anh kỹ thuật cơ bản.

**Lý do:**

- Documentation hầu hết bằng tiếng Anh
- Error messages bằng tiếng Anh
- Stack Overflow, GitHub bằng tiếng Anh

**Mức độ cần:**

- ❌ KHÔNG CẦN: Nói/nghe tốt, IELTS 7.0
- ✅ CẦN: Đọc hiểu error messages, docs

**Nếu tiếng Anh yếu:**

- Dùng Google Translate
- Học technical vocabulary từ từ
- Khóa này bằng tiếng Việt để giúp bạn!

---

### Q4: Máy tính cấu hình thấp có học được không?

**A:** Được, nhưng có giới hạn.

**Cấu hình tối thiểu:**

- CPU: Core i3 hoặc tương đương
- RAM: 8GB (foundation track còn chạy được)
- Disk: 30GB free space

**Lưu ý:**

- Foundation track: 8GB RAM OK for most labs
- Advanced track: Cần 16GB RAM (vì chạy Kubernetes local)

**Giải pháp nếu máy yếu:**

- Dùng Cloud VM (AWS, GCP free tier)
- GitHub Codespaces (free 60 hours/month)
- Xin mượn máy bạn bè :)

---

## Windows / WSL2 Questions

### Q5: Tôi dùng Windows. Có BẮT BUỘC phải cài WSL2 không?

**A:** Đối với course này - **CÓ, BẮT BUỘC**.

**Lý do:**

1. **90% công cụ DevOps được thiết kế cho Linux**
   - Ansible: KHÔNG có version Windows official
   - Nhiều scripts: Dùng bash (không phải PowerShell)
2. **Production servers hầu hết chạy Linux**
   - AWS EC2, GCP Compute: Default là Linux
   - Học trên WSL = Giống production
3. **WSL2 performance tốt**
   - Không chậm như Virtual Machine
   - Integration với Windows tốt

**Nếu THỰC SỰ không muốn WSL2:**

Các alternatives:

- **VirtualBox** + Ubuntu (không khuyến nghị - chậm)
- **Cloud VM** (AWS, GCP) - OK nhưng tốn kết nối internet
- **Dual boot** Linux + Windows - OK nhưng rất phức tạp

→ **WSL2 là cách đơn giản nhất!**

---

### Q6: Sự khác biệt giữa PowerShell và WSL là gì?

**A:** Hai môi trường khác biệt hoàn toàn.

| Aspect | PowerShell | WSL (Ubuntu) |
|--------|------------|--------------|
| **Shell** | PowerShell | Bash |
| **Commands** | `Get-ChildItem`, `Remove-Item` | `ls`, `rm` |
| **OS** | Windows | Linux |
| **DevOps tools** | Một số | Hầu hết |
| **Dùng để** | Quản trị Windows | Dev, DevOps |

**Ẩn dụ:**

```
PowerShell = Lái xe bên phải (Anh, Nhật)
Bash (WSL) = Lái xe bên trái (Việt Nam, US)

Cả hai đều là "lái xe" nhưng:
- Controls khác nhau
- Rules khác nhau
→ Đừng lẫn lộn!
```

**Trong course:**

- Module 00 setup: Dùng PowerShell (cài WSL)
- Từ Module 01 trở đi: Dùng WSL/Bash

---

### Q7: WSL2 có ảnh hưởng đến Windows không? Có thể gỡ sau không?

**A:** KHÔNG nh hưởng, VA dễ dàng gỡ nếu muốn.

**Ảnh hưởng:**

- ✅ Windows vẫn hoạt động bình thường
- ✅ Apps Windows vẫn chạy như thường
- ⚠️ Tốn ~2-4GB RAM khi WSL chạy
- ⚠️ Tốn ~5-10GB disk for Ubuntu

**Gỡ WSL2 (nếu cần):**

```powershell
# List distributions
wsl --list

# Unregister Ubuntu
wsl --unregister Ubuntu

# Disable WSL feature
dism.exe /online /disable-feature /featurename:Microsoft-Windows-Subsystem-Linux
dism.exe /online /disable-feature /featurename:VirtualMachinePlatform

# Restart
```

→ **Nhưng sau course này, bạn sẽ MUỐN giữ WSL2!** :)

---

## macOS Questions

### Q8: iTerm2 hay Terminal mặc định?

**A:** Cả hai đều OK, nhưng **iTerm2** tốt hơn.

**Terminal mặc định (Terminal.app):**

- ✅ Sẵn có, không cần cài
- ✅ Đủ dùng cho Foundation track
- ❌ Ít tính năng

**iTerm2:**

- ✅ Nhiều tính năng (split panes, search, themes)
- ✅ Customizable
- ❌ Phải cài thêm

**Recommendation cho course:**

- Foundation track: **Terminal.app đủ**
- Advanced track: Nên dùng **iTerm2** (vì làm việc nhiều với terminal hơn)

**Cài iTerm2:**

```bash
brew install --cask iterm2
```

---

### Q9: Homebrew có an toàn không?

**A:** **RẤT an toàn**. Homebrew là tool official, được dùng bởi hàng triệu macOS developers.

**Bằng chứng:**

- Open source: <https://github.com/Homebrew/brew>
- Maintained by trusted community
- Used by Apple engineers, Google, Facebook, ...

**Lưu ý bảo mật:**

- ✅ Luôn cài từ trang chính thức: brew.sh
- ❌ Đừng cài từ scripts lạ

---

## Linux Questions

### Q10: Distro Linux nào nên dùng ?

**A:** Cho course này: **Ubuntu 22.04 LTS**

**Lý do:**

1. **Phổ biến nhất** - Nhiều tài liệu, dễ tìm giải pháp khi lỗi
2. **Stable** - LTS = Long Term Support (5 năm)
3. **Package availability** - Hầu hết tools có .deb hoặc trong apt repository
4. **Course đã test trên Ubuntu**

**Nếu đã dùng distro khác:**

| Distro hiện tại | Có cần đổi? |
|-----------------|-------------|
| Debian, Linux Mint | Không cần - tương tự Ubuntu |
| Fedora, CentOS | Không cần - chỉ commands hơi khác (dnf thay vì apt) |
| Arch, Manjaro | Nếu đã quen thì OK, nhưng khó hơn cho người mới |
| Kali Linux | Không khuyến nghị - Kali cho security testing, không phải DevOps |

---

## VS Code Questions

### Q11: Bắt buộc phải dùng VS Code không? Có thể dùng Vim/Emacs/Nano không?

**A:** **VS Code khuyến nghị mạnh**, nhưng không bắt buộc.

**Tại sao khuyến nghị VS Code:**

- ✅ Syntax highlighting cho nhiều ngôn ngữ
- ✅ Extensions cho DevOps (Docker, Kubernetes, Terraform, ...)
- ✅ Integrated terminal
- ✅ Git integration
- ✅ Remote development (WSL, SSH)
- ✅ Miễn phí, cross-platform

**Nếu muốn dùng Vim/Emacs:**

- OK nếu bạn đã thành thạo
- Course vẫn hướng dẫn được
- Nhưng một số tasks sẽ mất thời gian hơn

**Nếu mới bắt đầu:** → Dùng VS Code. SAU NÀY học Vim.

---

### Q12: Extensions nào cần cài cho VS Code?

**A:** Cho **Foundation track** (cài trong Module 00):

- ✅ **Remote - WSL** (Windows only) - Kết nối VS Code với WSL
- ✅ **GitLens** (optional) - Git supercharged

Cho **các module sau:**

| Module | Extensions |
|--------|------------|
| 02 - Git | GitLens, Git Graph |
| 04 - HTML/CSS | Live Server, Prettier |
| 05 - Docker | Docker |
| 07 - Kubernetes (Advanced) | Kubernetes |
| 09 - Terraform (Advanced) | HashiCorp Terraform |

→ **Sẽ hướng dẫn cài khi đến module đó!**

---

## Download & Course Materials

### Q13: Tại sao KHÔNG dùng `git clone` để download tài liệu?

**A:** Vì chúng ta chưa học Git!

**Timeline đúng:**

```
Module 00: Download ZIP           ← Bây giờ
           ↓
Module 02: Học Git                 ← Tuần 3
           ↓
Module 02 trở đi: Dùng git pull    ← Update tài liệu
```

**Logic:**

- Dùng tool TRƯỚC KHI hiểu nó = học vẹt, không hiểu
- Học xong Git → Biết tại sao dùng Git → Dùng có ý thức

**Sau Module 02:**
Bạn sẽ hiểu `git clone` là gì và dùng nó để:

- Clone repos khác
- Update tài liệu course (git pull)

---

### Q14: Làm thế nào để update tài liệu course khi có bản mới?

**A:** Trước và sau khi học Git khác nhau.

**TRƯỚC Module 02 (chưa học Git):**

```
1. Backup folder hiện tại:
   mv DevOpsTraining DevOpsTraining-old

2. Download ZIP mới (như Module 00)

3. Extract vào ~/DevOps/

4. Copy notes của bạn từ folder cũ (nếu có)
```

**SAU Module 02 (đã học Git):**

```bash
cd ~/DevOps/DevOpsTraining
git pull origin main
# Tự động update!
```

→ **Đây là lý do tại sao cần học Git!**

---

## Accounts Questions

### Q15: Tại sao cần cả GitHub VÀ Docker Hub? Có phải một cái không?

**A:** **HAI mục đích khác nhau**, cả hai đều cần.

**GitHub:**

- Lưu **code** (`.js`, `.py`, `.yaml`, ...)
- Version control
- Collaborate với team
- Host websites (GitHub Pages)
- CI/CD (GitHub Actions)

**Docker Hub:**

- Lưu **Docker images** (packaged applications)
- Public images (nginx, postgres, redis, ...)
- Private images (your apps)

**Ẩn dụ:**

```
GitHub = Google Drive         → Lưu documents, code
Docker Hub = Container Port   → Lưu shipping containers (apps)
```

**Có thể dùng chỉ một?**

- Technically yes (GitHub có Container Registry)
- Nhưng Docker Hub là standard cho public images
- Course dạy cả hai → Skills transferable

---

### Q16: Có thể dùng tài khoản GitHub cá nhân không? Hay cần tạo mới?

**A:** **Dùng account cá nhân hoàn toàn OK!**

**Nếu đã có GitHub account:**

- ✅ Dùng luôn, khôngần tạo mới
- ✅ Course projects sẽ thêm vào portfolio của bạn
- ⚠️ Nên cleanup old repos nếu quá nhiều repos lộn xộn

**Nếu chưa có:**

- Tạo mới với **username chuyên nghiệp**
- Username này sẽ đi theo bạn trong career
- Ví dụ tốt: `john-smith`, `thanh-nguyen-dev`, `devops-engineer`
- Ví dụ xấu: `cuteboii123`, `xXx_hacker_xXx`

---

## Next Steps

### Q17: Sau khi hoàn thành Module 00, tôi nên làm gì?

**A:** Checklist:

```
1. ✅ Verify tất cả labs Module 00 done
2. ✅ Chạy verification script → All green
3. 📖 Read Module 01 README (đọc hết, không skim!)
4. 📝 Make notes về concepts mới
5. 💻 Bắt đầu Module 01 Labs
6. 🤔 Join Discord community để hỏi đáp
```

**ĐỪNG:**

- ❌ Rush sang Module 01 mà không verify môi trường
- ❌ Skip đọc README, nhảy thẳng vào labs
- ❌ Học một mình không hỏi ai khi stuck

---

### Q18: Module nào khó nhất trong Foundation track?

**A:** Dựa trên feedback từ students trước:

**Top 3 khó nhất:**

1. **Module 05: Docker** (khái niệm mới hoàn toàn)
   - Images vs Containers
   - Networking
   - Volumes
   → **Tip:** Làm labs nhiều lần, vẽ diagrams

2. **Module 06: CI/CD** (abstract concepts)
   - YAML syntax
   - GitHub Actions workflow
   - Pipeline thinking
   → **Tip:** Chạy thử từng step của workflow manually trước

3. **Module 02: Git** (branching, merging)
   - Branch concepts
   - Merge conflicts
   - Rebase vs Merge
   → **Tip:** Practice trên dummy repo trước khi apply vào dự án thật

**Dễ nhất:**

- Module 00: Setup (follow instructions)
- Module 08: Deployment (fun, thấy kết quả ngay)

---

### Q19: Nếu tôi stuck ở một module, có nên skip không?

**A:** **KHÔNG. Đừng skip!**

**Tại sao:**

- Modules build on each other
- Skip Module 02 (Git) → Module 06 (CI/CD) sẽ không hiểu gì
- Hiểu 70% Module A + 70% Module B ≠ 70% overall
  → = 49% overall (vì knowledge gaps)

**Nếu stuck:**

1. **Re-read README** slowly. Most answers are there.
2. **Check FAQ** (file này!) và Troubleshooting
3. **Search Google** với keywords: "DevOps [topic] explained"
4. **Ask in Discord** - Community sẽ giúp!
5. **Watch YouTube videos** about the topic
6. **Take a break** - Sometimes you need to sleep on it

**Khi nào thì OK để move on:**

- Hiểu được 80%+ concepts
- Làm được 90%+ labs
- Giải được 70%+ scenarios

---

### Q20: Tôi nên học bao nhiêu tiếng mỗi ngày?

**A:** **Quality > Quantity**

**Khuyến nghị:**

| Sessions | Duration | Breaks | Total/day |
|----------|----------|--------|-----------|
| 2 sessions | 45-60 min each | 15 min between | 1.5-2 hours |
| 3 sessions | 30-45 min each | 10 min between | 1.5-2.5 hours |

**Lý do:**

- Brain absorbs better with breaks
- DevOps cần hands-on → Không thể học "passive" như đọc sách
- Burnout real → Học quá nhiều → Bỏ cuộc

**Pomodoro Technique:**

```
25 min: Đọc lý thuyết
5 min: Break
25 min: Làm lab
5 min: Break
25 min: Làm exercises
15 min: Break
Repeat...
```

---

### Q21: Học xong Foundation có đủ đi làm không?

**A:** **Có thể!** Nhưng...

**Vị trí có thể apply:**

- ✅ Junior DevOps Engineer
- ✅ DevOps Intern
- ✅ Build/Release Engineer
- ✅ CI/CD Engineer (junior)

**Yêu cầu thêm để higher chance:**

- ✅ Hoàn thành **Final Project** tốt
- ✅ Có **2-3 projects** khác trên GitHub
- ✅ **Resume** được optimize
- ✅ **Practice interview** questions

**Để lên Senior:**

- Cần **Advanced Track**
- Hoặc **2-3 năm experience** làm việc

**Lương expected (Vietnam):**

- Intern: 5-8M VND/tháng
- Junior: 12-18M VND/tháng
- Mid-level: 20-30M VND/tháng

---

## 💬 Không tìm thấy câu hỏi của bạn?

- 🤔 **Hỏi trong:** [GitHub Discussions](https://github.com/your-org/DevOpsTraining/discussions)
- 💬 **Join Discord:** [discord.gg/devops-training](https://discord.gg/devops-training)
- 📧 **Email:** <support@devops-training.com>

---

<div align="center">

**FAQ được update thường xuyên dựa trên câu hỏi của learners!**

**Last updated:** 2025-01-15

</div>
