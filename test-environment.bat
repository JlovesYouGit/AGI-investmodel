@echo off
echo Testing Trade-MCP Environment Setup
echo ==================================

cd /d N:\autoinvestor

echo 1. Checking if venv311 exists...
if exist "venv311" (
    echo    [OK] venv311 directory found
) else (
    echo    [ERROR] venv311 directory not found
    exit /b 1
)

echo 2. Testing environment activation...
call .\activate-correct-venv.bat >nul 2>&1
if /i "%VIRTUAL_ENV%"=="%CD%\venv311" (
    echo    [OK] Environment activated correctly
) else (
    echo    [ERROR] Environment not activated correctly
    echo    Expected: %CD%\venv311
    echo    Actual: %VIRTUAL_ENV%
    exit /b 1
)

echo 3. Testing Python version...
python --version | findstr "3.11" >nul
if %errorlevel% equ 0 (
    echo    [OK] Python 3.11 detected
) else (
    echo    [ERROR] Python 3.11 not detected
    python --version
    exit /b 1
)

echo 4. Testing required packages...
pip show transformers >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] transformers package found
) else (
    echo    [ERROR] transformers package not found
    exit /b 1
)

pip show duckduckgo-search >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] duckduckgo-search package found
) else (
    echo    [ERROR] duckduckgo-search package not found
    exit /b 1
)

echo.
echo [SUCCESS] All tests passed! The Trade-MCP environment is correctly set up.
echo.
echo To start the application, run:
echo    .\start-trade-mcp.bat
echo or
echo    .\start-trade-mcp.ps1
echo.