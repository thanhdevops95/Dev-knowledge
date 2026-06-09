# 🎓 SSH Deep Dive — Keys, Config, Tunneling, Agent

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.2.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [Users & Permissions](00_users-and-permissions.md)

> 🎯 *SSH > basic. Học **key types** (RSA/ed25519), **`~/.ssh/config`** chuẩn, **SSH agent** (đỡ gõ passphrase), **tunneling** (local/remote/dynamic), **`scp`/`rsync`/`sshfs`** transfer file, **hardening** server (disable root, fail2ban), **debug** SSH lỗi.*

## 🎯 Sau bài này bạn sẽ

- [ ] Sinh **key pair ed25519** (modern, an toàn nhất)
- [ ] Setup **passwordless login** với `ssh-copy-id`
- [ ] Viết **`~/.ssh/config`** quản lý nhiều server (alias)
- [ ] Dùng **SSH agent** (đỡ gõ passphrase mỗi lần)
- [ ] **Agent forwarding** (-A) — SSH chain qua bastion
- [ ] **Tunnel local** (-L) — expose remote port lên local
- [ ] **Tunnel remote** (-R) — expose local port ra Internet
- [ ] **SOCKS proxy** (-D) — proxy mọi traffic qua SSH
- [ ] Transfer file: `scp`, `rsync`, `sshfs`
- [ ] Hardening server SSH (`PermitRootLogin no`, `PasswordAuthentication no`)
- [ ] Debug SSH với `-v` verbose

---

## Tình huống — bạn quản lý 5 server, gõ password mệt

Bạn đã có 5 VPS:
- `vps1.acmeshop.vn` (web)
- `vps2.acmeshop.vn` (DB)
- `vps3.acmeshop.vn` (cache)
- 1 dev server qua VPN
- 1 bastion server vào prod

Bạn mỗi sáng:
```bash
ssh user@vps1.acmeshop.vn         # Type password
ssh user@vps2.acmeshop.vn          # Type password
ssh user@vps3.acmeshop.vn          # Type password
# Quên IP DB...
```

Bạn ngơ:
- **Password auth** nguy hiểm — brute force được. Sao chuyển sang **SSH key**?
- Quản lý **5+ server** sao đỡ gõ host name?
- Vào prod phải qua **bastion** — chain SSH ra sao?
- Cần truy cập **Postgres trên VPS từ máy local** mà không expose port — **tunnel** ra sao?
- Backup file từ local lên VPS — `scp` hay `rsync`?

→ Bài này dạy SSH đầy đủ cho devops thường.

---

## 1️⃣ SSH key types — chọn loại nào?

### 4 thuật toán phổ biến

🪞 **Ẩn dụ**: *SSH key như **bộ chìa khoá cao cấp** — có nhiều loại (cũ kích thước to, mới kích thước nhỏ nhưng chắc hơn). Năm 2026 nên dùng **Ed25519** — chìa khoá nhỏ + an toàn nhất, dễ mang theo.*

SSH hỗ trợ 4 thuật toán mã hoá khoá khác nhau, mỗi cái sinh năm khác + độ an toàn khác. Bảng dưới chọn 1 cái dùng:

| Type | Năm | Key size | Status 2026 |
|---|---|---|---|
| **RSA** | 1977 | 2048-4096 bit | OK nhưng cũ |
| **DSA** | 1991 | 1024 bit (cap) | ❌ Deprecated |
| **ECDSA** | 2001 | 256-521 bit | OK |
| **Ed25519** | 2014 | 256 bit | ✅ **Recommended 2026** |

→ **Default 2026**: **ed25519**. Nhanh nhất, an toàn nhất, key ngắn nhất.

### Sinh key

Lệnh `ssh-keygen` tạo cặp public/private key. Tham số `-t` chọn thuật toán (ed25519 là khuyến nghị 2026), `-C` thêm "comment" để nhận biết key thuộc máy nào:

```bash
# Modern (recommended)
ssh-keygen -t ed25519 -C "user@laptop"

# Legacy compat (nếu server cũ không support ed25519)
ssh-keygen -t rsa -b 4096 -C "user@laptop"
```

