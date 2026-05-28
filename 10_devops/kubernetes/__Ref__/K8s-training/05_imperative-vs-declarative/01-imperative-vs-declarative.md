# Bài #13 — So Sánh Imperative vs Declarative

> 🎯 Khái niệm cốt lõi của **DevOps** và **Infrastructure as Code (IaC)** — không chỉ K8s mà rộng hơn.

---

## 📋 Metadata

- **Bài số:** #13
- **Module:** 05-imperative-vs-declarative
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Module 04 — NodePort](../04-expose-pod-nodeport/README.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Phân biệt rõ **Imperative** vs **Declarative**
- [ ] Hiểu vì sao **Declarative là best practice** cho production
- [ ] Tạo Pod đầu tiên bằng YAML manifest
- [ ] Biết cấu trúc 4 phần cơ bản của manifest: `apiVersion`, `kind`, `metadata`, `spec`

---

## 📚 Nội Dung

### 1. Định Nghĩa

#### Imperative — "Chỉ TỪNG BƯỚC LÀM SAO"

```
"Đi thẳng 500m, rẽ phải, đi thêm 200m, rẽ trái..."
```

→ Người làm gọi từng command/từng bước.

**Ví dụ K8s:**

```bash
kubectl run app-2 --image=nginx --port=80
kubectl expose pod app-2 --type=NodePort --port=80
kubectl scale --replicas=3 ...
```

#### Declarative — "Chỉ NƠI ĐẾN"

```
"Đi từ nhà đến trường" → người lái xe (hoặc Google Maps) tự lo cách đi
```

→ Người làm chỉ định **trạng thái mong muốn**, hệ thống tự lo cách đạt được.

**Ví dụ K8s:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-2
spec:
  containers:
    - name: app
      image: nginx
      ports:
        - containerPort: 80
```

```bash
kubectl apply -f pod.yaml   # ← K8s tự lo cách tạo Pod
```

---

### 2. So Sánh Chi Tiết

| Tiêu chí                   | Imperative                       | Declarative                     |
| -------------------------- | -------------------------------- | ------------------------------- |
| **Mô tả**                  | Từng bước thủ công               | Chỉ định trạng thái cuối        |
| **Lệnh K8s**               | `kubectl run`, `expose`, `scale` | `kubectl apply -f file.yaml`    |
| **Tốc độ học**             | Nhanh, dễ hiểu                   | Cần học YAML                    |
| **Tốc độ tạo 1 resource**  | Rất nhanh                        | Cần viết YAML trước             |
| **Lặp lại / Reproducible** | ❌ Khó                            | ✅ Dễ (lưu YAML, dùng lại)       |
| **Version Control**        | ❌ Không                          | ✅ Có (Git)                      |
| **CI/CD friendly**         | ❌                                | ✅                               |
| **Phù hợp với**            | Dev test nhanh, debug            | **Production**                  |
| **Rủi ro lỗi**             | Cao (gõ tay)                     | Thấp (review YAML, peer review) |

---

### 3. Vì Sao Production Cần Declarative?

#### Vấn đề khi dùng Imperative ở quy mô lớn

```
   Bạn deploy 50 Pod, 20 Service, 10 ConfigMap, 5 Secret...

   Imperative way:
   $ kubectl run pod-1 ...
   $ kubectl run pod-2 ...
   $ kubectl expose ...
   $ kubectl create configmap ...
   ... 100+ commands ...
   ❌ Quên 1 lệnh → khác nhau giữa env
   ❌ Bị disaster → tạo lại từ đầu rất khổ
   ❌ Không có audit trail
   ❌ Onboarding member mới rất khó
```

#### Declarative way

```
   $ git clone repo/
   $ kubectl apply -f manifests/
   ✅ 1 command — deploy hết
   ✅ Disaster? Re-apply, OK ngay
   ✅ Code review qua Pull Request
   ✅ Audit trail = git log
   ✅ Onboarding: đọc YAML là hiểu
```

---

### 4. Liên Hệ Tới DevOps Best Practices

Declarative là 1 phần của:

- **12-Factor App** (Heroku) — config, build/release/run separation
- **AWS Well-Architected Framework** — Operational Excellence pillar khuyến nghị **Infrastructure as Code (IaC)**
- **GitOps** — toàn bộ trạng thái cluster lưu trong Git
- **Terraform, Helm, Kustomize, ArgoCD** — đều dựa trên Declarative

> 🎓 Đầu tư học Declarative giờ = đầu tư cho DevOps career sau này.

---

## 💻 Hands-On / Demo

### Bước 1: Tạo file `pod.yaml`

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-app
  labels:
    app: simple-app
spec:
  containers:
    - name: simple-app
      image: nginx:latest
      ports:
        - containerPort: 80
```

> 💡 Bạn có thể mở bằng VS Code (`code pod.yaml`) thay vì terminal cho dễ chỉnh sửa.

### Bước 2: Apply

```bash
kubectl apply -f pod.yaml
# pod/simple-app created

kubectl get pods
# NAME         READY   STATUS    RESTARTS   AGE
# simple-app   1/1     Running   0          15s

kubectl describe pod simple-app
# (xem chi tiết)
```

### Bước 3: Sửa & Apply Lại

Sửa `pod.yaml` → thay `nginx:latest` thành `nginx:1.25-alpine`:

```bash
kubectl apply -f pod.yaml
# pod/simple-app configured  ← LƯU Ý: configured (không phải created!)
```

K8s tự nhận biết và update.

### Bước 4: Xóa

```bash
# Xóa bằng manifest (tiện cho many resources)
kubectl delete -f pod.yaml

# Hoặc xóa từng cái
kubectl delete pod simple-app
```

---

### So Sánh Workflow

```bash
# ===== IMPERATIVE =====
kubectl run app-2 --image=nginx --port=80
# (xong! nhanh thật, nhưng không lưu được)

# ===== DECLARATIVE =====
echo "apiVersion: v1
kind: Pod
metadata:
  name: app-2
spec:
  containers:
    - name: app
      image: nginx
" > pod.yaml

kubectl apply -f pod.yaml
git add pod.yaml && git commit -m "Add app-2 pod"
git push  # ← Có history, có review!
```

---

## ⚠️ Lưu Ý

- 🔥 **Production:** dùng **Declarative** 100%, không Imperative
- 🔥 Imperative tốt cho **dev/test/debug nhanh**
- 🔥 Mỗi project nên có folder `manifests/` chứa YAML, push Git
- ⚠️ Không trộn Imperative + Declarative trên cùng resource (gây drift)
- ⚠️ Khi `kubectl apply`, K8s so sánh với trạng thái hiện tại → chỉ thay đổi cái cần

---

## ✅ Self-Check

1. **Imperative khác Declarative ở điểm nào cốt lõi?**
   <details>
   <summary>Đáp án</summary>
   - **Imperative**: chỉ định **CÁCH** làm (từng bước)
   - **Declarative**: chỉ định **NƠI ĐẾN** (trạng thái cuối)
   </details>

2. **Lệnh nào áp dụng Declarative trong K8s?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl apply -f <file.yaml>
   kubectl apply -f <directory>/
   ```

   </details>

3. **Vì sao production phải dùng Declarative?**
   <details>
   <summary>Đáp án</summary>
   - Reproducible (lặp lại được)
   - Version Control (Git)
   - CI/CD friendly
   - Disaster Recovery dễ
   - Code Review / Audit
   </details>

4. **4 phần cơ bản của 1 manifest K8s là gì?**
   <details>
   <summary>Đáp án</summary>
   - `apiVersion`
   - `kind`
   - `metadata`
   - `spec`
   </details>

5. **`kubectl apply` lần 2 trên file đã apply rồi sẽ làm gì?**
   <details>
   <summary>Đáp án</summary>
   K8s **so sánh** với trạng thái hiện tại. Nếu giống → không làm gì (`unchanged`). Nếu khác → update (`configured`).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Module 04 — NodePort](../04-expose-pod-nodeport/README.md)
- ➡️ [Bài #14 — YAML Manifest 101](02-yaml-manifest-101.md)

### Tài Nguyên

- 📖 [Object Management](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/)
- 📖 [12 Factor App](https://12factor.net/)
- 📖 [AWS Operational Excellence](https://docs.aws.amazon.com/wellarchitected/latest/framework/operational-excellence.html)
- 📺 Video gốc: `Decopy_✅ #13 _ So sánh Imperative vs Declarative..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Khi đi thi chứng chỉ K8s, các bạn được mở `kubernetes.io`. Trên đó hầu hết các template Declarative — biết Declarative là biết cách thi nhanh."*

> 💬 *"Imperative tốt cho công việc TẠM THỜI, NGẮN HẠN. Triển khai quy mô lớn thì cần PHƯƠNG THỨC LẶP LẠI — đó là Declarative."*

> 💬 *"Tạo manifest 1 lần là dùng đi dùng lại nhiều lần. Sau này có thể tạo cả tenant chạy bằng 1 lệnh `kubectl apply` — quá tiện!"*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
