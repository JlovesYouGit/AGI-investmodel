@echo off
echo Current directory: %CD%
echo Script directory: %~dp0
echo Testing if we can activate the environment...
call .\activate-correct-venv.bat
echo Environment activation result: %ERRORLEVEL%