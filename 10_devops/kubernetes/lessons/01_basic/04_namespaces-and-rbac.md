# 🎓 Namespaces Và RBAC: Thiết Lập Biên Giới An Ninh Và Phân Quyền Hạn Chế Tối Đa

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [ConfigMaps & Secrets](03_configmaps-and-secrets.md)

> 🎯 **Mục tiêu cốt lõi:** Làm chủ **Namespaces** (mô hình multi-tenancy), **ResourceQuota** + **LimitRange** để quản lý tài nguyên, và hệ thống phân quyền **RBAC** (ClusterRole, Role, RoleBinding, ClusterRoleBinding, ServiceAccount). Bạn sẽ biết cách sử dụng `kubectl auth can-i` để gỡ lỗi phân quyền và thiết lập môi trường multi-team an toàn tuyệt đối trên Production.

---

## 🎯 Sau bài này bạn sẽ

- [x] Thấu suốt bản chất **Namespace** — Biên giới ảo cô lập tài nguyên logical.
- [x] Cấu hình thành thạo **ResourceQuota** + **LimitRange** để kiểm soát tài nguyên của từng đội ngũ.
- [x] Nắm vững **RBAC** qua 4 mảnh ghép: Role, ClusterRole, RoleBinding và ClusterRoleBinding.
- [x] Hiểu sâu về **ServiceAccount** — Định danh và cấp quyền cho ứng dụng chạy trong Pod.
- [x] Sử dụng thành thạo **`kubectl auth can-i`** để kiểm tra và gỡ lỗi phân quyền nhanh chóng.
- [x] Vận dụng các mô hình thực chiến: Tách biệt môi trường (Dev/Staging/Prod) và cô lập đội ngũ.
- [x] Nhận diện và phòng tránh 5 sai lầm chí mạng về bảo mật an ninh K8s.

---

## Tình huống thực tế: Cơn ác mộng dùng chung K8s Cluster

Bạn vừa thiết lập một K8s Cluster cực kỳ mạnh mẽ cho công ty. Mọi thứ đang chạy trơn tru cho đến khi ban giám đốc yêu cầu chia sẻ Cluster này cho 3 đội ngũ cùng sử dụng:
* **Team Backend (FastAPI):** Cần deploy liên tục các dịch vụ API cốt lõi.
* **Team Frontend (React):** Deploy các trang giao diện static và Web App.
* **Team Data Science (ML Jobs):** Chạy các tác vụ huấn luyện mô hình tốn rất nhiều tài nguyên CPU/RAM.

Nếu để cấu hình mặc định, thảm họa sẽ lập tức xảy ra:
1. 💸 **Mất kiểm soát tài nguyên:** Team Data chạy một Job huấn luyện mô hình ML bị lỗi vòng lặp vô hạn, "nuốt trửng" 100% CPU/RAM của Cluster, khiến dịch vụ FastAPI của Team Backend bị sập hàng loạt.
2. 🔒 **Thiếu an toàn bảo mật:** Một lập trình viên Junior của Team Frontend vô tình gõ nhầm lệnh `kubectl delete pods --all` và xóa sạch toàn bộ hệ thống API của Team Backend đang chạy thử nghiệm.
3. 🤖 **Đặc quyền CI/CD quá lớn:** Tài khoản CI/CD Bot của công ty được cấp quyền cao nhất (Cluster Admin) để deploy. Nếu hacker chiếm được token của bot này, toàn bộ hệ thống Cluster sẽ bị kiểm soát hoàn toàn.

Bạn hoang mang tự hỏi:
* *Làm sao để chia Cluster thành các "khu vực biệt lập" cho từng đội ngũ?*
* *Làm thế nào để giới hạn Team Data chỉ được dùng tối đa 40GB RAM và 10 CPU?*
* *Cơ chế nào giúp giới hạn quyền của từng người dùng và từng con Bot theo nguyên tắc đặc quyền tối thiểu (Least Privilege)?*

Đừng lo lắng, K8s đã thiết kế sẵn hai cơ chế cực kỳ mạnh mẽ để giải quyết triệt để nỗi đau này: **Namespaces** (Phân vùng tài nguyên) và **RBAC** (Phân quyền truy cập). Hãy cùng mình khám phá chi tiết ngay sau đây!

---

## 1️⃣ Namespaces Là Gì: Biên Giới Ảo Hay Bức Tường Lửa Thật Sự?

**Namespace** giống như các thư mục (folder) ảo trên máy tính của bạn. Thay vì cài đặt mọi phần mềm chung một chỗ, bạn chia chúng vào các thư mục `C:\Backend`, `C:\Frontend` để dễ quản lý. 

Khi bạn vừa cài đặt xong Kubernetes, hệ thống đã tự động tạo sẵn 4 Namespace mặc định:

```bash
# Liệt kê các Namespace hiện có trong Cluster
kubectl get namespaces

# OUTPUT mẫu:
# NAME              STATUS   AGE
# default           Active   2d     ← Nơi chứa các tài nguyên nếu bạn không khai báo Namespace
# kube-system       Active   2d     ← Nơi chứa các thành phần cốt lõi của K8s (API Server, DNS...)
# kube-public       Active   2d     ← Namespace công cộng, mọi người dùng đều có quyền đọc
# kube-node-lease   Active   2d     ← Nơi quản lý dữ liệu kiểm tra trạng thái sống (heartbeat) của Node
```

### Tạo Namespace Thế Nào Cho Chuẩn GitOps?

Để tạo Namespace mới, bạn có thể dùng lệnh nhanh hoặc khai báo qua tệp tin YAML để lưu trữ vào hệ thống Git kiểm soát phiên bản.

> [!TIP]
> Trên môi trường Production, luôn ưu tiên sử dụng YAML để khai báo Namespace nhằm dễ dàng quản lý và cấu hình các thẻ nhãn (Labels) cần thiết cho NetworkPolicy hoặc Service Mesh.

```yaml
# file: 00_team-a_namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
  labels:
    team: backend
    env: production     # Dùng nhãn này để áp dụng luật bảo mật hoặc định tuyến
```

```bash
# Tạo Namespace bằng lệnh nhanh
kubectl create namespace team-b

# Tạo Namespace chuẩn hóa từ file YAML
kubectl apply -f 00_team-a_namespace.yaml
```

### Sử Dụng Namespace Để Gom Nhóm Workload Ra Sao?

