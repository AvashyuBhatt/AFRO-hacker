"""
Configuration management for the Pokemon Fire Red Binary Hacking Tool
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for application settings"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".pokemon_fire_red_hacker"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "ui": {
                "theme": "dark",
                "window_width": 1400,
                "window_height": 900,
                "remember_window_size": True,
                "auto_save_interval": 300  # seconds
            },
            "rom": {
                "backup_on_save": True,
                "validate_on_load": True,
                "max_recent_files": 10
            },
            "features": {
                "roaming_pokemon": {
                    "default_behavior": "aggressive",
                    "default_speed": 50,
                    "default_chase_range": 5
                },
                "alpha_pokemon": {
                    "default_size_multiplier": 2.0,
                    "default_level_boost": 20,
                    "default_glow_effect": "red_eyes"
                },
                "quest_system": {
                    "auto_generate_ids": True,
                    "default_reward_type": "items"
                }
            },
            "paths": {
                "last_rom_directory": "",
                "symbol_file_path": "",
                "assets_directory": ""
            }
        }
        self._config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
                # Merge with defaults to ensure all keys exist
                self._config = self._merge_configs(self.default_config, self._config)
            else:
                self._config = self.default_config.copy()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self._config = self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'ui.theme')"""
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self._config
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        self.save_config()
    
    def get_recent_files(self) -> list:
        """Get list of recent ROM files"""
        return self.get("recent_files", [])
    
    def add_recent_file(self, file_path: str):
        """Add a file to the recent files list"""
        recent_files = self.get_recent_files()
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning
        recent_files.insert(0, file_path)
        
        # Limit to max recent files
        max_files = self.get("rom.max_recent_files", 10)
        recent_files = recent_files[:max_files]
        
        self.set("recent_files", recent_files)
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with default config"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result

