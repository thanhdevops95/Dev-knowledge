# Security Terms Dictionary -- Từ điển Thuật ngữ Bảo mật

> Security terminology from English to Vietnamese -- Thuật ngữ bảo mật từ tiếng Anh sang tiếng Việt

## 📋 Table of Contents -- Mục lục

- [Authentication & Authorization](#authentication--authorization) -- Xác thực và Phân quyền
- [Encryption](#encryption) -- Mã hóa
- [Threats & Attacks](#threats--attacks) -- Mối đe dọa và Tấn công
- [Defense](#defense) -- Phòng thủ
- [Compliance & Standards](#compliance--standards) -- Tuân thủ và Tiêu chuẩn
- [DevSecOps](#devsecops) -- DevSecOps

## Authentication & Authorization -- Xác thực và Phân quyền

### Authentication -- Xác thực
- **Definition -- Định nghĩa:** The process of verifying the identity of a user or system. -- Quá trình xác minh danh tính của người dùng hoặc hệ thống.
- **Methods -- Phương thức:**
  - Password -- Mật khẩu
  - MFA/2FA -- Xác thực đa yếu tố
  - Biometrics -- Sinh trắc học
  - OAuth/OIDC

### Authorization -- Phân quyền
- **Definition -- Định nghĩa:** The process of determining what a user can access. -- Quá trình xác định những gì người dùng có thể truy cập.
- **Models -- Mô hình:**
  - RBAC: Role-Based Access Control -- Kiểm soát truy cập dựa trên vai trò
  - ABAC: Attribute-Based Access Control -- Kiểm soát truy cập dựa trên thuộc tính
  - ACL: Access Control List -- Danh sách kiểm soát truy cập

### MFA/2FA (Multi-Factor Authentication -- Xác thực Đa yếu tố)
- **Definition -- Định nghĩa:** Requiring multiple verification factors to prove identity. -- Yêu cầu nhiều yếu tố xác minh để chứng minh danh tính.
- **Factors -- Yếu tố:**
  - Something you know -- Thứ bạn biết (password)
  - Something you have -- Thứ bạn có (phone, token)
  - Something you are -- Thứ bạn là (biometrics)

### OAuth (Open Authorization -- Ủy quyền Mở)
- **Definition -- Định nghĩa:** An open standard for access delegation. -- Tiêu chuẩn mở cho ủy quyền truy cập.
- **Use case -- Trường hợp dùng:** "Sign in with Google/Facebook" -- "Đăng nhập bằng Google/Facebook"

### JWT (JSON Web Token -- Token Web JSON)
- **Definition -- Định nghĩa:** A compact, self-contained token for securely transmitting information. -- Token nhỏ gọn, tự chứa để truyền thông tin an toàn.
- **Structure -- Cấu trúc:** Header.Payload.Signature

### SSO (Single Sign-On -- Đăng nhập Một lần)
- **Definition -- Định nghĩa:** Authentication that allows access to multiple systems with one login. -- Xác thực cho phép truy cập nhiều hệ thống với một lần đăng nhập.
- **Protocols -- Giao thức:** SAML, OAuth, OIDC

### LDAP (Lightweight Directory Access Protocol -- Giao thức Truy cập Thư mục Nhẹ)
- **Definition -- Định nghĩa:** Protocol for accessing and managing directory information. -- Giao thức truy cập và quản lý thông tin thư mục.
- **Use case -- Trường hợp dùng:** Centralized user management -- Quản lý người dùng tập trung

## Encryption -- Mã hóa

### Encryption -- Mã hóa
- **Definition -- Định nghĩa:** Converting data into an unreadable format to protect it. -- Chuyển đổi dữ liệu thành định dạng không đọc được để bảo vệ.
- **Types -- Loại:**
  - At rest -- Khi lưu trữ
  - In transit -- Khi truyền

### Symmetric Encryption -- Mã hóa Đối xứng
- **Definition -- Định nghĩa:** Using the same key for encryption and decryption. -- Sử dụng cùng một khóa để mã hóa và giải mã.
- **Algorithms -- Thuật toán:** AES, DES, 3DES

### Asymmetric Encryption -- Mã hóa Bất Đối xứng
- **Definition -- Định nghĩa:** Using a pair of public and private keys. -- Sử dụng cặp khóa công khai và riêng tư.
- **Algorithms -- Thuật toán:** RSA, ECC, DSA

### TLS/SSL (Transport Layer Security -- Bảo mật Tầng Vận chuyển)
- **Definition -- Định nghĩa:** Protocols for secure communication over networks. -- Giao thức cho giao tiếp an toàn qua mạng.
- **Use case -- Trường hợp dùng:** HTTPS, Secure email

### Certificate -- Chứng chỉ
- **Definition -- Định nghĩa:** A digital document that proves the identity of a website or entity. -- Tài liệu số chứng minh danh tính của website hoặc thực thể.
- **Types -- Loại:**
  - Self-signed -- Tự ký
  - CA-signed -- Được CA ký
  - Wildcard -- Wildcard

### PKI (Public Key Infrastructure -- Hạ tầng Khóa Công khai)
- **Definition -- Định nghĩa:** Framework for managing digital keys and certificates. -- Khung để quản lý khóa số và chứng chỉ.
- **Components -- Thành phần:** CA, RA, Certificates

### Hashing -- Băm
- **Definition -- Định nghĩa:** One-way conversion of data into a fixed-size string. -- Chuyển đổi một chiều dữ liệu thành chuỗi kích thước cố định.
- **Algorithms -- Thuật toán:** SHA-256, SHA-512, MD5 (deprecated), bcrypt

## Threats & Attacks -- Mối đe dọa và Tấn công

### Vulnerability -- Lỗ hổng
- **Definition -- Định nghĩa:** A weakness that can be exploited by attackers. -- Điểm yếu có thể bị kẻ tấn công khai thác.
- **Types -- Loại:** Software, Configuration, Human

### Exploit -- Khai thác
- **Definition -- Định nghĩa:** Code or technique that takes advantage of a vulnerability. -- Code hoặc kỹ thuật lợi dụng lỗ hổng.
- **Types -- Loại:** Zero-day, Known exploit

### Malware -- Phần mềm Độc hại
- **Definition -- Định nghĩa:** Software designed to damage or gain unauthorized access. -- Phần mềm được thiết kế để gây hại hoặc truy cập trái phép.
- **Types -- Loại:**
  - Virus -- Virus
  - Worm -- Sâu
  - Trojan -- Trojan
  - Ransomware -- Ransomware
  - Spyware -- Spyware

### DDoS (Distributed Denial of Service -- Từ chối Dịch vụ Phân tán)
- **Definition -- Định nghĩa:** Attack that overwhelms a system with traffic from multiple sources. -- Tấn công làm quá tải hệ thống với traffic từ nhiều nguồn.
- **Types -- Loại:** Volumetric, Protocol, Application layer

### SQL Injection -- Chèn SQL
- **Definition -- Định nghĩa:** Attack that injects malicious SQL code into queries. -- Tấn công chèn code SQL độc hại vào các truy vấn.
- **Prevention -- Phòng ngừa:** Parameterized queries, Input validation

### XSS (Cross-Site Scripting -- Tấn công Script Chéo)
- **Definition -- Định nghĩa:** Attack that injects malicious scripts into websites. -- Tấn công chèn scripts độc hại vào websites.
- **Types -- Loại:** Stored, Reflected, DOM-based

### CSRF (Cross-Site Request Forgery -- Giả mạo Yêu cầu Chéo)
- **Definition -- Định nghĩa:** Attack that tricks users into executing unwanted actions. -- Tấn công lừa người dùng thực hiện các hành động không mong muốn.
- **Prevention -- Phòng ngừa:** CSRF tokens, SameSite cookies

### Phishing -- Lừa đảo
- **Definition -- Định nghĩa:** Fraudulent attempt to obtain sensitive information. -- Nỗ lực gian lận để lấy thông tin nhạy cảm.
- **Types -- Loại:** Email phishing, Spear phishing, Whaling

### Man-in-the-Middle -- Tấn công Người đứng giữa
- **Definition -- Định nghĩa:** Attack where attacker intercepts communication between two parties. -- Tấn công mà kẻ tấn công chặn giao tiếp giữa hai bên.
- **Prevention -- Phòng ngừa:** TLS/SSL, Certificate pinning

## Defense -- Phòng thủ

### Firewall -- Tường lửa
- **Definition -- Định nghĩa:** Security system that monitors and controls network traffic. -- Hệ thống bảo mật giám sát và kiểm soát traffic mạng.
- **Types -- Loại:**
  - Network firewall -- Tường lửa mạng
  - WAF (Web Application Firewall) -- Tường lửa ứng dụng web
  - Host-based firewall -- Tường lửa dựa trên host

### IDS/IPS (Intrusion Detection/Prevention System -- Hệ thống Phát hiện/Ngăn chặn Xâm nhập)
- **Definition -- Định nghĩa:** Systems that detect and prevent network intrusions. -- Hệ thống phát hiện và ngăn chặn xâm nhập mạng.

### WAF (Web Application Firewall -- Tường lửa Ứng dụng Web)
- **Definition -- Định nghĩa:** Firewall that protects web applications from attacks. -- Tường lửa bảo vệ ứng dụng web khỏi các tấn công.
- **Protects against -- Bảo vệ khỏi:** SQL Injection, XSS, CSRF

### Zero Trust -- Không Tin tưởng
- **Definition -- Định nghĩa:** Security model that never trusts, always verifies. -- Mô hình bảo mật không bao giờ tin tưởng, luôn xác minh.
- **Principles -- Nguyên tắc:**
  - Verify explicitly -- Xác minh rõ ràng
  - Least privilege access -- Quyền truy cập tối thiểu
  - Assume breach -- Giả định bị xâm nhập

### Least Privilege -- Quyền Tối thiểu
- **Definition -- Định nghĩa:** Granting only the minimum access needed. -- Chỉ cấp quyền truy cập tối thiểu cần thiết.
- **Application -- Ứng dụng:** IAM policies, Container security

## Compliance & Standards -- Tuân thủ và Tiêu chuẩn

### SOC 2 (Service Organization Control 2 -- Kiểm soát Tổ chức Dịch vụ 2)
- **Definition -- Định nghĩa:** Framework for managing customer data based on five trust principles. -- Khung để quản lý dữ liệu khách hàng dựa trên năm nguyên tắc tin cậy.
- **Principles -- Nguyên tắc:** Security, Availability, Processing Integrity, Confidentiality, Privacy

### GDPR (General Data Protection Regulation -- Quy định Bảo vệ Dữ liệu Chung)
- **Definition -- Định nghĩa:** EU regulation for data protection and privacy. -- Quy định của EU về bảo vệ dữ liệu và quyền riêng tư.
- **Requirements -- Yêu cầu:** Consent, Data access, Right to be forgotten

### PCI-DSS (Payment Card Industry Data Security Standard -- Tiêu chuẩn Bảo mật Dữ liệu Ngành Thẻ)
- **Definition -- Định nghĩa:** Security standard for organizations handling credit cards. -- Tiêu chuẩn bảo mật cho tổ chức xử lý thẻ tín dụng.

### HIPAA (Health Insurance Portability and Accountability Act -- Đạo luật Bảo mật Thông tin Y tế)
- **Definition -- Định nghĩa:** US law for protecting health information. -- Luật Mỹ bảo vệ thông tin sức khỏe.

## DevSecOps -- DevSecOps

### DevSecOps (Development Security Operations -- Phát triển Bảo mật Vận hành)
- **Definition -- Định nghĩa:** Integrating security into the DevOps pipeline. -- Tích hợp bảo mật vào pipeline DevOps.
- **Principle -- Nguyên tắc:** Security as code, Shift left

### Shift Left -- Dịch trái
- **Definition -- Định nghĩa:** Moving security earlier in the development cycle. -- Chuyển bảo mật sớm hơn trong chu trình phát triển.
- **Practice -- Thực hành:** Early testing, Security in CI/CD

### SAST (Static Application Security Testing -- Kiểm thử Bảo mật Ứng dụng Tĩnh)
- **Definition -- Định nghĩa:** Analyzing source code for vulnerabilities without running it. -- Phân tích mã nguồn để tìm lỗ hổng mà không chạy nó.
- **Tools -- Công cụ:** SonarQube, Checkmarx, Fortify

### DAST (Dynamic Application Security Testing -- Kiểm thử Bảo mật Ứng dụng Động)
- **Definition -- Định nghĩa:** Testing running applications for vulnerabilities. -- Kiểm thử ứng dụng đang chạy để tìm lỗ hổng.
- **Tools -- Công cụ:** OWASP ZAP, Burp Suite

### Secret Management -- Quản lý Bí mật
- **Definition -- Định nghĩa:** Securely storing and accessing sensitive data like passwords and API keys. -- Lưu trữ và truy cập an toàn dữ liệu nhạy cảm như mật khẩu và API keys.
- **Tools -- Công cụ:** HashiCorp Vault, AWS Secrets Manager, Azure Key Vault

### Container Security -- Bảo mật Container
- **Definition -- Định nghĩa:** Protecting containers from threats throughout their lifecycle. -- Bảo vệ containers khỏi các mối đe dọa trong suốt vòng đời của chúng.
- **Practices -- Thực hành:**
  - Image scanning -- Quét image
  - Runtime protection -- Bảo vệ thời gian chạy
  - Least privilege -- Quyền tối thiểu

---
