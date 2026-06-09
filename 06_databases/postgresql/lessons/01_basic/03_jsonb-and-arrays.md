# 🎓 JSONB, Arrays & Full-text — Postgres killer features

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [Indexes & Performance](02_indexes-and-performance.md)

> 🎯 *Master 3 feature làm Postgres khác biệt: **JSONB** (binary JSON với index GIN), **arrays** native, **full-text search** (tsvector). Plus glance **pgvector** (AI embedding). Sau bài này hiểu tại sao 2026 Postgres thay được nhiều specialized DB.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **JSON** vs **JSONB** + khi nào dùng
- [ ] Query JSONB với **`->`**, **`->>`**, **`@>`**, **`?`**, **path**
- [ ] Index JSONB với **GIN** + **expression index**
- [ ] Dùng **arrays** native (`int[]`, `text[]`)
- [ ] **Full-text search** với `tsvector` + `tsquery` + GIN
- [ ] Hiểu **pgvector** intro cho AI embedding
- [ ] So sánh Postgres JSONB vs MongoDB document
- [ ] Khi nào tách table vs khi nào JSONB

---

## Tình huống — Bạn cần lưu config động per user

Bạn có table `users` với name/email/age. Giờ cần lưu **user preferences**:
- Theme (light/dark/auto)
- Language (en/vi/...)
- Notifications (email, push, sms — checkbox)
- Custom fields user định nghĩa (vd ngày sinh thú cưng cho user yêu mèo)

Bạn thử **add columns**:
```sql
ALTER TABLE users ADD COLUMN theme TEXT;
ALTER TABLE users ADD COLUMN language TEXT;
ALTER TABLE users ADD COLUMN notify_email BOOLEAN;
ALTER TABLE users ADD COLUMN notify_push BOOLEAN;
-- ...10 columns
-- Mỗi feature mới = ALTER TABLE production = lock
```

→ **Schema rigid**. Mỗi config mới = migration. Many sparse NULL columns.

Senior:
> *"Đây là use case của **JSONB**. Lưu config động trong 1 column `preferences JSONB`. Schema flexible mà vẫn query + index được. Khác MongoDB ở chỗ vẫn ACID + JOIN với SQL normal."*

→ Bài này dạy JSONB + arrays + full-text.

---

## 1️⃣ JSON vs JSONB

Postgres có **2 kiểu JSON** — `json` (lưu text raw) và `jsonb` (binary parsed). Khác biệt cốt lõi: speed + index support. 2026 default là `jsonb`, `json` gần như deprecated trừ niche case:

| Type | Storage | Query speed | Index | Preserve order/whitespace |
|---|---|---|---|---|
| **`json`** | Text (parse mỗi access) | Slow | Limited | ✅ |
| **`jsonb`** | Binary parsed | **Fast** | ✅ **GIN** | ❌ (re-formatted) |

→ **2026 default: `jsonb`**. `json` chỉ dùng khi cần preserve format exact (rare).

### Create + insert

Tạo cột JSONB rất đơn giản — chỉ thêm type `JSONB` ở `CREATE TABLE`. Có thể đặt `DEFAULT '{}'::jsonb` để row mới không bao giờ NULL. INSERT data dạng string JSON + cast `::jsonb`:

```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  preferences JSONB DEFAULT '{}'::jsonb
);

INSERT INTO users (name, preferences) VALUES
('Nguyen Van A', '{
  "theme": "dark",
  "language": "vi",
  "notifications": {
    "email": true,
    "push": false,
    "sms": true
  },
  "tags": ["dev", "vip"],
  "pet_birthday": "2020-05-15"
}'::jsonb);
```

### `'{}'::jsonb` — Cast

Cast `::jsonb` chuyển 1 string thành JSONB. Postgres support đầy đủ **6 dạng JSON** (object, array, string, number, bool, null) — quan trọng cho query nâng cao và default values:

```sql
'{"key": "val"}'::jsonb
'[1,2,3]'::jsonb
'"plain string"'::jsonb       -- JSON string (with quotes)
'5'::jsonb                       -- JSON number
'true'::jsonb                    -- JSON bool
'null'::jsonb                    -- JSON null
```

