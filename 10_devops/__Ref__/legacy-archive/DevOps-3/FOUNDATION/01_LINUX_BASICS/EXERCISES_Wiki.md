# EXERCISES - Module 01: LINUX BASICS

> **Purpose:** Master Linux command line through practice
> **Difficulty:** ⭐☆☆☆☆ to ⭐⭐⭐☆☆ | **Time:** 4-5 hours

---

## 📋 Exercise List (30 Exercises)

### File System Navigation (Ex 1-5)

1. Navigate to `/usr/local/bin` using 3 different methods
2. Create directory structure: `~/projects/{web,api,mobile}/{src,tests,docs}`
3. Find all directories named "config" under `/etc`
4. List all files in home directory modified in last 24 hours
5. Create symbolic link from `~/shortcuts/docs` to `/usr/share/doc`

### File Operations (Ex 6-10)

6. Copy all `.log` files from `/var/log` to `~/logs-backup`
2. Archive `/etc/nginx` with timestamp
3. Find and delete all files larger than 100MB in `/tmp`
4. Create 5 test files, rename them in sequence
5. Move all `.txt` files to subdirectory without overwriting

### Text Processing (Ex 11-15)

11. Extract all email addresses from file using grep
2. Count unique IP addresses in access log
3. Replace all occurrences of "error" with "ERROR" in file
4. Merge 3 CSV files and remove duplicates
5. Create report showing top 10 error types from logs

### Permissions & Ownership (Ex 16-20)

16. Create project with correct permissions (755 dirs, 644 files)
2. Fix broken permissions on web directory
3. Create shared folder with sticky bit
4. Find all world-writable files in `/tmp`
5. Set ACLs for multi-user project directory

### Process Management (Ex 21-25)

21. Find and kill all zombie processes
2. Monitor CPU usage and identify top 5 processes
3. Run background job, detach it, re-attach later
4. Set nice value for long-running process
5. Create script to restart service if it crashes

### Shell Scripting (Ex 26-30)

26. Write backup script with rotation (keep last 7 days)
2. Create system health monitor with alerts
3. Build log analyzer with statistics
4. Automate user account creation from CSV
5. Build interactive menu system for server management

---

## 🎯 Sample Solutions

### Exercise 11: Extract Emails

```bash
grep -Eo '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' file.txt | sort -u
```

### Exercise 26: Backup Script

```bash
#!/bin/bash
SOURCE="/var/www"
DEST="/backup"
DATE=$(date +%Y%m%d)
find $DEST -name "backup_*.tar.gz" -mtime +7 -delete
tar -czf $DEST/backup_$DATE.tar.gz $SOURCE
```

---

> **Complete 20/30 to pass | All 30 for mastery!** 🎖️
