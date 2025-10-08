@echo off
cd /d N:\autoinvestor

REM Setup Trade-MCP Environment (Python 3.11)
echo ========================================
echo Setting up Trade-MCP Environment
echo Python Version: 3.11.9
echo Virtual Environment: venv311
echo ========================================

REM Check if Python 3.11 is available
py -3.11 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.11 not found!
    echo Please install Python 3.11 before running this script.
    pause
    exit /b 1
)

REM Check if venv311 exists
if not exist "venv311" (
    echo Creating virtual environment with Python 3.11...
    py -3.11 -m venv venv311
    
    if exist "venv311" (
        echo Virtual environment created successfully.
    ) else (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv311\Scripts\activate.bat

REM Verify Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Using %PYTHON_VERSION%

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup complete!
echo Virtual environment is ready at: venv311
echo Python version: %PYTHON_VERSION%
echo ========================================
echo.
echo To activate the environment manually, run:
echo   venv311\Scripts\activate.bat
echo.
echo To start the application, run:
echo   python -m trade_mcp
echo.
pause