---

## 2️⃣ JSONB query operators

### `->` returns JSONB, `->>` returns TEXT

2 operator phân biệt **return type**: `->` trả JSONB (vẫn JSON object), `->>` trả TEXT plain. Chain `->` để navigate vào nested object, dùng `->>` ở cuối khi cần extract giá trị thực:

```sql
SELECT preferences -> 'theme' FROM users;        -- "dark" (jsonb, with quotes)
SELECT preferences ->> 'theme' FROM users;        -- dark (text, no quotes)
SELECT preferences -> 'notifications' -> 'email' FROM users;    -- true (jsonb)
SELECT preferences ->> 'notifications' FROM users;
   -- {"email":true,"push":false,"sms":true} (text dạng JSON)
```

→ **Quy tắc**: chain `->` cho navigate, **`->>` ở cuối** để extract value.

### Path access — `#>` + `#>>`

Khi cần navigate **nhiều cấp** một lúc, dùng path operator (`#>` JSONB, `#>>` TEXT) với array path. Cú pháp gọn hơn chain `->` nhiều lần — đặc biệt cho object lồng sâu:

```sql
SELECT preferences #> '{notifications,email}' FROM users;    -- true (jsonb)
SELECT preferences #>> '{notifications,email}' FROM users;    -- t (text)
SELECT preferences #>> '{tags,0}' FROM users;                  -- dev (first array)
```

### `?` — Key exists

```sql
SELECT * FROM users WHERE preferences ? 'theme';                    -- has key
SELECT * FROM users WHERE preferences ?| ARRAY['theme','lang'];     -- any of
SELECT * FROM users WHERE preferences ?& ARRAY['theme','lang'];     -- all of
```

### `@>` — Contains (subset)

```sql
-- "Tìm user có theme=dark"
SELECT * FROM users
WHERE preferences @> '{"theme": "dark"}'::jsonb;

-- "Tìm user vip"
SELECT * FROM users
WHERE preferences @> '{"tags": ["vip"]}'::jsonb;

-- Combine
SELECT * FROM users
WHERE preferences @> '{"theme": "dark", "language": "vi"}'::jsonb;
```

→ `@>` **dùng GIN index được** (fast). 90% query JSONB dùng `@>`.

### `<@` — Contained (reverse)

```sql
SELECT * FROM users
WHERE '{"theme": "dark"}'::jsonb <@ preferences;
-- Tương đương `preferences @> ...`
```

### `||` — Merge

```sql
UPDATE users
SET preferences = preferences || '{"theme": "light"}'::jsonb
WHERE id = 1;

-- Merge nested (chỉ top-level — nested override toàn bộ key)
```

### Delete keys

```sql
UPDATE users
SET preferences = preferences - 'theme'              -- Remove key 'theme'
WHERE id = 1;

UPDATE users
SET preferences = preferences - ARRAY['theme', 'language']   -- Multiple
WHERE id = 1;

UPDATE users
SET preferences = preferences #- '{notifications,sms}'   -- Path
WHERE id = 1;
```

### Update specific path — `jsonb_set`

```sql
UPDATE users
SET preferences = jsonb_set(preferences, '{theme}', '"light"')
WHERE id = 1;

-- Nested
UPDATE users
SET preferences = jsonb_set(preferences, '{notifications,sms}', 'false')
WHERE id = 1;

-- Create if missing
UPDATE users
SET preferences = jsonb_set(preferences, '{newKey}', '"value"', true)   -- 4th = create_if_missing
WHERE id = 1;
```

---

## 3️⃣ Index JSONB với GIN

### GIN index default

```sql
CREATE INDEX idx_users_prefs ON users USING GIN (preferences);
```

→ Support `@>`, `?`, `?|`, `?&`. **Slow build** + **big size**, nhưng query fast.

### GIN với `jsonb_path_ops` — Smaller + faster cho `@>`

```sql
CREATE INDEX idx_users_prefs ON users USING GIN (preferences jsonb_path_ops);
```

→ **Recommended** nếu chỉ dùng `@>` (90% case). 3x smaller, 2x faster lookup. **Không support `?`**.

