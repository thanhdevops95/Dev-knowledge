#!/bin/bash
# ============================================================
# Script tự động cài đặt môi trường DevOps cho macOS
# 
# Sử dụng: bash scripts/setup-mac.sh
# ============================================================

set -e

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 BẮT ĐẦU CÀI ĐẶT MÔI TRƯỜNG DEVOPS CHO macOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================================
# PHẦN 1: CÀI ĐẶT HOMEBREW
# ============================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 1: Cài đặt Homebrew"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v brew &> /dev/null; then
    echo "📥 Đang cài đặt Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew đã được cài đặt"
fi

# ============================================================
# PHẦN 2: CÀI ĐẶT TERMINAL TOOLS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 2: Cài đặt iTerm2 & Rectangle"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "📥 Đang cài đặt iTerm2 và Rectangle..."
brew install --cask iterm2 rectangle || echo "⚠️ Có thể đã cài đặt"

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
else
    echo "✅ Oh My Zsh đã được cài đặt"
fi

# ============================================================
# PHẦN 4: CÀI ĐẶT DEVOPS TOOLS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 4: Cài đặt DevOps Tools"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🛠️ Đang cài đặt Git, Docker, Kubectl, Terraform..."
brew install git wget curl jq htop \
    docker docker-compose \
    kubectl helm k9s \
    terraform ansible \
    awscli \
    pre-commit gitleaks || echo "⚠️ Một số tools có thể đã cài đặt"

# ============================================================
# PHẦN 5: CÀI ĐẶT PYTHON
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 5: Cài đặt Python 3.11"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🐍 Đang cài đặt Python..."
brew install python@3.11 || echo "✅ Python đã được cài đặt"

# ============================================================
# PHẦN 6: CÀI ĐẶT VS CODE
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 6: Cài đặt VS Code"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! command -v code &> /dev/null; then
    echo "📥 Đang cài đặt VS Code..."
    brew install --cask visual-studio-code
else
    echo "✅ VS Code đã được cài đặt"
fi

# ============================================================
# PHẦN 7: CÀI ĐẶT ZSH PLUGINS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 7: Cài đặt Zsh Plugins"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "🎨 Đang cài đặt zsh-autosuggestions..."
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions 2>/dev/null || echo "✅ zsh-autosuggestions đã có"

echo "🎨 Đang cài đặt zsh-syntax-highlighting..."
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting 2>/dev/null || echo "✅ zsh-syntax-highlighting đã có"

# ============================================================
# PHẦN 8: CẤU HÌNH GIT
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 PHẦN 8: Cấu hình Git"
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
echo "✅ HOÀN TẤT CÀI ĐẶT macOS!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 BƯỚC TIẾP THEO:"
echo ""
echo "   1. Mở iTerm2 và đặt font thành 'FiraCode Nerd Font'"
echo ""
echo "   2. Thêm plugins vào ~/.zshrc:"
echo "      plugins=(git zsh-autosuggestions zsh-syntax-highlighting)"
echo ""
echo "   3. Chạy lệnh sau để áp dụng thay đổi:"
echo "      source ~/.zshrc"
echo ""
echo "   4. Cài đặt Docker Desktop từ:"
echo "      https://www.docker.com/products/docker-desktop"
echo ""
echo "   5. Kiểm tra cài đặt:"
echo "      bash scripts/verify-tools.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Chúc bạn học tốt!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
