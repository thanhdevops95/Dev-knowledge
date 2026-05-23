#!/bin/bash

# Script kiểm tra các công cụ đã cài đặt

echo "=== KIỂM TRA MÔI TRƯỜNG DEVOPS ==="
echo ""

check_tool() {
    TOOL_NAME=$1
    CMD=$2
    
    if command -v $TOOL_NAME &> /dev/null; then
        VERSION=$($CMD 2>&1 | head -n 1)
        echo -e "✅ \033[32m$TOOL_NAME\033[0m: Đã cài đặt ($VERSION)"
    else
        echo -e "❌ \033[31m$TOOL_NAME\033[0m: Chưa tìm thấy!"
    fi
}

# Kiểm tra từng công cụ
check_tool "git" "git --version"
check_tool "node" "node --version"
check_tool "code" "code --version" # VS Code command line
check_tool "docker" "docker --version"

# Kiểm tra Docker Compose (Ưu tiên Plugin 'docker compose')
if docker compose version &> /dev/null; then
    VERSION=$(docker compose version | head -n 1)
    echo -e "✅ \033[32mdocker compose\033[0m: Đã cài đặt ($VERSION)"
else
    check_tool "docker-compose" "docker-compose --version"
fi

check_tool "terraform" "terraform --version"
check_tool "ansible" "ansible --version"
check_tool "kubectl" "kubectl version --client"
check_tool "aws" "aws --version"

echo ""
echo "=== KẾT THÚC KIỂM TRA ==="
echo "Nếu có công cụ nào hiện dấu ❌, vui lòng xem lại file README.md để cài đặt."