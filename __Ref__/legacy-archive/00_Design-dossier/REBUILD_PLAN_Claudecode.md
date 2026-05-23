# 📋 KẾ HOẠCH TỔ CHỨC LẠI DEV-KNOWLEDGE

**Ngày:** 2026-05-07  
**Trạng thái:** Planning Phase  
**Mục tiêu:** Làm sạch cấu trúc trùng lặp, tích hợp nội dung từ `.Old`, và đạt 80%+ hoàn thiện của MASTER-CATALOG

---

## 🎯 PHÂN TÍCH HIỆN TRẠNG

### Vấn đề phát hiện

1. **Trùng lặp category folders** (same content, different numbers):
   - `06-DevOps/` vs `09-DevOps/` → cùng Docker/K8s/CI-CD
   - `10-AI-ML/` vs `14-AI-ML/` → cùng ML, Deep Learning
   - `12-Soft-Skills/` vs `21-Soft-Skills/` → overlap 90%
   - `01-Fundamentals/` vs `01-CS-Fundamentals/` → cần merge
   - `05-Languages/` vs `02-Languages/` → trùng lặp Python/JS/Go
   - `07-Cloud/` vs `10-Cloud/` → trùng AWS/Azure/GCP

2. **Cấu trúc lộn xộn**:
   - `Dev-Knowledge/` hiện có **46 folders + 2055 files**
   - Một số folder chỉ có skeleton (🚧), nhiều folder chưa có gì (❌)
   - `_Draft_` folders cần cleanup
   - `_Delete` folders cần xác định xóa hay giữ

3. **Chất lượng nội dung không đồng đều**:
   - Một số bài rất tốt (✅): `06-DevOps/docker/` với cấu trúc bài mẹ → bài con
   - Một số bài chỉ là link/placeholder (❌)
   - `.Old/` chứa **592 files** chất lượng cao cần tích hợp

4. **Tính nhất quán**:
   - Một số dùng số thứ tự (01-, 02-), một số không
   - Naming convention khác nhau: `docker-basics.md` vs `01-docker-basics.md`
   - Một số dùng kebab-case, một số dùng snake_case

### Thế mạnh hiện có

✅ **MASTER-CATALOG.md** đã định nghĩa rõ:
- 396 chủ đề tổng thể
- Phân loại theo domain (00-21)
- Priority ordering cho việc điền nội dung
- Trạng thái (✅ 🚧 ❌) rõ ràng

✅ **Cấu trúc modular** đã tốt:
- Bài mẹ (parent lesson) với README/index/lesson/_sub-lessons/
- Templates trong `_templates/` đã sẵn sàng
- Triết lý "Learn by Doing" và "Từ WHY → WHAT → HOW" đã định rõ

✅ **Nội dung chất lượng** trong `.Old/`:
- `DevOps-Knowledge/` có THEORY/, CHEATSHEETS/, TROUBLESHOOTING/, CODE-SAMPLES/
- Rất nhiều cheat sheets, code samples thực tế
- Interview prep chất lượng

---

## 🎯 MỤC TIÊU (OBJECTIVES)

### Primary Goals

1. **Standardize structure** — 1 cấu trúc duy nhất, áp dụng cho tất cả categories
2. **Merge duplicates** — Giải quyết 6 cặp folder trùng lặp
3. **Integrate `.Old/`** — Move quality content vào Dev-Knowledge chính
4. **Cleanup drafts** — Xác định giữ/xóa `_Draft_`, `_Delete` folders
5. **Fill missing content** — Từ 48 complete → 396 complete (ít nhất 80%)
6. **Maintain navigation** — Giữ MASTER-CATALOG và SUMMARY đối chiếu

### Success Metrics

- ✅ Tất cả categories từ 00-21 chỉ có **1 folder duy nhất** mỗi loại
- ✅ Không còn duplicate content giữa các số thứ tự khác nhau
- ✅ >90% links trong MASTER-CATALOG trỏ đến file tồn tại
- ✅ Mỗi bài mẹ (parent topic) có đầy đủ: README.md, index.md, lesson.md, _sub-lessons/
- ✅ Tất cả .md files tuân theo template chuẩn

