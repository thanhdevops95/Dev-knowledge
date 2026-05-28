# 📎 Appendix

> **Nội dung bổ sung và tài liệu mở rộng**

---

## A. Common Commands Quick Reference

### Linux One-Liners

```bash
# Find large files
find / -type f -size +100M 2>/dev/null

# Find recently modified files
find . -mtime -1 -type f

# Kill process by port
kill $(lsof -t -i:8080)

# Watch command output
watch -n 1 'kubectl get pods'

# Disk usage by directory
du -sh */ | sort -h

# Memory usage by process
ps aux --sort=-%mem | head

# Network connections count
ss -s

# Check open files
lsof -p PID

# Trace system calls
strace -p PID

# Monitor file changes
inotifywait -m /path/to/dir
```

### Docker One-Liners

```bash
# Remove all stopped containers
docker container prune -f

# Remove all unused images
docker image prune -a -f

# Copy from container
docker cp container:/path/file ./file

# Get container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container

# Follow logs with timestamp
docker logs -f --timestamps container

# Resource usage
docker stats --no-stream

# Enter running container
docker exec -it container sh

# Export container filesystem
docker export container > container.tar
```

### Kubernetes One-Liners

```bash
# Get all resources in namespace
kubectl get all -n namespace

# Delete all pods in namespace
kubectl delete pods --all -n namespace

# Force delete stuck pod
kubectl delete pod name --grace-period=0 --force

# Get events sorted by time
kubectl get events --sort-by='.lastTimestamp'

# Port forward
kubectl port-forward pod/name 8080:80

# Copy from pod
kubectl cp namespace/pod:/path ./local

# Get pod logs for crashed container
kubectl logs pod --previous

# Scale deployment
kubectl scale deployment name --replicas=3

# Rollback deployment
kubectl rollout undo deployment/name

# Get secret value
kubectl get secret name -o jsonpath='{.data.key}' | base64 -d
```

---

## B. Configuration Examples

### .bashrc Additions

```bash
# Add to ~/.bashrc

# Aliases
alias k='kubectl'
alias d='docker'
alias dc='docker compose'
alias ll='ls -la'
alias gs='git status'
alias gp='git pull'

# kubectl autocomplete
source <(kubectl completion bash)
complete -F __start_kubectl k

# docker autocomplete
# source <(docker completion bash)

# Prompt with git branch
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "

# History settings
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups
```

### .gitconfig

```ini
[user]
    name = Your Name
    email = your.email@example.com

[core]
    editor = code --wait
    autocrlf = input

[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --oneline --graph --all
    last = log -1 HEAD
    undo = reset HEAD~1 --mixed

[pull]
    rebase = false

[init]
    defaultBranch = main
```

### SSH Config

```ssh-config
# ~/.ssh/config

Host *
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519

Host server
    HostName 192.168.1.100
    User admin
    Port 22

Host prod-*
    User deploy
    IdentityFile ~/.ssh/deploy_key

Host prod-web
    HostName 10.0.1.10

Host prod-db
    HostName 10.0.1.20
```

---

## C. Script Collections

### Health Check Script

```bash
#!/bin/bash
# health_check.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check_service() {
    if systemctl is-active --quiet "$1"; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

check_url() {
    if curl -sf "$1" > /dev/null; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
    fi
}

echo "=== System Health Check ==="
echo ""
echo "--- Services ---"
for svc in nginx docker postgresql redis; do
    check_service "$svc"
done

echo ""
echo "--- Endpoints ---"
check_url "http://localhost"
check_url "http://localhost:5000/health"

echo ""
echo "--- Resources ---"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
echo "Mem: $(free -h | awk '/^Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h / | awk 'NR==2 {print $5}')"
```

### Backup Script

```bash
#!/bin/bash
# backup.sh

set -euo pipefail

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Database backup
pg_dump -h localhost -U user mydb | gzip > "${BACKUP_DIR}/db_${DATE}.sql.gz"

# Application backup
tar -czf "${BACKUP_DIR}/app_${DATE}.tar.gz" /var/www/app

# Upload to S3 (optional)
# aws s3 cp "${BACKUP_DIR}/db_${DATE}.sql.gz" s3://bucket/backups/

# Cleanup old backups
find "$BACKUP_DIR" -name "*.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed: ${DATE}"
```

