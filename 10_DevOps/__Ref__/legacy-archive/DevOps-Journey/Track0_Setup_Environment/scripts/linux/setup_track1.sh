#!/bin/bash
# setup_track1.sh - Cài đặt môi trường Track 1 cho Linux

echo "🚀 Đang cài đặt môi trường Track 1..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Git
echo "📦 Đang cài đặt Git..."
sudo apt install -y git

# Install Docker
echo "📦 Đang cài đặt Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install VS Code
echo "📦 Đang cài đặt VS Code..."
sudo snap install code --classic

echo "✅ Hoàn thành cài đặt Track 1!"
echo "⚠️ Vui lòng logout và login lại để Docker hoạt động."