---

## 🗺️ CHIẾN LƯỢC TỔNG THỂ

### Phase 1: Analysis & Inventory (Week 1)
**Mục tiêu:** Hiểu sâu toàn bộ nội dung, tạo inventory chi tiết

**Tasks:**
1. Scan tất cả files trong Dev-Knowledge và .Old
2. Tạo spreadsheet với:
   - File path
   - Category assignment (theo MASTER-CATALOG)
   - Quality score (✅/🚧/❌)
   - Duplicate detection
   - Recommended action (Keep/Merge/Delete)
3. Phân tích từng duplicate pair:
   - `06-DevOps/` vs `09-DevOps/` → so sánh nội dung, chọn best version
   - `10-AI-ML/` vs `14-AI-ML/` → merge strategy
   - Similar cho các cặp khác
4. Audit `_Draft_` và `_Delete` folders → inventory + recommendation

**Deliverables:**
- `INVENTORY.md` — spreadsheet-like markdown với tất cả files
- `DUPLICATE_ANALYSIS.md` — chi tiết từng cặp trùng lặp
- `DRAFT_CLEANUP_PLAN.md` — decide keep/delete

---

### Phase 2: Define Standard Structure (Week 1)
**Mục tiêu:** Lock down canonical structure

**Decisions cần làm:**
1. **Folder naming convention:**
   - Prefix với số (01-, 02-) hay không?
   - Kebab-case vs snake_case?
   - Decision: **Tuân theo MASTER-CATALOG.md** — số 2-digit với prefix

2. **Parent lesson structure (finalized):**
```
[topic]/
├── README.md              # Introduction, learning objectives
├── index.md               # List of all sub-lessons (navigation)
├── lesson.md              # Core theory content
├── _sub-lessons/          # numbered sub-topics (01-xxx/, 02-xxx/)
│   ├── 01-[topic]/
│   │   ├── lesson.md
│   │   ├── exercises.md
│   │   ├── quiz.md
│   │   └── checklist.md
├── _quizzes/              # Comprehensive quizzes
├── _projects/             # Hands-on projects
└── _resources/            # External links, references
```

3. **Sub-lesson template** (xem `_templates/sub-lesson-template.md`):
   - Metadata block (level, time, prerequisites)
   - Learning objectives (bullet points)
   - Content (theory + examples)
   - Hands-on section
   - Self-check questions
   - Further reading

4. **Parent lesson template** (xem `_templates/parent-lesson-template.md`)

5. **File naming convention:**
   - Hyphens: `01-docker-basics.md` (consistent)
   - NOT underscores, NOT camelCase

6. **Category mapping:**
   - Map old folder numbers → new canonical numbers
   - Create `CATEGORY_MAPPING.md`:
     ```
     Old: 06-DevOps   → New: 09-DevOps  (merge into 09)
     Old: 09-DevOps   → New: 09-DevOps  (canonical)
     Old: 10-AI-ML    → New: 14-AI-ML   (merge into 14)
     Old: 14-AI-ML    → New: 14-AI-ML   (canonical)
     ```

**Deliverables:**
- `STANDARD_STRUCTURE.md` — cấu trúc canonical
- `CATEGORY_MAPPING.md` — mapping old → new
- Updated `_templates/` nếu cần

---

### Phase 3: Duplicate Resolution & Merging (Week 2-3)
**Mục tiêu:** Consolidate tất cả duplicate content vào 1 location

**Process cho mỗi duplicate pair:**

**Example: `06-DevOps/` vs `09-DevOps/`**

1. **Compare quality:**
   - `06-DevOps/docker/` → có cấu trúc bài mẹ → bài con tốt
   - `09-DevOps/docker/` → 4 flat files (basics, advanced, compose, cheatsheet)
   - **Decision:** Keep `06-DevOps/docker/` structure, merge additional content từ `09-DevOps/` vào

2. **Merge strategy:**
   - Copy missing `_sub-lessons/` từ `09-` vào `06-/_sub-lessons/`
   - Nếu `09-` có content tốt hơn trong flat files, refactor thành bài con mới
   - Update `index.md` và `README.md` để include tất cả bài con
   - Xóa `09-DevOps/docker/` sau khi merge

