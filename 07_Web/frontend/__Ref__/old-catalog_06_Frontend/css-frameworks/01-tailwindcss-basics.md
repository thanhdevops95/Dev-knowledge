# 🎨 Tailwind CSS — Utility-first CSS Framework

> `[INTERMEDIATE]` — Viết CSS trực tiếp trong HTML, nhanh và nhất quán

---

## Tại sao Tailwind?

CSS truyền thống có vấn đề khi project lớn:

**Vấn đề 1: Naming fatigue** — Bạn phải đặt tên cho mọi thứ: `.card-wrapper`, `.card-header-title-text`... Khi project phình to, tên class trở nên khó hiểu và đụng nhau.

**Vấn đề 2: Dead CSS** — CSS chỉ tăng, không giảm. Ai cũng sợ xóa class vì không biết nó dùng ở đâu. Sau 2 năm, bạn có 50KB CSS mà chỉ dùng 20%.

**Vấn đề 3: Context switching** — Viết HTML ở file A, nhảy sang file B để viết CSS, quay lại file A để check class name...

Tailwind giải quyết bằng cách **không viết CSS files** — mọi style nằm trực tiếp trong HTML dưới dạng utility classes:

```html
<!-- CSS truyền thống: viết riêng, đặt tên class -->
<div class="card">
    <h2 class="card-title">Hello</h2>
</div>
<style>
.card { padding: 1.5rem; border-radius: 0.5rem; box-shadow: ... }
.card-title { font-size: 1.5rem; font-weight: bold; }
</style>

<!-- Tailwind: style trong HTML, không cần đặt tên -->
<div class="p-6 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold">Hello</h2>
</div>
<!-- Không cần file CSS riêng! Production: chỉ ship CSS bạn THỰC SỰ dùng -->
```

### Trade-offs cần biết

| Ưu điểm | Nhược điểm |
|---|---|
| Không lo naming, dead CSS | HTML dài hơn, nhiều class |
| Consistent design tokens | Học curve: nhớ class names |
| Production CSS rất nhỏ (~10KB) | Khó đọc cho người mới |
| Thay đổi nhanh, không sợ side-effects | Custom design phức tạp cần config |

---

## 1. Core Concepts

### Spacing & Sizing

Tailwind dùng **scale cố định** thay vì magic numbers. Mỗi đơn vị = 0.25rem (4px):

```html
<!-- p-{n}: padding. m-{n}: margin. Số = đơn vị x 4px -->
<div class="p-4">padding: 16px (4 × 4px)</div>
<div class="p-6">padding: 24px (6 × 4px)</div>
<div class="mt-8">margin-top: 32px</div>
<div class="px-4 py-2">padding: 8px 16px (x = horizontal, y = vertical)</div>

<!-- w-{n}: width. h-{n}: height -->
<div class="w-full">width: 100%</div>
<div class="w-1/2">width: 50%</div>
<div class="h-screen">height: 100vh</div>
<div class="max-w-md">max-width: 28rem (medium)</div>

<!-- gap: khoảng cách giữa flex/grid children -->
<div class="flex gap-4">...</div>
```

### Colors

Tailwind cung cấp bảng màu nhất quán từ 50 (nhạt) → 950 (đậm):

```html
<!-- text-{color}-{shade} / bg-{color}-{shade} -->
<p class="text-gray-700">Text xám đậm</p>
<div class="bg-blue-500">Background xanh</div>
<button class="bg-blue-600 hover:bg-blue-700 text-white">
    Nút xanh, hover đậm hơn
</button>

<!-- Opacity -->
<div class="bg-black/50">Background đen 50% trong suốt</div>
```

### Typography

```html
<h1 class="text-4xl font-bold tracking-tight">Tiêu đề</h1>
<p class="text-base text-gray-600 leading-relaxed">Nội dung với line-height thoải mái</p>
<span class="text-sm text-gray-400 uppercase">Label nhỏ</span>
<p class="line-clamp-3">Text dài sẽ bị cắt sau 3 dòng...</p>
```

---

## 2. Layout — Flexbox & Grid

```html
<!-- Flexbox: center content -->
<div class="flex items-center justify-center min-h-screen">
    <div>Centered content</div>
</div>

<!-- Flex: navigation bar -->
<nav class="flex items-center justify-between px-6 py-4">
    <div class="text-xl font-bold">Logo</div>
    <div class="flex gap-6">
        <a href="#">Home</a>
        <a href="#">About</a>
    </div>
</nav>

<!-- Grid: product grid responsive -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <div class="bg-white rounded-lg shadow p-4">Product 1</div>
    <div class="bg-white rounded-lg shadow p-4">Product 2</div>
    <div class="bg-white rounded-lg shadow p-4">Product 3</div>
    <div class="bg-white rounded-lg shadow p-4">Product 4</div>
</div>

<!-- Responsive: mobile-first! Classes không có prefix = mobile default -->
<!-- sm: ≥640px | md: ≥768px | lg: ≥1024px | xl: ≥1280px | 2xl: ≥1536px -->
```