Mặc định, công cụ CLI `kubectl` sẽ thao tác trên Namespace `default`. Để thao tác với các tài nguyên ở Namespace khác, bạn bắt buộc phải truyền thêm cờ `-n <tên-namespace>` vào cuối câu lệnh.

```bash
# Xem danh sách Pod trong Namespace production
kubectl get pods -n production

# Deploy ứng dụng từ tệp manifest vào Namespace staging
kubectl apply -f app-deployment.yaml -n staging

# Xem nhật ký logs của một Pod thuộc Namespace production
kubectl logs fastapi-app-7d5f8b9b4f-abcde -n production
```

Để tránh việc phải gõ đi gõ lại cờ `-n`, bạn có thể đổi Namespace mặc định cho phiên làm việc hiện tại bằng lệnh sau:

```bash
# Thay đổi Namespace mặc định của ngữ cảnh hiện tại sang production
kubectl config set-context --current --namespace=production
```

> [!NOTE]
> **Cơ chế gọi dịch vụ liên Namespace (Cross-Namespace DNS):**
> Các Pod ở các Namespace khác nhau vẫn có thể kết nối với nhau thông qua tên miền DNS có cấu trúc đầy đủ (FQDN):
> `http://<tên-dịch-vụ>.<tên-namespace>.svc.cluster.local`
> Ví dụ: Một ứng dụng FastAPI ở Namespace `default` muốn kết nối tới cơ sở dữ liệu PostgreSQL ở Namespace `production` sẽ gọi địa chỉ: `http://postgres-service.production.svc.cluster.local:5432`.

### Những Tài Nguyên Nào Bị Giới Hạn Bởi Namespace, Những Gì Thuộc Về Cluster?

Không phải mọi đối tượng trong Kubernetes đều nằm trong một Namespace. Chúng được chia làm hai nhóm rõ rệt:

| Tài nguyên thuộc Namespace (Namespaced) | Tài nguyên thuộc Cluster (Cluster-scoped) |
| :--- | :--- |
| **Workloads:** Pod, Deployment, StateFulSet, Job, CronJob | **Hạ tầng:** Node (Máy chủ vật lý/ảo) |
| **Mạng & Cấu hình:** Service, Ingress, ConfigMap, Secret | **Lưu trữ:** PersistentVolume (PV), StorageClass |
| **Bảo mật:** Role, RoleBinding, ServiceAccount | **Bảo mật Cluster:** ClusterRole, ClusterRoleBinding |
| **Chính sách:** NetworkPolicy, ResourceQuota | **Cấu hình mở rộng:** Namespace, CustomResourceDefinition (CRD) |

Bạn có thể chạy lệnh sau để biết chính xác tài nguyên nào thuộc nhóm nào:

```bash
# Xem các tài nguyên thuộc Namespace (Trả về true/false)
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```

### Phân Chia Namespace Trong Thực Tế Theo Những Mô Hình Nào?

Tùy vào quy mô của công ty, bạn có thể chọn một trong các mô hình thiết kế phân vùng Namespace sau:

* **Mô hình 1: Theo Môi Trường (Per Environment):** Phù hợp với công ty quy mô vừa và nhỏ.
  * `development` (Phát triển thử nghiệm)
  * `staging` (Kiểm thử hệ thống)
  * `production` (Hệ thống chạy thực tế)
* **Mô hình 2: Theo Đội Ngũ (Per Team):** Phù hợp với doanh nghiệp lớn có nhiều phòng ban độc lập.
  * `team-frontend`
  * `team-backend`
  * `team-data-science`
* **Mô hình 3: Theo Khách Hàng (Per Tenant - SaaS Multi-tenancy):**
  * `customer-apple`
  * `customer-samsung`

### Sai Lầm Chí Mạng: Tại Sao Namespace Không Thể Thay Thế Cluster Vật Lý?

> [!WARNING]
> **Namespace KHÔNG phải là một hàng rào bảo mật tuyệt đối!**
> Đây là hiểu lầm cực kỳ nguy hiểm của nhiều DevOps Junior. Về bản chất, các Pod ở Namespace khác nhau vẫn chạy chung nhân OS (Kernel) của Node vật lý, vẫn có thể ping thấy nhau qua mạng nội bộ (mặc định) và dùng chung tài nguyên đĩa cứng. 
> 
> * **Giải pháp bảo mật mạng:** Sử dụng **NetworkPolicy** để chặn đứng các kết nối trái phép giữa các Namespace.
> * **Giải pháp cô lập tuyệt đối:** Đối với các tác vụ chạy mã nguồn không đáng tin cậy (untrusted code) hoặc yêu cầu chứng chỉ bảo mật nghiêm ngặt (như PCI-DSS), bạn **bắt buộc** phải sử dụng các **K8s Cluster vật lý độc lập** hoặc các giải pháp Virtual Cluster (như *vcluster*, *gVisor*).

---

## 2️⃣ ResourceQuota: Làm Sao Để Một Đội Ngũ Không "Nuốt Chửng" Toàn Bộ Cluster?

Khi dùng chung nhà, nếu một người bật máy lạnh 24/7 và dùng hết sạch dung lượng Internet, những người còn lại sẽ chịu thiệt thòi. **ResourceQuota** chính là "hạn mức chi tiêu" mà bạn áp đặt lên một Namespace để khống chế tổng tài nguyên tối đa mà Namespace đó được phép tiêu thụ.

Hãy xem tệp cấu hình ResourceQuota thực tế dưới đây:

```yaml
# file: 01_team-a_resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-a-quota
  namespace: team-a       # Áp dụng trực tiếp vào Namespace của Team A
spec:
  hard:
    # --- Hạn mức tài nguyên tính toán ---
    requests.cpu: "4"           # Tổng CPU yêu cầu tối thiểu không vượt quá 4 Core
    requests.memory: "8Gi"      # Tổng RAM yêu cầu tối thiểu không vượt quá 8 GB
    limits.cpu: "8"             # Tổng CPU tối đa không vượt quá 8 Core
    limits.memory: "16Gi"       # Tổng RAM tối đa không vượt quá 16 GB

    # --- Hạn mức số lượng đối tượng ---
    pods: "20"                  # Tối đa chỉ được chạy 20 Pod cùng lúc
    services: "10"              # Tối đa chỉ được tạo 10 Service
    services.loadbalancers: "1" # Tối đa chỉ được tạo 1 dịch vụ LoadBalancer (đắt tiền)
    secrets: "15"               # Tối đa chỉ được tạo 15 Secret
    configmaps: "15"            # Tối đa chỉ được tạo 15 ConfigMap
    persistentvolumeclaims: "3" # Tối đa chỉ được yêu cầu 3 ổ đĩa lưu trữ (PVC)
```

