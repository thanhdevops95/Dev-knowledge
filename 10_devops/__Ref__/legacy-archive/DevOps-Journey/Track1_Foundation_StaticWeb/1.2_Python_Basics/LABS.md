# 🔬 Labs: Python Basics

> **Hands-on Labs for Python DevOps Automation**
>
> *Bài thực hành Python cho DevOps automation.*

---

## 🎯 Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- VS Code với Python extension
- Terminal/Command line

### Verify Setup

```bash
python3 --version
pip3 --version
```

---

## 🔬 Lab 1: Python Environment Setup (Cài đặt môi trường Python)

### Objectives

- Install Python environment (Cài đặt môi trường Python)
- Create virtual environment (Tạo môi trường ảo)
- Install packages (Cài đặt các gói)

### Steps

#### Step 1: Create Project Directory

```bash
mkdir ~/python-devops-lab
cd ~/python-devops-lab
```

#### Step 2: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate

# Verify
which python  # Should show venv path
```

#### Step 3: Install Common Packages

```bash
pip install requests pyyaml python-dotenv
pip freeze > requirements.txt
cat requirements.txt
```

#### Step 4: Create First Script

```python
# hello.py
#!/usr/bin/env python3
"""My first DevOps Python script."""

import sys
import platform

def main():
    print("=" * 40)
    print("DevOps Python Lab")
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print("=" * 40)

if __name__ == "__main__":
    main()
```

```bash
python hello.py
```

---

## 🔬 Lab 2: Working with Files (Làm việc với File)

### Objectives

- Read and write files (Đọc và ghi files)
- Process text files (Xử lý text files)
- Work with JSON and YAML (Làm việc với JSON và YAML)

### Steps

#### Step 1: Create Sample Files

```bash
mkdir -p data logs
```

```python
# create_files.py
#!/usr/bin/env python3
"""Create sample files for lab."""

import json
import os

# Create sample log file
log_content = """2024-01-15 10:00:00 INFO Application started
2024-01-15 10:05:00 INFO User login: admin
2024-01-15 10:10:00 WARNING High memory usage: 85%
2024-01-15 10:15:00 ERROR Database connection failed
2024-01-15 10:20:00 INFO Retrying connection
2024-01-15 10:25:00 INFO Database connected
2024-01-15 10:30:00 ERROR API timeout
2024-01-15 10:35:00 INFO Request completed
"""

with open("logs/app.log", "w") as f:
    f.write(log_content)
print("Created logs/app.log")

# Create JSON config
config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "servers": [
        {"name": "web1", "host": "192.168.1.10", "port": 80},
        {"name": "web2", "host": "192.168.1.11", "port": 80},
        {"name": "db1", "host": "192.168.1.20", "port": 3306}
    ],
    "settings": {
        "debug": True,
        "log_level": "INFO",
        "timeout": 30
    }
}

with open("data/config.json", "w") as f:
    json.dump(config, f, indent=2)
print("Created data/config.json")
```

#### Step 2: Read and Parse Files

```python
# file_operations.py
#!/usr/bin/env python3
"""File operations lab."""

import json

# Read text file line by line
print("=== Reading Log File ===")
with open("logs/app.log", "r") as f:
    for line_num, line in enumerate(f, 1):
        print(f"{line_num}: {line.strip()}")

print("\n=== Parsing JSON Config ===")
with open("data/config.json", "r") as f:
    config = json.load(f)

print(f"App Name: {config['app_name']}")
print(f"Version: {config['version']}")
print(f"Debug Mode: {config['settings']['debug']}")

print("\nServers:")
for server in config['servers']:
    print(f"  - {server['name']}: {server['host']}:{server['port']}")
```

#### Step 3: Log Analyzer Script

```python
# log_analyzer.py
#!/usr/bin/env python3
"""Analyze log files."""

from collections import Counter

def analyze_log(filepath):
    """Analyze log file and return statistics."""
    stats = {
        "total_lines": 0,
        "levels": Counter(),
        "errors": []
    }
    
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            stats["total_lines"] += 1
            
            # Extract log level
            parts = line.split()
            if len(parts) >= 3:
                level = parts[2]
                stats["levels"][level] += 1
                
                if level == "ERROR":
                    # Get error message
                    message = " ".join(parts[3:])
                    stats["errors"].append({
                        "timestamp": f"{parts[0]} {parts[1]}",
                        "message": message
                    })
    
    return stats

