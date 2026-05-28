# ⚙️ Cài Đặt Môi Trường Container & Kích Hoạt Docker Engine Trên Mọi OS

> **Tác giả:** Mr.Rom  
> **Phiên bản:** v2.0.0  
> **Tạo lúc:** 16/05/2026  
> **Cập nhật:** 26/05/2026  
> **OS hỗ trợ:** macOS / Linux / Windows  
> **Độ khó:** ⭐⭐ Medium (Mức độ tiếp cận thực tế)  
> **Thời lượng:** ~15-30 phút (tải image ban đầu tùy thuộc tốc độ mạng)  

> [!IMPORTANT]
> **Mục tiêu cốt lõi:**  
> Kích hoạt thành công công cụ điều phối container Docker (Docker Desktop hoặc Docker Engine) trên máy cá nhân của bạn, chạy thử container đầu tiên (`hello-world` và máy chủ `nginx`). Đây là bước chuẩn bị quan trọng nhất trước khi bước vào thế giới DevOps thực chiến.

---

## 💡 Câu Chuyện Về Nam: Khi Máy Tính Trở Thành "Bãi Chiến Trường"

Nam là một nhà phát triển phần mềm năng nổ. Để phục vụ học tập và làm việc, máy tính của Nam được cài đặt trực tiếp (global install) hàng chục dịch vụ nặng nề:
*   Một cơ sở dữ liệu **PostgreSQL v14** cho dự án công ty.
*   Một cơ sở dữ liệu **PostgreSQL v16** để tự học tính năng mới ở nhà.
*   Máy chủ cache **Redis**, hàng đợi tin nhắn **RabbitMQ**, cùng hai phiên bản Web Server **Nginx** và **Apache**.

Sau vài tháng, máy tính của Nam bắt đầu có dấu hiệu quá tải, RAM luôn bị chiếm dụng ngay cả khi không làm việc vì các dịch vụ ngầm tự động khởi động cùng hệ thống. Cực đoan hơn, khi Nam muốn nâng cấp PostgreSQL v14 lên v16, các xung đột cổng kết nối (Port 5432) và file cấu hình nổ ra liên miên. Hệ điều hành gốc của Nam bị "bẩn" hoàn toàn bởi hàng tá thư viện rác còn sót lại sau những lần cài đặt và gỡ bỏ.

Để giải phóng Nam khỏi "bãi chiến trường" lộn xộn này, **Công nghệ Container (Docker)** ra đời.

### 🎭 Ẩn Dụ Sư Phạm: Đập Tường Lắp Đồ Cồng Kềnh vs Thùng Container Di Động Ngoài Sân

Hãy hình dung sự khác biệt giữa hai phương pháp quản lý phần mềm thông qua hình ảnh quen thuộc sau:

*   **Cài đặt trực tiếp lên hệ điều hành (Global Install):** Giống như bạn **đập tường trong nhà** để lắp ghép cố định các đồ đạc cồng kềnh. Mỗi khi muốn đổi đồ mới, bạn lại phải đập phá tường, chắp vá lớp sơn. Ngôi nhà chính (hệ điều hành gốc) của bạn sẽ nhanh chóng trở nên bong tróc, nham nhở và mất đi tính ổn định nguyên bản.
*   **Sử dụng Docker Container:** Giống như bạn đặt các **thùng container di động chuyên dụng** ngoài sân vườn. Bên trong thùng container đã được trang bị và bố trí sẵn giường, tủ, tivi (ứng dụng, dependencies, config). Khi cần dùng, bạn chỉ cần mở cửa bước vào. Khi dự án kết thúc và bạn không cần dùng nữa, xe cẩu (**Docker Engine**) sẽ cẩu thùng container đó đi chỉ trong vòng 3 giây, trả lại thảm cỏ sân vườn hoàn toàn sạch sẽ, xanh mướt và nguyên vẹn!

---

