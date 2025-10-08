@echo off
cd /d N:\autoinvestor

REM Deactivate any existing virtual environment
if defined VIRTUAL_ENV (
    echo Deactivating current virtual environment...
    deactivate
)

REM Always use venv311 (Python 3.11) - no fallback
if exist "venv311\Scripts\activate.bat" (
    echo Activating venv311 (Python 3.11) - the correct environment for Trade-MCP...
    call "venv311\Scripts\activate.bat"
    if errorlevel 1 (
        echo Failed to activate venv311.
        exit /b 1
    )
) else (
    echo ERROR: venv311 not found! Please run setup-env.bat to create it.
    exit /b 1
)

REM Verify the activation
echo Python version:
python --version
echo Virtual environment: %VIRTUAL_ENV%

echo.
echo Trade-MCP virtual environment (venv311) is now active.
echo To start the application, run: python -m trade_mcp
echo.