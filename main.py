#!/usr/bin/env python3
"""Pokemon Fire Red Binary Hacking Tool - FIXED VERSION"""

import sys, os, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from core.rom_engine import ROMEngine
from core.config import Config

class PokemonFireRedHacker:
    """Main application class"""

    def __init__(self):
        self.root = tk.Tk()
        self.config = Config()
        self.rom_engine = None
        self.main_window = None
        self.setup_application()

    def setup_application(self):
        """Initialize the application"""
        self.root.title("AFRO Hacker - Fire Red Advanced ROM Options v1.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)

        try:
            icon_path = Path(__file__).parent / "assets" / "icon.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass

        self.setup_dark_theme()
        self.rom_engine = ROMEngine()
        self.main_window = MainWindow(self.root, self.rom_engine, self.config)
        self.setup_menu_bar()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_dark_theme(self):
        """Configure dark theme"""
        style = ttk.Style()
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        select_bg = "#404040"

        style.theme_use('clam')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=select_bg, foreground=fg_color)
        style.configure('TEntry', background=select_bg, foreground=fg_color)
        style.configure('TCombobox', background=select_bg, foreground=fg_color)
        style.configure('TNotebook', background=bg_color)
        style.configure('TNotebook.Tab', background=select_bg, foreground=fg_color)
        self.root.configure(bg=bg_color)

    def setup_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open ROM...", command=self.open_rom)
        file_menu.add_command(label="Save ROM", command=self.save_rom)
        file_menu.add_command(label="Save ROM As...", command=self.save_rom_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", state="disabled")
        edit_menu.add_command(label="Redo", state="disabled")

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Hex Editor", command=lambda: self.main_window.show_tab("hex"))
        view_menu.add_command(label="Map Editor", command=lambda: self.main_window.show_tab("map"))
        view_menu.add_command(label="Pokemon Data", command=lambda: self.main_window.show_tab("pokemon"))
        view_menu.add_command(label="Roaming Pokemon", command=lambda: self.main_window.show_tab("roaming"))
        view_menu.add_command(label="Alpha Pokemon", command=lambda: self.main_window.show_tab("alpha"))
        view_menu.add_command(label="Quest System", command=lambda: self.main_window.show_tab("quest"))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def open_rom(self):
        """Open ROM"""
        file_path = filedialog.askopenfilename(
            title="Open Pokemon Fire Red ROM",
            filetypes=[("GBA ROM files", "*.gba"), ("All files", "*.*")]
        )
        if file_path:
            try:
                success = self.rom_engine.load_rom(file_path)
                if success:
                    self.main_window.on_rom_loaded()
                    messagebox.showinfo("Success", f"ROM loaded: {os.path.basename(file_path)}")
                else:
                    messagebox.showerror("Error", "Invalid Fire Red ROM (BPRE/BPGE)")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

    def save_rom(self):
        """Save ROM"""
        if self.rom_engine and self.rom_engine.is_loaded():
            try:
                if self.rom_engine.save_rom():
                    messagebox.showinfo("Success", "ROM saved!")
                else:
                    messagebox.showerror("Error", "Failed to save ROM")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No ROM loaded")

    def save_rom_as(self):
        """Save ROM as"""
        if self.rom_engine and self.rom_engine.is_loaded():
            file_path = filedialog.asksaveasfilename(
                title="Save ROM As",
                defaultextension=".gba",
                filetypes=[("GBA ROM files", "*.gba"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    if self.rom_engine.save_rom_as(file_path):
                        messagebox.showinfo("Success", f"ROM saved: {os.path.basename(file_path)}")
                    else:
                        messagebox.showerror("Error", "Failed to save ROM")
                except Exception as e:
                    messagebox.showerror("Error", f"Error: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No ROM loaded")

    def show_about(self):
        """Show about"""
        about_text = """AFRO Hacker v1.0 - Pokemon Fire Red ROM Hacking Tool

Features:
✓ HMA-Style Map Editor
✓ Roaming Pokemon System
✓ Alpha Pokemon
✓ Quest System
✓ Tile Editing

Developed with Python & Tkinter"""
        messagebox.showinfo("About", about_text)

    def on_closing(self):
        """Close app"""
        if self.rom_engine and self.rom_engine.has_unsaved_changes():
            result = messagebox.askyesnocancel("Unsaved Changes", "Save before closing?")
            if result is True:
                self.save_rom()
            elif result is None:
                return
        self.root.destroy()

    def run(self):
        """Run app"""
        self.root.mainloop()

def main():
    try:
        app = PokemonFireRedHacker()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

    try:
        import ui.alpha_pokemon_tab
        import ui.hex_editor_tab
        import ui.main_window
        import ui.map_editor_tab
        import ui.pokemon_data_tab
        import ui.quest_system_tab
        import ui.roaming_pokemon_tab
    except ImportError:
        pass
