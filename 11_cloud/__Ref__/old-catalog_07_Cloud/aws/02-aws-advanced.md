# AWS Advanced — ECS, Lambda, SQS, S3, VPC

> **Tags:** `aws` `ecs` `lambda` `serverless` `sqs` `s3` `vpc` `fargate`
> **Level:** Intermediate | **Prerequisite:** `cloud/01-aws-core.md`

---

## 1. ECS & Fargate — Container Orchestration

```
EC2 Launch Type:  You manage EC2 instances (capacity planning, patching)
Fargate:          AWS manages compute. You just define containers.
EKS:              Kubernetes on AWS

Fargate = Serverless containers
  - No EC2 management
  - Pay per vCPU + memory (per second)
  - Scales to zero
  - Good for: microservices, batch jobs, async workers
```

### Task Definition
```json
{
  "family": "my-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",      "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
  "containerDefinitions": [{
    "name": "api",
    "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-api:latest",
    "portMappings": [{ "containerPort": 8080, "protocol": "tcp" }],
    "environment": [
      { "name": "NODE_ENV", "value": "production" }
    ],
    "secrets": [
      { "name": "DATABASE_URL", "valueFrom": "arn:aws:ssm:us-east-1:...:parameter/app/db_url" },
      { "name": "JWT_SECRET", "valueFrom": "arn:aws:secretsmanager:us-east-1:...:secret:app/jwt-secret" }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/my-api",
        "awslogs-region": "us-east-1",
        "awslogs-stream-prefix": "ecs"
      }
    },
    "healthCheck": {
      "command": ["CMD-SHELL", "curl -f http://localhost:8080/health || exit 1"],
      "interval": 30,
      "timeout": 5,
      "retries": 3,
      "startPeriod": 60
    }
  }]
}
```

### ECS Service with Auto-scaling
```hcl
# Terraform: ECS Service
resource "aws_ecs_service" "api" {
  name            = "my-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = module.vpc.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
  
  deployment_circuit_breaker {
    enable   = true
    rollback = true    # Auto rollback if deployment fails
  }
}

# Auto-scaling
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = 20
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.api.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  name               = "scale-on-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace
  
  target_tracking_scaling_policy_configuration {
    target_value = 60.0   # Scale to keep CPU at 60%
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

---

## 2. Lambda — Serverless Functions

```python
# Python Lambda handler
import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
sqs = boto3.client('sqs')

def handler(event, context):
    """
    event: The event data (API Gateway, SQS, S3, etc.)
    context: Lambda runtime info (remaining_time_ms, function_name, etc.)
    """
    print(f"Event: {json.dumps(event)}")
    print(f"Remaining time: {context.get_remaining_time_in_millis()}ms")
    
    # API Gateway event
    if 'httpMethod' in event:
        return handle_api_request(event)
    
    # SQS event
    if 'Records' in event and event['Records'][0].get('eventSource') == 'aws:sqs':
        return handle_sqs_messages(event['Records'])
    
    # S3 event
    if 'Records' in event and 's3' in event['Records'][0]:
        return handle_s3_event(event['Records'])

def handle_api_request(event):
    method = event['httpMethod']
    path = event['path']
    body = json.loads(event.get('body') or '{}')
    user_id = event['requestContext']['authorizer']['claims']['sub']  # From Cognito JWT
    
    if method == 'GET' and path == '/items':
        result = table.scan(Limit=50)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps(result['Items'])
        }
    
    return { 'statusCode': 404, 'body': '{"error": "Not found"}' }

def handle_sqs_messages(records):
    successes = []
    failures = []
    
    for record in records:
        try:
            body = json.loads(record['body'])
            process_message(body)
            successes.append(record['messageId'])
        except Exception as e:
            print(f"Failed to process {record['messageId']}: {e}")
            failures.append({'itemIdentifier': record['messageId']})
    
    # Return failures for retry (partial batch response)
    return {'batchItemFailures': failures}
```

### Lambda Best Practices
```python
# 1. Initialize heavy resources OUTSIDE handler (reused across invocations)
import boto3
import psycopg2

# These run once, reused in warm invocations
db_connection = None
s3_client = boto3.client('s3')    # Global = reused!

def get_db():
    global db_connection
    if db_connection is None or db_connection.closed:
        db_connection = psycopg2.connect(os.environ['DATABASE_URL'])
    return db_connection

def handler(event, context):
    db = get_db()  # Reuse existing connection
    # ...

# 2. Optimize memory (CPU scales with memory)
# 128MB → 256MB may 2x CPU → potentially faster & same cost

# 3. Use Lambda Powertools for structured logging, tracing, metrics
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.metrics import MetricUnit

logger = Logger(service="order-service")
tracer = Tracer(service="order-service")
metrics = Metrics(namespace="MyApp")

