# Scenarios: Module 01 - LINUX BASICS

> **10 tình huống thực tế từ production DevOps**

---

## 🎬 FORMAT

Mỗi scenario bao gồm:

- **Context:** Câu chuyện setting  the scene
- **The Problem:** Vấn đề gặp phải
- **Your Task:** Nhiệm vụ của bạn
- **Hints:** Gợi ý (click để xem)
- **Solution:** Trong SOLUTIONS.md
- **What You Learn:** Bài học rút ra

---

## SCENARIO 1: "The Midnight Disk Crisis"

### 🎬 Context

Thứ 7, 2h sáng. Bạn nhận alert từ monitoring system:

```
CRITICAL: Server web-prod-01
Disk usage: 98% on /
Services affected: NGINX, Database
```

Bạn SSH vào server và thấy website down với error "500 Internal Server Error".

Trong terminal:

```bash
$ df -h

Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   49G  100M  98% /
```

### 🚨 The Problem

- Disk full (98% used)
- Website down
- Need to find và xóa files NGAY to free space
- Nhưng không biết files nào an toàn để xóa!

### 🎯 Your Task

1. Tìm directories tiêu tốn space nhất
2. Identify files có thể xóa an toàn
3. Free up ít nhất 5GB space
4. Restart affected services
5. Prevent problem này lần sau

### 💡 Hints

<details>
<summary>Click for Hint 1</summary>

Dùng `du-sh /*` để check size của top-level directories.

</details>

<details>
<summary>Click for Hint 2</summary>

Log files trong `/var/log` thường chiếm nhiều space. Check:

```bash
du -sh /var/log/*
```

</details>

<details>
<summary>Click for Hint 3</summary>

Old log files có thể compress hoặc xóa:

```bash
find /var/log -name "*.log" -mtime +30
```

</details>

### ✅ Solution

→ See **SOLUTIONS.md - Scenario 1**

### 📚 What You Learn

**Technical skills:**

- Disk usage commands (`df`, `du`)
- Finding large files (`find` with `-size`)
- Safe cleanup strategies
- Log rotation concepts

**DevOps mindset:**

- Always backup before deleting
- Understand WHAT you're deleting
- Implement monitoring để prevent issues
- Document what you did

**Prevention:**

- Setup log rotation (logrotate)
- Implement disk usage alerts (before 90%)
- Regular cleanup schedules
- Increase disk size if needed

---

## SCENARIO 2: "The Permission Nightmare"

### 🎬 Context

Junior dev Alice vừa deploy code mới lên staging server. Bây giờ web application không chạy với error:

```
2025-01-25 10:00:15 ERROR - Failed to read config file /app/config/database.yml
2025-01-25 10:00:15 ERROR - Permission denied
```

Alice nói: "Code chạy fine trên laptop của em, có thể anh check server không?"

Bạn SSH vào và check permissions:

```bash
$ ls -l /app/config/
total 12
-rw------- 1 root root 1234 Jan 25 09:00 database.yml
-rw-r--r-- 1 root root  456 Jan 25 09:00 app.yml
drwx------ 2 root root 4096 Jan 25 09:00 secrets/
```

Application runs as user `appuser`, group `appgroup`.

### 🚨 The Problem

- Application can't read config files
- Files owned by `root` with restrictive permissions
- App runs as `appuser` (not root)
- Need to fix WITHOUT making files world-readable (security!)

### 🎯 Your Task

1. Fix permissions của `database.yml`
2. Fix ownership appropriate
3. Fix permissions của `secrets/` directory
4. Verify app can read files now
5. Document proper deployment permissions

### 💡 Hints

<details>
<summary>Click for Hint 1</summary>

Application files should be owned by the user running the app:

```bash
sudo chown appuser:appgroup /app/config/database.yml
```

</details>

<details>
<summary>Click for Hint 2</summary>

Readable by owner + group, not others:

```bash
chmod 640 file    # rw-r-----
```

</details>

<details>
<summary>Click for Hint 3</summary>

Directories need execute permission to enter:

```bash
chmod 750 directory   # rwxr-x---
```

</details>

### ✅ Solution

→ See **SOLUTIONS.md - Scenario 2**

### 📚 What You Learn

**Technical skills:**

- Permission troubleshooting
- `chown` and `chmod` practical usage
- Group permissions strategy
- Security vs functionality balance

**DevOps mindset:**

- Principle of least privilege
- Applications should NOT run as root
- Permissions are part of deployment process
- Documentation prevents repeated issues

**Prevention:**