def main():
    stats = analyze_log("logs/app.log")
    
    print("=" * 50)
    print("LOG ANALYSIS REPORT")
    print("=" * 50)
    print(f"\nTotal Lines: {stats['total_lines']}")
    
    print("\nLog Levels:")
    for level, count in stats["levels"].items():
        percentage = (count / stats["total_lines"]) * 100
        print(f"  {level}: {count} ({percentage:.1f}%)")
    
    print(f"\nErrors Found: {len(stats['errors'])}")
    for error in stats["errors"]:
        print(f"  [{error['timestamp']}] {error['message']}")

if __name__ == "__main__":
    main()
```

---

## 🔬 Lab 3: System Information Script (Script thông tin hệ thống)

### Objectives

- Use os and platform modules (Sử dụng os và platform modules)
- Collect system information (Thu thập thông tin hệ thống)
- Format output (Định dạng đầu ra)

### Steps

```python
# sysinfo.py
#!/usr/bin/env python3
"""System Information Collector."""

import os
import platform
import subprocess
import socket
from datetime import datetime

def get_size(bytes_val, suffix="B"):
    """Convert bytes to human readable format."""
    for unit in ["", "K", "M", "G", "T"]:
        if abs(bytes_val) < 1024.0:
            return f"{bytes_val:.2f}{unit}{suffix}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f}P{suffix}"

