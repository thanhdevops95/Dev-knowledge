# BEGIN: Giới thiệu & Thiết lập Môi trường Toàn diện

Chào mừng bạn đến với lộ trình đào tạo DevOps! Bài này sẽ giúp bạn chuẩn bị một môi trường làm việc chuyên nghiệp và đầy đủ công cụ cần thiết cho toàn bộ hành trình.

## 1. Giới thiệu DevOps
DevOps là sự kết hợp của văn hóa, các thực hành và công cụ giúp tăng khả năng chuyển giao ứng dụng và dịch vụ ở tốc độ cao.

**Các công cụ chính sẽ học trong lộ trình này:**
- **Quản lý mã nguồn (SCM):** <u>Git</u>
- **Nền tảng SCM:** <u>GitHub</u>, GitLab, Bitbucket
- **Containerization & Orchestration:** <u>Docker</u>, <u>Kubernetes (K8s)</u>, Podman, Docker Swarm
- **Tự động hóa CI/CD:** <u>GitLab CI/CD</u>, Jenkins, GitHub Actions, CircleCI
- **Hạ tầng dưới dạng mã (IaC):** <u>Terraform</u>, OpenTofu, Pulumi, AWS CDK
- **Quản lý cấu hình (CM):** <u>Ansible</u>, Puppet, Chef, SaltStack
- **Giám sát (Monitoring):** <u>Prometheus</u> & <u>Grafana</u>, Datadog, New Relic
- **Quản lý Log:** <u>EFK Stack</u> (Elasticsearch, Fluentd, Kibana), ELK Stack, Loki, Splunk
- **Điện toán đám mây (Cloud):** <u>AWS</u>, Google Cloud (GCP), Microsoft Azure

**Các công cụ và kỹ năng phụ trợ quan trọng:**
- **`kubectl`**: Công cụ dòng lệnh để tương tác với cụm Kubernetes.
- **`aws-cli`**: Công cụ dòng lệnh để làm việc với tài nguyên trên AWS.
- **YAML**: Ngôn ngữ cấu hình được sử dụng trong hầu hết các công cụ DevOps hiện đại (Kubernetes, GitLab CI, Docker Compose, Ansible).
- **`curl`**: Công cụ không thể thiếu để kiểm tra kết nối mạng và các API.

---

## 2. Các tài khoản cần thiết
Bạn cần đăng ký các tài khoản sau (miễn phí) nếu chưa có. Đây là những dịch vụ cốt lõi mà chúng ta sẽ sử dụng.