Áp dụng hạn mức này vào Cluster:

```bash
kubectl apply -f 01_team-a_resource-quota.yaml
```

Kiểm tra trạng thái sử dụng hạn mức hiện tại:

```bash
kubectl describe quota -n team-a

# OUTPUT mẫu:
# Resource               Used  Hard
# --------               ----  ----
# configmaps             2     15
# limits.cpu             1     8
# limits.memory          2Gi   16Gi
# pods                   3     20
# requests.cpu           500m  4
# requests.memory        1Gi   8Gi
# secrets                4     15
# services               2     10
```

> [!IMPORTANT]
> Một khi tổng tài nguyên của Namespace đạt trần giới hạn (Hard Limit), bất kỳ yêu cầu tạo Pod hoặc tài nguyên mới nào vượt quá hạn mức này sẽ lập tức bị API Server của Kubernetes từ chối thẳng thừng với mã lỗi `Exceeded Quota`.

---

## 3️⃣ LimitRange: Làm Sao Để Tránh Tình Trạng Pod Không Khai Báo CPU/RAM?

ResourceQuota giải quyết bài toán khống chế tổng tài nguyên của cả Namespace. Tuy nhiên, nếu một lập trình viên deploy một Pod mà quên không khai báo thông số `resources.requests` và `resources.limits`, Pod đó có thể phình to vô hạn và chiếm dụng tài nguyên của các Pod khác trong cùng Namespace.

**LimitRange** ra đời để thiết lập các "luật biên giới" cho từng Container/Pod đơn lẻ chạy trong Namespace. Nó tự động gán giá trị mặc định (Default) nếu lập trình viên quên khai báo, đồng thời khống chế khoảng tài nguyên tối thiểu (Min) và tối đa (Max) mà một Container được phép khai báo.

```yaml
# file: 02_team-a_limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: team-a-limits
  namespace: team-a
spec:
  limits:
  - type: Container
    # --- Giá trị tự động gán nếu Pod không khai báo ---
    default:                    # Tự động gán limits (trần trên)
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:             # Tự động gán requests (định mức chạy)
      cpu: "100m"
      memory: "256Mi"
      
    # --- Giới hạn bắt buộc của một Container ---
    max:                        # Container không được phép khai báo vượt quá mức này
      cpu: "2"
      memory: "4Gi"
    min:                        # Container bắt buộc phải khai báo tối thiểu mức này
      cpu: "50m"
      memory: "64Mi"
```

Áp dụng quy định này:

```bash
kubectl apply -f 02_team-a_limit-range.yaml
```

### Sự Khác Biệt Giữa ResourceQuota Và LimitRange Là Gì?

Để dễ nhớ, bạn có thể so sánh hai khái niệm này qua bảng sau:

| Đặc trưng | ResourceQuota (Hạn Mức Vùng) | LimitRange (Luật Biên Giới Pod) |
| :--- | :--- | :--- |
| **Phạm vi áp dụng** | Toàn bộ Namespace cộng dồn lại. | Từng Container / Pod đơn lẻ. |
| **Mục đích cốt lõi** | Giới hạn ngân sách, tránh một đội chiếm dụng toàn bộ Cluster. | Đảm bảo mọi Pod đều có khai báo tài nguyên; chặn Pod quá dị biệt. |
| **Ví dụ thực tế** | *"Tổng dung lượng RAM của cả Team A không được quá 16GB."* | *"Một chiếc Pod bất kỳ tối thiểu phải chạy với 64MB RAM, mặc định gán 256MB."* |

---

## 4️⃣ RBAC: 4 Mảnh Ghép Xây Dựng Bản Đồ Quyền Lực Trong K8s

**RBAC (Role-Based Access Control)** là cơ chế kiểm soát truy cập dựa trên vai trò. Nó trả lời câu hỏi cốt lõi: **Ai (Subject) được phép làm gì (Verbs) trên tài nguyên nào (Resources)?**

Hệ thống RBAC của Kubernetes được xây dựng vững chắc trên 4 mảnh ghép chính:

```
                  +---------------------------+
                  |    ĐỐI TƯỢNG (Subject)    | -> (User, Group, ServiceAccount)
                  +---------------------------+
                                |
                                | liên kết bằng (Binding)
                                V
                  +---------------------------+
                  |  BẢN LIÊN KẾT (Binding)  | -> (RoleBinding, ClusterRoleBinding)
                  +---------------------------+
                                |
                                | trỏ đến danh mục quyền
                                V
                  +---------------------------+
                  |    DANH MỤC QUYỀN (Role)  | -> (Role, ClusterRole)
                  +---------------------------+
```

### Subject: Quyền Này Trao Cho Ai?

Có 3 nhóm đối tượng có thể được cấp quyền trong K8s:
1. **User (Người dùng):** Con người thực tế (ví dụ: Lập trình viên `alice@company.com`). K8s không tự quản lý danh sách User mà xác thực qua các hệ thống bên ngoài như chứng chỉ SSL Client, OIDC (Google/Okta), v.v.
2. **Group (Nhóm người dùng):** Tập hợp các User (ví dụ: Nhóm `dev-team`).
3. **ServiceAccount (Tài khoản dịch vụ):** Dành cho robot, các công cụ CI/CD, hoặc chính các ứng dụng chạy bên trong Pod cần giao tiếp với K8s API.

### Role: Phân Quyền Giới Hạn Trong Một Namespace

**Role** định nghĩa một tập hợp các hành động được phép thực hiện trên các tài nguyên, nhưng **bị giới hạn nghiêm ngặt trong phạm vi của một Namespace cụ thể**.

```yaml
# file: 03_developer_role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-manager
  namespace: team-a               # Chỉ có tác dụng trong Namespace team-a
rules:
- apiGroups: [""]                 # "" đại diện cho Core API Group (chứa Pods, Services, ConfigMaps...)
  resources: ["pods", "pods/log", "pods/status"] # Các tài nguyên được phép thao tác
  verbs: ["get", "list", "watch", "update", "patch"] # Các hành động được phép làm

- apiGroups: ["apps"]             # Nhóm API chứa Deployment, StatefulSet...
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"] # Lập trình viên có thể restart/scale deployment
```

