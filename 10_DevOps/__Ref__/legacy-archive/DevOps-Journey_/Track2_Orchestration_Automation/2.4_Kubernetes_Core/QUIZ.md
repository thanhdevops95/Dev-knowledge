# ❓ Quiz: Kubernetes Core

> **Knowledge Check for Kubernetes Fundamentals (8 Questions)**
>
> *Kiểm tra kiến thức Kubernetes cơ bản (8 câu hỏi).*

---

### Q1: Pod Definition

What is a Pod?

*(Pod là gì?)*

- a) Container
- b) Smallest deployable unit *(Đơn vị triển khai nhỏ nhất)*
- c) Node
- d) Service

---

### Q2: ReplicaSet Purpose

What does ReplicaSet ensure?

*(ReplicaSet đảm bảo gì?)*

- a) Desired number of pods *(Số lượng Pod mong muốn)*
- b) Network policy *(Chính sách mạng)*
- c) Storage *(Lưu trữ)*
- d) Secrets *(Bí mật)*

---

### Q3: External IP Service

Which Service type exposes external IP?

*(Service type nào expose ra external IP?)*

- a) ClusterIP
- b) NodePort
- c) LoadBalancer
- d) b and c *(b và c)*

---

### Q4: Kubectl Apply

What does `kubectl apply -f` do?

*(`kubectl apply -f` làm gì?)*

- a) Delete resource *(Xóa tài nguyên)*
- b) Create or update resource *(Tạo hoặc cập nhật tài nguyên)*
- c) View resource *(Xem tài nguyên)*
- d) Scale resource *(Mở rộng tài nguyên)*

---

### Q5: ConfigMap Purpose

What is ConfigMap used for?

*(ConfigMap dùng để?)*

- a) Store secrets *(Lưu trữ bí mật)*
- b) Store configuration *(Lưu trữ cấu hình)*
- c) Store images *(Lưu trữ images)*
- d) Store volumes *(Lưu trữ volumes)*

---

### Q6: Namespace Purpose

What is Namespace used for?

*(Namespace dùng để?)*

- a) Isolate resources *(Cô lập tài nguyên)*
- b) Network policies *(Chính sách mạng)*
- c) Storage *(Lưu trữ)*
- d) Monitoring *(Giám sát)*

---

### Q7: Liveness Probe

What is Liveness probe used for?

*(Liveness probe dùng để?)*

- a) Check if container is ready *(Kiểm tra container sẵn sàng chưa)*
- b) Check if container needs restart *(Kiểm tra container có cần restart)*
- c) Check resources *(Kiểm tra tài nguyên)*
- d) Check network *(Kiểm tra mạng)*

---

### Q8: Wide Output

What extra info does `kubectl get pods -o wide` show?

*(`kubectl get pods -o wide` hiển thị gì thêm?)*

- a) Logs *(Nhật ký)*
- b) Node and IP *(Node và IP)*
- c) Events *(Sự kiện)*
- d) Secrets *(Bí mật)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | b | Pod is the smallest deployable unit |
| 2 | a | Maintains desired pod count |
| 3 | d | Both NodePort and LoadBalancer expose externally |
| 4 | b | Declarative create/update |
| 5 | b | Non-sensitive configuration data |
| 6 | a | Logical isolation of resources |
| 7 | b | Restarts unhealthy containers |
| 8 | b | Shows Node and Pod IP |

</details>

---

**[← Back to README](./README.md)**
