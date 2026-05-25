# 🎓 systemd Services — Biến app thành service production

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~18 phút\
> **Prerequisites:** [Users & Permissions](00_users-and-permissions.md)

> 🎯 *Hiểu **systemd** thay init, viết **unit file** (`.service`), dùng `systemctl` start/stop/enable, đọc log với `journalctl`, biến FastAPI thành service auto-restart, hardening (`User=`, `NoNewPrivileges=`, `ProtectSystem=`). Sau bài này backend chạy 24/7 production-grade.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **systemd** thay init (SysV) + lý do
- [ ] Đọc cấu trúc **unit file** (`.service`, `.timer`, `.socket`)
- [ ] Tạo service cho **FastAPI/Node app** từ A-Z
- [ ] Dùng `systemctl`: start/stop/status/enable/restart/reload
- [ ] Đọc log với `journalctl` (filter, follow, jump time)
- [ ] Auto-restart on crash với `Restart=always`
- [ ] Hardening unit: `User=`, `NoNewPrivileges=`, `ProtectSystem=`
- [ ] Hiểu **timer unit** thay cron + viết job định kỳ

---

## Tình huống — Bạn deploy FastAPI, đóng SSH = app chết

Bạn deploy FastAPI lên VPS như bài 00:

```bash
ssh user@vps "fastapi run main.py --port 8000"
```

Bạn đóng terminal → **app tắt**. Reconnect SSH → app vẫn down.

Bạn thử:
```bash
nohup fastapi run main.py &              # Detach, OK
```

→ Tạm OK nhưng:
- 😱 Server reboot = app chết, không tự bật lại.
- 😱 App crash (segfault, OOM) = down forever cho đến reboot tay.
- 😱 Không có **log** → không biết app crashed lúc nào.
- 😱 Update code phải `kill PID` thủ công.

Senior bảo:
> *"Mọi production app phải chạy qua **systemd service**. Setup 5 phút, lợi cả đời: auto-start, auto-restart, log integrate, hardening."*

→ Bài này dạy đầy đủ.

---

## 1️⃣ systemd là gì?

**systemd** = init system + service manager **default trên đa số Linux distro hiện đại** (Ubuntu 16+, Debian 8+, RHEL 7+, Fedora, Arch).

| Thay thế | Mục đích |
|---|---|
| **init / SysV init** | Quản lý service (start, stop) |
| **rc.d scripts** | Boot scripts |
| **cron** (một phần) | Timer-based jobs |
| **inetd** | Socket-activated services |
| **syslog** (một phần) | Logging |

### Vai trò trong Linux

🪞 **Ẩn dụ**: *systemd như **quản gia cao cấp tòa nhà** — vừa mở khoá cửa lúc bạn về (boot), vừa bật điện nước (services), vừa giám sát nếu máy giặt hỏng (auto-restart), vừa ghi sổ ai vào ai ra (logs). 1 người làm việc của 5 người trước đây.*

Khi máy boot, systemd là process đầu tiên (PID 1) được kernel khởi động. Sau đó nó quản lý mọi thứ trong suốt vòng đời máy:

```
Boot:
  Kernel
    └ /sbin/init (= systemd, PID 1)
        ├ Mount filesystem
        ├ Start services (parallel)
        ├ Start user sessions
        └ Manage everything sau boot
```

### Concept chính

systemd có 6 loại "Unit" — mỗi loại quản lý 1 thứ khác nhau. Đọc bảng dưới để nhận biết khi gặp `*.service`, `*.timer`, ... bạn biết ngay nó là gì:

| Concept | Mô tả |
|---|---|
| **Unit** | Đơn vị quản lý (service, timer, mount, socket...) |
| **Target** | Group of units để boot (`multi-user.target` = bộ services chạy bình thường) |
| **Service** | App/daemon (vd `nginx.service`, `ssh.service`) |
| **Timer** | Trigger định kỳ (replace cron) |
| **Socket** | Socket-activated service |
| **Mount** | Filesystem mount point |

### Tại sao systemd thay SysV?

Trước 2010, Linux dùng SysV init. Vì sao đa số distro chuyển sang systemd? Bảng so sánh 6 điểm cốt lõi:

| Aspect | SysV init | systemd |
|---|---|---|
| Boot speed | Sequential (chậm) | Parallel (nhanh 3-5x) |
| Service dependency | Order số (`/etc/rc.d/S30nginx`) | Declarative (`After=`, `Requires=`) |
| Crash auto-restart | ❌ | ✅ `Restart=always` |
| Log integration | ❌ (rsyslog riêng) | ✅ `journalctl` |
| Resource limit | Manual (`ulimit`) | Declarative (`MemoryLimit=`) |
| Sandbox hardening | ❌ | ✅ Built-in |
| Adoption 2026 | Legacy | **99%+ distro modern** |

> ⚠️ **Controversy**: systemd bị phê bình "quá nhiều quyền lực, vi phạm Unix philosophy". Alternative: `runit`, `OpenRC` (Alpine), `s6`. Beginner: học systemd vì 99% server dùng.

---

## 2️⃣ `systemctl` — Tool điều khiển systemd

### Lệnh cơ bản

```bash
sudo systemctl start nginx                    # Start
sudo systemctl stop nginx                     # Stop
sudo systemctl restart nginx                  # Stop + start
sudo systemctl reload nginx                   # Reload config (không restart)
sudo systemctl status nginx                   # Trạng thái + log gần
sudo systemctl enable nginx                   # Auto-start boot
sudo systemctl disable nginx                  # Không auto-start
sudo systemctl is-active nginx                # → active / inactive / failed
sudo systemctl is-enabled nginx               # → enabled / disabled
sudo systemctl daemon-reload                  # Reload sau khi sửa unit file
```

### List services

```bash
systemctl list-units --type=service                  # Đang chạy
systemctl list-units --type=service --state=failed   # Crashed
systemctl list-unit-files --type=service             # All declared
```

### Disable + mask (block hoàn toàn)

```bash
sudo systemctl disable nginx                  # Tắt auto-start
sudo systemctl mask nginx                     # KHÔNG cho start bằng cách nào
sudo systemctl unmask nginx                   # Bỏ mask
```

→ `mask` = create symlink `/etc/systemd/system/nginx.service → /dev/null`. Mọi `start` đều fail. Dùng khi muốn **chắc chắn** service không bao giờ chạy.

---

## 3️⃣ Anatomy unit file

### Vị trí

| Path | Mục đích |
|---|---|
| `/lib/systemd/system/` hoặc `/usr/lib/systemd/system/` | Distro/package install (đừng sửa) |
| `/etc/systemd/system/` | Admin override / custom services |
| `~/.config/systemd/user/` | Per-user service (chạy as user, không root) |

### Cấu trúc

```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My FastAPI Application
Documentation=https://example.com/docs
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/fastapi run main.py --port 8000
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 3 sections

| Section | Mục đích |
|---|---|
| **`[Unit]`** | Metadata + dependency |
| **`[Service]`** | Lệnh chạy + behavior |
| **`[Install]`** | Khi `enable`, link vào target nào |

---

## 4️⃣ `[Unit]` section — Metadata + dependency

```ini
[Unit]
Description=My FastAPI App
Documentation=https://docs.example.com
After=network.target postgresql.service     # Start SAU những unit này
Requires=postgresql.service                  # PHẢI có postgres (stop postgres → stop myapp)
Wants=redis.service                           # Tốt nếu có (không bắt buộc)
ConditionPathExists=/opt/myapp/main.py        # Skip nếu file không có
```

| Directive | Ý nghĩa |
|---|---|
| `After=` | Start sau unit này (không đảm bảo unit kia chạy thành công) |
| `Before=` | Start trước unit này |
| `Requires=` | **Phải** có. Unit kia fail = unit này stop |
| `Wants=` | Cố gắng start unit kia, không fail nếu không được |
| `Conflicts=` | Không thể chạy cùng unit khác |
| `ConditionXxx=` | Pre-condition (file tồn tại, host name, ...) |

---

## 5️⃣ `[Service]` section — Core của service

### `Type=` — Service lifecycle

| Type | Khi nào dùng |
|---|---|
| `simple` (default) | Process chạy foreground, không fork. **Hầu hết app modern (FastAPI, Node, Go).** |
| `forking` | Process tự daemonize (parent fork và exit). Classic daemon. |
| `oneshot` | Chạy 1 lần rồi exit (script setup) |
| `notify` | Process tự thông báo "ready" via `sd_notify()` |
| `idle` | `simple` nhưng đợi mọi service khác xong |

### `ExecStart=` + family

```ini
ExecStart=/opt/myapp/venv/bin/fastapi run main.py
ExecStartPre=/opt/myapp/scripts/pre-start.sh    # Chạy trước
ExecStartPost=/opt/myapp/scripts/notify.sh       # Chạy sau khi start
ExecReload=/bin/kill -HUP $MAINPID                # Khi reload
ExecStop=/bin/kill -TERM $MAINPID                 # Khi stop
```

→ `$MAINPID` = PID của process chính.

### `Restart=` — Auto-restart policy

| Value | Khi nào restart |
|---|---|
| `no` (default) | Không bao giờ |
| `always` | Mọi exit (kể cả `systemctl stop` cũng restart!) |
| `on-failure` | Chỉ khi exit code ≠ 0 hoặc crash |
| `on-success` | Khi exit code = 0 |
| `on-abnormal` | Tín hiệu, timeout |
| `unless-stopped` | Như `always` nhưng tôn trọng `systemctl stop` |

→ **Service production**: `Restart=on-failure` hoặc `Restart=always`. `RestartSec=5` = đợi 5s giữa retry.

### `User=` / `Group=`

```ini
User=myapp
Group=myapp
```

→ Service chạy as user này (không root). Best practice.

### Resource limits

```ini
MemoryMax=512M             # OOM kill nếu vượt
CPUQuota=50%                # Max 0.5 CPU
TasksMax=100                # Max thread/process
LimitNOFILE=65535           # File descriptor (cho high-concurrency)
```

---

## 6️⃣ Hardening — Sandboxing

systemd có **30+ directive** restrict service. Best practice 2026:

```ini
[Service]
User=myapp
Group=myapp

