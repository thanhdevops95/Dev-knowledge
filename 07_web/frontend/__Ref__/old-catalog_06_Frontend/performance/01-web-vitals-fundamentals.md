# 📊 Core Web Vitals — Đo lường trải nghiệm người dùng

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Metrics Google dùng để xếp hạng website

---

## Tại sao Web Performance quan trọng?

Performance không chỉ là "nhanh hay chậm" — nó **ảnh hưởng trực tiếp đến kinh doanh**:

- **Amazon**: Mỗi 100ms chậm thêm → giảm 1% doanh thu
- **Google**: Trang chậm 0.5s → giảm 20% traffic
- **Pinterest**: Giảm 40% thời gian chờ → tăng 15% sign-ups

Google đã biến performance thành **yếu tố SEO ranking** thông qua Core Web Vitals — 3 metrics đo trải nghiệm thực tế của người dùng.

---

## 1. Ba Metrics chính (2024+)

```
Core Web Vitals:

┌──────────────────────────────────────────────────────────┐
│  LCP (Largest Contentful Paint)                          │
│  "Bao lâu để thấy nội dung chính?"                      │
│                                                          │
│  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  2.5s = Good      │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░  4.0s = Needs Fix │
│  ████████████████████░░░░░░░░░░░░░░░░  > 4s = Poor!     │
├──────────────────────────────────────────────────────────┤
│  INP (Interaction to Next Paint)                         │
│  "Bao lâu để phản hồi khi tôi click?"                   │
│                                                          │
│  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  200ms = Good     │
│  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  500ms = Needs Fix│
│  ██████████░░░░░░░░░░░░░░░░░░░░░░░░░  > 500ms = Poor!  │
├──────────────────────────────────────────────────────────┤
│  CLS (Cumulative Layout Shift)                           │
│  "Trang có nhảy lung tung không?"                        │
│                                                          │
│  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0.1 = Good       │
│  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0.25 = Needs Fix │
│  ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░  > 0.25 = Poor!   │
└──────────────────────────────────────────────────────────┘
```

---

## 2. LCP — Largest Contentful Paint

### Đo gì?

Thời gian từ khi user navigate đến trang → phần tử LỚN NHẤT trong viewport render xong. "Phần tử lớn nhất" thường là:
- Hero image
- Heading text block
- Video poster

### Nguyên nhân LCP chậm & cách fix

**a) Hình ảnh chưa tối ưu** (nguyên nhân #1):

```html
<!-- ❌ Hình 5MB PNG, không lazy, không responsive -->
<img src="hero.png" />

<!-- ✅ Tối ưu hoàn chỉnh -->
<img
    src="hero.webp"
    srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
    sizes="(max-width: 600px) 400px, (max-width: 1024px) 800px, 1200px"
    width="1200"
    height="600"
    alt="Hero banner"
    fetchpriority="high"
    decoding="async"
/>

<!-- Preload LCP image: báo browser download sớm nhất có thể -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high" />
```

**Tại sao `fetchpriority="high"`?** Vì browser mặc định load images muộn hơn CSS/JS. Với `fetchpriority`, bạn nói "ảnh này quan trọng, load trước!"

**b) Render-blocking resources:**

```html
<!-- ❌ CSS/JS chặn rendering -->
<link rel="stylesheet" href="all-styles.css" />  <!-- 500KB CSS! -->
<script src="analytics.js"></script>               <!-- Block! -->

<!-- ✅ Fix #1: Inline critical CSS -->
<style>
    /* Chỉ CSS cần thiết cho above-the-fold content */
    .hero { display: flex; min-height: 100vh; }
    .hero h1 { font-size: 3rem; }
</style>
<!-- Load phần CSS còn lại async -->
<link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'" />

<!-- ✅ Fix #2: Defer non-critical JS -->
<script src="analytics.js" defer></script>
```

**c) Server Response Time (TTFB):**

Nếu server trả HTML chậm, mọi thứ đều chậm. Mục tiêu: TTFB < 800ms.

```
Fix TTFB:
  ✅ CDN (serve từ edge gần user)
  ✅ Server-side caching (Redis, Varnish)
  ✅ SSG/ISR (pre-render tại build time)
  ✅ Database optimization (indexes, query tuning)
  ✅ HTTP/2 hoặc HTTP/3
```

---

## 3. INP — Interaction to Next Paint

### Đo gì?

Thời gian từ khi user **tương tác** (click, tap, key press) → browser **paint** phản hồi. INP là giá trị interaction **tệ nhất** (worst-case) trong suốt page visit.

### Nguyên nhân INP chậm & cách fix

**a) Long tasks block main thread:**

