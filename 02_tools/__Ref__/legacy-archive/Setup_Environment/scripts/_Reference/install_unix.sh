#!/bin/bash

# Script cài đặt môi trường DevOps cho macOS và Linux (Ubuntu/Debian)

set -e # Dừng script nếu có lỗi xảy ra

echo "=== Bắt đầu thiết lập môi trường DevOps ==="

OS="$(uname -s)"

install_mac() {
    echo "Phát hiện hệ điều hành: macOS"
    
    # Kiểm tra Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Homebrew chưa được cài đặt. Đang cài đặt..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew đã được cài đặt. Đang cập nhật..."
        brew update
    fi

    echo "Đang cài đặt các công cụ..."
    brew install git node terraform ansible kubectl awscli
    
    echo "Đang cài đặt Docker và VS Code (Cask)..."
    brew install --cask docker visual-studio-code
}

install_linux() {
    echo "Phát hiện hệ điều hành: Linux"
    
    # Yêu cầu quyền root
    if [ "$EUID" -ne 0 ]; then 
        echo "Vui lòng chạy script với quyền root (sudo ./install_unix.sh)"
        exit 1
    fi

    echo "Cập nhật hệ thống..."
    apt-get update && apt-get upgrade -y
    apt-get install -y curl wget unzip software-properties-common git nodejs npm

    # Cài đặt Terraform
    echo "Cài đặt Terraform..."
    wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list
    apt-get update && apt-get install -y terraform

    # Cài đặt Ansible
    echo "Cài đặt Ansible..."
    add-apt-repository --yes --update ppa:ansible/ansible
    apt-get install -y ansible

    # Cài đặt Kubectl
    echo "Cài đặt Kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl

    # Cài đặt AWS CLI
    echo "Cài đặt AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    ./aws/install --update
    rm -rf aws awscliv2.zip

    # Cài đặt Docker
    echo "Cài đặt Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh

    if [ -n "$SUDO_USER" ]; then
        echo "Thêm user $SUDO_USER vào group docker..."
        usermod -aG docker $SUDO_USER
    fi
}

if [ "$OS" = "Darwin" ]; then
    install_mac
elif [ "$OS" = "Linux" ]; then
    install_linux
else
    echo "Hệ điều hành không được hỗ trợ bởi script này: $OS"
    exit 1
fi

echo "=== Cài đặt hoàn tất! ==="
echo "Vui lòng khởi động lại terminal."