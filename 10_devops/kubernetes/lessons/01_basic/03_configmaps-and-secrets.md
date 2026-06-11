# 🎓 ConfigMaps Và Secrets: Tách Biệt Cấu Hình Và Bảo Mật Tuyệt Đối Môi Trường

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.2\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Cấu hình định tuyến dịch vụ với Services và Ingress](./02_services-and-networking.md)

> 🎯 **Lời dẫn:**
> Chào bạn, một trong những triết lý quan trọng nhất của việc xây dựng ứng dụng chuẩn đám mây (12-Factor App) là: **Tách biệt hoàn toàn mã nguồn (Code) khỏi cấu hình môi trường (Config)**. Việc hardcode mật khẩu, API key hay chuỗi kết nối Database trực tiếp vào file code hoặc file YAML deploy là một "thảm họa bảo mật" vô cùng nghiêm trọng. Bài học thực chiến này sẽ trang bị cho bạn tư duy thiết kế bảo mật đỉnh cao thông qua bộ đôi công cụ đắc lực: **ConfigMap** (cho thông tin cấu hình mở) và **Secret** (cho dữ liệu nhạy cảm), giúp hệ thống của bạn an toàn tuyệt đối trước mọi nguy cơ rò rỉ thông tin!

## 🎯 Sau bài học này, bạn sẽ làm chủ

- [x] Triết lý 12-Factor App trong thiết kế cấu hình và vai trò khác biệt giữa ConfigMap và Secret.
- [x] Phương pháp viết tệp YAML khai báo **ConfigMap** và **Secret** chuẩn chỉ.
- [x] Sử dụng thành thạo **3 phương pháp inject cấu hình** vào container: Biến môi trường đơn lẻ, Inject hàng loạt (envFrom), và Gắn kết dưới dạng tệp tin (Volume Mount).
- [x] Bản chất của mã hóa **Base64** trong K8s Secret và những cạm bẫy bảo mật mà bạn buộc phải tránh.
- [x] Giải pháp tự động khởi động lại container khi cấu hình thay đổi (**Hot Reload vs Restart**).
- [x] Cách cấu hình **External Secrets Operator (ESO)** để đồng bộ mật khẩu trực tiếp từ AWS Secrets Manager hoặc HashiCorp Vault.
- [x] Cách sử dụng **Sealed Secrets** để mã hóa an toàn các tệp tin mật khẩu trước khi đẩy lên Git công cộng.

---

## Tình Huống: Thảm Họa Rò Rỉ Mật Khẩu Database Lên Lịch Sử Git

Bạn đang chuẩn bị triển khai phiên bản mới của ứng dụng FastAPI lên Kubernetes. Do đang vội vã chạy kịp deadline, bạn viết trực tiếp chuỗi kết nối database có chứa mật khẩu thật vào phần khai báo biến môi trường của file YAML:

```yaml
# production-fastapi-vỡ-trận.yaml
spec:
  containers:
  - name: fastapi-container
    image: acmeshop/fastapi:v1.0
    env:
    - name: DATABASE_URL
      value: postgresql://dbadmin:MySuperSecretPassword2026@postgres-db:5432/acmedb  # ❌ HARDCODE MẬT KHẨU!
    - name: JWT_SECRET_KEY
      value: high-secured-jwt-key-never-share-this-random-string-12345                # ❌ HARDCODE SECRET KEY!
```

Bạn gõ lệnh apply, container chạy mượt mà. Tuy nhiên, 10 phút sau sếp đi ngang qua với gương mặt cực kỳ nghiêm nghị:

*"Em vừa commit file YAML này lên kho Git chung của công ty phải không? Toàn bộ mật khẩu Database chính và Secret Key mã hóa Token của chúng ta đã bị phơi bày hoàn toàn trên lịch sử Git công cộng cho hàng chục người thấy rồi kìa!"*

🔥 **Thảm họa ập đến:** Mặc dù bạn có xóa file đó đi và commit đè lên, nhưng mật khẩu vẫn nằm vĩnh viễn trong lịch sử Git (Git History). Cách duy nhất để khắc phục là bạn phải đổi toàn bộ mật khẩu hệ thống và viết script xóa trắng lịch sử Git cực kỳ phức tạp.

