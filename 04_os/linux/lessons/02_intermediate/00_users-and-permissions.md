# 🎓 Users & Permissions — chmod, chown, sudo, SUID, capabilities

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Linux Navigation](../01_basic/01_navigation.md), [File Operations](../01_basic/02_file-operations.md)

> 🎯 *Hiểu **user/group**, **3 quyền rwx** + **octal 755**, **chmod/chown/umask**, **sudo** vs root, **SUID/SGID/sticky bit**, và **capabilities** (modern alternative SUID). Sau bài này bạn đọc/viết được `ls -l` output + config permission server an toàn.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **user vs group vs other** (3-tier permission)
- [ ] Đọc được output `ls -l` (`-rwxr-xr-x` = ?)
- [ ] Tính được **octal** notation (`755`, `644`, `600`)
- [ ] Dùng `chmod` + `chown` + `chgrp` đúng
- [ ] Hiểu **`umask`** — default permission khi tạo file mới
- [ ] Sudo vs root + cấu hình `/etc/sudoers`
- [ ] Hiểu **SUID/SGID/sticky bit** + khi nào dùng
- [ ] Biết về **`capabilities`** (cap_net_bind, cap_sys_admin...) — thay SUID hiện đại

---

## Tình huống — Bạn deploy FastAPI lên VPS

Bạn deploy backend FastAPI ([cluster trước](../../../../07_web/backend/python-fastapi/)) lên VPS Ubuntu. Server có sẵn user `ubuntu`. Bạn copy code:

```bash
ubuntu@vps:~$ scp -r myapp/ vps:/home/ubuntu/

ubuntu@vps:~$ cd myapp && fastapi run main.py --port 80
Permission denied
# port < 1024 cần root!

ubuntu@vps:~$ sudo fastapi run main.py --port 80
# OK nhưng chạy as root → nguy hiểm
```

Bạn ngơ:
- **Port 80** sao cần `sudo`?
- Chạy backend as **root** thì sao?
- Có cách nào "non-root nhưng vẫn bind port 80"?
- Quyền `rwx` đọc sao? Số `755` nghĩa là gì?
- Sao log file thư mục bạn không xem được mà user `www-data` xem được?

→ Bài này dạy bạn (và bạn) **Linux permission system** đầy đủ.

---

## 1️⃣ User và Group — 3-tier permission

Linux phân quyền theo **3 nhóm**:

| Tier | Ai | Symbol |
|---|---|---|
| **Owner / User** | Người sở hữu file | `u` |
| **Group** | Group sở hữu file | `g` |
| **Others / Everyone** | Mọi người khác | `o` |

Mỗi nhóm có **3 quyền** riêng:

| Quyền | Đọc / file | Đọc / dir |
|---|---|---|
| **r** (read) | Đọc nội dung | List files trong dir |
| **w** (write) | Ghi/sửa | Tạo/xoá file trong dir |
| **x** (execute) | Chạy như script/binary | **cd** vào dir |

→ Quyền dir khác file. `x` trên dir = "cho phép cd vào", không phải "execute dir".

### Xem permission — `ls -l`

🪞 **Ẩn dụ**: *Output `ls -l` như **biên lai mua hàng** — mỗi cột là 1 thông tin khác (loại, quyền, chủ, kích thước, ngày). Đọc quen rồi, lướt mắt qua biết ngay file nào của ai, ai được xem.*

Gõ `ls -l` trong terminal sẽ hiện chi tiết mỗi file/folder thành 1 dòng. Mỗi dòng có 7 cột — xem ví dụ + sơ đồ chú thích:

```bash
$ ls -l
-rw-r--r-- 1 user admin  1024 May 23 14:00 readme.txt
drwxr-xr-x 2 user admin   512 May 23 14:00 myproject/
-rwxr-xr-x 1 root root  98432 May 22 10:00 /usr/bin/python3
└──┬───┘ │ │ └┬┘ └─┬─┘ └─┬──┘ └────────┘ └──┬──────┘
   │     │ │  │    │    │       │           └ tên file
   │     │ │  │    │    │       └ ngày sửa
   │     │ │  │    │    └ size
   │     │ │  │    └ group
   │     │ │  └ owner
   │     │ └ số hard link
   │     └ type: -, d, l, c, b
   └ permission 9 bit
```

