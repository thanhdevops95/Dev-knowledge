# ⚡ Cloudflare Workers + Pages — Edge compute & static + dynamic

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Xong [00_what-is-cloudflare-overview](00_what-is-cloudflare-overview.md) và [01_cdn-dns-and-ssl](01_cdn-dns-and-ssl.md), biết JS/TS cơ bản, đã từng dùng Node.js Express

> 🎯 *Trụ cột "Developer Platform" của Cloudflare bắt đầu ở đây. Bạn học Workers (V8 isolate edge compute), Workers KV (eventual consistent), Durable Objects (strongly consistent stateful), Pages (static + dynamic edge functions), Pages Functions. Cuối bài làm hands-on Hono.js REST API live tại 320+ POPs cho Acme Shop, kèm KV để cache.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Workers V8 isolate** khác Lambda containerized thế nào (cold start ~0ms)
- [ ] Viết Worker cơ bản: route, fetch, Response object, environment bindings
- [ ] Phân biệt **Workers KV** vs **Durable Objects** — chọn đúng cho use case
- [ ] Hiểu **Cloudflare Pages** — static hosting + Pages Functions
- [ ] Phân biệt **Workers** vs **Pages Functions** — khi nào dùng cái nào
- [ ] Deploy **Hono.js REST API** cho Acme Shop lên Workers với KV cache
- [ ] Biết limits 2026: CPU time mặc định 30s (paid cấu hình lên tới 5 phút), 128MB RAM, 1MB script size

---

## Tình huống — Acme Shop cần API toàn cầu, không Lambda cold start

Acme Shop hiện chạy API trên AWS Lambda + API Gateway. Khách Đông Nam Á complain "API chậm 800ms-1.5s đôi khi". Bạn biết đó là Lambda cold start ở region `ap-southeast-1`. Mở rộng đa region thì chi phí gấp 3 + complexity.

Đồng nghiệp đề xuất: *"Sao không thử Cloudflare Workers? V8 isolate cold start gần như 0ms, deploy 1 lần là chạy ở mọi POP."*

Bạn nghi ngờ: Workers chỉ 30s CPU, không có filesystem, không có Postgres native — liệu đủ thay Lambda?

Bài này gỡ rối: Workers làm được gì + không làm được gì, kết hợp với KV/DO/Pages thành stack hoàn chỉnh.

---

## 1️⃣ Workers — V8 isolate, không phải container

🪞 **Ẩn dụ**: *Lambda như **thuê 1 căn hộ đầy đủ** cho mỗi tenant — phải dọn dẹp, lắp đặt khi khách mới (cold start 100-500ms). Workers như **bàn làm việc trong coworking** — mỗi customer 1 bàn cùng phòng chung, không cần xây phòng riêng (cold start ~0ms, V8 isolate share runtime).*

### Định nghĩa

**Workers** = serverless function của Cloudflare, chạy trên runtime **V8 isolate** (cùng engine với Chrome/Node.js nhưng kiến trúc isolate). Code JavaScript/TypeScript/WASM được Cloudflare deploy lên **mọi POP** trong 320+ vị trí.

### Workers vs Lambda — kiến trúc

| Tiêu chí | AWS Lambda | Cloudflare Workers |
|---|---|---|
| **Runtime** | Container (Firecracker microVM) | V8 isolate |
| **Cold start** | 100-500ms (Node), 1-5s (JVM) | ~0-5ms |
| **Concurrency model** | 1 instance / 1 request | 1 isolate xử lý nhiều request đồng thời |
| **CPU limit** | 15 phút (configurable) | 30s (10ms free tier) |
| **Memory** | 128MB - 10GB | 128MB |
| **Filesystem** | `/tmp` 512MB | Không có (Vô filesystem) |
| **Languages** | Node, Python, Java, Go, Ruby, .NET, custom | JS/TS, Rust→WASM, Python (alpha) |
| **Triggers** | API Gateway, S3, SQS, EventBridge, ... | HTTP, Cron, Queues, Email |
| **Region** | Single region | 320+ POPs global |
| **Pricing** | Per ms-GB + invocation | Per request (no GB-s) |

