# 💾 Cloudflare R2 + D1 + Queues — Storage & data layer ở edge

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.2\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026
> **Level:** Basic (bài 03/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Xong [02_workers-and-pages](02_workers-and-pages.md), biết SQL cơ bản, đã từng dùng S3 (hoặc bất kỳ object storage)

> 🎯 *Stack Cloudflare developer chưa hoàn chỉnh nếu thiếu storage layer. Bài này dạy 4 service: **R2** (object storage S3-compatible zero egress), **D1** (SQLite edge-replicated), **Queues** (message queue), **Hyperdrive** (Postgres connection pool từ edge). Cuối bài làm hands-on Acme Shop image upload (R2) + product catalog (D1) + order processing (Queues). So sánh R2 vs S3 cost — minh hoạ vì sao Cloudflare thắng cuộc.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **R2 S3-compatible** + zero egress — vì sao thay được S3
- [ ] Đọc/ghi R2 từ Worker + presigned URL + multipart upload
- [ ] Hiểu **D1 SQLite edge-replicated** — limit + use case + when not
- [ ] Migrations + prepared statements D1
- [ ] Hiểu **Queues** — producer/consumer pattern + DLQ
- [ ] Biết **Hyperdrive** — connection pool Postgres từ Workers
- [ ] Tính được **R2 vs S3 cost** cho workload thật
- [ ] Hands-on: upload image (R2) + lưu metadata (D1) + queue resize task

---

## Tình huống — Acme Shop chi $1500/tháng cho S3 + RDS, muốn giảm

Acme Shop hiện:
- **S3**: 5TB ảnh sản phẩm + 200TB egress/tháng (khách xem ảnh) = **$18,000/tháng** chỉ riêng egress.
- **RDS Postgres**: db.r6g.large Multi-AZ = $400/tháng cho catalog 5GB.
- **SQS**: $50/tháng cho 10M messages xử lý ảnh.

Bạn được giao "POC chuyển sang Cloudflare nếu rẻ hơn 50%". Có thật không?

Bài này tính chi tiết + hướng dẫn migrate. Spoiler: R2 zero egress → tiết kiệm $18,000/tháng. Nhưng có trade-off cần biết.

---

## 1️⃣ R2 — Object storage S3-compatible, zero egress

🪞 **Ẩn dụ**: *S3 như **gửi xe trong garage trả phí cả tiền vào và tiền ra**. R2 như **garage cũng tốt, tiền gửi rẻ hơn, tiền ra MIỄN PHÍ** — bạn không tốn xu nào khi khách lấy xe đi. Đó là cách Cloudflare đánh bại S3 cho workload high-egress.*

### Định nghĩa

**R2** = object storage của Cloudflare, ra mắt GA 2022. Đặc điểm:
- **S3-compatible API** — code dùng AWS SDK chạy thẳng (chỉ đổi endpoint).
- **Zero egress fee** — không tính tiền dữ liệu ra.
- **Không có region** — bucket global, replicate tự động.
- **Pricing**: $0.015/GB-month storage + $4.50/M Class A op + $0.36/M Class B op. Egress = $0.

### Giá chi tiết

| Item | R2 | S3 (us-east-1) |
|---|---|---|
| Storage / GB-month | $0.015 | $0.023 |
| Class A ops (PUT, COPY, POST, LIST) | $4.50 / M | $5.00 / M |
| Class B ops (GET, HEAD) | $0.36 / M | $0.40 / M |
| **Egress (data out)** | **$0** | **$0.09 / GB** (first 10TB) |
| Free tier | 10 GB storage, 1M Class A, 10M Class B / tháng | 5 GB 12-month |

### Tính nhanh cho Acme Shop

| Item | Volume / tháng | R2 cost | S3 cost |
|---|---|---|---|
| Storage 5 TB | 5,120 GB | $76.80 | $117.76 |
| 1M Class A (uploads) | 1M | $4.50 | $5.00 |
| 200M Class B (downloads) | 200M | $72.00 | $80.00 |
| Egress 200 TB | 200,000 GB | **$0** | **$18,000** |
| **TỔNG** | | **$153** | **$18,203** |

→ Acme Shop tiết kiệm $18,050/tháng (99.2%). Đây là lý do R2 mạnh nhất khi egress lớn.

### Khi R2 KHÔNG thắng

| Workload | S3 vẫn tốt hơn |
|---|---|
| Egress thấp (<1 TB/tháng) | Ngưỡng break-even, S3 quen thuộc hơn |
| Stack đã AWS-only | Inter-service S3 → Lambda zero egress trong region |
| Cần Glacier deep archive | R2 chưa có cold tier deep |
| Cần S3 Object Lambda / Replication features | R2 thiếu |
| Compliance bắt region cụ thể (VN data residency) | R2 ít quyền control region (tình trạng *tính đến Q1 2026*; Jurisdictional Restrictions/Location Hints là tính năng dự kiến/đã ra tuỳ thời điểm — kiểm tra docs hiện hành) |

### Tạo R2 bucket

```bash
# Tạo bucket
wrangler r2 bucket create acmeshop-uploads

# List
wrangler r2 bucket list

# Upload object
wrangler r2 object put acmeshop-uploads/test.jpg --file=./test.jpg

# Get
wrangler r2 object get acmeshop-uploads/test.jpg --file=./downloaded.jpg

# Delete
wrangler r2 object delete acmeshop-uploads/test.jpg
```

### R2 từ Worker

```toml
# wrangler.toml
[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "acmeshop-uploads"
```

```typescript
// Upload
const ab = await request.arrayBuffer();
await env.UPLOADS.put('product-1/main.jpg', ab, {
    httpMetadata: { contentType: 'image/jpeg' },
    customMetadata: { uploadedBy: 'user-42', productId: '1' },
});

// Download
const obj = await env.UPLOADS.get('product-1/main.jpg');
if (!obj) return new Response('Not found', { status: 404 });
return new Response(obj.body, {
    headers: { 'content-type': obj.httpMetadata?.contentType ?? 'application/octet-stream' },
});

// List
const list = await env.UPLOADS.list({ prefix: 'product-1/' });
for (const obj of list.objects) {
    console.log(obj.key, obj.size);
}

// Delete
await env.UPLOADS.delete('product-1/main.jpg');
```

### Tương thích S3 API — dùng AWS SDK

```typescript
// R2 hoạt động với AWS SDK v3 (cho legacy code migration)
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const s3 = new S3Client({
    region: 'auto',
    endpoint: `https://<account-id>.r2.cloudflarestorage.com`,
    credentials: {
        accessKeyId: process.env.R2_ACCESS_KEY_ID,
        secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
    },
});

