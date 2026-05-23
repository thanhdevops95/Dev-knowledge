# Cloud Terms Dictionary -- Từ điển Thuật ngữ Cloud

> Cloud computing terminology from English to Vietnamese -- Thuật ngữ điện toán đám mây từ tiếng Anh sang tiếng Việt

## 📋 Table of Contents -- Mục lục

- [Cloud Models](#cloud-models) -- Mô hình Cloud
- [Cloud Services](#cloud-services) -- Dịch vụ Cloud
- [Compute](#compute) -- Tính toán
- [Storage](#storage) -- Lưu trữ
- [Networking](#networking) -- Mạng
- [Database](#database) -- Cơ sở dữ liệu
- [Security & Identity](#security--identity) -- Bảo mật và Danh tính
- [Monitoring & Management](#monitoring--management) -- Giám sát và Quản lý

## Cloud Models -- Mô hình Cloud

### Public Cloud -- Đám mây Công cộng
- **Definition -- Định nghĩa:** Cloud infrastructure shared among multiple organizations. -- Hạ tầng cloud được chia sẻ giữa nhiều tổ chức.
- **Providers -- Nhà cung cấp:** AWS, Azure, GCP

### Private Cloud -- Đám mây Riêng
- **Definition -- Định nghĩa:** Cloud infrastructure dedicated to a single organization. -- Hạ tầng cloud dành riêng cho một tổ chức.
- **Use case -- Trường hợp dùng:** High security requirements -- Yêu cầu bảo mật cao

### Hybrid Cloud -- Đám mây Lai
- **Definition -- Định nghĩa:** Combination of public and private clouds. -- Kết hợp đám mây công cộng và riêng.
- **Benefit -- Lợi ích:** Flexibility and control -- Linh hoạt và kiểm soát

### Multi-Cloud -- Đa Đám mây
- **Definition -- Định nghĩa:** Using multiple cloud providers simultaneously. -- Sử dụng nhiều nhà cung cấp cloud cùng lúc.
- **Benefit -- Lợi ích:** Avoid vendor lock-in -- Tránh phụ thuộc nhà cung cấp

## Cloud Services -- Dịch vụ Cloud

### IaaS (Infrastructure as a Service -- Hạ tầng dưới dạng Dịch vụ)
- **Definition -- Định nghĩa:** Cloud provider manages physical infrastructure; customer manages OS and above. -- Nhà cung cấp cloud quản lý hạ tầng vật lý; khách hàng quản lý OS trở lên.
- **Examples -- Ví dụ:** EC2, Azure VMs, Google Compute Engine
- **Customer manages -- Khách hàng quản lý:** OS, Middleware, Applications, Data

### PaaS (Platform as a Service -- Nền tảng dưới dạng Dịch vụ)
- **Definition -- Định nghĩa:** Cloud provider manages infrastructure and platform; customer manages applications. -- Nhà cung cấp cloud quản lý hạ tầng và nền tảng; khách hàng quản lý ứng dụng.
- **Examples -- Ví dụ:** Heroku, AWS Elastic Beanstalk, Google App Engine
- **Customer manages -- Khách hàng quản lý:** Applications, Data

### SaaS (Software as a Service -- Phần mềm dưới dạng Dịch vụ)
- **Definition -- Định nghĩa:** Cloud provider manages everything; customer uses the software. -- Nhà cung cấp cloud quản lý mọi thứ; khách hàng sử dụng phần mềm.
- **Examples -- Ví dụ:** Gmail, Salesforce, Slack, Zoom
- **Customer manages -- Khách hàng quản lý:** Data, User settings

### FaaS (Function as a Service -- Hàm dưới dạng Dịch vụ)
- **Definition -- Định nghĩa:** Serverless compute that runs code in response to events. -- Tính toán serverless chạy code để phản hồi các sự kiện.
- **Examples -- Ví dụ:** AWS Lambda, Azure Functions, Google Cloud Functions

## Compute -- Tính toán

### EC2 (Elastic Compute Cloud -- Đám mây Tính toán Đàn hồi)
- **Definition -- Định nghĩa:** AWS virtual server service. -- Dịch vụ máy chủ ảo của AWS.
- **Features -- Tính năng:** Scalable, Various instance types -- Có thể mở rộng, Nhiều loại instance

### Instance -- Phiên bản Máy chủ
- **Definition -- Định nghĩa:** A virtual server in the cloud. -- Máy chủ ảo trong cloud.
- **Types -- Loại:** General purpose, Compute optimized, Memory optimized

### Auto Scaling -- Tự động Mở rộng
- **Definition -- Định nghĩa:** Automatically adjusting compute resources based on demand. -- Tự động điều chỉnh tài nguyên tính toán dựa trên nhu cầu.
- **Types -- Loại:**
  - Horizontal: Add/remove instances -- Thêm/bớt instances
  - Vertical: Resize instances -- Thay đổi kích thước instances

### Serverless -- Không máy chủ
- **Definition -- Định nghĩa:** Cloud model where provider manages servers automatically. -- Mô hình cloud mà nhà cung cấp quản lý servers tự động.
- **Benefits -- Lợi ích:** No server management, Pay per use -- Không quản lý server, Trả theo sử dụng

### Spot Instance -- Instance Spot
- **Definition -- Định nghĩa:** Unused cloud capacity available at discounted rates. -- Dung lượng cloud không sử dụng có sẵn với giá giảm.
- **Use case -- Trường hợp dùng:** Batch processing, Fault-tolerant workloads -- Xử lý batch, Workloads chịu lỗi

## Storage -- Lưu trữ

### S3 (Simple Storage Service -- Dịch vụ Lưu trữ Đơn giản)
- **Definition -- Định nghĩa:** AWS object storage service. -- Dịch vụ lưu trữ đối tượng của AWS.
- **Storage classes -- Lớp lưu trữ:** Standard, IA, Glacier

### Object Storage -- Lưu trữ Đối tượng
- **Definition -- Định nghĩa:** Storage architecture that manages data as objects. -- Kiến trúc lưu trữ quản lý dữ liệu như các đối tượng.
- **Use case -- Trường hợp dùng:** Static files, Backups, Media -- Files tĩnh, Sao lưu, Media

### Block Storage -- Lưu trữ Khối
- **Definition -- Định nghĩa:** Storage that manages data in fixed-size blocks. -- Lưu trữ quản lý dữ liệu trong các khối kích thước cố định.
- **Examples -- Ví dụ:** EBS, Azure Managed Disks

### File Storage -- Lưu trữ File
- **Definition -- Định nghĩa:** Storage that organizes data as files and folders. -- Lưu trữ tổ chức dữ liệu như files và thư mục.
- **Examples -- Ví dụ:** EFS, Azure Files, Google Filestore

### CDN (Content Delivery Network -- Mạng Phân phối Nội dung)
- **Definition -- Định nghĩa:** Distributed servers that deliver content to users based on their location. -- Các servers phân tán phân phối nội dung đến users dựa trên vị trí của họ.
- **Examples -- Ví dụ:** CloudFront, Azure CDN, Cloudflare

## Networking -- Mạng

### VPC (Virtual Private Cloud -- Đám mây Riêng Ảo)
- **Definition -- Định nghĩa:** Isolated virtual network within the cloud. -- Mạng ảo cô lập trong cloud.
- **Components -- Thành phần:** Subnets, Route tables, Internet gateway

### Subnet -- Mạng con
- **Definition -- Định nghĩa:** A range of IP addresses within a VPC. -- Một dải địa chỉ IP trong VPC.
- **Types -- Loại:** Public subnet, Private subnet -- Subnet công cộng, Subnet riêng

### Load Balancer -- Bộ Cân bằng Tải
- **Definition -- Định nghĩa:** Distributes traffic across multiple servers. -- Phân phối traffic qua nhiều servers.
- **Types -- Loại:**
  - ALB: Application (L7) -- Tầng ứng dụng
  - NLB: Network (L4) -- Tầng mạng
  - CLB: Classic -- Cổ điển

### NAT Gateway -- Cổng NAT
- **Definition -- Định nghĩa:** Allows private subnet resources to access the internet. -- Cho phép tài nguyên subnet riêng truy cập internet.
- **Use case -- Trường hợp dùng:** Private instances needing internet access -- Instances riêng cần truy cập internet

## Database -- Cơ sở Dữ liệu

### RDS (Relational Database Service -- Dịch vụ CSDL Quan hệ)
- **Definition -- Định nghĩa:** Managed relational database service. -- Dịch vụ cơ sở dữ liệu quan hệ được quản lý.
- **Engines -- Engines:** MySQL, PostgreSQL, Oracle, SQL Server

### NoSQL Database -- Cơ sở Dữ liệu NoSQL
- **Definition -- Định nghĩa:** Non-relational database for flexible data models. -- Cơ sở dữ liệu phi quan hệ cho các mô hình dữ liệu linh hoạt.
- **Types -- Loại:** Document, Key-value, Graph, Wide-column

### DynamoDB -- DynamoDB
- **Definition -- Định nghĩa:** AWS managed NoSQL database. -- Cơ sở dữ liệu NoSQL được quản lý của AWS.
- **Features -- Tính năng:** Serverless, Scalable, Low latency

### ElastiCache -- ElastiCache
- **Definition -- Định nghĩa:** Managed in-memory caching service. -- Dịch vụ cache trong bộ nhớ được quản lý.
- **Engines -- Engines:** Redis, Memcached

## Security & Identity -- Bảo mật và Danh tính

### IAM (Identity and Access Management -- Quản lý Danh tính và Truy cập)
- **Definition -- Định nghĩa:** Service for managing access to cloud resources. -- Dịch vụ quản lý truy cập vào tài nguyên cloud.
- **Components -- Thành phần:** Users, Groups, Roles, Policies

### Security Group -- Nhóm Bảo mật
- **Definition -- Định nghĩa:** Virtual firewall for controlling inbound and outbound traffic. -- Tường lửa ảo để kiểm soát traffic vào và ra.
- **Behavior -- Hành vi:** Stateful -- Có trạng thái

### KMS (Key Management Service -- Dịch vụ Quản lý Khóa)
- **Definition -- Định nghĩa:** Managed service for creating and managing encryption keys. -- Dịch vụ được quản lý để tạo và quản lý khóa mã hóa.
- **Use case -- Trường hợp dùng:** Data encryption at rest -- Mã hóa dữ liệu lưu trữ

## Monitoring & Management -- Giám sát và Quản lý

### CloudWatch -- CloudWatch
- **Definition -- Định nghĩa:** AWS monitoring and observability service. -- Dịch vụ giám sát và quan sát của AWS.
- **Features -- Tính năng:** Metrics, Logs, Alarms, Dashboards

### CloudTrail -- CloudTrail
- **Definition -- Định nghĩa:** AWS service that logs API calls. -- Dịch vụ AWS ghi lại các cuộc gọi API.
- **Use case -- Trường hợp dùng:** Audit, Compliance -- Kiểm toán, Tuân thủ

### Tags -- Tags
- **Definition -- Định nghĩa:** Key-value pairs for organizing and managing cloud resources. -- Cặp key-value để tổ chức và quản lý tài nguyên cloud.
- **Use case -- Trường hợp dùng:** Cost allocation, Resource organization -- Phân bổ chi phí, Tổ chức tài nguyên

### Region -- Vùng
- **Definition -- Định nghĩa:** Geographic area containing multiple data centers. -- Khu vực địa lý chứa nhiều trung tâm dữ liệu.
- **Example -- Ví dụ:** us-east-1, ap-southeast-1

### Availability Zone -- Vùng Sẵn sàng
- **Definition -- Định nghĩa:** Isolated data center within a region. -- Trung tâm dữ liệu cô lập trong một vùng.
- **Purpose -- Mục đích:** High availability, Fault tolerance -- Tính sẵn sàng cao, Chịu lỗi

---
