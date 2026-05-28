# Solutions: Module 10 - FINAL PROJECT

> **Reference Implementation**

---

## COMPLETE DOCKERFILE

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

---

## NGINX CONFIGURATION

```nginx
upstream backend {
    server web:5000;
}

server {
    listen 80;
    server_name tasks.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tasks.example.com;
    
    ssl_certificate /etc/letsencrypt/live/tasks.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tasks.example.com/privkey.pem;
    
    location /static {
        alias /var/www/static;
        expires 1y;
    }
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## DEPLOYMENT SCRIPT

```bash
#!/bin/bash
set -e

echo "🚀 Deploying Task Manager..."

git pull origin main
docker-compose build
docker-compose down
docker-compose up -d

sleep 10

if curl -f http://localhost/health; then
    echo "✅ Deployment successful!"
else
    echo "❌ Health check failed!"
    docker-compose logs
    exit 1
fi
```

---

## ENVIRONMENT SETUP

```bash
# .env.production
SECRET_KEY=your-super-secret-key
DB_PASS=secure-database-password
```

---

## KEY IMPLEMENTATION NOTES

1. **Database:** PostgreSQL với volume persistence
2. **Backend:** Flask + Gunicorn
3. **Frontend:** Simple HTML/CSS/JS
4. **Docker:** Multi-stage optional
5. **CI/CD:** Test → Build → Deploy
6. **NGINX:** Reverse proxy + SSL
7. **Monitoring:** /health endpoint
8. **Deploy:** Zero-downtime với health checks

---

## TESTING CHECKLIST

- [ ] App runs locally
- [ ] Docker build succeeds
- [ ] Compose starts all services
- [ ] Health check returns 200
- [ ] CI/CD pipeline passes
- [ ] Production accessible
- [ ] SSL working

---

**Project hoàn thành = Junior DevOps Engineer! 🎓**
