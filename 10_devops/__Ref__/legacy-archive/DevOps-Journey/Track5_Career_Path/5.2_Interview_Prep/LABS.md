# 🔬 Labs: Interview Prep

---

## 🔬 Lab 1: Technical Questions Practice

### Linux/Bash

```bash
# Q: Find all .log files modified in last 7 days
find /var/log -name "*.log" -mtime -7

# Q: Count lines with "ERROR" in log file
grep -c "ERROR" app.log

# Q: Check disk usage
df -h
du -sh /var/*
```

### Networking

```
Q: Explain TCP 3-way handshake
A: SYN → SYN-ACK → ACK

Q: What's the difference between TCP and UDP?
A: TCP = reliable, ordered; UDP = fast, unreliable

Q: How does DNS work?
A: Recursive query → Root → TLD → Authoritative → IP
```

### Docker

```
Q: Image vs Container?
A: Image is template (read-only), Container is running instance

Q: How to reduce Docker image size?
A: Multi-stage builds, alpine base, .dockerignore

Q: What happens when container stops?
A: Container stops, data in writable layer lost unless volume used
```

---

## 🔬 Lab 2: System Design Practice

### Design: Scalable Web Application

```
Requirements:
- Handle 1M users
- 99.9% availability
- Global users

Solution components:
1. CDN for static content
2. Load balancer
3. Auto-scaling app tier
4. Read replicas for database
5. Redis caching
6. Message queue for async
```

### Design: CI/CD Pipeline

```
Requirements:
- Git-based trigger
- Multi-environment
- Automated testing
- Blue/green deployment

Solution:
1. Git webhook → CI server
2. Build → Unit tests → Integration tests
3. Docker build & push
4. Deploy to staging
5. Approval gate
6. Blue/green to production
```

---

## 🔬 Lab 3: Behavioral Questions (STAR)

### Example: Tell me about a challenging project

```
S - Situation:
   "Our production system was experiencing frequent outages"

T - Task:
   "I was responsible for improving system reliability"

A - Action:
   "I implemented monitoring with Prometheus/Grafana,
    set up auto-scaling, and created runbooks"

R - Result:
   "Reduced downtime by 90%, from 4 hours/month to 
    less than 30 minutes"
```

### Practice Questions

1. Describe a time you improved a process
2. How do you handle disagreements with team members?
3. Tell me about a failed project and what you learned
4. How do you prioritize when everything is urgent?

---

## 🔬 Lab 4: Mock Interview

### Structure (45-60 min)

1. Introduction (5 min)
2. Technical questions (20 min)
3. System design (20 min)
4. Behavioral (10 min)
5. Your questions (5 min)

### Questions to Ask Interviewer

- "What does a typical day look like?"
- "What are the biggest challenges for this role?"
- "How does the team handle on-call?"
- "What's the tech stack?"

---

## ✅ Interview Checklist

- [ ] Research the company
- [ ] Review job description
- [ ] Prepare STAR stories
- [ ] Practice technical questions
- [ ] Prepare questions to ask
- [ ] Test video/audio setup
- [ ] Professional attire

---

**[← Back to README](./README.md)**
