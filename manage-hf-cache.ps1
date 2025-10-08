# Script to manage Hugging Face cache in the current directory

Set-Location -Path "N:\autoinvestor"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hugging Face Cache Manager" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Current directory: $(Get-Location)" -ForegroundColor White
Write-Host ""

# Check if huggingface directory exists
$huggingfaceDir = Join-Path $PWD "huggingface"
if (Test-Path $huggingfaceDir) {
    Write-Host "✓ Local huggingface directory exists" -ForegroundColor Green
    Write-Host "Contents:" -ForegroundColor Yellow
    Get-ChildItem $huggingfaceDir | ForEach-Object { Write-Host "  $($_.Name)" -ForegroundColor White }
    Write-Host ""
} else {
    Write-Host "✗ Local huggingface directory does not exist" -ForegroundColor Red
    Write-Host "Creating huggingface directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $huggingfaceDir | Out-Null
    Write-Host "✓ Created huggingface directory" -ForegroundColor Green
    Write-Host ""
}

# Set environment variables
$env:HF_HOME = $huggingfaceDir
Write-Host "HF_HOME set to: $($env:HF_HOME)" -ForegroundColor White
Write-Host ""

# Show cache size
try {
    $size = (Get-ChildItem -Path $huggingfaceDir -Recurse | Measure-Object -Property Length -Sum).Sum
    Write-Host "Cache size: $([math]::Round($size / 1MB, 2)) MB" -ForegroundColor White
} catch {
    Write-Host "Could not determine cache size" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cache management complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

pause