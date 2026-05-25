# 🎓 StatefulSet & Storage — Postgres trong K8s, không mất data

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** [02_ingress-cert-manager-tls.md](02_ingress-cert-manager-tls.md), [K8s basic ConfigMap+Secret](../01_basic/03_configmaps-and-secrets.md)

> 🎯 *Deployment design cho **stateless** — Postgres/Redis/Kafka cần stable identity + persistent storage + ordered start = **StatefulSet**. Bài này dạy StatefulSet vs Deployment, PV/PVC/StorageClass, dynamic provisioning EBS/Longhorn, deploy Postgres 3-replica, backup/restore với VolumeSnapshot.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **StatefulSet vs Deployment** — khi nào dùng cái nào
- [ ] Hiểu **PV / PVC / StorageClass** + **CSI driver**
- [ ] **Dynamic provisioning** với AWS EBS, GCP PD, Longhorn (on-prem)
- [ ] Deploy **Postgres 3-replica** với StatefulSet + headless Service
- [ ] **VolumeSnapshot** — backup + restore PV
- [ ] **Resize PVC** khi đầy storage
- [ ] Debug: PVC stuck `Pending`, Pod stuck `ContainerCreating`, data loss scenario

---

## Tình huống — Postgres deploy bằng Deployment, restart mất data

Bạn deploy Postgres trong K8s lần đầu:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  template:
    spec:
      containers:
        - name: postgres
          image: postgres:16
          env:
            - name: POSTGRES_PASSWORD
              value: secret
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
      volumes:
        - name: data
          emptyDir: {}     # ← AI! ephemeral
```

Insert 1000 user, test app hoạt động. Sếp đi qua: *"Restart deployment test xem still works không?"*

```bash
kubectl rollout restart deployment/postgres
```

5 phút sau:
```sql
SELECT count(*) FROM users;
-- 0
```

🔥 **Mất sạch data**. Pod restart → `emptyDir` reset → Postgres start fresh.

Bạn thử `hostPath` volume:
```yaml
volumes:
  - name: data
    hostPath:
      path: /mnt/postgres
```

OK trên kind/single node, lên cluster 5 node → Postgres reschedule node khác → vẫn mất.

Bạn add 2 replica:
```yaml
replicas: 3
```

→ 3 pod chạy parallel, race condition trên cùng data → corruption.

Sếp: *"Stateful workload **không dùng Deployment**. Dùng **StatefulSet** + **PVC**. Bài học đầu tiên SRE."*

→ Bài này dạy.

---

## 1️⃣ StatefulSet vs Deployment — Vì sao khác

### Deployment design

Deployment giả định **mọi Pod đều bình đẳng** — không pod nào "đặc biệt" hơn pod khác. K8s tạo song song, kill ngẫu nhiên, hostname random. Triết lý này tuyệt vời cho stateless workload (web, API) nhưng phá hỏng database vì DB cần identity ổn định:

- **Stateless**: bất kỳ pod nào thay thế pod khác — replica 1 = replica 2.
- **Random hostname**: `myapp-deployment-7d8b9c4f-abc12`, `myapp-deployment-7d8b9c4f-xyz98`.
- **Parallel start/stop**: K8s tạo 3 pod cùng lúc.
- **Same storage** (nếu mount PVC shared) hoặc empty.

→ Tốt cho FastAPI, web app, worker.

### StatefulSet design

StatefulSet lật ngược giả định trên: mỗi Pod là **một thực thể riêng biệt** có hostname cố định, PVC riêng, thứ tự khởi động/tắt được kiểm soát. Pod `postgres-0` luôn là chính nó, không bao giờ "trở thành" `postgres-1`. Đây là điều DB cluster cần để bầu primary, replicate, recover:

- **Stateful**: pod 0 ≠ pod 1 ≠ pod 2 (data riêng, role riêng).
- **Stable hostname**: `postgres-0`, `postgres-1`, `postgres-2` (predictable).
- **Ordered start/stop**: pod 0 start trước, pod 1 chờ pod 0 ready, pod 2 chờ pod 1.
- **Per-pod PVC**: mỗi pod claim PVC riêng (`data-postgres-0`, `data-postgres-1`, ...).
- **Headless Service** required: DNS `postgres-0.postgres.namespace.svc.cluster.local`.

→ Tốt cho: Postgres, MySQL, MongoDB, Redis Sentinel, Kafka, Elasticsearch, Zookeeper.

### Bảng so sánh

Tóm gọn 8 điểm khác biệt cốt lõi giữa 2 controller. Mỗi dòng phản ánh 1 quyết định thiết kế: hostname, startup order, network identity, storage, scaling strategy. Chọn sai controller = workload không chạy đúng (DB không cluster được, app không tìm thấy nhau):

| Aspect | Deployment | StatefulSet |
|---|---|---|
| Pod hostname | Random | Stable (`name-N`) |
| Pod startup | Parallel | Sequential (0 → 1 → 2) |
| Pod shutdown | Parallel | Reverse (2 → 1 → 0) |
| Network ID | Service LB | Headless Service DNS per pod |
| Storage | Shared PVC hoặc emptyDir | `volumeClaimTemplate` → per-pod PVC |
| Use case | Stateless app | Stateful clusters |
| Scaling | `kubectl scale` instant | Ordered, slower |
| Update strategy | RollingUpdate (parallel) | RollingUpdate (sequential), OnDelete |

### Headless Service — DNS per pod

Service thông thường có ClusterIP (load-balance request giữa các Pod) — không cho phép gọi đích danh Pod nào. **Headless Service** (`clusterIP: None`) bỏ load-balance, thay vào đó tạo 1 DNS record cho **từng Pod**. Đây là điều kiện bắt buộc để StatefulSet hoạt động:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None              # ← key: makes it headless
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
```

