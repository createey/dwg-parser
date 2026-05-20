# dwg_parser/entities/geometric.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Point:
    """3D point"""
    x: float
    y: float
    z: float = 0.0

@dataclass
class Line:
    """Line entity"""
    start: Point
    end: Point
    layer: str = ""
    handle: int = 0

@dataclass
class Circle:
    """Circle entity"""
    center: Point
    radius: float
    layer: str = ""
    handle: int = 0

@dataclass
class Arc:
    """Arc entity"""
    center: Point
    radius: float
    start_angle: float
    end_angle: float
    layer: str = ""
    handle: int = 0

@dataclass
class Polyline:
    """Polyline entity"""
    vertices: List[Point]
    closed: bool = False
    layer: str = ""
    handle: int = 0

@dataclass
class Spline:
    """Spline entity"""
    control_points: List[Point]
    knots: List[float]
    degree: int = 3
    layer: str = ""
    handle: int = 0