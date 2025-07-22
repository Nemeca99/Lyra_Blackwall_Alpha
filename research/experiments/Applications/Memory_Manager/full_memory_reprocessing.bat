@echo off
echo =============================================
echo Lyra Memory System: Complete Reprocessing Tool
echo =============================================
echo.
echo This tool will:
echo  1. Reprocess memory files from raw JSON
echo  2. Fix markdown formatting
echo  3. Regenerate the memory index
echo  4. Restart the dashboard
echo.
echo Press Ctrl+C now to cancel, or...
pause

cd /d "%~dp0"

echo.
echo Step 1: Reprocessing memory files from raw JSON...
echo ------------------------------------------------
python Copilot\reprocess_memory_files.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to reprocess memory files.
    goto error
)

echo.
echo Step 2: Fixing markdown formatting...
echo -----------------------------------
python Copilot\fix_memory_markdown.py
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Markdown fixing completed with errors.
)

echo.
echo Step 3: Regenerating memory index...
echo ---------------------------------
python Copilot\generate_memory_index.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to regenerate memory index.
    goto error
)

echo.
echo Step 4: Restarting dashboard...
echo ----------------------------
echo All processing complete! Starting dashboard with ngrok...
echo.
call run_web_dashboard_with_ngrok.bat
exit /b 0

:error
echo.
echo An error occurred during processing. 
echo Check the log files for more information:
echo - memory_reprocessor.log
echo - memory_markdown_fixer.log
echo - memory_indexer.log
echo.
pause
exit /b 1