### Đọc 10 ký tự đầu

```
-rwxr-xr-x
│└┬┘└┬┘└┬┘
│ │  │  └ Others:  r-x  → đọc + execute, không write
│ │  └── Group:    r-x  → đọc + execute
│ └───── Owner:    rwx  → đọc + write + execute
└─────── Type:     -    → file thường ('d'=dir, 'l'=link)
```

| Type | Ý nghĩa |
|---|---|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `c` | Character device (`/dev/tty`) |
| `b` | Block device (`/dev/sda`) |
| `s` | Socket |
| `p` | Named pipe (FIFO) |

---

## 2️⃣ Octal notation — số 3 chữ số

🪞 **Ẩn dụ**: *Octal như **mật mã 3 số**: 1 số cho chủ nhà, 1 số cho người trong nhóm, 1 số cho khách lạ. Mỗi số mã hoá 3 quyền (đọc/ghi/chạy) thành 1 chữ số 0-7.*

3 quyền `rwx` mỗi cái là 1 bit. Gộp lại = 3 bit = số từ 0-7 (octal — hệ cơ số 8):
- `r` (đọc) = 4
- `w` (ghi) = 2
- `x` (chạy) = 1

Cộng 3 giá trị này tuỳ tổ hợp quyền → ra 8 mã có thể. Bảng dưới enumerate toàn bộ:

| Symbol | Binary | Octal |
|---|---|---|
| `---` | 000 | 0 |
| `--x` | 001 | 1 |
| `-w-` | 010 | 2 |
| `-wx` | 011 | 3 |
| `r--` | 100 | 4 |
| `r-x` | 101 | 5 |
| `rw-` | 110 | 6 |
| `rwx` | 111 | 7 |

→ 3 nhóm (owner/group/other) × 3 bit = **9 bit** = **3 số octal**.

### Permission phổ biến

Không phải mọi tổ hợp octal đều thường dùng. Trong thực tế, 7 mã dưới đây xuất hiện 95% trường hợp — học thuộc:

| Octal | Symbolic | Dùng cho |
|---|---|---|
| `755` | `rwxr-xr-x` | Script + binary + folder code |
| `644` | `rw-r--r--` | File text (config, readme) |
| `600` | `rw-------` | Secret (private key SSH, `.env`) |
| `700` | `rwx------` | Private folder (`~/.ssh`) |
| `666` | `rw-rw-rw-` | World writable — nguy hiểm |
| `777` | `rwxrwxrwx` | RẤT NGUY HIỂM — không nên dùng |
| `400` | `r--------` | Read-only secret (key cert) |

> ⚠️ **`chmod 777` = thảm hoạ bảo mật**. Bất kỳ user nào đều ghi đè được. Trừ debug nhanh trong dev container, **đừng dùng**.

---

## 3️⃣ `chmod` — Đổi permission

### Octal (recommended cho script)

```bash
chmod 755 myscript.sh                   # rwxr-xr-x
chmod 600 ~/.ssh/id_rsa                  # rw-------
chmod 644 readme.md                      # rw-r--r--
chmod -R 755 myproject/                  # recursive
```

### Symbolic (recommended cho 1-off đổi)

```bash
chmod u+x script.sh                      # Thêm execute cho owner
chmod g-w file.txt                       # Bỏ write của group
chmod o=r file.txt                       # Set others = chỉ read
chmod a+r file.txt                       # All (u+g+o) thêm read
chmod ug+rwx,o-rwx data/                 # Kết hợp
```

| Symbol | Meaning |
|---|---|
| `u` / `g` / `o` / `a` | user / group / other / all |
| `+` / `-` / `=` | add / remove / set exactly |
| `r` / `w` / `x` | read / write / execute |

### Recursive với loại file

```bash
# Cấu trúc: dir 755, file 644
find ./project -type d -exec chmod 755 {} \;
find ./project -type f -exec chmod 644 {} \;
```

→ Cẩn thận `-R` trên permission khác nhau (dir cần `x`, file thường không).

---

## 4️⃣ `chown` & `chgrp` — Đổi owner / group

