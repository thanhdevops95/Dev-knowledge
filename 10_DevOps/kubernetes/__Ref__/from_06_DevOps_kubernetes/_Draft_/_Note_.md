Intro

What is Kubernetes(K8s)?

What problem does Kubernetes(K8s) solve?

Nên/không nên chọn K8s?

K8s Architecture

Certification of CNCF

Install K8s
Docker install: https://docs.docker.com/engine/install/ 
Docker hub repos: https://hub.docker.com/repositories/v
Install kubectl: https://kubernetes.io/docs/tasks/tools/ 
kind: https://kind.sigs.k8s.io/ 
minikube installation: https://minikube.sigs.k8s.io/docs/start/ 


 - Docker installation
 - minikuke
 - Docker account
 - Kubectl installation
 - Verify

Imperative vs Declarative
Pod - Imperative
Pod - Declarative
NodePort service
Service Type
Namespaces
Labels & Selectors
ReplicaSet
Deployments
Rolling Updates & Rollbacks
Taints & Tolerance
NodeSlector
NodeAffinity
Pod -Eviroment variables




so sánh minikube vs kind để lựa chọn                                                                     
                                       
⏺ ┌──────────────┬─────────────────────────────────────────┬──────────────────────────────────────────┐    
  │   Tiêu chí   │                Minikube                 │       Kind (Kubernetes IN Docker)        │    
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Cách chạy    │ Tạo máy ảo riêng (Docker/VM)            │ Dùng container Docker có sẵn             │
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Tốc độ start │ Chậm (1-3 phút)                         │ Rất nhanh (<30s)                         │    
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Tài nguyên   │ Tốn RAM/CPU hơn                         │ Nhẹ hơn                                  │    
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Cài đặt      │ Cần cài riêng                           │ Cần Docker có sẵn (bạn đã có)            │
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Phù hợp      │ Học sâu K8s, cần NodePort, LoadBalancer │ Học nhanh, test CI/CD, tạo nhiều cluster │
  ├──────────────┼─────────────────────────────────────────┼──────────────────────────────────────────┤    
  │ Tính năng    │ Hỗ trợ addons (dashboard, ingress)      │ Tập trung vào dev/test                   │
  └──────────────┴─────────────────────────────────────────┴──────────────────────────────────────────┘    
                  
  Lời khuyên: Bạn đã có Docker sẵn → kind nhanh gọn hơn cho việc học. Nhưng minikube mô phỏng môi trường   
  thực tế tốt hơn (có dashboard, load balancer).



systems desig: k8s là gì

mô hình master-worker(slave)