---

## 3. State Variants

Tailwind xử lý states bằng **prefix**:

```html
<!-- Hover, Focus, Active -->
<button class="
    bg-blue-600
    hover:bg-blue-700
    focus:ring-2 focus:ring-blue-500 focus:outline-none
    active:bg-blue-800
    transition-colors duration-200
">
    Click me
</button>

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900">
    <p class="text-gray-800 dark:text-gray-200">
        Tự động đổi khi user preference là dark mode
    </p>
</div>

<!-- Group hover: hover parent → style child -->
<div class="group cursor-pointer">
    <img class="group-hover:scale-105 transition-transform" src="..." />
    <p class="group-hover:text-blue-600 transition-colors">Title</p>
</div>

<!-- Responsive + state kết hợp -->
<div class="text-sm md:text-base lg:text-lg hover:text-blue-600">
    Responsive text + hover color
</div>
```

---

## 4. Component Patterns

Khi UI pattern lặp lại nhiều, dùng **component** (React/Vue) thay vì copy-paste utilities:

```jsx
// ✅ React component thay vì @apply
function Button({ children, variant = 'primary', size = 'md', ...props }) {
    const base = 'inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
    
    const variants = {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    };

    const sizes = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg',
    };

    return (
        <button className={`${base} ${variants[variant]} ${sizes[size]}`} {...props}>
            {children}
        </button>
    );
}

// Sử dụng — sạch, nhất quán
<Button>Default</Button>
<Button variant="danger" size="lg">Delete</Button>
```

### Card component thực tế

```jsx
function ProductCard({ product }) {
    return (
        <div className="group overflow-hidden rounded-xl bg-white shadow-sm hover:shadow-md transition-shadow">
            {/* Image */}
            <div className="aspect-video overflow-hidden">
                <img
                    src={product.image}
                    alt={product.name}
                    className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
            </div>

            {/* Content */}
            <div className="p-4 space-y-2">
                <h3 className="font-semibold text-gray-900 line-clamp-1">
                    {product.name}
                </h3>
                <p className="text-sm text-gray-500 line-clamp-2">
                    {product.description}
                </p>
                <div className="flex items-center justify-between pt-2">
                    <span className="text-lg font-bold text-blue-600">
                        {formatPrice(product.price)}
                    </span>
                    <button className="rounded-lg bg-blue-600 px-3 py-1.5 text-sm text-white hover:bg-blue-700">
                        Mua ngay
                    </button>
                </div>
            </div>
        </div>
    );
}
```

---

## 5. Customization

```javascript
// tailwind.config.js
export default {
    content: ['./src/**/*.{js,ts,jsx,tsx}'],  // Purge unused CSS
    
    darkMode: 'class',  // 'media' = OS preference | 'class' = manual toggle

    theme: {
        extend: {
            // Thêm custom values (giữ defaults)
            colors: {
                brand: {
                    50: '#eff6ff',
                    500: '#3b82f6',
                    900: '#1e3a5f',
                },
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    
    plugins: [
        require('@tailwindcss/typography'),  // Prose: style cho markdown/HTML content
        require('@tailwindcss/forms'),       // Reset form elements
    ],
};
```

---

## Tailwind v4 (2024+): CSS-first config

Tailwind v4 bỏ `tailwind.config.js`, config trực tiếp trong CSS:

```css
/* app.css — Tailwind v4 */
@import "tailwindcss";

@theme {
    --color-brand-500: #3b82f6;
    --font-sans: "Inter", sans-serif;
    --breakpoint-3xl: 1920px;
}
```

---

## Bài tập thực hành

- [ ] Build landing page responsive với Tailwind (mobile-first)
- [ ] Dark mode toggle: class-based switching
- [ ] Component library: Button, Card, Modal reusable
- [ ] Custom theme: brand colors, fonts, animations

---

## Tài nguyên thêm

- [Tailwind Docs](https://tailwindcss.com/docs) — Official
- [Tailwind UI](https://tailwindui.com/) — Premium components (paid)
- [Headless UI](https://headlessui.com/) — Unstyled accessible components
- [shadcn/ui](https://ui.shadcn.com/) — Copy-paste components (free, rất phổ biến)
