# dwg_parser/tests/test_plugin.py
import pytest
from dwg_parser.plugin.cli import DWGPluginCLI

def test_cli_initialization():
    cli = DWGPluginCLI()
    assert cli is not None
    assert cli.parser is not None

def test_cli_parse_command():
    cli = DWGPluginCLI()
    # Test that parse command exists and is callable
    assert hasattr(cli, 'parse_dwg')
    assert callable(cli.parse_dwg)