# 🔄 KẾ HOẠCH TÁI TỔ CHỨC DEV-KNOWLEDGE

> **Phiên bản:** 1.0  
> **Ngày tạo:** 2026-05-07  
> **Tác giả:** AI Assistant  
> **Mục tiêu:** Chuyển đổi từ cấu trúc hỗn loạn (folder trùng số) sang cấu trúc rõ ràng, duy nhất, dễ bảo trì

---

## 1. PHÂN TÍCH HIỆN TRẠNG

### 1.1. Vấn đề chính

| Vấn đề | Mô tả | Hệ quả |
|--------|-------|--------|
| **Trùng lặp số thứ tự** | 22 folders có cùng category nhưng số khác nhau | Người dùng không biết folder nào là chính |
| **Không khớp tài liệu** | README.md ghi 1 cấu trúc, thực tế khác | MASTER-CATALOG không thể map đúng |
| **Content phân tán** | Cùng 1 topic nằm ở 2-3 folder khác nhau | Mất thời gian tìm kiếm, dễ duplicate |
| **Thiếu quy ước** | Có folder đặt tên kebab-case, có folder PascalCase | Không nhất quán |

### 1.2. Danh sách folder trùng lặp (phân tích từ `ls -la`)

```
01-CS-Fundamentals (28 items)     vs    01-Fundamentals (13 items)
02-Languages (11 items)           vs    05-Languages (38 items) ⭐
03-Terminal-OS (9 items)          vs    03-Frontend (9 items)
04-Networking (17 items)          vs    04-Backend (8 items)
05-Databases (8 items)            vs    08-Databases (29 items) ⭐
06-DevOps (50 items) ⭐            vs    06-Frontend (62 items) ⭐
                                   vs    09-DevOps (57 items)
07-Cloud (2 items)                vs    10-Cloud (24 items) ⭐
08-Architecture (7 items)         vs    11-Architecture (17 items) ⭐
09-Security (3 items)             vs    12-Security (19 items) ⭐
10-AI-ML (4 items)                vs    14-AI-ML (20 items) ⭐
11-Testing (1 items)              vs    13-Testing (17 items) ⭐
12-Soft-Skills (1 items)          vs    21-Soft-Skills (11 items) ⭐
13-Data-Engineering (1 items)     vs    15-Data-Engineering (12 items) ⭐
14-Tools (15 items) ⭐             (không có đối thủ)
```

> **⭐ = Folder chính (có nhiều content hơn, giữ lại)**

---

## 2. THIẾT KẾ MỚI

### 2.1. Nguyên tắc thiết kế

| Nguyên tắc | Áp dụng |
|------------|---------|
| **Single Source of Truth** | Mỗi topic chỉ tồn tại ở 1 folder duy nhất |
| **Logical Grouping** | Group theo "layer" từ thấp đến cao |
| **Progressive Disclosure** | Số thứ tự thể hiện thứ tự học logic |
| **Extensibility** | Để chừng khoảng số cho future expansion |
| **Consistency** | Một quy ước đặt tên duy nhất |

### 2.2. Cấu trúc mới (đề xuất)

