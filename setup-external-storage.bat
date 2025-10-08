@echo off
REM Setup external storage environment variables for Trade-MCP
REM Modify the base path below to your preferred location

set BASE_PATH=D:\TradeMCP

REM Set environment variables
set OLLAMA_MODELS=%BASE_PATH%\.ollama\models
set CONDA_ENVS_DIRS=%BASE_PATH%\.conda\envs
set CONDA_PKGS_DIRS=%BASE_PATH%\.conda\pkgs
set NPM_CONFIG_CACHE=%BASE_PATH%\.npm
set CHOCOLATEY_INSTALL=%BASE_PATH%\choco
set WHISPER_CPP_PATH=%BASE_PATH%\whisper.cpp
set DATA_DIR=%BASE_PATH%\.data

REM Add to PATH
set PATH=%CHOCOLATEY_INSTALL%\bin;%PATH%

echo External storage configured at: %BASE_PATH%
echo Environment variables set for current session.
echo.
echo To make these permanent, add them to your system environment variables.