Bạn ngơ ngác hỏi: *"Vậy làm thế nào để em có thể truyền các thông số cấu hình và mật khẩu bí mật vào container một cách an toàn mà không phải ghi trực tiếp vào file YAML deploy?"*

Mình muốn chia sẻ với bạn:

> [!NOTE]
> *"Đó chính là lý do vì sao Kubernetes phân tách rạch ròi thành hai tài nguyên độc lập: **ConfigMap** chuyên lưu cấu hình mở không nhạy cảm (như Port, Log Level, Domain), và **Secret** chuyên bảo mật dữ liệu nhạy cảm (như Mật khẩu, API Token, Private Key). Mọi thông số sẽ được lưu trữ an toàn trong RAM của cluster và chỉ được 'bơm' vào container khi khởi chạy!"*

Bài học này sẽ dắt tay bạn thực hiện quy trình bảo mật chuẩn mực đó!

---

## 1️⃣ Bản Chất Của ConfigMap: Tách Biệt Biến Cấu Hình Không Nhạy Cảm Khỏi Mã Nguồn

**ConfigMap** là một khối tài nguyên trong Kubernetes được thiết kế riêng biệt để lưu trữ các thông số cấu hình không nhạy cảm dưới dạng các cặp Key-Value hoặc các tệp tin cấu hình văn bản thuần túy.

```yaml
# configmap-app.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-configmap             # Tên đại diện để tham chiếu
data:
  LOG_LEVEL: "INFO"                   # Cấu hình mức độ ghi log
  API_TIMEOUT_SECONDS: "30"           # Thời gian chờ API tối đa
  CORS_ALLOW_ORIGINS: "https://acmeshop.vn"
  # Bạn thậm chí có thể chứa cả nội dung của một file cấu hình Nginx hoàn chỉnh vào đây!
  nginx.conf: |
    server {
      listen 80;
      location / {
        proxy_pass http://localhost:8000;
      }
    }
```

---

### Khởi tạo ConfigMap nhanh chóng bằng công cụ CLI

Ngoài việc viết file YAML, trong quá trình lập trình dev nhanh, bạn có thể ra lệnh trực tiếp cho `kubectl` tạo ConfigMap từ 3 nguồn dữ liệu khác nhau:

```bash
# 1. Tạo từ các tham số gõ trực tiếp (Literal values)
kubectl create configmap cli-config --from-literal=LOG_LEVEL=DEBUG --from-literal=PORT=5000

# 2. Tạo từ một file cấu hình có sẵn trên máy host
kubectl create configmap nginx-config --from-file=nginx.conf

# 3. Tạo từ một file chứa biến môi trường .env chuyên biệt
kubectl create configmap env-config --from-env-file=.env.production
```

Để kiểm tra nội dung ConfigMap vừa tạo:
```bash
kubectl get configmap fastapi-configmap -o yaml
```

---

## 2️⃣ Kubernetes Secret: Đóng Gói Thông Tin Nhạy Cảm Và Bản Chất Của Mã Hóa Base64

**Secret** hoạt động tương tự như ConfigMap nhưng được thiết kế chuyên biệt để bảo vệ các dữ liệu nhạy cảm (Mật khẩu, SSH Keys, Token, SSL Certificates). Tất cả các giá trị ghi trong tệp YAML Secret bắt buộc phải được mã hóa dưới dạng **Base64**.

```yaml
# secret-app.yaml
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-secrets
type: Opaque                          # Loại hình mặc định chứa dữ liệu tùy biến bảo mật
data:
  # Toàn bộ mật khẩu bắt buộc phải được mã hóa sang chuỗi Base64
  DATABASE_PASSWORD: c3VwZXJzZWNyZXQyMDI2    # base64("supersecret2026")
  JWT_SECRET_KEY: bXktand0LWtleS0xMjM0NQ==     # base64("my-jwt-key-12345")
```

---

### Cảnh báo quan trọng: Base64 KHÔNG PHẢI là mã hóa bảo mật!

