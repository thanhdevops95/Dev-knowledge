# Module 11: Cloud Labs

---

## 🔧 Lab 1: AWS CLI Setup

```bash
# Install
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure
aws configure

# Test
aws sts get-caller-identity
```

---

## 🔧 Lab 2: S3 Operations

```bash
# Create bucket
aws s3 mb s3://my-devops-bucket-unique-name

# Upload file
echo "Hello Cloud" > test.txt
aws s3 cp test.txt s3://my-bucket/

# List objects
aws s3 ls s3://my-bucket/

# Download
aws s3 cp s3://my-bucket/test.txt downloaded.txt

# Sync folder
aws s3 sync ./local-folder s3://my-bucket/folder/

# Delete bucket
aws s3 rb s3://my-bucket --force
```

---

## 🔧 Lab 3: EC2 Basics

```bash
# List instances
aws ec2 describe-instances

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name my-key

# Stop instance
aws ec2 stop-instances --instance-ids i-xxx

# Terminate
aws ec2 terminate-instances --instance-ids i-xxx
```

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | CLI setup |
| 2 | S3 operations |
| 3 | EC2 basics |

👉 **[SCENARIOS.md](SCENARIOS.md)**
