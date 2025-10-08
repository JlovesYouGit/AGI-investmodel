@echo off
:: Script to check which virtual environment is currently active

echo ==========================================
echo Trade-MCP Virtual Environment Checker
echo ==========================================

if defined VIRTUAL_ENV (
    echo Current virtual environment:
    echo %VIRTUAL_ENV%
    echo.
    
    :: Check if it's the correct environment
    echo Checking environment details...
    python --version
    
    echo.
    if /i "%VIRTUAL_ENV%"=="%CD%\venv311" (
        echo [CORRECT] You are using the official Trade-MCP environment (Python 3.11.9)
        echo This is the recommended environment for development.
    ) else if /i "%VIRTUAL_ENV%"=="%CD%\venv_py313_old" (
        echo [WARNING] You are using the DEPRECATED environment
        echo This environment should NOT be used for development.
        echo Please switch to the venv311 environment.
    ) else (
        echo [INFO] You are using a virtual environment, but it's not one of the standard Trade-MCP environments.
        echo.
        echo Current environment: %VIRTUAL_ENV%
        echo.
        echo Please switch to the venv311 environment for Trade-MCP development.
    )
) else (
    echo [WARNING] No virtual environment is currently active.
    echo Please activate the venv311 environment before proceeding.
    echo.
    echo To activate the correct environment, run:
    echo   activate-correct-venv.bat
)

echo.
echo ==========================================
pause