# 🎓 Secret management — Vault + External Secrets Operator + 12-factor

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [02_supply-chain-security.md](02_supply-chain-security.md), [K8s basic ConfigMap+Secret](../../../kubernetes/lessons/01_basic/03_configmaps-and-secrets.md)

> 🎯 *Secret trong K8s default base64 (không phải encryption). Production cần: external store (Vault/AWS SM), auto sync vào cluster, rotation, audit. Bài này dạy stack: **HashiCorp Vault + External Secrets Operator + Sealed Secrets + SOPS**. Apply 12-factor App principle #3.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **12-factor App #3** (config in environment, not code)
- [ ] So sánh **5 secret store options** 2026 (Vault, AWS SM, GCP SM, Azure KV, Doppler)
- [ ] Setup **HashiCorp Vault** + KV engine + auth methods
- [ ] Install **External Secrets Operator (ESO)** + sync Vault → K8s Secret
- [ ] Dùng **Sealed Secrets** + **SOPS** cho GitOps-friendly secret commit
- [ ] **Dynamic credentials** — Vault tạo Postgres role mỗi giờ
- [ ] **Secret rotation** workflow + audit
- [ ] Pre-commit hooks **gitleaks** chặn secret leak

---

## Tình huống — Secret leak vào public repo

Friday 5pm, dev commit `database.env` accident:
```bash
# database.env
DATABASE_URL=postgres://acme:SuperSecret123@db.acmeshop.vn/prod
STRIPE_SECRET_KEY=sk_live_abc123def456...
AWS_ACCESS_KEY_ID=AKIA1234567890ABCDEF
AWS_SECRET_ACCESS_KEY=very-secret-key-here
```

Repo public on GitHub. 30 phút sau:
- Bot scraper detect AWS key → bitcoin miner launched.
- Stripe key → fraudulent charges $20,000 in 2 hours.
- DB password → attacker `pg_dump` user table.

Damage: $25,000 + customer trust loss + week of incident response.

Post-mortem:
- **Root cause #1**: secret in Git is **forever**. Even `git rm` + `git push` doesn't help — history immutable. Need `git filter-repo` rewrite + force push (still cached on GitHub).
- **Root cause #2**: No pre-commit hook to detect.
- **Root cause #3**: No external secret manager. Dev pasted directly into file.

Sếp: *"Tuần này setup: Vault + ESO + pre-commit gitleaks. Cấm secret in Git, hết. Bài này dạy."*

---

## 1️⃣ 12-Factor App #3 — Store config in environment

