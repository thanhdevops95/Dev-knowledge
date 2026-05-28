# ⏱️ Background Jobs — Xử lý tác vụ nền

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Tách heavy tasks khỏi request/response cycle

---

## Tại sao cần Background Jobs?

HTTP request timeout thường là 30-60 giây. Nhưng nhiều tác vụ mất **phút hoặc giờ**: gửi 10,000 emails, process video 4K, generate PDF report, sync data...

Nếu chạy trong request handler → user chờ mãi → timeout → lỗi.

```
❌ Synchronous (user chờ):
  POST /api/reports → Generate report (5 phút) → Response
  User: "Trang bị treo?" → Refresh → Tạo lại report → Lỗi 😫

✅ Background Job (user không chờ):
  POST /api/reports → Tạo job → Response: "Đang xử lý..." (200ms)
  Background Worker: Process report (5 phút)
  → Notify user: "Report sẵn sàng, tải về tại đây"
```

### Types of Background Jobs

| Type | Ví dụ | Tool |
|---|---|---|
| **Queued jobs** | Send email, resize image | BullMQ, Celery |
| **Scheduled (cron)** | Daily report, cleanup old data | node-cron, Celery Beat |
| **Delayed** | "Nhắc nhở sau 24h nếu chưa thanh toán" | BullMQ delay |
| **Recurring** | Sync data mỗi giờ | Cron, CloudWatch Events |

---

## 1. BullMQ — Queue cho Node.js (Redis-backed)

### Tại sao BullMQ?

BullMQ dùng Redis làm message broker — đáng tin cậy, nhanh, hỗ trợ retry, delay, priority, rate limiting. Nó là standard de facto cho background jobs trong Node.js.

### Producer: Tạo job

```typescript
import { Queue } from 'bullmq';

// Tạo queue (connect Redis)
const emailQueue = new Queue('email', {
    connection: { host: '127.0.0.1', port: 6379 },
});

// API handler: tạo job, trả response ngay
app.post('/api/orders', async (req, res) => {
    const order = await db.orders.create(req.body);

    // Thêm job vào queue — KHÔNG chờ xử lý!
    await emailQueue.add('order-confirmation', {
        orderId: order.id,
        userEmail: req.user.email,
        orderTotal: order.total,
    }, {
        attempts: 3,                    // Retry 3 lần nếu fail
        backoff: { type: 'exponential', delay: 5000 },  // 5s, 10s, 20s
        removeOnComplete: { count: 1000 },   // Giữ 1000 completed jobs
        removeOnFail: { age: 7 * 24 * 3600 }, // Xóa failed jobs sau 7 ngày
    });

    res.status(201).json({ order, message: 'Email xác nhận đang được gửi' });
    // Response trong ~100ms, user không phải chờ email sending!
});

// Delayed job: nhắc nhở sau 24h
await emailQueue.add('payment-reminder', { orderId: order.id }, {
    delay: 24 * 60 * 60 * 1000,  // 24 giờ
});

// Scheduled (repeatable): daily report
await emailQueue.add('daily-report', {}, {
    repeat: { cron: '0 9 * * *' },  // 9 AM mỗi ngày
});
```

### Consumer: Xử lý job

```typescript
import { Worker } from 'bullmq';

// Worker chạy RIÊNG process (hoặc riêng server)
const worker = new Worker('email', async (job) => {
    console.log(`Processing job ${job.id}: ${job.name}`);

    switch (job.name) {
        case 'order-confirmation': {
            const { orderId, userEmail, orderTotal } = job.data;
            const order = await db.orders.findById(orderId);

            await sendEmail({
                to: userEmail,
                subject: `Xác nhận đơn hàng #${orderId}`,
                html: renderOrderConfirmation(order),
            });

            // Update progress (cho monitoring)
            await job.updateProgress(100);
            return { sent: true, email: userEmail };
        }

        case 'payment-reminder': {
            const order = await db.orders.findById(job.data.orderId);
            if (order.status === 'paid') return { skipped: true }; // Đã thanh toán
            await sendPaymentReminder(order);
            return { sent: true };
        }

        case 'daily-report': {
            const report = await generateDailyReport();
            await sendToSlack(report);
            return { reportDate: new Date().toISOString() };
        }
    }
}, {
    connection: { host: '127.0.0.1', port: 6379 },
    concurrency: 5,  // Xử lý 5 jobs đồng thời
    limiter: {
        max: 10,     // Rate limit: max 10 jobs
        duration: 1000, // per second (tránh spam API)
    },
});

