@echo off
cd /d "%~dp0"
title AI Network Orchestrator
echo [*] Checking dependencies...
py -m pip install -r requirements.txt
echo [*] Dependencies ready.
echo [*] Starting Autonomous Agent...
echo.
py main.py
echo.
pause
