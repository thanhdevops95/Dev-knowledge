# ✅ Solutions: Python Basics

> Solutions for Exercises. **Try to solve it yourself first!**
>
> *Đáp án cho Exercises. **Thử tự làm trước khi xem!***

---

## Exercise 1: Data Structures

```python
# 1. Create list
servers = ["web1", "web2", "web3", "db1", "db2"]

# 2. Add 2 servers
servers.append("cache1")
servers.append("cache2")

# 3. Remove 3rd server
servers.pop(2)  # or del servers[2]

# 4. Sort alphabetically
servers.sort()

# 5. Create dictionary
server_info = {
    "web1": "192.168.1.10",
    "web2": "192.168.1.11",
    "db1": "10.0.0.20",
    "db2": "10.0.0.21",
    "cache1": "192.168.1.30"
}

# 6. Filter by IP prefix
for name, ip in server_info.items():
    if ip.startswith("192"):
        print(f"{name}: {ip}")
```

---

## Exercise 2: String Processing

```python
def parse_log_line(line: str) -> dict:
    """Parse log line into components."""
    parts = line.strip().split(" ", 3)
    
    if len(parts) < 4:
        raise ValueError("Invalid log format")
    
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3]
    }

# Test
line = "2024-01-15 10:30:00 ERROR Database connection failed"
result = parse_log_line(line)
print(result)
# {'date': '2024-01-15', 'time': '10:30:00', 'level': 'ERROR', 'message': 'Database connection failed'}
```

---

## Exercise 3: File Processing

```python
#!/usr/bin/env python3
"""Process /etc/passwd file."""

import json

def parse_passwd_file(filepath="/etc/passwd"):
    users = []
    
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) >= 7:
                users.append({
                    "username": parts[0],
                    "uid": int(parts[2]),
                    "gid": int(parts[3]),
                    "home": parts[5],
                    "shell": parts[6]
                })
    
    return users

def analyze_users(users):
    total = len(users)
    bash_users = [u for u in users if u["shell"] == "/bin/bash"]
    regular_users = [u for u in users if u["uid"] >= 1000]
    
    return {
        "total_users": total,
        "bash_users": [u["username"] for u in bash_users],
        "regular_users": [u["username"] for u in regular_users]
    }

def main():
    users = parse_passwd_file()
    analysis = analyze_users(users)
    
    # Export to JSON
    with open("users_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Total users: {analysis['total_users']}")
    print(f"Bash users: {len(analysis['bash_users'])}")
    print(f"Regular users (UID >= 1000): {len(analysis['regular_users'])}")

if __name__ == "__main__":
    main()
```

---

## Exercise 4: API Client

```python
#!/usr/bin/env python3
"""GitHub API Client."""

import requests
from typing import Dict, List, Optional

class GitHubClient:
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.session = requests.Session()
        if token:
            self.session.headers["Authorization"] = f"token {token}"
        self.session.headers["Accept"] = "application/vnd.github.v3+json"
    
    def get_user(self, username: str) -> Dict:
        """Get user information."""
        url = f"{self.BASE_URL}/users/{username}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_repos(self, username: str) -> List[Dict]:
        """Get user's public repositories."""
        url = f"{self.BASE_URL}/users/{username}/repos"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_repo_languages(self, owner: str, repo: str) -> Dict:
        """Get languages used in a repository."""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/languages"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

# Usage
if __name__ == "__main__":
    client = GitHubClient()
    
    # Get user
    user = client.get_user("torvalds")
    print(f"User: {user['name']}")
    print(f"Followers: {user['followers']}")
    
    # Get repos
    repos = client.get_repos("torvalds")
    print(f"\nPublic repos: {len(repos)}")
    
    # Get languages for first repo
    if repos:
        repo = repos[0]
        languages = client.get_repo_languages("torvalds", repo["name"])
        print(f"\nLanguages in {repo['name']}: {languages}")
```

---

## Exercise 5: Config Parser

```python
#!/usr/bin/env python3
"""Configuration Manager with priority."""

import os
import yaml
import argparse
from typing import Dict, Any

def deep_merge(base: Dict, override: Dict) -> Dict:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def load_config(config_file: str, cli_args: argparse.Namespace) -> Dict[str, Any]:
    """Load config with priority: defaults < file < env < cli."""
    
    # 1. Default values (lowest priority)
    config = {
        "server": {
            "host": "localhost",
            "port": 8080
        },
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "logging": {
            "level": "INFO"
        }
    }
    
    # 2. Load from file
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            file_config = yaml.safe_load(f)
            config = deep_merge(config, file_config)
    
    # 3. Environment variables
    env_mappings = {
        "SERVER_HOST": ("server", "host"),
        "SERVER_PORT": ("server", "port"),
        "DB_HOST": ("database", "host"),
        "DB_PORT": ("database", "port"),
        "LOG_LEVEL": ("logging", "level")
    }
    
    for env_var, (section, key) in env_mappings.items():
        value = os.getenv(env_var)
        if value:
            if key == "port":
                value = int(value)
            config[section][key] = value
    
    # 4. CLI arguments (highest priority)
    if hasattr(cli_args, "port") and cli_args.port:
        config["server"]["port"] = cli_args.port
    if hasattr(cli_args, "debug") and cli_args.debug:
        config["logging"]["level"] = "DEBUG"
    
    return config

# Usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default="config.yaml")
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    
    config = load_config(args.config, args)
    print(yaml.dump(config, default_flow_style=False))
```

