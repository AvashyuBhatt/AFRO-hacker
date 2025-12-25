"""
Hex Editor functionality for Pokemon Fire Red Binary Hacking Tool

This module provides hex editing capabilities including viewing, editing,
searching, and navigation through ROM data.
"""

from typing import Optional, List, Tuple, Callable
import re

class HexEditor:
    """Hex editor for ROM data manipulation"""
    
    def __init__(self, rom_engine):
        self.rom_engine = rom_engine
        self.current_offset = 0
        self.bytes_per_row = 16
        self.selection_start = None
        self.selection_end = None
        self.search_results = []
        self.current_search_index = 0
        
    def get_hex_view(self, offset: int, num_rows: int = 16) -> List[str]:
        """
        Get hex view of ROM data
        
        Args:
            offset: Starting offset
            num_rows: Number of rows to display
            
        Returns:
            List of formatted hex strings
        """
        if not self.rom_engine.is_loaded():
            return []
        
        lines = []
        bytes_per_row = self.bytes_per_row
        
        for row in range(num_rows):
            row_offset = offset + (row * bytes_per_row)
            
            # Check if we're past the end of ROM
            if row_offset >= self.rom_engine.get_rom_size():
                break
            
            # Read bytes for this row
            row_data = self.rom_engine.read_bytes(row_offset, bytes_per_row)
            if not row_data:
                break
            
            # Format address
            addr_str = f"{row_offset:08X}"
            
            # Format hex bytes
            hex_bytes = []
            ascii_chars = []
            
            for i, byte in enumerate(row_data):
                hex_bytes.append(f"{byte:02X}")
                
                # ASCII representation
                if 32 <= byte <= 126:
                    ascii_chars.append(chr(byte))
                else:
                    ascii_chars.append('.')
            
            # Pad if row is incomplete
            while len(hex_bytes) < bytes_per_row:
                hex_bytes.append("  ")
                ascii_chars.append(" ")
            
            # Group hex bytes
            hex_groups = []
            for i in range(0, len(hex_bytes), 4):
                hex_groups.append(" ".join(hex_bytes[i:i+4]))
            
            hex_str = "  ".join(hex_groups)
            ascii_str = "".join(ascii_chars)
            
            line = f"{addr_str}  {hex_str}  |{ascii_str}|"
            lines.append(line)
        
        return lines
    
    def goto_offset(self, offset: int) -> bool:
        """
        Navigate to a specific offset
        
        Args:
            offset: Target offset
            
        Returns:
            True if valid offset, False otherwise
        """
        if not self.rom_engine.is_loaded():
            return False
        
        if 0 <= offset < self.rom_engine.get_rom_size():
            self.current_offset = offset
            return True
        
        return False
    
    def goto_symbol(self, symbol_name: str) -> bool:
        """
        Navigate to a symbol address
        
        Args:
            symbol_name: Name of the symbol
            
        Returns:
            True if symbol found, False otherwise
        """
        address = self.rom_engine.get_symbol_address(symbol_name)
        if address is not None:
            return self.goto_offset(address)
        return False
    
    def search_bytes(self, pattern: bytes, start_offset: int = 0) -> List[int]:
        """
        Search for byte pattern in ROM
        
        Args:
            pattern: Bytes to search for
            start_offset: Starting offset for search
            
        Returns:
            List of offsets where pattern was found
        """
        if not self.rom_engine.is_loaded() or not pattern:
            return []
        
        results = []
        rom_size = self.rom_engine.get_rom_size()
        
        # Search in chunks to avoid memory issues
        chunk_size = 1024 * 1024  # 1MB chunks
        pattern_len = len(pattern)
        
        for chunk_start in range(start_offset, rom_size, chunk_size):
            chunk_end = min(chunk_start + chunk_size + pattern_len - 1, rom_size)
            chunk_data = self.rom_engine.read_bytes(chunk_start, chunk_end - chunk_start)
            
            if not chunk_data:
                continue
            
            # Search within chunk
            pos = 0
            while True:
                pos = chunk_data.find(pattern, pos)
                if pos == -1:
                    break
                
                absolute_pos = chunk_start + pos
                results.append(absolute_pos)
                pos += 1
        
        self.search_results = results
        self.current_search_index = 0
        return results
    
    def search_hex_string(self, hex_string: str, start_offset: int = 0) -> List[int]:
        """
        Search for hex string pattern
        
        Args:
            hex_string: Hex string (e.g., "48656C6C6F" for "Hello")
            start_offset: Starting offset for search
            
        Returns:
            List of offsets where pattern was found
        """
        try:
            # Remove spaces and convert to bytes
            hex_clean = re.sub(r'[^0-9A-Fa-f]', '', hex_string)
            if len(hex_clean) % 2 != 0:
                return []
            
            pattern = bytes.fromhex(hex_clean)
            return self.search_bytes(pattern, start_offset)
            
        except ValueError:
            return []
    
    def search_text(self, text: str, encoding: str = 'ascii', start_offset: int = 0) -> List[int]:
        """
        Search for text string
        
        Args:
            text: Text to search for
            encoding: Text encoding
            start_offset: Starting offset for search
            
        Returns:
            List of offsets where text was found
        """
        try:
            pattern = text.encode(encoding, errors='ignore')
            return self.search_bytes(pattern, start_offset)
        except Exception:
            return []
    
    def goto_next_search_result(self) -> bool:
        """Navigate to next search result"""
        if not self.search_results:
            return False
        
        if self.current_search_index < len(self.search_results) - 1:
            self.current_search_index += 1
        else:
            self.current_search_index = 0
        
        offset = self.search_results[self.current_search_index]
        return self.goto_offset(offset)
    
    def goto_previous_search_result(self) -> bool:
        """Navigate to previous search result"""
        if not self.search_results:
            return False
        
        if self.current_search_index > 0:
            self.current_search_index -= 1
        else:
            self.current_search_index = len(self.search_results) - 1
        
        offset = self.search_results[self.current_search_index]
        return self.goto_offset(offset)
    
    def set_selection(self, start_offset: int, end_offset: int):
        """Set selection range"""
        self.selection_start = min(start_offset, end_offset)
        self.selection_end = max(start_offset, end_offset)
    
    def clear_selection(self):
        """Clear current selection"""
        self.selection_start = None
        self.selection_end = None
    
    def get_selected_bytes(self) -> Optional[bytes]:
        """Get bytes in current selection"""
        if self.selection_start is None or self.selection_end is None:
            return None
        
        length = self.selection_end - self.selection_start + 1
        return self.rom_engine.read_bytes(self.selection_start, length)
    
    def write_selected_bytes(self, data: bytes) -> bool:
        """Write bytes to current selection"""
        if self.selection_start is None:
            return False
        
        return self.rom_engine.write_bytes(self.selection_start, data)
    
    def copy_selection(self) -> Optional[bytes]:
        """Copy selected bytes to clipboard (returns bytes for now)"""
        return self.get_selected_bytes()
    
    def paste_bytes(self, data: bytes, offset: Optional[int] = None) -> bool:
        """
        Paste bytes at offset or current position
        
        Args:
            data: Bytes to paste
            offset: Target offset (uses current offset if None)
            
        Returns:
            True if successful, False otherwise
        """
        target_offset = offset if offset is not None else self.current_offset
        return self.rom_engine.write_bytes(target_offset, data)
    
    def fill_bytes(self, start_offset: int, length: int, value: int) -> bool:
        """
        Fill range with specified byte value
        
        Args:
            start_offset: Starting offset
            length: Number of bytes to fill
            value: Byte value (0-255)
            
        Returns:
            True if successful, False otherwise
        """
        if not (0 <= value <= 255):
            return False
        
        data = bytes([value] * length)
        return self.rom_engine.write_bytes(start_offset, data)
    
    def get_offset_info(self, offset: int) -> dict:
        """
        Get information about an offset
        
        Args:
            offset: Target offset
            
        Returns:
            Dictionary with offset information
        """
        info = {
            'offset': offset,
            'hex_offset': f"{offset:08X}",
            'valid': False,
            'byte_value': None,
            'symbol': None
        }
        
        if not self.rom_engine.is_loaded():
            return info
        
        if 0 <= offset < self.rom_engine.get_rom_size():
            info['valid'] = True
            info['byte_value'] = self.rom_engine.read_uint8(offset)
            
            # Check for symbol at this address
            symbol = self.rom_engine.symbol_parser.get_symbol_name(offset) if self.rom_engine.symbol_parser else None
            if symbol:
                info['symbol'] = symbol
        
        return info
    
    def export_range(self, start_offset: int, end_offset: int, file_path: str) -> bool:
        """
        Export byte range to file
        
        Args:
            start_offset: Starting offset
            end_offset: Ending offset
            file_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            length = end_offset - start_offset + 1
            data = self.rom_engine.read_bytes(start_offset, length)
            
            if not data:
                return False
            
            with open(file_path, 'wb') as f:
                f.write(data)
            
            return True
            
        except Exception as e:
            print(f"Error exporting range: {e}")
            return False
    
    def import_range(self, start_offset: int, file_path: str) -> bool:
        """
        Import bytes from file to ROM
        
        Args:
            start_offset: Target offset in ROM
            file_path: Input file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            return self.rom_engine.write_bytes(start_offset, data)
            
        except Exception as e:
            print(f"Error importing range: {e}")
            return False