> [!CAUTION]
> **Hố đen chết người:**
> Rất nhiều bạn mới học DevOps lầm tưởng rằng dữ liệu đã đổi sang Base64 (ví dụ `c3VwZXJzZWNyZXQyMDI2`) là đã được mã hóa an toàn và có thể thoải mái push tệp Secret YAML này lên GitHub. **Đây là một sai lầm chết người!**
> 
> Base64 chỉ là một chuẩn **mã hóa định dạng truyền tải dữ liệu (Encoding)** nhằm giúp bảo toàn ký tự đặc biệt khi truyền mạng. Bất kỳ ai có chuỗi Base64 đều có thể dễ dàng giải mã (Decode) ngược lại thành mật khẩu gốc trong vòng 0.1 giây chỉ bằng 1 câu lệnh đơn giản:

```bash
# Thử giải mã ngược chuỗi base64 về mật khẩu gốc cực kỳ dễ dàng
echo "c3VwZXJzZWNyZXQyMDI2" | base64 -d
# Output: supersecret2026
```

Do đó, bạn tuyệt đối **không bao giờ được phép commit các tệp tin Secret YAML chứa mật khẩu thật lên kho mã nguồn Git!** Để bảo vệ an toàn trên Production, chúng ta phải sử dụng các giải pháp mã hóa thực sự ở các lớp phía ngoài như *Sealed Secrets* hoặc *External Secrets* (sẽ học ở mục 6 và 7).

---

### Mẹo nhỏ: Sử dụng `stringData` để bỏ qua công đoạn tự gõ base64 thủ công

Nếu bạn không muốn mất thời gian mở terminal gõ lệnh để convert từng chuỗi sang base64 khi viết YAML ở local, hãy sử dụng trường khai báo **`stringData`**. Kubernetes sẽ tự động mã hóa base64 giúp bạn khi ghi nhận vào hệ thống:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-secrets-easy
type: Opaque
stringData:
  DATABASE_PASSWORD: supersecret2026  # Điền trực tiếp text thường, K8s sẽ tự base64 hóa giúp bạn!
  JWT_SECRET_KEY: my-jwt-key-12345
```

---

## 3️⃣ 3 Phương Pháp Inject Cấu Hình Vào Pod: Env Var, EnvFrom Và Volume Mount

Kubernetes cung cấp cho bạn 3 cách vô cùng linh hoạt để bơm (inject) dữ liệu từ ConfigMap và Secret vào bên trong Container của Pod. Sơ đồ dưới tóm gọn cả hai "con đường" mà dữ liệu cấu hình đi vào container — qua biến môi trường hoặc qua tệp tin:

```mermaid
flowchart LR
    CM["ConfigMap<br/>(config mở)"] --> ENV["Biến môi trường<br/>(env / envFrom)"]
    SE["Secret<br/>(dữ liệu nhạy cảm)"] --> ENV
    CM --> VOL["Volume mount<br/>(tệp trong /etc/config)"]
    SE --> VOL
    ENV --> POD["Container trong Pod"]
    VOL --> POD
```

→ Cùng một nguồn ConfigMap/Secret nhưng hai con đường có hành vi khác nhau: biến môi trường chỉ nạp một lần lúc container khởi chạy, còn tệp tin qua volume mount được tự động cập nhật (chi tiết ở mục 4).

### Phương pháp 1: Inject từng biến môi trường đơn lẻ (Khuyên dùng cho tính tường minh)

Phương pháp này giúp bạn map cụ thể từng key trong ConfigMap/Secret thành một tên biến môi trường tùy chỉnh trong Container:

```yaml
spec:
  containers:
  - name: fastapi-container
    image: acmeshop/fastapi:latest
    env:
    # 1. Bơm biến LOG_LEVEL từ ConfigMap
    - name: APP_LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: fastapi-configmap
          key: LOG_LEVEL
    # 2. Bơm biến DATABASE_PASSWORD từ Secret
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: fastapi-secrets
          key: DATABASE_PASSWORD
```

---

### Phương pháp 2: Inject toàn bộ các Key thành biến môi trường hàng loạt (`envFrom`)

Nếu ConfigMap/Secret của bạn có chứa hàng chục biến môi trường và bạn lười khai báo từng dòng, hãy yêu cầu K8s import toàn bộ chúng một lúc:

```yaml
spec:
  containers:
  - name: fastapi-container
    image: acmeshop/fastapi:latest
    # Bơm hàng loạt 100% các Key có trong ConfigMap và Secret thành biến môi trường của container
    envFrom:
    - configMapRef:
        name: fastapi-configmap
    - secretRef:
        name: fastapi-secrets