await s3.send(new PutObjectCommand({
    Bucket: 'acmeshop-uploads',
    Key: 'test.jpg',
    Body: data,
}));
```

→ Tạo access key: Dashboard → R2 → Manage R2 API Tokens.

### Public bucket + custom domain

R2 mặc định **private**. Để serve public:

**Cách 1**: Worker làm proxy (recommended — control + WAF).

**Cách 2**: R2.dev subdomain (free, dev only):
- Dashboard → R2 → Settings → Public access → Allow Access.
- URL: `https://pub-<hash>.r2.dev/<key>`

**Cách 3**: Custom domain (production):
- R2 → Settings → Connect Domain → `cdn.acmeshop.vn`.
- Cloudflare auto-config DNS + SSL.
- Cache tự động qua CDN.

### Presigned URL

Cho phép client upload/download trực tiếp R2 (không qua Worker):

```typescript
import { AwsClient } from 'aws4fetch';

const r2 = new AwsClient({
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
});

const url = new URL(`https://${ACCOUNT_ID}.r2.cloudflarestorage.com/acmeshop-uploads/upload-${Date.now()}.jpg`);
url.searchParams.set('X-Amz-Expires', '3600');

const signed = await r2.sign(
    new Request(url, { method: 'PUT' }),
    { aws: { signQuery: true } }
);

return Response.json({ uploadUrl: signed.url });
```

Client:

```typescript
const presigned = await fetch('/api/upload-url').then(r => r.json());
await fetch(presigned.uploadUrl, { method: 'PUT', body: file });
```

### Multipart upload

Cho file > 5GB hoặc resumable upload:

```typescript
// Init
const mp = await env.UPLOADS.createMultipartUpload('big-video.mp4');

// Upload parts (parallel)
const parts = await Promise.all([
    mp.uploadPart(1, part1Data),
    mp.uploadPart(2, part2Data),
    mp.uploadPart(3, part3Data),
]);

