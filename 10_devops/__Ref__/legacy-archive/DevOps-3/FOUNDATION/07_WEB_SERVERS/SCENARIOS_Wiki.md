# Scenarios: Module 07 - WEB SERVERS

> **5 Tình huống NGINX thực tế**

---

## Scenario 1: "502 Bad Gateway"

**Vấn đề:** NGINX shows 502

**Debug:**

```bash
sudo systemctl status backend-app
curl http://localhost:5000
```

**Solution:** Backend không running → Start backend service

---

## Scenario 2: "SSL Certificate Errors"

**Vấn đề:** HTTPS không work

**Debug:**

```bash
openssl s_client -connect example.com:443
```

**Solution:** Certificate expired → `sudo certbot renew`

---

## Scenario 3: "Config Syntax Error"

**Vấn đề:** NGINX không start

**Debug:**

```bash
sudo nginx -t
```

**Solution:** Fix typo trong config file

---

## Scenario 4: "Port Already Used"

**Vấn đề:** Không start được NGINX

**Debug:**

```bash
sudo lsof -i :80
```

**Solution:** Stop Apache hoặc service khác

---

## Scenario 5: "Load Balancer Không Phân Phối"

**Vấn đề:** Traffic chỉ đến 1 server

**Debug:**

```bash
cat /etc/nginx/nginx.conf | grep upstream
```

**Solution:** Fix upstream block syntax

---

**Chi tiết trong SOLUTIONS.md**