```

---

### Phương pháp 3: Gắn kết dưới dạng tệp tin (Volume Mount)

Đây là phương pháp bảo mật và tối ưu nhất chuyên dùng để truyền các tệp cấu hình đồ sộ (như `nginx.conf`, `settings.json`) hoặc các file chứng chỉ SSL vào container dưới dạng các tệp tin vật lý nằm trong một thư mục:

```yaml
spec:
  containers:
  - name: fastapi-container
    image: acmeshop/fastapi:latest
    volumeMounts:
    # Gắn kết ổ đĩa ảo chứa cấu hình vào thư mục /etc/config của container
    - name: config-volume
      mountPath: /etc/config
      readOnly: true                  # Đảm bảo an toàn bảo mật, cấm container ghi đè sửa file
  volumes:
  # Khai báo volume ảo liên kết với ConfigMap
  - name: config-volume
    configMap:
      name: fastapi-configmap
```

Sau khi Pod start, bên trong container sẽ tự động xuất hiện thư mục `/etc/config` chứa các tệp tin vật lý tương ứng với từng Key:
- Tệp `/etc/config/LOG_LEVEL` (Nội dung bên trong là chữ `"INFO"`).
- Tệp `/etc/config/nginx.conf` (Chứa toàn bộ nội dung tệp cấu hình Nginx).

---

## 4️⃣ Hot Reload Đối Đầu Restart: Làm Sao Để Cập Nhật Cấu Hình Không Cần Tắt Container?

Khi bạn tiến hành sửa đổi giá trị LOG_LEVEL từ `"INFO"` sang `"DEBUG"` trực tiếp trong ConfigMap:

```bash
# Ra lệnh sửa đổi ConfigMap trực tiếp trên cluster
kubectl edit configmap fastapi-configmap
```

Điều gì sẽ xảy ra với các Pod đang chạy?

- **Nếu bạn dùng biến môi trường (Cách 1 & 2):** **HOÀN TOÀN KHÔNG CÓ THAY ĐỔI.** Biến môi trường chỉ được nạp duy nhất một lần khi container khởi chạy. Khi ConfigMap thay đổi, giá trị biến môi trường trong Pod vẫn là giá trị cũ. Để cập nhật, bạn bắt buộc phải ra lệnh restart lại toàn bộ Pod:
  ```bash
  # Ra lệnh restart cuốn chiếu để nạp lại biến môi trường mới
  kubectl rollout restart deployment/fastapi-deployment
  ```
- **Nếu bạn sử dụng gắn kết tệp tin (Cách 3 - Volume Mount):** **TỰ ĐỘNG CẬP NHẬT SAU 60 GIÂY.** Kubelet chạy trên Node sẽ định kỳ kiểm tra và tự động cập nhật nội dung tệp tin `/etc/config/LOG_LEVEL` bên trong container. 
  Nếu website của bạn sử dụng Nginx hoặc các thư viện code có tính năng tự động giám sát tệp tin (File Watcher), ứng dụng của bạn sẽ tự động nạp lại cấu hình mới ngay lập tức (**Hot Reload**) mà không cần phải restart container gây gián đoạn hệ thống!

---

## 5️⃣ Encryption at Rest: Bảo Vệ An Toàn Dữ Liệu Secret Ngay Tại Trái Tim etcd

Mặc dù bạn đã bảo mật Secret rất kỹ trên file YAML, tuy nhiên ở cấu hình mặc định của Kubernetes, toàn bộ dữ liệu Secret sẽ được lưu trữ trong cơ sở dữ liệu `etcd` dưới dạng văn bản thuần túy (chỉ được encode base64 đơn giản). Bất kỳ ai có quyền truy cập root vào máy chủ Control Plane đều có thể trực tiếp đọc trộm toàn bộ mật khẩu từ ổ cứng của `etcd`.

Để bảo vệ chuẩn doanh nghiệp, bạn cần kích hoạt tính năng **Encryption at Rest (Mã hóa khi lưu trữ)**:

```yaml
# /etc/kubernetes/encryption-config.yaml mẫu cấu hình của Master Node
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
    - secrets
    providers:
    - aescbc:                         # Sử dụng thuật toán AES-CBC cực mạnh để mã hóa dữ liệu
        keys:
        - name: key1
          secret: c3VwZXJzZWNyZXQzMmJ5dGVzZXNlY3JldGtleTIwMjY= # Khóa mã hóa 32-byte an toàn
    - identity: {}
