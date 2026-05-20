# dwg_parser/plugin/cli.py
import argparse
import json
import sys
from typing import List, Optional
from ..dwg_parser import DWGParser
from ..data_converter import DataConverter
from .config import DWGPluginConfig

class DWGPluginCLI:
    """Command-line interface for DWG parser plugin"""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="DWG Parser Plugin for OpenCode"
        )
        self.setup_arguments()
        self.config = DWGPluginConfig()
    
    def setup_arguments(self):
        """Setup command-line arguments"""
        subparsers = self.parser.add_subparsers(
            dest='command', help='Available commands'
        )
        
        # parse-dwg command
        parse_parser = subparsers.add_parser(
            'parse-dwg', help='Parse a DWG file'
        )
        parse_parser.add_argument(
            'file_path', help='Path to DWG file'
        )
        parse_parser.add_argument(
            '--output', '-o', help='Output file path'
        )
        
        # batch-parse command
        batch_parser = subparsers.add_parser(
            'batch-parse', help='Parse multiple DWG files'
        )
        batch_parser.add_argument(
            'directory', help='Directory containing DWG files'
        )
        batch_parser.add_argument(
            '--pattern', '-p', default='*.dwg',
            help='File pattern (default: *.dwg)'
        )
        
        # dwg-info command
        info_parser = subparsers.add_parser(
            'dwg-info', help='Get DWG file information'
        )
        info_parser.add_argument(
            'file_path', help='Path to DWG file'
        )
    
    def parse_dwg(self, file_path: str, output: Optional[str] = None) -> dict:
        """Parse a single DWG file"""
        dwg_parser = DWGParser()
        converter = DataConverter()
        
        if not dwg_parser.load(file_path):
            return {"success": False, "error": "Failed to load DWG file"}
        
        try:
            entities = dwg_parser.get_entities()
            converted_entities = converter.convert_entities(entities)
            
            result = {
                "success": True,
                "file": file_path,
                "entities": [
                    {
                        "type": type(e).__name__,
                        "properties": e.__dict__
                    }
                    for e in converted_entities
                ]
            }
            
            if output:
                with open(output, 'w') as f:
                    json.dump(result, f, indent=2)
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self, args: Optional[List[str]] = None):
        """Run the CLI"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        if parsed_args.command == 'parse-dwg':
            result = self.parse_dwg(parsed_args.file_path, parsed_args.output)
            print(json.dumps(result, indent=2))
        elif parsed_args.command == 'batch-parse':
            # Batch processing will be implemented later
            print("Batch processing not yet implemented")
        elif parsed_args.command == 'dwg-info':
            # Info command will be implemented later
            print("Info command not yet implemented")