### Hello Worker

```typescript
// src/index.ts
export default {
    async fetch(
        request: Request,
        env: Env,
        ctx: ExecutionContext
    ): Promise<Response> {
        return new Response("Hello, edge world!");
    },
} satisfies ExportedHandler<Env>;
```

3 tham số:
- `request`: Standard `Request` object (Fetch API).
- `env`: Bindings — biến môi trường + KV/D1/R2/Service bindings.
- `ctx`: `ctx.waitUntil(promise)` cho task chạy sau khi response trả.

### Routing trong 1 Worker

Workers không có router built-in. Tự xử lý:

```typescript
export default {
    async fetch(request: Request): Promise<Response> {
        const url = new URL(request.url);

        switch (url.pathname) {
            case "/":
                return new Response("Home");
            case "/api/products":
                if (request.method !== "GET") {
                    return new Response("Method not allowed", { status: 405 });
                }
                return Response.json([{id: 1, name: "Phone"}]);
            default:
                return new Response("Not found", { status: 404 });
        }
    },
};
```

→ Manual switch dễ rối khi nhiều route. Khuyến nghị **Hono.js** framework (hands-on cuối bài).

### wrangler.toml — cấu hình Worker

```toml
name = "acmeshop-api"
main = "src/index.ts"
compatibility_date = "2026-05-01"
compatibility_flags = ["nodejs_compat"]

# Tài nguyên gắn vào Worker
[[kv_namespaces]]
binding = "PRODUCTS_KV"
id = "abc123..."

[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "acmeshop-uploads"

[[d1_databases]]
binding = "DB"
database_name = "acmeshop-db"
database_id = "xyz789..."

[vars]
ENVIRONMENT = "production"

# Secrets không đặt ở đây — dùng `wrangler secret put`

# Multi-environment
[env.staging]
name = "acmeshop-api-staging"
vars = { ENVIRONMENT = "staging" }
```

### Bindings — cách Worker access tài nguyên khác

| Binding | Mô tả | Ví dụ trong code |
|---|---|---|
| `vars` | Env variables (plain text) | `env.ENVIRONMENT` |
| `secret` | Secrets | `env.API_KEY` (set qua `wrangler secret put`) |
| `kv_namespaces` | Workers KV | `env.PRODUCTS_KV.get("key")` |
| `r2_buckets` | R2 bucket | `env.UPLOADS.put("file.jpg", data)` |
| `d1_databases` | D1 SQLite | `env.DB.prepare("SELECT 1").all()` |
| `queues` | Cloudflare Queues | `env.QUEUE.send({...})` |
| `services` | Service binding (Worker → Worker) | `env.OTHER_WORKER.fetch(...)` |
| `durable_objects` | Durable Object | `env.COUNTER.get(id)` |
| `ai` | Workers AI | `env.AI.run("@cf/llama-3", {...})` |

### Giới hạn (limits) Workers Free vs Paid

| Limit | Free | Paid ($5/tháng) |
|---|---|---|
| Requests/ngày | 100k | 10M included, $0.30/M sau |
| CPU time/request | 10ms | 30s |
| Memory/request | 128MB | 128MB |
| Script size | 1MB compressed | 10MB |
| Subrequest/request | 50 | 1000 |
| Environment variables | 64 | 128 |

---

## 2️⃣ Workers KV — eventual consistent key-value

🪞 **Ẩn dụ**: *KV như **thông báo dán bảng tin chung** ở mọi chi nhánh — bạn đính giấy ở Hà Nội, vài giây sau Hồ Chí Minh + Singapore mọi nơi cũng thấy. Nhưng nếu 2 người cùng ghi giấy mới đè cái cũ — Cloudflare không bảo đảm thứ tự, chỉ "rồi đến lúc đều thống nhất".*

### Đặc điểm

| Đặc điểm | Mô tả |
|---|---|
| **Storage model** | Key-value (key string, value bytes/JSON) |
| **Consistency** | Eventual — write tới mọi POP < 60s |
| **Read latency** | < 10ms tại POP đã cache (HOT) |
| **Write latency** | ~100-300ms |
| **Use case** | Config, feature flag, cache, session (read-heavy) |
| **Limits free** | 100k read/ngày, 1k write/ngày, 1 GB total |