```

Khi cấu hình này được kích hoạt, API Server sẽ tự động dùng khóa AES để mã hóa toàn bộ dữ liệu Secret trước khi ghi xuống ổ đĩa cứng của `etcd`. Bất kỳ hành vi đọc trộm dữ liệu vật lý nào tại `etcd` đều sẽ chỉ nhận về các ký tự rác vô nghĩa!

---

## 6️⃣ External Secrets Operator: Giải Pháp Đồng Bộ Secret Tự Động Từ Cloud Vault

Tại các doanh nghiệp lớn vận hành hàng trăm cluster, việc quản lý thủ công các tệp tin Secret K8s sẽ nhanh chóng trở thành một thảm họa (khó thu hồi quyền truy cập, không có log lịch sử ai đã đọc mật khẩu, không tự động xoay vòng đổi mật khẩu định kỳ).

Giải pháp tối cao của thế giới Production 2026+ là sử dụng **External Secrets Operator (ESO)**.

```text
  AWS Secrets Manager / Vault (Nơi lưu trữ mật khẩu tập trung duy nhất)
                            │
                            ▼ (External Secrets Operator liên tục kéo về)
           Tài nguyên ảo: ExternalSecret YAML
                            │
                            ▼ (Tự động khởi tạo và cập nhật)
              Kubernetes Secret nội bộ
                            │
                            ▼ (Bơm trực tiếp vào)
                    [Ứng dụng Pods]
```

ESO hoạt động như một cầu nối tự động. Nó liên tục kết nối với các kho quản lý mật khẩu chuyên nghiệp bên ngoài (như AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault) để tự động kéo mật khẩu về và đồng bộ hóa thành các K8s Secret nội bộ. Toàn bộ quá trình được bảo mật tuyệt đối và ghi log chi tiết!

---

## 7️⃣ Sealed Secrets: Mã Hóa Thông Tin Nhạy Cảm Để Lưu Trữ An Toàn Trong Git

Nếu dự án của bạn đi theo triết lý **GitOps** (tất cả mọi cấu hình deploy bắt buộc phải được đưa lên Git để tự động chạy), việc lưu giữ Secret là một thử thách lớn. Công cụ **Sealed Secrets** do hãng Bitnami phát triển sẽ giúp bạn hóa giải nỗi đau này.

Bạn sử dụng công cụ CLI `kubeseal` kết hợp với khóa công khai (Public Key) được cấp từ cluster để mã hóa an toàn tệp Secret thông thường thành một tệp tin đặc biệt gọi là **`SealedSecret`**:

```bash
# Mã hóa tệp Secret thông thường thành tệp SealedSecret an toàn tuyệt đối
kubectl create secret generic fastapi-secrets --from-literal=DB_PASSWORD=my-password --dry-run=client -o yaml | kubeseal -o yaml > sealed-secret.yaml
```

Nội dung tệp output thu được hoàn toàn được mã hóa bằng thuật toán bất đối xứng mạnh mẽ:

```yaml
# sealed-secret.yaml - AN TOÀN TUYỆT ĐỐI ĐỂ COMMIT LÊN GITHUB CÔNG CỘNG!
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: fastapi-secrets
spec:
  encryptedData:
    DB_PASSWORD: AgB123456789...super-encrypted-random-string...xyz
