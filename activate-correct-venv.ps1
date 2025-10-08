# Activate the correct virtual environment for Trade-MCP (venv311 only)
Set-Location -Path "N:\autoinvestor"

# Deactivate any existing virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "Deactivating current virtual environment..."
    deactivate
}

# Always use venv311 (Python 3.11) - no fallback
$venv311 = Join-Path $PWD "venv311\Scripts\Activate.ps1"

if (Test-Path $venv311) {
    Write-Host "Activating venv311 (Python 3.11) - the correct environment for Trade-MCP..." -ForegroundColor Green
    & $venv311
    if (-not $env:VIRTUAL_ENV) {
        Write-Host "ERROR: Failed to activate venv311." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ERROR: venv311 not found! Please run setup-env.ps1 to create it." -ForegroundColor Red
    exit 1
}

# Verify the activation
Write-Host "Python version:"
python --version
Write-Host "Virtual environment: $($env:VIRTUAL_ENV)"

Write-Host ""
Write-Host "Trade-MCP virtual environment (venv311) is now active." -ForegroundColor Green
Write-Host "To start the application, run: python -m trade_mcp"
Write-Host ""