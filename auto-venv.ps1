# Auto-activate correct virtual environment for Trade-MCP
# This script ensures we're using the Python 3.11 virtual environment

# Get the current directory
$currentDir = Get-Location

# Check if we're in the autoinvestor directory
if ($currentDir.Path -ne "N:\autoinvestor") {
    Write-Host "Changing directory to N:\autoinvestor"
    Set-Location -Path "N:\autoinvestor"
}

# Deactivate any existing virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "Deactivating current virtual environment..."
    deactivate
}

# Check if the correct virtual environment exists
if (-not (Test-Path "venv311")) {
    Write-Host "ERROR: Correct virtual environment (venv311) not found!" -ForegroundColor Red
    Write-Host "Please run setup-env.ps1 first to create the environment." -ForegroundColor Yellow
    return
}

# Activate the correct virtual environment (Python 3.11)
Write-Host "Activating Trade-MCP virtual environment (Python 3.11)..."
& .\venv311\Scripts\Activate.ps1

# Verify activation
if ($env:VIRTUAL_ENV -like "*venv311*") {
    Write-Host "Virtual environment activated successfully." -ForegroundColor Green
} else {
    Write-Host "WARNING: Virtual environment may not have activated correctly." -ForegroundColor Yellow
}

# Show current Python version
python --version

# Show current virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Host "Virtual environment: $($env:VIRTUAL_ENV)" -ForegroundColor Green
} else {
    Write-Host "No virtual environment activated." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To start the application, run: python -m trade_mcp"
Write-Host ""