Default location: `~/.ssh/id_ed25519` (private) + `~/.ssh/id_ed25519.pub` (public).

### Passphrase — bắt buộc?

```
Enter passphrase (empty for no passphrase):
```

→ **Có passphrase** = thêm 1 lớp bảo vệ (key file bị steal vẫn cần passphrase). Combine với **SSH agent** = chỉ gõ 1 lần / session.

→ **Không passphrase** = tiện cho script auto/CI/CD. Bù lại = key file phải `chmod 600 + chown user` + filesystem encrypt.

### File permission BẮT BUỘC

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519              # Private key
chmod 644 ~/.ssh/id_ed25519.pub          # Public key
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/config
```

→ SSH **từ chối** dùng key nếu permission rộng hơn (security feature).

---

## 2️⃣ Passwordless login — `ssh-copy-id`

### Workflow

1. Sinh key tại laptop: `ssh-keygen -t ed25519`
2. Copy public key lên server: `ssh-copy-id user@vps`
3. SSH = không hỏi password nữa.

```bash
$ ssh-copy-id user@vps1.acmeshop.vn
# Sẽ hỏi password 1 lần để copy
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/user/.ssh/id_ed25519.pub"
user@vps1.acmeshop.vn's password: ********

Number of key(s) added: 1

$ ssh user@vps1.acmeshop.vn       # Không password nữa!
```

### Behind scene

`ssh-copy-id` thêm public key vào `~/.ssh/authorized_keys` trên server:

```bash
# Trên server vps1
$ cat ~/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@laptop
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user@laptop      # ← thêm key 2
```

→ Mỗi dòng = 1 key được phép login.

### Manual copy (nếu không có `ssh-copy-id`)

```bash
cat ~/.ssh/id_ed25519.pub | ssh user@vps "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

---

## 3️⃣ `~/.ssh/config` — Quản lý nhiều server

### Viết config

```
# ~/.ssh/config

Host vps1
    HostName vps1.acmeshop.vn
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host vps2
    HostName 198.51.100.22
    User deploy
    Port 2222
    IdentityFile ~/.ssh/id_vps2_specific

Host prod-*
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519_prod
    ProxyJump bastion

Host bastion
    HostName bastion.acmeshop.vn
    User deploy

Host github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
```

### Dùng

```bash
ssh vps1                                  # = ssh user@vps1.acmeshop.vn:22
ssh vps2                                   # = ssh user@198.51.100.22:2222
ssh prod-web                                # = ssh deploy@prod-web qua bastion
scp file.tar prod-web:/tmp/                 # scp dùng alias luôn
git clone github.com:user/repo.git          # git dùng SSH config
```

### Directive thường dùng

| Directive | Ý nghĩa |
|---|---|
| `HostName` | DNS/IP thực |
| `User` | Username trên server |
| `Port` | Port (default 22) |
| `IdentityFile` | Key file dùng |
| `IdentitiesOnly yes` | CHỈ dùng IdentityFile, không thử key khác |
| `ProxyJump bastion` | Chain qua bastion |
| `ServerAliveInterval 60` | Send keepalive mỗi 60s |
| `StrictHostKeyChecking accept-new` | Auto-accept fingerprint lần đầu |
| `ControlMaster auto` | Reuse connection (mở nhanh hơn) |
| `ControlPath ~/.ssh/cm-%r@%h:%p` | Path socket reuse |

### Wildcard pattern

```
Host prod-*
    User deploy
    ProxyJump bastion

Host *
    ServerAliveInterval 60
    AddKeysToAgent yes
```

→ Match `prod-web`, `prod-db`, `prod-cache`... Cuối cùng `Host *` apply cho TẤT CẢ (đặt cuối).

---

## 4️⃣ SSH Agent — chỉ gõ passphrase 1 lần

Passphrase mỗi connection = phiền. **SSH agent** giữ unlocked key trong memory.

### Start agent

```bash
eval "$(ssh-agent -s)"               # Start agent (Mac/Linux thường có sẵn)
ssh-add ~/.ssh/id_ed25519             # Add key (hỏi passphrase 1 lần)
ssh-add -l                             # List loaded keys
ssh-add -D                             # Xoá tất cả (logout)
```