### Tạo KV namespace

```bash
# Tạo namespace
wrangler kv:namespace create PRODUCTS_KV
# Output: id = "abc123..."

# Add vào wrangler.toml
[[kv_namespaces]]
binding = "PRODUCTS_KV"
id = "abc123..."

# CLI put/get
wrangler kv:key put --binding=PRODUCTS_KV "p:1" '{"id":1,"name":"Phone"}'
wrangler kv:key get --binding=PRODUCTS_KV "p:1"
wrangler kv:key list --binding=PRODUCTS_KV
wrangler kv:key delete --binding=PRODUCTS_KV "p:1"
```

### Trong Worker code

```typescript
export default {
    async fetch(request: Request, env: Env): Promise<Response> {
        const url = new URL(request.url);
        const id = url.pathname.split("/").pop();

        // Get
        const cached = await env.PRODUCTS_KV.get(`p:${id}`, "json");
        if (cached) {
            return Response.json(cached, {
                headers: { "X-Cache": "HIT" }
            });
        }

        // Miss → fetch origin
        const product = await fetchFromOrigin(id);

        // Put (TTL 1 giờ)
        await env.PRODUCTS_KV.put(
            `p:${id}`,
            JSON.stringify(product),
            { expirationTtl: 3600 }
        );

        return Response.json(product, {
            headers: { "X-Cache": "MISS" }
        });
    },
};
```

### Eventual consistency — điểm dễ vấp (gotcha)

```typescript
// Worker A (POP Singapore) tại t=0:
await env.KV.put("counter", "5");

// Worker B (POP New York) tại t=0.5s:
const v = await env.KV.get("counter");
// Có thể trả "4" (giá trị cũ) — chưa propagate!

// Worker B tại t=70s:
const v2 = await env.KV.get("counter");
// "5" (đã propagate)
```

→ **Không dùng KV** cho:
- Counter realtime (race condition).
- Inventory (đếm số hàng còn).
- Session phải atomic.

→ **Dùng KV** cho:
- Cache.
- Feature flag (cập nhật chậm OK).
- Config (gần immutable).
- Lookup table.

---

## 3️⃣ Durable Objects — strongly consistent stateful

🪞 **Ẩn dụ**: *Durable Object như **két sắt ngân hàng có ổ khoá** — mỗi DO instance là 1 actor đơn lẻ giữ state, mọi request liên quan đến nó đều xếp hàng vào 1 cửa. Cloudflare đảm bảo **chỉ 1 instance** chạy 1 lúc cho 1 ID → atomic operation.*

### Định nghĩa

**Durable Objects (DO)** = stateful object trên Cloudflare edge. Mỗi DO instance có:
- ID duy nhất (chuỗi hex).
- State persistent (storage object built-in).
- **1 instance chạy 1 lúc** — không race condition.
- Tự động "near user" sau invocation đầu (geographic affinity).

### Khi nào dùng DO

| Use case | DO phù hợp |
|---|---|
| Counter atomic (likes, votes) | ✅ |
| Chat room (mỗi room = 1 DO) | ✅ |
| Online game (mỗi match = 1 DO) | ✅ |
| Rate limiter chính xác | ✅ |
| Auction (1 item = 1 DO, bid order matter) | ✅ |
| Lookup cache (read-heavy) | ❌ Dùng KV |
| Bulk data | ❌ Dùng R2 / D1 |

### Code mẫu — Counter

```typescript
// Define DO class
export class Counter {
    state: DurableObjectState;

    constructor(state: DurableObjectState) {
        this.state = state;
    }

    async fetch(request: Request): Promise<Response> {
        // Get current count from storage
        let count = (await this.state.storage.get<number>("count")) ?? 0;
        count++;
        await this.state.storage.put("count", count);

        return Response.json({ count });
    }
}

// Worker fetch handler
export default {
    async fetch(request: Request, env: Env): Promise<Response> {
        // Get DO instance by name
        const id = env.COUNTER.idFromName("global");
        const stub = env.COUNTER.get(id);

        // Forward request to DO
        return stub.fetch(request);
    },
};
```

