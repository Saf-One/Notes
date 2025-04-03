#!/usr/bin/env python3
# Simple Notes Viewer
# A lightweight script to open markdown files directly

import os
import sys
import webbrowser
import platform

def main():
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default to home if no argument provided
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "Home.md"
    
    # Check if target exists
    target_path = os.path.join(script_dir, target)
    if not os.path.exists(target_path):
        print(f"Error: File not found: {target}")
        print("Available options:")
        print("  Home.md")
        print("  Collection framework/Home.md")
        print("  Spring Boot/Home.md")
        sys.exit(1)
    
    # Convert to URL format for browser
    if platform.system() == "Windows":
        url = f"file:///{target_path.replace(os.sep, '/')}"
    else:
        url = f"file://{target_path}"
    
    # Open in browser
    webbrowser.open(url)
    
    print("\nOpened:", target)
    print("\nFor the best viewing experience, install a Markdown viewer extension:")
    print("https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg")
    
    print("\nTips:")
    print("- Run 'python view_notes.py Home.md' to view the main home page")
    print("- Run 'python view_notes.py Collection framework/Home.md' to view Java Collections")
    print("- Run 'python view_notes.py Spring Boot/Home.md' to view Spring Boot")
    print("- For a more feature-rich experience, run 'python notes_launcher.py'")

if __name__ == "__main__":
    main() 