// Event handlers
worker.on('completed', (job, result) => {
    console.log(`✅ Job ${job.id} completed:`, result);
});

worker.on('failed', (job, err) => {
    console.error(`❌ Job ${job.id} failed (attempt ${job.attemptsMade}):`, err.message);
    // Alert nếu hết retries
    if (job.attemptsMade >= job.opts.attempts) {
        alertOpsTeam(`Job permanently failed: ${job.name}`, err);
    }
});
```

---

## 2. Patterns & Best Practices

### Idempotency — Job chạy lại cho cùng kết quả

Jobs **có thể chạy nhiều lần** (retry, duplicate). Code phải **idempotent**:

```typescript
// ❌ Không idempotent: gửi email mỗi lần job chạy
async function processJob(job) {
    await sendEmail(job.data.email, 'Welcome!');
    // Retry 3 lần = gửi 3 emails! 😱
}

// ✅ Idempotent: check trước khi gửi
async function processJob(job) {
    const alreadySent = await db.emailLogs.findOne({
        jobId: job.id,
        status: 'sent',
    });
    if (alreadySent) return { skipped: true };

    await sendEmail(job.data.email, 'Welcome!');
    await db.emailLogs.create({ jobId: job.id, status: 'sent' });
}
```

### Dead Letter Queue (DLQ) — Jobs thất bại vĩnh viễn

```typescript
// Jobs fail sau tất cả retries → chuyển vào DLQ
worker.on('failed', async (job, err) => {
    if (job.attemptsMade >= job.opts.attempts) {
        // Chuyển vào dead letter queue để review manual
        await deadLetterQueue.add('failed-job', {
            originalQueue: 'email',
            originalJob: job.data,
            error: err.message,
            failedAt: new Date(),
        });
    }
});
```

### Monitoring — BullBoard UI

```typescript
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
createBullBoard({
    queues: [
        new BullMQAdapter(emailQueue),
        new BullMQAdapter(reportQueue),
    ],
    serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());
// Dashboard: xem jobs pending, active, completed, failed
```

---

## 3. Celery — Queue cho Python

```python
# tasks.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, user_email, subject, body):
    try:
        send_email(user_email, subject, body)
    except SMTPError as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 60)

@app.task
def generate_report(report_type, date_range):
    data = query_database(report_type, date_range)
    pdf = render_pdf(data)
    upload_to_s3(pdf)
    return {'url': pdf.url}

# Gọi task (async, không chờ)
result = send_email_task.delay('user@test.com', 'Welcome', 'Hello!')
# result.id → task ID để track status

# Scheduled tasks (Celery Beat)
# celeryconfig.py
beat_schedule = {
    'daily-cleanup': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # 2 AM daily
    },
}
```

---

## Khi nào dùng gì?

| Tình huống | Solution |
|---|---|
| Email, SMS, push notification | Queue (BullMQ/Celery) |
| Image/video processing | Queue + dedicated workers |
| Daily reports, cleanup | Scheduled jobs (cron) |
| "Nhắc nhở sau N giờ" | Delayed jobs |
| Real-time event processing | Kafka/RabbitMQ |
| Simple cron (< 5 tasks) | node-cron (không cần Redis) |
| Serverless | AWS SQS + Lambda |

---

## Bài tập thực hành

- [ ] BullMQ: email queue với retry + delay
- [ ] Dashboard: setup BullBoard monitoring
- [ ] Idempotency: đảm bảo job chạy lại không duplicate
- [ ] Scheduled: daily report job chạy 9AM

---

## Tài nguyên thêm

- [BullMQ Docs](https://docs.bullmq.io/) — Official
- [Celery Docs](https://docs.celeryq.dev/) — Python
- [BullBoard](https://github.com/felixmosh/bull-board) — Dashboard UI