→ DNS records:
- `postgres-0.postgres.production.svc.cluster.local` → IP pod 0
- `postgres-1.postgres.production.svc.cluster.local` → IP pod 1
- `postgres-2.postgres.production.svc.cluster.local` → IP pod 2

App connect specific pod (primary vs replica) bằng DNS này.

🪞 **Ẩn dụ**: *Deployment như **shift công nhân thay phiên** — ai cũng giống ai, manager chỉ đếm "có 5 người". StatefulSet như **bảng phân ca y tế** — mỗi y tá phụ trách phòng cố định (phòng 1, phòng 2, phòng 3), không thể swap vì data bệnh nhân gắn với phòng cụ thể (PVC riêng cho từng pod).*

---

## 2️⃣ PV / PVC / StorageClass — Storage abstraction

### Concepts

K8s tách storage thành 4 lớp abstraction để cho phép app yêu cầu storage mà không cần biết backend là EBS, GCP PD hay NFS. Admin quản hạ tầng (StorageClass + CSI), developer chỉ khai báo "cần 100Gi SSD" (PVC). Hiểu rõ 4 khái niệm dưới đây là điều kiện làm việc với DB trên K8s:

- **PersistentVolume (PV)**: cluster resource — 1 disk thực (EBS volume, GCP PD, NFS, Ceph block).
- **PersistentVolumeClaim (PVC)**: namespace resource — request storage.
- **StorageClass**: template "loại disk" — defines provisioner + parameters.
- **CSI driver** (Container Storage Interface): plugin storage backend (EBS CSI, GCP PD CSI, Longhorn CSI).

### Static vs Dynamic provisioning

**Static**: Admin create PV manually, user PVC bind PV.
```yaml
# Admin
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-postgres-0
spec:
  capacity:
    storage: 100Gi
  accessModes: [ReadWriteOnce]
  awsElasticBlockStore:
    volumeID: vol-0a1b2c3d4    # Pre-created EBS
    fsType: ext4
---
# User
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-postgres
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

❌ Tệ — Admin manual mỗi PVC. Không scale.

**Dynamic** (2026 default): PVC reference StorageClass → CSI driver auto-create PV.
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-postgres-0
spec:
  storageClassName: gp3-encrypted    # ← reference StorageClass
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

→ CSI driver tạo EBS volume + PV + bind PVC. 100% auto.

### StorageClass examples

**AWS EBS gp3**:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3-encrypted
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
  encrypted: "true"
  fsType: ext4
reclaimPolicy: Retain          # ← keep PV when PVC deleted
volumeBindingMode: WaitForFirstConsumer    # delay bind until pod scheduled
allowVolumeExpansion: true     # can resize PVC
```

**GCP PD**:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pd-ssd
provisioner: pd.csi.storage.gke.io
parameters:
  type: pd-ssd
  replication-type: regional-pd   # auto-replicate cross-zone
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

**Longhorn (on-prem, OSS)**:
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: longhorn
provisioner: driver.longhorn.io
parameters:
  numberOfReplicas: "3"            # 3 replica per volume
  staleReplicaTimeout: "30"
  fromBackup: ""
