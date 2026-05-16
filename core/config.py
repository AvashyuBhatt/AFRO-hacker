"""Configuration Manager"""

import json, os
from pathlib import Path
from typing import Any, Optional

class Config:
    """Manages application configuration"""

    DEFAULTS = {
        'window': {'width': 1400, 'height': 900, 'x': None, 'y': None},
        'map_editor': {'show_grid': True, 'zoom_level': 1.0},
        'recent_files': [],
        'theme': 'dark',
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self.get_default_path()
        self.config = self.DEFAULTS.copy()
        self.load_config()

    @staticmethod
    def get_default_path() -> str:
        """Get default config path"""
        config_dir = Path.home() / '.afro_hacker'
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / 'config.json')

    def load_config(self):
        """Load config"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
        except:
            pass

    def save_config(self):
        """Save config"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        """Get value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set value"""
        self.config[key] = value
        self.save_config()

    def reset(self):
        """Reset to defaults"""
        self.config = self.DEFAULTS.copy()
        self.save_config()
