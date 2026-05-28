# 🤖 AUDIT & FIX PROMPT - DevOps Journey

> **Prompt chuẩn để kiểm tra và sửa toàn bộ dự án DevOps-Journey**
>
> Dành cho AI hoặc người thay thế chưa từng biết project này.

---

## 📋 CONTEXT (Bối cảnh)

Bạn đang làm việc với **DevOps-Journey** - một dự án tài liệu học DevOps từ zero đến advanced. Dự án này là **song ngữ Anh-Việt** với quy tắc nghiêm ngặt.

**Vị trí Design Specifications:** `.DesignSpecifications/`

---

## 🎯 YOUR MISSION (Nhiệm vụ của bạn)

1. **ĐỌC KỸ** tất cả files trong `.DesignSpecifications/` trước khi làm bất cứ điều gì
2. **QUÉT TOÀN BỘ** files `.md` trong project
3. **PHÁT HIỆN** tất cả các vi phạm quy tắc
4. **SỬA NGAY** các vi phạm - KHÔNG hỏi lại
5. **BÁO CÁO** những gì đã sửa

---

## ⚠️ CRITICAL RULES (Quy tắc Quan trọng Nhất)

### RULE 1: ENGLISH FIRST - VIETNAMESE SECOND

**TUYỆT ĐỐI** tuân theo thứ tự: Tiếng Anh TRƯỚC, Tiếng Việt SAU.

| Element | ✅ Correct | ❌ Wrong |
|---------|-----------|----------|
| **Headers** | `## What is Docker? (Docker là gì?)` | `## Docker là gì? (What is Docker?)` |
| **Paragraphs** | `English first.\n\n*Vietnamese after.*` | Vietnamese first |
| **Lists** | `- English item *(Vietnamese)*` | `- Vietnamese *(English)*` |
| **Code Comments** | `# English (Vietnamese)` | `# Vietnamese (English)` |
| **Quiz Questions** | `What is X? *(X là gì?)*` | `X là gì? (What is X?)` |
| **Tables** | English in main cells | Vietnamese in main cells |

### RULE 2: MODULE STRUCTURE

Mỗi module (PHẢI có đủ 7 files + 1 folder):

```
Module_Name/
├── README.md        ✅ REQUIRED
├── LABS.md          ✅ REQUIRED
├── CHEATSHEET.md    ✅ REQUIRED
├── QUIZ.md          ✅ REQUIRED
├── EXERCISES.md     ✅ REQUIRED
├── PROJECT.md       ✅ REQUIRED
├── SOLUTIONS.md     ✅ REQUIRED
└── images/          ✅ REQUIRED
```

**Ngoại lệ:** Capstone modules chỉ cần README.md, SOLUTIONS.md, STARTER_CODE/, images/

### RULE 3: LAB REQUIREMENTS

Mỗi Lab trong LABS.md PHẢI có:

- ✅ **Objective** section
- ✅ **Prerequisites** section  
- ✅ **Steps** with numbered instructions
- ✅ **Verification** section (cách kiểm tra thành công)
- ✅ **Troubleshooting** section (lỗi thường gặp)
- ✅ **Cleanup** section (dọn dẹp)

### RULE 4: QUIZ FORMAT

```markdown
### Q1: Topic Name

English question here?

*(Vietnamese question translation?)*

- a) English option *(Vietnamese)*
- b) English option *(Vietnamese)*
- c) English option *(Vietnamese)*
- d) English option *(Vietnamese)*
```

---

## 📂 PROJECT STRUCTURE

```
DevOps-Journey/
├── .DesignSpecifications/    ← ĐỌC ĐẦU TIÊN
│   ├── CONTENT_GUIDELINES.md ← QUY TẮC CHÍNH
│   ├── ROADMAP_SPEC.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── TEMPLATE_MODULE.md
├── Track0_Setup_Environment/
├── Track1_Foundation_StaticWeb/
│   ├── 1.1_Linux_Bash/
│   ├── 1.2_Python_Basics/
│   ├── ...
│   └── 1.8_Capstone_Project/
├── Track2_Orchestration_Automation/
├── Track3_Cloud_Network_Design/
├── Track4_DevSecOps/
├── Track5_Career_Path/
├── resources/
├── README.md
├── CONTRIBUTING.md
└── BRANCH_PROTECTION_GUIDE.md
```

---

## 🔍 AUDIT CHECKLIST (Danh sách kiểm tra)

### Phase 1: Read Design Specs

```
[ ] Đọc .DesignSpecifications/CONTENT_GUIDELINES.md (QUAN TRỌNG NHẤT)
[ ] Đọc .DesignSpecifications/ROADMAP_SPEC.md
[ ] Đọc .DesignSpecifications/TEMPLATE_MODULE.md
[ ] Đọc .DesignSpecifications/IMPLEMENTATION_PLAN.md
```

### Phase 2: Structure Check

```
[ ] Kiểm tra mỗi module có đủ 7 files + images/
[ ] Liệt kê modules thiếu files
```

