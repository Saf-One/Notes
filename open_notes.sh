#!/bin/bash

echo "Starting Notes Repository Launcher..."
python3 notes_launcher.py

if [ $? -ne 0 ]; then
    echo "Python launcher failed, trying simple viewer..."
    python3 view_notes.py
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "Python seems to be unavailable. Opening Home.md directly..."
        
        # Determine which command to use based on OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            open "Home.md"
        else
            # Linux
            xdg-open "Home.md" 2>/dev/null || sensible-browser "Home.md" 2>/dev/null || firefox "Home.md" 2>/dev/null || google-chrome "Home.md" 2>/dev/null
        fi
        
        echo ""
        echo "For the best experience, please install a Markdown viewer extension:"
        echo "https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg"
        read -p "Press Enter to continue..."
    fi
fi 