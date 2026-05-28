# Solutions: Module 00 - SETUP

> **Đáp án và Troubleshooting cho Setup Exercises**

---

## EXERCISE 1: WSL2

**Expected Output:**

```
WSL version: 2.0.9.0
```

**Troubleshooting:**

```bash
# If WSL1, upgrade to WSL2
wsl --set-version Ubuntu 2

# If not installed
wsl --install
```

---

## EXERCISE 2: Shell

**Expected Output:**

```
/bin/bash
yourname
/home/yourname
```

**Troubleshooting:**

- If SHELL wrong: `chsh -s /bin/bash`
- If HOME wrong: Check /etc/passwd

---

## EXERCISE 3: Git

**Expected Output:**

```
git version 2.34.1
Your Name
your@email.com
```

**If not configured:**

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## EXERCISE 4: VS Code

**Expected Output:**

```
1.85.0
```

**Troubleshooting:**

```bash
# Install VS Code CLI
# In Windows, enable "Add to PATH" during install
# In WSL, VS Code auto-configures
```

---

## EXERCISE 5: Docker

**Expected Output:**

```
Docker version 24.0.x
Hello from Docker!
```

**Troubleshooting:**

```bash
# Start Docker Desktop (Windows/macOS)
# Or on Linux:
sudo systemctl start docker
sudo usermod -aG docker $USER
```

---

## EXERCISE 6: Directory

**Expected Output:**

```
drwxr-xr-x 2 user user 4096 Jan 25 00:00 PROJECTS
drwxr-xr-x 2 user user 4096 Jan 25 00:00 notes
```

**Troubleshooting:**

- Permission denied: Use `sudo mkdir` or check parent permissions

---

## EXERCISE 7: Network

**Expected Output:**

```
PING google.com: 3 packets transmitted, 3 received, 0% packet loss
HTTP/2 200
```

**Troubleshooting:**

- Check DNS: `cat /etc/resolv.conf`
- Check firewall: `sudo ufw status`

---

## EXERCISE 8: Verification Script

**Expected:**
All items show ✅

**Common Fixes:**

- Script not executable: `chmod +x verify-linux.sh`
- Path issues: Run from correct directory

---

## 🎯 SUMMARY

**All 8 exercises pass = Environment ready!**

**If any fail:**

1. Check the specific troubleshooting above
2. Review README.md setup steps
3. Check FAQ.md for common issues

---

**Setup complete = Start learning! 🚀**