def get_system_info():
    """Collect system information."""
    info = {}
    
    # Basic info
    info["hostname"] = socket.gethostname()
    info["platform"] = platform.system()
    info["platform_release"] = platform.release()
    info["platform_version"] = platform.version()
    info["architecture"] = platform.machine()
    info["processor"] = platform.processor()
    info["python_version"] = platform.python_version()
    
    # Current time
    info["current_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Environment
    info["user"] = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
    info["home"] = os.environ.get("HOME", os.environ.get("USERPROFILE", "unknown"))
    info["cwd"] = os.getcwd()
    
    return info

def print_report(info):
    """Print formatted report."""
    width = 60
    print("=" * width)
    print("SYSTEM INFORMATION REPORT".center(width))
    print("=" * width)
    print()
    
    print("General:")
    print(f"  Hostname      : {info['hostname']}")
    print(f"  Platform      : {info['platform']} {info['platform_release']}")
    print(f"  Architecture  : {info['architecture']}")
    print(f"  Processor     : {info['processor']}")
    print()
    
    print("Environment:")
    print(f"  User          : {info['user']}")
    print(f"  Home          : {info['home']}")
    print(f"  Working Dir   : {info['cwd']}")
    print(f"  Python Version: {info['python_version']}")
    print()
    
    print(f"Report Generated: {info['current_time']}")
    print("=" * width)

if __name__ == "__main__":
    info = get_system_info()
    print_report(info)
```

---

## 🔬 Lab 4: Working with APIs (Làm việc với APIs)

### Objectives

- Use requests library (Sử dụng thư viện requests)
- Parse JSON responses (Phân tích phản hồi JSON)
- Error handling (Xử lý lỗi)

### Steps

#### Step 1: Basic API Request

```python
# api_basics.py
#!/usr/bin/env python3
"""API basics with requests."""

import requests
import json

def get_github_user(username):
    """Fetch GitHub user information."""
    url = f"https://api.github.com/users/{username}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    username = "torvalds"  # Linux creator
    
    print(f"Fetching GitHub info for: {username}")
    print("-" * 40)
    
    user_data = get_github_user(username)
    
    if user_data:
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Bio: {user_data.get('bio', 'N/A')}")
        print(f"Public Repos: {user_data.get('public_repos', 0)}")
        print(f"Followers: {user_data.get('followers', 0)}")
        print(f"Location: {user_data.get('location', 'N/A')}")
    else:
        print("Failed to fetch user data")

if __name__ == "__main__":
    main()
```

#### Step 2: Server Health Checker

```python
# health_checker.py
#!/usr/bin/env python3
"""Check health of multiple servers/URLs."""

import requests
from concurrent.futures import ThreadPoolExecutor
import time

def check_url(url):
    """Check if URL is accessible."""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        elapsed = (time.time() - start_time) * 1000  # ms
        
        return {
            "url": url,
            "status": "UP",
            "status_code": response.status_code,
            "response_time_ms": round(elapsed, 2)
        }
    except requests.exceptions.Timeout:
        return {"url": url, "status": "TIMEOUT", "status_code": None, "response_time_ms": None}
    except requests.exceptions.RequestException as e:
        return {"url": url, "status": "DOWN", "status_code": None, "error": str(e)}

def main():
    urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.python.org",
        "https://httpstat.us/500",  # Returns 500
        "https://nonexistent.example.com",  # Will fail
    ]
    
    print("=" * 70)
    print("HEALTH CHECK REPORT")
    print("=" * 70)
    print(f"{'URL':<40} {'STATUS':<10} {'CODE':<6} {'TIME'}")
    print("-" * 70)
    
    # Check URLs in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_url, urls))
    
    for result in results:
        status = result["status"]
        code = result.get("status_code", "N/A")
        time_ms = result.get("response_time_ms", "N/A")
        
        # Color coding (ANSI)
        if status == "UP" and result.get("status_code", 0) < 400:
            status_display = f"\033[92m{status}\033[0m"  # Green
        elif status == "UP":
            status_display = f"\033[93m{status}\033[0m"  # Yellow
        else:
            status_display = f"\033[91m{status}\033[0m"  # Red
        
        print(f"{result['url']:<40} {status:<10} {str(code):<6} {time_ms}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
```

---

## 🔬 Lab 5: Subprocess and Command Execution (Subprocess và thực thi lệnh)

### Objectives

- Run system commands from Python (Chạy lệnh hệ thống từ Python)
- Capture output (Bắt đầu ra)
- Handle errors (Xử lý lỗi)

### Steps

```python
# run_commands.py
#!/usr/bin/env python3
"""Execute system commands from Python."""

import subprocess
import sys

def run_command(command, shell=False):
    """Run a command and return output."""
    try:
        if shell:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
        else:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    print("=== Running System Commands ===\n")
    
    # Command 1: Get hostname
    print("1. Getting hostname:")
    result = run_command(["hostname"])
    if result["success"]:
        print(f"   Hostname: {result['stdout'].strip()}")
    
    # Command 2: List directory
    print("\n2. Listing current directory:")
    if sys.platform == "win32":
        result = run_command(["dir"], shell=True)
    else:
        result = run_command(["ls", "-la"])
    
    if result["success"]:
        print(result["stdout"][:500])  # First 500 chars
    
    # Command 3: Get disk usage
    print("\n3. Disk usage:")
    if sys.platform != "win32":
        result = run_command(["df", "-h"])
        if result["success"]:
            print(result["stdout"])
    
    # Command 4: Chain commands with pipe (shell=True)
    print("\n4. Counting Python files:")
    if sys.platform != "win32":
        result = run_command("find . -name '*.py' | wc -l", shell=True)
        if result["success"]:
            print(f"   Python files found: {result['stdout'].strip()}")

if __name__ == "__main__":
    main()
```

---

## 🔬 Lab 6: Configuration Management (Quản lý cấu hình)

### Objectives

- Read config from multiple sources (Đọc config từ nhiều nguồn)
- Environment variables (Biến môi trường)
- Command line arguments (Tham số dòng lệnh)

### Steps

#### Step 1: Create Config Files

```yaml
# config.yaml
app:
  name: MyDevOpsApp
  version: 1.0.0
  
server:
  host: localhost
  port: 8080
  
database:
  host: localhost
  port: 5432
  name: myapp
  
logging:
  level: INFO
  file: /var/log/app.log
```

```python
# config_manager.py
#!/usr/bin/env python3
"""Configuration management example."""

import os
import yaml
import argparse
from dataclasses import dataclass
from typing import Optional

@dataclass
class ServerConfig:
    host: str
    port: int

@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: Optional[str] = None
    password: Optional[str] = None

@dataclass
class AppConfig:
    name: str
    version: str
    server: ServerConfig
    database: DatabaseConfig
    debug: bool = False

def load_yaml_config(filepath: str) -> dict:
    """Load configuration from YAML file."""
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def get_config(config_file: str, args: argparse.Namespace) -> AppConfig:
    """Build configuration from file, env vars, and CLI args."""
    
    # Load from file
    file_config = load_yaml_config(config_file)
    
    # Build config with environment variable overrides
    server = ServerConfig(
        host=os.getenv("SERVER_HOST", file_config["server"]["host"]),
        port=int(os.getenv("SERVER_PORT", file_config["server"]["port"]))
    )
    
    database = DatabaseConfig(
        host=os.getenv("DB_HOST", file_config["database"]["host"]),
        port=int(os.getenv("DB_PORT", file_config["database"]["port"])),
        name=os.getenv("DB_NAME", file_config["database"]["name"]),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    # CLI args override everything
    if args.port:
        server.port = args.port
    
    return AppConfig(
        name=file_config["app"]["name"],
        version=file_config["app"]["version"],
        server=server,
        database=database,
        debug=args.debug
    )

def main():
    parser = argparse.ArgumentParser(description="Config Management Demo")
    parser.add_argument("-c", "--config", default="config.yaml", help="Config file path")
    parser.add_argument("-p", "--port", type=int, help="Override server port")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    config = get_config(args.config, args)
    
    print("=" * 50)
    print("CONFIGURATION")
    print("=" * 50)
    print(f"App: {config.name} v{config.version}")
    print(f"Debug: {config.debug}")
    print(f"\nServer: {config.server.host}:{config.server.port}")
    print(f"Database: {config.database.host}:{config.database.port}/{config.database.name}")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

---

## 🔬 Lab 7: Automation Script - Server Provisioner (Script tự động hóa - Server Provisioner)

### Objectives

- Combine all skills (Kết hợp tất cả kỹ năng)
- Create automation script (Tạo script tự động hóa)
- Error handling and logging (Xử lý lỗi và ghi log)

### Steps

```python
# server_provisioner.py
#!/usr/bin/env python3
"""
Server Provisioner - Automation Example
Simulates provisioning a server with various configurations.
"""

import os
import json
import logging
import argparse
import subprocess
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("provisioner.log")
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProvisioningResult:
    step: str
    success: bool
    message: str
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class ServerProvisioner:
    """Handles server provisioning tasks."""
    
    def __init__(self, hostname: str, dry_run: bool = False):
        self.hostname = hostname
        self.dry_run = dry_run
        self.results: List[ProvisioningResult] = []
    
    def log_result(self, step: str, success: bool, message: str):
        """Log a provisioning result."""
        result = ProvisioningResult(step=step, success=success, message=message)
        self.results.append(result)
        
        if success:
            logger.info(f"[{step}] ✓ {message}")
        else:
            logger.error(f"[{step}] ✗ {message}")
    
    def run_command(self, command: str) -> bool:
        """Run a shell command."""
        if self.dry_run:
            logger.info(f"[DRY-RUN] Would execute: {command}")
            return True
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return False
    
    def update_system(self) -> bool:
        """Update system packages."""
        step = "System Update"
        logger.info(f"Starting {step}...")
        
        # Simulate update (would be apt update && apt upgrade -y)
        success = self.run_command("echo 'Updating system...'")
        self.log_result(step, success, "System packages updated" if success else "Update failed")
        return success
    
    def install_packages(self, packages: List[str]) -> bool:
        """Install required packages."""
        step = "Install Packages"
        logger.info(f"Installing packages: {', '.join(packages)}")
        
        all_success = True
        for package in packages:
            # Simulate installation
            success = self.run_command(f"echo 'Installing {package}...'")
            if not success:
                all_success = False
                self.log_result(step, False, f"Failed to install {package}")
        
        if all_success:
            self.log_result(step, True, f"Installed {len(packages)} packages")
        return all_success
    
    def create_user(self, username: str) -> bool:
        """Create a system user."""
        step = "Create User"
        logger.info(f"Creating user: {username}")
        
        success = self.run_command(f"echo 'Creating user {username}...'")
        self.log_result(step, success, f"User {username} created" if success else f"Failed to create {username}")
        return success
    
    def setup_directories(self, directories: List[str]) -> bool:
        """Create required directories."""
        step = "Setup Directories"
        logger.info("Setting up directories...")
        
        all_success = True
        for directory in directories:
            if self.dry_run:
                logger.info(f"[DRY-RUN] Would create: {directory}")
            else:
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    all_success = False
                    logger.error(f"Failed to create {directory}: {e}")
        
        self.log_result(step, all_success, f"Created {len(directories)} directories")
        return all_success
    
    def configure_firewall(self, ports: List[int]) -> bool:
        """Configure firewall rules."""
        step = "Configure Firewall"
        logger.info(f"Configuring firewall for ports: {ports}")
        
        success = self.run_command(f"echo 'Opening ports: {ports}'")
        self.log_result(step, success, f"Firewall configured for {len(ports)} ports")
        return success
    
    def generate_report(self) -> dict:
        """Generate provisioning report."""
        report = {
            "hostname": self.hostname,
            "dry_run": self.dry_run,
            "total_steps": len(self.results),
            "successful": sum(1 for r in self.results if r.success),
            "failed": sum(1 for r in self.results if not r.success),
            "details": [asdict(r) for r in self.results],
            "generated_at": datetime.now().isoformat()
        }
        return report
    
    def provision(self, config: dict) -> bool:
        """Run full provisioning."""
        logger.info(f"Starting provisioning for {self.hostname}")
        logger.info("=" * 50)
        
        steps = [
            ("update_system", lambda: self.update_system()),
            ("install_packages", lambda: self.install_packages(config.get("packages", []))),
            ("create_user", lambda: self.create_user(config.get("user", "deploy"))),
            ("setup_directories", lambda: self.setup_directories(config.get("directories", []))),
            ("configure_firewall", lambda: self.configure_firewall(config.get("ports", []))),
        ]
        
        all_success = True
        for step_name, step_func in steps:
            if not step_func():
                all_success = False
                if config.get("fail_fast", False):
                    logger.error("Fail-fast enabled, stopping provisioning")
                    break
        
        logger.info("=" * 50)
        logger.info("Provisioning complete!")
        
        return all_success

def main():
    parser = argparse.ArgumentParser(description="Server Provisioner")
    parser.add_argument("hostname", help="Target hostname")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without making changes")
    parser.add_argument("--config", default=None, help="Config file path")
    parser.add_argument("--output", default="report.json", help="Output report file")
    args = parser.parse_args()
    
    # Default configuration
    config = {
        "packages": ["nginx", "docker-ce", "git"],
        "user": "deploy",
        "directories": ["/opt/apps", "/var/log/apps", "/etc/app-configs"],
        "ports": [22, 80, 443],
        "fail_fast": False
    }
    
    # Load config from file if provided
    if args.config and os.path.exists(args.config):
        with open(args.config) as f:
            config.update(json.load(f))
    
    # Run provisioning
    provisioner = ServerProvisioner(args.hostname, dry_run=args.dry_run)
    success = provisioner.provision(config)
    
    # Generate and save report
    report = provisioner.generate_report()
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Report saved to {args.output}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("PROVISIONING SUMMARY")
    print("=" * 50)
    print(f"Hostname: {report['hostname']}")
    print(f"Dry Run: {report['dry_run']}")
    print(f"Total Steps: {report['total_steps']}")
    print(f"Successful: {report['successful']}")
    print(f"Failed: {report['failed']}")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
```

---

## ✅ Lab Completion Checklist

- [ ] Lab 1: Python Environment Setup
- [ ] Lab 2: Working with Files
- [ ] Lab 3: System Information Script
- [ ] Lab 4: Working with APIs
- [ ] Lab 5: Subprocess and Command Execution
- [ ] Lab 6: Configuration Management
- [ ] Lab 7: Server Provisioner

---

**[← Back to README](./README.md)** | **[Go to Exercises →](./EXERCISES.md)**
