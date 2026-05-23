# Solutions: Module 08 - DEPLOYMENT

> **Đáp Án Đầy Đủ Cho Exercises, Scenarios, và Quiz**

---

## 📋 EXERCISES SOLUTIONS

### Phần A: Trắc Nghiệm

1. **B** - Blue-green deployment
2. **B** - Update từng instance một
3. **B** - Deploy cho % nhỏ users trước
4. **B** - Restart khi crash và boot
5. **B** - Trong .env files (gitignored)
6. **C** - 200
7. **B** - Forward-compatible changes
8. **A** - Previous version sẵn sàng
9. **B** - 2 environments đồng thời
10. **B** - Health checks + gradual switch

### Phần B: Scenarios

**Câu 11: Debug Failed Deployment**

```bash
# Check logs
sudo journalctl -u myapp

# Found: Missing environment variable

# Fix
echo "NEW_VAR=value" >> .env
sudo systemctl restart myapp
curl http://localhost/health
# Now 200 OK
```

**Câu 12: Blue-Green**

```nginx
upstream backend {
    server localhost:5001;  # Blue or Green
}
```

Switch bằng cách thay port, reload NGINX.

**Câu 13: Database Migration**

```sql
-- Step 1: Add column (không break old code)
ALTER TABLE users ADD COLUMN email VARCHAR(255);

-- Deploy new code

-- Step 2 (later): Make required nếu cần
```

**Câu 14: Rollback Script**

```bash
#!/bin/bash
git checkout previous-stable
./deploy.sh
curl -f http://localhost/health || exit 1
echo "Rollback complete!"
```

### Phần C: Practical

**Câu 15: Deployment Script**

```bash
#!/bin/bash
set -e

echo "Starting deployment..."

# Pull latest
git pull origin main

# Install deps
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Restart
sudo systemctl restart myapp

# Wait
sleep 5

# Health check
if curl -f http://localhost/health; then
    echo "Deployment successful!"
else
    echo "Failed! Rolling back..."
    git checkout HEAD~1
    sudo systemctl restart myapp
    exit 1
fi
```

**Câu 16: Health Endpoint**

```python
@app.route('/health')
def health():
    try:
        # Check database
        db.execute('SELECT 1')
        
        # Check Redis
        redis.ping()
        
        # Check disk
        disk = shutil.disk_usage('/')
        if disk.percent > 90:
            return jsonify({'status': 'unhealthy'}), 500
            
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500
```

**Câu 17: systemd Service**

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
EnvironmentFile=/var/www/myapp/.env
ExecStart=/var/www/myapp/venv/bin/gunicorn -w 4 app:app
Restart=always
RestartSec=10
StandardOutput=append:/var/log/myapp/app.log
StandardError=append:/var/log/myapp/error.log

[Install]
WantedBy=multi-user.target
```

**Câu 18: NGINX Config**

```nginx
upstream backend {
    server localhost:5001;  # Change to 5002 for green
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🎬 SCENARIOS SOLUTIONS

**Scenario 1:** Migrate TRƯỚC deploy code  
**Scenario 2:** Atomic all-or-nothing deployment  
**Scenario 3:** Validate .env trước deployment  
**Scenario 4:** Forward-compatible migrations ONLY  
**Scenario 5:** Canary + memory monitoring  
**Scenario 6:** Health check gates trước switch  
**Scenario 7:** Online schema change tools  
**Scenario 8:** Blue-green = perfect pattern  

---

## 📝 QUIZ SOLUTIONS

Tất cả đáp án = **B**

Key learnings:

- Blue-green cho zero-downtime
- Rolling updates cho gradual rollout
- Canary cho % nhỏ test trước
- Health checks PHẢI pass trước switch
- .env trong gitignore
- Automated scripts với rollback
- Monitor sau deployment

---

## 📊 KEY TAKEAWAYS

✅ **Deployment strategies:**

- Blue-green: Instant switch, instant rollback
- Rolling: Gradual update, one at a time
- Canary: Small % first, gradually increase

✅ **Best practices:**

- Health checks required
- Automated scripts
- Rollback always ready
- Test on staging first
- Monitor after deploy

✅ **Common mistakes:**

- Deploy without migration
- No rollback plan
- Manual processes
- Friday 5pm deploys
- Skip staging
