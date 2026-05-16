"""Map Renderer for Fire Red"""

import struct
from PIL import Image, ImageTk
from typing import Tuple, Optional

class MapRenderer:
    """Renders Pokemon Fire Red maps"""

    MAP_BANKS_OFFSET = 0x3526A8
    MAP_LAYOUTS_OFFSET = 0x352764
    TILESET_HEADERS_OFFSET = 0x351F08

    def __init__(self, rom_data: bytes):
        self.rom_data = rom_data
        self.tile_cache = {}

    def read_pointer(self, offset: int) -> int:
        """Read GBA pointer"""
        if offset + 3 >= len(self.rom_data):
            return 0
        ptr = struct.unpack('<I', self.rom_data[offset:offset+4])[0]
        return (ptr - 0x08000000) if ptr >= 0x08000000 else 0

    def read_byte(self, offset: int) -> int:
        """Read byte"""
        return self.rom_data[offset] if offset < len(self.rom_data) else 0

    def read_short(self, offset: int) -> int:
        """Read 16-bit"""
        if offset + 1 >= len(self.rom_data):
            return 0
        return struct.unpack('<H', self.rom_data[offset:offset+2])[0]

    def read_int(self, offset: int) -> int:
        """Read 32-bit"""
        if offset + 3 >= len(self.rom_data):
            return 0
        return struct.unpack('<I', self.rom_data[offset:offset+4])[0]

    def get_map_banks(self):
        """Get map banks"""
        names = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City",
                 "Lavender Town", "Vermilion City", "Celadon City", "Fuchsia City",
                 "Cinnabar Island", "Indigo Plateau", "Saffron City"] + [f"Route {i}" for i in range(1, 26)]
        names += ["Dungeons", "Silph Co", "Pokemon League", "Seven Island", "Six Island", "Five Island", "Four Island"]
        return [f"Bank {i}: {names[i] if i < len(names) else 'Unknown'}" for i in range(43)]

    def get_maps_in_bank(self, bank: int):
        """Get maps in bank"""
        try:
            bank_ptr = self.read_pointer(self.MAP_BANKS_OFFSET + (bank * 4))
            if bank_ptr == 0:
                return []
            count = self.read_byte(bank_ptr)
            return [f"Map {i}" for i in range(count)]
        except:
            return []

    def load_map(self, bank: int, map_idx: int) -> dict:
        """Load map"""
        try:
            bank_ptr = self.read_pointer(self.MAP_BANKS_OFFSET + (bank * 4))
            if bank_ptr == 0:
                raise ValueError("Invalid bank")
            map_ptr = self.read_pointer(bank_ptr + 4 + (map_idx * 4))
            if map_ptr == 0:
                raise ValueError("Invalid map")
            
            layout_ptr = self.read_pointer(map_ptr)
            width = self.read_int(layout_ptr)
            height = self.read_int(layout_ptr + 4)
            map_data_ptr = self.read_pointer(layout_ptr + 0xC)
            
            blocks = []
            for y in range(height):
                row = []
                for x in range(width):
                    offset = map_data_ptr + ((y * width + x) * 2)
                    block_id = self.read_short(offset)
                    row.append(block_id)
                blocks.append(row)
            
            return {'width': width, 'height': height, 'blocks': blocks}
        except Exception as e:
            print(f"Error loading map: {e}")
            return None

    def render_map(self, map_data: dict) -> Optional[Image.Image]:
        """Render map to image"""
        if not map_data:
            return None
        
        try:
            width = map_data['width']
            height = map_data['height']
            
            img = Image.new('RGB', (width * 16, height * 16), color=(0, 0, 0))
            pixels = img.load()
            
            for y in range(height):
                for x in range(width):
                    for py in range(16):
                        for px in range(16):
                            color = (50 + (y % 4) * 50, 50 + (x % 4) * 50, 100)
                            pixels[x * 16 + px, y * 16 + py] = color
            
            return img
        except:
            return None
