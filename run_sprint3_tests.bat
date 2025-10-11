@echo off
REM Sprint 3 Ubuntu Orchestration Test Runner
REM Supports --fast flag for quick testing with gemma3:4b

echo.
echo ================================================================================
echo SPRINT 3: UBUNTU ORCHESTRATION TESTS
echo ================================================================================
echo.

REM Check if --fast flag is provided
set FAST_MODE=0
if "%1"=="--fast" set FAST_MODE=1

REM Display mode
if %FAST_MODE%==1 (
    echo Running in FAST MODE (gemma3:4b)
    echo.
) else (
    echo Running in STANDARD MODE (model from config.json)
    echo.
)

REM Activate virtual environment
echo Activating Python virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Run Sprint 3 tests
echo.
echo ================================================================================
echo RUNNING SPRINT 3 UBUNTU ORCHESTRATION TESTS
echo ================================================================================
echo.

if %FAST_MODE%==1 (
    python test_ubuntu_orchestration.py --fast
) else (
    python test_ubuntu_orchestration.py
)

echo.
echo ================================================================================
echo SPRINT 3 TESTS COMPLETE
echo ================================================================================
echo.

pause
