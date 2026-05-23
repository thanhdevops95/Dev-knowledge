# QUIZ - Modules 01-09 (Combined)

> **Passing Score:** 80% per module
> **Time:** 15 minutes per module

---

## Module 01: LINUX BASICS (20 Questions)

### Multiple Choice

1. What does `chmod 755` mean?
   - A) rwxrwxrwx
   - B) rwxr-xr-x ✓
   - C) rw-r--r--
   - **Answer: B**

2. Which command shows current directory?
   - A) cwd
   - B) pwd ✓
   - C) dir
   - **Answer: B**

3. What does `grep -r` do?
   - A) Reverse search
   - B) Recursive search ✓
   - C) Regular expression
   - **Answer: B**

4. Command to find files larger than 100MB?
   - A) find . -size +100M ✓
   - B) find . -bigger 100M
   - C) ls -size 100M
   - **Answer: A**

5. What does `ps aux` show?
   - A) Only your processes
   - B) All processes ✓
   - C) System processes
   - **Answer: B**

### True/False

6. `/etc` contains system configuration files - TRUE ✓
2. `sudo` allows running commands as root - TRUE ✓
3. `rm -rf /` is safe to run - FALSE ✓
4. Permissions 644 = rw-r--r-- - TRUE ✓
5. `apt` is used on RedHat systems - FALSE ✓

### Fill in Blank

11. Extract tar.gz: `tar ______ file.tar.gz` - **Answer: -xzf**
2. Change ownership: `______ user:group file` - **Answer: chown**
3. Install package: `sudo apt ______ package` - **Answer: install**

### Practical

14-15. Write command to:

- Find all .log files and delete them
- **Answer:** `find . -name "*.log" -delete`
- List top 5 CPU processes
- **Answer:** `ps aux --sort=-%cpu | head -6`

---

## Module 02: GIT & GITHUB (20 Questions)

### Multiple Choice

1. Initialize Git repo: `git ______`
   - A) start
   - B) init ✓
   - C) begin
   - **Answer: B**

2. Undo last commit (keep changes)?
   - A) git reset HEAD~1 ✓
   - B) git revert HEAD
   - C) git undo
   - **Answer: A**

3. Create and switch to branch?
   - A) git branch -c name
   - B) git checkout -b name ✓
   - C) git create name
   - **Answer: B**

4. What is a merge conflict?
   - A) Server error
   - B) Same lines changed in branches ✓
   - C) Network issue
   - **Answer: B**

5. Push new branch to remote?
   - A) git push -u origin branch ✓
   - B) git upload branch
   - C) git send branch
   - **Answer: A**

### True/False

6. Git is centralized VCS - FALSE ✓
2. `.gitignore` prevents tracking files - TRUE ✓
3. Commits can be edited after push - TRUE (with force) ✓
4. Pull requests are Git feature - FALSE (GitHub feature) ✓
5. Branches are pointers to commits - TRUE ✓

### Practical

11-15. Commands for:

- Stage all files: `git add .`
- Commit with message: `git commit -m "message"`
- View history: `git log`
- Undo staged file: `git restore --staged file`
- Clone repo: `git clone url`

---

## Module 03: NETWORKING (20 Questions)

### Multiple Choice

1. /24 subnet has how many hosts?
   - A) 24
   - B) 256
   - C) 254 ✓
   - **Answer: C**

2. DNS port number?
   - A) 22
   - B) 53 ✓
   - C) 80
   - **Answer: B**

3. Which is private IP range?
   - A) 20.0.0.0/8
   - B) 192.168.0.0/16 ✓
   - C) 8.8.8.8/32
   - **Answer: B**

4. HTTP default port?
   - A) 443
   - B) 8080
   - C) 80 ✓
   - **Answer: C**

5. Command to test DNS?
   - A) dig domain.com ✓
   - B) test dns
   - C) check domain
   - **Answer: A**

---

## Module 04: HTML/CSS/JS (20 Questions)

### Multiple Choice

1. Which tag for largest heading?
   - A) `<h6>`
   - B) `<h1>` ✓
   - C) `<heading>`
   - **Answer: B**

