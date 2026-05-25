# 🎓 ConfigMaps & Secrets — Manage config + sensitive data

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [Services & Networking](02_services-and-networking.md)

> 🎯 *Master **ConfigMap** (non-sensitive config), **Secret** (passwords/keys/tokens), **3 cách inject** vào Pod (env, file mount, args), **Secret encryption at rest**, **External Secrets** (Vault/AWS Secrets Manager), **sealed-secrets** GitOps. Sau bài này manage 12-factor app config đúng cách.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết **ConfigMap** + 3 cách dùng (env var, env file, mounted file)
- [ ] Viết **Secret** + base64 encoding caveats
- [ ] Pod consume ConfigMap/Secret 3 ways
- [ ] **Hot reload** vs **restart** khi config đổi
- [ ] **Encryption at rest** cho etcd
- [ ] **External Secrets Operator** (HashiCorp Vault, AWS Secrets Manager)
- [ ] **Sealed Secrets** for GitOps (encrypt in git)
- [ ] **Image pull secret** for private registry

---

## Tình huống — Bạn hardcode DATABASE_URL trong YAML

Bạn deploy FastAPI K8s. YAML:

```yaml
spec:
  containers:
  - name: fastapi
    env:
    - name: DATABASE_URL
      value: postgresql://user:supersecret@postgres:5432/db    # ← Hardcoded!
    - name: JWT_SECRET
      value: my-jwt-key-12345                                    # ← Hardcoded!
```

→ Push to git → **password leak** to mọi developer + GitHub history.

Bạn ngơ:
- Sao **không** hardcode trong YAML?
- **ConfigMap** vs **Secret** khác sao?
- **Secret K8s base64** — secure không?
- Production: dùng **Vault** hay K8s Secret?

Senior:
> *"12-factor app: **config ngoài code**. K8s tách: ConfigMap (non-sensitive), Secret (sensitive). Plus encryption at rest cho etcd. Production: External Secret từ Vault/AWS — vault encrypt + audit + rotate."*

→ Bài này dạy đầy đủ.

---

## 1️⃣ ConfigMap — Non-sensitive config

ConfigMap là K8s object lưu **config plain text** — URL, port, log level, feature flag. KHÔNG dùng cho password/key (đó là vai trò Secret). YAML structure đơn giản: key-value trong field `data`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "INFO"
  API_TIMEOUT: "30"
  FEATURE_FLAGS: "feature_a,feature_b"
  app.conf: |
    [database]
    pool_size = 10
    [cache]
    ttl = 300
```

→ `data` = key-value pairs. Values **plain text**. **KHÔNG cho secrets** (password, keys).

### Use cases

ConfigMap được tạo ra cho 4 loại config phổ biến nhất — tách biệt code khỏi config theo 12-Factor App principle:

- Environment-specific URLs (dev/staging/prod).
- Feature flags.
- Application config files (nginx.conf, app.conf).
- Log levels.

### Create from CLI

Ngoài viết YAML, có thể tạo ConfigMap trực tiếp từ CLI với **4 nguồn input** — literal value, file, env file, directory. Tiện cho dev nhanh:

```bash
# From literal
kubectl create configmap app-config \
  --from-literal=LOG_LEVEL=INFO \
  --from-literal=API_TIMEOUT=30

# From file
kubectl create configmap app-config --from-file=app.conf

# From env file
kubectl create configmap app-config --from-env-file=.env.production

# From directory (each file → key)
kubectl create configmap app-config --from-file=./config/
```

→ Verify: `kubectl get configmap app-config -o yaml`.

---

## 2️⃣ Secret — Sensitive data

Secret giống ConfigMap nhưng cho data **nhạy cảm** (password, API key, JWT secret). Value bắt buộc encode base64. K8s ETCD lưu Secret riêng + RBAC chặt chẽ hơn ConfigMap:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque                          # Default — arbitrary data
data:
  DATABASE_PASSWORD: c3VwZXJzZWNyZXQ=    # base64("supersecret")
  JWT_SECRET: bXktand0LWtleS0xMjM0NQ==     # base64("my-jwt-key-12345")
```