3. **Handle conflicts:**
   - Nếu cả hai đều có bài con giống nhau → diff content, merge manually
   - Keep better version, preserve authors/credits

**Duplicate pairs to process:**

| Old Paths | Canonical Path | Action |
|-----------|----------------|--------|
| `06-DevOps/` + `09-DevOps/` | `09-DevOps/` | Merge into `09-` (keep better structure) |
| `10-AI-ML/` + `14-AI-ML/` | `14-AI-ML/` | Merge, preserve 14's structure |
| `12-Soft-Skills/` + `21-Soft-Skills/` | `21-Soft-Skills/` | Merge, keep 21's topics |
| `01-CS-Fundamentals/` + `01-Fundamentals/` | `01-CS-Fundamentals/` | Merge, rename to match |
| `05-Languages/` + `02-Languages/` | `02-Languages/` | Merge language-specific folders |
| `07-Cloud/` + `10-Cloud/` | `10-Cloud/` | Merge, keep 10's structure |

**Special cases:**
- `04-Networking/` vs `01-Fundamentals/networking/`? → check content, decide canonical location
- `02-Version-Control/` vs `01-Fundamentals/git/`? → merge into `01-Fundamentals/git/`

**Deliverables:**
- Duplicate merge plan cho từng pair
- Post-merge structure documentation

---

### Phase 4: `.Old/` Content Integration (Week 3-4)
**Mục tiêu:** Move quality content từ `.Old/` vào Dev-Knowledge chính

**Strategy:**

1. **Categorize `.Old/` content:**
   - `DevOps-Knowledge/` → merge vào `09-DevOps/`
   - `Devops-Exercises/` → create projects/quizzes trong topics
   - `DevOps-Journey_*` → likely outdated, check for gems, else archive
   - `Track*` folders → interview prep? add to `00-Roadmaps/` or `21-Soft-Skills/`
   - `Tutorials/` → distribute vào relevant topics
   - `resources/` (GLOSSARY.md, SOFTWARE_LINKS.md) → merge vào `_resources/` của mỗi topic hoặc global

2. **Quality filter:**
   - Only move content that matches current standard
   - Refactor nếu cần (convert flat file → sub-lesson structure)
   - Preserve author credits nếu có

3. **Integration plan:**

**From `DevOps-Knowledge/THEORY/`:**
- Each file → become sub-lesson or enhance parent lesson
- Example: `THEORY/Containerization/docker.md` → merge into `09-DevOps/docker/lesson.md` or create new sub-lesson

**From `DevOps-Knowledge/CHEATSHEETS/`:**
- Move to `09-DevOps/_resources/` hoặc `14-Tools/_resources/`
- Or embed vào relevant sub-lessons

**From `DevOps-Knowledge/CODE-SAMPLES/`:**
- Move to `09-DevOps/_resources/code-samples/`
- Or create `_projects/` from them

**From `DevOps-Knowledge/TROUBLESHOOTING/`:**
- Convert to `09-DevOps/docker/_quizzes/` style? Or create dedicated troubleshooting guides
- Could become: `09-DevOps/docker/_sub-lessons/99-troubleshooting/`

**From `Devops-Exercises/`:**
- README.md → likely overview, check
- FAQ → add to `09-DevOps/_resources/faq.md`
- Interview questions → `21-Soft-Skills/04-coding-interviews-practices/` or create DevOps-specific interview guide

4. **Archive old content:**
- Sau khi move, xóa `.Old/` hoặc move vào `.Old_ARCHIVED/` để backup
- Update links trong Dev-Knowledge nếu cần

**Deliverables:**
- `.Old` integration plan by category
- Moved content tracking (what went where)

---

### Phase 5: Structure Cleanup & Standardization (Week 4-5)
**Mục tiêu:** Apply canonical structure to all topics

**Tasks:**

