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
VERSION_FILE = ".version"
CONFIG_FILE = ".notes_config.json"

# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class NotesLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Repository Launcher")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # Set app icon if available
        try:
            if platform.system() == "Windows":
                self.root.iconbitmap(os.path.join(SCRIPT_DIR, "icon.ico"))
        except:
            pass
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#0366d6")
        style.configure("TFrame", background="#f6f8fa")
        style.configure("TLabel", background="#f6f8fa", font=("Arial", 11))
        style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        style.configure("Topic.TLabel", font=("Arial", 12, "bold"))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20 20 20 20", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(main_frame, text="Notes Repository", style="Header.TLabel")
        header_label.pack(pady=(0, 10), anchor=tk.W)
        
        description = ttk.Label(main_frame, text="Select a topic to view or use the options below", wraplength=550)
        description.pack(pady=(0, 20), anchor=tk.W)
        
        # Topics frame
        topics_frame = ttk.Frame(main_frame)
        topics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Topic: Java Collections
        java_frame = ttk.Frame(topics_frame, padding="10 10 10 10", relief="solid", borderwidth=1)
        java_frame.pack(fill=tk.X, pady=5)
        
        java_label = ttk.Label(java_frame, text="Java Collections Framework", style="Topic.TLabel")
        java_label.pack(anchor=tk.W)
        
        java_desc = ttk.Label(java_frame, text="Notes on Java's collections, implementations, and traversal mechanisms", wraplength=550)
        java_desc.pack(anchor=tk.W, pady=(5, 10))
        
        java_button = ttk.Button(java_frame, text="View Topic", command=lambda: self.open_topic("Collection framework/Home.md"))
        java_button.pack(anchor=tk.W)
        
        # Topic: Spring Boot
        spring_frame = ttk.Frame(topics_frame, padding="10 10 10 10", relief="solid", borderwidth=1)
        spring_frame.pack(fill=tk.X, pady=5)
        
        spring_label = ttk.Label(spring_frame, text="Spring Boot", style="Topic.TLabel")
        spring_label.pack(anchor=tk.W)
        
        spring_desc = ttk.Label(spring_frame, text="Notes on Spring Boot framework, features, and development techniques", wraplength=550)
        spring_desc.pack(anchor=tk.W, pady=(5, 10))
        
        spring_button = ttk.Button(spring_frame, text="View Topic", command=lambda: self.open_topic("Spring Boot/Home.md"))
        spring_button.pack(anchor=tk.W)
        
        # Options frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.main_home_button = ttk.Button(options_frame, text="Open Main Home", command=lambda: self.open_topic("Home.md"))
        self.main_home_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.check_updates_button = ttk.Button(options_frame, text="Check for Updates", command=self.check_for_updates)
        self.check_updates_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.install_md_button = ttk.Button(options_frame, text="Install Markdown Viewer", command=self.install_markdown_viewer)
        self.install_md_button.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Last checked: {self.get_last_check_date()}")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Check for updates on startup if enabled in config
        config = self.load_config()
        if config.get("check_updates_on_startup", True):
            self.root.after(1000, self.check_for_updates_silent)
    
    def open_topic(self, path):
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
            with urlopen(f"{API_URL}/commits") as response:
                commits = json.loads(response.read().decode())
                
                if not commits:
                    self.status_var.set("No commits found in repository")
                    return
                
                latest_commit_sha = commits[0]["sha"]
                current_commit = self.get_current_version()
                
                if current_commit != latest_commit_sha:
                    if messagebox.askyesno("Updates Available", 
                                           "There are updates available for the Notes Repository.\nWould you like to update now?"):
                        self.update_repository(latest_commit_sha)
                else:
                    messagebox.showinfo("Up to Date", "Your Notes Repository is up to date!")
                    self.status_var.set(f"Up to date. Last checked: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Save last check date
            config = self.load_config()
            config["last_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_config(config)
            
        except URLError as e:
            self.status_var.set(f"Error checking for updates: {e.reason}")
    
    def check_for_updates_silent(self):
        """Check for updates without user interaction"""
        try:
            with urlopen(f"{API_URL}/commits") as response:
                commits = json.loads(response.read().decode())
                
                if not commits:
                    return
                
                latest_commit_sha = commits[0]["sha"]
                current_commit = self.get_current_version()
                
                if current_commit != latest_commit_sha:
                    if messagebox.askyesno("Updates Available", 
                                           "There are updates available for the Notes Repository.\nWould you like to update now?"):
                        self.update_repository(latest_commit_sha)
                else:
                    self.status_var.set(f"Up to date. Last checked: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
            # Save last check date
            config = self.load_config()
            config["last_check"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            self.save_config(config)
            
        except URLError:
            # Silently fail
            pass
    
    def update_repository(self, new_version):
        """Update the repository to the latest version"""
        self.status_var.set("Updating repository...")
        
        try:
            # First determine if git is available
            try:
                subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                has_git = True
            except (subprocess.SubprocessError, FileNotFoundError):
                has_git = False
            
            if has_git:
                # Use git to update
                result = subprocess.run(["git", "pull"], cwd=SCRIPT_DIR, 
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if result.returncode == 0:
                    self.set_current_version(new_version)
                    messagebox.showinfo("Update Complete", "The Notes Repository has been updated successfully!")
                    self.status_var.set("Update complete")
                else:
                    messagebox.showerror("Update Failed", f"Error updating repository:\n{result.stderr}")
                    self.status_var.set("Update failed")
            else:
                # Manual update - direct users to download latest
                webbrowser.open(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/latest")
                messagebox.showinfo("Manual Update Required", 
                                    "Please download the latest release from the GitHub page that has opened in your browser.")
                self.status_var.set("Manual update required")
                
        except Exception as e:
            messagebox.showerror("Update Error", f"Error updating repository: {str(e)}")
            self.status_var.set("Update error")
    
    def get_current_version(self):
        """Get the current version from the version file"""
        version_path = os.path.join(SCRIPT_DIR, VERSION_FILE)
        if os.path.exists(version_path):
            with open(version_path, 'r') as f:
                return f.read().strip()
        return ""
    
    def set_current_version(self, version):
        """Save the current version to the version file"""
        version_path = os.path.join(SCRIPT_DIR, VERSION_FILE)
        with open(version_path, 'w') as f:
            f.write(version)
    
    def get_last_check_date(self):
        """Get the date of the last update check"""
        config = self.load_config()
        return config.get("last_check", "Never")
    
    def load_config(self):
        """Load the configuration file"""
        config_path = os.path.join(SCRIPT_DIR, CONFIG_FILE)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"check_updates_on_startup": True, "last_check": "Never"}
    
    def save_config(self, config):
        """Save the configuration file"""
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