@echo off
setlocal enabledelayedexpansion

:: Build script for Meme-Mayhem
:: Automatically sets up Python, installs dependencies, runs the build with arguments, then cleans up if Python was installed.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Installing Python...

    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe', 'python_installer.exe')"
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

    if %errorlevel% neq 0 (
        echo Python installation failed.
        exit /b 1
    )
    set PYTHON_INSTALLED=1
) else (
    set PYTHON_INSTALLED=0
)

:: Add Python to path
set "PATH=%PATH%;C:\Program Files\Python311\Scripts\;C:\Program Files\Python311\"

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run build script and forward arguments
echo Running build system...
python __BUILD_SYS__.py %*

:: If Python was installed temporarily, remove it
if %PYTHON_INSTALLED%==1 (
    echo Cleaning up temporary Python environment...

    pip freeze > installed_packages.txt
    for /f %%p in (installed_packages.txt) do pip uninstall -y %%p
    del installed_packages.txt

    powershell -Command "Start-Process 'python_installer.exe' -ArgumentList '/uninstall /quiet' -NoNewWindow -Wait"
    del python_installer.exe
)

:: General cleanup
echo Cleaning up build artifacts...
del /f /q python_installer.exe 2>nul
rd /s /q __pycache__ 2>nul
del /f /q Main.spec 2>nul
del /f /q Server.spec 2>nul
del /f /q Client.spec 2>nul
rd /s /q build 2>nul

echo Done.
endlocal
exit /b 0
