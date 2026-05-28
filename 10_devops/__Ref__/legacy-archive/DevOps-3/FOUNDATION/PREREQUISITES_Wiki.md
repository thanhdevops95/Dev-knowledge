# 📋 PREREQUISITES: YÊU CẦU ĐẦU VÀO

> **Track:** Foundation (Zero to Junior DevOps)
>
> **Triết lý:** "No prerequisites" - Bắt đầu từ con số 0

---

## 🎯 TÓM TẮT

Foundation Track được thiết kế cho người **HOÀN TOÀN MỚI** với DevOps và IT.

**Không yêu cầu:**

- ❌ Kinh nghiệm lập trình
- ❌ Kiến thức Linux
- ❌ Biết Git/Docker/CI/CD
- ❌ Background IT/CS

**Chỉ cần:**

- ✅ Máy tính (Windows/macOS/Linux)
- ✅ Kết nối Internet
- ✅ Tinh thần học hỏi
- ✅ Kiên nhẫn với command line

---

## 💻 YÊU CẦU PHẦN CỨNG (HARDWARE REQUIREMENTS)

### Tối thiểu (Minimum)

| Component | Requirement |
|-----------|-------------|
| **CPU** | Dual-core 2.0 GHz |
| **RAM** | 8 GB |
| **Disk** | 50 GB free space (SSD khuyến nghị) |
| **OS** | Windows 10 (1903+) / macOS 10.15+ / Ubuntu 20.04+ |
| **Internet** | Stable connection (download source code, Docker images) |

### Khuyến nghị (Recommended)

| Component | Recommendation |
|-----------|----------------|
| **CPU** | Quad-core 2.5 GHz+ |
| **RAM** | 16 GB |
| **Disk** | 100 GB SSD |
| **OS** | Windows 11 / macOS 13+ / Ubuntu 22.04 |

### Notes

- **WSL2 (Windows):** Cần bật Virtualization trong BIOS
- **Docker:** Cần CPU hỗ trợ virtualization
- **VS Code:** Chạy trơn tru với 8GB RAM, tốt hơn với 16GB

---

## 📚 YÊU CẦU KIẾN THỨC (KNOWLEDGE REQUIREMENTS)

### ✅ Bắt buộc (Mandatory)

**1. Sử dụng máy tính cơ bản:**

- Biết mở/đóng ứng dụng
- Copy/paste text
- Download & install software
- Browse internet

**2. Đọc tiếng Anh kỹ thuật:**

- Tài liệu tiếng Việt, nhưng thuật ngữ giữ nguyên tiếng Anh
- Cần đọc hiểu: "container", "deployment", "pipeline"...
- Không cần nói/viết Anh giỏi

**3. Tư duy logic:**

- Hiểu nhân quả (nếu A thì B)
- Debug: "Lỗi gì? Tại sao? Fix thế nào?"

### ⭐ Có thì tốt (Nice to have)

**1. Lập trình cơ bản (bất kỳ ngôn ngữ):**

- Hiểu biến, hàm, vòng lặp
- → Dễ học Bash/Python scripting trong Advanced

**2. HTML/CSS:**

- Biết tạo web page đơn giản
- → Module 04 sẽ dễ hơn

**3. Tiếng Anh:**

- Đọc tài liệu technical
- → Mở rộng học từ nguồn quốc tế

### ❌ KHÔNG cần (NOT required)

- ❌ Degree Computer Science
- ❌ Kinh nghiệm IT
- ❌ Biết server administration
- ❌ Networking knowledge
- ❌ Cloud experience

---

## 🛠️ YÊU CẦU CÔNG CỤ (TOOLS)

### Giai đoạn đầu (Module 00)

**Cần cài đặt:**

1. **Terminal:**
   - Windows: Windows Terminal (từ Microsoft Store)
   - macOS: iTerm2 (khuyến nghị) hoặc Terminal built-in
   - Linux: Terminal built-in

2. **Code Editor:**
   - VS Code (recommended)
   - Extensions: Remote-WSL, GitLens

3. **Linux Environment:**
   - Windows: WSL2 + Ubuntu 22.04
   - macOS: Native terminal (zsh)
   - Linux: Native

**Tài khoản:**

- GitHub (free)
- Docker Hub (free)

### Các công cụ sẽ học dần

Không cần cài trước! Module tương ứng sẽ hướng dẫn:

- Git (Module 02)
- Docker (Module 05)
- NGINX (Module 07)
- Cloud accounts (Advanced Track)

---

## ⏰ YÊU CẦU THỜI GIAN (TIME COMMITMENT)

### Flexible Learning

Foundation Track **KHÔNG YÊU CẦU** timeline cố định.

Tùy vào:

- Thời gian rảnh của bạn
- Background hiện tại
- Tốc độ học

### Ước tính (Estimates)

**Full-time (8h/ngày, 5 ngày/tuần):**

- Foundation: 4-6 tuần

**Part-time (2h/ngày, 5 ngày/tuần):**

- Foundation: 3-4 tháng

**Casual (5h/tuần, weekend):**

- Foundation: 6-8 tháng

### Lời khuyên

- Quan trọng là **consistency** hơn speed
- Làm đúng > Làm nhanh
- Hiểu sâu > Học vẹt

