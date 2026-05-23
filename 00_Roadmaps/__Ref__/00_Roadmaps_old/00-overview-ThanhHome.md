# 🗺️ Tổng quan — Ngành Phát triển Phần mềm & Cách sử dụng kho Dev-Knowledge

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Điểm xuất phát cho mọi người

---

## Ngành phát triển phần mềm là gì?

Phát triển phần mềm (Software Development) là quá trình thiết kế, xây dựng và vận hành các ứng dụng, hệ thống và dịch vụ số — từ app trên điện thoại, website thương mại điện tử, đến hệ thống ngân hàng xử lý hàng triệu giao dịch mỗi ngày. Đây là một trong những ngành có nhu cầu nhân lực lớn nhất và liên tục phát triển, nơi bạn giải quyết các bài toán thực tế bằng code.

Hãy hình dung xây phần mềm giống xây một tòa nhà: cần kiến trúc sư (Architect) vẽ bản thiết kế, thợ xây (Developer) dựng từng phần, thợ điện nước (DevOps) đảm bảo hệ thống chạy ổn, và người kiểm định chất lượng (QA). Trong phần mềm, Frontend lo giao diện người dùng nhìn thấy, Backend xử lý logic phía sau, DevOps vận hành hạ tầng, còn Data/AI biến dữ liệu thành giá trị. Mỗi vai trò đều quan trọng, và bạn có thể chọn hướng phù hợp nhất với mình.

---

## Các vai trò phổ biến

| Vai trò | Công việc chính | Kỹ năng cần | Lộ trình |
|---|---|---|---|
| **Frontend** | Xây giao diện web, tương tác người dùng | HTML, CSS, JS, React/Vue | [frontend-roadmap](./frontend-roadmap.md) |
| **Backend** | Xây API, xử lý logic, quản lý database | Python/Node/Go/Java, SQL, REST | [backend-roadmap](./backend-roadmap.md) |
| **Fullstack** | Làm cả Frontend lẫn Backend | Kết hợp FE + BE | [fullstack-roadmap](./fullstack-roadmap.md) |
| **DevOps** | CI/CD, hạ tầng, monitoring, tự động hóa | Docker, K8s, Terraform, Linux | [devops-roadmap](./devops-roadmap.md) |
| **Data Engineer** | Pipeline dữ liệu, ETL, data warehouse | SQL, Python, Spark, Airflow | [data-engineer-roadmap](./data-engineer-roadmap.md) |
| **AI / ML** | Huấn luyện model, NLP, Computer Vision | Python, PyTorch, Math, Statistics | [ai-ml-roadmap](./ai-ml-roadmap.md) |
| **Mobile** | App iOS / Android / cross-platform | Swift, Kotlin, React Native, Flutter | [mobile-roadmap](./mobile-roadmap.md) |
| **QA / Testing** | Kiểm thử chất lượng, automation test | Selenium, Playwright, test strategy | [qa-roadmap](./qa-roadmap.md) |
| **Security** | Bảo mật ứng dụng, pentest, compliance | OWASP, cryptography, network security | [security-roadmap](./security-roadmap.md) |
| **Blockchain / Game / Embedded** | Smart contract, game engine, firmware | Solidity, Unity, C/C++, IoT | [blockchain](./blockchain-roadmap.md) · [game](./game-dev-roadmap.md) · [embedded](./embedded-iot-roadmap.md) |

---

## Kiến thức nền tảng — Bắt buộc cho MỌI vai trò

Dù bạn chọn hướng nào, 5 kỹ năng sau là **không thể bỏ qua**:

- [ ] **Git & GitHub** — Quản lý phiên bản code → [git basics](../02-Version%20Control/git/01-git-basics.md)
- [ ] **Terminal / Command Line** — Làm việc hiệu quả với máy tính → [terminal basics](../03-Terminal%20%26%20OS/terminal/01-terminal-basics.md)
- [ ] **Networking (HTTP, DNS)** — Hiểu cách Internet hoạt động → [http fundamentals](../04-Networking/01-http-fundamentals.md)
- [ ] **DSA cơ bản** — Tư duy giải quyết vấn đề → [dsa fundamentals](../01-CS-Fundamentals/dsa/01-dsa-fundamentals.md)
- [ ] **Hệ điều hành** — Process, thread, memory → [os concepts](../01-CS-Fundamentals/cs/02-os-concepts-fundamentals.md)