1. **Rename folders to canonical numbers:**
```bash
# Before
Dev-Knowledge/
├── 01-Fundamentals/
├── 02-Languages/
├── 03-Frontend/
├── 04-Backend/
├── 05-Databases/
├── 06-DevOps/
├── 07-Cloud/
├── 08-Architecture/
├── 09-Security/
├── 10-AI-ML/
├── 11-Testing/
├── 12-Soft-Skills/
├── 13-Data-Engineering/
├── 14-Tools/
├── 15-Databases/        ← duplicate number!
├── 16-Mobile/
├── 17-GameDev/
├── 18-Blockchain/
├── 19-Embedded-IoT/
├── 21-Soft-Skills/

# After (canonical from MASTER-CATALOG)
Dev-Knowledge/
├── 00-Roadmaps/
├── 01-CS-Fundamentals/
├── 02-Version-Control/
├── 03-Terminal-OS/
├── 04-Networking/
├── 05-Languages/
├── 06-Frontend/
├── 07-Backend/
├── 08-Databases/
├── 09-DevOps/
├── 10-Cloud/
├── 11-Architecture/
├── 12-Security/
├── 13-Testing/
├── 14-AI-ML/
├── 15-Data-Engineering/
├── 16-Mobile/
├── 17-GameDev/
├── 18-Blockchain/
├── 19-Embedded-IoT/
├── 20-Tools/
└── 21-Soft-Skills/
```

2. **Handle orphaned folders:**
- `15-Databases/` exists but also `08-Databases/` → decide canonical
- According to MASTER-CATALOG: `08-Databases/` is correct
- **Action:** Move `15-Databases/` content into `08-Databases/` (merge), delete `15-`

3. **Apply structure to parent topics:**
- Every topic folder (e.g., `09-DevOps/docker/`) must have:
  - `README.md`
  - `index.md`
  - `lesson.md`
  - `_sub-lessons/` (with numbered sub-folders)
  - `_quizzes/` (optional)
  - `_projects/` (optional)
  - `_resources/` (optional)

4. **Convert flat files to sub-lessons:**
- Topics với chỉ 4 flat files (01-xxx.md, 02-xxx.md...) → convert to `_sub-lessons/01-xxx/lesson.md` structure
- Update `index.md` to point to new structure

5. **Standardize naming:**
- All files: kebab-case, lowercase
- Sub-lesson folders: `01-<topic>`, `02-<topic>`,...
- Consistent prefixes

6. **Update MASTER-CATALOG.md links:**
- Ensure all file paths in catalog match new structure
- Update status indicators (✅/🚧/❌) based on actual content

**Deliverables:**
- Renamed folder structure
- Standardized all topic folders
- Updated MASTER-CATALOG.md
- Verified all internal links work

---

### Phase 6: Content Gap Filling (Week 5-8)
**Mục tiêu:** Từ current state → 80% complete (318/396 topics)

**Priority từ MASTER-CATALOG:**

```
TIER 1 (Must-have):
├── 01-CS-Fundamentals/ (cs/, programming/, dsa/)
├── 02-Version-Control/ (git/)
├── 03-Terminal-OS/ (terminal/, linux/, regex/)
├── 04-Networking/ (all 12 topics)
├── 05-Languages/ (Python, JavaScript, TypeScript, Go, Java)
├── 06-Frontend/ (HTML, CSS, React, Next.js, Vue)
├── 07-Backend/ (API design, FastAPI, Express, Django, NestJS)
├── 08-Databases/ (SQL, NoSQL, ORM)
├── 09-DevOps/ (Docker, Kubernetes, CI/CD, IaC)
└── 10-Cloud/ (AWS, Azure, GCP core)

TIER 2 (High-value):
├── 11-Architecture/ (Design Patterns, System Design)
├── 12-Security/ (Web Security, Auth, Encryption)
├── 13-Testing/ (all testing topics)
├── 14-AI-ML/ (ML fundamentals, LLMs)
└── 21-Soft-Skills/ ( interviews, code review, tech writing)
```

**Process:**

1. **For each missing topic:**
   - Check if stub exists (🚧) → expand
   - If completely missing (❌) → create from scratch using template