// Complete
await mp.complete(parts);
```

---

## 2️⃣ D1 — SQLite edge-replicated

🪞 **Ẩn dụ**: *D1 như **sổ ghi chép giống nhau ở mọi chi nhánh** — viết bản chính 1 chỗ, vài giây sau mọi chi nhánh thấy. Đọc thì lấy từ chi nhánh gần. Không phải Postgres mạnh — là SQLite "phân tán" thông minh.*

### Định nghĩa

**D1** = managed SQLite của Cloudflare. Đặc điểm:
- **SQLite engine** (không phải Postgres/MySQL).
- **Edge-replicated** — primary 1 region, read replicas khắp POPs.
- **Serverless** — không quản instance, scale tự động.
- **HTTP API** — Worker truy cập qua binding.

### Giới hạn (limits) 2026

| Limit | Free | Paid ($5/tháng) |
|---|---|---|
| Database size | 500 MB | 10 GB / DB |
| Số DB / account | 10 | 50 |
| Row reads/ngày | 5M | 25M included, $0.001/M sau |
| Row writes/ngày | 100k | 50M included, $1/M sau |
| Query time | 30s | 30s |
| Result set max | 6 MB | 6 MB |

### Use case D1 phù hợp

- ✅ Catalog (read-heavy, write hiếm)
- ✅ User profile, session
- ✅ Analytics aggregation
- ✅ Multi-tenant SaaS (1 DB/tenant nhỏ)
- ✅ Edge-first app

### Use case D1 KHÔNG phù hợp

- ❌ Heavy write transactional (e-commerce checkout per second)
- ❌ Complex JOIN 5+ tables nhiều ms
- ❌ Stored procedure / function phức tạp
- ❌ Postgres-specific features (jsonb, arrays, full-text search)
- ❌ > 10 GB

→ Big workload: vẫn dùng Postgres origin + Hyperdrive (phần dưới).

### Tạo D1 + migration

```bash
# Tạo DB
wrangler d1 create acmeshop-db
# Output:
# [[d1_databases]]
# binding = "DB"
# database_name = "acmeshop-db"
# database_id = "xxxxxxxx-..."

# Add vào wrangler.toml
```

### Migrations — theo file (file-based)

```bash
# Tạo migration đầu
mkdir -p migrations
cat > migrations/0001_create_products.sql << 'EOF'
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE INDEX idx_products_name ON products(name);
EOF

# Apply local
wrangler d1 migrations apply acmeshop-db --local

# Apply remote
wrangler d1 migrations apply acmeshop-db --remote
```

### Query qua wrangler

```bash
wrangler d1 execute acmeshop-db --remote --command="SELECT * FROM products LIMIT 5"

wrangler d1 execute acmeshop-db --remote --file=./seed.sql
```

### Trong Worker — Prepared statements

```typescript
type Bindings = { DB: D1Database; };
const app = new Hono<{ Bindings: Bindings }>();

// List products
app.get('/api/products', async (c) => {
    const { results } = await c.env.DB
        .prepare('SELECT * FROM products ORDER BY id LIMIT ? OFFSET ?')
        .bind(20, 0)
        .all();
    return c.json(results);
});

// Get by id
app.get('/api/products/:id', async (c) => {
    const id = c.req.param('id');
    const product = await c.env.DB
        .prepare('SELECT * FROM products WHERE id = ?')
        .bind(id)
        .first();
    if (!product) return c.json({ error: 'Not found' }, 404);
    return c.json(product);
});

// Insert
app.post('/api/products', async (c) => {
    const body = await c.req.json();
    const result = await c.env.DB
        .prepare('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)')
        .bind(body.name, body.price, body.stock ?? 0)
        .run();
    return c.json({ id: result.meta.last_row_id }, 201);
});

// Batch (atomic)
const stmt = c.env.DB.prepare('UPDATE products SET stock = stock - 1 WHERE id = ?');
await c.env.DB.batch([
    stmt.bind(1),
    stmt.bind(2),
    stmt.bind(3),
]);
```

### Read replicas + Sessions API (2024+)

D1 hỗ trợ **read replicas** ở mọi POP. Để đảm bảo **read-your-write consistency**, dùng Sessions API:

```typescript
const session = c.env.DB.withSession('first-primary');

// Write
await session.prepare('INSERT INTO ...').bind(...).run();

// Read sau đó — đảm bảo thấy write (sticky session)
const result = await session.prepare('SELECT ...').first();

