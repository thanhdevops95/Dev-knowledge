# Bài #5 — Hệ Thống Chứng Chỉ Kubernetes của CNCF

---

## 📋 Metadata

- **Bài số:** #5
- **Module:** 00-introduction
- **Cấp độ:** `BEGINNER` (định hướng nghề nghiệp)
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Bài #1 — Giới thiệu series](01-gioi-thieu-series.md)
- **Last Updated:** 09/05/2026
- **Author:** Mr.Rom 

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Phân biệt được **3 nhóm chứng chỉ** chính của CNCF (Specialist, Associate, Bổ trợ)
- [ ] Hiểu **format thi** (online, performance-based vs trắc nghiệm)
- [ ] Biết **chiến lược chọn chứng chỉ** đầu tiên (CKA → CKAD → CKS)
- [ ] Nắm các **mẹo thi & nguồn tài nguyên** quan trọng

---

## 📚 Nội Dung

### 1. CNCF là gì?

**CNCF = Cloud Native Computing Foundation** — tổ chức (thuộc Linux Foundation) đứng sau Kubernetes và hệ sinh thái cloud-native (storage, networking, GitOps, service mesh, observability…).

### 2. Bản đồ Chứng Chỉ CNCF (10 chứng chỉ)

```
┌──────────────────────────────────────────────────────────┐
│ NHÓM 1: SPECIALIST (3 chứng chỉ phổ biến nhất)            │
│  ├─ CKA   — Certified Kubernetes Administrator           │
│  ├─ CKAD  — Certified Kubernetes Application Developer   │
│  └─ CKS   — Certified Kubernetes Security Specialist     │
│      (yêu cầu có CKA trước)                              │
├──────────────────────────────────────────────────────────┤
│ NHÓM 2: ASSOCIATE (entry-level, dễ hơn)                   │
│  ├─ KCNA  — Kubernetes & Cloud Native Associate          │
│  └─ KCSA  — Kubernetes & Cloud Native Security Associate │
├──────────────────────────────────────────────────────────┤
│ NHÓM 3: BỔ TRỢ (chuyên ngành)                             │
│  ├─ PCA   — Prometheus Certified Associate (monitoring)  │
│  ├─ ICA   — Istio Certified Associate (service mesh)     │
│  ├─ CCA   — Cilium Certified Associate (networking/sec)  │
│  ├─ CAPA  — Argo Project Associate (GitOps)              │
│  └─ CGOA  — Certified GitOps Associate                   │
└──────────────────────────────────────────────────────────┘
```

### 3. So sánh CKA / CKAD / CKS

| Tiêu chí          | CKA                            | CKAD                        | CKS                              |
| ----------------- | ------------------------------ | --------------------------- | -------------------------------- |
| **Đối tượng**     | Sysadmin, kiến trúc sư hạ tầng | Developer triển khai app    | Security engineer                |
| **Định hướng**    | Cluster operation              | Build & deploy app trên K8s | Hardening, supply chain security |
| **Format**        | Performance-based (LAB)        | Performance-based (LAB)     | Performance-based (LAB)          |
| **Thời gian thi** | 2 giờ                          | 2 giờ                       | 2 giờ                            |
| **Pass score**    | 66%                            | 66%                         | 67%                              |
| **Hạn chứng chỉ** | 3 năm                          | 3 năm                       | **2 năm**                        |
| **Yêu cầu trước** | Không                          | Không                       | **Phải có CKA**                  |
| **Giá**           | ~$395                          | ~$395                       | ~$395                            |

> 💡 **Lời khuyên:** Bắt đầu với **CKA** — đây là chứng chỉ tổng quan nhất, giúp bạn có bức tranh toàn cảnh K8s. Sau đó mới chuyển qua CKAD / CKS tùy hướng đi.

### 4. Các Chứng Chỉ Bổ Trợ

| Chứng chỉ            | Phù hợp cho                                    |
| -------------------- | ---------------------------------------------- |
| **PCA** (Prometheus) | Engineer làm về **observability/monitoring**   |
| **ICA** (Istio)      | Người làm về **service mesh**                  |
| **CCA** (Cilium)     | Networking + Security + Observability advanced |
| **CAPA** (Argo)      | GitOps, ML pipeline, data scientist            |
| **CGOA** (GitOps)    | Foundation về GitOps best practices            |

> Khuyến nghị: học **CKA + CKAD trước**, rồi mới đi sâu vào các chứng chỉ bổ trợ tùy nhu cầu công việc.

---

## 💻 Format Thi & Mẹo Thực Chiến

### Format thi

- **Online 100%** — không có trung tâm thi vật lý.
- **Performance-based** (CKA/CKAD/CKS): bạn được đưa vào môi trường lab thật, làm các task như upgrade cluster, tạo Deployment, cấu hình NetworkPolicy…
- **Trắc nghiệm** (KCNA/KCSA): multiple choice trong 90 phút.
- **Mở tài liệu** (chỉ `kubernetes.io`) — nhưng bạn **không có đủ thời gian** để tra cứu hết, phải nhớ hầu hết.