### Mac — Keychain integrate

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

→ Mac lưu passphrase vào Keychain → reboot không phải gõ lại.

### `~/.ssh/config` auto-add

```
Host *
    AddKeysToAgent yes
    UseKeychain yes              # Mac
    IdentityFile ~/.ssh/id_ed25519
```

→ Lần đầu connect, SSH tự add key vào agent. Sau đó không hỏi passphrase.

---

## 5️⃣ Agent forwarding (`-A`) — Chain SSH qua bastion

**Vấn đề**: bạn ssh vào bastion → từ bastion ssh tiếp vào prod. Prod cần SSH key của bạn, nhưng **key đang ở laptop**, không nên copy lên bastion (single point of failure).

**Solution**: **Agent forwarding** — forward SSH agent vào bastion. Prod hỏi key → bastion forward về laptop → laptop ký.

```bash
ssh -A user@bastion           # Agent forwarded
[bastion]$ ssh deploy@prod    # Dùng key từ laptop qua forward
[prod]$                        # Logged in OK
```

### Config

```
Host bastion
    HostName bastion.acmeshop.vn
    ForwardAgent yes
```

→ `ForwardAgent yes` thay `-A` flag mỗi lần.

### `ProxyJump` (-J) — Cách MỚI tốt hơn

```bash
ssh -J bastion deploy@prod
```

→ Hoặc trong config:

```
Host prod
    HostName prod.acmeshop.vn
    User deploy
    ProxyJump bastion
```

→ `ProxyJump` = SSH connect bastion → từ bastion làm TCP forwarder tới prod → laptop SSH thẳng prod. **An toàn hơn ForwardAgent** (không expose agent ra bastion).

### So sánh

| Cách | Pros | Cons |
|---|---|---|
| `ForwardAgent yes` | Đơn giản | Bastion bị hack = stole agent (impersonate được mọi server) |
| `ProxyJump` | **Recommended** — bastion chỉ là forwarder, không thấy agent | |

→ **2026 best practice**: `ProxyJump`. `ForwardAgent` khi cần cụ thể (git on remote).

---

## 6️⃣ SSH Tunneling — 3 loại

### Local forward (`-L`) — Map remote port lên local

**Use case**: DB Postgres trên VPS chỉ listen `127.0.0.1:5432` (an toàn). Bạn muốn dùng pgAdmin GUI từ laptop.

```bash
ssh -L 5432:localhost:5432 user@vps
```

→ Laptop `localhost:5432` ↔ tunnel SSH ↔ vps `localhost:5432`. pgAdmin connect `127.0.0.1:5432` → thực ra hit Postgres trên vps. **Không cần expose Postgres ra Internet**.

```bash
# Background tunnel (-N: không exec command, -f: fork)
ssh -fN -L 5432:localhost:5432 user@vps
```

### Remote forward (`-R`) — Expose local lên remote

**Use case**: app local `localhost:3000` (dev), muốn cho team trên Internet thử.

```bash
ssh -R 8080:localhost:3000 user@vps
```

→ Trên vps, ai connect `localhost:8080` (hoặc public IP nếu `GatewayPorts yes`) → thực ra hit `localhost:3000` của laptop bạn.

→ Alternative hiện đại: **ngrok**, **Cloudflare tunnel** (zero-config).

### Dynamic / SOCKS proxy (`-D`) — Proxy mọi traffic qua SSH

```bash
ssh -D 1080 user@vps
```

→ Laptop có SOCKS5 proxy ở `127.0.0.1:1080`. Config browser dùng proxy → mọi traffic đi qua vps. **VPN nhanh không cần setup OpenVPN**.

```
Browser → SOCKS proxy 127.0.0.1:1080 → SSH tunnel → vps → Internet
```

→ Hữu ích bypass geo-block, public Wi-Fi không an toàn, dev access internal network từ home.

---

## 7️⃣ File transfer — `scp`, `rsync`, `sshfs`

### `scp` — Đơn giản, basic

