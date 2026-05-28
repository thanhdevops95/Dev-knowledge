# 🎓 Backup & Replication — Production essentials

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [psql & Meta-commands](01_psql-and-meta-commands.md)

> 🎯 *Master Postgres production essentials: **`pg_dump`** + **`pg_restore`** (logical backup), **`pg_basebackup`** (physical), **streaming replication** (HA + read replica), **WAL + PITR** intro, **3-2-1 backup rule**, schedule cron + monitoring. Sau bài này tự tin chạy Postgres production.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **logical** (pg_dump) vs **physical** (pg_basebackup) backup
- [ ] Dùng **`pg_dump`** custom format + restore với `pg_restore`
- [ ] **Schedule** backup tự động (cron + systemd timer)
- [ ] **3-2-1 backup rule** + offsite storage (S3)
- [ ] Setup **streaming replication** (primary + replica)
- [ ] **Read replica** cho scale + analytics
- [ ] Hiểu **WAL** + **PITR** (Point-In-Time Recovery)
- [ ] Tools: **pgBackRest**, **Barman**, **WAL-G** intro

---

## Tình huống — bạn bị rm -rf database

Bạn deploy production, mọi thứ ổn. Một hôm tinh nghịch test query:

```sql
DELETE FROM users;
-- (bạn quên WHERE)
COMMIT;
```

→ 50,000 user **mất sạch**. App down. CEO call.

Bạn ngơ:
- Có **backup** không? Backup ở **đâu**?
- **Restore** thế nào?
- Tại sao không có **replica** để fallback?
- Production phải có **strategy** thế nào?

Senior:
> *"Production DB không có **backup automated + replica** = đùa giỡn với business. **3-2-1 rule**: 3 copies, 2 different media, 1 offsite. Plus replica để 0-downtime + read scaling."*

→ Bài này dạy backup + replication đầy đủ.

---

## 1️⃣ 2 loại backup Postgres

Postgres có **2 chiến lược backup hoàn toàn khác nhau** — logical (SQL statements) và physical (raw file). Pick đúng dựa vào kích thước DB + nhu cầu restore: portable/selective hay nhanh/PITR:

| Loại | Tool | Format | Use case |
|---|---|---|---|
| **Logical** | `pg_dump`, `pg_dumpall` | SQL hoặc binary custom | Small-medium DB, cross-version restore |
| **Physical** | `pg_basebackup`, `pgBackRest` | Raw files | Large DB, PITR, replication |

### Logical (pg_dump)

Logical backup dump ra **SQL statements** — đọc được, restore cross-version, selective theo table. Tradeoff: chậm khi DB rất lớn (>100GB) vì phải scan + format từng row:

- **Ưu**: portable, cross-version, selective (table/schema), readable SQL.
- **Nhược**: chậm trên DB lớn, lock issues nếu transaction kéo dài.

### Physical (pg_basebackup)

Physical backup copy **raw data file** từ disk — cực nhanh cho DB lớn, support Point-in-Time Recovery (PITR) + setup replica. Tradeoff: bị khoá version + architecture giống nhau, không restore selective được:

- **Ưu**: nhanh cho DB lớn, support PITR + replication.
- **Nhược**: cần cùng version + architecture, all-or-nothing.

→ **Default 2026**: `pg_dump` cho DB <100GB, `pgBackRest` cho prod >100GB.

---

## 2️⃣ `pg_dump` — Logical backup

### 4 format

`pg_dump` có **4 format output** — chọn theo use case. Format mặc định plain SQL dễ đọc nhưng chậm restore; custom format (`-Fc`) là **default cho production** vì compressed + restore selective được:

```bash
# 1. Plain SQL (default — readable but slow restore)
pg_dump myapp > backup.sql

# 2. Custom format (-Fc) — binary compressed (recommended)
pg_dump -Fc myapp > backup.dump
pg_dump -Fc -f backup.dump myapp

# 3. Tar (-Ft) — uncompressed tar
pg_dump -Ft myapp > backup.tar

# 4. Directory (-Fd) — parallel dump
pg_dump -Fd -j 4 -f /backup/myapp myapp     # 4 parallel workers
```

