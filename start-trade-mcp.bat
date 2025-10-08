@echo off
:: Unified starter: activates correct venv, configures environment, and runs Trade-MCP

cd /d N:\autoinvestor

echo ========================================
echo Trade-MCP Application Starter
echo ========================================

REM Activate the correct virtual environment (venv311)
echo Activating the correct virtual environment...
call .\activate-correct-venv.bat
if errorlevel 1 (
    echo Failed to activate the correct virtual environment. Exiting.
    pause
    exit /b 1
)

REM Ensure we're in the right environment
if /i not "%VIRTUAL_ENV%"=="%CD%\venv311" (
    echo ERROR: Not in the correct virtual environment (venv311)
    echo Current environment: %VIRTUAL_ENV%
    echo.
    echo Please make sure venv311 exists and is working properly.
    pause
    exit /b 1
)

REM Ensure offload directory exists for memory-efficient loading
if not exist ".\offload" (
    echo Creating offload directory...
    mkdir ".\offload"
)

REM Configure environment for downloads/offload and visible logs
set "TRANSFORMERS_OFFLOAD_DIR=%CD%\offload"
set "HF_HUB_ENABLE_HF_XET=1"
set "HF_HUB_DOWNLOAD_TIMEOUT=300"
set "PYTHONLOGLEVEL=INFO"

REM Set HF cache to local directory for better performance
set "HF_HOME=%CD%\huggingface"

REM Set HF_TOKEN if not already set
if "%HF_TOKEN%"=="" (
    echo Setting HF_TOKEN from default value...
    set "HF_TOKEN=YOUR_HF_TOKEN_HERE"
)

echo.
echo Environment configuration:
echo Virtual Environment: %VIRTUAL_ENV%
echo Python Version: 
python --version
echo HF_HOME: %HF_HOME%
echo HF_TOKEN set: %HF_TOKEN%
echo.

REM Start the application
echo Starting Trade-MCP application...
echo ========================================
python -m trade_mcp
set "EXITCODE=%ERRORLEVEL%"

echo.
echo ========================================
if not "%EXITCODE%"=="0" (
    echo Trade-MCP exited with error code %EXITCODE%.
    echo The terminal is kept open so you can read the error above.
) else (
    echo Trade-MCP exited normally.
)
echo.
pause
