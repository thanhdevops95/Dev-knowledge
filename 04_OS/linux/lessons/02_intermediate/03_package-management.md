# 🎓 Package Management — apt, dnf, snap, dependency, security updates

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.2.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~16 phút\
> **Prerequisites:** [Users & Permissions](00_users-and-permissions.md)

> 🎯 *Hiểu **`apt`** (Debian/Ubuntu) vs **`dnf`** (RHEL/Fedora) vs **snap/flatpak** (universal), **dependency resolution**, **repositories + PPA**, **security updates** + unattended-upgrades, lock file `dpkg`, build từ source khi cần.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng `apt` đầy đủ: `update` / `upgrade` / `install` / `remove` / `search` / `show`
- [ ] Hiểu **package vs binary vs source** + cài source khi cần
- [ ] Quản lý **PPA** (Personal Package Archive) Ubuntu
- [ ] Phân biệt `apt-get` / `apt` / `apt-cache` / `aptitude`
- [ ] So sánh **apt** vs **dnf** vs **pacman** vs **zypper**
- [ ] Hiểu **snap** + **flatpak** + **AppImage** (universal package)
- [ ] Setup **security updates tự động** (unattended-upgrades)
- [ ] Resolve **dependency hell** + dpkg lock conflict

---

## Tình huống — Bạn deploy FastAPI và `apt install postgresql`

Bạn deploy lên Ubuntu VPS. Cần Postgres, Redis, Nginx. Anh gõ:

```bash
$ sudo apt install postgresql
E: Could not get lock /var/lib/dpkg/lock-frontend
# Lỗi: process khác đang cài gì đó

$ sudo apt install python3.12
E: Unable to locate package python3.12
# Ubuntu 22.04 default chỉ có python 3.10

$ sudo apt install nginx
W: Update was held back: nginx-common
# Nâng cấp partial, có vấn đề?

$ sudo apt install redis
# Default Ubuntu cài Redis 6.x — anh muốn 7.x mới
```

Bạn ngơ:
- Sao **lock file** chặn? Là gì?
- Sao **Python 3.12** không có trên Ubuntu 22? Cách thêm?
- **`update`** vs **`upgrade`** khác sao?
- Cài **bản mới hơn distro default** — qua PPA? snap? source?
- **`apt`** vs **`apt-get`** — dùng cái nào?

→ Bài này dạy package management Linux đầy đủ.

---

## 1️⃣ Package manager là gì?

**Package manager** = tool quản lý cài đặt/upgrade/xóa **phần mềm + dependencies** từ central repository.

| Distro | Package manager | Format file |
|---|---|---|
| **Ubuntu / Debian / Mint** | **apt** (frontend), **dpkg** (backend) | `.deb` |
| **RHEL / CentOS / Rocky / AlmaLinux** | **dnf** (mới), **yum** (cũ) | `.rpm` |
| **Fedora** | **dnf** | `.rpm` |
| **SUSE / openSUSE** | **zypper** | `.rpm` |
| **Arch Linux / Manjaro** | **pacman** | `.pkg.tar.zst` |
| **Alpine** | **apk** | `.apk` |
| **NixOS** | **nix** | Nix store |

→ **Anti-cargo-cult**: lệnh không xuyên distro. Học lệnh của distro bạn dùng.

### Vai trò

🪞 **Ẩn dụ**: *Package manager như **app store + thợ sửa nhà combo** — bạn nói "tôi muốn nginx", nó tự tải về, gọi điện thợ lắp đặt (resolve dependencies), check chứng chỉ hợp lệ (GPG), lưu sổ "đã lắp ngày nào". Bạn không cần biết nginx cần thư viện gì.*

Mỗi package manager có 7 vai trò chính. Hiểu để biết khi gõ `apt install` nó làm gì đằng sau:

| Vai trò | Mô tả |
|---|---|
| **Install** | Tải binary + cài dependencies tự động |
| **Upgrade** | Tải version mới + reload service |
| **Remove** | Uninstall + cleanup config |
| **Search** | Tìm package theo tên/từ khoá |
| **Resolve dependencies** | Tính toán: cần lib A, A cần B, B cần C... → cài hết |
| **Verify** | Check checksum + GPG signature |
| **Repository** | Source download (URL list) |

---

## 2️⃣ `apt` — Lệnh thường dùng

### Update vs Upgrade — KHÁC NHAU

