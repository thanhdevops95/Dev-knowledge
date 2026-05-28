# Bài 59 — RBAC + ServiceAccount + Role/RoleBinding 🔴

> **Tiên quyết:** Hoàn thành Bài 58; hiểu cluster API và `kubectl`.
> **File:** `serviceaccount.yaml`, `role.yaml`, `rolebinding.yaml`, `clusterrole.yaml`, `clusterrolebinding.yaml`.

## Lệnh thủ công

```bash
# 1. Tạo ServiceAccount
kubectl apply -f serviceaccount.yaml

# 2. Tạo Role (namespace-scoped) + RoleBinding
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml

# 3. Tạo ClusterRole (cluster-wide) + ClusterRoleBinding
kubectl apply -f clusterrole.yaml
kubectl apply -f clusterrolebinding.yaml

# 4. Verify quyền bằng kubectl auth can-i
kubectl auth can-i list pods -n myapp-dev \
  --as=system:serviceaccount:myapp-dev:myapp-sa
# yes

kubectl auth can-i delete pods -n myapp-dev \
  --as=system:serviceaccount:myapp-dev:myapp-sa
# no

kubectl auth can-i list nodes \
  --as=system:serviceaccount:myapp-dev:myapp-sa
# yes (nhờ ClusterRoleBinding)

# 5. Xem trong cluster
kubectl get sa -n myapp-dev
kubectl get role,rolebinding -n myapp-dev
kubectl get clusterrole,clusterrolebinding | grep myapp
```

## Kết quả mong đợi

- `kubectl get sa myapp-sa -n myapp-dev` thấy SA.
- `kubectl auth can-i list pods --as=...` → `yes`.
- `kubectl auth can-i delete pods --as=...` → `no`.
- `kubectl auth can-i list nodes --as=...` → `yes`.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `Forbidden` khi pod gọi API | RB chưa bind đúng SA; verify `kubectl auth can-i --as=...` |
| RB trỏ Role ở namespace khác | RB & Role cùng namespace mới hợp lệ |
| Nhầm `Role` với `ClusterRole` trong `roleRef` | RB trỏ ClusterRole vẫn được (tái sử dụng), nhưng phạm vi áp dụng vẫn 1 namespace |

## Phân biệt nhanh

| Cặp | Khác chỗ nào |
|-----|--------------|
| `Role` vs `ClusterRole` | Role chỉ trong 1 namespace · ClusterRole áp dụng cluster-wide (Node, PV...) |
| `RoleBinding` vs `ClusterRoleBinding` | RB bind ở namespace · CRB bind cluster-wide |
| `subjects` vs `roleRef` | subjects = AI được trao quyền · roleRef = quyền GÌ |

## Câu hỏi

- Role vs ClusterRole — chính xác khác chỗ nào?
- Nếu app KHÔNG cần gọi K8s API, có cần SA không?
  *(Mỗi pod luôn có default SA. Nếu không cần API → `automountServiceAccountToken: false` để giảm attack surface.)*

## Bài kế tiếp

```bash
cd ../60-networkpolicy
```