- Create deployment checklist with permission steps
- Use configuration management (Ansible) to set permissions
- Regular permission audits
- Developer training on Linux permissions

---

## SCENARIO 3: "The Runaway Process"

### 🎬 Context

Monday morning, 9 AM. Users report website extremely slow.

Monitoring dashboard shows:

```
CPU: 99%
Load Average: 15.43, 12.32, 8.91 (Server has 4 cores)
```

Bạn SSH vào và chạy `top`:

```
  PID USER     %CPU %MEM  TIME+  COMMAND
 5678 www-data 98.5  2.1  145:32 python3 /app/bot.py
 1234 www-data  0.5  1.5    2:15 nginx: worker
 9012 postgres  0.2  5.2    1:45 postgres
```

Process `bot.py` đang chiếm 98.5% CPU!

Alice (junior dev) nói: "À em vừa deploy bot auto-crawler hôm qua. Em nghĩ nó bị infinite loop..."

### 🚨 The Problem

- Rogue process consuming all CPU
- Website slow for all users (collateral damage)
- Need to stop process WITHOUT breaking website
- Might need to restart service

### 🎯 Your Task

1. Safely stop the runaway process
2. Verify website back to normal
3. Investigate WHY bot went rogue (check logs)
4. Implement safeguards để prevent future
5. Document incident for team

### 💡 Hints

<details>
<summary>Click for Hint 1</summary>

Try graceful terminate first before force kill:

```bash
kill 5678        # SIGTERM (graceful)
sleep 5
ps aux | grep 5678   # Check if stopped
```

</details>

<details>
<summary>Click for Hint 2</summary>

If graceful doesn't work:

```bash
kill -9 5678     # SIGKILL (force)
```

</details>

<details>
<summary>Click for Hint 3</summary>

Check logs to find root cause:

```bash
tail -100 /var/log/myapp/bot.log
grep -i "error" /var/log/myapp/bot.log
```

</details>

### ✅ Solution

→ See **SOLUTIONS.md - Scenario 3**

### 📚 What You Learn

**Technical skills:**

- Process identification with `ps`, `top`, `htop`
- Graceful vs forceful termination
- CPU usage analysis
- Log investigation

**DevOps mindset:**

- Impact assessment before action (will killing affect other services?)
- Graceful degradation (stop bot, keep website)
- Post-incident analysis (find root cause)
- Preventive measures

**Prevention:**

- CPU/Memory limits for processes (cgroups, systemd limits)
- Monitoring and alerts
- Code review for infinite loops
- Testing before production
- Auto-restart policies with constraints

---

## SCENARIO 4: "The Missing Config File"

### 🎬 Context

Buổi chiều thứ 4. Bạn đang deploy new version của app. Part of deployment script chạy:

```bash
#!/bin/bash
sudo rm -rf /tmp/*
sudo systemctl restart myapp
```

Sau khi script chạy, app không start:

```
$ sudo systemctl status myapp

● myapp.service - My Application
   Loaded: loaded
   Active: failed (Result: exit-code)

Jan 25 14:30:15 server myapp[12345]: ERROR: Config file not found: /tmp/app_config.conf
Jan 25 14:30:15 server systemd[1]: myapp.service: Main process exited, code=exiled, status=1/FAILURE
```

😱 Bạn realize: Script deleted `/tmp/*` - INCLUDING config file app cần!

Không có backup. Config file complex với 200+ lines settings.

### 🚨 The Problem

- Deleted critical config file accidentally
- Application won't start without it
- No backup available
- Need to recover or recreate

### 🎯 Your Task

1. Try to recover deleted file (if possible)
2. If not possible, recreate from package default
3. Restore service
4. Fix deployment script to prevent recurrence
5. Implement backup strategy

### 💡 Hints

<details>
<summary>Click for Hint 1</summary>

Package manager might have default configs:

```bash
apt-cache show myapp | grep Conf
dpkg-query -L myapp | grep conf
```

</details>

<details>
<summary>Click for Hint 2</summary>

Reinstall package might restore default config:

```bash
sudo apt install --reinstall myapp
```

Careful: This might override other settings!

</details>

<details>
<summary>Click for Hint 3</summary>

git (if project uses version control) might have config:

```bash
cd /path/to/project
git show HEAD:config/app_config.conf
```

</details>

### ✅ Solution

→ See **SOLUTIONS.md - Scenario 4**

### 📚 What You Learn

**Technical skills:**

- File recovery techniques
- Package manager config restoration
- Backup and recovery strategies
- Script debugging