```bash
chown user file.txt                      # Đổi owner = user
chown user:admin file.txt                # Đổi owner=long, group=admin
chown :admin file.txt                    # Chỉ đổi group
chgrp admin file.txt                     # Tương đương trên
chown -R www-data:www-data /var/www/     # Recursive — web server owner
```

→ Đổi owner cần **root** (`sudo`). User thường không thể "give file" sang user khác.

---

## 5️⃣ `umask` — Default permission khi tạo file mới

Khi `touch file.txt`, file mới có permission gì?

```
Max permission file: 666 (rw-rw-rw-)
Max permission dir:  777 (rwxrwxrwx)
umask:               022 (default Ubuntu)
File default:        666 - 022 = 644 (rw-r--r--)
Dir default:         777 - 022 = 755 (rwxr-xr-x)
```

→ `umask 022` là **default** modern Linux. Production safer: `umask 027` → file `640`, dir `750` (others không đọc).

### Set umask

```bash
umask                                    # Show current
umask 027                                # Set strict cho session
# Permanent: thêm vào ~/.bashrc hoặc /etc/profile
```

---

## 6️⃣ `sudo` vs root — phân quyền admin

### Root vs sudo

| Concept | Mô tả |
|---|---|
| **root** | User UID 0 — toàn quyền hệ thống |
| **`sudo`** | Run lệnh **as root** với password user (không cần root password) |
| **`su`** | Switch user — `su -` = switch sang root (cần root password) |

→ **2026 best practice**: **DISABLE root login**, mọi admin task dùng `sudo`. Audit trail: log mọi `sudo` vào `/var/log/auth.log`.

### Cấu hình `/etc/sudoers`

```
# /etc/sudoers
root    ALL=(ALL:ALL) ALL
%admin  ALL=(ALL) ALL                    # group admin → sudo full
%sudo   ALL=(ALL:ALL) ALL                # group sudo → sudo full

# User cụ thể với rule riêng
deploy  ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart myapp
        # ↑ deploy không cần password chỉ cho 1 command
```

→ **Luôn edit qua `visudo`** (kiểm tra syntax trước save). `sudo nano /etc/sudoers` = nguy hiểm (lỗi syntax = lock-out!).

### `sudo` 3 cách dùng

```bash
sudo apt update                          # Run 1 command as root
sudo -i                                  # Shell login as root (giữ env root)
sudo -u www-data ls /var/log/nginx/      # Run as user khác (không phải root)
```

### Trace audit

```bash
# Mọi sudo log vào auth.log
sudo grep sudo /var/log/auth.log

# Last 20 sudo
sudo last | head -20
```

---

## 7️⃣ SUID / SGID / Sticky bit — special permission

### SUID (Set User ID)

```bash
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd
   ↑
   's' instead of 'x' → SUID set
```

→ User thường chạy `passwd` → process **chạy as root** (effective UID = file owner). Cần để update `/etc/shadow` (chỉ root đọc/ghi).

```bash
chmod u+s file       # Set SUID
chmod 4755 file      # Octal: 4 = SUID, 755 = rwxr-xr-x
```

### SGID (Set Group ID)

```bash
$ ls -l /usr/bin/wall
-rwxr-sr-x 1 root tty ... /usr/bin/wall
        ↑
        's' on group → SGID
```

→ Process chạy with effective GID = group của file. Cũng dùng cho **shared directories** — file mới trong dir tự inherit group của dir.

### Sticky bit

```bash
$ ls -ld /tmp
drwxrwxrwt 11 root root ... /tmp
         ↑
         't' instead of 'x' → sticky bit
```

→ `/tmp` mọi user ghi vào nhưng **chỉ owner xoá được file mình** (others không thể xoá file của người khác). Mỗi user 1 ngăn riêng.

```bash
chmod +t /shared/dir       # Set sticky bit
chmod 1777 /shared/dir     # Octal: 1=sticky
```

### Tổng kết octal đầu

```
Format chmod 4 số: ABCD
A = SUID(4) + SGID(2) + sticky(1)
B = owner rwx
C = group rwx
D = other rwx

VD:
4755 = SUID + rwxr-xr-x
2755 = SGID + rwxr-xr-x
1777 = sticky + rwxrwxrwx (như /tmp)
```

### ⚠️ SUID nguy hiểm