@tracer.capture_lambda_handler
@logger.inject_lambda_context
@metrics.log_metrics
def handler(event, context):
    logger.info("Processing order", order_id=event['orderId'])
    
    with tracer.capture_method("process_payment"):
        result = process_payment(event)
    
    metrics.add_metric(name="OrdersProcessed", unit=MetricUnit.Count, value=1)
    return result
```

### Lambda with Terraform
```hcl
resource "aws_lambda_function" "api" {
  function_name = "my-api"
  runtime       = "python3.12"
  handler       = "main.handler"
  role          = aws_iam_role.lambda.arn
  
  # Package (zip or ECR image)
  filename      = "lambda_package.zip"
  source_code_hash = filebase64sha256("lambda_package.zip")
  # Or ECR image:
  # package_type = "Image"
  # image_uri    = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda:latest"
  
  memory_size = 512      # MB
  timeout     = 30       # seconds
  
  environment {
    variables = {
      TABLE_NAME    = aws_dynamodb_table.items.name
      QUEUE_URL     = aws_sqs_queue.orders.url
    }
  }
  
  vpc_config {
    subnet_ids         = module.vpc.private_subnet_ids
    security_group_ids = [aws_security_group.lambda.id]
  }
  
  tracing_config { mode = "Active" }  # X-Ray tracing
}

# Trigger from SQS
resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn = aws_sqs_queue.orders.arn
  function_name    = aws_lambda_function.api.arn
  batch_size       = 10
  
  # Partial batch response
  function_response_types = ["ReportBatchItemFailures"]
  
  # Scaling concurrency
  scaling_config {
    maximum_concurrency = 100
  }
}
```

---

## 3. SQS — Message Queuing

```
Standard Queue:   At-least-once delivery, best-effort ordering
                  Up to ~120k msg/s, unlimited messages
                  
FIFO Queue:       Exactly-once processing, strict FIFO ordering
                  Up to 3,000 msg/s per API action
                  Deduplication ID prevents duplicate processing
```

### Key Concepts
```
Visibility Timeout: Time message hidden after Consumer receives it
                    Consumer must delete before timeout or message reappears
                    Set to max processing time + buffer (e.g., 5min for 3min job)

Dead-Letter Queue:  After N failed attempts, message moves to DLQ
                    Inspect failed messages, fix code, redrive

Message Retention:  Default 4 days, max 14 days

Delay Queue:        Delay delivery of new messages (0s to 15min default)

Long Polling:       Wait up to 20s for messages (reduces empty API calls)
```

### Python SQS Worker
```python
import boto3
import json
import time
import signal
from contextlib import contextmanager

sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

class Worker:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGTERM, self._handle_shutdown)
        signal.signal(signal.SIGINT, self._handle_shutdown)
    
    def _handle_shutdown(self, *args):
        print("Shutdown signal received...")
        self.running = False
    
    def run(self):
        print("Worker started")
        while self.running:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,     # Batch up to 10
                WaitTimeSeconds=20,          # Long polling
                VisibilityTimeout=300,       # 5 minute processing window
                MessageAttributeNames=['All'],
            )
            
            messages = response.get('Messages', [])
            if not messages:
                continue
            
            for msg in messages:
                success = self.process_message(msg)
                if success:
                    self.delete_message(msg)
                # If failed, message becomes visible again after timeout
    
    def process_message(self, msg) -> bool:
        try:
            body = json.loads(msg['Body'])
            message_type = msg.get('MessageAttributes', {}).get('type', {}).get('StringValue')
            
            match message_type:
                case 'order.created':
                    handle_new_order(body)
                case 'payment.processed':
                    handle_payment(body)
                case _:
                    print(f"Unknown message type: {message_type}")
            
            return True
        except Exception as e:
            print(f"Error processing message: {e}")
            return False  # Message will be retried
    
    def delete_message(self, msg):
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg['ReceiptHandle']
        )

# Terraform: SQS with DLQ
resource "aws_sqs_queue" "orders" {
  name                       = "orders"
  visibility_timeout_seconds = 300
  message_retention_seconds  = 86400  # 1 day
  
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 3   # Move to DLQ after 3 failures
  })
}

resource "aws_sqs_queue" "orders_dlq" {
  name                      = "orders-dlq"
  message_retention_seconds = 1209600  # 14 days
}
```

---

## 4. S3 — Object Storage

```python
import boto3
from botocore.config import Config

s3 = boto3.client('s3', config=Config(
    retries={'mode': 'adaptive', 'max_attempts': 3}
))

# Upload
s3.upload_fileobj(
    file_obj,
    'my-bucket',
    'uploads/profile/user123.jpg',
    ExtraArgs={
        'ContentType': 'image/jpeg',
        'CacheControl': 'max-age=31536000',
        'ServerSideEncryption': 'AES256',
        'Tagging': 'user_id=123&content_type=profile_photo',
    }
)

