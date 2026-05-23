# 🎯 Project: Network Basics

> Mini project: **Network Health Dashboard**

---

## 📋 Project Overview

### Project Name: **Network Health Dashboard**

Xây dựng tool monitoring network health cho DevOps.

### Duration: 2-3 ngày

---

## 🎯 Requirements

### Core Features

#### 1. Host Checker

- Ping multiple hosts
- Measure latency
- Track uptime

#### 2. Port Monitor

- Check open ports
- Service detection
- Alert on port changes

#### 3. SSL Monitor

- Certificate expiration
- Certificate validation
- Alert before expiry

#### 4. DNS Checker

- Resolution time
- Record verification
- Compare across DNS servers

---

## 📁 Project Structure

```
network-dashboard/
├── src/
│   ├── ping_checker.py
│   ├── port_monitor.py
│   ├── ssl_checker.py
│   └── dns_checker.py
├── config/
│   ├── hosts.yaml
│   └── alerts.yaml
├── reports/
├── main.py
├── requirements.txt
└── README.md
```

---

## 📊 Expected Output

```
===========================================
NETWORK HEALTH REPORT - 2024-01-15 10:30:00
===========================================

HOSTS STATUS:
Host             Status    Latency    Uptime
---------------------------------------------
web-server       ✅ UP     12ms       99.9%
db-server        ✅ UP     5ms        100%
api-gateway      ❌ DOWN   -          95.2%

PORTS STATUS:
Host             Port    Service    Status
---------------------------------------------
web-server       80      HTTP       ✅ Open
web-server       443     HTTPS      ✅ Open
db-server        3306    MySQL      ✅ Open

SSL CERTIFICATES:
Domain                  Expires      Days Left
---------------------------------------------
example.com             2024-06-15   152 ⚠️
api.example.com         2024-12-31   350 ✅

ALERTS:
- ❌ api-gateway is DOWN
- ⚠️ example.com SSL expires in 152 days

===========================================
```

---

## ✅ Acceptance Criteria

- [ ] Ping check for multiple hosts
- [ ] Port check with service detection
- [ ] SSL certificate check
- [ ] Configuration via YAML
- [ ] Text report generation
- [ ] Basic alerting

---

**Good luck! 🚀**