### Expression index — Index value cụ thể

```sql
-- Index theme value
CREATE INDEX idx_users_theme ON users((preferences ->> 'theme'));
SELECT * FROM users WHERE preferences ->> 'theme' = 'dark';    -- Fast (B-tree)

-- Index nested
CREATE INDEX idx_users_country ON users((preferences ->> 'country'));
```

→ B-tree expression index nhanh hơn GIN cho **exact value** filter của 1 key cụ thể. GIN tốt cho complex `@>`.

### Strategy

| Query pattern | Index |
|---|---|
| Filter 1 key cụ thể (`->>= X`) | **Expression B-tree** |
| Multiple key search, partial match (`@>`) | **GIN jsonb_path_ops** |
| Key existence (`?`) | **GIN** (full) |

---

## 4️⃣ Arrays native

Postgres support array native — không cần JSONB cho list đơn giản.

### Create + insert

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title TEXT,
  tags TEXT[],
  view_counts INTEGER[]
);

INSERT INTO posts (title, tags, view_counts) VALUES
('Post 1', ARRAY['dev', 'react', 'js'], ARRAY[100, 200, 350]),
('Post 2', '{"python","fastapi","postgres"}', '{50,80,120}');

-- 2 cách: ARRAY[...] hoặc '{...}'
```

### Access + slice

```sql
SELECT tags[1] FROM posts;                      -- 'dev' (1-indexed!)
SELECT tags[2:3] FROM posts;                     -- {'react','js'}
SELECT array_length(tags, 1) FROM posts;         -- 3
SELECT array_position(tags, 'react') FROM posts;  -- 2
```

→ ⚠️ Postgres array **1-indexed** (khác Python/JS 0-indexed).

### Query

```sql
-- Contains element
SELECT * FROM posts WHERE 'react' = ANY(tags);
SELECT * FROM posts WHERE tags @> ARRAY['react'];         -- Same

-- Contains multiple
SELECT * FROM posts WHERE tags @> ARRAY['react', 'js'];

-- Has any of
SELECT * FROM posts WHERE tags && ARRAY['react', 'vue'];   -- overlap

-- Doesn't contain
SELECT * FROM posts WHERE NOT (tags @> ARRAY['old']);
```

### Manipulate

```sql
-- Append
UPDATE posts SET tags = array_append(tags, 'new');
UPDATE posts SET tags = tags || 'new';                     -- same
UPDATE posts SET tags = tags || ARRAY['a', 'b'];           -- multiple

-- Prepend
UPDATE posts SET tags = array_prepend('first', tags);

-- Remove
UPDATE posts SET tags = array_remove(tags, 'old');

-- Update at position
UPDATE posts SET tags[2] = 'updated' WHERE id = 1;
```

### Unnest — Array → rows

```sql
SELECT id, title, unnest(tags) AS tag FROM posts;
-- post1, Post 1, dev
-- post1, Post 1, react
-- post1, Post 1, js
-- post2, ...
```

→ Useful cho aggregation:

```sql
SELECT tag, COUNT(*) FROM posts, unnest(tags) AS tag
GROUP BY tag ORDER BY count DESC;
```

### Index — GIN

```sql
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);
SELECT * FROM posts WHERE tags @> ARRAY['react'];    -- Fast
```

### Array vs JSONB array — Khi nào dùng?

| Use case | Choose |
|---|---|
| List **homogeneous primitive** (tags, IDs) | **Array** (`text[]`, `int[]`) |
| List **heterogeneous objects** | **JSONB** array |
| Need to **query nested** | JSONB |
| Cross-database compatibility | JSONB (more universal) |

---

## 5️⃣ Full-text search — `tsvector` + `tsquery`

### Vấn đề `LIKE '%word%'`

```sql
SELECT * FROM articles WHERE content LIKE '%postgresql%';
-- Slow on big table (full scan)
-- Không match "Postgres" hay "postgres," ranking, ...
```

### Solution — Postgres FTS native

```sql
-- 1. Tạo column tsvector (parsed + stemmed)
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- 2. Populate
UPDATE articles
SET search_vector = to_tsvector('english', title || ' ' || content);

