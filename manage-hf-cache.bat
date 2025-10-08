@echo off
:: Script to manage Hugging Face cache in the current directory

cd /d N:\autoinvestor

echo ========================================
echo Hugging Face Cache Manager
echo ========================================

echo Current directory: %CD%
echo.

:: Check if huggingface directory exists
if exist ".\huggingface" (
    echo ✓ Local huggingface directory exists
    echo Contents:
    dir ".\huggingface" /b
    echo.
) else (
    echo ✗ Local huggingface directory does not exist
    echo Creating huggingface directory...
    mkdir ".\huggingface"
    echo ✓ Created huggingface directory
    echo.
)

:: Set environment variables
set "HF_HOME=%CD%\huggingface"
echo HF_HOME set to: %HF_HOME%
echo.

:: Show cache size
echo Cache size:
for /f "tokens=*" %%i in ('dir ".\huggingface" /s /a-d ^| find /v "File(s)" ^| find /v "Dir(s)"') do set size=%%i
echo %size%
echo.

echo ========================================
echo Cache management complete
echo ========================================
pause