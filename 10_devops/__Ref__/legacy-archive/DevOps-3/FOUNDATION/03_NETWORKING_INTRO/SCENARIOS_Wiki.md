# Scenarios: Module 03 - NETWORKING INTRO

> **5 Tình huống Networking thực tế**

---

## Scenario 1: "Website Không Connect Được Database"

**Tình huống:** Web app không connect được DB

**Debug:**

```bash
# Check DB port listening
netstat -tulpn | grep 5432

# Check firewall
sudo ufw status

# Test connectivity
telnet db-server 5432
```

**Solution:** UFW blocking port 5432 → `sudo ufw allow 5432`

---

## Scenario 2: "DNS Không Resolve"

**Tình huống:** Domain không resolve

**Debug:**

```bash
nslookup domain.com
dig domain.com
cat /etc/resolv.conf
```

**Solution:** DNS server misconfigured → sửa /etc/resolv.conf

---

## Scenario 3: "Firewall Block Tất Cả"

**Tình huống:** Không SSH được sau enable UFW

**Debug:** Đã enable UFW mà không allow port 22

**Solution:** Phải access qua console và `sudo ufw allow 22`

**Prevention:** LUÔN allow SSH trước khi enable UFW!

---

## Scenario 4: "API Response Chậm"

**Tình huống:** API mất 5+ giây

**Debug:**

```bash
curl -w "Time: %{time_total}\n" https://api.example.com
traceroute api.example.com
ping api.example.com
```

**Solution:** Network latency → sử dụng CDN

---

## Scenario 5: "SSL Certificate Expired"

**Tình huống:** HTTPS warning

**Debug:**

```bash
openssl s_client -connect example.com:443
echo | openssl s_client -connect example.com:443 | openssl x509 -noout -dates
```

**Solution:** Renew với `sudo certbot renew`

---

**Xem SOLUTIONS.md cho chi tiết!**