### ClusterRole: Sức Mạnh Toàn Cluster

Khác với Role, **ClusterRole** định nghĩa các quyền hạn không bị giới hạn bởi Namespace. Nó được dùng cho các tài nguyên cấp Cluster (như Node, PersistentVolume) hoặc để phân quyền đồng nhất trên toàn bộ tất cả Namespace.

```yaml
# file: 04_cluster-reader_cluster-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-resource-viewer   # Không khai báo trường namespace vì đây là đối tượng cấp Cluster
rules:
- apiGroups: [""]
  resources: ["nodes", "persistentvolumes"] # Xem thông tin phần cứng và ổ đĩa của toàn hệ thống
  verbs: ["get", "list", "watch"]
```

### Những ClusterRole Có Sẵn Cực Kỳ Tiện Lợi

Kubernetes đã tinh ý tạo sẵn 4 ClusterRole tiêu chuẩn để bạn sử dụng ngay lập tức mà không cần tự viết:
* **`cluster-admin`:** Quyền tối cao (Superuser). Có thể làm mọi thứ trên toàn Cluster.
* **`admin`:** Quyền quản trị tối cao **nhưng chỉ trong giới hạn một Namespace** (khi kết hợp với RoleBinding).
* **`edit`:** Quyền đọc và ghi (Read-Write) hầu hết tài nguyên trong Namespace, ngoại trừ quyền sửa đổi RBAC (không thể tự cấp thêm quyền cho mình hoặc người khác).
* **`view`:** Quyền chỉ đọc (Read-Only) tất cả tài nguyên trong Namespace.

### RoleBinding: Gán Role Cho Subject Trong Namespace

**RoleBinding** là chiếc cầu nối gắn kết một **Role** (hoặc một **ClusterRole**) với một **Subject** (User/Group/ServiceAccount) bên trong phạm vi một Namespace cụ thể.

```yaml
# file: 05_alice-binding_role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: alice-pod-manager-binding
  namespace: team-a               # Quyền này chỉ có hiệu lực tại Namespace team-a
subjects:
- kind: User
  name: alice@company.com         # Tên định danh của lập trình viên Alice
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-manager               # Trỏ tới Role đã định nghĩa ở trên
  apiGroup: rbac.authorization.k8s.io
```

> [!TIP]
> Bạn có thể bind một **ClusterRole** với một **RoleBinding**! Quyền hạn trong ClusterRole đó sẽ lập tức bị "thu nhỏ" lại và chỉ có tác dụng bên trong Namespace khai báo ở RoleBinding. Đây là mẹo cực hay để tái sử dụng các ClusterRole mặc định như `view` hay `edit` cho từng Namespace mà không phải viết lại nhiều lần.

### ClusterRoleBinding: Gán Quyền Lực Trên Toàn Cluster

Nếu bạn muốn cấp quyền cho một ai đó truy cập tài nguyên trên **toàn bộ tất cả Namespace** hoặc thao tác với tài nguyên cấp Cluster (như Node), bạn phải dùng **ClusterRoleBinding**.

```yaml
# file: 06_bob-binding_cluster-role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: bob-cluster-view-binding  # Không có trường namespace
subjects:
- kind: User
  name: bob@company.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-resource-viewer   # Trỏ tới ClusterRole cấp Cluster ở trên
  apiGroup: rbac.authorization.k8s.io
```

### Verbs: Những Động Từ Định Đoạt Hành Động

Các hành động trong RBAC được mô tả bằng các động từ (Verbs) tiêu chuẩn:

| Động từ (Verbs) | Hành động tương đương trong REST API | Ý nghĩa thực tế |
| :--- | :--- | :--- |
| **`get`** | GET (đơn lẻ) | Xem chi tiết thông tin của 1 đối tượng cụ thể. |
| **`list`** | GET (danh sách) | Liệt kê toàn bộ danh sách các đối tượng. |
| **`watch`** | GET (truyền phát) | Lắng nghe các thay đổi thời gian thực của đối tượng. |
| **`create`** | POST | Tạo mới một tài nguyên. |
| **`update`** | PUT | Cập nhật đè lên tài nguyên hiện có. |
| **`patch`** | PATCH | Cập nhật một phần thông tin của tài nguyên. |
| **`delete`** | DELETE | Xóa một tài nguyên cụ thể. |
| **`deletecollection`** | DELETE (danh sách) | Xóa hàng loạt tài nguyên cùng lúc. |

---

## 5️⃣ ServiceAccount: Làm Sao Để Pod Tự Chứng Minh Danh Tính Với K8s API?

Khi một Pod (ứng dụng) chạy bên trong Cluster cần thực hiện các thao tác tự động hóa với Kubernetes API Server (ví dụ: Một ứng dụng Python cần liệt kê danh sách các Pod khác để tự động khám phá dịch vụ), nó cần một danh tính để xác thực. Danh tính đó chính là **ServiceAccount**.

Mặc định, mọi Namespace đều có sẵn một ServiceAccount tên là `default`. Nếu bạn không chỉ định rõ ràng, mọi Pod được tạo ra sẽ tự động sử dụng ServiceAccount này và tự động gắn (mount) một mã JWT Token bảo mật vào thư mục: `/var/run/secrets/kubernetes.io/serviceaccount/token`.

```bash
# Thử đọc token bảo mật tự động gắn bên trong một Pod bất kỳ
kubectl exec -it my-fastapi-pod-xyz -- cat /var/run/secrets/kubernetes.io/serviceaccount/token

# OUTPUT: Một chuỗi JWT siêu dài bắt đầu bằng 'eyJhbGciOiJSUzI1NiIs...'
```

### Khởi Tạo Một ServiceAccount Chuyên Biệt Như Thế Nào?

> [!WARNING]
> Trên môi trường Production, không bao giờ dùng chung ServiceAccount `default` cho các tác vụ đặc thù. Hãy luôn áp dụng nguyên tắc **đặc quyền tối thiểu** bằng cách tạo riêng ServiceAccount cho từng ứng dụng cần quyền truy cập API.

```yaml
# file: 07_ci-bot_service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: github-ci-bot
  namespace: team-a               # Nằm trong Namespace team-a
```

