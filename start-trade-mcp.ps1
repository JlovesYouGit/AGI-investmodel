# Script to automatically activate the correct environment and start Trade-MCP

Set-Location -Path "N:\autoinvestor"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Trade-MCP Application Starter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activate the correct virtual environment
Write-Host "Activating the correct virtual environment..." -ForegroundColor Yellow
& .\activate-correct-venv.ps1

# Check if activation was successful
if ($env:VIRTUAL_ENV -ne "$(Get-Location)\venv311") {
    Write-Host "ERROR: Not in the correct virtual environment (venv311)" -ForegroundColor Red
    Write-Host "Current environment: $($env:VIRTUAL_ENV)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure venv311 exists and is working properly." -ForegroundColor Yellow
    pause
    exit 1
}

# Ensure offload directory exists for memory-efficient loading
$offloadDir = Join-Path $PWD "offload"
if (-not (Test-Path $offloadDir)) {
    Write-Host "Creating offload directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $offloadDir | Out-Null
}

# Configure environment for downloads/offload and visible logs
$env:TRANSFORMERS_OFFLOAD_DIR = $offloadDir
$env:HF_HUB_ENABLE_HF_XET = "1"
$env:HF_HUB_DOWNLOAD_TIMEOUT = "600"  # 10 minutes timeout for better reliability
$env:PYTHONLOGLEVEL = "INFO"

# Set HF cache to local directory for better performance
$env:HF_HOME = "$(Get-Location)\huggingface"

# Set HF_TOKEN if not already set
if (-not $env:HF_TOKEN) {
    Write-Host "Setting HF_TOKEN from default value..." -ForegroundColor Yellow
    $env:HF_TOKEN = "YOUR_HF_TOKEN_HERE"
}

Write-Host ""
Write-Host "Environment configuration:" -ForegroundColor Yellow
Write-Host "Virtual Environment: $($env:VIRTUAL_ENV)" -ForegroundColor White
Write-Host "Python Version: $(python --version)" -ForegroundColor White
Write-Host "HF_HOME: $($env:HF_HOME)" -ForegroundColor White
Write-Host "HF_TOKEN set: $($env:HF_TOKEN -ne $null)" -ForegroundColor White
Write-Host ""

# Start the application
Write-Host "Starting Trade-MCP application..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
python -m trade_mcp

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Trade-MCP application finished." -ForegroundColor Green
Write-Host ""
pause
