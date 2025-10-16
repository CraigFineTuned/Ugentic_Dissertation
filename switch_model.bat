@echo off
REM Model Switcher for UGENTIC
REM Quickly switch between different Ollama models

echo.
echo ========================================
echo   UGENTIC MODEL SWITCHER
echo ========================================
echo.
echo Available Models:
echo   1. qwen2.5:7b (Current - Balanced)
echo   2. gemma3n:e4b (Fast - 4B params)
echo   3. deepseek-r1:7b (Reasoning - Step-by-step)
echo   4. granite4:small-h (Multilingual - IBM)
echo   5. Custom (Enter model name)
echo   6. Exit
echo.

set /p choice="Select model (1-6): "

if "%choice%"=="1" (
    set model=qwen2.5:7b
    goto :switch
)
if "%choice%"=="2" (
    set model=gemma3n:e4b
    goto :check_and_switch
)
if "%choice%"=="3" (
    set model=deepseek-r1:7b
    goto :check_and_switch
)
if "%choice%"=="4" (
    set model=granite4:small-h
    goto :check_and_switch
)
if "%choice%"=="5" (
    set /p model="Enter model name: "
    goto :check_and_switch
)
if "%choice%"=="6" (
    echo Exiting...
    exit /b 0
)

echo Invalid choice!
pause
exit /b 1

:check_and_switch
echo.
echo Checking if model is available...
ollama list | findstr /C:"%model%" >nul
if errorlevel 1 (
    echo.
    echo Model '%model%' not found locally.
    set /p pull="Pull model now? (y/n): "
    if /i "%pull%"=="y" (
        echo.
        echo Pulling %model%...
        ollama pull %model%
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to pull model!
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Cannot switch to unpulled model.
        pause
        exit /b 1
    )
)

:switch
echo.
echo Switching to: %model%
echo.

REM Backup current config
copy config.json config.json.backup >nul 2>&1

REM Update config.json using PowerShell
powershell -Command "(Get-Content config.json) -replace '\"reasoning_model\": \"[^\"]*\"', '\"reasoning_model\": \"%model%\"' | Set-Content config.json"

echo.
echo ✅ Successfully switched to: %model%
echo.
echo Current configuration:
type config.json | findstr "reasoning_model"
echo.
echo Run 'python app.py' to start with new model.
echo.
pause