reclaimPolicy: Delete
volumeBindingMode: Immediate
allowVolumeExpansion: true
```

### Access modes

| Mode | Mô tả | Khi dùng |
|---|---|---|
| `ReadWriteOnce` (RWO) | 1 node mount RW | Block storage (EBS, GCP PD). Default cho database |
| `ReadWriteOncePod` (RWOP) | 1 POD mount RW | K8s 1.27+, stricter than RWO |
| `ReadOnlyMany` (ROX) | Nhiều node mount RO | Distribute config, static asset |
| `ReadWriteMany` (RWX) | Nhiều node mount RW | Shared filesystem (NFS, CephFS, EFS) |

→ **EBS/PD = RWO only**. RWX cần NFS/EFS/CephFS/Longhorn (slower nhưng share được).

### reclaimPolicy

| Policy | Khi PVC delete |
|---|---|
| `Delete` (default cloud) | PV + underlying storage **deleted forever** |
| `Retain` | PV stays as `Released`, data preserved. Admin manually cleanup/reuse |

→ **Production database**: ALWAYS `Retain`. Delete PVC accident = không mất data.

### `volumeBindingMode`

| Mode | Khi nào bind PV với PVC |
|---|---|
| `Immediate` | Ngay khi PVC create |
| `WaitForFirstConsumer` | Wait until Pod schedule, bind PV ở **same AZ** với pod |

→ Multi-AZ cluster: dùng `WaitForFirstConsumer` để tránh PV ở `us-east-1a` nhưng pod schedule `us-east-1b` → mount fail (EBS region-bound).

---

## 3️⃣ StatefulSet anatomy

### Full example — Postgres 3 replica

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres                # ← reference headless Service
  replicas: 3
  
  podManagementPolicy: OrderedReady    # default — sequential start
  # OR: Parallel (start all at once, lose ordering)
  
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      partition: 0                     # 0 = update all; N = update [N, replicas-1]
  
  selector:
    matchLabels:
      app: postgres
  
  template:
    metadata:
      labels:
        app: postgres
    spec:
      terminationGracePeriodSeconds: 30
      containers:
        - name: postgres
          image: postgres:16
          ports:
            - containerPort: 5432
              name: postgres
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - name: data                # ← from volumeClaimTemplates
              mountPath: /var/lib/postgresql/data
          livenessProbe:
            exec:
              command: [pg_isready, -U, postgres]
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command: [pg_isready, -U, postgres]
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            limits:
              cpu: 2
              memory: 4Gi
            requests:
              cpu: 500m
              memory: 1Gi
  
  volumeClaimTemplates:                 # ← magic — per pod PVC
    - metadata:
        name: data
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: gp3-encrypted
        resources:
          requests:
            storage: 100Gi
```

### Resulting resources

After apply:
```bash
kubectl get sts,pvc,pod -n production
# NAME                          READY   AGE
# statefulset.apps/postgres     3/3     5m

# NAME                                   STATUS   VOLUME      CAPACITY
# persistentvolumeclaim/data-postgres-0  Bound    pvc-aaaa    100Gi
# persistentvolumeclaim/data-postgres-1  Bound    pvc-bbbb    100Gi
# persistentvolumeclaim/data-postgres-2  Bound    pvc-cccc    100Gi

# NAME             READY   STATUS    AGE
# pod/postgres-0   1/1     Running   5m
# pod/postgres-1   1/1     Running   4m
# pod/postgres-2   1/1     Running   3m
```

### Key behaviors

- **Pod startup order**: `postgres-0` start first, wait Ready → `postgres-1` start → wait Ready → `postgres-2`.
- **Pod restart**: nếu `postgres-1` chết, K8s recreate `postgres-1` **same name + same PVC**. Data preserved.
- **Scale down**: từ 3 → 1 thì K8s xoá `postgres-2` → `postgres-1`. PVC ở lại (theo `persistentVolumeClaimRetentionPolicy`).
- **Scale up**: từ 1 → 3, K8s tạo `postgres-1` rồi `postgres-2`, mỗi cái claim PVC mới.

### `persistentVolumeClaimRetentionPolicy` (K8s 1.27+)

```yaml
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain     # Keep PVC khi StatefulSet xoá
    whenScaled: Retain      # Keep PVC khi scale down
```

→ Default Retain — safe cho database. Dev/test có thể Delete để cleanup.

---

## 4️⃣ Hands-on: Deploy Postgres 3-replica với primary-replica

### Step 1: StorageClass (assume EBS CSI installed)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3-postgres
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  encrypted: "true"
reclaimPolicy: Retain
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### Step 2: Secret