## 1️⃣ Docker Thực Sự Là Gì Và Khi Nào Bạn Cần Đến Nó?

**Docker** là một nền tảng mã nguồn mở cho phép đóng gói toàn bộ ứng dụng, mã nguồn, thư viện đi kèm và các tệp cấu hình môi trường thành một đơn vị duy nhất gọi là **Container**. Đơn vị này có thể chạy nhất quán trên bất kỳ máy tính nào có cài đặt Docker, chấm dứt vĩnh viễn lỗi kinh điển của lập trình viên: *"Nhưng code chạy rất tốt trên máy của em!"*.

### 🎯 Khi nào bạn nên cài?
*   Khi bạn bước vào **Stage 3** của lộ trình học tập, bắt đầu học cách container hóa ứng dụng.
*   Khi bạn làm việc trong các vai trò: Backend Developer, DevOps Engineer, SRE, hay Data Engineer.
*   Khi bạn chuẩn bị học Kubernetes (K8s) — Docker là kiến thức bắt buộc phải biết trước.

### ❌ Khi nào bạn chưa cần cài?
*   Nếu bạn đang học thuần Frontend cắt giao diện (HTML/CSS/JS chạy trực tiếp trên trình duyệt).
*   Nếu bạn đang học cú pháp Python căn bản ở những tuần đầu tiên. Hãy tập trung làm quen với thuật toán trước khi bước sang tư duy container hóa.

> [!NOTE]
> Để hiểu sâu sắc về bản chất lý thuyết, kiến trúc hoạt động bên dưới và cách phân biệt giữa Container và Máy ảo (VM), bạn hãy đọc bài viết: [Bản chất của Docker và Cuộc cách mạng Container hóa](../lessons/01_basic/00_what-is-docker.md). Bài viết này sẽ tập trung 100% vào hướng dẫn thực hành cài đặt môi trường sạch.

---

## 2️⃣ Cỗ Máy Của Bạn Cần Những Gì Để Khởi Chạy Container?

Docker chạy một máy ảo Linux siêu nhẹ ngầm bên dưới trên macOS và Windows, do đó hãy đảm bảo máy tính của bạn đáp ứng các thông số tài nguyên cơ bản sau:

| Tiêu chí | Cấu hình tối thiểu | Khuyến nghị (Premium) |
| :--- | :--- | :--- |
| **Hệ điều hành (OS)** | macOS 11 (Big Sur) / Windows 10 Pro / Ubuntu 20.04 | macOS 13+ / Windows 11 / Ubuntu 22.04 LTS |
| **Dung lượng RAM** | 4 GB RAM | 8 GB RAM trở lên (Docker Desktop cần khoảng 2-4 GB RAM để vận hành mượt mà) |
| **Dung lượng đĩa trống** | 10 GB trống | 50 GB trống trở lên (Vì các Image và Container sẽ tích tụ rất nhanh) |
| **CPU** | Hỗ trợ ảo hóa 64-bit | Apple Silicon (M1/M2/M3/M4) hoặc CPU Intel/AMD hiện đại |
| **Ảo hóa phần cứng** | Phải được kích hoạt trong BIOS (Nếu dùng Windows/Linux) | Đã được tự động kích hoạt mặc định trên macOS |

---

## 3️⃣ Đâu Là Con Đường Cài Đặt Phù Hợp Nhất Cho Bạn?

### Phân biệt rõ ràng: Docker Desktop vs Docker Engine

Trước khi cài đặt, bạn cần hiểu rõ sự khác biệt giữa hai bộ cài đặt này của hãng:

*   **Docker Desktop (Khuyên dùng cho Dev local):** Cung cấp giao diện đồ họa trực quan (GUI) giúp bạn dễ dàng theo dõi các container đang chạy, kiểm tra log, quản lý tài nguyên đĩa cứng. Đi kèm sẵn các công cụ nâng cao như Kubernetes local, Docker Compose.
*   **Docker Engine (Dành cho môi trường Linux / Server):** Không có giao diện đồ họa, chỉ quản lý hoàn toàn bằng dòng lệnh (CLI). Cực kỳ nhẹ, tốn ít tài nguyên và là tiêu chuẩn bắt buộc cho môi trường máy chủ chạy thật (Production) hoặc các máy ảo Linux.