### wrangler.toml cho DO

```toml
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"

[[migrations]]
tag = "v1"
new_classes = ["Counter"]
```

### Giá

DO là **Workers Paid only** ($5/tháng). Pricing:
- Request: $0.15/M.
- Duration: $12.50/M GB-s.
- Storage: $0.20/GB-month.

### Lưu ý: SQLite-backed DO (2024+)

Cloudflare giới thiệu **SQLite-backed Durable Objects** — mỗi DO có SQLite riêng (vs key-value storage truyền thống). Cho phép query SQL trong DO. Beta 2025, ổn định 2026.

---

## 4️⃣ Cloudflare Pages — static hosting + Functions

🪞 **Ẩn dụ**: *Pages là **"Vercel/Netlify của Cloudflare"** — bạn push code lên GitHub, Cloudflare auto-build static site, deploy lên CDN edge. Khác Vercel/Netlify: nằm trên hạ tầng Cloudflare → Workers/KV/R2 tích hợp sẵn, free tier siêu rộng.*

### Workflow của Pages

```
1. Connect GitHub repo
2. Choose framework preset (Next.js, Astro, Hugo, ...)
3. Build settings (build command, output dir)
4. Deploy
5. Every git push → auto build + deploy
   - Production: branch `main`
   - Preview: mọi branch khác → URL riêng
```

### Tạo Pages project

**Qua Dashboard**: Workers & Pages → Create → Pages → Connect Git → chọn repo.

**Qua wrangler**:

```bash
# Direct upload (không qua Git)
npx wrangler pages deploy ./dist --project-name=acmeshop-web
```

### Framework presets hỗ trợ 2026

| Framework | Preset | Note |
|---|---|---|
| **Next.js** | ✅ Next-on-Pages | Edge runtime, SSR via Functions |
| **Astro** | ✅ | SSG + edge SSR |
| **SvelteKit** | ✅ | adapter-cloudflare |
| **Nuxt** | ✅ | Nuxt 3 Nitro preset |
| **Remix** | ✅ | cloudflare-pages adapter |
| **Hugo** | ✅ | Pure SSG |
| **Jekyll** | ✅ | Pure SSG |
| **Gatsby** | ✅ | SSG |
| **Vue/React/Angular** (Vite) | ✅ | SPA |

### Deploy static thuần (static-only)

Nếu site chỉ static (Hugo, Jekyll, plain HTML):
- Build → output static files trong `dist/` hoặc `public/`.
- Pages serve qua CDN với cache-control thông minh.
- Custom domain + SSL + unlimited bandwidth.

### Pages Functions — logic động

Trong Pages project, thêm folder `functions/`:

```
acmeshop-web/
├── functions/
│   ├── api/
│   │   ├── products.ts          → GET /api/products
│   │   └── products/[id].ts     → GET /api/products/123
│   └── _middleware.ts
├── public/
│   ├── index.html
│   └── style.css
```

```typescript
// functions/api/products.ts
export const onRequestGet: PagesFunction<Env> = async (context) => {
    const { env, request } = context;
    const products = await env.DB.prepare("SELECT * FROM products").all();
    return Response.json(products.results);
};
```

### Pages Functions vs Workers — khác gì

| Tiêu chí | Pages Functions | Workers |
|---|---|---|
| **Setup** | Add file vào `functions/` | Tạo project Worker riêng |
| **Routing** | File-based (giống Next.js API routes) | Manual switch hoặc Hono |
| **Triển khai** | Cùng với Pages site (1 lần `git push`) | `wrangler deploy` riêng |
| **Bindings** | Cùng config Pages | wrangler.toml |
| **Use case** | Static site cần dynamic API nhỏ | Standalone API/service |
| **Limits** | Giống Workers (10ms free, 30s paid) | Giống |

### Khi nào dùng Pages vs Workers thuần

| Use case | Choice |
|---|---|
| Static blog | Pages thuần (no Functions) |
| Marketing site + form submit | Pages + Functions |
| Next.js SSR | Pages với Next-on-Pages |
| Pure API microservice | Workers thuần |
| WebSocket / real-time | Workers + Durable Objects |
| Cron job | Workers + scheduled trigger |

