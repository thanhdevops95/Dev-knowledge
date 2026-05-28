# 🔧 Troubleshooting Guide

> **Hướng dẫn debug các vấn đề DevOps phổ biến**

---

## 🔴 Quick Diagnosis Flowchart

```
Problem Reported
       │
       ▼
┌──────────────────┐
│ Can you access   │──No──► Check Network
│ the server?      │
└────────┬─────────┘
         │ Yes
         ▼
┌──────────────────┐
│ Is the service   │──No──► Check Service Status
│ running?         │
└────────┬─────────┘
         │ Yes
         ▼
┌──────────────────┐
│ Are there        │──Yes──► Analyze Error Logs
│ errors in logs?  │
└────────┬─────────┘
         │ No
         ▼
┌──────────────────┐
│ Is it a          │──Yes──► Check Metrics
│ performance issue│
└────────┬─────────┘
         │ No
         ▼
    Continue investigating...
```

---

## 1. Network Issues

### Cannot Connect to Server

```bash
# Step 1: Check if host is reachable
ping hostname

# Step 2: Check if port is open
nc -zv hostname port
curl -v hostname:port

# Step 3: Check DNS resolution
nslookup hostname
dig hostname

# Step 4: Check route
traceroute hostname

# Step 5: Check local firewall
sudo iptables -L -n
sudo ufw status
```

### Common Causes & Solutions

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| Connection refused | Service not running | `systemctl start service` |
| Connection timeout | Firewall blocking | Check firewall rules |
| No route to host | Network config | Check routing tables |
| Name resolution failed | DNS issue | Check DNS config |

---

## 2. Application Issues

### Service Won't Start

```bash
# Step 1: Check service status
systemctl status service-name

# Step 2: Check logs
journalctl -u service-name -n 50
journalctl -u service-name -f  # Follow live

# Step 3: Check config syntax
nginx -t
apache2ctl configtest

# Step 4: Check port conflicts
ss -tuln | grep :port
lsof -i :port

# Step 5: Check permissions
ls -la /path/to/config
ls -la /path/to/data
```

### Application Crashing

```bash
# Check application logs
tail -f /var/log/app/error.log

# Check system logs
dmesg | tail -20
journalctl -xe

# Check memory (OOM killer?)
dmesg | grep -i "killed process"
free -h

# Check disk space
df -h
```

---

## 3. Docker Issues

### Container Won't Start

```bash
# Check container logs
docker logs container-name

# Check container details
docker inspect container-name

# Check if image exists
docker images | grep image-name

# Try running interactively
docker run -it --entrypoint sh image-name
```

### Container Keeps Restarting

```bash
# Check exit code
docker inspect container-name --format='{{.State.ExitCode}}'

# Common exit codes:
# 0   - Normal exit
# 1   - Application error
# 137 - OOM killed (128 + 9)
# 143 - SIGTERM (128 + 15)

# Check previous logs
docker logs container-name --tail 100
```

### Docker Troubleshooting Table

| Error | Cause | Solution |
|-------|-------|----------|
| `image not found` | Wrong image name | Check Docker Hub |
| `port already in use` | Port conflict | Use different port |
| `permission denied` | Socket access | Add user to docker group |
| `no space left` | Disk full | `docker system prune` |
| `OOMKilled` | Memory limit | Increase memory limit |

---

## 4. Kubernetes Issues

### Pod Stuck in Pending

```bash
# Check pod events
kubectl describe pod pod-name

# Common causes:
# - Insufficient resources → Scale cluster
# - No matching nodes → Check node selector/affinity
# - PVC not bound → Check storage class
```

### Pod CrashLoopBackOff

```bash
# Check logs
kubectl logs pod-name
kubectl logs pod-name --previous

# Check container command
kubectl describe pod pod-name | grep -A5 "Command"

# Debug with shell
kubectl run debug --image=busybox -it --rm -- sh
```

### Kubernetes Troubleshooting Table

| Status | Meaning | Action |
|--------|---------|--------|
| Pending | Can't schedule | Check resources, node selector |
| CrashLoopBackOff | App crashing | Check logs |
| ImagePullBackOff | Can't pull image | Check image name, registry auth |
| OOMKilled | Out of memory | Increase memory limit |
| Error | Container failed | Check logs |