```bash
scp file.txt vps:/tmp/                       # Upload
scp vps:/var/log/app.log ./                  # Download
scp -r ./project/ vps:/home/user/             # Recursive directory
scp -P 2222 file vps:/tmp                     # Custom port
```

> ⚠️ **OpenSSH 9.0+ (2022)**: `scp` đang **deprecated** — chuyển sang `sftp` hoặc `rsync`. Nhưng vẫn dùng được trong UX vài năm tới.

### `rsync` — Mạnh nhất, mọi devops yêu

```bash
rsync -avz ./project/ vps:/opt/myapp/         # Sync (-a archive, -v verbose, -z compress)
rsync -avz --delete ./project/ vps:/opt/myapp/    # Delete file thừa ở đích
rsync -avz --exclude="*.log" --exclude="node_modules" ./project/ vps:/opt/myapp/
rsync --progress -avz huge.tar vps:/tmp/      # Show progress
rsync -avz vps:/var/log/ ./logs/              # Reverse (pull)
```

**Power feature**: chỉ transfer **delta** (phần thay đổi) — sync 10GB → đổi 1MB → chỉ gửi 1MB.

### `sshfs` — Mount remote folder như local

```bash
sshfs vps:/opt/myapp/ ~/mnt/myapp
cd ~/mnt/myapp && ls                          # Truy cập như local
fusermount -u ~/mnt/myapp                     # Unmount (Linux)
umount ~/mnt/myapp                            # Unmount (Mac)
```

→ Dùng editor local (VS Code) edit file trên server. Latency cao nhưng tiện.

### So sánh

| Tool | Pros | Cons |
|---|---|---|
| `scp` | Đơn giản | Slow, deprecated |
| `rsync` | **Best — delta + resume + flexible** | Cú pháp phức tạp |
| `sshfs` | Truy cập như local | Slow, latency cao |
| `sftp` | Interactive (như FTP) | Manual file by file |

---

## 8️⃣ Hardening SSH server

```
# /etc/ssh/sshd_config

# 1. Đổi port (security through obscurity — chỉ bonus, không thay key)
Port 2222

# 2. Disable root login
PermitRootLogin no

# 3. Disable password auth — KEY ONLY
PasswordAuthentication no
PubkeyAuthentication yes

# 4. Disable empty password
PermitEmptyPasswords no

# 5. Limit user
AllowUsers user deploy
# Hoặc:
# AllowGroups ssh-users

# 6. Idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# 7. Max auth retry
MaxAuthTries 3

# 8. Disable forwarding nếu không cần
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no                       # nếu không cần tunnel

# 9. Modern crypto only
KexAlgorithms curve25519-sha256@libssh.org
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
```

Reload:
```bash
sudo sshd -t                                  # Test config
sudo systemctl reload sshd                    # Reload
```

> ⚠️ **CỰC KỲ CẨN THẬN**: edit `sshd_config` mà sai → mất quyền SSH → lock-out. **Luôn giữ 1 SSH session active** trong khi reload + test bằng session **MỚI** trước khi close.

### `fail2ban` — Tự ban IP brute force

```bash
sudo apt install fail2ban
sudo systemctl enable --now fail2ban
```

→ Default config: 5 lần SSH fail trong 10 phút → ban IP 10 phút.

### Custom jail — `/etc/fail2ban/jail.local`

```ini
# Tránh edit jail.conf trực tiếp — bị ghi đè khi upgrade
[DEFAULT]
bantime  = 1h                            # Ban 1 giờ
findtime = 10m                            # Đếm trong 10 phút
maxretry = 5                              # 5 lần fail = ban
ignoreip = 127.0.0.1/8 ::1 1.2.3.4        # Không ban IP văn phòng

[sshd]
enabled = true
port    = 22
logpath = /var/log/auth.log              # Debian/Ubuntu
                                          # = /var/log/secure (RHEL)
backend = systemd                          # journalctl thay text file (modern)
```

→ Reload: `sudo systemctl restart fail2ban`.

### Commands hữu ích

