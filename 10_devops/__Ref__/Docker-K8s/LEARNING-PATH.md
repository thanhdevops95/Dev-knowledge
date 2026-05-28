# 🗺️ Thứ tự học khuyến nghị (Learning Path)

> **Author:** Mr.Rom
> **Mục đích:** Đề có 69 bài đánh số 01→69. Đọc tuần tự vẫn được, **nhưng** vài bài Bonus là **prerequisite** cho các "dự án tổng hợp" (Bài 41, 50). File này đề xuất 2 track tuỳ mục tiêu của bạn.

---

## ⚠️ Vấn đề sequencing (lý do có file này)

Khi mình thêm Phần D — Bonus (Bài 51-69) vào sau bộ 50 bài cũ, **giữ số folder nguyên** để khỏi phá structure. Hệ quả: vài Bonus dạy **kiến thức nền** mà các bài cũ đã giả định có sẵn:

| Bài Core | Reference Bonus chưa được dạy |
|----------|--------------------------------|
| **Bài 41** Dự án full stack K8s | Bonus 56 (Job), 58 (Init/Sidecar), 59 (RBAC), 60 (NetworkPolicy), 66 (Prometheus) |
| **Bài 44** Helm Hooks | Bonus 56 (Job — đoạn `kind: Job` chưa được dạy) |
| **Bài 46** GitOps workflow | Bonus 64 (Kustomize — file `kustomization.yaml` chưa được dạy) |
| **Bài 50** Istio dự án cuối | Bonus 59 (RBAC), 66 (Prometheus), Loki/EFK (chỉ note, không có bài) |

→ Nếu học strict 01→69, đến Bài 41 sẽ phải "tin lời đề" về NetworkPolicy/RBAC mà chưa làm tay; đến Bonus 60/59 mới biết. Không sai, nhưng UX không tối ưu.

→ **Đề xuất 2 track** dưới đây.

---

## Track A — "Lộ trình tuyến tính" (mới bắt đầu)

Đi từ 01→69 nguyên thứ tự, **chấp nhận**:
- Đến Bài 41, làm các phần CƠ BẢN (Frontend + Backend + Redis + DB + Helm + HPA + Ingress + Probes), **bỏ qua** các bullet `🔴 yêu cầu nâng cao: NetworkPolicy + RBAC + ServiceAccount + Backup`.
- Đến Bài 44, đọc Bonus 56 (Job) **trước** khi làm phần Hooks (~5 phút đọc).
- Đến Bài 46, đọc Bonus 64 (Kustomize) **trước** (~5 phút).
- Đến Bài 50, làm phần MTLS + Tracing (không cần advanced RBAC); để Logging Loki/EFK cho sau.
- Sau khi xong 50 → vào Bonus 51-69 hoàn thiện kỹ năng production.

**Thời lượng:** ~17 tuần (theo bảng Tổng kết lộ trình)
**Phù hợp:** Người mới hoàn toàn, muốn câu chuyện liền mạch.

```
[Docker 01-24] → [K8s 25-41 basic] → [Advanced 42-50 + đọc bonus liên quan]
              → [Bonus 51-69 hoàn thiện]
```

---

## Track B — "Production-first" (đã có nền tảng)

Re-order **theo dependency**, không theo số:

```
PHASE 1 — Docker fundamentals + production hygiene
  Docker 01-23  +  51-55         (~2 tuần)

PHASE 2 — K8s fundamentals
  K8s 25-40                       (~2.5 tuần)

PHASE 3 — K8s production primitives (Bonus chèn vào trước)
  Bonus 56 Job/CronJob
  Bonus 57 DaemonSet
  Bonus 58 Init/Sidecar
  Bonus 59 RBAC                  ← BẮT BUỘC trước 41
  Bonus 60 NetworkPolicy         ← BẮT BUỘC trước 41
  Bonus 61 Affinity/Taints
  Bonus 62 Quota/PDB
  Bonus 63 StorageClass
  Bonus 64 Kustomize             ← BẮT BUỘC trước 46
  K8s 41 Dự án tổng hợp           ← bây giờ làm với đủ tools

PHASE 4 — Helm chuyên sâu
  Bonus 56 (đã xong)
  Advanced 42-44                  (Bài 44 dùng Job → 56 đã có)

PHASE 5 — GitOps + Service Mesh
  Advanced 45 ArgoCD install
  Bonus 64 (đã xong)
  Advanced 46-47                  (dùng Kustomize → 64 đã có)
  Advanced 48-50

PHASE 6 — Production stack
  Bonus 65 cert-manager
  Bonus 66 Prometheus
  Bonus 67 Velero
  Bonus 68 Sealed Secrets
  Bonus 69 Operator + CRD
```

