@echo off
setlocal
PowerShell -ExecutionPolicy Bypass -File "%~dp0RUN_ME.ps1" %*
exit /b %ERRORLEVEL%