---

### 🅰️ macOS — Cài đặt Docker Desktop (Giao diện đồ họa)

#### Bước 1: Tải về bộ cài đặt
Truy cập trang chủ [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) và chọn tải phiên bản phù hợp với chip máy Mac của bạn:
*   Chọn **Mac with Apple Chip** nếu bạn dùng máy chip M1, M2, M3, M4.
*   Chọn **Mac with Intel Chip** nếu bạn dùng máy sản xuất từ năm 2020 trở về trước.

#### Bước 2: Tiến hành cài đặt
1.  Click đúp vào file `.dmg` vừa tải về.
2.  Kéo biểu tượng **Docker** thả vào thư mục **Applications**.
3.  Tìm mở ứng dụng **Docker** từ Launchpad. Ở lần đầu tiên, hệ thống sẽ yêu cầu cấp quyền quản trị để thiết lập mạng ảo, hãy nhập mật khẩu máy Mac của bạn để đồng ý.
4.  Khi biểu tượng chú cá voi xanh (🐳) trên menu bar ngừng nhấp nháy và chuyển sang màu xanh đứng yên, môi trường của bạn đã sẵn sàng!

#### Bước 3: Xác minh bằng Terminal
Mở ứng dụng Terminal lên và gõ lệnh sau để kiểm tra:
```bash
docker --version
# Kết quả mong đợi: Docker version 25.x.x hoặc mới hơn
```

---

### 🅱️ macOS — Cài đặt nhanh bằng dòng lệnh Homebrew