# Presigned URLs (client-side upload directly to S3)
def create_presigned_upload_url(key: str, content_type: str, expiry: int = 3600) -> str:
    return s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': 'my-bucket',
            'Key': key,
            'ContentType': content_type,
        },
        ExpiresIn=expiry
    )

def create_presigned_download_url(key: str, expiry: int = 3600) -> str:
    return s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': 'my-bucket',
            'Key': key,
        },
        ExpiresIn=expiry
    )

# API handler
async def get_upload_url(user_id: str, filename: str):
    key = f"uploads/{user_id}/{uuid4()}/{filename}"
    url = create_presigned_upload_url(key, 'image/jpeg')
    return { "uploadUrl": url, "key": key }

# Multipart upload for large files
def upload_large_file(filepath: str, bucket: str, key: str):
    config = boto3.s3.transfer.TransferConfig(
        multipart_threshold=1024 * 25,   # 25MB threshold
        max_concurrency=10,
        multipart_chunksize=1024 * 25,
        use_threads=True
    )
    s3.upload_file(filepath, bucket, key, Config=config)
```

### S3 Event Notifications
```hcl
# Trigger Lambda on S3 upload
resource "aws_s3_bucket_notification" "uploads" {
  bucket = aws_s3_bucket.uploads.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.process_upload.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "uploads/"
    filter_suffix       = ".jpg"
  }
}

resource "aws_lambda_permission" "s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_upload.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.uploads.arn
}
```

---

## 5. VPC — Networking

```
┌─────────────────────────── VPC (10.0.0.0/16) ──────────────────────────┐
│                                                                          │
│  ┌──────────────────────────── Public Subnets ─────────────────────┐    │
│  │  10.0.1.0/24 (us-east-1a)   10.0.2.0/24 (us-east-1b)           │    │
│  │  ALB, NAT Gateway, Bastion                                       │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                          │ ↑ Internet Gateway                            │
│                          │                                               │
│  ┌──────────────────────── Private Subnets ────────────────────────┐    │
│  │  10.0.10.0/24 (us-east-1a)  10.0.11.0/24 (us-east-1b)          │    │
│  │  ECS Tasks, Lambda, EC2 apps                                     │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                          │ NAT Gateway (for outbound internet)           │
│  ┌──────────────────────── Data Subnets ──────────────────────────┐     │
│  │  10.0.20.0/24 (us-east-1a)  10.0.21.0/24 (us-east-1b)         │     │
│  │  RDS, ElastiCache, no internet access                           │     │
│  └─────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────┘
```

```hcl
# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "production"
  cidr = "10.0.0.0/16"
  
  azs              = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets  = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
  public_subnets   = ["10.0.1.0/24",  "10.0.2.0/24",  "10.0.3.0/24"]
  database_subnets = ["10.0.20.0/24", "10.0.21.0/24", "10.0.22.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = false   # One per AZ for HA
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  # VPC Flow Logs
  enable_flow_log                = true
  flow_log_destination_type      = "cloud-watch-logs"
  create_flow_log_cloudwatch_log_group = true
}
```

### Security Groups
```hcl
# ALB security group
resource "aws_security_group" "alb" {
  vpc_id = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP from internet"
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }
  
  egress { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}

# Application security group
resource "aws_security_group" "app" {
  vpc_id = module.vpc.vpc_id
  
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]  # Only from ALB!
    description     = "App port from ALB"
  }
  
  egress { from_port = 0; to_port = 0; protocol = "-1"; cidr_blocks = ["0.0.0.0/0"] }
}

# Database security group
resource "aws_security_group" "db" {
  vpc_id = module.vpc.vpc_id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]  # Only from app!
    description     = "PostgreSQL from app"
  }
}
```

---

## 6. IAM Best Practices

```hcl
# Minimal IAM role for ECS task
resource "aws_iam_role" "ecs_task" {
  name = "ecs-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "ecs_task" {
  name = "ecs-task-policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      # Only the S3 bucket it needs
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject"]
        Resource = ["${aws_s3_bucket.uploads.arn}/*"]
      },
      # Only the SQS queue it needs
      {
        Effect = "Allow"
        Action = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage"]
        Resource = [aws_sqs_queue.orders.arn]
      },
      # Read SSM params with specific prefix only
      {
        Effect = "Allow"
        Action = ["ssm:GetParameter", "ssm:GetParameters"]
        Resource = ["arn:aws:ssm:*:*:parameter/app/prod/*"]
      }
    ]
  })
}

# OIDC for GitHub Actions (no static credentials!)
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_actions" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Federated = aws_iam_openid_connect_provider.github.arn }
      Action = "sts:AssumeRoleWithWebIdentity"
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          "token.actions.githubusercontent.com:sub" = "repo:myorg/myrepo:ref:refs/heads/main"
        }
      }
    }]
  })
}
```

---

*Tài liệu liên quan: `cloud/01-aws-core.md` | `iac/02-terraform-advanced.md` | `kubernetes/01-kubernetes.md`*
