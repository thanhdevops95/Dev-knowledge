# Module 00: Introduction Scenarios

---

## 🎯 Mục đích

Module này không có scenarios khó như các module sau. Thay vào đó, đây là các **câu hỏi thường gặp** và **mindset cần có** trước khi bắt đầu.

---

## ❓ Scenario 1: "Tôi không biết gì về DevOps, bắt đầu từ đâu?"

### Tình huống

Bạn là developer/sinh viên/người mới. Nhìn vào danh sách tools (Docker, Kubernetes, Terraform, AWS...) và cảm thấy overwhelming.

### Giải đáp

**Đừng lo.** Đây là lộ trình chi tiết:

```
Tuần 1-2: Linux basics
    ↓
Tuần 3-4: Git (version control)
    ↓
Tuần 5-6: Docker (containers)
    ↓
Tuần 7-8: CI/CD basics
    ↓
... (tiếp tục theo thứ tự modules)
```

**Quy tắc quan trọng:**

1. **Học theo thứ tự** - Modules được sắp xếp từ dễ đến khó
2. **Không skip** - Module sau build trên kiến thức module trước
3. **Làm labs** - Đọc không thì quên 90%

### Mindset đúng

```
❌ "Tôi phải biết hết mọi thứ trước khi apply việc"

✅ "Tôi sẽ học từng bước, apply việc khi đủ kiến thức cơ bản"
```

---

## ❓ Scenario 2: "Tôi đã biết Linux/Docker rồi, có cần học lại không?"

### Tình huống

Bạn là dev đã dùng Docker, hoặc sysadmin đã quản lý Linux servers.

### Giải đáp

**Tùy mức độ:**

| Mức độ | Dấu hiệu | Nên làm |
|--------|----------|---------|
| **Cơ bản** | Biết `docker run`, `ls`, `cd` | Học lại, sẽ có nhiều điều mới |
| **Trung cấp** | Viết Dockerfile, bash scripts | Skim README, tập trung LABS |
| **Nâng cao** | Debug production, write CI/CD | Đọc SCENARIOS, skip nếu đã biết |

**Tip:** Mỗi module có SCENARIOS.md với tình huống thực tế. Nếu bạn giải được dễ dàng, có thể skip module đó.

---

## ❓ Scenario 3: "Tools không cài được, Docker không chạy"

### Tình huống

Bạn chạy `docker run hello-world` nhưng báo lỗi:

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

### Điều tra & Giải quyết

**Bước 1: Docker service có chạy không?**

```bash
# Linux/WSL
sudo systemctl status docker

# macOS - Docker Desktop có đang mở không?
```

**Bước 2: Nếu không chạy, khởi động**

```bash
sudo systemctl start docker
```

**Bước 3: Nếu vẫn lỗi "permission denied"**

```bash
# Thêm user vào group docker
sudo usermod -aG docker $USER

# PHẢI logout và login lại!
# Hoặc restart terminal
```

**Bước 4: Windows specific - WSL2 backend**

1. Mở Docker Desktop
2. Settings → General → "Use the WSL 2 based engine" ✓
3. Settings → Resources → WSL Integration → Enable for Ubuntu
4. Apply & Restart

**Vẫn không được?**

```bash
# Thử chạy với sudo (tạm thời)
sudo docker run hello-world
```

---

## ❓ Scenario 4: "Tôi học chậm, sợ không theo kịp"

### Tình huống

Bạn thấy người khác học 1 module/tuần, mình mất 2 tuần.

### Giải đáp

**Điều quan trọng:** Tốc độ học KHÔNG quan trọng bằng độ vững kiến thức.

```
❌ Học nhanh, không làm labs, quên sau 1 tuần

✅ Học chậm, làm hết labs, nhớ mãi
```

**So sánh thực tế:**

| Học nhanh | Học chậm + làm labs |
|-----------|---------------------|
| "À tui biết Docker" | Viết được Dockerfile |
| "Kubernetes dễ mà" | Debug được pod crash |
| Interview fail | Interview pass |

### Tips khi học chậm