```bash
kubectl create secret generic postgres-secret \
  --from-literal=password=$(openssl rand -base64 32) \
  -n production
```

### Step 3: Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: production
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
    - port: 5432
      name: postgres
---
# Regular Service for client connect (load balance read replicas)
apiVersion: v1
kind: Service
metadata:
  name: postgres-read
  namespace: production
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      name: postgres
```

### Step 4: ConfigMap (Postgres config + init script)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: postgres-config
  namespace: production
data:
  postgresql.conf: |
    listen_addresses = '*'
    max_connections = 100
    shared_buffers = 256MB
    effective_cache_size = 1GB
    wal_level = replica
    hot_standby = on
    max_wal_senders = 10
    
  init.sh: |
    #!/bin/bash
    set -e
    
    if [[ "$HOSTNAME" == "postgres-0" ]]; then
      # Primary
      echo "host replication replicator 10.0.0.0/8 md5" >> /var/lib/postgresql/data/pgdata/pg_hba.conf
      psql -c "CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'repl_pass'"
    else
      # Replica
      pg_basebackup -h postgres-0.postgres -D /var/lib/postgresql/data/pgdata -U replicator -X stream
    fi
```

(Simplified — production dùng Postgres Operator hoặc patroni cho HA proper)

### Step 5: StatefulSet (Postgres official, simplified)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
        - name: postgres
          image: postgres:16
          ports: [{ containerPort: 5432 }]
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef: { name: postgres-secret, key: password }
            - name: PGDATA
              value: /var/lib/postgresql/data/pgdata
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
            - name: config
              mountPath: /etc/postgresql
      volumes:
        - name: config
          configMap:
            name: postgres-config
  volumeClaimTemplates:
    - metadata: { name: data }
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: gp3-postgres
        resources: { requests: { storage: 100Gi } }
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Retain
```

Apply:
```bash
kubectl apply -f postgres.yaml -n production

# Watch start order
kubectl get pods -n production -l app=postgres -w
# postgres-0   0/1 ContainerCreating
# postgres-0   1/1 Running
# postgres-1   0/1 Pending          (waiting postgres-0 Ready)
# postgres-1   1/1 Running
# postgres-2   0/1 Pending
# postgres-2   1/1 Running
```

### Step 6: Test data persistence

```bash
# Connect to postgres-0 (primary)
kubectl exec -it postgres-0 -n production -- psql -U postgres

# Inside psql:
CREATE TABLE users (id SERIAL, name TEXT);
INSERT INTO users (name) SELECT 'user-' || g FROM generate_series(1,1000) g;
SELECT count(*) FROM users;
-- 1000

\q
```

Delete pod:
```bash
kubectl delete pod postgres-0 -n production

# Watch
kubectl get pods -n production -l app=postgres -w
# postgres-0   0/1 ContainerCreating    ← recreated (same name)
# postgres-0   1/1 Running              ← back online

# Re-check data
kubectl exec -it postgres-0 -n production -- psql -U postgres -c "SELECT count(*) FROM users;"
# count
# -------
#  1000          ← data preserved!
```

→ **StatefulSet + PVC = data persistent across pod restart**.

---

## 5️⃣ VolumeSnapshot — Backup + Restore

### Setup snapshot class

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: ebs-snapshot
driver: ebs.csi.aws.com
deletionPolicy: Retain
parameters:
  encrypted: "true"
```

### Create snapshot

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: postgres-0-snap-20260524
  namespace: production
spec:
  volumeSnapshotClassName: ebs-snapshot
  source:
    persistentVolumeClaimName: data-postgres-0
```

```bash
kubectl apply -f snapshot.yaml

# Wait until ReadyToUse
kubectl get volumesnapshot -n production
# NAME                          READYTOUSE  SOURCEPVC          AGE
# postgres-0-snap-20260524      true        data-postgres-0    2m
```

→ EBS snapshot created in AWS. Cost storage thấp (incremental).

### Restore from snapshot

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-postgres-restored
  namespace: production
spec:
  storageClassName: gp3-postgres
  dataSource:
    name: postgres-0-snap-20260524    # ← restore source
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

→ Mount PVC này vào pod mới → data từ snapshot.

### Automated backup with CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: production
spec:
  schedule: "0 2 * * *"          # daily at 2am
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: postgres-backup-sa
          restartPolicy: OnFailure
          containers:
            - name: backup
              image: bitnami/kubectl:latest
              command:
                - /bin/sh
                - -c
                - |
                  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
                  cat <<EOF | kubectl apply -f -
                  apiVersion: snapshot.storage.k8s.io/v1
                  kind: VolumeSnapshot
                  metadata:
                    name: postgres-0-snap-$TIMESTAMP
                    namespace: production
                  spec:
                    volumeSnapshotClassName: ebs-snapshot
                    source:
                      persistentVolumeClaimName: data-postgres-0
                  EOF
                  
                  # Cleanup snapshot >7 days old
                  kubectl get volumesnapshot -n production \
                    -o jsonpath='{range .items[?(@.metadata.creationTimestamp < "'$(date -d '7 days ago' -Iseconds)'")]}{.metadata.name}{"\n"}{end}' \
                    | xargs -r kubectl delete volumesnapshot -n production
```

