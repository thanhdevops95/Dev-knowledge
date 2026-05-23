# 🔥 GitOps Practices — Quản Lý Triển Khai Bằng Nền Tảng Git

> `[ADVANCED]` ⭐ `[MUST-KNOW]` — Thay đổi phương pháp cài đặt hệ thống từ việc thao tác bằng câu lệnh sang cấu hình lưu kho hoàn toàn bằng Github.
> **Prerequisite:** `09-DevOps/kubernetes/01-kubernetes-basics.md`, `09-DevOps/cicd/04-argocd-gitops-basics.md`

---

## 1. Bản Chất Hoạt Động Của GitOps

Nguyên lý duy nhất của GitOps: "Tài liệu lưu trên kho Git là nguồn sự thật duy nhất (Single Source of Truth) quyết định trạng thái mạng của hệ thống".

Ở kiểu cũ (Ops truyền thống): 
Người vận hành muốn nâng cấu hình máy ảo lên 5 RAM. Họ mở Console lệnh Bash, gõ lệnh `kubectl edit deployment` và cấu hình hệ thống máy chạy ở hạ tầng tăng lên 5.
Nhưng đồng nghiệp của anh ta không nhìn vào lệnh Console đó. Khi cần cài mới, họ lại đưa mã lệnh cũ ở công ty vào (Cấu hình là 3 RAM). Hệ thống bị xung đột (Drift state).

Ở kiểu GitOps (Sử dụng ArgoCD/Flux): 
Hệ thống Kubernetes bị cấm hoàn toàn hành động cho phép người dùng gõ lệnh bằng tay.
1. Bạn sửa file `deployment.yaml` trên Github, tăng con số RAM lên 5.
2. Công cụ GitOps Agent (Cài sẵn trong lõi Kubernetes) cứ 1 phút lại tải mã trên Github về 1 lần.
3. Node K8s đọc thấy file YAML Github vừa đổi thành 5, nó tự động áp dụng mạng lên Cụm máy cục bộ.
Không ai có quyền thao tác trực tiếp với máy chủ. Mọi lịch sử điều chỉnh cấu hình mạng đều được máy trạm máy ghi log ở nhánh commit của GitHub.

---

## 2. Tổ Chức Thư Mục Mã Cho Hai Trạm Kho Repo Git

Khi áp dụng GitOps, bạn tuyệt đối không được để chung mã lập trình (Application Code - Node.js web) vào một kho với mã cơ sở hạ tầng (Infrastructure Code - K8s yaml/ArgoCD). Mọi hệ thống chuẩn sẽ yêu cầu cắt mạng 2 luồng rõ ràng.

1. **Kho Ứng Lập Trình (App Repo):** Các tệp thư chứa lệnh hàm React hay Python. Đội kỹ thuật Dev chỉ tải code vào đây. Khi code được sếp duyệt qua Pull Request, hệ lệnh mạng CI (Github Actions) sẽ nén máy ảnh Docker mới và đóng dấu phiên bản nhánh `v1.2.0`.
2. **Kho Cấu Hạ Tầng Mạng (Infra Repo):** Kho này thuần trạm chứa các mã mạng K8s YAML định dạng. Sau khi nhánh CI App ở trên tải nhãn `v1.2.0`. Nó đánh lệnh gọi sang Kho Infra này, yêu cầu sửa text số ở file `values.yaml` của Kubernetes Helm đổi Image tag thành chữ `v1.2.0`. 
Sau đó máy trạm ArgoCD sẽ làm nốt công việc nhận bản thiết lập mới và cập nhật K8s.

---

## Gotchas

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cấp quyền sửa trực tiếp cấu mạng cho Ops thao tác gõ mã cập rẽ máy trạm `kubectl apply` từ thiết thiết bị cá nhân ở máy nhà. | Hủy khóa và thu hồi mọi quyền điều lệnh máy (Write Access API) với bất kì cài giao nhân nào trên Cụm máy API Mạng thật AWS. | Khi ứng dụng phương châm mạng GitOps cấu K8s, Git mã lệnh trạm đóng vai trò đại diện lệnh cập nhật duy nhất. Việc kĩ thuật viên áp tay lệnh hệ bash gây mất đồng bộ với thông mạng GitHub. |
| 2 | Giữ tập lưu file vòng bí mật Database Mạng (Secret) thẳng ở chữ text trong kho Hạ Tầng Thiết Github. | Áp Hàm mã Lệnh mã hóa tệp chữ API Bắn Cấu Sealed Secrets lưới hoặc sử cấu quản API Vault cài trạm để nhét khóa che trước Github thiết. | Github là mã mạng chữ tĩnh dạng kho lưu công cộng hoặc dễ chép (Bị sao chép lệnh rẽ bản ổ). Dữ liệu mã hóa hệ Secret băm văn bản hệ phải được công cụ API che mã khóa mật thiết lập trước. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cài máy lập mạng cấu ArgoCD tại Local. Lệnh tải file mạng Kubernetes App định Cấu Bảng từ Github Public Repo mã của tài hàm khoản thực bạn rồi ép đồng lệnh Bộ Mạng qua ArgoCD Lệnh máy.
- [ ] **Bài 2:** Thử sửa lệnh mã bản YAML ở kho GitHub. Chọn lệnh thiết Ứng dụng số Repilcas (Số lượng vỏ Pod ảo) thay đổi số 1 Lệnh về 3. Về Dashboard của ArgoCD trạm cục bộ chờ 3 phút và quan sát mạng nó tự sinh.

---

## Tài nguyên thêm
- [Weaveworks Guide To GitOps Lệnh](https://www.weave.works/technologies/gitops/) — Bài đọc định danh phương châm cấu lập tạo văn lệnh hóa thiết cấu hệ mạng GitOps nguyên thủy gốc.
