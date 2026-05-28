# 💪 Exercises: Network Basics

> **Self-practice exercises for Networking.**
>
> *Bài tập tự luyện về Networking.*

---

## Exercise 1: Subnet Calculation ⭐

Given network `192.168.10.0/26`, calculate:

*(Cho network `192.168.10.0/26`, tính:)*

1. Subnet mask
2. Number of usable hosts *(Số hosts khả dụng)*
3. Network address
4. Broadcast address
5. Usable IP range

---

## Exercise 2: DNS Investigation ⭐

1. Find all DNS records of `google.com` *(Tìm tất cả DNS records của `google.com`)*
2. Find mail servers (MX records) of `microsoft.com` *(Tìm mail servers của `microsoft.com`)*
3. Trace DNS resolution path of `github.com` *(Trace DNS resolution path của `github.com`)*
4. Find authoritative name servers *(Tìm authoritative name servers)*

---

## Exercise 3: Network Diagnostics ⭐⭐

Write a script to diagnose connectivity issues:

*(Viết script diagnose connectivity issues:)*

```bash
#!/bin/bash
# diagnose.sh
# Input: hostname or IP
# Output: Diagnostic report
```

Checks:

- Local interface status
- Gateway reachability
- DNS resolution
- Target reachability
- Port connectivity (80, 443)

---

## Exercise 4: Port Scanner ⭐⭐

Write a script to scan ports:

*(Viết script scan ports:)*

```python
#!/usr/bin/env python3
# port_scanner.py

def scan_ports(host, ports):
    """
    Scan specified ports on host.
    Return list of open ports.
    """
    pass
```

---

## Exercise 5: HTTP Client ⭐⭐

Using cURL or Python requests:

*(Sử dụng cURL hoặc Python requests:)*

1. GET request with custom headers *(GET request với custom headers)*
2. POST request with JSON body *(POST request với JSON body)*
3. Follow redirects and log each hop *(Follow redirects và log each hop)*
4. Download file with progress *(Download file với progress)*
5. Test API with authentication *(Test API với authentication)*

---

## Exercise 6: Firewall Rules ⭐⭐

Design firewall rules for a web server:

*(Thiết kế firewall rules cho web server:)*

Requirements:

- Allow SSH from management network (10.0.0.0/8) *(Allow SSH từ management network)*
- Allow HTTP/HTTPS from anywhere *(Allow HTTP/HTTPS từ anywhere)*
- Allow MySQL from app servers (192.168.1.0/24) *(Allow MySQL từ app servers)*
- Block everything else *(Block mọi thứ khác)*
- Log dropped packets *(Log các packets bị chặn)*

---

## Exercise 7: Network Monitoring ⭐⭐⭐

Write a script to monitor network:

*(Viết script monitor network:)*

```python
#!/usr/bin/env python3
# network_monitor.py

class NetworkMonitor:
    def check_hosts(self, hosts: list) -> dict:
        """Ping multiple hosts concurrently."""
        pass
    
    def check_ports(self, host: str, ports: list) -> dict:
        """Check multiple ports."""
        pass
    
    def measure_latency(self, host: str, count: int) -> dict:
        """Measure average latency."""
        pass
```

---

## Exercise 8: SSL Certificate Checker ⭐⭐⭐

Write a tool to check SSL certificates:

*(Viết tool check SSL certificates:)*

```python
#!/usr/bin/env python3
# ssl_checker.py

def check_certificate(hostname: str) -> dict:
    """
    Return:
    - Issuer
    - Subject
    - Valid from/to
    - Days until expiration
    - Is expired
    """
    pass
```

---

## 📝 Checklist

- [ ] Exercise 1: Subnet Calculation
- [ ] Exercise 2: DNS Investigation
- [ ] Exercise 3: Network Diagnostics
- [ ] Exercise 4: Port Scanner
- [ ] Exercise 5: HTTP Client
- [ ] Exercise 6: Firewall Rules
- [ ] Exercise 7: Network Monitoring
- [ ] Exercise 8: SSL Checker

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