Nếu bạn là một lập trình viên thích sử dụng dòng lệnh và đã cài sẵn [Homebrew](https://brew.sh/):

```bash
# Cài đặt trọn gói Docker Desktop (bao gồm cả GUI)
brew install --cask docker
```

---

### 🅲 Linux — Cài đặt Docker Engine (Khuyến nghị cho Server)

Trên hệ điều hành Linux (ví dụ Ubuntu/Debian), chúng ta sẽ cài đặt Docker Engine trực tiếp để tối ưu hóa hiệu năng tối đa.

#### Quy trình cài đặt 5 bước chuẩn trên Ubuntu:

```bash
# Bước 1: Cập nhật hệ thống và cài đặt các thư viện chứng thực bảo mật cần thiết
sudo apt update
sudo apt install -y ca-certificates curl gnupg

# Bước 2: Tạo thư mục chứa khóa bảo mật GPG của Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Bước 3: Thêm kho lưu trữ (Repository) chính thức của Docker vào hệ thống apt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Bước 4: Cập nhật lại apt và cài đặt các thành phần cốt lõi của Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Bước 5: Cấu hình phân quyền cho phép User hiện tại chạy Docker không cần gõ sudo
sudo usermod -aG docker $USER
# Áp dụng thay đổi quyền ngay lập tức mà không cần đăng xuất hệ thống
newgrp docker 
```

Kiểm tra trạng thái dịch vụ Docker chạy ngầm:
```bash
sudo systemctl status docker
```

---

### 🅳 Windows — Cài đặt Docker Desktop (Hỗ trợ WSL2)

#### Yêu cầu chuẩn bị:
Docker trên Windows hoạt động tốt nhất thông qua nhân Linux thực thụ của **WSL 2 (Windows Subsystem for Linux)**.

1.  Mở PowerShell dưới quyền Administrator và chạy lệnh sau để kích hoạt WSL 2:
    ```powershell
    wsl --install
    ```
    *Lưu ý:* Khởi động lại máy tính nếu Windows yêu cầu.
2.  Tải bộ cài đặt Windows từ: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
3.  Chạy file `.exe` vừa tải về, hãy chắc chắn tích chọn ô **Use WSL 2 instead of Hyper-V** (Khuyến nghị để đạt hiệu năng cao nhất).
4.  Nhấp OK để tiến hành cài đặt và khởi động lại máy tính khi hoàn tất.
5.  Khởi động ứng dụng **Docker Desktop** từ Start Menu để kích hoạt engine.

---

### 🅴 VPS / Cloud Server — Script cài đặt tự động siêu tốc

Nếu bạn đang đứng ở trên một máy chủ đám mây ảo mới tinh (như AWS EC2 hay DigitalOcean Droplet) và muốn cài nhanh Docker:

```bash
# Tải và chạy script cài đặt tự động chính thức được cung cấp bởi Docker
curl -fsSL https://get.docker.com | sudo sh

# Thêm quyền chạy cho user hiện tại để không cần dùng sudo
sudo usermod -aG docker $USER
```

---

## 4️⃣ Làm Sao Để Chắc Chắn Docker Đã Hoạt Động Hoàn Hảo?

Hãy thực hiện quy trình kiểm tra 3 bước nghiêm ngặt sau để đảm bảo hệ thống đã vận hành trơn tru:

### Bước 1: Kiểm tra phiên bản công cụ
```bash
docker --version
# Kết quả chuẩn: Docker version 26.x.x, build ...

docker compose version
# Kết quả chuẩn: Docker Compose version v2.x.x
```

### Bước 2: Chạy thử Container thử nghiệm huyền thoại `hello-world`
Chạy lệnh sau trên Terminal:
```bash
docker run hello-world
```

> [!NOTE]
> **Bản chất hoạt động ngầm của câu lệnh trên:**  
> 1. Docker Engine tìm kiếm Image có tên `hello-world` ở máy của bạn (Local) nhưng không thấy.  
> 2. Nó tự động kết nối lên kho lưu trữ đám mây **Docker Hub** để tải (Pull) Image này về máy.  
> 3. Khởi tạo một Container từ Image đó và thực thi mã nguồn bên trong.  
> 4. Container in ra dòng chữ chào mừng và lập tức tự động tắt đi để giải phóng tài nguyên.

Nếu bạn nhìn thấy dòng chữ sau xuất hiện trên màn hình, xin chúc mừng:
```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

### Bước 3: Khởi chạy thử một máy chủ Web Nginx thực tế
Hãy thử chạy một dịch vụ thực sự chạy ngầm dài hạn:

```bash
# Khởi chạy một container nginx chạy ngầm (-d), mở cổng kết nối 8080 trỏ vào cổng 80 của container (-p)
docker run -d -p 8080:80 --name my-nginx nginx
```

Bây giờ, hãy mở trình duyệt web của bạn và truy cập địa chỉ: `http://localhost:8080`.  
Bạn sẽ thấy trang chào mừng `"Welcome to nginx!"` hiển thị rực rỡ. Bạn đã chính thức dựng thành công một web server trong vòng chưa đầy 5 giây mà không cần cài đặt bất kỳ thư viện nào lên hệ điều hành gốc của máy!

#### Cách dọn dẹp container sau khi thử nghiệm xong:
```bash
# Bước 1: Dừng container đang chạy ngầm
docker stop my-nginx

# Bước 2: Xóa container khỏi bộ nhớ hệ thống
docker rm my-nginx
```

---

## 5️⃣ Làm Chủ Các Thiết Lập Ban Đầu Và Bảo Trì Hệ Thống

### 1. Cấu hình phân bổ tài nguyên tối ưu cho Docker Desktop
Mặc định, Docker Desktop chỉ được cấp phát khoảng 2 CPU và 4 GB RAM. Khi bạn làm việc với các dự án lớn (như build ứng dụng Java, NodeJS hay chạy nhiều database cùng lúc), mức này sẽ khiến quá trình build bị chậm hoặc treo máy.

*   **Cách điều chỉnh:** Vào mục **Settings (Hình bánh răng)** trên Docker Desktop -> Chọn **Resources** -> **Advanced**.
*   **Mức khuyến nghị (Nếu máy bạn có 16 GB RAM):** Hãy tăng lên **4 CPU** và **8 GB RAM** để đạt hiệu năng tối ưu nhất.

---

### 2. Định kỳ dọn dẹp bộ nhớ đệm (Garbage Collection)
Các Image cũ, các Container đã tắt và các ổ đĩa ảo (Volume) không dùng đến sẽ tích tụ theo thời gian và có thể chiếm dụng hàng chục GB dung lượng ổ cứng của bạn. Hãy chạy bộ lệnh bảo trì sau mỗi tháng:

```bash
# Xem dung lượng thực tế Docker đang chiếm dụng trên đĩa cứng
docker system df

# Xóa sạch toàn bộ container đã dừng, các network không dùng và các image mồ côi (dangling)
docker system prune -a

# Xóa sạch các volume mồ côi không còn kết nối với container nào (Cẩn thận để tránh mất data database)
docker volume prune
```

---

### 3. Đăng ký tài khoản trên Docker Hub
[hub.docker.com](https://hub.docker.com) là kho lưu trữ Image lớn nhất thế giới. Bạn nên đăng ký một tài khoản miễn phí tại đây để:
*   Có thể tải các Image cá nhân tự build lên đám mây.
*   Tránh bị giới hạn số lần tải Image (Rate limit dành cho tài khoản vô danh).

Sau khi đăng ký, hãy đăng nhập trực tiếp trên Terminal:
```bash
docker login
# Nhập Username và Password tài khoản Docker Hub của bạn
```

---

## 6️⃣ Những Vũ Khí Nào Giúp Bạn Quản Lý Docker Chuyên Nghiệp?

### 1. Các tiện ích mở rộng bắt buộc trên VS Code
Để nâng cao năng suất viết Dockerfile và quản lý container trực quan ngay trong trình soạn thảo code, hãy cài đặt các Extension sau (Xem chi tiết tại [Hướng dẫn thiết kế Workspace Premium](../../../02_tools/ide/vs-code.md)):

*   **Docker (`ms-azuretools.vscode-docker`):** Hỗ trợ tự động gợi ý cú pháp viết Dockerfile, hiển thị cây thư mục trực quan quản lý Image, Container, Volume và Network ngay bên thanh Sidebar của VS Code.
*   **Dev Containers (`ms-vscode-remote.remote-containers`):** Tính năng đỉnh cao cho phép bạn mở toàn bộ Workspace và lập trình trực tiếp *bên trong* một container đang chạy.

---

### 2. Các công cụ giao diện dòng lệnh (CLI Tools) nâng cao cho Power User
Khi đã thành thạo các câu lệnh cơ bản, hãy trang bị thêm các vũ khí sau:

*   **CTop (`brew install ctop`):** Hiển thị bảng theo dõi tài nguyên (CPU, RAM, Network) thời gian thực của tất cả container dưới dạng Terminal đồ họa cực kỳ trực quan (giống như lệnh `top` hay `htop` của Linux).
*   **LazyDocker (`brew install lazydocker`):** Trình quản lý Docker chạy hoàn toàn trên Terminal cực kỳ đẹp mắt, cho phép bạn xem log, restart, xóa container chỉ bằng việc di chuyển các phím mũi tên.

---

## 7️⃣ "Giải Cứu": Các Lỗi Cài Đặt Docker Kinh Điển Và Cách Vượt Qua

### ❌ Lỗi 1: `Cannot connect to the Docker daemon. Is the docker daemon running?`
*   **Triệu chứng:** Khi bạn gõ bất kỳ lệnh docker nào, hệ thống báo lỗi không thể kết nối tới file socket.
*   **Nguyên nhân:** Dịch vụ Docker chạy ngầm (Docker Daemon) chưa được khởi động trên máy của bạn.
*   **Cách khắc phục:**
    *   *Trên macOS/Windows:* Hãy tìm và click mở ứng dụng **Docker Desktop** để kích hoạt engine.
    *   *Trên Linux:* Chạy lệnh kích hoạt dịch vụ hệ thống: `sudo systemctl start docker`.

### ❌ Lỗi 2: Lỗi phân quyền `Permission Denied` khi gõ lệnh trên Linux
*   **Triệu chứng:** Bạn gõ `docker ps` và nhận về lỗi từ chối truy cập socket, chỉ khi gõ `sudo docker ps` mới hoạt động.
*   **Nguyên nhân:** User hiện tại của bạn chưa được cấp quyền truy cập vào file socket của Docker.
*   **Cách khắc phục:** Chạy lệnh thêm user vào nhóm docker (xem lại Bước 5 của phần cài đặt Linux):
    ```bash
    sudo usermod -aG docker $USER
    newgrp docker
    ```

### ❌ Lỗi 3: Lỗi trùng cổng kết nối `Port already allocated`
*   **Triệu chứng:** Xuất hiện lỗi `Bind for 0.0.0.0:8080 failed: port is already allocated` khi khởi chạy container.
*   **Nguyên nhân:** Cổng kết nối ngoài máy của bạn (ví dụ 8080) đang bị chiếm dụng bởi một phần mềm khác hoặc một container Docker khác.
*   **Cách khắc phục:**
    1.  Kiểm tra xem container nào đang chiếm dụng cổng bằng lệnh: `docker ps`.
    2.  Dừng container đó lại bằng lệnh: `docker stop <tên_container>`.
    3.  Hoặc đổi sang một cổng trống khác ngoài máy khi chạy: `docker run -d -p 9090:80 nginx` (cổng 9090 ngoài máy trỏ vào cổng 80 trong container).

### ❌ Lỗi 4: Lỗi hết dung lượng bộ nhớ ảo `No space left on device`
*   **Triệu chứng:** Không thể tải thêm Image mới hoặc container tự động sập giữa chừng.
*   **Nguyên nhân:** Phân vùng đĩa ảo cấp phát cho Docker Desktop đã bị đầy hoàn toàn.
*   **Cách khắc phục:** Thực hiện quy trình dọn dẹp hệ thống triệt để:
    ```bash
    docker system prune -a --volumes
    ```

---

## 8️⃣ Quản Lý Vòng Đời: Nâng Cấp Và Gỡ Bỏ Sạch Sẽ

### 1. Cách nâng cấp phiên bản Docker
*   **Với Docker Desktop (Mac/Win):** Hệ thống sẽ hiển thị một chấm tròn thông báo bản update ở góc màn hình. Bạn chỉ cần click chọn **Update and Restart** để hệ thống tự động tải và cài đặt đè.
*   **Với Linux apt:** Chạy bộ lệnh cập nhật hệ thống thông thường:
    ```bash
    sudo apt update
    sudo apt --only-upgrade install -y docker-ce docker-ce-cli
    ```

---

### 2. Cách gỡ bỏ hoàn toàn Docker sạch sẽ khỏi máy tính
Nếu bạn muốn dọn sạch máy để cài lại từ đầu:

*   **Trên Windows:** Vào **Settings** -> **Apps** -> **Installed Apps** -> Gỡ cài đặt **Docker Desktop**. Sau đó xóa thủ công thư mục cấu hình ẩn: `C:\Users\<Tên_User>\.docker`.
*   **On macOS:** Chọn **Troubleshoot (Hình biểu tượng cái phao cứu sinh)** trên giao diện Docker Desktop -> Chọn **Uninstall** -> Kéo ứng dụng Docker thả vào Thùng rác. Chạy lệnh sau trên Terminal để xóa file rác:
    ```bash
    rm -rf ~/.docker
    rm -rf ~/Library/Containers/com.docker.docker
    ```
*   **Trên Linux:** Gỡ bỏ các gói dịch vụ và xóa sạch thư mục lưu trữ dữ liệu container gốc:
    ```bash
    sudo apt purge -y docker-ce docker-ce-cli containerd.io
    sudo rm -rf /var/lib/docker
    sudo rm -rf /var/lib/containerd
    ```

---

## 9️⃣ Bức Tranh Toàn Cảnh: Các Công Cụ Thay Thế Docker Trong Năm 2026

Mặc dù Docker là tiêu chuẩn vàng thống trị tuyệt đối, thế giới container hóa năm 2026 cung cấp thêm các sự lựa chọn thay thế rất đáng giá:

| Công cụ thay thế | Điểm mạnh vượt trội | Khi nào bạn nên chọn? |
| :--- | :--- | :--- |
| **OrbStack** (macOS) | **Siêu tốc và siêu nhẹ.** Khởi động chỉ mất 2 giây, tốn ít hơn 80% RAM so với Docker Desktop. Tích hợp cực mượt mà với Finder của Mac. | Lập trình viên sử dụng máy Mac cấu hình vừa phải, muốn tối ưu hóa pin và hiệu năng RAM. |
| **Podman** | **Rootless Security.** Không cần chạy một tiến trình ngầm quyền root (Daemonless), nâng cao bảo mật hệ thống tối đa. Cú pháp lệnh giống 100% Docker. | Môi trường doanh nghiệp yêu cầu bảo mật thông tin cực kỳ khắt khe. |
| **Colima** (macOS) | Mã nguồn mở hoàn toàn, quản lý qua dòng lệnh cực kỳ gọn nhẹ để thay thế cho bản Docker Desktop thương mại. | Các doanh nghiệp lớn muốn tránh phí bản quyền thương mại của Docker Desktop. |

> [!TIP]
> **Khuyên dùng từ Mr.Rom:**  
> Nếu bạn đang sử dụng MacBook, mình cực kỳ khuyến khích bạn tải dùng thử **OrbStack**. Công cụ này tương thích hoàn toàn với tất cả các câu lệnh `docker` và `docker-compose` tiêu chuẩn của bạn, nhưng tốc độ chạy và khả năng tiết kiệm RAM của nó sẽ khiến bạn vô cùng kinh ngạc!

---

## 🔗 Liên kết bài học tiếp theo

Môi trường Container của bạn đã được kích hoạt hoàn tất! Hãy tự tin bước vào bài học đầu tiên để làm chủ công nghệ này:

*   📖 [Bài 01: Bản chất của Docker và Cuộc cách mạng Container hóa](../lessons/01_basic/00_what-is-docker.md)
*   📖 [Bài 02: Làm chủ 8 lệnh điều khiển Image và Container cơ bản](../lessons/01_basic/01_images-and-containers.md)
*   🧭 [Tấm bản đồ sự nghiệp: DevOps Engineer Career Roadmap](../../../00_roadmaps/career/devops-engineer_career-roadmap.md)

---

## 📌 Nhật ký thay đổi (Changelog)

*   **v1.0.0 (16/05/2026)** — Phiên bản đầu tiên của Mr.Rom hướng dẫn cài đặt Docker Desktop, Engine trên các OS.
*   **v2.0.0 (26/05/2026)** — **Bản nâng cấp Premium bởi Mr.Rom** — Thay đổi tiêu đề H1 và metadata block chuẩn Blueprint; bổ sung câu chuyện dẫn nhập về bãi chiến trường cài database của Nam và ẩn dụ sư phạm container di động ngoài sân vườn; đổi H2 sang dạng câu hỏi mở tư duy; chuẩn hóa 100% Alerts sang định dạng GitHub Alerts; Việt hóa toàn diện comment trong các code block cài đặt Linux và chạy thử Nginx; bổ sung đánh giá các công cụ thay thế OrbStack/Podman hiện đại.
