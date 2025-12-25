"""
Pokemon Data Tab for Pokemon Fire Red Binary Hacking Tool

This module implements the Pokemon data editing interface similar to Hex Maniac Advance.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional

class PokemonDataTab:
    """Pokemon data editor tab implementation"""
    
    def __init__(self, parent, rom_engine):
        self.parent = parent
        self.rom_engine = rom_engine
        
        self.frame = ttk.Frame(parent)
        self.current_pokemon_id = 1
        self.pokemon_data = {}
        
        # UI variables
        self.pokemon_name_var = tk.StringVar()
        self.hp_var = tk.IntVar()
        self.attack_var = tk.IntVar()
        self.defense_var = tk.IntVar()
        self.speed_var = tk.IntVar()
        self.sp_attack_var = tk.IntVar()
        self.sp_defense_var = tk.IntVar()
        self.type1_var = tk.StringVar()
        self.type2_var = tk.StringVar()
        self.catch_rate_var = tk.IntVar()
        self.base_exp_var = tk.IntVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the Pokemon data editor UI"""
        # Create main paned window
        paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Pokemon selection
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Pokemon selection
        selection_frame = ttk.LabelFrame(left_frame, text="Pokemon Selection")
        selection_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pokemon list
        list_frame = ttk.Frame(selection_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Search
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.bind('<KeyRelease>', self.filter_pokemon_list)
        
        # Pokemon listbox
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.pokemon_listbox = tk.Listbox(listbox_frame, bg='#2b2b2b', fg='#ffffff')
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.pokemon_listbox.yview)
        self.pokemon_listbox.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.pokemon_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.pokemon_listbox.bind('<<ListboxSelect>>', self.on_pokemon_select)
        
        # Navigation buttons
        nav_frame = ttk.Frame(selection_frame)
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(nav_frame, text="Previous", command=self.prev_pokemon).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="Next", command=self.next_pokemon).pack(side=tk.LEFT, padx=(5, 0))
        
        # Center panel - Pokemon data editor
        center_frame = ttk.Frame(paned)
        paned.add(center_frame, weight=2)
        
        # Pokemon info
        info_frame = ttk.LabelFrame(center_frame, text="Pokemon Data")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create scrollable frame
        canvas = tk.Canvas(info_frame, bg='#2b2b2b')
        scrollbar_v = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_v.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Pokemon name
        name_frame = ttk.Frame(scrollable_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="Name:", width=15).pack(side=tk.LEFT)
        ttk.Entry(name_frame, textvariable=self.pokemon_name_var, width=20).pack(side=tk.LEFT, padx=(5, 0))
        
        # Base stats
        stats_frame = ttk.LabelFrame(scrollable_frame, text="Base Stats")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # HP
        hp_frame = ttk.Frame(stats_frame)
        hp_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(hp_frame, text="HP:", width=15).pack(side=tk.LEFT)
        ttk.Scale(hp_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.hp_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(hp_frame, textvariable=self.hp_var, width=5).pack(side=tk.RIGHT)
        
        # Attack
        attack_frame = ttk.Frame(stats_frame)
        attack_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(attack_frame, text="Attack:", width=15).pack(side=tk.LEFT)
        ttk.Scale(attack_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.attack_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(attack_frame, textvariable=self.attack_var, width=5).pack(side=tk.RIGHT)
        
        # Defense
        defense_frame = ttk.Frame(stats_frame)
        defense_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(defense_frame, text="Defense:", width=15).pack(side=tk.LEFT)
        ttk.Scale(defense_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.defense_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(defense_frame, textvariable=self.defense_var, width=5).pack(side=tk.RIGHT)
        
        # Speed
        speed_frame = ttk.Frame(stats_frame)
        speed_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(speed_frame, text="Speed:", width=15).pack(side=tk.LEFT)
        ttk.Scale(speed_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.speed_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(speed_frame, textvariable=self.speed_var, width=5).pack(side=tk.RIGHT)
        
        # Special Attack
        sp_attack_frame = ttk.Frame(stats_frame)
        sp_attack_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(sp_attack_frame, text="Sp. Attack:", width=15).pack(side=tk.LEFT)
        ttk.Scale(sp_attack_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.sp_attack_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(sp_attack_frame, textvariable=self.sp_attack_var, width=5).pack(side=tk.RIGHT)
        
        # Special Defense
        sp_defense_frame = ttk.Frame(stats_frame)
        sp_defense_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(sp_defense_frame, text="Sp. Defense:", width=15).pack(side=tk.LEFT)
        ttk.Scale(sp_defense_frame, from_=1, to=255, orient=tk.HORIZONTAL, variable=self.sp_defense_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(sp_defense_frame, textvariable=self.sp_defense_var, width=5).pack(side=tk.RIGHT)
        
        # Types
        types_frame = ttk.LabelFrame(scrollable_frame, text="Types")
        types_frame.pack(fill=tk.X, padx=5, pady=5)
        
        type1_frame = ttk.Frame(types_frame)
        type1_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(type1_frame, text="Type 1:", width=15).pack(side=tk.LEFT)
        type1_combo = ttk.Combobox(type1_frame, textvariable=self.type1_var, width=15)
        type1_combo['values'] = self.get_pokemon_types()
        type1_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        type2_frame = ttk.Frame(types_frame)
        type2_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(type2_frame, text="Type 2:", width=15).pack(side=tk.LEFT)
        type2_combo = ttk.Combobox(type2_frame, textvariable=self.type2_var, width=15)
        type2_combo['values'] = self.get_pokemon_types()
        type2_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Other data
        other_frame = ttk.LabelFrame(scrollable_frame, text="Other Data")
        other_frame.pack(fill=tk.X, padx=5, pady=5)
        
        catch_rate_frame = ttk.Frame(other_frame)
        catch_rate_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(catch_rate_frame, text="Catch Rate:", width=15).pack(side=tk.LEFT)
        ttk.Scale(catch_rate_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.catch_rate_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(catch_rate_frame, textvariable=self.catch_rate_var, width=5).pack(side=tk.RIGHT)
        
        base_exp_frame = ttk.Frame(other_frame)
        base_exp_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(base_exp_frame, text="Base Exp:", width=15).pack(side=tk.LEFT)
        ttk.Scale(base_exp_frame, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.base_exp_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        ttk.Label(base_exp_frame, textvariable=self.base_exp_var, width=5).pack(side=tk.RIGHT)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="Save Changes", command=self.save_pokemon_data).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Reset", command=self.reset_pokemon_data).pack(side=tk.LEFT, padx=(5, 0))
        
        # Right panel - Sprite display
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        sprite_frame = ttk.LabelFrame(right_frame, text="Sprites")
        sprite_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Placeholder for sprite display
        self.sprite_label = ttk.Label(sprite_frame, text="Sprite will be\ndisplayed here", 
                                     background='#404040', foreground='white')
        self.sprite_label.pack(expand=True, padx=20, pady=20)
        
        # Sprite buttons
        sprite_button_frame = ttk.Frame(sprite_frame)
        sprite_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(sprite_button_frame, text="Import", state="disabled").pack(side=tk.LEFT)
        ttk.Button(sprite_button_frame, text="Export", state="disabled").pack(side=tk.LEFT, padx=(5, 0))
        
        # Initialize Pokemon list
        self.populate_pokemon_list()
    
    def get_pokemon_types(self) -> List[str]:
        """Get list of Pokemon types"""
        return [
            "Normal", "Fighting", "Flying", "Poison", "Ground", "Rock",
            "Bug", "Ghost", "Steel", "Fire", "Water", "Grass",
            "Electric", "Psychic", "Ice", "Dragon", "Dark"
        ]
    
    def populate_pokemon_list(self):
        """Populate the Pokemon list"""
        # Placeholder Pokemon names (in a real implementation, these would be loaded from ROM)
        pokemon_names = [
            "001 - Bulbasaur", "002 - Ivysaur", "003 - Venusaur",
            "004 - Charmander", "005 - Charmeleon", "006 - Charizard",
            "007 - Squirtle", "008 - Wartortle", "009 - Blastoise",
            "010 - Caterpie", "011 - Metapod", "012 - Butterfree"
        ]
        
        for name in pokemon_names:
            self.pokemon_listbox.insert(tk.END, name)
        
        # Select first Pokemon
        if pokemon_names:
            self.pokemon_listbox.selection_set(0)
            self.on_pokemon_select(None)
    
    def filter_pokemon_list(self, event=None):
        """Filter Pokemon list based on search"""
        search_term = self.search_var.get().lower()
        
        # Clear current list
        self.pokemon_listbox.delete(0, tk.END)
        
        # Repopulate with filtered results
        pokemon_names = [
            "001 - Bulbasaur", "002 - Ivysaur", "003 - Venusaur",
            "004 - Charmander", "005 - Charmeleon", "006 - Charizard",
            "007 - Squirtle", "008 - Wartortle", "009 - Blastoise",
            "010 - Caterpie", "011 - Metapod", "012 - Butterfree"
        ]
        
        for name in pokemon_names:
            if search_term in name.lower():
                self.pokemon_listbox.insert(tk.END, name)
    
    def on_pokemon_select(self, event):
        """Handle Pokemon selection"""
        selection = self.pokemon_listbox.curselection()
        if selection:
            index = selection[0]
            pokemon_name = self.pokemon_listbox.get(index)
            
            # Extract Pokemon ID from name
            try:
                pokemon_id = int(pokemon_name.split(' - ')[0])
                self.current_pokemon_id = pokemon_id
                self.load_pokemon_data(pokemon_id)
            except ValueError:
                pass
    
    def load_pokemon_data(self, pokemon_id: int):
        """Load Pokemon data from ROM"""
        # Placeholder implementation
        # In a real implementation, this would read from ROM using symbol addresses
        
        # Sample data for demonstration
        sample_data = {
            1: {"name": "Bulbasaur", "hp": 45, "attack": 49, "defense": 49, "speed": 45, "sp_attack": 65, "sp_defense": 65, "type1": "Grass", "type2": "Poison", "catch_rate": 45, "base_exp": 64},
            4: {"name": "Charmander", "hp": 39, "attack": 52, "defense": 43, "speed": 65, "sp_attack": 60, "sp_defense": 50, "type1": "Fire", "type2": "Fire", "catch_rate": 45, "base_exp": 62},
            7: {"name": "Squirtle", "hp": 44, "attack": 48, "defense": 65, "speed": 43, "sp_attack": 50, "sp_defense": 64, "type1": "Water", "type2": "Water", "catch_rate": 45, "base_exp": 63}
        }
        
        data = sample_data.get(pokemon_id, sample_data[1])  # Default to Bulbasaur
        
        # Update UI
        self.pokemon_name_var.set(data["name"])
        self.hp_var.set(data["hp"])
        self.attack_var.set(data["attack"])
        self.defense_var.set(data["defense"])
        self.speed_var.set(data["speed"])
        self.sp_attack_var.set(data["sp_attack"])
        self.sp_defense_var.set(data["sp_defense"])
        self.type1_var.set(data["type1"])
        self.type2_var.set(data["type2"])
        self.catch_rate_var.set(data["catch_rate"])
        self.base_exp_var.set(data["base_exp"])
    
    def save_pokemon_data(self):
        """Save Pokemon data to ROM"""
        if not self.rom_engine.is_loaded():
            messagebox.showerror("Error", "No ROM loaded")
            return
        
        # In a real implementation, this would write to ROM
        messagebox.showinfo("Save", f"Pokemon #{self.current_pokemon_id} data saved")
    
    def reset_pokemon_data(self):
        """Reset Pokemon data to original values"""
        self.load_pokemon_data(self.current_pokemon_id)
    
    def prev_pokemon(self):
        """Navigate to previous Pokemon"""
        current_selection = self.pokemon_listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            if current_index > 0:
                self.pokemon_listbox.selection_clear(0, tk.END)
                self.pokemon_listbox.selection_set(current_index - 1)
                self.pokemon_listbox.see(current_index - 1)
                self.on_pokemon_select(None)
    
    def next_pokemon(self):
        """Navigate to next Pokemon"""
        current_selection = self.pokemon_listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            if current_index < self.pokemon_listbox.size() - 1:
                self.pokemon_listbox.selection_clear(0, tk.END)
                self.pokemon_listbox.selection_set(current_index + 1)
                self.pokemon_listbox.see(current_index + 1)
                self.on_pokemon_select(None)
    
    def on_rom_loaded(self):
        """Called when ROM is loaded"""
        # Reload Pokemon data from ROM
        self.populate_pokemon_list()
    
    def on_rom_closed(self):
        """Called when ROM is closed"""
        self.pokemon_listbox.delete(0, tk.END)

