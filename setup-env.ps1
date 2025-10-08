# Setup Trade-MCP Environment (Python 3.11)
Set-Location -Path "N:\autoinvestor"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Trade-MCP Environment" -ForegroundColor Cyan
Write-Host "Python Version: 3.11.9" -ForegroundColor Cyan
Write-Host "Virtual Environment: venv311" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Python 3.11 is available
try {
    $pythonVersion = py -3.11 --version
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python 3.11 not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11 before running this script." -ForegroundColor Yellow
    exit 1
}

# Check if venv311 exists
if (-not (Test-Path "venv311")) {
    Write-Host "Creating virtual environment with Python 3.11..." -ForegroundColor Yellow
    py -3.11 -m venv venv311
    
    if (Test-Path "venv311") {
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create virtual environment!" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv311\Scripts\Activate.ps1

# Verify Python version
$pythonVersion = python --version
Write-Host "Using $pythonVersion" -ForegroundColor Green

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup complete!" -ForegroundColor Cyan
Write-Host "Virtual environment is ready at: venv311" -ForegroundColor Cyan
Write-Host "Python version: $pythonVersion" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the environment manually, run:" -ForegroundColor Yellow
Write-Host "  venv311\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "To start the application, run:" -ForegroundColor Yellow
Write-Host "  python -m trade_mcp" -ForegroundColor Yellow
Write-Host ""