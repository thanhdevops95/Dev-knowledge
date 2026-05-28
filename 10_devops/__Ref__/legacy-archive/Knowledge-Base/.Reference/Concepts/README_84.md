# Module 09: MONITORING BASICS - Giám sát ứng dụng

> **Thời gian học:** 1 tuần
>
> **Prerequisite:** Module 05 (Docker), Module 07 (NGINX), Module 08 (Deployment)
>
> **Difficulty:** ⭐⭐⭐☆☆

---

## 📋 Mục lục

1. [Monitoring là gì?](#1-monitoring-là-gì)
2. [Metrics & Logs](#2-metrics--logs)
3. [Docker Logs](#3-docker-logs)
4. [Health Checks](#4-health-checks)
5. [Basic Metrics Collection](#5-basic-metrics-collection)
6. [Alerting Fundamentals](#6-alerting-fundamentals)
7. [Uptime Monitoring](#7-uptime-monitoring)
8. [Dashboard Basics](#8-dashboard-basics)
9. [Incident Response](#9-incident-response)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **tại sao monitoring quan trọng** trong production
- ✅ Phân biệt **metrics, logs, traces**
- ✅ Thu thập và xem **Docker container logs**
- ✅ Implement **health check endpoints**
- ✅ Monitor **basic metrics** (CPU, memory, disk)
- ✅ Setup **uptime monitoring** miễn phí
- ✅ Tạo **simple dashboard** hiển thị metrics
- ✅ Respond đúng cách khi có **incidents**
- ✅ Follow **on-call best practices**

---

## 1. Monitoring là gì?

### 1.1. Vấn đề khi không có Monitoring

**Scenario: Production app không có monitoring**

```
03:00 AM - User tweets: "Website down!"
03:30 AM - More complaints on social media
04:00 AM - CEO calls: "Why is our site down?!"
04:15 AM - You wake up, check phone, panic
04:30 AM - SSH vào server
04:45 AM - Find issue: Disk full (logs filled drive)
05:00 AM - Fix: Clean logs, restart app
05:30 AM - Site back up (2.5 hours downtime)

Problems:
❌ Found issue 1+ hour sau khi users noticed
❌ No visibility vào what happened
❌ Manual investigation (slow)
❌ No alert (relied on user complaints)
❌ Damage: Lost revenue, angry users, bad PR
```

### 1.2. Monitoring Benefits

**With monitoring:**

```
03:00 AM - Alert: "Disk usage > 90%"
03:01 AM - You receive SMS/email
03:05 AM - Check dashboard từ phone
03:10 AM - Run cleanup script remotely
03:15 AM - Disk back to 60%, app stable
03:20 AM - Back to sleep

Results:
✅ Detected BEFORE users noticed
✅ Fixed in 15 minutes (not 2.5 hours)
✅ Zero user impact
✅ Know exact problem location
✅ Can prevent future issues
```

**Key benefits:**

| Benefit | Description |
|---------|-------------|
| **Early detection** | Catch problems trước khi users affected |
| **Faster resolution** | Know exactly what's wrong, where |
| **Capacity planning** | Track growth, plan resources |
| **SLA compliance** | Prove uptime commitments |
| **Performance optimization** | Identify bottlenecks |
| **Debugging** | Logs help reproduce bugs |
| **Security** | Detect suspicious activity |

### 1.3. Observability Pillars

**Three pillars of observability:**

```
┌─────────────────────────────────────────┐
│          OBSERVABILITY                  │
│                                         │
│  ┌────────┐  ┌──────┐  ┌────────────┐  │
│  │ METRICS│  │ LOGS │  │  TRACES    │  │
│  │        │  │      │  │            │  │
│  │ What?  │  │ Why? │  │ Where?     │  │
│  │ Nums   │  │Events│  │ Flow       │  │
│  └────────┘  └──────┘  └────────────┘  │
└─────────────────────────────────────────┘
```

**1. Metrics (Số liệu):**

```
What is happening?
- CPU: 75%
- Memory: 2.5 GB
- Requests/sec: 1000
- Error rate: 0.5%
- Response time: 250ms

Time-series data (numbers over time)
```

**2. Logs (Nhật ký):**

```
Why did it happen?
[2024-12-25 10:30:15] INFO User login: alice@example.com
[2024-12-25 10:30:18] ERROR Database connection timeout
[2024-12-25 10:30:20] WARN Retrying connection (attempt 2/3)
[2024-12-25 10:30:25] INFO Connection restored

Event records (text, structured data)
```

**3. Traces (Dấu vết):**

```
Where did request go?
Request: GET /api/users/123
  ↓ 10ms - API Gateway
  ↓ 50ms - Auth Service
  ↓ 200ms - User Service
    ↓ 180ms - Database query
  ↓ 30ms - Response formatting
Total: 290ms

Distributed tracing (request flow)
```

**Module này focus:** Metrics & Logs basics

---

## 2. Metrics & Logs

### 2.1. What are Metrics?

**Metrics = Numerical measurements over time**

**Types:**

**1. Counters (đếm, chỉ tăng):**

```javascript
total_requests: 1,234,567
total_errors: 156
total_sales: $45,000
```

**2. Gauges (giá trị tại thời điểm):**

```javascript
cpu_usage: 45.2%
memory_used: 2.5 GB
active_connections: 87
queue_size: 12
```

**3. Histograms (phân phối):**

```javascript
response_time:
  p50: 100ms  (50% requests < 100ms)
  p95: 250ms  (95% requests < 250ms)
  p99: 500ms  (99% requests < 500ms)
```

**4. Rates (tốc độ):**

```javascript
requests_per_second: 1000
errors_per_minute: 5
bytes_sent_per_second: 1.5 MB
```

**Common metrics:**

| Category | Examples | Why important |
|----------|----------|---------------|
| **System** | CPU, RAM, disk, network | Resource exhaustion |
| **Application** | Request rate, error rate, latency | Performance issues |
| **Business** | Orders/min, revenue, active users | Business health |
| **Custom** | Items processed, cache hit rate | App-specific |

### 2.2. What are Logs?

**Logs = Events recorded by application**

**Log levels:**

```javascript
TRACE   // Very detailed (development only)
DEBUG   // Debug information
INFO    // Normal operations
WARN    // Warning, potential issue
ERROR   // Error occurred, handled
FATAL   // Critical error, app crash
```

**Example log entries:**

```log
# Good log (structured, informative)
2024-12-25T10:30:15.123Z [INFO] user_service | User login successful | user_id=123 email=alice@example.com ip=192.168.1.1 duration=45ms

# Bad log (không đủ context)
2024-12-25 10:30:15 Login OK

# Error log
2024-12-25T10:35:42.567Z [ERROR] payment_service | Payment failed | order_id=456 reason="insufficient_funds" user_id=789 amount=$99.99
```

**Structured logging (JSON):**

```json
{
  "timestamp": "2024-12-25T10:30:15.123Z",
  "level": "INFO",
  "service": "user_service",
  "message": "User login successful",
  "user_id": 123,
  "email": "alice@example.com",
  "ip": "192.168.1.1",
  "duration_ms": 45
}
```

**Benefits của structured logs:**

- Easy to parse
- Searchable by fields
- Can aggregate (count logins per user)
- Machine-readable

### 2.3. Metrics vs Logs

**When to use what:**

| Scenario | Use | Example |
|----------|-----|---------|
| Overall health | Metrics | CPU at 75% |
| Specific event | Logs | User 123 logged in |
| Performance trend | Metrics | Response time p95 increasing |
| Debug issue | Logs | Error stack trace |
| Alert | Metrics | Error rate > 5% |
| Audit trail | Logs | Who deleted file X? |

**Best practice:** Use both!

```
Alert from metrics → Check logs for details
```

---

## 3. Docker Logs

### 3.1. Docker Logging Basics

**Docker forwards container output (stdout/stderr) to logs**

**View logs:**

```bash
# Show all logs
docker logs container-name

# Follow logs (real-time)
docker logs -f container-name

# Last 100 lines
docker logs --tail 100 container-name

# Since timestamp
docker logs --since 2024-12-25T10:00:00 container-name

# With timestamps
docker logs -t container-name
```

**Example:**

```bash
# Start NGINX container
docker run -d --name nginx nginx:alpine

# View logs
docker logs nginx

# Output:
# /docker-entrypoint.sh: Configuration complete; ready for start up
# 2024/12/25 10:30:15 [notice] 1#1: nginx/1.25.3
# 2024/12/25 10:30:15 [notice] 1#1: start worker processes
```

### 3.2. Application Logging in Containers

**NodeJS app logging:**

```javascript
// app.js
console.log('Server starting...');  // stdout → Docker logs

process.on('uncaughtException', (err) => {
    console.error('FATAL ERROR:', err);  // stderr → Docker logs
    process.exit(1);
});

app.use((req, res, next) => {
    // Request log
    console.log(`${req.method} ${req.url} ${req.ip}`);
    next();
});

app.get('/', (req, res) => {
    console.log('Index page accessed');
    res.send('Hello World');
});
```

**Run and view logs:**

```bash
docker build -t myapp .
docker run -d --name app myapp

docker logs -f app
# Output:
# Server starting...
# GET / 172.17.0.1
# Index page accessed
```

**Best practices:**

```javascript
// ✅ GOOD: Log to stdout/stderr
console.log('Info message');
console.error('Error message');

// ❌ BAD: Log to files inside container
fs.appendFile('/var/log/app.log', 'message');
// Lý do: Files lost khi container removed
//        Disk fills up
//        Hard to access
```

### 3.3. Log Drivers

**Docker supports multiple log drivers:**

```bash
# Default: json-file
docker run -d --log-driver json-file myapp

# Syslog
docker run -d --log-driver syslog myapp

# None (no logs, performance)
docker run -d --log-driver none myapp

# Custom options
docker run -d \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp
# Keeps max 3 files of 10MB each = 30MB total
```

**In docker-compose.yml:**

```yaml
services:
  app:
    image: myapp
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

### 3.4. Centralized Logging

**Problem:** Logs scattered across containers

**Solution:** Send all logs to central location

**Simple approach - File aggregation:**

```yaml
services:
  app:
    image: myapp
    volumes:
      - ./logs:/var/log/app  # Mount host directory

# All containers log to ./logs/
# Can use: tail -f ./logs/*.log
```

**Advanced (sẽ học trong Advanced Track):**

- ELK Stack (Elasticsearch, Logstash, Kibana)
- Loki (from Grafana)
- Fluentd
- Cloud services (AWS CloudWatch, Google Cloud Logging)

---

## 4. Health Checks

### 4.1. What is Health Check?

**Health check = Endpoint để verify app đang healthy**

**HTTP health check:**

```javascript
// NodeJS Express
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'healthy' });
});

// Returns:
// HTTP 200 OK
// { "status": "healthy" }
```

**Comprehensive health check:**

```javascript
app.get('/health', async (req, res) => {
    const health = {
        uptime: process.uptime(),
        timestamp: Date.now(),
        status: 'healthy'
    };
    
    try {
        // Check database
        await db.query('SELECT 1');
        health.database = 'connected';
        
        // Check Redis
        await redis.ping();
        health.redis = 'connected';
        
        // All good
        res.status(200).json(health);
    } catch (error) {
        health.status = 'unhealthy';
        health.error = error.message;
        res.status(503).json(health);  // 503 Service Unavailable
    }
});
```

**Response:**

```json
{
  "uptime": 12345.67,
  "timestamp": 1703500000000,
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
```

### 4.2. Docker Health Checks

**In Dockerfile:**

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "server.js"]
```

**healthcheck.js:**

```javascript
const http = require('http');

const options = {
    host: 'localhost',
    port: 3000,
    path: '/health',
    timeout: 2000
};

const request = http.request(options, (res) => {
    if (res.statusCode === 200) {
        process.exit(0);  // Healthy
    } else {
        process.exit(1);  // Unhealthy
    }
});

request.on('error', () => {
    process.exit(1);
});

request.end();
```

**View health status:**

```bash
docker ps

# CONTAINER ID   IMAGE    STATUS
# abc123         myapp    Up 5 min (healthy)

# If unhealthy:
# abc123         myapp    Up 5 min (unhealthy)
```

**In docker-compose.yml:**

```yaml
services:
  app:
    image: myapp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 40s
```

### 4.3. Readiness vs Liveness

**Two types of health checks:**

**1. Liveness probe:**

```
Question: "Is container alive?"
If fail: Restart container
Use case: Detect crashed/deadlocked containers
```

**2. Readiness probe:**

```
Question: "Is container ready to accept traffic?"
If fail: Stop sending traffic, but don't restart
Use case: Container starting up, loading data
```

**Example:**

```javascript
// Liveness: Simple check
app.get('/healthz', (req, res) => {
    res.status(200).send('OK');
});

// Readiness: Check dependencies
app.get('/ready', async (req, res) => {
    try {
        await db.ping();
        await cache.ping();
        res.status(200).send('Ready');
    } catch (err) {
        res.status(503).send('Not ready');
    }
});
```

---

## 5. Basic Metrics Collection

### 5.1. System Metrics

**Monitor server resources:**

**CPU usage:**

```bash
# Real-time
top

# Or htop (better UI)
sudo apt install htop
htop

# Average load
uptime
# 10:30:15 up 5 days, 3:25, 2 users, load average: 0.5, 0.8, 1.2
#                                              1min  5min  15min

# Per-core usage
mpstat -P ALL
```

**Memory:**

```bash
# Overall
free -h

# Output:
#               total        used        free      shared  buff/cache   available
# Mem:           7.7Gi       2.1Gi       3.2Gi       15Mi        2.4Gi       5.3Gi

# Detailed
vmstat 1
# Every second stats
```

**Disk:**

```bash
# Disk usage
df -h

# Output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1        50G   35G   13G  74% /

# Disk I/O
iostat -x 1
```

**Network:**

```bash
# Network usage
iftop

# Or
nload

# Connections
netstat -an | grep ESTABLISHED | wc -l
# Count of active connections
```

### 5.2. Application Metrics

**NodeJS example (using prom-client):**

```javascript
const express = require('express');
const promClient = require('prom-client');

const app = express();

// Create metrics
const register = new promClient.Registry();

// Counter: Total requests
const httpRequestsTotal = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total HTTP requests',
    labelNames: ['method', 'path', 'status'],
    registers: [register]
});

// Histogram: Response time
const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration',
    labelNames: ['method', 'path'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 5],
    registers: [register]
});

// Gauge: Active connections
const activeConnections = new promClient.Gauge({
    name: 'active_connections',
    help: 'Number of active connections',
    registers: [register]
});

// Middleware để track metrics
app.use((req, res, next) => {
    const start = Date.now();
    
    activeConnections.inc();
    
    res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        
        httpRequestsTotal.labels(req.method, req.path, res.statusCode).inc();
        httpRequestDuration.labels(req.method, req.path).observe(duration);
        activeConnections.dec();
    });
    
    next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
});

app.listen(3000);
```

**Metrics output:**

```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",path="/",status="200"} 1234

# HELP http_request_duration_seconds HTTP request duration
# TYPE http_request_duration_seconds histogram
http_request_duration_seconds_bucket{le="0.05",method="GET",path="/"} 890
http_request_duration_seconds_bucket{le="0.1",method="GET",path="/"} 1150
http_request_duration_seconds_sum{method="GET",path="/"} 45.67
http_request_duration_seconds_count{method="GET",path="/"} 1234

# HELP active_connections Number of active connections
# TYPE active_connections gauge
active_connections 45
```

### 5.3. Docker Metrics

**Docker stats command:**

```bash
docker stats

# Output:
CONTAINER ID   NAME     CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
a1b2c3d4       app      2.5%      150MiB / 1GiB        14.6%     1.2kB / 648B
```

**Programmatic access:**

```bash
# Get stats as JSON
docker stats --no-stream --format "{{json .}}" app

# Output:
{"Container":"app","CPUPerc":"2.5%","MemUsage":"150MiB / 1GiB"}
```

**cAdvisor (Container Advisor):**

```yaml
# docker-compose.yml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

# Access: http://localhost:8080
# Shows all container metrics
```

---

## 6. Alerting Fundamentals

### 6.1. When to Alert

**Alert fatigue problem:**

```
Too many alerts → Ignore all alerts → Miss critical issues
```

**Good alerting rules:**

**DO alert on:**

- ✅ User-impacting issues (site down, errors)
- ✅ Security incidents (intrusion, DDoS)
- ✅ Critical thresholds (disk 95% full)
- ✅ SLA violations (uptime < 99.9%)

**DON'T alert on:**

- ❌ Expected variations (traffic spikes during sales)
- ❌ Self-healing issues (auto-scaled, recovered)
- ❌ Non-critical warnings (disk 60% full)
- ❌ False positives (flapping checks)

### 6.2. Alert Levels

**Severity levels:**

```
P0 (Critical):
- Production down
- Data loss
- Security breach
→ Page on-call engineer immediately (SMS, phone call)

P1 (High):
- Degraded performance
- Some features broken
- High error rate
→ Alert via Slack, email

P2 (Medium):
- Potential issues
- Approaching limits
→ Log, notify during business hours

P3 (Low):
- FYI, informational
→ Log only
```

### 6.3. Simple Alerting

**Email alerts với cron:**

```bash
#!/bin/bash
# check_disk.sh

USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $USAGE -gt 90 ]; then
    echo "Disk usage critical: ${USAGE}%" | mail -s "ALERT: Disk full" admin@example.com
fi
```

```bash
# Add to crontab (run every hour)
crontab -e
0 * * * * /home/user/check_disk.sh
```

**Slack webhook:**

```bash
#!/bin/bash
# alert_slack.sh

WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"⚠️ Server disk usage > 90%"}' \
  $WEBHOOK_URL
```

**In application:**

```javascript
// NodeJS - Send alert on high error rate
let errorCount = 0;
let lastAlertTime = 0;

app.use((err, req, res, next) => {
    errorCount++;
    
    // Alert if > 10 errors in 1 minute
    if (errorCount > 10 && Date.now() - lastAlertTime > 60000) {
        sendSlackAlert(`High error rate: ${errorCount} errors/min`);
        lastAlertTime = Date.now();
        errorCount = 0;
    }
    
    res.status(500).send('Error');
});

async function sendSlackAlert(message) {
    await fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message })
    });
}
```

---

## 7. Uptime Monitoring

### 7.1. External Monitoring Services

**Free uptime monitors:**

**1. UptimeRobot (uptimerobot.com):**

- 50 monitors free
- Check every 5 minutes
- Email/SMS/Slack alerts
- Public status page

**Setup:**

```
1. Create account
2. Add monitor:
   - Type: HTTP(S)
   - URL: https://example.com
   - Interval: 5 minutes
3. Add alert contacts
4. Done!
```

**2. Pingdom (free tier):**

- Email alerts
- Global checks
- Response time tracking

**3. StatusCake:**

- Unlimited tests (free tier)
- 5 min intervals
- Email alerts

### 7.2. Simple Self-Hosted Monitoring

**Bash script watchdog:**

```bash
#!/bin/bash
# watchdog.sh

URL="https://example.com/health"
SLACK_WEBHOOK="https://hooks.slack.com/..."

while true; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
    
    if [ "$HTTP_CODE" != "200" ]; then
        echo "$(date): Site down! HTTP $HTTP_CODE"
        
        # Alert
        curl -X POST -H 'Content-type: application/json' \
          --data "{\"text\":\"🚨 Site down! HTTP $HTTP_CODE\"}" \
          $SLACK_WEBHOOK
        
        # Wait 5 min before re-alert
        sleep 300
    fi
    
    # Check every minute
    sleep 60
done
```

**Run with systemd:**

```ini
# /etc/systemd/system/watchdog.service
[Unit]
Description=Website Watchdog
After=network.target

[Service]
Type=simple
User=monitor
ExecStart=/home/monitor/watchdog.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
```

### 7.3. Status Page

**Why status page:**

- Users can self-check nếu site down
- Reduce support tickets
- Transparency builds trust

**Free options:**

- UptimeRobot (has public status page)
- Statuspage.io (Atlassian, free tier)
- Cachet (self-hosted, open source)

**Simple static status page:**

```html
<!-- status.html -->
<!DOCTYPE html>
<html>
<head>
    <title>System Status</title>
    <meta http-equiv="refresh" content="60">
</head>
<body>
    <h1>System Status</h1>
    
    <div id="status">Checking...</div>
    
    <script>
    async function checkStatus() {
        try {
            const res = await fetch('https://example.com/health');
            const data = await res.json();
            
            if (data.status === 'healthy') {
                document.getElementById('status').innerHTML = 
                    '✅ All systems operational';
            } else {
                document.getElementById('status').innerHTML = 
                    '⚠️ Partial outage';
            }
        } catch (err) {
            document.getElementById('status').innerHTML = 
                '🚨 Major outage';
        }
    }
    
    checkStatus();
    setInterval(checkStatus, 60000);  // Check every minute
    </script>
</body>
</html>
```

---

## 8. Dashboard Basics

### 8.1. Why Dashboards?

**Dashboard = Visual overview của system health**

**Good dashboard:**

- Glanceable (hiểu trong 5 giây)
- Actionable (biết cần làm gì)
- Relevant (chỉ important metrics)
- Current (real-time hoặc near real-time)

**Bad dashboard:**

- Too many metrics (information overload)
- Irrelevant data
- Slow/outdated
- No context (80% CPU, but is that bad?)

### 8.2. Essential Metrics to Display

**Golden Signals (from Google SRE):**

**1. Latency (độ trễ):**

```
How long requests take?
- Average: 100ms
- p95: 250ms
- p99: 500ms
```

**2. Traffic (lưu lượng):**

```
How many requests?
- Requests/second: 1000
- Bandwidth: 10 MB/s
```

**3. Errors (lỗi):**

```
How many failed?
- Error rate: 0.5%
- 5xx errors: 50/10000 requests
```

**4. Saturation (bão hòa):**

```
How full are resources?
- CPU: 75%
- Memory: 80%
- Disk: 60%
- Queue depth: 20 items
```

### 8.3. Simple Dashboard Example

**Using HTML + JavaScript:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Monitoring Dashboard</title>
    <style>
        .metric {
            display: inline-block;
            margin: 20px;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 8px;
        }
        .value {
            font-size: 48px;
            font-weight: bold;
        }
        .label {
            font-size: 14px;
            color: #666;
        }
        .healthy { color: green; }
        .warning { color: orange; }
        .critical { color: red; }
    </style>
</head>
<body>
    <h1>System Dashboard</h1>
    
    <div class="metric">
        <div class="value" id="cpu">-</div>
        <div class="label">CPU %</div>
    </div>
    
    <div class="metric">
        <div class="value" id="memory">-</div>
        <div class="label">Memory %</div>
    </div>
    
    <div class="metric">
        <div class="value" id="requests">-</div>
        <div class="label">Requests/sec</div>
    </div>
    
    <div class="metric">
        <div class="value" id="errors">-</div>
        <div class="label">Error rate %</div>
    </div>
    
    <script>
    async function updateMetrics() {
        const res = await fetch('/api/metrics');
        const data = await res.json();
        
        // CPU
        document.getElementById('cpu').textContent = data.cpu.toFixed(1);
        document.getElementById('cpu').className = 
            data.cpu > 90 ? 'value critical' :
            data.cpu > 70 ? 'value warning' : 'value healthy';
        
        // Memory
        document.getElementById('memory').textContent = data.memory.toFixed(1);
        
        // Requests
        document.getElementById('requests').textContent = data.requestsPerSec;
        
        // Errors
        document.getElementById('errors').textContent = data.errorRate.toFixed(2);
    }
    
    updateMetrics();
    setInterval(updateMetrics, 5000);  // Update every 5s
    </script>
</body>
</html>
```

**API endpoint:**

```javascript
app.get('/api/metrics', (req, res) => {
    const metrics = {
        cpu: getCPUUsage(),
        memory: getMemoryUsage(),
        requestsPerSec: getRequestRate(),
        errorRate: getErrorRate()
    };
    res.json(metrics);
});
```

---

## 9. Incident Response

### 9.1. Incident Lifecycle

```
1. DETECTION
   Alert fires → Someone notified
   ↓
2. ACKNOWLEDGMENT
   On-call engineer: "I got this"
   ↓
3. TRIAGING
   How bad? What's affected? Priority?
   ↓
4. INVESTIGATION
   Check logs, metrics, recent changes
   ↓
5. MITIGATION
   Quick fix to restore service
   ↓
6. RESOLUTION
   Proper fix deployed
   ↓
7. POST-MORTEM
   What happened? Why? How prevent?
```

### 9.2. On-Call Best Practices

**DO:**

- ✅ Acknowledge alerts nhanh (< 5 min)
- ✅ Update status page
- ✅ Communication clear, frequent
- ✅ Document actions taken
- ✅ Focus on mitigation first (restore service)
- ✅ Root cause analysis sau

**DON'T:**

- ❌ Panic
- ❌ Make changes without thinking
- ❌ Skip documentation
- ❌ Blame others
- ❌ Deploy untested fixes to production

**Incident communication template:**

```
Subject: [INCIDENT] Production API degraded

Status: INVESTIGATING
Started: 2024-12-25 10:30 UTC
Affected: API response time 10x slower
Impact: ~30% users experiencing slow page loads

Timeline:
10:30 - Alert fired: p95 latency > 5s
10:32 - ACK by Alice
10:35 - Initial investigation: DB CPU at 95%
10:40 - Identified slow query
10:45 - Applied temporary fix (added index)
10:50 - Metrics improving
11:00 - RESOLVED

Next steps:
- Monitor for 1 hour
- Post-mortem tomorrow
- Long-term fix: optimize query
```

### 9.3. Post-Mortem

**Blameless post-mortem:**

- Focus on WHAT happened, not WHO
- System improvements, not punishment
- Learning opportunity

**Template:**

```markdown
# Incident Post-Mortem: API Downtime 2024-12-25

## Summary
Production API was down for 30 minutes on Dec 25, affecting 10k users.

## Timeline (UTC)
- 10:30 - Alert: API returning 500 errors
- 10:32 - On-call acknowledged
- 10:35 - Found: Database connection pool exhausted
- 10:40 - Mitigation: Increased pool size 10 → 50
- 10:45 - Service recovering
- 11:00 - Fully recovered

## Root Cause
Traffic spike (2x normal) filled connection pool.
App couldn't get DB connections → errors.

## Impact
- Duration: 30 minutes
- Affected users: ~10,000
- Failed requests: ~5,000
- Revenue impact: ~$500

## What Went Well
✅ Alert fired immediately
✅ Mitigation quick (15 min)
✅ No data loss

## What Went Wrong
❌ Connection pool too small
❌ No auto-scaling for traffic spikes
❌ Missing alarm for connection pool usage

## Action Items
- [ ] Implement connection pool monitoring
- [ ] Auto-scale pool based on traffic
- [ ] Load testing with 5x expected traffic
- [ ] Add traffic spike alerts

## Lessons Learned
- Need better capacity planning
- Monitor resource limits, not just usage
- Test failure scenarios regularly
```

---

## 📚 Tổng kết

### Key Takeaways

1. **Monitoring = Eyes on production** - Detect issues early
2. **Metrics + Logs** - Numbers + events = complete picture
3. **Health checks** - Essential for automated recovery
4. **Alerts** - Too many = noise, too few = danger
5. **Dashboards** - Visual overview, glanceable
6. **Incident response** - Calm, methodical, documented
7. **Post-mortems** - Learn, improve, don't blame

### Checklist

- [ ] Understand monitoring importance
- [ ] Collect & view Docker logs
- [ ] Implement health check endpoints
- [ ] Monitor basic system metrics (CPU, memory, disk)
- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Create simple dashboard
- [ ] Configure alerts (email/Slack)
- [ ] Practice incident response
- [ ] Write post-mortem after incidents

### 🎉 Foundation Track Complete

**Congratulations! Bạn đã hoàn thành Foundation Track!**

**What you've learned:**

- ✅ Module 00: Environment setup
- ✅ Module 01: Linux basics
- ✅ Module 02: Git & GitHub
- ✅ Module 03: Networking
- ✅ Module 04: HTML/CSS/JS
- ✅ Module 05: Docker
- ✅ Module 06: CI/CD
- ✅ Module 07: NGINX
- ✅ Module 08: Deployment
- ✅ Module 09: Monitoring ← You are here!

**You can now:**

- Build web applications
- Containerize with Docker
- Setup CI/CD pipelines
- Deploy to production
- Monitor and maintain systems

### Next Steps

**1. Final Project:**
Complete Foundation FINAL_PROJECT để apply tất cả kiến thức!

**2. Advanced Track:**
17 modules chuyên sâu:

- Kubernetes
- Terraform
- Ansible
- Cloud (AWS/GCP)
- Advanced monitoring (Prometheus, Grafana)
- Security
- And more...

**3. Real-world practice:**

- Deploy personal projects
- Contribute to open source
- Build portfolio
- Apply for Junior DevOps roles

---

> **"Monitoring is not just about knowing when things break. It's about understanding how things work." - DevOps SRE** 📊

**🎓 Chúc mừng! Bạn đã sẵn sàng trở thành Junior DevOps Engineer!** 🚀
