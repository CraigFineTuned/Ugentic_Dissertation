@echo off
echo Cleaning up irrelevant knowledge base files...
echo.

cd documents\policies

echo Removing budget.csv...
if exist budget.csv (
    del budget.csv
    echo   - Removed budget.csv
) else (
    echo   - budget.csv already removed
)

echo Removing HR_Policy_2025.md...
if exist HR_Policy_2025.md (
    del HR_Policy_2025.md
    echo   - Removed HR_Policy_2025.md
) else (
    echo   - HR_Policy_2025.md already removed
)

echo Removing market_research.md...
if exist market_research.md (
    del market_research.md
    echo   - Removed market_research.md
) else (
    echo   - market_research.md already removed
)

echo.
echo Cleanup complete!
echo Knowledge base now contains only IT-specific documents:
echo   - IT_Department_Policies.md
echo   - IT_Support_Knowledge_Base.md
echo.
pause
