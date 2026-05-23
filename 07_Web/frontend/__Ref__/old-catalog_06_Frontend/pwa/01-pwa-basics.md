# 📱 PWA — Progressive Web Apps

> `[INTERMEDIATE]` — Web app chạy như native app: offline, install, push notifications

---

## Tại sao PWA?

User không muốn install app từ App Store chỉ để xem menu nhà hàng. Nhưng mobile web thì trải nghiệm kém: chậm, không offline, không push notification.

**PWA = web app + native superpowers:**

| Feature | Web thường | PWA | Native App |
|---|---|---|---|
| Install trên Home Screen | ❌ | ✅ | ✅ |
| Hoạt động Offline | ❌ | ✅ | ✅ |
| Push Notifications | ❌ | ✅ | ✅ |
| Truy cập Camera, GPS | ⚠️ Partial | ✅ | ✅ |
| App Store distribution | ❌ | ⚠️ Partial | ✅ |
| Cần install | ❌ | Optional | ✅ Bắt buộc |
| Update tự động | ✅ | ✅ | ❌ Cần download |
| Chi phí phát triển | Thấp | Thấp | Cao (iOS + Android) |

**Ai dùng PWA?** Twitter Lite (65% tăng pages/session), Starbucks (2x daily active users), Pinterest (60% tăng engagement).

---

## 1. Ba thành phần cốt lõi

### a) Web App Manifest — "Metadata cho app"

```json
// manifest.json — nằm ở root
{
    "name": "My Awesome App",
    "short_name": "MyApp",
    "description": "Ứng dụng quản lý công việc",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0f172a",
    "theme_color": "#3b82f6",
    "orientation": "portrait",
    "icons": [
        { "src": "/icons/192.png", "sizes": "192x192", "type": "image/png" },
        { "src": "/icons/512.png", "sizes": "512x512", "type": "image/png" },
        { "src": "/icons/maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
    ]
}
```

```html
<!-- Link trong HTML -->
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#3b82f6" />
<link rel="apple-touch-icon" href="/icons/192.png" />
```

`display: "standalone"` → app trông giống native: không có address bar, chạy fullscreen.

### b) Service Worker — "Proxy giữa app và network"

Service Worker chạy **background thread** riêng, chặn mọi network request → quyết định trả từ cache hay network:

```javascript
// sw.js — Service Worker file
const CACHE_NAME = 'my-app-v1';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/styles.css',
    '/app.js',
    '/icons/192.png',
];

// INSTALL: cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(STATIC_ASSETS))
    );
    self.skipWaiting();  // Activate ngay, không chờ tab cũ đóng
});

// ACTIVATE: cleanup old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
            )
        )
    );
    self.clients.claim();
});

// FETCH: intercept requests → cache-first strategy
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then(cached => {
                if (cached) return cached;  // Có trong cache → trả ngay (offline OK!)

                return fetch(event.request).then(response => {
                    // Clone response và cache cho lần sau
                    const clone = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => cache.put(event.request, clone));
                    return response;
                });
            })
            .catch(() => caches.match('/offline.html'))  // Fallback offline page
    );
});
```

### Caching Strategies

```
1. Cache First (static assets):
   Request → Cache? → YES → Return cached
                    → NO  → Network → Cache → Return

2. Network First (API data):
   Request → Network? → OK → Cache → Return
                      → FAIL → Cache → Return (stale data)

3. Stale While Revalidate (mix):
   Request → Return cached immediately
          → Phía sau: fetch network → update cache
   → Lần sau user thấy data mới. Best UX!
```

### c) HTTPS — Bắt buộc

Service Workers chỉ chạy trên HTTPS (trừ localhost). Đây là yêu cầu bảo mật — bạn không muốn ai đó intercept service worker và inject malicious code.

---

## 2. Register Service Worker

```javascript
// main.js
if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
        try {
            const reg = await navigator.serviceWorker.register('/sw.js');
            console.log('SW registered:', reg.scope);

            // Khi có version mới
            reg.addEventListener('updatefound', () => {
                const newWorker = reg.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'activated') {
                        // Thông báo user: "New version available!"
                        showUpdateBanner();
                    }
                });
            });
        } catch (err) {
            console.error('SW registration failed:', err);
        }
    });
}
```

---

## 3. Với Frameworks (Vite PWA Plugin)

Tự viết service worker khá phức tạp. Trong production, dùng **Workbox** (Google) hoặc framework plugins:

```bash
npm install -D vite-plugin-pwa
```

```typescript
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
    plugins: [
        VitePWA({
            registerType: 'autoUpdate',
            manifest: {
                name: 'My App',
                short_name: 'MyApp',
                theme_color: '#3b82f6',
                icons: [
                    { src: '/icons/192.png', sizes: '192x192', type: 'image/png' },
                    { src: '/icons/512.png', sizes: '512x512', type: 'image/png' },
                ],
            },
            workbox: {
                globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
                runtimeCaching: [
                    {
                        urlPattern: /^https:\/\/api\.example\.com\/.*/i,
                        handler: 'NetworkFirst',
                        options: {
                            cacheName: 'api-cache',
                            expiration: { maxEntries: 50, maxAgeSeconds: 300 },
                        },
                    },
                ],
            },
        }),
    ],
});
// → Service Worker auto-generated + manifest + caching strategies!
```

---

## PWA Checklist

```
✅ manifest.json với name, icons (192 + 512), display: standalone
✅ Service Worker registered + caching strategy
✅ HTTPS (required)
✅ Responsive design (mobile-friendly)
✅ Offline fallback page
✅ Fast load (< 3s on 3G)

Kiểm tra: Chrome DevTools → Application tab → Manifest / Service Workers
Lighthouse: chạy PWA audit
```

---

## Bài tập thực hành

- [ ] Thêm manifest.json + icons cho website hiện có
- [ ] Service Worker: cache-first cho static, network-first cho API
- [ ] Offline page: hiển thị khi mất mạng
- [ ] Lighthouse PWA audit: đạt 100%

---

## Tài nguyên thêm

- [web.dev/progressive-web-apps](https://web.dev/progressive-web-apps/) — Google guide
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/) — Easiest setup
- [Workbox](https://developer.chrome.com/docs/workbox/) — Google's caching library