---

## 5. Database Issues

### Cannot Connect to Database

```bash
# Check if service is running
systemctl status postgresql
systemctl status mysql

# Check if port is listening
ss -tuln | grep 5432
ss -tuln | grep 3306

# Check access from app server
psql -h db-host -U user -d database
mysql -h db-host -u user -p database

# Check pg_hba.conf / mysql access
cat /etc/postgresql/*/main/pg_hba.conf
```

### Slow Queries

```bash
# PostgreSQL - find slow queries
SELECT pid, now() - query_start AS duration, query 
FROM pg_stat_activity 
WHERE state = 'active' AND now() - query_start > interval '5 seconds';

# MySQL - find slow queries
SHOW FULL PROCESSLIST;
```

---

## 6. Performance Issues

### High CPU Usage

```bash
# Find CPU-hungry processes
top -c
htop

# Find specific process
ps aux --sort=-%cpu | head

# Profile application
perf top
strace -p PID
```

### High Memory Usage

```bash
# Check memory usage
free -h
vmstat 1

# Find memory-hungry processes
ps aux --sort=-%mem | head

# Check for memory leaks
# Watch memory grow over time
while true; do free -h; sleep 5; done
```

### High Disk I/O

```bash
# Check I/O usage
iotop
iostat -x 1

# Find large files
du -sh /* | sort -h
ncdu /
```

### Disk Full

```bash
# Find large files
du -sh /* | sort -h
find / -type f -size +100M

# Find large logs
du -sh /var/log/*

# Clear package cache
apt clean
yum clean all

# Clear Docker
docker system prune -a
```

---

## 7. SSL/TLS Issues

### Certificate Problems

```bash
# Check certificate expiry
echo | openssl s_client -connect host:443 2>/dev/null | openssl x509 -noout -dates

# Check certificate chain
openssl s_client -connect host:443 -showcerts

# Verify certificate file
openssl x509 -in cert.pem -text -noout

# Test SSL configuration
openssl s_client -connect host:443
```

---

## 8. Log Analysis

### Common Log Locations

| Application | Log Path |
|-------------|----------|
| System | `/var/log/syslog` or `/var/log/messages` |
| Auth | `/var/log/auth.log` |
| Nginx | `/var/log/nginx/` |
| Apache | `/var/log/apache2/` |
| Docker | `docker logs container` |
| Kubernetes | `kubectl logs pod` |
| PostgreSQL | `/var/log/postgresql/` |
| MySQL | `/var/log/mysql/` |

### Log Analysis Commands

```bash
# Search for errors
grep -i error /var/log/app.log

# Count error occurrences
grep -c ERROR /var/log/app.log

# Find unique errors
grep ERROR /var/log/app.log | sort | uniq -c | sort -rn

# Watch live logs
tail -f /var/log/app.log | grep --line-buffered ERROR

# Logs from specific time
journalctl --since "1 hour ago"
journalctl --since "2024-01-15 10:00:00"
```

---

## 9. Quick Recovery Actions

### Emergency Commands

```bash
# Restart service
sudo systemctl restart service-name

# Restart Docker container
docker restart container-name

# Kubernetes rollback
kubectl rollout undo deployment/app-name

# Clear caches
sync; echo 3 > /proc/sys/vm/drop_caches  # Linux cache
redis-cli FLUSHALL  # Redis

# Kill runaway process
pkill -9 process-name
```

### Escalation Checklist

1. ✅ Document the issue
2. ✅ Collect logs and metrics
3. ✅ Note timeline of events
4. ✅ List attempted solutions
5. ✅ Identify impact scope
6. ✅ Escalate with context

---

## 📞 When to Escalate

| Severity | Examples | Action |
|----------|----------|--------|
| **Critical** | Production down, data loss | Immediate escalation |
| **High** | Major feature broken | Escalate within 15 min |
| **Medium** | Degraded performance | Escalate within 1 hour |
| **Low** | Minor issues | Normal process |

---

**💡 Remember: Always check logs first!**