2. CSS for center with Flexbox?
   - A) `justify-content: center` ✓
   - B) `align: center`
   - C) `center: true`
   - **Answer: A**

3. JavaScript variable declaration?
   - A) var, let, const ✓
   - B) int, string
   - C) variable
   - **Answer: A**

4. Select element by class?
   - A) `document.querySelector('.class')` ✓
   - B) `get.class('class')`
   - C) `select.class`
   - **Answer: A**

5. Responsive meta tag?
   - A) `<meta name="viewport" content="width=device-width">` ✓
   - B) `<meta responsive>`
   - C) `<responsive>`
   - **Answer: A**

---

## Module 05: DOCKER (20 Questions)

### Multiple Choice

1. Build Docker image?
   - A) docker create
   - B) docker build ✓
   - C) docker make
   - **Answer: B**

2. Run container detached?
   - A) docker run -d ✓
   - B) docker start -b
   - C) docker exec -d
   - **Answer: A**

3. Port mapping syntax?
   - A) `-p host:container` ✓
   - B) `-port host container`
   - C) `--map host container`
   - **Answer: A**

4. Where is Dockerfile instruction for base image?
   - A) BASE
   - B) FROM ✓
   - C) IMAGE
   - **Answer: B**

5. Start Compose services?
   - A) docker-compose start
   - B) docker-compose up ✓
   - C) docker-compose run
   - **Answer: B**

### Practical

6-10. Write Dockerfile for:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Module 06: CI/CD (20 Questions)

### Multiple Choice

1. GitHub Actions workflow file location?
   - A) `.github/workflows/` ✓
   - B) `.actions/`
   - C) `workflows/`
   - **Answer: A**

2. Trigger on push to main?
   - A) `on: push: branches: [main]` ✓
   - B) `trigger: main`
   - C) `when: push main`
   - **Answer: A**

3. Access secrets in workflow?
   - A) `${{ secrets.NAME }}` ✓
   - B) `${SECRETS.NAME}`
   - C) `secrets[NAME]`
   - **Answer: A**

### Practical

4-10. Create workflow:

```yaml
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

---

## Module 07: WEB SERVERS (15 Questions)

### Multiple Choice

1. NGINX config file location?
   - A) /etc/nginx/nginx.conf ✓
   - B) /var/nginx/config
   - C) ~/nginx.conf
   - **Answer: A**

2. Test NGINX config?
   - A) nginx check
   - B) nginx -t ✓
   - C) nginx test
   - **Answer: B**

3. Reverse proxy directive?
   - A) proxy_pass ✓
   - B) reverse_to
   - C) backend_url
   - **Answer: A**

### Practical

4-10. NGINX server block:

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Module 08: DEPLOYMENT (15 Questions)

1. PM2 start app?
   - A) pm2 start app.js ✓
   - B) pm2 run app.js
   - C) pm2 execute app.js
   - **Answer: A**

2. Blue-green deployment benefit?
   - A) Zero downtime ✓
   - B) Faster deployment
   - C) Less cost
   - **Answer: A**

3. Environment variables file?
   - A) .env ✓
   - B) .config
   - C) settings.js
   - **Answer: A**

---

## Module 09: MONITORING (15 Questions)

1. View Docker logs?
   - A) docker logs container ✓
   - B) docker view container
   - C) docker read container
   - **Answer: A**

2. Health check HTTP code?
   - A) 200 ✓
   - B) 201
   - C) 204
   - **Answer: A**

3. Top command shows?
   - A) Processes & resources ✓
   - B) Only CPU
   - C) Network usage
   - **Answer: A**

---

## Scoring Guide

**Per Module:**

- 18-20: Excellent ⭐⭐⭐
- 16-17: Pass ⭐⭐
- 14-15: Review & Retake ⭐
- <14: Study More ❌

**Overall Foundation Track:**

- Must pass ALL module quizzes
- Average score 80%+
- Complete all labs & exercises
- Build mini-projects

---

> **Total Questions: 180 across all modules!** 📝