```bash
# Tìm SUID binary lạ — có thể là backdoor
find / -perm -4000 -type f 2>/dev/null
```

→ Audit định kỳ. SUID binary tùy chỉnh = **backdoor** thường gặp khi server bị hack.

---

## 8️⃣ Capabilities — Modern alternative SUID

**Problem**: SUID = "give root toàn bộ". Quá nhiều quyền. Nếu binary bị lỗ hổng → toàn root.

**Solution (Linux 2.2+)**: **Capabilities** — chia root thành ~38 quyền nhỏ. Cho binary chỉ quyền nó cần.

### Vài capability quan trọng

| Capability | Cho phép |
|---|---|
| `CAP_NET_BIND_SERVICE` | Bind port < 1024 |
| `CAP_NET_RAW` | Raw socket (ping, tcpdump) |
| `CAP_SYS_ADMIN` | Hầu hết "admin" actions (~root toàn quyền) |
| `CAP_DAC_OVERRIDE` | Bypass file permission |
| `CAP_KILL` | Kill mọi process |
| `CAP_CHOWN` | Đổi owner file |

### Bạn fix port 80 — không cần root

```bash
# Cho binary fastapi quyền bind port < 1024, KHÔNG cần root
sudo setcap 'cap_net_bind_service=+ep' $(which python3)

# Giờ user thường chạy
python3 -m fastapi run main.py --port 80
# OK, bind 80 thành công, KHÔNG là root
```

→ **Best practice** thay vì `sudo` toàn bộ. Process chỉ có quyền bind port — không quyền khác.

### Xem + xoá

```bash
getcap /usr/bin/python3                  # Xem
setcap -r /usr/bin/python3               # Xoá
```

### Nginx, Caddy, FastAPI tự dùng

```bash
$ getcap /usr/sbin/nginx
/usr/sbin/nginx cap_net_bind_service=ep
```

→ Cài qua package manager đã set sẵn. User tự build thì cần `setcap` tay.

---

## 9️⃣ Bạn deploy FastAPI an toàn

### ❌ Cũ — chạy as root

```bash
sudo fastapi run main.py --port 80
# Process là root → app crash = exploit có thể root cả server
```

### ✅ Mới — dedicated user + capability

```bash
# 1. Tạo user dedicated
sudo useradd -r -s /sbin/nologin myapp     # -r: system user, -s: no login shell

# 2. Đặt code thuộc user này
sudo chown -R myapp:myapp /opt/myapp/

# 3. Cho Python bind port 80
sudo setcap 'cap_net_bind_service=+ep' /opt/myapp/venv/bin/python3

# 4. Chạy as myapp (systemd làm trong bài kế tiếp)
sudo -u myapp /opt/myapp/venv/bin/fastapi run main.py --port 80
```

→ Process chạy as `myapp` (non-root), nhưng vẫn bind 80. App crash = exploit chỉ giới hạn user `myapp`, không root.

→ Production thực: chạy qua **systemd service** (bài 01 cluster này).

---

## ⚠️ 5 pitfall hay vướng

1. **`chmod 777` để "fix permission lỗi"** → tạm fix nhưng mở toang. Audit/staging server bị flag bảo mật. Tìm root cause: owner sai? umask sai?
2. **Quên `x` trên dir** → user có `r` trên dir cũng không list/cd được. Dir cần **cả `r` và `x`**.
3. **`sudo nano /etc/sudoers`** → lỗi syntax = mất quyền sudo, lock-out. **Luôn dùng `visudo`** (check syntax trước save).
4. **Chạy service as root** → app exploit = toàn server. Dedicated user + capabilities.
5. **Quên umask** trong shell script → file tạo permission khác nhau giữa dev và prod. Set explicit `chmod` sau create.

---

## ✅ Self-check

1. Đọc `ls -l` thấy `-rwxr-xr--`. Owner làm gì được? Group? Other?
2. `chmod 750` = symbolic gì?
3. Sao port < 1024 cần root? Cách workaround non-root?
4. Khác `sudo` và `su`?
5. SUID có gì khác SGID?

<details>
<summary>Gợi ý đáp án</summary>

1. `-rwxr-xr--` = owner `rwx` (read+write+execute), group `r-x` (read+execute), other `r--` (read only). File thường (`-`), không phải dir.