```

Tệp tin này hoàn toàn an toàn để bạn push lên GitHub công khai. Khi được đưa vào K8s Cluster, một controller chạy ngầm (nơi duy nhất nắm giữ Khóa Bí Mật - Private Key) sẽ tự động giải mã tệp này và khôi phục lại thành một K8s Secret thông thường phục vụ cho Pod!

---

## 8️⃣ Image Pull Secret: Cấp Quyền Xác Thực Tải Image Từ Private Registry

Khi bạn đóng gói ứng dụng của công ty và đẩy lên một kho lưu trữ bảo mật riêng tư (Private Registry) như GitHub Packages (GHCR.io) hoặc AWS ECR, Kubernetes mặc định sẽ không có quyền tải (pull) image này về và báo lỗi nghiêm trọng: **`ErrImagePull`** hoặc **`ImagePullBackOff`**.

Để cấp quyền xác thực cho K8s, bạn cần tạo một Secret đặc biệt loại `docker-registry`:

```bash
# Tạo Secret chứa thông tin tài khoản đăng nhập registry
kubectl create secret docker-registry my-registry-key \
  --docker-server=ghcr.io \
  --docker-username=github-username \
  --docker-password=github-personal-access-token \
  --docker-email=admin@company.com
```

Trong file YAML của Deployment, bạn tiến hành khai báo Secret này để cấp quyền tải image cho Pod:

```yaml
spec:
  imagePullSecrets:
  - name: my-registry-key             # Cấp chứng chỉ đăng nhập để tải image bảo mật
  containers:
  - name: internal-app
    image: ghcr.io/company/private-app:v1.0
```

---

## 9️⃣ Thực Hành Thực Chiến: Tách Biệt Cấu Hình Và Inject Mật Khẩu An Toàn Cho FastAPI

Để tổng hợp trọn vẹn kiến thức, chúng ta sẽ thiết kế một bản vẽ cấu hình hoàn chỉnh nhất cho ứng dụng FastAPI: Tách biệt cấu hình không nhạy cảm ra ConfigMap, bảo mật thông tin kết nối nhạy cảm bằng Secret, và truyền toàn bộ chúng vào Deployment bằng cờ `envFrom` hàng loạt.

### Bước 9.1: Tạo tệp manifest cấu hình `fastapi-config-secrets.yaml`

```yaml
# fastapi-config-secrets.yaml
# -------------------------------------------------------------
# 1. KHAI BÁO CONFIGMAP: Các thông số cấu hình mở
# -------------------------------------------------------------
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-production-config
data:
  LOG_LEVEL: "INFO"
  API_TIMEOUT_LIMIT: "45"
  CORS_ORIGIN_URL: "https://acmeshop.vn"

---
# -------------------------------------------------------------
# 2. KHAI BÁO SECRET: Mật khẩu bảo mật dạng stringData dễ viết
# -------------------------------------------------------------
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-production-secrets
type: Opaque
stringData:
  DATABASE_URL: postgresql://admin:StrongSecurePassword2026@postgres-db:5432/acmedb
  JWT_SECRET_KEY: super-secured-jwt-token-signing-key-for-production
```

---

### Bước 9.2: Tạo tệp manifest triển khai ứng dụng `fastapi-deployment.yaml`

```yaml
# fastapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-fastapi
  labels:
    app: secure-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
    spec:
      containers:
      - name: app-container
        image: bitnami/fastapi:latest
        ports:
        - containerPort: 8000
        
        # Bơm hàng loạt 100% biến cấu hình và mật khẩu vào môi trường Container
        envFrom:
        - configMapRef:
            name: fastapi-production-config
        - secretRef:
            name: fastapi-production-secrets

        # Giới hạn tài nguyên an toàn tránh nghẽn node
        resources:
          requests:
            cpu: "150m"
            memory: "128Mi"
          limits:
            cpu: "300m"
            memory: "256Mi"
```

---

### Bước 9.3: Triển khai thực tế và xác minh bảo mật

Hãy gõ các dòng lệnh sau để chạy thử nghiệm và kiểm tra xem biến môi trường đã được inject an toàn vào sâu bên trong container chưa:

```bash
# 1. Triển khai cấu hình và Deployment lên cluster
kubectl apply -f fastapi-config-secrets.yaml
kubectl apply -f fastapi-deployment.yaml

# 2. Chờ 5-10 giây để các Pod sẵn sàng hoạt động
kubectl get pods