-- 3. Index GIN
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- 4. Query với tsquery
SELECT title, ts_rank(search_vector, query) AS rank
FROM articles, plainto_tsquery('english', 'postgres performance') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 10;
```

### Auto-update tsvector — Generated column (Postgres 12+)

```sql
ALTER TABLE articles
DROP COLUMN search_vector;

ALTER TABLE articles
ADD COLUMN search_vector tsvector
GENERATED ALWAYS AS (
  to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))
) STORED;

-- Auto-rebuild khi title/content đổi
```

### `tsquery` syntax

```sql
plainto_tsquery('english', 'postgres performance')
-- → 'postgr' & 'perform'

to_tsquery('english', 'postgres & (perform | speed)')
-- → 'postgr' & ('perform' | 'speed')

websearch_to_tsquery('english', 'postgres "exact phrase" -slow')
-- → Google-style: AND, exact phrase, exclude with -
```

### Highlight matches

```sql
SELECT ts_headline('english', content, query, 'StartSel=<b>, StopSel=</b>')
FROM articles, plainto_tsquery('english', 'postgres') query
WHERE search_vector @@ query;
-- Output: "...about <b>Postgres</b> performance..."
```

### Multi-language

```sql
to_tsvector('english', 'I love Postgres')        -- English stemming
to_tsvector('simple', 'không có stemming')        -- No language processing
to_tsvector('vietnamese', 'tôi yêu Postgres')    -- Custom (cần extension)
```

→ Postgres không có Vietnamese dictionary built-in. Workaround: `unaccent` extension + `simple` dictionary.

### When FTS đủ vs khi nào Elasticsearch?

| Use case | Choose |
|---|---|
| < 10M rows, simple search | **Postgres FTS** |
| Complex faceting, fuzzy, multi-language | Elasticsearch |
| Real-time + analytics | Elasticsearch |
| Want 1 less infra component | Postgres FTS (worth tradeoff) |

→ **2026 trend**: Postgres FTS cover 70% search cases. Save running Elasticsearch separate.

---

## 6️⃣ pgvector — AI embedding (intro)

**Vector embeddings** = numeric representation cho text/image. Similarity search = "tìm tài liệu giống ý nghĩa".

### Setup

```sql
CREATE EXTENSION vector;

CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536)        -- OpenAI text-embedding-3-small = 1536 dim
);
```

### Insert (sau khi tạo embedding qua API)

```sql
INSERT INTO documents (content, embedding) VALUES
('Postgres is great', '[0.1, 0.2, ..., 0.5]'),
('FastAPI tutorial', '[0.3, 0.1, ..., 0.4]');
```

### Search nearest

```sql
-- Cosine similarity (most common cho text)
SELECT content, 1 - (embedding <=> '[query embedding]') AS similarity
FROM documents
ORDER BY embedding <=> '[query embedding]'
LIMIT 5;
```

### Index HNSW (fast approximate)

```sql
CREATE INDEX idx_docs_embedding
  ON documents USING hnsw (embedding vector_cosine_ops);
```

→ **2026 hot**: Postgres + pgvector thay Pinecone/Weaviate cho 80% RAG (Retrieval Augmented Generation). 1 DB cho cả structured + vector. Saves infra.

→ pgvector chi tiết là cluster riêng (advanced). Beginner: biết tồn tại.

---

## 7️⃣ Lưu user preferences kiểu modern

```sql
-- Schema
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  preferences JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_users_prefs_gin ON users USING GIN (preferences jsonb_path_ops);
CREATE INDEX idx_users_theme ON users((preferences ->> 'theme'));

-- Insert
INSERT INTO users (email, name, preferences) VALUES
('nguyenvana@ex.com', 'Nguyen Van A', '{
  "theme": "dark",
  "language": "vi",
  "notifications": {"email": true, "push": false},
  "tags": ["vip", "early-access"]
}');

-- Queries
-- 1. User theme dark
SELECT * FROM users WHERE preferences ->> 'theme' = 'dark';

-- 2. User có push notify
SELECT * FROM users WHERE preferences @> '{"notifications": {"push": true}}';

