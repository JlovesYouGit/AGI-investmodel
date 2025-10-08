# Script to check which virtual environment is currently active

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Trade-MCP Virtual Environment Checker" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if ($env:VIRTUAL_ENV) {
    Write-Host "Current virtual environment:" -ForegroundColor Yellow
    Write-Host $env:VIRTUAL_ENV -ForegroundColor White
    Write-Host ""
    
    # Check if it's the correct environment
    Write-Host "Checking environment details..." -ForegroundColor Yellow
    python --version
    
    Write-Host ""
    if ($env:VIRTUAL_ENV -eq "$(Get-Location)\venv311") {
        Write-Host "[CORRECT] You are using the official Trade-MCP environment (Python 3.11.9)" -ForegroundColor Green
        Write-Host "This is the recommended environment for development." -ForegroundColor Green
    } elseif ($env:VIRTUAL_ENV -eq "$(Get-Location)\venv_py313_old") {
        Write-Host "[WARNING] You are using the DEPRECATED environment" -ForegroundColor Red
        Write-Host "This environment should NOT be used for development." -ForegroundColor Red
        Write-Host "Please switch to the venv311 environment." -ForegroundColor Red
    } else {
        Write-Host "[INFO] You are using a virtual environment, but it's not one of the standard Trade-MCP environments." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Current environment: $($env:VIRTUAL_ENV)" -ForegroundColor White
        Write-Host ""
        Write-Host "Please switch to the venv311 environment for Trade-MCP development." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARNING] No virtual environment is currently active." -ForegroundColor Red
    Write-Host "Please activate the venv311 environment before proceeding." -ForegroundColor Red
    Write-Host ""
    Write-Host "To activate the correct environment, run:" -ForegroundColor Yellow
    Write-Host "  .\activate-correct-venv.ps1" -ForegroundColor White
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Press any key to continue..." -ForegroundColor Gray
$host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")