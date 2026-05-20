# dwg_parser/entities/__init__.py
"""Entity data structures for DWG parsing"""
from .geometric import Point, Line, Circle, Arc, Polyline, Spline
from .text import Text, MText, Dimension
from .blocks import Block, Attribute, Insert

__all__ = [
    'Point', 'Line', 'Circle', 'Arc', 'Polyline', 'Spline',
    'Text', 'MText', 'Dimension',
    'Block', 'Attribute', 'Insert'
]