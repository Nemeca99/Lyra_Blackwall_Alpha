@echo off
echo Fixing markdown formatting in memory chunks...
python Copilot\fix_memory_markdown.py

echo Regenerating memory index...
python Copilot\generate_memory_index.py

echo Done! You can now run the dashboard to see the improved display.
