@echo off
echo Starting Notes Repository Launcher...
python notes_launcher.py
if %errorlevel% neq 0 (
    echo Python launcher failed, trying simple viewer...
    python view_notes.py
    if %errorlevel% neq 0 (
        echo.
        echo Python seems to be unavailable. Opening Home.md directly...
        start "" "Home.md"
        echo.
        echo For the best experience, please install a Markdown viewer extension:
        echo https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg
        pause
    )
) 