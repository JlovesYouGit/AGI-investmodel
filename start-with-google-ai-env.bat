@echo off
REM Easy Trade-MCP Startup with Google AI (Environment-based)
REM This version reads API keys from environment variables

echo ========================================
echo Trade-MCP Easy Startup (Google AI)
echo ========================================

cd /d "%~dp0"

REM Check if .env file exists and load it
if exist ".env" (
    echo Loading configuration from .env file...
    for /f "tokens=1,2 delims==" %%a in (.env) do (
        set "%%a=%%b"
    )
) else (
    echo WARNING: No .env file found. Using default configuration.
    echo Create a .env file based on .env.example.google to configure API keys.
)

REM Activate the correct virtual environment
echo Activating virtual environment...
call .\activate-correct-venv.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Set Google AI configuration from environment or defaults
if "%USE_GOOGLE_AI%"=="" set USE_GOOGLE_AI=1
if "%GOOGLE_API_KEY%"=="" (
    echo ERROR: GOOGLE_API_KEY not set!
    echo Please set your Google API key in the GOOGLE_API_KEY environment variable
    echo or create a .env file with your API key.
    pause
    exit /b 1
)

echo Google AI: %USE_GOOGLE_AI%
echo API Key: SET
echo.

REM Start the Trade-MCP Web UI
echo Starting Trade-MCP Web UI...
echo.
echo The web interface will be available at: http://localhost:10001 (or check console for actual port)
echo.
echo Press Ctrl+C in this window to stop the application.
echo.
echo Note: The Windows port rescue system automatically found an available port.

python -m trade_mcp.webui

pause
