# Dev-Knowledge Rebuild Execution Plan

## 1) Muc tieu
- Dung `Dev-Knowledge` lam kho tri thuc chinh, de hoc va de tra cuu.
- Tai su dung noi dung tot tu `.Old`, khong copy nguyen trang noi dung kem.
- Xoa trung lap cau truc va tao quy trinh de maintain dai han.

## 2) Van de hien tai
- Trung lap category theo nhieu cap so (vi du DevOps, Backend, Databases).
- Tron 2 truc phan loai: domain ky thuat va kieu noi dung (cheatsheet, troubleshooting...).
- Chat luong bai khong dong deu; co bai bi noise/ngon ngu hong can viet lai.
- Ke hoach cu manh migration, nhung chua co quality gate chat.

## 3) Nguyen tac thiet ke moi
1. Single source of truth: moi topic chi co 1 vi tri chinh.
2. Tach ro domain va asset type.
3. Quality-first: bai kem chat luong vao hang rewrite, khong merge thong.
4. Onboarding nhanh: nguoi moi tim duong hoc trong 5 phut.

## 4) Kien truc de xuat (V2)
```text
Dev-Knowledge/
├── 00-META/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   ├── STYLE-GUIDE.md
│   ├── CONTENT-INVENTORY.md
│   └── MIGRATION-LOG.md
├── 01-FOUNDATIONS/
├── 02-LANGUAGES/
├── 03-FRONTEND/
├── 04-BACKEND/
├── 05-DATABASES/
├── 06-DEVOPS-INFRA/
├── 07-CLOUD/
├── 08-ARCHITECTURE/
├── 09-SECURITY/
├── 10-AI-DATA/
└── 11-CAREER-TOOLS/
```

Trong moi domain, dung chung bo thu muc:
- `concepts/`
- `guides/`
- `cheatsheets/`
- `troubleshooting/`
- `projects/`
- `resources/`

## 5) Yeu cau moi bai viet (Definition of Done)
- Co metadata: level, prerequisite, ngay cap nhat.
- Co cau truc: Why -> What -> How.
- Co vi du code/command hoac case thuc te.
- Khong co doan van noise/vo nghia.
- Link noi bo hop le.

## 6) He thong danh gia file de migration
Gan nhan tung file trong `00-META/CONTENT-INVENTORY.md`:
- `A-keep`: giu nguyen.
- `B-polish`: sua nhe.
- `C-rewrite`: viet lai lon/hoan toan.
- `D-archive`: luu tru, khong dua vao kho chinh.

Quy trinh:
- Move A truoc.
- Move + edit B.
- C tao bai moi, giu file cu lam ref.
- D dua archive.

## 7) Dan bai chuan cho 1 bai
```markdown
# [Topic]
> Level:
> Prerequisites:
> Last updated:

## 1. Why this matters
## 2. Core concepts
## 3. Hands-on
## 4. Common mistakes
## 5. Quick checklist
## 6. Further reading
```

## 8) Roadmap 6 tuan

### Tuan 1: Inventory + mapping
- Quet toan bo markdown o `Dev-Knowledge` va `.Old`.
- Gan nhan A/B/C/D.
- Chot map folder cu -> folder moi.

### Tuan 2: Dung khung V2 + pilot
- Tao khung 11 domain.
- Pilot 2 domain: `04-BACKEND`, `06-DEVOPS-INFRA`.
- Test navigation va links.

### Tuan 3: Core migration
- Migration `01-FOUNDATIONS`, `02-LANGUAGES`, `05-DATABASES`.
- Tao skeleton cho file C-rewrite.

### Tuan 4: Domain con lai
- Migration `03-FRONTEND`, `07-CLOUD`, `08-ARCHITECTURE`, `09-SECURITY`.
- Dong bo style guide.

### Tuan 5: AI/Data + Career/Tools
- Migration `10-AI-DATA`, `11-CAREER-TOOLS`.
- Chuan hoa interview/workflow/resources.

### Tuan 6: Cleanup + release
- Kiem broken links.
- Kiem duplicate titles.
- Chot `README`, `SUMMARY`, `CONTRIBUTING`.
- Dong bang cau truc cu (deprecation notice).

## 9) Acceptance criteria
- Khong con category trung lap.
- 100% file co nhan A/B/C/D trong inventory.
- Cac file C co skeleton rewrite + owner + due date.
- 0 broken internal links muc critical.
- Nguoi moi tim duoc 1 topic trong <= 3 click.

## 10) Viec can lam ngay (next actions)
1. Tao `00-META/CONTENT-INVENTORY.md`.
2. Chot bo domain 11 muc nhu muc 4.
3. Chon 20 bai A-keep dau tien de migration nhanh.
4. Chon 10 bai C-rewrite uu tien (Docker, API Design, SQL, Git, Linux...).
5. Chot lich review hang tuan (1 buoi, 60-90 phut).

---

Ghi chu:
- Rebuild nay uu tien chat luong hoc that su, khong chay theo so luong file.
- Neu can, giu folder cu o che do read-only trong giai doan chuyen tiep de doi chieu.
