@echo off
echo ============================================================
echo PHASE 3 PREPARATION - COMPREHENSIVE CLEANUP
echo ============================================================
echo.

REM Create archive directory
if not exist "docs\Project_Tracker\archive" mkdir "docs\Project_Tracker\archive"

REM Archive old session summaries
echo Archiving old session summaries...
if exist "SESSION_25_COMPLETION_REPORT.md" move "SESSION_25_COMPLETION_REPORT.md" "docs\Project_Tracker\archive\"
if exist "SESSION_25_HANDOFF_SUMMARY.md" move "SESSION_25_HANDOFF_SUMMARY.md" "docs\Project_Tracker\archive\"
if exist "SESSION_26_COMPLETENESS_CHECKLIST.md" move "SESSION_26_COMPLETENESS_CHECKLIST.md" "docs\Project_Tracker\archive\"
if exist "SESSION_26_FINAL_HANDOFF.md" move "SESSION_26_FINAL_HANDOFF.md" "docs\Project_Tracker\archive\"
if exist "SESSION_26_FINAL_SUMMARY.md" move "SESSION_26_FINAL_SUMMARY.md" "docs\Project_Tracker\archive\"
if exist "PHASE2_PIVOT_SUMMARY.md" move "PHASE2_PIVOT_SUMMARY.md" "docs\Project_Tracker\archive\"
if exist "QUICK_START.md" move "QUICK_START.md" "docs\Project_Tracker\archive\"
if exist "QUICK_START_SESSION_25.md" move "QUICK_START_SESSION_25.md" "docs\Project_Tracker\archive\"
if exist "TESTING_GUIDE.md" move "TESTING_GUIDE.md" "docs\Project_Tracker\archive\"
if exist "DEVELOPER_GUIDE.md" move "DEVELOPER_GUIDE.md" "docs\Project_Tracker\archive\"
if exist "STRUCTURE.md" move "STRUCTURE.md" "docs\Project_Tracker\archive\"

REM Delete outdated proposal versions
echo Deleting outdated proposal versions...
if exist "Honours_Research_Proposal_FINAL_Oct6_2025.docx" del "Honours_Research_Proposal_FINAL_Oct6_2025.docx"
if exist "Honours_Research_Proposal_FINAL_Oct6_2025.pdf" del "Honours_Research_Proposal_FINAL_Oct6_2025.pdf"
if exist "Honours_Research_Proposal_UPDATED_References_Oct11_2025.md" del "Honours_Research_Proposal_UPDATED_References_Oct11_2025.md"

REM Delete diagnostic files
echo Deleting diagnostic files...
if exist "DxDiag.txt" del "DxDiag.txt"
if exist "diagnose_session25.py" del "diagnose_session25.py"

REM Delete old test scripts
echo Deleting old test scripts...
if exist "run_comprehensive_tests.py" del "run_comprehensive_tests.py"
if exist "run_integration_tests.py" del "run_integration_tests.py"
if exist "run_tests.bat" del "run_tests.bat"
if exist "run_ugentic.bat" del "run_ugentic.bat"
if exist "switch_model.bat" del "switch_model.bat"

REM Clear Python cache
echo Clearing Python cache...
if exist "src\ugentic\core\__pycache__" rmdir /s /q "src\ugentic\core\__pycache__"
if exist "src\ugentic\tools\__pycache__" rmdir /s /q "src\ugentic\tools\__pycache__"
if exist "src\ugentic\agents\__pycache__" rmdir /s /q "src\ugentic\agents\__pycache__"
if exist "src\ugentic\agents\react_agents\__pycache__" rmdir /s /q "src\ugentic\agents\react_agents\__pycache__"
if exist "src\ugentic\__pycache__" rmdir /s /q "src\ugentic\__pycache__"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Clear logs (preserve directory)
echo Clearing old logs...
if exist "logs" (
    del /q "logs\*.jsonl" 2>nul
    if exist "logs\agents" del /q "logs\agents\*.jsonl" 2>nul
)

REM Clear plans (preserve directory)
echo Clearing old investigation plans...
if exist "plans" del /q "plans\*.json" 2>nul

REM Clear test results (preserve directory)
echo Clearing old test results...
if exist "test_results" del /q "test_results\*" 2>nul

echo.
echo ============================================================
echo CLEANUP COMPLETE
echo ============================================================
echo.
echo System ready for Phase 3 expert demonstrations.
echo.
echo PRESERVED:
echo   - docs/ (all planning files)
echo   - DISSERTATION_ACADEMIC/ (dissertation)
echo   - src/ (source code)
echo   - knowledge_base/ (agent knowledge)
echo   - data/memory/ (66 investigation history)
echo   - config.json (configuration)
echo   - .venv/ (virtual environment)
echo   - .git/ (version control)
echo.
echo ARCHIVED:
echo   - Old session summaries -^> docs\Project_Tracker\archive\
echo.
echo REMOVED:
echo   - Outdated proposal versions
echo   - Old test scripts
echo   - Diagnostic files
echo   - Python cache files
echo   - Old logs, plans, test results
echo.
echo Next Steps:
echo   1. Review docs\Project_Tracker\SESSION_29_SYSTEM_ANALYSIS.md
echo   2. Verify system with: python app.py
echo   3. Begin Phase 3 expert validation interviews
echo.
pause
