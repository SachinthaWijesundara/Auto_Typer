@echo off
setlocal
title AutoTyper

REM Always run from the folder this .bat lives in (so input.txt is found)
cd /d "%~dp0"

REM ---- 1. Find Python ----
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (
    where python >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo [ERROR] Python was not found. Install it from https://www.python.org/downloads/
    echo         and tick "Add Python to PATH" during install.
    pause
    exit /b 1
)

REM ---- 2. Create the virtual environment if it doesn't exist ----
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment in .venv ...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Could not create the virtual environment.
        pause
        exit /b 1
    )
)

REM ---- 3. Activate it ----
call ".venv\Scripts\activate.bat"

REM ---- 4. Install dependencies only if requirements.txt changed ----
fc /b "requirements.txt" ".venv\requirements.installed" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies ...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Dependency install failed.
        pause
        exit /b 1
    )
    copy /y "requirements.txt" ".venv\requirements.installed" >nul
) else (
    echo Dependencies already installed.
)

REM ---- 5. Run the program ----
echo.
python main.py
echo.
echo AutoTyper closed.
pause
endlocal
