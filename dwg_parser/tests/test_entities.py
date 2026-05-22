# dwg_parser/tests/test_entities.py
import pytest
from dwg_parser.entities.geometric import Point, Line, Circle, Arc, Polyline, Spline

def test_point_creation():
    point = Point(1.0, 2.0, 3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

def test_line_creation():
    start = Point(0.0, 0.0, 0.0)
    end = Point(1.0, 1.0, 0.0)
    line = Line(start, end)
    assert line.start == start
    assert line.end == end

def test_circle_creation():
    center = Point(0.0, 0.0, 0.0)
    circle = Circle(center, 5.0)
    assert circle.center == center
    assert circle.radius == 5.0