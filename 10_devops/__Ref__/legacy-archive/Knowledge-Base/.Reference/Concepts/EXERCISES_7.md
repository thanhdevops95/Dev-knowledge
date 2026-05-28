# Exercises: Module 07 - WEB SERVERS

> **Bài tập NGINX cho Production**

**Tổng điểm:** 100 | **Thời gian:** 45 phút | **Đạt:** 70/100

---

## PHẦN A: TRẮC NGHIỆM (30 điểm)

**Câu 1:** NGINX là gì?

- A) Web server và reverse proxy ✓
- B) Database server
- C) DNS server
- D) Mail server

**Câu 2:** Port mặc định HTTP?

- A) 22
- B) 443
- C) 80 ✓
- D) 8080

**Câu 3:** Kiểm tra config syntax?

- A) nginx -c
- B) nginx -t ✓
- C) nginx -v
- D) nginx -s

**Câu 4:** Reload không downtime?

- A) systemctl reload nginx ✓
- B) systemctl restart nginx
- C) nginx -s stop
- D) nginx -k stop

**Câu 5:** Directive cho reverse proxy?

- A) forward_pass
- B) reverse_pass
- C) proxy_pass ✓
- D) upstream_pass

**Câu 6:** Load balancing block?

- A) backend {}
- B) upstream {} ✓
- C) balance {}
- D) servers {}

**Câu 7:** SSL certificate tool miễn phí?

- A) certbot ✓
- B) openssl only
- C) ssl-gen
- D) letsencrypt-cli

**Câu 8:** Enable gzip compression?

- A) compress on
- B) gzip true
- C) gzip on ✓
- D) enable_gzip

**Câu 9:** Rate limiting zone?

- A) rate_limit_zone
- B) limit_req ✓
- C) throttle_zone
- D) request_limit

**Câu 10:** Add security header?

- A) add_header ✓
- B) set_header
- C) header_add
- D) response_header

---

## PHẦN B: THỰC HÀNH (70 điểm)

**Câu 11:** Install và verify NGINX (5 điểm)

```bash
sudo apt install nginx
sudo systemctl start nginx
curl http://localhost
```

**Câu 12:** Configure virtual host (10 điểm)

**Câu 13:** Setup reverse proxy cho Flask app (15 điểm)

**Câu 14:** Load balance 3 backend servers (10 điểm)

**Câu 15:** SSL với Let's Encrypt (10 điểm)

**Câu 16:** Add security headers (5 điểm)

**Câu 17:** Enable gzip compression (5 điểm)

**Câu 18:** Troubleshoot 502 Bad Gateway (10 điểm)

---

## 📊 THANG ĐIỂM

- **90-100:** NGINX Expert ⭐⭐⭐
- **80-89:** Proficient ⭐⭐
- **70-79:** Competent ⭐
- **<70:** Cần review

**Xem SOLUTIONS.md cho đáp án!**
