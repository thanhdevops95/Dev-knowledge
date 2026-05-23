# 💪 Exercises: Python Basics

> **Self-practice exercises for Python DevOps.**
>
> *Bài tập tự luyện Python cho DevOps.*

---

## 📋 Instructions (Hướng dẫn)

- Complete exercises after finishing Labs *(Làm bài tập sau khi hoàn thành Labs)*
- Difficulty: ⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Hard
- Check Solutions after trying yourself *(Xem Solutions sau khi thử tự làm)*

---

## 📊 Exercise 1: Data Structures ⭐

### Tasks

1. Create a list `servers` containing 5 server names *(Tạo list `servers` chứa 5 server names)*
2. Add 2 new servers to the end of the list *(Thêm 2 servers mới vào cuối list)*
3. Remove the 3rd server *(Xóa server thứ 3)*
4. Sort the list alphabetically *(Sắp xếp list theo alphabet)*
5. Create dictionary `server_info` mapping server name → IP address *(Tạo dictionary mapping server name → IP)*
6. Print all servers with IP starting with "192" *(In ra tất cả servers có IP bắt đầu bằng "192")*

---

## 📝 Exercise 2: String Processing ⭐

### Task

Write function `parse_log_line(line)` to parse a log line:

*(Viết function `parse_log_line(line)` phân tích log line:)*

Input:

```
"2024-01-15 10:30:00 ERROR Database connection failed"
```

Output:

```python
{
    "date": "2024-01-15",
    "time": "10:30:00",
    "level": "ERROR",
    "message": "Database connection failed"
}
```

---

## 🔄 Exercise 3: File Processing ⭐⭐

### Task

Write a script to read file `/etc/passwd` (or create a mock file) and:

*(Viết script đọc file `/etc/passwd` (hoặc tạo file giả) và:)*

1. Count number of users *(Đếm số users)*
2. List users with shell `/bin/bash` *(Liệt kê users có shell là `/bin/bash`)*
3. Find users with UID >= 1000 *(Tìm users có UID >= 1000)*
4. Export results to JSON file *(Export kết quả ra JSON file)*

---

## 🌐 Exercise 4: API Client ⭐⭐

### Task

Write class `GitHubClient` with methods:

*(Viết class `GitHubClient` với methods:)*

```python
class GitHubClient:
    def get_user(self, username) -> dict:
        """Get user info"""
        pass
    
    def get_repos(self, username) -> list:
        """Get user's public repos"""
        pass
    
    def get_repo_languages(self, owner, repo) -> dict:
        """Get languages used in a repo"""
        pass
```

Test with real GitHub API.

---

## 🔧 Exercise 5: Config Parser ⭐⭐

### Task

Write a function to read config from multiple sources with priority:

*(Viết function đọc config từ nhiều sources với priority:)*

1. Default values (lowest)
2. Config file (YAML)
3. Environment variables
4. Command line args (highest)

```python
def load_config(config_file, cli_args) -> dict:
    """
    Returns merged config with proper priority.
    """
    pass
```

---

## 📊 Exercise 6: Log Aggregator ⭐⭐⭐

### Task

Write a script to analyze multiple log files:

*(Viết script phân tích multiple log files:)*

Features:

- Read all `.log` files in a folder *(Đọc tất cả `.log` files trong folder)*
- Aggregate errors by type
- Generate HTML report with:
  - Pie chart (text-based) of error types
  - Timeline of errors
  - Top 10 frequent errors

---

## 🖥️ Exercise 7: Server Monitor ⭐⭐⭐

### Task

Write class `ServerMonitor`:

*(Viết class `ServerMonitor`:)*

```python
class ServerMonitor:
    def __init__(self, servers: list):
        pass
    
    def check_ping(self, host) -> bool:
        """Check if host responds to ping"""
        pass
    
    def check_port(self, host, port) -> bool:
        """Check if port is open"""
        pass
    
    def check_http(self, url) -> dict:
        """Check HTTP endpoint, return status + response time"""
        pass
    
    def run_all_checks(self) -> list:
        """Run all checks on all servers"""
        pass
    
    def generate_report(self) -> str:
        """Generate markdown report"""
        pass
```

---

## 🔐 Exercise 8: Password Generator ⭐

### Task

Write a CLI tool to create secure passwords:

*(Viết CLI tool tạo secure passwords:)*

```bash
python password_gen.py --length 16 --uppercase --lowercase --digits --special
```

Features:

- Configurable length
- Include/exclude character types
- Copy to clipboard (optional)
- Check against common passwords list

---

## 📦 Exercise 9: Backup Script ⭐⭐

### Task

Write a backup script with features:

*(Viết backup script với features:)*

```python
def backup_directory(
    source: str,
    destination: str,
    compress: bool = True,
    exclude_patterns: list = None,
    max_backups: int = 5
) -> str:
    """
    Backup a directory.
    
    Returns path to backup file.
    Rotates old backups (keeps max_backups).
    """
    pass
```

---

## 🚀 Exercise 10: Deployment Script ⭐⭐⭐

### Task

Write deployment automation:

*(Viết deployment automation:)*

```python
class Deployer:
    def __init__(self, config_file: str):
        pass
    
    def validate_config(self) -> bool:
        """Validate deployment configuration"""
        pass
    
    def pre_deploy_checks(self) -> bool:
        """Run pre-deployment checks"""
        pass
    
    def deploy(self, version: str, environment: str) -> bool:
        """
        Execute deployment:
        1. Pull latest code
        2. Run tests
        3. Build application
        4. Stop old version
        5. Deploy new version
        6. Health check
        7. Rollback if failed
        """
        pass
    
    def rollback(self, version: str) -> bool:
        """Rollback to previous version"""
        pass
```

---

## 📝 Checklist

- [ ] Exercise 1: Data Structures
- [ ] Exercise 2: String Processing
- [ ] Exercise 3: File Processing
- [ ] Exercise 4: API Client
- [ ] Exercise 5: Config Parser
- [ ] Exercise 6: Log Aggregator
- [ ] Exercise 7: Server Monitor
- [ ] Exercise 8: Password Generator
- [ ] Exercise 9: Backup Script
- [ ] Exercise 10: Deployment Script

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