Người mới hay nhầm `apt update` với `apt upgrade`. **Khác nhau quan trọng**: update = refresh danh sách package có sẵn; upgrade = thực sự cài bản mới:

```bash
sudo apt update                          # Update index repo (KHÔNG cài gì)
sudo apt upgrade                          # Upgrade package đã cài
sudo apt full-upgrade                     # Upgrade + có thể remove package conflict
sudo apt dist-upgrade                     # Như full-upgrade (alias cũ)
```

→ Quy trình:
```
1. sudo apt update           ← refresh "đang có gì mới trong repo"
2. sudo apt upgrade           ← apply update
```

→ Skip step 1 = upgrade với index cũ → có thể bỏ lỡ security patch.

### Install / Remove

Hai cặp lệnh chính: `install`/`remove` cho cài/gỡ thông thường, `install=<version>` cho cài đúng version, `purge` cho gỡ kèm config:

```bash
sudo apt install nginx                          # Cài
sudo apt install nginx redis postgresql         # Cài nhiều
sudo apt install nginx=1.24.0-1ubuntu1          # Cài version cụ thể
sudo apt install ./mypackage.deb                # Cài từ file .deb local

sudo apt remove nginx                            # Uninstall (giữ config)
sudo apt purge nginx                             # Uninstall + xoá config
sudo apt autoremove                              # Xoá dependency không còn cần
```

### Tìm + Info

```bash
apt search "web server"                          # Tìm trong description
apt show nginx                                    # Detail 1 package
apt list --installed                              # Đã cài
apt list --upgradable                             # Có update không?
dpkg -l                                           # Detailed list (dpkg backend)
dpkg -L nginx                                     # File nào của package
dpkg -S /etc/nginx/nginx.conf                     # File này thuộc package nào?
```

### Clean

```bash
sudo apt clean                                    # Xoá .deb cache (/var/cache/apt/archives/)
sudo apt autoclean                                # Chỉ xoá .deb cũ không còn trong repo
```

### `apt` vs `apt-get` vs `aptitude`

| Tool | Khi nào |
|---|---|
| **`apt`** | **Recommended 2026** — UX đẹp, progress bar, đa số lệnh phổ thông |
| **`apt-get`** | Old API — script tin cậy hơn (stable output) |
| **`apt-cache`** | Search + show (cũ, giờ apt làm hết) |
| **`aptitude`** | TUI interactive, dependency resolution thông minh hơn (legacy) |

> 💡 **Quy tắc**: human interactive → `apt`. Shell script → `apt-get` (output stable).

---

## 3️⃣ Repository + GPG keys

`apt` đọc danh sách repo từ:
- `/etc/apt/sources.list` — main repo
- `/etc/apt/sources.list.d/*.list` — repo bổ sung

### Xem repo

```bash
cat /etc/apt/sources.list
# deb http://archive.ubuntu.com/ubuntu/ jammy main restricted
# deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted
```

Format: `deb URL distribution components`:
- `deb` — binary package (vs `deb-src` source).
- `URL` — mirror.
- `distribution` — codename (`jammy` = Ubuntu 22.04, `noble` = 24.04).
- `components` — `main` (free, official), `restricted` (proprietary driver), `universe` (community), `multiverse` (legal restrict).

### Thêm PPA (Ubuntu)

**PPA** = Personal Package Archive — repo cộng đồng hosting bởi Launchpad.

```bash
# Thêm PPA cho deadsnakes (Python phiên bản mới)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv
```

→ Bạn fix Python 3.12 = PPA deadsnakes.

### Thêm repo từ vendor (Docker, Postgres official, ...)