### Khai Báo Sử Dụng ServiceAccount Trong Pod Ra Sao?

Bạn chỉ định ServiceAccount muốn sử dụng thông qua trường `spec.serviceAccountName` trong cấu hình Pod:

```yaml
# file: 08_api-pod_with-sa.yaml
apiVersion: v1
kind: Pod
metadata:
  name: internal-api-operator
  namespace: team-a
spec:
  serviceAccountName: github-ci-bot # Sử dụng tài khoản dịch vụ chuyên biệt
  containers:
  - name: python-operator
    image: python:3.10-slim
    command: ["sleep", "3600"]
```

### Trao Quyền Cho ServiceAccount Giữa Các Namespace Thế Nào?

Một con Bot chạy ở Namespace `team-a` hoàn toàn có thể được cấp quyền tác động lên Namespace `production` nếu bạn khai báo chính xác trong cấu hình RoleBinding:

```yaml
# file: 09_bot-cross-ns_role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cross-ns-deploy-binding
  namespace: production           # Quyền này có hiệu lực trên Namespace production
subjects:
- kind: ServiceAccount
  name: github-ci-bot
  namespace: team-a               # Chỉ rõ ServiceAccount này đến từ Namespace team-a
roleRef:
  kind: ClusterRole
  name: edit                      # Cấp quyền edit các tài nguyên trong namespace production
  apiGroup: rbac.authorization.k8s.io
```

### Vô Hiệu Hóa Token Automount Để Bảo Mật Tối Đa

Nếu ứng dụng của bạn chỉ làm nhiệm vụ xử lý logic nghiệp vụ thông thường (như một Web API kết nối Database) mà không có bất kỳ nhu cầu nào giao tiếp với Kubernetes API Server, việc tự động gắn Token bảo mật vào Pod là một lỗ hổng bảo mật tiềm ẩn. 

Nếu tin tặc tấn công và chiếm quyền điều khiển Pod, chúng sẽ lấy được token này để dò tìm các lỗ hổng khác trong Cluster. Bạn hãy tắt tính năng này đi bằng cách cấu hình:

```yaml
spec:
  # Vô hiệu hóa việc tự động gắn mã token bảo mật K8s vào Pod
  automountServiceAccountToken: false
  containers:
  - name: my-secure-app
    image: my-app:latest
```

---

## 6️⃣ `kubectl auth can-i`: Làm Sao Để Tự Kiểm Tra Quyền Hạn Trước Khi Gặp Lỗi?

Khi bạn thiết lập hệ thống phân quyền phức tạp, việc người dùng hoặc công cụ CI/CD báo lỗi *"I cannot do X"* diễn ra rất thường xuyên. Thay vì phải cấu hình thử và đợi hệ thống báo lỗi, Kubernetes cung cấp cho bạn một công cụ kiểm tra quyền lực cực kỳ tiện lợi: `kubectl auth can-i`.

```bash
# --- 1. Tự kiểm tra quyền hạn của chính bạn ---
# Mình có quyền tạo Pod trong Namespace hiện tại không?
kubectl auth can-i create pods
# KẾT QUẢ: yes

# Mình có quyền xóa Node vật lý của Cluster không?
kubectl auth can-i delete nodes
# KẾT QUẢ: no

# --- 2. Giả lập quyền hạn của người khác (Yêu cầu bạn phải có quyền admin để giả lập) ---
# Kiểm tra xem lập trình viên Alice có thể lấy Secret ở Namespace production không?
kubectl auth can-i get secrets -n production --as=alice@company.com
# KẾT QUẢ: no

# Kiểm tra xem ServiceAccount github-ci-bot có quyền update deployment ở production không?
kubectl auth can-i update deployments -n production --as=system:serviceaccount:team-a:github-ci-bot
# KẾT QUẢ: yes
```

### Cách Hiển Thị Toàn Bộ Quyền Hạn Hiện Có

Để xem một bức tranh toàn cảnh về tất cả những gì bạn hoặc một đối tượng có thể làm, hãy dùng cờ `--list`:

```bash
# Xem danh sách tất cả các hành động mình được phép làm trong Namespace production
kubectl auth can-i --list -n production

# OUTPUT mẫu:
# Resources                      Non-Resource URLs  Resource Names  Verbs
# deployments.*                  []                 []              [get list watch update patch]
# pods                           []                 []              [get list watch]
# selfsubjectaccessreviews.rbac  []                 []              [create]
```

---

## 7️⃣ Những Mô Hình RBAC Thực Chiến Trên Production

Để giúp bạn dễ dàng áp dụng vào thực tế công việc, mình đã tổng hợp 4 mẫu cấu hình phân quyền phổ biến nhất trên các hệ thống Production thực tế:

### Mô hình 1: Phân Quyền Chỉ Đọc (Read-Only) Cho Đội Dev Trên Dashboard

Mục tiêu: Đội ngũ lập trình viên có thể vào xem log, xem trạng thái hệ thống của môi trường chạy thực tế (`production`) nhưng tuyệt đối không được phép chỉnh sửa hoặc xóa bất cứ thứ gì.

```yaml
# file: rbac-pattern_devs-read-only.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devs-production-read-only
  namespace: production           # Giới hạn an toàn trong Namespace production
subjects:
- kind: Group
  name: dev-team                  # Gán cho toàn bộ thành viên thuộc nhóm dev-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view                      # Tái sử dụng ClusterRole 'view' có sẵn của K8s
  apiGroup: rbac.authorization.k8s.io
```

### Mô hình 2: Đội Ngũ Làm Chủ Hoàn Toàn Một Namespace

Mục tiêu: Trao cho Team A toàn quyền quản lý, tự tạo Pod, Service, ConfigMap, Database trong Namespace `team-a` của họ, nhưng không thể can thiệp sang Namespace của đội khác.

```yaml
# file: rbac-pattern_team-admin.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-a-full-admin
  namespace: team-a               # Trao quyền hạn trong bờ cõi team-a
subjects:
- kind: Group
  name: backend-developers-team
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: admin                     # Tái sử dụng ClusterRole 'admin' (toàn quyền trừ việc can thiệp RBAC gốc)
  apiGroup: rbac.authorization.k8s.io
```

### Mô hình 3: CI/CD Bot Chỉ Có Quyền Deploy Mà Không Được Can Thiệp Hệ Thống

