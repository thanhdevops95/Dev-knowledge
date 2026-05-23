# 📚 Glossary - Thuật ngữ DevOps

> **Từ điển các thuật ngữ DevOps từ A-Z**

---

## A

**Agile**
Phương pháp phát triển phần mềm linh hoạt, chia nhỏ công việc thành các sprint ngắn.

**Ansible**
Công cụ automation mã nguồn mở để cấu hình servers, deploy ứng dụng.

**API (Application Programming Interface)**
Giao diện cho phép các ứng dụng giao tiếp với nhau.

**ArgoCD**
Công cụ GitOps cho Kubernetes, tự động sync cluster với Git repository.

**Artifact**
Sản phẩm đầu ra của build process (JAR, Docker image, binary).

**AWS (Amazon Web Services)**
Nền tảng cloud computing của Amazon.

---

## B

**Blue-Green Deployment**
Chiến lược deploy với 2 môi trường giống nhau, chuyển traffic khi sẵn sàng.

**Build**
Quá trình biên dịch và đóng gói source code thành artifact.

---

## C

**Canary Deployment**
Chiến lược deploy từ từ, bắt đầu với một phần nhỏ traffic.

**CD (Continuous Delivery/Deployment)**
Tự động deploy code đã pass CI lên các môi trường.

**CI (Continuous Integration)**
Tự động build và test code mỗi khi có thay đổi.

**Cluster**
Nhóm servers làm việc cùng nhau như một hệ thống.

**ConfigMap (Kubernetes)**
Resource lưu trữ configuration data không nhạy cảm.

**Container**
Đơn vị đóng gói application và dependencies, chạy isolated.

**Container Orchestration**
Quản lý nhiều containers trên nhiều hosts (Kubernetes, Docker Swarm).

---

## D

**DaemonSet (Kubernetes)**
Đảm bảo một pod chạy trên mỗi node trong cluster.

**Deployment (Kubernetes)**
Resource quản lý ReplicaSets và cung cấp declarative updates.

**DevOps**
Văn hóa và thực hành kết hợp Development và Operations.

**DevSecOps**
Tích hợp Security vào DevOps pipeline.

**Docker**
Platform để build, ship, và run containers.

**Docker Compose**
Tool định nghĩa và chạy multi-container Docker applications.

**Dockerfile**
File chứa instructions để build Docker image.

---

## E

**EKS (Elastic Kubernetes Service)**
Managed Kubernetes service của AWS.

**Elasticsearch**
Search và analytics engine, thường dùng cho logging.

**Environment Variable**
Biến môi trường dùng để cấu hình applications.

**Error Budget**
Lượng downtime cho phép dựa trên SLO (1 - SLO).

---

## F

**Fluentd**
Open-source data collector cho unified logging.

**Fork**
Bản copy của repository để phát triển độc lập.

---

## G

**Git**
Hệ thống version control phân tán.

**GitHub**
Platform hosting Git repositories với collaboration features.

**GitHub Actions**
CI/CD platform tích hợp trong GitHub.

**GitLab**
Platform DevOps với Git repository, CI/CD, và nhiều features khác.

**GitOps**
Quản lý infrastructure và deployments qua Git.

**GKE (Google Kubernetes Engine)**
Managed Kubernetes service của Google Cloud.

**Grafana**
Platform visualization và monitoring.

---

## H

**Helm**
Package manager cho Kubernetes.

**Horizontal Pod Autoscaler (HPA)**
Tự động scale pods dựa trên metrics.

**HTTP (Hypertext Transfer Protocol)**
Protocol truyền tải web content.

**HTTPS**
HTTP với mã hóa SSL/TLS.

---

## I

**IaC (Infrastructure as Code)**
Quản lý infrastructure bằng code (Terraform, Ansible).

**Image**
Template read-only để tạo containers.

**Ingress (Kubernetes)**
Resource quản lý external access vào services trong cluster.

---

## J

**Jenkins**
Open-source automation server cho CI/CD.

---

## K

**Kibana**
Visualization frontend cho Elasticsearch.

**kubectl**
Command-line tool để tương tác với Kubernetes.

**Kubernetes (K8s)**
Container orchestration platform.

---

## L

**Load Balancer**
Phân phối traffic đến nhiều servers.

**Loki**
Log aggregation system của Grafana Labs.

---

## M

**Microservices**
Kiến trúc chia application thành các services nhỏ, độc lập.

**Minikube**
Tool chạy Kubernetes locally.

**Monitoring**
Theo dõi và thu thập metrics của hệ thống.

---

## N

**Namespace (Kubernetes)**
Cách chia cluster thành multiple virtual clusters.

**Network Policy (Kubernetes)**
Rules kiểm soát traffic giữa pods.

**Nginx**
Web server và reverse proxy phổ biến.

**Node**
Một machine (physical hoặc virtual) trong Kubernetes cluster.

---

## O

**Observability**
Khả năng hiểu trạng thái hệ thống qua outputs (logs, metrics, traces).

---

## P

**Pipeline**
Chuỗi các bước tự động trong CI/CD.

**Pod**
Đơn vị nhỏ nhất trong Kubernetes, chứa một hoặc nhiều containers.

**Prometheus**
Monitoring và alerting toolkit.

**Proxy**
Trung gian giữa client và server.

---

## R

**RBAC (Role-Based Access Control)**
Kiểm soát quyền truy cập dựa trên roles.

**Redis**
In-memory data store, thường dùng làm cache.

**Registry**
Nơi lưu trữ và phân phối container images.

**Replica**
Bản copy của pod/service để high availability.

**ReplicaSet (Kubernetes)**
Đảm bảo số lượng pod replicas mong muốn.

**REST API**
API theo kiến trúc RESTful.

**Rollback**
Quay lại version trước khi có lỗi.

**Rolling Update**
Cập nhật từng phần, không downtime.

---

## S

**Scaling**

- **Horizontal**: Thêm instances
- **Vertical**: Tăng resources của instance

**Secret**
Dữ liệu nhạy cảm (passwords, API keys) được mã hóa.

**Service (Kubernetes)**
Abstraction để expose pods ra network.

**Service Mesh**
Infrastructure layer cho service-to-service communication (Istio).

**SLA (Service Level Agreement)**
Hợp đồng về mức độ service.

**SLI (Service Level Indicator)**
Metric đo lường service.

**SLO (Service Level Objective)**
Mục tiêu cho SLI (ví dụ: 99.9% availability).

**SRE (Site Reliability Engineering)**
Kỹ sư vận hành với mindset software engineering.

**SSH (Secure Shell)**
Protocol truy cập remote server an toàn.

**SSL/TLS**
Protocols mã hóa network communication.

**StatefulSet (Kubernetes)**
Quản lý stateful applications trong Kubernetes.

---

## T

**Terraform**
IaC tool của HashiCorp.

**Toil**
Công việc thủ công, lặp lại, có thể tự động hóa.

---

## V

**Vault**
Tool quản lý secrets của HashiCorp.

**Virtual Machine (VM)**
Máy ảo chạy trên hypervisor.

**Volume**
Persistent storage cho containers.

**VPC (Virtual Private Cloud)**
Mạng riêng ảo trong cloud.

---

## Y

**YAML**
Format dữ liệu human-readable, thường dùng cho config files.

---

## Số & Ký hiệu

**12-Factor App**
Methodology xây dựng SaaS applications.

**3 Ways of DevOps**

1. Flow (left to right)
2. Feedback (right to left)
3. Continuous Learning

---

**💡 Tip**: Bookmark trang này để tra cứu nhanh!
