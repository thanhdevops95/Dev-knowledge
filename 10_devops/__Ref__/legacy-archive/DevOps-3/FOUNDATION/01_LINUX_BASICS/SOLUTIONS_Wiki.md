# Solutions: Module 01 - Linux Basics

> **Answer key for exercises, scenarios, and quiz**

---

## 📋 EXERCISE SOLUTIONS

### Section A: Multiple Choice Questions

1. **A** - `/` (root directory)
2. **C** - `ls -la`
3. **B** - `cd ..`
4. **A** - `pwd`
5. **C** - `mkdir new_folder`
6. **B** - `rm file.txt`
7. **D** - `cp file.txt /destination/`
8. **A** - `mv oldname.txt newname.txt`
9. **C** - `cat file.txt`
10. **B** - `grep "pattern" file.txt`
11. **D** - `chmod 755 script.sh`
12. **A** - `chown user:group file.txt`
13. **C** - `ps aux`
14. **B** - `top`
15. **A** - `kill PID`
16. **D** - `sudo apt update && sudo apt install package`
17. **C** - `df -h`
18. **B** - `du -sh directory/`
19. **A** - `find / -name file.txt`
20. **D** - `|` (pipe)

### Section B: Fill in the Blank

1. `ls -la`
2. `cd /var/log`
3. `mkdir`
4. `rm -rf directory/`
5. `cp source dest`
6. `chmod 755`
7. `chown`
8. `ps aux`
9. `kill`
10. `grep`
11. `find`
12. `df -h`
13. `>`
14. `>>`
15. `|`

### Section C: Hands-on Tasks

**Task 36-40:** (Command demonstrations)

1. Navigate to /tmp:

```bash
cd /tmp
pwd  # Verify
```

1. Create files and directory:

```bash
mkdir test_dir
touch test_dir/file1.txt test_dir/file2.txt test_dir/file3.txt
ls test_dir/
```

1. Search for .conf files:

```bash
find /etc -name "*.conf" 2>/dev/null
```

1. Find large files:

```bash
find /var -type f -size +100M 2>/dev/null
```

1. Process commands:

```bash
# Find process
ps aux | grep nginx

# Kill process
kill PID

# Verify
ps aux | grep nginx
```

### Section D: Debugging Scenarios

**41. Permission Denied:**

```bash
# Solution
chmod +x script.sh
./script.sh
```

**42. Cannot delete directory:**

```bash
# Directory not empty
rm -rf old_folder/

# Or remove contents first
rm old_folder/*
rmdir old_folder/
```

**43. Command not found:**

```bash
# Install the package
sudo apt update
sudo apt install tree
```

**44. Disk full:**

```bash
# Find large files
du -sh /var/* | sort -h
# Or
find / -type f -size +1G 2>/dev/null

# Remove large logs
sudo rm /var/log/large.log
# Or clean package cache
sudo apt clean
```

**45. Process won't stop:**

```bash
# Force kill
kill -9 PID

# Verify
ps aux | grep process_name
```

### Section E: Advanced Tasks

**46. Backup script:**

```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup_$DATE.tar.gz /home/user/data/
```

**47. Find and delete old files:**

```bash
find /tmp -type f -mtime +30 -delete

# Or safer (check first):
find /tmp -type f -mtime +30
# Then delete
find /tmp -type f -mtime +30 -delete
```

**48. Monitor disk usage:**

```bash
#!/bin/bash
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt 80 ]; then
    echo "WARNING: Disk usage is ${USAGE}%"
fi
```

**49. User and group:**

```bash
# Create user
sudo useradd -m devuser

# Create group
sudo groupadd developers

# Add user to group
sudo usermod -aG developers devuser

# Verify
groups devuser
```

**50. Automated cleanup:**

```bash
#!/bin/bash
# cleanup.sh

# Remove old logs
find /var/log -name "*.log" -mtime +7 -delete

# Clear package cache
apt clean

# Remove old temp files
find /tmp -type f -mtime +3 -delete

echo "Cleanup complete"
```

---

## 🎬 SCENARIO SOLUTIONS

### Scenario 1: The Midnight Disk Crisis

**Solution Steps:**

1. **Check disk usage:**

```bash
df -h
# / is 98% full
```

1. **Find large files:**

```bash
du -sh /var/* | sort -h
# /var/log is 45GB
```