```
Dev-Knowledge-v2/
│
├── 00-META/                          # Meta & Project files
│   ├── README.md                     # Giới thiệu chính
│   ├── CONTRIBUTING.md                 # Hướng dẫn đóng góp
│   ├── MASTER-CATALOG.md             # Index toàn bộ
│   ├── SUMMARY.md                    # Tóm tắt nhanh
│   ├── _templates/                   # Templates cho bài viết
│   └── _scripts/                     # Scripts hỗ trợ
│
├── 10-FOUNDATIONS/                   # 🧱 Kiến thức nền tảng (layer 1)
│   ├── 00-roadmaps/                  # Lộ trình các role
│   ├── 10-computer-science/            # CS fundamentals
│   ├── 20-data-structures-algorithms/ # DSA
│   ├── 30-git-version-control/         # Git & GitHub/GitLab
│   ├── 40-terminal-shell/              # Terminal, Bash, CLI
│   ├── 50-networking-basics/           # HTTP, TCP/IP, DNS
│   └── 60-operating-systems/           # Linux, OS concepts
│
├── 20-LANGUAGES/                     # 💻 Ngôn ngữ (layer 2)
│   ├── 00-overview/
│   ├── 10-python/
│   ├── 20-javascript/
│   ├── 30-typescript/
│   ├── 40-go/
│   ├── 50-java/
│   ├── 60-csharp/
│   └── 90-other/                       # Rust, C++, v.v.
│
├── 30-FRONTEND/                      # 🎨 Frontend (layer 3)
│   ├── 00-core-web/                    # HTML, CSS, DOM
│   ├── 10-react/
│   ├── 20-vue/
│   ├── 30-angular/
│   ├── 40-nextjs/
│   ├── 50-state-management/
│   ├── 60-build-tools/
│   └── 70-testing/                     # Frontend testing
│
├── 40-BACKEND/                       # ⚙️ Backend (layer 3)
│   ├── 00-core-concepts/               # API design, REST, GraphQL
│   ├── 10-frameworks/                   # FastAPI, Express, Django...
│   ├── 20-databases/                     # SQL, NoSQL, ORM
│   ├── 30-messaging-caching/             # Redis, Kafka, MQ
│   ├── 40-authentication/
│   └── 50-testing/
│
├── 50-INFRASTRUCTURE/                # 🔧 DevOps & Infra (layer 4)
│   ├── 00-containers/                   # Docker, Podman
│   ├── 10-kubernetes/
│   ├── 20-cicd/                          # GitHub Actions, GitLab CI
│   ├── 30-infrastructure-as-code/        # Terraform, Ansible
│   ├── 40-monitoring-observability/      # Prometheus, Grafana
│   └── 50-cloud-platforms/               # AWS, Azure, GCP
│
├── 60-ARCHITECTURE/                  # 🏗️ Architecture (layer 5)
│   ├── 00-design-patterns/
│   ├── 10-system-design/
│   ├── 20-microservices/
│   ├── 30-clean-architecture/
│   └── 40-domain-driven-design/
│
├── 70-SECURITY/                      # 🔐 Security (layer 5)
│   ├── 00-web-security/
│   ├── 10-authentication-authorization/
│   ├── 20-encryption-cryptography/
│   ├── 30-devsecops/
│   └── 40-compliance/
│
├── 80-SPECIALIZED/                   # 🚀 Chuyên sâu (layer 6)
│   ├── 00-ai-machine-learning/
│   ├── 10-data-engineering/
│   ├── 20-mobile-development/
│   ├── 30-game-development/
│   ├── 40-blockchain-web3/
│   ├── 50-embedded-iot/
│   └── 60-testing-qa/                    # Testing as domain
│
└── 90-CAREER/                        # 💼 Career & Soft Skills
    ├── 00-soft-skills/
    ├── 10-interview-prep/
    ├── 20-career-growth/
    └── 30-tools-productivity/
```

### 2.3. Giải thích cấu trúc số 2-digit

| Range | Layer | Ý nghĩa |
|-------|-------|---------|
| `00` | META | Project metadata, templates |
| `10-19` | FOUNDATIONS | Đòi hỏi ít hoặc không đòi hỏi prerequisite |
| `20-29` | LANGUAGES | Có thể học song song với Foundations |
| `30-39` | FRONTEND | Cần Foundations + ít nhất 1 Language |
| `40-49` | BACKEND | Cần Foundations + ít nhất 1 Language |
| `50-59` | INFRASTRUCTURE | Cần hiểu Backend + Linux basics |
| `60-69` | ARCHITECTURE | Cần kinh nghiệm FE/BE thực tế |
| `70-79` | SECURITY | Cần hiểu sâu tất cả layers trên |
| `80-89` | SPECIALIZED | Domain-specific, optional |
| `90-99` | CAREER | Không liên quan technical depth |

**Ưu điểm của 2-digit:**
- Dễ insert thêm topic giữa (e.g., `15-` nếu cần thêm 1 foundations topic)
- Không bị overflow khi mở rộng (còn 10 slot mỗi layer)
- Visual rõ ràng hơn 1-digit

