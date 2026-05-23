# 📦 npm, yarn, pnpm — Package Managers so sánh

> `[INTERMEDIATE]` — Hiểu sâu công cụ bạn dùng hàng ngày

---

## Tại sao cần hiểu Package Manager?

Hầu hết developer chỉ biết `npm install` rồi quên. Nhưng package manager quyết định:
- **Tốc độ**: Install mất 3 giây hay 30 giây?
- **Disk space**: 1 project 300MB hay 30MB?
- **Security**: Có ai inject malicious code vào dependencies không?
- **Reproducibility**: "Works on my machine" xảy ra vì lock file?

---

## 1. Hiểu package.json

```jsonc
{
    "name": "my-app",
    "version": "1.0.0",
    "dependencies": {
        // Production dependencies — ship cùng app
        "express": "^4.18.2",     // >= 4.18.2 && < 5.0.0 (caret)
        "prisma": "~5.10.0",      // >= 5.10.0 && < 5.11.0 (tilde)
        "zod": "3.22.4"           // Exact version
    },
    "devDependencies": {
        // Development only — không ship
        "typescript": "^5.3.0",
        "vitest": "^1.0.0",
        "eslint": "^8.56.0"
    },
    "scripts": {
        "dev": "tsx watch src/index.ts",
        "build": "tsc && node dist/index.js",
        "test": "vitest",
        "lint": "eslint src/",
        "prepare": "husky install"   // Chạy tự động sau npm install
    },
    "engines": {
        "node": ">=20.0.0"          // Yêu cầu Node version
    }
}
```

### Semver — Hiểu version numbers

```
     MAJOR.MINOR.PATCH
     ─────  ─────  ─────
      1  .  2  .  3

MAJOR: Breaking changes     (1.x.x → 2.0.0: API thay đổi, code cũ CÓ THỂ break)
MINOR: New features          (1.2.x → 1.3.0: thêm tính năng, backward compatible)
PATCH: Bug fixes             (1.2.3 → 1.2.4: fix bug, backward compatible)

Ranges trong package.json:
  ^1.2.3  → >=1.2.3 <2.0.0  (caret: cho phép minor + patch updates)
  ~1.2.3  → >=1.2.3 <1.3.0  (tilde: chỉ cho phép patch updates)
  1.2.3   → exact version    (pin: không update gì cả)
  >=1.2.3 → 1.2.3 trở lên   (risky! major changes vào được)
```

**Lời khuyên**: Dùng `^` (default) cho hầu hết packages. Dùng exact version cho packages thường breaking (database drivers, CSS frameworks).

---

## 2. Lock Files — Tại sao quan trọng?

```
Vấn đề không có lock file:
  Developer A: npm install → gets express 4.18.2 ✅
  Developer B (tuần sau): npm install → gets express 4.19.0 (có bug!) ❌
  CI/CD: npm install → gets 4.19.1 → test fail ❌
  → "Works on my machine!" syndrome

Lock file fix:
  package-lock.json (npm) / yarn.lock / pnpm-lock.yaml
  → Pin CHÍNH XÁC version + integrity hash cho MỌI dependency (kể cả transitive)
  → Mọi người install → CHÍNH XÁC cùng versions
```

**Rules:**
1. **LUÔN commit lock file** vào git
2. **KHÔNG edit** lock file manually
3. Dùng `npm ci` (thay vì `npm install`) trong CI/CD → nhanh hơn, strict hơn

---

## 3. npm vs yarn vs pnpm

### npm — Default, đơn giản

```bash
npm install express              # Add dependency
npm install -D vitest            # Add devDependency
npm ci                           # Clean install (CI/CD)
npm update                       # Update packages theo semver
npm audit                        # Security vulnerabilities scan
npm run dev                      # Run script
npx create-vite@latest my-app    # Run package without installing
```

### yarn — Nhanh hơn npm, Plug'n'Play

```bash
yarn add express                 # Add dependency
yarn add -D vitest               # Add devDependency
yarn install --frozen-lockfile   # CI/CD (strict)
yarn up                          # Update packages
yarn dlx create-vite my-app      # Like npx
```