→ **Custom format `-Fc`** = default cho production. Compressed + can restore selectively.

### Options

Production `pg_dump` cần thêm vài flag để portable + an toàn: `--no-owner`/`--no-acl` để restore sang môi trường khác user/permission, `--verbose` để log progress. Template đầy đủ:

```bash
pg_dump \
  -h localhost -p 5432 \
  -U myapp \
  -d myapp \
  -Fc \
  -f /backup/myapp-2026-05-23.dump \
  --verbose \
  --no-owner \                # Skip OWNER statements (cross-env restore)
  --no-acl                     # Skip permissions
```

### Selective dump

```bash
# Only specific schema
pg_dump -Fc -n public myapp > backup.dump

# Only specific tables
pg_dump -Fc -t users -t orders myapp > backup.dump

# Schema only (no data)
pg_dump --schema-only myapp > schema.sql

# Data only
pg_dump --data-only myapp > data.sql

# Exclude tables
pg_dump --exclude-table='logs_*' myapp > backup.sql
```

### Backup all databases — `pg_dumpall`

```bash
# Backup mọi DB + roles + tablespaces
pg_dumpall -f all-databases.sql

# Chỉ roles (cho restore replica)
pg_dumpall --roles-only > roles.sql

# Chỉ globals (roles + tablespaces)
pg_dumpall --globals-only > globals.sql
```

→ `pg_dumpall` cho cluster-wide. `pg_dump` cho per-DB.

---

## 3️⃣ `pg_restore` — Logical restore

```bash
# Custom format
pg_restore -d myapp_restored backup.dump

# With options
pg_restore \
  -h localhost -U postgres -d myapp_restored \
  --clean \                # Drop existing objects trước
  --create \               # Create DB
  --if-exists \            # Don't error if doesn't exist
  -j 4 \                   # 4 parallel workers (fast restore)
  --verbose \
  backup.dump

# Plain SQL — dùng psql
psql -d myapp_restored < backup.sql

# Selective restore (custom format only)
pg_restore -d myapp -t users backup.dump        # Chỉ table users
pg_restore -d myapp -n public backup.dump        # Chỉ schema public
```

### Pre-restore checklist

```bash
# 1. Create empty DB
psql -c "CREATE DATABASE myapp_restored;"

# 2. List content trong dump (preview)
pg_restore -l backup.dump | less

# 3. Restore
pg_restore -d myapp_restored -j 4 backup.dump

# 4. Verify
psql -d myapp_restored -c "SELECT COUNT(*) FROM users;"
```

### bạn restore sau disaster

```bash
# Last backup yesterday 2 AM
ls -la /backup/
# myapp-2026-05-22-02-00.dump (32 GB)

# Create restore DB (don't overwrite original)
psql -c "CREATE DATABASE myapp_restored;"

# Restore
pg_restore -d myapp_restored -j 8 --verbose /backup/myapp-2026-05-22-02-00.dump
# Took 20 minutes

# Verify rows
psql -d myapp_restored -c "SELECT COUNT(*) FROM users;"
# 49,123 (yesterday's count, vs 50,000 today — lost 877 users last 24h)

# Switch app to restored DB (update DATABASE_URL)
# Lost: signups + actions từ 2 AM hôm qua đến giờ.
```

→ **Recovery Point Objective** (RPO) = 24h với daily backup. Cần PITR để giảm xuống minutes.

---

## 4️⃣ Schedule backup tự động

### Cron approach (basic)

```bash
# /etc/cron.d/postgres-backup
0 2 * * * postgres /usr/local/bin/backup-pg.sh
```

