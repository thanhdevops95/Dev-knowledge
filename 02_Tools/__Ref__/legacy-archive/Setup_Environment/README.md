# Thiết lập Môi trường DevOps (Environment Setup)

Chào mừng bạn đến với module đầu tiên của **DevOps Journey**! Để bắt đầu hành trình trở thành một DevOps Engineer, việc chuẩn bị một môi trường làm việc mạnh mẽ và đầy đủ công cụ là bước quan trọng nhất.

Tài liệu này sẽ hướng dẫn bạn cài đặt các công cụ cốt lõi (Core Tools) cần thiết cho toàn bộ khóa học, bao gồm: Git, Docker, VS Code, Terraform, Ansible, và Kubernetes CLI.

#📚 Bảng thuật ngữ (CHEAT SHEET)

Trước khi bắt đầu, hãy làm quen với các thuật ngữ quan trọng trong phần :
{Link tới cheat sheet}




# Danh sách công cụ cần thiết

| Công cụ | Mục đích | Phiên bản khuyến nghị |
| :--- | :--- | :--- |
| **Visual Studio Code** | Trình soạn thảo mã nguồn (Code Editor) tốt nhất hiện nay. | Mới nhất |
| **Git** | Quản lý phiên bản mã nguồn (SCM). | > 2.30 |
| **Docker & Docker Compose** | Nền tảng Containerization để chạy ứng dụng. | > 20.10 |
| **Node.js** | Môi trường chạy JavaScript (cần cho một số bài lab Frontend/Backend). | LTS (16.x hoặc 18.x) |
| **Terraform** | Công cụ Infrastructure as Code (IaC). | > 1.0 |
| **Ansible** | Công cụ quản lý cấu hình (Configuration Management). | > 2.9 |
| **Kubectl** | Công cụ dòng lệnh để tương tác với Kubernetes. | Mới nhất |
| **AWS CLI** | (Tùy chọn) Công cụ dòng lệnh của AWS. | v2 |

---

## Hướng dẫn Cài đặt Thủ công

### 1. Windows

Đối với Windows, chúng tôi khuyến khích sử dụng **WSL2 (Windows Subsystem for Linux)** để có trải nghiệm giống Linux nhất. Tuy nhiên, bạn cũng có thể cài đặt trực tiếp lên Windows.

**Cách 1: Sử dụng Chocolatey (Khuyên dùng)**
Nếu bạn đã cài [Chocolatey](https://chocolatey.org/), hãy mở PowerShell với quyền Administrator và chạy:

```powershell
choco install git docker-desktop vscode nodejs terraform kubernetes-cli awscli -y
```

**Cách 2: Cài đặt từng phần mềm**
1.  **VS Code**: Tải từ [code.visualstudio.com](https://code.visualstudio.com/).
2.  **Git**: Tải từ [git-scm.com](https://git-scm.com/download/win). Khi cài đặt, chọn "Git Bash Here" để có terminal xịn xò.
3.  **Docker Desktop**: Tải từ [docker.com](https://www.docker.com/products/docker-desktop). *Lưu ý: Cần bật ảo hóa (Virtualization) trong BIOS.*
4.  **Terraform**: Tải binary từ [terraform.io](https://www.terraform.io/downloads), giải nén và thêm vào biến môi trường PATH.

### 2. macOS

Trên macOS, công cụ quản lý gói tốt nhất là **Homebrew**.

1.  **Cài đặt Homebrew** (nếu chưa có):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Cài đặt các công cụ**:
    ```bash
    brew install git node terraform ansible kubectl awscli
    brew install --cask docker visual-studio-code
    ```

### 3. Linux (Ubuntu/Debian)

Sử dụng `apt` để cài đặt.

1.  **Cập nhật hệ thống**:
    ```bash
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y curl wget unzip software-properties-common
    ```

2.  **Cài đặt Git & Node.js**:
    ```bash
    sudo apt-get install -y git nodejs npm
    ```

3.  **Cài đặt Docker**:
    Tham khảo hướng dẫn chính thức tại docs.docker.com để cài bản mới nhất.

4.  **Cài đặt Terraform**:
    ```bash
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install terraform
    ```

5.  **Cài đặt Ansible**:
    ```bash
    sudo add-apt-repository --yes --update ppa:ansible/ansible
    sudo apt install -y ansible
    ```

---

## Cài đặt Tự động (Automation Scripts)

Để tiết kiệm thời gian, chúng tôi cung cấp các script cài đặt tự động trong thư mục `scripts/`.

### Cấu trúc thư mục
```
0.Setup_Environment/
├── scripts/
│   ├── install_windows.ps1  # Script cho Windows
│   ├── install_unix.sh      # Script cho macOS và Linux
│   └── verify_env.sh        # Script kiểm tra sau khi cài đặt
├── README.md
└── ...
```

### Cách sử dụng

**Trên Windows (PowerShell Administrator):**
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; ./scripts/install_windows.ps1
```

**Trên macOS/Linux:**
```bash
chmod +x scripts/*.sh
./scripts/install_unix.sh
```

### Kiểm tra cài đặt (Verify)

Sau khi cài đặt xong, hãy chạy script kiểm tra để đảm bảo mọi thứ đã sẵn sàng:

```bash
# Trên Git Bash hoặc Terminal
./scripts/verify_env.sh
```

---

## Khắc phục sự cố thường gặp

1.  **Lỗi Docker không chạy trên Windows**:
    *   Đảm bảo bạn đã bật WSL2.
    *   Kiểm tra Task Manager xem Docker Desktop Service có đang chạy không.

2.  **Lỗi "command not found"**:
    *   Thường do biến môi trường `PATH` chưa được cập nhật. Hãy thử khởi động lại Terminal hoặc máy tính.

3.  **Lỗi quyền (Permission denied) trên Linux**:
    *   Thêm `sudo` trước câu lệnh.
    *   Để chạy Docker không cần sudo: `sudo usermod -aG docker $USER` sau đó đăng xuất và đăng nhập lại.

Chúc bạn cài đặt thành công và sẵn sàng cho bài học tiếp theo!