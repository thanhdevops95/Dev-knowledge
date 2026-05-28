# 🔥 Kubernetes Security — Kiến Trúc Tường Lửa K8s Nâng Cao

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Tránh bị lỗ hổng xâm nhập để Hacker chiếm toàn quyền xóa Cụm hệ thống mây bằng kỹ thuật RBAC giới hạn mạng.
> **Prerequisite:** `09-DevOps/kubernetes/03-k8s-networking-advanced.md`

---

## 1. Bảo Quản Hệ Network Policies (Tường Lửa Không Gian Máy)

Nguy hiểm rất lớn của Cụm Kubernetes là theo cài đặt mạng ảo gốc: Mọi Container Pod ở bất cứ khu vực nào đều có thể chọc thẳng kiểm tra dữ liệu kết nối truyền tải bằng giao tiếp với tất cả hàng chục nghìn Pod khác. Bạn chỉ cần 1 Pod sơ hở (bị Hack web mã nguồn mở Frontend), Hacker sẽ từ Pod đó quét lệnh cài tìm CSDL thẳng vào DB mà không gì chặn lại.

**Network Policy** đóng vai trò là Tường lửa cục bộ (Firewall) đặt giữa chính các con Pod nội bộ với nhau trong K8s.

```yaml
# Cấm tất cả Pod lạ chọc vào bộ nhớ CSDL. Trừ phi Pod có dán nhãn là backend.
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cs-db-policy
spec:
  # Gắn khiêng khiên chắn vào hệ CSDL có nhãn database_app
  podSelector:
    matchLabels:
      app: database_app
  policyTypes:
  - Ingress # (Bảo mật đường dữ liệu gọi kết nối Đi Vào mũi tên chọc Pod)
  ingress:
  - from:
    # Chỉ Mở chừa cổng mạng dữ liệu nhận cho các ai gõ cửa dán mã chữ backend
    - podSelector: 
        matchLabels:
          app: backend
    ports:
    - protocol: TCP
      port: 5432
```

---

## 2. RBAC Phân Quyền Vai Trò (Role-Based Access Control)

RBAC quy định cấp bậc khóa hạn người truy cập điều khiển API Cụm máy trạm (Ví dụ lập trình viên mới vào công ty không được phép gọi câu chữ lệnh `kubectl delete db`).
Hệ thống K8s chạy qua các móc nối:
1. **ServiceAccount / User:** Tài khoản cấp phát nhân dạng của Lập trình viên thiết lập hoặc cấu của CI/CD kết nối Pipeline Jenkins.
2. **Role:** Tệp bằng chứng xác lệnh ghi rõ các việc được làm (Khai Tên Lệnh: Ví dụ Role A chỉ được phép Gõ Lệnh cài `Get/List`, không cấp quyền lệnh gọi mạng `Create/Delete`).
3. **RoleBinding:** Sợi dây để thắt nối buộc tài khoản (ServiceAccount) vào Bằng Role quyền trên. Từ đây tài khoản đó phải phục tùng mệnh định đó. Cấm vượt rào.

---

## 3. Pod Security Standards (Giới Hạn Nâng Quyền HĐH)

Mọi Vỏ máy (Pod) thường nằm ẩn chạy trên máy tính Linux Thực của nhà cung AWS ở dưới sàn dưới cùng (Node). Các hacker dùng kỹ năng (Privilege Escalation) từ 1 lõi hổng Code Web, truy vấn nâng tài khoản người dùng thành Root và nhảy thủng cái Pod, nhảy vào quản lý hoàn toàn hệ điều hành Ubuntu máy trạm lõi Thực.

Phải thiết lập bảo khóa bằng định chế chặn `securityContext` cấm khởi chạy chế tác Root trong khai báo K8s:

```yaml
# Bên trong yaml thiết của Deployment
    spec:
      containers:
      - name: app
        image: my-app
        securityContext:
          # Ép chạy user người thường thấp hạng 1000, không được dùng tài khoản 0 (Root máy)
          runAsUser: 1000
          # Cấm cờ cho phép tăng giới cấu quyền rào vĩnh viễn ở máy hđh
          allowPrivilegeEscalation: false 
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấp mã quyền mở API K8s bừa bãi định lệnh tên là chức `ClusterRoleBinding` quyền quản lý Administrator vô bờ bến cho ServiceAccount của Jenkins Pipeline. | Hạn chặt giới vùng tạo lệnh chỉ gán hệ RoleBinding vào duy nhất trong rào 1 `Namespace` nhất định dùng để Test ứng dụng. | Chức `ClusterRole` là quyền thiết lập cho Trùm Máy Ảo Mẹ Mọi Cụm Không Gian. Jenkins rò mật khẩu thiết thì ai có mã đó sẽ thâu xóa thiết diệt toàn bộ Cụm, lấy hết Database hệ trên toàn K8s công ty. Phân quyền chỉ cho nó phá ở thư mục khoang tàu Namespace của riêng Jenkins tải rẽ ứng. |
| 2 | Code Mạng mặc định Cài mạng thiết mạng hệ thống tường lửa lập Firewall Network Policy trên hệ cụm MiniKube nhưng tường firewall cấm chọc lỗi thủng hoàn toàn không chặn được tí nào mạng gửi. | Trạm lập Cài K8s gốc bằng trình cắm Mạng Môi Bộ tạo cài điều luồng ảo Mạng chuyên tương tương thích (CNI Plugin như Calico hoặc thụ Cilium). | Lệnh mốc Network Policy chỉ là Giấy Mệnh Lệnh Khuyến Nghị thông luật. Không có Plugin công an CNI tương thích gác cửa trạm máy (Như hệ Calico ở thiết cài AWS gốc, Minikube dùng CNI sơ đẳng rỗng rẽ cài cấu máy). Thư viện Tường rỗng Không cấm được lưới rẽ tạo. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cấu hình lập trạm Namespace cấp không gian ứng dựng tên `dev-team`. Tạo lưới mã YAML để lập trình trạm Role (Quyền) chỉ được Đọc Tìm (`get`, `list`) đối với đối tượng thiết kế mạng Pod. 
- [ ] **Bài 2:** Thiết kế mã kết buộc RoleBinding buộc khối quyền từ bài số 1 vào trong tài khoản `dev-bot` hệ ServiceAccount phân mạng lập ứng K8s hệ nội. Dùng lệnh mảng gọi báo của lệnh `kubectl auth can-i delete pods --as=system:serviceaccount:dev-team:dev-bot` kiểm lưới xem K8s khóa xóa mạng thành công.
- [ ] **Bài 3:** Thiết mạng cấu hình 1 tập Pod ứng CSDL hệ tĩnh. Cấu thiết 1 tờ Network Policy Tường chặn luồng mọi hệ liên kết đường mạng chạy Ingress vào cấm thiết. Và Gõ kiểm dùng gọi bash thư Cấu mạng PING rẽ lệnh từ Pod Cục ứng gọi thứ 2 bắn thư kết vào Pod DB để rà xác nhận kết nối bị lỗi Drop cấu chặn.

---

## Tài nguyên thêm
- [K8S Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) — Mạch lưới mảng tài mảng lưới liệu chuẩn phân cách thiết bảo Firewall cục cách cấm mở lưới luồng truy cập phân mạng.
- [RBAC Authorization Kubernetes](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) — Hệ Giao Kiến Mạch Trí Danh sách các Bảng Gọi Điều Kiểu Danh từ cấu quyền mảng Nhóm Giới hệ API Server.