```bash
#!/bin/bash
# /usr/local/bin/backup-pg.sh
set -euo pipefail

BACKUP_DIR="/backup"
DATE=$(date +%Y-%m-%d-%H-%M)
RETENTION_DAYS=14

# Dump
pg_dump -Fc -f "$BACKUP_DIR/myapp-$DATE.dump" myapp

# Verify
if [ ! -s "$BACKUP_DIR/myapp-$DATE.dump" ]; then
  echo "Backup failed!" | mail -s "PG backup FAIL" ops@acmeshop.vn
  exit 1
fi

# Upload to S3 (offsite — 3-2-1 rule)
aws s3 cp "$BACKUP_DIR/myapp-$DATE.dump" s3://acmeshop-backups/postgres/

# Cleanup local backups > 14 days
find "$BACKUP_DIR" -name "myapp-*.dump" -mtime +$RETENTION_DAYS -delete

echo "Backup OK: myapp-$DATE.dump"
```

### systemd timer (modern alternative — xem [bài systemd](../../../../04_os/linux/lessons/02_intermediate/01_systemd-services.md))

```ini
# /etc/systemd/system/pg-backup.service
[Unit]
Description=Postgres backup

[Service]
Type=oneshot
User=postgres
ExecStart=/usr/local/bin/backup-pg.sh
```

```ini
# /etc/systemd/system/pg-backup.timer
[Unit]
Description=Daily Postgres backup at 2 AM

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable --now pg-backup.timer
```

### Cloud managed (Supabase, RDS) — Auto

Managed Postgres tự backup mỗi ngày + retain N ngày. Settings configurable. **No setup needed**.

---

## 5️⃣ 3-2-1 backup rule

| Rule | Meaning |
|---|---|
| **3** | 3 copies of data |
| **2** | 2 different storage media (disk + cloud) |
| **1** | 1 offsite copy (different region/cloud) |

### Practical setup

```
1. Production DB (live)               ← copy #1
2. Local backup /backup/              ← copy #2 (different disk)
3. S3 us-east-1                       ← copy #3 (offsite, different region)
   + GCS or another region (extra safety)
```

→ **Disaster scenarios covered**:
- App bug → restore from /backup/.
- Disk failure → restore from S3.
- Region outage → restore from cross-region copy.
- Ransomware → restore from immutable S3 (versioning + lock).

### Test restore — Quan trọng

> ⚠️ **Backup không test = không có backup**.

```bash
# Monthly: full restore drill
# Restore vào staging environment, run smoke tests, verify data integrity
```

→ Disaster lúc đầu mới phát hiện backup corrupt = quá muộn.

---

## 6️⃣ Streaming replication — HA + read replica

### Architecture

```
┌──────────────┐        WAL stream         ┌──────────────┐
│   Primary    │ ──────────────────────────> │   Replica    │
│  (read+write)│                              │  (read only) │
└──────────────┘                              └──────────────┘
   App writes                                   Analytics
                                                Read scaling
                                                Failover
```

### Setup primary

```bash
# /etc/postgresql/18/main/postgresql.conf
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
```

```bash
# /etc/postgresql/18/main/pg_hba.conf
host    replication     replicator     10.0.0.0/8     md5
```

```sql
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replpass';
SELECT pg_create_physical_replication_slot('slot_replica1');
```

```bash
sudo systemctl restart postgresql
```

### Setup replica

```bash
# On replica server — STOP postgres first, clear data dir
sudo systemctl stop postgresql
sudo rm -rf /var/lib/postgresql/18/main/*

# Base backup from primary
sudo -u postgres pg_basebackup \
  -h primary.acmeshop.vn \
  -U replicator \
  -D /var/lib/postgresql/18/main \
  -P \
  -R \                                     # Auto write recovery.conf
  -S slot_replica1 \
  -X stream                                # Stream WAL during backup

# Start replica
sudo systemctl start postgresql
```

→ Replica giờ tự stream WAL từ primary, **read-only**, lag thường <1s.