# Quyền cao
NoNewPrivileges=true              # Cấm setuid/capabilities mới
ProtectSystem=strict              # /usr, /boot, /etc read-only
ProtectHome=true                  # /home, /root invisible
PrivateTmp=true                   # /tmp riêng
PrivateDevices=true               # Không thấy /dev/sd* (chỉ /dev/null, /dev/zero, ...)
ProtectKernelTunables=true        # Không sysctl
ProtectKernelModules=true         # Không load module
ProtectControlGroups=true         # Không sửa cgroups
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
RestrictNamespaces=true
LockPersonality=true
MemoryDenyWriteExecute=true       # JIT app (PHP, JVM) phải bỏ này

# Capability — chỉ cho bind port nếu cần
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
```

→ Kiểm tra security score:
```bash
systemd-analyze security myapp.service
# Score: 1.2 OK
```

→ Mỗi directive là 1 lớp bảo vệ. App lỗi = exploit giới hạn.

---

## 7️⃣ Bạn viết unit file cho FastAPI

### `/etc/systemd/system/myapp.service`

```ini
[Unit]
Description=bạn Shop FastAPI
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
EnvironmentFile=/etc/myapp/myapp.env

# Bind port 80 không cần root
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

ExecStart=/opt/myapp/venv/bin/fastapi run main.py --port 80
Restart=on-failure
RestartSec=5

# Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/var/log/myapp /var/lib/myapp

# Resource limits
MemoryMax=512M
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

### `/etc/myapp/myapp.env`

```env
DATABASE_URL=postgresql+psycopg2://myapp:secret@localhost:5432/myapp
JWT_SECRET=<generated-secret>
LOG_LEVEL=INFO
```

→ `chmod 600 /etc/myapp/myapp.env && chown myapp:myapp` — secrets không cho user khác đọc.

### Enable + start

```bash
sudo systemctl daemon-reload                  # Reload unit files
sudo systemctl enable myapp.service           # Auto-start boot
sudo systemctl start myapp.service            # Start ngay
sudo systemctl status myapp.service           # Verify
```

### Update code → reload

```bash
# Pull code mới
cd /opt/myapp && git pull

# Restart service
sudo systemctl restart myapp.service

# Check status
sudo systemctl status myapp.service
```

→ Zero-downtime cần advanced (blue-green, k8s rolling update). systemd basic = 1-2s downtime mỗi restart.

---

## 8️⃣ `journalctl` — Đọc log

systemd **integrate logging** — mọi service stdout/stderr vào journal binary, query bằng `journalctl`.

### Lệnh thường dùng

