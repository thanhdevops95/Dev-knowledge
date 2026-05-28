# 🔥 Kubernetes Storage — Giải Quyết Bài Toán Dữ Liệu Vĩnh Cửu

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Hiểu nguyên lý lưu trữ dữ liệu State để triển khai ứng dụng CSDL như MySQL, Redis an toàn trên K8s.
> **Prerequisite:** `09-DevOps/kubernetes/02-kubernetes-advanced.md`

---

## Tại sao Kubernetes gặp vấn đề với lưu trữ?

Triết lý lõi của Kubernetes là **Ephemeral** (Phù du). Điều này có nghĩa là mọi Pod (Container) đều có thể bị hệ thống tiêu diệt bất cứ lúc nào để giải phóng bộ nhớ, hoặc do lỗi phần cứng trên Node.
Khi một Pod chứa PostgreSQL bị xóa đi để khởi động lại ở một máy chủ khác, toàn bộ dữ liệu nằm trong hệ điều hành của Pod đó cũng bị xóa trắng theo.

Kubernetes giải quyết bài toán này thông qua khái niệm ngắt kết nối cấu trúc ổ đĩa ra khỏi vòng đời của Pod. 

---

## 1. Cơ Chế Kết Nối Persistent Volume (PV) & Persistent Volume Claim (PVC)

K8s sử dụng phương thức quản lý tài nguyên ổ cứng thông qua cơ chế người cấp và người xin.

1. **PersistentVolume (PV):** Là một thiết bị lưu trữ vật lý thực tế được định nghĩa trong mạng K8s. Đại diện cho ổ cứng ngoài đời thực đã được máy chủ định dạng, ví dụ ổ cứng trống 100GB cài trên AWS EBS hoặc ổ cứng nội bộ NFS ở máy chủ trong nhà bạn. Do quản trị viên K8s trực tiếp tạo bằng YAML.
2. **PersistentVolumeClaim (PVC):** Đây là đơn xin cấp phát dung lượng. Lập trình viên không cần biết 100GB máy chủ đặt ở đâu, họ tạo PVC yêu cầu K8s: "Cho tôi mượn 10GB ổ đĩa để lưu DB nhanh nhất có thể".
3. **StorageClass (Cấp Độ Lưu Trữ):** Quản trị viên gắn tem chứng nhận tự động. Nếu thấy đơn PVC gửi đến đòi loại ổ cứng "SSD Nhanh Khủng Khiếp", K8s sẽ tự động kết nối API ra ngoài hệ thống Mây AWS, móc vào một ổ SSD EBS vĩnh viễn (Dynamically Provisioning), gửi 10GB đó kết vào Pod. Việc này hoàn toàn tự động!

---

## 2. Các Kiểu Hình Cấp Quyền Đọc Ghi (Access Modes)

Ổ cứng ngoài mạng không giống như ổ C hay máy cá nhân. Nếu bạn có cụm 5 cái MySQL chạy trên 5 cái Node khác nhau, thì việc chia sẻ cùng 1 ổ đĩa đòi hỏi việc quyết định quyền lợi Ghi dữ liệu rất khắt khe để tránh làm gãy bảng nhớ CSDL mạng. K8s quy định 3 loại chuẩn ở PVC:

1. **ReadWriteOnce (RWO):** Thường sử dụng nhất với các Database (Mysql). Ổ đĩa gắn mạng chỉ cho phép đúng MỘT máy chủ duy nhất (Node) truy xuất ghi đọc. Các Node khác bị khóa hoàn toàn quyền để chạy hệ thống lưu trữ tĩnh. Tránh xung đột do tranh ghi CSDL.
2. **ReadOnlyMany (ROX):** Chỉ cho xem. Số lượng giới hạn vô cực các Pod ở mạng 10 Node có thể truy cập đọc dữ liệu chung một ổ. Phù hợp lưu trữ tài liệu Ảnh hoặc Static File của hệ quy trình Website máy Frontend.  
3. **ReadWriteMany (RWX):** Mở hoàn toàn trên hạ tầng chuyên dụng đặc biệt đắt tiền như AWS EFS Hệ mảng Mạng Giao hoặc NFS mạng công ty. Dùng chung cho nhiều máy chủ có thể thao tác Ghi Xóa đọc trên chung khối. Không hoạt động với các ổ cứng phổ thông thường rẻ như EBS vì tính năng vật lý phần cứng mạng.

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình cấu hình PVC với tham số Mode là `ReadWriteMany` trên ổ lưu mạng ổ cứng khối Block thông thường như AWS EBS để chia cho 2 ứng dụng Backend ở 2 Node khác nhau. | Cần cài đặt EBS trên chế độ khóa mạng `ReadWriteOnce`. Chỉ dùng dịch vụ File Mạng (EFS/NFS) cho mạng RWX. | Đám mây EBS là ổ cứng gắn chặn cổng trên phần cứng mạng CPU duy nhất. Không cái ổ vật lý chuẩn khối cứng nào có thể cắm 2 dây cáp song song cùng cho 2 máy Mainboard ở 2 khu vực địa lí mạng cùng đọc một dữ liệu. EBS trên K8s sẽ khóa ngay PVC vì thiết bị từ đám mây AWS báo lỗi. |
| 2 | Kỹ thuật viên không quy định chỉ thị vòng rác `reclaimPolicy` kết cấu của thiết bị lưu PV. Khi Pod Xóa đi lệnh K8s sẽ gỡ và tự nhiên Xóa Đè Toàn Bộ File Ổ Cứng mây mạng PV có sẵn theo chế độ Xóa (`Delete`). | Phải chỉnh đặt hệ bảo toàn PV luôn cố định để trạng thái ở chế độ hệ mạng Giữ Lại (`Retain`) cho các tệp nhạy cảm (CSDL MySQL). | Khi PVC CSDL cũ thiết ở môi trường gỡ lệnh dẹp hệ YAML mạng bị hủy dọn mạng (Gõ kubelete delete pvc), PV là thùng lưu Cloud Mạng Đám cũng bị Hủy lệnh API xóa mây theo vì mây hiểu rằng rác. Bật cài chế độ `Retain` rẽ để K8s buông ổ đĩa mây rớt dưới đám ra độc lập, cho dù Pod có xóa, dữ liệu mạng EBS vật lí CSDL mây bạn khóa mạng tài khoản vẫn không bị tính cước hủy và tệp tồn nguyên vẹn chờ bạn tạo kết Pod mạng khác thu hồi phục cài mạng. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cấu file tạo yaml quy lệnh cấp 1 StorageClass cục định nghĩa loại giao giao bộ Local Storage trên ứng Minikube mạng lưới ở trạm nội máy.
- [ ] **Bài 2:** Thiết yaml yêu cầu thiết lập mảng 1 tệp yêu cầu PVC với dung mảng kích mạng cỡ `1Gi` dùng thông loại lưu trữ `ReadWriteOnce`. Dùng kiểm lệnh mạng Bash `kubectl get pvc` xem lưới trạng của nó báo gắn `Pending` rẽ sang `Bound` hay rỗng mảng.
- [ ] **Bài 3:** Thiết cấu mạng 1 hệ khối mạng Nginx dạng Pod, ở mục định dòng `volumes` nối mạng nó tới số mạng tệp định danh của cái tệp PVC từ bài số 2. Kết luồng mạng ổ ổ ảo mountPath cài lưới mạng định phân gắn đường truyền `/usr/share/nginx/html`. Gõ cấu bash truy cập chạy thẳng hệ ứng `kubectl exec -it` truy mạng lưới gắn tạo một file mạng thư mục HTML rỗng cài mạng trong đó. Tắt xóa máy Pod ảo Nginx, tự cài 1 Pod định lại dùng y hệt PV cũ. Chọc chạy mạng vào và báo thấy tệp html không rớt mất.

---

## Tài nguyên thêm
- [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) — Cẩm rào hướng tài cài mạng dẫn giải mảng phân từ K8s mạng tệp lưới về Cấu Hệ thiết bộ lưu ổ gắn.
- [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) — Hệ Giao Thông Tạo Mạch Cấu Chỉ Cách Lưới Cài Tự Ảo Tự Gọi Ổ Hệ Rẽ Nối API Tạo Cấp EBS Tạo.
