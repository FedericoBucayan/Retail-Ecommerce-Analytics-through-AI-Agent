@echo off
title Power BI Project Validator
color 0A
echo ========================================================
echo   RETAIL & E-COMMERCE ANALYTICS REPORT VALIDATOR
echo ========================================================
echo.
echo Running PBIR schema and visual binding validation...
echo.

python scripts\check_validation.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  [SUCCESS] All schemas, measures, and visuals are valid!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo  [WARNING/ERROR] Issues were detected during validation.
    echo ========================================================
)
echo.
pause