### Base64 — NOT encryption!

**Pitfall #1** của K8s Secret: base64 KHÔNG phải encryption — chỉ là encoding để safe-transport binary data. Anyone có quyền `kubectl get secret` đều decode được. Để encrypt thực sự cần Vault/Sealed Secrets:

```bash
echo -n "supersecret" | base64
# c3VwZXJzZWNyZXQ=

echo "c3VwZXJzZWNyZXQ=" | base64 -d
# supersecret
```

→ **Base64 = encoding, không phải encryption**. K8s use base64 cho transport (binary-safe). Anyone with `get secret` permission đọc được.

### `stringData` — Skip base64 manual

```yaml
apiVersion: v1
kind: Secret
metadata: { name: app-secrets }
type: Opaque
stringData:
  DATABASE_PASSWORD: supersecret         # K8s auto base64
  JWT_SECRET: my-jwt-key-12345
```

→ Easier viết. K8s convert sang base64 lúc save.

### Create from CLI

```bash
# Literal
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_PASSWORD=supersecret \
  --from-literal=JWT_SECRET=mykey

# From file
kubectl create secret generic ssh-key --from-file=id_rsa=/path/to/id_rsa

# From env file (recommended)
kubectl create secret generic app-secrets --from-env-file=.env.prod
```

### Secret types

| Type | Use case |
|---|---|
| `Opaque` (default) | Arbitrary data |
| `kubernetes.io/tls` | TLS cert + key (Ingress) |
| `kubernetes.io/dockerconfigjson` | Private registry auth |
| `kubernetes.io/service-account-token` | Service account |
| `kubernetes.io/basic-auth` | username + password |
| `kubernetes.io/ssh-auth` | SSH key |

---

## 3️⃣ 3 cách Pod consume ConfigMap/Secret

### Way 1 — Single key as env var

```yaml
spec:
  containers:
  - name: app
    env:
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
    - name: DATABASE_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_PASSWORD
```

→ In container: `echo $LOG_LEVEL` → `INFO`.

### Way 2 — All keys as env vars (envFrom)

```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: app-config
    - secretRef:
        name: app-secrets
```

→ **Inject mọi key** thành env vars. Tiện cho config có nhiều keys.

```bash
# Container env vars:
LOG_LEVEL=INFO
API_TIMEOUT=30
DATABASE_PASSWORD=supersecret
JWT_SECRET=my-jwt-key-12345
```

### Way 3 — Mount as files (volume)

```yaml
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: config-vol
      mountPath: /etc/app
      readOnly: true
    - name: secret-vol
      mountPath: /etc/secrets
      readOnly: true

  volumes:
  - name: config-vol
    configMap:
      name: app-config
  - name: secret-vol
    secret:
      secretName: app-secrets
```

→ Container thấy:
```
/etc/app/LOG_LEVEL              (contains "INFO")
/etc/app/app.conf               (contains config content)
/etc/secrets/DATABASE_PASSWORD   (contains "supersecret")
```

### Selective mount

```yaml
volumes:
- name: config-vol
  configMap:
    name: app-config
    items:                              # Mount selective keys
    - key: app.conf
      path: nginx.conf                   # Rename when mount
    defaultMode: 0644
```

### Mount specific key as different filename

→ Useful when app expect specific config file names.

### Best practice

| Case | Choose |
|---|---|
| Few env vars (FastAPI/Node app) | **`env` + `valueFrom`** |
| Many env vars | **`envFrom`** |
| Config files (nginx.conf, app.conf) | **Volume mount** |
| Secret rotated frequently | **Volume mount** (auto-refresh ~1 min) |
| Secret in env var | Less secure (visible in `ps`) |

---

## 4️⃣ Hot reload vs restart

### Env vars — KHÔNG hot reload

```bash
# Update ConfigMap
kubectl edit configmap app-config       # Change LOG_LEVEL: DEBUG

# Pod env vars vẫn cũ — env vars set lúc Pod start
kubectl exec mypod -- env | grep LOG_LEVEL
# LOG_LEVEL=INFO     ← cũ
```

