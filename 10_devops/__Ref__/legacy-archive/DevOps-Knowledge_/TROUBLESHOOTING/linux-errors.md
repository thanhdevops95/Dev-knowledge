# Linux Errors & Troubleshooting

> Các lỗi Linux thường gặp và cách xử lý

## 📋 Mục lục

- [Permission Errors](#permission-errors)
- [Disk Space Issues](#disk-space-issues)
- [Network Issues](#network-issues)
- [Process Issues](#process-issues)
- [Package Management](#package-management)
- [System Issues](#system-issues)

## Permission Errors

### Error: "Permission denied"

**Lỗi:**
```bash
bash: ./script.sh: Permission denied
```

**Giải pháp:**
```bash
# Add execute permission
chmod +x script.sh

# Or run with bash
bash script.sh

# Check current permissions
ls -l script.sh
```

### Error: "Operation not permitted"

**Nguyên nhân:** Cần quyền root

**Giải pháp:**
```bash
# Use sudo
sudo command

# Switch to root (not recommended)
sudo -i

# Check if you're in sudoers
sudo -l
```

## Disk Space Issues

### Error: "No space left on device"

**Giải pháp:**
```bash
# Check disk usage
df -h

# Find large directories
du -sh /* | sort -hr | head -10
du -h --max-depth=1 /var | sort -hr

# Clean up
sudo apt clean                    # Clean package cache
sudo journalctl --vacuum-time=3d  # Clean old logs
docker system prune -a            # Clean Docker

# Find and remove large files
find / -type f -size +100M 2>/dev/null
```

*Nội dung sẽ được bổ sung thêm...*

---

