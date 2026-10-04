@echo off
setlocal
cd /d "%~dp0"

set PORT=8502
title Abhilash Job Tracker

where python >nul 2>&1
if %ERRORLEVEL%==0 (
    set "PY=python"
) else (
    where py >nul 2>&1
    if %ERRORLEVEL%==0 (
        set "PY=py"
    ) else (
        echo Python was not found on this computer.
        echo Install Python from https://www.python.org/downloads/ and try again.
        pause
        exit /b 1
    )
)

echo Starting Abhilash Career Suite at http://localhost:%PORT%
echo Close this window or press Ctrl+C to stop the server.
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:%PORT%"
"%PY%" dashboard_server.py
if errorlevel 1 (
    echo.
    echo The dashboard server failed to start.
    pause
)
endlocal