→ Daily snapshot, keep 7 days. Production-grade backup.

---

## 6️⃣ Resize PVC khi đầy

### Pre-condition

- StorageClass có `allowVolumeExpansion: true`.
- CSI driver hỗ trợ resize (EBS, GCP PD, Longhorn yes).

### Resize

```bash
# Edit PVC, tăng size
kubectl edit pvc data-postgres-0 -n production
```

```yaml
spec:
  resources:
    requests:
      storage: 200Gi    # was 100Gi
```

→ CSI driver:
1. Resize underlying EBS volume (online — no downtime).
2. Notify pod: filesystem expansion needed.
3. K8s expand filesystem (online if CSI supports, hoặc restart pod).

```bash
# Verify
kubectl get pvc data-postgres-0 -n production
# NAME              STATUS   CAPACITY
# data-postgres-0   Bound    200Gi

kubectl exec postgres-0 -- df -h /var/lib/postgresql/data
# /dev/nvme1n1      200G   50G  150G  25% /var/lib/postgresql/data
```

⚠️ AWS EBS chỉ resize **lên** được, không shrink. GCP PD cũng vậy. Plan storage carefully.

---

## 7️⃣ When NOT use StatefulSet — Operator pattern preview

StatefulSet là building block, nhưng setup database production cần:
- Primary-replica replication.
- Auto failover.
- Backup automation.
- Connection pooling.
- Monitor specific metrics.

→ Viết hết bằng YAML = 500+ dòng + custom controller logic.

**Solution**: Database **Operator**.

### Postgres Operator examples

- **Zalando Postgres Operator** — Patroni-based HA.
- **CloudNativePG (CNCF)** — Postgres-native, no Patroni dependency.
- **Crunchy PGO** — commercial + OSS.

```yaml
# CloudNativePG cluster
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: acme-pg
spec:
  instances: 3
  primaryUpdateStrategy: unsupervised
  
  bootstrap:
    initdb:
      database: acme
      owner: acme
      secret:
        name: acme-pg-credentials
  
  storage:
    storageClass: gp3-encrypted
    size: 100Gi
  
  monitoring:
    enablePodMonitor: true
  
  backup:
    barmanObjectStore:
      destinationPath: s3://acme-backups/pg/
      s3Credentials:
        accessKeyId: { name: aws-creds, key: ACCESS_KEY_ID }
        secretAccessKey: { name: aws-creds, key: SECRET_ACCESS_KEY }
    retentionPolicy: "30d"
```

→ **8 dòng spec** → Operator tạo: 3-node Postgres cluster với automatic failover, point-in-time recovery, monitoring, S3 backup.

→ Bài 04 deep Operator pattern + Postgres Operator example.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Multi-AZ cluster + StorageClass `volumeBindingMode: Immediate`

→ PVC bind PV ở AZ-a, pod scheduled AZ-b → mount fail `volume node affinity conflict`.

→ **Fix**:
```yaml
volumeBindingMode: WaitForFirstConsumer
```
PV chỉ create sau khi pod schedule, ở same AZ.

### ❌ Pitfall: Delete StatefulSet → PVC gone (K8s <1.27)

K8s pre-1.27 default policy: delete StatefulSet → PVC orphan (vẫn ở) NHƯNG nếu user xoá PVC cũng = mất data.

→ **Fix K8s 1.27+**:
```yaml
persistentVolumeClaimRetentionPolicy:
  whenDeleted: Retain
  whenScaled: Retain
```

Cộng thêm `reclaimPolicy: Retain` ở StorageClass.

### ❌ Pitfall: Scale up StatefulSet bị stuck

→ `postgres-1` waiting `postgres-0` Ready, nhưng `postgres-0` không Ready (vì init script lỗi, healthcheck fail).