```bash
journalctl -u myapp                          # Log của 1 service
journalctl -u myapp -f                        # Follow (như tail -f)
journalctl -u myapp -n 100                    # Last 100 line
journalctl -u myapp --since "10 min ago"
journalctl -u myapp --since "2025-05-23 14:00" --until "14:30"
journalctl -u myapp -p err                    # Chỉ ERROR và cao hơn
journalctl --boot                              # Log của boot hiện tại
journalctl --boot=-1                           # Log boot trước
journalctl -u myapp -o json                   # JSON format
journalctl -u myapp --grep "OutOfMemory"      # Filter pattern
journalctl --disk-usage                        # Size log
```

### Priority levels

| Code | Name |
|---|---|
| 0 | emerg |
| 1 | alert |
| 2 | crit |
| 3 | **err** |
| 4 | warning |
| 5 | notice |
| 6 | **info** |
| 7 | debug |

### Vault rotation + size limit

```ini
# /etc/systemd/journald.conf
[Journal]
SystemMaxUse=2G                              # Max disk
SystemMaxFileSize=500M                        # Max 1 file
MaxRetentionSec=30day                         # Giữ 30 ngày
```

```bash
sudo systemctl restart systemd-journald
```

### Bạn debug crash FastAPI

```
Bạn: sudo systemctl status myapp.service
   Active: failed (Result: exit-code) since ...
   Process: 12345 ExecStart=... (code=exited, status=1)

Bạn: sudo journalctl -u myapp -n 50 --no-pager
   May 23 14:32:01 vps myapp[12345]: ImportError: No module named 'pydantic'

Bạn: ah, pip install pydantic
   sudo -u myapp /opt/myapp/venv/bin/pip install pydantic

Bạn: sudo systemctl restart myapp.service
   Active: active (running)
```

→ `status` + `journalctl` = 90% debug systemd service.

---

## 9️⃣ Timer units — Thay thế cron

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily database backup

[Service]
Type=oneshot
User=backup
ExecStart=/opt/scripts/backup-db.sh
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup daily at 2 AM
Requires=backup.service

[Timer]
OnCalendar=*-*-* 02:00:00            # Mỗi ngày 2:00
Persistent=true                        # Chạy nếu missed (server tắt)

[Install]
WantedBy=timers.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
sudo systemctl list-timers              # List all timers
```

### `OnCalendar=` syntax

| Pattern | Khi |
|---|---|
| `*-*-* 02:00:00` | Mỗi ngày 2:00 AM |
| `Mon..Fri *-*-* 09:00` | Thứ 2-6, 9 AM |
| `*-*-01 00:00` | Đầu mỗi tháng |
| `hourly` | Mỗi giờ |
| `daily` | Mỗi ngày 0:00 |
| `weekly` | Thứ 2 0:00 |

### Pros vs cron

| Aspect | cron | systemd timer |
|---|---|---|
| Syntax | `0 2 * * *` (khó nhớ) | `*-*-* 02:00:00` (rõ ràng) |
| Log integrate | ❌ (syslog riêng) | ✅ journalctl |
| Missed run | ❌ | ✅ `Persistent=true` |
| Dependencies | ❌ | ✅ `After=`, `Requires=` |
| Resource limit | ❌ | ✅ |

→ 2026: server modern dùng systemd timer. Cron còn cho legacy / personal script.

---

## ⚠️ 5 pitfall hay vướng

1. **Quên `daemon-reload`** sau sửa unit file → systemd vẫn dùng version cũ. Reload trước restart.
2. **`Type=simple` mà app tự fork** → systemd tưởng app exited, kill main → tắt. Dùng `Type=forking` cho daemon classic.
3. **`Restart=always` cho oneshot script** → script chạy xong exit → systemd restart → loop vô tận. Dùng `Restart=on-failure` hoặc bỏ.
4. **Permission ENV file** → secret 0644 (anyone read) → leak. `chmod 600 + chown service-user`.
5. **Hardening quá strict cho JIT app** (Python với extension, Node) → `MemoryDenyWriteExecute=true` block JIT → crash. Audit từng directive.

---

## ✅ Self-check

1. Vì sao systemd thay SysV init?
2. 3 section bắt buộc trong unit file?
3. Lệnh enable + start service?
4. Khác `Restart=always` và `Restart=on-failure`?
5. Đọc log của `myapp` 100 dòng cuối + filter ERROR?

<details>
<summary>Gợi ý đáp án</summary>

1. (a) Parallel boot 3-5x nhanh hơn. (b) Declarative dependency thay vì số thứ tự. (c) Auto-restart on crash. (d) Log integrate (journalctl). (e) Hardening built-in (`NoNewPrivileges=`, `ProtectSystem=`). (f) Timer thay cron.

2. **`[Unit]`** (metadata + dependency), **`[Service]`** (lệnh chạy + behavior), **`[Install]`** (target khi enable). `[Install]` không bắt buộc nếu chỉ start tay.

3. ```bash
   sudo systemctl daemon-reload    # Sau khi sửa file
   sudo systemctl enable myapp.service
   sudo systemctl start myapp.service
   ```

4. **`Restart=always`** restart **mọi** lần process exit (kể cả `systemctl stop` cũng restart liền — bạn không stop được!). **`Restart=on-failure`** chỉ restart khi exit code ≠ 0 hoặc crash. `unless-stopped` = always nhưng tôn trọng manual stop.

5. ```bash
   journalctl -u myapp -n 100 -p err
   # Hoặc follow:
   journalctl -u myapp -f --grep "error"
   ```
</details>

---

## ⚡ Cheatsheet

### `systemctl` daily

```bash
systemctl status myapp
systemctl start/stop/restart myapp
systemctl reload myapp
systemctl enable/disable myapp
systemctl is-active myapp
systemctl daemon-reload                    # Sau sửa unit file
systemctl list-units --type=service --state=failed
systemctl mask/unmask service               # Block hoàn toàn
```

### `journalctl` daily

```bash
journalctl -u myapp                        # All
journalctl -u myapp -f                      # Follow
journalctl -u myapp -n 50                   # Last 50
journalctl -u myapp --since "1h ago"
journalctl -u myapp -p err                  # Errors only
journalctl -u myapp --grep "pattern"
journalctl --disk-usage
```

### Unit file template

```ini
[Unit]
Description=My Service
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/run.sh
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
ProtectSystem=strict
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Timer template