### pnpm — Tiết kiệm disk, nhanh nhất

```bash
pnpm add express
pnpm add -D vitest
pnpm install --frozen-lockfile
pnpm update
pnpm dlx create-vite my-app
```

**Tại sao pnpm nhanh và nhỏ hơn?**

npm và yarn tạo **flat node_modules** — copy packages vào mỗi project. 10 projects dùng React → 10 copies of React.

pnpm dùng **content-addressable store** — lưu packages 1 lần duy nhất trên disk, project chỉ chứa symlinks. 10 projects dùng React → 1 copy, 10 symlinks.

```
npm/yarn: mỗi project copy riêng
  project-a/node_modules/react/  (10MB)
  project-b/node_modules/react/  (10MB)
  Total: 20MB

pnpm: shared store + hard links
  ~/.pnpm-store/react@18.2.0/   (10MB)  ← 1 copy duy nhất
  project-a/node_modules/react → link to store
  project-b/node_modules/react → link to store
  Total: 10MB + 2 links
```

### So sánh

| Feature | npm | yarn | pnpm |
|---|---|---|---|
| **Speed** | Chậm nhất | Nhanh | Nhanh nhất |
| **Disk** | Nhiều nhất | Nhiều | Ít nhất (~50%) |
| **node_modules** | Flat | Flat / PnP | Symlinked |
| **Monorepo** | Workspaces | Workspaces | Workspaces (tốt nhất) |
| **Security** | npm audit | yarn audit | Strict deps (không phantom) |
| **Popularity** | Mọi nơi | Giảm dần | Tăng nhanh |
| **Khi nào** | Default, tutorials | Legacy projects | New projects, monorepos |

---

## 4. Security — Dependencies đáng tin không?

```bash
# Scan vulnerabilities
npm audit
pnpm audit

# Fix automatically
npm audit fix

# Check outdated packages
npm outdated

# Xem dependency tree
npm ls --depth=2
pnpm ls --depth=2
```

### Supply Chain Attack — Rủi ro thực tế

Năm 2021, `ua-parser-js` (7.8M downloads/tuần) bị hack — malware được inject vào package. Bất kỳ ai `npm install` đều bị compromise.

**Phòng tránh:**
1. **Lock file**: Pin exact versions
2. **npm audit**: Chạy trong CI, fail nếu có critical
3. **Limit permissions**: `npm config set ignore-scripts true` (chặn postinstall scripts)
4. **Socket.dev / Snyk**: Advanced dependency scanning
5. **Ít dependencies hơn**: Mỗi dependency = 1 attack surface. Cân nhắc trước khi `npm install`.

---

## 5. Monorepo Workspaces

```jsonc
// Root package.json
{
    "name": "my-monorepo",
    "private": true,          // Không publish root
    "workspaces": [           // Khai báo workspace paths
        "packages/*",
        "apps/*"
    ]
}
```

```
my-monorepo/
├── package.json
├── apps/
│   ├── web/           ← Next.js app
│   └── api/           ← Express API
└── packages/
    ├── ui/            ← Shared UI components
    ├── utils/         ← Shared utilities
    └── tsconfig/      ← Shared TypeScript config
```

```bash
# pnpm: filter by package
pnpm --filter web dev          # Chạy dev chỉ cho web app
pnpm --filter ./packages/* build  # Build tất cả packages
pnpm add lodash --filter api   # Add dependency cho api only

# npm: workspace flag
npm run dev -w apps/web
npm install lodash -w apps/api
```

---

## Bài tập thực hành

- [ ] So sánh: install cùng project với npm, yarn, pnpm — đo thời gian + disk size
- [ ] Security: chạy `npm audit`, fix vulnerabilities
- [ ] Monorepo: tạo workspace với shared package (utils dùng chung)
- [ ] Lock file: xóa lock file, install lại, diff versions — hiểu tại sao cần commit

---

## Tài nguyên thêm

- [npm Docs](https://docs.npmjs.com/) — Official
- [pnpm Docs](https://pnpm.io/) — Official
- [Socket.dev](https://socket.dev/) — Dependency security