### Log Rotation Script

```bash
#!/bin/bash
# rotate_logs.sh

LOG_DIR="/var/log/myapp"
ARCHIVE_DIR="/var/log/myapp/archive"
MAX_SIZE=100M
KEEP_DAYS=30

mkdir -p "$ARCHIVE_DIR"

for log in "$LOG_DIR"/*.log; do
    if [ -f "$log" ]; then
        size=$(stat -f%z "$log" 2>/dev/null || stat -c%s "$log")
        if [ "$size" -gt $((100*1024*1024)) ]; then
            gzip -c "$log" > "${ARCHIVE_DIR}/$(basename "$log").$(date +%Y%m%d).gz"
            > "$log"
        fi
    fi
done

find "$ARCHIVE_DIR" -name "*.gz" -mtime +$KEEP_DAYS -delete
```

---

## D. Regex Patterns

### Common Patterns

```regex
# IP Address
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b

# Email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# URL
https?://[^\s]+

# Date (YYYY-MM-DD)
\d{4}-\d{2}-\d{2}

# Time (HH:MM:SS)
\d{2}:\d{2}:\d{2}

# UUID
[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}

# Docker image tag
[a-z0-9]+([._-][a-z0-9]+)*(/[a-z0-9]+([._-][a-z0-9]+)*)*:[a-zA-Z0-9._-]+
```

### Log Parsing

```bash
# Extract IPs from log
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log

# Extract timestamps
grep -oE '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' app.log

# Count by status code
awk '{print $9}' access.log | sort | uniq -c | sort -rn
```

---

## E. Port Reference

### Standard Ports

| Port | Service | Protocol |
|------|---------|----------|
| 20, 21 | FTP | TCP |
| 22 | SSH | TCP |
| 23 | Telnet | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | TCP/UDP |
| 80 | HTTP | TCP |
| 110 | POP3 | TCP |
| 143 | IMAP | TCP |
| 443 | HTTPS | TCP |
| 993 | IMAPS | TCP |
| 995 | POP3S | TCP |

### Application Ports

| Port | Service |
|------|---------|
| 3000 | Node.js (default) |
| 3306 | MySQL |
| 5000 | Flask (default) |
| 5432 | PostgreSQL |
| 5672 | RabbitMQ |
| 6379 | Redis |
| 8080 | HTTP alternate |
| 8443 | HTTPS alternate |
| 9090 | Prometheus |
| 9200 | Elasticsearch |
| 9300 | Elasticsearch (cluster) |
| 27017 | MongoDB |

### Kubernetes Ports

| Port | Service |
|------|---------|
| 6443 | API Server |
| 2379-2380 | etcd |
| 10250 | Kubelet |
| 10251 | Scheduler |
| 10252 | Controller Manager |
| 30000-32767 | NodePort range |

---

## F. Exit Codes

### Standard Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of command |
| 126 | Permission problem |
| 127 | Command not found |
| 128 | Invalid argument |
| 128+N | Signal N received |
| 130 | Ctrl+C (128+2) |
| 137 | SIGKILL (128+9) |
| 143 | SIGTERM (128+15) |
| 255 | Exit status out of range |

### Docker Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Application error |
| 137 | Container was killed (OOM) |
| 139 | Segmentation fault |
| 143 | Graceful shutdown |

---

## G. Time Reference

### Cron Schedule

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6)
│ │ │ │ │
* * * * *
```

### Common Cron Schedules

```bash
0 * * * *     # Every hour
0 0 * * *     # Daily at midnight
0 0 * * 0     # Weekly on Sunday
0 0 1 * *     # Monthly on 1st
*/5 * * * *   # Every 5 minutes
0 9-17 * * *  # Every hour 9am-5pm
```

### Time Calculations

| Duration | Seconds | Minutes |
|----------|---------|---------|
| 1 minute | 60 | 1 |
| 1 hour | 3,600 | 60 |
| 1 day | 86,400 | 1,440 |
| 1 week | 604,800 | 10,080 |
| 30 days | 2,592,000 | 43,200 |
| 1 year | 31,536,000 | 525,600 |

---

**📌 Use this appendix as a quick reference!**
