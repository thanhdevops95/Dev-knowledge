# 🏛️ Module 3.6: System Design & Reliability

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Building Reliable Systems** - High Availability, Scalability, Disaster Recovery.
>
> *Xây dựng hệ thống đáng tin cậy - Tính sẵn sàng cao, Khả năng mở rộng, Khắc phục thảm họa.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Implement High Availability patterns (Triển khai mẫu HA)
- ✅ Design Scalability strategies (Thiết kế chiến lược mở rộng)
- ✅ Plan Disaster Recovery (Lập kế hoạch DR)
- ✅ Perform Capacity planning (Quy hoạch dung lượng)
- ✅ Understand SLAs, SLOs, SLIs (Hiểu SLAs, SLOs, SLIs)
- ✅ Learn Chaos Engineering basics (Tìm hiểu Chaos Engineering)

---

## 📚 Content (Nội dung)

### 1. Why Reliability Matters? (Tại sao Reliability quan trọng?)

In DevOps, you don't just deploy applications - you must ensure they are **always available** when users need them.

*Trong DevOps, bạn không chỉ deploy ứng dụng - bạn phải đảm bảo nó **luôn hoạt động** khi người dùng cần.*

#### Cost of Downtime (Chi phí của Downtime)

| System Type | Cost per minute | Example |
|-------------|-----------------|----------|
| Large E-commerce | $100,000+ | Amazon loses ~$13 million/min |
| Banking | $10,000+ | Transactions interrupted |
| SaaS B2B | $1,000+ | Customer churn |
| Internal tools | $100+ | Productivity loss |

**Conclusion:** Investing in reliability is not a cost - it's saving costs!

*Kết luận: Đầu tư vào reliability không phải là chi phí - nó là tiết kiệm chi phí!*

---

### 2. HA Patterns (Mẫu High Availability)

**High Availability (HA)** ensures the system continues operating when components fail. Principle: **Eliminate Single Points of Failure**.

*HA đảm bảo hệ thống tiếp tục hoạt động khi có thành phần bị lỗi. Nguyên tắc: Loại bỏ điểm lỗi đơn lẻ.*

```
┌─────────────────────────────────────────┐
│           Load Balancer                  │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐    ┌───▼───┐    ┌───▼───┐
│ App 1 │    │ App 2 │    │ App 3 │
│ (AZ-a)│    │ (AZ-b)│    │ (AZ-c)│
└───────┘    └───────┘    └───────┘
```

**Giải thích:** Nếu App 1 hoặc toàn bộ AZ-a chết, Load Balancer tự động chuyển traffic sang App 2 và 3.

---

### 3. Scaling (Mở rộng)

| Loại | Mô tả | Ưu điểm | Nhược điểm |
|------|-------|---------|------------|
| **Vertical** | Máy mạnh hơn (upgrade CPU/RAM) | Đơn giản | Có giới hạn, downtime khi upgrade |
| **Horizontal** | Nhiều máy hơn | Vô tận, không downtime | Phức tạp hơn (stateless required) |
| **Auto Scaling** | Tự động thêm/bớt theo metrics | Tiết kiệm chi phí | Cần tune cẩn thận |

---

### 4. DR Strategies (Chiến lược Disaster Recovery)

| Strategy (Chiến lược) | RTO | RPO | Cost (Chi phí) |
|-----------------------|-----|-----|----------------|
| Backup/Restore (Sao lưu) | Hours (Giờ) | Hours (Giờ) | $ |
| Pilot Light | Minutes (Phút) | Minutes (Phút) | $$ |
| Warm Standby | Minutes (Phút) | Seconds (Giây) | $$$ |
| Active-Active | Zero (Không) | Zero (Không) | $$$$ |

### 5. SRE Metrics

- **SLA**: Service Level Agreement - Thỏa thuận cấp độ dịch vụ (99.9%)
- **SLO**: Service Level Objective - Mục tiêu (target)
- **SLI**: Service Level Indicator - Chỉ số thực tế (actual)

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [3.5 Terraform](../3.5_Terraform_IaC/) | **3.6 System Design** | [3.7 Capstone](../3.7_Capstone_Project/) |

---

**Build reliable systems! 🏛️**

*Xây dựng hệ thống đáng tin cậy!*

</div>
