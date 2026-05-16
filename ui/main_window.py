"""Main Window UI"""

import tkinter as tk
from tkinter import ttk
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ui.map_editor_tab import MapEditorTab
from ui.hex_editor_tab import HexEditorTab
from ui.roaming_pokemon_tab import RoamingPokemonTab
from ui.alpha_pokemon_tab import AlphaPokemonTab
from ui.quest_system_tab import QuestSystemTab
from ui.pokemon_data_tab import PokemonDataTab

class MainWindow:
    """Main window"""

    def __init__(self, root, rom_engine, config):
        self.root = root
        self.rom_engine = rom_engine
        self.config = config
        self.map_editor_tab = None
        self.hex_editor_tab = None
        self.roaming_pokemon_tab = None
        self.alpha_pokemon_tab = None
        self.quest_system_tab = None
        self.pokemon_data_tab = None
        self.setup_ui()

    def setup_ui(self):
        """Create UI"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Map Editor")
            self.map_editor_tab = MapEditorTab(frame, self.rom_engine)
        except Exception as e:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Map Editor")
            ttk.Label(frame, text=f"Error: {str(e)}").pack(padx=10, pady=10)

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Hex Editor")
            self.hex_editor_tab = HexEditorTab(frame, self.rom_engine)
        except Exception as e:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Hex Editor")

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Pokemon Data")
            self.pokemon_data_tab = PokemonDataTab(frame, self.rom_engine)
        except:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Pokemon Data")

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Roaming Pokemon")
            self.roaming_pokemon_tab = RoamingPokemonTab(frame, self.rom_engine)
        except:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Roaming Pokemon")

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Alpha Pokemon")
            self.alpha_pokemon_tab = AlphaPokemonTab(frame, self.rom_engine)
        except:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Alpha Pokemon")

        try:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Quest System")
            self.quest_system_tab = QuestSystemTab(frame, self.rom_engine)
        except:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text="Quest System")

    def on_rom_loaded(self):
        """ROM loaded callback"""
        print("✓ ROM loaded signal in main window")
        if self.map_editor_tab and hasattr(self.map_editor_tab, 'on_rom_loaded'):
            try:
                self.map_editor_tab.on_rom_loaded()
            except Exception as e:
                print(f"Error notifying map editor: {e}")

    def show_tab(self, tab_name: str):
        """Show tab"""
        tabs = {'map': 0, 'hex': 1, 'pokemon': 2, 'roaming': 3, 'alpha': 4, 'quest': 5}
        if tab_name in tabs:
            self.notebook.select(tabs[tab_name])