```bash
sudo fail2ban-client status                  # Tổng quan: jail nào active
sudo fail2ban-client status sshd             # Chi tiết SSH jail
sudo fail2ban-client banned                  # IP đang bị ban
sudo fail2ban-client set sshd unbanip 1.2.3.4   # Unban thủ công
sudo fail2ban-client set sshd banip 5.6.7.8     # Ban thủ công

# Xem log
sudo tail -f /var/log/fail2ban.log
```

→ Best practice: **whitelist IP văn phòng + VPN** trong `ignoreip` để không bị ban nhầm. Bantime tăng dần (`bantime.increment = true`) cho repeat offender.

---

## 9️⃣ Debug SSH lỗi — `-v` verbose

```bash
ssh -v user@host                              # Verbose level 1
ssh -vv user@host                              # Level 2 (chi tiết hơn)
ssh -vvv user@host                             # Level 3 (max)
```

Output ví dụ:
```
debug1: Connecting to vps [203.0.113.42] port 22.
debug1: Connection established.
debug1: identity file /home/user/.ssh/id_ed25519 type 3
debug1: Authentications that can continue: publickey,password
debug1: Next authentication method: publickey
debug1: Offering public key: /home/user/.ssh/id_ed25519
debug1: Authentication succeeded (publickey).
```

### Lỗi thường + fix

| Lỗi | Nguyên nhân + Fix |
|---|---|
| `Permission denied (publickey)` | Server từ chối key. Check: (1) public key có trong `~/.ssh/authorized_keys`? (2) Permission `~/.ssh` (700) + `authorized_keys` (600)? (3) `PubkeyAuthentication yes` ở sshd? |
| `Connection refused` | sshd không chạy / port sai / firewall block |
| `Connection timed out` | Network không reach (firewall? IP sai?) |
| `Host key verification failed` | Server đổi key (reinstall? MITM?). Edit `~/.ssh/known_hosts` xoá dòng cũ |
| `Too many authentication failures` | SSH thử nhiều key. Add `IdentitiesOnly yes` + `IdentityFile` cụ thể |

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`PasswordAuthentication yes` production** → brute force dễ. Force key-only.
2. **`PermitRootLogin yes`** → attacker biết username = root. **Always no**.
3. **Permission key file rộng** (755) → SSH refuse. **600 + 700 cho dir**.
4. **Edit sshd_config + reload trong cùng session SSH** → sai = lock-out. Mở session 2 trước khi reload.
5. **Quên `chmod 600 authorized_keys`** → SSH `StrictModes yes` refuse. Set permission đúng sau scp.

---

## 🧠 Tự kiểm tra (Self-check)

1. Loại key SSH **modern + an toàn** nhất 2026?
2. Sinh + copy public key lên server bằng lệnh gì?
3. Viết `~/.ssh/config` cho 2 host: `vps1` (user@vps1.x.com:22), `prod` (deploy@prod.x.com qua bastion `bastion.x.com`).
4. Khác nhau giữa `ssh -L` và `ssh -R`?
5. Hardening sshd 4 setting quan trọng nhất?

<details>
<summary>Gợi ý đáp án</summary>

1. **Ed25519** — nhanh, an toàn, key ngắn. `ssh-keygen -t ed25519`.

2. ```bash
   ssh-keygen -t ed25519 -C "user@laptop"
   ssh-copy-id user@vps
   ```

3. ```
   Host vps1
       HostName vps1.x.com
       User deploy
       Port 22
       IdentityFile ~/.ssh/id_ed25519

   Host bastion
       HostName bastion.x.com
       User deploy

   Host prod
       HostName prod.x.com
       User deploy
       ProxyJump bastion
   ```

4. **`-L`** (Local forward) = local port → remote service. Vd `ssh -L 5432:localhost:5432 vps` cho phép laptop connect Postgres ở vps. **`-R`** (Remote forward) = ngược lại — expose local port lên remote. Vd `ssh -R 8080:localhost:3000 vps` cho team connect tới dev server local bạn qua vps.

5. (a) `PermitRootLogin no`. (b) `PasswordAuthentication no` (key only). (c) `AllowUsers <list>` hoặc `AllowGroups <list>`. (d) `MaxAuthTries 3` + `fail2ban`. Bonus: đổi port (mỏng), `X11Forwarding no` nếu không cần.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Daily commands

