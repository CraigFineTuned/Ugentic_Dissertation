@echo off
echo ============================================================
echo SESSION 31 - CLEAR PYTHON CACHE
echo ============================================================
echo.
echo This script clears Python __pycache__ to ensure fixes are loaded
echo.

echo Clearing core module cache...
if exist "src\ugentic\core\__pycache__" (
    rmdir /s /q "src\ugentic\core\__pycache__"
    echo   ✓ Cleared src\ugentic\core\__pycache__
) else (
    echo   - src\ugentic\core\__pycache__ does not exist
)

echo Clearing agents cache...
if exist "src\ugentic\agents\react_agents\__pycache__" (
    rmdir /s /q "src\ugentic\agents\react_agents\__pycache__"
    echo   ✓ Cleared src\ugentic\agents\react_agents\__pycache__
) else (
    echo   - src\ugentic\agents\react_agents\__pycache__ does not exist
)

echo Clearing agents main cache...
if exist "src\ugentic\agents\__pycache__" (
    rmdir /s /q "src\ugentic\agents\__pycache__"
    echo   ✓ Cleared src\ugentic\agents\__pycache__
) else (
    echo   - src\ugentic\agents\__pycache__ does not exist
)

echo Clearing tools cache...
if exist "src\ugentic\tools\__pycache__" (
    rmdir /s /q "src\ugentic\tools\__pycache__"
    echo   ✓ Cleared src\ugentic\tools\__pycache__
) else (
    echo   - src\ugentic\tools\__pycache__ does not exist
)

echo Clearing utils cache...
if exist "src\ugentic\utils\__pycache__" (
    rmdir /s /q "src\ugentic\utils\__pycache__"
    echo   ✓ Cleared src\ugentic\utils\__pycache__
) else (
    echo   - src\ugentic\utils\__pycache__ does not exist
)

echo.
echo ============================================================
echo ✓ CACHE CLEAR COMPLETE
echo ============================================================
echo.
echo Next steps:
echo   1. Run: python app.py
echo   2. Test printer issue
echo   3. Test finance app issue
echo.
pause