→ Env vars **immutable after Pod start**. Must **restart Pod**:
```bash
kubectl rollout restart deployment/myapp
```

### Volume mounts — Auto-refresh

```bash
# Update ConfigMap
kubectl edit configmap app-config

# Wait ~60-90s (kubelet refresh)
kubectl exec mypod -- cat /etc/app/LOG_LEVEL
# DEBUG     ← cập nhật!
```

→ **Subprocess in container** can detect file change → reload config (Nginx `reload`, app watch file).

### Trigger restart on ConfigMap change

Annotation pattern — hash of ConfigMap in Deployment:

```yaml
# Use tool like Helm/Kustomize
metadata:
  annotations:
    checksum/config: <hash-of-configmap>
```

→ ConfigMap change → hash change → Deployment template change → rolling update.

Or operator: **Reloader** (https://github.com/stakater/Reloader) auto-restart deployments when ConfigMap/Secret change.

---

## 5️⃣ Encryption at rest — etcd

By default, K8s store Secrets in **etcd plain (base64)**. Anyone access etcd = read secrets.

### Enable encryption

```yaml
# /etc/kubernetes/encryption-config.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64 32-byte key>
  - identity: {}
```

→ API server encrypt Secrets before storing etcd.

### Cloud managed

| Provider | Encryption at rest |
|---|---|
| GKE | ✅ Default (Cloud KMS) |
| EKS | Optional (configure KMS) |
| AKS | Optional |

→ Managed K8s thường default. Self-host phải config.

---

## 6️⃣ External Secrets Operator — Production way

K8s Secret in cluster = OK cho start. Production scale:
- Multi-cluster sync.
- Rotation policy.
- Audit log.
- IAM-based access.

→ **External Secret** từ **Vault / AWS Secrets Manager / GCP Secret Manager / Azure Key Vault**.

### Install External Secrets Operator

```bash
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  -n external-secrets-system --create-namespace
```

### ClusterSecretStore — Backend config

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata: { name: aws-secrets }
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        secretRef:
          accessKeyIDSecretRef: { name: aws-creds, key: access-key }
          secretAccessKeySecretRef: { name: aws-creds, key: secret-key }
```

### ExternalSecret — Define secret to fetch

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata: { name: app-secrets }
spec:
  refreshInterval: 1h
  secretStoreRef: { name: aws-secrets, kind: ClusterSecretStore }
  target:
    name: app-secrets        # K8s Secret created
  data:
  - secretKey: DATABASE_PASSWORD
    remoteRef:
      key: prod/db
      property: password
  - secretKey: JWT_SECRET
    remoteRef:
      key: prod/jwt
```

→ Operator pull from AWS Secrets Manager every 1h, create/update K8s Secret. Pod use Secret normal. **Single source of truth = AWS SM. K8s Secret = projection**.

---

## 7️⃣ Sealed Secrets — Encrypt in git

GitOps: commit YAML to git. Plain Secret in git = leak. Solution: **Sealed Secrets** (Bitnami).

```bash
# Encrypt secret with controller's public key
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_PASSWORD=supersecret \
  --dry-run=client -o yaml | kubeseal -o yaml > sealed-secret.yaml
```

```yaml
# sealed-secret.yaml — safe to commit!
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata: { name: app-secrets }
spec:
  encryptedData:
    DATABASE_PASSWORD: AgB1234...kzNlMjY     # Encrypted!
```

→ Controller in cluster decrypt (only it has private key) → create K8s Secret. Git safe.

### Vs External Secrets

| Sealed Secrets | External Secrets |
|---|---|
| Commit encrypted to git | Fetch from external vault |
| Self-contained | Need external system |
| Manual rotation | Auto-refresh |
| Good for solo / small | Good for enterprise |

---

## 8️⃣ Image pull secret — Private registry

Default Pod pull from public Docker Hub. Private registry (GHCR, ECR) cần auth.

### Create

```bash
kubectl create secret docker-registry regcred \
  --docker-server=ghcr.io \
  --docker-username=acmeshop \
  --docker-password=<github_token> \
  --docker-email=ops@acmeshop.vn
```

### Use in Pod

```yaml
spec:
  imagePullSecrets:
  - name: regcred
  containers:
  - name: app
    image: ghcr.io/acmeshop/fastapi:v1.0
```

### Or default for namespace

```yaml
apiVersion: v1
kind: ServiceAccount
metadata: { name: default }
imagePullSecrets:
- name: regcred
```

→ Mọi Pod trong namespace tự dùng regcred (no need per-Pod).

---

## 9️⃣ Hands-on — Apply config + secrets cho FastAPI

### `config.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: fastapi-config }
data:
  LOG_LEVEL: "INFO"
  CORS_ORIGINS: "https://acmeshop.vn"
  CACHE_TTL: "300"

---

apiVersion: v1
kind: Secret
metadata: { name: fastapi-secrets }
type: Opaque
stringData:
  DATABASE_URL: postgresql://user:strongpass@postgres:5432/acmeshop
  JWT_SECRET: <generated-by-openssl-rand>
  AWS_SECRET_KEY: <from-aws-iam>
```

### `deployment.yaml` (updated)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: fastapi }
spec:
  replicas: 3
  selector: { matchLabels: { app: fastapi } }
  template:
    metadata: { labels: { app: fastapi } }
    spec:
      containers:
      - name: fastapi
        image: ghcr.io/acmeshop/fastapi:v1.0
        ports: [{ containerPort: 8000 }]
        envFrom:
        - configMapRef: { name: fastapi-config }
        - secretRef: { name: fastapi-secrets }
        resources:
          requests: { memory: "256Mi", cpu: "250m" }
          limits:   { memory: "512Mi", cpu: "500m" }
        livenessProbe:
          httpGet: { path: /healthz, port: 8000 }
        readinessProbe:
          httpGet: { path: /ready, port: 8000 }
      imagePullSecrets:
      - name: ghcr-pull
```

### Deploy

```bash
# Create secrets first
kubectl create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io \
  --docker-username=acmeshop \
  --docker-password=$GHCR_TOKEN

kubectl apply -f config.yaml
kubectl apply -f deployment.yaml

# Verify env in pod
kubectl exec deploy/fastapi -- env | grep -E "LOG_|DATABASE_"
# LOG_LEVEL=INFO
# DATABASE_URL=postgresql://...
```

→ Production-ready: no secrets in git, config separated, image pull authenticated.

---

## ⚠️ 5 pitfall hay vướng

1. **Secret as env var in `ps`** → process list visible. Mount as file when sensitive (`/var/run/secrets/...`).
2. **Hardcode in YAML + commit git** → leak forever in git history. Sealed Secrets / External Secrets.
3. **Forget restart after ConfigMap update (env vars)** → Pod runs old config. `kubectl rollout restart deployment/x`.
4. **Base64 = encryption** misconception → just encoding. Real encryption: etcd-level + KMS.
5. **Mount mode 0644 secret** → other users on node can read. Use `defaultMode: 0400` for sensitive.

---

## ✅ Self-check

1. **ConfigMap** vs **Secret** — khi nào dùng cái nào?
2. Secret base64 — **encryption** không? Implication?
3. 3 cách Pod consume Secret — pros/cons?
4. ConfigMap update — env vars có **hot reload** không? Volume mount?
5. **Sealed Secrets** vs **External Secrets** — khác sao?

<details>
<summary>Gợi ý đáp án</summary>

1. **ConfigMap**: non-sensitive (LOG_LEVEL, feature flags, URLs, config files). Plain text. **Secret**: sensitive (passwords, tokens, keys, certs). Base64 + encryption at rest support. Use right type — Secret have better access control + encryption.

2. **KHÔNG**. Base64 = encoding (binary-safe transport). Anyone with `get secret` permission decode trivially. Real **encryption** = etcd encryption at rest + KMS. Plus K8s Secret = good cho intra-cluster, sensitive prod = External Secrets.

3. **`env: valueFrom`**: 1 key as env var — explicit, control names, easy debug. **`envFrom`**: all keys auto inject — concise, but no rename, prefix `prefix: APP_`. **Volume mount**: file at `/path/key` — sensitive (not in `ps`), auto-refresh, can rename. Best practice: volume mount for sensitive, envFrom for bulk config.

4. **Env vars**: NO hot reload — set at Pod start, immutable. Restart Pod (`kubectl rollout restart deployment/x`). **Volume mount**: YES auto-refresh ~60-90s. App can `inotify` watch + reload config without restart.

5. **Sealed Secrets**: encrypt cleartext → store encrypted YAML in git → controller decrypt in cluster. Self-contained, simple, good cho solo/small. **External Secrets**: fetch from external vault (Vault/AWS SM) → create K8s Secret. Better cho enterprise — central management, audit, rotation, IAM auth. Different problems both legit.
</details>

---

## ⚡ Cheatsheet

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: app-config }
data:
  KEY1: "value1"
  KEY2: "value2"
  config.yaml: |
    nested: file
