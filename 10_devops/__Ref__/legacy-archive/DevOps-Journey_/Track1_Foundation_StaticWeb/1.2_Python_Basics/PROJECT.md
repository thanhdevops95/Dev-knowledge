# 🎯 Project: Python Basics

> Mini project: **DevOps Automation Toolkit**

---

## 📋 Project Overview (Tổng quan dự án)

### Project Name: **DevOps Automation Toolkit**

Xây dựng bộ tools Python cho DevOps tasks hàng ngày.

### Objectives (Mục tiêu)

- Apply Python to real-world DevOps tasks (Áp dụng Python cho real-world DevOps tasks)
- Build reusable modules (Xây dựng reusable modules)
- Practice CLI development (Thực hành phát triển CLI)
- Error handling and logging (Xử lý lỗi và logging)

### Duration: 3-4 ngày

---

## 🎯 Requirements (Yêu cầu)

### Core Modules

#### 1. System Monitor (`monitor.py`)

```python
"""
Features:
- CPU, Memory, Disk usage
- Process monitoring
- Network connections
- Alert when thresholds exceeded
"""
```

#### 2. Log Analyzer (`log_analyzer.py`)

```python
"""
Features:
- Parse various log formats
- Aggregate by level/time
- Pattern matching
- Generate reports (JSON, HTML)
"""
```

#### 3. Configuration Manager (`config_manager.py`)

```python
"""
Features:
- Load from YAML/JSON/ENV
- Validate configurations
- Merge with priority
- Template rendering
"""
```

#### 4. HTTP Health Checker (`health_checker.py`)

```python
"""
Features:
- Check multiple endpoints
- Measure response times
- Parallel checking
- Alerting
"""
```

#### 5. CLI Interface (`cli.py`)

```python
"""
Main entry point combining all tools.

Usage:
  devops-toolkit monitor [--watch]
  devops-toolkit logs analyze <path>
  devops-toolkit health check <endpoints-file>
  devops-toolkit config validate <config-file>
"""
```

---

## 📁 Project Structure (Cấu trúc dự án)

```
devops-toolkit/
├── devops_toolkit/
│   ├── __init__.py
│   ├── cli.py
│   ├── monitor.py
│   ├── log_analyzer.py
│   ├── config_manager.py
│   ├── health_checker.py
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py
│       └── validators.py
├── tests/
│   ├── test_monitor.py
│   ├── test_log_analyzer.py
│   └── test_config_manager.py
├── examples/
│   ├── config.yaml
│   ├── endpoints.yaml
│   └── sample.log
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
```

---

## 📝 Detailed Specifications (Thông số kỹ thuật chi tiết)

### monitor.py

```python
#!/usr/bin/env python3
"""System Monitoring Module."""

from dataclasses import dataclass
from typing import List, Dict
import psutil  # pip install psutil

@dataclass
class SystemMetrics:
    cpu_percent: float
    memory_percent: float
    disk_usage: Dict[str, float]
    top_processes: List[Dict]
    network_connections: int

class SystemMonitor:
    def __init__(self, thresholds: Dict = None):
        self.thresholds = thresholds or {
            "cpu": 80,
            "memory": 90,
            "disk": 85
        }
    
    def get_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        pass
    
    def check_thresholds(self, metrics: SystemMetrics) -> List[str]:
        """Check if any thresholds exceeded. Return list of alerts."""
        pass
    
    def watch(self, interval: int = 5):
        """Continuously monitor and print metrics."""
        pass
    
    def export_metrics(self, format: str = "json") -> str:
        """Export metrics to JSON or Prometheus format."""
        pass
```

### log_analyzer.py

```python
#!/usr/bin/env python3
"""Log Analysis Module."""

import re
from dataclasses import dataclass
from typing import List, Dict, Iterator
from collections import Counter
from datetime import datetime

@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    source: str = ""

class LogAnalyzer:
    # Common log patterns
    PATTERNS = {
        "syslog": r"(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\w+)\s+(.+)",
        "nginx": r'(\d+\.\d+\.\d+\.\d+).*\[(.+)\]\s+"(\w+)\s+(.+)"',
        "apache": r'(\d+\.\d+\.\d+\.\d+).*\[(.+)\]\s+"(\w+)\s+(.+)"',
        "json": None,  # Parse as JSON
    }
    
    def __init__(self, log_format: str = "auto"):
        self.format = log_format
    
    def parse_file(self, filepath: str) -> Iterator[LogEntry]:
        """Parse log file and yield entries."""
        pass
    
    def analyze(self, entries: List[LogEntry]) -> Dict:
        """Analyze entries and return statistics."""
        pass
    
    def find_patterns(self, entries: List[LogEntry], pattern: str) -> List[LogEntry]:
        """Find entries matching regex pattern."""
        pass
    
    def generate_report(self, analysis: Dict, format: str = "text") -> str:
        """Generate report in text, JSON, or HTML format."""
        pass
```

### health_checker.py

```python
#!/usr/bin/env python3
"""HTTP Health Checking Module."""

import requests
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Optional
import time

@dataclass 
class HealthCheckResult:
    url: str
    status: str  # "UP", "DOWN", "TIMEOUT", "ERROR"
    status_code: Optional[int]
    response_time_ms: Optional[float]
    error_message: Optional[str] = None

class HealthChecker:
    def __init__(self, timeout: int = 5, max_workers: int = 10):
        self.timeout = timeout
        self.max_workers = max_workers
    
    def check_endpoint(self, url: str, expected_status: int = 200) -> HealthCheckResult:
        """Check single endpoint."""
        pass
    
    def check_all(self, endpoints: List[Dict]) -> List[HealthCheckResult]:
        """Check multiple endpoints in parallel."""
        pass
    
    def load_endpoints(self, filepath: str) -> List[Dict]:
        """Load endpoints from YAML/JSON file."""
        pass
    
    def generate_report(self, results: List[HealthCheckResult]) -> str:
        """Generate status report."""
        pass
```

---

## ✅ Acceptance Criteria (Tiêu chí chấp nhận)

### Must Have

- [ ] All 4 core modules implemented
- [ ] CLI interface working
- [ ] Proper error handling
- [ ] Logging implemented
- [ ] README with usage examples

### Should Have

- [ ] Unit tests (coverage > 70%)
- [ ] Type hints throughout
- [ ] Configuration file support
- [ ] Multiple output formats

### Nice to Have

- [ ] Docker containerization
- [ ] Prometheus metrics export
- [ ] Slack/Email alerting
- [ ] Web dashboard

---

## 🚀 Getting Started (Bắt đầu)

### Step 1: Setup

```bash
mkdir devops-toolkit
cd devops-toolkit
python -m venv venv
source venv/bin/activate
pip install requests pyyaml psutil
```

### Step 2: Create Package Structure

```bash
mkdir -p devops_toolkit/utils tests examples
touch devops_toolkit/__init__.py
touch devops_toolkit/utils/__init__.py
```

### Step 3: Start with Monitor

```python
# devops_toolkit/monitor.py
#!/usr/bin/env python3
"""System Monitor - Start here."""

def main():
    print("System Monitor starting...")
    # Your implementation

if __name__ == "__main__":
    main()
```

---

## 📊 Evaluation (Đánh giá)

| Criteria (Tiêu chí) | Points (Điểm) |
|----------|--------|
| Functionality | 40 |
| Code Quality | 20 |
| Error Handling | 15 |
| Documentation | 15 |
| Testing | 10 |
| **Total** | **100** |

---

**Good luck! 🚀**