---

## Exercise 7: Server Monitor

```python
#!/usr/bin/env python3
"""Server Monitor with multiple checks."""

import subprocess
import socket
import requests
from dataclasses import dataclass
from typing import List, Dict, Optional
import time

@dataclass
class CheckResult:
    server: str
    check_type: str
    success: bool
    message: str
    response_time: Optional[float] = None

class ServerMonitor:
    def __init__(self, servers: List[Dict]):
        """
        servers: list of dicts with keys:
        - host: hostname or IP
        - ports: list of ports to check (optional)
        - http_endpoints: list of URLs (optional)
        """
        self.servers = servers
    
    def check_ping(self, host: str) -> bool:
        """Check if host responds to ping."""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "2", host],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def check_port(self, host: str, port: int, timeout: int = 5) -> bool:
        """Check if port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_http(self, url: str, timeout: int = 10) -> Dict:
        """Check HTTP endpoint."""
        try:
            start = time.time()
            response = requests.get(url, timeout=timeout)
            elapsed = (time.time() - start) * 1000
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "response_time_ms": round(elapsed, 2)
            }
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_all_checks(self) -> List[CheckResult]:
        """Run all checks on all servers."""
        results = []
        
        for server in self.servers:
            host = server["host"]
            
            # Ping check
            ping_ok = self.check_ping(host)
            results.append(CheckResult(
                server=host,
                check_type="ping",
                success=ping_ok,
                message="OK" if ping_ok else "Failed"
            ))
            
            # Port checks
            for port in server.get("ports", []):
                port_ok = self.check_port(host, port)
                results.append(CheckResult(
                    server=host,
                    check_type=f"port:{port}",
                    success=port_ok,
                    message="Open" if port_ok else "Closed"
                ))
            
            # HTTP checks
            for url in server.get("http_endpoints", []):
                http_result = self.check_http(url)
                results.append(CheckResult(
                    server=host,
                    check_type=f"http:{url}",
                    success=http_result.get("success", False),
                    message=str(http_result.get("status_code", http_result.get("error"))),
                    response_time=http_result.get("response_time_ms")
                ))
        
        return results
    
    def generate_report(self) -> str:
        """Generate markdown report."""
        results = self.run_all_checks()
        
        lines = [
            "# Server Monitor Report",
            f"\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Results\n",
            "| Server | Check | Status | Details |",
            "|--------|-------|--------|---------|"
        ]
        
        for r in results:
            status = "✅" if r.success else "❌"
            details = r.message
            if r.response_time:
                details += f" ({r.response_time}ms)"
            lines.append(f"| {r.server} | {r.check_type} | {status} | {details} |")
        
        return "\n".join(lines)

# Usage
if __name__ == "__main__":
    servers = [
        {
            "host": "google.com",
            "ports": [80, 443],
            "http_endpoints": ["https://www.google.com"]
        },
        {
            "host": "github.com",
            "ports": [443],
            "http_endpoints": ["https://github.com"]
        }
    ]
    
    monitor = ServerMonitor(servers)
    report = monitor.generate_report()
    print(report)
```

---

## Exercise 8: Password Generator

```python
#!/usr/bin/env python3
"""Secure Password Generator."""

import argparse
import secrets
import string

def generate_password(
    length: int = 16,
    uppercase: bool = True,
    lowercase: bool = True,
    digits: bool = True,
    special: bool = True
) -> str:
    """Generate a secure random password."""
    
    charset = ""
    required = []
    
    if uppercase:
        charset += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if lowercase:
        charset += string.ascii_lowercase
        required.append(secrets.choice(string.ascii_lowercase))
    if digits:
        charset += string.digits
        required.append(secrets.choice(string.digits))
    if special:
        charset += "!@#$%^&*"
        required.append(secrets.choice("!@#$%^&*"))
    
    if not charset:
        raise ValueError("At least one character type must be selected")
    
    # Fill remaining length
    remaining = length - len(required)
    password_chars = required + [secrets.choice(charset) for _ in range(remaining)]
    
    # Shuffle
    secrets.SystemRandom().shuffle(password_chars)
    
    return "".join(password_chars)

def main():
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    parser.add_argument("-l", "--length", type=int, default=16)
    parser.add_argument("--no-uppercase", action="store_true")
    parser.add_argument("--no-lowercase", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-special", action="store_true")
    parser.add_argument("-n", "--count", type=int, default=1)
    args = parser.parse_args()
    
    for _ in range(args.count):
        password = generate_password(
            length=args.length,
            uppercase=not args.no_uppercase,
            lowercase=not args.no_lowercase,
            digits=not args.no_digits,
            special=not args.no_special
        )
        print(password)

if __name__ == "__main__":
    main()
```

---

## Notes

- The above solutions are **one of many ways** to solve (Solutions trên là **một trong nhiều cách** để giải quyết)
- Always possible to optimize or write differently (Luôn có thể optimize hoặc viết khác đi)
- Important to understand logic and error handling (Quan trọng là hiểu logic và error handling)

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