---

## 5️⃣ Service Bindings — Worker gọi Worker

Worker A có thể gọi Worker B **không qua HTTP** mà qua **service binding** — fast (in-process) và free (không tính subrequest).

```toml
# Worker A's wrangler.toml
[[services]]
binding = "AUTH"
service = "auth-worker"
```

```typescript
// In Worker A
const authResp = await env.AUTH.fetch("https://internal/verify", {
    method: "POST",
    body: JSON.stringify({ token }),
});
```

→ Worker A gọi Worker B trong cùng POP, 0ms overhead, 0 cost. Pattern cho microservice.

---

## 6️⃣ Triggers — không chỉ HTTP

Workers chạy bởi nhiều loại trigger:

| Trigger | Mô tả | Use case |
|---|---|---|
| **HTTP** | `fetch(request)` handler | API, web service |
| **Cron** | `scheduled(event)` handler | Daily job, cleanup, sync |
| **Queues** | `queue(batch)` handler | Background processing |
| **Email** | `email(message)` handler | Process inbound email |
| **WebSocket** | Through Durable Objects | Chat, realtime |
| **Tail** | Real-time log forwarding | Observability |

### Cron Trigger

```toml
[triggers]
crons = ["0 2 * * *"]  # 2:00 UTC daily
```

```typescript
export default {
    async fetch() { /* ... */ },
    async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
        console.log("Cron fired:", event.cron);
        await env.DB.prepare("DELETE FROM sessions WHERE expires_at < ?").bind(Date.now()).run();
    },
};
```

→ Cron Workers free tier: 1 trigger per worker.

---

## 🛠️ Hands-on — Hono.js REST API cho Acme Shop với KV cache

### Mục tiêu

Bạn deploy 1 REST API cho Acme Shop:
- `GET /api/products` — list (cache 5 min trong KV)
- `GET /api/products/:id` — detail (cache 1 hour)
- `POST /api/products` — create (invalidate cache)

API chạy ở 320+ POPs, latency < 30ms global.

### Bước 1 — Khởi tạo project với Hono

```bash
mkdir acmeshop-api && cd acmeshop-api
npm create hono@latest -- . --template cloudflare-workers
# Chọn: cloudflare-workers
npm install
```

Output structure:

```
acmeshop-api/
├── src/
│   └── index.ts
├── wrangler.toml
├── package.json
└── tsconfig.json
```

### Bước 2 — Tạo KV namespace

```bash
wrangler kv:namespace create PRODUCTS_KV
# id = "abc123def456..."
```

Update `wrangler.toml`:

```toml
name = "acmeshop-api"
main = "src/index.ts"
compatibility_date = "2026-05-01"

[[kv_namespaces]]
binding = "PRODUCTS_KV"
id = "abc123def456..."

[vars]
ENVIRONMENT = "production"
```

### Bước 3 — Code Hono router