**Thời lượng:** ~14 tuần (ít hơn vì không phải quay lại)
**Phù hợp:** Đã biết Docker, muốn nhảy thẳng vào production K8s.

---

## Bảng dependency rõ ràng

| Bài | Phụ thuộc bắt buộc | Khuyến nghị đọc trước |
|-----|--------------------|----------------------|
| 41 Full stack | 25-40 | **56, 59, 60** (cho phần 🔴 advanced); 58 (sidecar); 66 (monitoring) |
| 44 Helm Hooks | 40, 42, 43 | **56** (Job concept) |
| 46 GitOps | 45 | **64** (Kustomize) |
| 50 Istio Security | 48, 49 | **59** (RBAC ngôn ngữ chung); 66 (tracing/metrics) |
| 56 Job | 29-30 | — |
| 58 Init/Sidecar | 35 (Redis), 27 (Pod) | — |
| 59 RBAC | 32-33 | — |
| 60 NetworkPolicy | 35 (multi-pod cùng namespace) | Calico CNI (xem §12 TIPS) |
| 64 Kustomize | 29-32 | — |
| 65 cert-manager | 38 (Ingress) | — |
| 66 Prometheus | 29 (Deployment) | — |
| 69 Operator/CRD | 39 (StatefulSet hiểu PVC) | 65/66 (Operator example) |

---

## Đề xuất khi xây dựng giáo trình

Nếu bạn dạy theo lớp (instructor-led):

1. **Tuần 1-3:** Docker (01-24) + 51-55 — 5h/tuần × 3
2. **Tuần 4-6:** K8s core (25-40) — 5h/tuần × 3
3. **Tuần 7:** Bonus 56-58 (workload patterns) — 5h
4. **Tuần 8:** Bonus 59-60 (security: RBAC + NetPol) — 5h
5. **Tuần 9:** Bonus 61-64 (Affinity/Quota/Storage/Kustomize) — 5h
6. **Tuần 10:** **K8s 41 dự án tổng hợp** (giờ học viên đã có đủ) — 8h
7. **Tuần 11-12:** Helm chuyên sâu (42-44) + ArgoCD (45-47) — 10h
8. **Tuần 13-14:** Istio (48-50) + dự án cuối — 10h
9. **Tuần 15-16:** Bonus 65-69 (production stack) — 10h

**Tổng:** ~16 tuần / 75-80h.

---

## Thay đổi nhỏ trong tài liệu

Mỗi bài có forward reference đã được **bổ sung box "Prerequisites"** ở đầu:

- Bài 41: box `🔴 Phần advanced trong bài này dùng RBAC/NetPol — đọc Bonus 59, 60 trước hoặc skip phần đó`
- Bài 44: box `📌 Đoạn Hooks dùng K8s Job — đọc Bonus 56 trước nếu chưa quen`
- Bài 46: box `📌 Workflow GitOps dùng Kustomize — đọc Bonus 64 trước`
- Bài 50: box `📌 Phần Authorization nâng cao kết hợp Bonus 59`

---

## Tóm tắt

- File master `docker-k8s-practice.md` **giữ nguyên đánh số** 01→69 cho dễ tham chiếu.
- Folder thực hành cũng giữ nguyên số.
- **Học theo Track A** nếu mới: đi tuần tự, đến forward reference thì xem note + nhảy đọc Bonus tương ứng.
- **Học theo Track B** nếu đã biết: theo phase, không theo số.

Cả hai đều đến cùng đích: 69 bài hoàn thành, hiểu được cả `myapp` evolution lẫn production K8s.

## Tham chiếu

- [`docker-k8s-practice.md`](docker-k8s-practice.md) — đề master
- [`MINIKUBE-LOCAL-TIPS.md`](MINIKUBE-LOCAL-TIPS.md) — mẹo local
- [`LAB-RUN-LOG.md`](LAB-RUN-LOG.md) — verify thực tế
