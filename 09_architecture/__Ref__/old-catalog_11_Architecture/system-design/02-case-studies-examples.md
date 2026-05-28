# System Design — Case Studies

> **Tags:** `system-design` `scalability` `distributed-systems` `interview` `architecture`
> **Level:** Advanced | **Prerequisite:** `system-design/01-system-design.md`

---

## 1. URL Shortener (Bitly/TinyURL)

### Requirements
```
Functional:
  - Shorten long URL → short URL (e.g., tinyurl.com/abc123)
  - Redirect short URL → original long URL
  - Optional: custom alias, expiry, analytics

Non-functional:
  - 100M URLs shortened per day
  - 10:1 read:write ratio → 1000M reads/day
  - High availability, low latency (<100ms)
  - Short URL is unique globally

Estimates:
  Writes:  100M/day = ~1200/s
  Reads:   1B/day   = ~12000/s
  Storage: 100M × 500 bytes = 50GB/day → 18TB/year
```

### Design
```
1. URL Shortening Algorithm:
   Option A: Random ID (Base62)
     - Generate random 7 chars from [a-zA-Z0-9] = 62^7 = 3.5 trillion combinations
     - Check DB for collision, retry if exists
   
   Option B: MD5 Hash (take first 7 chars)
     - MD5(long_url) = 128-bit hash → Base62 encode → take first 7 chars
     - Deterministic (same URL always gets same hash)
     - Collision risk: store full hash, collision → append counter
   
   Option C: Counter + Base62 (Twitter Snowflake-like)
     - Auto-incrementing counter → Base62 encode
     - Predictable/enumerable (security risk)

2. Database Schema:
   urls table:
     short_id  VARCHAR(7) PRIMARY KEY
     long_url  TEXT NOT NULL
     user_id   INT (nullable)
     created_at TIMESTAMP
     expires_at TIMESTAMP (nullable)
     click_count INT DEFAULT 0

3. System Architecture:
   [Client] → [CDN/Cache] → [Load Balancer]
                              ↓
                         [API Servers] → [Cache (Redis)] → [DB (PostgreSQL)]
                              ↓
                         [Analytics Service] → [ClickHouse/BigQuery]

4. Redirect Flow:
   - Client → GET tinyurl.com/abc123
   - API checks Redis cache (L1)
   - Cache miss → query PostgreSQL
   - Return HTTP 301 (permanent, browser caches) or 302 (temporary, we track)
   - 301 causes fewer requests but harder to track analytics
   - 302 every request → accurate analytics

5. Scaling:
   - Cache hit rate should be ~99% (20% URLs = 80% traffic)
   - Read replicas for DB
   - Async analytics (fire-and-forget to Kafka → consumer updates count)
```

---

## 2. Twitter/X Feed

### Requirements
```
- Post tweet (text, images, video)
- Follow/unfollow users
- View home timeline (tweets from people you follow, reverse chronological)
- 300M DAU, 350K tweets/minute = ~6000 writes/s
- Read: 100x more than writes

Key challenge: "Fan-out" problem
  Celebrity with 50M followers posts → 50M people need to see it!
```

### Design
```
Two approaches for home timeline:

Approach 1: Pull (Fan-out on read)
  - Query DB: "get tweets from all users I follow, sort by time"
  - Problem: hot user with 10K followees → heavy DB query on every timeline load

Approach 2: Push (Fan-out on write)  ← Twitter uses this for most users
  - When user tweets → write to timeline cache of ALL followers
  - Timeline request → instant lookup from pre-computed cache
  - Problem: 50M followers × 1 tweet = 50M cache writes = SLOW!

Hybrid (Twitter actual approach):
  - Regular users (<10K followers): push to follower timelines
  - "Hot users" (>1M followers): pull on read, merged at serving time
  
Timeline Service Architecture:
  POST /tweet → [Fanout Service]
                     ↓
            [Message Queue (Kafka)]
                     ↓
        [Fanout Workers] → write tweet_id to follower's timeline in Redis
  
  GET /timeline → [Timeline API] → Redis (pre-built timeline)
                                 → For hot users: merge with DB query
```