```typescript
// src/index.ts
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

type Bindings = {
    PRODUCTS_KV: KVNamespace;
    ENVIRONMENT: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.use('*', logger());
app.use('*', cors());

// Mock origin data (in real app: D1 or external API)
const PRODUCTS = [
    { id: 1, name: 'iPhone 15', price: 999 },
    { id: 2, name: 'MacBook Pro', price: 1999 },
    { id: 3, name: 'AirPods', price: 249 },
];

// Health check
app.get('/', (c) => c.json({
    service: 'acmeshop-api',
    env: c.env.ENVIRONMENT,
    colo: c.req.raw.cf?.colo ?? 'unknown',
}));

// List products with KV cache
app.get('/api/products', async (c) => {
    const cacheKey = 'products:list';
    const cached = await c.env.PRODUCTS_KV.get(cacheKey, 'json');

    if (cached) {
        return c.json(cached, 200, { 'X-Cache': 'HIT' });
    }

    // Simulate origin fetch (could be D1, external API, ...)
    const products = PRODUCTS;

    // Cache 5 min
    await c.env.PRODUCTS_KV.put(cacheKey, JSON.stringify(products), {
        expirationTtl: 300,
    });

    return c.json(products, 200, { 'X-Cache': 'MISS' });
});

// Get product detail
app.get('/api/products/:id', async (c) => {
    const id = c.req.param('id');
    const cacheKey = `product:${id}`;
    const cached = await c.env.PRODUCTS_KV.get(cacheKey, 'json');

    if (cached) {
        return c.json(cached, 200, { 'X-Cache': 'HIT' });
    }

    const product = PRODUCTS.find(p => p.id === Number(id));
    if (!product) {
        return c.json({ error: 'Not found' }, 404);
    }

    // Cache 1 hour
    await c.env.PRODUCTS_KV.put(cacheKey, JSON.stringify(product), {
        expirationTtl: 3600,
    });

    return c.json(product, 200, { 'X-Cache': 'MISS' });
});

// Create product (mock — invalidate cache)
app.post('/api/products', async (c) => {
    const body = await c.req.json();
    // ... save to DB

    // Invalidate list cache
    await c.env.PRODUCTS_KV.delete('products:list');

    return c.json({ ok: true, id: 999 }, 201);
});

// 404
app.notFound((c) => c.json({ error: 'Not found' }, 404));

export default app;
```

### Bước 4 — Dev local

```bash
wrangler dev
# ⛅️ Ready on http://localhost:8787
```

Test:

```bash
curl http://localhost:8787/
# {"service":"acmeshop-api","env":"production","colo":"local"}

curl http://localhost:8787/api/products
# [{"id":1,"name":"iPhone 15",...}]
# Header: X-Cache: MISS (lần đầu)

curl http://localhost:8787/api/products
# Header: X-Cache: HIT (lần sau)
```

### Bước 5 — Deploy production

```bash
wrangler deploy
# Total Upload: 24.5 KiB
# Uploaded acmeshop-api (1.2 sec)
# Published acmeshop-api (0.5 sec)
#   https://acmeshop-api.<your-subdomain>.workers.dev
```

### Bước 6 — Test production

```bash
URL="https://acmeshop-api.<your-subdomain>.workers.dev"

curl $URL/
# {"service":"acmeshop-api","env":"production","colo":"SIN"}

curl -v $URL/api/products 2>&1 | grep -i x-cache
# < x-cache: MISS  (lần đầu)

curl -v $URL/api/products 2>&1 | grep -i x-cache
# < x-cache: HIT   (lần sau)

# Test latency
time curl -s $URL/api/products > /dev/null
# real 0m0.045s
```

### Bước 7 — Tail logs

```bash
wrangler tail acmeshop-api
# Hit endpoint vài lần → thấy log realtime
```

### Bước 8 — Custom domain (tuỳ chọn)

```bash
# Trong Cloudflare Dashboard:
# Workers & Pages → acmeshop-api → Settings → Triggers
# Custom Domain → Add Custom Domain → api.acmeshop.vn
# (Zone phải đã add vào Cloudflare)
```

→ **Kết quả**: REST API chạy 320+ POPs, KV cache hit < 10ms, MISS đi origin và cache lại. Cost: $0 cho 100k requests/ngày free.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Dùng KV như database transactional

**Triệu chứng**: Inventory đếm sai khi nhiều người mua cùng lúc. Counter likes mất số.

**Nguyên nhân**: KV eventual consistent. Read-modify-write race condition.

**Cách tránh**:
- Counter / inventory → **Durable Objects**.
- KV chỉ cho cache, config, feature flag.

### ❌ Cạm bẫy: Vượt 10ms CPU free tier

**Triệu chứng**: Worker bị kill khi compute nặng (parse JSON lớn, hash, ...). Error 1102.

**Nguyên nhân**: Free tier 10ms CPU/request. Heavy compute → exceed.

**Cách tránh**:
- Upgrade Workers Paid ($5/tháng, 30s CPU).
- Hoặc offload heavy work cho Queues (background).
- Hoặc dùng `ctx.waitUntil()` để chạy async sau response trả.

### ❌ Cạm bẫy: Quên `compatibility_date`

**Triệu chứng**: Worker chạy local OK, deploy production behavior khác.

