# 🌍 CDN — Content Delivery Network

> `[BEGINNER → INTERMEDIATE]` — Prerequisite: hiểu HTTP, DNS cơ bản
> Mạng phân phối nội dung giúp website nhanh hơn toàn cầu.

---

## Tại sao cần CDN?

Hãy tưởng tượng server của bạn ở **Hà Nội**. User Mỹ truy cập → tín hiệu phải đi qua cáp quang **xuyên Thái Bình Dương** → ~250ms mỗi request! Với CDN, bản sao nội dung được đặt tại **edge servers** ở các thành phố lớn trên thế giới.

```
Không có CDN:                       Có CDN:
                                    
User (NY) ──15,000km──→ Server (HN)  User (NY) ──100km──→ Edge (NY)
Latency: ~250ms                      Latency: ~20ms ⚡
```

**CDN giúp:**
- **Latency giảm 10x+** — nội dung gần user hơn
- **Bandwidth giảm** — origin server không serve static files
- **DDoS protection** — absorb traffic tại edge
- **High availability** — nếu 1 PoP down, route đến PoP khác

---

## 1. Cách CDN hoạt động

```
User request: https://example.com/image.jpg
     │
     ▼
DNS resolves → CDN edge IP (nearest PoP)
     │
     ▼
Edge server (PoP)
  ├── Cache HIT?  → Return cached content 🚀 (< 20ms)
  └── Cache MISS? → Fetch from origin
                          │
                          ▼
                    Origin server
                    (your server)
                          │
                          ▼
              Edge caches response 
              → Returns to user
              → Next requests: Cache HIT
```

### Thuật ngữ quan trọng

| Thuật ngữ | Ý nghĩa |
|---|---|
| **PoP** (Point of Presence) | Data center chứa edge servers (~300 locations) |
| **Edge server** | Server tại PoP, gần user nhất |
| **Origin** | Server gốc của bạn (nơi chứa data thật) |
| **Cache HIT** | Content có sẵn tại edge → trả về ngay |
| **Cache MISS** | Content chưa có → fetch từ origin |
| **TTL** | Time To Live — thời gian cache hợp lệ |
| **Purge** | Xóa cache trên tất cả edges |

---

## 2. Cache-Control Headers — Kiểm soát caching

```
# Origin server trả về header chỉ định caching behavior:

Cache-Control: public, max-age=31536000    # CDN + browser cache 1 năm
Cache-Control: private, max-age=0          # CHỈ browser cache, không CDN
Cache-Control: no-cache                    # Luôn revalidate với origin
Cache-Control: no-store                    # KHÔNG cache (sensitive data)
```

```nginx
# Nginx config caching headers
server {
    # Static assets — cache lâu (CSS, JS, images)
    location ~* \.(css|js|png|jpg|gif|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # HTML pages — revalidate
    location ~* \.html$ {
        add_header Cache-Control "no-cache";  
        # Browser sẽ check ETag/Last-Modified trước khi dùng cache
    }
    
    # API responses — không cache
    location /api/ {
        add_header Cache-Control "private, no-cache, no-store";
    }
}
```

### Cache Invalidation Strategies

```
1. TTL-based:
   Cache-Control: max-age=3600  (1 giờ)
   → Sau 1 giờ, edge fetch lại từ origin
   
2. Cache busting (recommended ⭐):
   style.css → style.a1b2c3.css  (hash trong filename)
   → Mỗi lần build → hash mới → CDN fetch version mới
   → Old version vẫn cached cho users chưa refresh
   
3. Purge/Invalidate:
   POST /purge https://api.cloudflare.com/cache/purge
   → Xóa cache trên tất cả edges (2-5 giây)
   → Dùng khi cần invalidate ngay lập tức
   
4. Stale-While-Revalidate:
   Cache-Control: max-age=3600, stale-while-revalidate=86400
   → Serve stale content NGAY, revalidate in background
   → User không bao giờ thấy slow response
```

---

## 3. CDN Providers — So sánh

