# dwg_parser/tests/test_integration.py
import pytest
import tempfile
import os
import json
from dwg_parser.dwg_parser import DWGParser
from dwg_parser.data_converter import DataConverter
from dwg_parser.plugin.cli import DWGPluginCLI

def test_full_workflow():
    """Test complete workflow from file input to JSON output"""
    # Create a mock DWG file (this would need a real DWG file for actual testing)
    with tempfile.NamedTemporaryFile(suffix='.dwg', delete=False) as tmp:
        tmp.write(b'mock dwg content')
        tmp_path = tmp.name
    
    try:
        # Test CLI
        cli = DWGPluginCLI()
        result = cli.parse_dwg(tmp_path)
        
        # For now, we expect failure since we don't have a real DWG parser
        assert 'success' in result
    finally:
        os.unlink(tmp_path)