**Nguyên nhân**: Mỗi date có set runtime flags khác. Mất `compatibility_date` → default cũ → thiếu API mới.

**Cách tránh**: Luôn set `compatibility_date = "YYYY-MM-DD"` trong `wrangler.toml`. Update khi cần feature mới.

### ❌ Cạm bẫy: Workers Free không có subrequest tới chính domain

**Triệu chứng**: Worker A fetch tới Worker B trên cùng zone → "loop detected".

**Nguyên nhân**: Free tier không cho Worker fetch tới cùng zone (anti-loop).

**Cách tránh**:
- Dùng **Service Binding** (kết nối in-process).
- Hoặc upgrade Paid.

### ❌ Cạm bẫy: Pages Functions vs Workers — config nhầm

**Triệu chứng**: Set binding KV trong Pages Functions nhưng code `env.KV` không thấy.

**Nguyên nhân**: Pages bindings ở Dashboard (Settings → Functions → KV namespace bindings), không phải wrangler.toml.

**Cách tránh**:
- Pages → Settings → Functions: setup bindings ở đây.
- Hoặc dùng `wrangler.toml` cho Pages mới (2024+ support).

### ❌ Cạm bẫy: `ctx.waitUntil` quên

**Triệu chứng**: Async logging/analytics không chạy. Worker trả response xong, async task bị cancel.

**Nguyên nhân**: Sau khi response trả, Worker terminate. Pending promise bị abort.

**Cách tránh**: Bọc async task vào `ctx.waitUntil(promise)` để Worker giữ alive cho task xong.

```typescript
ctx.waitUntil(logToAnalytics(request));
return new Response("OK");
```

### ❌ Cạm bẫy: Bundle size > 1MB

**Triệu chứng**: `wrangler deploy` fail với "script too large".

**Nguyên nhân**: Free tier 1MB compressed. Import lib lớn (vd: full lodash).

**Cách tránh**:
- Tree-shake imports.
- Dynamic import.
- Upgrade Paid (10MB).
- Hoặc Workers Smart Placement + R2 để serve assets.

### ❌ Cạm bẫy: Workers `Date.now()` không thay đổi trong 1 request

**Triệu chứng**: Code dùng `Date.now()` trả cùng giá trị nhiều lần trong 1 request.

**Nguyên nhân**: Workers freeze time tại request boundary để chống timing attack.

**Cách tránh**:
- Acceptable cho hầu hết logic.
- Nếu cần thời gian thực: dùng external time API hoặc Durable Object alarm.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Workers cold start ~0ms — vì sao? Lambda thì 100-500ms.

<details>
<summary>💡 Đáp án</summary>

**Workers**: V8 isolate share runtime. 1 V8 process load sẵn, isolate mới là "ngăn cách memory" 1-5ms tạo. Không cần khởi container.

**Lambda**: Mỗi function instance = 1 container (Firecracker microVM). Khởi container + load runtime (Node 100-200ms, JVM 1-5s) → cold start.
</details>

**Q2.** Khi nào KV, khi nào Durable Object?

<details>
<summary>💡 Đáp án</summary>

- **KV**: Read-heavy, eventual consistent OK (cache, feature flag, config, lookup).
- **Durable Object**: Strong consistency cần (counter, room, rate limit, auction). 1 DO instance = 1 actor = no race condition.
</details>

**Q3.** Pages Functions vs Workers — khi nào dùng cái nào?

<details>
<summary>💡 Đáp án</summary>

- **Pages Functions**: Static site + chút dynamic logic (form submit, contact, OG image gen). Tích hợp file-based routing với Pages.
- **Workers thuần**: Standalone API/microservice. Linh hoạt routing, độc lập với static site.
</details>

**Q4.** `ctx.waitUntil(promise)` để làm gì?

<details>
<summary>💡 Đáp án</summary>

Giữ Worker alive đến khi promise resolve, kể cả khi response đã trả. Dùng cho async task non-blocking như log, analytics, cache warm-up. Không dùng → task bị cancel khi response trả.
</details>

**Q5.** Free tier Workers: 100k req/ngày → tương đương bao nhiêu req/giây trung bình?