| Provider | Free Tier | Edge Locations | Đặc biệt |
|---|---|---|---|
| **Cloudflare** | ✅ Generous free tier | 300+ | CDN + WAF + DNS + Workers |
| **AWS CloudFront** | 1TB/month free | 450+ | Tích hợp AWS ecosystem |
| **Fastly** | ❌ | 90+ | Instant purge, VCL config |
| **Akamai** | ❌ | 4000+ | Enterprise, largest network |
| **Vercel Edge** | ✅ (limited) | 70+ | Next.js optimized |
| **BunnyCDN** | ❌ ($1/TB) | 100+ | Cheapest |

---

## 4. Edge Computing — Code tại CDN edge

CDN hiện đại cho phép **chạy code tại edge** (gần user), không cần gửi request về origin.

```javascript
// Cloudflare Workers — code chạy tại 300+ PoPs
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  // A/B testing tại edge — không cần origin
  if (Math.random() < 0.5) {
    return fetch('https://cdn.example.com/page-a.html');
  } else {
    return fetch('https://cdn.example.com/page-b.html');
  }
}
```

### Edge use cases

```
1. Geolocation routing:  Redirect user đến nearest server
2. A/B testing:          Random split tại edge
3. Authentication:       Validate JWT tại edge, block invalid
4. Image optimization:   Resize/compress tại edge based on device
5. Bot protection:       Block suspicious IPs tại edge
6. Personalization:      Customize response based on cookies/geo
```

---

## 5. Image Optimization via CDN

```
# URL-based image transformation (Cloudflare, imgix)
https://cdn.example.com/photo.jpg?width=300&quality=80&format=webp

# Cloudflare Image Resizing
https://example.com/cdn-cgi/image/width=300,quality=80,format=auto/photo.jpg

# Next.js Image Optimization (built-in CDN)
<Image src="/photo.jpg" width={300} height={200} />
```

---

## 6. CDN Architecture Patterns

### Multi-CDN

```
DNS-based Multi-CDN:
  User request → DNS → 
    ├── Cloudflare (primary, 70% traffic)
    └── CloudFront (fallback, 30% traffic)

Benefits:
  - No single CDN failure → redundancy  
  - Use each CDN's strengths per region
  - Price optimization
```

### Origin Shield

```
Không có Origin Shield:
  Edge A (NY)   → cache miss → fetch origin
  Edge B (LA)   → cache miss → fetch origin  
  Edge C (London)→ cache miss → fetch origin
  → Origin nhận 3 requests cho cùng 1 content!

Có Origin Shield:
  Edge A (NY)   → cache miss → Shield (Virginia)
  Edge B (LA)   → cache miss → Shield (Virginia) ← CACHE HIT!
  Edge C (London)→ cache miss → Shield (Virginia) ← CACHE HIT!
  Shield → cache miss → fetch origin (chỉ 1 lần!)
  → Origin chỉ nhận 1 request ⭐
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cache API responses vĩnh viễn | Set TTL phù hợp hoặc no-cache cho dynamic content | Data cũ → user thấy thông tin sai |
| 2 | Deploy code mới nhưng old CSS cached | Dùng cache busting: `style.[hash].css` | Content-hash tự invalidate khi thay đổi |
| 3 | Cache HTML pages với user data | `Cache-Control: private` hoặc `no-store` cho personalized content | User A thấy data của User B 😱 |
| 4 | Quên set CORS headers on CDN | Config CORS tại origin + CDN | Cross-origin requests fail |
| 5 | "CDN sẽ tự tối ưu mọi thứ" | CDN cần config đúng — cache rules, headers, purging | Bad config → worse performance |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Setup Cloudflare free tier cho website, check cache HIT/MISS trong headers
- [ ] **Bài 2 (Trung bình):** Config Cache-Control headers: static assets 1 năm, HTML no-cache, API no-store
- [ ] **Bài 3 (Trung bình):** Implement cache busting trong build pipeline (hash filenames)
- [ ] **Bài 4 (Khó):** Deploy Cloudflare Worker cho A/B testing hoặc geo-based routing

---

## Tài nguyên thêm

- [Cloudflare Learning Center](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/) — CDN fundamentals
- [Web.dev — HTTP Caching](https://web.dev/http-cache/) — Google caching guide
- [AWS CloudFront Developer Guide](https://docs.aws.amazon.com/cloudfront/) — AWS CDN
- [CDN Planet](https://www.cdnplanet.com/) — CDN comparison & tools