### Verify replication

On primary:
```sql
SELECT * FROM pg_stat_replication;
-- client_addr | state | sync_state | replay_lag
-- 10.0.0.5    | streaming | async   | 00:00:00.012
```

On replica:
```sql
SELECT pg_is_in_recovery();    -- true
SELECT now() - pg_last_xact_replay_timestamp();    -- lag
```

### Use cases

| Use case | Implementation |
|---|---|
| **HA failover** | Primary down → promote replica to primary (manual or `repmgr`/`Patroni`) |
| **Read scaling** | App route read queries → replica, write → primary |
| **Analytics** | Heavy report queries on replica (không slow primary) |
| **Cross-region read** | Replica gần user → low latency |

→ **2026 production**: minimum 1 standby replica + automated failover (Patroni/repmgr) cho HA.

### Cloud managed — automatic

| Provider | Replica feature |
|---|---|
| AWS RDS | Multi-AZ + Read Replicas (1-click) |
| Supabase | Read replicas (paid) |
| Neon | Branching (different concept) |

---

## 7️⃣ WAL + PITR — Point-In-Time Recovery

### WAL (Write-Ahead Log) là gì?

```
1. Postgres viết changes vào WAL FIRST
2. Sau đó apply vào data files
3. Crash → replay WAL → recover
```

→ **WAL = transaction log**, key cho durability + replication + PITR.

### PITR concept

```
Backup base (Monday 2 AM)
   ↓
WAL archive (continuous)
   ↓
Restore base + replay WAL đến Tuesday 14:32:01
   ↓
Database at EXACT point in time
```

→ Lost data 1 phút trước disaster = restore tới phút đó.

### Setup WAL archiving

```bash
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://acmeshop-wal/%f'   # Upload WAL to S3
# Hoặc gcs, azure, ssh
```

→ Mỗi WAL segment (16MB default) upload S3.

### Tools dễ hơn — pgBackRest, Barman, WAL-G

Setup PITR thủ công phức tạp. Production dùng tools:

| Tool | Highlights |
|---|---|
| **pgBackRest** | **#1 2026** — incremental backup + PITR + compression + cloud-native (S3/GCS) |
| **Barman** | Italian, mature, server-based |
| **WAL-G** | Yandex/Citus, supports many cloud, written Go |

### pgBackRest example

```bash
# /etc/pgbackrest/pgbackrest.conf
[global]
repo1-type=s3
repo1-s3-bucket=acmeshop-pg
repo1-s3-region=us-east-1
repo1-retention-full=14

[main]
pg1-path=/var/lib/postgresql/18/main

# Take full backup
pgbackrest --stanza=main backup --type=full

# Incremental
pgbackrest --stanza=main backup --type=incr

# PITR restore
pgbackrest --stanza=main restore \
  --type=time --target='2026-05-23 14:32:00'
```

→ pgBackRest handles full + incremental + WAL + PITR + parallel. **Production essential**.

---

## 8️⃣ bạn's production setup

### Architecture

```
┌──────────────────────────────────────┐
│      AWS us-east-1                    │
│                                       │
│  ┌─────────────┐    streaming         │
│  │  Primary    │ ─────────────┐       │
│  │  RDS Postgres│              │       │
│  └─────────────┘              ▼       │
│                          ┌────────┐   │
│                          │ Replica│   │
│                          │ Multi-AZ│  │
│                          └────────┘   │
│                                       │
│  pgBackRest → S3 us-east-1            │
└──────────────┬───────────────────────┘
               │
               ▼
       S3 us-west-2 (cross-region copy)
       + Glacier (long-term archive)
```

### Backup strategy

| Tier | Frequency | Retention | Location |
|---|---|---|---|
| Full backup | Weekly Sunday 2 AM | 4 weeks | S3 us-east-1 |
| Incremental backup | Daily 2 AM | 14 days | S3 us-east-1 |
| WAL archive | Continuous | 7 days | S3 us-east-1 |
| Cross-region replica | Continuous | Live | S3 us-west-2 |
| Annual archive | Yearly | 7 years | Glacier |

