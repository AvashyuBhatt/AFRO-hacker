"""
ROM Engine for Pokemon Fire Red Binary Hacking Tool

This module handles all ROM file operations including loading, saving, validation,
and binary data manipulation for Pokemon Fire Red ROM files.
"""

import os
import struct
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from .symbol_parser import SymbolParser

class ROMEngine:
    """Core engine for ROM file manipulation"""
    
    # Pokemon Fire Red ROM validation constants
    FIRE_RED_TITLE = b"POKEMON FIRE"
    FIRE_RED_GAME_CODE = b"BPRE"  # English Fire Red
    EXPECTED_ROM_SIZE = 16 * 1024 * 1024  # 16MB
    
    def __init__(self):
        self.rom_data: Optional[bytearray] = None
        self.rom_path: Optional[str] = None
        self.rom_info: Dict[str, Any] = {}
        self.symbol_parser: Optional[SymbolParser] = None
        self.unsaved_changes = False
        self.backup_data: Optional[bytes] = None
        
    def load_rom(self, file_path: str) -> bool:
        """
        Load a Pokemon Fire Red ROM file
        
        Args:
            file_path: Path to the ROM file
            
        Returns:
            True if ROM loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"ROM file not found: {file_path}")
            
            with open(file_path, 'rb') as f:
                rom_data = f.read()
            
            # Validate ROM
            if not self._validate_rom(rom_data):
                return False
            
            # Create backup
            self.backup_data = rom_data
            
            # Load ROM data
            self.rom_data = bytearray(rom_data)
            self.rom_path = file_path
            self.unsaved_changes = False
            
            # Parse ROM header
            self._parse_rom_header()
            
            # Load symbol file
            self._load_symbol_file()
            
            return True
            
        except Exception as e:
            print(f"Error loading ROM: {e}")
            return False
    
    def save_rom(self) -> bool:
        """
        Save the current ROM to its original file
        
        Returns:
            True if saved successfully, False otherwise
        """
        if not self.rom_path:
            return False
        
        return self.save_rom_as(self.rom_path)
    
    def save_rom_as(self, file_path: str) -> bool:
        """
        Save the ROM to a specified file
        
        Args:
            file_path: Path to save the ROM
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if not self.rom_data:
                return False
            
            # Create backup of original file if it exists
            if os.path.exists(file_path):
                backup_path = file_path + ".backup"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(file_path, backup_path)
            
            # Write ROM data
            with open(file_path, 'wb') as f:
                f.write(self.rom_data)
            
            self.rom_path = file_path
            self.unsaved_changes = False
            
            return True
            
        except Exception as e:
            print(f"Error saving ROM: {e}")
            return False
    
    def read_bytes(self, offset: int, length: int) -> Optional[bytes]:
        """
        Read bytes from ROM at specified offset
        
        Args:
            offset: Byte offset in ROM
            length: Number of bytes to read
            
        Returns:
            Bytes data or None if error
        """
        try:
            if not self.rom_data or offset < 0 or offset + length > len(self.rom_data):
                return None
            
            return bytes(self.rom_data[offset:offset + length])
            
        except Exception:
            return None
    
    def write_bytes(self, offset: int, data: bytes) -> bool:
        """
        Write bytes to ROM at specified offset
        
        Args:
            offset: Byte offset in ROM
            data: Bytes to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.rom_data or offset < 0 or offset + len(data) > len(self.rom_data):
                return False
            
            self.rom_data[offset:offset + len(data)] = data
            self.unsaved_changes = True
            
            return True
            
        except Exception:
            return False
    
    def read_uint8(self, offset: int) -> Optional[int]:
        """Read unsigned 8-bit integer from ROM"""
        data = self.read_bytes(offset, 1)
        return struct.unpack('<B', data)[0] if data else None
    
    def read_uint16(self, offset: int) -> Optional[int]:
        """Read unsigned 16-bit integer from ROM (little-endian)"""
        data = self.read_bytes(offset, 2)
        return struct.unpack('<H', data)[0] if data else None
    
    def read_uint32(self, offset: int) -> Optional[int]:
        """Read unsigned 32-bit integer from ROM (little-endian)"""
        data = self.read_bytes(offset, 4)
        return struct.unpack('<L', data)[0] if data else None
    
    def write_uint8(self, offset: int, value: int) -> bool:
        """Write unsigned 8-bit integer to ROM"""
        return self.write_bytes(offset, struct.pack('<B', value))
    
    def write_uint16(self, offset: int, value: int) -> bool:
        """Write unsigned 16-bit integer to ROM (little-endian)"""
        return self.write_bytes(offset, struct.pack('<H', value))
    
    def write_uint32(self, offset: int, value: int) -> bool:
        """Write unsigned 32-bit integer to ROM (little-endian)"""
        return self.write_bytes(offset, struct.pack('<L', value))
    
    def read_string(self, offset: int, length: int, encoding: str = 'ascii') -> Optional[str]:
        """
        Read string from ROM
        
        Args:
            offset: Byte offset in ROM
            length: Maximum length to read
            encoding: String encoding (default: ascii)
            
        Returns:
            String or None if error
        """
        try:
            data = self.read_bytes(offset, length)
            if not data:
                return None
            
            # Find null terminator
            null_pos = data.find(b'\x00')
            if null_pos >= 0:
                data = data[:null_pos]
            
            return data.decode(encoding, errors='ignore')
            
        except Exception:
            return None
    
    def write_string(self, offset: int, text: str, max_length: int, encoding: str = 'ascii') -> bool:
        """
        Write string to ROM
        
        Args:
            offset: Byte offset in ROM
            text: String to write
            max_length: Maximum length including null terminator
            encoding: String encoding (default: ascii)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encode string
            encoded = text.encode(encoding, errors='ignore')
            
            # Truncate if too long
            if len(encoded) >= max_length:
                encoded = encoded[:max_length - 1]
            
            # Add null terminator and pad
            data = encoded + b'\x00' * (max_length - len(encoded))
            
            return self.write_bytes(offset, data)
            
        except Exception:
            return False
    
    def get_symbol_address(self, symbol_name: str) -> Optional[int]:
        """
        Get address of a symbol from the symbol file
        
        Args:
            symbol_name: Name of the symbol to look up
            
        Returns:
            Address or None if not found
        """
        if self.symbol_parser:
            return self.symbol_parser.get_symbol_address(symbol_name)
        return None
    
    def get_symbols_by_pattern(self, pattern: str) -> List[Tuple[str, int]]:
        """
        Get symbols matching a pattern
        
        Args:
            pattern: Pattern to match (supports wildcards)
            
        Returns:
            List of (symbol_name, address) tuples
        """
        if self.symbol_parser:
            return self.symbol_parser.get_symbols_by_pattern(pattern)
        return []
    
    def is_loaded(self) -> bool:
        """Check if a ROM is currently loaded"""
        return self.rom_data is not None
    
    def has_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes"""
        return self.unsaved_changes
    
    def get_rom_info(self) -> Dict[str, Any]:
        """Get ROM information"""
        return self.rom_info.copy()
    
    def get_rom_size(self) -> int:
        """Get ROM size in bytes"""
        return len(self.rom_data) if self.rom_data else 0
    
    def calculate_checksum(self) -> str:
        """Calculate MD5 checksum of ROM data"""
        if not self.rom_data:
            return ""
        return hashlib.md5(self.rom_data).hexdigest()
    
    def restore_backup(self) -> bool:
        """Restore ROM from backup"""
        if self.backup_data:
            self.rom_data = bytearray(self.backup_data)
            self.unsaved_changes = True
            return True
        return False
    
    def _validate_rom(self, rom_data: bytes) -> bool:
        """
        Validate that the ROM is a Pokemon Fire Red ROM
        
        Args:
            rom_data: ROM file data
            
        Returns:
            True if valid Pokemon Fire Red ROM, False otherwise
        """
        try:
            # Check minimum size
            if len(rom_data) < 0x200:
                return False
            
            # Check game title (offset 0xA0)
            title = rom_data[0xA0:0xAC]
            if not title.startswith(self.FIRE_RED_TITLE):
                return False
            
            # Check game code (offset 0xAC)
            game_code = rom_data[0xAC:0xB0]
            if game_code != self.FIRE_RED_GAME_CODE:
                return False
            
            # Check header checksum
            header_checksum = rom_data[0xBD]
            calculated_checksum = self._calculate_header_checksum(rom_data)
            if header_checksum != calculated_checksum:
                print(f"Warning: Header checksum mismatch (expected {calculated_checksum:02X}, got {header_checksum:02X})")
            
            return True
            
        except Exception as e:
            print(f"ROM validation error: {e}")
            return False
    
    def _calculate_header_checksum(self, rom_data: bytes) -> int:
        """Calculate GBA header checksum"""
        checksum = 0
        for i in range(0xA0, 0xBD):
            checksum = (checksum - rom_data[i]) & 0xFF
        return (checksum - 0x19) & 0xFF
    
    def _parse_rom_header(self):
        """Parse ROM header information"""
        if not self.rom_data:
            return
        
        try:
            self.rom_info = {
                'title': self.read_string(0xA0, 12).strip(),
                'game_code': self.read_string(0xAC, 4),
                'maker_code': self.read_string(0xB0, 2),
                'version': self.read_uint8(0xBC),
                'header_checksum': self.read_uint8(0xBD),
                'file_size': len(self.rom_data),
                'checksum': self.calculate_checksum()
            }
        except Exception as e:
            print(f"Error parsing ROM header: {e}")
    
    def _load_symbol_file(self):
        """Load the Pokemon Fire Red symbol file"""
        try:
            # Look for symbol file in assets directory
            symbol_path = Path(__file__).parent.parent.parent / "assets" / "pokefirered.sym"
            
            if symbol_path.exists():
                self.symbol_parser = SymbolParser()
                self.symbol_parser.load_symbol_file(str(symbol_path))
            else:
                print("Warning: Symbol file not found")
                
        except Exception as e:
            print(f"Error loading symbol file: {e}")

