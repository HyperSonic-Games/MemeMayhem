:: Build script for Meme-Mayhem
:: Runs without anything and is able to setup the build enviroment,
:: build this program, and then clean up

@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Installing Python...
    
    :: Download Python installer
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe', 'python_installer.exe')"
    
    :: Install Python silently
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo Python installation failed.
        exit /b 1
    )
    
    set PYTHON_INSTALLED=1
) else (
    set PYTHON_INSTALLED=0
)

:: Ensure python is accessible in the session
set "PATH=%PATH%;C:\Program Files\Python311\Scripts\;C:\Program Files\Python311\"

:: Install required packages
echo Installing dependencies...
pip install -r requirements.txt

:: Build the project
echo Building Meme-Mayhem...
python __BUILD_SYS__.py

:: Cleanup
if %PYTHON_INSTALLED%==1 (
    echo Uninstalling pip packages...
    pip freeze > installed_packages.txt
    for /f %%p in (installed_packages.txt) do pip uninstall -y %%p
    del installed_packages.txt

    echo Uninstalling Python...
    powershell -Command "Start-Process 'python_installer.exe' -ArgumentList '/uninstall /quiet' -NoNewWindow -Wait"
    del python_installer.exe
)

echo Build complete. Cleaning up...
del /f /q python_installer.exe 2>nul
rd /s /q __pycache__ 2>nul
del /f /q Main.spec 2>nul
del /f /q Server.spec 2>nul
del /f /q Client.spec 2>nul
del /s /p build 2>nul

echo Done.
endlocal
exit /b 0
