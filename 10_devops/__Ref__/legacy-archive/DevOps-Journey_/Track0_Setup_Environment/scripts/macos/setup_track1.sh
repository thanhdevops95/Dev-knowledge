#!/bin/bash
# setup_track1.sh - Cài đặt môi trường Track 1 cho macOS

echo "🚀 Đang cài đặt môi trường Track 1..."

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "📦 Đang cài đặt Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install tools
echo "📦 Đang cài đặt Git..."
brew install git

echo "📦 Đang cài đặt Docker..."
brew install --cask docker

echo "📦 Đang cài đặt VS Code..."
brew install --cask visual-studio-code

echo "✅ Hoàn thành cài đặt Track 1!"
