# EXERCISES - Modules 02-09

This file contains exercises for modules 02 through 09. Each module has 15-20 targeted exercises.

---

## Module 02: GIT & GITHUB (20 Exercises)

### Basic Git (1-5)

1. Initialize repo, make 5 commits with meaningful messages
2. Create `.gitignore` for Node.js project
3. Amend last commit to add forgotten file
4. View diff between current state and 3 commits ago
5. Stash changes, switch branches, apply stash

### Branching (6-10)

6. Create feature branch, make changes, merge to main
2. Resolve merge conflict between two branches
3. Rebase feature branch onto updated main
4. Cherry-pick specific commit to another branch
5. Delete merged branches locally and remotely

### GitHub Collaboration (11-15)

11. Fork repository, clone, make changes, create PR
2. Review PR, request changes, approve
3. Sync forked repo with upstream
4. Create release with tags
5. Set up branch protection rules

### Advanced (16-20)

16. Interactive rebase to squash commits
2. Bisect to find bug-introducing commit
3. Recover deleted branch using reflog
4. Set up Git hooks for commit validation
5. Create Git alias for complex command

---

## Module 03: NETWORKING (15 Exercises)

### IP & Subnetting (1-5)

1. Calculate subnet info for 192.168.10.50/26
2. Design network for 500 hosts (choose CIDR)
3. Identify network/broadcast for 10.50.100.25/22
4. Split 172.16.0.0/16 into 4 equal subnets
5. Determine if two IPs are on same subnet

### DNS (6-10)

6. Query DNS records (A, AAAA, MX, NS, TXT) for domain
2. Trace DNS resolution path with dig +trace
3. Set up local DNS override in /etc/hosts
4. Troubleshoot DNS not resolving
5. Compare response times of different DNS servers

### Connectivity (11-15)

11. Diagnose why server is unreachable
2. Trace route to external server, identify hops
3. Test if specific port is open on remote host
4. Measure latency to 5 different servers
5. Capture HTTP request/response with tcpdump

---

## Module 04: HTML/CSS/JS (20 Exercises)

### HTML (1-5)

1. Create semantic HTML page with header/nav/main/footer
2. Build accessible form with labels and validation
3. Create responsive image gallery
4. Build data table with sorting capability
5. Implement meta tags for SEO

### CSS (6-10)

6. Style card component with shadows and hover effects
2. Create navigation bar with dropdown menu
3. Build responsive grid layout (3 columns → 1 on mobile)
4. Animate button with CSS transitions
5. Create loading spinner with pure CSS

### JavaScript (11-15)

11. Validate form input before submission
2. Fetch data from API and display
3. Implement dark mode toggle
4. Create image carousel
5. Build todo list with localStorage

### Integration (16-20)

16. Build complete landing page
2. Create contact form with validation
3. Implement smooth scroll navigation
4. Build responsive navbar with hamburger menu
5. Create pricing table with toggle (monthly/yearly)

---

## Module 05: DOCKER (20 Exercises)

### Images & Containers (1-5)

1. Run 3 different containers (nginx, mysql, redis)
2. Build custom image from Dockerfile
3. Tag image with 3 different tags
4. Push image to Docker Hub
5. Inspect image layers and identify optimization opportunities

### Dockerfile (6-10)

6. Create multi-stage build for Node.js app
2. Optimize Dockerfile to reduce image size by 50%
3. Add HEALTHCHECK to Dockerfile
4. Use build arguments for flexibility
5. Create Dockerfile for Python Flask app

### Volumes & Networks (11-15)

11. Create named volume for database persistence
2. Share data between containers using volumes
3. Create custom network and connect 3 containers
4. Access containerized app from host via port mapping
5. Backup and restore volume data

### Docker Compose (16-20)

16. Write docker-compose.yml for NGINX + Node.js
2. Add MySQL database to compose file
3. Implement environment variables in compose
4. Scale service to 3 replicas
5. Create complete MERN stack with Docker Compose

---

## Module 06: CI/CD (15 Exercises)

### GitHub Actions Basics (1-5)

1. Create workflow that runs on every push
2. Add linting step to workflow
3. Run tests in parallel for Node 16, 18, 20
4. Create manual workflow with inputs
5. Add status badge to README

### Build & Test (6-10)

6. Build Docker image in CI
2. Run integration tests in workflow
3. Generate code coverage report
4. Cache node_modules for faster builds
5. Upload build artifacts

### Advanced CI/CD (11-15)

11. Push Docker image to registry on tag
2. Deploy to staging on main branch push
3. Create approval gate for production deploy
4. Implement rollback mechanism
5. Build complete CI/CD pipeline (test → build → deploy)

---

## Module 07: WEB SERVERS (15 Exercises)

### NGINX Basics (1-5)

1. Configure NGINX to serve static site
2. Set up virtual hosts for 3 domains
3. Enable directory listing
4. Configure custom error pages
5. Add basic authentication to location

### Reverse Proxy (6-10)

6. Proxy requests to Node.js backend
2. Load balance across 3 backend servers
3. Configure sticky sessions
4. Add custom headers to proxied requests
5. Implement rate limiting

### SSL & Performance (11-15)

11. Generate self-signed certificate
2. Configure HTTPS with SSL
3. Enable HTTP/2
4. Set up gzip compression
5. Implement browser caching with expires headers

---

## Module 08: DEPLOYMENT (15 Exercises)

### Static Deployment (1-5)

1. Deploy to Netlify via CLI
2. Set up GitHub Pages with custom domain
3. Deploy to Vercel with environment variables
4. Configure redirects and rewrites
5. Enable HTTPS on deployment

### Server Deployment (6-10)

6. Deploy Node.js app to VPS with PM2
2. Set up NGINX reverse proxy for app
3. Configure auto-restart on crashes
4. Implement log rotation
5. Set up staging and production environments

### Advanced Deployment (11-15)

11. Blue-green deployment
2. Canary release (10% traffic to new version)
3. Rollback deployment to previous version
4. Zero-downtime deployment
5. Automated deploy on git push (CI/CD integration)

---

## Module 09: MONITORING (15 Exercises)

### Logging (1-5)

1. Centralize logs from multiple containers
2. Parse and analyze NGINX access logs
3. Set up log rotation
4. Create log dashboard
5. Implement structured logging in app

### Metrics & Alerts (6-10)

6. Monitor CPU, memory, disk usage
2. Set up uptime monitoring
3. Create health check endpoint
4. Configure alerts for high resource usage
5. Track application-specific metrics

### Incident Response (11-15)

11. Simulate high CPU and diagnose
2. Investigate memory leak
3. Debug slow API responses
4. Troubleshoot container restart loop
5. Write post-mortem for incident

---

## 🎯 Completion Requirements

**To complete each module:**

- ✅ Complete 70% of exercises (11-14 exercises per module)
- ✅ Submit solutions or screenshots
- ✅ Pass associated quiz (in QUIZ.md)

**For certification:**

- Complete ALL exercises across all modules
- Score 90%+ on all quizzes
- Complete all mini-projects

---

> **Total Across All Modules: 165 Exercises!** 💪