```

```bash
kubectl create configmap app --from-literal=KEY=val
kubectl create configmap app --from-env-file=.env
kubectl create configmap app --from-file=config.yaml
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata: { name: app-secrets }
type: Opaque
stringData:
  KEY1: "secret-value"
```

```bash
kubectl create secret generic app --from-literal=KEY=secret
kubectl create secret docker-registry regcred \
  --docker-server=... --docker-username=... --docker-password=...
kubectl create secret tls my-tls --cert=cert.pem --key=key.pem
```

### Consume in Pod

```yaml
# Env var
env:
- name: KEY1
  valueFrom:
    configMapKeyRef: { name: app-config, key: KEY1 }
- name: PWD
  valueFrom:
    secretKeyRef: { name: app-secrets, key: PWD }

# Bulk env
envFrom:
- configMapRef: { name: app-config }
- secretRef: { name: app-secrets }

# Volume
volumeMounts:
- name: cfg
  mountPath: /etc/app
volumes:
- name: cfg
  configMap: { name: app-config }
- name: sec
  secret: { secretName: app-secrets, defaultMode: 0400 }
```

### Restart after update

```bash
kubectl rollout restart deployment/myapp
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **ConfigMap** | Non-sensitive config (key-value) |
| **Secret** | Sensitive data (base64 encoded) |
| **`Opaque`** | Default Secret type |
| **`stringData`** | Plain text input, K8s auto-base64 |
| **`envFrom`** | Inject all keys as env vars |
| **Volume mount** | Files at path (sensitive friendly) |
| **`imagePullSecret`** | Auth for private registry |
| **Encryption at rest** | Encrypt Secrets in etcd |
| **KMS** | Cloud Key Management Service |
| **External Secrets Operator** | Sync external vault → K8s Secret |
| **Sealed Secrets** | Encrypted Secret YAML in git |
| **Reloader** | Operator auto-restart on ConfigMap/Secret change |
| **Vault / AWS Secrets Manager** | External secret stores |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Services & Networking](02_services-and-networking.md)
- → Tiếp: [Namespaces & RBAC](04_namespaces-and-rbac.md)
- ↑ Cluster: [kubernetes README](../../README.md)

### Cross-reference
- [FastAPI auth + secrets](../../../../07_Web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)
- [Linux SSH keys](../../../../04_OS/linux/lessons/02_intermediate/02_ssh-deep-dive.md)

### External
- 📖 [K8s docs — ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/)
- 📖 [K8s docs — Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
- 📖 [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- 📖 [External Secrets Operator](https://external-secrets.io/)
- 📖 [Reloader](https://github.com/stakater/Reloader)
- 📖 [Vault on K8s](https://developer.hashicorp.com/vault/tutorials/kubernetes)

---

> 🎯 *Sau bài này manage config + secrets đúng cách. Bài cuối cluster dạy **Namespaces + RBAC** — multi-tenancy + permission.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước §1 ConfigMap + Use cases + Create from CLI + §2 Secret + Base64 warning.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster K8s basic lesson 4/5. Cover: ConfigMap YAML + 4 nguồn input + Use cases + Secret base64 encoding + types (Opaque, TLS, Docker, ServiceAccount) + mount as env vs volume + immutable Secret + Sealed Secrets intro.