[The Twelve-Factor App](https://12factor.net/) — Heroku's principles (2011, still relevant 2026).

### Factor 3 — Config

> *Store **config (especially secrets) in the environment**, NOT in code.*

Reasons:
- Code = OSS (or shareable); config = sensitive.
- Different environments (dev/staging/prod) = different config, same code.
- Rotate secret without redeploy code.

### Anti-patterns

❌ Commit `.env` to Git:
```bash
echo "API_KEY=xxx" > .env
git add .env && git commit
```

❌ Hardcode in Dockerfile:
```dockerfile
ENV API_KEY=xxx
```

❌ Build args (leaks to layer history):
```dockerfile
ARG API_KEY
ENV API_KEY=$API_KEY
```

❌ K8s Secret without encryption-at-rest:
```bash
kubectl create secret generic mysec --from-literal=key=xxx
# Base64-encoded, NOT encrypted
```

### Right pattern

✅ Config from environment at runtime:
```python
# Python
import os
api_key = os.environ['API_KEY']
```

```go
// Go
apiKey := os.Getenv("API_KEY")
```

Environment populated from:
- External secret store (Vault/AWS SM/GCP SM/Azure KV).
- Sync to K8s Secret via ESO.
- Mount K8s Secret as env var or file.

🪞 **Ẩn dụ**: *Config in code như **mật khẩu vào USB cắm vĩnh viễn**. 12-factor như **vault có quyền access** — code không biết mật khẩu, chỉ "lấy mật khẩu mỗi lần khởi động".*

---

## 2️⃣ Secret store options 2026

8 tool secret management chính 2026 — chia 3 nhóm: self-host (Vault, Infisical OSS), cloud-native (AWS SM, GCP SM, Azure KV), multi-cloud SaaS (Doppler, 1Password). Cost + features khác nhau lớn:

| Tool | Type | Strengths | Cost |
|---|---|---|---|
| **HashiCorp Vault** | Self-host / Cloud | Dynamic credentials, transit encryption, multi-cloud, audit | OSS free; HCP from $0.50/hour |
| **AWS Secrets Manager** | SaaS (AWS) | IAM integration, auto-rotation (Postgres/MySQL native) | $0.40/secret/month + $0.05/10k API calls |
| **AWS Systems Manager Parameter Store** | SaaS (AWS) | Free standard, hierarchical paths | Free (standard); $0.05/secure-string-month (advanced) |
| **GCP Secret Manager** | SaaS (GCP) | IAM integration, versioning | $0.06/secret/month |
| **Azure Key Vault** | SaaS (Azure) | HSM-backed, multi-tenant | $0.03/10k transactions |
| **Doppler** | SaaS multi-cloud | Best DX (dev-friendly UI), sync to anywhere | $5/user/month + |
| **Infisical** | OSS / SaaS | Open source alternative to Doppler | Free OSS; $5/user/month cloud |
| **1Password Secrets Automation** | SaaS | Familiar password manager UX | $20/user/month + |

### Comparison matrix

So sánh 4 tool đầu bảng theo 8 trục — multi-cloud, dynamic creds, K8s integration, audit, self-host, compliance. Vault thắng feature; cloud-native thắng UX/cost cho single-cloud:

| Feature | Vault | AWS SM | GCP SM | Doppler |
|---|---|---|---|---|
| Multi-cloud | ✅ | AWS only | GCP only | ✅ |
| Dynamic credentials | ✅ (DB, AWS IAM, etc.) | ✅ (limited DB) | ❌ | ❌ |
| Transit encryption-as-a-service | ✅ | ❌ | ❌ | ❌ |
| K8s integration | ESO / Agent injector | ESO / IRSA | ESO / Workload Identity | ESO / SDK |
| Audit log | ✅ comprehensive | CloudTrail | Audit log | UI |
| Self-host option | ✅ free | ❌ | ❌ | ✅ free (OSS) |
| Compliance ready | SOC2, FIPS 140-2 | SOC2, HIPAA | SOC2, HIPAA | SOC2 |
| Learning curve | Steep | Easy | Easy | Easy |

→ **Recommend 2026**:
- **Startup small**: AWS Secrets Manager (AWS-only) or Doppler (multi-cloud, dev-friendly).
- **Mid-size**: Vault HCP (managed) or self-host.
- **Enterprise / multi-cloud**: Vault self-host with HA + audit pipeline.

---

## 3️⃣ HashiCorp Vault setup

### Vault concepts

Vault gồm **3 layer chính** — Auth methods (identity verification), Secret engines (KV/Database/PKI/Transit), Policies (HCL access rules). Diagram architecture:

```mermaid
graph TB
    Vault[Vault Server]
    Auth[Auth methods]
    KV[KV Engine]
    DB[Database Engine]
    PKI[PKI Engine]
    Transit[Transit Engine]
    Policy[Policies]
    
    User[User/App] -->|authenticate| Auth
    Auth --> Vault
    Vault --> KV
    Vault --> DB
    Vault --> PKI
    Vault --> Transit
    Policy --> Auth
```

**Concepts**:
- **Auth methods**: how clients prove identity (Kubernetes ServiceAccount, OIDC, AppRole, AWS IAM, ...).
- **Secret engines**: backend storing/generating secrets:
  - **KV** (key-value): static secrets.
  - **Database**: dynamic credentials (Postgres role auto-generated).
  - **PKI**: issue X.509 certificates.
  - **Transit**: encryption-as-a-service (encrypt without storing).
- **Policies**: HCL — control what auth identity can access.

### Install (dev mode)

Vault dev mode: in-memory, single replica — chỉ dùng để **học/test** (NOT production!). Production cần HA setup với storage backend (Consul/Raft) + unseal keys + audit log:

```bash
# macOS
brew install vault

# Run dev server (in-memory, single replica — NOT for prod!)
vault server -dev -dev-root-token-id=devroot

# In another terminal
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='devroot'

vault status
# Key             Value
# Seal Type       shamir
# Initialized     true
# Sealed          false
# ...
```

### KV engine — Static secret

KV engine (Key-Value v2) là engine cơ bản nhất — lưu **static secrets** (DB password, API key, JWT secret). Support versioning + soft delete. Workflow: enable engine → put/get/list:

```bash
# Enable KV v2
vault secrets enable -path=secret -version=2 kv

# Write secret
vault kv put secret/myapp/prod \
  database_url='postgres://...' \
  api_key='sk_live_...'

# Read
vault kv get secret/myapp/prod

# List
vault kv list secret/myapp
```

### Production install (Helm in K8s)

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set server.ha.enabled=true \
  --set server.ha.replicas=3 \
  --set server.ha.raft.enabled=true \
  --set ui.enabled=true \
  --set server.dataStorage.size=10Gi
```

Initialize:
```bash
# Init (only first time)
kubectl exec -n vault vault-0 -- vault operator init \
  -key-shares=5 \
  -key-threshold=3 \
  > vault-keys.txt
# !!! SAVE vault-keys.txt SAFELY !!! 5 keys, need 3 to unseal

# Unseal each replica
kubectl exec -n vault vault-0 -- vault operator unseal <key1>
kubectl exec -n vault vault-0 -- vault operator unseal <key2>
kubectl exec -n vault vault-0 -- vault operator unseal <key3>
# Repeat for vault-1, vault-2
```

→ Vault sealed after restart → must unseal manually unless **auto-unseal** (AWS KMS, GCP KMS, Azure Key Vault).

### Auth method: Kubernetes ServiceAccount

```bash
# Enable
vault auth enable kubernetes

# Configure
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443"

# Create policy
vault policy write myapp-policy - <<EOF
path "secret/data/myapp/prod" {
  capabilities = ["read"]
}
EOF

# Create role
vault write auth/kubernetes/role/myapp-role \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=production \
  policies=myapp-policy \
  ttl=1h
```

→ K8s ServiceAccount `myapp-sa` in namespace `production` can authenticate to Vault, read `secret/myapp/prod`.

---

## 4️⃣ External Secrets Operator (ESO)

### Concept

```mermaid
graph LR
    Vault[Vault] -->|read API| ESO[External Secrets Operator]
    ESO -->|create| K8sSecret[K8s Secret]
    K8sSecret -->|env/volume| Pod[Pod]
    
    ESO -.->|refresh every N| Vault
```

ESO watches `ExternalSecret` CRD → pull from secret store → create K8s Secret. Refresh periodically.

### Install

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace
```

### SecretStore — Define backend

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "http://vault.vault.svc:8200"
      path: "secret"        # KV engine mount path
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp-role"
          serviceAccountRef:
            name: myapp-sa
```

### ExternalSecret — Sync rule

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secret
  namespace: production
spec:
  refreshInterval: 1h         # re-sync every hour
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-secret         # K8s Secret name to create
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        DATABASE_URL: "{{ .database_url }}"
        API_KEY: "{{ .api_key }}"
  data:
    - secretKey: database_url
      remoteRef:
        key: myapp/prod
        property: database_url
    - secretKey: api_key
      remoteRef:
        key: myapp/prod
        property: api_key
```

Apply:
```bash
kubectl apply -f externalsecret.yaml

# Check generated Secret
kubectl get secret myapp-secret -n production -o yaml
# data:
#   DATABASE_URL: <base64>
#   API_KEY: <base64>
```

Pod consume:
```yaml
spec:
  containers:
    - name: app
      envFrom:
        - secretRef:
            name: myapp-secret
```

### ClusterSecretStore — Shared backend

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: vault-global
spec:
  provider:
    vault:
      server: "http://vault.vault.svc:8200"
      ...
```

→ `ClusterSecretStore` cross-namespace. `ExternalSecret` reference cluster-scoped store.

### Refresh on Vault update

ESO poll Vault every `refreshInterval`. To trigger immediate refresh:
```bash
kubectl annotate externalsecret myapp-secret \
  force-sync=$(date +%s) \
  -n production
```

---

## 5️⃣ Dynamic credentials — Vault Database Engine

### Use case

Static DB password: 1 password forever → if leaked, attacker access until rotate.

Dynamic: Vault generates **temporary Postgres user** with TTL (1 hour) → leak = 1h damage window.

### Setup Postgres database engine

```bash
# Enable
vault secrets enable database

# Configure connection
vault write database/config/postgres-prod \
  plugin_name=postgresql-database-plugin \
  allowed_roles=myapp-role \
  connection_url="postgresql://{{username}}:{{password}}@postgres.production.svc:5432/myapp?sslmode=require" \
  username="vault-admin" \
  password="vault-admin-password"

# Create role
vault write database/roles/myapp-role \
  db_name=postgres-prod \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
                       GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"
```

### Get dynamic credential

```bash
vault read database/creds/myapp-role
# Key                Value
# ---                -----
# lease_id           database/creds/myapp-role/abc123
# lease_duration     1h
# lease_renewable    true
# password           random-generated-password
# username           v-token-myapp-AbCdEf123-1234567890
```

→ Postgres user `v-token-myapp-AbCdEf123-1234567890` valid 1 hour. After expire, Vault revoke user.

### ESO with dynamic credential

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: postgres-credentials
spec:
  refreshInterval: 30m         # Refresh before 1h TTL expires
  secretStoreRef:
    name: vault-backend
  target:
    name: postgres-credentials
  dataFrom:
    - extract:
        key: database/creds/myapp-role    # Dynamic endpoint
        decodingStrategy: None
```

→ ESO call `database/creds/myapp-role` → Vault generate fresh user → K8s Secret update → Pod restart pick new credentials. Old user auto-revoked after TTL.

### Auto-rotation workflow

```mermaid
sequenceDiagram
    ESO->>Vault: Read database/creds/myapp-role
    Vault->>Postgres: CREATE USER v-token-xxx
    Vault-->>ESO: username + password (1h TTL)
    ESO->>K8s: Update Secret
    K8s-->>Pod: Trigger reload (if app supports)
    
    Note over Pod: Use credentials for 30min
    
    ESO->>Vault: Refresh credentials
    Vault->>Postgres: CREATE USER v-token-yyy
    Vault-->>ESO: New credentials
    ESO->>K8s: Update Secret
    
    Note over Vault,Postgres: After 1h, v-token-xxx auto-revoked
```

→ No human ever sees or types Postgres password. Rotation transparent.

---

## 6️⃣ Sealed Secrets — GitOps-friendly secret in Git

### Vấn đề

GitOps: everything in Git. But secret? Plain Secret base64 → leak if Git public.

### Sealed Secrets (Bitnami)

Encrypt K8s Secret with **cluster's public key** → only **specific cluster** can decrypt → safe to commit Git.

### Install

```bash
helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system
```

### Encrypt secret

```bash
# Install kubeseal CLI
brew install kubeseal

# Create regular Secret
kubectl create secret generic mysecret \
  --from-literal=password=supersecret \
  --dry-run=client \
  -o yaml > secret.yaml

# Encrypt
kubeseal --controller-namespace=kube-system \
  --controller-name=sealed-secrets \
  -f secret.yaml \
  -o yaml > sealedsecret.yaml
```

Resulting `sealedsecret.yaml`:
```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: production
spec:
  encryptedData:
    password: AgB7g8s...encrypted-blob...
```

→ Commit `sealedsecret.yaml` to Git safely. No one (except cluster) can decrypt.

### Apply

```bash
kubectl apply -f sealedsecret.yaml

# SealedSecret controller decrypt → creates regular Secret
kubectl get secret mysecret -n production
```

### Limitations

- **Cluster-specific**: SealedSecret encrypted for **cluster A** can't decrypt at cluster B. Multi-cluster: encrypt N times.
- **Key rotation pain**: rotate cluster key → re-encrypt all SealedSecrets.
- **Less suited for dynamic credentials**: static encrypted value.

### When use Sealed Secrets vs ESO

| Scenario | Sealed Secrets | ESO + Vault |
|---|---|---|
| Static config (API key, DB URL) | ✅ Simple | ✅ |
| Dynamic credential (rotating DB user) | ❌ | ✅ |
| Multi-cluster | ❌ Encrypt N times | ✅ Sync everywhere |
| Audit trail | Limited | ✅ Comprehensive |
| Self-host operator complexity | Simple | Vault is complex |
| Cost | Free | Vault HCP $$ or self-host |

→ **Recommend**: ESO + Vault for production. Sealed Secrets for small team or as backup encryption layer.

---

## 7️⃣ SOPS — File-level encryption

### Concept

**SOPS** (Mozilla) = encrypt **values** trong YAML/JSON file (keys plain). Encryption với cloud KMS (AWS KMS, GCP KMS, Azure KV, PGP).

### Install

```bash
brew install sops
```

### Encrypt file

```yaml
# secrets.yaml (plain)
database_url: postgres://acme:supersecret@db.acmeshop.vn/prod
api_key: sk_live_abc123
```

```bash
# Encrypt with AWS KMS
sops --encrypt \
  --kms 'arn:aws:kms:us-east-1:123:key/abc' \
  secrets.yaml > secrets.enc.yaml

# Decrypt
sops --decrypt secrets.enc.yaml
```

Result `secrets.enc.yaml`:
```yaml
database_url: ENC[AES256_GCM,data:abc...,iv:def...,tag:ghi...]
api_key: ENC[AES256_GCM,data:jkl...,iv:mno...,tag:pqr...]
sops:
  kms:
    - arn: arn:aws:kms:...
      created_at: 2026-05-24T10:00:00Z
```

→ Keys (`database_url`, `api_key`) plaintext, values encrypted. Safe to commit.

### With ArgoCD via Helm Secrets plugin

```yaml
# Application
spec:
  source:
    repoURL: https://github.com/acme/gitops-config
    path: charts/myapp
    plugin:
      name: helm-secrets
      env:
        - name: HELM_SECRETS_BACKEND
          value: sops
```

→ ArgoCD render Helm chart, SOPS decrypt values inline.

### When SOPS vs Sealed Secrets vs ESO

| Aspect | SOPS | Sealed Secrets | ESO |
|---|---|---|---|
| Encrypts | Values in file | Whole Secret | Nothing in Git (external store) |
| Decryption | CLI tool with KMS key | Controller in cluster | Operator pulls from external |
| Multi-cluster | KMS key shared | Cluster-specific key | Backend is shared |
| Rotation | Re-encrypt files | Re-encrypt + re-deploy | Backend rotates, ESO syncs |
| Audit | KMS access log | Limited | Vault/SM extensive log |
| Best for | Helm chart with secret values | Simple K8s Secret in Git | Production scale |

→ Hybrid common: SOPS for Helm values commit Git, ESO for runtime sensitive (DB credentials).

---

## 8️⃣ Pre-commit hook — Prevent secret leak

### gitleaks — Open source secret scanner

```bash
# Install
brew install gitleaks
```

### Pre-commit setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.20.0
    hooks:
      - id: gitleaks
```

```bash
# Install pre-commit framework
brew install pre-commit
pre-commit install
```

→ Every `git commit` runs gitleaks scan. Detects AWS keys, GitHub tokens, Stripe keys, SSH keys, etc.

### Bypass option (rare)

```bash
git commit --no-verify -m "skip hook"
```

→ Should be banned by team policy. Audit if used.

### CI scan

```yaml
# .github/workflows/security.yml
- uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

### Backup: TruffleHog

```bash
trufflehog git https://github.com/acme/repo --since-commit HEAD~10
```

→ Different detection rules. Run both for higher coverage.

---

## 9️⃣ Hands-on: Setup ESO + Vault end-to-end

### Step 1: Install Vault

```bash
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set server.dev.enabled=true   # dev mode for hands-on
```

### Step 2: Configure Vault KV + Kubernetes auth

```bash
kubectl exec -it -n vault vault-0 -- /bin/sh

# Inside Vault pod
vault login token=root
vault secrets enable -path=secret kv-v2
vault kv put secret/fastapi/prod \
  database_url='postgres://acme:supersecret@postgres.production.svc:5432/acme' \
  api_key='sk_live_xxx'

# Enable Kubernetes auth
vault auth enable kubernetes
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443"

# Policy
vault policy write fastapi-policy - <<EOF
path "secret/data/fastapi/prod" {
  capabilities = ["read"]
}
EOF

# Role
vault write auth/kubernetes/role/fastapi-role \
  bound_service_account_names=fastapi-sa \
  bound_service_account_namespaces=production \
  policies=fastapi-policy \
  ttl=24h
```

### Step 3: Install ESO

```bash
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace
```

### Step 4: ServiceAccount + SecretStore

```yaml
# fastapi-sa.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: fastapi-sa
  namespace: production
---
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: production
spec:
  provider:
    vault:
      server: "http://vault.vault.svc:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "fastapi-role"
          serviceAccountRef:
            name: fastapi-sa
```

```bash
kubectl apply -f fastapi-sa.yaml
```

### Step 5: ExternalSecret

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: fastapi-secret
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: fastapi-secret
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: fastapi/prod
        property: database_url
    - secretKey: API_KEY
      remoteRef:
        key: fastapi/prod
        property: api_key
```

```bash
kubectl apply -f externalsecret.yaml

# Verify
kubectl get externalsecret -n production
kubectl get secret fastapi-secret -n production -o yaml | yq '.data'
```

### Step 6: Use in Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: fastapi-sa
      containers:
        - name: fastapi
          image: ghcr.io/acme/fastapi:v1.2.3
          envFrom:
            - secretRef:
                name: fastapi-secret
```

→ Pod read env from K8s Secret. Behind scenes: ESO sync from Vault every hour. Vault is source of truth.

### Step 7: Test rotation

```bash
# Update value in Vault
kubectl exec -it -n vault vault-0 -- vault kv put secret/fastapi/prod \
  database_url='postgres://acme:new-password-rotated@postgres:5432/acme' \
  api_key='sk_live_new'

# Force sync (or wait refreshInterval)
kubectl annotate externalsecret fastapi-secret force-sync=$(date +%s) -n production

# Check Secret updated
kubectl get secret fastapi-secret -n production -o yaml | yq '.data.DATABASE_URL' | base64 -d
# postgres://acme:new-password-rotated@...

# Restart pods to pick up (or use reloader)
kubectl rollout restart deployment/fastapi -n production
```

### Step 8: Stimulus reloader (auto restart on secret change)

```bash
# Install Stakater Reloader
helm install reloader stakater/reloader -n kube-system
```

```yaml
# Deployment add annotation
metadata:
  annotations:
    reloader.stakater.com/auto: "true"
```

→ Reloader watch Secret. Update → trigger rolling restart Deployment using that Secret. **Zero manual restart**.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Vault unsealed key in repo

→ Vault initial 5 keys + root token. If commit to Git = game over. Anyone unseal Vault, read all secrets.

→ **Fix**:
- Auto-unseal with cloud KMS (AWS KMS / GCP KMS / Azure KV / Transit unseal).
- Shamir keys distributed to **5 different people**, threshold 3 → no single person can unseal.
- Document Disaster Recovery procedure offline (encrypted USB in safe).

### ❌ Cạm bẫy: ExternalSecret refresh too aggressive

```yaml
refreshInterval: 10s   # ← every 10 seconds!
```

→ ESO hammer Vault API → rate limit or load. Vault audit log explode.

→ **Fix**: `refreshInterval: 1h` minimum. For dynamic credential closer to TTL (e.g., 30m for 1h TTL).

### ❌ Cạm bẫy: Sealed Secret key rotation forgotten

→ Cluster compromise — must rotate Sealed Secret encryption key. But forgot to **re-encrypt** existing SealedSecrets → next deploy fail.

→ **Fix**: 
- Document rotation procedure.
- Automate re-encryption (kubeseal --recovery-private-key + re-encrypt).
- Test rotation in staging quarterly.

### ❌ Cạm bẫy: ESO refresh fail silently

→ Vault network down → ESO can't refresh → K8s Secret stale → app keeps using old credentials. Eventually Vault rotates dynamic credential → app auth fail.

→ **Fix**:
- ESO Prometheus metrics: `external_secrets_sync_calls_total` + `external_secrets_provider_api_calls_error_total`.
- Alert if errors > threshold.
- Health check on K8s Secret freshness (annotation timestamp).

### ❌ Cạm bẫy: Hardcoded service account credentials in Vault

→ Anti-pattern: store AWS IAM access key in Vault → used by app. Now AWS key is in 2 places (AWS + Vault). Rotation = update both.

→ **Fix**: Use Vault's **AWS Secret Engine** — Vault assumes role on demand, generates short-lived AWS credentials. Or use **IRSA** (IAM Roles for Service Accounts) — no Vault needed for AWS access.

### ❌ Cạm bẫy: Audit log not centralized

→ Vault audit log in Vault server only. Lost when Vault recreate.

→ **Fix**: Vault audit device → syslog → Loki/CloudWatch/Splunk. Retain 90+ days.

```bash
vault audit enable file file_path=/vault/logs/audit.log
vault audit enable syslog tag="vault" facility="AUTH"
```

### ❌ Cạm bẫy: ESO ServiceAccount permissions too broad

```yaml
# Policy giving full access
path "secret/*" { capabilities = ["read", "write", "delete"] }
```

→ Compromised pod → full Vault access.

→ **Fix**: Least privilege. ESO read-only specific paths:
```hcl
path "secret/data/fastapi/prod" { capabilities = ["read"] }
```

### ✅ Best practice: Workload Identity > static credentials

- AWS: **IRSA** (IAM Roles for Service Accounts) — pod assume IAM role via OIDC.
- GCP: **Workload Identity** — same concept.
- Azure: **Workload Identity** — same.

→ No static credential in cluster. Pod identity = K8s ServiceAccount → cloud IAM role. Short-lived tokens auto-rotated.

### ✅ Best practice: Tier secrets

| Tier | Type | Storage | Rotation |
|---|---|---|---|
| Tier 0 — Disaster recovery | Vault root token, KMS master key | Offline (USB safe) | Manual, rare |
| Tier 1 — Infrastructure | DB admin pass, cluster CA | Vault | Quarterly |
| Tier 2 — App | API keys, DB user pass | Vault → ESO → K8s Secret | Monthly (or dynamic) |
| Tier 3 — User session | JWT signing key, session token | Vault Transit (encrypt without storing) | Rolling |

### ✅ Best practice: Audit + alert on access pattern

```promql
# Anomalous Vault read (PromQL)
rate(vault_secret_kv_read_total[5m]) > 10 * avg_over_time(rate(vault_secret_kv_read_total[5m])[1h:5m])
```

→ Sudden spike in secret reads → maybe attacker exfiltrating. Alert SOC.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** K8s Secret default — vì sao không an toàn?

<details>
<summary>💡 Đáp án</summary>

K8s Secret defaults:
1. **Base64 encoded, NOT encrypted**. `echo "data" | base64 -d` decode trivial.
2. **Stored in etcd plain text** (unless encryption-at-rest configured).
3. **Anyone with `get secrets` permission can read** — RBAC defaults loose.
4. **Pod env vars in process memory** + `/proc/PID/environ` readable by node-local processes.
5. **No audit log per secret access** (need separate logging).

**Make it production**:
1. **Encryption-at-rest in etcd**: K8s API server flag `--encryption-provider-config` with AES-CBC + KMS provider (cloud KMS).
2. **External secret store** (Vault/AWS SM) — K8s Secret only **cache** of external truth.
3. **RBAC strict** — only specific ServiceAccount can read specific Secret.
4. **Audit log** — log all `get secrets` events to SIEM.
5. **No env vars** — mount as file (`subPath`) so secret not in env memory.

→ **K8s Secret = transport mechanism**, not security boundary. Real security upstream (Vault/SM) + downstream (RBAC + encryption at rest).
</details>

**Q2.** Vault dynamic credentials — TTL trade-offs?

<details>
<summary>💡 Đáp án</summary>

**Short TTL** (e.g., 15 minutes):
- ✅ Smaller damage window if leaked.
- ✅ Forces rotation discipline.
- ❌ More API calls (Vault + Postgres) — load.
- ❌ App must handle re-fetch credentials (connection pool drain).

**bạn TTL** (e.g., 24 hours):
- ✅ Less API load.
- ✅ Simpler app logic (refresh less often).
- ❌ Longer damage window.
- ❌ Postgres has many concurrent users (one per refresh) — bloat `pg_roles`.

**Recommended**:
- **Production DB**: 1-2 hour TTL.
- **Highly sensitive (PII access)**: 15 min TTL + audit trail.
- **Dev/test**: 24h OK.
- **Long-running connections** (data pipeline): max_ttl 24h, default 1h, ESO renew before expiry.

**Renewal vs new lease**:
- ESO refreshes lease (renew) — same credentials, extend TTL.
- After max_ttl reached, must get new lease (new credentials) — pod needs new env, restart required.

→ Balance security (short TTL) vs operational (long TTL). Start 1h + adjust based on incident frequency.
</details>

**Q3.** Sealed Secrets vs ESO — multi-cluster?

<details>
<summary>💡 Đáp án</summary>

**Sealed Secrets multi-cluster**:
- Encryption with cluster-specific public key.
- Cluster A's SealedSecret can't decrypt at Cluster B.
- Options:
  1. **Encrypt N times** (once per cluster) — N SealedSecret files in Git. Maintenance burden.
  2. **Shared private key** across clusters — defeats purpose (one compromise = all).
  3. **Sealed Secret Bridge** (community tool) — limited adoption.

→ Sealed Secrets best for single-cluster.

**ESO multi-cluster**:
- Vault as **central** secret store.
- ESO in each cluster pulls from Vault.
- 1 secret in Vault → N clusters automatically have it.
- Cross-cluster secret rotation: change in Vault, ESO syncs everywhere within `refreshInterval`.

→ ESO scales better for multi-cluster/multi-cloud.

**Hybrid**:
- ESO for runtime secrets (dynamic, multi-cluster).
- Sealed Secrets for bootstrap secrets (e.g., Vault root token recovery).

**Production multi-cluster recommendation**: ESO + Vault (or cloud SM). Sealed Secrets supplementary for specific use cases.
</details>

**Q4.** Pre-commit hook bypass với `--no-verify` — chấp nhận được không?

<details>
<summary>💡 Đáp án</summary>

**Technically possible**: `git commit --no-verify -m "..."` bypasses pre-commit hooks.

**Should not be accepted** for production repo:

1. **Pre-commit hooks are last line defense client-side**. Bypass = secret could slip into history (forever, even after delete).
2. **Server-side enforcement needed**:
   - **GitHub branch protection**: Required status checks include CI security scan.
   - **CI scans on every push**: gitleaks-action runs server-side, blocks merge if secret found.
   - **Pre-receive hook** (self-hosted Git): reject push if secret detected.

3. **Audit `--no-verify` usage**:
   - Pre-commit hook itself can log commits bypassed (write to local file).
   - Team policy: bypass requires Slack note + manager approval.

**Acceptable bypass cases**:
- Detected file is **false positive** (e.g., test fixture mock key starting with "AKIA" — clearly fake).
- Emergency commit with known clean diff (rare).

**Recommended setup**:
1. Pre-commit hook (gitleaks) — fast feedback.
2. CI scan (gitleaks-action + TruffleHog) — server-side enforcement.
3. Branch protection — required CI status check.
4. Secret scanning at **GitHub repo level** (free for OSS, paid for private).
5. Auto-revoke detected token (Github partner program with AWS/Slack/etc).

→ Defense in depth. Pre-commit alone is insufficient.
</details>

**Q5.** Workload Identity (IRSA) vs Vault for AWS cred — pick which?

<details>
<summary>💡 Đáp án</summary>

**IRSA (IAM Roles for Service Accounts)**:
- AWS-native. K8s ServiceAccount maps to IAM role via OIDC.
- AWS SDK in pod auto-fetch short-lived credentials (15-60min).
- Zero secret in cluster.
- No external system (just AWS).

**Vault AWS Secret Engine**:
- Vault assumes IAM role on behalf of app, returns credentials.
- Extra layer: app calls Vault, Vault calls AWS STS.
- Audit log in Vault.
- Multi-cloud support (Vault GCP, Azure engines too).

**Pick IRSA when**:
- AWS-only stack.
- Want simplest setup (no Vault to maintain).
- Trust AWS audit (CloudTrail).

**Pick Vault when**:
- Multi-cloud (need same pattern AWS + GCP + Azure).
- Need centralized audit log across clouds.
- Already using Vault for other secrets.
- Need fine-grained: same K8s pod might need 5 different IAM roles for different operations.

**Real-world**: 
- Small AWS startup → IRSA.
- Multi-cloud enterprise → Vault for secret consistency.
- Hybrid: IRSA for cloud creds, Vault for app-level secrets (DB, API keys).

→ Right answer depends on **what you're securing** + **what cloud(s) you're on**. Not one-size-fits-all.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

```bash
# === Vault ===
vault status
vault login token=<token>
vault kv put secret/<path> key=value
vault kv get secret/<path>
vault kv list secret/
vault read database/creds/<role>      # dynamic credential
vault audit list
vault policy list

# === ESO ===
kubectl get externalsecret -A
kubectl get secretstore -A
kubectl get clustersecretstore
kubectl describe externalsecret <name>
kubectl annotate externalsecret <name> force-sync=$(date +%s)

# === Sealed Secrets ===
kubeseal --controller-namespace=kube-system --controller-name=sealed-secrets -f secret.yaml -o yaml > sealedsecret.yaml
kubectl get sealedsecret -A

# === SOPS ===
sops --encrypt --kms <arn> file.yaml > file.enc.yaml
sops --decrypt file.enc.yaml
sops file.enc.yaml                    # interactive edit

# === Gitleaks ===
gitleaks detect --source . --verbose
gitleaks protect --source . --verbose

# === TruffleHog ===
trufflehog git https://github.com/acme/repo
trufflehog filesystem .

# === Reloader (auto restart on Secret change) ===
# Add to Deployment:
# annotations:
#   reloader.stakater.com/auto: "true"
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Term | Vietnamese / Explanation |
|---|---|
| **12-Factor App** | Heroku's principles for modern apps (factor 3: config in env) |
| **Secret store** | Centralized backend for credentials (Vault/AWS SM/GCP SM/...) |
| **HashiCorp Vault** | Multi-cloud secret management, dynamic credentials, transit encryption |
| **External Secrets Operator (ESO)** | CNCF Operator sync secret stores → K8s Secret |
| **SecretStore / ClusterSecretStore** | ESO CRD define backend config |
| **ExternalSecret** | ESO CRD define sync rule |
| **Dynamic credential** | Vault generates short-lived credential on-demand (DB role, AWS STS) |
| **Vault Transit engine** | Encryption-as-a-service (encrypt without storing) |
| **Vault Database engine** | Generate dynamic DB credentials (Postgres/MySQL/Mongo/...) |
| **Vault PKI engine** | Issue X.509 certificates |
| **Sealed Secrets** | Bitnami tool encrypt K8s Secret with cluster key (safe for Git) |
| **SOPS** | Mozilla file-level encryption (YAML/JSON) with cloud KMS |
| **gitleaks** | OSS secret scanner pre-commit + CI |
| **TruffleHog** | Alternative secret scanner (different detection rules) |
| **IRSA** | IAM Roles for Service Accounts (AWS — pod assume IAM via OIDC) |
| **Workload Identity** | GCP/Azure equivalent of IRSA |
| **Pre-commit framework** | Hook orchestrator for git pre-commit checks |
| **Reloader** | Stakater controller auto-restart Deployment on Secret/CM change |
| **Vault unseal** | Initial decrypt of Vault master key (Shamir secret sharing) |
| **Auto-unseal** | Vault unseal via cloud KMS (AWS KMS/GCP KMS/Azure KV) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Supply chain security — SLSA Level 3 pipeline + admission verify](02_supply-chain-security.md)
- ➡️ **Bài tiếp theo:** [Progressive Delivery — Argo Rollouts canary + Feature flags](04_progressive-delivery.md) *(sắp viết)*
- ↑ **Về cụm:** [CI/CD README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- ☸️ [K8s basic ConfigMap+Secret](../../../kubernetes/lessons/01_basic/03_configmaps-and-secrets.md) — K8s Secret foundation
- ☸️ [K8s intermediate Autoscaling+Operators](../../../kubernetes/lessons/02_intermediate/04_autoscaling-and-operators.md) — ESO is Operator pattern
- 🐳 [Docker intermediate BuildKit](../../../docker/lessons/02_intermediate/01_buildkit-and-multistage-advanced.md) — secret mount build-time

### 🌐 Tài nguyên tham khảo khác
- 📖 [12-Factor App](https://12factor.net/) — original principles
- 📖 [HashiCorp Vault docs](https://www.vaultproject.io/docs)
- 📖 [External Secrets Operator](https://external-secrets.io/)
- 📖 [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- 📖 [SOPS](https://github.com/getsops/sops)
- 📖 [gitleaks](https://github.com/gitleaks/gitleaks)
- 📖 [TruffleHog](https://github.com/trufflesecurity/trufflehog)
- 📖 [Stakater Reloader](https://github.com/stakater/Reloader)
- 📖 [IRSA AWS docs](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html)
- 📖 [pre-commit framework](https://pre-commit.com/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 03 intermediate. 12-Factor App #3 + secret store landscape 2026 + Vault deep (KV/DB/Transit engines, K8s auth) + ESO sync workflow + Sealed Secrets vs SOPS vs ESO comparison + dynamic credentials + pre-commit gitleaks + Reloader auto-restart. Apply insight `__Ref__/` (12-factor violations). 7 pitfall + 3 best practice + 5 self-check + cheatsheet.
- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §2 Secret store options + Comparison matrix + §3 Vault concepts + Install dev mode + KV engine.
