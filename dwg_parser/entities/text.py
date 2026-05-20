# dwg_parser/entities/text.py
from dataclasses import dataclass
from typing import Optional
from .geometric import Point

@dataclass
class Text:
    """Text entity"""
    content: str
    position: Point
    height: float = 1.0
    rotation: float = 0.0
    layer: str = ""
    handle: int = 0

@dataclass
class MText:
    """MText (formatted text) entity"""
    content: str
    position: Point
    width: float = 0.0
    height: float = 1.0
    layer: str = ""
    handle: int = 0

@dataclass
class Dimension:
    """Dimension entity"""
    type: str
    definition_point: Point
    text_position: Point
    text: str = ""
    layer: str = ""
    handle: int = 0