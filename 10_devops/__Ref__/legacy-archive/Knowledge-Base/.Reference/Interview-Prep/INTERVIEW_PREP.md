# 🎯 DevOps Interview Preparation Guide

> **Hướng dẫn chuẩn bị phỏng vấn DevOps Engineer toàn diện**

---

## 📋 Tổng quan

Tài liệu này giúp bạn chuẩn bị cho phỏng vấn vị trí DevOps Engineer ở mọi cấp độ.

---

## 🎓 Interview Process

### Các vòng phỏng vấn điển hình

```mermaid
graph LR
    A[HR Screening] --> B[Technical Phone]
    B --> C[Technical Deep-dive]
    C --> D[System Design]
    D --> E[Behavioral]
    E --> F[Offer]
```

| Vòng | Thời gian | Nội dung |
|------|-----------|----------|
| HR Screening | 15-30 phút | Background, salary, availability |
| Technical Phone | 45-60 phút | Kiến thức cơ bản, coding |
| Technical Deep-dive | 1-2 giờ | Hands-on, troubleshooting |
| System Design | 1 giờ | Thiết kế hệ thống |
| Behavioral | 30-45 phút | Soft skills, teamwork |

---

## 📚 Chủ đề cần chuẩn bị

### 1. Linux & OS

**Câu hỏi thường gặp:**

- Giải thích file permissions trong Linux
- Làm sao tìm file lớn nhất trong filesystem?
- Process vs Thread khác nhau thế nào?
- Giải thích boot process của Linux
- TCP vs UDP khác gì nhau?

**Lệnh cần thành thạo:**

```bash
# Files & Directories
ls, cd, cp, mv, rm, find, grep, awk, sed

# Processes
ps, top, kill, nohup, &

# Networking
netstat, ss, curl, ping, traceroute

# System
df, du, free, vmstat, iostat
```

### 2. Networking

**Câu hỏi thường gặp:**

- OSI model có bao nhiêu layers? Giải thích từng layer
- TCP 3-way handshake hoạt động thế nào?
- DNS resolution process?
- HTTP vs HTTPS khác gì?
- Load balancer hoạt động thế nào?

### 3. Git & Version Control

**Câu hỏi thường gặp:**

- Git merge vs rebase khác gì?
- Giải thích Gitflow workflow
- Làm sao undo last commit?
- Git cherry-pick dùng khi nào?
- Conflict resolution như thế nào?

**Commands cần biết:**

```bash
git rebase -i HEAD~5
git reset --soft/--mixed/--hard
git cherry-pick <commit>
git reflog
git stash
```

### 4. Docker & Containers

**Câu hỏi thường gặp:**

- Container khác VM như thế nào?
- Docker image layers là gì?
- Dockerfile best practices?
- Docker networking types?
- Làm sao optimize Docker image size?

**Dockerfile example để thảo luận:**

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "server.js"]
```

### 5. Kubernetes

**Câu hỏi thường gặp:**

- Pod là gì? Tại sao không dùng container trực tiếp?
- Deployment vs StatefulSet?
- Service types trong K8s?
- Ingress hoạt động thế nào?
- K8s scheduling process?
- Làm sao debug Pod not starting?

**Troubleshooting commands:**

```bash
kubectl get pods -o wide
kubectl describe pod <name>
kubectl logs <pod> -c <container>
kubectl exec -it <pod> -- bash
kubectl get events --sort-by='.lastTimestamp'
```

### 6. CI/CD

**Câu hỏi thường gặp:**

- CI vs CD khác gì?
- Giải thích CI/CD pipeline của bạn
- Blue-green vs Canary deployment?
- GitOps là gì?
- Làm sao rollback deployment?

### 7. Infrastructure as Code

**Câu hỏi thường gặp:**

- Terraform state là gì? Tại sao quan trọng?
- Terraform modules? Khi nào dùng?
- Terraform vs Ansible khác gì?
- Idempotency là gì?
- Làm sao handle secrets trong Terraform?

### 8. Cloud (AWS/GCP/Azure)

**Câu hỏi AWS thường gặp:**

- VPC, Subnets, Security Groups?
- EC2 instance types?
- S3 storage classes?
- IAM concepts (Users, Roles, Policies)?
- Load balancer types (ALB, NLB, CLB)?

### 9. Monitoring & Observability

**Câu hỏi thường gặp:**

- 3 pillars of observability?
- Prometheus vs other monitoring tools?
- PromQL basics?
- Alerting best practices?
- SLO, SLI, SLA khác gì?

### 10. Security

**Câu hỏi thường gặp:**

- DevSecOps là gì?
- Secrets management?
- Container security best practices?
- SAST vs DAST?
- Least privilege principle?

---

## 🔧 Hands-on Exercises

### Exercise 1: Troubleshooting

> "Production website returning 502 errors. Walk me through debugging."

**Approach:**

1. Check load balancer health checks
2. Check application logs
3. Check backend server status
4. Check resource usage (CPU, Memory, Disk)
5. Check network connectivity
6. Check recent deployments

### Exercise 2: Design

> "Design a CI/CD pipeline for a microservices application."

**Discuss:**

- Source control workflow
- Build stages
- Testing strategy
- Artifact management
- Deployment strategy
- Rollback plan
- Monitoring

### Exercise 3: Coding

> "Write a script to find all EC2 instances without tags."

```python
import boto3

def find_untagged_instances():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    
    untagged = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if not instance.get('Tags'):
                untagged.append(instance['InstanceId'])
    
    return untagged

print(find_untagged_instances())
```

---

## 💬 Behavioral Questions

### STAR Method

**S**ituation - **T**ask - **A**ction - **R**esult

### Câu hỏi phổ biến

1. **Tell me about a production incident you handled**
   - Describe the situation
   - Your role
   - Actions taken
   - Outcome and lessons learned

2. **Describe a time you automated a manual process**
   - What was the process?
   - Why did you automate?
   - How did you approach it?
   - What was the impact?

3. **How do you handle disagreement with teammates?**
   - Specific example
   - How you resolved
   - What you learned

4. **Tell me about a failure**
   - What happened
   - Your responsibility
   - How you fixed it
   - What you changed afterward

---

## 📝 Questions to Ask Interviewers

### Về Team & Culture

- Team structure và size?
- On-call rotation như thế nào?
- Tech stack hiện tại?
- Agile/Scrum practices?

### Về Growth

- Learning và development opportunities?
- Career path cho DevOps?
- Conference/training budget?

### Về Technical

- Biggest technical challenges?
- Recent improvements to infrastructure?
- Deployment frequency?
- Testing strategy?

---

## 📋 Checklist trước Interview

### 1 tuần trước

- [ ] Research công ty
- [ ] Review job description
- [ ] Prepare STAR stories
- [ ] Review resume

### 1 ngày trước

- [ ] Test internet/camera/mic
- [ ] Prepare environment (quiet, clean background)
- [ ] Prepare questions for interviewer
- [ ] Get enough sleep

### Ngày interview

- [ ] Join 5 phút sớm
- [ ] Have water nearby
- [ ] Turn off notifications
- [ ] Have notepad ready

---

## 🔗 Resources

### Practice Platforms

- [LeetCode](https://leetcode.com/) - Coding
- [HackerRank](https://hackerrank.com/) - DevOps challenges
- [KillerCoda](https://killercoda.com/) - Interactive scenarios
- [Play with Docker](https://labs.play-with-docker.com/)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

### Mock Interviews

- [Pramp](https://pramp.com/)
- [Interviewing.io](https://interviewing.io/)

### Reading

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/1942788290)

---

**Chúc bạn phỏng vấn thành công! 🎉**
