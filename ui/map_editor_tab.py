"""Map Editor Tab"""

import tkinter as tk
from tkinter import ttk, Canvas
from PIL import Image, ImageTk
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.map_renderer import MapRenderer

class MapEditorTab:
    """Map editor"""

    def __init__(self, parent, rom_engine):
        self.parent = parent
        self.rom_engine = rom_engine
        self.map_renderer = None
        self.current_map_data = None
        self.current_bank = 0
        self.current_map = 0
        self.zoom_level = 1.0
        self.show_grid = True
        self.setup_ui()

    def setup_ui(self):
        """Create UI"""
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_frame.columnconfigure(0, weight=0, minsize=250)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=0, minsize=250)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=0)

        self.create_toolbar()
        self.create_left_panel()
        self.create_map_canvas()
        self.create_right_panel()
        self.create_status_bar()

    def create_toolbar(self):
        """Toolbar"""
        toolbar = ttk.Frame(self.main_frame, relief=tk.RAISED, borderwidth=1)
        toolbar.grid(row=0, column=0, columnspan=3, sticky='ew', padx=2, pady=2)

        ttk.Label(toolbar, text="Zoom:").pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔍+", width=5, command=lambda: self.change_zoom(0.25)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🔍-", width=5, command=lambda: self.change_zoom(-0.25)).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="100%", width=5, command=self.reset_zoom).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        self.grid_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Grid", variable=self.grid_var, command=self.toggle_grid).pack(side=tk.LEFT, padx=5)

    def create_left_panel(self):
        """Left panel"""
        left_frame = ttk.LabelFrame(self.main_frame, text="Map Selection", padding=10)
        left_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        ttk.Label(left_frame, text="Map Bank:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        self.bank_combo = ttk.Combobox(left_frame, state='readonly', width=30)
        self.bank_combo.pack(fill=tk.X, pady=(0, 10))
        self.bank_combo.bind('<<ComboboxSelected>>', self.on_bank_selected)

        ttk.Label(left_frame, text="Maps:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.map_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, bg='#2b2b2b', fg='white', height=20)
        self.map_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.map_listbox.yview)
        self.map_listbox.bind('<<ListboxSelect>>', self.on_map_selected)

    def create_map_canvas(self):
        """Map canvas"""
        canvas_frame = ttk.Frame(self.main_frame)
        canvas_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.map_canvas = Canvas(canvas_frame, bg='#1a1a1a', xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        self.map_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        h_scrollbar.config(command=self.map_canvas.xview)
        v_scrollbar.config(command=self.map_canvas.yview)

    def create_right_panel(self):
        """Right panel"""
        right_frame = ttk.Frame(self.main_frame)
        right_frame.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        props_frame = ttk.Frame(notebook, padding=10)
        notebook.add(props_frame, text="Properties")
        ttk.Label(props_frame, text="Map Properties", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 10))
        self.width_label = ttk.Label(props_frame, text="Width: -")
        self.width_label.pack(anchor='w', pady=2)
        self.height_label = ttk.Label(props_frame, text="Height: -")
        self.height_label.pack(anchor='w', pady=2)

    def create_status_bar(self):
        """Status bar"""
        status_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=1)
        status_frame.grid(row=2, column=0, columnspan=3, sticky='ew')
        self.status_label = ttk.Label(status_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def on_rom_loaded(self):
        """ROM loaded"""
        rom_data = self.rom_engine.get_rom_data()
        if not rom_data:
            return

        self.map_renderer = MapRenderer(rom_data)
        bank_names = self.map_renderer.get_map_banks()
        self.bank_combo['values'] = bank_names
        if bank_names:
            self.bank_combo.current(0)
            self.load_maps_for_bank(0)

    def on_bank_selected(self, event):
        """Bank selected"""
        if self.bank_combo.current() >= 0:
            self.current_bank = self.bank_combo.current()
            self.load_maps_for_bank(self.current_bank)

    def load_maps_for_bank(self, bank: int):
        """Load maps"""
        if not self.map_renderer:
            return
        self.map_listbox.delete(0, tk.END)
        maps = self.map_renderer.get_maps_in_bank(bank)
        for m in maps:
            self.map_listbox.insert(tk.END, m)
        if maps:
            self.map_listbox.selection_set(0)
            self.load_map(bank, 0)

    def on_map_selected(self, event):
        """Map selected"""
        sel = self.map_listbox.curselection()
        if sel:
            self.current_map = sel[0]
            self.load_map(self.current_bank, self.current_map)

    def load_map(self, bank: int, map_idx: int):
        """Load map"""
        if not self.map_renderer:
            return
        try:
            self.current_map_data = self.map_renderer.load_map(bank, map_idx)
            if self.current_map_data:
                self.width_label.config(text=f"Width: {self.current_map_data['width']}")
                self.height_label.config(text=f"Height: {self.current_map_data['height']}")
                self.render_current_map()
                self.status_label.config(text=f"Loaded: Bank {bank}, Map {map_idx}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def render_current_map(self):
        """Render map"""
        if not self.current_map_data or not self.map_renderer:
            return
        try:
            pil_image = self.map_renderer.render_map(self.current_map_data)
            if pil_image and self.zoom_level != 1.0:
                new_w = int(pil_image.width * self.zoom_level)
                new_h = int(pil_image.height * self.zoom_level)
                pil_image = pil_image.resize((new_w, new_h), Image.NEAREST)
            if pil_image:
                self.map_photo = ImageTk.PhotoImage(pil_image)
                self.map_canvas.delete('all')
                self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)
                self.map_canvas.config(scrollregion=self.map_canvas.bbox('all'))
        except Exception as e:
            self.status_label.config(text=f"Render error: {str(e)}")

    def change_zoom(self, delta):
        """Change zoom"""
        self.zoom_level = max(0.25, min(4.0, self.zoom_level + delta))
        self.render_current_map()

    def reset_zoom(self):
        """Reset zoom"""
        self.zoom_level = 1.0
        self.render_current_map()

    def toggle_grid(self):
        """Toggle grid"""
        self.show_grid = self.grid_var.get()
