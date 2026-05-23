# Script cài đặt môi trường DevOps cho Windows
# Yêu cầu: Chạy với quyền Administrator

Write-Host "=== Bắt đầu thiết lập môi trường DevOps trên Windows ===" -ForegroundColor Cyan

# 1. Kiểm tra và cài đặt Chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey chưa được cài đặt. Đang tiến hành cài đặt..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    
    # Refresh biến môi trường để nhận lệnh choco ngay lập tức
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
} else {
    Write-Host "Chocolatey đã được cài đặt." -ForegroundColor Green
}

# 2. Danh sách các gói cần cài đặt
$packages = @(
    "git",
    "vscode",
    "docker-desktop",
    "nodejs-lts",
    "terraform",
    "kubernetes-cli",
    "awscli",
    "putty" # Hữu ích để SSH
)

# 3. Cài đặt các gói
foreach ($pkg in $packages) {
    Write-Host "Đang kiểm tra/cài đặt: $pkg ..." -ForegroundColor Cyan
    choco install $pkg -y
}

Write-Host "=== Cài đặt hoàn tất! ===" -ForegroundColor Green
Write-Host "Lưu ý:" -ForegroundColor Yellow
Write-Host "1. Vui lòng khởi động lại máy tính hoặc log out/log in để cập nhật biến môi trường."
Write-Host "2. Hãy mở Docker Desktop và đợi nó khởi động xong."
Write-Host "3. Chạy script 'verify_env.sh' (bằng Git Bash) để kiểm tra lại các phiên bản."

# Pause để người dùng đọc
Read-Host -Prompt "Nhấn Enter để thoát"