@echo off
setlocal
cd /d "%~dp0..\.."
echo flowsearch root: %CD%
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install-faerie.ps1" -Interactive
if errorlevel 1 exit /b 1
echo.
pause
