# ⚡ Vite — Build Tool thế hệ mới

> `[INTERMEDIATE]` — Hiểu tại sao Vite nhanh và cách tận dụng nó

---

## Tại sao Vite thay thế Webpack?

Để hiểu Vite, cần hiểu **vấn đề** của Webpack trước:

### Webpack: Bundle-based (2015)

```
Khi dev (npm run dev):
  Entry Point → Parse ALL imports → Bundle ALL files → Serve 1 big bundle
  
  Dự án 1000 files → parse 1000 files → bundle → serve
  Thời gian: 30-60 giây cold start 😫
  
  Sửa 1 file → Webpack rebuild chunks → 2-5 giây ⏳
```

### Vite: Native ESM (2020)

```
Khi dev (npm run dev):
  Start server ngay lập tức → Browser request module → Transform on-demand
  
  Dự án 1000 files → KHÔNG bundle → chỉ transform file browser request
  Thời gian: < 1 giây cold start 🚀
  
  Sửa 1 file → HMR chỉ update ĐÚNG file đó → < 50ms ⚡
```

**Bí mật của Vite:**
1. **Dev mode**: Dùng native ES modules của browser + esbuild (Go, nhanh 10-100x so với JS-based tools)
2. **Build mode**: Dùng Rollup (mature, ecosystem lớn) cho production bundle
3. **HMR**: Only invalidate module thay đổi, không cần rebuild dependency tree

---

## 1. Setup & Project Structure

```bash
# Tạo project mới
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev
```

```
my-app/
├── index.html           ← Entry point (Vite dùng HTML làm entry, không phải JS!)
├── package.json
├── vite.config.ts       ← Cấu hình Vite
├── tsconfig.json
├── public/              ← Static files (copy nguyên, không transform)
│   └── favicon.ico
└── src/
    ├── main.tsx         ← JS entry (linked từ index.html)
    ├── App.tsx
    ├── App.css
    └── assets/          ← Assets (transform: hash, optimize)
        └── logo.svg
```

Điểm khác biệt quan trọng: `index.html` nằm ở **root** (không phải trong `public/`) vì Vite coi nó là entry point chính:

```html
<!-- index.html — Vite xử lý file này trực tiếp -->
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
</head>
<body>
    <div id="root"></div>
    <!-- Module script — browser load trực tiếp! -->
    <script type="module" src="/src/main.tsx"></script>
</body>
</html>
```

---

## 2. Cấu hình

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
    // Plugins
    plugins: [react()],

    // Path aliases — thay "../../../components" → "@/components"
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
            '@components': path.resolve(__dirname, './src/components'),
            '@lib': path.resolve(__dirname, './src/lib'),
        },
    },

    // Dev server
    server: {
        port: 3000,
        open: true,    // Tự mở browser

        // Proxy API → tránh CORS khi dev
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            },
        },
    },

    // Build options
    build: {
        outDir: 'dist',
        sourcemap: true,
        
        // Code splitting
        rollupOptions: {
            output: {
                manualChunks: {
                    // Tách vendor code → cache riêng
                    vendor: ['react', 'react-dom'],
                    ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
                },
            },
        },

        // Chunk size warning
        chunkSizeWarningLimit: 500,  // KB
    },

    // CSS
    css: {
        modules: {
            localsConvention: 'camelCase',  // CSS Modules convention
        },
        preprocessorOptions: {
            scss: {
                additionalData: `@use "@/styles/variables" as *;`,
            },
        },
    },
});
```

---

## 3. Environment Variables

Vite dùng prefix `VITE_` để expose biến cho client code (giống `REACT_APP_` trong CRA):

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My Application
DB_PASSWORD=secret               # ❌ KHÔNG có VITE_ → không expose cho client!

# .env.development
VITE_API_URL=http://localhost:8080

# .env.production
VITE_API_URL=https://api.production.com
```

```typescript
// Truy cập trong code
const apiUrl = import.meta.env.VITE_API_URL;
const isDev = import.meta.env.DEV;     // true khi dev
const isProd = import.meta.env.PROD;   // true khi build
const mode = import.meta.env.MODE;     // 'development' | 'production'

// TypeScript type-safe env
// env.d.ts
interface ImportMetaEnv {
    readonly VITE_API_URL: string;
    readonly VITE_APP_TITLE: string;
}
```

---

## 4. Import Features

Vite hỗ trợ nhiều loại import out-of-the-box mà không cần cấu hình thêm:

```typescript
// Static import (bundled)
import logo from './assets/logo.svg';        // URL sau build
import styles from './App.module.css';       // CSS Modules
import data from './data.json';              // JSON (tree-shake!)

// Dynamic import → code splitting tự động
const AdminPanel = lazy(() => import('./pages/AdminPanel'));

// Import với query params (Vite-specific)
import imgUrl from './image.png?url';        // URL string
import imgRaw from './shader.glsl?raw';      // Raw string content
import Worker from './worker.ts?worker';     // Web Worker

// Glob import — import nhiều files cùng lúc
const modules = import.meta.glob('./pages/**/*.tsx');
// → { './pages/Home.tsx': () => import('./pages/Home.tsx'), ... }

// Eager glob (load ngay, không lazy)
const eagerModules = import.meta.glob('./icons/*.svg', { eager: true });
```

---

## 5. Vite vs Alternatives

| Feature | Vite | Webpack | Turbopack | esbuild |
|---|---|---|---|---|
| **Dev start** | < 1s | 10-60s | < 1s | N/A |
| **HMR** | < 50ms | 100ms-5s | < 50ms | N/A |
| **Production build** | Rollup | Webpack | N/A (WIP) | esbuild |
| **Config** | Đơn giản | Phức tạp | Next.js only | API-only |
| **Ecosystem** | Tốt | Rất lớn | Next.js | Libraries |
| **Framework support** | React, Vue, Svelte, Solid | Mọi thứ | Next.js only | Libraries |
| **Khi nào dùng** | Mọi project mới | Legacy projects | Next.js apps | Library builds |

**Lời khuyên thực tế:**
- **Project mới** → Vite (99% cases)
- **Đang dùng CRA** → Migrate sang Vite (rất dễ)
- **Next.js** → Turbopack (built-in)
- **Build library** → tsup (based on esbuild) hoặc Vite library mode

---

## Bài tập thực hành

- [ ] Tạo React + TypeScript project với Vite
- [ ] Cấu hình path aliases, proxy API, env variables
- [ ] Code splitting: lazy load routes
- [ ] Analyze bundle: `npx vite-bundle-visualizer`

---

## Tài nguyên thêm

- [Vite Docs](https://vitejs.dev/) — Official
- [Why Vite (Evan You)](https://vitejs.dev/guide/why.html) — Tại sao tạo Vite
- [Migrating from CRA](https://vitejs.dev/guide/migration.html)
