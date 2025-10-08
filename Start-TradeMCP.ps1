# Trade-MCP PowerShell Launcher (PowerShell 7)
# Run from n:\autoinvestor
param(
  [string]$VenvPython = ".\venv311\Scripts\python.exe",
  [int]$WebUIPort = 7863
)

$ErrorActionPreference = "Stop"

Write-Host "[INFO] Working directory: $((Get-Location).Path)"

# Set HF_HOME to local cache
$env:HF_HOME = Join-Path (Get-Location).Path "huggingface"
Write-Host "[INFO] HF_HOME set to $env:HF_HOME"

# Optional: set HF_TOKEN only if not already present
if (-not $env:HF_TOKEN -or [string]::IsNullOrWhiteSpace($env:HF_TOKEN)) {
  Write-Host "[WARN] HF_TOKEN not set. Set it in your environment for HuggingFace downloads if needed."
  # Uncomment and set your token if you want to force it:
  # $env:HF_TOKEN = "YOUR_HF_TOKEN_HERE"
}

$env:HF_HUB_DOWNLOAD_TIMEOUT = "300"
$env:HF_HUB_ENABLE_HF_XET = "1"

# Check venv python
if (-not (Test-Path $VenvPython)) {
  Write-Error "[ERROR] Python venv not found at $VenvPython"
  Write-Host "Create the venv or adjust -VenvPython path."
  exit 1
}

# Check if port is already in use
try {
  $conn = Get-NetTCPConnection -State Listen -LocalPort $WebUIPort -ErrorAction SilentlyContinue
  if ($conn) {
    Write-Host "[WARN] Port $WebUIPort appears in use (PID $($conn.OwningProcess)). Web UI may fail to bind."
  }
} catch { }

# Start MCP server in a new window
Write-Host "[INFO] Starting MCP server..."
Start-Process -FilePath $VenvPython -ArgumentList "-m trade_mcp.mcp_server" -WindowStyle Normal -WorkingDirectory (Get-Location).Path

Start-Sleep -Seconds 2

# Start Web UI in current window for visible logs
Write-Host "[INFO] Starting Web UI at http://0.0.0.0:$WebUIPort ..."
& $VenvPython -m trade_mcp.webui

Write-Host "[INFO] Web UI exited. Review logs above."