### Chuẩn bị máy & môi trường thi

```
✅ Phòng yên tĩnh, không có người ra vào
✅ Webcam HD (sẽ scan kỹ phòng)
✅ Internet ổn định
✅ Máy tính cá nhân (KHÔNG dùng máy công ty - nhiều process bị block)
✅ Có không gian rộng trên bàn (giám thị check kỹ)
```

> ⚠️ **Quan trọng:** Đoạn check máy tính được **tính trong 2 giờ thi**! Chuẩn bị máy chu đáo trước.

### Simulation Test (kèm khi mua exam)

- Mua exam → được **2 lần** Active simulation
- Mỗi lần Active có **36 giờ** thi thử **không giới hạn số lần**
- Thi thử thường **khó hơn thi thật**
- 💡 Mẹo: Active simulation **cuối tuần** để có 1.5 ngày thi liên tục
- ⚠️ Nếu Active rồi đi thi thật, simulation sẽ bị xóa → tận dụng trước!

### Free Retake

Mua 1 voucher → **được thi lại 1 lần miễn phí** nếu rớt lần đầu.

### Voucher Giảm Giá

CNCF/Linux Foundation thường có **2 đợt giảm giá lớn/năm**:
- Tháng 2 (đầu năm)
- Cuối năm (Black Friday)
- Mức giảm: **40-50%** + có thể tặng kèm khóa học online

> 💬 *"Các bạn nhớ tìm những đợt sale off thì sẽ rẻ hơn. Voucher có thời hạn 1 năm từ ngày mua, nên đã mua rồi thì sắp xếp học và thi luôn."*

---

## ⚠️ Lưu Ý Quan Trọng

- ⏰ Voucher mua rồi **chỉ valid 1 năm** — đừng để hết hạn.
- 🔁 K8s release **3-4 minor version/năm** → cần học tiếp tục để keep up to date.
- 📚 Đề thi **mở tài liệu** nhưng tốc độ là yếu tố quyết định — **luyện hands-on nhiều, gõ command nhanh**.
- 🚫 Không thi máy tính công ty (nhiều process bảo mật cản exam app).
- ✅ Kết quả thi: thông báo trong vòng **24 giờ** sau khi hoàn thành.

---

## ✅ Self-Check

1. **CKS có yêu cầu gì đặc biệt khác CKA và CKAD?**
   <details>
   <summary>Đáp án</summary>
   CKS yêu cầu phải có CKA trước, và CKS chỉ valid 2 năm (CKA/CKAD valid 3 năm).
   </details>

2. **Khi mua exam, được tặng kèm những gì?**
   <details>
   <summary>Đáp án</summary>
   - 1 lần thi lại miễn phí (free retake) nếu rớt
   - 2 lần Active simulation (mỗi lần 36h thi thử không giới hạn)
   - Đôi khi có khóa học online tiếng Anh kèm theo
   </details>

3. **Nên thi chứng chỉ đầu tiên là gì?**
   <details>
   <summary>Đáp án</summary>
   **CKA** — vì cho bức tranh tổng quan nhất về K8s. Nếu chưa có nhiều kinh nghiệm, có thể bắt đầu với **KCNA** (associate) trước.
   </details>

4. **Pass score của CKA là bao nhiêu phần trăm?**
   <details>
   <summary>Đáp án</summary>
   66%. CKAD cũng 66%, CKS là 67%.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #1 — Giới thiệu series](01-gioi-thieu-series.md)
- ➡️ [Bài #2 — Kubernetes là gì? K8s là gì?](../01-core-concepts/01-kubernetes-la-gi.md)
- 🏠 [Quay về index Module 00 — Introduction](README.md)
- 🏠 [Quay về index Series K8s Training](../README.md)

### Tài Nguyên

- 🌐 [CNCF Certifications](https://www.cncf.io/training/certification/)
- 🌐 [Linux Foundation Training Portal](https://trainingportal.linuxfoundation.org/)
- 🌐 [CKA Curriculum](https://github.com/cncf/curriculum)
- 📺 Video gốc: `Decopy_✅ #5 _ Hệ Thống Chứng Chỉ Kubernetes _ CNCF_captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Mình recommend các bạn thi CKA trước — đây là chứng chỉ giúp các bạn có một bức tranh tổng quan về K8s. Sau này tương lai xa các bạn có thể quan tâm nhiều hơn đến CKAD hay CKS."*

> 💬 *"Cái đoạn người ta kiểm tra máy tính các bạn — mình thấy nó tính kệ trong 2 giờ luôn! Cho nên các bạn nhớ chuẩn bị máy tính cho nó tốt một xíu, đừng nên thi bằng máy tính của công ty."*

> 💬 *"Đề thi mở tài liệu (kubernetes.io) nhưng các bạn sẽ không có đủ thời gian để tra cứu cho tất cả mọi thứ đâu — chỉ kịp tra những thứ ít làm thôi. Còn lại phải gõ command nhanh và thuộc."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
