# ✅ Solutions: Network Basics

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Subnet Calculation

**Network: `192.168.10.0/26`**

```
1. Subnet mask: 255.255.255.192

2. Host bits: 32 - 26 = 6 bits
   Total addresses: 2^6 = 64
   Usable hosts: 64 - 2 = 62

3. Network address: 192.168.10.0

4. Broadcast address: 192.168.10.63

5. Usable range: 192.168.10.1 - 192.168.10.62
```

---

## Exercise 3: Network Diagnostics Script

```bash
#!/bin/bash
# diagnose.sh

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <hostname_or_ip>"
    exit 1
fi

echo "=========================================="
echo "Network Diagnostic Report for: $TARGET"
echo "=========================================="
echo ""

# 1. Check local interface
echo "[1] Local Interface Status:"
ip addr show | grep -E "^[0-9]+:|inet " | head -10
echo ""

# 2. Check gateway
GATEWAY=$(ip route | grep default | awk '{print $3}')
echo "[2] Gateway Connectivity:"
ping -c 2 $GATEWAY >/dev/null 2>&1 && echo "✓ Gateway $GATEWAY reachable" || echo "✗ Gateway unreachable"
echo ""

# 3. DNS resolution
echo "[3] DNS Resolution:"
if nslookup $TARGET >/dev/null 2>&1; then
    echo "✓ DNS resolution successful"
    nslookup $TARGET | grep -A1 "Name:"
else
    echo "✗ DNS resolution failed"
fi
echo ""

# 4. Target reachability
echo "[4] Target Reachability:"
ping -c 3 $TARGET 2>/dev/null
echo ""

# 5. Port connectivity
echo "[5] Port Connectivity:"
for port in 80 443; do
    nc -zv -w2 $TARGET $port 2>&1 | grep -q "succeeded" && \
        echo "✓ Port $port open" || echo "✗ Port $port closed"
done
echo ""

echo "=========================================="
echo "Diagnostic completed"
```

---

## Exercise 4: Port Scanner

```python
#!/usr/bin/env python3
"""Simple port scanner."""

import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(host: str, port: int, timeout: float = 1.0) -> bool:
    """Check if port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(host: str, ports: list, workers: int = 50) -> list:
    """Scan multiple ports concurrently."""
    open_ports = []
    
    def check(port):
        if scan_port(host, port):
            return port
        return None
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = executor.map(check, ports)
        open_ports = [p for p in results if p is not None]
    
    return open_ports

if __name__ == "__main__":
    import sys
    
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    ports = range(1, 1025)
    
    print(f"Scanning {host}...")
    open_ports = scan_ports(host, ports)
    
    print(f"\nOpen ports: {len(open_ports)}")
    for port in open_ports:
        print(f"  {port}/tcp open")
```

---

## Exercise 6: Firewall Rules

```bash
# Firewall rules for web server

# Reset rules
sudo ufw reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH from management network
sudo ufw allow from 10.0.0.0/8 to any port 22

# Allow HTTP/HTTPS from anywhere
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow MySQL from app servers
sudo ufw allow from 192.168.1.0/24 to any port 3306

# Enable logging
sudo ufw logging on

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status verbose
```

---

## Exercise 8: SSL Certificate Checker

```python
#!/usr/bin/env python3
"""SSL Certificate Checker."""

import ssl
import socket
from datetime import datetime

def check_certificate(hostname: str, port: int = 443) -> dict:
    """Check SSL certificate for a hostname."""
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parse dates
                not_before = datetime.strptime(
                    cert['notBefore'], 
                    '%b %d %H:%M:%S %Y %Z'
                )
                not_after = datetime.strptime(
                    cert['notAfter'], 
                    '%b %d %H:%M:%S %Y %Z'
                )
                
                days_left = (not_after - datetime.now()).days
                
                return {
                    "hostname": hostname,
                    "issuer": dict(x[0] for x in cert['issuer']),
                    "subject": dict(x[0] for x in cert['subject']),
                    "valid_from": not_before.isoformat(),
                    "valid_until": not_after.isoformat(),
                    "days_until_expiry": days_left,
                    "is_expired": days_left < 0,
                    "is_warning": 0 < days_left < 30
                }
    except Exception as e:
        return {
            "hostname": hostname,
            "error": str(e)
        }

if __name__ == "__main__":
    hosts = ["google.com", "github.com", "python.org"]
    
    for host in hosts:
        result = check_certificate(host)
        print(f"\n{host}:")
        if "error" in result:
            print(f"  Error: {result['error']}")
        else:
            print(f"  Issuer: {result['issuer'].get('organizationName')}")
            print(f"  Valid until: {result['valid_until']}")
            print(f"  Days left: {result['days_until_expiry']}")
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
