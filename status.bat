@echo off
tasklist /fi "imagename eq python.exe" /v /fo table | findstr /i "Trade-MCP"
if %errorlevel% equ 0 (
    echo Trade-MCP is running
) else (
    echo Trade-MCP is not running
)