# 💰 Cloud Cost Management (FinOps)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Cụm Basic hoàn chỉnh (5/5 bài)

> 🎯 *FinOps không phải là một công cụ, mà là sự kết hợp giữa văn hóa và thực hành để cả đội cùng chịu trách nhiệm về chi phí cloud. Cụm bài này đi từ 6 nguyên tắc của FinOps Foundation, qua các mô hình giá giúp tiết kiệm (Reserved Instances, Committed Use Discounts, Spot, Hybrid Benefit), đến chiến lược gắn thẻ (tagging) để truy vết chi phí về đúng đội, rồi các chiến thuật tối ưu thực tế và cuối cùng là bộ công cụ tự động hóa.*

---

## 🚀 Bắt đầu nhanh

Nếu bạn chưa biết nên đọc gì trước, hãy đi tuần tự từ trên xuống — mỗi bài là một mảnh ghép nối tiếp nhau, từ tư duy nền tảng đến hành động cụ thể.

- [🎓 FinOps — Văn hóa quản lý chi phí Cloud](lessons/01_basic/00_what-is-finops-overview.md)
- [🎓 Pricing Models — On-demand / Reserved / Spot / Savings Plans](lessons/01_basic/01_pricing-models-deep.md)
- [🎓 Tagging, Allocation & Showback Reports](lessons/01_basic/02_tagging-allocation-and-showback.md)
- [🎓 Optimization Tactics — Compute / Storage / Network / Database](lessons/01_basic/03_optimization-tactics-compute-storage-network.md)
- [🎓 FinOps Tools & Automation](lessons/01_basic/04_finops-tools-and-automation.md)

---

## 📖 Danh sách bài — Cụm Basic (5 bài)

Năm bài dưới đây được sắp theo đúng vòng đời quản lý chi phí: hiểu văn hóa trước, nắm cách tính giá, biết cách quy chi phí về từng đội, rồi mới tối ưu và tự động hóa. Bạn nên đọc theo thứ tự để mạch kiến thức liền lạc.

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [FinOps là gì](lessons/01_basic/00_what-is-finops-overview.md) | 6 nguyên tắc + 3 giai đoạn (Inform/Optimize/Operate) + cơ cấu đội + phân biệt showback và chargeback |
| 01 | [Mô hình giá chuyên sâu](lessons/01_basic/01_pricing-models-deep.md) | Reserved Instances / Committed Use Discounts + Savings Plans + Spot + Hybrid Benefit + các chi phí ẩn |
| 02 | [Tagging + Showback](lessons/01_basic/02_tagging-allocation-and-showback.md) | Chiến lược gắn thẻ, ép tuân thủ qua SCP/Terraform, phân bổ chi phí và báo cáo showback |
| 03 | [Chiến thuật tối ưu](lessons/01_basic/03_optimization-tactics-compute-storage-network.md) | Right-sizing + vòng đời lưu trữ + chi phí egress + tối ưu Database |
| 04 | [Công cụ + tự động hóa](lessons/01_basic/04_finops-tools-and-automation.md) | Công cụ native + bên thứ ba (CloudHealth/Cloudability/Infracost) + tự động hóa |

→ **Trọng tâm cụm này là thực hành: phần lớn giá trị nằm ở việc bạn tự áp các chiến thuật tối ưu lên môi trường thật của mình.**

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [☁️ 11_cloud](../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS](../aws/) — nơi áp dụng Reserved Instances + Savings Plans
- ☁️ [GCP](../gcp/) — Committed Use Discounts + Sustained Use Discounts + Spot
- ☁️ [Azure](../azure/) — Reserved Instances + Hybrid Benefit
- 🌐 [Multi-cloud Strategies](../multi-cloud-strategies/) — quản lý chi phí khi chạy nhiều nhà cung cấp

### 🌐 Tài nguyên tham khảo khác

- 📖 [FinOps Foundation](https://www.finops.org/) — tổ chức chuẩn hóa khung FinOps
- ⬅️ **Bài trước:** [Infracost](https://www.infracost.io/) — xem trước chi phí ngay trong Pull Request
- 📖 [CloudHealth](https://cloudhealth.vmware.com/)
- 📖 [Apptio Cloudability](https://www.cloudability.com/)
- 📖 [Vantage](https://www.vantage.sh/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Cụm Basic hoàn chỉnh 5/5 bài, tập trung vào thực hành FinOps.
- **v2.0.0 (01/06/2026)** — Việt hóa block giới thiệu và mô tả bảng (bỏ văn phong điện tín EN); link bài dùng tiêu đề H1 thực; chuẩn hóa nav theo 3 nhóm (🧭/🧩/🌐); bỏ cột "Thời lượng" và mọi ước tính thời gian; Việt hóa field "Trạng thái".
