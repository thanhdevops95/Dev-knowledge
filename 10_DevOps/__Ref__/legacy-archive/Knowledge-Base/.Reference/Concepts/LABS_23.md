# LABS - Module 07: WEB SERVERS BASICS

> **Objective:** Master NGINX configuration through hands-on practice
>
> **Duration:** 3-4 hours  
>
> **Prerequisites:** Module 01 (Linux), Module 04 (HTML/CSS/JS) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | NGINX Installation & Basic Config | 30 min | ⭐⭐☆☆☆ |
| Lab 2 | Serving Static Websites | 35 min | ⭐⭐☆☆☆ |
| Lab 3 | Reverse Proxy Setup | 40 min | ⭐⭐⭐☆☆ |
| Lab 4 | Load Balancing | 40 min | ⭐⭐⭐☆☆ |
| Lab 5 | SSL/TLS with Let's Encrypt | 45 min | ⭐⭐⭐⭐☆ |
| Lab 6 | Performance Optimization | 30 min | ⭐⭐⭐☆☆ |

**Total Duration:** ~3.5 hours

---

## Lab 1: NGINX Installation & Basic Config

### Objectives

- Install NGINX
- Understand configuration structure
- Start, stop, reload NGINX
- View logs

### Instructions

#### Step 1.1: Install NGINX

```bash
# Update packages
sudo apt update

# Install NGINX
sudo apt install nginx -y
```

**Expected Output:**

```
Reading package lists... Done
Setting up nginx (1.18.0-6ubuntu14) ...
```

#### Step 1.2: Start NGINX

```bash
# Start NGINX
sudo systemctl start nginx

# Enable auto-start on boot
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

**Expected Output:**

```
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
     Active: active (running) since Wed 2024-12-25 12:00:00 UTC
```

#### Step 1.3: Test NGINX

```bash
# Test from command line
curl http://localhost
```

**Expected Output:**

```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

#### Step 1.4: Configuration Files

```bash
# Main config
sudo nano /etc/nginx/nginx.conf

# Test configuration
sudo nginx -t
```

**Expected Output:**

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

#### Step 1.5: Basic Commands

```bash
# Reload (graceful restart)
sudo nginx -s reload

# Stop
sudo systemctl stop nginx

# Start
sudo systemctl start nginx

# Restart
sudo systemctl restart nginx

# View error log
sudo tail -f /var/log/nginx/error.log

# View access log
sudo tail -f /var/log/nginx/access.log
```

✅ **Lab 1 Complete!** NGINX is running!

---

## Lab 2: Serving Static Websites

### Objectives

- Create virtual hosts
- Serve static HTML sites
- Configure directory listings

### Instructions

#### Step 2.1: Create Website

```bash
# Create site directory
sudo mkdir -p /var/www/mysite

# Create index.html
sudo tee /var/www/mysite/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My Site</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Welcome to My Site!</h1>
    <p>Served by NGINX</p>
</body>
</html>
EOF

# Set permissions
sudo chown -R www-data:www-data /var/www/mysite
sudo chmod -R 755 /var/www/mysite
```

#### Step 2.2: Configure Site

```bash
# Create site config
sudo tee /etc/nginx/sites-available/mysite << 'EOF'
server {
    listen 80;
    server_name mysite.local;
    
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    access_log /var/log/nginx/mysite_access.log;
    error_log /var/log/nginx/mysite_error.log;
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload
sudo nginx -s reload
```

#### Step 2.3: Test Site

```bash
# Add to hosts file (for local testing)
echo "127.0.0.1 mysite.local" | sudo tee -a /etc/hosts

# Test
curl http://mysite.local
```

✅ **Lab 2 Complete!** Serving static sites!

---

## Lab 3: Reverse Proxy Setup

### Objectives

- Configure NGINX as reverse proxy
- Proxy to backend application
- Set proxy headers

### Instructions

#### Step 3.1: Create Backend App

```bash
# Create Node.js app
mkdir -p ~/nginx-labs/backend
cd ~/nginx-labs/backend

cat > server.js << 'EOF'
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({
    message: 'Hello from backend!',
    path: req.url,
    headers: req.headers
  }));
});

server.listen(3000, () => {
  console.log('Backend running on port 3000');
});
EOF

# Run backend
node server.js &
```

#### Step 3.2: Configure Reverse Proxy

```bash
sudo tee /etc/ngin/sites-available/proxy << 'EOF'
upstream backend {
    server localhost:3000;
}

server {
    listen 80;
    server_name proxy.local;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/proxy /etc/nginx/sites-enabled/
sudo nginx -t && sudo nginx -s reload
```

✅ **Lab 3 Complete!** Reverse proxy working!

---

## Labs 4-6 Summary

- **Lab 4:** Load Balancing (multiple backends, health checks)
- **Lab 5:** SSL/TLS (HTTPS, Let's Encrypt, certificates)
- **Lab 6:** Performance (caching, compression, optimization)

---

## 🎉 NGINX Mastery Checklist

- [x] Install and configure NGINX
- [x] Serve static websites
- [x] Setup reverse proxy
- [] Configure load balancing
- [] Enable HTTPS/SSL
- [] Optimize performance

### Next: Module 08 - DEPLOYMENT BASICS

---

> **"NGINX: Simple, Fast, Reliable!" 🚀**
