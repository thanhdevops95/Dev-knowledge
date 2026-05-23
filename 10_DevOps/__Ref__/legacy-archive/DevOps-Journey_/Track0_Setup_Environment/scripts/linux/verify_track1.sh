#!/bin/bash
# verify_track1.sh - Kiểm tra môi trường Track 1

echo "🔍 Đang kiểm tra môi trường Track 1..."
echo "========================================"

PASS=0
FAIL=0

# Check Git
if command -v git &> /dev/null; then
    echo "✅ Git: $(git --version)"
    ((PASS++))
else
    echo "❌ Git: CHƯA CÀI ĐẶT"
    ((FAIL++))
fi

# Check Docker
if command -v docker &> /dev/null; then
    if docker info &> /dev/null 2>&1; then
        echo "✅ Docker: $(docker --version)"
        ((PASS++))
    else
        echo "⚠️ Docker: Đã cài nhưng không chạy"
        ((FAIL++))
    fi
else
    echo "❌ Docker: CHƯA CÀI ĐẶT"
    ((FAIL++))
fi

# Check VS Code
if command -v code &> /dev/null; then
    echo "✅ VS Code: Installed"
    ((PASS++))
else
    echo "❌ VS Code: CHƯA CÀI ĐẶT"
    ((FAIL++))
fi

echo "========================================"
echo "📊 Kết quả: $PASS ✅ PASS | $FAIL ❌ FAIL"

if [ $FAIL -eq 0 ]; then
    echo "🎉 CHÚC MỪNG! Bạn đã sẵn sàng học Track 1!"
else
    echo "⚠️ Vui lòng cài đặt các tools còn thiếu."
fi