2. `750` = `7` (owner rwx) + `5` (group r-x) + `0` (other ---) = `rwxr-x---`.

3. Port < 1024 = well-known, **reserved cho root** (truyền thống Unix — chống user thường giả service). Workaround: (a) **capabilities** `setcap cap_net_bind_service=+ep`, (b) reverse proxy (Nginx) bind 80, forward sang FastAPI port 8000, (c) chạy service via systemd với `AmbientCapabilities=`.

4. **`sudo`** = run 1 command as another user (default: root), cần **password user**. **`su`** = switch user (full shell), cần **password user đích** (mặc định root). Modern Linux: prefer `sudo` (audit trail tốt, không cần biết root password).

5. **SUID** = run as **file owner** (thường root). **SGID** trên binary = run as **file group**. **SGID trên dir** = file mới tạo trong dir tự inherit group của dir (shared workspace pattern).
</details>

---

## ⚡ Cheatsheet

### Phép tính octal

```
r=4, w=2, x=1
755 = rwx r-x r-x
644 = rw- r-- r--
600 = rw- --- ---
700 = rwx --- ---
```

### Thường dùng

```bash
chmod 755 script.sh       chown user:admin file
chmod 600 ~/.ssh/id_rsa   chown -R www:www /var/www
chmod 644 config.json     chgrp admin file
chmod u+x file            umask 022
chmod a-w sensitive       umask 027 (strict)
```

### Sudo

```bash
sudo command              sudo visudo
sudo -i                   sudo -u www-data ls
sudo -k                   (revoke sudo cache)
```

### SUID/SGID/Sticky

```bash
chmod 4755 file           # SUID
chmod 2755 file           # SGID
chmod 1777 dir            # Sticky (/tmp)
find / -perm -4000 -type f 2>/dev/null   # SUID audit
```

### Capabilities

```bash
sudo setcap 'cap_net_bind_service=+ep' /path/binary
getcap /path/binary
setcap -r /path/binary
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **UID / GID** | User / Group ID (root = 0, system users < 1000, regular ≥ 1000) |
| **`rwx`** | Read / Write / Execute |
| **`u` / `g` / `o` / `a`** | User / Group / Other / All |
| **Octal permission** | `755` = `rwxr-xr-x` |
| **`umask`** | Default permission mask cho file/dir mới |
| **`sudo`** | Run 1 command as another user |
| **`/etc/sudoers`** | Config file sudo, edit qua `visudo` |
| **SUID / SGID** | Special bit — run as file owner/group |
| **Sticky bit** | Chỉ owner xoá file của mình trong dir |
| **Capabilities** | Quyền root chia nhỏ — modern alternative SUID |
| **`setcap` / `getcap`** | Tool quản lý capabilities |
| **System user** | UID < 1000, không login shell, run service |

---

## 🔗 Links

### Trong cluster
- → Tiếp: [systemd Services](01_systemd-services.md)
- ↑ Cluster: [linux README](../../README.md)

### Cross-reference
- [TCP/IP ports/sockets/firewall](../../../../05_networking/tcp-ip-fundamentals/lessons/01_basic/03_ports-sockets-firewall.md) — port < 1024 cần root/capability
- [FastAPI auth](../../../../07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md) — backend dedicated user

### External
- 📖 [Linux man page: chmod(1)](https://man7.org/linux/man-pages/man1/chmod.1.html)
- 📖 [Capabilities(7) man page](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- 📖 [SUID/SGID/Sticky bits explained — DigitalOcean](https://www.digitalocean.com/community/tutorials/linux-permissions-basics-and-how-to-use-umask-on-a-vps)
- 📖 [sudo manual + advanced sudoers — Ubuntu wiki](https://help.ubuntu.com/community/RootSudo)

---

> 🎯 *Sau bài này bạn config permission server an toàn. Bài kế tiếp dạy **systemd** — biến FastAPI thành service tự khởi động + restart khi crash.*

## 📌 Changelog

- **v1.1.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm 2 ẩn dụ (biên lai mua hàng cho `ls -l`, mật mã 3 số cho octal), 3 lead-in trước bảng (permission, octal table, permission phổ biến), thay username fictional `long` → `rom`.