Mục tiêu: Cấp quyền cho GitHub Actions Bot chỉ được phép cập nhật mã nguồn (Deploy/Patch) ứng dụng, tuyệt đối không được vào Pod đọc nhật ký nhạy cảm hoặc can thiệp sâu hệ thống.

```yaml
# file: rbac-pattern_cicd-deployer.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-updater
  namespace: production
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"] # Chỉ được cập nhật deployment
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]                              # Được xem danh sách Pod chứ không được xóa hay exec
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: cicd-deployer-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: github-ci-bot
  namespace: team-a
roleRef:
  kind: Role
  name: deployment-updater
  apiGroup: rbac.authorization.k8s.io
```

### Mô hình 4: Giới Hạn Quyền Truy Cập Secret Nhạy Cảm

Mục tiêu: Đội ngũ vận hành thông thường chỉ được phép tương tác với các tệp cấu hình ConfigMap, nhưng không được phép đọc mã Secret chứa khóa API Token tài chính của doanh nghiệp, ngoại trừ một vài khóa cấu hình cơ bản.

```yaml
# file: rbac-pattern_restrict-secrets.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: general-developer
  namespace: production
rules:
- apiGroups: ["", "apps", "networking.k8s.io"]
  resources: ["pods", "deployments", "services", "configmaps"]
  verbs: ["*"]                    # Được toàn quyền thao tác với Pod, Deploy, Service, ConfigMap
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]                  # Chỉ được lấy (get) chứ không được liệt kê (list) tất cả Secrets
  resourceNames: ["shared-db-config", "public-tls"] # Chỉ được phép chạm vào đúng 2 Secret chỉ định này
```

---

## 8️⃣ OPA Gatekeeper Và Kyverno: Làm Sao Để Kiểm Soát Luật Lệ Tự Động Toàn Cluster?

RBAC giúp chúng ta trả lời câu hỏi *"Ai có quyền làm gì"*. Tuy nhiên, có những quy định về an toàn kỹ thuật áp dụng chung cho toàn bộ Cluster mà RBAC không thể giải quyết được. Ví dụ:
* *Không cho phép bất kỳ ai deploy Pod sử dụng thẻ ảnh `:latest` (thiếu nhất quán trên Production).*
* *Bắt buộc tất cả các Pod khi deploy lên Cluster đều phải khai báo giới hạn tài nguyên `resources.limits`.*
* *Chặn đứng không cho phép chạy Pod ở chế độ đặc quyền cao nhất (Privileged Container).*

Để giải quyết bài toán này, bạn cần sử dụng các công cụ kiểm soát chính sách (Policy Enforcement) như **Kyverno** hoặc **OPA Gatekeeper**.

### So Sánh Giữa Kyverno Và OPA Gatekeeper

Hiện nay trên các hệ thống Cloud-Native hiện đại, cộng đồng DevOps rất ưu tiên sử dụng Kyverno nhờ tính năng thân thiện:

| Tiêu chí | Kyverno (Khuyên dùng) | OPA Gatekeeper |
| :--- | :--- | :--- |
| **Ngôn ngữ viết luật** | Định nghĩa bằng **YAML thuần túy** thân thuộc với K8s. | Sử dụng ngôn ngữ lập trình **Rego** phức tạp và khó học hơn. |
| **Tích hợp K8s** | Thiết kế dành riêng cho Kubernetes. | Thiết kế đa dụng cho nhiều hệ thống phần mềm khác nhau. |
| **Tính năng tự động** | Có khả năng tự động sửa lỗi (Mutate) và tạo tài nguyên mới. | Tập trung chủ yếu vào việc kiểm tra và chặn lỗi (Validate). |

Dưới đây là một ví dụ thực tế về cách khai báo một quy định (Policy) bằng Kyverno để bắt buộc mọi Container trong Cluster đều phải cấu hình giới hạn tài nguyên RAM/CPU:

```yaml
# file: kyverno-policy_require-limits.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resource-limits
spec:
  validationFailureAction: enforce # Cưỡng chế chặn đứng (enforce) nếu vi phạm, hoặc cảnh báo (audit)
  rules:
  - name: check-container-limits
    match:
      any:
      - resources:
          kinds:
          - Pod           # Áp dụng cho mọi tài nguyên thuộc loại Pod
    validate:
      message: "Táo bạo quá! Bạn bắt buộc phải khai báo giới hạn tài nguyên (limits.cpu và limits.memory) cho container."
      pattern:
        spec:
          containers:
          - resources:
              limits:
                cpu: "?*"      # Ký tự đại diện yêu cầu bắt buộc phải có giá trị bất kỳ
                memory: "?*"
```

---

## 9️⃣ Dự Án Thực Chiến: Thiết Lập Hệ Thống Multi-Team Hoàn Chỉnh Trực Quan

Để đúc kết toàn bộ kiến thức lý thuyết đã học từ đầu bài, chúng ta sẽ cùng nhau thực hiện một dự án thực tế: **Xây dựng biên giới bảo mật và phân quyền hoàn chỉnh cho hai đội ngũ `team-backend` và `team-frontend` dùng chung một K8s Cluster.**

### Đề bài yêu cầu
1. Tạo 2 Namespace riêng biệt: `team-backend` và `team-frontend`.
2. Áp đặt hạn mức tài nguyên (ResourceQuota) cho `team-backend`: Tối đa chỉ được dùng 2 CPU, 4GB RAM và chạy tối đa 5 Pod.
3. Thiết lập mặc định (LimitRange) cho `team-frontend` nếu lập trình viên quên khai báo RAM/CPU.
4. Tạo ServiceAccount `api-deployer-sa` trong Namespace `team-backend`.
5. Tạo Role `deployer-role` cho phép cập nhật Deployments trong `team-backend`.
6. Liên kết ServiceAccount với Role thông qua RoleBinding.
7. Sử dụng `kubectl auth can-i` giả lập chạy thử để kiểm toán an ninh toàn bộ hệ thống.

---

### 1. Khai báo phân vùng tài nguyên (Namespaces, Quotas & LimitRange)

Hãy tạo một tệp YAML tổng hợp để khởi tạo hạ tầng cơ bản:

```yaml
# file: 10_infrastructure-setup.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-backend
---
apiVersion: v1
kind: Namespace
metadata:
  name: team-frontend
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: backend-quota
  namespace: team-backend
spec:
  hard:
    requests.cpu: "1"
    requests.memory: "2Gi"
    limits.cpu: "2"
    limits.memory: "4Gi"
    pods: "5"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: frontend-limits
  namespace: team-frontend
spec:
  limits:
  - type: Container
    default:
      cpu: "200m"
      memory: "256Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
```

Áp dụng hạ tầng cơ bản lên hệ thống:

```bash
kubectl apply -f 10_infrastructure-setup.yaml
```

---

### 2. Thiết lập định danh và phân quyền RBAC cho Bot Deploy của Team Backend

Chúng ta sẽ tạo ServiceAccount đóng vai trò là "con bot" tự động deploy ứng dụng, sau đó cấp quyền cho nó thông qua Role và RoleBinding.

```yaml
# file: 11_rbac-setup.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: api-deployer-sa
  namespace: team-backend
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager-role
  namespace: team-backend         # Giới hạn quyền lực an toàn trong team-backend
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"] # Cho phép bot xem danh sách Pod để kiểm tra sức khỏe
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: api-deployer-binding
  namespace: team-backend
subjects:
- kind: ServiceAccount
  name: api-deployer-sa
  namespace: team-backend
roleRef:
  kind: Role
  name: deployment-manager-role
  apiGroup: rbac.authorization.k8s.io
```

Áp dụng cấu hình phân quyền:

```bash
kubectl apply -f 11_rbac-setup.yaml
```

---

### 3. Kiểm toán an ninh bằng giả lập quyền (Audit Verification)

Sau khi deploy xong, chúng ta hãy đóng vai trò là một kỹ sư bảo mật hệ thống (Security Auditor) để chạy thử nghiệm các lệnh kiểm toán an ninh thực tế sau:

```bash
# Câu hỏi 1: Con bot deployer của team-backend có thể cập nhật Deployments trong bờ cõi của nó không?
kubectl auth can-i patch deployments -n team-backend --as=system:serviceaccount:team-backend:api-deployer-sa
# KẾT QUẢ MONG ĐỢI: yes  (Đúng như thiết kế!)

# Câu hỏi 2: Con bot deployer này có thể táy máy xóa Deployments bên Namespace team-frontend không?
kubectl auth can-i delete deployments -n team-frontend --as=system:serviceaccount:team-backend:api-deployer-sa
# KẾT QUẢ MONG ĐỢI: no   (Tuyệt vời! Biên giới an ninh đã hoạt động chặn đứng hành vi chéo namespace)

# Câu hỏi 3: Lập trình viên Alice (được giả định có quyền view mặc định) có thể đọc Secret ở Namespace production không?
kubectl auth can-i get secrets -n production --as=alice@company.com
# KẾT QUẢ MONG ĐỢI: no   (Dữ liệu nhạy cảm được bảo vệ an toàn!)
```

Chúc mừng bạn! Bạn đã hoàn thành xuất sắc hệ thống phân vùng và phân quyền multi-team chuẩn hóa Production quốc tế.

---

## ⚠️ 5 Sai Lầm Chí Mạng Thường Gặp Trên Hệ Thống Thực Tế

1. **Quên cờ `-n namespace` khi deploy:** 
   * *Hậu quả:* Mọi tài nguyên sẽ tự động rơi vào Namespace `default`, làm lộn xộn môi trường chạy thực tế.
   * *Khắc phục:* Luôn cấu hình Namespace rõ ràng ngay trong thẻ `metadata.namespace` của tệp YAML thay vì phụ thuộc vào tham số dòng lệnh CLI.
2. **Lạm dụng cấp quyền tối cao `cluster-admin`:**
   * *Hậu quả:* Cấp quyền admin toàn hệ thống cho các tài khoản CI/CD Bot thông thường. Nếu bot bị lộ token, hacker sẽ xóa sạch K8s Cluster của doanh nghiệp.
   * *Khắc phục:* Tuân thủ nguyên tắc đặc quyền tối thiểu (Least Privilege). Chỉ sử dụng Role và giới hạn các hành động (verbs) thật sự cần thiết.
3. **Cấu hình ResourceQuota nhưng bỏ quên LimitRange:**
   * *Hậu quả:* K8s Server sẽ lập tức từ chối toàn bộ các Pod mới deploy nếu Pod đó không khai báo chính xác tài nguyên `resources.requests`, khiến lập trình viên bực bội vì lỗi không rõ nguyên nhân.
   * *Khắc phục:* Luôn đồng hành cấu hình LimitRange kèm theo các giá trị mặc định (Default) bất cứ khi nào bạn áp đặt ResourceQuota lên Namespace.
4. **Tin tưởng tuyệt đối Namespace là ranh giới bảo mật mạng:**
   * *Hậu quả:* Pod ở Namespace Staging bị hack có thể quét IP mạng nội bộ và kết nối trực tiếp đến Database chứa dữ liệu thực tế ở Namespace Production.
   * *Khắc phục:* Luôn luôn thiết lập **NetworkPolicy** để chặn kết nối chéo giữa các Namespace ngoại trừ các dịch vụ được chỉ định rõ ràng.
5. **Bật tính năng Token Automount cho mọi Pod vô tội vạ:**
   * *Hậu quả:* Bất kỳ Pod Web API cơ bản nào khi bị tấn công chiếm quyền cũng đều chứa sẵn token truy cập K8s API Server với quyền hạn mặc định.
   * *Khắc phục:* Khai báo `automountServiceAccountToken: false` cho tất cả các Pod nghiệp vụ thông thường.

---

## ✅ Bài Tập Tự Đánh Giá Tư Duy Cốt Lõi

Hãy trả lời nhanh các câu hỏi sau để tự kiểm tra độ thấu suốt kiến thức của bản thân:

1. **Sự khác biệt cốt lõi giữa Role và ClusterRole là gì? Khi nào ta có thể liên kết ClusterRole thông qua RoleBinding?**
2. **Tại sao việc cấu hình `automountServiceAccountToken: false` lại cực kỳ quan trọng đối với các ứng dụng Web API thông thường chạy trên Kubernetes?**
3. **Nếu một Namespace đã cấu hình ResourceQuota đạt mức tối đa RAM là 4GB, chuyện gì xảy ra khi bạn cố tình scale Deployment từ 2 Pod lên 5 Pod với mỗi Pod yêu cầu 1GB RAM?**
4. **Điểm khác biệt căn bản giữa tài khoản người dùng (User) và tài khoản dịch vụ (ServiceAccount) trong Kubernetes là gì?**