// Pass session bookmark cho client để dùng request sau
const bookmark = session.getBookmark();
```

### Mẹo tối ưu chi phí

- Cache `SELECT` qua KV (free read).
- Batch insert thay vì N lần INSERT.
- Index columns hay query (WHERE/ORDER BY).
- Tránh `SELECT *` — chỉ chọn columns cần.

---

## 3️⃣ Queues — message queue cho background work

🪞 **Ẩn dụ**: *Queues như **băng chuyền nhà máy** — producer đặt món lên, consumer nhặt xuống xử lý theo batch. Cho phép tách phần "nhận request nhanh" (Worker producer) khỏi "xử lý nặng" (consumer Worker chạy nền).*

### Khái niệm

| Khái niệm | Mô tả |
|---|---|
| **Queue** | Pipe message FIFO |
| **Producer** | Worker đẩy message vào queue |
| **Consumer** | Worker xử lý batch message |
| **Batch** | Group message gửi cho consumer 1 lần (1-100 messages) |
| **DLQ** (Dead Letter Queue) | Queue chứa message fail nhiều lần |
| **Retry** | Tự động retry với exponential backoff |

### Giá

- Free tier: không có (Queues yêu cầu Workers Paid).
- Paid: $0.40/M operations (write + read + delete count separately).
- Acme Shop 10M message/tháng → $4. Rẻ hơn SQS ($50).

### Tạo queue

```bash
wrangler queues create acmeshop-image-resize
```

### Cấu hình producer

```toml
# Producer Worker (e.g., upload handler)
[[queues.producers]]
binding = "RESIZE_QUEUE"
queue = "acmeshop-image-resize"
```

```typescript
// Producer code
app.post('/api/upload', async (c) => {
    const file = await c.req.formData();
    const key = `uploads/${Date.now()}.jpg`;
    await c.env.UPLOADS.put(key, file.get('image') as File);

    // Enqueue resize job
    await c.env.RESIZE_QUEUE.send({
        bucketKey: key,
        sizes: ['thumb', 'medium', 'large'],
        productId: c.req.query('product_id'),
    });

    return c.json({ ok: true, key });
});
```

### Cấu hình consumer

```toml
# Consumer Worker (riêng, hoặc cùng worker)
[[queues.consumers]]
queue = "acmeshop-image-resize"
max_batch_size = 10
max_batch_timeout = 30
max_retries = 3
dead_letter_queue = "acmeshop-image-resize-dlq"
```

```typescript
// Consumer code
export default {
    async fetch() { /* ... */ },

    async queue(batch: MessageBatch<ResizeJob>, env: Env) {
        for (const msg of batch.messages) {
            try {
                const { bucketKey, sizes } = msg.body;
                const obj = await env.UPLOADS.get(bucketKey);
                // Resize logic (Image API or external service)
                for (const size of sizes) {
                    await env.UPLOADS.put(`${bucketKey}.${size}`, resizedBytes);
                }
                msg.ack();  // Mark success
            } catch (err) {
                msg.retry({ delaySeconds: 60 });  // Retry 60s later
            }
        }
    },
};
```

### Các use case của Queues

- ✅ Image/video processing
- ✅ Send email (delay non-critical)
- ✅ Webhook fan-out
- ✅ Analytics batch ingestion
- ✅ Order processing (decouple checkout + fulfillment)
- ✅ Retry external API call

### Khi không dùng Queues

- ❌ Realtime (latency < 1s critical) → Workers + Durable Object
- ❌ Strict ordering across queue (FIFO chỉ within batch)
- ❌ Pub/Sub fan-out 1:N → dùng Workers + Service binding

---

## 4️⃣ Hyperdrive — Postgres connection pool từ Workers

🪞 **Ẩn dụ**: *Postgres origin như **quán phở nổi tiếng ở Hà Nội**. Workers ở 320+ POPs như **khách khắp thế giới**. Mỗi khách phải đặt món qua Hà Nội → quán đông quá, connection pool overflow. Hyperdrive là **gọi điện đặt món tập trung** — gom request từ khắp nơi qua 1 vài đường dây ổn định, đỡ tải cho quán.*

### Vấn đề Hyperdrive giải quyết

Workers chạy ở 320+ POPs. Mỗi Worker request → mở connection mới đến Postgres origin → Postgres connection limit (default 100) → overflow nhanh.

### Hyperdrive làm gì

- **Connection pooling** — Cloudflare giữ pool kết nối tới origin.
- **Query result cache** — cache `SELECT` ngắn (configurable).
- **Encrypted tunnel** — TLS tới origin, không expose Postgres public.

### Cài đặt

```bash
# Create Hyperdrive với connection string
wrangler hyperdrive create acmeshop-pg \
    --connection-string="postgres://user:pass@your-postgres.com:5432/acmeshop"

# Output:
# [[hyperdrive]]
# binding = "PG"
# id = "abc123..."
```

### Trong Worker

```typescript
import { Client } from 'pg';

app.get('/api/users', async (c) => {
    const client = new Client({
        connectionString: c.env.PG.connectionString,
    });
    await client.connect();

    const { rows } = await client.query('SELECT * FROM users LIMIT 100');

    await client.end();
    return c.json(rows);
});
```

→ `c.env.PG.connectionString` là URL tới Cloudflare Hyperdrive proxy, không phải origin trực tiếp.

### Khi nào Hyperdrive

- ✅ Có Postgres legacy không thể migrate D1
- ✅ Workload write-heavy cần Postgres ACID
- ✅ Cần feature Postgres (jsonb, full-text, PostGIS, ...)

### So sánh stack

| Stack | Khi dùng |
|---|---|
| Workers + D1 | Greenfield, SQLite đủ |
| Workers + Hyperdrive + RDS Postgres | Postgres feature cần |
| Workers + KV (only) | Read-heavy cache, simple key-value |
| Workers + R2 only | File serving, no DB |

---

## 🛠️ Hands-on — Acme Shop image upload + catalog + resize queue

### Mục tiêu

End-to-end pipeline:
1. User upload ảnh sản phẩm qua `POST /api/upload`.
2. Worker lưu ảnh gốc vào R2.
3. Worker insert metadata vào D1.
4. Worker enqueue resize job.
5. Consumer Worker resize ảnh thành thumb/medium/large.
6. `GET /api/products/:id` trả product info + URL ảnh các size.

### Bước 1 — Chuẩn bị project

```bash
mkdir acmeshop-fullstack && cd acmeshop-fullstack
npm create hono@latest -- . --template cloudflare-workers
npm install
```

### Bước 2 — Tạo R2 + D1 + Queue

```bash
# R2
wrangler r2 bucket create acmeshop-uploads