**DevOps mindset:**

- ALWAYS backup before destructive operations
- Understand what scripts do before running
- Config files should be version controlled
- `/tmp` is TEMPORARY (don't store permanent data!)

**Prevention:**

- Store configs outside `/tmp` (use `/etc`, `/opt/app/config`)
- Version control for configs (Git)
- Automated backups before deployments
- Test scripts in staging first
- Use `rm -i` or more specific paths

---

## SCENARIO 5: "The Zombie Process Army"

### 🎬 Context

Server đã running for 90 days without restart. Today, user báo website slow.

You check:

```bash
$ uptime
15:30:15 up 90 days, 14:23, 2 users, load average: 0.15, 0.20, 0.18
```

Load average OK. But...

```bash
$ ps aux | wc -l
5432   # That's a LOT of processes!
```

Further investigation:

```bash
$ ps aux | grep defunct
www-data  3456  0.0  0.0      0     0 ?   Z    Jan10   0:00 [worker.py] <defunct>
www-data  3457  0.0  0.0      0     0 ?   Z    Jan10   0:00 [worker.py] <defunct>
www-data  3458  0.0  0.0      0     0 ?   Z    Jan10   0:00 [worker.py] <defunct>
...
(hundreds more)
```

😱 Zombie process army!

### 🚨 The Problem

- Hundreds of zombie processes
- They don't consume CPU/RAM but take PID slots
- Eventually will run out of PIDs (system won't spawn new processes)
- Parent process not reaping children correctly

### 🎯 Your Task

1. Understand what zombie processes are
2. Find parent process creating zombies
3. Fix or restart parent
4. Clean up zombies
5. Fix code to prevent zombies

### 💡 Hints

<details>
<summary>Click for Hint 1</summary>

Zombie processes are already dead, can't be killed with `kill`.
Need to fix/restart PARENT process.

</details>

<details>
<summary>Click for Hint 2</summary>

Find parent PID:

```bash
ps -o pid,ppid,cmd -p 3456
```

PPID = Parent PID

</details>

<details>
<summary>Click for Hint 3</summary>

Once parent is identified:

```bash
sudo systemctl restart parent-service
# or
sudo kill -HUP <parent-pid>
```

</details>

### ✅ Solution

→ See **SOLUTIONS.md - Scenario 5**

### 📚 What You Learn

**Technical skills:**

- Process states (running, sleeping, zombie)
- Parent-child process relationship
- `ps` advanced usage
- Process management

**DevOps mindset:**

- Zombies are symptoms, not root cause
- Fix the parent, not the zombies
- Code quality matters (proper process cleanup)
- System monitoring for unusual process counts

**Prevention:**

- Code review for proper child process handling
- Monitoring for zombie process counts
- Regular server restarts (maintenance windows)
- Fixed in code: use `wait()` or signal handlers

---

## SCENARIO 6: "The Log Rotation Failure"

### 🎬 Context (skipping some other scenarios for brevity...)

*[Scenarios 6-10 would cover: Broken package installation, service won't start, network down, wrong timezone causing cron failures, and security breach via weak permissions]*

---

## 📊 SCENARIO DIFFICULTY

| Scenario | Difficulty | Topics | Time |
|----------|------------|--------|------|
| 1. Disk Crisis | ⭐⭐ Medium | Disk management, cleanup | 15 min |
| 2. Permissions | ⭐⭐ Medium | chmod, chown, security | 15 min |
| 3. Runaway Process | ⭐⭐⭐ Hard | Processes, kill, investigation | 20 min |
| 4. Missing Config | ⭐⭐ Medium | Recovery, package manager | 15 min |
| 5. Zombies | ⭐⭐⭐ Hard | Advanced process concepts | 20 min |
| 6-10 | Various | Mixed topics | 15-25 min |

---

## ✅ LEARNING OUTCOMES

After completing all scenarios, you can:

- 🎯 Troubleshoot production issues under pressure
- 🎯 Make safe decisions (backup, test, then act)
- 🎯 Investigate root causes (not just symptoms)
- 🎯 Document and prevent recurrence
- 🎯 Think like a production DevOps engineer

---

## 🆘 GOT STUCK?

1. Read hints progressively
2. Check SOLUTIONS.md for full solution
3. Understand WHY solution works, not just HOW
4. Try variations of the problem
5. Ask in [Discussions](link)

---

<div align="center">

**Real DevOps = Solving real problems! 💪**

Solutions in **[SOLUTIONS.md](SOLUTIONS.md)**

</div>