---

## 3. KẾ HOẠCH DI CHUYỂN CONTENT

### 3.1. Mapping từ folder cũ → mới

#### Block 1: Foundations (Priority: 🔴 HIGH)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `01-CS-Fundamentals/cs/` | 7 items | `10-FOUNDATIONS/10-computer-science/` | Move |
| `01-CS-Fundamentals/dsa/` | 14 items | `10-FOUNDATIONS/20-data-structures-algorithms/` | Move |
| `01-CS-Fundamentals/programming/` | 7 items | `10-FOUNDATIONS/10-computer-science/programming-paradigms/` | Move |
| `01-Fundamentals/cs/` (2 items) | Trùng lặp | — | Review, merge nếu unique |
| `01-Fundamentals/dsa/` (1 item) | Trùng lặp | — | Review, merge nếu unique |
| `01-Fundamentals/git/` | 3 items | `10-FOUNDATIONS/30-git-version-control/` | Move |
| `01-Fundamentals/terminal/` | 2 items | `10-FOUNDATIONS/40-terminal-shell/` | Move |
| `01-Fundamentals/networking/` | 4 items | `10-FOUNDATIONS/50-networking-basics/` | Move |
| `01-Fundamentals/how-internet-works.md` | 1 file | `10-FOUNDATIONS/50-networking-basics/` | Move |
| `02-Version-Control/` | 5 items | `10-FOUNDATIONS/30-git-version-control/` | Move & Merge |
| `03-Terminal-OS/` | 9 items | `10-FOUNDATIONS/40-terminal-shell/` & `10-FOUNDATIONS/60-operating-systems/` | Split |
| `04-Networking/` | 17 items | `10-FOUNDATIONS/50-networking-basics/` | Move |

#### Block 2: Languages (Priority: 🔴 HIGH)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `02-Languages/` (11 items) | + `05-Languages/` (38 items) | `20-LANGUAGES/` | Merge toàn bộ |
| Cấu trúc hiện: `python/`, `javascript/`, `typescript/`, `go/`... | Giữ nguyên subfolders | `20-LANGUAGES/10-python/`, `20-LANGUAGES/20-javascript/`... | Rename prefix |

#### Block 3: Frontend (Priority: 🟡 MEDIUM)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `03-Frontend/` (9 items) | + `06-Frontend/` (62 items) | `30-FRONTEND/` | Merge |
| `html/`, `css/` | Core web | `30-FRONTEND/00-core-web/` | Move |
| `react/`, `vue/`, `angular/` | Frameworks | `30-FRONTEND/10-react/`, etc. | Rename prefix |
| `nextjs/`, `nuxtjs/`, `astro/` | Meta-frameworks | `30-FRONTEND/40-nextjs/`, etc. | Rename prefix |
| `state-management/` | State | `30-FRONTEND/50-state-management/` | Move |
| `build-tools/` | Build | `30-FRONTEND/60-build-tools/` | Move |
| `testing/` (FE specific) | Testing | `30-FRONTEND/70-testing/` | Move |

#### Block 4: Backend (Priority: 🟡 MEDIUM)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `04-Backend/` (8 items) | + `07-Backend/` (39 items) | `40-BACKEND/` | Merge |
| `api-design/` | API concepts | `40-BACKEND/00-core-concepts/` | Move |
| `frameworks/` | BE frameworks | `40-BACKEND/10-frameworks/` | Move |
| `realtime/`, `messaging/` | Realtime | `40-BACKEND/30-messaging-caching/` | Move |
| `authentication/` nếu có | Auth | `40-BACKEND/40-authentication/` | Move |

#### Block 5: Databases (Priority: 🟡 MEDIUM)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `05-Databases/` (8 items) | + `08-Databases/` (29 items) | `40-BACKEND/20-databases/` | Merge & Move |
| Lưu ý: Đưa vào Backend vì là dependency của BE |