# D1
wrangler d1 create acmeshop-db
# Lưu database_id

# Queue (cần Workers Paid)
wrangler queues create acmeshop-image-resize
wrangler queues create acmeshop-image-resize-dlq
```

### Bước 3 — wrangler.toml

```toml
name = "acmeshop-fullstack"
main = "src/index.ts"
compatibility_date = "2026-05-01"

[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "acmeshop-uploads"

[[d1_databases]]
binding = "DB"
database_name = "acmeshop-db"
database_id = "<your-d1-id>"

[[queues.producers]]
binding = "RESIZE_QUEUE"
queue = "acmeshop-image-resize"

[[queues.consumers]]
queue = "acmeshop-image-resize"
max_batch_size = 5
max_batch_timeout = 30
max_retries = 3
dead_letter_queue = "acmeshop-image-resize-dlq"
```

### Bước 4 — Migration

```bash
mkdir -p migrations

cat > migrations/0001_init.sql << 'EOF'
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image_key TEXT,
    created_at INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE product_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    size TEXT NOT NULL,  -- 'original', 'thumb', 'medium', 'large'
    bucket_key TEXT NOT NULL,
    width INTEGER,
    height INTEGER,
    created_at INTEGER NOT NULL DEFAULT (unixepoch()),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX idx_images_product ON product_images(product_id);

INSERT INTO products (name, price) VALUES
    ('iPhone 15', 999),
    ('MacBook Pro', 1999);
EOF

wrangler d1 migrations apply acmeshop-db --remote
```

### Bước 5 — Worker code

```typescript
// src/index.ts
import { Hono } from 'hono';

type Bindings = {
    UPLOADS: R2Bucket;
    DB: D1Database;
    RESIZE_QUEUE: Queue<ResizeJob>;
};

type ResizeJob = {
    productId: number;
    bucketKey: string;
    sizes: ('thumb' | 'medium' | 'large')[];
};

const app = new Hono<{ Bindings: Bindings }>();

// List products with image URLs
app.get('/api/products', async (c) => {
    const products = await c.env.DB
        .prepare(`
            SELECT p.id, p.name, p.price,
                   GROUP_CONCAT(pi.size || ':' || pi.bucket_key) AS images
            FROM products p
            LEFT JOIN product_images pi ON pi.product_id = p.id
            GROUP BY p.id
        `)
        .all();
    return c.json(products.results);
});

app.get('/api/products/:id', async (c) => {
    const id = c.req.param('id');
    const product = await c.env.DB
        .prepare('SELECT * FROM products WHERE id = ?')
        .bind(id)
        .first();
    if (!product) return c.json({ error: 'Not found' }, 404);

    const images = await c.env.DB
        .prepare('SELECT * FROM product_images WHERE product_id = ?')
        .bind(id)
        .all();

    return c.json({ ...product, images: images.results });
});

// Upload image for product
app.post('/api/products/:id/upload', async (c) => {
    const productId = Number(c.req.param('id'));
    const formData = await c.req.formData();
    const file = formData.get('image') as File | null;

    if (!file) return c.json({ error: 'No image' }, 400);

    const bucketKey = `products/${productId}/${Date.now()}.jpg`;
    await c.env.UPLOADS.put(bucketKey, await file.arrayBuffer(), {
        httpMetadata: { contentType: file.type },
    });

    // Insert original
    await c.env.DB
        .prepare('INSERT INTO product_images (product_id, size, bucket_key) VALUES (?, ?, ?)')
        .bind(productId, 'original', bucketKey)
        .run();

    // Enqueue resize
    await c.env.RESIZE_QUEUE.send({
        productId,
        bucketKey,
        sizes: ['thumb', 'medium', 'large'],
    });

    return c.json({ ok: true, bucketKey, status: 'resize queued' });
});

// Serve image from R2
app.get('/img/*', async (c) => {
    const key = c.req.path.replace(/^\/img\//, '');
    const obj = await c.env.UPLOADS.get(key);
    if (!obj) return c.notFound();
    return new Response(obj.body, {
        headers: {
            'content-type': obj.httpMetadata?.contentType ?? 'image/jpeg',
            'cache-control': 'public, max-age=31536000',
        },
    });
});

// Queue consumer
const queueHandler = async (batch: MessageBatch<ResizeJob>, env: Bindings) => {
    for (const msg of batch.messages) {
        try {
            const { productId, bucketKey, sizes } = msg.body;
            const obj = await env.UPLOADS.get(bucketKey);
            if (!obj) {
                msg.ack();
                continue;
            }

            // Simulate resize — in real app use Cloudflare Images or external lib
            for (const size of sizes) {
                const resizedKey = `${bucketKey}.${size}`;
                // Pseudo: const resized = await resizeImage(obj.body, size);
                const resized = await obj.arrayBuffer();  // mock — same data
                await env.UPLOADS.put(resizedKey, resized);

                await env.DB
                    .prepare('INSERT INTO product_images (product_id, size, bucket_key) VALUES (?, ?, ?)')
                    .bind(productId, size, resizedKey)
                    .run();
            }

            msg.ack();
        } catch (err) {
            console.error('Resize failed:', err);
            msg.retry({ delaySeconds: 30 });
        }
    }
};

export default {
    fetch: app.fetch,
    queue: queueHandler,
};
```

### Bước 6 — Deploy + test

```bash
wrangler deploy

URL="https://acmeshop-fullstack.<sub>.workers.dev"

# Upload
curl -X POST -F "image=@./test.jpg" $URL/api/products/1/upload
# {"ok":true,"bucketKey":"products/1/1716...jpg","status":"resize queued"}

# Đợi 30s cho queue process
sleep 35

# Check
curl $URL/api/products/1
# {
#   "id": 1, "name": "iPhone 15", "price": 999,
#   "images": [
#     { "size": "original", "bucket_key": "products/1/...jpg" },
#     { "size": "thumb", "bucket_key": "products/1/....thumb" },
#     ...
#   ]
# }

# Serve image
curl $URL/img/products/1/1716....jpg.thumb -o thumb.jpg
```

### Bước 7 — Giám sát queue

```bash
# Tail Worker logs
wrangler tail acmeshop-fullstack

# Trong Dashboard:
# Queues → acmeshop-image-resize → Metrics
# - Messages in queue
# - Consumer concurrency
# - DLQ count
```

→ **Kết quả**: Pipeline upload → R2 → metadata D1 → queue resize → background process. Stack hoàn toàn Cloudflare, zero egress, ~$5-10/tháng cho Acme Shop scale.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: R2 public access mở hết bucket

**Triệu chứng**: Bật Public access → 1 attacker scan list bucket → tải hết 5TB ảnh → bandwidth chính bạn vẫn $0 (R2 zero egress) nhưng compute / processing tăng.

**Nguyên nhân**: Public bucket cho phép unlisted access nếu biết key.

**Cách tránh**:
- Public bucket chỉ cho dev/test.
- Production: Worker làm proxy + WAF rate limit.
- Hoặc presigned URL với TTL ngắn.

### ❌ Cạm bẫy: D1 schema migration nhầm — drop production

**Triệu chứng**: Chạy migration `DROP TABLE products` ở production thay vì local.

**Nguyên nhân**: Quên `--local` flag.

**Cách tránh**:
- Default migration luôn `--local` trước.
- CI/CD áp dụng remote chỉ sau review.
- Backup D1 thường xuyên: `wrangler d1 export acmeshop-db --output=backup.sql`.

### ❌ Cạm bẫy: D1 SELECT \* khi > 6 MB

**Triệu chứng**: Query 10k rows trả result quá 6MB → error 7500.

**Nguyên nhân**: D1 limit response 6MB.

**Cách tránh**:
- Pagination `LIMIT ... OFFSET ...`.
- Chỉ select columns cần.

### ❌ Cạm bẫy: Queue consumer infinite retry

**Triệu chứng**: Bug consumer → retry mãi → quota cạn → cost tăng.

**Nguyên nhân**: Không set `max_retries` hoặc DLQ.

**Cách tránh**:
- Luôn set `max_retries = 3` + `dead_letter_queue`.
- Monitor DLQ size — alert khi > N.

### ❌ Cạm bẫy: Quên ack/retry message

**Triệu chứng**: Message đứng yên trong queue, không xử lý lại.

**Nguyên nhân**: Code consumer throw exception nhưng không gọi `msg.retry()` rõ ràng → Cloudflare đợi visibility timeout → retry. Confusing.

**Cách tránh**:
- Wrap try/catch, gọi `msg.ack()` khi thành công, `msg.retry()` khi fail.

### ❌ Cạm bẫy: Hyperdrive cache SELECT có user-specific data

**Triệu chứng**: User A query `SELECT * FROM orders WHERE user_id = 1` → cached → user B query cùng SQL string với param khác → có thể trả cache của A.

**Nguyên nhân**: Hyperdrive cache theo SQL + params. Nếu params không khác → cache leak.

**Cách tránh**:
- Disable cache cho query user-specific.
- Hoặc dùng SQL khác nhau per user.

### ❌ Cạm bẫy: R2 + S3 SDK timeout config

**Triệu chứng**: AWS SDK kết nối R2 timeout 30s default → Worker bị kill 30s limit.

**Nguyên nhân**: SDK retry 3 lần × 10s.

**Cách tránh**:
- Cấu hình SDK timeout 5-10s.
- Hoặc dùng R2 binding (`env.UPLOADS`) thay vì AWS SDK — nhanh + tích hợp.

### ❌ Cạm bẫy: D1 transaction nhầm — không atomic

**Triệu chứng**: Insert order + decrease stock → 2 lệnh riêng → 1 fail còn 1 thành công → data inconsistent.

**Nguyên nhân**: D1 batch là pseudo-transaction (1 connection, sequential), nhưng không có ROLLBACK truyền thống.

**Cách tránh**:
- Dùng `db.batch([stmt1, stmt2])` — nếu 1 fail, toàn batch rollback.
- Hoặc dùng Durable Object cho operation cần ACID phức tạp.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Vì sao R2 zero egress nhưng S3 thì không?

<details>
<summary>💡 Đáp án</summary>

Cloudflare là Tier-1 ISP với backbone toàn cầu + thành viên Bandwidth Alliance. AWS phải trả tiền egress cho ISP peering nên phải tính lại cho khách. R2 cũng là chiến lược cạnh tranh S3 — Cloudflare chấp nhận lỗ egress để chiếm thị phần.
</details>

**Q2.** Khi nào D1, khi nào Hyperdrive + Postgres?

<details>
<summary>💡 Đáp án</summary>

- **D1**: Greenfield, SQLite đủ, < 10GB, read-heavy, không cần feature Postgres riêng.
- **Hyperdrive + Postgres**: Legacy Postgres, cần jsonb/full-text/PostGIS, transactional heavy, > 10GB.
</details>

**Q3.** Queue producer/consumer tại sao tách thành 2 Worker hoặc 1 Worker với 2 handler?

<details>
<summary>💡 Đáp án</summary>

- **Tách**: Independent scale, deploy riêng, monitor riêng.
- **Cùng Worker**: Đơn giản, share binding, code chung. Acme Shop scale nhỏ thì 1 Worker đủ.
</details>

**Q4.** R2 vs S3 cho workload 1TB storage + 50TB egress/tháng — chọn cái nào? Tính cost.

<details>
<summary>💡 Đáp án</summary>

- R2: 1024 × $0.015 = $15.36 + ops + **egress $0** ≈ $20.
- S3: 1024 × $0.023 = $23.55 + 50,000 × $0.09 = $4,500 ≈ $4,525.

→ R2 thắng $4,505/tháng (99.5%).
</details>

**Q5.** D1 read replica đảm bảo read-your-write thế nào?

<details>
<summary>💡 Đáp án</summary>

Dùng **Sessions API** (`db.withSession('first-primary')`). Session sticky 1 replica đã thấy write. Bookmark có thể truyền qua client (header/cookie) cho request sau dùng cùng session → thấy write từ request trước.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh / cách |
|---|---|
| Tạo R2 bucket | `wrangler r2 bucket create <name>` |
| Upload R2 | `wrangler r2 object put <bucket>/<key> --file=...` |
| Tạo D1 | `wrangler d1 create <name>` |
| Apply migration | `wrangler d1 migrations apply <name> --remote` |
| Query D1 | `wrangler d1 execute <name> --command="SELECT 1"` |
| Backup D1 | `wrangler d1 export <name> --output=backup.sql` |
| Tạo Queue | `wrangler queues create <name>` |
| Tạo Hyperdrive | `wrangler hyperdrive create <name> --connection-string=...` |
| R2 binding code | `env.UPLOADS.put(key, data)` |
| D1 prepared | `env.DB.prepare(sql).bind(...).all()` |
| Queue send | `env.MY_QUEUE.send(payload)` |
| Multipart R2 | `env.UPLOADS.createMultipartUpload(key)` |
| Sessions API | `env.DB.withSession('first-primary')` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **R2** | Object storage edge | Object storage của Cloudflare, S3-compatible, zero egress |
| **D1** | SQLite phân tán | Managed SQLite edge-replicated (primary 1 region, read replica khắp POP) |
| **Queues** | Hàng đợi message | Message queue của Cloudflare cho background work |
| **Hyperdrive** | Pool kết nối Postgres | Connection pool + cache cho Postgres origin từ Workers |
| **Egress** | Dữ liệu ra | Data ra khỏi cloud (download bandwidth) — chỗ S3 tính phí, R2 thì miễn phí |
| **Class A op** | Thao tác ghi/liệt kê | Operation kiểu PUT/POST/COPY/LIST trên R2 |
| **Class B op** | Thao tác đọc | Operation kiểu GET/HEAD trên R2 |
| **Presigned URL** | URL ký sẵn | URL ngắn hạn cho client upload/download trực tiếp R2 |
| **Multipart upload** | Upload nhiều phần | Upload file lớn theo chunk, hỗ trợ resumable |
| **DLQ** | Hàng đợi chết | Dead Letter Queue — chứa message fail quá số lần retry |
| **Batch** | Lô message | Nhóm message giao cho consumer xử lý 1 lần (1–100 message) |
| **Sessions API** | API phiên D1 | API của D1 đảm bảo read-your-write consistency trên read replica |
| **Bookmark** | Dấu mốc đọc | Token mô tả "đã thấy write này" để Sessions API dùng cho request sau |
| **Hyperdrive cache** | Cache truy vấn | Cache câu SELECT ngay tại Cloudflare proxy |
| **Bandwidth Alliance** | Liên minh băng thông | Liên minh nhà mạng giảm/miễn phí egress khi truyền giữa các thành viên |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloudflare Workers + Pages — Edge compute & static + dynamic](02_workers-and-pages.md)
- ➡️ **Bài tiếp theo:** [Cloudflare Security — WAF, Zero Trust, DDoS, Bot, Turnstile](04_security-zero-trust-and-waf.md)
- ↑ **Về cụm:** [Cloudflare](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [S3 chuyên sâu + Nền tảng IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — đối chiếu R2 với object storage gốc của AWS.
- ☁️ [RDS + DynamoDB — Managed databases](../../../aws/lessons/01_basic/03_rds-and-dynamodb.md) — so sánh D1/Hyperdrive với managed DB của AWS.
- ☁️ [GCP Cloud Storage + IAM](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md) — object storage tương đương bên GCP.
- ☁️ [GCP Cloud SQL + Firestore](../../../gcp/lessons/01_basic/03_cloud-sql-and-firestore.md) — managed SQL + NoSQL bên GCP.

### 🌐 Tài nguyên tham khảo khác (2026)
- 📖 [R2 docs](https://developers.cloudflare.com/r2/)
- 📖 [D1 docs](https://developers.cloudflare.com/d1/)
- 📖 [Queues docs](https://developers.cloudflare.com/queues/)
- 📖 [Hyperdrive docs](https://developers.cloudflare.com/hyperdrive/)
- 📖 [R2 vs S3 cost calculator](https://r2-calculator.cloudflare.com/)
- 📖 [D1 Sessions API](https://developers.cloudflare.com/d1/best-practices/read-replication/)
- 📖 [R2 S3 API compatibility](https://developers.cloudflare.com/r2/api/s3/api/)
- 📖 [Bandwidth Alliance](https://www.cloudflare.com/bandwidth-alliance/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 03 cluster Cloudflare basic. R2 S3-compatible + zero egress + cost comparison + presigned URL + multipart + D1 SQLite edge replica + migrations + Sessions API + Queues producer/consumer + DLQ + Hyperdrive Postgres pool + hands-on Acme Shop upload pipeline (R2 + D1 + Queue) + 8 pitfalls. Pattern theo AWS lesson 02-03.
- **v1.1.0 (01/06/2026)** — Chuẩn hoá QA: đổi field metadata "Prerequisites" → "Yêu cầu trước"; sửa typo "Triệu chextual" → "Triệu chứng" ở pitfall D1 SELECT 6MB; Glossary chuyển sang 3 cột "Thuật ngữ | Tiếng Việt | Giải thích"; đồng bộ nav (⬅️/➡️/↑) với link-text là tiêu đề thật của bài đích và 3 sub-heading chuẩn (🧭 Định hướng / 🧩 Chủ đề liên quan / 🌐 Tài nguyên).
- **v1.1.1 (10/06/2026)** — Làm rõ tuyên bố "R2 không control region (Q1 2026)" ở bảng "Khi R2 KHÔNG thắng": gắn mốc *tính đến Q1 2026* và ghi chú khả năng control region (Jurisdictional Restrictions/Location Hints) là dự kiến/đã ra tuỳ thời điểm, nên kiểm tra docs hiện hành.
- **v1.1.2 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
