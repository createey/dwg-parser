# dwg_parser/tests/test_libredwg_bindings.py
import pytest
from dwg_parser.libredwg_bindings import LibreDWGBindings

def test_libredwg_initialization():
    bindings = LibreDWGBindings()
    assert bindings is not None
    assert bindings.initialized is False

def test_libredwg_load_library():
    bindings = LibreDWGBindings()
    result = bindings.load_library()
    assert result is True
    assert bindings.initialized is True