```bash
ssh user@host                          ssh -i ~/.ssh/key user@host
ssh -p 2222 user@host                   ssh -A user@host (forward agent)
ssh -J bastion user@host                ssh -L 5432:localhost:5432 user@host
ssh -R 8080:localhost:3000 user@host    ssh -D 1080 user@host (SOCKS)
ssh -v user@host                        ssh-add ~/.ssh/id_ed25519
ssh-keygen -t ed25519                   ssh-copy-id user@host
```

### `~/.ssh/config` minimal

```
Host *
    AddKeysToAgent yes
    UseKeychain yes              # Mac
    ServerAliveInterval 60

Host vps1
    HostName vps1.example.com
    User deploy
    IdentityFile ~/.ssh/id_ed25519

Host prod
    HostName prod.example.com
    User deploy
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User deploy
```

### Transfer

```bash
scp file vps:/tmp/                      rsync -avz dir/ vps:/path/
scp -r dir vps:/tmp/                    rsync -avz --delete dir/ vps:/path/
scp vps:/path/file ./                   rsync --progress huge.tar vps:/tmp/
```

### Hardening checklist

```
[ ] PermitRootLogin no
[ ] PasswordAuthentication no
[ ] AllowUsers <list>
[ ] MaxAuthTries 3
[ ] ClientAliveInterval 300
[ ] fail2ban installed
[ ] Public key in authorized_keys
[ ] chmod 600 ~/.ssh/* and 700 ~/.ssh
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **SSH** | Secure Shell — protocol shell từ xa |
| **OpenSSH** | Implementation phổ thông |
| **Ed25519** | Modern key type (recommended 2026) |
| **Passphrase** | Mật khẩu mở khóa private key |
| **SSH agent** | Process giữ unlocked key trong memory |
| **Agent forwarding (`-A`)** | Forward agent qua connection (caution) |
| **`ProxyJump`** | SSH chain qua bastion an toàn |
| **Local forward (`-L`)** | Tunnel local port → remote service |
| **Remote forward (`-R`)** | Tunnel remote port → local service |
| **Dynamic / SOCKS (`-D`)** | SOCKS5 proxy qua SSH |
| **Bastion / Jump host** | Server intermediate vào private network |
| **`~/.ssh/authorized_keys`** | Public keys được phép login |
| **`~/.ssh/known_hosts`** | Server fingerprints (TOFU) |
| **`fail2ban`** | Auto-ban IP brute force |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [systemd Services — Biến app thành service production](01_systemd-services.md)
- ➡️ **Bài tiếp theo:** [Package Management — apt, dnf, snap, dependency, security updates](03_package-management.md)
- ↑ **Về cụm:** [linux README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [TCP/IP ports/sockets/firewall](../../../../05_networking/tcp-ip-fundamentals/lessons/01_basic/03_ports-sockets-firewall.md) — port 22, firewall SSH
- [git over SSH](../../../../02_tools/git/) — git push/pull qua SSH key

### 🌐 Tài nguyên tham khảo khác
- 📖 [OpenSSH manual](https://man.openbsd.org/ssh)
- 📖 [SSH best practices — Mozilla](https://infosec.mozilla.org/guidelines/openssh)
- 📖 [DigitalOcean: SSH essentials](https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys)
- 📖 [SSH tunneling tutorial — Linuxize](https://linuxize.com/post/how-to-setup-ssh-tunneling/)
- 📖 [Mosh](https://mosh.org/) — SSH alternative cho mạng kém

---

> 🎯 *Sau bài này bạn quản lý fleet 10+ server thuần thục. Bài kế tiếp dạy **package management** — apt/dnf/snap, dependency hell, security updates.*

## 📌 Nhật ký thay đổi (Changelog)

- **v1.2.0 (24/05/2026)** — Thêm ẩn dụ "bộ chìa khoá cao cấp" cho SSH keys, 2 lời dẫn trước bảng thuật toán + lệnh ssh-keygen. Chuẩn hóa username trong ví dụ.
