# LABS - Module 08: DEPLOYMENT BASICS

> **Objective:** Deploy applications to production
>
> **Duration:** 4-5 hours
>
> **Prerequisites:** All previous modules completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | Deploy Static Site to Netlify | 25 min | ⭐⭐☆☆☆ |
| Lab 2 | Deploy to GitHub Pages | 20 min | ⭐☆☆☆☆ |
| Lab 3 | VPS Setup & Deployment | 60 min | ⭐⭐⭐⭐☆ |
| Lab 4 | Docker Deployment | 45 min | ⭐⭐⭐☆☆ |
| Lab 5 | Zero-Downtime Deployment | 40 min | ⭐⭐⭐⭐☆ |
| Lab 6 | Monitoring After Deploy | 30 min | ⭐⭐⭐☆☆ |

**Total Duration:** ~4 hours

---

## Lab 1: Deploy Static Site to Netlify

### Objectives

- Deploy static site
- Configure custom domain
- Enable continuous deployment

### Instructions

#### Step 1.1: Prepare Site

```bash
mkdir -p ~/deploy-labs/static-site
cd ~/deploy-labs/static-site

cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Hello from Netlify!</h1>
    <p>This site is deployed automatically.</p>
</body>
</html>
EOF

cat > style.css << 'EOF'
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
}
EOF
```

#### Step 1.2: Deploy via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy
```

**Follow prompts:**

```
? What would you like to do? Create & configure a new site
? Site name: my-portfolio-site
? Publish directory: .
```

**Production deploy:**

```bash
netlify deploy --prod
```

✅ **Lab 1 Complete!** Site is live!

---

## Lab 2: Deploy to GitHub Pages

### Objectives

- Deploy via GitHub Pages
- Auto-deploy on push

### Instructions

#### Step 2.1: Create Repository

```bash
cd ~/deploy-labs/static-site
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/username/my-site.git
git branch -M main
git push -u origin main
```

#### Step 2.2: GitHub Actions Deploy

```bash
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/upload-pages-artifact@v2
        with:
          path: .
      - uses: actions/deploy-pages@v2
EOF

git add .
git commit -m "Add deploy workflow"
git push
```

**Enable Pages:**

1. Repo → Settings → Pages
2. Source: GitHub Actions
3. Site live at: <https://username.github.io/my-site>

✅ **Lab 2 Complete!** GitHub Pages deployed!

---

## Lab 3: VPS Setup & Deployment

### Objectives

- Setup production VPS
- Deploy Node.js app with PM2
- Configure NGINX

### Instructions

#### Step 3.1: Create VPS

**Use DigitalOcean, Linode, or AWS:**

- Ubuntu 22.04
- $5/month tier
- SSH key authentication

#### Step 3.2: Initial Server Setup

```bash
# SSH to server
ssh root@your-server-ip

# Create user
adduser deploy
usermod -aG sudo deploy

# Setup SSH for new user
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy

# Switch to deploy user
su - deploy
```

#### Step 3.3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install NGINX
sudo apt install -y nginx
```

#### Step 3.4: Deploy Application

```bash
# Clone app
cd /var/www
sudo git clone https://github.com/username/my-app.git
cd my-app
sudo npm install

# Start with PM2
pm2 start server.js --name myapp
pm2 startup systemd
pm2 save
```

#### Step 3.5: Configure NGINX

```bash
sudo tee /etc/nginx/sites-available/myapp << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

✅ **Lab 3 Complete!** App deployed to VPS!

---

## Labs 4-6 Summary

- **Lab 4:** Docker Compose deployment
- **Lab 5:** Blue-green deployment strategy
- **Lab 6:** Health checks and monitoring

---

## 🎉 Deployment Mastery Checklist

- [x] Deploy static sites (Netlify, GitHub Pages)
- [x] Deploy to VPS
- [] Docker deployments
- [] Zero-downtime strategies
- [] Production monitoring

### Next: Module 09 - MONITORING BASICS

---

> **"Deploy fast, deploy safe!" 🚀**
