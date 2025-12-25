#!/usr/bin/env python3
"""
Pokemon Fire Red Binary Hacking Tool
Main application entry point

This application provides comprehensive ROM hacking capabilities for Pokemon Fire Red,
including roaming Pokemon mechanics, alpha Pokemon features, and quest systems.
The interface is designed to be identical to Hex Maniac Advance.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from core.rom_engine import ROMEngine
from core.config import Config

class PokemonFireRedHacker:
    """Main application class for the Pokemon Fire Red Binary Hacking Tool"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.config = Config()
        self.rom_engine = None
        self.main_window = None
        
        self.setup_application()
    
    def setup_application(self):
        """Initialize the application"""
        # Configure the main window
        self.root.title("Pokemon Fire Red Binary Hacking Tool v1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Set application icon (if available)
        try:
            icon_path = Path(__file__).parent.parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception:
            pass  # Icon not available, continue without it
        
        # Configure style for dark theme
        self.setup_dark_theme()
        
        # Initialize ROM engine
        self.rom_engine = ROMEngine()
        
        # Create main window
        self.main_window = MainWindow(self.root, self.rom_engine, self.config)
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_dark_theme(self):
        """Configure the dark theme for the application"""
        style = ttk.Style()
        
        # Configure dark theme colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        select_bg = "#404040"
        select_fg = "#ffffff"
        
        # Configure ttk styles
        style.theme_use('clam')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=select_bg, foreground=fg_color)
        style.configure('TEntry', background=select_bg, foreground=fg_color)
        style.configure('TCombobox', background=select_bg, foreground=fg_color)
        style.configure('TNotebook', background=bg_color)
        style.configure('TNotebook.Tab', background=select_bg, foreground=fg_color)
        
        # Configure root window
        self.root.configure(bg=bg_color)
    
    def setup_menu_bar(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open ROM...", command=self.open_rom)
        file_menu.add_command(label="Save ROM", command=self.save_rom)
        file_menu.add_command(label="Save ROM As...", command=self.save_rom_as)
        file_menu.add_separator()
        file_menu.add_command(label="Recent Files", state="disabled")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", state="disabled")
        edit_menu.add_command(label="Redo", state="disabled")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", state="disabled")
        edit_menu.add_command(label="Replace...", state="disabled")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Hex Editor", command=lambda: self.main_window.show_tab("hex"))
        view_menu.add_command(label="Map Editor", command=lambda: self.main_window.show_tab("map"))
        view_menu.add_command(label="Pokemon Data", command=lambda: self.main_window.show_tab("pokemon"))
        view_menu.add_command(label="Roaming Pokemon", command=lambda: self.main_window.show_tab("roaming"))
        view_menu.add_command(label="Alpha Pokemon", command=lambda: self.main_window.show_tab("alpha"))
        view_menu.add_command(label="Quest System", command=lambda: self.main_window.show_tab("quest"))
        
        # Utilities menu
        utilities_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Utilities", menu=utilities_menu)
        utilities_menu.add_command(label="Symbol File Manager", state="disabled")
        utilities_menu.add_command(label="Asset Extractor", state="disabled")
        utilities_menu.add_command(label="Script Compiler", state="disabled")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Validate ROM", state="disabled")
        tools_menu.add_command(label="Backup Manager", state="disabled")
        tools_menu.add_command(label="Settings", state="disabled")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", state="disabled")
        help_menu.add_command(label="Tutorials", state="disabled")
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def open_rom(self):
        """Open a Pokemon Fire Red ROM file"""
        file_path = filedialog.askopenfilename(
            title="Open Pokemon Fire Red ROM",
            filetypes=[
                ("GBA ROM files", "*.gba"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                success = self.rom_engine.load_rom(file_path)
                if success:
                    self.main_window.on_rom_loaded()
                    messagebox.showinfo("Success", f"ROM loaded successfully: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Failed to load ROM file. Please check if it's a valid Pokemon Fire Red ROM.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the ROM: {str(e)}")
    
    def save_rom(self):
        """Save the current ROM"""
        if self.rom_engine and self.rom_engine.is_loaded():
            try:
                success = self.rom_engine.save_rom()
                if success:
                    messagebox.showinfo("Success", "ROM saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save ROM file.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the ROM: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No ROM file is currently loaded.")
    
    def save_rom_as(self):
        """Save the ROM with a new filename"""
        if self.rom_engine and self.rom_engine.is_loaded():
            file_path = filedialog.asksaveasfilename(
                title="Save ROM As",
                defaultextension=".gba",
                filetypes=[
                    ("GBA ROM files", "*.gba"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                try:
                    success = self.rom_engine.save_rom_as(file_path)
                    if success:
                        messagebox.showinfo("Success", f"ROM saved successfully: {os.path.basename(file_path)}")
                    else:
                        messagebox.showerror("Error", "Failed to save ROM file.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while saving the ROM: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No ROM file is currently loaded.")
    
    def show_about(self):
        """Show the about dialog"""
        about_text = """Pokemon Fire Red Binary Hacking Tool v1.0

A comprehensive ROM hacking tool for Pokemon Fire Red with advanced features:
• Roaming Pokemon mechanics
• Alpha Pokemon system
• Quest management
• Map editing with drag-and-drop sprites
• Interface identical to Hex Maniac Advance

Developed using Python and tkinter
Compatible with Pokemon Fire Red (English)"""
        
        messagebox.showinfo("About", about_text)
    
    def on_closing(self):
        """Handle application closing"""
        if self.rom_engine and self.rom_engine.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?"
            )
            if result is True:  # Yes
                self.save_rom()
            elif result is None:  # Cancel
                return
        
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = PokemonFireRedHacker()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"A fatal error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



# Explicitly import ui submodules to ensure PyInstaller includes them
import ui.alpha_pokemon_tab
import ui.hex_editor_tab
import ui.main_window
import ui.map_editor_tab
import ui.pokemon_data_tab
import ui.quest_system_tab
import ui.roaming_pokemon_tab


