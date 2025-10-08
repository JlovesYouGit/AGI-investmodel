@echo off
REM Simple Trade-MCP Startup (Direct Python execution)
REM This version directly calls the virtual environment Python

echo ========================================
echo Trade-MCP Simple Startup (Local Model)
echo ========================================

cd /d "%~dp0"

REM Set local model configuration (no Google AI)
set USE_GOOGLE_AI=0

echo Local Model: ENABLED
echo API Key: NOT NEEDED
echo.
echo Starting Trade-MCP Web UI...
echo.
echo The web interface will be available at: http://localhost:10001 (or check console for actual port)
echo.
echo The application is now running in this window.
echo Close this window or press Ctrl+C to stop the application.
echo.
echo Note: The Windows port rescue system automatically found an available port.

.\venv311\Scripts\python.exe -m trade_mcp.webui

pause
