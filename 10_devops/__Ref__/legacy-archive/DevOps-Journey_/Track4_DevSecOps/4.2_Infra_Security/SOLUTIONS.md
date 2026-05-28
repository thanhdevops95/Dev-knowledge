# ✅ Solutions: Infrastructure Security

---

## Exercise 1: Secrets Management

```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name prod/database \
  --secret-string '{"username":"admin","password":"SuperSecret123!"}'

# Retrieve in application
import boto3
import json

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='prod/database')
    return json.loads(response['SecretString'])

# Rotate automatically
aws secretsmanager rotate-secret \
  --secret-id prod/database \
  --rotation-lambda-arn arn:aws:lambda:xxx
```

---

## Exercise 3: Network Security

```bash
# Audit open security groups
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].{GroupId:GroupId,GroupName:GroupName}'

# Enable VPC Flow Logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-xxx \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name vpc-flow-logs

# NACL for added security
aws ec2 create-network-acl-entry \
  --network-acl-id acl-xxx \
  --rule-number 100 \
  --protocol tcp \
  --port-range From=443,To=443 \
  --cidr-block 0.0.0.0/0 \
  --rule-action allow \
  --ingress
```

---

**[← Back to Exercises](./EXERCISES.md)**
