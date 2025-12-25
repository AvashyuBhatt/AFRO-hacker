"""
Main Window UI for Pokemon Fire Red Binary Hacking Tool

This module implements the main application window with tabbed interface
matching the Hex Maniac Advance design.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any

from .hex_editor_tab import HexEditorTab
from .pokemon_data_tab import PokemonDataTab
from .map_editor_tab import MapEditorTab
from .roaming_pokemon_tab import RoamingPokemonTab
from .alpha_pokemon_tab import AlphaPokemonTab
from .quest_system_tab import QuestSystemTab

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, rom_engine, config):
        self.root = root
        self.rom_engine = rom_engine
        self.config = config
        
        self.notebook = None
        self.tabs: Dict[str, Any] = {}
        self.status_bar = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the main UI components"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create toolbar
        self.create_toolbar(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar
        self.create_status_bar(main_frame)
        
        # Initially disable tabs until ROM is loaded
        self.set_tabs_enabled(False)
    
    def create_toolbar(self, parent):
        """Create the main toolbar"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Navigation buttons
        nav_frame = ttk.Frame(toolbar_frame)
        nav_frame.pack(side=tk.LEFT)
        
        ttk.Button(nav_frame, text="◀", width=3, command=self.go_back).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(nav_frame, text="▶", width=3, command=self.go_forward).pack(side=tk.LEFT, padx=(0, 10))
        
        # Search frame
        search_frame = ttk.Frame(toolbar_frame)
        search_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(5, 2))
        search_entry.bind('<Return>', self.perform_search)
        
        ttk.Button(search_frame, text="🔍", width=3, command=self.perform_search).pack(side=tk.LEFT)
        
        # Row width controls
        row_frame = ttk.Frame(toolbar_frame)
        row_frame.pack(side=tk.RIGHT)
        
        ttk.Label(row_frame, text="Row Width:").pack(side=tk.LEFT)
        self.row_width_var = tk.StringVar(value="16")
        row_spinbox = ttk.Spinbox(row_frame, from_=8, to=32, width=5, 
                                 textvariable=self.row_width_var,
                                 command=self.update_row_width)
        row_spinbox.pack(side=tk.LEFT, padx=(5, 2))
        
        ttk.Button(row_frame, text="Auto", command=self.auto_row_width).pack(side=tk.LEFT)
    
    def create_tabs(self):
        """Create all application tabs"""
        # Hex Editor Tab
        self.tabs['hex'] = HexEditorTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['hex'].frame, text="Hex Editor")
        
        # Pokemon Data Tab
        self.tabs['pokemon'] = PokemonDataTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['pokemon'].frame, text="Pokemon Data")
        
        # Map Editor Tab
        self.tabs['map'] = MapEditorTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['map'].frame, text="Map Editor")
        
        # Roaming Pokemon Tab
        self.tabs['roaming'] = RoamingPokemonTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['roaming'].frame, text="Roaming Pokemon")
        
        # Alpha Pokemon Tab
        self.tabs['alpha'] = AlphaPokemonTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['alpha'].frame, text="Alpha Pokemon")
        
        # Quest System Tab
        self.tabs['quest'] = QuestSystemTab(self.notebook, self.rom_engine)
        self.notebook.add(self.tabs['quest'].frame, text="Quest System")
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        self.status_bar = ttk.Frame(parent)
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Left side - ROM info
        self.rom_info_label = ttk.Label(self.status_bar, text="No ROM loaded")
        self.rom_info_label.pack(side=tk.LEFT)
        
        # Right side - Position info
        self.position_label = ttk.Label(self.status_bar, text="")
        self.position_label.pack(side=tk.RIGHT)
    
    def show_tab(self, tab_name: str):
        """Show a specific tab"""
        if tab_name in self.tabs:
            # Find the tab index
            for i in range(self.notebook.index("end")):
                if self.notebook.tab(i, "text").lower().replace(" ", "") == tab_name.lower():
                    self.notebook.select(i)
                    break
    
    def set_tabs_enabled(self, enabled: bool):
        """Enable or disable all tabs"""
        state = "normal" if enabled else "disabled"
        for i in range(self.notebook.index("end")):
            self.notebook.tab(i, state=state)
    
    def on_rom_loaded(self):
        """Called when a ROM is successfully loaded"""
        self.set_tabs_enabled(True)
        
        # Update status bar
        rom_info = self.rom_engine.get_rom_info()
        rom_name = rom_info.get('title', 'Unknown ROM')
        rom_size = self.rom_engine.get_rom_size()
        self.rom_info_label.config(text=f"{rom_name} ({rom_size:,} bytes)")
        
        # Notify all tabs
        for tab in self.tabs.values():
            if hasattr(tab, 'on_rom_loaded'):
                tab.on_rom_loaded()
        
        messagebox.showinfo("ROM Loaded", f"Successfully loaded: {rom_name}")
    
    def on_rom_closed(self):
        """Called when ROM is closed"""
        self.set_tabs_enabled(False)
        self.rom_info_label.config(text="No ROM loaded")
        self.position_label.config(text="")
        
        # Notify all tabs
        for tab in self.tabs.values():
            if hasattr(tab, 'on_rom_closed'):
                tab.on_rom_closed()
    
    def update_position_info(self, offset: int, info: str = ""):
        """Update position information in status bar"""
        if offset >= 0:
            hex_offset = f"{offset:08X}"
            symbol = ""
            
            # Check for symbol at this address
            if self.rom_engine.symbol_parser:
                symbol_name = self.rom_engine.symbol_parser.get_symbol_name(offset)
                if symbol_name:
                    symbol = f" ({symbol_name})"
            
            position_text = f"Address: {hex_offset}{symbol}"
            if info:
                position_text += f" | {info}"
            
            self.position_label.config(text=position_text)
        else:
            self.position_label.config(text="")
    
    def go_back(self):
        """Navigate back (implement history later)"""
        current_tab = self.get_current_tab()
        if current_tab and hasattr(current_tab, 'go_back'):
            current_tab.go_back()
    
    def go_forward(self):
        """Navigate forward (implement history later)"""
        current_tab = self.get_current_tab()
        if current_tab and hasattr(current_tab, 'go_forward'):
            current_tab.go_forward()
    
    def perform_search(self, event=None):
        """Perform search in current tab"""
        search_term = self.search_var.get().strip()
        if not search_term:
            return
        
        current_tab = self.get_current_tab()
        if current_tab and hasattr(current_tab, 'search'):
            current_tab.search(search_term)
    
    def update_row_width(self):
        """Update row width in hex editor"""
        try:
            width = int(self.row_width_var.get())
            if 'hex' in self.tabs:
                self.tabs['hex'].set_bytes_per_row(width)
        except ValueError:
            pass
    
    def auto_row_width(self):
        """Set automatic row width"""
        self.row_width_var.set("16")
        self.update_row_width()
    
    def get_current_tab(self):
        """Get the currently selected tab object"""
        try:
            current_index = self.notebook.index(self.notebook.select())
            tab_names = list(self.tabs.keys())
            if 0 <= current_index < len(tab_names):
                return self.tabs[tab_names[current_index]]
        except:
            pass
        return None
    
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show info dialog"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show warning dialog"""
        messagebox.showwarning(title, message)