1. **Chia nhỏ** - Mỗi ngày 1-2 giờ tốt hơn weekend marathon
2. **Ghi chép** - Viết lại bằng ngôn ngữ của bạn
3. **Dạy lại** - Giải thích cho bạn bè, dù họ không quan tâm
4. **Thực hành 2x** - Làm lab lần 2 không nhìn hướng dẫn

---

## ❓ Scenario 5: "Đọc hoài không hiểu, quá nhiều khái niệm mới"

### Tình huống

Bạn đọc về Kubernetes:

> "Pod chạy trên Node, được quản lý bởi ReplicaSet, được tạo bởi Deployment, expose qua Service..."

Và cảm thấy đau đầu.

### Giải đáp

**Đây là bình thường!** Mọi người đều như vậy lần đầu.

**Strategies:**

**1. Đọc lại nhiều lần**

```
Lần 1: Đọc qua, không hiểu 70%
Lần 2: Hiểu thêm 20%
Lần 3: Bắt đầu "click"
```

**2. Làm lab trước, đọc lý thuyết sau**

```
Thay vì: Đọc 10 trang về Docker → confused
Thử: Chạy `docker run nginx` → "À, nó serve web!"
     Sau đó đọc lý thuyết → "À, đây là container!"
```

**3. Vẽ ra giấy**

```
Vẽ sơ đồ: User → Browser → Nginx → App → Database
Dán lên tường phòng làm việc
```

**4. Giải thích như nói với trẻ 5 tuổi**

```
Docker = "Hộp chứa app, giống như hộp đựng đồ chơi"
Kubernetes = "Người quản lý nhiều hộp, biết hộp nào hỏng để thay"
```

---

## ❓ Scenario 6: "Tôi muốn apply việc DevOps, cần học đến đâu?"

### Tình huống

Bạn muốn chuyển sang DevOps nhưng không biết cần học đến mức nào.

### Mức độ cho các vị trí

**Junior DevOps / DevOps Intern:**

```
✅ Linux basics (Module 01)
✅ Git (Module 04)
✅ Docker basics (Module 07)
✅ CI/CD basics (Module 08)
◻️ Các module khác - nice to have
```

**Mid-level DevOps (1-3 năm):**

```
✅ Tất cả Junior skills
✅ Kubernetes (Module 09-10)
✅ Cloud basics - AWS/GCP (Module 11)
✅ Terraform basics (Module 12)
✅ Monitoring basics (Module 14)
```

**Senior DevOps (3+ năm):**

```
✅ Tất cả Mid skills, master level
✅ Architecture design
✅ Security (Module 13)
✅ SRE practices (Module 15)
✅ Mentoring juniors
```

### Timeline thực tế

| Mục tiêu | Thời gian học | Thời gian tìm việc |
|----------|---------------|-------------------|
| Junior | 3-6 tháng | 1-3 tháng |
| Mid (từ junior) | 1-2 năm exp | Khi sẵn sàng |
| Mid (từ dev) | 3-6 tháng học + projects | 1-2 tháng |

---

## 💡 Mindset của DevOps Engineer

### 1. "Automate everything"

```
Nếu làm việc gì 2 lần → Viết script
Nếu làm việc gì hàng ngày → Tự động hóa
```

### 2. "If it's not in Git, it doesn't exist"

```
Code → Git
Config → Git
Documentation → Git
Infrastructure → Git (IaC)
```

### 3. "Hope is not a strategy"

```
❌ "Hy vọng deploy không lỗi"
✅ Test trước, deploy từ từ, có rollback plan
```

### 4. "Failure is inevitable, recovery is mandatory"

```
Servers WILL crash
Deploys WILL fail
Databases WILL corrupt

→ Có monitoring để biết
→ Có backups để restore
→ Có runbooks để fix
```

### 5. "Cattle, not pets"

```
Old school: Mỗi server có tên, được chăm sóc cẩn thận (pet)
DevOps: Servers giống nhau, thay thế được (cattle)

→ Server hỏng? Kill và tạo mới
→ Không debug trên production
→ Infrastructure is code
```

---

## ⏭️ Tiếp theo

Mindset đã có, môi trường đã setup. Bắt đầu học thật!

👉 **[Module 01: Linux Fundamentals](../01_LINUX/README.md)**
