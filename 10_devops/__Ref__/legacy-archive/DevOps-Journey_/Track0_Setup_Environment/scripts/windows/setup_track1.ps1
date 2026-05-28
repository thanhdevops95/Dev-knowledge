# setup_track1.ps1 - Cài đặt môi trường Track 1
# Chạy với quyền Administrator

Write-Host "🚀 Đang cài đặt môi trường Track 1..." -ForegroundColor Cyan

# Check if running as admin
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ Vui lòng chạy PowerShell với quyền Administrator!" -ForegroundColor Red
    exit 1
}

# Install WSL2
Write-Host "📦 Đang cài đặt WSL2..." -ForegroundColor Yellow
wsl --install

# Install Chocolatey if not present
if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "📦 Đang cài đặt Chocolatey..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
}

# Install tools
Write-Host "📦 Đang cài đặt Git..." -ForegroundColor Yellow
choco install git -y

Write-Host "📦 Đang cài đặt VS Code..." -ForegroundColor Yellow
choco install vscode -y

Write-Host "📦 Đang cài đặt Docker Desktop..." -ForegroundColor Yellow
choco install docker-desktop -y

Write-Host "✅ Hoàn thành cài đặt Track 1!" -ForegroundColor Green
Write-Host "⚠️ Vui lòng khởi động lại máy tính để hoàn tất." -ForegroundColor Yellow