→ **Fix**: Check pod 0 logs:
```bash
kubectl logs postgres-0 -n production
kubectl describe pod postgres-0 -n production
```

Fix root cause → pod 0 Ready → pod 1, 2 sẽ start.

### ❌ Pitfall: `reclaimPolicy: Delete` + PVC accidentally deleted

```bash
kubectl delete pvc data-postgres-0 -n production
# → Delete + PV deleted + EBS volume deleted in AWS
# → DATA GONE FOREVER
```

→ **Fix**: 
1. Production: `reclaimPolicy: Retain` always.
2. RBAC: deny `delete pvc` cho non-admin.
3. Audit log + alert if PVC deleted.

### ❌ Pitfall: Resize PVC nhưng filesystem không expand

→ Online filesystem resize có thể không trigger trên 1 số FS type. Fix: pod restart trigger filesystem expand:
```bash
kubectl delete pod postgres-0 -n production
# Recreated, filesystem expanded
```

### ❌ Pitfall: VolumeSnapshot không restore đúng timing

→ Snapshot trong khi DB write → consistency issue. Postgres recovery sau restore (WAL replay).

→ **Fix production**:
1. **Cold snapshot**: stop pod → snapshot → start pod. Downtime nhưng consistent.
2. **Application-aware snapshot**: dùng `pg_basebackup` + `pg_dump` (logical) thay storage snapshot.
3. **Operator** (CloudNativePG) handle backup proper: WAL archiving + base backup → point-in-time recovery.

### ✅ Best practice: PodAntiAffinity spread replica

```yaml
spec:
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: postgres
              topologyKey: kubernetes.io/hostname
```

→ 3 replica không cùng 1 node. Node fail → mất 1, không phải 3.

→ Multi-AZ: change `topologyKey: topology.kubernetes.io/zone` cho spread cross-AZ.

### ✅ Best practice: PDB cho stateful

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: postgres-pdb
  namespace: production
spec:
  minAvailable: 2          # always keep 2/3 available
  selector:
    matchLabels:
      app: postgres
