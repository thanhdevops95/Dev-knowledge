# 📋 MODULE 04: CD - YÊU CẦU & TIÊU CHÍ NGHIỆM THU

## 🎯 Mục tiêu Module

1. ✅ Hiểu Continuous Deployment và GitOps
2. ✅ Deploy app lên Kubernetes (K8s)
3. ✅ Sử dụng ArgoCD cho GitOps workflow
4. ✅ Implement rolling updates và rollbacks
5. ✅ Configure load balancing và auto-scaling

## 📖 Thuật ngữ

| Từ viết tắt | Tiếng Anh đầy đủ | Nghĩa tiếng Việt |
|-------------|------------------|------------------|
| **CD** | Continuous Deployment | Triển khai liên tục |
| **K8s** | Kubernetes | Hệ thống orchestration containers |
| **Pod** | Pod | Đơn vị nhỏ nhất trong K8s |
| **Deployment** | Deployment | Quản lý pods |
| **Service** | Service | Load balancer cho pods |
| **Ingress** | Ingress | HTTP routing |
| **GitOps** | GitOps | Deploy bằng Git làm source of truth |
| **ArgoCD** | ArgoCD | GitOps tool |

## ✅ Checklist LABS

- [ ] LAB 1: Setup local Kubernetes (minikube/kind)
- [ ] LAB 2: Deploy Counter App to K8s
- [ ] LAB 3: Install và configure ArgoCD
- [ ] LAB 4: Implement rolling update

## 🚨 Checklist SCENARIOS

- [ ] Scenario 1: Pods crash loop (CrashLoopBackOff)
- [ ] Scenario 2: Service không accessible từ ngoài
- [ ] Scenario 3: Rolling update failed, cần rollback
- [ ] Scenario 4: Out of Memory (OOM) kills pods
- [ ] Scenario 5: ArgoCD sync stuck ở "Progressing"

## ⏱️ Thời lượng: 10-12 giờ