1.  **Tài khoản Nền tảng SCM:**
    -   **<u>GitHub</u>** (Khuyến nghị): Nơi lưu trữ mã nguồn và portfolio của bạn. [Đăng ký tại đây](https://github.com/).
    -   **GitLab**: Một lựa chọn thay thế mạnh mẽ với CI/CD tích hợp sẵn. [Đăng ký tại đây](https://gitlab.com/users/sign_up).

2.  **Tài khoản Container Registry:**
    -   **<u>Docker Hub</u>**: Nơi lưu trữ các "khuôn mẫu" ứng dụng (Docker Image) của bạn. [Đăng ký tại đây](https://hub.docker.com/).

3.  **Tài khoản Cloud:**
    -   **<u>AWS Free Tier</u>**: Cung cấp 12 tháng sử dụng miễn phí các dịch vụ phổ biến, đủ cho chúng ta thực hành. **Lưu ý:** bạn sẽ cần thẻ tín dụng/ghi nợ quốc tế để đăng ký. [Đăng ký tại đây](https://aws.amazon.com/free/).

4.  **Tài khoản Quản lý dự án:**
    -   **<u>Jira (Atlassian)</u>**: Công cụ theo dõi công việc và quản lý dự án theo phương pháp Agile/Scrum. DevOps không chỉ là code, mà còn là quy trình. [Đăng ký gói miễn phí tại đây](https://www.atlassian.com/software/jira).

---

## 3. Cài đặt Môi trường Dòng lệnh (CLI)
Một môi trường dòng lệnh mạnh mẽ sẽ tăng năng suất của bạn gấp nhiều lần.

### 3.1. MacOS
1.  **Cài đặt Homebrew** (Trình quản lý gói):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2.  **Cài đặt iTerm2 & Rectangle** (Terminal thay thế & Quản lý cửa sổ):
    ```bash
    brew install --cask iterm2 rectangle
    ```
3.  **Cài đặt Oh My Zsh** (Framework cho Zsh):
    ```bash
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
4.  **Cài đặt các công cụ CLI hữu ích:**
    ```bash
    brew install git wget curl jq nmap htop telnet direnv gitleaks helm k9s ansible terraform awscli pre-commit
    ```
5.  **Thiết lập VS Code `code` command:** Mở VS Code, nhấn `Cmd+Shift+P`, gõ `Shell Command` và chọn `Shell Command: Install 'code' command in PATH`.

### 3.2. Linux (Ubuntu/Debian)
1.  **Cài đặt các gói cần thiết & Python Pip:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    sudo apt install git wget curl jq nmap htop telnet zsh unzip python3-pip -y
    ```
2.  **Cài đặt Oh My Zsh** (Tùy chọn nhưng khuyến khích):
    ```bash
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
3.  **Cài đặt các công cụ DevOps khác:**

    - **Terraform (Qua repository của HashiCorp):**
      ```bash
      wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
      echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
      sudo apt update && sudo apt install terraform -y
      ```

    - **Ansible & Direnv (Qua Apt):**
      ```bash
      sudo apt install ansible direnv -y
      ```

    - **AWS CLI:**
      ```bash
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      ```

    - **Helm:**
      ```bash
      curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
      ```

    - **k9s & Gitleaks (Qua Homebrew):**
      Cách dễ nhất là dùng Homebrew cho Linux. Nếu chưa có, hãy cài:
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
      *Lưu ý: Sau khi cài xong, terminal sẽ hướng dẫn bạn 2-3 lệnh để thêm brew vào PATH, hãy làm theo.*
      
      Sau đó, cài đặt công cụ:
      ```bash
      brew install k9s gitleaks
      ```
      *(Ghi chú: Hoặc bạn có thể tải binary trực tiếp từ trang GitHub releases của k9s và gitleaks).*

    - **Pre-commit (Qua Pip):**
      ```bash
      pip3 install pre-commit
      ```

### 3.3. Windows 10/11
Cách tiếp cận tốt nhất trên Windows là sử dụng **Windows Subsystem for Linux (WSL) 2**.
1.  **Cài đặt Windows Terminal & WSL 2 với Ubuntu:**
    - Cài Windows Terminal từ **Microsoft Store** hoặc bằng `winget`:
      ```powershell
      winget install Microsoft.WindowsTerminal
      ```
    - Mở PowerShell với quyền Admin và chạy lệnh sau để cài WSL2 và Ubuntu:
      ```powershell
      wsl --install -d Ubuntu
      ```
    - Khởi động lại máy nếu được yêu cầu. Lần đầu mở Ubuntu, bạn sẽ cần tạo user/password.
2.  **Lưu ý quan trọng cho người dùng Windows:**
    > Hầu hết các công cụ DevOps trong lộ trình này (Ansible, Terraform, kubectl, Docker CLI...) được thiết kế để chạy tốt nhất trên môi trường Linux. Do đó, bạn phải luôn **mở Windows Terminal, chọn tab Ubuntu (WSL)** và **chạy tất cả các lệnh trong đó**, không chạy trên PowerShell hay CMD của Windows.

3.  **Cài đặt Oh My Zsh** (bên trong Terminal Ubuntu của WSL):
    ```bash
    # Cập nhật Ubuntu trước
    sudo apt update && sudo apt upgrade -y
    # Cài đặt Zsh và các công cụ cần thiết
    sudo apt install zsh git wget curl jq nmap htop telnet unzip -y
    # Cài Oh My Zsh
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    ```
4.  **Cài đặt các công cụ DevOps khác** (bên trong Terminal Ubuntu của WSL):
    - Dùng **Homebrew cho Linux** (Cách khuyến nghị):
      ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      ```
      Sau đó thêm brew vào PATH theo hướng dẫn và cài đặt:
      ```bash
      brew install gitleaks helm k9s terraform ansible pre-commit direnv
      ```
    - Cài **AWS CLI**:
      ```bash
      curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
      unzip awscliv2.zip
      sudo ./aws/install
      ```

### 3.4. Nâng cao Terminal & Shell (Tùy chọn nhưng rất khuyến khích)
Để có trải nghiệm terminal "xịn" nhất với icon và gợi ý lệnh:
1.  **Cài đặt Nerd Font:**
    - **Khuyến nghị:** [Fira Code Nerd Font](https://www.nerdfonts.com/font-downloads). Tải về, giải nén và cài đặt font vào hệ điều hành.
    - Sau đó, vào phần cài đặt của **iTerm2 / Windows Terminal / Terminal** và **chọn font chữ là `FiraCode Nerd Font`**.
2.  **Cài đặt Zsh Plugins** (dành cho Oh My Zsh):
    - **zsh-autosuggestions** (Gợi ý lệnh dựa trên lịch sử):
      ```bash
      git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
      ```
    - **zsh-syntax-highlighting** (Tô màu cú pháp cho dòng lệnh):
      ```bash
      git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
      ```
    - Sau đó, mở file `~/.zshrc` và thêm tên các plugin vào dòng `plugins=(...)`, ví dụ:
      `plugins=(git zsh-autosuggestions zsh-syntax-highlighting)`

---
## 4. Cài đặt các Công cụ DevOps chính
1.  **VS Code (Visual Studio Code):**
    - **Tất cả các OS:** Tải từ [trang chủ](https://code.visualstudio.com/) hoặc dùng `winget`/`brew` như trên.
    - **Tích hợp với WSL (cho Windows):** Sau khi cài VS Code trên Windows, mở terminal Ubuntu và gõ `code .` để tự động cài đặt VS Code Server và mở thư mục hiện tại.

2.  **Docker:**
    - **MacOS & Windows:** Tải và cài đặt **Docker Desktop** từ [trang chủ](https://www.docker.com/products/docker-desktop/).
    - **Linux:**
      ```bash
      sudo apt install docker.io docker-compose-plugin -y
      sudo usermod -aG docker $USER
      # Logout và Login lại để có hiệu lực
      ```
3. **Kubernetes (Local):**
   - **Minikube:** Công cụ tạo một cụm Kubernetes chỉ có một node trên máy của bạn. Rất tốt để học tập. [Xem hướng dẫn cài đặt](https://minikube.sigs.k8s.io/docs/start/).
   - **k9s:** Giao diện Terminal UI cực kỳ mạnh mẽ để quản lý cụm Kubernetes. Sau khi cài (ở bước 3), chỉ cần chạy `k9s` trong terminal.

---

## 5. Tối ưu hóa VS Code (Các Extensions hữu ích)
Mở VS Code, vào tab Extensions (Ctrl+Shift+X) và cài đặt các tiện ích sau:

-   **GitLens**: Nâng cấp trải nghiệm Git trong VS Code.
-   **Docker**: Quản lý container và image.
-   **Kubernetes**: Hỗ trợ viết file YAML và quản lý cụm K8s.
-   **HashiCorp Terraform**: Hỗ trợ cho việc viết code Terraform.
-   **Ansible**: Hỗ trợ cho việc viết playbook Ansible.
-   **YAML by Red Hat**: Hỗ trợ và kiểm tra lỗi cho file YAML.
-   **Prettier**: Tự động định dạng code.
-   **EditorConfig for VS Code**: Giúp duy trì style code nhất quán.
-   **Remote - WSL** (Cho người dùng Windows): Giúp VS Code kết nối mượt mà với môi trường WSL.

---

## 6. Cấu hình Git cơ bản (Chung cho mọi OS)
Mở Terminal và chạy lệnh sau với thông tin của bạn:
```bash
git config --global user.name "Ten Cua Ban"
git config --global user.email "email@example.com"
```
**Ghi chú về Diagramming:** Trong quá trình học, bạn nên tập thói quen vẽ biểu đồ kiến trúc. Sử dụng các công cụ như [draw.io](https://app.diagrams.net/) (online) hoặc dùng extension `draw.io` cho VS Code, hoặc học cú pháp **Mermaid** để vẽ diagram dưới dạng code.

---
## 7. Tổng kết & Lời khuyên cho người mới bắt đầu

Danh sách các công cụ ở trên có thể làm bạn choáng ngợp. Đừng lo lắng! Bạn không cần phải thành thạo tất cả ngay lập tức.

**Để bắt đầu, hãy tập trung cài đặt và làm quen với những thứ cơ bản sau:**
- [ ] Một **Terminal** tốt (iTerm2 cho Mac, Windows Terminal + WSL2 cho Windows).
- [ ] Trình quản lý gói **Homebrew** (Mac) hoặc **apt** (Linux/WSL).
- [ ] **Git** để quản lý mã nguồn.
- [ ] **VS Code** làm trình soạn thảo code.
- [ ] **Docker Desktop** (hoặc Docker Engine trên Linux) để làm việc với container.
- [ ] Tạo các tài khoản **GitHub** và **Docker Hub**.

Các công cụ nâng cao khác như **Kubernetes, Terraform, Ansible, Prometheus...** sẽ được giới thiệu và cài đặt ở từng bài học tương ứng khi chúng ta cần đến chúng. Việc cài đặt sẵn tất cả chỉ là một bước chuẩn bị để bạn có một môi trường hoàn chỉnh.

**Bây giờ, bạn đã thực sự sẵn sàng cho bài học đầu tiên!**