# DevOps Terms Dictionary -- Từ điển Thuật ngữ DevOps

> DevOps terminology from English to Vietnamese -- Thuật ngữ DevOps từ tiếng Anh sang tiếng Việt

## 📋 Table of Contents -- Mục lục

- [A-C](#a-c)
- [D-I](#d-i)
- [K-P](#k-p)
- [R-Z](#r-z)

## A-C

### Agile -- Phương pháp Agile
- **Definition -- Định nghĩa:** A software development methodology that emphasizes iterative development and collaboration. -- Phương pháp phát triển phần mềm nhấn mạnh việc phát triển lặp lại và cộng tác.
- **Example -- Ví dụ:** Scrum, Kanban

### Artifact -- Sản phẩm Đầu ra
- **Definition -- Định nghĩa:** A file or package produced by a build process. -- File hoặc gói được tạo ra từ quá trình build.
- **Example -- Ví dụ:** JAR, WAR, Docker image, npm package

### Blue-Green Deployment -- Triển khai Xanh-Lục
- **Definition -- Định nghĩa:** A deployment strategy using two identical environments to reduce downtime. -- Chiến lược deployment sử dụng 2 môi trường giống hệt nhau để giảm downtime.
- **How it works -- Cách hoạt động:** 
  - Blue: Current production -- Môi trường production hiện tại
  - Green: New version -- Phiên bản mới
  - Switch traffic when ready -- Chuyển traffic khi sẵn sàng

### Canary Deployment -- Triển khai Canary
- **Definition -- Định nghĩa:** A deployment strategy that gradually rolls out changes to a small subset of users. -- Chiến lược deployment triển khai dần thay đổi cho một nhóm nhỏ users.
- **Use case -- Trường hợp dùng:** Risk mitigation for new releases. -- Giảm thiểu rủi ro cho bản phát hành mới.

### CI/CD (Continuous Integration/Continuous Deployment -- Tích hợp/Triển khai Liên tục)
- **Definition -- Định nghĩa:** Practices that automate the build, test, and deployment process. -- Các thực hành tự động hóa quá trình build, test và deploy.
- **Components -- Thành phần:**
  - CI: Merge code frequently, run automated tests -- Merge code thường xuyên, chạy tests tự động
  - CD: Automatically deploy to staging/production -- Tự động deploy lên staging/production

### Configuration Management -- Quản lý Cấu hình
- **Definition -- Định nghĩa:** The process of maintaining system configuration consistently. -- Quá trình duy trì cấu hình hệ thống một cách nhất quán.
- **Tools -- Công cụ:** Ansible, Chef, Puppet, SaltStack

### Container -- Container
- **Definition -- Định nghĩa:** A lightweight, standalone package that includes everything needed to run an application. -- Một gói nhẹ, độc lập bao gồm mọi thứ cần thiết để chạy ứng dụng.
- **Key features -- Đặc điểm chính:**
  - Isolated environment -- Môi trường cô lập
  - Portable across platforms -- Di động qua các nền tảng
  - Shares OS kernel -- Chia sẻ OS kernel

### Continuous Delivery -- Phân phối Liên tục
- **Definition -- Định nghĩa:** Practice where code changes are automatically prepared for release to production. -- Thực hành mà các thay đổi code được tự động chuẩn bị để phát hành lên production.
- **Difference from CD -- Khác với CD:** Requires manual approval for production. -- Yêu cầu phê duyệt thủ công cho production.

## D-I

### Docker -- Docker
- **Definition -- Định nghĩa:** A platform for developing, shipping, and running applications in containers. -- Nền tảng để phát triển, vận chuyển và chạy ứng dụng trong containers.
- **Key concepts -- Khái niệm chính:**
  - Image: Read-only template -- Template chỉ đọc
  - Container: Running instance of image -- Instance đang chạy của image
  - Dockerfile: Build instructions -- Hướng dẫn build

### GitOps -- GitOps
- **Definition -- Định nghĩa:** Using Git as the single source of truth for declarative infrastructure. -- Sử dụng Git làm nguồn sự thật duy nhất cho infrastructure khai báo.
- **Principles -- Nguyên tắc:**
  - Declarative configuration -- Cấu hình khai báo
  - Version controlled -- Được quản lý phiên bản
  - Automated sync -- Đồng bộ tự động

### IaC (Infrastructure as Code -- Hạ tầng dưới dạng Mã)
- **Definition -- Định nghĩa:** Managing infrastructure through code instead of manual processes. -- Quản lý hạ tầng bằng code thay vì thao tác thủ công.
- **Tools -- Công cụ:** Terraform, CloudFormation, Pulumi
- **Benefits -- Lợi ích:**
  - Version control -- Quản lý phiên bản
  - Reproducibility -- Có thể tái tạo
  - Automation -- Tự động hóa

### Idempotent -- Bất biến
- **Definition -- Định nghĩa:** An operation that produces the same result regardless of how many times it's executed. -- Thao tác tạo ra kết quả giống nhau bất kể được thực thi bao nhiêu lần.
- **Example -- Ví dụ:** Running `terraform apply` multiple times gives same result. -- Chạy `terraform apply` nhiều lần cho kết quả giống nhau.

### Immutable Infrastructure -- Hạ tầng Bất biến
- **Definition -- Định nghĩa:** Infrastructure that is never modified after deployment; changes require replacement. -- Hạ tầng không bao giờ được sửa đổi sau khi deploy; thay đổi yêu cầu thay thế.
- **Benefits -- Lợi ích:**
  - Predictable deployments -- Triển khai có thể dự đoán
  - Easy rollbacks -- Dễ dàng rollback
  - No configuration drift -- Không bị lệch cấu hình

## K-P

### Kubernetes/K8s (Container Orchestration Platform -- Nền tảng Điều phối Container)
- **Definition -- Định nghĩa:** An open-source platform for automating deployment, scaling, and management of containerized applications. -- Nền tảng mã nguồn mở để tự động hóa triển khai, mở rộng và quản lý ứng dụng container.
- **Key concepts -- Khái niệm chính:**
  - Pod: Smallest deployable unit -- Đơn vị triển khai nhỏ nhất
  - Service: Network abstraction -- Trừu tượng hóa mạng
  - Deployment: Manages replicas -- Quản lý replicas

### Load Balancer -- Bộ Cân bằng Tải
- **Definition -- Định nghĩa:** Distributes network traffic across multiple servers. -- Phân phối traffic mạng qua nhiều servers.
- **Types -- Loại:**
  - L4: Transport layer (TCP/UDP) -- Tầng vận chuyển
  - L7: Application layer (HTTP) -- Tầng ứng dụng

### Microservices -- Kiến trúc Microservices
- **Definition -- Định nghĩa:** An architectural style where an application is composed of small, independent services. -- Kiến trúc mà ứng dụng được tạo thành từ các services nhỏ, độc lập.
- **Characteristics -- Đặc điểm:**
  - Loosely coupled -- Liên kết lỏng
  - Independently deployable -- Có thể deploy độc lập
  - Organized around business capabilities -- Tổ chức theo nghiệp vụ

### Monitoring -- Giám sát
- **Definition -- Định nghĩa:** Observing and tracking system performance and health. -- Quan sát và theo dõi hiệu suất và sức khỏe hệ thống.
- **Types -- Loại:**
  - Metrics: Numerical data -- Dữ liệu số
  - Logs: Event records -- Ghi chép sự kiện
  - Traces: Request flows -- Luồng request

### Orchestration -- Điều phối
- **Definition -- Định nghĩa:** Automated coordination of complex tasks and workflows. -- Phối hợp tự động các tác vụ và quy trình phức tạp.
- **Example -- Ví dụ:** Kubernetes orchestrates containers. -- Kubernetes điều phối containers.

### Pipeline -- Pipeline
- **Definition -- Định nghĩa:** A series of automated steps in CI/CD. -- Chuỗi các bước tự động trong CI/CD.
- **Stages -- Các giai đoạn:** Build → Test → Deploy → Monitor

### Pod -- Pod
- **Definition -- Định nghĩa:** The smallest deployable unit in Kubernetes, containing one or more containers. -- Đơn vị nhỏ nhất có thể triển khai trong Kubernetes, chứa một hoặc nhiều containers.
- **Features -- Đặc điểm:**
  - Shared network namespace -- Chia sẻ namespace mạng
  - Shared storage -- Chia sẻ storage
  - Co-located containers -- Containers cùng vị trí

### Provisioning -- Cấp phát
- **Definition -- Định nghĩa:** The process of setting up IT infrastructure. -- Quá trình thiết lập hạ tầng IT.
- **Types -- Loại:**
  - Server provisioning -- Cấp phát server
  - Network provisioning -- Cấp phát mạng
  - Storage provisioning -- Cấp phát storage

## R-Z

### Rollback -- Hoàn tác Triển khai
- **Definition -- Định nghĩa:** Reverting to a previous version when issues occur. -- Quay lại phiên bản trước đó khi có vấn đề.
- **Best practices -- Thực hành tốt:**
  - Keep previous versions -- Giữ các phiên bản trước
  - Automate rollback process -- Tự động hóa quy trình rollback
  - Test rollback procedures -- Kiểm thử quy trình rollback

### Rolling Update -- Cập nhật Cuốn chiếu
- **Definition -- Định nghĩa:** Gradually updating instances one at a time without downtime. -- Cập nhật từng instance một cách dần dần mà không có downtime.
- **How it works -- Cách hoạt động:** Replace old pods with new ones gradually. -- Thay thế pods cũ bằng pods mới dần dần.

### Scaling -- Mở rộng
- **Definition -- Định nghĩa:** Adjusting resources to handle varying loads. -- Điều chỉnh tài nguyên để xử lý tải thay đổi.
- **Types -- Loại:**
  - **Horizontal Scaling** -- Mở rộng ngang: Add/remove instances -- Thêm/bớt instances
  - **Vertical Scaling** -- Mở rộng dọc: Increase/decrease instance resources -- Tăng/giảm tài nguyên instance

### Service Discovery -- Khám phá Dịch vụ
- **Definition -- Định nghĩa:** Automatic detection of services in a network. -- Tự động phát hiện các services trong mạng.
- **Tools -- Công cụ:** Consul, etcd, CoreDNS

### Service Mesh -- Lưới Dịch vụ
- **Definition -- Định nghĩa:** An infrastructure layer for managing service-to-service communication. -- Lớp hạ tầng để quản lý giao tiếp giữa các services.
- **Tools -- Công cụ:** Istio, Linkerd, Consul Connect

### SRE (Site Reliability Engineering -- Kỹ thuật Độ tin cậy Hệ thống)
- **Definition -- Định nghĩa:** Applying software engineering practices to operations problems. -- Áp dụng các thực hành kỹ thuật phần mềm vào các vấn đề vận hành.
- **Key concepts -- Khái niệm chính:**
  - SLI/SLO/SLA
  - Error budgets -- Ngân sách lỗi
  - Toil reduction -- Giảm thiểu công việc thủ công

### Toil -- Công việc Thủ công
- **Definition -- Định nghĩa:** Manual, repetitive, automatable work related to running a production service. -- Công việc thủ công, lặp đi lặp lại, có thể tự động hóa liên quan đến vận hành dịch vụ production.
- **Goal -- Mục tiêu:** Minimize toil through automation. -- Giảm thiểu toil thông qua tự động hóa.

### Zero-Downtime Deployment -- Triển khai Không Gián đoạn
- **Definition -- Định nghĩa:** Deployment strategies that ensure no service interruption. -- Các chiến lược triển khai đảm bảo không gián đoạn dịch vụ.
- **Strategies -- Chiến lược:** Blue-green, Rolling update, Canary

---
