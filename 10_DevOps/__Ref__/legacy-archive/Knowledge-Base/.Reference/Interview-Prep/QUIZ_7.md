# Quiz: Module 07 - WEB SERVERS

> **15 Câu Trắc Nghiệm NGINX Production**

**Thời gian:** 15 phút | **Đạt:** 11/15 (73%)

---

## CÂU HỎI

**Câu 1:** NGINX chủ yếu dùng để làm gì?

- A) Web server và reverse proxy ✓
- B) Database management
- C) Email server
- D) DNS resolution

**Câu 2:** Directive nào cho reverse proxy?

- A) forward_to
- B) redirect_to
- C) proxy_pass ✓
- D) backend_url

**Câu 3:** Load balancing định nghĩa trong block nào?

- A) servers {}
- B) upstream {} ✓
- C) balance {}
- D) backend {}

**Câu 4:** SSL certificate miễn phí từ?

- A) Let's Encrypt / certbot ✓
- B) VeriSign
- C) DigiCert
- D) Comodo

**Câu 5:** Enable compression với directive nào?

- A) compress on
- B) zip enable
- C) gzip on ✓
- D) deflate true

**Câu 6:** Test config syntax?

- A) nginx -c
- B) nginx -t ✓
- C) nginx -check
- D) nginx -validate

**Câu 7:** Reload config không downtime?

- A) systemctl reload nginx ✓
- B) systemctl restart nginx
- C) nginx -s quit
- D) service nginx restart

**Câu 8:** 502 Bad Gateway nghĩa là gì?

- A) File không tìm thấy
- B) Forbidden access
- C) Backend không respond ✓
- D) Timeout

**Câu 9:** Add custom response header?

- A) set_header
- B) add_header ✓
- C) response_add
- D) header_set

**Câu 10:** Rate limiting configuration?

- A) limit_req_zone ✓
- B) rate_limit
- C) throttle_zone
- D) request_rate

**Câu 11:** Config files location?

- A) /var/nginx/
- B) /usr/nginx/
- C) /etc/nginx/ ✓
- D) /opt/nginx/

**Câu 12:** Default HTTP port?

- A) 443
- B) 80 ✓
- C) 8080
- D) 3000

**Câu 13:** Load balance algorithm ít connections nhất?

- A) least_conn ✓
- B) min_conn
- C) least_users
- D) round_robin

**Câu 14:** Pass client IP to backend?

- A) set_ip
- B) forward_ip
- C) proxy_set_header ✓
- D) client_header

**Câu 15:** Access log directive?

- A) log_access
- B) access_log ✓
- C) request_log
- D) http_log

---

## ĐÁP ÁN

1-A, 2-C, 3-B, 4-A, 5-C, 6-B, 7-A, 8-C, 9-B, 10-A
11-C, 12-B, 13-A, 14-C, 15-B

---

## THANG ĐIỂM

- **14-15:** NGINX Expert ⭐⭐⭐
- **12-13:** Proficient ⭐⭐
- **11:** Pass ⭐
- **<11:** Cần review