#### Block 6: DevOps & Infrastructure (Priority: 🟡 MEDIUM)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `06-DevOps/` (50 items) | + `09-DevOps/` (57 items) | `50-INFRASTRUCTURE/` | Merge toàn bộ |
| `docker/` | Containers | `50-INFRASTRUCTURE/00-containers/` | Move |
| `kubernetes/` | K8s | `50-INFRASTRUCTURE/10-kubernetes/` | Move |
| `cicd/` | CI/CD | `50-INFRASTRUCTURE/20-cicd/` | Move |
| `iac/` | IaC | `50-INFRASTRUCTURE/30-infrastructure-as-code/` | Move |
| `observability/` | Monitoring | `50-INFRASTRUCTURE/40-monitoring-observability/` | Move |
| `nginx/`, `web-servers/` | Web servers | `50-INFRASTRUCTURE/00-containers/web-servers/` hoặc riêng | Review |

#### Block 7: Cloud (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `07-Cloud/` (2 items) | + `10-Cloud/` (24 items) | `50-INFRASTRUCTURE/50-cloud-platforms/` | Merge & Move |
| Note: Cloud là sub-category của Infrastructure |

#### Block 8: Architecture (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `08-Architecture/` (7 items) | + `11-Architecture/` (17 items) | `60-ARCHITECTURE/` | Merge |
| `design-patterns/` | Patterns | `60-ARCHITECTURE/00-design-patterns/` | Move |
| `system-design/` | System Design | `60-ARCHITECTURE/10-system-design/` | Move |
| `microservices/` | Microservices | `60-ARCHITECTURE/20-microservices/` | Move |
| `clean-architecture/`, `ddd/` | Methodologies | `60-ARCHITECTURE/30-clean-architecture/`, `40-domain-driven-design/` | Move |

#### Block 9: Security (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `09-Security/` (3 items) | + `12-Security/` (19 items) | `70-SECURITY/` | Merge |
| `01-web-security-fundamentals.md` | Web security | `70-SECURITY/00-web-security/` | Move |
| `02-authentication.md` | Auth | `70-SECURITY/10-authentication-authorization/` | Move |
| `encryption/` | Crypto | `70-SECURITY/20-encryption-cryptography/` | Move |

#### Block 10: Testing (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `11-Testing/` (1 item) | + `13-Testing/` (17 items) | `80-SPECIALIZED/60-testing-qa/` | Merge & Move |
| Note: Testing có thể là cross-cutting concern nhưng để trong Specialized cho gọn |

#### Block 11: AI/ML (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `10-AI-ML/` (4 items) | + `14-AI-ML/` (20 items) | `80-SPECIALIZED/00-ai-machine-learning/` | Merge |
| `llm/`, `deep-learning/`, `mlops/` | Sub-topics | Giữ nguyên cấu trúc sub | Move |

#### Block 12: Data Engineering (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `13-Data-Engineering/` (1 item) | + `15-Data-Engineering/` (12 items) | `80-SPECIALIZED/10-data-engineering/` | Merge |

#### Block 13: Other Specialized (Priority: ⚪ ON-DEMAND)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `16-Mobile/` | Mobile | `80-SPECIALIZED/20-mobile-development/` | Move |
| `17-GameDev/` | Game | `80-SPECIALIZED/30-game-development/` | Move |
| `18-Blockchain/` | Blockchain | `80-SPECIALIZED/40-blockchain-web3/` | Move |
| `19-Embedded-IoT/` | Embedded | `80-SPECIALIZED/50-embedded-iot/` | Move |

#### Block 14: Tools & Career (Priority: 🟢 LOW)

| Folder cũ | Nội dung | → Folder mới | Hành động |
|-----------|----------|--------------|-----------|
| `14-Tools/` (15 items) | Tools | `90-CAREER/30-tools-productivity/` | Move |
| `12-Soft-Skills/` (1 item) | + `21-Soft-Skills/` (11 items) | `90-CAREER/00-soft-skills/` | Merge |
| Nội dung interview, career | Career | `90-CAREER/10-interview-prep/`, `20-career-growth/` | Tạo mới/organize |

