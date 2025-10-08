@echo off
setlocal

REM Trade-MCP Launcher (Windows .bat)
REM Working directory should be n:\autoinvestor

REM Set Hugging Face cache dir to local folder
set "HF_HOME=%CD%\huggingface"

REM TODO: Set your real Hugging Face token (replace the placeholder)
REM If you already have HF_TOKEN in your system env, you can comment the next line.
set "HF_TOKEN=YOUR_HF_TOKEN_HERE"

REM Optional: widen file descriptors for downloads
set "HF_HUB_DOWNLOAD_TIMEOUT=300"
set "HF_HUB_ENABLE_HF_XET=1"

REM Check venv python
if not exist ".\venv311\Scripts\python.exe" (
  echo [ERROR] Python venv not found at .\venv311\Scripts\python.exe
  echo Create venv or adjust path in this script.
  pause
  exit /b 1
)

echo [INFO] Starting MCP server in a new window...
start "Trade-MCP Server" cmd /c ".\venv311\Scripts\python.exe -m trade_mcp.mcp_server"

REM Small delay to let server initialize
timeout /t 2 /nobreak >nul

echo [INFO] Starting Web UI (http://0.0.0.0:7863) ...
.\venv311\Scripts\python.exe -m trade_mcp.webui

echo [INFO] Web UI exited. Check logs above for details.
pause