```javascript
// ❌ Heavy computation trên main thread → UI freeze
function filterProducts(products, query) {
    // Filter 100,000 products → main thread bị block 500ms!
    return products.filter(p =>
        p.name.toLowerCase().includes(query.toLowerCase())
    );
}

// ✅ Fix #1: Debounce input
const debouncedFilter = debounce(filterProducts, 300);

// ✅ Fix #2: Yield to main thread (cho browser xen render)
async function filterProductsYielding(products, query) {
    const results = [];
    for (let i = 0; i < products.length; i++) {
        if (products[i].name.toLowerCase().includes(query.toLowerCase())) {
            results.push(products[i]);
        }
        // Mỗi 1000 items → yield cho browser render
        if (i % 1000 === 0) {
            await new Promise(resolve => setTimeout(resolve, 0));
        }
    }
    return results;
}

// ✅ Fix #3: Web Worker (chạy trên thread riêng!)
const worker = new Worker(new URL('./filter-worker.ts', import.meta.url));
worker.postMessage({ products, query });
worker.onmessage = (e) => setResults(e.data);
```

**b) React re-renders quá nhiều:**

```jsx
// ❌ Component re-render mỗi khi parent render
function ProductList({ products }) {
    return products.map(p => <ProductCard key={p.id} product={p} />);
}

// ✅ Memo: chỉ re-render khi props thay đổi
const ProductCard = React.memo(function ProductCard({ product }) {
    return <div>{product.name}</div>;
});

// ✅ useMemo: tránh tính toán lại
function Dashboard({ data }) {
    const stats = useMemo(() => computeExpensiveStats(data), [data]);
    return <StatsPanel stats={stats} />;
}
```

---

## 4. CLS — Cumulative Layout Shift

### Đo gì?

Tổng các "nhảy layout" không mong muốn. Ví dụ: bạn đang đọc bài báo, quảng cáo load xong → text shift xuống → mất vị trí đọc.

### Nguyên nhân CLS cao & cách fix

```html
<!-- ❌ Image không có size → layout shift khi load xong -->
<img src="photo.jpg" />

<!-- ✅ Luôn set width/height hoặc aspect-ratio -->
<img src="photo.jpg" width="800" height="600" />
<img src="photo.jpg" style="aspect-ratio: 4/3;" />
```

```css
/* ❌ Font swap gây text shift */
@font-face {
    font-family: 'Custom';
    src: url('font.woff2');
    /* Không có font-display → FOIT (flash of invisible text) */
}

/* ✅ font-display: swap — hiện fallback font trước, swap khi custom font load */
@font-face {
    font-family: 'Custom';
    src: url('font.woff2');
    font-display: swap;
}

/* ✅ Preload font */
/* <link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin /> */
```

```html
<!-- ❌ Quảng cáo / embed không có reserved space -->
<div class="ad-container">
    <!-- Ad loads 2s later → push content down! -->
</div>

<!-- ✅ Reserve space bằng min-height -->
<div class="ad-container" style="min-height: 250px;">
    <!-- Content shift = 0 khi ad loads -->
</div>
```

---

## 5. Đo lường & Monitoring

### Chrome DevTools

```
1. F12 → Lighthouse tab → "Analyze page load"
   → Xem LCP, CLS, INP scores + recommendations

2. F12 → Performance tab → Record
   → Xem timeline: Long Tasks (đỏ), Layout Shifts, Paint events

3. F12 → Performance Insights → Start recording
   → Thấy trực quan bottleneck ở đâu
```

### JavaScript API (Real User Monitoring)

```javascript
// web-vitals library — measure real user metrics
import { onLCP, onINP, onCLS } from 'web-vitals';

function sendToAnalytics(metric) {
    // Gửi lên analytics service
    fetch('/api/metrics', {
        method: 'POST',
        body: JSON.stringify({
            name: metric.name,
            value: metric.value,
            rating: metric.rating,  // 'good' | 'needs-improvement' | 'poor'
            page: window.location.pathname,
        }),
    });
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
```

### Tools

| Tool | Loại | Free? |
|---|---|---|
| **Lighthouse** | Lab (simulated) | ✅ |
| **PageSpeed Insights** | Lab + Field | ✅ |
| **Chrome UX Report** | Field (real users) | ✅ |
| **web-vitals (JS)** | Field (your users) | ✅ |
| **Vercel Analytics** | Field | Freemium |
| **SpeedCurve** | Lab + Field | Paid |

> **Lab vs Field**: Lab data đo trong môi trường controlled (Lighthouse). Field data đo từ real users (Chrome UX Report). Google ranking dùng **field data**.

---

## Bài tập thực hành

- [ ] Lighthouse: Audit 1 website, đọc hiểu từng metric
- [ ] Optimize images: WebP, srcset, fetchpriority cho LCP
- [ ] Fix CLS: add width/height cho tất cả images trên trang
- [ ] web-vitals: track RUM metrics cho app của bạn

---

## Tài nguyên thêm

- [web.dev/vitals](https://web.dev/vitals/) — Google official
- [web-vitals library](https://github.com/GoogleChrome/web-vitals) — Measure in code
- [PageSpeed Insights](https://pagespeed.web.dev/) — Free audit tool
