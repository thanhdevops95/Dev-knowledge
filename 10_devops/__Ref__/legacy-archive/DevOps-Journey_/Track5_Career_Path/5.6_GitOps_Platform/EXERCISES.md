# 💪 Exercises: GitOps Platform

> **Practice Exercises for GitOps**
>
> *Bài tập thực hành GitOps.*

---

## Exercise 1: Setup GitOps Repository (Beginner)

Create a GitOps repository structure:

*(Tạo cấu trúc repository GitOps:)*

```
gitops-repo/
├── apps/
│   ├── base/
│   │   ├── deployment.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/
│       └── prod/
├── infrastructure/
│   ├── monitoring/
│   └── ingress/
└── clusters/
    ├── dev/
    └── prod/
```

---

## Exercise 2: Multi-Environment Deployment (Beginner)

Deploy same app to dev and prod with different configs:

*(Deploy cùng app đến dev và prod với config khác nhau:)*

- Dev: 1 replica, debug logging
- Prod: 3 replicas, warn logging

---

## Exercise 3: Helm Chart GitOps (Intermediate)

Create ArgoCD application that:

*(Tạo ArgoCD application mà:)*

1. Deploys PostgreSQL from Bitnami Helm chart
2. Uses external secret for password
3. Configures persistence

---

## Exercise 4: Progressive Delivery (Intermediate)

Implement canary deployment with:

*(Triển khai canary deployment với:)*

1. Argo Rollouts
2. 20% traffic to canary
3. Automated promotion after 5 minutes

---

## Exercise 5: Complete GitOps Platform (Advanced)

Build production-ready GitOps platform:

*(Xây dựng nền tảng GitOps sẵn sàng production:)*

1. ArgoCD with SSO
2. Image automation (commit to repo)
3. Notifications to Slack
4. Multi-cluster support

---

## ✅ Submission Checklist

- [ ] GitOps repository created *(Repository GitOps đã tạo)*
- [ ] Applications syncing *(Applications đang sync)*
- [ ] Environments configured *(Môi trường đã cấu hình)*
- [ ] Documentation complete *(Tài liệu hoàn chỉnh)*

---

**[← Back to README](./README.md)**