-- 3. User VIP
SELECT * FROM users WHERE preferences @> '{"tags": ["vip"]}';

-- 4. Update theme
UPDATE users
SET preferences = jsonb_set(preferences, '{theme}', '"light"')
WHERE id = 1;

-- 5. Add tag
UPDATE users
SET preferences = jsonb_set(
  preferences, '{tags}',
  preferences -> 'tags' || '"new-tag"'
)
WHERE id = 1;
```

→ Schema flexible (preferences đổi không migrate), index hỗ trợ query fast. **Best of both worlds**.

---

## 8️⃣ JSONB vs MongoDB — Postgres replaces?

| Aspect | Postgres JSONB | MongoDB |
|---|---|---|
| ACID transactions | ✅ Full | Partial (single doc default) |
| Joins | ✅ SQL | $lookup (slower) |
| Schema | Optional | Schema-less |
| Index JSON | ✅ GIN | ✅ |
| Query performance | ✅ Excellent với GIN | Excellent native |
| Scale horizontal | Manual (Citus) | Native (sharding) |
| Ecosystem (ORM, tooling) | Mature (SQL world) | Native to JS world |
| Operations | DBA traditional | DevOps simpler |

→ **2026 reality**: Postgres JSONB **đủ** cho 80% MongoDB use case + **plus structured + JOIN + transactions**. Choose Mongo when: schema vô cùng đa dạng, native horizontal scale critical, team Node-only.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`->` vs `->>`** — `->` returns JSONB, `->>` returns TEXT. Compare text: `preferences ->> 'theme' = 'dark'`. Compare JSONB: `preferences -> 'theme' = '"dark"'::jsonb`.
2. **Index `jsonb` mà query `->>`** → không dùng index GIN. GIN cho `@>`/`?`. B-tree expression cho `->>= X`.
3. **Mutate JSONB** — JSONB **immutable**. `jsonb_set` returns new value, phải `UPDATE ... SET col = jsonb_set(...)`.
4. **Array 1-indexed** → `tags[0]` returns NULL (không phải first). Always `tags[1]`.
5. **FTS quên update tsvector** sau update content → search miss. Dùng generated column (Postgres 12+) cho auto-rebuild.

---

## 🧠 Tự kiểm tra (Self-check)

1. JSON vs JSONB — chọn cái nào 2026, tại sao?
2. `->` vs `->>` — khác sao? Cho ví dụ.
3. Best index cho query JSONB `@>`?
4. Postgres array vs JSONB array — khi nào dùng cái nào?
5. Postgres FTS thay Elasticsearch khi nào?

<details>
<summary>Gợi ý đáp án</summary>

1. **JSONB** — binary format, parsed once, faster query, support GIN index. **JSON** — text, parsed mỗi access, slower, preserve order/whitespace. Modern 2026: dùng **JSONB** trừ khi cần preserve exact format (audit log original).

2. **`->`** returns JSONB. **`->>`** returns TEXT. VD: `preferences -> 'theme'` = `"dark"` (JSONB with quotes). `preferences ->> 'theme'` = `dark` (plain text). Use `->>` khi compare với TEXT: `preferences ->> 'theme' = 'dark'`.

3. **GIN với `jsonb_path_ops`**:
   ```sql
   CREATE INDEX ON users USING GIN (preferences jsonb_path_ops);
   ```
   3x smaller + 2x faster cho `@>` operator. Chỉ support `@>` (không `?`). 90% case `@>` đủ.

4. **Array native** (`text[]`, `int[]`): list **homogeneous primitive** (tags, IDs). Simpler, faster scalar ops. **JSONB array**: list **heterogeneous objects** hoặc nested. JSONB flexible nhưng overhead hơn.

5. **Postgres FTS đủ** khi: <10M rows, simple search, want 1 less infra component. **Elasticsearch** khi: complex faceting, multi-language stemming, real-time + analytics big-data, fuzzy match advanced. 2026 trend: Postgres FTS cover 70% case → save running ES.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### JSONB operators

```sql
->  ->>     navigate (jsonb / text)
#>  #>>     path access
@>  <@      contains / contained
?   ?| ?&    key exists / any / all
||           merge (top-level only)
-            remove key
#-           remove path
jsonb_set()  update path
```

### JSONB indexes

```sql
-- GIN cho @>, ?
CREATE INDEX ON t USING GIN (col jsonb_path_ops);