1. **Check log directory:**

```bash
du -sh /var/log/* | sort -h
# app.log is 40GB
```

1. **Temporarily free space:**

```bash
# Compress current log
gzip /var/log/app.log

# Or truncate
> /var/log/app.log
```

1. **Setup log rotation:**

```bash
# /etc/logrotate.d/app
/var/log/app.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
}
```

1. **Verify:**

```bash
df -h
# / now at 65%
```

### Scenario 2: The Permission Nightmare

**Solution:**

1. **Check current permissions:**

```bash
ls -la /var/www/myapp
# All files owned by root
```

1. **Fix ownership:**

```bash
sudo chown -R www-data:www-data /var/www/myapp
```

1. **Fix permissions:**

```bash
# Directories: 755
sudo find /var/www/myapp -type d -exec chmod 755 {} \;

# Files: 644
sudo find /var/www/myapp -type f -exec chmod 644 {} \;
```

1. **Verify:**

```bash
ls -la /var/www/myapp/
# Should show www-data ownership
# Directories drwxr-xr-x
# Files -rw-r--r--
```

### Scenario 3: The Runaway Process

**Solution:**

1. **Find process:**

```bash
top
# Or
ps aux | grep python | grep 98
# PID: 12345
```

1. **Try graceful stop:**

```bash
kill 12345
```

1. **If doesn't stop, force kill:**

```bash
kill -9 12345
```

1. **Find root cause:**

```bash
# Check logs
tail -f /var/log/app.log
# Infinite loop detected
```

1. **Fix code and restart:**

```bash
# Fix the infinite loop code
# Then restart properly
systemctl restart myapp
```

### Scenario 4: Missing Config File

**Solution:**

1. **Find file:**

```bash
find / -name "app.conf" 2>/dev/null
# Found at /etc/nginx/sites-available/app.conf
```

1. **Check if symlink exists:**

```bash
ls -la /etc/nginx/sites-enabled/
# No symlink to app.conf
```

1. **Create symlink:**

```bash
sudo ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/
```

1. **Test and reload:**

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Scenario 5: Zombie Process Army

**Solution:**

1. **Find zombies:**

```bash
ps aux | grep Z
# Or
ps aux | awk '$8=="Z"'
```

1. **Find parent:**

```bash
ps -o ppid= -p ZOMBIE_PID
# Parent PID: 1234
```

1. **Kill parent (will clean up zombies):**

```bash
kill 1234
```

1. **Prevent future zombies (fix code):**

```python
# In parent process code:
import signal
signal.signal(signal.SIGCHLD, signal.SIG_IGN)
```

---

## 📝 QUIZ SOLUTIONS

1. **C** - Root (/)
2. **B** - Hidden files and directories
3. **A** - Home directory
4. **D** - /var
5. **C** - cp source dest
6. **B** - mv
7. **A** - rm -r
8. **D** - touch newfile.txt
9. **C** - cat file.txt
10. **B** - grep "text" file.txt
11. **A** - find / -name file.txt
12. **D** - rwxr-xr-x
13. **C** - chmod 755 file.sh
14. **B** - chown user:group file
15. **A** - ps aux
16. **D** - kill PID
17. **C** - top
18. **B** - sudo apt install package
19. **A** - df -h
20. **D** - du -sh directory/
21. **C** - |
22. **B** - >
23. **A** - >>
24. **D** - /etc
25. **C** - /var/log
26. **B** - /home
27. **A** - /tmp
28. **D** - chown
29. **C** - 755
30. **B** - Interrupt (stop) a running command

---

## 📊 GRADING RUBRIC

**Total Points: 200**

### Breakdown

- Section A (MCQ): 20 × 2 = 40 points
- Section B (Fill): 15 × 2 = 30 points
- Section C (Tasks): 10 × 8 = 80 points
- Section D (Debug): 5 × 10 = 50 points

### Grading Scale

- 180-200: Excellent (A) ⭐⭐⭐
- 160-179: Good (B) ⭐⭐
- 140-159: Pass (C) ⭐
- < 140: Review needed

### Quiz Grading

- 28-30: Expert level
- 24-27: Proficient
- 20-23: Competent
- < 20: Needs review

---

<div align="center">

**Review explanations, not just answers!** 📚

**Practice makes perfect! 💪**

</div>
