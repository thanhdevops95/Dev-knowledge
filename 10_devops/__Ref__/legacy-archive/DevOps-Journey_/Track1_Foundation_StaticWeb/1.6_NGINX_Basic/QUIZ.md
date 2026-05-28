# ❓ Quiz: NGINX Basic

> **Knowledge Check for NGINX (15 Questions)**
>
> *Kiểm tra kiến thức NGINX (15 câu hỏi).*

---

### Q1

What is NGINX mainly used for?

*(NGINX chủ yếu được sử dụng cho?)*

- a) Database
- b) Web server & reverse proxy *(Máy chủ web & reverse proxy)*
- c) Container runtime
- d) Version control  

---

### Q2

What is the main config file of NGINX?

*(File config chính của NGINX?)*

- a) /etc/nginx/nginx.config
- b) /etc/nginx/nginx.conf
- c) /nginx/config.conf
- d) /etc/nginx.conf  

---

### Q3

Which command tests NGINX config?

*(Lệnh test config NGINX?)*

- a) `nginx -c`
- b) `nginx -t`
- c) `nginx --test`
- d) `nginx -check`  

---

### Q4

What does the directive `listen 80` mean?

*(Directive `listen 80` có nghĩa gì?)*

- a) Listen on port 80 *(Lắng nghe trên cổng 80)*
- b) Forward to port 80 *(Chuyển tiếp đến cổng 80)*
- c) Block port 80 *(Chặn cổng 80)*
- d) Log port 80 *(Ghi log cổng 80)*  

---

### Q5

What is `proxy_pass` used for?

*(`proxy_pass` dùng để?)*

- a) Pass files *(Truyền file)*
- b) Forward requests to backend *(Chuyển tiếp request đến backend)*
- c) Pass variables *(Truyền biến)*
- d) Pass headers *(Truyền header)*  

---

### Q6

How to reload NGINX without downtime?

*(Reload NGINX không downtime?)*

- a) `nginx -s restart`
- b) `nginx -s reload`
- c) `systemctl restart nginx`
- d) `nginx reload`  

---

### Q7

What is the `upstream` block used for?

*(`upstream` block dùng để?)*

- a) Define log format *(Định nghĩa định dạng log)*
- b) Define backend servers *(Định nghĩa server backend)*
- c) Define SSL
- d) Define locations  

---

### Q8

What does the `try_files` directive do?

*(`try_files` directive làm gì?)*

- a) Try different servers *(Thử các server khác nhau)*
- b) Check files exist in order *(Kiểm tra file tồn tại theo thứ tự)*
- c) Try connections *(Thử kết nối)*
- d) Retry requests *(Thử lại request)*  

---

### Q9

When to use 301 redirect?

*(Return 301 redirect dùng khi?)*

- a) Temporary redirect *(Chuyển hướng tạm thời)*
- b) Permanent redirect *(Chuyển hướng vĩnh viễn)*
- c) Error redirect *(Chuyển hướng lỗi)*
- d) Internal redirect *(Chuyển hướng nội bộ)*  

---

### Q10

How to enable gzip compression?

*(Gzip compression enable bằng?)*

- a) `compression on`
- b) `gzip on`
- c) `enable gzip`
- d) `compress true`  

---

### Q11

What does location block `location ~` mean?

*(Location block `location ~` có nghĩa gì?)*

- a) Exact match *(Khớp chính xác)*
- b) Prefix match *(Khớp tiền tố)*
- c) Regex match *(Khớp biểu thức chính quy)*
- d) Default match *(Khớp mặc định)*  

---

### Q12

How is the SSL certificate declared?

*(SSL certificate được khai báo bằng?)*

- a) `ssl_cert`
- b) `ssl_certificate`
- c) `certificate`
- d) `https_cert`  

---

### Q13

What is the default root directory of NGINX?

*(Default root directory của NGINX?)*

- a) /var/www/html
- b) /usr/share/nginx/html
- c) /etc/nginx/html
- d) /www  

---

### Q14

What does `worker_processes auto` mean?

*(`worker_processes auto` có nghĩa gì?)*

- a) 1 worker
- b) Max workers
- c) Match CPU cores *(Khớp số nhân CPU)*
- d) No workers  

---

### Q15

What is the default access log format?

*(Access log format default là?)*

- a) combined
- b) common
- c) json
- d) simple  

---

## 📝 Answers

<details>
<summary>Click to view / Nhấn để xem đáp án</summary>

| Q | A | Q | A |
|---|---|---|---|
| 1 | b | 9 | b |
| 2 | b | 10 | b |
| 3 | b | 11 | c |
| 4 | a | 12 | b |
| 5 | b | 13 | b |
| 6 | b | 14 | c |
| 7 | b | 15 | a |
| 8 | b |   |   |

</details>

---

**[← Back to README](./README.md)**
