# 📋 Interview Prep - Cheatsheet

> **Quick Reference for DevOps Interviews**
>
> *Tra cứu nhanh phỏng vấn DevOps*

---

## 🎯 Common Topics (Chủ đề thường gặp)

| Topic | Key Concepts |
|-------|--------------|
| **Linux** | Permissions, processes, systemd, logs |
| **Networking** | TCP/IP, DNS, HTTP, load balancing |
| **Docker** | Images, containers, Dockerfile, compose |
| **Kubernetes** | Pods, deployments, services, ingress |
| **CI/CD** | GitLab CI, pipelines, deployment strategies |
| **Cloud** | AWS services, VPC, IAM, S3, EC2 |
| **IaC** | Terraform, Ansible, state management |
| **Monitoring** | Prometheus, Grafana, alerting |

---

## 💡 Sample Questions (Câu hỏi mẫu)

### Linux

- What happens when you run `chmod 755 file.txt`?
- How do you find processes using port 80?
- Explain the difference between `kill` and `kill -9`.

### Docker

- What is the difference between CMD and ENTRYPOINT?
- How do you reduce Docker image size?
- What is the difference between `COPY` and `ADD`?

### Kubernetes

- Explain the difference between Deployment and StatefulSet.
- How does a Service route traffic to pods?
- What is a PersistentVolumeClaim?

### CI/CD

- What is the difference between GitLab CI and GitHub Actions?
- Explain blue-green deployment.
- How do you handle secrets in pipelines?

---

## 🔄 GitLab CI vs GitHub Actions

| Feature | GitLab CI | GitHub Actions |
|---------|-----------|----------------|
| Config | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| Triggers | Auto on push | `on:` keyword |
| Stages | `stages:` | `jobs:` + `needs:` |
| Variables | `$CI_*` | `$GITHUB_*` |
| Registry | Built-in | GitHub Packages |

---

## 🏗️ System Design Framework

```
1. REQUIREMENTS (5 min)
   - Functional: What does it do?
   - Non-functional: Scale, latency, availability?

2. CAPACITY (5 min)
   - Users, requests/sec, data size

3. HIGH-LEVEL DESIGN (10 min)
   - Draw components on whiteboard
   - Show data flow

4. DEEP DIVE (15 min)
   - Database choice
   - Caching strategy
   - Scale considerations

5. TRADE-OFFS (5 min)
   - Discuss design decisions
```

---

## ✅ Interview Tips (Mẹo phỏng vấn)

1. **Think aloud** (Nói ra suy nghĩ)
2. **Ask clarifying questions** (Hỏi câu hỏi làm rõ)
3. **Discuss trade-offs** (Thảo luận đánh đổi)
4. **Be honest about unknowns** (Thật thà về điều không biết)
5. **Show curiosity** (Thể hiện sự tò mò)

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
