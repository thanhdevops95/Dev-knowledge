# ☁️ AWS Core Services — Dịch vụ cốt lõi

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng cloud phổ biến nhất thế giới

---

## AWS Service Map

```
┌────────────────────────────────────────────────────────────┐
│                         AWS Cloud                          │
│                                                            │
│  Compute          Storage          Database                │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │   EC2    │    │    S3    │    │   RDS    │             │
│  │  Lambda  │    │   EBS   │    │ DynamoDB │             │
│  │   ECS    │    │   EFS   │    │ElastiCache│             │
│  │   EKS    │    │Glacier  │    │  Aurora  │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                                                            │
│  Networking       Security        Monitoring               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │   VPC    │    │   IAM   │    │CloudWatch│             │
│  │Route 53  │    │   KMS   │    │CloudTrail│             │
│  │CloudFront│    │   WAF   │    │ X-Ray    │             │
│  │   ALB    │    │Cognito  │    │          │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                                                            │
│  App Integration   Developer      AI/ML                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │   SQS    │    │CodeBuild│    │SageMaker │             │
│  │   SNS    │    │CodePipe │    │ Bedrock  │             │
│  │EventBrdg │    │  CDK    │    │ Rekogniz │             │
│  └──────────┘    └──────────┘    └──────────┘             │
└────────────────────────────────────────────────────────────┘
```

---

## 1. EC2 — Virtual Servers

```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.micro \
    --key-name my-keypair \
    --security-group-ids sg-12345 \
    --subnet-id subnet-12345 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=web-server}]'
```

```
Instance Types:
t3.micro   — Burstable, $8/month     → Dev, testing
t3.medium  — Burstable, $30/month    → Small apps
m6i.large  — General, $70/month      → Production apps
c6i.large  — Compute, $62/month      → CPU-intensive
r6i.large  — Memory, $91/month       → Databases, caching
g5.xlarge  — GPU, ~$760/month        → ML training

Pricing models:
• On-Demand:     Trả theo giờ (linh hoạt nhất)
• Reserved:      Cam kết 1-3 năm → tiết kiệm 40-70%
• Spot:          Bid giá → tiết kiệm đến 90% (có thể bị terminate!)
• Savings Plans: Cam kết usage → tiết kiệm 40-60%
```

---

## 2. S3 — Object Storage

```javascript
import { S3Client, PutObjectCommand, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({ region: 'ap-southeast-1' });

// Upload file
await s3.send(new PutObjectCommand({
    Bucket: 'my-app-uploads',
    Key: `avatars/${userId}/${filename}`,
    Body: fileBuffer,
    ContentType: 'image/jpeg',
}));

// Generate presigned URL (upload trực tiếp từ client)
const uploadUrl = await getSignedUrl(s3, new PutObjectCommand({
    Bucket: 'my-app-uploads',
    Key: `uploads/${filename}`,
}), { expiresIn: 300 });  // 5 phút
// Client upload trực tiếp lên S3, không qua server!

// Generate presigned URL (download)
const downloadUrl = await getSignedUrl(s3, new GetObjectCommand({
    Bucket: 'my-app-uploads',
    Key: 'avatars/user1/photo.jpg',
}), { expiresIn: 3600 });
```

```
S3 Storage Classes:
• Standard:          Hot data, truy cập thường xuyên
• Intelligent-Tier:  Auto-move between tiers
• Standard-IA:       Ít truy cập, lưu lâu dài
• Glacier:           Archive, lấy mất vài phút-giờ
• Glacier Deep:      Archive, lấy mất 12-48 giờ, rẻ nhất
```

---

## 3. Lambda — Serverless Functions

```javascript
// handler.js
export const handler = async (event) => {
    const { httpMethod, path, body, queryStringParameters } = event;

    try {
        switch (`${httpMethod} ${path}`) {
            case 'GET /users':
                const users = await db.query('SELECT * FROM users LIMIT 20');
                return response(200, { data: users });

            case 'POST /users':
                const { name, email } = JSON.parse(body);
                const user = await db.query(
                    'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
                    [name, email]
                );
                return response(201, { data: user });

            default:
                return response(404, { error: 'Not Found' });
        }
    } catch (err) {
        return response(500, { error: err.message });
    }
};

function response(statusCode, body) {
    return {
        statusCode,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    };
}
```

```yaml
# SAM template (Infrastructure as Code cho Lambda)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: handler.handler
      Runtime: nodejs20.x
      MemorySize: 256
      Timeout: 30
      Events:
        GetUsers:
          Type: Api
          Properties:
            Path: /users
            Method: GET
        CreateUser:
          Type: Api
          Properties:
            Path: /users
            Method: POST
      Environment:
        Variables:
          DATABASE_URL: !Ref DatabaseUrl
```

```
Lambda pricing:
• Trả theo request + thời gian chạy
• 1M requests FREE/month
• $0.20 per 1M requests sau đó
• Cold start: 100ms-1s (lần đầu chạy)

Lambda vs EC2:
• Lambda: Event-driven, auto-scale 0→∞, < 15 min
• EC2: Long-running, persistent, full control
```