```

→ Voluntary disruption (node drain, autoscaler) keep majority alive.

---

## 🧠 Self-check

**Q1.** Khi nào dùng `Deployment + PVC RWO` thay vì `StatefulSet`?

<details>
<summary>💡 Đáp án</summary>

`Deployment + PVC RWO` (single replica, persistent storage):
- **Use case**: Single-instance app cần data persistent nhưng KHÔNG stateful cluster (Grafana, Redis single, single-node Postgres dev).
- **Why not StatefulSet**: StatefulSet overhead (ordered start, headless Service, naming) không cần khi 1 replica.

Caveat:
- **`strategy.type: Recreate`** required cho Deployment với RWO PVC. RollingUpdate fail vì 2 pod cùng mount RWO PVC.
- **Single point of failure**: 1 pod = downtime khi update/node fail.
- **Không scale**: scale = 2 pod → 2nd pod stuck (PVC RWO).

**Khi cần HA** (multi-replica) hoặc **cluster semantics** (Postgres replication, Redis Sentinel, Kafka, Elasticsearch) → StatefulSet.

→ Pattern: dev single-instance = Deployment + PVC. Prod cluster = StatefulSet.
</details>

**Q2.** Headless Service vs regular Service — khác nhau gì?

<details>
<summary>💡 Đáp án</summary>

**Regular Service** (`clusterIP: <IP>`):
- 1 stable IP (ClusterIP) → kube-proxy load balance to pods.
- DNS `postgres.production.svc.cluster.local` → ClusterIP.
- Client connects ClusterIP → traffic split random across pods.
- Use: stateless app, client doesn't care which pod.

**Headless Service** (`clusterIP: None`):
- No ClusterIP allocated.
- DNS returns **A records of ALL pod IPs**: `postgres.production.svc.cluster.local` → [10.0.1.5, 10.0.1.6, 10.0.1.7].
- Per-pod DNS: `postgres-0.postgres.production.svc.cluster.local` → IP pod 0 specifically.
- Use: client need to connect specific pod (primary vs replica), service discovery for clustered apps.

StatefulSet **requires headless Service** to provide stable per-pod DNS. Each pod (`postgres-0`, `postgres-1`, `postgres-2`) has own DNS — apps connect specific pod by name.

→ Headless = DNS-only service discovery, no LB. Regular = LB with ClusterIP.
</details>

**Q3.** PV `reclaimPolicy: Delete` vs `Retain` — production database chọn cái nào?

<details>
<summary>💡 Đáp án</summary>

**Production database**: **ALWAYS `Retain`**.

Reason:
- `Delete`: PVC delete → PV delete → underlying storage (EBS/PD) **deleted forever**. Mất data, không recover được.
- `Retain`: PVC delete → PV stays as `Released` status. Underlying storage preserved. Admin manually:
  1. Recover: edit PV `claimRef` = null → PV `Available` → new PVC bind reuse.
  2. Cleanup: delete PV (data gone) khi confirm không cần nữa.

`Delete` only OK for:
- Dev/test environment, OK to lose data.
- Cache layer (Redis) where data is regenerable.
- Ephemeral workload (CI runner).

Defense-in-depth:
1. `reclaimPolicy: Retain` ở StorageClass.
2. `persistentVolumeClaimRetentionPolicy` ở StatefulSet.
3. RBAC deny `delete pvc` cho non-admin.
4. Volume snapshot daily cron.
5. External backup (S3, off-cluster).

→ Production data layer: belt + suspenders.
</details>

**Q4.** Tại sao `volumeBindingMode: WaitForFirstConsumer` quan trọng cho multi-AZ?

<details>
<summary>💡 Đáp án</summary>

**`Immediate`**:
- PVC create → CSI driver tạo PV ngay (random AZ trong cluster's AZ list).
- Pod schedule sau → có thể schedule AZ khác.
- EBS volume bound AZ-a, pod schedule AZ-b → **mount fail** vì EBS chỉ accessible from same AZ.
- Pod stuck `Pending: 1 node(s) had volume node affinity conflict`.

**`WaitForFirstConsumer`**:
- PVC create → CSI wait, không tạo PV ngay.
- Pod schedule → K8s scheduler chọn node theo policy (anti-affinity, resource).
- Sau khi pod assigned node X → CSI tạo PV ở **same AZ với node X**.
- Bind PVC → PV.
- Mount success.

→ For block storage (EBS/PD) trong multi-AZ cluster: **always `WaitForFirstConsumer`**.

Single-AZ cluster: `Immediate` OK (no AZ conflict).
RWX storage (EFS/CephFS): cross-AZ accessible → `Immediate` OK.

K8s cloud StorageClass default 2026 = `WaitForFirstConsumer` (best practice baked in).
</details>

**Q5.** Khi nào dùng **Operator** thay vì StatefulSet trực tiếp?

<details>
<summary>💡 Đáp án</summary>

**StatefulSet đủ khi**:
- Simple stateful app: 1 instance cache, single-node Postgres dev, lightweight cluster.
- App handle replication tự (Postgres single primary, no failover).
- Team biết details + manual ops OK.

**Operator cần khi**:
- **Production HA database** (Postgres/MySQL/Redis cluster): replication, auto-failover, primary election.
- **Backup automation**: scheduled snapshot + WAL archiving + point-in-time recovery.
- **Schema management**: migration safe execution.
- **Monitoring + alerting**: built-in ServiceMonitor + alerts.
- **Cluster lifecycle**: scale, upgrade, repair automatic.
- **Reduce ops burden**: operator codify SRE knowledge.

Real example:
- StatefulSet Postgres = 100 dòng YAML, manual failover, no automatic backup.
- CloudNativePG cluster CRD = 30 dòng YAML, auto failover via raft consensus, scheduled S3 backup, monitoring integration, point-in-time recovery, online major upgrade.

→ Production: prefer Operator-managed stateful workload. StatefulSet là implementation detail behind Operator.

Bài 04 sẽ dạy Operator pattern + viết simple one + use CloudNativePG.
</details>

---

## ⚡ Cheatsheet

```bash
# === StatefulSet ===
kubectl get sts -n <ns>
kubectl describe sts <name> -n <ns>
kubectl rollout status sts/<name> -n <ns>
kubectl rollout history sts/<name>
kubectl rollout undo sts/<name>

# === PVC ===
kubectl get pvc -n <ns>
kubectl describe pvc <name> -n <ns>
kubectl edit pvc <name> -n <ns>           # resize size
kubectl delete pvc <name> -n <ns>         # CAREFUL — verify reclaimPolicy

# === PV ===
kubectl get pv
kubectl describe pv <name>
kubectl patch pv <name> -p '{"spec":{"claimRef":null}}'   # release for reuse

# === StorageClass ===
kubectl get sc
kubectl describe sc <name>

# === VolumeSnapshot ===
kubectl get volumesnapshot -n <ns>
kubectl get volumesnapshotcontent