# 3. Thực thi truy vấn biến môi trường trực tiếp từ container đang chạy
kubectl exec deploy/secure-fastapi -- env | grep -E "LOG_LEVEL|DATABASE_URL"
```

Màn hình terminal sẽ in ra kết quả phản hồi cực kỳ tuyệt vời:

```text
LOG_LEVEL=INFO
DATABASE_URL=postgresql://admin:StrongSecurePassword2026@postgres-db:5432/acmedb
```

Mật khẩu và cấu hình đã được bơm thành công hoàn hảo vào container mà không hề để lại bất kỳ dấu vết rò rỉ nào trong file YAML deploy chính trên Git của bạn!

---

## ⚠️ 5 Cạm Bẫy Bảo Mật Chết Người Khi Quản Lý Config Và Secret

1. **Commit nhầm tệp Secret YAML chứa mật khẩu thật lên Git:** Kể cả khi bạn xóa tệp đó ở commit sau, mật khẩu vẫn tồn tại vĩnh viễn trong lịch sử Git. Hãy luôn sử dụng Sealed Secrets hoặc cấu hình tệp `.gitignore` thật chặt.
2. **Nhầm lẫn Base64 là mã hóa bảo mật:** Base64 chỉ là một chuẩn định dạng dữ liệu thô. Bất kỳ ai có quyền đọc file YAML đều có thể giải mã ngược lại thành mật khẩu thường chỉ bằng một lệnh đơn giản.
3. **Quên restart Pod sau khi cập nhật biến môi trường trong ConfigMap:** Pod sẽ tiếp tục chạy bằng cấu hình cũ mãi mãi cho đến khi container bị crash hoặc được deploy mới.
4. **Không giới hạn quyền RBAC truy cập Secret trong cluster:** Cấp quyền cho mọi tài khoản developer được phép gõ lệnh `kubectl get secrets` vô tội vạ, dẫn đến việc rò rỉ mật khẩu chéo giữa các dự án.
5. **Mount Secret dưới dạng Volume nhưng để quyền ghi mặc định:** Tạo cơ hội cho các mã độc hoặc lỗi code trong ứng dụng có thể trực tiếp sửa đổi nội dung file mật khẩu hệ thống. Hãy luôn khai báo cờ cấu hình `readOnly: true`.

---

## 🧠 Tự kiểm tra (Self-check)

Bạn hãy tự kiểm tra kiến thức bằng cách trả lời nhanh 5 câu hỏi cốt lõi sau:
1. Khi nào nên dùng ConfigMap và khi nào bắt buộc phải dùng Secret?
2. Tại sao triết lý 12-Factor App lại yêu cầu tách biệt hoàn toàn mã nguồn (Code) khỏi cấu hình (Config)?
3. Sự khác biệt lớn nhất về mặt cập nhật dữ liệu (Hot Reload) giữa phương pháp Inject bằng biến môi trường và gắn kết tệp tin (Volume Mount) là gì?
4. Sealed Secrets giúp giải quyết nỗi đau gì cho đội ngũ vận hành đi theo hướng GitOps?
5. Làm thế nào để giải quyết lỗi `ImagePullBackOff` khi tải image từ một Docker registry riêng tư bảo mật?

<details>
<summary><b>💡 Bấm để xem gợi ý đáp án</b></summary>

1. **Khi nào dùng gì:** ConfigMap dùng cho thông số cấu hình mở không nhạy cảm (URLs, Ports, Log Levels). Secret bắt buộc dùng cho các dữ liệu nhạy cảm cần bảo vệ an toàn (Mật khẩu DB, Token, private SSH keys).
2. **Triết lý 12-Factor App:** Giúp mã nguồn của bạn hoàn toàn độc lập với môi trường chạy. Bạn có thể mang 1 file code đó deploy lên Dev, Staging hay Production mà không cần sửa đổi một dòng code nào, chỉ cần nạp tệp Config tương ứng của môi trường đó.
3. **Sự khác biệt Hot Reload:** 
   - Inject bằng biến môi trường: **Không** hỗ trợ cập nhật động khi ConfigMap/Secret thay đổi (phải restart Pod).
   - Inject bằng Volume Mount: **Tự động** đồng bộ hóa và cập nhật nội dung tệp tin bên trong container sau khoảng 60-90 giây mà không cần tắt/mở lại container.
4. **Giải pháp Sealed Secrets:** Cho phép mã hóa mật khẩu an toàn bằng thuật toán bất đối xứng mạnh mẽ thành tệp `SealedSecret` có thể thoải mái push lên Git công cộng mà không lo rò rỉ, chỉ có controller chạy trong cluster mới giải mã được.
5. **Giải quyết ImagePullBackOff:** Phải tạo một K8s Secret loại `docker-registry` chứa tài khoản xác thực đăng nhập của bạn, sau đó khai báo Secret này vào trường `imagePullSecrets` trong file YAML Deployment của ứng dụng.

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Cấu pháp tạo ConfigMap và Secret nhanh từ CLI
```bash
kubectl create configmap app-cfg --from-env-file=.env.production
kubectl create secret generic app-sec --from-literal=DB_PASSWORD=my-secure-password
```

### Cách thức mount Secret an toàn dưới dạng file readonly (Volume Mount)
```yaml
volumeMounts:
- name: secrets-volume
  mountPath: /etc/secrets
  readOnly: true                      # Cấm tuyệt đối quyền ghi
