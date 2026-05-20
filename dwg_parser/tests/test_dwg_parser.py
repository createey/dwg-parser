# dwg_parser/tests/test_dwg_parser.py
import pytest
import tempfile
import os
from dwg_parser.dwg_parser import DWGParser

def test_dwg_parser_initialization():
    parser = DWGParser()
    assert parser is not None
    assert parser.bindings is not None

def test_dwg_parser_load_file():
    parser = DWGParser()
    # Create a temporary DWG file for testing
    with tempfile.NamedTemporaryFile(suffix='.dwg', delete=False) as tmp:
        tmp.write(b'test dwg content')
        tmp_path = tmp.name
    
    try:
        result = parser.load(tmp_path)
        assert result is True
        assert parser.file_loaded is True
    finally:
        os.unlink(tmp_path)