# === Postgres in StatefulSet ===
kubectl exec -it postgres-0 -n production -- psql -U postgres
kubectl logs postgres-0 -n production
kubectl exec postgres-0 -- df -h           # check disk usage

# === Debug pending PVC ===
kubectl describe pvc <name>                # look for events
kubectl get events -n <ns> --sort-by=.lastTimestamp | tail
kubectl get pods -l app=ebs-csi-controller -n kube-system   # CSI driver running?
```

```yaml
# === Common StorageClass parameters ===
# AWS EBS gp3
provisioner: ebs.csi.aws.com
parameters: { type: gp3, encrypted: "true" }

# GCP PD
provisioner: pd.csi.storage.gke.io  
parameters: { type: pd-ssd, replication-type: regional-pd }

# Azure Disk
provisioner: disk.csi.azure.com
parameters: { skuName: Premium_LRS }

# NFS (RWX)
provisioner: nfs.csi.k8s.io
parameters: { server: nfs.acmeshop.vn, share: /export }

# Longhorn (on-prem)
provisioner: driver.longhorn.io
parameters: { numberOfReplicas: "3" }
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **StatefulSet** | Workload type cho stateful app: stable identity + per-pod PVC + ordered |
| **Headless Service** | Service `clusterIP: None` — DNS per pod, không LB |
| **PV (PersistentVolume)** | Cluster-wide storage resource — 1 actual disk |
| **PVC (PersistentVolumeClaim)** | Namespace request for storage — bind to PV |
| **StorageClass** | Template for dynamic PV provisioning — defines CSI provisioner + params |
| **CSI** | Container Storage Interface — plugin spec storage driver |
| **`volumeClaimTemplates`** | StatefulSet field — auto-create PVC per pod |
| **`reclaimPolicy`** | What happens to PV when PVC delete: `Delete` (gone) hoặc `Retain` (keep) |
| **`volumeBindingMode`** | When PVC bind PV: `Immediate` hoặc `WaitForFirstConsumer` (multi-AZ safe) |
| **Access mode** | RWO (1 node RW), RWX (many nodes RW), ROX (many nodes RO), RWOP (1 pod RW) |
| **`allowVolumeExpansion`** | StorageClass flag — PVC resizable |
| **VolumeSnapshot** | K8s resource — point-in-time backup of PV |
| **VolumeSnapshotClass** | Template for VolumeSnapshot (như StorageClass cho snapshot) |
| **Longhorn** | OSS distributed block storage (Rancher, on-prem) |
| **CloudNativePG** | Postgres Operator native K8s (CNCF) |
| **PodDisruptionBudget (PDB)** | Guarantee N pod available during voluntary disruption |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [02_ingress-cert-manager-tls.md](02_ingress-cert-manager-tls.md)
- → Tiếp: [04_autoscaling-and-operators.md](04_autoscaling-and-operators.md) *(sắp viết)*
- ↑ Cluster: [Kubernetes README](../../README.md)

### Cross-reference
- 🗄️ [PostgreSQL basic](../../../../06_Databases/postgresql/) — Postgres concepts
- 🏗️ [IaC Terraform](../../../iac/lessons/01_basic/01_terraform-basics.md) — provision EBS/PD via Terraform
- 📊 [Observability Prometheus](../../../observability/lessons/01_basic/01_metrics-prometheus.md) — monitor PV usage

### Tài nguyên ngoài
- 📖 [StatefulSet docs](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
- 📖 [PV/PVC docs](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- 📖 [CSI docs](https://kubernetes-csi.github.io/docs/)
- 📖 [EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
- 📖 [Longhorn docs](https://longhorn.io/docs/)
- 📖 [CloudNativePG docs](https://cloudnative-pg.io/documentation/)
- 📖 [Postgres Operator comparison](https://k8spgrun.com/) — Zalando vs CNPG vs Crunchy
- 📖 [VolumeSnapshot docs](https://kubernetes.io/docs/concepts/storage/volume-snapshots/)
- 📖 [Velero](https://velero.io/) — cluster-wide backup/restore tool

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Deployment design + StatefulSet design + Bảng so sánh + Headless Service + Concepts (PV/PVC/StorageClass).
- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 03 của intermediate. StatefulSet vs Deployment + PV/PVC/StorageClass + dynamic provisioning (EBS/PD/Longhorn) + headless Service + Postgres 3-replica hands-on + VolumeSnapshot backup + resize PVC + Operator pattern preview (CloudNativePG). 6 pitfall + 2 best practice + 5 self-check + cheatsheet.
