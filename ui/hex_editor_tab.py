"""
Hex Editor Tab for Pokemon Fire Red Binary Hacking Tool

This module implements the hex editor interface tab.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.hex_editor import HexEditor

class HexEditorTab:
    """Hex editor tab implementation"""
    
    def __init__(self, parent, rom_engine):
        self.parent = parent
        self.rom_engine = rom_engine
        self.hex_editor = HexEditor(rom_engine)
        
        self.frame = ttk.Frame(parent)
        self.hex_text = None
        self.offset_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the hex editor UI"""
        # Create main paned window
        paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Navigation and tools
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Navigation frame
        nav_frame = ttk.LabelFrame(left_frame, text="Navigation")
        nav_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Offset entry
        ttk.Label(nav_frame, text="Offset:").pack(anchor=tk.W)
        offset_frame = ttk.Frame(nav_frame)
        offset_frame.pack(fill=tk.X, pady=2)
        
        offset_entry = ttk.Entry(offset_frame, textvariable=self.offset_var, width=12)
        offset_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        offset_entry.bind('<Return>', self.goto_offset)
        
        ttk.Button(offset_frame, text="Go", command=self.goto_offset).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Symbol navigation
        ttk.Label(nav_frame, text="Symbol:").pack(anchor=tk.W, pady=(10, 0))
        symbol_frame = ttk.Frame(nav_frame)
        symbol_frame.pack(fill=tk.X, pady=2)
        
        self.symbol_var = tk.StringVar()
        symbol_entry = ttk.Entry(symbol_frame, textvariable=self.symbol_var)
        symbol_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        symbol_entry.bind('<Return>', self.goto_symbol)
        
        ttk.Button(symbol_frame, text="Go", command=self.goto_symbol).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Search frame
        search_frame = ttk.LabelFrame(left_frame, text="Search")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Search type
        self.search_type_var = tk.StringVar(value="hex")
        search_type_frame = ttk.Frame(search_frame)
        search_type_frame.pack(fill=tk.X, pady=2)
        
        ttk.Radiobutton(search_type_frame, text="Hex", variable=self.search_type_var, 
                       value="hex").pack(side=tk.LEFT)
        ttk.Radiobutton(search_type_frame, text="Text", variable=self.search_type_var, 
                       value="text").pack(side=tk.LEFT, padx=(10, 0))
        
        # Search entry
        search_entry_frame = ttk.Frame(search_frame)
        search_entry_frame.pack(fill=tk.X, pady=2)
        
        search_entry = ttk.Entry(search_entry_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind('<Return>', self.perform_search)
        
        ttk.Button(search_entry_frame, text="Search", command=self.perform_search).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Search results
        results_frame = ttk.Frame(search_frame)
        results_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(results_frame, text="◀", command=self.prev_result).pack(side=tk.LEFT)
        ttk.Button(results_frame, text="▶", command=self.next_result).pack(side=tk.LEFT, padx=(2, 0))
        
        self.results_label = ttk.Label(results_frame, text="No results")
        self.results_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Tools frame
        tools_frame = ttk.LabelFrame(left_frame, text="Tools")
        tools_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(tools_frame, text="Export Range", command=self.export_range).pack(fill=tk.X, pady=1)
        ttk.Button(tools_frame, text="Import Range", command=self.import_range).pack(fill=tk.X, pady=1)
        ttk.Button(tools_frame, text="Fill Range", command=self.fill_range).pack(fill=tk.X, pady=1)
        
        # Right panel - Hex display
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)
        
        # Hex display
        hex_frame = ttk.LabelFrame(right_frame, text="Hex View")
        hex_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(hex_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.hex_text = tk.Text(text_frame, font=('Courier', 10), wrap=tk.NONE,
                               bg='#2b2b2b', fg='#ffffff', insertbackground='white')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.hex_text.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.hex_text.xview)
        
        self.hex_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars and text
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.hex_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.hex_text.bind('<Button-1>', self.on_hex_click)
        self.hex_text.bind('<KeyPress>', self.on_key_press)
    
    def on_rom_loaded(self):
        """Called when ROM is loaded"""
        self.refresh_hex_view()
    
    def on_rom_closed(self):
        """Called when ROM is closed"""
        self.hex_text.delete(1.0, tk.END)
    
    def refresh_hex_view(self):
        """Refresh the hex view display"""
        if not self.rom_engine.is_loaded():
            return
        
        # Get hex lines
        lines = self.hex_editor.get_hex_view(self.hex_editor.current_offset, 32)
        
        # Update text widget
        self.hex_text.delete(1.0, tk.END)
        for line in lines:
            self.hex_text.insert(tk.END, line + '\n')
        
        # Update offset display
        self.offset_var.set(f"{self.hex_editor.current_offset:08X}")
    
    def goto_offset(self, event=None):
        """Navigate to specified offset"""
        try:
            offset_str = self.offset_var.get().strip()
            if offset_str.startswith('0x') or offset_str.startswith('0X'):
                offset = int(offset_str, 16)
            else:
                offset = int(offset_str, 16)
            
            if self.hex_editor.goto_offset(offset):
                self.refresh_hex_view()
            else:
                messagebox.showerror("Error", "Invalid offset")
        except ValueError:
            messagebox.showerror("Error", "Invalid offset format")
    
    def goto_symbol(self, event=None):
        """Navigate to symbol address"""
        symbol_name = self.symbol_var.get().strip()
        if not symbol_name:
            return
        
        if self.hex_editor.goto_symbol(symbol_name):
            self.refresh_hex_view()
        else:
            messagebox.showerror("Error", f"Symbol '{symbol_name}' not found")
    
    def perform_search(self, event=None):
        """Perform search operation"""
        search_term = self.search_var.get().strip()
        if not search_term:
            return
        
        search_type = self.search_type_var.get()
        
        try:
            if search_type == "hex":
                results = self.hex_editor.search_hex_string(search_term)
            else:
                results = self.hex_editor.search_text(search_term)
            
            if results:
                self.results_label.config(text=f"{len(results)} results")
                # Go to first result
                self.hex_editor.goto_offset(results[0])
                self.refresh_hex_view()
            else:
                self.results_label.config(text="No results")
                messagebox.showinfo("Search", "No matches found")
        
        except Exception as e:
            messagebox.showerror("Search Error", str(e))
    
    def next_result(self):
        """Go to next search result"""
        if self.hex_editor.goto_next_search_result():
            self.refresh_hex_view()
    
    def prev_result(self):
        """Go to previous search result"""
        if self.hex_editor.goto_previous_search_result():
            self.refresh_hex_view()
    
    def export_range(self):
        """Export byte range to file"""
        # Simple implementation - export current view
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Range",
                filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
            )
            
            if file_path:
                start_offset = self.hex_editor.current_offset
                end_offset = start_offset + 512  # Export 512 bytes
                
                if self.hex_editor.export_range(start_offset, end_offset, file_path):
                    messagebox.showinfo("Success", "Range exported successfully")
                else:
                    messagebox.showerror("Error", "Failed to export range")
        
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def import_range(self):
        """Import bytes from file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Import Range",
                filetypes=[("Binary files", "*.bin"), ("All files", "*.*")]
            )
            
            if file_path:
                offset = self.hex_editor.current_offset
                
                if self.hex_editor.import_range(offset, file_path):
                    self.refresh_hex_view()
                    messagebox.showinfo("Success", "Range imported successfully")
                else:
                    messagebox.showerror("Error", "Failed to import range")
        
        except Exception as e:
            messagebox.showerror("Import Error", str(e))
    
    def fill_range(self):
        """Fill range with specified value"""
        # Simple dialog for fill operation
        dialog = tk.Toplevel(self.frame)
        dialog.title("Fill Range")
        dialog.geometry("300x150")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Start Offset:").pack(pady=5)
        start_var = tk.StringVar(value=f"{self.hex_editor.current_offset:08X}")
        ttk.Entry(dialog, textvariable=start_var).pack(pady=2)
        
        ttk.Label(dialog, text="Length:").pack(pady=5)
        length_var = tk.StringVar(value="16")
        ttk.Entry(dialog, textvariable=length_var).pack(pady=2)
        
        ttk.Label(dialog, text="Fill Value (hex):").pack(pady=5)
        value_var = tk.StringVar(value="00")
        ttk.Entry(dialog, textvariable=value_var).pack(pady=2)
        
        def do_fill():
            try:
                start = int(start_var.get(), 16)
                length = int(length_var.get())
                value = int(value_var.get(), 16)
                
                if self.hex_editor.fill_bytes(start, length, value):
                    self.refresh_hex_view()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Range filled successfully")
                else:
                    messagebox.showerror("Error", "Failed to fill range")
            except ValueError:
                messagebox.showerror("Error", "Invalid input values")
        
        ttk.Button(dialog, text="Fill", command=do_fill).pack(pady=10)
    
    def on_hex_click(self, event):
        """Handle click on hex display"""
        # Get cursor position and calculate offset
        # This is a simplified implementation
        pass
    
    def on_key_press(self, event):
        """Handle key press in hex display"""
        # Implement hex editing functionality
        # This is a simplified implementation
        return "break"  # Prevent default text widget behavior
    
    def set_bytes_per_row(self, bytes_per_row):
        """Set bytes per row for hex display"""
        self.hex_editor.bytes_per_row = bytes_per_row
        self.refresh_hex_view()
    
    def search(self, search_term):
        """Search interface for main window"""
        self.search_var.set(search_term)
        self.perform_search()