---

## 4. VPC — Networking

```
┌──────────────────── VPC (10.0.0.0/16) ─────────────────┐
│                                                          │
│  ┌──── Public Subnet ────┐  ┌──── Public Subnet ────┐  │
│  │ 10.0.1.0/24 (AZ-1a)  │  │ 10.0.2.0/24 (AZ-1b)  │  │
│  │ ┌─────┐ ┌─────┐      │  │ ┌─────┐               │  │
│  │ │ ALB │ │ NAT │      │  │ │ ALB │               │  │
│  │ └─────┘ └─────┘      │  │ └─────┘               │  │
│  └───────────────────────┘  └───────────────────────┘  │
│           ↕ Internet Gateway                            │
│  ┌── Private Subnet ────┐  ┌── Private Subnet ────┐   │
│  │ 10.0.3.0/24 (AZ-1a)  │  │ 10.0.4.0/24 (AZ-1b)  │  │
│  │ ┌─────┐ ┌─────┐      │  │ ┌─────┐ ┌─────┐      │  │
│  │ │ EC2 │ │ EC2 │      │  │ │ EC2 │ │ EC2 │      │  │
│  │ └─────┘ └─────┘      │  │ └─────┘ └─────┘      │  │
│  └───────────────────────┘  └───────────────────────┘  │
│                                                          │
│  ┌── Private Subnet (DB) ┐  ┌── Private Subnet (DB) ┐  │
│  │ 10.0.5.0/24           │  │ 10.0.6.0/24           │  │
│  │ ┌─────┐               │  │ ┌─────┐               │  │
│  │ │ RDS │ (Primary)     │  │ │ RDS │ (Standby)    │  │
│  │ └─────┘               │  │ └─────┘               │  │
│  └───────────────────────┘  └───────────────────────┘  │
└──────────────────────────────────────────────────────────┘

Rules:
• Public subnet:   Internet Gateway → public IP
• Private subnet:  NAT Gateway → outbound only
• DB subnet:       Không internet access → max security
```

---

## 5. SQS + SNS — Message Systems

```javascript
import { SQSClient, SendMessageCommand, ReceiveMessageCommand } from '@aws-sdk/client-sqs';

const sqs = new SQSClient({ region: 'ap-southeast-1' });

// Gửi message vào queue
await sqs.send(new SendMessageCommand({
    QueueUrl: 'https://sqs.ap-southeast-1.amazonaws.com/123/orders-queue',
    MessageBody: JSON.stringify({
        orderId: '12345',
        action: 'process_payment',
    }),
    MessageGroupId: 'orders',  // FIFO queue
}));

// Nhận & xử lý messages (worker)
const { Messages } = await sqs.send(new ReceiveMessageCommand({
    QueueUrl: queueUrl,
    MaxNumberOfMessages: 10,
    WaitTimeSeconds: 20,  // Long polling
}));

for (const msg of Messages || []) {
    const order = JSON.parse(msg.Body);
    await processOrder(order);
    await sqs.send(new DeleteMessageCommand({
        QueueUrl: queueUrl,
        ReceiptHandle: msg.ReceiptHandle,
    }));
}
```

```
SQS vs SNS:
SQS (Queue):    Producer → Queue → 1 Consumer
SNS (Pub/Sub):  Publisher → Topic → N Subscribers

Common pattern: SNS + SQS (fanout)
Order Created → SNS Topic ──┬──► SQS (Email service)
                              ├──► SQS (Inventory service)
                              └──► SQS (Analytics service)
```

---

## 6. Costs — Tối ưu chi phí

```
Top cost drivers:
1. EC2 instances (compute)
2. RDS databases
3. Data transfer (outbound)
4. S3 storage
5. NAT Gateway (!!! $0.045/GB)

Tips tiết kiệm:
✅ Reserved Instances cho workloads ổn định → -40-70%
✅ Spot Instances cho batch jobs → -90%
✅ Auto Scaling: scale down đêm/weekend
✅ S3 Lifecycle: auto-move old data → Glacier
✅ CloudFront: giảm origin requests + data transfer
✅ Set Budget Alerts: email khi vượt ngưỡng
❌ NAT Gateway: $0.045/GB → dùng VPC endpoints thay thế
```

---

## Bài tập thực hành

- [ ] Deploy static website lên S3 + CloudFront
- [ ] Lambda: tạo REST API xử lý form submission
- [ ] VPC: setup public + private subnet + NAT
- [ ] SQS: producer-consumer pattern cho order processing

---

## Tài nguyên thêm

- [AWS Free Tier](https://aws.amazon.com/free/) — 12 tháng miễn phí
- [AWS Well-Architected Labs](https://www.wellarchitectedlabs.com/) — Hands-on
- [AWS Skill Builder](https://skillbuilder.aws/) — Free courses
