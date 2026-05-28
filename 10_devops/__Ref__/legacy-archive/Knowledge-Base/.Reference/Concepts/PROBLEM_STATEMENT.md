# Đề Bài: Hệ Thống 2 App Microservices (Python & Go)

## 1. Giới thiệu
Xây dựng một hệ thống mô phỏng kiến trúc microservices đơn giản gồm 2 dịch vụ giao tiếp với nhau. Mục tiêu là hiểu rõ luồng dữ liệu, cách các dịch vụ gọi nhau qua mạng, và cách đóng gói, triển khai ứng dụng từ môi trường "bare-metal" (chạy trực tiếp) lên Docker container và cuối cùng là giải quyết vấn đề lưu trữ dữ liệu.

## 2. Kiến trúc hệ thống

Hệ thống bao gồm 2 ứng dụng riêng biệt:

### App 1: Python Service (Gateway/Frontend)
- **Vai trò:** Là cổng giao tiếp chính với người dùng (User Interface/API Gateway).
- **Nghiệp vụ:**
  - Nhận yêu cầu từ người dùng (User).
  - Gửi yêu cầu (Ping) sang **App 2**.
  - Nhận phản hồi và trả kết quả về cho người dùng.
- **Yêu cầu kỹ thuật:** Sử dụng Python (Flask/FastAPI/Django...).

### App 2: Go Service (Backend/Processor)
- **Vai trò:** Xử lý logic nghiệp vụ và lưu trữ trạng thái.
- **Nghiệp vụ:**
  - Cung cấp HTTP API để App 1 gọi sang (Ping).
  - Có 2 API chính:
    1. **Ghi (Ping):** Nhận tín hiệu ping, ghi nhận vào bộ nhớ. Trả về "Pong" nếu thành công.
    2. **Đọc (Stats):** Trả về thống kê số lần ping thành công/thất bại.
  - **Lưu trữ:** Mặc định lưu database trong RAM (biến toàn cục).
    - *Vấn đề:* Khi tắt ứng dụng hoặc restart docker, dữ liệu RAM sẽ mất.
    - *Option:* Có thể mở rộng để lưu xuống File System.
- **Bảo mật:** Không cho phép người dùng cuối gọi trực tiếp (Frontend <---> Go), chỉ chấp nhận gọi từ App 1 hoặc curl nội bộ.

## 3. Các bước thực hiện (Milestones)

### Giai đoạn 1: Chạy trực tiếp (Bare Metal)
- Viết code cho 2 App.
- Chạy thủ công bằng lệnh `python app.py` và `go run main.go`.
- Kiểm tra kết nối giữa 2 App trên `localhost`.

### Giai đoạn 2: Đóng gói Docker (Containerization)
- Viết `Dockerfile` cho từng App.
- Build Docker Image riêng biệt cho 2 App.
- Chạy 2 container và cấu hình mạng (Docker Network) để chúng nhìn thấy nhau.

### Giai đoạn 3: Persisting Data (Volumes)
- **Vấn đề:** Khi kill container Go hoặc update image mới, dữ liệu đếm trong RAM bị mất.
- **Giải pháp:** Cấu hình Docker Volume để map dữ liệu từ trong container ra máy thật (Host Machine), đảm bảo dữ liệu tồn tại qua vòng đời container.

### Giai đoạn 4: CI/CD & Deployment (Nâng cao)
- Tự động hóa quy trình build image.
- Mô phỏng việc pull image về và chạy trên môi trường server khác.

## 4. Yêu cầu đầu ra
- Source code hoàn chỉnh của 2 App.
- Dockerfile tối ưu cho từng ngôn ngữ.
- Các câu lệnh dùng để build, run, debug.
- Giải thích chi tiết ý nghĩa từng lệnh.