<details>
<summary>💡 Đáp án</summary>

100,000 / 86,400 ≈ 1.16 req/s. Free đủ chạy 1 personal project / 1 nội bộ team nhỏ. Khi spike (>100 req/s vài giây) cũng OK miễn tổng ngày < 100k.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh / cách |
|---|---|
| Init Worker | `npm create cloudflare@latest` |
| Init với Hono | `npm create hono@latest` |
| Dev local | `wrangler dev` |
| Deploy | `wrangler deploy` |
| Tail logs | `wrangler tail <name>` |
| Tạo KV namespace | `wrangler kv:namespace create <NAME>` |
| KV put | `wrangler kv:key put --binding=<NAME> "k" "v"` |
| Set secret | `wrangler secret put MY_SECRET` |
| Service binding | `[[services]]` trong wrangler.toml |
| Cron trigger | `[triggers] crons = ["0 2 * * *"]` |
| Pages deploy direct | `wrangler pages deploy ./dist --project-name=X` |
| Compatibility date | `compatibility_date = "2026-05-01"` |
| Bindings trong code | `env.MY_KV.get(...)` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN / Giải thích |
|---|---|
| **Worker** | Function code chạy ở edge (V8 isolate) |
| **V8 isolate** | Sandbox lightweight chia sẻ V8 runtime — cold start ~0ms |
| **Binding** | Cách Worker truy cập tài nguyên (KV/R2/DO/...) |
| **KV** | Workers KV — eventual consistent key-value |
| **Durable Object (DO)** | Stateful object, strong consistent, 1 instance/ID |
| **Pages** | Static + dynamic site hosting (Vercel-like) |
| **Pages Functions** | API serverless trong Pages project (file-based routing) |
| **Service Binding** | Worker A gọi Worker B in-process |
| **Cron Trigger** | Worker chạy theo schedule cron |
| **wrangler.toml** | Config file Worker |
| **compatibility_date** | Snapshot ngày của runtime API |
| **ctx.waitUntil** | Giữ Worker alive cho async task |
| **Hono** | Web framework siêu nhẹ cho Workers/edge |
| **Subrequest** | Fetch từ Worker ra external (max 50 free / 1000 paid) |
| **Smart Placement** | Cloudflare tự chọn POP gần origin nhất |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Cloudflare CDN + DNS + SSL — Foundation của edge](01_cdn-dns-and-ssl.md)
- ➡️ **Bài tiếp theo:** [Cloudflare R2 + D1 + Queues — Storage & data layer ở edge](03_r2-and-d1-and-queues.md) — Storage layer
- ↑ **Về cụm:** [Cloudflare README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- ☁️ [AWS Lambda + API Gateway](../../../aws/lessons/01_basic/04_lambda-and-api-gateway.md) — so sánh
- ☁️ [GCP Cloud Functions + Run](../../../gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md) — so sánh
- 🌐 [Serverless](../../../serverless/) — paradigm chung
- 🟦 [TypeScript](../../../../03_languages/javascript-typescript/) — code Worker

### Tài nguyên ngoài (2026)
- 📖 [Workers docs](https://developers.cloudflare.com/workers/)
- 📖 [Hono framework](https://hono.dev/)
- 📖 [Workers KV docs](https://developers.cloudflare.com/kv/)
- 📖 [Durable Objects docs](https://developers.cloudflare.com/durable-objects/)
- 📖 [Pages docs](https://developers.cloudflare.com/pages/)
- 📖 [Pages Functions docs](https://developers.cloudflare.com/pages/functions/)
- 📖 [Workers Examples](https://developers.cloudflare.com/workers/examples/)
- 📖 [Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)
- 📖 [Next-on-Pages](https://github.com/cloudflare/next-on-pages)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 02 cluster Cloudflare basic. Workers V8 isolate vs Lambda + KV eventual consistent + Durable Objects strong consistent + Pages static + Pages Functions + Service Bindings + Cron triggers + hands-on Hono.js REST API Acme Shop với KV cache + 8 pitfalls. Pattern theo AWS/GCP lesson 04 (compute).
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
