🏛️ ĐẶC TẢ GIÁO TRÌNH: DEVOPS ZERO TO HERO (MASTER BLUEPRINT)

1. NGUYÊN TẮC CỐT LÕI (CORE PRINCIPLES)

AI bắt buộc phải tuân thủ các nguyên tắc sau khi tạo nội dung:

Ngôn ngữ: Tiếng Việt. Phong cách trực diện, gãy gọn, không văn hoa ("No fluff").

- Tất cả văn bản giải thích, hướng dẫn sang tiếng Việt
- Code, command, tool names có thể giữ nguyên (vd: git push, docker build)
- Technical headers trong code blocks (vd: "Problems:", "Root cause:") có thể giữ hoặc dịch

Giải thích thuật ngữ: Với mỗi từ chuyên ngành hoặc từ viết tắt xuất hiện lần đầu, BẮT BUỘC dùng định dạng:

Từ viết tắt (Tiếng Anh đầy đủ - Nghĩa tiếng Việt)
Ví dụ: CI (Continuous Integration - Tích hợp liên tục)

Phương pháp Ẩn dụ (Metaphor): Khi giải thích khái niệm trừu tượng, BẮT BUỘC phải có một ví dụ so sánh đời thường.

Ví dụ: "Docker Container giống như hộp cơm trưa. Bạn nấu ở nhà (Dev), đóng hộp lại, mang lên công ty (Server) mở ra ăn thì vị vẫn y hệt, không bị ảnh hưởng bởi môi trường bên ngoài."

Dự án xuyên suốt: "The Counter App"

App: Python Flask (Web đơn giản).

DB: Redis (Lưu số đếm).

2. CẤU TRÚC THƯ MỤC BẮT BUỘC

AI phải tạo chính xác cấu trúc sau:

/devops-course
│── 00_GIOI_THIEU.md            (Lộ trình & Cài đặt môi trường)
│── /source-code                (Code mẫu Python & Redis hoàn chỉnh)
│── /01_PLAN                    (Module 1)
│   ├── REQUIREMENT.md          (Yêu cầu & Tiêu chí nghiệm thu)
│   ├── README.md               (Lý thuyết & Ẩn dụ)
│   ├── LABS.md                 (Bài tập thực hành từng bước)
│   └── SCENARIOS.md            (5 Tình huống giải quyết sự cố)
│── /02_BUILD                   (Module 2 - Cấu trúc y hệt trên)
│── /03_CI                      (Module 3 - Cấu trúc y hệt trên)
│── /04_CD                      (Module 4 - Cấu trúc y hệt trên)
│── /05_OPERATE                 (Module 5 - Cấu trúc y hệt trên)
│── /06_MONITOR                 (Module 6 - Cấu trúc y hệt trên)
│── /07_FEEDBACK                (Module 7 - Cấu trúc y hệt trên)

3. QUY ĐỊNH NỘI DUNG TỪNG FILE

A. REQUIREMENT.md (Đề bài)

Đây là tờ hướng dẫn nhiệm vụ. Phải bao gồm:

Mục tiêu: Học được gì?

Danh sách thuật ngữ: Bảng các từ viết tắt sẽ dùng trong bài.

Checklist bài tập: Các việc cần làm (Ví dụ: Cài Docker, Viết Dockerfile).

Checklist tình huống: Danh sách 5 sự cố cần giải quyết.

B. README.md (Lý thuyết & Tư duy)

Giải thích khái niệm bằng ngôn ngữ bình dân + Ẩn dụ.

Dùng Mermaid Diagram để vẽ sơ đồ luồng đi.

Luôn trả lời câu hỏi: "Tại sao tôi phải dùng cái này?" trước khi chỉ cách dùng.

C. LABS.md (Thực hành)

Hướng dẫn từng bước (Step-by-step).

Code mẫu phải tường minh, có comment giải thích từng dòng lệnh quan trọng.

Có ảnh minh họa hoặc text mô tả kết quả đầu ra (Expected Output).

D. SCENARIOS.md (Tình huống thực chiến - QUAN TRỌNG)

Mỗi Module phải có đúng 5 Tình huống (Scenarios) theo format sau:

🚨 Bối cảnh (Context): Mô tả triệu chứng lỗi (Ví dụ: Web sập, Build chậm).

🕵️ Điều tra (Investigation): Dùng công cụ gì để tìm nguyên nhân?

💡 Giải pháp (Solution): Cách sửa lỗi triệt để.

🧠 Bài học (Key Takeaway): Rút kinh nghiệm.

4. CHI TIẾT 7 MODULE

01_PLAN: Tư duy DevOps, Agile, Cấu trúc dự án. (Ẩn dụ: Xây nhà cần bản vẽ).

02_BUILD: Git, Docker, Containerization. (Ẩn dụ: Đóng gói hành lý).

03_CI: GitHub Actions, Tự động test. (Ẩn dụ: Dây chuyền kiểm tra chất lượng nhà máy).

04_CD: Kubernetes, ArgoCD, Deploy. (Ẩn dụ: Người điều phối giao thông/Bến cảng).

05_OPERATE: Terraform (IaC), Ansible. (Ẩn dụ: Robot xây dựng tự động).

06_MONITOR: Prometheus, Grafana, Logs. (Ẩn dụ: Bảng điều khiển máy bay/Khám sức khỏe).

07_FEEDBACK: ChatOps, Alerting, Post-mortem. (Ẩn dụ: Hệ thống báo cháy & Họp rút kinh nghiệm).