```ini
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **systemd** | Init system + service manager mặc định Linux modern |
| **PID 1** | Process đầu tiên kernel start — là systemd |
| **Unit** | Đơn vị quản lý (service/timer/mount/socket/target) |
| **`.service`** | Unit type — app/daemon |
| **`.timer`** | Unit type — scheduled job (thay cron) |
| **`.target`** | Unit group (như "runlevel" cũ) |
| **`systemctl`** | CLI điều khiển systemd |
| **`journalctl`** | CLI đọc log từ journal |
| **`Restart=on-failure`** | Auto-restart khi crash |
| **`Type=simple/forking/oneshot/notify`** | Cách systemd track process |
| **`AmbientCapabilities=`** | Quyền cho process (vd bind port 80) |
| **`NoNewPrivileges=`** | Cấm escalate (block setuid) |
| **`ProtectSystem=strict`** | /usr, /boot read-only cho service |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Users & Permissions](00_users-and-permissions.md)
- → Tiếp: [SSH Deep Dive](02_ssh-deep-dive.md)
- ↑ Cluster: [linux README](../../README.md)

### Cross-reference
- [FastAPI auth + middleware](../../../../07_Web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md) — backend cần systemd để run
- [Docker compose](../../../../10_DevOps/docker/lessons/01_basic/03_docker-compose.md) — alternative tới systemd cho container

### External
- 📖 [systemd man pages](https://man7.org/linux/man-pages/man1/systemd.1.html)
- 📖 [DigitalOcean: systemctl essentials](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
- 📖 [Arch wiki: systemd](https://wiki.archlinux.org/title/Systemd) — best resource
- 📖 [Systemd Service Hardening — RHEL](https://access.redhat.com/sysadmin/mastering-systemd)
- 📖 [systemd-analyze security](https://www.freedesktop.org/software/systemd/man/systemd-analyze.html#security%20%5BUNIT...%5D)

---

> 🎯 *Sau bài này FastAPI của bạn chạy 24/7 production-grade. Bài kế tiếp dạy **SSH deep dive** — config, key types, tunneling, agent forwarding — quản lý server từ xa.*

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm ẩn dụ "quản gia cao cấp" cho systemd, 2 lead-in trước bảng concepts + so sánh SysV/systemd. Fix grammar "FastAPI Bạn" → "FastAPI của bạn".
