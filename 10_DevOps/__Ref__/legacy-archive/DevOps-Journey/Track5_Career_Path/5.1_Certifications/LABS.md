# 🔬 Labs: Certifications

---

## 🔬 Lab 1: AWS Cloud Practitioner Prep

### Study Resources

- AWS Skill Builder (Free)
- Whizlabs/Tutorials Dojo practice exams
- AWS Documentation

### Key Topics

- Cloud concepts (25%)
- Security & Compliance (25%)
- Technology (33%)
- Billing & Pricing (17%)

### Practice

```bash
# Hands-on with AWS Free Tier (Hands-on với AWS Free Tier)
# Create: EC2, S3, Lambda, RDS
# Explore: IAM, VPC, CloudWatch
```

---

## 🔬 Lab 2: AWS Solutions Architect Associate

### Key Topics

- Resilient architectures (30%)
- High-performing architectures (28%)
- Secure applications (24%)
- Cost optimization (18%)

### Hands-on Practice

- Design multi-tier VPC
- Implement Auto Scaling
- Setup Multi-AZ RDS
- Configure CloudFront CDN

---

## 🔬 Lab 3: CKA/CKAD Prep

```bash
# Practice environment
minikube start

# Key commands to master
kubectl run nginx --image=nginx
kubectl create deployment web --image=nginx --replicas=3
kubectl expose deployment web --port=80 --type=NodePort
kubectl get pods -o wide
kubectl describe pod nginx
kubectl logs nginx
kubectl exec -it nginx -- sh

# Practice scenarios
# - Deploy application from YAML
# - Troubleshoot failing pods
# - Configure ConfigMaps/Secrets
# - Setup NetworkPolicies
```

### Practice Platforms

- killer.sh (official simulator)
- KodeKloud
- CKAD-exercises GitHub repo

---

## 🔬 Lab 4: Terraform Associate

### Key Topics

- IaC concepts
- Terraform workflow
- Modules
- State management
- HCL syntax

### Practice

```bash
# Create resources with Terraform
terraform init
terraform plan
terraform apply

# Practice:
# - Write modules
# - Use remote state
# - Import existing resources
# - Workspaces
```

---

## ✅ Exam Day Checklist

- [ ] Valid ID
- [ ] Stable internet (online proctored)
- [ ] Quiet room
- [ ] Practice tests completed
- [ ] Hands-on experience

---

**[← Back to README](./README.md)**