```
Data Model:
  tweets:      (id, user_id, content, media_urls, created_at)
  follows:     (follower_id, followee_id, created_at)
  timeline:    Redis sorted set: key="timeline:{user_id}", score=timestamp, member=tweet_id

Media Storage:
  Upload → [API] → [Object Store (S3)] → [CDN (CloudFront)]
  Store media URL in tweet, CDN serves video/images
```

---

## 3. YouTube / Video Streaming

### Requirements
```
- Upload videos
- Watch videos (adaptive streaming)
- Search, recommendations
- 500 hours of video uploaded per minute
- 1B hours watched per day

Storage:
  1 min video (HD) = ~375MB raw
  Compressed: ~50MB for 1080p at 1min
  500 hours/min = 30,000 min/min × 50MB = 1.5TB/minute = 2.2PB/day
```

### Design
```
Video Upload Pipeline:
  [User] → [Upload Service] → [Raw Video Storage (S3)]
                                        ↓
                              [Message Queue (Kafka)]
                                        ↓
                         [Transcoding Workers (FFmpeg)]
                                        ↓
                    [Multiple resolutions: 360p/720p/1080p/4K]
                                        ↓
                         [Transcoded Video CDN (CloudFront)]
                                        ↓
                            [Update DB: video ready]

Adaptive Bitrate Streaming (ABR):
  - Video split into 4-10 second segments
  - Served as HLS (HTTP Live Streaming) or DASH
  - Player adapts quality based on bandwidth
  - m3u8 playlist → contains segment URLs at each quality level

Video Metadata DB:
  videos: (id, user_id, title, description, duration, view_count, upload_at, status)
  status: 'processing' | 'ready' | 'failed'

Watch Service:
  - GET /watch/{video_id} → API → Metadata DB (video info)
  - Video segments served from CDN (never from API servers!)
  - Track resume position → Redis: "position:{user_id}:{video_id}" = timestamp

Recommendations:
  Separate ML service (TF/PyTorch) running collaborative filtering
  Scores updated in batch (hourly) → stored in Redis for fast serving
```

---

## 4. Chat Application (WhatsApp)

### Requirements
```
- 1:1 direct messages
- Group messages (up to 256 members)
- Online/offline status
- Message delivery receipts (sent ✓, delivered ✓✓, read ✓✓ blue)
- 65B messages/day = ~750K messages/second
```

### Design
```
Architecture:
  [Client A] → [WebSocket Connection] → [Chat Server A]
  [Client B] → [WebSocket Connection] → [Chat Server B]
  
  How message A→B gets from Server A to Server B?
  → Pub/Sub: Server A publishes to Redis channel → Server B subscribes and delivers

Message Flow:
  1. Client A sends message to Server A (WebSocket)
  2. Server A saves message to DB (Cassandra for write-heavy workload)
  3. Server A looks up which Chat Server handles Client B
     → Service Discovery: "user_server_map" in Redis/ZooKeeper
  4. Server A → publishes to Redis Pub/Sub channel for Client B
  5. Server B → receives from Redis → delivers to Client B via WebSocket
  6. Client B sends "delivered" receipt
  7. Client B reads → sends "read" receipt

Message Storage:
  Cassandra — excellent for chat:
    Partition key: conversation_id
    Clustering key: message_id (time-based UUID)
    → Fast retrieval: "get all messages in conversation X since timestamp Y"
  
  Cassandra table:
    (conversation_id, message_id, sender_id, content, media_url, type, status)

Online Presence:
  - User connects: SET "online:{user_id}" = {server_id, last_seen} with TTL=30s
  - Heartbeat every 10s (client → server) → refresh TTL
  - Disconnect: key expires → offline after 30s
  - "Is X online?" → check Redis key exists

Group Messages:
  - Store group_members list
  - Fan-out: for each member → deliver via their server
  - Large groups: async fan-out via queue
```

---

## 5. Ride-Sharing (Uber)

### Requirements
```
- Drivers share real-time location
- Riders request ride → match nearest available driver
- Real-time tracking during ride
- 15M rides/day, surge pricing
- Location updates: drivers ping every 4 seconds

Estimates:
  Active drivers peak = 1M
  Location updates: 1M × (1 update/4s) = 250K writes/second
```

