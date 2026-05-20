# dwg_parser/entities/blocks.py
from dataclasses import dataclass
from typing import List, Dict, Any
from .geometric import Point

@dataclass
class Block:
    """Block definition"""
    name: str
    base_point: Point
    entities: List[Any] = None
    handle: int = 0
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []

@dataclass
class Attribute:
    """Block attribute"""
    tag: str
    value: str
    position: Point
    layer: str = ""
    handle: int = 0

@dataclass
class Insert:
    """Block insert"""
    block_name: str
    insertion_point: Point
    scale: Point = None
    rotation: float = 0.0
    attributes: List[Attribute] = None
    layer: str = ""
    handle: int = 0
    
    def __post_init__(self):
        if self.scale is None:
            self.scale = Point(1.0, 1.0, 1.0)
        if self.attributes is None:
            self.attributes = []