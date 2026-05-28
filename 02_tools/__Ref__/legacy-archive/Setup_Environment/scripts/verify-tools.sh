#!/bin/bash
# ============================================================
# Script kiểm tra các công cụ DevOps đã được cài đặt chưa
# 
# Sử dụng: bash scripts/verify-tools.sh
# ============================================================

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 KIỂM TRA MÔI TRƯỜNG DEVOPS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================================
# HÀM KIỂM TRA CÔNG CỤ
# ============================================================
check_tool() {
    if command -v $1 &> /dev/null; then
        version=$($1 --version 2>&1 | head -n 1)
        echo "✅ $1: $version"
        return 0
    else
        echo "❌ $1: Chưa cài đặt"
        return 1
    fi
}

# ============================================================
# KIỂM TRA CÔNG CỤ CƠ BẢN
# ============================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Công cụ cơ bản"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

missing_count=0
check_tool "git" || ((missing_count++))
check_tool "python3" || ((missing_count++))
check_tool "code" || ((missing_count++))

# ============================================================
# KIỂM TRA CONTAINER TOOLS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐳 Container & Orchestration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_tool "docker" || ((missing_count++))
check_tool "docker-compose" || check_tool "docker" || true
check_tool "kubectl" || ((missing_count++))
check_tool "helm" || ((missing_count++))
check_tool "k9s" || ((missing_count++))

# ============================================================
# KIỂM TRA IaC TOOLS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏗️ Infrastructure as Code"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_tool "terraform" || ((missing_count++))
check_tool "ansible" || ((missing_count++))
check_tool "aws" || ((missing_count++))

# ============================================================
# KIỂM TRA SECURITY TOOLS
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Security & Quality"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_tool "gitleaks" || true
check_tool "pre-commit" || true

# ============================================================
# KẾT QUẢ
# ============================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $missing_count -eq 0 ]; then
    echo "🎉 TẤT CẢ CÔNG CỤ ĐÃ ĐƯỢC CÀI ĐẶT!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🚀 Bạn đã sẵn sàng bắt đầu khóa học!"
    echo ""
    echo "   Bước tiếp theo: Đọc README.md và bắt đầu với Module 01"
    echo ""
else
    echo "⚠️  CÒN $missing_count CÔNG CỤ CHƯA CÀI ĐẶT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "💡 Chạy script setup tương ứng với OS của bạn:"
    echo ""
    echo "   • macOS:   bash scripts/setup-mac.sh"
    echo "   • Linux:   bash scripts/setup-linux.sh"
    echo "   • Windows: .\\scripts\\setup-windows.ps1 (PowerShell Admin)"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
