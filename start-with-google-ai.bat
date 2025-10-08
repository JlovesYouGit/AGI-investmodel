@echo off
REM Easy Trade-MCP Startup with Google AI
REM Just double-click this file to start Trade-MCP with Google AI enabled

echo ========================================
echo Trade-MCP Easy Startup (Google AI)
echo ========================================

cd /d "%~dp0"

REM Activate the correct virtual environment
echo Activating virtual environment...
call .\activate-correct-venv.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Set Google AI configuration
echo Setting up Google AI...
set USE_GOOGLE_AI=1
set GOOGLE_API_KEY=AIzaSyC__z2fAlj9swxc-4K8NR-kmkJNEqPeE9s

echo Google AI: ENABLED
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