```bash
# Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

→ Modern Ubuntu yêu cầu `signed-by=<keyring>` (security). Không còn `apt-key add` (deprecated).

### Pin priority — Lock version

```
# /etc/apt/preferences.d/nginx
Package: nginx
Pin: version 1.24.*
Pin-Priority: 1001
```

→ Không upgrade lên 1.25. Dùng khi compatibility.

---

## 4️⃣ `dpkg` — Backend (deep dive 1 chút)

`dpkg` = lệnh quản lý `.deb` file trực tiếp (low-level). `apt` gọi `dpkg` bên trong.

```bash
dpkg -i package.deb                              # Install .deb (KHÔNG resolve dep)
dpkg --remove package_name
dpkg --purge package_name
dpkg -l                                           # List installed
dpkg -L package_name                              # File nào của package
dpkg -S /usr/bin/python3                         # File này thuộc package nào
dpkg --configure -a                              # Fix broken (sau ctrl+C giữa cài)
dpkg --get-selections                             # List + state
```

### Lock file conflict

```bash
# Error: Could not get lock /var/lib/dpkg/lock-frontend
sudo lsof /var/lib/dpkg/lock-frontend           # Tìm process đang giữ
sudo kill <PID>
sudo rm /var/lib/dpkg/lock-frontend             # Cẩn thận! Chỉ khi chắc không có process
sudo dpkg --configure -a                         # Resync state
```

→ **DO NOT** xoá lock khi `apt install` đang chạy thật → corrupt package db.

---

## 5️⃣ `dnf` — Cho RHEL/Fedora (so sánh nhanh)

```bash
sudo dnf update                                  # = apt update + upgrade combined
sudo dnf upgrade                                  # Alias of update
sudo dnf install nginx
sudo dnf remove nginx
sudo dnf search "web server"
sudo dnf info nginx
sudo dnf list installed
sudo dnf list --upgrades
sudo dnf autoremove
sudo dnf clean all
```

### Repo

```
/etc/yum.repos.d/*.repo
```

### Bonus — `dnf module`

RHEL/Fedora có **module streams** — multiple version cùng package:

```bash
sudo dnf module list nodejs
# nodejs 14, 16, 18, 20 (available)
sudo dnf module enable nodejs:20
sudo dnf install nodejs
```

→ Hữu ích install version cụ thể không phá hệ thống.

---

## 6️⃣ Snap, Flatpak, AppImage — Universal package

Vấn đề của apt/dnf:
- Phiên bản trong distro **cũ** (Ubuntu 22.04 = Python 3.10, không 3.12).
- Package list theo distro — không cross-distro.

→ **Universal package format** sinh ra:

| Format | Backed by | Sandbox | Auto-update | Use case |
|---|---|---|---|---|
| **Snap** | Canonical (Ubuntu) | ✅ | ✅ (force) | Ubuntu default |
| **Flatpak** | Fedora + community | ✅ | Optional | Linux desktop |
| **AppImage** | Independent | ❌ (basic) | Manual | Portable app |

### Snap

```bash
snap install code --classic              # VS Code (--classic = full system access)
snap install postman
snap list                                  # Đã cài
snap refresh                                # Update all
snap remove code
```

→ Snap cài chậm hơn apt (vì download self-contained, mỗi snap 100-500MB).

### Flatpak

```bash
flatpak install flathub org.mozilla.firefox
flatpak run org.mozilla.firefox
flatpak update
flatpak list
```

### AppImage

```bash
# Tải `app.AppImage` (single file binary)
chmod +x app.AppImage
./app.AppImage
```

→ Portable, không cài system. Hữu ích cho USB stick / test.

### Khi nào dùng gì?

| Use case | Chọn |
|---|---|
| Server core (Postgres, Nginx, ...) | **apt/dnf** native |
| Desktop GUI app (VS Code, browser, ...) | snap / flatpak / native (theo distro) |
| Portable app (1-off, test) | AppImage |
| Containerized service | **Docker** (không phải universal package) |

→ **Quy tắc**: server stack dùng native package. Desktop có thể mix.

---

## 7️⃣ Security updates — Tự động

Server production cần security patch **mọi tuần**. Manual = quên.

### `unattended-upgrades` (Ubuntu/Debian)

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Config `/etc/apt/apt.conf.d/50unattended-upgrades`:

```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    // "${distro_id}:${distro_codename}-updates";    // (optional)
};

// Auto-reboot khi kernel update yêu cầu
Unattended-Upgrade::Automatic-Reboot "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "false";   // Tránh reboot khi có user login
Unattended-Upgrade::Automatic-Reboot-Time "02:00";

// Email report
Unattended-Upgrade::Mail "ops@acmeshop.vn";
Unattended-Upgrade::MailOnlyOnError "true";

// Cleanup
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
```

→ Mỗi đêm 2 AM: tự apply security patch, reboot nếu cần (kernel update). Email report nếu fail.

### Production strategy — Khi nào tắt auto-reboot?

| Scenario | Auto-reboot? |
|---|---|
| **Single server, có user request 24/7** | ❌ Tắt — schedule maintenance window |
| **HA cluster** (2+ node load-balanced) | ✅ OK — rolling reboot không downtime |
| **Stateless container host** | ✅ OK |
| **Database master (Postgres/MySQL)** | ❌ Manual — coordinate failover trước |

→ Test config:

```bash
sudo unattended-upgrade --dry-run --debug
sudo unattended-upgrade -d                   # Run thực (verbose)
cat /var/log/unattended-upgrades/unattended-upgrades.log
```

### Disable auto-reboot cho critical service

```bash
# Touch file này → block auto-reboot dù kernel update
sudo touch /var/run/reboot-required.pkgs

# Hoặc thêm cron job check + page on-call thay vì auto reboot
```

→ Mỗi server có window riêng. Document trong runbook.

### `dnf-automatic` (RHEL/Fedora)

```bash
sudo dnf install dnf-automatic
sudo systemctl enable --now dnf-automatic.timer
```

Config `/etc/dnf/automatic.conf` → set `apply_updates = yes`.

### Pros vs Cons

| Pros | Cons |
|---|---|
| ✅ Security patch trong 24h | ❌ Update có thể break (hiếm, nhưng có) |
| ✅ Compliance | ❌ Reboot tự động — disruption nếu không HA |
| ✅ Đỡ con người | ❌ Không có rollback (chỉ patch security, ít rủi ro) |

→ **2026 best practice**: bật unattended security updates cho mọi server. App update qua CI/CD, không qua auto-update.

---

## 8️⃣ Build từ source — Khi distro không có

```bash
# Cài build tools
sudo apt install build-essential libssl-dev libreadline-dev ...

# Download + extract source
wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
tar xzf Python-3.12.3.tgz && cd Python-3.12.3

# Configure
./configure --prefix=/opt/python3.12 --enable-optimizations

# Build (long, dùng CPU max)
make -j$(nproc)

# Install (vào /opt — không đụng system)
sudo make install
```

→ Pattern `configure → make → make install` chuẩn 40 năm Unix.

> ⚠️ Build source = không có dependency tracking. Update phải tự làm. Khuyên dùng package khi có thể.

---

## 9️⃣ Dependency hell + fix

### Triệu chứng

```
$ sudo apt install package-A
The following packages have unmet dependencies:
 package-A : Depends: libfoo (>= 2.0) but 1.5 is to be installed
 E: Unable to correct problems, you have held broken packages.
```

→ Package A cần libfoo 2.0+, system có 1.5, không upgrade được vì lib khác cần 1.5.

### Cách giải

```bash
# 1. Xem cây dependency
apt-cache depends package-A
apt-cache rdepends libfoo

# 2. Update toàn bộ system (đôi khi đủ)
sudo apt update && sudo apt full-upgrade

# 3. Force install nếu chắc chắn
sudo apt install -f                       # Fix broken
sudo dpkg --configure -a                  # Resync

# 4. Last resort: container hoá
docker run --rm -it ubuntu:24.04 bash      # Test trong env clean
```

### Phòng tránh

- Đừng cài quá nhiều từ source / mixed repo.
- Đừng skip `apt update` lâu.
- Container hoá khi cần env riêng (Docker, podman).

---

## ⚠️ 5 pitfall hay vướng

1. **`apt upgrade` không `update` trước** → dùng index cũ. Luôn 2 lệnh: `update && upgrade`.
2. **Cài qua `dpkg -i` không qua `apt`** → không resolve dependency → broken. Dùng `apt install ./file.deb`.
3. **Xoá `dpkg lock` khi `apt` đang chạy** → corrupt db. Đợi process xong hoặc `kill -TERM` đúng.
4. **Snap mọi thứ** → tốn 5-10GB cho 20 snap. App server dùng native.
5. **Quên `apt update` sau khi đổi `sources.list`** → không thấy package mới của repo mới.

---

## ✅ Self-check

1. Khác nhau **`apt update`** vs **`apt upgrade`**?
2. Cài Python 3.12 trên Ubuntu 22.04 (default 3.10) — cách nào?
3. Package `nginx` thuộc file `/etc/nginx/nginx.conf` không? Lệnh check?
4. Khác **snap** và **apt**?
5. Setup security updates tự động trên Ubuntu — gói nào + config gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **`apt update`** = refresh package index (download metadata), KHÔNG cài/upgrade. **`apt upgrade`** = upgrade các package đã cài có version mới trong index. Phải `update` trước `upgrade` để có thông tin mới nhất.

2. (a) **PPA**: `sudo add-apt-repository ppa:deadsnakes/ppa && sudo apt install python3.12`. (b) **Snap**: `sudo snap install python --channel=edge`. (c) **Build source**: download Python.org, `./configure && make && make install`. (d) **Container Docker**: `docker run python:3.12`. (e) **pyenv**: per-user Python version. Recommend: PPA cho server, pyenv/Docker cho dev.

3. Lệnh: `dpkg -S /etc/nginx/nginx.conf`. Output: `nginx-common: /etc/nginx/nginx.conf`.

4. **apt** = native Debian/Ubuntu, package nhẹ (shared lib), tích hợp distro chặt, version cũ thường. **snap** = self-contained (bao gồm lib), sandbox, version mới hơn, tốn disk, slow start.

5. ```bash
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   # Edit /etc/apt/apt.conf.d/50unattended-upgrades:
   # Bật Allowed-Origins ${distro_id}:${distro_codename}-security
   # Bật Automatic-Reboot "true"
   ```
</details>

---

## ⚡ Cheatsheet

### apt — Daily

```bash
sudo apt update                    # Refresh index
sudo apt upgrade                    # Apply updates
sudo apt full-upgrade               # Apply + remove conflicts
sudo apt install pkg                sudo apt remove pkg
sudo apt purge pkg                  sudo apt autoremove
apt search "keyword"                apt show pkg
apt list --installed                apt list --upgradable
dpkg -l                              dpkg -L pkg
dpkg -S /path/file                  sudo dpkg --configure -a
```

### dnf — Daily (RHEL/Fedora)

```bash
sudo dnf update                    sudo dnf upgrade
sudo dnf install pkg               sudo dnf remove pkg
sudo dnf search "kw"               sudo dnf info pkg
sudo dnf list installed             sudo dnf autoremove
```

### Universal

```bash
snap install pkg                   flatpak install flathub org.x
snap refresh                       flatpak update
snap list                          flatpak list
./app.AppImage
```

### Add repo (Ubuntu)

```bash
sudo add-apt-repository ppa:user/ppa
sudo apt update
```

### Security updates

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Package manager** | Tool quản lý install/upgrade phần mềm |
| **apt / dnf / pacman / apk** | Frontend của Debian/RHEL/Arch/Alpine |
| **dpkg / rpm** | Backend low-level (Debian/RHEL) |
| **Repository** | URL chứa danh sách package + binary |
| **PPA** | Personal Package Archive — Ubuntu community repo |
| **Pin priority** | Lock package ở version cụ thể |
| **Dependency resolution** | Tính cây dependency để cài đúng |
| **`.deb` / `.rpm`** | Format binary package |
| **Snap / Flatpak / AppImage** | Universal package format (cross-distro) |
| **Unattended-upgrades** | Auto-apply security patches |
| **`/etc/apt/sources.list`** | Danh sách repo apt |
| **`dpkg lock`** | File lock chống concurrent install |

---

## 🔗 Links

### Trong cluster
- ← Trước: [SSH Deep Dive](02_ssh-deep-dive.md)
- → Tiếp: [Text Processing Advanced](04_text-processing-advanced.md)
- ↑ Cluster: [linux README](../../README.md)

### Cross-reference
- [systemd services](01_systemd-services.md) — package có thể tự cài service files
- [Docker](../../../../10_DevOps/docker/) — alternative khi package conflict

### External
- 📖 [Debian apt manual](https://manpages.debian.org/bookworm/apt/apt.8.en.html)
- 📖 [RHEL dnf docs](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
- 📖 [Snap docs](https://snapcraft.io/docs)
- 📖 [Unattended Upgrades — Ubuntu wiki](https://help.ubuntu.com/community/AutomaticSecurityUpdates)
- 📖 [Comparison of Linux package managers — Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_Linux_package-management_systems)

---

> 🎯 *Sau bài này bạn quản lý package, repo, security updates thuần thục. Bài cuối cluster — `grep`/`sed`/`awk` — power text processing.*

## 📌 Changelog

- **v1.2.0 (24/05/2026)** — Apply Blueprint v0.5.4. Thêm ẩn dụ "app store + thợ sửa nhà combo", 3 lead-in trước bảng vai trò + update vs upgrade + install/remove.
