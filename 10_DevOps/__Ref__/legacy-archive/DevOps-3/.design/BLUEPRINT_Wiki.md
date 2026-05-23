# 📐 BLUEPRINT - DevOps Training Project

> **Master Design Document**
>
> Created: 2025-01-24  
> Last Updated: 2025-01-24  
> Version: 1.0.0

---

## 📋 MỤC LỤC

1. [Vision & Principles](#vision--principles)
2. [Project Structure](#project-structure)
3. [Content Philosophy](#content-philosophy)
4. [Module Templates](#module-templates)
5. [Naming Conventions](#naming-conventions)
6. [Quality Standards](#quality-standards)
7. [Implementation Phases](#implementation-phases)

---

## 1. VISION & PRINCIPLES

### Vision Statement

Tạo tài liệu đào tạo DevOps **toàn diện, chi tiết, chuyên sâu** nhất bằng tiếng Việt, phục vụ từ người hoàn toàn mới (zero) đến expert/mastery level.

### Core Principles

#### P1: "Không sợ dài"

- ✅ Càng chi tiết càng tốt
- ✅ Giải thích sâu bản chất vấn đề
- ✅ Nhiều ví dụ, nhiều scenarios
- ❌ Không rút gọn để "ngắn gọn"

#### P2: "Hiểu WHY trước HOW"

- ✅ Giải thích tại sao cần công cụ/khái niệm
- ✅ Bối cảnh lịch sử, vấn đề giải quyết
- ✅ So sánh alternatives
- ❌ Không chỉ liệt kê commands

#### P3: "Thực hành thực chiến"

- ✅ Mỗi module có labs hands-on
- ✅ Scenarios từ production thật
- ✅ Projects demo working code
- ❌ Không chỉ lý thuyết suông

#### P4: "Fix logic flow"

- ✅ Tools được học TRƯỚC KHI dùng
- ✅ Ví dụ: Download ZIP → Học Git → Dùng git
- ❌ KHÔNG dùng `git clone` trước khi học Git

#### P5: "Accessibility"

- ✅ Tiếng Việt dễ hiểu
- ✅ Technical terms: Giữ tiếng Anh + giải thích
- ✅ Ẩn dụ đời thường
- ✅ Support mọi OS (Windows/macOS/Linux)

---

## 2. PROJECT STRUCTURE

### Top-Level Organization

```
DevOpsTraining/
├── README.md                 # Hub chính, điều hướng
├── LICENSE                   # MIT
├── CONTRIBUTING.md           # Guidelines
├── CHANGELOG.md              # Version history
│
├── .design/                  # Meta-documentation (this folder)
│   ├── BLUEPRINT.md          # Master plan (this file)
│   ├── PROGRESS.md           # What's done, what's next
│   ├── DECISIONS.md          # Design decisions & rationale
│   └── TEMPLATES/            # Content templates
│
├── FOUNDATION/               # Track 1: Zero → Junior
│   ├── README.md             # Track overview
│   ├── 00_SETUP/             # Module structure (see below)
│   ├── 01_LINUX_BASICS/
│   ├── ... (08 modules total)
│   └── FINAL_PROJECT/
│
├── ADVANCED/                 # Track 2: Junior → Mastery
│   ├── README.md
│   ├── 00_ASSESSMENT/
│   ├── 01-16 modules
│   └── CAPSTONE_PROJECT/
│
├── PROJECTS/                 # Demo applications
│   ├── simple-html-site/     # Foundation project
│   ├── counter-app-basic/    # Foundation final
│   └── counter-app-advanced/ # Advanced capstone
│
├── SHARED/                   # Cross-track resources
│   ├── GLOSSARY.md           # 1000+ terms
│   ├── CHEATSHEETS/
│   ├── TROUBLESHOOTING/
│   ├── INTERVIEW_PREP/
│   ├── CAREER/
│   └── REFERENCES/
│
└── scripts/                  # Utility scripts
    ├── setup/
    ├── verification/
    └── utils/
```

### Module Structure (Standard)

Mỗi module PHẢI có cấu trúc sau:

```
XX_MODULE_NAME/
├── README.md           # Lý thuyết (30-50 pages)
├── LABS.md             # Thực hành step-by-step (15-25 labs)
├── EXERCISES.md        # Bài tập củng cố (50-100 exercises)
├── SOLUTIONS.md        # Đáp án exercises
├── SCENARIOS.md        # 10 tình huống thực tế
├── QUIZ.md             # 30 câu trắc nghiệm
├── CHEATSHEET.md       # Quick reference
├── TERMINOLOGY.md      # Thuật ngữ A-Z
├── FURTHER_READING.md  # Tài liệu bổ sung
└── assets/             # Images, diagrams, code samples
```

---

## 3. CONTENT PHILOSOPHY

### README.md Structure (Per Module)

**Minimum 30 pages**, bao gồm:

#### Part 1: Introduction (10%)

```markdown
## 1. Giới thiệu
- Câu chuyện mở đầu (real story)
- [Topic] là gì?
- Tại sao cần học?
- Lịch sử / Bối cảnh

## 2. Bảng thuật ngữ
| Thuật ngữ | Phiên âm | Giải thích |
```

#### Part 2: Core Concepts (60%)

```markdown
## 3. Khái niệm cơ bản
- Giải thích từ zero
- Ẩn dụ dễ hiểu
- Diagrams (Mermaid)
- So sánh alternatives

## 4. Deep Dive
- Internals
- How it works under the hood
- Best practices
- Common patterns

## 5. Hands-on Examples
- 5-10 ví dụ có code complete
- Expected output
- Explanation
```

#### Part 3: Advanced (20%)

```markdown
## 6. Advanced Topics
- Performance considerations
- Security implications
- Troubleshooting
- Production tips

## 7. Common Mistakes
- Pitfalls to avoid
- Anti-patterns
- How to debug
```

#### Part 4: Summary (10%)

```markdown
## 8. Tổng kết
- Key takeaways
- Checklist
- Preview next module
- Further reading
```

### LABS.md Structure

**Format chuẩn:**

```markdown
# Labs: Module XX - [NAME]

## 🎯 Objectives
[What student will achieve]

## 📋 Prerequisites
[What they need before starting]

## Lab 1: [Descriptive Title]

**Time:** X minutes

**Steps:**
1. **Step 1 description**
   ```bash
   command here
   ```

   **Expected output:**

   ```
   exact output
   ```

   **Explanation:**
   [Why this output, what it means]

1. **Step 2...**

**Verification:**
[How to confirm lab success]

**Troubleshooting:**
[Common errors và fixes]

```

### SCENARIOS.md Structure

**10 scenarios per module:**

```markdown
## Scenario X: [Catchy Title]

**🎬 Context (The Story):**
[2-3 paragraphs setting the scene]

**🚨 The Problem:**
[What went wrong]

**🎯 Your Task:**
[What student needs to do]

**💡 Hints:**
<details>
<summary>Click for hints</summary>
[Progressive hints]
</details>

**✅ Solution:**
[In SOLUTIONS.md, not inline]

**📚 What You Learn:**
- Lesson 1
- Lesson 2
- Prevention strategy
```

---

## 4. MODULE TEMPLATES

### Foundation Track Modules

| Module | Pages | Labs | Exercises | Scenarios |
|--------|-------|------|-----------|-----------|
| 00_SETUP | 30 | 6 | 20 | 5 |
| 01_LINUX_BASICS | 40 | 20 | 50 | 10 |
| 02_GIT_GITHUB | 35 | 15 | 40 | 10 |
| 03_NETWORKING_INTRO | 25 | 10 | 30 | 8 |
| 04_HTML_CSS_JS | 30 | 12 | 35 | 8 |
| 05_DOCKER_BASICS | 35 | 18 | 45 | 10 |
| 06_CI_BASICS | 30 | 10 | 25 | 8 |
| 07_WEB_SERVERS | 25 | 8 | 20 | 8 |
| 08_DEPLOYMENT | 25 | 8 | 20 | 8 |
| FINAL_PROJECT | 20 | 1 | - | - |

**Total Foundation:** ~295 pages, 108 labs, 285 exercises, 75 scenarios

### Advanced Track Modules

[Similar structure, 35-50 pages each]

**Total Advanced:** ~700 pages, 320 labs, 960 exercises, 160 scenarios

---

## 5. NAMING CONVENTIONS

### Files

- `README.md` - ALWAYS capitalized
- `LABS.md` - ALWAYS capitalized
- `EXERCISES.md`, `SOLUTIONS.md`, `SCENARIOS.md` - Capitalized
- `.md` - ALWAYS markdown extension

### Folders

- `XX_NAME/` - Number prefix + UPPERCASE_WITH_UNDERSCORES
- Modules: `00_`, `01_`, `02_`, ... `15_`, `16_`
- Projects: lowercase `simple-html-site/`, `counter-app/`

### Variables in Code

- Bash: `snake_case` for variables
- Python: `snake_case` for functions, `PascalCase` for classes
- YAML: `kebab-case` for keys

### Git Commits

```
type: Short description

type = docs | feat | fix | refactor | style
```

Examples:

- `docs: Complete Module 00 SETUP README`
- `feat: Add verification scripts`
- `fix: Correct kubectl command in Lab 05`

---

## 6. QUALITY STANDARDS

### Code Examples

**ALL code examples MUST have:**

1. ✅ Language specified in fence
2. ✅ Comments explaining what it does
3. ✅ Expected output shows
4. ✅ Tested and working
5. ✅ Error handling mentioned

**Good example:**

```markdown
```bash
# Check Docker version
docker --version

# Expected output:
# Docker version 24.0.7, build afdd53b

# If error "command not found":
# Docker is not installed or not in PATH
\```
```

### Markdown Quality

- ✅ No broken links
- ✅ All images have alt text
- ✅ Tables formatted properly
- ✅ Lists consistent (either `-` or `*`, not mixed)
- ✅ Heading hierarchy (no skip levels)
- ✅ Code blocks have language tags

### Vietnamese Language

- ✅ Dấu đầy đủ, chính xác
- ✅ Technical terms: Tiếng Anh + giải thích
  - Example: "Container - môi trường cô lập để chạy ứng dụng"
- ✅ Tránh Vietlish: "check mail" → "kiểm tra email"
- ✅ Nhất quán thuật ngữ (không đổi term giữa chừng)

### Screenshots/Diagrams

- ✅ Use Mermaid for diagrams (text-based, version control friendly)
- ✅ Screenshots only when absolutely necessary
- ✅ If screenshot: Annotate với arrows/text
- ✅ Alt text describing image

---

## 7. IMPLEMENTATION PHASES

### Phase 1: Foundation Core (Week 1-6)

**Goal:** Complete FOUNDATION track, ready for learners

#### Sprint 1 (Week 1)

- [x] Project setup & structure
- [x] Main README.md
- [x] Module 00: SETUP complete
- [ ] Module 01: LINUX_BASICS complete

#### Sprint 2 (Week 2)

- [ ] Module 02: GIT_GITHUB
- [ ] Module 03: NETWORKING_INTRO
- [ ] Simple HTML site starter project

#### Sprint 3 (Week 3)

- [ ] Module 04: HTML_CSS_JS_BASICS
- [ ] Module 05: DOCKER_BASICS

#### Sprint 4 (Week 4)

- [ ] Module 06: CI_BASICS
- [ ] Module 07: WEB_SERVERS_BASICS
- [ ] Module 08: DEPLOYMENT_BASICS

#### Sprint 5 (Week 5)

- [ ] FINAL_PROJECT setup
- [ ] Counter-app-basic project
- [ ] All Foundation SHARED resources

#### Sprint 6 (Week 6)

- [ ] Beta testing with 5-10 learners
- [ ] Bug fixes
- [ ] Polish & improvements

**Deliverable:** Foundation track ready for public beta

---

### Phase 2: Advanced Track (Week 7-14)

#### Sprint 7-12 (Week 7-12)

- [ ] Advanced modules 01-16
- [ ] Counter-app-advanced project
- [ ] Production-ready examples

#### Sprint 13-14 (Week 13-14)

- [ ] Advanced CAPSTONE project
- [ ] Beta testing Advanced track
- [ ] Final polish

**Deliverable:** Full course (Foundation + Advanced)

---

### Phase 3: Ecosystem & Community (Week 15+)

- [ ] Video tutorials
- [ ] Interactive labs platform
- [ ] Certificate system
- [ ] Discord community active
- [ ] Monthly office hours
- [ ] Alumni network

---

## 8. METRICS & KPIs

### Content Metrics (Target)

| Metric | Foundation | Advanced | Total |
|--------|------------|----------|-------|
| **Pages** | 300-400 | 700-800 | 1000-1200 |
| **Labs** | 100-120 | 280-320 | 380-440 |
| **Exercises** | 280-320 | 850-960 | 1130-1280 |
| **Scenarios** | 70-80 | 140-160 | 210-240 |
| **Code Examples** | 200+ | 400+ | 600+ |

### Quality Metrics

- ✅ 0 broken links
- ✅ 100% code examples tested
- ✅ Vietnamese spelling: 99%+ correct
- ✅ All READMEs 30+ pages
- ✅ Every module has all 9 standard files

### Learner Success Metrics (Post-Launch)

- 🎯 80%+ completion rate for Foundation
- 🎯 70%+ pass rate for final project
- 🎯 4.5+/5.0 average rating
- 🎯 50%+ Foundation → Advanced conversion

---

## 9. DESIGN DECISIONS LOG

### Decision 001: Git After Download

**Date:** 2025-01-24  
**Decision:** Download materials via ZIP, learn Git in Module 02  
**Rationale:** Avoid confusion, teach tools before using  
**Impact:** Module 00 setup flow changed

### Decision 002: Two Separate Tracks

**Date:** 2025-01-24  
**Decision:** Foundation (8 weeks) + Advanced (12 weeks) separate  
**Rationale:** Clear progression, prevent overwhelm  
**Impact:** Different complexity levels, different projects

### Decision 003: HTML/CSS/JS in Foundation

**Date:** 2025-01-24  
**Decision:** Add Module 04 for frontend basics  
**Rationale:** Students need to understand what they deploy  
**Impact:** Added 1 module, 30 pages, projects easier to understand

### Decision 004: Verification Scripts

**Date:** 2025-01-24  
**Decision:** Auto verification for environment setup  
**Rationale:** Reduce support burden, instant feedback  
**Impact:** Students confident before Module 01

[More decisions added as project progresses]

---

## 10. REVISION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-01-24 | Initial blueprint | ThanhRòm |

---

<div align="center">

**This is a living document.**  
Updated as project evolves.

**Last Review:** 2025-01-24

</div>
