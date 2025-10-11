@echo off
echo ========================================
echo UGENTIC Comprehensive Testing Suite
echo ========================================
echo.
echo Activating Python environment...
call .venv\Scripts\activate.bat

echo.
echo Running comprehensive scenario tests...
python run_comprehensive_tests.py

echo.
echo Tests complete! Check test_results/ for detailed output.
pause
