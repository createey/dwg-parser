# dwg_parser/dwg_parser.py
from typing import Optional, List, Dict, Any
from .libredwg_bindings import LibreDWGBindings

class DWGParser:
    """Main DWG parser class"""
    
    def __init__(self):
        self.bindings = LibreDWGBindings()
        self.file_loaded = False
        self.dwg_data = None
        
    def load(self, file_path: str) -> bool:
        """Load a DWG file"""
        try:
            if not self.bindings.initialized:
                self.bindings.load_library()
            
            self.dwg_data = self.bindings.read_file(file_path)
            self.file_loaded = True
            return True
        except Exception as e:
            print(f"Failed to load DWG file: {e}")
            return False
    
    def get_entities(self) -> List[Dict[str, Any]]:
        """Get all entities from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        return self.bindings.get_entities(self.dwg_data)
    
    def get_layers(self) -> List[Dict[str, Any]]:
        """Get all layers from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        return self.bindings.get_layers(self.dwg_data)
    
    def get_blocks(self) -> List[Dict[str, Any]]:
        """Get all block references from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        # This will be implemented in the next task
        raise NotImplementedError