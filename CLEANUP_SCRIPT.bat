@echo off
REM ========================================
REM UGENTIC PROJECT CLEANUP SCRIPT
REM October 14, 2025
REM ========================================
REM
REM IMPORTANT: Review this script before running!
REM This will archive reference folders and remove obsolete files.
REM
REM ========================================

echo.
echo ========================================
echo UGENTIC PROJECT CLEANUP
echo ========================================
echo.
echo This script will:
echo 1. Archive servers-main and elysia-main folders
echo 2. Remove obsolete/temporary files
echo 3. Clean up the project structure
echo.
echo Press Ctrl+C to cancel or
pause

echo.
echo ========================================
echo Step 1: Creating Archive Directory
echo ========================================
cd ..
if not exist "UGENTIC_ARCHIVE" mkdir UGENTIC_ARCHIVE
cd Ugentic_Dissertation

echo.
echo ========================================
echo Step 2: Archiving Reference Folders
echo ========================================
echo Moving servers-main to archive...
move servers-main ..\UGENTIC_ARCHIVE\

echo Moving elysia-main to archive...
move elysia-main ..\UGENTIC_ARCHIVE\

echo.
echo ========================================
echo Step 3: Removing Obsolete Files
echo ========================================

if exist app_old.py (
    echo Deleting app_old.py...
    del app_old.py
)

if exist "brave.pdf" (
    echo Deleting brave.pdf...
    del brave.pdf
)

if exist "Do_Not_Read.md" (
    echo Deleting Do_Not_Read.md...
    del Do_Not_Read.md
)

if exist "compress_ref_temp.md" (
    echo Deleting compress_ref_temp.md...
    del compress_ref_temp.md
)

if exist "global biased test.md" (
    echo Deleting global biased test.md...
    del "global biased test.md"
)

if exist "main" (
    echo Deleting main...
    del main
)

echo Deleting temp files...
if exist temp.md del temp.md
if exist temp.txt del temp.txt
if exist temp_log.txt del temp_log.txt
if exist temp_prompt.md del temp_prompt.md
if exist temp_prompt_now.md del temp_prompt_now.md
if exist temp_terminal.md del temp_terminal.md
if exist temp_terminal_out.md del temp_terminal_out.md

echo.
echo ========================================
echo Step 4: Removing Sprint Test Files
echo ========================================

if exist run_sprint3_tests.bat (
    echo Deleting run_sprint3_tests.bat...
    del run_sprint3_tests.bat
)

if exist run_sprint_tests.bat (
    echo Deleting run_sprint_tests.bat...
    del run_sprint_tests.bat
)

echo.
echo ========================================
echo CLEANUP COMPLETE!
echo ========================================
echo.
echo Archived folders:
echo - ..\UGENTIC_ARCHIVE\servers-main
echo - ..\UGENTIC_ARCHIVE\elysia-main
echo.
echo Removed obsolete files successfully.
echo.
echo Next steps:
echo 1. Verify archive folder exists: ..\UGENTIC_ARCHIVE
echo 2. Run: python tests\test_phase2_memory.py (after new memory implemented)
echo 3. Run: python app.py
echo.
pause
