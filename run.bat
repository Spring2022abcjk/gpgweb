@echo off
set INSTALL_LIBS=false
for %%i in (flask flask-cors cryptography) do (
    call pip show %%~ni > nul 2>&1
    if errorlevel 1 (
        echo Installing %%~ni...
        pip install %%~ni
        set INSTALL_LIBS=true
    )
)
if %INSTALL_LIBS%==false (
    echo All required libraries are installed. Starting Flask server...
) else (
    echo Please run this script again to install missing libraries.
    pause
    exit /b 1
)

start "" cmd /k "python main.py"
start "" cmd /k "caddy run"