2. **Content sources:**
   - `.Old/` integration (already done in Phase 4)
   - Official docs (link in _resources/)
   - Known patterns from existing good content
   - Author's knowledge (you!)

3. **Minimum viable content** cho mỗi topic:
   - Parent lesson: README.md + lesson.md (at least 500 words)
   - 2-3 sub-lessons với full structure (lesson.md, exercises.md, quiz.md, checklist.md)
   - Exercises: at least 3-5 practical questions/tasks
   - Quiz: 5-10 multiple choice questions

4. **Writing standards:**
   - Use "Từ WHY → WHAT → HOW"
   - Include real-world examples
   - Code snippets với syntax highlighting
   - Diagrams nếu cần (Mermaid)
   - Vietnamese explanations + English terms

**Deliverables:**
- Completed topics tracking
- Content quality checklist per topic

---

### Phase 7: Quality Assurance (Week 8-9)
**Mục tiêu:** Verify consistency, fix broken links, ensure quality

**QA Checklist:**

1. **Structure validation:**
   - Every parent topic has required files
   - Every sub-lesson has required files
   - `_sub-lessons/` folders numbered sequentially (01, 02, 03...)

2. **Link validation:**
   - All internal links (`[text](../path/file.md`) point to existing files
   - No broken links
   - Relative paths correct

3. **Content quality:**
   - Each lesson.md > 300 words
   - At least 3 learning objectives
   - Exercises.md có ít nhất 3 exercises
   - Quiz.md có 5+ questions
   - Checklist.md có 5+ items