<details>
<summary>💡 Gợi ý giải đáp câu hỏi tự đánh giá</summary>

1. **Trả lời:** 
   * **Role** bị giới hạn trong **một Namespace duy nhất**. **ClusterRole** áp dụng trên **toàn bộ Cluster** (bao gồm các tài nguyên không thuộc Namespace như Node, PersistentVolume).
   * Bạn có thể liên kết **ClusterRole** qua **RoleBinding** để gán nhanh các quyền năng đã định nghĩa sẵn trong ClusterRole (ví dụ: quyền chỉ đọc `view`) nhưng quyền lực đó sẽ lập tức bị giới hạn an toàn chỉ hoạt động bên trong phạm vi của một Namespace khai báo trong RoleBinding đó.

2. **Trả lời:**
   * Mặc định, K8s sẽ tự động tạo và gắn một mã JWT Token xác thực vào bên trong tất cả các Pod. Nếu ứng dụng Web API của bạn không cần tự động giao tiếp với K8s API Server để điều khiển hệ thống, việc có sẵn mã token này là lỗ hổng an ninh lớn. Nếu Web API bị hack, tin tặc sẽ lập tức lấy được token này để tấn công chiếm quyền điều khiển toàn Cluster. Tắt automount giúp giảm thiểu tối đa bề mặt bị tấn công (Attack Surface).

3. **Trả lời:**
   * K8s API Server sẽ kiểm tra tổng tài nguyên RAM yêu cầu của 5 Pod (5 Pod x 1GB = 5GB RAM). Khi phát hiện con số này vượt quá hạn mức tối đa của Namespace là 4GB, API Server sẽ **từ chối yêu cầu scale**. Trạng thái Deployment sẽ báo lỗi vi phạm hạn mức (ResourceQuota Exceeded) và 3 Pod mới sẽ không bao giờ được khởi tạo.

4. **Trả lời:**
   * **User (Người dùng):** Đại diện cho con người ngoài đời thực (Lập trình viên, Quản trị viên). K8s không quản lý thông tin mật khẩu/danh tính của User mà giao phó cho các dịch vụ bảo mật ngoài (Client Cert, OIDC, Active Directory).
   * **ServiceAccount (Tài khoản dịch vụ):** Là đối tượng nguyên bản nằm bên trong Kubernetes, dành riêng cho các chương trình máy, bot CI/CD, hoặc các Pod chạy trong hệ thống tự động chứng minh danh tính với API Server.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Thao tác nhanh với Namespace

```bash
# Tạo nhanh Namespace mới
kubectl create namespace team-c

# Thiết lập Namespace mặc định cho phiên làm việc hiện tại
kubectl config set-context --current --namespace=team-c
```

### Cú pháp YAML gộp tối giản Role & RoleBinding thực chiến

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-operator
  namespace: team-c
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch", "delete"] # Cho phép restart pod bằng cách xóa pod
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-operator-binding
  namespace: team-c
subjects:
- kind: User
  name: developer-bob
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: app-operator
  apiGroup: rbac.authorization.k8s.io
```

### 4 ClusterRole mặc định cốt lõi cần nhớ

```
cluster-admin  -> Quyền tối thượng, Superuser toàn Cluster.
admin          -> Toàn quyền quản trị nhưng giới hạn trong 1 Namespace.
edit           -> Được phép đọc/ghi tài nguyên trong Namespace (không thể sửa đổi RBAC).
view           -> Quyền chỉ đọc (Read-only) an toàn, phù hợp để giám sát.
```

---

## 🔗 Liên Kết Hữu Ích Cần Tham Khảo

### Tài liệu cùng chuyên mục
* ← Bài học trước: [ConfigMaps Và Secrets: Quản Lý Cấu Hình Và Dữ Liệu Nhạy Cảm Đúng Cách](03_configmaps-and-secrets.md)
* ↑ Thư mục cha: [Kubernetes Basic Overview](../../README.md)

### Liên kết hệ thống
* 🛠️ [Hướng dẫn thiết lập môi trường soạn thảo chuyên nghiệp chuẩn DevOps](../../../../02_tools/ide/vs-code.md)
* 🗺️ [Lộ trình phát triển sự nghiệp Kỹ sư DevOps chuyên nghiệp v2.0](../../../../00_roadmaps/career/devops-engineer_career-roadmap.md)

### Tài liệu chính thức từ Kubernetes
* 📖 [Tài liệu Kubernetes chính thức — Tổng quan về Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
* 📖 [Tài liệu Kubernetes chính thức — Kiểm soát truy cập RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
* 📖 [Tài liệu Kyverno chính thức — Quản lý chính sách an ninh K8s](https://kyverno.io/)

---

> 🎯 **Lời khuyên:** Chúc mừng bạn đã cùng mình hoàn thành xuất sắc module **Kubernetes Basic (5/5 bài học)**! Bạn hiện đã nắm giữ những khối kiến thức nền móng vững chắc nhất để tự tin vận hành các dịch vụ trên môi trường K8s thực tế. Hãy tiếp tục cùng mình chinh phục các chuyên đề nâng cao tiếp theo như K8s Storage (PV/PVC/StatefulSet), hệ thống GitOps (ArgoCD) và giám sát hệ thống nhé!

---

## 📜 Nhật Ký Thay Đổi (Changelog)

- **v2.0.0 (26/05/2026)** — Nâng cấp Premium chuẩn 5 sao: Việt hóa 100% chú thích trong tệp YAML; Thiết kế tiêu đề H2 dạng câu hỏi gợi mở tư duy sâu sắc; Tích hợp dự án thực tế Multi-Team hoàn chỉnh ở cuối bài; Chuẩn hóa tất cả các cảnh báo sang GitHub Alerts bảo mật.
- **v1.1.0 (25/05/2026)** — Áp dụng Blueprint v0.5.4 §3.6: thêm lead-in trước §1.
- **v1.0.0 (23/05/2026)** — Phiên bản sơ khởi đầu tiên thuộc Kubernetes Sprint #5.
- **v2.0.1 (10/06/2026)** — Đổi field metadata block-quote sang tiếng Việt (Author → Tác giả, Prerequisites → Yêu cầu trước); gỡ tên tác giả khỏi thân bài và changelog.
