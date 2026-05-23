# verify_track1.ps1 - Kiểm tra môi trường Track 1

Write-Host "🔍 Đang kiểm tra môi trường Track 1..." -ForegroundColor Cyan
Write-Host "========================================"

$pass = 0
$fail = 0

# Check WSL
try {
    $wslVersion = wsl --version 2>$null
    Write-Host "✅ WSL: Installed" -ForegroundColor Green
    $pass++
}
catch {
    Write-Host "❌ WSL: CHƯA CÀI ĐẶT" -ForegroundColor Red
    $fail++
}

# Check Git
try {
    $gitVersion = git --version 2>$null
    Write-Host "✅ Git: $gitVersion" -ForegroundColor Green
    $pass++
}
catch {
    Write-Host "❌ Git: CHƯA CÀI ĐẶT" -ForegroundColor Red
    $fail++
}

# Check VS Code
try {
    $codeVersion = code --version 2>$null
    Write-Host "✅ VS Code: Installed" -ForegroundColor Green
    $pass++
}
catch {
    Write-Host "❌ VS Code: CHƯA CÀI ĐẶT" -ForegroundColor Red
    $fail++
}

# Check Docker
try {
    $dockerVersion = docker --version 2>$null
    Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
    $pass++
}
catch {
    Write-Host "❌ Docker: CHƯA CÀI ĐẶT" -ForegroundColor Red
    $fail++
}

Write-Host "========================================"
Write-Host "📊 Kết quả: $pass ✅ PASS | $fail ❌ FAIL"

if ($fail -eq 0) {
    Write-Host "🎉 CHÚC MỪNG! Bạn đã sẵn sàng học Track 1!" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Vui lòng cài đặt các tools còn thiếu." -ForegroundColor Yellow
}
