"""ROM Engine for Pokemon Fire Red"""

import os
from typing import Optional

class ROMEngine:
    """Handles Pokemon Fire Red ROM operations"""

    VALID_GAME_CODES = ['BPRE', 'BPGE']

    def __init__(self):
        self.rom_data: Optional[bytes] = None
        self.rom_path: Optional[str] = None
        self.modified = False

    def load_rom(self, file_path: str) -> bool:
        """Load a Pokemon Fire Red ROM file"""
        try:
            if not os.path.exists(file_path):
                print(f"Error: File not found: {file_path}")
                return False

            with open(file_path, 'rb') as f:
                self.rom_data = f.read()

            if not self.validate_fire_red():
                self.rom_data = None
                print("Error: Invalid Fire Red ROM")
                return False

            self.rom_path = file_path
            self.modified = False
            print(f"✓ ROM loaded: {os.path.basename(file_path)}")
            return True
        except Exception as e:
            print(f"Error loading ROM: {e}")
            return False

    def validate_fire_red(self) -> bool:
        """Validate ROM is Pokemon Fire Red"""
        try:
            if not self.rom_data or len(self.rom_data) < 0xB0:
                return False
            game_code = self.rom_data[0xAC:0xB0].decode('ascii', errors='ignore')
            return game_code in self.VALID_GAME_CODES
        except:
            return False

    def get_rom_data(self) -> Optional[bytes]:
        """Get raw ROM data"""
        return self.rom_data

    def is_loaded(self) -> bool:
        """Check if ROM is loaded"""
        return self.rom_data is not None

    def has_unsaved_changes(self) -> bool:
        """Check for unsaved changes"""
        return self.modified if self.is_loaded() else False

    def save_rom(self) -> bool:
        """Save ROM"""
        if not self.is_loaded() or not self.rom_path:
            return False
        try:
            backup_path = f"{self.rom_path}.bak"
            if not os.path.exists(backup_path):
                with open(self.rom_path, 'rb') as f:
                    with open(backup_path, 'wb') as bf:
                        bf.write(f.read())
            with open(self.rom_path, 'wb') as f:
                f.write(self.rom_data)
            self.modified = False
            print(f"✓ ROM saved")
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def save_rom_as(self, file_path: str) -> bool:
        """Save ROM as new file"""
        if not self.is_loaded() or not self.rom_data:
            return False
        try:
            with open(file_path, 'wb') as f:
                f.write(self.rom_data)
            self.rom_path = file_path
            self.modified = False
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def read_byte(self, offset: int) -> int:
        """Read byte"""
        return self.rom_data[offset] if self.rom_data and offset < len(self.rom_data) else 0

    def get_rom_name(self) -> str:
        """Get ROM name"""
        return os.path.basename(self.rom_path) if self.rom_path else "No ROM"

    def get_rom_size_mb(self) -> float:
        """Get ROM size in MB"""
        return len(self.rom_data) / 1024 / 1024 if self.rom_data else 0.0