### Phase 3: Language Check (English First)

```
[ ] Quét tất cả headers - tìm Vietnamese đứng trước
[ ] Quét paragraphs - tìm Vietnamese đứng trước
[ ] Quét lists - tìm Vietnamese đứng trước
[ ] Quét code comments - tìm Vietnamese đứng trước
[ ] Quét QUIZ.md files - tìm questions Vietnamese trước
[ ] Quét tables - tìm Vietnamese trong main cells
```

### Phase 4: Lab Structure Check

```
[ ] Mỗi LABS.md có Verification section?
[ ] Mỗi LABS.md có Troubleshooting section?
[ ] Mỗi LABS.md có Cleanup section?
```

### Phase 5: Fix & Report

```
[ ] Sửa tất cả vi phạm tìm được
[ ] Tạo báo cáo những gì đã sửa
```

---

## 🛠️ HOW TO FIX (Cách sửa)

### Fix Vietnamese First → English First

**Before:**

```markdown
## Docker là gì? (What is Docker?)

Docker là nền tảng container hóa.

*Docker is a containerization platform.*
```

**After:**

```markdown
## What is Docker? (Docker là gì?)

Docker is a containerization platform.

*Docker là nền tảng container hóa.*
```

### Fix Quiz Questions

**Before:**

```markdown
### Q1

Docker image là gì?

- a) Container đang chạy
- b) Mẫu chỉ đọc
```

**After:**

```markdown
### Q1: Docker Image

What is a Docker image?

*(Docker image là gì?)*

- a) Running container *(Container đang chạy)*
- b) Read-only template *(Mẫu chỉ đọc)*
```

### Fix Code Comments

**Before:**

```bash
# Tạo thư mục mới
mkdir project
```

**After:**

```bash
# Create new directory (Tạo thư mục mới)
mkdir project
```

---

## 📊 GREP PATTERNS (Mẫu tìm kiếm)

Sử dụng các patterns này để tìm vi phạm:

```bash
# Tìm headers Vietnamese first
grep -rn "^##* [ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]" --include="*.md"

# Tìm dòng bắt đầu bằng Vietnamese
grep -rn "^(Nếu|Khi|Với|Trong|Sau|Trước|Cần|Mỗi|Tất cả|Bạn|Đây|Các|Để) " --include="*.md"

# Tìm code comments Vietnamese first
grep -rn "^# [ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]" --include="*.md"
```

---

## 📝 REPORT TEMPLATE (Mẫu báo cáo)

Sau khi hoàn thành, báo cáo theo format:

```markdown
## 📊 AUDIT REPORT - DevOps Journey

### 1. Files Checked
- Total: XX files
- Passed: XX files
- Fixed: XX files

### 2. Structure Issues Found & Fixed
| Module | Missing Files | Action |
|--------|--------------|--------|
| 5.5_Golang | All except README | Created |

### 3. Language Issues Found & Fixed  
| File | Issue | Fix |
|------|-------|-----|
| 1.4_Git/QUIZ.md | Vietnamese questions | Converted to English First |

### 4. Lab Structure Issues Fixed
| File | Missing Section | Added |
|------|-----------------|-------|
| 2.1_Docker/LABS.md | Troubleshooting | ✅ |

### 5. Summary
- ✅ All modules have required files
- ✅ All content follows English First rule
- ✅ All labs have required sections
```

---

## ⚡ QUICK START COMMANDS

```
1. FIRST: Read all files in .DesignSpecifications/
2. List all .md files: find_by_name with Extensions=["md"]
3. Check module structure: list_dir for each Track folder
4. Search for violations: grep_search with patterns above
5. Fix each violation: replace_file_content or write_to_file
6. Create report in IMPLEMENTATION_PLAN.md
```

---

## 🚫 DO NOT

- ❌ KHÔNG bỏ qua bất kỳ file nào
- ❌ KHÔNG hỏi xác nhận trước khi sửa lỗi rõ ràng
- ❌ KHÔNG thay đổi nội dung - chỉ sửa FORMAT
- ❌ KHÔNG sửa file trong `.DesignSpecifications/` - đó là quy tắc
- ❌ KHÔNG dịch thuật ngữ kỹ thuật (Container, Docker, Pipeline...)

---

## ✅ DO

- ✅ Đọc Design Specs TRƯỚC KHI làm bất cứ gì
- ✅ Sửa ngay khi phát hiện lỗi
- ✅ Giữ nguyên nghĩa - chỉ đảo thứ tự English/Vietnamese
- ✅ Báo cáo chi tiết sau khi hoàn thành
- ✅ Kiểm tra lại sau khi sửa

---

## 📞 ESCALATION

Chỉ hỏi owner khi:

- Không chắc nội dung đúng hay sai (không phải format)
- Phát hiện lỗi logic trong content
- Cần tạo nội dung mới (không phải sửa format)

---

*Last Updated: 2026-01-16*

**Prompt này được tạo bởi ThanhRòm để chuẩn hóa quy trình audit DevOps-Journey.**