---

## 🧠 YÊU CẦU TƯ DUY (MINDSET)

### ✅ DevOps Mindset

**1. Automation-first:**

- "Nếu làm 2 lần → Nên tự động hóa"
- Shell scripts, CI/CD pipelines

**2. Failure is normal:**

- Errors là cơ hội học
- Read error messages carefully
- Google/Stack Overflow là bạn

**3. Iterative improvement:**

- Version 1: Chạy được
- Version 2: Chạy tốt
- Version 3: Chạy đẹp

**4. Documentation:**

- Ghi chép mọi thứ
- README cho mọi project
- Comments trong code

### ❌ Anti-patterns

- ❌ "Chạy được rồi, đừng đụng vào"
- ❌ Manual deployments mãi mãi
- ❌ Không test trước khi deploy
- ❌ Không monitor sau khi deploy

---

## 📖 LEARNING RESOURCES PREPARATION

### Trước khi bắt đầu

**1. Tải toàn bộ tài liệu:**

```bash
# Via GitHub (khi đã học Git - Module 02)
git clone https://github.com/[repo]/DevOpsTraining.git

# Hoặc download ZIP từ GitHub
# Module 00 sẽ hướng dẫn chi tiết
```

**2. Setup folder structure:**

```
~/devops-learning/
├── DevOpsTraining/          # Tài liệu course
├── my-projects/              # Projects của bạn
│   ├── learning-journal/     # Integration 01
│   ├── landing-page/         # Integration 02
│   └── ...
└── notes/                    # Ghi chú cá nhân
```

**3. Join communities (optional):**

- DevOps Discord servers
- Reddit: r/devops
- Stack Overflow

---

## ✅ SELF-ASSESSMENT CHECKLIST

Trả lời YES/NO cho các câu sau:

### Phần cứng

- [ ] Tôi có máy tính đáp ứng yêu cầu tối thiểu
- [ ] Tôi có kết nối Internet ổn định
- [ ] Tôi có thể cài software trên máy (admin rights)

### Kỹ năng

- [ ] Tôi biết sử dụng máy tính cơ bản
- [ ] Tôi có thể đọc hiểu tiếng Anh kỹ thuật (ít nhất 50%)
- [ ] Tôi sẵn sàng học command line (dù chưa biết gì)

### Thời gian & động lực

- [ ] Tôi có ít nhất 5-10 hours/tuần để học
- [ ] Tôi kiên nhẫn với learning curve ban đầu
- [ ] Tôi muốn học DevOps (không bị ép buộc)

### Mindset

- [ ] Tôi không sợ lỗi/failures
- [ ] Tôi thích tự động hóa & optimize processes
- [ ] Tôi sẵn sàng Google & đọc docs

**KẾT QUẢ:**

- **10-12 YES:** Perfect! Bạn sẵn sàng 100%
- **7-9 YES:** Good! Bạn có thể bắt đầu
- **4-6 YES:** OK, nhưng cần chuẩn bị thêm (hardware/time)
- **< 4 YES:** Nên xem xét lại trước khi bắt đầu

---

## 🚀 GETTING STARTED

### Bước 1: Verify Prerequisites

Chạy checklist ở trên → Đảm bảo >= 7 YES

### Bước 2: Prepare Environment

- Đảm bảo máy tính đủ specs
- Kết nối Internet stable
- Tâm lý sẵn sàng học điều mới

### Bước 3: Start Module 00

Mở `FOUNDATION/00_SETUP/README.md` và bắt đầu!

Module 00 sẽ hướng dẫn:

- Cài đặt tất cả công cụ cần thiết
- Setup môi trường Linux
- VS Code configuration
- Tạo tài khoản GitHub/Docker Hub

### Bước 4: Follow the Roadmap

Xem `FOUNDATION/ROADMAP.md` để biết lộ trình đầy đủ.

---

## ❓ FAQ

**Q: Tôi chưa biết gì về IT, có học được không?**

A: **CÓ!** Foundation Track thiết kế cho zero background. Bắt đầu từ Module 00.

---

**Q: Tôi cần bao lâu để hoàn thành Foundation?**

A: Phụ thuộc thời gian bạn có. Trung bình 3-6 tháng part-time.

---

**Q: Tôi có cần laptop đắt tiền không?**

A: Không. Laptop tầm 10-15 triệu (i5, 8GB RAM) là đủ.

---

**Q: Học xong Foundation làm được gì?**

A: Deploy & monitor web app lên production. Apply Junior DevOps roles.

---

**Q: Tôi không giỏi Anh, có vấn đề không?**

A: Tài liệu tiếng Việt, nhưng thuật ngữ kỹ thuật giữ nguyên. Cần đọc hiểu cơ bản.

---

**Q: Tôi nên học Full-time hay Part-time?**

A: Part-time (2h/ngày) vẫn hiệu quả. Consistency > Intensity.

---

## 📞 NEED HELP?

Nếu không chắc mình đủ điều kiện:

1. Đọc kỹ checklist trên
2. Thử Module 00 - nếu quá khó → xem xét lại
3. Join community Discord để hỏi đáp

---

> **Nhớ:** DevOps là hành trình, không phải đích đến.
>
> **Bắt đầu từ Module 00 ngay! 🚀**
