# ============================================================
# Script tự động cài đặt môi trường DevOps cho Windows 10/11
# Sử dụng WSL 2 (Windows Subsystem for Linux)
# 
# Chạy PowerShell với quyền Administrator:
# .\scripts\setup-windows.ps1
# ============================================================

Write-Host "🚀 Bắt đầu cài đặt môi trường DevOps cho Windows..." -ForegroundColor Cyan
Write-Host ""

# Kiểm tra quyền Administrator
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Vui lòng chạy PowerShell với quyền Administrator!" -ForegroundColor Red
    Write-Host "   Chuột phải PowerShell → Run as Administrator" -ForegroundColor Yellow
    exit 1
}

# ============================================================
# PHẦN 1: CÀI ĐẶT WSL 2 VÀ UBUNTU
# ============================================================
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 1: Cài đặt WSL 2 + Ubuntu" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

# Kiểm tra WSL đã cài chưa
$wslInstalled = Get-Command wsl -ErrorAction SilentlyContinue

if (-not $wslInstalled) {
    Write-Host "📥 Đang cài đặt WSL 2..." -ForegroundColor Green
    wsl --install -d Ubuntu
    Write-Host ""
    Write-Host "⚠️  QUAN TRỌNG:" -ForegroundColor Yellow
    Write-Host "   1. Khởi động lại máy sau khi cài xong" -ForegroundColor Yellow
    Write-Host "   2. Sau khi restart, mở Ubuntu từ Start Menu" -ForegroundColor Yellow
    Write-Host "   3. Tạo username và password cho Ubuntu" -ForegroundColor Yellow
    Write-Host "   4. Chạy lại script này" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Nhấn Enter để tiếp tục..."
} else {
    Write-Host "✅ WSL đã được cài đặt" -ForegroundColor Green
    
    # Kiểm tra Ubuntu
    $ubuntuInstalled = wsl -l -v 2>&1 | Select-String "Ubuntu"
    if (-not $ubuntuInstalled) {
        Write-Host "📥 Đang cài đặt Ubuntu..." -ForegroundColor Green
        wsl --install -d Ubuntu
    } else {
        Write-Host "✅ Ubuntu đã được cài đặt" -ForegroundColor Green
    }
}

# ============================================================
# PHẦN 2: CÀI ĐẶT WINDOWS TERMINAL
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 2: Cài đặt Windows Terminal" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$wtInstalled = Get-Command wt -ErrorAction SilentlyContinue
if (-not $wtInstalled) {
    Write-Host "📥 Đang cài đặt Windows Terminal..." -ForegroundColor Green
    winget install Microsoft.WindowsTerminal --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "✅ Windows Terminal đã được cài đặt" -ForegroundColor Green
}

# ============================================================
# PHẦN 3: CÀI ĐẶT DOCKER DESKTOP
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 3: Cài đặt Docker Desktop" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "📥 Đang cài đặt Docker Desktop..." -ForegroundColor Green
    winget install Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
    Write-Host "⚠️  Sau khi cài xong, mở Docker Desktop và enable WSL 2 backend" -ForegroundColor Yellow
} else {
    Write-Host "✅ Docker đã được cài đặt" -ForegroundColor Green
}

# ============================================================
# PHẦN 4: CÀI ĐẶT VS CODE
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 4: Cài đặt VS Code" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$codeInstalled = Get-Command code -ErrorAction SilentlyContinue
if (-not $codeInstalled) {
    Write-Host "📥 Đang cài đặt VS Code..." -ForegroundColor Green
    winget install Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "✅ VS Code đã được cài đặt" -ForegroundColor Green
}

# ============================================================
# PHẦN 5: CÀI ĐẶT GIT
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 5: Cài đặt Git" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "📥 Đang cài đặt Git..." -ForegroundColor Green
    winget install Git.Git --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "✅ Git đã được cài đặt" -ForegroundColor Green
}

# ============================================================
# PHẦN 6: CÀI ĐẶT PYTHON
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "📦 PHẦN 6: Cài đặt Python 3.11" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "📥 Đang cài đặt Python 3.11..." -ForegroundColor Green
    winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements
} else {
    Write-Host "✅ Python đã được cài đặt" -ForegroundColor Green
}

# ============================================================
# HOÀN TẤT
# ============================================================
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "✅ HOÀN TẤT CÀI ĐẶT WINDOWS!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "📝 BƯỚC TIẾP THEO:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Khởi động lại máy (nếu chưa)" -ForegroundColor White
Write-Host ""
Write-Host "2. Mở Windows Terminal → chọn tab Ubuntu" -ForegroundColor White
Write-Host ""
Write-Host "3. Trong Ubuntu, chạy lệnh sau để cài đặt tools DevOps:" -ForegroundColor White
Write-Host "   cd devops-course" -ForegroundColor Yellow
Write-Host "   bash scripts/setup-linux.sh" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Mở Docker Desktop và enable WSL 2 backend:" -ForegroundColor White
Write-Host "   Settings → General → Use the WSL 2 based engine ✓" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  LƯU Ý QUAN TRỌNG:" -ForegroundColor Red
Write-Host "   Luôn chạy các lệnh DevOps trong WSL Ubuntu," -ForegroundColor Yellow
Write-Host "   KHÔNG chạy trong PowerShell/CMD!" -ForegroundColor Yellow
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🎉 Chúc bạn học tốt!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
