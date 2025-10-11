@echo off
echo ========================================
echo UGENTIC Environment Setup
echo Elysia + Hierarchical Ubuntu Framework
echo ========================================
echo.

echo Step 1: Deleting old virtual environment...
if exist .venv (
    rmdir /s /q .venv
    echo    Old .venv deleted
) else (
    echo    No old .venv found
)
echo.

echo Step 2: Creating fresh virtual environment...
python -m venv .venv
if %ERRORLEVEL% NEQ 0 (
    echo    ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo    Virtual environment created successfully
echo.

echo Step 3: Activating virtual environment...
call .venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo    ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo    Virtual environment activated
echo.

echo Step 4: Upgrading pip...
python -m pip install --upgrade pip
echo    Pip upgraded
echo.

echo Step 5: Installing dependencies...
echo    This may take a few minutes...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo    ERROR: Failed to install dependencies
    echo    Check requirements.txt for issues
    pause
    exit /b 1
)
echo    All dependencies installed successfully
echo.

echo ========================================
echo UGENTIC Environment Setup COMPLETE!
echo ========================================
echo.
echo Framework: Elysia Tree + MCP + Hierarchical Ubuntu
echo Status: Ready to run
echo.
echo To run the application:
echo    1. Make sure virtual environment is activated: .venv\Scripts\activate
echo    2. Run: python app.py
echo.
pause