---

## 4. CẬP NHẬT TÀI LIỆU

### 4.1. File cần cập nhật

| File | Thay đổi |
|------|----------|
| `README.md` | Cập nhật cấu trúc thư mục mới, navigation |
| `CONTRIBUTING.md` | Quy ước đặt tên mới, 2-digit system |
| `MASTER-CATALOG.md` | Remap toàn bộ đường dẫn |
| `SUMMARY.md` | Tóm tắt cấu trúc mới |
| Templates | Cập nhật path examples trong templates |

### 4.2. Nội dung README.md mới cần có

```markdown
# 🚀 Dev-Knowledge v2 — Kho Kiến Thức Lập Trình

## Cấu trúc thư mục (2-digit system)

| Code | Thư mục | Mô tả |
|------|---------|-------|
| 00 | META | Templates, scripts, project docs |
| 10-19 | FOUNDATIONS | CS, DSA, Git, Terminal, Networking |
| 20 | LANGUAGES | Python, JS/TS, Go, Java, etc. |
| 30 | FRONTEND | HTML/CSS, React, Vue, Next.js |
| 40 | BACKEND | API, Frameworks, Databases |
| 50 | INFRASTRUCTURE | Docker, K8s, CI/CD, Cloud |
| 60 | ARCHITECTURE | Patterns, System Design |
| 70 | SECURITY | Auth, Crypto, DevSecOps |
| 80 | SPECIALIZED | AI/ML, Data, Mobile, Game |
| 90 | CAREER | Soft skills, Interview, Tools |

## Quick Navigation

- 🔰 Người mới: Bắt đầu từ `10-FOUNDATIONS/`
- 🎨 Frontend Dev: `20-LANGUAGES/` → `30-FRONTEND/`
- ⚙️ Backend Dev: `20-LANGUAGES/` → `40-BACKEND/`
- 🔧 DevOps: `10-FOUNDATIONS/` → `50-INFRASTRUCTURE/`
```

---

## 5. KẾ HOẠCH THỰC HIỆN

### 5.1. Phân pha (Roadmap)

```
Pha 1: Setup (Ngày 1)
├── Tạo thư mục mới Dev-Knowledge-v2/
├── Copy _templates/, _scripts/ vào 00-META/
├── Tạo folder structure trống
└── Viết README-v2.md tóm tắt

Pha 2: Migration Foundations (Ngày 2-3)
├── Merge 01-CS-Fundamentals + 01-Fundamentals
├── Merge 02-Version-Control
├── Split 03-Terminal-OS
├── Merge 04-Networking
└── Verify + cập nhật MASTER-CATALOG

Pha 3: Migration Core Dev (Ngày 4-6)
├── Merge + move 02/05-Languages → 20-LANGUAGES
├── Merge + move 03/06-Frontend → 30-FRONTEND
├── Merge + move 04/07-Backend → 40-BACKEND
└── Merge 05/08-Databases → 40-BACKEND/20-databases

Pha 4: Migration Infrastructure (Ngày 7-8)
├── Merge 06/09-DevOps → 50-INFRASTRUCTURE
├── Merge 07/10-Cloud → 50-INFRASTRUCTURE/50-cloud
└── Move web servers, observability

Pha 5: Migration Advanced (Ngày 9-10)
├── Merge 08/11-Architecture → 60-ARCHITECTURE
├── Merge 09/12-Security → 70-SECURITY
├── Move Testing → 80-SPECIALIZED/60-testing-qa
└── Move AI/ML, Data Eng, Mobile, etc.

Pha 6: Migration Career (Ngày 11)
├── Merge 12/21-Soft-Skills → 90-CAREER/00-soft-skills
├── Move 14-Tools → 90-CAREER/30-tools-productivity
└── Organize interview prep content

Pha 7: Cleanup & Launch (Ngày 12-13)
├── Cập nhật toàn bộ internal links
├── Cập nhật MASTER-CATALOG.md
├── Cập nhật CONTRIBUTING.md
├── Backup và xóa folder cũ
└── Final review
```