volumes:
- name: secrets-volume
  secret:
    secretName: fastapi-production-secrets
    defaultMode: 0400                 # Chỉ cho phép chủ sở hữu đọc file (Chặn quyền đọc chéo)
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

- **ConfigMap:** Tài nguyên lưu trữ cấu hình mở không nhạy cảm dưới dạng các cặp Key-Value hoặc tệp văn bản.
- **Secret:** Tài nguyên lưu trữ dữ liệu mật nhạy cảm bắt buộc được mã hóa dạng Base64.
- **External Secrets Operator (ESO):** Bộ điều khiển tự động hóa đồng bộ dữ liệu mật từ các kho lưu trữ đám mây (Vault, AWS Secrets Manager) vào Kubernetes.
- **Sealed Secrets:** Công cụ mã hóa tệp cấu hình mật khẩu an toàn phục vụ lưu trữ trực tiếp trên Git GitOps.
- **Hot Reload:** Khả năng ứng dụng tự động cập nhật và nạp lại cấu hình mới mà không cần tắt đi khởi động lại tiến trình container.

---

## 🔗 Liên Kết & Tài Nguyên Học Tập Bổ Sung

### Các bài học liên quan trực tiếp
- [⬅️ Bài học trước: Cấu hình định tuyến dịch vụ với Services và Ingress](./02_services-and-networking.md)
- [➡️ Bài học tiếp theo: Phân chia biên giới an ninh với Namespaces và RBAC](./04_namespaces-and-rbac.md)

### Tài liệu chính hãng tham khảo thêm
- [Tài liệu chính thức về quản lý ConfigMap trong Kubernetes](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Tài liệu chính thức về bảo mật Secret trong Kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/)

---

## 📌 Lịch Sử Thay Đổi (Changelog)

- **v2.0.0 (26/05/2026)** — **Nâng cấp Premium chuẩn 5 sao:**
  - Viết lại toàn diện bài học đạt chuẩn chất lượng Premium 5 sao của Blueprint mới.
  - Cấu trúc lại tiêu đề H1 và metadata block YAML chuẩn chỉnh chuyên nghiệp.
  - Chuyển đổi 100% tiêu đề H2 thành câu hỏi mở kích thích tư duy sâu sắc.
  - Sửa đổi toàn bộ các Alerts cũ sang định dạng GitHub Alerts chuẩn chỉnh.
  - Việt hóa 100% các dòng ghi chú giải thích bên trong các block code YAML, Python, và Bash.
  - Nâng cấp chương thực hành thực chiến: Bản thiết kế cấu hình an toàn cho FastAPI tách biệt cấu hình mở (ConfigMap), mật khẩu nhạy cảm (Secret) và inject an toàn bằng cờ `envFrom`.
- **v1.1.0 (25/05/2026)** — Áp dụng Blueprint v0.5.4+ §3.6: bổ sung lời dẫn trước phần phân biệt ConfigMap và Secret.
- **v1.0.0 (23/05/2026)** — Khởi tạo bản thảo sơ khai đầu tiên về ConfigMap và Secret.
- **v2.0.1 (10/06/2026)** — Chuyển metadata YAML frontmatter → block-quote chuẩn (field tiếng Việt); gỡ tên tác giả khỏi thân bài; bỏ dấu ":" cuối heading.
- **v2.0.2 (11/06/2026)** — Bổ sung sơ đồ flow inject ConfigMap/Secret (env var vs volume mount → container) cho trực quan.
