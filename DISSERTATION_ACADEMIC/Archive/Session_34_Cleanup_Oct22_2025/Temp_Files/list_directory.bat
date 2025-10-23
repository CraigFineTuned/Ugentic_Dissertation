@echo off
setlocal enabledelayedexpansion
set "output_file=directory_structure.txt"
echo Listing directory structure... > "%output_file%"

rem Check if .venv exists and note its presence
if exist ".venv" echo [.venv exists - Virtual Environment] >> "%output_file%"

rem Recursively list files and folders excluding .venv
(for /f "delims=" %%A in ('dir /s /b /a-d ^| findstr /v /i "\.venv\\"') do echo %%A) >> "%output_file%"

echo Directory structure exported to "%output_file%"
