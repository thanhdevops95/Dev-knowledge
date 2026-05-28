# 🔥 Chứng Chỉ CKA — Kế Hoạch Đạt Chứng Chỉ Kubernetes Cao Cấp Nhất

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Hướng dẫn học tập để lấy chứng chỉ CKA (Certified Kubernetes Administrator) cực kỳ danh giá của tổ chức Cloud Native Computing Foundation (CNCF).
> **Prerequisite:** Bất kì kiến thức nền tảng về Kubernetes (Từ `01` đến `08`).

---

## Tại sao chứng chỉ CKA lại quan trọng?

Trong thế giới đám mây, chứng chỉ AWS, Azure thường là các bài kiểm tra trắc nghiệm đọc hiểu (Multiple Choice). Nhưng **CKA (Certified Kubernetes Administrator)** là bài kiểm tra thực hành 100% trên giao diện dòng lệnh Linux (Command Line). Bạn phải vượt qua 15-20 bài tập sửa lỗi hệ thống máy chủ thật trong vòng 2 tiếng. Nó cực kỳ khốc liệt vì bạn phải gõ hàng loạt cấu hình mã YAML mà không có trình soạn thảo báo lỗi màu hỗ trợ.

**Giá trị:**
Chính vì độ khó thi thực tế hoàn toàn, một kỹ sư cầm bằng CKA luôn được đánh giá rất cao, minh chứng cho việc bạn có đủ kỹ năng tự cứu sống toàn bộ hệ thống máy chủ của công ty khi bị sập hoàn toàn.

---

## 1. Cơ Cấu Tổ Chức Bài Thi Cấu Hình

Tỉ lệ điểm số phân loại trong bài thi bao gồm các chủ đề chính:
1. **Khắc phục sự cố (Troubleshooting) - 30%:** Đây là module chiếm nhiều điểm nhất. Kịch bản: K8s bị dập chết máy chủ con (Worker node xập, Kubelet tự tắt đèn do báo lỗi cấu hình sai). Yêu cầu dùng lệnh Linux sửa cấu hình khởi động Cụm máy bật lại.
2. **Kiến trúc cụm và Cài đặt (Cluster Architecture, Upgrade) - 25%:** Yêu cầu dùng công cụ cài đặt Kubernetes gốc (Kubeadm) để tạo cụm mới và nâng cấp Cụm K8s từ bản cũ (v1.28) lên hệ mới (v1.29) trong nháy mắt mà không ảnh hưởng máy trạm.
3. **Quản lý thiết bị lưu trữ và khối công việc (Workloads & Storage) - 15%:** Dùng YAML tạo máy ảo MySQL và cấp thêm mạng ổ cứng (Persistent Volume PVC).
4. **Mạng lưới Network và Dịch vụ (Services & Networking) - 20%:** Tạo Ingress Controller, tạo DNS liên thông và cấu hình Tường Lửa (Network Policies) cấm giao tiếp rác.

---

## 2. Bí Tuyết Thi Lệnh Kubectl Thần Tốc (Imperative Commands)

Cách tốt nhất rớt bài thi CKA là ngồi đi gõ tay định lượng tạo 50 dòng YAML của file Deployment hay Pod. Thời gian thi chỉ có 2 tiếng (Trung bình khoảng 5 phút 1 bài tập).

Nắm vững ngón nghề cài lệnh trực tiếp sinh YAML là bí thuật duy nhất vượt kỳ thi. Gọi là "Imperative Commands".

```bash
# KHÔNG BAO GIỜ GÕ YAML TỪ SỐ O.
# Hãy dùng lệnh hệ thống gõ 1 dòng sau để sinh ra Khối Deployment 3 Máy.
kubectl create deployment con-ran --image=nginx --replicas=3 

# Lập trình tạo YAML nhưng không đưa lên máy chủ ngay, chỉ xuất ra file.
# Cờ Dry-run = giả vờ chạy | -o yaml = trả ra chữ định dạng YAML
kubectl run cai-pod-may-chu --image=nginx --dry-run=client -o yaml > pod1.yaml

# Thiết lập Service chọc thẳng ứng dụng mạng nội bộ 
kubectl expose deployment con-ran --port=80 --target-port=8080
```
Sau đó bạn dùng Visual Editor của Linux (Vim) mở tệp `pod1.yaml`, sửa hai ba dòng nhỏ và lưu lại gõ `kubectl apply` là xong bài toán. Tiết kiệm 10 phút ngồi tự làm định dạng gõ tay.

---

## Gotchas — Những lỗi thường gặp khi đi thi

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Quên không chuyển hướng mạng (Context) giữa các Cụm máy bài thi khi giải câu mới. Nếu bạn đang làm bài thi số 5 ở Cụm A mà không đổi mạng, đụng bài 6 gõ lên Cụm B, nó sẽ lưu sai kết quả bài thi. | Đọc kỹ yêu cầu đề đầu câu hỏi. Luôn áp dụng dòng đổi lệnh thiết bị cung cấp màu đầu trang. Dùng lệnh `kubectl config use-context cum-b` để trỏ vào vùng máy mới. | CKA sử dụng 6 cụm máy ảo độc lập gán cho 20 bài. Không đọc để nhảy mạng nhầm sẽ sai lệch hoàn toàn tệp mục tiêu bài. Điểm bài đó bằng 0. |
| 2 | Mở trình duyệt Web lướt Google tìm cách sửa file lỗi Kubernetes ngay trong giờ thi bật camera. Giám thị sẽ nhấn nút hủy bài kiểm tra. | CKA là kỳ thi chuẩn mạng mở, cho phép bạn vào duy nhất cấu hình 1 trang Web tên là `kubernetes.io/docs`. Tập tìm kiếm YAML tại trang gốc này. | Đây là trang chính thức, mọi thứ tài nguyên như Persistent Volume, Deployment, Probes đều có ví dụ chuẩn trong trang này. Nếu biết cách tìm kiếm ở trang Docs, bạn chỉ cần Sao chép (Copy) về máy ảo trạm bài thi để dán (Paste). |

---

## Bài tập thực hành luyện tập

- [ ] **Bài 1:** Tập sử dụng hệ Linux Terminal thuần không chuột. (Thiết lập công cụ Editor như Vim. Gõ các lệnh xóa 1 chữ, xóa 1 dòng hay 10 dòng tức khắc không dùng nút Delete). Luyện sao chép và dán chữ trên hệ thống.
- [ ] **Bài 2:** Dùng lệnh Imperative Command để mở tệp YAML cấu hình cho việc chạy thử một Máy ảo Pod chứa 2 hộp Container bên trong (1 cái Nginx, 1 cái BusyBox log ảo). Xuất thành file, dùng trình soạn `vim` sửa YAML thêm con thứ 3.
- [ ] **Bài 3:** Thiết lập cụm K8s thực tế tạo bằng tay qua công cụ `Kubeadm` (Đừng dùng Minikube nén). Lấy một đĩa máy ảo Linux Ubuntu, thiết lập từ phần tải CNI Network Flannel. 

---

## Tài nguyên thêm
- [Khóa K8s CKA của Mumshad Mannambeth](https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/) — Khóa học thần thánh nhất luyện thi lấy chứng chỉ CKA. Nó có hệ máy ảo Test y như thật trên mạng web để rèn cấu hình Bash.
- [Trang tài liệu mẫu K8s Exam](https://kubernetes.io/docs/home/) — Trang tra cứu để kéo mẫu YAML. Giấy thông hành duy nhất mang vào phòng thi.