4. **Formatting:**
   - Consistent heading levels (# ## ###)
   - Code blocks với language tags ```python, ```bash
   - No TODO markers left (except in truly incomplete topics)
   - Frontmatter metadata nếu cần

5. **Navigation:**
   - All README.md include "Next Steps" section
   - All lessons include "Prerequisites" if any
   - `index.md` lists all sub-lessons with descriptions

6. **MASTER-CATALOG sync:**
   - Count actual files vs catalog predictions
   - Update status indicators
   - Add any new topics discovered

**Tools:**
- Write simple script to check broken links
- Manual spot-check 20% of content

**Deliverables:**
- QA report with issues found
- Fixed issues

---

### Phase 8: Documentation & Finalization (Week 9-10)
**Mục tiêu:** Wrap up, document changes, prepare for ongoing maintenance

**Tasks:**

1. **Update core documentation:**
   - `README.md` — reflect new structure, update progress stats
   - `SUMMARY.md` — rewrite with new organization
   - `CONTRIBUTING.md` — update with new guidelines, templates
   - Create `MIGRATION_GUIDE.md` — for contributors unfamiliar with new structure

2. **Create change log:**
   - `MIGRATION_LOG.md` — what changed, why, where things moved from/to
   - Include category mapping table

3. **Update templates:**
   - Ensure `_templates/` match final structure
   - Add examples from best topics

4. **Create maintenance guide:**
   - How to add new topic
   - How to update existing topic
   - How to handle duplicates in future
   - Style guide

5. **Archive `.Old/`:**
   - Move `.Old/` to `.Old_ARCHIVED_2026-05-07/`
   - Keep for reference only, no longer part of knowledge base
   - Document what was archived

6. **Final stats:**
   - Count total topics: should match MASTER-CATALOG
   - Count complete vs incomplete
   - Generate completion report

**Deliverables:**
- Updated docs
- Migration guide
- Maintenance guide
- Final stats report

---

## 📊 TIMELINE ƯỚC TÍNH

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 1: Analysis | Week 1 | INVENTORY.md, DUPLICATE_ANALYSIS.md |
| Phase 2: Standards | Week 1 | STANDARD_STRUCTURE.md, CATEGORY_MAPPING.md |
| Phase 3: Duplicate Merge | Week 2-3 | Merged folders, conflict resolution doc |
| Phase 4: `.Old` Integration | Week 3-4 | Integration plan, moved content |
| Phase 5: Cleanup | Week 4-5 | Renamed folders, standardized structure |
| Phase 6: Gap Filling | Week 5-8 | 80% of topics complete |
| Phase 7: QA | Week 8-9 | QA report, fixed issues |
| Phase 8: Finalization | Week 9-10 | Final docs, migration guide |

**Total estimated:** 10 weeks (2.5 months)

---

## 🔄 EXECUTION ORDER (Recommended)

1. **Week 1:**
   - [ ] Complete Phase 1 (Inventory)
   - [ ] Complete Phase 2 (Standards)
   - **Decision point:** Review mapping, approve structure before proceeding

2. **Week 2-3:**
   - [ ] Phase 3: Start with EASIEST duplicate pairs first (e.g., `15-Databases` → `08-Databases`)
   - [ ] Build confidence with simple merges
   - [ ] Document merge process as you go

3. **Week 3-4:**
   - [ ] Phase 4: `.Old/` integration — START WITH `DevOps-Knowledge/` (highest quality)
   - [ ] Phase 3 continue: handle harder duplicates (AI-ML, Soft-Skills)

4. **Week 4-5:**
   - [ ] Phase 5: Rename/standardize folders — DO THIS AFTER ALL CONTENT MERGED
   - [ ] Update MASTER-CATALOG.md continuously

5. **Week 5-8:**
   - [ ] Phase 6: Gap filling — follow TIER priority
   - [ ] Focus on must-have topics first (DevOps, Frontend, Backend, CS Fundamentals)
   - [ ] Use templates, reuse patterns from existing good content

6. **Week 8-9:**
   - [ ] Phase 7: QA pass
   - [ ] Fix broken links
   - [ ] Standardize formatting

7. **Week 9-10:**
   - [ ] Phase 8: Documentation
   - [ ] Final stats
   - [ ] Celebrate! 🎉

---

## ⚠️ RISKS & MITIGATION

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Lose content during merge | High | Medium | Create backup branch before each phase, use git extensively |
| Broken links after rename | High | High | Use script to find/replace links, test thoroughly |
| Duplicate resolution disputes | Medium | Low | Document decisions, involve stakeholders if needed |
| Timeline overrun | Medium | High | MVP approach: can defer Tier 2 topics to later |
| Content quality inconsistent | Medium | High | Use existing high-quality content as templates, enforce standards |
| `.Old/` integration overwhelming | High | Medium | Prioritize high-value folders, archive low-value without merging |

---

## 📝 DECISIONS NEEDED (From You)

Before starting implementation:

1. **Category canonical numbers:**
   - DevOps: `09` (MASTER-CATALOG) or `06` (existing)?
   - AI-ML: `14` or keep both `10` and `14` as separate tracks?
   - Soft-Skills: `21` or consolidate?

2. **`.Old/` treatment:**
   - Move everything? Or cherry-pick only high-quality?
   - Archive untouched content or delete?

3. **Timeline:**
   - 10 weeks realistic? Or want faster/slower?
   - Want to do it in phases with review gates?

4. **Quality threshold:**
   - 80% complete (318 topics) enough? Or 100%?
   - What defines "complete" — minimum viable content vs comprehensive?

5. **Resources:**
   - Will you write content yourself? Or need help?
   - Any existing contributors to coordinate with?

---

## 🎯 NEXT STEPS (Immediate Actions)

**Week 1 Tasks (Start Now):**

1. [ ] Read this plan, ask questions
2. [ ] Approve Phase 1 & 2 approach
3. [ ] Run inventory script (will provide)
4. [ ] Review DUPLICATE_ANALYSIS once generated
5. [ ] Approve CATEGORY_MAPPING.md
6. [ ] Create git branch: `reorg/phase-1-analysis`
7. [ ] Begin Phase 1: generate inventory

**I will help you execute each phase. Just say "start Phase 1" and I'll begin generating the analysis documents.**

---

## 📚 REFERENCES

- Current `MASTER-CATALOG.md` — blueprint for target structure
- Current `README.md` & `SUMMARY.md` — current state docs
- `_templates/` — content templates to follow
- `.Old/DevOps-Knowledge/` — example of good structure (THEORY/, CHEATSHEETS/, etc.)

---

**Ready to execute?** Let's start with Phase 1: comprehensive inventory of everything.
