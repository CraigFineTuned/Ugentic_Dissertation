@echo off
REM Clear Python cache to force recompilation of all modules with Session 23 fixes

echo Clearing Python cache directories...

REM Clear core module cache
if exist "src\ugentic\core\__pycache__" (
    echo Removing src\ugentic\core\__pycache__
    rmdir /s /q "src\ugentic\core\__pycache__"
)

REM Clear tools cache
if exist "src\ugentic\tools\__pycache__" (
    echo Removing src\ugentic\tools\__pycache__
    rmdir /s /q "src\ugentic\tools\__pycache__"
)

REM Clear agents cache
if exist "src\ugentic\agents\__pycache__" (
    echo Removing src\ugentic\agents\__pycache__
    rmdir /s /q "src\ugentic\agents\__pycache__"
)

if exist "src\ugentic\agents\react_agents\__pycache__" (
    echo Removing src\ugentic\agents\react_agents\__pycache__
    rmdir /s /q "src\ugentic\agents\react_agents\__pycache__"
)

REM Clear main package cache
if exist "src\ugentic\__pycache__" (
    echo Removing src\ugentic\__pycache__
    rmdir /s /q "src\ugentic\__pycache__"
)

echo.
echo Cache cleared. Python will recompile all modules on next run.
echo.
pause
