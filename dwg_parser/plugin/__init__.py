# dwg_parser/plugin/__init__.py
"""OpenCode plugin for DWG parsing"""
from .cli import DWGPluginCLI
from .config import DWGPluginConfig

__all__ = ['DWGPluginCLI', 'DWGPluginConfig']