---

## Lộ trình gợi ý theo mục tiêu

| Nếu bạn muốn... | Bắt đầu từ... | Roadmap |
|---|---|---|
| Làm website đẹp, tương tác | HTML → CSS → JS → React | [frontend-roadmap](./frontend-roadmap.md) |
| Xây API, xử lý dữ liệu | Python/Node → REST → SQL | [backend-roadmap](./backend-roadmap.md) |
| Làm được cả FE lẫn BE | Frontend cơ bản → Backend → Kết hợp | [fullstack-roadmap](./fullstack-roadmap.md) |
| Tự động hóa hạ tầng, deploy | Linux → Docker → K8s → CI/CD | [devops-roadmap](./devops-roadmap.md) |
| Làm việc với dữ liệu lớn | SQL → Python → ETL pipeline | [data-engineer-roadmap](./data-engineer-roadmap.md) |
| Huấn luyện AI / ML model | Math → Python → PyTorch/TF | [ai-ml-roadmap](./ai-ml-roadmap.md) |
| Phát triển app mobile | Dart/Swift/Kotlin → Framework | [mobile-roadmap](./mobile-roadmap.md) |
| Kiểm thử & chất lượng | Test fundamentals → Automation | [qa-roadmap](./qa-roadmap.md) |
| Bảo mật hệ thống | Web security → OWASP → Pentest | [security-roadmap](./security-roadmap.md) |
| Blockchain / Web3 | Cryptography → Solidity → DApps | [blockchain-roadmap](./blockchain-roadmap.md) |
| Phát triển game | C# → Unity / C++ → Unreal | [game-dev-roadmap](./game-dev-roadmap.md) |
| Embedded / IoT | C/C++ → Microcontroller → RTOS | [embedded-iot-roadmap](./embedded-iot-roadmap.md) |

---

## Cách sử dụng kho Dev-Knowledge

1. **Đọc file này trước** — nắm bức tranh toàn cảnh và chọn hướng đi
2. **Chọn roadmap → học theo thứ tự** — mỗi roadmap chia giai đoạn rõ ràng, đi từ cơ bản đến nâng cao
3. **Xem level badge để ưu tiên** — bài có `[BEGINNER]` đọc trước, `[ADVANCED]` đọc sau
4. **Dùng suffix để chọn loại bài** — `-basics` để học lý thuyết, `-cheatsheet` để tra cứu nhanh, `-examples` để xem code thực tế, `-practices` để học best practice

---

## Nguyên tắc học hiệu quả

🔨 **Học qua làm** — Đọc xong mỗi bài → code ngay, đừng chỉ đọc lý thuyết suông
🧱 **Nền tảng trước, framework sau** — Hiểu JS rồi hãy học React, hiểu HTTP rồi hãy xây API
🔁 **Lặp lại theo chu kỳ** — Quay lại ôn kiến thức cũ, mỗi lần hiểu sâu hơn
📐 **Xây project thực tế** — Portfolio dự án > bằng cấp chứng chỉ
🤝 **Học cùng cộng đồng** — Tham gia open-source, code review, chia sẻ kiến thức

---

## Sơ đồ tổng quan

```
                           🗺️ BẮT ĐẦU TỪ ĐÂY
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                             ▼
             Kiến thức nền               Chọn ngôn ngữ
          (Git, Terminal, HTTP,        (Python, JS, Go,
           DSA, OS concepts)           Java, C#, ...)
                    │                             │
                    └─────────────┬───────────────┘
                                  ▼
                        Chọn hướng chuyên môn
                                  │
          ┌──────┬──────┬─────────┼─────────┬──────┬──────┐
          ▼      ▼      ▼         ▼         ▼      ▼      ▼
        🎨     ⚙️     🚀       📊       🤖     📱    🔒
       Front   Back   DevOps   Data     AI/ML  Mobile  Sec
       end     end             Eng                     tic
```

---

## Tài nguyên bên ngoài

- [roadmap.sh](https://roadmap.sh) — Lộ trình trực quan cho mọi vai trò
- [freeCodeCamp](https://www.freecodecamp.org) — Học lập trình miễn phí với project thực hành
- [The Odin Project](https://www.theodinproject.com) — Fullstack curriculum mã nguồn mở
- [CS50 — Harvard](https://cs50.harvard.edu/x/) — Khóa nhập môn Computer Science nổi tiếng nhất