### Design
```
Location Update Flow:
  Driver App → Every 4 seconds: POST /driver/{id}/location {lat, lng}
  
  Location Storage Options:
  A) Redis Geospatial (ZADD with geo score)
     GEOADD drivers_online {long} {lat} driver_123
     GEORADIUS drivers_online {user_lng} {user_lat} 5 km → nearest drivers
  
  B) Geohash (subdivide area into cells)
     lat/lng → 7-char geohash (≈153m × 153m cell)
     Key: "geohash:{cell}" → set of driver IDs in that cell
     Nearby search: query cell + 8 surrounding cells

Ride Matching:
  1. Rider requests ride from location X
  2. Find nearby drivers (geospatial query, 5km radius)
  3. Filter: available, high rating, right vehicle type
  4. Send ride offer to top N candidates (simultaneously)
  5. First to accept gets the ride
  6. Update driver status → BUSY
  
Matching Service:
  [Rider Request] → [Matching Service]
                         ↓
               [Location Service (Redis Geo)]
                         ↓
               [N nearest drivers found]
                         ↓
               [Push notification to drivers (WebSocket/FCM)]
                         ↓
               [First accept → Ride Created (SQL DB)]

Real-time Tracking:
  Driver → Location Update Service (every 4s) → Redis
  Rider → Polls /ride/{id}/driver-location → Returns from Redis
  Or: WebSocket push from driver to rider
  
ETA Calculation:
  Maps service (Google Maps API or internal road graph + Dijkstra)
  Takes into account: traffic data, road type, time of day
```

---

## 6. Notification System

### Requirements
```
- Push (mobile), SMS, Email
- 10M notifications/day
- Priority support (OTP SMS must be fast, newsletter can wait)
- Retry on failure
- Rate limiting per user
```

### Design
```
Architecture:
  [Services (Order, Auth, etc.)] → [Notification API]
                                           ↓
                                   [Message Queue]
                                    /      |      \
                              [SMS]  [Email] [Push]
                             Worker  Worker  Worker
                                |      |       |
                              Twilio SendGrid  APNs/FCM

Notification API:
  POST /notify {
    user_id,
    channel: ["sms", "push"],
    template: "order_confirmed",
    data: { order_id: "ORD-123" },
    priority: "high" | "normal",
  }

Priority Queues:
  high_priority_queue  → OTP, security alerts (process immediately)
  normal_queue         → Order updates, promotions
  batch_queue          → Newsletter, marketing (process overnight)

Worker Design:
  - Fetch user preferences (opt-in/opt-out)
  - Render template with user data
  - Call provider API (Twilio/SendGrid/FCM)
  - On failure: retry with exponential backoff
  - Max retries: 3, then move to DLQ
  - Log delivery status back to DB

Rate Limiting:
  - Max 5 SMS per user per hour
  - Max 3 push per user per 5 minutes
  - Implemented with Redis sliding window counter

Database:
  notifications: (id, user_id, channel, template, status, sent_at, attempts)
  status: 'pending' | 'sent' | 'failed' | 'delivered' | 'clicked'
  
  user_preferences: (user_id, channel, enabled, time_zone, quiet_hours_start/end)
```

---

## 7. Design Numbers Reference

```
Latency Target by Component:
  In-memory cache (Redis): 0.1-1ms
  Same-region DB query:    5-20ms
  Inter-region:            50-150ms
  
Throughput Ballparks:
  Single DB server (PostgreSQL): 5,000-10,000 QPS (simple queries)
  Redis single node:             100,000+ ops/s
  Kafka partition:               10,000+ messages/s
  HTTP API server (8-core):      5,000-20,000 RPS

Storage:
  1 char = 1 byte
  1 photo = 1MB average
  1 min video = 50MB (compressed, 1080p)
  1 min audio = 1MB (MP3 128kbps)

Users to servers (rough):
  1M  requests/day = ~12 RPS = 1 small server
  10M requests/day = ~120 RPS = 1 medium server
  1B  requests/day = ~12K RPS = ~10 servers + caching
```

---

*Tài liệu liên quan: `system-design/01-system-design.md` | `system-design/03-scalability.md` | `nosql/02-redis-deep-dive.md`*
