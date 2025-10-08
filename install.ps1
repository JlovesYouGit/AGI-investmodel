# install.ps1  –  self-contained, no external drive required
param(
    [switch]$SkipChoco = $false
)

$ErrorActionPreference = "Stop"
$base = Split-Path -Parent $MyInvocation.MyCommand.Definition
$data = "$base\.data\external"
Write-Host "Installing Trade-MCP into $base  (data -> $data)" -ForegroundColor Green

# 1. create data dirs
@(
    "$data\ollama",
    "$data\npm-cache",
    "$data\whisper.cpp",
    "$data\models",
    "$data\logs"
) | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

# 2. link them to default locations
if (-not (Test-Path "$env:USERPROFILE\.ollama")) {
    cmd /c mklink /D "$env:USERPROFILE\.ollama" "$data\ollama"
}
if (-not (Test-Path "$env:APPDATA\npm-cache")) {
    cmd /c mklink /D "$env:APPDATA\npm-cache" "$data\npm-cache"
}
$env:OLLAMA_MODELS = "$data\ollama\models"
$env:NPM_CONFIG_CACHE = "$data\npm-cache"
$env:WHISPER_CPP_PATH = "$data\whisper.cpp"

# 3. (optional) install chocolatey once
if (-not $SkipChoco -and -not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# 4. minimal tools  (skip if already present)
# Skipping CUDA installation as it's not required for basic functionality
@("git", "python", "nodejs") | ForEach-Object {
    if (-not (Get-Command $_ -ErrorAction SilentlyContinue)) {
        Write-Host "Installing $_..." -ForegroundColor Yellow
        choco install $_ -y --no-progress --limit-output
    } else {
        Write-Host "$_ already installed" -ForegroundColor Green
    }
}

# 5. ollama (manual download to avoid curl alias issue)
$ollamaZip = "$data\ollama-windows-amd64.zip"
if (-not (Test-Path "$data\ollama\ollama.exe")) {
    Write-Host "Downloading Ollama..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://github.com/ollama/ollama/releases/latest/download/ollama-windows-amd64.zip" -OutFile $ollamaZip
    Write-Host "Extracting Ollama..." -ForegroundColor Yellow
    Expand-Archive -Path $ollamaZip -DestinationPath "$data\ollama" -Force
    Remove-Item $ollamaZip
}
$env:PATH += ";$data\ollama"

# 6. whisper.cpp (optional - only if C++ compiler is available)
Write-Host "Checking for C++ compiler for whisper.cpp..." -ForegroundColor Yellow
$hasCompiler = $false
if (Get-Command "gcc" -ErrorAction SilentlyContinue) {
    $hasCompiler = $true
    Write-Host "Found gcc compiler" -ForegroundColor Green
} elseif (Get-Command "clang" -ErrorAction SilentlyContinue) {
    $hasCompiler = $true
    Write-Host "Found clang compiler" -ForegroundColor Green
} elseif (Get-Command "cl" -ErrorAction SilentlyContinue) {
    $hasCompiler = $true
    Write-Host "Found Visual Studio compiler" -ForegroundColor Green
}

if ($hasCompiler) {
    if (-not (Test-Path "$data\whisper.cpp\main.exe")) {
        Write-Host "Cloning whisper.cpp..." -ForegroundColor Yellow
        git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git "$data\whisper.cpp"
        Push-Location "$data\whisper.cpp"
        
        # Check if make.exe exists in the expected location
        $makePath = "$env:ProgramFiles\Git\usr\bin\make.exe"
        if (Test-Path $makePath) {
            # use bundled make for windows (from git install)
            Write-Host "Compiling whisper.cpp with Git's make..." -ForegroundColor Yellow
            & $makePath -j4
        } else {
            # Try alternative compilation method
            Write-Host "Git's make not found, trying alternative compilation..." -ForegroundColor Yellow
            # Check if we have gcc or clang available
            if (Get-Command "gcc" -ErrorAction SilentlyContinue) {
                gcc -O3 -std=c11 -pthread -mavx -mavx2 -mfma -mf16c -I. -Iggml/include -Iggml/src main.cpp ggml/src/ggml.c ggml/src/ggml-alloc.c ggml/src/ggml-backend.c ggml/src/ggml-quants.c whisper.cpp -o main.exe
            } elseif (Get-Command "clang" -ErrorAction SilentlyContinue) {
                clang -O3 -std=c11 -pthread -mavx -mavx2 -mfma -mf16c -I. -Iggml/include -Iggml/src main.cpp ggml/src/ggml.c ggml/src/ggml-alloc.c ggml/src/ggml-backend.c ggml/src/ggml-quants.c whisper.cpp -o main.exe
            } elseif (Get-Command "cl" -ErrorAction SilentlyContinue) {
                cl /O2 /EHsc main.cpp ggml/src/ggml.c ggml/src/ggml-alloc.c ggml/src/ggml-backend.c ggml/src/ggml-quants.c whisper.cpp /Fe:main.exe
            }
        }
        Pop-Location
    }
} else {
    Write-Host "No C++ compiler found. Skipping whisper.cpp compilation." -ForegroundColor Yellow
    Write-Host "Audio emotion analysis features will be disabled." -ForegroundColor Yellow
}

# 7. npm & playwright
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
$env:PATH += ";$env:ProgramFiles\nodejs"
npm config set cache "$data\npm-cache" --global
npm install -g npm@latest
npx playwright install chromium

# 8. python venv inside repo
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow
$venv = "$base\venv"
if (-not (Test-Path $venv)) {
    python -m venv $venv
}
& "$venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
pip install -r "$base\requirements.txt"
pip install -e $base

# 9. pull models (small 3 B variant to save space)
Write-Host "Downloading language models..." -ForegroundColor Yellow
ollama pull llama3:3b-instruct-q4_K_M

# 10. windows service (winsw)
Write-Host "Setting up Windows service..." -ForegroundColor Yellow
$svc = "$base\winsw"
New-Item -ItemType Directory -Force -Path $svc | Out-Null
Invoke-WebRequest -Uri "https://github.com/winsw/winsw/releases/download/v3.0.0-alpha.11/WinSW.NETCore31.x64.exe" -OutFile "$svc\trade-mcp.exe"
@"
<service>
  <id>trade-mcp</id>
  <name>Trade-MCP Bot</name>
  <description>Autonomous trading assistant with browser-MCP</description>
  <executable>$venv\Scripts\python.exe</executable>
  <arguments>-m trade_mcp</arguments>
  <workingdirectory>$base</workingdirectory>
  <logpath>$data\logs</logpath>
  <log mode="roll-by-size">
    <sizeThreshold>52428800</sizeThreshold>
    <keepFiles>5</keepFiles>
  </log>
  <onfailure action="restart" delay="10 sec"/>
  <priority>Normal</priority>
</service>
"@ | Out-File -Encoding UTF8 "$svc\trade-mcp.xml"

& "$svc\trade-mcp.exe" install   "$svc\trade-mcp.xml"
& "$svc\trade-mcp.exe" start     "$svc\trade-mcp.xml"

Write-Host "✅ Trade-MCP installed and started as Windows service." -ForegroundColor Green
Write-Host "   Logs: $data\logs" -ForegroundColor Yellow
Write-Host "   Models/cache: $data" -ForegroundColor Yellow
Write-Host "   Note: Audio emotion analysis features are disabled due to missing C++ compiler." -ForegroundColor Yellow