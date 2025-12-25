"""
Symbol Parser for Pokemon Fire Red Symbol Files

This module parses the pokefirered.sym file to provide symbol name to address mapping
for accurate ROM manipulation and asset location.
"""

import re
from typing import Dict, List, Tuple, Optional

class SymbolParser:
    """Parser for Pokemon Fire Red symbol files"""
    
    def __init__(self):
        self.symbols: Dict[str, int] = {}
        self.addresses: Dict[int, str] = {}
        self.loaded = False
    
    def load_symbol_file(self, file_path: str) -> bool:
        """
        Load symbols from a .sym file
        
        Args:
            file_path: Path to the symbol file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            self.symbols.clear()
            self.addresses.clear()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse symbol line format: ADDRESS TYPE SIZE NAME
                # Example: 02000000 g 00000000 gHeap
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        address_str = parts[0]
                        symbol_type = parts[1]
                        size_str = parts[2]
                        symbol_name = parts[3]
                        
                        # Convert address from hex string
                        address = int(address_str, 16)
                        
                        # Store symbol mapping
                        self.symbols[symbol_name] = address
                        self.addresses[address] = symbol_name
                        
                    except ValueError as e:
                        print(f"Warning: Invalid symbol on line {line_num}: {line} ({e})")
                        continue
            
            self.loaded = True
            print(f"Loaded {len(self.symbols)} symbols from {file_path}")
            return True
            
        except Exception as e:
            print(f"Error loading symbol file: {e}")
            return False
    
    def get_symbol_address(self, symbol_name: str) -> Optional[int]:
        """
        Get the address of a symbol
        
        Args:
            symbol_name: Name of the symbol
            
        Returns:
            Address or None if not found
        """
        return self.symbols.get(symbol_name)
    
    def get_symbol_name(self, address: int) -> Optional[str]:
        """
        Get the symbol name at an address
        
        Args:
            address: Memory address
            
        Returns:
            Symbol name or None if not found
        """
        return self.addresses.get(address)
    
    def get_symbols_by_pattern(self, pattern: str) -> List[Tuple[str, int]]:
        """
        Get symbols matching a pattern
        
        Args:
            pattern: Pattern to match (supports * and ? wildcards)
            
        Returns:
            List of (symbol_name, address) tuples
        """
        # Convert wildcard pattern to regex
        regex_pattern = pattern.replace('*', '.*').replace('?', '.')
        regex = re.compile(regex_pattern, re.IGNORECASE)
        
        matches = []
        for symbol_name, address in self.symbols.items():
            if regex.match(symbol_name):
                matches.append((symbol_name, address))
        
        return sorted(matches, key=lambda x: x[1])  # Sort by address
    
    def get_pokemon_data_symbols(self) -> List[Tuple[str, int]]:
        """Get symbols related to Pokemon data"""
        patterns = [
            'gBaseStats*',
            'gPokemon*',
            'gSpeciesNames*',
            'gMoveNames*',
            'gAbilityNames*',
            'gTypeNames*'
        ]
        
        all_matches = []
        for pattern in patterns:
            all_matches.extend(self.get_symbols_by_pattern(pattern))
        
        return all_matches
    
    def get_map_data_symbols(self) -> List[Tuple[str, int]]:
        """Get symbols related to map data"""
        patterns = [
            'gMapHeader*',
            'gMapGroup*',
            'gTileset*',
            'gMapEvents*'
        ]
        
        all_matches = []
        for pattern in patterns:
            all_matches.extend(self.get_symbols_by_pattern(pattern))
        
        return all_matches
    
    def get_sprite_symbols(self) -> List[Tuple[str, int]]:
        """Get symbols related to sprites"""
        patterns = [
            'gMonFrontPic*',
            'gMonBackPic*',
            'gMonPalette*',
            'gMonShinyPalette*',
            'gTrainerFrontPic*',
            'gTrainerPalette*'
        ]
        
        all_matches = []
        for pattern in patterns:
            all_matches.extend(self.get_symbols_by_pattern(pattern))
        
        return all_matches
    
    def get_script_symbols(self) -> List[Tuple[str, int]]:
        """Get symbols related to scripts and events"""
        patterns = [
            'gScript*',
            'gEvent*',
            'gText*',
            'gMovement*'
        ]
        
        all_matches = []
        for pattern in patterns:
            all_matches.extend(self.get_symbols_by_pattern(pattern))
        
        return all_matches
    
    def get_battle_symbols(self) -> List[Tuple[str, int]]:
        """Get symbols related to battle system"""
        patterns = [
            'gBattle*',
            'gMove*',
            'gAbility*',
            'gType*'
        ]
        
        all_matches = []
        for pattern in patterns:
            all_matches.extend(self.get_symbols_by_pattern(pattern))
        
        return all_matches
    
    def search_symbols(self, search_term: str) -> List[Tuple[str, int]]:
        """
        Search for symbols containing a term
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of (symbol_name, address) tuples
        """
        matches = []
        search_lower = search_term.lower()
        
        for symbol_name, address in self.symbols.items():
            if search_lower in symbol_name.lower():
                matches.append((symbol_name, address))
        
        return sorted(matches, key=lambda x: x[0])  # Sort by name
    
    def get_symbol_count(self) -> int:
        """Get total number of loaded symbols"""
        return len(self.symbols)
    
    def is_loaded(self) -> bool:
        """Check if symbols are loaded"""
        return self.loaded
    
    def get_address_range_symbols(self, start_addr: int, end_addr: int) -> List[Tuple[str, int]]:
        """
        Get symbols within an address range
        
        Args:
            start_addr: Start address (inclusive)
            end_addr: End address (inclusive)
            
        Returns:
            List of (symbol_name, address) tuples
        """
        matches = []
        
        for symbol_name, address in self.symbols.items():
            if start_addr <= address <= end_addr:
                matches.append((symbol_name, address))
        
        return sorted(matches, key=lambda x: x[1])  # Sort by address
    
    def export_symbols(self, file_path: str, filter_pattern: Optional[str] = None) -> bool:
        """
        Export symbols to a file
        
        Args:
            file_path: Output file path
            filter_pattern: Optional pattern to filter symbols
            
        Returns:
            True if exported successfully, False otherwise
        """
        try:
            symbols_to_export = self.symbols.items()
            
            if filter_pattern:
                filtered_symbols = self.get_symbols_by_pattern(filter_pattern)
                symbols_to_export = filtered_symbols
            
            with open(file_path, 'w') as f:
                f.write("# Pokemon Fire Red Symbol Export\n")
                f.write("# Format: ADDRESS SYMBOL_NAME\n\n")
                
                for symbol_name, address in sorted(symbols_to_export, key=lambda x: x[1]):
                    f.write(f"{address:08X} {symbol_name}\n")
            
            return True
            
        except Exception as e:
            print(f"Error exporting symbols: {e}")
            return False