### 5.2. Checklist chi tiết mỗi pha

#### Template cho mỗi folder merge

```markdown
## Merge Checklist: [Folder A] + [Folder B] → [New Folder]

- [ ] 1. Tạo folder đích mới
- [ ] 2. Copy toàn bộ từ folder chính (nhiều content hơn)
- [ ] 3. So sánh folder phụ, identify unique content
- [ ] 4. Copy unique content sang folder đích
- [ ] 5. Rename files theo quy ước: `XX-topic-name.md`
- [ ] 6. Update internal links trong các file đã move
- [ ] 7. Tạo index.md tổng hợp cho folder mẹ
- [ ] 8. Mark old folders as deprecated (thêm _DEPRECATED suffix)
- [ ] 9. Update MASTER-CATALOG
```

---

## 6. RỦI RO & GIẢI PHÁP

| Rủi ro | Xác suất | Impact | Giải pháp |
|--------|----------|--------|-----------|
| Broken internal links | Cao | Trung bình | Dùng script tìm/replace; manual review |
| Mất content trong merge | Trung bình | Cao | Checklist so sánh trước khi merge; backup |
| Links từ bên ngoài (bookmarks) | Thấp | Thấp | Để lại redirect notes; giữ old README |
| Confusion trong quá trình | Trung bình | Trung bình | Communication rõ ràng; làm từng pha |
| Double-work nếu design sai | Thấp | Cao | Review design trước khi execute; prototype |

---

## 7. CÔNG CỤ HỖ TRỢ

### 7.1. Script cần có

```bash
# 1. Script tìm internal links
find . -name "*.md" -exec grep -l "\.\./" {} \;

# 2. Script tìm duplicate filenames
find . -type f -name "*.md" | sed 's|.*/||' | sort | uniq -d

# 3. Script tạo folder structure
tree -d -L 2 > structure.txt

# 4. Script backup trước migrate
rsync -av Dev-Knowledge/ Dev-Knowledge-backup-$(date +%Y%m%d)/
```

### 7.2. Manual review points

- [ ] Check các file có `../` links
- [ ] Check các file có `./` relative links
- [ ] Check các file có tên trùng nhau (sẽ conflict khi merge)
- [ ] Check các file dùng emoji trong tên (có thể gây issue cross-platform)

---

## 8. THÀNH CÔNG LÀ GÌ?

### 8.1. Metrics

| Metric | Target |
|--------|--------|
| Total folders | Từ 40+ → 10 chính + subfolders |
| Duplicate categories | Từ 22 → 0 |
| Internal broken links | < 5% |
| Navigation clarity | Tìm topic bất kỳ trong < 3 clicks |
| New contributor onboarding | Hiểu structure trong < 5 phút |

### 8.2. Definition of Done

- [ ] Không còn folder nào có số thứ tự trùng lặp
- [ ] Tất cả content đã migrate sang vị trí mới
- [ ] MASTER-CATALOG.md đã cập nhật với paths mới
- [ ] README.md mô tả rõ cấu trúc 2-digit
- [ ] CONTRIBUTING.md có quy ước mới
- [ ] Không còn broken internal links
- [ ] Folder cũ đã được backup và đánh dấu deprecated

---

## 9. TÀI LIỆU THAM KHẢO

### Similar Knowledge Base Structures

1. **Developer Roadmap** (roadmap.sh) - Cấu trúc theo skill tree
2. **MDN Web Docs** - Flat structure với deep linking
3. **AWS Documentation** - Service-based grouping
4. **Kubernetes Docs** - Concept → Task → Reference

### Lessons Learned

- Numbering system phải để buffer (2-digit thay vì 1-digit)
- Nên có 1 "index" file ở mỗi folder (không chỉ README)
- Cross-links cần được automated check
- Template bắt buộc phải có metadata (date, level, author)

---

**Ghi chú cuối:** Kế hoạch này là comprehensive guideline. Trong thực tế, cần linh hoạt điều chỉnh khi phát hiện edge cases trong quá trình migrate. Ưu tiên **giữ nguyên content** > **perfect structure**.
