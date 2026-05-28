#!/bin/bash
# ============================================================
# Script tự động cài đặt môi trường DevOps cho Linux (Ubuntu/Debian)
# 
# Sử dụng: bash scripts/setup-linux.sh
# ============================================================

set -e

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 BẮT ĐẦU CÀI ĐẶT MÔI TRƯỜNG DEVOPS CHO LINUX"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================================
# PHẦN 1: CẬP NHẬT HỆ THỐNG
# ============================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 1: Cập nhật hệ thống"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "📥 Đang cập nhật hệ thống..."
sudo apt update && sudo apt upgrade -y

# ============================================================
# PHẦN 2: CÀI ĐẶT CÁC GÓI CƠ BẢN
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 2: Cài đặt gói cơ bản"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🛠️ Đang cài đặt Git, Python, Zsh..."
sudo apt install -y git wget curl jq htop zsh unzip \
    python3 python3-pip build-essential

# ============================================================
# PHẦN 3: CÀI ĐẶT OH MY ZSH
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 3: Cài đặt Oh My Zsh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "📥 Đang cài đặt Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    chsh -s $(which zsh) || echo "⚠️ Cần chạy thủ công: chsh -s \$(which zsh)"
else
    echo "✅ Oh My Zsh đã được cài đặt"
fi

# ============================================================
# PHẦN 4: CÀI ĐẶT DOCKER
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 4: Cài đặt Docker"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v docker &> /dev/null; then
    echo "🐳 Đang cài đặt Docker..."
    sudo apt install -y docker.io docker-compose-plugin
    sudo usermod -aG docker $USER
    sudo systemctl enable docker
    sudo systemctl start docker
    echo "⚠️ Cần logout và login lại để Docker group có hiệu lực"
else
    echo "✅ Docker đã được cài đặt"
fi

# ============================================================
# PHẦN 5: CÀI ĐẶT KUBECTL
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 5: Cài đặt kubectl"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v kubectl &> /dev/null; then
    echo "☸️ Đang cài đặt kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
else
    echo "✅ kubectl đã được cài đặt"
fi

# ============================================================
# PHẦN 6: CÀI ĐẶT TERRAFORM
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 6: Cài đặt Terraform"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v terraform &> /dev/null; then
    echo "🏗️ Đang cài đặt Terraform..."
    wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install -y terraform
else
    echo "✅ Terraform đã được cài đặt"
fi

# ============================================================
# PHẦN 7: CÀI ĐẶT ANSIBLE
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 7: Cài đặt Ansible"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v ansible &> /dev/null; then
    echo "📜 Đang cài đặt Ansible..."
    sudo apt install -y ansible
else
    echo "✅ Ansible đã được cài đặt"
fi

# ============================================================
# PHẦN 8: CÀI ĐẶT AWS CLI
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 8: Cài đặt AWS CLI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v aws &> /dev/null; then
    echo "☁️ Đang cài đặt AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip -q awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
else
    echo "✅ AWS CLI đã được cài đặt"
fi

# ============================================================
# PHẦN 9: CÀI ĐẶT HELM
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 9: Cài đặt Helm"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v helm &> /dev/null; then
    echo "⛵ Đang cài đặt Helm..."
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
else
    echo "✅ Helm đã được cài đặt"
fi

# ============================================================
# PHẦN 10: CÀI ĐẶT HOMEBREW + K9S + GITLEAKS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 10: Cài đặt k9s & gitleaks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v brew &> /dev/null; then
    echo "🍺 Đang cài đặt Homebrew for Linux..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.zshrc
fi

echo "📥 Đang cài đặt k9s, gitleaks, pre-commit..."
brew install k9s gitleaks pre-commit || echo "⚠️ Một số tools có thể đã cài đặt"

# ============================================================
# PHẦN 11: CÀI ĐẶT ZSH PLUGINS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 11: Cài đặt Zsh Plugins"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🎨 Đang cài đặt zsh-autosuggestions..."
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions 2>/dev/null || echo "✅ zsh-autosuggestions đã có"

echo "🎨 Đang cài đặt zsh-syntax-highlighting..."
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting 2>/dev/null || echo "✅ zsh-syntax-highlighting đã có"

# ============================================================
# PHẦN 12: CẤU HÌNH GIT
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 12: Cấu hình Git"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🔧 Nhập thông tin Git của bạn:"
read -p "   Nhập tên của bạn: " git_name
read -p "   Nhập email của bạn: " git_email
git config --global user.name "$git_name"
git config --global user.email "$git_email"
echo "✅ Đã cấu hình Git"

# ============================================================
# HOÀN TẤT
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ HOÀN TẤT CÀI ĐẶT LINUX!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 BƯỚC TIẾP THEO:"
echo ""
echo "   1. Logout và login lại để Docker group có hiệu lực"
echo ""
echo "   2. Thêm plugins vào ~/.zshrc:"
echo "      plugins=(git zsh-autosuggestions zsh-syntax-highlighting)"
echo ""
echo "   3. Chạy lệnh sau để áp dụng thay đổi:"
echo "      source ~/.zshrc"
echo ""
echo "   4. Kiểm tra cài đặt:"
echo "      bash scripts/verify-tools.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Chúc bạn học tốt!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