-- B-tree expression cho ->>= 'X'
CREATE INDEX ON t ((col ->> 'key'));
```

### Arrays

```sql
ARRAY['a','b']  '{a,b}'   -- create
arr[1]  arr[2:3]            -- access (1-indexed!)
arr @> ARRAY['x']           -- contains
arr && ARRAY['x','y']       -- overlap
arr || 'new'                -- append
array_remove(arr, 'x')
unnest(arr)                  -- expand to rows
```

### Full-text search

```sql
-- Setup
ALTER TABLE t ADD COLUMN sv tsvector
GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;
CREATE INDEX ON t USING GIN (sv);

-- Search
SELECT *, ts_rank(sv, q) FROM t, plainto_tsquery('english', 'query') q
WHERE sv @@ q ORDER BY ts_rank(sv, q) DESC;

-- Highlight
SELECT ts_headline('english', content, q) FROM t, plainto_tsquery(...) q;
```

### pgvector

```sql
CREATE EXTENSION vector;
ALTER TABLE t ADD COLUMN emb VECTOR(1536);
CREATE INDEX ON t USING hnsw (emb vector_cosine_ops);
SELECT * FROM t ORDER BY emb <=> '[...]' LIMIT 10;
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **JSON** | Text format, parsed mỗi access (slow) |
| **JSONB** | Binary JSON, indexed, fast (default) |
| **`->` `->>`** | JSONB / text accessor |
| **`#>` `#>>`** | Path JSONB / text accessor |
| **`@>` `<@`** | Contains / contained |
| **GIN** | Generalized Inverted Index for JSONB/array |
| **`jsonb_path_ops`** | GIN smaller + faster cho `@>` |
| **`jsonb_set`** | Update specific path |
| **`||`** | Merge JSONB |
| **Array native** | `text[]`, `int[]`, 1-indexed |
| **`tsvector`** | Parsed + stemmed text for FTS |
| **`tsquery`** | Search query for FTS |
| **`@@`** | FTS match operator |
| **`ts_rank`** | FTS relevance score |
| **`ts_headline`** | FTS highlight matches |
| **pgvector** | Extension for vector embeddings |
| **HNSW** | Approximate nearest neighbor index |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Indexes & Performance — EXPLAIN ANALYZE, B-tree, GIN, BRIN](02_indexes-and-performance.md)
- ➡️ **Bài tiếp theo:** [Backup & Replication — Production essentials](04_backup-and-replication.md)
- ↑ **Về cụm:** [postgresql README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [Postgres JSONB docs](https://www.postgresql.org/docs/current/datatype-json.html)
- 📖 [Postgres FTS docs](https://www.postgresql.org/docs/current/textsearch.html)
- 📖 [pgvector docs](https://github.com/pgvector/pgvector)
- 📖 [Crunchy Data: JSONB performance](https://www.crunchydata.com/blog/jsonb-multi-column-type-casting-in-postgres-17)
- 📖 [Supabase: AI vector embeddings](https://supabase.com/docs/guides/ai)

---

> 🎯 *Sau bài này bạn dùng JSONB + arrays + FTS — Postgres killer features. Bài cuối cluster dạy **backup + replication** — production essentials.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `postgresql/` lesson 4/5. Cover: JSON vs JSONB + 7 operator (`->`, `->>`, `#>`, `#>>`, `?`, `@>`, `<@`) + GIN index cho JSONB + Arrays (1D, multi-D) + ANY/ALL + Full-text search (tsvector, tsquery, ranking) + GIN cho FTS.
- **v1.1.0 (25/05/2026)** — Thêm lead-in 2-3 câu trước §1 JSON vs JSONB + Create+insert + `'{}'::jsonb` cast + §2 `->` vs `->>` + path `#>` + `#>>`. Chuẩn hoá tên trong INSERT example + tiêu đề §7. Thêm Changelog section.
