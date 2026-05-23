# 🔬 Labs: Infrastructure Security

---

## 🔬 Lab 1: HashiCorp Vault

```bash
# Start Vault in dev mode
docker run -d --name vault \
  -p 8200:8200 \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=root' \
  hashicorp/vault

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Store secret
vault kv put secret/myapp \
  db_host=localhost \
  db_password=secret123

# Get secret
vault kv get secret/myapp
vault kv get -field=db_password secret/myapp

# Enable AppRole auth
vault auth enable approle
vault write auth/approle/role/myapp \
  secret_id_ttl=10m \
  token_num_uses=10 \
  token_ttl=20m
```

---

## 🔬 Lab 2: AWS Secrets Manager

```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{"username":"admin","password":"secret123"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database \
  --query SecretString --output text

# Rotate secret
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:xxx
```

```python
# Python SDK
import boto3
import json

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='myapp/database')
secret = json.loads(response['SecretString'])
print(secret['password'])
```

---

## 🔬 Lab 3: CIS Benchmarks

```bash
# Install Lynis
sudo apt install lynis

# Run audit
sudo lynis audit system

# Docker CIS benchmark
docker run --rm -it \
  --net host \
  --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

---

## 🔬 Lab 4: InSpec Compliance

```ruby
# controls/ssh.rb
control 'ssh-01' do
  impact 1.0
  title 'SSH root login disabled'
  
  describe sshd_config do
    its('PermitRootLogin') { should eq 'no' }
  end
end

control 'ssh-02' do
  impact 0.7
  title 'SSH password auth disabled'
  
  describe sshd_config do
    its('PasswordAuthentication') { should eq 'no' }
  end
end
```

```bash
inspec exec controls/ -t ssh://user@host
```

---

## 🔬 Lab 5: Network Security

```bash
# AWS Security Group audit
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]]'

# Find open ports
nmap -sV -p 1-65535 target_ip

# Verify SSL/TLS
openssl s_client -connect example.com:443 -tls1_2
testssl.sh example.com
```

---

## ✅ Checklist

- [ ] Lab 1: Vault
- [ ] Lab 2: AWS Secrets
- [ ] Lab 3: CIS Benchmarks
- [ ] Lab 4: InSpec
- [ ] Lab 5: Network Security

---

**[← Back to README](./README.md)**
