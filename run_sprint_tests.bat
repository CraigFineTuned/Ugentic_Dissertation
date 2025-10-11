@echo off
setlocal enabledelayedexpansion

REM Check if --fast flag was provided
set "FAST_MODE="
if "%1"=="--fast" set "FAST_MODE=--fast"

REM Display mode
if defined FAST_MODE (
    echo ========================================
    echo UGENTIC SPRINT TESTS - FAST MODE
    echo Using gemma3:4b for quick iterations
    echo ========================================
) else (
    echo ========================================
    echo UGENTIC SPRINT TESTS - STANDARD MODE
    echo Using model from config.json
    echo ========================================
)

echo.
echo Activating Python environment...
call .venv\Scripts\activate.bat

echo.
echo ========================================
echo SPRINT 1 TEST: Infrastructure Agent
echo ========================================
python test_react_agent.py %FAST_MODE%

echo.
echo.
echo ========================================
echo SPRINT 2 TEST: All Agents System
echo ========================================
python test_all_agents.py %FAST_MODE%

echo.
echo ========================================
echo All tests complete!
echo ========================================
if defined FAST_MODE (
    echo Ran in FAST MODE with gemma3:4b
) else (
    echo Ran in STANDARD MODE with config.json model
)
pause