### Recovery objectives

| Metric | Target | Tool |
|---|---|---|
| **RPO** (Recovery Point Objective — max data loss) | 1 minute | WAL archive + replica |
| **RTO** (Recovery Time Objective — max downtime) | 5 minutes | Multi-AZ failover (auto) |

### Monitoring

```bash
# Check replication lag
psql -c "SELECT now() - pg_last_xact_replay_timestamp() AS lag;" -h replica

# Alert if lag > 30s
prometheus + postgres_exporter
```

→ Alert tới Slack/PagerDuty khi replica lag cao hoặc backup fail.

---

## 9️⃣ Bạn fix disaster

```bash
# DELETE FROM users; xảy ra 14:32:01
# Discovery time: 14:35

# Step 1: Stop application writes
kubectl scale deployment myapp --replicas=0

# Step 2: PITR to 14:31:59
pgbackrest --stanza=main restore \
  --type=time --target='2026-05-23 14:31:59' \
  --target-action=promote

# Step 3: Verify
psql -c "SELECT COUNT(*) FROM users;"
# 50000  ← restored

# Step 4: Update DATABASE_URL nếu cần
# Step 5: Scale back app
kubectl scale deployment myapp --replicas=3

# Total downtime: ~15 phút
# Data loss: ~2 phút (giữa 14:31:59 và discovery time)
```

→ Without PITR + WAL archive: lost all data từ daily backup time. With: 2 minutes only.

---

## ⚠️ 5 pitfall hay vướng

1. **Backup chưa test restore** → corrupt, không restore được. Monthly drill.
2. **Backup local same disk** → disk fail mất cả 2. 3-2-1 rule.
3. **Hardcode credentials trong backup script** → leak. Dùng `.pgpass` + env vars.
4. **Replica có write traffic** → conflict. Replica chỉ read.
5. **No monitoring** → backup fail silent 6 tháng → đụng disaster mới biết. Alert mỗi backup.

---

## ✅ Self-check

1. Khác **logical** (pg_dump) và **physical** (pg_basebackup) backup?
2. **3-2-1 rule** = gì?
3. **WAL** trong Postgres dùng cho gì?
4. **Read replica** — 3 use cases?
5. Khác **RPO** vs **RTO**?

<details>
<summary>Gợi ý đáp án</summary>

1. **Logical (pg_dump)**: SQL hoặc binary custom, **portable** (cross-version, cross-arch), selective table/schema, slow trên DB lớn. **Physical (pg_basebackup)**: raw file copy, **fast** trên DB lớn, supports PITR + replication, **same version + arch required**. Default: pg_dump cho <100GB, physical (pgBackRest) cho >100GB.

2. **3-2-1**: 3 copies of data, 2 different storage media (disk + cloud), 1 offsite (different region/cloud). Disaster covers: bug → local, disk fail → cloud, region outage → cross-region, ransomware → immutable backup.

3. **WAL** (Write-Ahead Log) = transaction log. (a) **Durability** — write WAL trước data file, crash recovery replay. (b) **Replication** — stream WAL từ primary → replica. (c) **PITR** — base backup + WAL archive = restore exact point in time.

4. (a) **HA failover** — primary down, promote replica. (b) **Read scaling** — app route read → replica, write → primary. (c) **Analytics** — heavy report queries trên replica không slow primary. (d) **Cross-region read** — replica gần user low latency.

5. **RPO** (Recovery Point Objective) = max data loss acceptable (vd "1 minute"). **RTO** (Recovery Time Objective) = max downtime acceptable (vd "5 minutes"). RPO drives backup frequency, RTO drives recovery procedure speed.
</details>

---

## ⚡ Cheatsheet

### pg_dump

