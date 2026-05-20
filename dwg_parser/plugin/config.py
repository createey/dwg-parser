# dwg_parser/plugin/config.py
import json
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DWGPluginConfig:
    """Configuration for DWG parser plugin"""
    output_format: str = "json"
    pretty_print: bool = True
    include_layers: bool = True
    include_blocks: bool = True
    
    @classmethod
    def from_file(cls, config_path: str) -> 'DWGPluginConfig':
        """Load configuration from file"""
        if not os.path.exists(config_path):
            return cls()
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def save(self, config_path: str):
        """Save configuration to file"""
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)