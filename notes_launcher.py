#!/usr/bin/env python3
# Notes Repository Launcher
# This script provides an easy way to browse the Notes Repository
# and can check for updates if connected to the internet

import os
import sys
import webbrowser
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import platform
import datetime
import json
from urllib.request import urlopen
from urllib.error import URLError

# Configuration
REPO_OWNER = "Saf-One"
REPO_NAME = "Notes"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
VERSION_FILE = "utils/.version"
CONFIG_FILE = "utils/.notes_config.json"

# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class NotesLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Repository Launcher")
        self.root.geometry("500x300")
        self.root.resizable(True, True)
        
        # Set app icon if available
        try:
            if platform.system() == "Windows":
                self.root.iconbitmap(os.path.join(SCRIPT_DIR, "utils/icon.ico"))
        except:
            pass
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#0366d6")
        style.configure("TFrame", background="#f6f8fa")
        style.configure("TLabel", background="#f6f8fa", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(main_frame, text="Notes Repository", style="Header.TLabel")
        header_label.pack(pady=(0, 10), anchor=tk.W)
        
        description = ttk.Label(main_frame, text="Your personal programming study notes collection", wraplength=450)
        description.pack(pady=(0, 20), anchor=tk.W)
        
        # Main button
        open_button = ttk.Button(main_frame, text="Open Notes Home", command=lambda: self.open_file("Home.md"))
        open_button.pack(pady=10)
        
        # Options frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.check_updates_button = ttk.Button(options_frame, text="Check for Updates", command=self.check_for_updates)
        self.check_updates_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.install_md_button = ttk.Button(options_frame, text="Install Markdown Viewer", command=self.install_markdown_viewer)
        self.install_md_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to view your notes")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_file(self, path):
        """Open a markdown file in the default browser"""
        full_path = os.path.join(SCRIPT_DIR, path)
        
        if not os.path.exists(full_path):
            messagebox.showerror("Error", f"File not found: {path}")
            return
        
        # Convert to URL format for browser
        if platform.system() == "Windows":
            url = f"file:///{full_path.replace(os.sep, '/')}"
        else:
            url = f"file://{full_path}"
        
        webbrowser.open(url)
        self.status_var.set(f"Opened: {path}")
        
        # Suggest markdown viewer if not installed
        config = self.load_config()
        if not config.get("markdown_viewer_suggested", False):
            if messagebox.askyesno("Markdown Viewer", 
                "For the best viewing experience, we recommend installing a Markdown viewer extension.\n\nWould you like to install one now?"):
                self.install_markdown_viewer()
            config["markdown_viewer_suggested"] = True
            self.save_config(config)
    
    def check_for_updates(self):
        """Check for updates and show a message to the user"""
        self.status_var.set("Checking for updates...")
        try:
            # Create utils directory if it doesn't exist
            utils_dir = os.path.join(SCRIPT_DIR, "utils")
            if not os.path.exists(utils_dir):
                os.makedirs(utils_dir)
            
            with urlopen(f"{API_URL}/releases/latest") as response:
                release_info = json.loads(response.read().decode())
                
                if not release_info:
                    self.status_var.set("No releases found")
                    return
                
                latest_version = release_info["tag_name"]
                current_version = self.get_current_version()
                
                if current_version != latest_version:
                    if messagebox.askyesno("Updates Available", 
                                           f"New version available: {latest_version}\nYour version: {current_version or 'Unknown'}\n\nWould you like to download the update?"):
                        self.download_update(release_info["html_url"])
                else:
                    messagebox.showinfo("Up to Date", f"Your Notes Repository is up to date! (Version {current_version})")
                    self.status_var.set(f"Up to date. Last checked: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Save last check date
            config = self.load_config()
            config["last_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_config(config)
            
        except URLError as e:
            self.status_var.set(f"Error checking for updates: {e.reason}")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def download_update(self, release_url):
        """Direct the user to download the updated release"""
        self.status_var.set("Opening release page...")
        webbrowser.open(release_url)
        messagebox.showinfo("Manual Update Required", 
                            "Please download the latest release from the GitHub page that has opened in your browser.")
    
    def get_current_version(self):
        """Get the current version from the version file"""
        version_path = os.path.join(SCRIPT_DIR, VERSION_FILE)
        if os.path.exists(version_path):
            with open(version_path, 'r') as f:
                return f.read().strip()
        return "v1.0"  # Default version if file doesn't exist
    
    def set_current_version(self, version):
        """Save the current version to the version file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.join(SCRIPT_DIR, VERSION_FILE)), exist_ok=True)
        
        version_path = os.path.join(SCRIPT_DIR, VERSION_FILE)
        with open(version_path, 'w') as f:
            f.write(version)
    
    def load_config(self):
        """Load the configuration file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.join(SCRIPT_DIR, CONFIG_FILE)), exist_ok=True)
        
        config_path = os.path.join(SCRIPT_DIR, CONFIG_FILE)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"markdown_viewer_suggested": False, "last_check": "Never"}
    
    def save_config(self, config):
        """Save the configuration file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.join(SCRIPT_DIR, CONFIG_FILE)), exist_ok=True)
        
        config_path = os.path.join(SCRIPT_DIR, CONFIG_FILE)
        with open(config_path, 'w') as f:
            json.dump(config, f)
    
    def install_markdown_viewer(self):
        """Open the Chrome Web Store to install the Markdown Reader extension"""
        webbrowser.open("https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg")
        self.status_var.set("Opened Markdown Reader extension page")


def main():
    # If no GUI arguments provided, just open the main Home.md
    if len(sys.argv) > 1 and sys.argv[1] == "--no-gui":
        home_path = os.path.join(SCRIPT_DIR, "Home.md")
        if platform.system() == "Windows":
            url = f"file:///{home_path.replace(os.sep, '/')}"
        else:
            url = f"file://{home_path}"
        webbrowser.open(url)
        print("Opened Home.md in your default browser.")
        print("For best viewing experience, install a Markdown viewer extension like:")
        print("https://chromewebstore.google.com/detail/markdown-reader/medapdbncneneejhbgcjceippjlfkmkg")
        return
    
    # Start the GUI
    root = tk.Tk()
    app = NotesLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main() 