```bash
# Full DB
pg_dump -Fc -f backup.dump myapp

# Custom format (recommended)
pg_dump -Fc -j 4 -f backup.dump myapp

# Schema only / data only
pg_dump --schema-only myapp > schema.sql
pg_dump --data-only myapp > data.sql

# All DBs + roles
pg_dumpall > all.sql
```

### pg_restore

```bash
pg_restore -d new_db -j 4 --verbose backup.dump
pg_restore --list backup.dump            # Preview content
```

### Streaming replication

```sql
-- Primary postgresql.conf
wal_level = replica
max_wal_senders = 10
hot_standby = on

-- Setup replica
pg_basebackup -h primary -D /var/lib/postgresql/main -R -S slot_replica1
```

### pgBackRest

```bash
pgbackrest --stanza=main backup --type=full
pgbackrest --stanza=main backup --type=incr
pgbackrest --stanza=main restore --type=time --target='2026-05-23 14:31:59'
```

### Schedule

```bash
# Cron
0 2 * * * postgres /usr/local/bin/backup.sh

# Or systemd timer (modern)
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`pg_dump`** | Logical backup (SQL hoặc binary) |
| **`pg_restore`** | Restore from custom-format dump |
| **`pg_dumpall`** | Backup mọi DB + roles + globals |
| **`pg_basebackup`** | Physical backup (raw file copy) |
| **WAL** | Write-Ahead Log — transaction log |
| **WAL archiving** | Upload WAL segments to safe storage |
| **PITR** | Point-In-Time Recovery |
| **Streaming replication** | Primary stream WAL → replica real-time |
| **Replica / standby** | Read-only copy of primary |
| **Failover** | Promote replica → primary when primary down |
| **Multi-AZ** | AWS replica in different availability zone |
| **3-2-1 rule** | 3 copies, 2 media, 1 offsite |
| **RPO / RTO** | Max data loss / Max downtime acceptable |
| **pgBackRest / Barman / WAL-G** | Production backup tools |
| **Patroni / repmgr** | Auto-failover orchestrators |

---

## 🔗 Links

### Trong cluster
- ← Trước: [JSONB & Arrays](03_jsonb-and-arrays.md)
- ↑ Cluster: [postgresql README](../../README.md)

### Cross-reference
- [systemd timer thay cron](../../../../04_os/linux/lessons/02_intermediate/01_systemd-services.md#9️⃣-timer-units--thay-thế-cron) — scheduling backup
- [Linux SSH](../../../../04_os/linux/lessons/02_intermediate/02_ssh-deep-dive.md) — manage backups across servers

### External
- 📖 [Postgres backup docs](https://www.postgresql.org/docs/current/backup.html)
- 📖 [pgBackRest docs](https://pgbackrest.org/)
- 📖 [PostgreSQL High Availability — Tatiana Krupenya](https://highavailability.network/) — concepts
- 📖 [AWS RDS Postgres Best Practices](https://aws.amazon.com/blogs/database/category/database/amazon-rds-postgresql/)
- 📖 [Crunchy Data: PG backup deep dive](https://www.crunchydata.com/blog/category/backup)

---

> 🎯 *Cluster PostgreSQL basic 5/5 đóng. Bạn vận hành Postgres production tự tin: install + psql + perf + JSONB + backup/replication. Bài kế tiếp ngoài cluster: advanced (partitioning, sharding với Citus, pgvector deep, advanced replication).*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 "2 loại backup" + Logical pg_dump pros/cons (Việt hoá "Pros/Cons" → "Ưu/Nhược") + Physical pg_basebackup + §2 4 format pg_dump + Options. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `postgresql/` lesson 5/5. Cover: logical (pg_dump 4 format + pg_dumpall) + pg_restore + physical (pg_basebackup) + PITR (WAL archive + recovery_target_time) + streaming replication setup + logical replication + monitor lag + backup strategy (3-2-1) + production checklist.
