"""Hex Editor Tab"""

import tkinter as tk
from tkinter import ttk

class HexEditorTab:
    def __init__(self, parent, rom_engine):
        self.parent = parent
        self.rom_engine = rom_engine
        label = ttk.Label(self.parent, text="Hex Editor - Coming Soon", font=('Arial', 14, 'bold'))
        label.pack(padx=20, pady=20)
