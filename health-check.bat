@echo off
curl -f http://localhost:8080/healthz
if %errorlevel% equ 0 (
    echo Health check passed
) else (
    echo Health check failed
)